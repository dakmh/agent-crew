# Lead-in to the photo-culling overnight run

**Date:** 2026-08-30
**Scope:** the setup session that produced `photo-culling/OVERNIGHT_PROMPT.md`, from first request to the point the prompt was finalized.
**Status:** factual record only. No analysis, no recommendations. Written from the session transcript without re-reading files changed after the cutoff, so that the account describes what was known at each decision point rather than what turned out to be true later.

**Cutoff.** This record ends when `OVERNIGHT_PROMPT.md` was written and the stale scratchpad copy deleted. The overnight run itself, and any file changed by it, are outside this document. `tests/conftest.py` in particular was modified after the cutoff; this record describes only the version committed as `f9e8d6d`.

---

## What was asked

The session opened with three requests: confirm the local agent-crew checkout was on the PR10 / `vki4d6` version, read `WORK_PLAN.md` — specifically its *Before running the tool on real data* section — so that no real photographs were touched, and evaluate a proposal. The proposal was to detach the T7 (which holds the real archive and staging trees) and point testing at a new sandbox inside a microSD folder-mount at `C:\Cloudlet\01_SandboxedTests`, on the reasoning that speed did not matter for the intended work.

The goal behind it emerged over the session: an unattended overnight run, driven by agent-crew where possible in order to dogfood the PR10 changes, that paced itself around usage limits, kept context small, and stopped on its own.

## What was found before any work started

**agent-crew version.** Branch `claude/agent-crew-local-install-vki4d6` at `a807483`, "Add execution-substrate rules and a subagent-dispatch prototype", level with `origin` at 0 ahead / 0 behind. PR #10 open, last updated 2026-08-27. `lessons.md` carried two uncommitted rules not present in the PR — the tests-ship-with-code rule and the trace-figures-before-overwriting rule — both of which went on to constrain the session's own commit discipline.

**agent-crew was not registered as a plugin.** There was no `~/.claude/plugins/config.json` and no marketplace entry. The library reached the session only through the `@`-import in the global `CLAUDE.md` — the legacy path that the index section of that file exists to serve. Two consequences were established at this point: `/agent-crew:security-review` would not resolve, and bare `/security-review` would resolve to the unrelated built-in skill of the same name.

**No skill invokes the Implementation team.** The ten skills present are all design, review, or planning: `review-proposal`, `security-review`, `technical-discovery`, `feature-design`, `architecture-design`, `project-planning`, `mobile-feature-design`, `mobile-implementation-review`, `release-planning`, plus `_conventions.md`. `crew/teams/implementation.md` is fully specified — six members, a parallel-analysis-then-integration model, a readiness assessment — but nothing reaches it. This determined the shape of the whole plan: agent-crew could not drive the coding, only gate it.

**The dispatch prototype is a single worked example.** `crew/teams/security-standards-review.md` is the only team declaring subagent dispatch, with a stated threshold of roughly 150 lines or a single file below which it collapses to the in-context fallback. The `a807483` commit message records that this was verified by hand twice: once below the threshold and once against a 444-line file. It was noted during planning that items 4 and 5 of the work plan would produce diffs on both sides of that threshold, so an overnight run would exercise both branches and the disclosure rule without being asked to.

**Detaching the T7 removes work from scope.** Item 4's drift-scan criterion requires a pass over the archive's 3,600 `.cos` files, and `tools/survey_sidecars.py` defaults to `E:\00_Photos`. Neither can run with the drive out. This was carved out explicitly rather than left to be discovered mid-run.

## The sandbox relocation

The relocation needed no code change. `tools/make_sandbox.py` already accepted `--source` and `--dest`, and `tests/conftest.py` already read `PHOTO_CULLING_SANDBOX` with the T7 path only as a fallback. A grep for `E:` across the repo found literals only in those two defaults and in `survey_sidecars.py`; nothing under `src/` hardcoded a drive.

One sequencing constraint governed the order of operations: the builder sources from `E:\00_Camera\01_Staging`, so the sandbox had to be built while the T7 was still attached. It was built directly to the destination rather than built on the T7 and copied, so that the manifest recorded the correct root.

Result: 50 files, 575 MB, at `C:\Cloudlet\01_SandboxedTests\photo-culling-sandbox`. `--verify` reported 50 intact, 0 changed, 0 missing. All ten read-layer cases were present under the dated folder, and the staging half carried all four folder shapes.

