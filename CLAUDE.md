# agent-crew

A reusable, framework- and language-agnostic system of personas, teams, modifiers, and skills for Claude: define who is involved and how they interact once, then invoke by name.

Distributed as a Claude Code plugin (see `README.md` → Installation); installed skills register with the harness as `/agent-crew:<command>` and load their own dependencies. This file serves two remaining audiences: sessions working in a checkout of this repo, and legacy setups that `@`-import it — the index below exists for the latter.

## Session rules

- At the start of each session, read `lessons.md` before doing anything else.
- Whenever you make a mistake and the user corrects you, append a concise rule to `lessons.md` that would prevent that mistake in future sessions.

## Index (legacy-import discovery)

When a skill is invoked by bare command (e.g. `/review-proposal`) and no plugin registration exists, resolve it here, then follow `skills/<command>/SKILL.md` — each SKILL.md states what to load (shared protocol `skills/_conventions.md`, its team, that team's personas, referenced standards).

Paths: `skills/<command>/SKILL.md`, `crew/{teams,stable}/<stem>.md`, `crew/modifiers/<name>.md`, `standards/<stem>.md`. Stem = name lowercased; `&`, `/`, `'` dropped; each whitespace run becomes a single `-` (e.g. Staff / Principal Engineer → `staff-principal-engineer`).

### Skills (`/command`)
`/review-proposal`, `/security-review`, `/technical-discovery`, `/feature-design`, `/architecture-design`, `/project-planning`, `/mobile-feature-design`, `/mobile-implementation-review`, `/release-planning`

### Teams
- Planning: Project Planning
- Design: Technical Discovery, Feature Design, Architecture Design
- Implementation & review: General Review, Implementation, Mobile Development, DevOps / Automation, Dev Environments, Server / Cloud Infrastructure, Security & Standards Review, Release Management

### Personas
Junior Developer, Senior Developer, Tech Lead, Staff / Principal Engineer, System Architect, Domain Expert, Product Manager, Project Owner, Devil's Advocate, QA Engineer, Security Engineer, DevOps / Platform Engineer, Build & Toolchain Engineer, Systems / Infrastructure Engineer, Code Standards Reviewer, UX Reviewer, Consolidation Architect, Mobile App Developer, Release Manager, Digital Fabrication Engineer, Inkscape Extension Developer, Woodworking / Joinery Specialist, 2D Vector Graphics Engineer, 3D Vector Graphics Engineer

### Standards
Code Review Severity (P0–P4 finding classification), Review Verdicts (Proceed / Proceed with conditions / Do not proceed), Risk Assessment (likelihood/impact, dispositions), Mobile Release Readiness (app store submission gates)

### Modifiers
optimistic/pessimistic (disposition), pragmatist/purist (methodology), cautious/move-fast (risk appetite) — pairs mutually exclusive. Applied at invocation: `/review-proposal [architect:cautious] [dev:pragmatist]`. Full rules in `skills/_conventions.md`.

## Execution

Who actually runs a team — in-context roleplay vs. real subagent dispatch — is a runtime rule,
not an authoring note, so it lives in `skills/_conventions.md` (loaded with every skill run)
rather than here. Summary for orientation: in-context roleplay is the default and the required
fallback; a team file may declare subagent dispatch for steps with no cross-persona visibility
requirement, using plain background `Agent` calls — **not** Claude Code's experimental,
message-passing agent-teams feature, a same-named but different thing. Full rules and the
worked example are in `skills/_conventions.md` and `crew/teams/security-standards-review.md`.

Every run discloses its substrate, the size that selected it, and the library root it loaded
from. When working in this checkout, that last field is how you tell whether your edits are what
just executed — see `README.md` → *Which copy executes*.

## Conventions (authoring in this repo)

- Personas are self-contained and task-agnostic. Teams define *who* participates and *how* they interact. Skills define the task, deliverable, and output format. Standards are authoritative references cited by path.
- The team file is the single source of truth for interaction models; skills declare only overrides. The shared runtime protocol (context gathering, in-character requirement, optional-member activation, dissent handling, modifier rules) lives in `skills/_conventions.md` — it, not this file, is loaded with every skill run.
- The personas directory is `crew/`, not `agents/` — `agents/` has reserved meaning in the Claude Code plugin layout. Don't rename it back.
- New skills need trigger-phrase-heavy `description` frontmatter (it is the only discovery mechanism for plugin consumers) and an entry in this index and the README table. Validate with `claude plugin validate .claude-plugin/plugin.json` before pushing.
