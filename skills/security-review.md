# Skill: Security Review

## Command

`/security-review`

## Description

Code-level security and standards review. Takes code (pasted directly or described by component) and returns a structured findings report tiered by severity.

Focuses exclusively on security posture and standards conformance — not on whether the code works. Assumes functional correctness.

## Team

`agents/teams/security-standards-review.md`

Uses the default Security & Standards Code Review interaction model unless overridden below.

## Interaction model overrides

None. Use the full interaction model: parallel review → findings consolidation → prioritisation.

## Context gathering

When `/security-review` is invoked:

1. If code has been included in the same message, use it directly
2. If invoked alone, prompt the user:

   > "Please paste the code you'd like reviewed, or describe the component if it's too large to paste in full. Include any relevant context: what it does, what system it's part of, and any known constraints."

3. Ask the following optional context questions:

   - **Coding standards**: "Are there specific coding standards, style guides, or architectural patterns this code should conform to? If not, I'll apply general best practices."
   - **Domain**: "Does this code operate in a regulated domain (e.g. healthcare, payments, financial services)? If so, I'll activate the Domain Expert for compliance-specific findings."
   - **Specific concerns**: "Are there particular areas you're concerned about, or anything you'd like the team to focus on?"

   These are optional — if the user wants to proceed without answering, do so using whatever context is available.

4. Activate optional team members based on context:
   - **Domain Expert**: activate if a regulated domain is specified or clearly implied by the code
   - **QA Engineer**: activate if the user explicitly asks for testability or test coverage review

Do not proceed until code or a clear code description has been provided.

## Execution

Run the Security & Standards Code Review interaction model:

1. **[Security Engineer]** — Full security review in character: threat surface, OWASP Top 10 patterns, authentication and authorisation, data handling and exposure, dependency vulnerabilities, secrets and credential handling, injection risks, error handling that leaks information, audit and logging gaps.

2. **[Code Standards Reviewer]** — Full standards review in character: naming conventions, architectural pattern adherence, consistency, documentation, dead code, dependency hygiene, test code standards.

3. **[Senior Developer]** — Practical review in character: implementability of findings, hidden complexity or risk in proposed fixes, any code-level concerns not covered by the security or standards lenses.

4. If Domain Expert is activated: domain compliance review in parallel with steps 1–3, focusing on regulatory requirements relevant to the specified domain. Findings feed into consolidation.

5. If QA Engineer is activated: testability and test coverage review in parallel with steps 1–3. Findings feed into consolidation.

6. **[Security Engineer — Consolidation]** — Consolidate all findings, deduplicate overlapping concerns, note where security and standards findings interact.

7. **[Security Engineer — Prioritisation]** — Tier all findings P0–P3 and produce the final report.

Each persona must respond in character — voice, priorities, and concerns should reflect their definition in `agents/stable/`, not generic commentary.

## Output format

Use the output format defined in `agents/teams/security-standards-review.md`:

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

If no findings exist in a tier, omit that tier rather than printing an empty section.

## Example invocation

```
/security-review

This is our authentication middleware. It validates JWTs and attaches the user to the
request context. Stack is Express + Node.js. We use RS256 tokens issued by our own
auth service.

[code pasted here]
```
