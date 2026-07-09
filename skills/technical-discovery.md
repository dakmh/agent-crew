# Skill: Technical Discovery

## Command

`/technical-discovery`

## Description

Maps an ambiguous problem space before any design is committed. Takes a problem statement and returns a structured discovery report: what is known, what is unknown, what options exist, and what must be resolved before design can begin.

## Team

`agents/teams/technical-discovery.md`

## Interaction model

Follow the team's default interaction model in `agents/teams/technical-discovery.md`. The shared protocol in `skills/_conventions.md` applies.

No overrides.

## Context gathering

Per `skills/_conventions.md`. Required context: a description of the problem space to map.

> "Please describe the problem you're trying to map. Include: what you're trying to accomplish, any constraints or requirements you know about, what you already know or have ruled out, and what questions you most need answered. There's no required format — write it however is natural."

Optional focus question: "Is there a domain or industry context I should apply (e.g. payments, healthcare, real-time systems)? If not, I'll infer it from context."

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

## Example invocation

```
/technical-discovery

We want to add offline support to our field-service app so technicians can work in
areas with no signal, but we're not sure what "offline" should even mean here — full
read/write, read-only, or queued actions. Data is currently server-authoritative and
some records are edited by multiple technicians. We haven't picked a sync approach and
want to understand the option space and the risks before committing to a design.
```
