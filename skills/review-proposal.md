# Skill: Review Proposal

## Command

`/review-proposal`

## Description

Multi-persona evaluation of a technical proposal. Takes a plain-text description of a technical approach, decision, or design and returns structured critique and a recommendation.

No external dependencies — context is provided by the user directly.

## Team

`agents/teams/general-review.md`

Uses the default General Review interaction model unless overridden below.

## Interaction model overrides

None. Use the full General Review interaction model including cross-examination and synthesis.

## Context gathering

When `/review-proposal` is invoked:

1. If the user has included proposal text in the same message, use it directly
2. If invoked alone, prompt the user:

   > "Please describe the proposal you'd like reviewed. Include: what you're proposing, why, any constraints or requirements, and any alternatives you've already considered. There's no required format — write it however is natural."

3. Optionally ask: "Is there anything specific you want the team to focus on, or any concerns you already have?"

Do not proceed until proposal text has been provided.

## Execution

Run the General Review interaction model in order:

1. **[System Architect]** — Evaluate the proposal. Address: structural soundness, feasibility, long-term implications, missing non-functional requirements, and any assumptions that need to be validated.

2. **[Devil's Advocate]** — Evaluate the proposal independently. Address: assumptions being treated as facts, failure scenarios, optimistic estimates, underspecified edge cases, and whether alternatives were genuinely considered.

3. **[Cross-examination]** — Each persona briefly responds to the other's key points. Flag agreements, disagreements, and any points that change the overall picture.

4. **[System Architect — Synthesis]** — Produce a final summary.

Each persona must respond in character — voice, priorities, and concerns should reflect their definition in `agents/stable/`, not a generic "here are some thoughts" response.

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
