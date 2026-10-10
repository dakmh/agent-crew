# Review record: agent-crew installation mechanism

Date: 2026-08-18 · Team: General Review (`agents/teams/general-review.md`) · Skill protocol: `/review-proposal`
Context: a self-review, dogfooding the library on its own packaging decision.

## Proposal

Give agent-crew a low-friction, high-availability, minimal-context installation option. Today the
only discovery mechanism is a 65-line `CLAUDE.md` imported wholesale into a consumer's
`~/.claude/CLAUDE.md` — always in context, hand-wired per machine, and dependent on the model
following an index. Skills have no frontmatter, so the harness never registers them.

Options considered:

- **A — Claude Code plugin, self-hosted marketplace in this repo.** Add
  `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` (plugin `source: "./"`).
  Restructure `skills/<name>.md` → `skills/<name>/SKILL.md` with `name` + `description`
  frontmatter. Teams, personas, standards, and `skills/_conventions.md` stay as shared reference
  files addressed from skill bodies via the plugin root. Install:
  `/plugin marketplace add dakmh/agent-crew` then `/plugin install agent-crew@agent-crew`.
- **B — Trim the import.** Shrink `CLAUDE.md` to the ~20-line index; keep the per-machine `@` import.
- **C — Install script.** A script that copies/links skills into `~/.claude/skills/` with
  frontmatter added at install time.

---

### 🏛️ System Architect — structure, boundaries, longevity

The core defect in the status quo is that *discovery* and *content* share one channel: the
always-on import exists only because nothing else registers the skills. Any fix that keeps
discovery model-dependent (B) leaves the failure mode in place — the index works until the model
doesn't follow it, and it costs 65 lines on every request whether or not a skill is in play.

A is the only option with the right ownership boundaries. The harness owns discovery
(deterministic registration, JIT body loading), the repo owns content, and the marketplace owns
distribution and updates (`/plugin marketplace update` gives consumers a pull-based update path —
that's the "high availability" ask answered structurally, not by convention). C gets JIT loading
but forks the content: copied skills drift from the repo the moment either changes, and symlinks
don't survive Windows consumers well — the primary consumer environment named in the handoff is a
Windows path (`S:\`).

Two structural risks in A, both addressable:

1. **The repo's `agents/` directory collides with the plugin layout's meaning of `agents/`** —
   the plugin scanner treats that directory as subagent definitions. Twenty-four persona files
   with no frontmatter will be scanned as subagents. This must be neutralized explicitly in
   `plugin.json`, not left to whatever the scanner happens to do.
2. **Path resolution changes.** Installed, the working directory is the consumer's project, not
   this repo; every cross-reference (`agents/teams/…`, `skills/_conventions.md`,
   `standards/…`) must resolve from the plugin root. This needs one stated convention, applied
   everywhere, that still works in a plain checkout of this repo.

This works if the skill descriptions carry the triggering load the index used to carry. If they
don't, we've traded a weak discovery mechanism for a silent one.

---

### 😈 Devil's Advocate — assumptions under stress

I want to stress-test one assumption: *"convert to a plugin and friction goes away."* The
conversion moves friction; whether it shrinks depends on three things nobody has verified end to
end:

- **Command names change.** `/review-proposal` becomes `/agent-crew:review-proposal`. The handoff
  calls the bare commands "muscle memory" and says to preserve them exactly — a plugin cannot,
  by design. That's also the fix for the `/security-review` builtin collision, so it's a good
  trade, but it must be sold as a trade, not slipped in.
- **Descriptions are now a single point of failure.** With the index gone, a skill nobody
  triggers is indistinguishable from a skill that doesn't exist. What's the check? (Proposed
  answer: trigger-phrase-heavy descriptions plus a listed-command table in README — acceptable,
  but the first fresh-session verification is a hard condition, per the handoff's own gotcha
  about registration being decided at session start.)
- **The `lessons.md` session rule silently dies** when the always-on import goes. For consumers
  it was never relevant; for *this repo's* development sessions it must survive in the repo's own
  `CLAUDE.md`, which still loads on checkout. Verify that's where it lands.

B I can dismiss quickly: it's the same work half-done and keeps the per-machine wiring. C fails
on its own terms — "high availability" with copy-drift is a contradiction.

Ranked risks for A: (1) unverified plugin schema details — write nothing from memory, validate
with tooling; (2) the `agents/` scan collision; (3) description quality; (4) the namespaced
command change surprising the user. None is a blocker. I don't have a strong objection to A.

---

### Cross-examination

- Architect on DA's naming concern: agreed it's a real cost, but the collision with the builtin
  `/security-review` makes bare names untenable anyway; namespacing is the honest resolution.
- DA on Architect's path-convention point: extends it — the convention must be *tested from an
  installed context*, not just a checkout, before the old import is removed. Both agree the
  import stays until a fresh session confirms registration (handoff gotcha #1).

---

## Synthesis (System Architect)

**Verdict: Proceed with conditions** — proceed with Option A, the plugin + self-hosted
marketplace conversion.

Criteria measured: friction (one-time two-command install vs. per-machine hand-wiring), context
cost (JIT skill bodies + one-line descriptions vs. 65 always-on lines), availability (marketplace
update path vs. copy drift), determinism of discovery (harness registration vs. model-followed
index). A wins on all four; B fails determinism and friction; C fails availability.

Conditions (owner: implementer, this branch):

1. **Resolve before proceeding** — neutralize the `agents/` subagent scan in `plugin.json`
   explicitly; validate the manifest with real tooling, not memory.
2. **Resolve before proceeding** — one path convention for shared references that works both
   installed (plugin root) and in a checkout; applied in every skill, team reference, and
   `_conventions.md`.
3. **Resolve before proceeding** — trigger-phrase-heavy descriptions for all nine skills; README
   documents the namespaced commands.
4. **Resolve before proceeding** — `lessons.md` session rule survives in the repo `CLAUDE.md`.
5. **Tracked** — fresh-session verification that all nine skills register and one full skill run
   loads team + personas + standard from the plugin; consumers drop the `@` import only after
   this passes. Cannot be completed from inside the converting session (registration is decided
   at session start).

No unresolved dissent.
