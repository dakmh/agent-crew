# agent-crew

A reusable library of Claude agent personas, team compositions, modifiers, and skills.

## Concept

Instead of re-specifying who you want involved and how they should interact every time you start a task, `agent-crew` lets you define those things once and invoke them by name.

```
/review-proposal
```

...is shorthand for: load the right team, adopt each persona authentically, run the defined interaction model, and return structured output — all from a standing start.

## Structure

```
agent-crew/
  CLAUDE.md                        ← Claude bootstrap (load this into your project)
  agents/
    stable/                        ← Individual persona definitions
      junior-developer.md
      senior-developer.md
      tech-lead.md
      staff-principal-engineer.md
      system-architect.md
      domain-expert.md
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
    teams/                         ← Named team compositions + interaction models
      general-review.md
      implementation.md
      devops-automation.md
      dev-environments.md
      server-cloud-infrastructure.md
      security-standards-review.md
      technical-discovery.md
      feature-design.md
      architecture-design.md
    modifiers/                     ← Lightweight overlays that adjust persona disposition
      optimistic.md
      pessimistic.md
      pragmatist.md
      purist.md
      cautious.md
      move-fast.md
  skills/                          ← Invocable slash-command definitions
    review-proposal.md
    security-review.md
    technical-discovery.md
    feature-design.md
    architecture-design.md
```

## Usage

1. Clone or copy this repo
2. Open it as a Claude Code project (or include `CLAUDE.md` in your project context)
3. Invoke any skill by its command name

Modifiers can be applied at invocation time to adjust how a persona weighs and communicates their concerns:

```
/review-proposal [architect:cautious] [dev:pragmatist]
```

## Adding personas

Copy any file in `agents/stable/` as a template. Define:
- Role and domain
- Perspective and priorities
- What they push back on
- How they communicate

## Adding teams

Create a file in `agents/teams/`. Define:
- Which personas participate
- The interaction model (sequential, parallel, synthesized, etc.)
- Who produces the final output

## Adding modifiers

Create a file in `agents/modifiers/`. Define:
- Which dimension it operates on (disposition, methodology, risk appetite)
- What it changes about a persona's behaviour
- What it does *not* change
- Which other modifiers it is mutually exclusive with

## Adding skills

Create a file in `skills/`. Define:
- The slash command name
- Which team to use
- How to gather context
- The interaction model (may override team default)
- Output format and structure
