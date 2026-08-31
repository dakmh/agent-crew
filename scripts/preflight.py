#!/usr/bin/env python3
r"""Assert that an unattended run's environment is what the run assumes.

An unattended run has nobody watching where it writes. The assertions that
matter are not "the tests pass" — a suite that silently skips the tests which
would have caught a wrong environment reports green — but "this exact string
appeared in that command's output", and "this path does not resolve".

The assertions live in the *project*, not here, because every project's are
different. Default location `.agent-crew/preflight.json`:

    {
      "assertions": [
        {
          "name": "sandbox is strict and correctly rooted",
          "run": "./venv/Scripts/python.exe -m pytest --collect-only -q",
          "expect_stdout_contains": "sandbox [strict]: C:/Sandbox/project"
        },
        {
          "name": "archive drive is detached",
          "run": "python -c \"import os,sys; sys.exit(1 if os.path.exists('E:/') else 0)\"",
          "expect_exit": 0
        },
        {
          "name": "on a working branch, not main",
          "run": "git rev-parse --abbrev-ref HEAD",
          "expect_stdout_not_matches": "^(main|master)$"
        }
      ]
    }

JSON rather than YAML deliberately: the standard library has no YAML parser,
and a dependency for this would cost more than the readability it buys.

Each assertion may carry any of:

    expect_exit                int, default 0 (null to ignore the exit code)
    expect_stdout_contains     substring that must appear
    expect_stdout_not_contains substring that must not appear
    expect_stdout_matches      regex that must match (searched, multiline)
    expect_stdout_not_matches  regex that must not match
    timeout                    seconds, default 300
    cwd                        relative to the project root

Usage:

    preflight.py --check [--config .agent-crew/preflight.json] [--project .]
                 [--json] [--quiet]

Exits 0 when every assertion passes, 1 when any fails, 2 on a usage or config
error. A failure names the assertion, what was expected, and what was seen.

Standard library only, Python 3.9+.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

DEFAULT_CONFIG = ".agent-crew/preflight.json"


def _fail(assertion: Dict[str, Any], reason: str, seen: str) -> Dict[str, Any]:
    return {"name": assertion.get("name", assertion.get("run", "?")),
            "ok": False, "reason": reason, "seen": seen[:500]}


def _check_one(assertion: Dict[str, Any], project: Path) -> Dict[str, Any]:
    command = assertion.get("run")
    name = assertion.get("name", command or "?")
    if not command:
        return {"name": name, "ok": False, "reason": "assertion has no `run` command", "seen": ""}

    cwd = project / assertion["cwd"] if assertion.get("cwd") else project
    try:
        proc = subprocess.run(command, shell=True, cwd=str(cwd), capture_output=True,
                              text=True, timeout=assertion.get("timeout", 300))
    except subprocess.TimeoutExpired:
        return _fail(assertion, f"timed out after {assertion.get('timeout', 300)}s", "")
    except OSError as exc:
        return _fail(assertion, f"could not run: {exc}", "")

    out = proc.stdout + proc.stderr

    expected_exit = assertion.get("expect_exit", 0)
    if expected_exit is not None and proc.returncode != expected_exit:
        return _fail(assertion, f"exit {proc.returncode}, expected {expected_exit}", out)

    needle = assertion.get("expect_stdout_contains")
    if needle is not None and needle not in out:
        return _fail(assertion, f"output does not contain {needle!r}", out)

    anti = assertion.get("expect_stdout_not_contains")
    if anti is not None and anti in out:
        return _fail(assertion, f"output contains {anti!r} and should not", out)

    pattern = assertion.get("expect_stdout_matches")
    if pattern is not None and not re.search(pattern, out, re.MULTILINE):
        return _fail(assertion, f"output does not match /{pattern}/", out)

    anti_pattern = assertion.get("expect_stdout_not_matches")
    if anti_pattern is not None and re.search(anti_pattern, out, re.MULTILINE):
        return _fail(assertion, f"output matches /{anti_pattern}/ and should not", out)

    return {"name": name, "ok": True, "reason": "", "seen": ""}


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--check", action="store_true", help="run the assertions (the only mode)")
    ap.add_argument("--project", default=".", help="project root (default: cwd)")
    ap.add_argument("--config", default=None, help=f"assertions file (default {DEFAULT_CONFIG})")
    ap.add_argument("--json", action="store_true", help="machine-readable result")
    ap.add_argument("--quiet", action="store_true", help="print only failures")
    args = ap.parse_args(argv)

    project = Path(args.project).resolve()
    config = Path(args.config) if args.config else project / DEFAULT_CONFIG
    if not config.exists():
        print(f"no assertions file at {config}", file=sys.stderr)
        print("An unattended run with no environment assertions is a run with nobody watching "
              "where it writes; see standards/unattended-run-readiness.md.", file=sys.stderr)
        return 2

    try:
        data = json.loads(config.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"{config} is not valid JSON: {exc}", file=sys.stderr)
        return 2

    assertions = data.get("assertions") if isinstance(data, dict) else data
    if not isinstance(assertions, list) or not assertions:
        print(f"{config} defines no assertions", file=sys.stderr)
        return 2

    results = [_check_one(a, project) for a in assertions]
    failed = [r for r in results if not r["ok"]]

    if args.json:
        print(json.dumps({"ok": not failed, "results": results}, indent=2))
    else:
        for r in results:
            if r["ok"]:
                if not args.quiet:
                    print(f"  ok    {r['name']}")
            else:
                print(f"  FAIL  {r['name']}")
                print(f"        {r['reason']}")
                if r["seen"]:
                    for line in r["seen"].strip().splitlines()[:8]:
                        print(f"        | {line}")
        if failed:
            print(f"\n{len(failed)} of {len(results)} assertions failed. "
                  "The environment is not what the run assumes; stop.")
        elif not args.quiet:
            print(f"\nall {len(results)} assertions pass.")

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
