#!/usr/bin/env python3
r"""Write-ahead run log for unattended agent runs.

Owns two files that sit side by side in the project being worked on:

  RUN_LOG.md     the human log — a summary header, then prose the agent writes
  RUN_LOG.jsonl  the machine journal — append-only, fsynced, authoritative

The markdown is what a person reads and what a resuming run reads to find out
where it got to; it is the artifact that makes a restart nearly free. The JSONL
is what `status --json` and the watchdog read, so that no tool has to parse
prose to answer "is this run alive".

Why both, rather than one: the markdown gets rewritten (the header carries a
`Last cycle:` line), and a rewrite can be interrupted. The JSONL is only ever
appended to and fsynced, so the record of what happened survives a crash even
if the markdown is caught mid-write. A truncated final JSONL line is expected
rather than exceptional — that is the shape a killed process leaves — and is
skipped on read.

Usage:

  runlog.py init   --budget-hours 8 --max-dispatches 9 [--max-cycles 48]
  runlog.py begin  "build the merge core"
  runlog.py end    --status done "landed, suite green at 166"
  runlog.py note   "blocked on a decision, see Blocked section"
  runlog.py spend  --dispatches 3
  runlog.py stop   --reason completed "items 4-6 done"
  runlog.py status [--json] [--stale-after 1200]

`begin` before the work and `end` after, sharing a sequence number: an entry
with a begin and no end names exactly the unit that was in flight when the run
died. In flight is not the same as failed — the work may have completed with
the process dying before the outcome was recorded — so a resuming run
reconciles that one item rather than redoing it.

Standard library only, Python 3.9+, no configuration. Every command is safe to
run twice.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional

DEFAULT_LOG = "RUN_LOG.md"
HEADER_BEGIN = "<!-- runlog:begin -->"
HEADER_END = "<!-- runlog:end -->"

STOP_REASONS = ("completed", "budget", "blocked", "environment", "no-progress", "other")
END_STATUSES = ("done", "blocked", "noop", "failed")


# --------------------------------------------------------------------------
# time


def _now() -> _dt.datetime:
    return _dt.datetime.now(_dt.timezone.utc)


def _iso(t: _dt.datetime) -> str:
    return t.replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _parse(ts: str) -> Optional[_dt.datetime]:
    try:
        return _dt.datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        return None


# --------------------------------------------------------------------------
# the journal


def _journal_path(log: Path) -> Path:
    return log.with_suffix(".jsonl")


def _read_records(log: Path) -> List[Dict[str, Any]]:
    """Every complete record. A ragged final line is skipped, not fatal."""
    path = _journal_path(log)
    if not path.exists():
        return []
    out: List[Dict[str, Any]] = []
    with path.open("r", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue  # truncated tail, or a line someone hand-edited badly
            if isinstance(rec, dict):
                out.append(rec)
    return out


def _ends_with_newline(path: Path) -> bool:
    with path.open("rb") as fh:
        fh.seek(-1, os.SEEK_END)
        return fh.read(1) == b"\n"


def _append_record(log: Path, rec: Dict[str, Any]) -> None:
    """Append one record, flushed and fsynced.

    A journal buffered inside a process that then dies records nothing about
    the cycle that mattered most. The cost is trivial against the work a cycle
    does.
    """
    path = _journal_path(log)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as fh:
        # If a previous process died mid-append the file ends without a
        # newline. Appending straight onto that would fuse the ragged tail to
        # this record and lose both; a leading newline costs one byte and
        # keeps the damage to the line that was already lost.
        if path.stat().st_size and not _ends_with_newline(path):
            fh.write("\n")
        fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
        fh.flush()
        os.fsync(fh.fileno())


def _next_seq(records: List[Dict[str, Any]]) -> int:
    return max((int(r.get("seq", 0)) for r in records), default=0) + 1


def _config(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    """The most recent init record's settings, or empty."""
    for rec in reversed(records):
        if rec.get("type") == "init":
            return rec
    return {}


# --------------------------------------------------------------------------
# the markdown


