#!/usr/bin/env python3
r"""Restart a stalled unattended agent run.

The problem this exists for: every scheduling mechanism inside a Claude Code
session dies with that session. `ScheduleWakeup` (the self-pacing form of
`/loop`) is documented as session-scoped, and the fixed-interval form runs on
an in-memory cron whose own documentation says jobs "live only in this Claude
session". So an overnight run that hits a usage limit does not pause — it
stops, and nothing brings it back. That is exactly what happened on
2026-08-30: one cycle completed, a wakeup was scheduled, and nine hours passed.

The fix has to live outside Claude Code, which also makes it the one that works
on every plan. The OS scheduler runs this script every N minutes; it reads the
run log, and if the run has gone quiet without recording a stop, it starts a
fresh headless session pointed at the log.

    watchdog.py --project PATH [--log RUN_LOG.md] [--stale-after 1200]
                [--resume-prompt .agent-crew/resume-prompt.md]
                [--max-budget-usd 15] [--notify-cmd "..."]
                [--dry-run]

What it deliberately does not do:

* It does not grant immunity to usage limits. If the resume attempt fails
  because the account is rate-limited, the attempt is recorded and the next
  firing tries again. The property being bought is automatic recovery, not
  immunity, and describing it as anything more is how people end up trusting
  it more than they should.
* It does not resume a session by id. A fresh `claude -p` reading the log has
  no dependence on a session that may have died in an unclean state, and it
  exercises the resume protocol on every recovery rather than only in the
  emergency. `--resume-session` is available for the case where the session is
  known-alive and merely idle.
* It does not decide when a run is finished. Only the run does that, by
  recording a stop; the watchdog reads that and goes quiet.

A healthy self-paced run makes this script a no-op on every firing. That is
the intended steady state.

Standard library only, Python 3.9+.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

sys.path.insert(0, str(Path(__file__).resolve().parent))
import runlog  # noqa: E402  (same directory, deliberately)

DEFAULT_RESUME_PROMPT = """Read RUN_LOG.md, then continue the run it describes.

