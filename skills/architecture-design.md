# Skill: Architecture Design

## Command

`/architecture-design`

## Description

Designs new systems, services, or significant architectural changes. Takes a design brief and returns a recommended architecture with rationale, key decisions, known risks, and a verdict.

Engaged when the decision will shape the technical landscape for years and the cost of getting it wrong is high.

No external dependencies — context is provided by the user directly.

## Team

`agents/teams/architecture-design.md`

Uses the default Architecture Design interaction model unless overridden below.

## Interaction model overrides

None. Use the full Architecture Design interaction model including cross-examination and synthesis.

## Context gathering

When `/architecture-design` is invoked:

1. If the user has included a design brief in the same message, use it directly
2. If invoked alone, prompt the user:

   > "Please describe what you need designed. Include: what system or change you're designing, the problem it solves, any constraints or requirements, existing architecture context that's relevant, and any approaches you've already considered or ruled out. There's no required format — write it however is natural."

3. Optionally ask: "Is there anything specific you want the team to focus on — component boundaries, scalability, security, org-level coherence, or something else?"

Do not proceed until a design brief has been provided.

## Execution

Run the Architecture Design interaction model in order:

1. **[System Architect]** — Propose or evaluate the architecture: component design, boundaries and interfaces, key technical decisions, tradeoffs considered, and rationale for the recommended approach. Explicitly name decisions that are hard to reverse.

2. **[Staff / Principal Engineer]** — Evaluate from the organisational and long-term view: cross-system coherence, alignment with technical strategy, duplication of existing capability, standards implications, and what this decision forecloses for the future.

3. **[Devil's Advocate]** — Challenge the architecture: what assumptions is this design making? What are the failure modes? What happens at scale, under load, or when the team changes? Were alternatives genuinely considered?

4. **[Project Owner]** — Evaluate proportionality: is the complexity justified by the value? Does this solve the actual user and business problem, or has the design drifted into interesting-but-unnecessary territory?

5. **[Cross-examination]** — System Architect responds to the DA's stress-test findings and the Staff/Principal's strategic concerns; Staff/Principal and DA address areas of agreement and disagreement; Project Owner responds to any scope or proportionality concerns raised.

6. **[Synthesis — System Architect]** — Produce the final architectural output.

Each persona must respond in character — voice, priorities, and concerns should reflect their definition in `agents/stable/`, not generic commentary.

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
