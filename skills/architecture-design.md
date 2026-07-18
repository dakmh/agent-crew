# Skill: Architecture Design

## Command

`/architecture-design`

## Description

Designs new systems, services, or significant architectural changes. Takes a design brief and returns a recommended architecture with rationale, key decisions, known risks, and a verdict.

Engaged when the decision will shape the technical landscape for years and the cost of getting it wrong is high.

## Team

`agents/teams/architecture-design.md`

## Interaction model

Follow the team's default interaction model in `agents/teams/architecture-design.md`. The shared protocol in `skills/_conventions.md` applies.

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

**Verdict:** Recommended / Recommended with conditions / Further design required

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