If an entry is in flight (a `begin` with no `end`), reconcile that one item first — in flight is not the same as failed. Then do one unit of work, record it with scripts/runlog.py, and stop."""


def _now() -> _dt.datetime:
    return _dt.datetime.now(_dt.timezone.utc)


# --------------------------------------------------------------------------
# lock


class Lock:
    """Single-holder lock so two firings cannot start two runs.

    Created with O_EXCL so acquisition is atomic. A lock older than
    `stale_seconds` is broken: the alternative is a crashed run that can never
    be restarted, which is the failure this whole script exists to prevent.
    """

    def __init__(self, path: Path, stale_seconds: int = 3 * 3600):
        self.path = path
        self.stale_seconds = stale_seconds
        self.held = False

    def acquire(self) -> bool:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        try:
            fd = os.open(str(self.path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        except FileExistsError:
            age = time.time() - self.path.stat().st_mtime
            if age < self.stale_seconds:
                return False
            try:
                self.path.unlink()
            except OSError:
                return False
            return self.acquire()
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump({"pid": os.getpid(), "since": runlog._iso(_now())}, fh)
        self.held = True
        return True

    def release(self) -> None:
        if self.held:
            try:
                self.path.unlink()
            except OSError:
                pass
            self.held = False


# --------------------------------------------------------------------------


def _resolve_claude(explicit: Optional[str]) -> Optional[str]:
    if explicit:
        return explicit
    return shutil.which("claude")


def _read_prompt(project: Path, path_arg: Optional[str]) -> str:
    if path_arg:
        return Path(path_arg).read_text(encoding="utf-8").strip()
    default = project / ".agent-crew" / "resume-prompt.md"
    if default.exists():
        return default.read_text(encoding="utf-8").strip()
    return DEFAULT_RESUME_PROMPT


def _build_command(args: argparse.Namespace, claude: str, prompt: str) -> List[str]:
    cmd = [claude, "-p", prompt, "--output-format", "json"]
    if args.resume_session:
        cmd += ["--resume", args.resume_session]
    if args.permission_mode:
        cmd += ["--permission-mode", args.permission_mode]
    if args.model:
        cmd += ["--model", args.model]
    if args.max_budget_usd is not None:
        # API-key auth only; harmless elsewhere but do not rely on it there.
        cmd += ["--max-budget-usd", str(args.max_budget_usd)]
    cmd += args.claude_arg
    return cmd


def _notify(cmd_template: Optional[str], message: str) -> None:
    if not cmd_template:
        return
    try:
        subprocess.run(cmd_template.replace("{message}", message), shell=True, timeout=60)
    except Exception as exc:  # a broken notifier must never stop a run
        print(f"notify failed: {exc}", file=sys.stderr)


def _summarize(stdout: str) -> Dict[str, Any]:
    """Pull what we can out of `--output-format json`; tolerate anything else."""
    try:
        data = json.loads(stdout)
    except json.JSONDecodeError:
        return {}
    if isinstance(data, list) and data:
        data = data[-1]
    if not isinstance(data, dict):
        return {}
    return {
        k: data[k]
        for k in ("is_error", "total_cost_usd", "num_turns", "duration_ms", "subtype", "session_id")
        if k in data
    }


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--project", required=True, help="working directory of the run")
    ap.add_argument("--log", default=runlog.DEFAULT_LOG, help="log path, relative to --project")
    ap.add_argument("--stale-after", type=int, default=1200,
                    help="seconds of silence before the run is considered stalled "
                         "(default 1200; roughly 3x a cycle, floor 20m)")
    ap.add_argument("--resume-prompt", default=None,
                    help="file holding the prompt to send (default .agent-crew/resume-prompt.md)")
    ap.add_argument("--claude", default=None, help="path to the claude executable")
    ap.add_argument("--resume-session", default=None,
                    help="resume this session id instead of starting a fresh one; only for a "
                         "session known to be alive and merely idle (see the module docstring)")
    ap.add_argument("--permission-mode", default="acceptEdits")
    ap.add_argument("--model", default=None)
    ap.add_argument("--max-budget-usd", type=float, default=None)
    ap.add_argument("--timeout", type=int, default=3600, help="seconds before the launched run is killed")
    ap.add_argument("--notify-cmd", default=None,
                    help="shell command run on a terminal state; {message} is substituted")
    ap.add_argument("--lock", default=None, help="lock file path (default <project>/.agent-crew/watchdog.lock)")
    ap.add_argument("--claude-arg", action="append", default=[],
                    help="extra argument passed through to claude (repeatable)")
    ap.add_argument("--dry-run", action="store_true", help="print what would happen and exit")
    args = ap.parse_args(argv)

    project = Path(args.project).resolve()
    if not project.is_dir():
        print(f"--project is not a directory: {project}", file=sys.stderr)
        return 2
    log = project / args.log

    st = runlog._status(log, stale_after=args.stale_after)

    if not st["should_resume"]:
        print(f"no action: {st['resume_blocked_by']}")
        if st["stopped"]:
            _notify(args.notify_cmd,
                    f"run in {project.name} stopped: {st['stop_reason']} - {st['stop_detail']}")
        return 0

    claude = _resolve_claude(args.claude)
    if not claude:
        print("claude executable not found; pass --claude", file=sys.stderr)
        _notify(args.notify_cmd, f"watchdog for {project.name} cannot find the claude executable")
        return 2

    prompt = _read_prompt(project, args.resume_prompt)
    cmd = _build_command(args, claude, prompt)

    if args.dry_run:
        print(f"would run in {project}:")
        print("  " + " ".join(f'"{c}"' if " " in c else c for c in cmd))
        return 0

    lock = Lock(Path(args.lock) if args.lock else project / ".agent-crew" / "watchdog.lock")
    if not lock.acquire():
        print("another watchdog firing holds the lock; skipping")
        return 0

    try:
        runlog.cmd_note(argparse.Namespace(
            log=str(log),
            text=f"watchdog: run stale ({runlog._ago(st['last_entry_age_s'])} since last entry), restarting",
            source="watchdog",
        ))
        started = time.time()
        try:
            proc = subprocess.run(cmd, cwd=str(project), capture_output=True,
                                  text=True, timeout=args.timeout)
            out, code = proc.stdout, proc.returncode
            err = proc.stderr.strip()
        except subprocess.TimeoutExpired:
            out, code, err = "", -1, f"killed after {args.timeout}s"
        except OSError as exc:
            # A bad --claude path, a missing interpreter, a full disk. Record
            # it and let the next firing try again; a traceback here would
            # leave the run stalled with nothing in the log saying why.
            out, code, err = "", -1, f"could not launch: {exc}"

        info = _summarize(out)
        elapsed = int(time.time() - started)
        bits = [f"exit {code}", f"{elapsed}s"]
        if "total_cost_usd" in info:
            bits.append(f"${info['total_cost_usd']:.2f}")
        if "num_turns" in info:
            bits.append(f"{info['num_turns']} turns")
        flat_err = " ".join(err.split())[:200]  # one log line, however it failed
        detail = ", ".join(bits) + (f" - {flat_err}" if flat_err else "")
        runlog.cmd_note(argparse.Namespace(log=str(log), source="watchdog",
                                           text=f"watchdog: restart finished ({detail})"))
        print(f"restart finished ({detail})")

        # Read the state the restarted run left behind, not the one we saw
        # before launching it.
        after = runlog._status(log, stale_after=args.stale_after)
        if after["stopped"]:
            _notify(args.notify_cmd,
                    f"run in {project.name} stopped: {after['stop_reason']} - {after['stop_detail']}")
        elif code != 0:
            _notify(args.notify_cmd,
                    f"run in {project.name} failed to restart ({detail}); will retry on the next firing")
        return 0
    finally:
        lock.release()


if __name__ == "__main__":
    sys.exit(main())
