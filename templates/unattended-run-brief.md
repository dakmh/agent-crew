# Unattended run brief — template

Fill in every `<angle-bracket>` field, delete what does not apply, and check the result against `standards/unattended-run-readiness.md` before launching.

**Two audiences, separated by the horizontal rule.** Everything above it is for the operator and is never sent to the agent. Everything below it is the brief, pasted as the run's prompt — paste the text rather than pointing at the file, so that the resume prompt and the brief cannot drift apart.

Each section carries a one-line note saying why it is there. Delete the notes; keep the sections.

---
---

## Operator preconditions

Check each one, and re-check all of them if the machine has rebooted. *(These are the gates from `standards/unattended-run-readiness.md`; they are checks, not prose to be trusted.)*

- [ ] **Trigger installed and fired once.** `scripts/install-watchdog-windows.ps1 -Project <path>` or `scripts/install-watchdog-cron.sh --project <path>`, then fire it manually and confirm it ran. An untested trigger is indistinguishable from a working one.
- [ ] **Machine will stay awake.** On Windows, `powercfg -q SCHEME_CURRENT SUB_SLEEP STANDBYIDLE` and `HIBERNATEIDLE` both read `0x00000000` on AC — **check the value, do not trust a note saying it was fixed.** On macOS, Energy Saver set to never sleep on power, or `caffeinate -s` for the duration.
- [ ] **Preflight assertions pass.** `python scripts/preflight.py --check` against `<project>/.agent-crew/preflight.json`.
- [ ] **Run log initialized.** `python scripts/runlog.py init --budget-hours <N> --max-dispatches <N>`.
- [ ] **Resume prompt in place** at `<project>/.agent-crew/resume-prompt.md`, from `templates/resume-prompt.md`, with its fields filled in.
- [ ] **Working branch cut**, not `main`, in every repo the run will touch.
- [ ] **agent-crew installed and enabled** (`claude plugin list`) if the run uses a review gate.
- [ ] **Run environment carried in `.claude/settings.local.json`**, not prefixed onto each command. Variables the run depends on belong in that file's `env` block, which puts them in the environment of every tool call in both VS Code and the CLI — a per-invocation prefix is one forgotten command away from a run that silently means nothing. It is gitignored and machine-specific, so a fresh clone or a second machine will not have it: create it as a precondition rather than assuming it survived.

---
---

**Unattended run — `<project>`, `<scope in one line>`.**

## Resume protocol — do this first, every wake

*(First because it is what makes a restart nearly free; the log is the resume artifact, not just a report.)*

Read `RUN_LOG.md`, then `<the work plan>`. **Do not read `<the large design documents>` in full** — grep them for the specific decision or section a task cites.

Check for an entry in flight — a `begin` with no `end`. **In flight is not the same as failed**: the work may have completed with the session dying before the outcome was recorded. Reconcile that one item against the tree first and record what you found, then continue.

## Environment — assert before any work

*(Every cycle, not once at launch, and by value rather than by claim.)*

Run `python <agent-crew>/scripts/preflight.py --check`. If any assertion fails, run `runlog.py stop --reason environment "<what failed>"` and stop. The environment is not what this run assumes and nothing after that point means anything.

**Verify the environment variables rather than setting them.** They come from `.claude/settings.local.json` and are already in every tool call's environment, so a cycle that sets them per invocation is testing something other than what will run unattended. Read them back by value — from a test-harness header line if the suite prints one — and stop if any names an unexpected path, or a lenient mode where the run assumed strict.

**Name the interpreter explicitly, and say why.** A project's virtualenv is usually not what a bare `python` resolves to: the system default may be a newer version with none of the project's compiled dependencies installed, so the suite fails to start or, worse, collects a different set of tests than the one the run's criteria were written against. Give the exact path — `./venv/Scripts/python.exe` on Windows, `./venv/bin/python` elsewhere — and state the version the environment was built from.

