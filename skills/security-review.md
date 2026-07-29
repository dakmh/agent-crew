# Skill: Security Review

## Command

`/security-review`

## Description

Code-level security and standards review. Takes code (pasted directly or described by component) and returns a structured findings report classified per `standards/code-review-severity.md` (P0–P4).

Focuses exclusively on security posture and standards conformance — not on whether the code works. Assumes functional correctness.

## Team

`agents/teams/security-standards-review.md`

Conditionally activates optional members:
- **Domain Expert** — when a regulated domain (e.g. healthcare, payments, financial services) is specified or clearly implied by the code, for compliance-specific findings.
- **QA Engineer** — when the user explicitly asks for testability or test coverage review.

## Interaction model

Follow the team's default interaction model in `agents/teams/security-standards-review.md`. The shared protocol in `skills/_conventions.md` applies.

No overrides.

## Context gathering

Per `skills/_conventions.md`. Required context: code, pasted directly or described by component.

> "Please paste the code you'd like reviewed, or describe the component if it's too large to paste in full. Include any relevant context: what it does, what system it's part of, and any known constraints."

Optional focus questions:
- **Coding standards**: "Are there specific coding standards, style guides, or architectural patterns this code should conform to? If not, I'll apply general best practices."
- **Domain**: "Does this code operate in a regulated domain (e.g. healthcare, payments, financial services)? If so, I'll activate the Domain Expert for compliance-specific findings."
- **Specific concerns**: "Are there particular areas you're concerned about, or anything you'd like the team to focus on?"

## Output format

Use the output format defined in `agents/teams/security-standards-review.md`.

## Example invocation

```
/security-review

This is our authentication middleware. It validates JWTs and attaches the user to the
request context. Stack is Express + Node.js. We use RS256 tokens issued by our own
auth service.

[code pasted here]
```
