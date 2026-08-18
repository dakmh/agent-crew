---
name: architecture-design
description: "Designs new systems, services, or significant architectural changes via the Architecture Design team: recommended architecture with rationale, key decisions, known risks, and a verdict. Use when asked to design a system or service architecture, evaluate a major structural change, choose between architectural options, plan a re-architecture or platform migration, or when the user says 'design the architecture', 'how should we structure this system', or invokes /architecture-design. For decisions that shape the technical landscape long-term."
---

# Skill: Architecture Design

> **Loading:** all repo-relative paths in this file (`skills/_conventions.md`, `crew/…`,
> `standards/…`) resolve from the plugin root — `${CLAUDE_PLUGIN_ROOT}` when installed as a
> plugin, the repository root in a checkout. Before running: load `skills/_conventions.md`
> (shared protocol), the team file referenced below, every persona the team lists, and any
> standard referenced by the skill, team, or personas.

## Command

`/agent-crew:architecture-design` (installed as a plugin) — historically bare `/architecture-design` in
pre-plugin setups; treat both as this skill.

## Description

Designs new systems, services, or significant architectural changes. Takes a design brief and returns a recommended architecture with rationale, key decisions, known risks, and a verdict.

Engaged when the decision will shape the technical landscape for years and the cost of getting it wrong is high.

## Team

`crew/teams/architecture-design.md`

## Interaction model

Follow the team's default interaction model in `crew/teams/architecture-design.md`. The shared protocol in `skills/_conventions.md` applies.

No overrides.

## Context gathering

Per `skills/_conventions.md`. Required context: a design brief for the system or change to be designed.

> "Please describe what you need designed. Include: what system or change you're designing, the problem it solves, any constraints or requirements, existing architecture context that's relevant, and any approaches you've already considered or ruled out. There's no required format — write it however is natural."

Optional focus question: "Is there anything specific you want the team to focus on — component boundaries, scalability, security, org-level coherence, or something else?"

## Output format

---

### 🏗️ System Architect — Architectural Analysis

[In-character analysis: component design, boundaries, key decisions, tradeoffs, recommendation]

---

### ⚙️ Staff / Principal Engineer — Strategic Perspective

[In-character evaluation: cross-system coherence, strategic alignment, org-level implications]

---

### 😈 Devil's Advocate

[In-character challenge: assumptions, failure modes, scale behaviour, alternatives not considered]

---

### 🎯 Project Owner — Value Anchoring

[In-character evaluation: is the complexity proportionate to the value? Is this solving the right problem?]

---

### 🔄 Cross-Examination

**System Architect on DA's and Staff/Principal's concerns:** [Response]

**Staff / Principal Engineer and DA — areas of agreement and disagreement:** [Response]

**Project Owner on scope and proportionality concerns:** [Response]

---

### ✅ Architecture Decision (System Architect)

**Recommended architecture:** [With rationale]

**Key decisions made:** [Including alternatives considered and rejected]

**Hard-to-reverse decisions:** [And confidence level behind them]

**Open questions:** [Requiring further investigation or validation]

**Known risks and mitigations:** [...]

**Conditions for success:** [What must be true for this architecture to work]

**Verdict** (per `standards/review-verdicts.md`)**:** Proceed / Proceed with conditions / Do not proceed

[If Staff/Principal or DA has significant unresolved concerns: **Dissent:** [...]]

---

## Example invocation

```
/architecture-design

We're splitting our monolith's billing logic into a separate service so other teams can
consume it. It owns invoices, subscriptions, and payment-provider integration. Must stay
consistent with the orders system, which currently reads billing tables directly. ~5M
invoices, growing. We're weighing a synchronous API vs an event-driven model and haven't
committed. Existing stack is Java + Postgres + Kafka.
```
