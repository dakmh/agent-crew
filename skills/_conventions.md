# Skill Conventions

Shared protocol for all skills in `skills/`. Individual skill files define only what is
unique to them — command, team, genuine overrides, task-specific emphasis, and output
format. Everything below applies to every skill unless the skill explicitly overrides it.

## Sources of authority

- The **team file** is the single source of truth for the interaction model: member list,
  step order, cross-examination pairings, who synthesises, and dissent rules. Skills do
  not restate it.
- A skill may **override** the team model — add steps, activate members, reorder, or
  change the synthesiser. Overrides are listed explicitly in the skill file; everything
  not overridden follows the team file.
- If a skill and its team file conflict outside a declared override, the team file wins,
  and the conflict should be flagged to the user as a defect in the library.
- **Output format:** if the team file defines an output format, the skill uses it unless
  the skill declares its own. A format declared in the skill file wins.
- **Standards** (`standards/`) are authoritative for what they define (e.g. finding
  classification). When a team or skill references a standard, load it and apply it as
  written. A team or skill may deviate from a referenced standard only via an explicitly
  declared override, same as team-model overrides; the standard wins otherwise.

## Context gathering

When a skill is invoked:

1. If the user included the required context (brief, proposal, code, problem statement)
   in the same message, use it directly.
2. If invoked alone, prompt the user with the skill's context prompt.
3. Optionally ask the skill's focus question. If the user declines to answer, proceed
   with whatever context is available.
4. Do not proceed until the skill's required context has been provided.

Unless a skill states otherwise, it has no external dependencies — context comes from
the user directly.

## Execution substrate

Every team runs **in-context** by default: one Claude session reads each persona file and
writes their section in character, sequentially, in its own context. Every interaction model
in `crew/teams/` assumes this unless the team file states otherwise — cross-examination, a
named synthesiser, and dissent all require personas to see each other's text, which only a
shared context guarantees. In-context is also the required fallback whenever a declared
alternative's tool is unavailable.

A team file may instead declare **subagent dispatch** for a step whose members have no
cross-persona visibility requirement — no cross-examination, no dependency on a co-member's
draft. Independent-analysis-then-single-consolidator steps qualify; anything with a
cross-examination step does not, because isolated subagents cannot see each other's output.
Where declared, each such persona runs as an ordinary background subagent: the `Agent` tool
called without a `name` argument, one call per persona, all independent calls issued together
so they run concurrently. This is deliberately **not** Claude Code's experimental agent-teams
feature (named `Agent` calls, `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`, mailbox messaging
between teammates — [docs](https://code.claude.com/docs/en/agent-teams)); agent-crew's "team" is
a persona grouping defined in `crew/teams/`, unrelated to that harness feature beyond sharing a
word. A plain subagent call ([docs](https://code.claude.com/docs/en/sub-agents)) gets an
isolated context, no inherited conversation history, and returns a summarized result to
whichever context dispatched it — consolidation across dispatched personas is done by whoever
dispatched them, reading all returned reports once they're back.

Rules that apply regardless of which substrate a team declares:
- The team file states the dispatch mechanics (which members, which subagent type, what each
  one's prompt contains); a skill does not re-declare them.
- **A run states near the top of its output which substrate it used.** An in-context single
  pass and a dispatched run must never be visually indistinguishable to the reader.
- If a team declares subagent dispatch but the `Agent` tool is unavailable, fall back to
  in-context and say so in the same disclosure.

`crew/teams/security-standards-review.md` is the current example of a team using subagent
dispatch — see it for the pattern before adding another.

## Running the interaction model

- Each persona responds **in character** — voice, priorities, and concerns reflect their
  definition in `crew/stable/`, not generic commentary or a labelled section of
  boilerplate.
- Personas with overlapping domains do not re-cover ground a prior persona has already
  addressed unless they disagree — they reference the prior finding and extend it.
  Persona files may declare explicit boundaries in a "Boundaries" section; respect them.
- **Optional team members** are activated when the run's context matches the team file's
  "When to include" guidance, or when the user asks for them. State at the start of the
  run which optional members are active and why.
- **Modifiers** (`crew/modifiers/`) are applied at invocation — e.g.
  `/agent-crew:review-proposal [architect:cautious] [dev:pragmatist]` — or set as defaults in
  team/skill definitions. Modifiers stack across dimensions on one persona; the pairs
  optimistic/pessimistic (disposition), pragmatist/purist (methodology), and
  cautious/move-fast (risk appetite) are mutually exclusive within their dimension.
  Mutually exclusive modifiers on the same persona are a configuration error — flag it,
  don't guess. With no modifier, personas respond from their default disposition.

## Output

- Persona sections are formatted as `### <emoji> <Persona> — <lens>` headings separated by
  horizontal rules, each body written in character. Skills declare the emoji per persona in
  their output format; keep a persona's emoji consistent within a skill.
- Teams that close with a verdict use the scale in `standards/review-verdicts.md`; the team
  names the action ("Proceed to implementation"), the tier words stay fixed.
- Omit empty sections or tiers rather than printing placeholders.
- If the stress-testing persona (usually the Devil's Advocate) has unresolved concerns
  after synthesis, append their dissent to the final output rather than softening the
  synthesis to manufacture consensus.
- The synthesis is the deliverable — earlier persona sections support it, but the final
  section must stand alone.

## Example invocations

Each skill file ends with a short `## Example invocation` section: the command plus a
realistic context snippet (≤ 8 lines). This is user documentation, not part of the
run-time protocol.
