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

## Running the interaction model

- Each persona responds **in character** — voice, priorities, and concerns reflect their
  definition in `agents/stable/`, not generic commentary or a labelled section of
  boilerplate.
- Personas with overlapping domains do not re-cover ground a prior persona has already
  addressed unless they disagree — they reference the prior finding and extend it.
  Persona files may declare explicit boundaries in a "Boundaries" section; respect them.
- **Optional team members** are activated when the run's context matches the team file's
  "When to include" guidance, or when the user asks for them. State at the start of the
  run which optional members are active and why.
- **Modifiers** apply per the rules in `CLAUDE.md`. Mutually exclusive modifiers on the
  same persona are a configuration error — flag it, don't guess.

## Output

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
