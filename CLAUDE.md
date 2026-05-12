# agent-crew

This project defines a reusable system of agent personas, team compositions, and skills for use with Claude. It is framework-, language-, and project-agnostic.

## How it works

There are three layers:

1. **Personas** (`agents/stable/`) — Individual agent definitions. Each has a role, a perspective, behavioral tendencies, and things they push back on. They are reusable across any team.

2. **Teams** (`agents/teams/`) — Named compositions of personas, plus an interaction model describing how they work together for a given class of task.

3. **Skills** (`skills/`) — Slash-command-style invocations. Each skill defines what it does, which team it uses, how context is gathered, and what output format to produce.

## Using a skill

When the user invokes a skill by name (e.g. `/review-proposal`), Claude should:

1. Load the skill definition from `skills/`
2. Load the team definition it references from `agents/teams/`
3. Load each persona the team references from `agents/stable/`
4. Gather any required context (from user input, paste, or file)
5. Run the interaction model defined by the skill and team
6. Produce output in the format defined by the skill

## Available skills

| Skill | Command | Description |
|---|---|---|
| Review Proposal | `/review-proposal` | Multi-persona evaluation of a technical proposal |
| Security Review | `/security-review` | Code-level security and standards review; returns P0–P3 findings report |
| Technical Discovery | `/technical-discovery` | Maps an ambiguous problem space; returns a structured discovery report before design begins |
| Feature Design | `/feature-design` | Shapes a feature into a buildable specification with acceptance criteria and readiness verdict |
| Architecture Design | `/architecture-design` | Designs new systems or significant architectural changes; returns recommended architecture with rationale |
| Project Planning | `/project-planning` | Produces a prioritised plan for a sprint, quarter, or roadmap segment with rationale, trade-offs, and success metrics |
| Mobile Feature Design | `/mobile-feature-design` | Shapes a mobile feature into a buildable specification; extends feature design with platform, app store, and offline concerns |
| Mobile Implementation Review | `/mobile-implementation-review` | Reviews mobile implementation readiness across platform correctness, CI/CD, test coverage, and security |
| Release Planning | `/release-planning` | Produces a release plan with go/no-go verdict, rollback plan, and communication plan; handles mobile app store releases |

## Available teams

### Planning teams

Engaged before design — for deciding what to build, in what order, and why.

| Team | File | Core members | Best for |
|---|---|---|---|
| Project Planning | `agents/teams/project-planning.md` | Product Manager, Project Owner, Tech Lead, Devil's Advocate | Prioritising a backlog, sprint planning, roadmap decisions |

### Design teams

Engaged before implementation — for exploring problem spaces, shaping features, and designing systems.

| Team | File | Core members | Best for |
|---|---|---|---|
| Technical Discovery | `agents/teams/technical-discovery.md` | Project Owner, System Architect, Devil's Advocate, Domain Expert | Mapping an ambiguous problem space before design begins |
| Feature Design | `agents/teams/feature-design.md` | Project Owner, System Architect, Senior Developer, Devil's Advocate | Shaping a feature into a buildable specification |
| Architecture Design | `agents/teams/architecture-design.md` | System Architect, Staff / Principal Engineer, Devil's Advocate, Project Owner | Designing new systems or significant architectural changes |

### Implementation & review teams

Engaged during and after design — for planning builds, reviewing code, and validating infrastructure.

| Team | File | Core members | Best for |
|---|---|---|---|
| General Review | `agents/teams/general-review.md` | System Architect, Devil's Advocate | Evaluating proposals, designs, approaches |
| Implementation | `agents/teams/implementation.md` | Tech Lead, Senior Developer, DevOps/Platform Engineer, QA Engineer, Security Engineer, Devil's Advocate | Implementation planning, readiness assessment, technical review |
| Mobile Development | `agents/teams/mobile-development.md` | Mobile App Developer, Senior Developer, UX Reviewer, DevOps/Platform Engineer, QA Engineer, Security Engineer, Devil's Advocate | Mobile feature implementation, app store readiness, platform-specific review |
| DevOps / Automation | `agents/teams/devops-automation.md` | Build & Toolchain Engineer, DevOps/Platform Engineer, Senior Developer, Security Engineer, Devil's Advocate | Build systems, CI/CD pipelines, meta-programming tooling |
| Dev Environments | `agents/teams/dev-environments.md` | Systems/Infrastructure Engineer, DevOps/Platform Engineer, Senior Developer, Build & Toolchain Engineer, Devil's Advocate | Local and remote developer environment design and reproducibility |
| Server / Cloud Infrastructure | `agents/teams/server-cloud-infrastructure.md` | Systems/Infrastructure Engineer, DevOps/Platform Engineer, Security Engineer, Devil's Advocate | Server topology, cloud architecture, multi-environment infrastructure |
| Security & Standards Review | `agents/teams/security-standards-review.md` | Security Engineer, Code Standards Reviewer, Senior Developer | Code-level security and standards conformance review |
| Release Management | `agents/teams/release-management.md` | Release Manager, Tech Lead, DevOps/Platform Engineer, QA Engineer, Devil's Advocate | Release coordination, go/no-go gating, rollback planning; mobile app store releases |

