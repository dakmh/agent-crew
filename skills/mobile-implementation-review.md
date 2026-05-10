# Skill: Mobile Implementation Review

## Command

`/mobile-implementation-review`

## Description

Reviews and plans the implementation of a mobile feature or release, assessing readiness across platform correctness, code quality, mobile CI/CD pipeline, test coverage, and security. Returns a structured implementation readiness assessment with a go/no-go verdict for beginning or continuing mobile implementation.

This is the mobile counterpart to the general implementation review. It extends the standard readiness model with mobile-specific gates: platform conformance, app store viability, device and OS version coverage, offline behaviour, and mobile-specific security requirements.

No external dependencies — context is provided by the user directly.

## Team

`agents/teams/mobile-development.md`

Uses the default Mobile Development interaction model unless overridden below.

## Interaction model overrides

None. Use the full Mobile Development interaction model.

## Context gathering

When `/mobile-implementation-review` is invoked:

1. If the user has included an implementation brief or feature specification in the same message, use it directly
2. If invoked alone, prompt the user:

   > "Please describe what you're building or reviewing. Include: the feature or change being implemented, which platforms are in scope (iOS, Android, or both), the target OS version range, any existing implementation or design decisions already made, and what you most want the team to focus on. There's no required format — write it however is natural."

3. Optionally ask: "Is this a new feature, a change to existing functionality, or a pre-submission review? Are there known risks or concerns you want the team to address specifically?"

Do not proceed until an implementation brief has been provided.

## Execution

Run the Mobile Development interaction model in order:

1. **[Mobile App Developer]** — Evaluate platform viability: is the implementation approach sound on each target platform, does it comply with app store policies, are OS version and device constraints correctly handled, and is the offline behaviour addressed? Identify any platform-specific risks or implementation decisions that need to be resolved before development proceeds.

2. **[Senior Developer]** — Assess implementability: is the approach buildable as described, what hidden complexity exists in the shared or platform-specific code, and are effort estimates credible? Identify specification gaps that would block a developer from starting.

3. **[UX Reviewer]** — Evaluate the mobile user experience: do the proposed flows conform to platform conventions on each target platform, are there accessibility requirements specific to mobile, and are interaction patterns native and intuitive?

4. **[DevOps / Platform Engineer]** — Assess CI/CD and distribution readiness: is the build pipeline configured for the target platforms, are code signing and provisioning in order, are distribution channels (TestFlight, Play Store tracks) set up, and is crash reporting and analytics instrumentation planned?

5. **[QA Engineer]** — Evaluate test strategy: what unit, integration, and UI tests are needed, what is the device and OS version test matrix, are real-device tests planned, and are acceptance criteria complete and testable?

6. **[Security Engineer]** — Review mobile security: are data stored on device encrypted appropriately, is API communication secured with certificate pinning or equivalent, are credentials handled correctly, and is the permission model appropriate?

7. **[Devil's Advocate]** — Stress-test the approach: are platform assumptions validated or assumed? Is the app store submission risk assessed? Are offline edge cases handled or deferred without acknowledgement? Is the device and OS matrix realistic given the user base?

8. **[Integration — Mobile App Developer]** — Reviews all responses, identifies conflicts, shared concerns, and gaps, and produces the readiness assessment.

Each persona must respond in character — voice, priorities, and concerns should reflect their definition in `agents/stable/`.

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

**Consciously accepted risks or debt:**
- [Item — rationale: ...]

**App store readiness:**
- [Known policy risks]
- [Required metadata or assets]
- [Required device testing before submission]

**Mobile CI/CD readiness:** [Pipeline status, signing, distribution channel]

**Overall mobile readiness verdict:** Ready / Ready with conditions / Not ready

[If DA has unresolved concerns: **Devil's Advocate dissent:** [...]]

---