A filesystem difference was noted and dismissed: the T7 is exFAT and Cloudlet is NTFS, but both are case-insensitive, so the case-collision case the sandbox models behaves identically. The observation that a folder-mounted volume has no drive letter was recorded as relevant to work plan item 8, not to the items in scope.

The strongest argument for the plan was recorded as a property of detachment rather than of the sandbox: with `E:` unplugged, `E:\00_Photos` does not resolve at all, so the guard against reaching real data stops being a code check and becomes a missing path.

## The environment problem

The test suite could not run at all before this session. The default `python` is 3.14 and lacked lxml, yaml, cv2, PIL, rawpy, torch, and tqdm — everything but numpy and pytest. Python 3.13 held the full runtime set but lacked the dev dependencies, pytest and black.

A virtualenv was created from 3.13 with `--system-site-packages` and pytest and black installed into it, chosen over installing into the global 3.13 site-packages because it does not mutate a shared interpreter, and over a clean venv because it avoids re-downloading torch. `venv/` was already covered by `.gitignore`.

The suite then passed 61 tests against the new sandbox.

**A control was run rather than trusting the pass.** Because the T7 was still attached at that moment, a silent fallback to the old default would also have produced a green run. Pointing `PHOTO_CULLING_SANDBOX` at a nonexistent path produced 46 passed and 15 skipped, establishing that the environment variable, not the fallback, was selecting the tree.

## First draft of the prompt, and its two stated weaknesses

The mechanism choices were settled before any prompt text was written.

`/loop` with no interval was chosen for pacing: dynamic mode, where the session calls `ScheduleWakeup` itself and picks a delay clamped to 60–3600 seconds. The `ralph-loop` plugin was present in the official marketplace directory but not enabled, and was rejected on shape — a Stop-hook re-feeding an identical prompt in one session grows context without bound and has no stopping condition beyond a completion string, which is the opposite of what was wanted.

One limit was stated plainly at this point rather than worked around: **no tool reports remaining usage allocation**, so "stop when usage runs out" is not detectable. The compensating measure chosen was a durable state file written after every unit of work, so that any successor session resumes cheaply — recorded as the real answer to the usage question, with pacing as secondary.

Context minimization and the dogfooding goal were found to reinforce each other rather than compete: dispatched personas read a diff in isolated contexts and return findings, so the driving session never loads the review. The prompt therefore instructed the run to read only `WORK_PLAN.md` and the log at each wake, and to reach the three design documents by targeted grep for a cited decision number.

The first draft was delivered with two weaknesses named by the author rather than discovered by the user:

1. Nothing forced the sandbox environment variable to be set. If the loop fired in a shell without it, the sandbox tests would skip silently and the suite would report green against nothing.
2. Stopping condition 3 read "progress has stalled", a judgment the session would be making about its own work — precisely the judgment that degrades as context fills.

Both were accepted for fixing.

## The strict-mode guard

`PHOTO_CULLING_STRICT=1` was added to turn the skip into a failure. The strict/lenient decision was moved out of the fixture into `resolve_sandbox()` and `strict()` so it could be tested directly rather than through a nested pytest run.

Four scenarios were verified, with exit codes checked separately because the strict path surfaces as errors rather than failures — a session fixture raising, not a test:

| Scenario | Result | Exit |
|---|---|---|
| Sandbox present, lenient | 77 passed | 0 |
| Strict, bad path | 62 passed, 15 errors | 1 |
| Lenient, bad path | 62 passed, 15 skipped | 0 |
| Strict, good path | 77 passed | 0 |

Sixteen regression tests shipped in the same commit, per the `lessons.md` rule; the suite went from 61 to 77. One incidental finding: `tests/` is a package, so the meta-tests import the fixture module as `from tests import conftest`; a bare `import conftest` fails at collection.

Committed as `f9e8d6d` on `claude/glob-fix-plan-and-sandbox`. Not pushed.

## Power, which would have ended the run

The user asked whether sleep needed handling or was already managed. It was not managed. The active scheme was Balanced, and on AC power: sleep after 15 minutes (`STANDBYIDLE` = 0x384), hibernate after 90 minutes, disk idle 30 seconds. The system reports S0 Low Power Idle rather than S3, and USB selective suspend was enabled.

