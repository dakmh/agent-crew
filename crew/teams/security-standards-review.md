# Team: Security & Standards Code Review

## Purpose

A specialist review team focused on code-level security and standards conformance. Engaged when code needs rigorous review against security requirements and coding standards — not functional review (does it work?) but quality and safety review (is it secure, is it consistent, is it maintainable?).

This is a review team, not a planning or design team. It operates on existing or proposed code, not on proposals or briefs. It assumes the code is functionally correct and focuses exclusively on security posture and standards conformance.

Distinct from the Implementation team's review activities in that it goes deeper on security and standards specifically, and does not concern itself with architectural design, delivery planning, or effort estimation.

## Members

| Persona | File | Role in this team |
|---|---|---|
| Security Engineer | `crew/stable/security-engineer.md` | Lead security review; threat model, vulnerability patterns, OWASP, dependency risk, data handling |
| Code Standards Reviewer | `crew/stable/code-standards-reviewer.md` | Standards conformance, naming, pattern consistency, architectural layer adherence, documentation |
| Senior Developer | `crew/stable/senior-developer.md` | Implementability of required changes, practical code-level concerns, hidden complexity in findings |

## Optional members

| Persona | File | When to include |
|---|---|---|
| Domain Expert | `crew/stable/domain-expert.md` | When domain-specific compliance requirements (HIPAA, PCI-DSS, GDPR, etc.) apply to the code being reviewed |
| QA Engineer | `crew/stable/qa-engineer.md` | When testability and test coverage are in scope alongside security and standards |

## Execution

**This team dispatches real subagents by default** — see `skills/_conventions.md` → Execution
substrate for the general rule; this is the worked example it points to. It qualifies because
step 2 has no cross-persona visibility requirement: every member reviews the same fixed
artifact independently, and nothing in this team's model asks one member to read another's
draft before finishing their own. Only the consolidation step (3) needs to see every member's
output, and that's the dispatcher's job — dispatched-subagent results already return to
whoever dispatched them, so no extra machinery is needed for it.

Dispatch mechanics for step 2:
- One `Agent` call per active member (core three, plus Domain Expert and/or QA Engineer when
  activated), all issued in the same response so they run concurrently. No `name` argument —
  these are plain subagents, not the experimental agent-teams feature.
- `subagent_type: Explore` for every member. Explore excludes Edit/Write, so a reviewer cannot
  drift into fixing the code instead of reporting on it — a real constraint the in-context
  fallback below can't offer, since a single roleplaying session always keeps its full tool
  access regardless of which persona it's voicing. (Explore still has Bash, so this is a strong
  default, not a hard sandbox — note that in the disclosure if it matters for the artifact at
  hand.)
- Each subagent's prompt contains: the persona file's content verbatim (`crew/stable/…`), the
  code or component under review (or a path/description for the subagent to `Read`/`Grep`
  itself if it lives in the checkout), any coding-standards or domain-compliance context
  gathered from the user, and an instruction to return findings only, in the persona's own
  voice, with no meta-commentary about being a subagent.
- **Fallback:** for a small, well-defined change (roughly: a single file or a diff under ~150
  lines) or when the `Agent` tool is unavailable, collapse to in-context — one session voices
  all active members sequentially, per the default substrate in `skills/_conventions.md`. State
  which path was taken at the top of the output either way.

## Default interaction model

This team operates in a **independent review → findings consolidation → classification** model.
Security and standards reviews are independent analyses that are consolidated into a unified
set of findings; nothing before consolidation requires cross-persona visibility.

### 1. Context intake
The dispatcher (or, in-context, each persona) gathers the code under review and any relevant
context: the team's coding standards, the security requirements for the system, and any domain
compliance requirements.

### 2. Independent review
Each active member reviews the artifact independently — dispatched as parallel subagents by
default, per Execution above:

