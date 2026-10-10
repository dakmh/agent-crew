# Decision record: execution substrate for teams

Date: 2026-08-27. Prompted by a real divergence: two Claude instances given comparable
"spawn a team" requests behaved differently — one ran in-context, one dispatched subagents. The
full analysis is preserved at `docs/reviews/2026-08-27-execution-substrate-analysis.md`; this
record covers what changed in the library as a result and why.

## The gap the analysis found

Nothing in agent-crew ever said *who executes a team*. `CLAUDE.md`'s skill flow described
*what* to do (load the team, load personas, run the interaction model) but never *who* — a
single context, or something dispatched. Read plainly, that's a recipe for one context to
follow, which is what one instance concluded; a machine with local memory files asserting
"running a team means spawning agents" concluded the opposite. Both were defensible; the
silence was the actual defect.

The analysis also surfaced a naming collision worth being explicit about going forward:
agent-crew's "team" (a persona grouping in `crew/teams/`) is unrelated to Claude Code's
experimental **agent-teams** feature (named `Agent` calls, `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`,
mailbox-based messaging between teammates) beyond sharing a word. Every reference to subagent
dispatch added below says so explicitly, to stop this from recurring.

## Decision

Per the analysis's taxonomy — in-context roleplay, one-subagent-per-team, one-teammate-per-persona
(experimental) — the choice made here is narrower than the analysis's own global recommendation
(adopt one-subagent-per-team everywhere). Scope, chosen directly by the project owner rather than
run as a formal team review: **prototype real per-persona subagent dispatch on one team —
Security & Standards Review — before touching anything else**, plus stand up a self-check loop
so this kind of drift gets caught going forward rather than found by accident again.

Security & Standards Review was the right first target, not an arbitrary one: its interaction
model has no cross-examination step — members review the same fixed artifact independently, and
only consolidation needs to see everyone's output. That's a stronger case than the analysis's
own "one-subagent-per-team" default: because no persona needs mid-run visibility into another's
draft, dispatching *each persona* as its own plain background subagent (`Agent` tool, no `name`,
not the agent-teams feature) gets true independence and true parallelism, at no cost to the
interaction model, which the analysis's own default (roleplay-inside-one-dispatched-subagent)
would not have delivered.

Teams with a cross-examination step (General Review, Implementation, and others) were
deliberately **not** touched. Plain subagents can't preserve a cross-examination step — isolated
subagents can't see each other's output without a message bus, which is exactly what the
experimental agent-teams feature provides and plain subagents do not. Migrating those is a
separate, larger decision, not a natural extension of this one.

## What changed

- **`skills/_conventions.md`** gained an authoritative "Execution substrate" section (this is the
  runtime-loaded home for the rule — `CLAUDE.md` only points to it, per the same lesson learned
  converting modifiers during the plugin conversion): in-context is the default and required
  fallback; a team may declare subagent dispatch for steps with no cross-persona visibility
  requirement; a run must disclose which substrate it used, so an in-context pass and a
  dispatched run are never visually indistinguishable to the reader.
- **`crew/teams/security-standards-review.md`** gained an Execution section stating the
  mechanics (one `Explore`-type subagent per active member, issued together; fallback to
  in-context below a ~150-line threshold or when `Agent` is unavailable) and an Assumptions
  section naming what this depends on, for the audit loop below to check.
- **A real inconsistency in that team file got fixed while restructuring it**, not papered over:
  the interaction model described the Senior Developer's review as independent (step 2), but the
  Notes section described them pressure-testing *other members' findings* — which requires
  seeing those findings first, i.e. not independent. Resolved in favour of independence (the
  team's actual design goal): the Senior Developer's independent notes are used by whoever
  consolidates, at consolidation time, to pressure-test the other findings for practicality.
- **`skills/security-review/SKILL.md`** now accepts a path/file reference (dispatched subagents
  can read a checkout themselves) alongside pasted code, and states that dispatch is the team's
  property, not a skill-level override.
- **`docs/capability-audit.md`** — the self-check mechanism: what to re-verify each cycle (plugin
  validation, skill registration, each team's Assumptions section against current harness
  capability, schema drift, decision-log health), and what to do with findings (always write a
  dated record via a PR; escalate with a GitHub issue only when something material changed;
  never push unreviewed commits to `main` from an unattended run).
- **A quarterly Routine** (`trig_01QpRs8CHWFsa33JpuJfdWc9`, Jan/Apr/Jul/Oct 1st) fires a fresh
  session that follows `docs/capability-audit.md` against this repo.

## Verified

- `claude plugin validate` (marketplace, manifest, skills, `--strict`) passes after every edit.
- A headless run against a small file correctly took the in-context fallback and disclosed it
  (`_Run in-context (single file, well under the ~150-line threshold for subagent dispatch)._`).
- A headless run against a 444-line file correctly dispatched three parallel `Explore` subagents
  (Security Engineer, Code Standards Reviewer, Senior Developer), disclosed the substrate and
  subagent count/type up front, and consolidated correctly — including surfacing that the
  Security Engineer and Senior Developer subagents converged independently on the same root
  cause (40 duplicated unauthenticated handlers), which is real signal from genuine isolation,
  not something the in-context model could produce the same way (a single session roleplaying
  both personas back-to-back always has the earlier persona's text in view).

## Open, deliberately not resolved here

- Whether other teams should move to subagent dispatch, and by which mechanism (plain subagents
  vs. the experimental agent-teams feature for teams with a cross-examination step) is future
  work, tracked via `docs/capability-audit.md`'s cadence rather than decided now.
- Whether a fired capability-audit session actually retains GitHub PR/issue tooling in a fresh
  session on this environment is unverified — the trigger's prompt was written defensively (fall
  back to a local file and say so, don't force a raw push) specifically because this wasn't
  confirmed before the trigger was created.