`<Name the destructive surface explicitly, and what proves it is out of reach — e.g. "the archive drive is detached by design: if `E:` resolves at all, stop and log it. Nothing in this run may touch `E:/00_Photos`.">`

## Budget

*(Denominated in the thing that actually runs out. A run can exhaust its account with 47 of 48 cycles unspent.)*

- **At most `<N>` review-team dispatches.** Record each one with `runlog.py spend --dispatches <n>`. This is the primary bound.
- Hard stops, as backstops: `<N>` cycles total, or `start + <N>h`, whichever comes first.
- Stop after `<N>` consecutive cycles with no test moving red→green and no new log entry beyond a restatement.

## First cycle is a canary

*(If the setup is going to fail, it should fail cheaply. The 2026-08-30 run made cycle 1 the largest of the whole run, which is exactly backwards.)*

Cycle 1: assert the environment, write the log skeleton and the planned sub-cycle breakdown for `<first item>`, do **one small unit** of work, commit, and stop. **No review dispatch in cycle 1.**

## Scope, in order

*(Ordered, with completion defined per item, so that "done" is not a judgment call at 3am.)*

`<Item 1>`, then `<item 2>`, then `<item 3>`. Do not start an item until the previous one's "Done when" criteria pass. `<Note anything explicitly carved out of scope, and why.>`

## Each cycle

*(Write-ahead: intent before the action, outcome after. A log written only after the work leaves uncommitted files with nothing explaining them.)*

1. `python <agent-crew>/scripts/runlog.py begin "<what you are about to do>"`
2. Do **one** unit of work. Run the suite.
3. Write what happened into `RUN_LOG.md` in prose — what landed, what is owed, what the next unit is. This is what a resuming session reads.
4. `python <agent-crew>/scripts/runlog.py end --status done|blocked|noop "<outcome>"`

Record a cycle that achieved nothing too: "attempted X, blocked by Y" is the point.

## Review gate

*(One dispatch per unit of work that becomes one commit — never per intermediate change. The dispatch is the most expensive single action available to this run.)*

Run `/agent-crew:security-review <git ref>` against each completed item's diff before committing it. The namespace prefix matters: bare `/security-review` resolves to an unrelated built-in skill.

Let the skill and its team drive themselves rather than restating their protocol. Record the disclosure line verbatim in the log — substrate, changeset size, and the library root it loaded from. **Do not assume which copy of the library is executing**; the disclosure line says, and the answer has been guessed wrong before. If you find a defect in a library file and the run is executing from a checkout, the fix is live — log it, fix it on a branch in that repo, and say whether you re-exercised it.

Record `runlog.py spend --dispatches <n>` for each dispatch.

## Commit discipline

*(These are `lessons.md` rules; they are here because an unattended run has nobody to catch a violation.)*

- A fix and its regression test go in one commit.
- Stay on the current branch in each repo. Never commit to `main`, never push.
- Before overwriting any figure recorded in the docs, trace where the original came from.

## If a criterion turns out to be wrong

*(A run that silently redefines its own success conditions is worse than one that fails.)*

If an acceptance criterion is unachievable as written, change it explicitly to an accurate weaker one, record the reasoning inline where the criterion lives, and flag it in the final summary. Do not quietly meet a redefined version.

## Stop conditions

*(All of them notify. Then silence means "still running", unambiguously.)*

Call `runlog.py stop` when any of these is true:

1. Everything in scope passes its "Done when" criteria with the suite green. — `--reason completed`
2. Everything remaining needs a human. Log the questions under `## Blocked` and stop; **do not guess at them.** — `--reason blocked`
3. Any budget above is exhausted. — `--reason budget`
4. An environment assertion failed. — `--reason environment`
5. The no-progress rule fired. — `--reason no-progress`

## Before stopping

Write a short summary at the top of `RUN_LOG.md`: what landed, what is owed, what needs a decision. **Assume the human reads only that.**