def _atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=".runlog-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text)
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp, path)
    except BaseException:
        # KeyboardInterrupt is not an Exception, and Ctrl-C during a run is
        # ordinary. Don't leave the temp file behind either way.
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def _render_header(log: Path, records: List[Dict[str, Any]]) -> str:
    st = _status(log, records)
    lines = [
        HEADER_BEGIN,
        "",
        "| | |",
        "|---|---|",
        f"| **Started** | {st['started'] or 'not started'} |",
        f"| **Last entry** | {st['last_entry_ts'] or 'none'}"
        + (f" ({_ago(st['last_entry_age_s'])} ago)" if st["last_entry_age_s"] is not None else "")
        + " |",
        f"| **Cycles** | {st['cycles_used']}"
        + (f" of {st['max_cycles']}" if st["max_cycles"] else "")
        + " |",
        f"| **Dispatches** | {st['dispatches_used']}"
        + (f" of {st['max_dispatches']}" if st["max_dispatches"] else "")
        + " |",
    ]
    if st["seconds_remaining"] is not None:
        lines.append(f"| **Budget left** | {_ago(max(0, st['seconds_remaining']))} |")
    if st["in_flight"]:
        flight = "; ".join(f"#{e['seq']} {e['intent']}" for e in st["in_flight"])
        lines.append(f"| **In flight** | {flight} |")
    if st["stopped"]:
        lines.append(f"| **Stopped** | {st['stop_reason']} — {st['stop_detail']} |")
    lines += ["", HEADER_END]
    return "\n".join(lines)


def _ago(seconds: Optional[float]) -> str:
    if seconds is None:
        return "?"
    seconds = int(seconds)
    if seconds < 90:
        return f"{seconds}s"
    if seconds < 5400:
        return f"{seconds // 60}m"
    return f"{seconds // 3600}h{(seconds % 3600) // 60:02d}m"


def _refresh_header(log: Path, records: List[Dict[str, Any]]) -> None:
    """Rewrite the header block in place, leaving the body untouched."""
    header = _render_header(log, records)
    if log.exists():
        text = log.read_text(encoding="utf-8", errors="replace")
    else:
        text = ""
    if HEADER_BEGIN in text and HEADER_END in text:
        pre, rest = text.split(HEADER_BEGIN, 1)
        _, post = rest.split(HEADER_END, 1)
        text = pre + header + post
    else:
        title = f"# Run log\n\n"
        text = title + header + "\n\n" + text.lstrip("\n")
    _atomic_write(log, text)


def _append_body(log: Path, line: str) -> None:
    text = log.read_text(encoding="utf-8", errors="replace") if log.exists() else ""
    if not text.endswith("\n"):
        text += "\n"
    _atomic_write(log, text + line + "\n")


# --------------------------------------------------------------------------
# status


def _status(log: Path, records: Optional[List[Dict[str, Any]]] = None,
            stale_after: int = 1200) -> Dict[str, Any]:
    records = _read_records(log) if records is None else records
    cfg = _config(records)
    now = _now()

    started = cfg.get("ts")
    started_dt = _parse(started) if started else None

    # Liveness means the *run* did something. The watchdog's own notes are
    # bookkeeping, and counting them would let a failed restart reset the
    # staleness clock and push its own retry out by a whole interval.
    live = [r for r in records if r.get("source", "agent") == "agent"]
    last = live[-1]["ts"] if live else None
    last_dt = _parse(last) if last else None
    age = (now - last_dt).total_seconds() if last_dt else None

    cycles = sum(1 for r in records if r.get("type") == "begin")
    dispatches = sum(int(r.get("dispatches", 0)) for r in records if r.get("type") == "spend")

    ended = {int(r["seq_ref"]) for r in records if r.get("type") == "end" and "seq_ref" in r}
    in_flight = [
        {"seq": int(r["seq"]), "intent": r.get("intent", ""), "ts": r.get("ts")}
        for r in records
        if r.get("type") == "begin" and int(r.get("seq", -1)) not in ended
    ]

    stop = next((r for r in reversed(records) if r.get("type") == "stop"), None)

    budget_s = cfg.get("budget_seconds")
    elapsed = (now - started_dt).total_seconds() if started_dt else None
    remaining = (budget_s - elapsed) if (budget_s and elapsed is not None) else None

    max_cycles = cfg.get("max_cycles")
    max_dispatches = cfg.get("max_dispatches")

    blocked: Optional[str] = None
    if not records:
        blocked = "no run log — nothing to resume"
    elif stop is not None:
        blocked = f"run stopped ({stop.get('reason')})"
    elif remaining is not None and remaining <= 0:
        blocked = "wall-clock budget exhausted"
    elif max_cycles and cycles >= int(max_cycles):
        blocked = "cycle budget exhausted"
    elif max_dispatches and dispatches >= int(max_dispatches):
        blocked = "dispatch budget exhausted"
    elif age is not None and age < stale_after:
        blocked = f"last entry {_ago(age)} ago, under the {_ago(stale_after)} staleness threshold"

    return {
        "log": str(log),
        "now": _iso(now),
        "started": started,
        "last_entry_ts": last,
        "last_entry_age_s": None if age is None else int(age),
        "cycles_used": cycles,
        "max_cycles": max_cycles,
        "dispatches_used": dispatches,
        "max_dispatches": max_dispatches,
        "elapsed_s": None if elapsed is None else int(elapsed),
        "budget_seconds": budget_s,
        "seconds_remaining": None if remaining is None else int(remaining),
        "in_flight": in_flight,
        "stopped": stop is not None,
        "stop_reason": stop.get("reason") if stop else None,
        "stop_detail": stop.get("detail") if stop else None,
        "should_resume": blocked is None,
        "resume_blocked_by": blocked,
    }


