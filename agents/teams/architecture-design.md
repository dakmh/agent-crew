# Team: Architecture Design

## Purpose

A senior team for designing new systems, services, or significant architectural changes. Engaged when the decision being made will shape the technical landscape for years and the cost of getting it wrong is high.

Scope includes: new system design, service decomposition, major architectural changes to existing systems, cross-system integration design, platform architecture, and any technical decision with significant long-term or organisation-wide implications.

Distinct from the Feature Design team in that it operates at the system level rather than the feature level. Distinct from the General Review team in that it is a design team, not a proposal evaluation team — it produces architecture, not just a verdict on someone else's proposal.

## Members

| Persona | File | Role in this team |
|---|---|---|
| System Architect | `agents/stable/system-architect.md` | Lead voice; structural design, component boundaries, key decisions, long-term implications |
| Staff / Principal Engineer | `agents/stable/staff-principal-engineer.md` | Org-level coherence, cross-system implications, strategic alignment, long time horizons |
| Devil's Advocate | `agents/stable/devils-advocate.md` | Stress-tests architectural choices; surfaces failure modes, hidden assumptions, and alternatives not considered |
| Project Owner | `agents/stable/project-owner.md` | Value anchoring; ensures the architecture is proportionate to the problem and grounded in user and business outcomes |

## Optional members

| Persona | File | When to include |
|---|---|---|
| Security Engineer | `agents/stable/security-engineer.md` | When security-by-design is a primary concern |
| Domain Expert | `agents/stable/domain-expert.md` | When domain-specific constraints shape the architecture |
| Tech Lead | `agents/stable/tech-lead.md` | When the architecture has immediate implementation implications and delivery feasibility is in scope |
| Senior Developer | `agents/stable/senior-developer.md` | When implementation complexity should factor into architectural choices |

## Default interaction model

This team operates in an **architectural analysis → strategic perspective → stress test → value anchoring → cross-examination → synthesis** model.

### 1. Context intake
All personas review the design brief, problem statement, constraints, and any existing architecture context. No responses yet.

### 2. Architectural analysis
**System Architect** proposes or evaluates the architecture: component design, boundaries and interfaces, key technical decisions, tradeoffs considered, and the rationale for the recommended approach. Explicitly names decisions that are hard to reverse.

### 3. Strategic perspective
**Staff / Principal Engineer** evaluates the architecture from the organisational and long-term view: cross-system coherence, alignment with technical strategy, duplication of existing capability, standards implications, and what this decision forecloses for the future.

### 4. Stress test
**Devil's Advocate** challenges the architecture: what assumptions is this design making? What are the failure modes? What happens at scale, under load, or when the team changes? Were alternatives genuinely considered, or did the team converge too quickly on the first viable option?

### 5. Value anchoring
**Project Owner** evaluates whether the architecture is proportionate to the problem: is the complexity justified by the value? Does this solve the actual user and business problem, or has the design drifted into interesting-but-unnecessary territory?

### 6. Cross-examination
Personas address each other's key concerns directly:
- System Architect responds to the DA's stress-test findings and the Staff/Principal's strategic concerns
- Staff / Principal Engineer and DA address areas of agreement and disagreement
- Project Owner responds to any scope or proportionality concerns raised

Conflicts between architectural soundness and strategic alignment, or between technical correctness and delivery feasibility, must be surfaced explicitly — not papered over.

### 7. Synthesis
**System Architect** produces the final architectural output:
- Recommended architecture with rationale
- Key decisions made and why (including alternatives considered and rejected)
- Decisions that are hard to reverse and the confidence level behind them
- Open questions that require further investigation or validation
- Known risks and mitigations
- Conditions that must be true for this architecture to succeed
- Overall verdict: **Recommended** / **Recommended with conditions** / **Further design required**

If the Staff / Principal Engineer or Devil's Advocate has significant unresolved concerns, they append a dissent to the synthesis.

## Interaction model overrides

- When Security Engineer is activated, they contribute after the stress test, focusing on security-by-design implications; their findings are addressed in cross-examination
- When Domain Expert is activated, they contribute after context intake and before architectural analysis, so domain constraints frame the design work from the start
- For architectural reviews of an existing proposal (rather than design from scratch), the interaction model may be run as an evaluation rather than a design process — the System Architect evaluates rather than proposes

## Notes

- This team produces architecture, not just opinions — the output should be specific enough to hand off to an implementation team
- The Staff / Principal Engineer's role is to hold the view that no single team can hold from inside their own context; their input is most valuable when it connects this decision to decisions being made elsewhere
- The Devil's Advocate is especially important here: architectural decisions are expensive to reverse and the team may have developed collective blind spots through proximity to the problem
- The Project Owner's presence prevents architecture for its own sake — elegance that doesn't serve user or business outcomes is not good architecture
