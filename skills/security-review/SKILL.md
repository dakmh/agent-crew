---
name: security-review
description: "Code-level security and standards review by the Security & Standards Review team, returning findings classified P0-P4 per the code-review-severity standard. Use when asked for a security review, security audit, or vulnerability check of code, to review auth/crypto/input-handling code, to check standards conformance or secure coding practices, or when the user says 'security review this', 'check this for vulnerabilities', 'is this code secure', or invokes /security-review. Assumes functional correctness; reviews security posture and standards only."
---

# Skill: Security Review

> **Loading:** all repo-relative paths in this file (`skills/_conventions.md`, `crew/…`,
> `standards/…`) resolve from the plugin root — `${CLAUDE_PLUGIN_ROOT}` when installed as a
> plugin, the repository root in a checkout. Before running: load `skills/_conventions.md`
> (shared protocol), the team file referenced below, every persona the team lists, and any
> standard referenced by the skill, team, or personas.

## Command

`/agent-crew:security-review` (installed as a plugin) — historically bare `/security-review` in
pre-plugin setups; treat both as this skill.

## Description

Code-level security and standards review. Takes code (pasted directly or described by component) and returns a structured findings report classified per `standards/code-review-severity.md` (P0–P4).

Focuses exclusively on security posture and standards conformance — not on whether the code works. Assumes functional correctness.

## Team

`crew/teams/security-standards-review.md`

Conditionally activates optional members:
- **Domain Expert** — when a regulated domain (e.g. healthcare, payments, financial services) is specified or clearly implied by the code, for compliance-specific findings.
- **QA Engineer** — when the user explicitly asks for testability or test coverage review.

## Interaction model

Follow the team's default interaction model in `crew/teams/security-standards-review.md`,
**including its Execution section** — this team dispatches real subagents by default rather
than running fully in-context; that's a property of the team, not an override here. The shared
protocol in `skills/_conventions.md` applies.

No overrides.

## Context gathering

Per `skills/_conventions.md`. Required context: code, pasted directly, described by component,
or given as a path/file reference in the current checkout (dispatched subagents can `Read`/`Grep`
a path themselves; a paste is still fine and is required when the code isn't in a checkout this
session can reach).

> "Please paste the code you'd like reviewed, describe the component if it's too large to paste in full, or point me at the file(s)/path in this checkout. Include any relevant context: what it does, what system it's part of, and any known constraints."

Optional focus questions:
- **Coding standards**: "Are there specific coding standards, style guides, or architectural patterns this code should conform to? If not, I'll apply general best practices."
- **Domain**: "Does this code operate in a regulated domain (e.g. healthcare, payments, financial services)? If so, I'll activate the Domain Expert for compliance-specific findings."
- **Specific concerns**: "Are there particular areas you're concerned about, or anything you'd like the team to focus on?"

## Output format

Use the output format defined in `crew/teams/security-standards-review.md`.

## Example invocation

```
/security-review

This is our authentication middleware. It validates JWTs and attaches the user to the
request context. Stack is Express + Node.js. We use RS256 tokens issued by our own
auth service.

[code pasted here]
```
