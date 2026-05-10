# Team: Project Planning

## Purpose

A cross-functional team for roadmap decisions and iteration planning. Focused on the question of what to build next, in what order, and why — before any individual feature goes to design or implementation.

This team operates upstream of the Technical Discovery and Feature Design teams. It does not design features or evaluate technical approaches — it decides which work should be prioritised across a horizon and produces a structured, justified plan. The output is a prioritised backlog slice, sprint plan, or roadmap segment with explicit rationale, trade-offs, and success criteria for each item.

Distinct from the Project Owner role in other teams: the Project Owner stewards a specific initiative; this team decides whether that initiative should be prioritised at all relative to competing options.

## Members

| Persona | File | Role in this team |
|---|---|---|
| Product Manager | `agents/stable/product-manager.md` | Roadmap ownership, strategic framing, prioritisation rationale, success metrics |
| Project Owner | `agents/stable/project-owner.md` | User value validation, scope discipline, delivery feasibility from a business perspective |
| Tech Lead | `agents/stable/tech-lead.md` | Technical feasibility, effort sizing, dependency and sequencing constraints |
| Devil's Advocate | `agents/stable/devils-advocate.md` | Challenges prioritisation assumptions, surfaces hidden costs, questions whether stated priorities reflect actual strategy |

## Optional members

| Persona | File | When to include |
|---|---|---|
| Senior Developer | `agents/stable/senior-developer.md` | When effort estimates need ground-level validation before committing to a plan |
| QA Engineer | `agents/stable/qa-engineer.md` | When quality debt, testing infrastructure, or release readiness constraints affect what can be prioritised |
| Domain Expert | `agents/stable/domain-expert.md` | When domain-specific constraints (regulatory, compliance, market timing) are a significant input to prioritisation |

## Default interaction model

This team operates in a **propose → validate → challenge → sequence → synthesise** model, reflecting that prioritisation is a sequential reasoning process: you cannot challenge priorities before they are proposed, and you cannot sequence work before feasibility is assessed.

### 1. Context intake
All personas review the planning input: backlog candidates, strategic goals, current capacity constraints, known dependencies, and any existing commitments. No responses yet.

### 2. Proposal
**Product Manager** opens by proposing a prioritised set of items for the planning horizon, with rationale for each: what user or business problem does it address, what is the expected outcome, and what is being deprioritised as a result. Framing is explicit about trade-offs — prioritisation is a zero-sum activity.

### 3. Value and scope validation
**Project Owner** evaluates each proposed item against user value and delivery realism:
- Does the item's scope match the stated user problem, or is it over- or under-specified?
- Are acceptance criteria clear enough to know when the item is done?
- Are there delivery dependencies that affect the proposed sequence?

### 4. Technical feasibility
**Tech Lead** assesses each proposed item against technical reality:
- Is the effort sizing credible?
- Are there technical dependencies or prerequisites not reflected in the sequence?
- Are there items that would be significantly cheaper to do in a different order?
- What technical debt or infrastructure work, if not addressed, becomes a blocker further in the horizon?

### 5. Stress test
**Devil's Advocate** challenges the plan:
- What assumptions does this prioritisation rely on? Which are unvalidated?
- What is the cost of being wrong about the top priorities?
- Are there items being deprioritised that will create problems later?
- Does the stated rationale for each item reflect actual strategic intent, or post-hoc justification?

### 6. Cross-examination
Personas address the key conflicts and gaps surfaced in steps 3–5:
- Product Manager responds to feasibility and sequencing concerns
- Tech Lead responds to scope and value concerns that have technical implications
- Project Owner and Devil's Advocate address any unresolved trade-offs

### 7. Synthesis
**Product Manager** and **Tech Lead** jointly produce the final plan, incorporating the resolved concerns.

## Interaction model overrides

- When planning a single sprint with a fixed team capacity, collapse steps 2–4 and focus on feasibility and sequencing rather than strategic framing
- When planning a multi-quarter roadmap, extend step 5 with explicit scenario analysis: what does this plan look like if the top-priority bet is wrong?
- When Senior Developer is activated, they contribute between steps 4 and 5 with ground-level effort validation

## Notes

- The Product Manager owns the prioritisation decision in this team — the Tech Lead and Project Owner inform it, but the Product Manager is accountable for the outcome
- Every prioritised item should exit this team with: a stated user/business problem, an expected outcome with a measurable indicator, and a "why now" rationale
- The Devil's Advocate's most valuable contribution in planning is often surfacing the implicit cost of what is being deprioritised — not just questioning what is being prioritised
- This team's output should be complete enough that individual items can be handed directly to Technical Discovery or Feature Design without re-litigating priority or scope
