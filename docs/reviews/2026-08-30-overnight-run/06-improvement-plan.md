# Improvement plan — unattended runs and the review gate

**Status:** proposal, nothing implemented. **Date:** 2026-08-30. **Inputs:** the five records in this folder, plus a direct audit of the library performed while writing this.

**What this plan is for.** One unattended run on 2026-08-30 produced good work and a bad process: it stopped after a single cycle and nothing restarted it for nine hours. The work items landed, the review gate performed well, and the failure was entirely in how the run was bounded and triggered. This plan turns that into changes to agent-crew: directives in the library, helper scripts that did not exist, and a prompt template that encodes what the run had to learn the hard way.

**Design constraint, stated up front.** Everything proposed here must work for someone on Pro, Max, Team, Enterprise, or a raw API key. That rules out the obvious fix. It is the reason [Workstream B](#3-workstream-b--tooling-and-helper-scripts) is built on the OS scheduler and the `claude` CLI rather than on cloud routines, and the reason cloud routines appear only as an optional upgrade.

---

## 1. The findings this plan acts on

Condensed from [03-postmortem.md](03-postmortem.md) and [04-run-log-copy.md](04-run-log-copy.md). Everything in this section is evidenced there; the corrections in §1.1 are new to this document.

**F1 — The budget was denominated in the wrong unit.** The brief bounded cycles (48) and wall-clock (8 hours). The run ended with 47 cycles and 7h58m unspent, having exhausted the resource that was neither counted nor named: account usage. The cost was front-loaded — cycle 1 built a whole work item *and* dispatched three parallel review subagents, and those three dispatches are the dominant term in the whole first session.

**F2 — The trigger died with the session.** `ScheduleWakeup` is session-scoped by design. For a run explicitly framed as unattended and overnight, a session-scoped trigger is a single point of failure, and nothing in the brief compensated for it.

**F3 — Nobody could tell "stopped" from "sleeping".** The log carried one timestamp on line 1 and never another. A per-cycle timestamp and a `Last cycle:` header would have answered the question at a glance, at zero cost.

**F4 — The log recorded outcomes, not intent.** Entries were written after the work. A death at 80% through a cycle would have left uncommitted files with no record of what they were. The run was, at that moment, building a write-ahead journal for exactly this failure mode.

**F5 — A standard cited by a persona was not loaded by the team running it.** The Security Engineer persona points at `standards/risk-assessment.md` for its disposition scale; the security-review team loaded only `code-review-severity.md`. Three dispatched subagents reproduced the scale correctly from persona text alone, which is luck. Fixed for that one team in `7a79ce0`; the general defect is not fixed, and §2.1 shows it is larger than one team.

**F6 — The substrate threshold is ambiguous and unexercised.** The team file reads "a single file **or** a diff under ~150 lines". A 2-file, 82-line changeset satisfied the second clause and not the first, and the reviewing session had to decide the clauses were alternatives. Separately, all three in-run diffs were 950–1,375 lines, so the in-context branch never ran and the ~150-line boundary has never been tested from either side.

**F7 — Which copy of the library executes was folklore, and the folklore was wrong.** The brief asserted that `/agent-crew:*` runs from the installed snapshot in the plugin cache and that checkout edits would be inert. All three runs announced their base directory as the working checkout. This decides whether a defect found mid-run can be fixed and re-exercised in the same run, so it should be settled and stated, not inferred.

**F8 — The skill was invoked with a bare commit SHA from a directory holding several repos**, a context form the skill's context-gathering section does not name. Resolution took an ad-hoc two-stage filesystem search.

### 1.1 Corrections and additions to the postmortem

The postmortem recommends a cloud schedule as the durable trigger and correctly marks its interaction with usage limits as untested. Two things need adding before that recommendation is built on.

**No in-session scheduling mechanism is durable — including the interval form of `/loop`.** `ScheduleWakeup` (dynamic `/loop`) is documented as session-scoped. The fixed-interval form runs on `CronCreate`, whose own tool description states that jobs "live only in this Claude session — nothing is written to disk, and the job is gone when Claude exits", that they fire only while the REPL is idle, and that recurring jobs auto-expire after 7 days. So switching from `/loop` (no interval) to `/loop 20m` would **not** have survived this failure. That distinction matters because it is the fix a reader is most likely to reach for first.

**Cloud routines are not universally available.** `/schedule` creates cloud-side scheduled agents, which depend on cloud sessions being available to the account. That is a property of the plan and the environment, not of agent-crew, and an API-key-only or air-gapped setup will not have it. **Verify before relying on it; do not write it into a template as a prerequisite.**

**The consequence for this plan:** the only trigger that is both durable and available on every plan is one that lives outside Claude Code entirely — the operating system's scheduler invoking `claude -p`. That is what Workstream B builds. Cloud routines remain a legitimate upgrade where present, and the same run log and resume protocol serve both.

---

## 2. Workstream A — library directives

Changes to the text of the library. Cheap, self-contained, and independent of the tooling in Workstream B — this workstream is worth landing on its own even if nothing else here is built.

### A1. Any standard a persona cites by path must be loaded by whatever runs that persona

**The general rule, stated once.** Add to `skills/_conventions.md` → *Sources of authority*: a persona that references a standard by path and is handed only its own text will improvise that standard's content from memory. That may happen to match and it is not a design. Every team file's member list is therefore responsible for loading every standard its members cite, and the skill loads every standard the team names.

**The audit, already run.** The Security Engineer cites `standards/risk-assessment.md` and appears in **8 teams**; **4 of them do not load it**:

| Team | Loads `risk-assessment.md` |
|---|---|
| `security-standards-review.md` | yes — fixed in `7a79ce0` |
| `implementation.md` | yes |
| `release-management.md` | yes |
| `server-cloud-infrastructure.md` | yes |
| `architecture-design.md` | **no** |
| `dev-environments.md` | **no** |
| `devops-automation.md` | **no** |
| `mobile-development.md` | **no** |

The Release Manager cites `standards/review-verdicts.md`; the one team it belongs to (`release-management.md`) loads it. No other persona cites a standard by path today.

**Do:** add `standards/risk-assessment.md` to the load list of the four teams above; add the general rule to `_conventions.md`; add the citation check to `docs/capability-audit.md` as a recurring item, since new personas will reintroduce the drift.

**Acceptance:** no pair of (persona, standard-it-cites) exists for which some team containing that persona fails to name that standard. Worth encoding as a check script — see B4.

### A2. Make the substrate rule decidable

**The defect (F6).** "roughly: a single file or a diff under ~150 lines" has two clauses that can disagree, and a reader had to adjudicate mid-run.

**Do:** restate the fallback in `crew/teams/security-standards-review.md` → *Execution* as a single test on one quantity — dispatch when the changeset exceeds ~150 changed lines, collapse to in-context at or below it, regardless of file count — plus the unconditional fallback when the `Agent` tool is unavailable. Keep "roughly": the number is a judgment aid, and a 160-line diff should not become a rules-lawyering exercise. State the count's basis (added plus deleted lines, as `git diff --stat` reports them) so that two runs against the same diff pick the same branch.

**Do also:** move the rule's *statement* into `skills/_conventions.md` as the default shape for any dispatching team, leaving the team file to name its own number. There is one dispatching team today, and a second one will otherwise copy the ambiguity along with the pattern.

### A3. Disclose the cost of a run, not only its substrate

**Why (F1).** The disclosure line today says which substrate was used. It does not say how many subagents were dispatched — which is the number a run budget is actually denominated in, and the number a human reading the output needs in order to decide whether to run the gate again.

**Do:** extend the disclosure requirement in `skills/_conventions.md` → *Execution substrate*. A dispatched run states the member count and the changeset size that selected the branch. An in-context run states the size too, so the threshold accumulates evidence from both sides — which is what makes A6 possible.

Suggested form, replacing the current one-liner:

> `_Substrate: 3 parallel Explore subagents (Security Engineer, Code Standards Reviewer, Senior Developer). Changeset 1,336 lines / 10 files, above the team's ~150-line threshold. Library root: <path>._`

### A4. State the library root in the disclosure

**Why (F7).** Two sessions disagreed about whether the checkout or the plugin cache was executing, and the run's brief was written on the wrong assumption. The run itself can answer this in one line, and then it never has to be guessed at again.

**Do:** add the resolved plugin root to the disclosure line, as shown in A3. Update `README.md` and `CLAUDE.md` with what was actually observed — a marketplace registered with a `directory` source resolved to the checkout on all three runs, so edits there were live. Mark it as observed in one configuration rather than as a general guarantee, and add "does a directory-source marketplace still execute from the checkout" to `docs/capability-audit.md`.

**Note the consequence for briefs.** If the checkout is live, then a brief telling a run that library fixes cannot take effect mid-run is wrong, and the run may legitimately fix a library defect and re-exercise it in the same session. The template in Workstream C reflects this rather than repeating the old assumption.

### A5. Accept a git ref as review context

**Why (F8).** A commit SHA, a branch, a tag, a range like `HEAD~3..HEAD`, or "the working tree" are the natural ways to point a review at code, and the skill's context-gathering section names none of them.

**Do:** in `skills/security-review/SKILL.md` → *Context gathering*, add a git-ref form alongside paste and path, with the resolution procedure written down. Resolve against the repo containing the current working directory; if the working directory is not itself a repo, search its immediate children one level deep and name every repo where the ref resolves; if it resolves in more than one, or in none, ask rather than guess. One level deep, deliberately — the session that had to do this scanned to depth 4, and that is a filesystem crawl rather than a resolution rule.

**Not the other review skills.** `review-proposal` and `mobile-implementation-review` were candidates on the face of it and turn out not to be: both take a proposal or an implementation brief as required context, not code, so a git ref is not a form their input comes in. Put the resolution procedure in `skills/_conventions.md` → *Context gathering* anyway, so that a future code-taking skill inherits it rather than reinventing it.

### A6. Calibrate the substrate threshold instead of asserting it

**Why (F6).** ~150 lines is an unvalidated guess, and three runs at 950–1,375 lines gave it no evidence from either side.

**Do:** two things, neither of which is a code change.

1. Add an explicit invocation override so the branch can be forced: `/agent-crew:security-review [substrate:in-context]` and `[substrate:dispatch]`. This makes the fallback branch testable on demand instead of only when a small diff happens along, and it gives a human a cost lever on plans where dispatch is expensive. Document it in `skills/_conventions.md` → *Modifiers* as a distinct kind of override — it targets the run rather than a persona, so it does not belong to the mutually-exclusive modifier pairs.
2. Record each run's disclosure line in `docs/reviews/` when the run is notable, and revisit the number once roughly ten runs exist on both sides of it. Do not move it before then.

### A7. A readiness standard for unattended runs

**Why.** The guidance in [03-postmortem.md](03-postmortem.md) → *Guidance for long runs* is eight rules that a brief either satisfies or does not. That is the same shape as `standards/mobile-release-readiness.md` — a gate checklist a team can be pointed at — and the library already has the slot for it.

**Do:** add `standards/unattended-run-readiness.md`, structured as gates with one pass condition each. Draft contents:

| Gate | Passes when |
|---|---|
| Durable trigger | A trigger exists that survives the session ending, and it has been fired once before the run, to prove it fires. |
| Budget in the scarce unit | The brief bounds the resource that actually runs out — dispatch count, or dollars via `--max-budget-usd` — and not only cycles and wall-clock. |
| Canary first cycle | Cycle 1 asserts the environment, writes the log skeleton and the planned sub-cycle breakdown, does one small unit of work, commits, and schedules. It is the cheapest cycle, not the most expensive. |
| Write-ahead log | Intent is appended before the action and the outcome after, sharing an identifier. |
| Liveness | Every entry is timestamped in UTC, and a `Last cycle:` line sits at the top of the log. |
| Resume protocol | The brief names, in order, exactly what to read on waking, and forbids reading the large documents in full. |
| Terminal-state notification | Every stop condition notifies. Silence then means "still running", unambiguously. |
| Stop conditions | Budget exhaustion, completion, blocked-on-a-human, and a no-progress rule are all present and all reachable. |
| Blast radius | The destructive surface is named, the environment assertion proving it is out of reach runs every cycle, and failing that assertion is itself a stop condition. |

The last gate is not in the postmortem's list. It is in the run's own brief — the detached archive drive, the strict-mode pytest header, "if `E:` resolves at all, stop and log it" — and it is the part of that brief that most deserves generalizing. An unattended run has nobody watching where it writes.

### A8. A directive on review cadence inside a loop

**Do:** add to `crew/teams/security-standards-review.md` → *Notes*: when this team is used as a gate inside an automated loop, dispatch once per unit of work that will become one commit, never per intermediate change. State the reason — the dispatch is the most expensive single action available to a run of this shape, and batching to the commit is what makes the review affordable without making it rarer than the commits it gates. This is the mid-run correction a human made on 2026-08-30, and it is what let the second run finish.

---

## 3. Workstream B — tooling and helper scripts

This is the part that did not exist and that the run needed. Four scripts and two installers, all of them small.

### B0. A decision to make first: agent-crew ships executable code for the first time

Today the repo is entirely documents. Workstream B adds a `scripts/` directory, and that is a real change in what the project is — it acquires a runtime, a platform surface, and a thing that can break independently of the prose.

**Recommendation: accept it, with constraints.** The alternative — writing the mechanics into a template and having each run's agent reimplement them — is exactly what produced the untimestamped log and the missing write-ahead, because an agent asked to invent its own logging under time pressure invents the cheap version. A script that is the same on every run is also the only way the watchdog can read the log without parsing prose.

Constraints, in order of importance:

- **Python 3.9+, standard library only, no third-party imports, one file per script.** Windows, macOS, and Linux all have a usable Python; nothing else is universally present. No `pip install` step, ever.
- **Every script is optional.** A run that ignores `scripts/` entirely must still work, and the prompt template must still be followable by hand. The scripts remove toil; they are not a dependency of the method.
- **No network access, no credentials, no telemetry.** These scripts touch the run log, the clock, and the OS scheduler.
- **The watchdog is the only script that invokes `claude`**, and it does so with an explicit, visible command line.

### B1. `scripts/runlog.py` — the write-ahead run log

Fixes F3 and F4 — the two failures that cost nothing to prevent and made the outage undiagnosable.

Owns one markdown file (default `RUN_LOG.md`) with a machine-readable header block and a human-readable body. The agent calls it instead of hand-editing the log's bookkeeping; the agent still writes prose into the body, because the prose is the resume artifact and that is the thing that worked.

```
runlog.py init   --budget-hours 8 --max-dispatches 9 --max-cycles 48 [--log PATH]
runlog.py begin  "build the merge core"            # write-ahead: intent, before the work
runlog.py end    --status done|blocked|noop "..."  # outcome, same seq as the begin
runlog.py note   "..."                             # free-form append, timestamped
runlog.py spend  --dispatches 3                    # increment the scarce-resource counter
runlog.py stop   --reason completed|budget|blocked|environment "..."
runlog.py status --json
```

Behavior worth pinning down now, because each of these is a lesson from the run:

- **`begin` writes before the work and `end` after**, sharing a sequence number. An entry with a `begin` and no `end` is exactly the unit that was in flight when the run died — and in flight is not the same as failed, so the resume protocol reconciles that one item rather than redoing it.
- **Every line carries a UTC timestamp, and the header carries `Last cycle:`.** This alone answers "dead or sleeping".
- **Flush and `fsync` on every append.** A log buffered inside a process that then dies records nothing about the cycle that mattered most. The cost is nothing against the work a cycle does. (The run's own item 6 reached this conclusion independently, for the same reason.)
- **`status --json` is the machine interface** and the only thing the watchdog reads: last-cycle timestamp and age in seconds, cycles used against budget, dispatches used against budget, wall-clock remaining, whether a `stop` has been recorded and why, and whether an entry is in flight. No prose parsing.
- **A truncated final line is survivable.** That is the shape a killed process leaves, and refusing to read the file because the crash left it ragged defeats the one case it exists for.
- **`init` is idempotent** — re-running against an existing log resumes rather than truncating. The watchdog will call the resume path far more often than the fresh one, and truncating a run log on restart is the worst available failure.

### B2. `scripts/preflight.py` — environment assertions

Fixes the *Blast radius* gate (A7) and makes the run's best-designed feature reusable. The 2026-08-30 brief required that a specific string appear in the pytest header, not merely that the tests pass, and that a drive letter fail to resolve. That is the right shape, and every project's version of it is different.

Declarative, with the assertions living in the **project**, not in agent-crew:

```yaml
# .agent-crew/preflight.yaml  — in the project being worked on
assertions:
  - name: sandbox is strict and correctly rooted
    run: ./venv/Scripts/python.exe -m pytest --collect-only -q
    expect_stdout_contains: "sandbox [strict]: C:/Cloudlet/01_SandboxedTests/photo-culling-sandbox"
  - name: archive drive is detached
    run: python -c "import os,sys; sys.exit(0 if not os.path.exists('E:/') else 1)"
    expect_exit: 0
  - name: on the working branch, not main
    run: git rev-parse --abbrev-ref HEAD
    expect_stdout_not_matches: "^(main|master)$"
```

`preflight.py --check` exits non-zero and prints which assertion failed and what it saw. The prompt template makes a failure a **stop condition**, not a warning: the environment is not what the run assumes, and nothing after that point means anything.

Use a small subset of YAML parsed by hand, or ship the format as JSON — the standard library has no YAML parser, and adding a dependency for this would violate B0. **Recommendation: JSON, with the docs showing it formatted readably.** Ugly beats a dependency.

### B3. `scripts/watchdog.py` plus installers — the durable trigger

Fixes F2, the failure that cost nine hours. This is the part that must work on every plan, and therefore the part that cannot live inside Claude Code.

**Mechanism.** The OS scheduler runs `watchdog.py` every N minutes. Each firing:

1. Read `runlog.py status --json`.
2. Exit quietly if a `stop` is recorded, if the budget is exhausted, or if the last cycle is younger than the staleness threshold. A healthy self-paced run makes the watchdog a no-op — that is the intended steady state.
3. If the log is stale beyond the threshold and no stop is recorded, take a lockfile (so two firings cannot overlap) and launch the resume command:

```
claude -p "$(cat .agent-crew/resume-prompt.md)" \
  --output-format json \
  --permission-mode acceptEdits \
  --max-budget-usd 15
```

4. Append the returned `total_cost_usd` and result status to the run log via `runlog.py note`, release the lock, and notify on any terminal state.

**Why a fresh `-p` session rather than `--resume <id>`.** The postmortem's highest-value finding was that the log made the restart nearly free. A fresh session reading the log has no dependence on a session that may have died in an unclean state, and it exercises the resume protocol on every recovery instead of only in the emergency. Keep `--resume` available as a flag for the case where the session is alive and merely idle.

**Staleness threshold.** Roughly three times the expected cycle length, floor of 20 minutes. Too tight and the watchdog starts a second run alongside a healthy slow cycle; the lockfile prevents overlap but not waste.

**Usage limits are a delay, not a stop.** If the resume attempt fails because the account is rate-limited, the watchdog records the attempt and exits — the next firing tries again. This is the property the postmortem correctly identified as the real prize: **automatic recovery, not immunity.** Nothing here grants immunity to usage limits and the docs must not imply otherwise.

**Installers, one per platform, each about twenty lines:**

- `scripts/install-watchdog-windows.ps1` — registers a Scheduled Task at the given interval, with "run whether user is logged on or not", AC-power conditions, and **`-WakeToRun` off**. The 2026-08-30 preconditions had to fight `HIBERNATEIDLE`; a watchdog task that cannot wake the machine is honest about needing the sleep settings handled, and the installer prints the current `powercfg` values and the fix command rather than silently changing power policy.
- `scripts/install-watchdog-cron.sh` — a crontab line for Linux, a launchd plist for macOS. Same defaults.

Both installers accept `--dry-run` and print the exact command they would register. Both are **verified once before the run** — the *Durable trigger* gate in A7 requires the trigger to have fired at least once, because an unfired trigger is indistinguishable from a working one until the moment it matters.

**Cloud routines, where available.** Where the account has cloud sessions, `/schedule` is a legitimate substitute for the OS scheduler and needs no local machine to stay awake. The run log, resume prompt, and stop conditions are identical either way — only the thing that pulls the trigger changes. Document it as the alternative, never as the prerequisite (see §1.1).

### B4. `scripts/lint.py` — library consistency checks

Small, and it turns three of this document's findings into things that cannot regress.

- Every `standards/*.md` cited in a persona is loaded by every team containing that persona (A1).
- Every persona named in a team file exists; every team named in a skill exists; every path referenced anywhere in the library resolves.
- Every skill's frontmatter `description` exists and is non-trivial, since it is the only discovery mechanism for plugin consumers.
- Every skill in `skills/` appears in both `README.md`'s table and `CLAUDE.md`'s index — the three-index drift already noted in `docs/optimization-plan.md` §2.1.

Run it in whatever CI this repo grows, and name it in `docs/capability-audit.md` as a first step of each audit.

---

## 4. Workstream C — guidance, templates, and the question of a new skill

### C1. `docs/unattended-runs.md` — the operator guide

One document, the thing a person reads before launching. Contents, in order:

1. **What an unattended run is and what it costs.** The honest version: the trigger is the hard part, the review gate is the expensive part, and the log is what makes recovery cheap.
2. **The trigger decision, by plan.** OS scheduler plus `claude -p` works everywhere and is the default. Cloud routines are an upgrade where the account has them. In-session scheduling — `/loop` in either form — is **not** a durable trigger, and §1.1 of this plan explains why in one paragraph that belongs here too, because it is the mistake a reader will otherwise make.
3. **The readiness gates**, pointing at `standards/unattended-run-readiness.md` rather than restating them.
4. **Sizing the budget.** How to count dispatches, what `--max-budget-usd` does and for whom, and why cycles and wall-clock are the wrong unit on their own.
5. **The scripts**, with the three-command quickstart.
6. **Worked example**, drawn from this folder: what the 2026-08-30 brief got right, what it got wrong, and the corrected version.

### C2. `templates/unattended-run-brief.md` — the prompt template

The single highest-leverage artifact here, because it is what a person actually copies. Built from [05-run-prompt-as-launched.md](05-run-prompt-as-launched.md), which was a good brief with two holes in it — no durable trigger and a budget in the wrong unit — and one wrong assumption (F7).

Structure, with placeholders in angle brackets and every section carrying a one-line note saying why it exists:

- **Operator preconditions** (above the rule, never pasted to the agent) — trigger installed and fired once, preflight assertions pass, power settings checked by value rather than by claim, plugin installed and enabled, working branch cut.
- **Resume protocol, first and unconditional** — what to read on waking, in order, and what not to read in full. This was the single highest-value element of the original brief and it belongs at the top of the template for the same reason it belonged at the top of the run.
- **Environment assertion** — run `preflight.py --check` before any work; a failure is a stop, not a warning.
- **Canary rule for cycle 1** — assert, write the log skeleton and the planned sub-cycle breakdown, do one small unit, commit, schedule. Explicitly: cycle 1 is the smallest cycle, and it does not dispatch a review team.
- **Budget** — dispatches first and by name, then dollars where the plan supports it, then cycles and wall-clock as backstops rather than as the primary bound.
- **Write-ahead logging** — `runlog.py begin` before, `runlog.py end` after, prose in the body, one entry per cycle even when the cycle achieved nothing.
- **Review gate** — one dispatch per unit of work that becomes one commit, per A8; record the disclosure line verbatim.
- **Commit discipline** — a fix and its regression test in one commit; stay on the working branch; never push; trace a recorded figure before overwriting it.
- **Criteria changes** — if an acceptance criterion turns out to be unachievable as written, weaken it explicitly with the reasoning inline and flag it in the summary. A run that silently redefines its own success conditions is worse than one that fails. This is in the template because the 2026-08-30 run did it correctly and unprompted, and that should not depend on luck.
- **Stop conditions and notification** — completion, budget exhaustion, blocked-on-a-human, no-progress, failed environment assertion. Every one of them notifies. **Silence must mean "still running".**
- **Final summary** — written at the top of the log, on the assumption that the human reads only that.

Two things the template must **not** carry forward from the original brief: the claim that checkout edits cannot affect a run (F7 — state the observed behavior instead, and have the run disclose its library root per A4), and any wording that treats `/loop` as durable.

### C3. A short template for the resume prompt

`templates/resume-prompt.md` — what the watchdog pastes into `claude -p`. Deliberately tiny, because it is re-sent on every recovery and its whole job is to point at the log:

> Read `RUN_LOG.md`, then continue the run it describes. Follow the brief at `<path>`. If an entry is in flight (a `begin` with no `end`), reconcile that one item first — in flight is not the same as failed. Then do one unit of work, update the log, and stop.

Note the last clause. Under a watchdog, each recovery does **one** unit and exits; the scheduler provides the loop. That is a materially simpler contract than a self-pacing session, and it is the one that survives.

### C4. A new skill — recommended, but not yet

The tempting move is `/agent-crew:unattended-run-brief`: hand it a work plan and constraints, and a team produces the brief. There is a plausible team for it — Project Planning plus the Devil's Advocate, or a new small team pairing the DevOps / Platform Engineer with the Devil's Advocate against `standards/unattended-run-readiness.md`.

**Recommendation: defer it until the template has been used twice.** The library's own `docs/optimization-plan.md` §3 already records that 4 of 12 teams are unreachable and 6 of 24 personas belong to no team — this project's failure mode is speculative growth, not missing capability. A template plus a standard is testable by a human in ten minutes; a skill is not testable until someone runs it. Build the skill when there is evidence that writing the brief by hand from the template is the slow part.

If it is built later, the readiness gates in A7 are its output format, and the deliverable is a filled-in copy of the C2 template with the gates evaluated.

---

## 5. What the corrected 2026-08-30 brief would have looked like

Concretely, against the same work, the changes are five:

1. A Scheduled Task firing `watchdog.py` every 20 minutes, installed and fired once before launch. **This one change converts the whole incident from a nine-hour outage into a twenty-minute pause.**
2. A budget reading "at most 9 review dispatches" alongside the existing cycle and wall-clock stops.
3. Cycle 1 doing the environment assertion, the log skeleton, the sub-cycle breakdown for item 4, and *one* of item 4's sub-cycles — with no review dispatch until the item was complete.
4. `runlog.py begin` / `end` around every cycle, giving a timestamped `Last cycle:` line from the first minute.
5. The paragraph asserting that checkout edits are inert replaced by an instruction to report the library root the skill actually loaded from.

Nothing else about that brief needed to change. The scope discipline, the environment assertions, the resume protocol, the commit-per-item rule, and the stop conditions were all well formed, and the run's outcome — three items, 86 tests to 253, nine findings fixed with regression tests — is the evidence for that.

---

## 6. Sequencing

Ordered so that each phase is useful alone and nothing depends on a later phase.

| Phase | Contents | Why here |
|---|---|---|
| **1 — Directives** | A1, A2, A3, A4, A5, A8 | Pure text, no new machinery, fixes every library defect the run actually found. Landable in one sitting. |
| **2 — The trigger** | B1 (`runlog.py`), B3 (`watchdog.py` and installers), C3 (resume prompt) | The nine-hour failure. Do not wait for the rest of the tooling — the log and the watchdog are the whole fix. |
| **3 — Guidance** | A7 (`unattended-run-readiness.md`), C1 (operator guide), C2 (brief template) | Turns phases 1–2 into something a person other than their author can use. |
| **4 — Hardening** | B2 (`preflight.py`), B4 (`lint.py`), A6 (threshold calibration) | Valuable, and none of it blocks a run. |
| **5 — Reassess** | C4 (the skill), the ~150-line number, whether cloud routines earn a first-class path | Explicitly gated on evidence from phases 2–4 rather than scheduled. |

**Validation for phase 2**, which is the phase most able to fail silently: kill the Claude session mid-cycle on purpose and confirm the watchdog restarts it, that the in-flight entry is reconciled rather than redone, and that the lockfile prevents a double start. An untested watchdog is indistinguishable from a working one until the night it matters — which is precisely the shape of the failure being fixed.

---

## 7. Open questions for a human

1. **Does agent-crew accept a `scripts/` runtime at all** (B0)? Everything in Workstream B follows from this and nothing else in the plan does. If the answer is no, Workstream C still stands and the mechanics move into the template as instructions — accepting that each run will implement them slightly differently.
2. **Which venv path is authoritative in photo-culling** — recorded as unresolved in [02-pre-run-review-session-record.md](02-pre-run-review-session-record.md) §7 and still unresolved. Not agent-crew's problem, but it will bite the next run there.
3. **Should the `[substrate:…]` override be a modifier or a separate concept** (A6)? It is proposed as separate because it targets the run rather than a persona, but the invocation syntax is the same shape and one reader may reasonably expect one mechanism.
4. **Are cloud routines available on the plans that matter here?** Untested. It changes nothing in the plan — the OS path is the default regardless — but it determines how prominent the alternative should be in C1.

---

## 8. What this plan does not claim

- **That a durable trigger prevents usage limits.** It does not. It converts a stop into a delay, and that is the entire benefit being claimed.
- **That the ~150-line threshold is wrong.** It is unvalidated, which is a different thing. A6 proposes measuring it, not moving it.
- **That the review gate was too expensive to be worth it.** Three dispatched runs found nine findings with regression tests, including two bugs in correct-looking code that no test could have caught. The argument here is for spending it deliberately, not for spending less of it.
- **That the checkout-versus-cache behavior is settled.** It was observed three times in one configuration. A4 proposes making every run state it, which is how it becomes settled.
