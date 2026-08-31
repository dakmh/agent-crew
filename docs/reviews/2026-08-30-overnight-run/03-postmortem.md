# Long agentic runs: postmortem and usage guidance

**What this is.** A postmortem of one unattended multi-hour agent run, and the guidance that came out of it. Written from a run in `photo-culling` on 2026-08-30, but the findings are not specific to that project — the failure was in how the run was *bounded and triggered*, not in what it was building.

**Who it is for.** Two audiences, and the recommendations are split accordingly. Anyone planning another unattended run should read *The run*, *Root causes* and *Guidance for long runs*. `agent-crew` should read *Guidance for agent-crew*, which carries three library observations and the measured evidence behind them.

---

## The run

**The task.** Three checklist items in a Python/Windows photo pipeline, each requiring code, tests, a multi-persona review, and a commit. The brief specified an 8-hour wall-clock budget, a 48-cycle limit, a stop rule for four consecutive unproductive cycles, environment assertions to run before any work, and a review gate: `/agent-crew:security-review` against each completed item's diff before committing it.

**The mechanism.** Claude Code's `/loop` in dynamic mode — the agent self-paces by calling `ScheduleWakeup` at the end of each turn with the loop prompt to re-enter on.

**The outcome.** All three items landed and the suite went from 86 tests to 253. But that took two runs, because the first one stopped after a single cycle and nothing restarted it.

---

## What happened

| Time (UTC) | |
|---|---|
| 06:37 | Run starts. Environment asserted: strict sandbox, correct path, archive drive confirmed detached. |
| 06:37–06:39 | Cycle 1: item 4 built, reviewed by three dispatched subagents, five findings fixed, committed as `a1df017`. Suite green at 146. |
| ~06:39 | `ScheduleWakeup` called for 06:41. |
| 06:41 | **Nothing happens.** |
| 14:37 | The 8-hour budget window expires, unobserved. |
| 15:29 | A human asks what happened. |

The session had hit a usage limit. The pending wakeup died with the session, and there was no durable trigger to bring it back.

Two things worth separating, because they point at different fixes.

**The loop mechanism itself was not the problem.** After the manual restart it fired reliably about eight times over the rest of the work. That is verifiable from the transcript rather than assumed: each cycle arrived carrying the prompt text written into the *previous* cycle's `ScheduleWakeup` call, text no human was transcribing by hand. Self-pacing worked. Surviving a session stop is what it cannot do.

**What could not be determined from inside.** An agent gets no signal that its session is being cut off. There is no "you are about to stop" event and no post-hoc record of why. The agent's own account of the gap can only be "I scheduled a wakeup, and the next thing I saw was nine hours later" — which is exactly as much as an external observer can see, and less than they need.

---

## Root causes

### 1. The budget was denominated in the wrong unit

The brief bounded **cycles** (48) and **wall-clock** (8 hours). Neither was the scarce resource. The scarce resource was account usage, and it was unbounded and unmonitored. The run ended with 47 cycles and 7h58m of headroom remaining, in units that did not constrain anything.

Worse, the cost was front-loaded. Cycle 1 was by a wide margin the most expensive cycle of either run: it read a 300-line work plan and half a dozen source files, wrote four new files totalling roughly 870 lines, **dispatched three parallel review subagents** with long prompts that returned long reports, then acted on five findings and wrote further tests. An entire work item plus a full multi-agent review, in one turn.

The subagent dispatch is the dominant term. Each subagent is a separate context, paid for in full, and three of them run concurrently.

### 2. A single point of failure with no recovery and no liveness signal

`ScheduleWakeup` is session-scoped by design — the `/loop` skill's own documentation says a dynamic loop ends when the session does. For a task explicitly framed as unattended and overnight, that is the wrong trigger, and nothing in the brief compensated for it.

Compounding it: nobody could tell the difference between *stopped* and *sleeping until limits reset*. The log carried `Session start: 06:37:27Z` on line 1 and then never timestamped another entry. A per-cycle timestamp would have shown "last cycle 06:39Z" at a glance and answered the question without anyone having to ask.