1. **Security Engineer** — full security review: threat surface, OWASP Top 10 pattern check, authentication and authorisation, data handling and exposure, dependency vulnerabilities, secrets and credential handling, injection risks, error handling that leaks information, audit and logging gaps
2. **Code Standards Reviewer** — full standards review: naming conventions, architectural pattern adherence, consistency, documentation, dead code, dependency hygiene, test code standards
3. **Senior Developer** — an independent implementability pass over the same artifact: hidden complexity or risk in the code as written, any code-level concerns not covered by security or standards lenses. (Not a review *of the other members' findings* — see the note below.)

### 3. Findings consolidation
The **dispatcher** consolidates all returned reports into a unified list — in the Security
Engineer's voice when in-context, or directly (informed by the Security Engineer persona's
consolidation criteria) when the members were dispatched as subagents, since no single member
saw the others' output to consolidate from. Consolidation: deduplicate overlapping concerns,
note where security and standards findings interact (e.g. inconsistent error handling that is
both a standards violation and a security risk), and use the Senior Developer's independent
notes to pressure-test the security/standards findings for practicality — proposing a practical
alternative alongside any finding whose fix, as stated, isn't realistically implementable. This
is where the Notes section's "pressure-test findings for practicality" actually happens; it was
previously described as if the Senior Developer did it directly, which conflicted with step 2
being independent — resolved here in favour of independence, since nothing in this team's
design otherwise needs the Senior Developer to see findings before reviewing the code.

### 4. Classification
Findings are classified per the code review severity standard in `standards/code-review-severity.md` — load it with this team. Each finding is graded independently against the standard's absolute criteria and labelled with both its P-value and verbal tier (P0 — Blocker through P4 — Info). Security findings additionally carry a CVSS base score and vector per the standard's security findings protocol.

### 5. Output
Final structured findings report — see output format below.

## Output format

```
## Security & Standards Review: [code / component name]

### Summary
[2-3 sentence overall assessment]

### Findings

#### P0 — Blocker
[Each finding: description, location, risk/impact, required fix. Security findings: CVSS score + vector]

#### P1 — Critical
[Each finding: description, location, risk/impact, required fix. Security findings: CVSS score + vector]

#### P2 — Major
[Each finding: description, location, improvement rationale, suggested approach]

#### P3 — Minor
[Each finding: brief description and location]

#### P4 — Info
[Each observation: brief description; no action required]

### Systemic Patterns
[Any findings that appear repeatedly, indicating a systemic issue rather than isolated instances]

### Verdict
**Security posture:** [Acceptable / Needs work / Unacceptable]
**Standards conformance:** [Conformant / Minor gaps / Non-conformant]
**Overall** (per `standards/review-verdicts.md`)**:** [Proceed / Proceed with conditions / Do not proceed]
```

Prepend a one-line disclosure above `### Summary` stating the substrate used, e.g. `_Dispatched as
N parallel subagents._` or `_Run in-context (small changeset)._`

## Interaction model overrides

- When Domain Expert is activated, they are dispatched alongside the Security Engineer and Code Standards Reviewer (or, in-context, review alongside them), focusing on domain compliance requirements; their findings feed into the consolidation step
- When QA Engineer is activated, they review testability and test coverage the same way; their findings are incorporated into the consolidated output with appropriate tiering
- For lightweight reviews of small changesets, dispatch is skipped in favour of the in-context fallback (see Execution above) and the synthesis produced directly

## Assumptions

This team's subagent dispatch depends on: the `Agent` tool being available and callable without
a `name` argument for plain background subagents, and `Explore` remaining a read-oriented
built-in subagent type. If either stops holding, fall back to in-context (already the documented
default) until this section is revisited. Worth reconsidering at that time: whether
`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` has stabilized enough to justify moving *other* teams —
ones with a cross-examination step, which this one deliberately avoids needing — onto real
per-persona independence via message-passing teammates rather than in-context roleplay. See
`docs/capability-audit.md`.

## Notes

- This team reviews code, not people — findings are about the code, not the author
- P0 findings are non-negotiable; no code with an open P0 finding should be merged or deployed
- Pressure-testing findings for practicality happens at consolidation, using the Senior Developer's independent notes — see step 3. A security finding that requires an impractical fix needs a practical alternative proposed alongside it.
- Systemic patterns are as important as individual findings — if the same issue appears ten times, the root cause (missing linting rule, unclear standard, missing training) is the real finding
