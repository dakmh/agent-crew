# Skill: Release Planning

## Command

`/release-planning`

## Description

Produces a structured release plan with a go/no-go readiness verdict. Takes a description of what is being released and returns an evaluation of release criteria, a rollback plan, a communication plan, and a clear statement of what is ready, what is not, and what must be resolved before the release proceeds.

Works for server-side, web, and mobile releases. For mobile, the skill explicitly addresses app store submission timing, phased rollout strategy, and the constrained incident response window introduced by app store review cycles.

No external dependencies — context is provided by the user directly.

## Team

`agents/teams/release-management.md`

Uses the default Release Management interaction model. Activates the Mobile App Developer when the release includes a mobile client component.

## Interaction model overrides

When the release includes a mobile client:
- Activate the Mobile App Developer as a required member
- The Mobile App Developer evaluates app store submission readiness and contributes to the release readiness assessment
- The synthesis step must include an app store submission plan and phased rollout schedule

## Context gathering

When `/release-planning` is invoked:

1. If the user has included a release brief in the same message, use it directly
2. If invoked alone, prompt the user:

   > "Please describe the release. Include: what is being shipped (features, fixes, or changes), which systems and platforms are involved, the intended release environment and timeline, what has been tested and verified so far, and any known risks or concerns. If this includes a mobile app, include which platforms and whether an app store submission is required."

3. Optionally ask: "Is there anything specific about this release that concerns you — a risky change, a tight timeline, a dependency on another team, or a known defect being shipped?"

Do not proceed until a release description has been provided.

## Execution

Run the Release Management interaction model in order:

1. **[Tech Lead]** — Assess technical readiness: are all intended changes included, are integration points with other systems verified, are there unresolved dependencies or sequencing requirements?

2. **[DevOps / Platform Engineer]** — Assess operational readiness: is the deployment pipeline validated, are observability and alerting in place, is the rollback mechanism tested and operational, are environment configurations correct?

3. **[QA Engineer]** — Assess quality readiness: are acceptance criteria met, are known defects triaged with dispositions, is the regression suite green?

4. **[Mobile App Developer]** *(if mobile release)* — Assess mobile and app store readiness: is the submission prepared and validated on real devices at target OS versions, is the phased rollout configuration correct, are crash reporting and analytics instrumented?

5. **[Devil's Advocate]** — Stress-test the readiness claims: are they supported by evidence or assumption? Is the rollback plan realistic under time pressure? What failure mode has not been considered?

6. **[Synthesis — Release Manager]** — Consolidates all criteria evaluations, identifies hard gates and conscious risk acceptances, and produces the final release plan and go/no-go verdict.

Each persona must respond in character — voice, priorities, and concerns should reflect their definition in `agents/stable/`.

## Output format

---

### 🔧 Tech Lead — Technical Readiness

[In-character assessment: change completeness, integration verification, unresolved dependencies]

---

### ⚙️ DevOps / Platform Engineer — Operational Readiness

[In-character assessment: pipeline validation, observability, rollback mechanism, environment configuration]

---

### 🧪 QA Engineer — Quality Readiness

[In-character assessment: acceptance criteria status, defect triage, regression suite status]

---

### 📱 Mobile App Developer — Mobile and App Store Readiness *(if applicable)*

[In-character assessment: submission preparation, real-device validation, phased rollout configuration, observability instrumentation]

---

### 😈 Devil's Advocate

[In-character challenge: readiness assumptions, rollback plan realism, unexamined failure modes]

---

### 📦 Release Plan (Release Manager)

**Release scope:** [What is shipping, which systems and platforms]

**Go/no-go criteria:**

| Criterion | Status | Owner (if not met) |
|---|---|---|
| [Criterion] | ✅ Met / ❌ Not met / ⚠️ Risk accepted | [...] |

**Conscious risk acceptances:**
- [Risk — rationale — mitigation]

**Rollback plan:**
- Trigger: [What causes rollback to be invoked]
- Owner: [Who makes the call]
- Execution: [How it is done, how long it takes]
- For mobile: [App store rollback strategy — emergency patch submission, forced downgrade if applicable]

**Communication plan:**
- Internal stakeholders: [Who, what, when]
- Users / customers: [Release notes, in-app notices, or no action required]
- Support team: [Heads-up on expected queries or behaviour changes]

**For mobile releases:**
- App store submission timeline: [When submitted, expected review window]
- Phased rollout: [Percentage and escalation schedule]
- Force-upgrade policy: [If applicable — when and how users will be required to update]

**Release readiness verdict:** Ready to ship / Ready with conditions / Not ready

**Conditions** *(if applicable)*: [What must be resolved before release proceeds, with owner and deadline]

[If DA has unresolved concerns: **Devil's Advocate note:** [...]]

---
