# scripts/

Helpers for unattended runs. Everything here is **Python 3.9+, standard library only, no installation** — copy the directory, or point at it in a checkout. Nothing here reaches the network, reads credentials, or emits telemetry.

Every script is **optional**. A run that ignores this directory entirely still works; `docs/unattended-runs.md` and `templates/unattended-run-brief.md` are followable by hand. These remove toil and make the run's state machine-readable, which is what lets a watchdog answer "is this alive" without parsing prose.

| Script | What it does |
|---|---|
| `runlog.py` | Write-ahead run log: intent before the work, outcome after, timestamps, budget counters, and `status --json` for tooling. |
| `watchdog.py` | Restarts a stalled run. Meant to be fired by the OS scheduler, which is the only durable trigger available on every plan. |
| `install-watchdog-windows.ps1` | Registers `watchdog.py` as a Scheduled Task. `-DryRun` prints what it would register. |
| `install-watchdog-cron.sh` | The same for cron (Linux) and macOS. `--dry-run` likewise. |

## Quickstart

From the project being worked on, with `AC` pointing at an agent-crew checkout or install:

```
python $AC/scripts/runlog.py init --budget-hours 8 --max-dispatches 9
cp $AC/templates/resume-prompt.md .agent-crew/resume-prompt.md   # then edit the two fields
python $AC/scripts/watchdog.py --project . --dry-run             # confirm the command looks right
pwsh $AC/scripts/install-watchdog-windows.ps1 -Project . -IntervalMinutes 20
```

Then launch the run itself with the brief from `templates/unattended-run-brief.md`.

**Fire the trigger once before relying on it.** An untested trigger is indistinguishable from a working one until the night it matters, which is exactly the failure this directory exists because of.

## Why these exist

On 2026-08-30 an unattended run completed one cycle, scheduled its own next wake, hit a usage limit, and stopped. Nothing restarted it for nine hours, and nobody could tell from the log whether it was dead or sleeping, because the log carried one timestamp on line 1 and never another.

Both halves of that are addressed here, and neither is clever: a log that timestamps every entry and records intent before the action, and a trigger that lives outside the session so that a stop becomes a delay. The full account is in `docs/reviews/2026-08-30-overnight-run/`.

## What the watchdog does not buy

**Not immunity to usage limits.** If a restart fails because the account is rate-limited, the attempt is recorded and the next firing tries again. Automatic recovery is the property; describing it as more than that is how people end up trusting it further than it goes.

**Not a substitute for the run's own stop conditions.** The watchdog restarts a run that has gone quiet. Only the run decides it is finished, by recording a stop — at which point the watchdog reads that and goes quiet too.
