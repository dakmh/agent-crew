# Skill: Mobile Implementation Review

## Command

`/mobile-implementation-review`

## Description

Reviews and plans the implementation of a mobile feature or release, assessing readiness across platform correctness, code quality, mobile CI/CD pipeline, test coverage, and security. Returns a structured implementation readiness assessment with a go/no-go verdict for beginning or continuing mobile implementation.

This is the mobile counterpart to the general implementation review. It extends the standard readiness model with mobile-specific gates: platform conformance, app store viability, device and OS version coverage, offline behaviour, and mobile-specific security requirements.

## Team

`agents/teams/mobile-development.md`

## Interaction model

Follow the team's default interaction model in `agents/teams/mobile-development.md`. The shared protocol in `skills/_conventions.md` applies.

No overrides.

## Context gathering

Per `skills/_conventions.md`. Required context: an implementation brief or feature specification for the mobile work being reviewed.

> "Please describe what you're building or reviewing. Include: the feature or change being implemented, which platforms are in scope (iOS, Android, or both), the target OS version range, any existing implementation or design decisions already made, and what you most want the team to focus on. There's no required format — write it however is natural."

Optional focus question: "Is this a new feature, a change to existing functionality, or a pre-submission review? Are there known risks or concerns you want the team to address specifically?"

## Output format

---

### 📱 Mobile App Developer — Platform Analysis

[In-character analysis: platform viability per target, app store compliance, OS and device constraints, offline handling, platform-specific risks]

---

### 👷 Senior Developer — Implementability

[In-character assessment: buildability, hidden complexity, shared vs platform-specific code, effort realism, specification gaps]

---

### 🎨 UX Reviewer — Mobile Experience

[In-character evaluation: platform convention conformance, accessibility, interaction patterns]

---

### ⚙️ DevOps / Platform Engineer — CI/CD and Distribution

[In-character assessment: build pipeline, code signing, distribution channels, observability, crash reporting]

---

### 🧪 QA Engineer — Test Strategy

[In-character assessment: test coverage, device and OS matrix, real-device requirements, acceptance criteria completeness]

---

### 🔒 Security Engineer — Mobile Security

[In-character assessment: on-device storage, transport security, credential handling, permission model]

---

### 😈 Devil's Advocate

[In-character challenge: platform assumptions, app store risk, offline edge cases, device matrix realism]

---

### ✅ Mobile Implementation Readiness Assessment (Mobile App Developer)

**Platforms in scope:** [iOS / Android, minimum OS versions, device targets]

**What is clear and ready to implement:**
- [Item]

**Must be resolved before implementation starts:**
- [Item — owner: ...]

**Can be resolved during implementation:**
- [Item — owner: ...]

**Consciously accepted risks or debt** (per `standards/risk-assessment.md`)**:**
- [Item — rationale — mitigation — owner]

**App store readiness** (per `standards/mobile-release-readiness.md`)**:**
- [Known policy risks]
- [Required metadata or assets]
- [Required device testing before submission]

**Mobile CI/CD readiness:** [Pipeline status, signing, distribution channel]

**Overall mobile readiness verdict** (per `standards/review-verdicts.md`)**:** Proceed / Proceed with conditions / Do not proceed

[If DA has unresolved concerns: **Devil's Advocate dissent:** [...]]

---

## Example invocation

```
/mobile-implementation-review

Reviewing our new in-app document scanner before we start building. iOS and Android, min
iOS 16 / Android 12. Uses the camera plus on-device OCR; scans are uploaded to our API and
also cached locally so users can re-view them offline. Team has a working prototype on iOS
only. We want a readiness check across platform correctness, CI/CD, test coverage, and
security before committing to the Android build and a submission timeline.
```
