# agent-crew

A reusable library of Claude agent personas, team compositions, modifiers, and skills for use with Claude Code.

## Concept

Instead of re-specifying who you want involved and how they should interact every time you start a task, `agent-crew` lets you define those things once and invoke them by name.

```
/feature-design
/project-planning
/release-planning
```

...is shorthand for: load the right team, adopt each persona authentically, run the defined interaction model, and return structured output — all from a standing start.

## Quick-start installation

> **These steps are written to be executed by Claude Code.** If you are in a Claude Code session (including web or mobile), you can simply say: *"Please install the github/dakmh/agent-crew project in this repo"* and Claude will follow the steps below.

### Steps

**1. Add agent-crew as a git submodule**

```bash
git submodule add https://github.com/dakmh/agent-crew.git .agent-crew
```

**2. Add a SessionStart hook to initialise the submodule**

In `.claude/settings.json`, add the following hook. If that file already exists, merge the `SessionStart` entry into the existing `hooks` object rather than replacing the file.

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "git submodule update --init --recursive"
          }
        ]
      }
    ]
  }
}
```

**3. Import agent-crew into the project's CLAUDE.md**

Add the following line to the project's `CLAUDE.md` (create the file if it does not exist). Place it at or near the top so it loads before any project-specific instructions:

```
@.agent-crew/CLAUDE.md
```

**4. Commit everything**

```bash
git add .agent-crew .gitmodules .claude/settings.json CLAUDE.md
git commit -m "Install agent-crew"
```

### After installation

Skills are immediately available in any Claude Code session. Invoke by name:

```
/project-planning
/feature-design
/mobile-feature-design
/release-planning
```

## Skills

| Command | Description |
|---|---|
| `/review-proposal` | Multi-persona evaluation of a technical proposal |
| `/technical-discovery` | Maps an ambiguous problem space before design begins |
| `/feature-design` | Shapes a feature into a buildable specification |
| `/architecture-design` | Designs new systems or significant architectural changes |
| `/project-planning` | Prioritised plan for a sprint, quarter, or roadmap segment |
| `/mobile-feature-design` | Feature design extended with platform, app store, and offline concerns |
| `/mobile-implementation-review` | Mobile implementation readiness across platform, CI/CD, test coverage, and security |
| `/release-planning` | Release plan with go/no-go verdict, rollback plan, and communication plan |
| `/security-review` | Code-level security and standards review; returns P0–P3 findings report |

Modifiers adjust how a persona weights and communicates its concerns:

```
/review-proposal [architect:cautious] [dev:pragmatist]
```

## Structure

```
agent-crew/
  CLAUDE.md                        ← Claude bootstrap (imported by your project)
  agents/
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
  skills/                          ← Invocable slash-command definitions
    review-proposal.md
    technical-discovery.md
    feature-design.md
    architecture-design.md
    project-planning.md
    mobile-feature-design.md
    mobile-implementation-review.md
    release-planning.md
    security-review.md
```

## Extending

### Adding a persona

Copy any file in `agents/stable/` as a template. Define: role and domain, perspective and priorities, what they push back on, and how they communicate.

### Adding a team

Create a file in `agents/teams/`. Define: which personas participate, the interaction model (sequential, parallel, synthesised), and who produces the final output.

### Adding a modifier

Create a file in `agents/modifiers/`. Define: which dimension it operates on (disposition, methodology, risk appetite), what it changes about a persona's behaviour, what it does *not* change, and which other modifiers it is mutually exclusive with.

### Adding a skill

Create a file in `skills/`. Define: the slash command name, which team to use, how to gather context, the interaction model (may override the team default), and output format.
