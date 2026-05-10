# Team: Release Management

## Purpose

A cross-functional team for coordinating, gating, and planning software releases. Focused on release readiness — determining whether what has been built is genuinely ready to ship, producing a clear go/no-go verdict, and documenting the plan for execution and recovery.

This team operates downstream of implementation. It does not revisit implementation decisions or feature scope — those are settled. It asks: is this safe to ship, do we have a recovery plan if it is not, and is everything in place for a controlled, observable deployment?

For mobile applications, this team explicitly addresses app store submission timing, phased rollout strategy, and the constrained incident response window that app store review cycles create.

## Members

| Persona | File | Role in this team |
|---|---|---|
| Release Manager | `agents/stable/release-manager.md` | Release coordination, go/no-go criteria, rollback planning, communication plan, versioning |
| Tech Lead | `agents/stable/tech-lead.md` | Technical readiness assessment, dependency verification, integration risk |
| DevOps / Platform Engineer | `agents/stable/devops-platform-engineer.md` | Deployment pipeline readiness, observability, environment parity, rollback execution |
| QA Engineer | `agents/stable/qa-engineer.md` | Test completion status, known defect triage, acceptance criteria sign-off |
| Devil's Advocate | `agents/stable/devils-advocate.md` | Challenges readiness assumptions, stress-tests the rollback plan, questions whether risks are genuinely mitigated or merely accepted |

## Optional members

| Persona | File | When to include |
|---|---|---|
| Security Engineer | `agents/stable/security-engineer.md` | When the release includes security-sensitive changes, new attack surface, or compliance-relevant modifications |
| Mobile App Developer | `agents/stable/mobile-app-developer.md` | When the release includes a mobile client component requiring app store submission |
| Product Manager | `agents/stable/product-manager.md` | When the release involves significant user-facing changes, a coordinated launch, or requires stakeholder communication planning |

## Default interaction model

This team operates in a **criteria evaluation → risk assessment → gap resolution → readiness verdict** model. Unlike design or implementation teams, this team does not generate options or explore approaches — it evaluates specific, concrete readiness criteria and produces a structured verdict.

### 1. Context intake
All personas review the release brief: what is being shipped, to which environments and platforms, what the expected user impact is, and what has already been verified. No responses yet.

### 2. Criteria evaluation
Each persona evaluates readiness from their domain independently:

1. **Tech Lead** — Are all intended changes included? Are integration points with other systems verified? Are there unresolved technical dependencies or sequencing requirements?
2. **DevOps / Platform Engineer** — Is the deployment pipeline validated in staging? Are observability, alerting, and logging in place? Is the rollback mechanism tested and ready? Are environment configurations correct?
3. **QA Engineer** — Are all acceptance criteria met? Are known defects triaged and dispositioned (fix before release, fix after release, accepted)? Is the regression suite green?
4. **Devil's Advocate** — Are readiness claims supported by evidence or by assumption? Is the rollback plan realistic under time pressure? What failure mode has not been considered?

If **Mobile App Developer** is activated:
5. **Mobile App Developer** — Is the app store submission prepared and validated? Are real-device tests completed for the target OS version matrix? Is the phased rollout configuration correct? Are crash reporting and analytics instrumented?

If **Security Engineer** is activated:
6. **Security Engineer** — Are there security-sensitive changes that require review? Have secrets, permissions, and data handling been verified for the new version?

### 3. Risk assessment
The **Release Manager** reviews all criteria evaluations and produces:
- A list of hard gates: criteria that must be met before release proceeds
- A list of conscious risk acceptances: known issues the team is choosing to ship with, with documented mitigations
- A list of open questions that must be answered before the go/no-go decision is made

### 4. Gap resolution
For any open gate or unresolved question, the relevant personas confirm the path to resolution: what must change, who owns it, and what is the minimum acceptable state to proceed. The Devil's Advocate validates that proposed mitigations are real, not rhetorical.

### 5. Readiness verdict
The **Release Manager** produces the final structured output and go/no-go verdict.

If the Devil's Advocate has unresolved concerns that were not addressed in the verdict, they may append a dissent.

## Interaction model overrides

- For routine, low-risk releases with a stable track record, collapse steps 2–4 into a single lightweight checklist review — the full model is for releases with elevated risk or novel changes
- When Mobile App Developer is activated, extend step 5 to include app store submission plan and phased rollout schedule
- For hotfixes under time pressure, the Tech Lead and DevOps/Platform Engineer may co-lead with an accelerated criteria review; the Devil's Advocate role is especially important in compressed timelines

## Notes

- The Release Manager makes the go/no-go call — but the criteria are defined by the team, not the Release Manager alone; a go/no-go is not a judgement call, it is a measurement against agreed criteria
- Conscious risk acceptances must be documented explicitly — "we know about this and are shipping anyway because [reason], with [mitigation]" is a valid position; "we didn't check" is not
- The rollback plan is a hard requirement — a release without a tested rollback mechanism is not ready regardless of other criteria
- For mobile releases: the app store review window means that a detected post-submission defect may take 24–72 hours to reach users even after a fix is ready; this changes the risk calculus for known issues at submission time