### 3. The log recorded outcomes, not intent

Each cycle wrote its log entry at the end, after the work. Had the session died at 80% through cycle 1 rather than after it, the tree would have held uncommitted files with no record of what they were or why.

This is worth stating plainly because of what the run was building: **item 6 of that work is a write-ahead journal** — record intent before the action, outcome after, so a crash leaves exactly the in-flight item identifiable. The loop supervising that work had the precise defect the code was written to fix.

---

## What worked, and is worth keeping

- **Commit per item, stage between sub-cycles.** Nothing was lost to the stop. `a1df017` was clean on disk, and the git index carried the in-progress work across wakeups.
- **The log as a resume artifact rather than only a report.** The restart cost almost nothing because the log said what had landed, what was owed, and what the next unit of work was. This was the single highest-value element of the brief.
- **Environment assertions every cycle.** Cheap, and they make a changed environment loud instead of silent. The brief's insistence that a specific string appear in the test-runner header — not merely that tests pass — is the right shape for this.
- **Smaller sub-cycles after the restart.** Splitting each item into build / test / wire / review sub-cycles, with one review dispatch per *item* rather than per change, is what let the second run finish. That was a human's call mid-run and it was correct.
- **Recording a weakened criterion rather than quietly meeting it.** One acceptance criterion ("byte-identical") turned out to be unachievable as designed and was changed to a weaker, accurate one ("field-identical") with the reasoning written inline. A run that silently redefines its own success conditions is worse than one that fails.

---

## Guidance for long runs

1. **Use a durable trigger for anything meant to run unattended for hours.** A cloud schedule (`/schedule`) re-fires on its own cadence regardless of what happened to the local session, which converts a usage limit from *stop* into *delay* — the next fire reads the log and picks up. This does not grant immunity to usage limits and should not be described as if it does; the property being bought is **automatic recovery**, not immunity.
2. **Budget the expensive thing by name.** "At most N subagent dispatches" constrains the actual resource; "48 cycles" does not. If a review team is in the loop, count the dispatches, not the reviews.
3. **Make the first cycle a canary.** Assert the environment, write the log skeleton and the planned sub-cycle breakdown, do one *small* unit of work, commit, schedule. If the setup is going to fail, fail cheaply. In this run the first cycle was the largest of all of them, which is exactly backwards.
4. **Write-ahead the log.** Append "starting X" before doing X, not just "finished X" after. One line, and it closes the window in which work exists on disk with nothing explaining it.
5. **Timestamp every cycle entry, and keep a `Last cycle:` line at the top of the log.** This is the whole fix for "I can't tell whether it's dead or sleeping," and it costs nothing.
6. **Notify on terminal states, not only on success.** If any stop condition fires, push. Then silence is unambiguous rather than ambiguous.
7. **Keep the stop conditions.** The cycle budget, the wall-clock stop, and the "four consecutive cycles with no test going red→green and no new log content" rule were all well-formed. The no-progress rule never fired here because progress was continuous, but it is the correct guard against a loop that spins while appearing busy.
8. **Front-load cheap durable state.** The plan, the sub-cycle breakdown, and the log skeleton cost almost nothing and are what make a death in cycle 1 survivable.

---

## Guidance for agent-crew

The review gate ran three times, once per work item, using `/agent-crew:security-review` and its Security & Standards Review team. All three took the dispatch branch. Measured results below, because they are evidence about whether the team's design does what it claims.

### The dispatch model works, and the evidence is the convergence

| Run | Diff | Substrate | Disclosure emitted | Independent convergence |
|---|---|---|---|---|
| Item 4 | 952 lines | 3 parallel `Explore` subagents | Yes | 2 of 3 found the same headline defect by different routes |
| Item 5 | 1,336 lines | 3 parallel `Explore` subagents | Yes | 3 of 3 found the missing exception boundary; 2 of 3 found a broken undo path |
| Item 6 | 1,374 lines | 3 parallel `Explore` subagents | Yes | 3 of 3 found a caught-exception mismatch; 2 of 3 found a relocated guarantee |

