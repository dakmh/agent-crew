# agent-crew

A reusable, framework- and language-agnostic system of personas, teams, modifiers, and skills for Claude: define who is involved and how they interact once, then invoke by name.

## How it works

- **Personas** (`agents/stable/`) — role, perspective, tendencies, what they push back on.
- **Teams** (`agents/teams/`) — personas plus an interaction model for a task class.
- **Skills** (`skills/`) — slash-command invocations: task, deliverable, output format.
- **Modifiers** (`agents/modifiers/`) — overlays shifting how a persona weights/communicates concerns; role unchanged.

Detail lives in each file; `README.md` is the human-facing index.

## Using a skill

When a skill is invoked (e.g. `/review-proposal`):

1. Load the skill definition from `skills/` and the shared protocol in `skills/_conventions.md`
2. Load the team it references from `agents/teams/`
3. Load each persona from `agents/stable/`
4. Gather required context (user input, paste, or file)
5. Run the skill/team interaction model
6. Produce output in the skill's format

## Index

Paths: `skills/<command>.md`, `agents/{teams,stable}/<stem>.md`, `agents/modifiers/<name>.md`. Stem = name lowercased; `&`, `/`, `'` dropped; each whitespace run becomes a single `-` (e.g. Staff / Principal Engineer → `staff-principal-engineer`).

### Skills (`/command`)
`/review-proposal`, `/security-review`, `/technical-discovery`, `/feature-design`, `/architecture-design`, `/project-planning`, `/mobile-feature-design`, `/mobile-implementation-review`, `/release-planning`

### Teams
- Planning: Project Planning
- Design: Technical Discovery, Feature Design, Architecture Design
- Implementation & review: General Review, Implementation, Mobile Development, DevOps / Automation, Dev Environments, Server / Cloud Infrastructure, Security & Standards Review, Release Management

### Personas
Junior Developer, Senior Developer, Tech Lead, Staff / Principal Engineer, System Architect, Domain Expert, Product Manager, Project Owner, Devil's Advocate, QA Engineer, Security Engineer, DevOps / Platform Engineer, Build & Toolchain Engineer, Systems / Infrastructure Engineer, Code Standards Reviewer, UX Reviewer, Consolidation Architect, Mobile App Developer, Release Manager, Digital Fabrication Engineer, Inkscape Extension Developer, Woodworking / Joinery Specialist, 2D Vector Graphics Engineer, 3D Vector Graphics Engineer

### Modifiers
optimistic/pessimistic (disposition), pragmatist/purist (methodology), cautious/move-fast (risk appetite) — pairs mutually exclusive.

Applied at invocation: `/review-proposal [architect:cautious] [dev:pragmatist]`. May also be set as defaults in team/skill definitions.

## Session rules

- At the start of each session, read `lessons.md` before doing anything else.
- Whenever you make a mistake and the user corrects you, append a concise rule to `lessons.md` that would prevent that mistake in future sessions.

## Conventions

- Personas are self-contained and make no assumptions about the task. Teams define *who* participates and *how* they interact, not *what* the task is. Skills define the task, deliverable, and output format (in the skill or delegated to the team file).
- The team file is the single source of truth for interaction models; skills declare only overrides and task-specific emphasis. If a skill conflicts with its team file outside a declared override, the team file wins. See `skills/_conventions.md`.
- Shared skill protocol (context gathering, in-character requirement, optional-member activation, dissent handling) lives in `skills/_conventions.md` — load it with every skill.
- "Respond in character" means adopt that persona's voice, biases, and concerns authentically — not just a labelled section.
- Some teams define **optional members** — not included by default but available for specific task types; skills may activate them explicitly.
- The Domain Expert infers domain from context if not specified, and states that inference openly so it can be corrected.
- Modifiers stack across dimensions on one persona. Mutually exclusive modifiers within the same dimension may not be combined — applying both is a configuration error Claude should flag. With no modifier, personas respond from their default disposition.
