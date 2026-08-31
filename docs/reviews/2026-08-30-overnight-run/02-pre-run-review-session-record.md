# Overnight run — lead-in record

A factual account of the session that produced the state the overnight run started from, written for handoff to the `agent-crew` project.

**What this is.** A chronological record of what happened, what was observed, and what was changed, in the session immediately preceding the unattended run. It exists so that the analysis of that run has a description of its starting conditions that was not reconstructed after the fact.

**What this is not.** Analysis, evaluation, or recommendation. Where an observation invites a conclusion, the observation is recorded and the conclusion is left to the analysis that follows. Nothing here judges whether a behavior was correct.

**Provenance and cutoff.** Written at the end of the lead-in session on 2026-08-30, from that session's own context, deliberately without re-reading any of the files it describes — so that the record reflects what was actually known and done at the time rather than the final state of the files. The record ends at the point where launch instructions were given. **The run had not been launched when this was written.** Any file content quoted below is quoted as it stood at the moment it was read or written during the session, not as it stands now.

---

## Session context

| | |
|---|---|
| Date | 2026-08-30, small hours (user described the close of the session as "well after 2am") |
| Harness | Claude Code, VS Code extension (`CLAUDE_CODE_ENTRYPOINT=claude-vscode`) |
| Model | Opus 5 |
| Session working directory | `c:\Users\dakmh\Documents\00_src` — the **parent** of the repo under review, not the repo itself |
| Repo acted on | `ai-tooling/photo-culling`, branch `claude/glob-fix-plan-and-sandbox` at session start |
| Invocation | `/agent-crew:security-review f9e8d6d` |
| Modifiers applied | None |
| Optional team members activated | None |

The session began with a direct user invocation of the review skill. This was **not** the in-run review gate described in `OVERNIGHT_PROMPT.md` — it was a manual pre-run invocation against an already-committed change, and the overnight run had not started.

Two environment facts recorded during the session, both relevant later:

- The skill's reported base directory was `C:\Users\dakmh\Documents\00_src\ai-tooling\agent-crew\skills\security-review` — the working checkout path.
- `~/.claude/settings.json` registers the `agent-crew` marketplace with `"source": {"source": "directory", "path": "C:\\Users\\dakmh\\Documents\\00_src\\ai-tooling\\agent-crew"}`, and `enabledPlugins` lists `agent-crew@agent-crew`.

`OVERNIGHT_PROMPT.md` states that the installed plugin is a snapshot copied into `~/.claude/plugins/cache/agent-crew/agent-crew/1.0.0` and that edits to the checkout will not affect `/agent-crew:*` behavior during a run. Both the observed base directory and the observed marketplace source are recorded here alongside that claim. Whether checkout edits take effect live was **not tested** in this session.

---

## Timeline

### 1. Skill and target resolution

Per the skill file, the session loaded `skills/_conventions.md`, `crew/teams/security-standards-review.md`, `standards/code-review-severity.md`, `standards/review-verdicts.md`, and the three core persona files. `agent-crew/lessons.md` was read at session start per the repo's session rules; it contained two rules (tests ship in the same commit as the code they cover; trace a recorded figure before overwriting it).

The skill was invoked with a bare commit SHA (`f9e8d6d`) and no repository. The session's working directory was the multi-repo parent, so the SHA did not resolve against any repo in scope. Resolution took two steps: a scan of top-level directories for git repos containing the object (no match), then a `find`-based scan to depth 4, which located it in `ai-tooling/photo-culling`.

The skill's *Context gathering* section names three accepted forms of context: pasted code, a described component, or "a path/file reference in the current checkout." A bare commit SHA with the session rooted above several repos was not among them.

### 2. Substrate selection

The diff was 2 files, +75/−7. The team file's fallback rule reads: "for a small, well-defined change (roughly: a single file or a diff under ~150 lines) or when the `Agent` tool is unavailable, collapse to in-context."

The run took the in-context branch and emitted the required disclosure line (`_Run in-context (small changeset — 2 files, +75/−7, under the team's ~150-line dispatch threshold…)_`) above the summary.

