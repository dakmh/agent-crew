---
name: review-proposal
description: "Multi-persona review of a technical proposal, decision, or approach by the General Review team (System Architect + Devil's Advocate): independent critique, cross-examination, and a Proceed / Proceed with conditions / Do not proceed verdict. Use when asked to review a proposal, evaluate or sanity-check a technical approach or design decision, poke holes in a plan, stress-test an idea, get a second opinion on an architecture or migration choice, or when the user says 'review this proposal', 'what does the team/crew think', or invokes /review-proposal."
---

# Skill: Review Proposal

> **Loading:** all repo-relative paths in this file (`skills/_conventions.md`, `crew/…`,
> `standards/…`) resolve from the plugin root — `${CLAUDE_PLUGIN_ROOT}` when installed as a
> plugin, the repository root in a checkout. Before running: load `skills/_conventions.md`
> (shared protocol), the team file referenced below, every persona the team lists, and any
> standard referenced by the skill, team, or personas.

## Command

`/agent-crew:review-proposal` (installed as a plugin) — historically bare `/review-proposal` in
pre-plugin setups; treat both as this skill.

## Description

Multi-persona evaluation of a technical proposal. Takes a plain-text description of a technical approach, decision, or design and returns structured critique and a recommendation.

## Team

`crew/teams/general-review.md`

## Interaction model

Follow the team's default interaction model in `crew/teams/general-review.md`. The shared protocol in `skills/_conventions.md` applies.

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

**Verdict** (per `standards/review-verdicts.md`)**:** Proceed / Proceed with conditions / Do not proceed

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