# --------------------------------------------------------------------------
# commands


def cmd_init(args: argparse.Namespace) -> int:
    log = Path(args.log)
    records = _read_records(log)
    if records:
        # Resuming is the common case; truncating a run log on restart is the
        # worst available failure, so init never overwrites.
        print(f"{log} already has {len(records)} entries - resuming, not reinitializing.")
        _refresh_header(log, records)
        return 0

    rec: Dict[str, Any] = {
        "seq": 1,
        "ts": _iso(_now()),
        "type": "init",
        "brief": args.brief,
    }
    if args.budget_hours:
        rec["budget_seconds"] = int(args.budget_hours * 3600)
    if args.max_cycles:
        rec["max_cycles"] = args.max_cycles
    if args.max_dispatches:
        rec["max_dispatches"] = args.max_dispatches
    _append_record(log, rec)

    records = _read_records(log)
    _refresh_header(log, records)  # writes the title too, when there is no file yet
    _append_body(log, "\n## Cycles\n")
    print(f"initialized {log} and {_journal_path(log).name}")
    return 0


def cmd_begin(args: argparse.Namespace) -> int:
    log = Path(args.log)
    records = _read_records(log)
    seq = _next_seq(records)
    ts = _iso(_now())
    _append_record(log, {"seq": seq, "ts": ts, "type": "begin", "intent": args.intent})
    _append_body(log, f"\n### {ts} — #{seq} {args.intent}\n")
    _refresh_header(log, _read_records(log))
    print(seq)
    return 0


def cmd_end(args: argparse.Namespace) -> int:
    log = Path(args.log)
    records = _read_records(log)
    if args.seq:
        ref = args.seq
    else:
        ended = {int(r["seq_ref"]) for r in records if r.get("type") == "end" and "seq_ref" in r}
        open_begins = [int(r["seq"]) for r in records
                       if r.get("type") == "begin" and int(r["seq"]) not in ended]
        if not open_begins:
            print("no entry in flight - nothing to end (was `begin` called?)", file=sys.stderr)
            return 2
        ref = open_begins[-1]
    ts = _iso(_now())
    _append_record(log, {
        "seq": _next_seq(records), "ts": ts, "type": "end",
        "seq_ref": ref, "status": args.status, "outcome": args.outcome,
    })
    _append_body(log, f"\n**{ts} — #{ref} {args.status}.** {args.outcome}\n")
    _refresh_header(log, _read_records(log))
    return 0


def cmd_note(args: argparse.Namespace) -> int:
    log = Path(args.log)
    records = _read_records(log)
    ts = _iso(_now())
    source = getattr(args, "source", None) or "agent"
    _append_record(log, {"seq": _next_seq(records), "ts": ts, "type": "note",
                         "text": args.text, "source": source})
    _append_body(log, f"\n_{ts}_ — {args.text}\n")
    _refresh_header(log, _read_records(log))
    return 0


