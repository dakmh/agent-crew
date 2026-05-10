# Team: Technical Discovery

## Purpose

An exploratory team for investigating an ambiguous problem space before any design is committed. Engaged when the team knows *roughly* what problem they need to solve but not yet how — or when they suspect their current understanding of the problem may itself be wrong.

This team does not produce a design or a decision. It produces a structured map of the territory: what is known, what is unknown, what options exist, and what assumptions need to be validated before meaningful design can begin.

Distinct from the Architecture Design team in that it operates before design — its output is the input to design work, not design itself. Distinct from the General Review team in that there is no proposal to evaluate; the work is exploration, not critique.

## Members

| Persona | File | Role in this team |
|---|---|---|
| Project Owner | `agents/stable/project-owner.md` | Problem framing; anchors discovery to real user and business needs; prevents exploration from drifting into interesting-but-irrelevant territory |
| System Architect | `agents/stable/system-architect.md` | Technical landscape mapping; identifies the solution space, key unknowns, and approach options |
| Devil's Advocate | `agents/stable/devils-advocate.md` | Challenges assumptions about the problem itself — not just the solutions |
| Domain Expert | `agents/stable/domain-expert.md` | Domain constraints, known patterns, prior art, and the mistakes everyone makes the first time in this space |

## Optional members

| Persona | File | When to include |
|---|---|---|
| Staff / Principal Engineer | `agents/stable/staff-principal-engineer.md` | When the problem has org-level or cross-system implications that should shape the discovery |
| Senior Developer | `agents/stable/senior-developer.md` | When implementation feasibility signals are needed to bound the option space |

## Default interaction model

This team operates in a **problem framing → domain landscape → technical landscape → assumption challenge → synthesis** model. The output is a discovery report, not a design or a recommendation.

### 1. Context intake
All personas review the problem statement, any existing context, and the questions the team most needs to answer. No responses yet.

### 2. Problem framing
**Project Owner** articulates the problem as they currently understand it: what user or business need drives this, what success looks like, what constraints exist, and what questions need to be answered before design can begin. This framing is deliberately provisional — it is the starting point, not the conclusion.

### 3. Domain landscape
**Domain Expert** maps the domain context: what does this problem look like in this domain? What patterns, standards, or prior art are relevant? What constraints does the domain impose? What are the known failure modes that teams encounter in this space?

### 4. Technical landscape
**System Architect** maps the technical solution space: what approaches exist? What are their tradeoffs? What technical unknowns need to be resolved before a design can be committed? What spikes or prototypes would reduce the key uncertainties?

### 5. Assumption challenge
**Devil's Advocate** challenges the foundations: what assumptions is the problem framing making? What if the problem is different from how it's been described? What are we not considering? What would cause all of the options identified to fail?

### 6. Synthesis
**Project Owner** and **System Architect** jointly produce the discovery report:

**What we know**
- Confirmed facts about the problem and domain
- Constraints that are fixed
- Options that are clearly ruled out and why

**What we don't know**
- Key uncertainties that must be resolved before design can start
- Assumptions embedded in the current problem framing that need validation

**Option space**
- Identified approaches with tradeoffs (no recommendation at this stage unless one option is clearly dominant)
- For each option: what would need to be true for it to be the right choice

**Recommended next steps**
- Spikes, prototypes, or research that would reduce the highest-priority uncertainties
- Questions to answer before the Architecture Design or Feature Design team is engaged
- Whether the problem framing needs revision before proceeding

## Interaction model overrides

- When Staff / Principal Engineer is activated, they contribute after the domain landscape, providing org-level context that should shape the technical landscape mapping
- When Senior Developer is activated, they contribute after the technical landscape, providing a practical feasibility signal on the options identified
- For narrow or well-understood problem spaces, steps 3 and 4 may be collapsed

## Notes

- This team explicitly does not make design decisions — premature convergence on a solution during discovery is a failure mode, not a success
- The Devil's Advocate's most important contribution here is questioning the problem framing, not the solutions — discovering you're solving the wrong problem during discovery is far cheaper than discovering it during implementation
- The Domain Expert's inference behaviour applies: if no domain is specified, they infer from context and state that inference explicitly
- A good discovery report makes the subsequent design work faster and more confident — not by answering all questions, but by identifying exactly which questions matter
