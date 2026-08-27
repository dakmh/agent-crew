# Execution substrate: what "run a team" actually means

**Status:** Analysis, no changes made to the library.
**Scope:** Why two Claude instances disagreed about whether invoking an agent-crew team spawns subagents, and what the library should say about it.
**Date:** 2026-08-27.

---

## 1. The observation

Two Claude instances given comparable requests behaved differently.

One, on Sonnet in a web-interface container, stated:

> So if you type "spawn an agent-crew team to work on issue #42," I'd interpret that as "run the closest-matching skill" and proceed with the in-context roleplay above — I would not actually launch subagents via the Agent tool, because nothing in the library tells me to, and nothing in the library's design assumes I would.

The other, on Opus in a local Claude Code session, called the `Agent` tool twice and dispatched two background subagents, each of which ran an agent-crew team.

Both behaviors were defensible. The divergence is not a bug in either instance — it is a gap in the library.

## 2. What actually ran in the local session

Worth being precise, because there are three distinct things that all get called "a team" and only one of them happened.

Two `Agent` tool calls were made, each with `subagent_type: general-purpose`, backgrounded, **with no `name` argument**.
Per the [sub-agents documentation](https://code.claude.com/docs/en/sub-agents), those are ordinary subagents: each gets its own context window, its own tool access, loads `CLAUDE.md` from the hierarchy, does **not** inherit the caller's conversation history, and returns a result to the caller when it finishes.

They were **not** agent teams.
Per the [agent-teams documentation](https://code.claude.com/docs/en/agent-teams), that feature is experimental and gated behind `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`, and a teammate is launched by calling the `Agent` tool **with a `name`**.
Teammates get a shared task list, mailbox files under `~/.claude/teams/{team-name}/inboxes/`, and can message each other directly and be addressed individually by the user.
None of that was in play.

Inside each subagent, the personas were single-context roleplay.
One subagent played Product Manager, Project Owner, Tech Lead, Domain Expert, Senior Developer and Devil's Advocate within one context window; the other played seven personas the same way.

So the structure was two-level:

| Level | Mechanism |
|---|---|
| Orchestrator → the two teams | Real subagents, isolated context windows, results returned to the caller |
| Team → its personas | Self-roleplay inside one context window |

No agent was spawned per persona.
The Sonnet instance's description of persona-level behavior was accurate; it was describing a level of the stack that the Opus instance also ran as roleplay.

## 3. Why the two instances diverged

In descending order of confidence. Model tier is not on the list; there is no evidence it mattered.

**The user's phrasing carried most of it.**
The local session's request was "spin up an agent-crew team to work on this" and "spin up a separate agent-crew team," repeated across two tasks.
In Claude Code's vocabulary, "spin up" is dispatch language, not skill-invocation language.
The Sonnet instance was reasoning about what naming the library implies *on its own*, and answered that question correctly.

**The local machine carried a user-authored layer that redefines the library.**
Two memory files in `~/.claude/memory/` on that machine assert, in the user's own words, that running a team means spawning agents:

> Running a team means spawning agents, and agent use needs Daniel's explicit approval.
> — `use-agent-crew-for-reviews.md`

A companion file, `agent-dispatch-approval-gate.md`, builds an interactive approval protocol on that premise.
**Neither statement appears anywhere in this repository.**
An instance without those files has no reason to reach that reading, and the Sonnet instance did not.

**The harness told the local instance the capability existed.**
Its session prompt carried "Do not call the AgentTool unless the user requested it," which simultaneously confirms the tool is available and establishes that a user request unlocks it.

**Tool availability may have made it moot for the other instance.**
A web-interface container may not expose the `Agent` tool at all, in which case its statement is not a judgment call but a description of its tool list.

## 4. The actual gap

**The library never says who executes a team, and that silence is the entire divergence.**

`CLAUDE.md`'s "Using a skill" flow says: load the skill definition, load the team, load each persona and any referenced standard, gather context, run the interaction model, produce output in the skill's format.
Every step describes *what to do*.
No step describes *who does it*.
Read plainly and without a local override, that is a recipe for a single context to follow — which is exactly what the Sonnet instance concluded.

## 5. The design constraint that makes this non-trivial

Before adding "spawn a subagent per persona" to the library, note that the interaction model would fight it.

`skills/_conventions.md` states:

> Personas with overlapping domains do not re-cover ground a prior persona has already addressed unless they disagree — they reference the prior finding and extend it.

Team files build on the same assumption: cross-examination steps, a named synthesizer, explicit response ordering, and a dissent rule that requires the stress-testing persona to have read the synthesis.

All of that requires every persona to see what the others wrote.
Isolated subagents cannot, unless given a message bus — which is precisely what the agent-teams feature provides and plain subagents do not.

This is why the two-level structure in §2 preserved the interaction model correctly.
Each team stayed in one context, so cross-examination worked natively; the subagent boundary sat *around* the team, not *inside* it.

## 6. Three coherent targets

These are genuinely different products, not three implementations of one idea.

### 6a. In-context roleplay

What the library describes today, and the only one requiring no change.

- Cheapest by a wide margin.
- Cross-examination, ordering, synthesis and dissent all work natively.
- Bounded by one context window, so a large team on a large artifact competes for space with the artifact itself.
- Personas anchor on each other's text, which weakens adversarial value — the Devil's Advocate has already read the synthesis it is meant to stress.

### 6b. One subagent per team

What ran in the local session.

- Isolation and parallelism at the team level; several teams can run concurrently on different artifacts.
- The interaction model survives unchanged, because each team occupies one context.
- The team gets a full fresh context window for the artifact, rather than sharing the orchestrator's.
- Results come back summarized, so the orchestrator keeps the conclusion rather than the whole run.
- Requires nothing from the library except permission to dispatch.
- Costs more tokens than 6a and returns less visible working detail to the main session.

### 6c. One teammate per persona

Requires `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`, and the `Agent` call must pass a `name`.

- Genuine independence: personas cannot anchor on each other's prose, so disagreement is real rather than performed.
- Each teammate is separately addressable by the user mid-run, which no other option offers.
- Highest token cost; teammates scale linearly.
- **The interaction model needs rewriting around messages rather than sequential sections.** Steps like "Tech Lead responds to scope and value concerns" become message exchanges with no guaranteed ordering.
- Teammates cannot spawn their own teammates, so a skill that wants sub-teams is out.
- Experimental, with documented limitations around session resumption and shutdown.

## 7. Recommendation

**Adopt 6b as the library's default and say so explicitly. Keep 6a as the documented fallback. Treat 6c as a per-skill opt-in, not a global mode.**

6b is the only option that improves on today's behavior without touching a single team or skill file — the interaction models are already correct for it.
6a stays because it is the right answer for a small team on a small artifact, and because it is what runs when the `Agent` tool is unavailable, which is a real condition rather than a hypothetical.
6c is worth reserving for the teams whose value genuinely comes from independence — a Devil's Advocate that has not read the synthesis is a different instrument from one that has — but it is not a free upgrade, and adopting it globally would silently break the interaction models.

## 8. Concrete changes proposed

1. **Add an "Execution" section to `CLAUDE.md`**, adjacent to "Using a skill," naming the default substrate and the fallback. Two or three sentences. This is the change that closes the gap.
2. **State the invariant that decides everything else:** a team runs in one context; the isolation boundary goes around the team, never between its personas — unless a skill explicitly opts into 6c and supplies a message-based interaction model.
3. **Give skills an optional `execution:` declaration** with values along the lines of `inline`, `subagent`, `teammates`. Defaults to `subagent`, falls back to `inline` when the tool is absent. This follows the existing override precedent — skills already declare team-model overrides, and this is the same shape.
4. **Say what happens when the substrate is unavailable.** The failure mode worth naming is the invisible one: an inline single-voice pass reads identically to a full team run in the output. The library should require the run to state which substrate it used.
5. **Decide where the approval gate lives.** On the local machine it currently sits in user memory files, and the library does not know it exists. If dispatch is going to be the default, the library should acknowledge that dispatch may require the user's per-use approval, and that a skill instruction is not itself that approval. Otherwise every instance that reads only the library will treat the default as self-authorizing.
6. **Cross-reference the two Claude Code docs** so the vocabulary is unambiguous: [subagents](https://code.claude.com/docs/en/sub-agents) and [agent teams](https://code.claude.com/docs/en/agent-teams). "Team" currently means an agent-crew persona grouping and, in the harness, a specific experimental feature. Those are not the same thing and the collision will keep causing this.

## 9. Not verified

- Whether the Sonnet instance had the `Agent` tool available at all. If it did not, the "would not launch subagents" statement is a report rather than an interpretation, and the phrasing hypothesis in §3 carries correspondingly more weight.
- Whether `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` is set anywhere in the local environment. The absence of a `name` argument settles what ran regardless, but not what was available.
- Whether model tier contributes anything. Nothing here suggests it does, and no test was run that would separate it from the environment differences.
