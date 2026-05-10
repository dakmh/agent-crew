# Skill: Project Planning

## Command

`/project-planning`

## Description

Produces a prioritised plan for a planning horizon — sprint, quarter, or roadmap segment. Takes a set of candidate items (backlog, feature requests, strategic goals, or a mix) and returns a prioritised sequence with rationale, trade-offs, success metrics, and sequencing constraints.

Focuses on the *what* and *why* of the plan, not the *how* of any individual item. Individual items that emerge from this process can be handed to Technical Discovery or Feature Design for further elaboration.

No external dependencies — context is provided by the user directly.

## Team

`agents/teams/project-planning.md`

Uses the default Project Planning interaction model unless overridden below.

## Interaction model overrides

None. Use the full Project Planning interaction model including cross-examination and synthesis.

## Context gathering

When `/project-planning` is invoked:

1. If the user has included a planning brief in the same message, use it directly
2. If invoked alone, prompt the user:

   > "Please describe what you're planning. Include: the planning horizon (sprint, quarter, or roadmap), the candidate items you're considering, any known constraints (team capacity, dependencies, deadlines, or technical prerequisites), and any strategic goals or priorities already established. There's no required format — write it however is natural."

3. Optionally ask: "Is there anything the team should weight especially — business urgency, technical risk, user impact, or something else?"

Do not proceed until a planning brief with candidate items has been provided.

## Execution

Run the Project Planning interaction model in order:

1. **[Product Manager]** — Frame the planning horizon and propose a prioritised ordering of the candidate items. For each item: state the user or business problem it addresses, the expected outcome with a measurable indicator, and what is being deprioritised as a result of its inclusion. Name trade-offs explicitly.

2. **[Project Owner]** — Validate user value and scope for each proposed item: does the scope match the stated problem, are acceptance criteria clear enough to know when the item is done, and are there delivery dependencies that affect the proposed sequence?

3. **[Tech Lead]** — Assess technical feasibility and sequencing: is the effort sizing credible, are there technical prerequisites or dependencies not reflected in the sequence, and are there items that would be significantly cheaper or more valuable in a different order?

4. **[Devil's Advocate]** — Challenge the plan: what assumptions does this prioritisation depend on? What is the cost of being wrong about the top priorities? Are items being deprioritised that will become blockers or regrets later?

5. **[Cross-examination]** — Product Manager responds to feasibility and scope concerns; Tech Lead responds to value and sequencing challenges from the DA; Project Owner addresses any delivery concerns raised by the DA.

6. **[Synthesis — Product Manager + Tech Lead]** — Jointly produce the final plan.

Each persona must respond in character — voice, priorities, and concerns should reflect their definition in `agents/stable/`, not generic commentary.

## Output format

---

### 🗺️ Product Manager — Proposed Plan

[In-character prioritised proposal: each item with user/business problem, expected outcome, measurable indicator, and deprioritisation rationale]

---

### 🎯 Project Owner — Value and Scope Validation

[In-character validation: scope fit, acceptance criteria clarity, delivery dependencies]

---

### 🔧 Tech Lead — Feasibility and Sequencing

[In-character assessment: effort credibility, technical prerequisites, sequencing optimisations, technical debt implications]

---

### 😈 Devil's Advocate

[In-character challenge: prioritisation assumptions, cost of being wrong, what's being deprioritised that should not be]

---

### 🔄 Cross-Examination

**Product Manager on feasibility and scope concerns:** [Response]

**Tech Lead on DA's sequencing and priority challenges:** [Response]

**Project Owner on delivery concerns:** [Response]

---

### 📋 Plan (Product Manager + Tech Lead)

**Planning horizon:** [Sprint / quarter / roadmap segment and time frame]

**Prioritised items:**

| Priority | Item | User/Business problem | Expected outcome | Success indicator | Notes / conditions |
|---|---|---|---|---|---|
| 1 | [Item] | [...] | [...] | [...] | [...] |
| 2 | [...] | [...] | [...] | [...] | [...] |

**Sequencing constraints:** [Items that must come before others, and why]

**Deprioritised items:** [What is not in this plan and why]

**Assumptions:** [What this plan depends on being true]

**Open questions:** [Must be resolved before or during the planning horizon]

**Readiness verdict:** Ready to execute / Ready with conditions / Needs further input

[If DA has unresolved concerns: **Devil's Advocate note:** [...]]

---
