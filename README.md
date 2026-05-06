# agent-crew

A reusable library of Claude agent personas, team compositions, and skills.

## Concept

Instead of re-specifying who you want involved and how they should interact every time you start a task, `agent-crew` lets you define those things once and invoke them by name.

```
/review-proposal
```

...is shorthand for: load the right team, adopt each persona authentically, run the defined interaction model, and return structured output — all from a standing start.

## Structure

```
agent-crew/
  CLAUDE.md                   ← Claude bootstrap (load this into your project)
  agents/
    stable/                   ← Individual persona definitions
      system-architect.md
      devils-advocate.md
    teams/                    ← Named team compositions + interaction models
      general-review.md
  skills/                     ← Invocable slash-command definitions
    review-proposal.md
```

## Usage

1. Clone or copy this repo
2. Open it as a Claude Code project (or include `CLAUDE.md` in your project context)
3. Invoke any skill by its command name

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

## Adding skills

Create a file in `skills/`. Define:
- The slash command name
- Which team to use
- How to gather context
- The interaction model (may override team default)
- Output format and structure
