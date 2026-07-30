# Skill: Project Planning

## Command

`/project-planning`

## Description

Produces a prioritised plan for a planning horizon — sprint, quarter, or roadmap segment. Takes a set of candidate items (backlog, feature requests, strategic goals, or a mix) and returns a prioritised sequence with rationale, trade-offs, success metrics, and sequencing constraints.

Focuses on the *what* and *why* of the plan, not the *how* of any individual item. Individual items that emerge from this process can be handed to Technical Discovery or Feature Design for further elaboration.

## Team

`agents/teams/project-planning.md`

## Interaction model

Follow the team's default interaction model in `agents/teams/project-planning.md`. The shared protocol in `skills/_conventions.md` applies.

No overrides.

## Context gathering

Per `skills/_conventions.md`. Required context: a planning brief that includes the candidate items to prioritise.

> "Please describe what you're planning. Include: the planning horizon (sprint, quarter, or roadmap), the candidate items you're considering, any known constraints (team capacity, dependencies, deadlines, or technical prerequisites), and any strategic goals or priorities already established. There's no required format — write it however is natural."

Optional focus question: "Is there anything the team should weight especially — business urgency, technical risk, user impact, or something else?"

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

**Readiness verdict** (per `standards/review-verdicts.md`)**:** Proceed to execution / Proceed with conditions / Do not proceed

[If DA has unresolved concerns: **Devil's Advocate note:** [...]]

---

## Example invocation

```
/project-planning

Planning next quarter for a team of five. Candidates: a self-serve onboarding flow, a
long-requested SSO integration, paying down a flaky test suite that's slowing every
release, and a redesign of the reporting page. Sales is pushing SSO hard for two
enterprise deals; engineering wants the test-suite work first. No hard deadlines except
the SSO deals close end of quarter.
```
