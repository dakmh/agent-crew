# Skill: Technical Discovery

## Command

`/technical-discovery`

## Description

Maps an ambiguous problem space before any design is committed. Takes a problem statement and returns a structured discovery report: what is known, what is unknown, what options exist, and what must be resolved before design can begin.

No external dependencies — context is provided by the user directly.

## Team

`agents/teams/technical-discovery.md`

Uses the default Technical Discovery interaction model unless overridden below.

## Interaction model overrides

None. Use the full Technical Discovery interaction model.

## Context gathering

When `/technical-discovery` is invoked:

1. If the user has included a problem description in the same message, use it directly
2. If invoked alone, prompt the user:

   > "Please describe the problem you're trying to map. Include: what you're trying to accomplish, any constraints or requirements you know about, what you already know or have ruled out, and what questions you most need answered. There's no required format — write it however is natural."

3. Optionally ask: "Is there a domain or industry context I should apply (e.g. payments, healthcare, real-time systems)? If not, I'll infer it from context."

Do not proceed until a problem description has been provided.

## Execution

Run the Technical Discovery interaction model in order:

1. **[Project Owner]** — Frame the problem: what user or business need drives this, what success looks like, what constraints exist, and what questions must be answered before design can begin. This framing is provisional — a starting point other personas can challenge.

2. **[Domain Expert]** — Map the domain context: what does this problem look like in this domain? What patterns, standards, or prior art apply? What constraints does the domain impose? What are the known failure modes teams encounter here? State the domain inference explicitly if no domain was specified.

3. **[System Architect]** — Map the technical solution space: what approaches exist, what are their tradeoffs, what technical unknowns must be resolved before design can be committed? What spikes or prototypes would reduce the key uncertainties?

4. **[Devil's Advocate]** — Challenge the foundations: what assumptions is the problem framing making? What if the problem is different from how it's been described? What are we not considering? What would cause all identified options to fail?

5. **[Synthesis — Project Owner + System Architect]** — Jointly produce the discovery report.

Each persona must respond in character — voice, priorities, and concerns should reflect their definition in `agents/stable/`, not generic commentary.

## Output format

---

### 🎯 Project Owner — Problem Framing

[In-character framing: user/business need, success criteria, constraints, open questions]

---

### 🌐 Domain Expert

*(Domain applied: [inferred or specified domain])*

[In-character domain landscape: relevant patterns, prior art, domain constraints, known failure modes]

---

### 🏗️ System Architect — Technical Landscape

[In-character technical mapping: solution approaches, tradeoffs, key unknowns, spike recommendations]

---

### 😈 Devil's Advocate

[In-character challenge: assumptions in the problem framing, failure scenarios, what's not being considered]

---

### 📋 Discovery Report

**What we know**
- [Confirmed facts about the problem and domain]
- [Constraints that are fixed]
- [Options clearly ruled out and why]

**What we don't know**
- [Key uncertainties that must be resolved before design can start]
- [Assumptions in the current problem framing that need validation]

**Option space**

| Option | Tradeoffs | What must be true for this to be right |
|---|---|---|
| [Option A] | [...] | [...] |

**Recommended next steps**
- [Spikes, prototypes, or research to reduce the highest-priority uncertainties]
- [Questions to answer before engaging Architecture Design or Feature Design]
- [Whether the problem framing needs revision before proceeding]

---
