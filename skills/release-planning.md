# Skill: Release Planning

## Command

`/release-planning`

## Description

Produces a structured release plan with a go/no-go readiness verdict. Takes a description of what is being released and returns an evaluation of release criteria, a rollback plan, a communication plan, and a clear statement of what is ready, what is not, and what must be resolved before the release proceeds.

Works for server-side, web, and mobile releases. For mobile, the skill explicitly addresses app store submission timing, phased rollout strategy, and the constrained incident response window introduced by app store review cycles.

## Team

`agents/teams/release-management.md`

Activates the **Mobile App Developer** as a required member when the release includes a mobile client component requiring app store submission. (Other optional members — Security Engineer, Product Manager — activate per the team file's "When to include" guidance.)

## Interaction model

Follow the team's default interaction model in `agents/teams/release-management.md`. The shared protocol in `skills/_conventions.md` applies.

Overrides:
- For a mobile release, the Mobile App Developer evaluates app store submission readiness in the criteria-evaluation step, and the Release Manager's synthesis must include an app store submission plan and phased rollout schedule.

## Context gathering

Per `skills/_conventions.md`. Required context: a description of the release being planned.

> "Please describe the release. Include: what is being shipped (features, fixes, or changes), which systems and platforms are involved, the intended release environment and timeline, what has been tested and verified so far, and any known risks or concerns. If this includes a mobile app, include which platforms and whether an app store submission is required."

Optional focus question: "Is there anything specific about this release that concerns you — a risky change, a tight timeline, a dependency on another team, or a known defect being shipped?"

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

## Example invocation

```
/release-planning

Planning the 3.4 release of our web app plus the matching iOS and Android clients. Ships a
new checkout flow (server + all clients) and a fix for a data-export bug. Web deploys to
production behind a feature flag; mobile needs an app store submission. QA has signed off
on web; mobile real-device testing is still in progress. Target is end of next week, which
is tight given the app review window.
```