An ambiguity in that rule was recorded during the run: the parenthetical gives two clauses — "a single file" and "a diff under ~150 lines" — and this changeset satisfied the second but not the first. The clauses were read as alternatives. This was logged in the session output as a point to raise with `agent-crew`, with a suggested rewording ("or fewer than ~150 lines regardless of file count").

Because the in-context branch was taken, **this run produced no data on whether isolated subagents converge or diverge on the same finding** — one of the items `OVERNIGHT_PROMPT.md` asks to be recorded under `## agent-crew dogfooding notes`.

### 3. Context gathering

Files read or searched before the personas ran: `tests/conftest.py`, `tests/test_sandbox.py`, `tools/make_sandbox.py`, `OVERNIGHT_PROMPT.md`, the repo tree and test directory listing, a grep for both environment variables across the repo, a grep for all skip paths in the test suite, and a check for pytest configuration and CI (`pytest.ini`, `setup.cfg`, `pyproject.toml`, `tox.ini`, `.github` — none present).

`OVERNIGHT_PROMPT.md` was read as part of context gathering and became load-bearing for the review, because it supplied the operating constraints the code was assessed against — specifically the instruction that the T7 is detached by design, that a resolving `E:\` is a stop condition, and that nothing may touch `E:\00_Photos` or `E:\00_Camera\01_Staging`.

### 4. Review output

Three personas ran in character sequentially in one context: Security Engineer, Code Standards Reviewer, Senior Developer. Optional members were not activated — no regulated domain applied, and testability was not separately requested.

Findings were consolidated by the dispatcher and classified per the severity standard:

| Tier | Count |
|---|---|
| P0 | 0 |
| P1 | 1 |
| P2 | 3 |
| P3 | 5 |
| P4 | 4 |

The central finding: the reviewed commit added `PHOTO_CULLING_STRICT` to turn a skipped sandbox into a failure, but covered only one of the two branches an unset `PHOTO_CULLING_SANDBOX` can take. With the drive detached, resolution found no manifest and strict mode fired. With the drive attached, resolution fell back to a hardcoded default inside `E:\00_Camera`, found a manifest there, and returned it as usable — so strict mode never fired and the suite would run green against the live drive.

The security finding carried CVSS 6.1 (`AV:L/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:N`, CWE-1188) with an explicitly stated and justified adjustment from the default P2 to P1, per the standard's requirement that such adjustments never be silent. The `I:H` component was scored forward to the writer work in items 4–5 rather than at the then-current read-only state, and this was flagged in the finding text as the component driving the score.

Verdict: **Proceed with conditions**, with four enumerated conditions, two marked *before proceeding* and two *tracked during*. No dissent was appended.

A closing note was included in the review output listing the items `OVERNIGHT_PROMPT.md` asks to be recorded under `## agent-crew dogfooding notes`: substrate branch and diff size, whether the disclosure was emitted, subagent convergence (not available), whether P0–P4 classification was applied, and the team-file ambiguity described above.

### 5. Remediation

The user instructed that the T7 would not be reattached and asked for a branch and a fix. Work proceeded on `claude/sandbox-guard-hardening`, cut from `claude/glob-fix-plan-and-sandbox`.

Changes made:

- **`src/paths.py`** (new) — `ARCHIVE`, `STAGING`, `SANDBOX_ON_DRIVE`, and `protected_reason()`, a single guard shared by the builder and the fixtures.
- **`tests/conftest.py`** — the hardcoded default removed entirely; `PHOTO_CULLING_SANDBOX` made required; an unset variable returns before any filesystem call; protected trees refused outright; `pytest_report_header` added to print the resolved sandbox and mode on every run.
- **`tests/test_conftest.py`** (new) — the resolution tests, moved out of `test_sandbox.py` and rewritten. The prior test asserting that an absent variable falls back to the drive default was replaced with tests asserting refusal.
- **`tests/test_sandbox.py`** — resolution tests removed.
- **`tools/make_sandbox.py`** — rewired to the shared guard; its two path literals replaced with imports.
- **`pytest.ini`** (new) — `testpaths`, and `addopts = -ra` so skip reasons always appear.

