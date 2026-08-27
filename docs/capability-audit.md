# Capability audit protocol

Purpose: agent-crew's design makes concrete bets on what the Claude Code harness can do —
plugin schema, subagent dispatch, tool scoping. Those bets are dated the moment they're made;
this doc is what a session (scheduled or manual) follows to re-check them without assuming the
outcome.

Run this: quarterly via the scheduled Routine (see below), or any time on request ("run a
capability audit"). Each run produces one dated record in `docs/reviews/`; nothing else changes
unless a human acts on that record afterward.

## What to check

1. **Plugin validation.** `claude plugin validate .claude-plugin/plugin.json --strict` and
   `claude plugin validate skills --strict` from a checkout. Note any new warnings — a new
   reserved directory name, a changed frontmatter requirement, anything not seen in prior runs.

2. **Skill registration.** Fresh headless session, `claude --plugin-dir <checkout>`, list
   registered skills, confirm all nine (or however many then exist) appear under `agent-crew:`.
   Confirm no new built-in command collides with one of agent-crew's command names (the way
   `/security-review` did before namespacing).

3. **Subagent dispatch assumptions.** Re-read every team file's `## Assumptions` section (only
   `security-standards-review.md` has one as of 2026-08-27; more may exist by the time this
   runs). For each: is the named capability still true? Specifically worth checking every run:
   - Is `Explore` still a read-oriented built-in subagent type with no Edit/Write? Has a
     narrower, genuinely read-only type appeared that would be a strict improvement?
   - Has a way appeared to register a *named*, tool-scoped subagent directly from a plugin's
     persona files (`crew/stable/*.md`) without colliding with the reserved `agents/` directory
     semantics that forced the `agents/` → `crew/` rename? If so, that's a strict upgrade path
     for any team currently faking per-persona dispatch through generic `Explore` calls.
   - Has `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` stabilized (left experimental, or gained wider
     default availability)? If so, it's worth reconsidering for teams that *do* have a
     cross-examination step (General Review, Implementation, and others) — those can't use plain
     subagent dispatch (see `skills/_conventions.md` → Execution substrate for why), but a
     message-passing teammates model might let them get real per-persona independence without
     losing cross-examination, the way `security-standards-review.md` already does for its
     independent-review step. Don't adopt this speculatively; note it as a candidate.

4. **Command/skill schema drift.** Skim the current plugin/marketplace/SKILL.md schema docs
   against what agent-crew's manifests actually declare. Flag anything deprecated, anything new
   that would reduce boilerplate (e.g. a cheaper way to express the loading preamble every
   SKILL.md currently repeats by hand).

5. **Decision log health.** Are there consequential changes to the library since the last audit
   that *don't* have a `docs/reviews/` record? If so, that's a process gap worth naming even
   though it's not a capability question.

## Output

Write `docs/reviews/YYYY-MM-DD-capability-audit.md`: what was checked, what changed since the
last audit (if there was one — `git log --oneline -- docs/reviews/*capability-audit*` finds it),
and what — if anything — needs action.

**The dated record always gets written, on a branch, via a PR — never a direct commit to
`main`.** Even a "nothing changed" run is worth having on record (it's what lets the *next*
audit answer "what changed since last time" cheaply), but an unattended run doesn't get to land
on `main` unreviewed: branch, commit the record, open a PR, done. Merging it is a human decision.

**Escalate separately, and only when something is material.** If something material changed (a
strict upgrade path opened up, an assumption broke, a schema deprecation needs a fix before it
becomes a hard failure), *also* open a single GitHub issue on `dakmh/agent-crew` summarizing it,
tagged so it's easy to find later, referencing the audit PR. Don't act on the finding itself —
issue and PR are both for a human to pick up. Nothing changed → the record-only PR is the whole
output; don't open an issue just to say so.

## Cadence rationale

Quarterly, not more often: harness capabilities relevant here (plugin schema, subagent
primitives, experimental-feature graduation) move on the order of months, not weeks. A tighter
cadence would mostly produce no-op runs. If a capability change is big enough to matter before
the next scheduled run, it'll usually surface some other way (a validate failure, a skill that
stops registering) rather than needing to wait for the audit to notice it.
