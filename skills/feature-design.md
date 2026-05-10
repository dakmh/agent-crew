# Skill: Feature Design

## Command

`/feature-design`

## Description

Shapes a feature into a buildable specification. Takes a feature request or user story and returns an agreed scope, recommended technical approach, testable acceptance criteria, and a readiness verdict.

Assumes the *why* is established — this team focuses on the *what* and *how* at a level of fidelity sufficient for confident implementation.

No external dependencies — context is provided by the user directly.

## Team

`agents/teams/feature-design.md`

Uses the default Feature Design interaction model unless overridden below.

## Interaction model overrides

None. Use the full Feature Design interaction model including cross-examination and synthesis.

## Context gathering

When `/feature-design` is invoked:

1. If the user has included a feature description in the same message, use it directly
2. If invoked alone, prompt the user:

   > "Please describe the feature you'd like designed. Include: what user problem it solves, any constraints or requirements, what technical approach (if any) you're already considering, and anything that's already been decided or ruled out. There's no required format — write it however is natural."

3. Optionally ask: "Is there anything specific you want the team to focus on — scope, technical approach, acceptance criteria, or something else?"

Do not proceed until a feature description has been provided.

## Execution

Run the Feature Design interaction model in order:

1. **[Project Owner]** — Restate the user problem and goal the feature serves, the success criteria, the known constraints, and the scope boundary as currently understood. This is a shared starting point that other personas can challenge.

2. **[System Architect]** — Evaluate technical approach options: what exists, what the structural implications of each are, what the tradeoffs are, and which approach is recommended and why. Flag any decisions that would be expensive to reverse.

3. **[Senior Developer]** — Assess whether the proposed approach can actually be built as described: hidden complexity, unresolved dependencies, effort realism, and what needs to be specified more precisely before a developer can start.

4. **[Devil's Advocate]** — Challenge the feature design: is the problem framing correct? Are we solving the right problem? Are scope assumptions justified? Are estimates credible? What are we assuming that might be wrong?

5. **[Cross-examination]** — Project Owner responds to scope and framing challenges from the DA; System Architect responds to implementability concerns from the Senior Developer; Senior Developer and DA address any architectural concerns they share or disagree on.

6. **[Synthesis — Project Owner + System Architect]** — Jointly produce the final feature specification.

Each persona must respond in character — voice, priorities, and concerns should reflect their definition in `agents/stable/`, not generic commentary.

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