Verification performed with the drive detached, against the Cloudlet sandbox: all four strict/lenient × good/bad-path combinations (pass, pass, exit 1, pass-with-15-skips), `make_sandbox.py --verify` (50 intact), and the builder's refusal of `E:\00_Photos`. Committed as **`3fdf302`**, fix and tests together per `lessons.md`.

**Incidental discovery during implementation.** The Bash tool was observed silently collapsing doubled backslashes in heredocs, which produced Python source where `E:\\00_Photos` became `E:\00_Photos` inside a non-raw docstring — making `\0` a null byte. Two module docstrings were affected and were corrected to raw strings with an assertion that no null bytes remained. From that point in the session, files containing Windows paths were written with the editor tools rather than Bash heredocs. The same collapse later caused one `--settings` invocation to fail with `Invalid JSON`.

### 6. Environment mechanism

The user asked whether the environment variable could be set within a VS Code session or whether the run should be launched from the command line.

Facts established by testing rather than assertion:

- The Bash tool in this session inherits the VS Code **extension host** process environment (`VSCODE_ESM_ENTRYPOINT=vs/workbench/api/node/extensionHostProcess`). No `PHOTO_CULLING_*` variable was set.
- An `env` block in a settings file passed via `--settings <file>` reached the Bash tool environment. Confirmed with a probe returning `C:/PROBE/it-works`.
- The same `env` block in an auto-discovered `.claude/settings.local.json` reached the Bash tool environment. Confirmed with a probe returning `C:/PROBE/auto-discovered`. The probe file was deleted afterward.
- `.claude/` was **not** gitignored in this repo, though `.vscode/` was.

One claim was recorded as reasoning rather than test: that VS Code's `terminal.integrated.env.windows` would not reach the Bash tool, on the grounds that the tool spawns from the extension host rather than from a VS Code integrated terminal. This was explicitly flagged in-session as not directly tested, because testing it would have required editing user settings and restarting the editor.

### 7. Configuration and document changes

The user asked for the changes to be made, for `OVERNIGHT_PROMPT.md` to be updated, and for one-liner commands for anything requiring an elevated PowerShell console.

A check of the overnight preconditions found **`HIBERNATEIDLE` on AC at `0x00001518` (90 minutes)**, while `OVERNIGHT_PROMPT.md` stated that the preconditions were "all currently satisfied" and required `0x00000000`. `STANDBYIDLE` on AC was already `0x00000000`.

Changes made:

- **`.claude/settings.local.json`** (new, gitignored) — `env` block setting `PHOTO_CULLING_SANDBOX` to the Cloudlet path and `PHOTO_CULLING_STRICT` to `1`.
- **`.gitignore`** — added `.claude/settings.local.json`.
- **`OVERNIGHT_PROMPT.md`** — the environment paragraph rewritten to say the variables come from settings and must **not** be set per invocation, replacing that with a single verification against the pytest header line and a stop condition if it reads `lenient` or names another path. The preconditions block lost the "all currently satisfied" claim, gained a bullet for the settings file, and gained a dated note that `HIBERNATEIDLE` had been found non-compliant despite the list's prior claim, with the fix command inline.
- **`CLAUDE.md`** — the `tests/conftest.py` row, which described fixtures that only skip, updated for the required variable and strict mode; rows added for `tests/test_conftest.py` and `src/paths.py`.

Committed as **`71951af`** (tracked files only — `.claude/settings.local.json` is ignored and `OVERNIGHT_PROMPT.md` was and remains untracked).

The elevated-PowerShell answer given was that only `powercfg` required elevation; the environment variables did not, being handled by the settings file. User-scope and machine-scope `SetEnvironmentVariable` one-liners were supplied as unrecommended alternatives.

