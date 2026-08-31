# Overnight autonomous session — prompt

The prompt for an unattended run against `WORK_PLAN.md` items 4–6. Launch with `/loop` and **no interval**, so the session self-paces via `ScheduleWakeup` rather than firing on a fixed clock, then paste everything below the rule.

Preconditions — check each one before launching, and re-check them all if the machine has rebooted:

- The sandbox exists at `C:\Cloudlet\01_SandboxedTests\photo-culling-sandbox` (`tools/make_sandbox.py --verify --dest <path>` confirms it), and the T7 is detached.
- `.claude/settings.local.json` exists and carries the `env` block setting `PHOTO_CULLING_SANDBOX` to that sandbox and `PHOTO_CULLING_STRICT` to `1`. It is gitignored and machine-specific, so a fresh clone will not have it. This is what puts the variables in the environment of every tool call, in VS Code and the CLI alike — nothing sets them per invocation any more.
- `powercfg -q SCHEME_CURRENT SUB_SLEEP STANDBYIDLE` and `HIBERNATEIDLE` both read `0x00000000` on AC. A background CLI does not hold off the idle timer, so a non-zero value here ends the run at the first long wake delay. **`HIBERNATEIDLE` was found at `0x00001518` (90 minutes) on 2026-08-30 despite this list previously claiming otherwise — check the value, do not trust the claim.** Fix from an elevated PowerShell with `powercfg /setacvalueindex SCHEME_CURRENT SUB_SLEEP HIBERNATEIDLE 0; powercfg /setactive SCHEME_CURRENT`.
- `agent-crew@agent-crew` is installed and enabled (`claude plugin list`).

---

**Overnight autonomous session — photo-culling items 4–6.**

**Cycle budget.** Record a UTC timestamp on the first line of the log on your first cycle. Hard stops: 48 cycles total, or `start + 8h`, whichever comes first. Stop after 4 consecutive cycles with no test moving red→green and no new log entry beyond a restatement.

**Resume protocol (do this first, every wake).** Read `OVERNIGHT_LOG.md` if it exists, then `WORK_PLAN.md`. Do not read `DESIGN.md`, `TECHNICAL_DESIGN.md` or `ARCHIVE_SURVEY.md` in full — grep them for the specific decision number a task cites. If `OVERNIGHT_LOG.md` does not exist, create it with sections `## Done`, `## In progress`, `## Blocked — needs Dak`, `## agent-crew dogfooding notes`.

**Environment — assert before any work.** `PHOTO_CULLING_SANDBOX` and `PHOTO_CULLING_STRICT` come from `.claude/settings.local.json` and are already in the environment of every tool call, so **do not set them per invocation** — verify them once instead. On your first pytest run, read the header line pytest prints: it must say `sandbox [strict]: C:\Cloudlet\01_SandboxedTests\photo-culling-sandbox`. If it says `lenient`, or names any other path, or reports a problem, **stop and log it** — the environment is not what this run assumes and nothing after that point means anything. Strict mode makes an unusable sandbox a failure rather than a silent skip, and resolution has no fallback path at all, so a green run means something. Use `./venv/Scripts/python.exe`, never bare `python` (3.14 is the default and lacks lxml/torch/rawpy). The T7 is detached by design: if `E:\` resolves at all, **stop and log it**. Never write outside the sandbox path. Nothing in this run may touch `E:\00_Photos` or `E:\00_Camera\01_Staging`.

**Scope, in order:** items 4, then 5, then 6. Do not start an item until the previous one's "Done when" criteria pass. **Item 4's drift-scan criterion is explicitly out of scope** — it needs the detached archive; build the scanner, unit-test it against the sandbox's `COS_AGREES`/`COS_DISAGREES` cases, and log the archive run as owed. Item 5 includes turning `write_shared_xmp` off in `ai_culling_config.yaml`.

**Review gate — dogfood agent-crew.** Run `/agent-crew:security-review` against each completed item's diff before committing it. The namespace prefix matters: bare `/security-review` resolves to an unrelated built-in skill of the same name. Let the skill and its team drive themselves rather than restating their protocol — in particular, obey the team's own substrate rule (parallel `Explore` subagents above roughly 150 lines of diff, in-context fallback below it) and check that the run discloses which substrate it used, as `skills/_conventions.md` requires it to.

Record in `## agent-crew dogfooding notes`: which substrate branch triggered and at what diff size, whether the disclosure was actually emitted, whether isolated subagents converged or diverged on the same finding, whether P0–P4 classification was applied per `standards/code-review-severity.md`, and any point where a team or skill file was ambiguous about what to do.

**The installed plugin is a snapshot, not a live link.** `claude plugin install` copied the checkout into `~/.claude/plugins/cache/agent-crew/agent-crew/1.0.0`. Fixes you make in `../agent-crew/` will **not** change the behavior of `/agent-crew:*` for the rest of this run, because the copy is what executes. So: log the defect, fix it in the checkout on an agent-crew branch if the fix is clear, and do not re-run the skill expecting different behavior or go hunting for why the edit had no effect. Reinstalling mid-run is out of scope.

**Commit discipline.** A fix and its regression test go in one commit (`agent-crew/lessons.md`). Stay on the current branch in each repo, never commit to main, never push. Before overwriting any figure recorded in the docs, trace where the original came from.

**Each cycle:** do one unit of work, run the suite, update `OVERNIGHT_LOG.md`, then schedule the next wake. Update the log even on a cycle that achieved nothing — "attempted X, blocked by Y" is the point. Use `noop: true` only when genuinely nothing changed.

**Stop — call ScheduleWakeup with `stop: true` — when any of these is true:**

1. Items 4, 5 and 6 all pass their "Done when" criteria (minus the carved-out drift scan) with the suite green.
2. Everything remaining needs Dak's input. The known ones are in `WORK_PLAN.md` → *Open questions to settle*: which sidecar form is canonical (deferred by decision, gates the sync tool), other raw formats, video. **Do not guess at these** — log them under `## Blocked — needs Dak` and stop.
3. Either cycle budget above is exhausted.

Before stopping, write a short summary at the top of `OVERNIGHT_LOG.md`: what landed, what's owed, what needs a decision. Assume I read only that.
