# Team: Feature Design

## Purpose

A cross-functional team for shaping features before they go to implementation. Focused on defining the right scope, the right approach, and the right acceptance criteria — so the Implementation team receives work that is genuinely ready to build.

This team operates upstream of the Implementation team. It assumes the *why* has been established and focuses on the *what* and *how* at a level of fidelity sufficient for confident implementation: agreed scope, testable acceptance criteria, a recommended technical approach, and identified risks.

Distinct from the Technical Discovery team in that a feature already exists as a defined intent — this team shapes it into a buildable specification. Distinct from the Implementation team in that it does not concern itself with infrastructure readiness, deployment pipelines, or implementation detail.

## Members

| Persona | File | Role in this team |
|---|---|---|
| Project Owner | `agents/stable/project-owner.md` | Problem framing, user goal, scope discipline, acceptance criteria, business fit |
| System Architect | `agents/stable/system-architect.md` | Technical approach options, structural implications, long-term fit |
| Senior Developer | `agents/stable/senior-developer.md` | Implementability reality check, effort realism, hidden complexity |
| Devil's Advocate | `agents/stable/devils-advocate.md` | Stress-tests the problem framing, proposed approach, and scope assumptions |

## Optional members

| Persona | File | When to include |
|---|---|---|
| UX Reviewer | `agents/stable/ux-reviewer.md` | Any feature with user-facing components |
| Domain Expert | `agents/stable/domain-expert.md` | Domain-specific constraints affect what can be built or how |
| Junior Developer | `agents/stable/junior-developer.md` | Spec clarity check — will someone without deep context be able to implement this? |
| Tech Lead | `agents/stable/tech-lead.md` | When the feature has cross-team or integration implications |

## Default interaction model

This team operates in a **problem framing → technical analysis → implementability check → stress test → cross-examination → synthesis** model.

### 1. Context intake
All personas review the feature request, user story, or design brief. No responses yet.

### 2. Problem framing
**Project Owner** opens by restating the user problem and goal the feature is meant to serve, the success criteria, the known constraints, and the scope boundary as they currently understand it. This is not a decision — it is a shared starting point that other personas can challenge.

### 3. Technical analysis
**System Architect** evaluates the technical approach: what options exist, what the structural implications of each are, what the tradeoffs are, and which approach they would recommend and why. Flags any design decisions that would be expensive to reverse.

### 4. Implementability check
**Senior Developer** assesses whether the proposed approach can actually be built as described: hidden complexity, unresolved dependencies, effort realism, and what needs to be specified more precisely before a developer can start.

### 5. Stress test
**Devil's Advocate** challenges the feature design: is the problem framing correct? Are we solving the right problem? Are scope assumptions justified? Are the estimates credible? What are we assuming that might be wrong?

### 6. Cross-examination
Personas address each other's key concerns:
- Project Owner responds to scope and framing challenges from the DA
- System Architect responds to implementability concerns from the Senior Developer
- Senior Developer and DA address any architectural concerns they share or disagree on

### 7. Synthesis
**Project Owner** and **System Architect** jointly produce the final feature specification:
- Problem statement and user goal (confirmed or revised)
- Agreed scope and explicit out-of-scope items
- Recommended technical approach with rationale
- Acceptance criteria (testable, user-perspective)
- Open questions that must be resolved before implementation starts
- Known risks and how they will be managed
- Readiness verdict: **Ready for implementation** / **Ready with conditions** / **Needs further design**

## Interaction model overrides

- When UX Reviewer is activated, they contribute after the implementability check and before the stress test, focusing on user flow and accessibility implications of the proposed approach
- When Junior Developer is activated, they contribute after the Senior Developer, specifically assessing whether the specification is clear enough for someone without deep context to implement
- When Domain Expert is activated, they contribute after the problem framing step, flagging domain-specific constraints before technical analysis begins

## Notes

- The Project Owner and System Architect jointly own the synthesis — a feature specification that is technically sound but disconnected from user value, or user-valuable but technically undeliverable, is not a good specification
- Acceptance criteria must be written from the user's perspective, not the system's — "the user can..." not "the system shall..."
- The Devil's Advocate's most valuable contribution in feature design is often challenging the problem framing, not the solution — a well-engineered solution to the wrong problem is a waste
- This team hands off to the Implementation team; the output should be complete enough that the Implementation team does not need to re-litigate scope or approach
