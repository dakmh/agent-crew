# Skill: Review Proposal

## Command

`/review-proposal`

## Description

Multi-persona evaluation of a technical proposal. Takes a plain-text description of a technical approach, decision, or design and returns structured critique and a recommendation.

## Team

`agents/teams/general-review.md`

## Interaction model

Follow the team's default interaction model in `agents/teams/general-review.md`. The shared protocol in `skills/_conventions.md` applies.

No overrides.

## Context gathering

Per `skills/_conventions.md`. Required context: a description of the proposal to review.

> "Please describe the proposal you'd like reviewed. Include: what you're proposing, why, any constraints or requirements, and any alternatives you've already considered. There's no required format — write it however is natural."

Optional focus question: "Is there anything specific you want the team to focus on, or any concerns you already have?"

## Output format

---

### 🏗️ System Architect

[In-character analysis]

---

### 😈 Devil's Advocate

[In-character analysis]

---

### 🔄 Cross-Examination

**System Architect on DA's points:**
[Response]

**Devil's Advocate on Architect's points:**
[Response]

---

### ✅ Synthesis (System Architect)

**What holds up:** [...]

**What needs work:** [...]

**Open questions:** [...]

**Recommendation:** Proceed / Proceed with changes / Do not proceed

[If DA dissents from recommendation, append:]

**Devil's Advocate dissent:** [...]

---

## Example invocation

```
/review-proposal

We're planning to replace our existing REST polling mechanism with WebSockets for real-time 
dashboard updates. The current system polls every 5 seconds; users complain about latency. 
We've considered SSE but ruled it out because we need bidirectional communication for 
future features. Stack is Node.js + Redis. About 2,000 concurrent users at peak.
```
