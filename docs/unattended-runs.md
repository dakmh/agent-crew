# Unattended runs

What to read before leaving an agent to work for hours without a human watching. The gates themselves are in `standards/unattended-run-readiness.md`; this document is the reasoning behind them and the mechanics of setting one up.

Written from one run on 2026-08-30 that produced good work and a bad process — three work items landed, a test suite went from 86 to 253, nine review findings were fixed with regression tests, and the whole thing stopped after a single cycle with nothing to restart it for nine hours. The full record is in `docs/reviews/2026-08-30-overnight-run/`.

## What an unattended run actually costs

Three things are worth knowing before starting, because each of them surprised somebody.

**The trigger is the hard part.** Not the work, not the prompt. Every scheduling mechanism inside a Claude Code session dies when that session does, so the interesting question is never "how does the agent pace itself" but "what brings it back".

**The review gate is the expensive part.** A dispatching review team is several isolated contexts, each paid for in full, running concurrently. In the 2026-08-30 run, three dispatches in the first cycle consumed the entire first session. The review was worth it — it found two bugs in correct-looking code that no test could have caught — but it is a purchase, not a step.

**The log is what makes recovery cheap.** The restart after that nine-hour gap cost almost nothing, because the log said what had landed, what was owed, and what the next unit of work was. This was the single highest-value element of that run's brief, and it is the reason the resume protocol goes at the *top* of the template rather than the bottom.

## Choosing a trigger

| Mechanism | Survives the session ending? | Available on |
|---|---|---|
| `/loop` with no interval (`ScheduleWakeup`) | **No** — session-scoped by documentation | everywhere |
| `/loop 20m` (in-memory cron) | **No** — jobs "live only in this Claude session"; also fires only while the session is idle, and expires after 7 days | everywhere |
| OS scheduler running `claude -p` | **Yes** | everywhere — this is the default |
| Cloud routines (`/schedule`) | **Yes** | accounts with cloud sessions; verify before relying on it |

The second row is the one worth pausing on, because switching from the self-pacing form of `/loop` to a fixed interval is the fix most people reach for first, and it does not survive a session stop either. Both forms are fine *inside* a run — self-pacing worked reliably for eight cycles once restarted — they are simply not the thing that brings a dead session back.

**Neither durable option grants immunity to usage limits.** What they buy is that a stop becomes a delay: the next firing reads the log and picks up. Do not describe it as more than that.

`scripts/watchdog.py` plus one of the installers in `scripts/` is the OS-scheduler path. Where cloud routines are available they substitute cleanly — the run log, the resume prompt, and the stop conditions are identical, and only the thing pulling the trigger changes.

## Sizing the budget

Bound the resource that actually runs out. The 2026-08-30 brief bounded cycles (48) and wall-clock (8 hours), and the run ended with 47 cycles and 7h58m unspent, having exhausted account usage — which was neither counted nor named.

- **Dispatches** are the primary unit whenever a review team is in the loop. "At most 9 review dispatches" constrains the real cost; "48 cycles" does not. Count them with `runlog.py spend --dispatches N`.
- **Dollars** are available under API-key auth via `claude -p --max-budget-usd N`, which `watchdog.py` passes through. Under subscription auth, treat the `total_cost_usd` field in `--output-format json` output as a relative measure for ranking cycle expense rather than a bill.
- **Cycles and wall-clock** stay as backstops. They are cheap to state and they catch the runaway case; they are just not the binding constraint.

Front-loading is the other half of this. Make cycle 1 the *cheapest* cycle — assert, write the skeleton, do one small unit, commit — because if the setup is going to fail, it should fail cheaply. In the run this document comes from, cycle 1 built an entire work item and dispatched three reviewers, which is exactly backwards.

## Setting one up

From the project, with `AC` pointing at an agent-crew checkout or install:

```
python $AC/scripts/runlog.py init --budget-hours 8 --max-dispatches 9
cp $AC/templates/resume-prompt.md .agent-crew/resume-prompt.md      # fill in its two fields
cp $AC/templates/preflight.example.json .agent-crew/preflight.json  # write your own assertions
python $AC/scripts/preflight.py --check
python $AC/scripts/watchdog.py --project . --dry-run
pwsh $AC/scripts/install-watchdog-windows.ps1 -Project . -IntervalMinutes 20
```

Then check the filled-in brief against `standards/unattended-run-readiness.md`, fire the trigger once by hand to prove it fires, and launch with the text below the rule in `templates/unattended-run-brief.md`.

Paste the brief rather than pointing at the file. The material above the rule in that template is addressed to the operator, not the agent, and a run that reads its own preconditions section will try to satisfy checks that a human has already done.

## The assertions are the safety mechanism

`preflight.py` reads assertions from the project, and they are worth writing carefully, because an unattended run has nobody watching where it writes.

Assert **by value, never by claim**. "The tests pass" is nearly worthless: a suite that silently skips the tests which would have caught a wrong environment reports green. "The pytest header contains this exact sandbox path, in strict mode" is worth a great deal. Likewise, a precondition recorded in a document as "currently satisfied" is a claim, and claims go stale — the 2026-08-30 run found its own preconditions document wrong about a power setting on the morning of the run.

Name the destructive surface explicitly and assert that it is out of reach. A drive that should not resolve, a path that should not exist, a branch that should not be checked out.

## When it goes wrong

**"Is it dead or sleeping?"** `runlog.py status` answers it: last entry, its age, budget remaining, and whether a stop was recorded. That question took a human nine hours to ask and could not be answered from the log at all, which is why liveness is a gate.

**An entry is in flight.** A `begin` with no `end` names exactly the unit that was running when the session died. **In flight is not the same as failed** — the work may have completed with the process dying before the outcome was recorded — so reconcile that one item against the tree rather than redoing it.

**The watchdog keeps restarting and nothing progresses.** The no-progress stop condition is what should catch this from the inside. From the outside, `runlog.py status` shows cycles climbing with no `end --status done`; stop the task, read the log, and fix the brief rather than the run.

**The restart fails because of a usage limit.** Expected, and handled: the attempt is recorded and the next firing tries again. This is the delay the durable trigger buys.

## Worked example

`docs/reviews/2026-08-30-overnight-run/06-improvement-plan.md` §5 lists the five changes that would have turned that run's nine-hour outage into a twenty-minute pause, against a brief that was otherwise well formed. It is the shortest useful thing to read before writing your own.