The convergence is the argument for the substrate. Isolated contexts cannot echo each other, so agreement is evidence rather than repetition — and in run 1 the Security Engineer reached the defect through the threat model while the Senior Developer reached it by tracing error paths, which is the ideal shape of that agreement.

Two findings in run 3 were bugs no test could have caught, in code that read correctly: an exception raised from inside an `except` clause that masked the real error and stranded a journal entry permanently, and a report section that listed unchanged files under a heading saying "what changed". Both were reproduced before being fixed. Two reviewers ran experiments rather than reasoning from memory — confirming a platform-specific `os.replace` behavior, and confirming that the XML parser's defaults already blocked two classic attack shapes so the category could be closed out as *checked, nothing found* rather than left silent.

Severity divergence appeared in every run and was informative rather than a defect: the Security Engineer scoring on CVSS and the Senior Developer on the code-quality scale reached different P-values for the same finding, each defensible against its own scale. The standard's instruction to grade independently rather than relative to the rest of the review is what makes that legible instead of confusing.

### Three library observations

**1. `standards/risk-assessment.md` was cited but never loaded.** The Security Engineer persona points at that file for its disposition scale (must fix before shipping / should fix soon / accept and document / monitor), while the skill and team load only `standards/code-review-severity.md`. Across all three runs the dispatched persona reproduced that scale correctly from its own text alone — which is luck, not design, and the kind of thing that holds until it quietly stops. **Fixed** in the checkout as `7a79ce0`, adding it to the team's load list. Generalizable rule: *any standard a persona references by path must be loaded by whatever runs that persona.* Worth auditing the other personas for the same shape.

**2. The skill loaded from the checkout, not the installed plugin cache.** The brief assumed `claude plugin install` had snapshotted the library and that checkout edits would be inert for the run's duration. That is not what happened — the skill announced its base directory as the working copy on all three runs. This should be settled deliberately rather than left as folklore, because it decides whether a defect found mid-run can be fixed and re-exercised in the same run.

**3. The in-context fallback branch was never exercised.** The team file specifies parallel subagents above roughly 150 lines of diff and an in-context fallback below it. All three diffs were 950–1,375 lines, so the fallback never ran. Partly a property of the work, partly a consequence of batching a whole item into one commit. If that branch matters, it needs a deliberately small change to test it — and if it is rarely reached in practice, that is worth knowing too.

**No ambiguity was found in any team or skill file across three runs.** Step 3's consolidation rule, the substrate threshold, the optional-member activation conditions, and the disclosure requirement all read as written and needed no interpretation. The team file's note explaining that its consolidation step was *previously* contradictory and how it was resolved is a good pattern and should be copied elsewhere.

### Base usage recommendation

**Treat a dispatched review as a large discrete purchase, not a step.** Three parallel subagents with substantial prompts and substantial returns is the most expensive single action in a run of this shape — nine dispatches across this run, and the first three of them consumed the entire first session. Concretely:

- Dispatch **once per work item**, not per sub-change. The mid-run correction to this pattern is what made the second run finish.
- Below the substrate threshold the in-context fallback is not merely cheaper, it is the *designed* path — smaller, more frequent commits make it reachable.
- If the run is budgeted at all, budget it in dispatches.
- The value is real. This is not an argument for skipping the review; it is an argument for spending it deliberately.

---

## What could not be determined

Recorded so that nobody re-derives it or assumes more was knowable than was.

- **Why the session stopped, precisely.** "Usage limit" is the human-side observation. From inside the run there is no signal, no event, and no record.
- **Whether a cloud schedule would have survived this specific stop.** The mechanism differs and the recovery property is real, but its exact interaction with account-level usage limits was not tested here and should not be asserted.
- **Whether the ~150-line substrate threshold is well-calibrated.** No diff in this run came close to it.