def cmd_spend(args: argparse.Namespace) -> int:
    log = Path(args.log)
    records = _read_records(log)
    ts = _iso(_now())
    _append_record(log, {
        "seq": _next_seq(records), "ts": ts, "type": "spend",
        "dispatches": args.dispatches, "note": args.note,
    })
    st = _status(log)
    detail = f" ({st['dispatches_used']} of {st['max_dispatches']} used)" if st["max_dispatches"] else ""
    _append_body(log, f"\n_{ts}_ — spent {args.dispatches} review dispatch(es){detail}. {args.note or ''}".rstrip() + "\n")
    _refresh_header(log, _read_records(log))
    return 0


def cmd_stop(args: argparse.Namespace) -> int:
    log = Path(args.log)
    records = _read_records(log)
    ts = _iso(_now())
    _append_record(log, {
        "seq": _next_seq(records), "ts": ts, "type": "stop",
        "reason": args.reason, "detail": args.detail,
    })
    _append_body(log, f"\n**{ts} — STOPPED ({args.reason}).** {args.detail}\n")
    _refresh_header(log, _read_records(log))
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    st = _status(Path(args.log), stale_after=args.stale_after)
    if args.json:
        print(json.dumps(st, indent=2))
        return 0
    print(f"log            {st['log']}")
    print(f"started        {st['started']}")
    print(f"last entry     {st['last_entry_ts']}  ({_ago(st['last_entry_age_s'])} ago)")
    print(f"cycles         {st['cycles_used']}" + (f" of {st['max_cycles']}" if st["max_cycles"] else ""))
    print(f"dispatches     {st['dispatches_used']}" + (f" of {st['max_dispatches']}" if st["max_dispatches"] else ""))
    if st["seconds_remaining"] is not None:
        print(f"budget left    {_ago(max(0, st['seconds_remaining']))}")
    for e in st["in_flight"]:
        print(f"in flight      #{e['seq']} {e['intent']}  (since {e['ts']})")
    if st["stopped"]:
        print(f"stopped        {st['stop_reason']} - {st['stop_detail']}")
    print(f"resume         {'yes' if st['should_resume'] else 'no'}"
          + ("" if st["should_resume"] else f"  ({st['resume_blocked_by']})"))
    return 0


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--log", default=DEFAULT_LOG, help=f"markdown log path (default {DEFAULT_LOG})")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("init", help="create the log, or resume an existing one")
    p.add_argument("--budget-hours", type=float, default=None)
    p.add_argument("--max-cycles", type=int, default=None)
    p.add_argument("--max-dispatches", type=int, default=None,
                   help="the scarce unit: review-team subagent dispatches")
    p.add_argument("--brief", default=None, help="path to the run brief")
    p.set_defaults(func=cmd_init)

    p = sub.add_parser("begin", help="record intent BEFORE doing the work")
    p.add_argument("intent")
    p.set_defaults(func=cmd_begin)

    p = sub.add_parser("end", help="record the outcome after the work")
    p.add_argument("outcome")
    p.add_argument("--status", choices=END_STATUSES, default="done")
    p.add_argument("--seq", type=int, default=None, help="defaults to the newest in-flight entry")
    p.set_defaults(func=cmd_end)

    p = sub.add_parser("note", help="timestamped free-form append")
    p.add_argument("text")
    p.add_argument("--source", default="agent",
                   help='who wrote it; anything other than "agent" does not count as liveness')
    p.set_defaults(func=cmd_note)

    p = sub.add_parser("spend", help="record consumption of the scarce resource")
    p.add_argument("--dispatches", type=int, required=True)
    p.add_argument("--note", default=None)
    p.set_defaults(func=cmd_spend)

    p = sub.add_parser("stop", help="record a terminal state")
    p.add_argument("detail")
    p.add_argument("--reason", choices=STOP_REASONS, required=True)
    p.set_defaults(func=cmd_stop)

    p = sub.add_parser("status", help="machine-readable run state")
    p.add_argument("--json", action="store_true")
    p.add_argument("--stale-after", type=int, default=1200,
                   help="seconds since the last entry before a run counts as stale")
    p.set_defaults(func=cmd_status)

    args = ap.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
