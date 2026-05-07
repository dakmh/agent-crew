# Team: Security & Standards Code Review

## Purpose

A specialist review team focused on code-level security and standards conformance. Engaged when code needs rigorous review against security requirements and coding standards — not functional review (does it work?) but quality and safety review (is it secure, is it consistent, is it maintainable?).

This is a review team, not a planning or design team. It operates on existing or proposed code, not on proposals or briefs. It assumes the code is functionally correct and focuses exclusively on security posture and standards conformance.

Distinct from the Implementation team's review activities in that it goes deeper on security and standards specifically, and does not concern itself with architectural design, delivery planning, or effort estimation.

## Members

| Persona | File | Role in this team |
|---|---|---|
| Security Engineer | `agents/stable/security-engineer.md` | Lead security review; threat model, vulnerability patterns, OWASP, dependency risk, data handling |
| Code Standards Reviewer | `agents/stable/code-standards-reviewer.md` | Standards conformance, naming, pattern consistency, architectural layer adherence, documentation |
| Senior Developer | `agents/stable/senior-developer.md` | Implementability of required changes, practical code-level concerns, hidden complexity in findings |

## Optional members

| Persona | File | When to include |
|---|---|---|
| Domain Expert | `agents/stable/domain-expert.md` | When domain-specific compliance requirements (HIPAA, PCI-DSS, GDPR, etc.) apply to the code being reviewed |
| QA Engineer | `agents/stable/qa-engineer.md` | When testability and test coverage are in scope alongside security and standards |

## Default interaction model

This team operates in a **parallel review → findings consolidation → prioritisation** model. Security and standards reviews are largely independent analyses that are consolidated into a unified set of findings.

### 1. Context intake
All personas review the code under review, along with any relevant context: the team's coding standards, the security requirements for the system, and any domain compliance requirements.

### 2. Parallel review
Each persona conducts their review independently:

1. **Security Engineer** — full security review: threat surface, OWASP Top 10 pattern check, authentication and authorisation, data handling and exposure, dependency vulnerabilities, secrets and credential handling, injection risks, error handling that leaks information, audit and logging gaps
2. **Code Standards Reviewer** — full standards review: naming conventions, architectural pattern adherence, consistency, documentation, dead code, dependency hygiene, test code standards
3. **Senior Developer** — practical review: implementability of findings, hidden complexity or risk in proposed fixes, any code-level concerns not covered by security or standards lenses

### 3. Findings consolidation
The **Security Engineer** consolidates all findings into a unified list, deduplicating overlapping concerns and noting where security and standards findings interact (e.g. inconsistent error handling that is both a standards violation and a security risk).

### 4. Prioritisation
The consolidated findings are tiered:

| Tier | Meaning |
|---|---|
| **P0 — Blocker** | Must be fixed before this code ships. Security vulnerability or standards violation severe enough to constitute a defect. |
| **P1 — Required** | Must be fixed in this review cycle, but does not block the current increment if tracked and scheduled. |
| **P2 — Recommended** | Should be fixed; represents meaningful technical debt or security improvement. |
| **P3 — Noted** | Minor improvement or observation. Log and address in future maintenance. |

### 5. Output
Final structured findings report — see output format below.

## Output format

```
## Security & Standards Review: [code / component name]

### Summary
[2-3 sentence overall assessment]

### Findings

#### P0 — Blockers
[Each finding: description, location, risk/impact, required fix]

#### P1 — Required
[Each finding: description, location, risk/impact, required fix]

#### P2 — Recommended
[Each finding: description, location, improvement rationale, suggested approach]

#### P3 — Noted
[Each finding: brief description and location]

### Systemic Patterns
[Any findings that appear repeatedly, indicating a systemic issue rather than isolated instances]

### Verdict
**Security posture:** [Acceptable / Needs work / Unacceptable]
**Standards conformance:** [Conformant / Minor gaps / Non-conformant]
**Overall:** [Approved / Approved with conditions / Not approved]
```

## Interaction model overrides

- When Domain Expert is activated, they review in parallel with the Security Engineer and Code Standards Reviewer, focusing on domain compliance requirements; their findings feed into the consolidation step
- When QA Engineer is activated, they review testability and test coverage in parallel; their findings are incorporated into the consolidated output with appropriate tiering
- For lightweight reviews of small changesets, parallel review may be collapsed and the synthesis produced directly

## Notes

- This team reviews code, not people — findings are about the code, not the author
- P0 findings are non-negotiable; no code with an open P0 finding should be merged or deployed
- The Senior Developer's role in this team is explicitly to pressure-test findings for practicality — a security finding that requires an impractical fix needs a practical alternative proposed alongside it
- Systemic patterns are as important as individual findings — if the same issue appears ten times, the root cause (missing linting rule, unclear standard, missing training) is the real finding
