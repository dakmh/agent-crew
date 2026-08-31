# Standard: Unattended Run Readiness

The gates a run must pass before it is left to work without a human watching. Cited by briefs, teams, and skills instead of restating the checklist inline.

An unattended run is not a long attended run. Three things change: nobody notices when it stops, nobody notices where it writes, and the thing that runs out is not the thing the brief usually counts.

## Why runs stop and nobody notices

Every scheduling mechanism *inside* a Claude Code session ends when the session does. `ScheduleWakeup` — the self-pacing form of `/loop` — is session-scoped by documentation. The fixed-interval form runs on an in-memory cron whose own documentation says jobs "live only in this Claude session", so it is no more durable, and it fires only while the session is idle. A run that hits a usage limit therefore does not pause: it stops, and the pending wakeup dies with it.

The trigger has to live outside the session. The operating system's scheduler is the option available on every plan; cloud routines are an upgrade where the account has them. Neither grants immunity to usage limits — what they buy is that a stop becomes a delay, because the next firing reads the log and picks up.

## The gates

A run is ready when every gate passes. A gate that cannot pass is a reason to shorten the run or attend it, not a reason to proceed hoping.

| Gate | Passes when |
|---|---|
| **Durable trigger** | A trigger exists that survives the session ending, **and it has been fired once, before the run, to prove it fires.** An untested trigger is indistinguishable from a working one until the night it matters. |
| **Budget in the scarce unit** | The brief bounds the resource that actually runs out. Where a review team is in the loop, that is the number of subagent dispatches; under API-key auth, dollars via `--max-budget-usd` are also available. Cycles and wall-clock are backstops, not the primary bound — a run can exhaust its account with 47 of 48 cycles and 7h58m unspent. |
| **Canary first cycle** | Cycle 1 asserts the environment, writes the log skeleton and the planned breakdown of the work, does **one small unit**, commits, and schedules. It is the cheapest cycle of the run, not the most expensive. If the setup is going to fail, it should fail cheaply. |
| **Write-ahead log** | Intent is recorded **before** the action and the outcome after, sharing an identifier, so that a death mid-cycle leaves the in-flight unit identifiable. A log written only after the work leaves uncommitted files with nothing explaining them. |
| **Liveness** | Every entry carries a UTC timestamp and the log's top line names the last one. This is the whole fix for "I cannot tell whether it is dead or sleeping," and it costs nothing. |
| **Resume protocol** | The brief names, in order, exactly what to read on waking — and what **not** to read in full. A resuming run that re-reads the design documents spends its first cycle on context it does not need. |
| **Terminal-state notification** | Every stop condition notifies, not only the successful one. Then silence is unambiguous: it means the run is still going. |
| **Stop conditions** | Completion, budget exhaustion, blocked-on-a-human, and a no-progress rule are all present and all reachable. The no-progress rule ("N consecutive cycles with no test going red→green and no new log content") is the guard against a loop that spins while appearing busy. |
| **Blast radius** | The destructive surface is named explicitly; an assertion that proves it is out of reach runs **every cycle**, not once at launch; and failing that assertion is itself a stop condition. An unattended run has nobody watching where it writes. |

## Notes on the gates

**Assert the environment by value, never by claim.** An assertion that a specific string appears in a tool's output is worth far more than "the tests pass" — a suite that silently skips the tests that would have caught a wrong environment reports green. Preconditions recorded in a document as "currently satisfied" are a claim, and claims go stale: check the value.

**In flight is not the same as failed.** An entry with a recorded intent and no outcome is the unit that was in flight when the run died. The work may well have completed with the process dying before the outcome was written, so the correct response is to reconcile that one item against the tree, not to redo it.

**A weakened acceptance criterion is reported, never absorbed.** If a criterion turns out to be unachievable as written, the run changes it explicitly, records the reasoning inline, and flags it in the summary. A run that silently redefines its own success conditions is worse than one that fails.

**Budget the review gate as a purchase, not a step.** Where a dispatching review team gates the work (see `crew/teams/security-standards-review.md`), a dispatch is the most expensive single action the run can take: several isolated contexts, each paid for in full, running concurrently. Dispatch once per unit of work that becomes one commit — never per intermediate change.
