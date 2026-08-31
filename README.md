# agent-crew

A reusable library of Claude agent personas, team compositions, modifiers, skills, and standards, distributed as a Claude Code plugin.

## Concept

Instead of re-specifying who you want involved and how they should interact every time you start a task, `agent-crew` lets you define those things once and invoke them by name.

```
/agent-crew:feature-design
/agent-crew:project-planning
/agent-crew:release-planning
```

...is shorthand for: load the right team, adopt each persona authentically, run the defined interaction model, and return structured output — all from a standing start.

## Installation

This repository is both the plugin and its marketplace. In any Claude Code session:

```
/plugin marketplace add dakmh/agent-crew
/plugin install agent-crew@agent-crew
```

The install prompt asks for a scope (user = every project, project = this repo's collaborators, local = just you here). If the install summary says `Run /reload-plugins to activate.`, run that; otherwise the skills register at the next session start.

Skills load just-in-time: only their one-line descriptions are in context until one is invoked, so the library costs almost nothing when idle.

To try changes from a local checkout without installing: `claude --plugin-dir /path/to/agent-crew`.

Updates: `/plugin marketplace update agent-crew` pulls the latest published version.

**Which copy executes.** Don't assume; every run reports it. Where the marketplace is registered with a `directory` source pointing at a checkout, runs have been observed executing from that checkout rather than from the installed snapshot in `~/.claude/plugins/cache/` — so edits to the checkout are live, and a defect found mid-run can be fixed and re-exercised in the same session. That is one observation in one install shape, not a guarantee, which is why every skill run states its resolved library root in its disclosure line (`skills/_conventions.md` → *The disclosure line*) and why `docs/capability-audit.md` re-checks it. Read the line rather than reasoning about it.

### Legacy installation (CLAUDE.md import)

Before the plugin existed, agent-crew was wired in by adding it as a git submodule and importing `@.agent-crew/CLAUDE.md` from the host project's `CLAUDE.md`. That still works — `CLAUDE.md` keeps a compact index for it — but it costs always-on context and per-machine setup. Prefer the plugin; remove the import once a fresh session confirms the plugin's skills are registered.

## Skills

| Command | Description |
|---|---|
| `/agent-crew:review-proposal` | Multi-persona evaluation of a technical proposal |
| `/agent-crew:technical-discovery` | Maps an ambiguous problem space before design begins |
| `/agent-crew:feature-design` | Shapes a feature into a buildable specification |
| `/agent-crew:architecture-design` | Designs new systems or significant architectural changes |
| `/agent-crew:project-planning` | Prioritised plan for a sprint, quarter, or roadmap segment |
| `/agent-crew:mobile-feature-design` | Feature design extended with platform, app store, and offline concerns |
| `/agent-crew:mobile-implementation-review` | Mobile implementation readiness across platform, CI/CD, test coverage, and security |
| `/agent-crew:release-planning` | Release plan with go/no-go verdict, rollback plan, and communication plan |
| `/agent-crew:security-review` | Code-level security and standards review; returns P0–P4 findings report per the code review severity standard |

(In legacy CLAUDE.md-import setups the commands are the bare, un-namespaced forms: `/review-proposal`, etc. The namespaced form also avoids colliding with Claude Code's built-in `/security-review`.)

Modifiers adjust how a persona weights and communicates its concerns:

```
/agent-crew:review-proposal [architect:cautious] [dev:pragmatist]
```

## Structure

```
agent-crew/
  .claude-plugin/
    plugin.json                    ← plugin manifest
    marketplace.json               ← self-hosted marketplace (source: "./")
  CLAUDE.md                        ← checkout sessions + legacy-import index
  crew/
    stable/                        ← Individual persona definitions
      junior-developer.md
      senior-developer.md
      tech-lead.md
      staff-principal-engineer.md
      system-architect.md
      domain-expert.md
      product-manager.md
      project-owner.md
      devils-advocate.md
      qa-engineer.md
      security-engineer.md
      devops-platform-engineer.md
      build-toolchain-engineer.md
      systems-infrastructure-engineer.md
      code-standards-reviewer.md
      ux-reviewer.md
      consolidation-architect.md
      mobile-app-developer.md
      release-manager.md
      digital-fabrication-engineer.md
      inkscape-extension-developer.md
      woodworking-joinery-specialist.md
      2d-vector-graphics-engineer.md
      3d-vector-graphics-engineer.md
    teams/                         ← Named team compositions + interaction models
      project-planning.md
      general-review.md
      technical-discovery.md
      feature-design.md
      architecture-design.md
      implementation.md
      mobile-development.md
      devops-automation.md
      dev-environments.md
      server-cloud-infrastructure.md
      security-standards-review.md
      release-management.md
    modifiers/                     ← Lightweight overlays that adjust persona disposition
      optimistic.md
      pessimistic.md
      pragmatist.md
      purist.md
      cautious.md
      move-fast.md
  skills/                          ← Invocable skills (one directory per command)
    _conventions.md                ← shared skill protocol, loaded with every skill
    review-proposal/SKILL.md
    technical-discovery/SKILL.md
    feature-design/SKILL.md
    architecture-design/SKILL.md
    project-planning/SKILL.md
    mobile-feature-design/SKILL.md
    mobile-implementation-review/SKILL.md
    release-planning/SKILL.md
    security-review/SKILL.md
  standards/                       ← Named reference standards cited by teams and skills
    code-review-severity.md        ← finding classification: P0–P4 ↔ Blocker–Info, CVSS for security
    review-verdicts.md             ← fixed verdict scale: Proceed / with conditions / Do not proceed
    risk-assessment.md             ← likelihood/impact rating, dispositions, risk acceptance records
    mobile-release-readiness.md    ← app store submission checklist, review-window risk calculus
  docs/
    optimization-plan.md           ← analysis & roadmap
    reviews/                       ← decision records produced with agent-crew itself
```

Note: the personas directory is `crew/`, not `agents/` — `agents/` has reserved meaning in the Claude Code plugin layout (subagent definitions), and these personas are reference material for skills, not standalone subagents.

## Extending

### Adding a persona

Copy any file in `crew/stable/` as a template. Define: role and domain, perspective and priorities, what they push back on, and how they communicate.

### Adding a team

Create a file in `crew/teams/`. Define: which personas participate, the interaction model (sequential, parallel, synthesised), and who produces the final output.

### Adding a modifier

Create a file in `crew/modifiers/`. Define: which dimension it operates on (disposition, methodology, risk appetite), what it changes about a persona's behaviour, what it does *not* change, and which other modifiers it is mutually exclusive with.

### Adding a skill

Create `skills/<command>/SKILL.md` with `name` and `description` YAML frontmatter — the description is the triggering mechanism, so make it verbose and trigger-phrase-heavy ("Use when asked to…", plus the phrasings people actually say). Define: which team to use, how to gather context, the interaction model (may override the team default), and output format. Reference shared material (`crew/`, `standards/`, `skills/_conventions.md`) by repo-root-relative path; those resolve from the plugin root when installed. Add the skill to `CLAUDE.md`'s index (for legacy imports) and the table above.

### Adding a standard

Create a file in `standards/`. Define a self-contained reference (classification scale, protocol, convention) that multiple teams or skills can cite by path instead of defining inline. Standards are authoritative for what they define; teams and skills deviate only via explicitly declared overrides.

## Releasing a new version

Bump `version` in both `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`, then push to `main`. Consumers pick it up with `/plugin marketplace update agent-crew`. Validate before pushing: `claude plugin validate .claude-plugin/plugin.json` and `claude plugin validate .`.