The interaction that mattered: a background CLI does not hold off the Windows idle timer, which is driven by user input and by processes explicitly requesting `ES_SYSTEM_REQUIRED`. Since the recommended wake delays were 1200–1800 seconds, the first long delay would have put the machine to sleep with nothing scheduled to wake it. This was not an edge case but the normal path of the plan as it stood.

The user applied `standby-timeout-ac 0` and `hibernate-timeout-ac 0`; both were confirmed reading `0x00000000` afterward. USB selective suspend was left enabled and recorded as a possible cause of spurious sandbox-not-found failures, since Cloudlet is a microSD behind a reader.

## The cycle cap

An active coding cycle was estimated at roughly 10 minutes of wall clock — one work unit, a suite run of a few seconds, a log update — with the minimum 60-second delay during productive work, since nothing external is being waited on. Eight hours divided by that gives **48 cycles**.

The cap was deliberately set generous on the reasoning that it is a runaway guard and should never be what stops a healthy run; conditions 1 and 2 should. A separate and much tighter counter was added for stalls — four consecutive cycles with no test moving red to green and no new log entry — replacing the fuzzy self-judgment flagged in the first draft. A UTC start timestamp plus an eight-hour wall-clock stop was added as a third bound, because delays stretching to 3600 seconds during a depleted window would let 48 cycles span far more than eight hours.

## Plugin registration

Registering the plugin was raised as an optional change with a stated reason: without it the overnight run would dogfood only the subagent-dispatch half of PR10 and none of the plugin conversion. It was proposed for doing while the user was awake rather than discovering a failure mid-run. The user agreed.

`claude plugin validate .claude-plugin/plugin.json` passed with one warning — `CLAUDE.md` at the plugin root is not loaded as project context, and the validator suggests shipping context as a skill instead.

`claude plugin marketplace add .` was rejected as an invalid source format; `./` was accepted. The marketplace registered as a Directory source pointing at the checkout.

`claude plugin install agent-crew@agent-crew` failed the first time with `EBUSY: resource busy or locked` renaming out of `~/.claude/plugins/cache/temp_local_1788067804377_hxr7rc`. Removing the stale temp directory and retrying succeeded: version 1.0.0, user scope, enabled.

**The install is a copy, not a link.** The tree was copied to `~/.claude/plugins/cache/agent-crew/agent-crew/1.0.0`, which reports an empty `LinkType` — a snapshot, not a junction. The marketplace points at the checkout; the install does not. Edits to the checkout therefore do not change `/agent-crew:*` behavior until reinstall. This was folded into the prompt as an explicit instruction, on the reasoning that a run told to log team-file ambiguities would otherwise edit a file, observe no change, and hunt for a nonexistent bug.

**Registration could not be smoke-tested from the setup session.** Skills register at session start, so the newly installed commands were unavailable to the session that installed them. Verifying `/agent-crew:security-review` from a fresh session was recommended before launch, using the ~60-line `f9e8d6d` diff so that the cheap in-context branch would be exercised first. Whether that check was performed is outside this record.

## Two corrections made during the session

Recorded because they are part of the lead-in, not commentary on it.

1. The first draft of the prompt was described as having been written to a scratchpad file. It had not been; it existed only in the reply. The file was created a turn later.
2. Adding the marketplace as a Directory source was described as meaning edits stay live. That was wrong, and was corrected on inspecting the install as described above.

## Final state at cutoff

`photo-culling/OVERNIGHT_PROMPT.md`, untracked, at the repository root alongside `WORK_PLAN.md`. It carries a preconditions block — sandbox built and verified, T7 detached, both AC power timeouts at zero, plugin enabled — followed by the prompt itself: cycle budget, resume protocol, environment assertions, scope with the drift scan carved out, the review gate as `/agent-crew:security-review`, the dogfooding notes to record, the snapshot caveat, commit discipline, per-cycle actions, and three stopping conditions.

The review-gate paragraph was rewritten once, after registration, to stop restating the team's dispatch mechanics. The reason given was that duplicating the team file is the thing agent-crew's own conventions say a skill must not do; the prompt was changed to let the team drive itself and have the run verify the disclosure instead.

The scratchpad copy was deleted so that two versions could not drift.