A secondary inconsistency was recorded and deliberately **not** changed: `CLAUDE.md` directs the suite to be run with a venv at `ai-tooling/photo_pipeline/ai_photo_culling/venv/Scripts/python.exe`, while `OVERNIGHT_PROMPT.md` specifies `./venv/Scripts/python.exe`. Both paths were confirmed to exist. The repo-local venv ran the full suite green including the lxml-dependent tests. Which is authoritative was not determined.

### 8. Launch readiness

A final check established:

- `HIBERNATEIDLE` and `STANDBYIDLE` on AC both `0x00000000` — the user had applied the fix.
- `E:\` did not resolve; the T7 was detached.
- The sandbox verified clean and the suite ran green under strict mode.
- A fresh non-interactive session launched **from the repo** printed `sandbox [strict]: C:\Cloudlet\01_SandboxedTests\photo-culling-sandbox` in the pytest header, with nothing set per invocation.
- A fresh non-interactive session launched **from the parent directory** (`00_src`, this session's own root) did **not** receive the variables: `printenv` returned empty with `EXIT=1`. `.claude/settings.local.json` is project-scoped and was not loaded from the parent.

The last point was surfaced to the user before launch, with the note that the resulting failure mode is safe under the new code — no fallback, so the suite skips rather than touching the drive — but that it would skip all 15 sandbox tests and report green, and that the header check written into `OVERNIGHT_PROMPT.md` is what would catch it.

Launch instructions given: open the tab with `photo-culling` as the working directory; invoke `/loop` with no interval; paste the prompt text below the horizontal rule rather than pointing at the file, on the grounds that `/loop` re-injects its prompt each wake and that the material above the rule is addressed to the operator rather than the agent. A shorter file-pointer alternative was offered with an explicit clause excluding the preconditions section.

The branch question was raised: the run would inherit `claude/sandbox-guard-hardening` under the prompt's "stay on the current branch" rule, placing items 4–6 on the same branch as the guard work. A command to cut a separate branch was offered. **The record ends here; which option was taken is not known to this session.**

---

## Artifacts

| Artifact | State at cutoff |
|---|---|
| `3fdf302` | Committed — sandbox resolution hardening, fix and tests together |
| `71951af` | Committed — settings mechanism, `.gitignore`, `CLAUDE.md` |
| `.claude/settings.local.json` | Created, gitignored, verified loading from the repo root |
| `OVERNIGHT_PROMPT.md` | Updated, untracked (as it was before the session) |
| `pytest.ini`, `src/paths.py`, `tests/test_conftest.py` | Created, committed in `3fdf302` |
| Branch `claude/sandbox-guard-hardening` | Current, not merged, not pushed |

## Items carried forward for `agent-crew`

Recorded as observations from this session, without evaluation:

1. The skill was invoked with a bare commit SHA from a directory containing multiple repos. The skill's context-gathering section does not name that form, and resolution required an ad-hoc multi-repo search.
2. The team file's in-context fallback threshold reads as two clauses ("a single file **or** a diff under ~150 lines") that this changeset satisfied only partly. They were read as alternatives.
3. The substrate disclosure was emitted as required.
4. P0–P4 classification was applied per the standard, including the security protocol's CVSS requirement and a stated non-silent P-value adjustment.
5. The in-context branch means no subagent convergence/divergence data exists for this run, though `OVERNIGHT_PROMPT.md` asks for it.
6. The skill's reported base directory was the working checkout, and the marketplace is registered as a directory source, alongside `OVERNIGHT_PROMPT.md`'s statement that the installed plugin is a cached snapshot. Live-edit behavior was not tested.
7. `OVERNIGHT_PROMPT.md`, a document written for the run, became primary review context — the code's threat model was assessed against its operating constraints.

## Not covered by this record

- The overnight run itself, which had not started.
- Whether the separate branch was cut before launch.
- Any file state later than the cutoff; nothing was re-read for this write-up.
- Whether checkout edits to `agent-crew` take effect live during a run.
- Which of the two venv paths is authoritative.
