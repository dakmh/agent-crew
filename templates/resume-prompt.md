# Resume prompt

Copy this into `<project>/.agent-crew/resume-prompt.md`, replacing the two angle-bracket fields. `scripts/watchdog.py` reads it from there and sends it verbatim to a fresh `claude -p` session whenever the run has gone quiet.

Keep it short. It is re-sent on every recovery, and its whole job is to point at the log — the log is what carries the state, and a resume prompt that tries to restate the run's own context will drift from it.

---

Read `RUN_LOG.md`, then `<the brief, e.g. .agent-crew/run-brief.md>`, then continue the run they describe.

Before doing anything else:

1. Run `python <path to agent-crew>/scripts/preflight.py --check`. If any assertion fails, run `runlog.py stop --reason environment "<what failed>"` and stop. The environment is not what this run assumes and nothing after that point means anything.
2. Check the log for an entry in flight — a `begin` with no `end`. **In flight is not the same as failed**: the work may have completed with the session dying before the outcome was recorded. Reconcile that one item against the tree before starting anything new, and record what you found.

Then do **one** unit of work, record it (`runlog.py begin` before, `runlog.py end` after), and stop. Do not schedule your own next wake — the scheduler provides the loop, and one unit per session is what makes a stop survivable.

If everything in scope is done, or everything remaining needs a human, call `runlog.py stop` with the reason and a one-line detail. That is what tells the watchdog to go quiet.