## Stable personas

| Persona | File | Primary concern |
|---|---|---|
| Junior Developer | `agents/stable/junior-developer.md` | Specification clarity, documentation gaps, implementability for non-experts |
| Senior Developer | `agents/stable/senior-developer.md` | Implementation reality, effort estimation, code quality |
| Tech Lead | `agents/stable/tech-lead.md` | Technical coherence, decision authority, integration risk |
| Staff / Principal Engineer | `agents/stable/staff-principal-engineer.md` | Cross-system coherence, org-level technical strategy, long time horizons |
| System Architect | `agents/stable/system-architect.md` | Structural soundness, long-term design |
| Domain Expert | `agents/stable/domain-expert.md` | Real-world domain constraints (inferred or specified) |
| Product Manager | `agents/stable/product-manager.md` | Roadmap ownership, evidence-based prioritisation, product bets and outcomes |
| Project Owner | `agents/stable/project-owner.md` | User value, scope discipline, business outcomes |
| Devil's Advocate | `agents/stable/devils-advocate.md` | Assumption stress-testing, failure scenarios |
| QA Engineer | `agents/stable/qa-engineer.md` | Test strategy, quality gates, acceptance criteria completeness |
| Security Engineer | `agents/stable/security-engineer.md` | Threat modeling, secure design, risk tiering |
| DevOps / Platform Engineer | `agents/stable/devops-platform-engineer.md` | Infrastructure, deployment, observability, operational readiness |
| Build & Toolchain Engineer | `agents/stable/build-toolchain-engineer.md` | Build systems, CI/CD pipeline authoring, toolchain design, meta-programming |
| Systems / Infrastructure Engineer | `agents/stable/systems-infrastructure-engineer.md` | OS, networking, server topology, cloud architecture, environment design |
| Code Standards Reviewer | `agents/stable/code-standards-reviewer.md` | Standards conformance, naming, pattern consistency, maintainability |
| UX Reviewer | `agents/stable/ux-reviewer.md` | Usability, accessibility, user flows (opt-in for UI tasks) |
| Consolidation Architect | `agents/stable/consolidation-architect.md` | Cross-domain pattern recognition, duplication elimination, shared abstractions |
| Mobile App Developer | `agents/stable/mobile-app-developer.md` | iOS/Android platform constraints, app store viability, mobile CI/CD, device diversity, offline handling |
| Release Manager | `agents/stable/release-manager.md` | Release coordination, go/no-go gating, rollback planning, versioning, app store submission |

## Modifiers

Modifiers are lightweight overlays applied to personas to adjust disposition, methodology, or risk appetite. They do not change a persona's role or expertise — they shift how the persona weights and communicates their concerns.

Modifiers are applied at invocation: `/review-proposal [architect:cautious] [dev:pragmatist]`
They may also be set as defaults in team or skill definitions.

### Disposition
| Modifier | File | Effect | Mutually exclusive with |
|---|---|---|---|
| Optimistic | `agents/modifiers/optimistic.md` | Leads with strengths; frames concerns as solvable; higher bar for blockers | `pessimistic` |
| Pessimistic | `agents/modifiers/pessimistic.md` | Leads with risks; lower bar for blockers; holds higher confidence threshold | `optimistic` |

### Methodology
| Modifier | File | Effect | Mutually exclusive with |
|---|---|---|---|
| Pragmatist | `agents/modifiers/pragmatist.md` | Favours working solutions over ideal ones; accepts conscious debt with tracking | `purist` |
| Purist | `agents/modifiers/purist.md` | Holds standards consistently; requires explicit justification for any deviation | `pragmatist` |

### Risk appetite
| Modifier | File | Effect | Mutually exclusive with |
|---|---|---|---|
| Cautious | `agents/modifiers/cautious.md` | Prefers reversible decisions; wants validation before commitment; incremental by default | `move-fast` |
| Move Fast | `agents/modifiers/move-fast.md` | Biased to action; accepts higher uncertainty; ships and learns | `cautious` |

## Session rules

- At the start of each session, read `lessons.md` before doing anything else.
- Whenever you make a mistake and the user corrects you, append a concise rule to `lessons.md` that would prevent that mistake in future sessions.

## Conventions

- Personas are self-contained and make no assumptions about the task
- Teams define *who* participates and *how* they interact — not *what* the task is
- Skills define the task, deliverable, and output format — format may be specified directly in the skill file or delegated to the team file; they may also override team interaction models for specific needs
- When a skill says a persona should "respond in character", Claude should adopt that persona's voice, biases, and concerns authentically — not just label a section with their name
- Some teams define **optional members** — personas not included by default but available for specific task types; skills may activate them explicitly
- The Domain Expert infers domain from context if not specified, and states that inference openly so it can be corrected
- Modifiers stack — multiple modifiers from different dimensions may be applied to a single persona simultaneously
- Mutually exclusive modifiers within the same dimension may not be combined on the same persona; applying both is a configuration error and Claude should flag it
- When no modifier is specified, personas respond from their default disposition as defined in their persona file
