# Skill: Feature Design

## Command

`/feature-design`

## Description

Shapes a feature into a buildable specification. Takes a feature request or user story and returns an agreed scope, recommended technical approach, testable acceptance criteria, and a readiness verdict.

Assumes the *why* is established — this team focuses on the *what* and *how* at a level of fidelity sufficient for confident implementation.

## Team

`agents/teams/feature-design.md`

## Interaction model

Follow the team's default interaction model in `agents/teams/feature-design.md`. The shared protocol in `skills/_conventions.md` applies.

No overrides.

## Context gathering

Per `skills/_conventions.md`. Required context: a description of the feature to design.

> "Please describe the feature you'd like designed. Include: what user problem it solves, any constraints or requirements, what technical approach (if any) you're already considering, and anything that's already been decided or ruled out. There's no required format — write it however is natural."

Optional focus question: "Is there anything specific you want the team to focus on — scope, technical approach, acceptance criteria, or something else?"

## Output format

---

### 🎯 Project Owner — Problem Framing

[In-character framing: user problem, success criteria, constraints, scope boundary]

---

### 🏗️ System Architect — Technical Analysis

[In-character analysis: approach options, structural implications, tradeoffs, recommendation]

---

### 👷 Senior Developer — Implementability Check

[In-character assessment: hidden complexity, dependencies, effort realism, specification gaps]

---

### 😈 Devil's Advocate

[In-character challenge: problem framing, scope assumptions, estimates, what might be wrong]

---

### 🔄 Cross-Examination

**Project Owner on DA's framing challenges:** [Response]

**System Architect on Senior Developer's implementability concerns:** [Response]

**Senior Developer + DA on shared/disputed architectural concerns:** [Response]

---

### ✅ Feature Specification (Project Owner + System Architect)

**Problem statement and user goal:** [Confirmed or revised]

**Agreed scope:** [What's in]

**Out of scope:** [Explicitly excluded]

**Recommended technical approach:** [With rationale]

**Acceptance criteria:**
- The user can [...]
- [...]

**Open questions:** [Must be resolved before implementation starts]

**Known risks:** [And how they will be managed]

**Readiness verdict:** Ready for implementation / Ready with conditions / Needs further design

[If DA has unresolved concerns: **Devil's Advocate note:** [...]]

---

## Example invocation

```
/feature-design

We want to let users export their transaction history to CSV from the account page.
It's a small feature but finance keeps asking for it. Should support date-range
filtering. Stack is Rails + Postgres; exports could be large for long-tenured accounts.
Nothing's been decided on sync vs async generation yet.
```
