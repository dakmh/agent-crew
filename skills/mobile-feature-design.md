# Skill: Mobile Feature Design

## Command

`/mobile-feature-design`

## Description

Shapes a feature into a buildable specification for mobile applications. Extends the standard feature design process with mobile-specific concerns: platform targeting, app store policy implications, offline behaviour, device and OS version constraints, and the distribution model differences between mobile and server-side software.

Takes a feature request or user story and returns an agreed scope, recommended technical approach (including platform-specific considerations), testable acceptance criteria, and a readiness verdict.

Assumes the *why* is established — this team focuses on the *what* and *how* at a level of fidelity sufficient for confident mobile implementation.

## Team

`agents/teams/feature-design.md`

Activates the **Mobile App Developer** and **UX Reviewer** as required members (not optional) for every run of this skill.

## Interaction model

Follow the team's default interaction model in `agents/teams/feature-design.md`. The shared protocol in `skills/_conventions.md` applies.

Overrides:
- Add a **Mobile App Developer** platform-analysis step after the System Architect's technical analysis and before the Senior Developer's implementability check — target platforms and OS versions, app store policy implications, offline and network-degraded behaviour, platform-specific APIs, and mobile CI/CD or distribution considerations.
- The **UX Reviewer** contributes after the Senior Developer's implementability check (before the stress test), focusing on mobile user flows and platform-native interaction patterns.
- Extend the cross-examination with two mobile pairings: Mobile App Developer + Senior Developer on conflicts between platform requirements and implementation approach; UX Reviewer + Mobile App Developer on platform-convention tensions.
- Synthesis is a trio — **Project Owner + System Architect + Mobile App Developer** — and must address platform-specific scope explicitly (which platforms, which OS versions, what offline behaviour is required).

## Context gathering

Per `skills/_conventions.md`. Required context: a feature description and the target platform(s).

> "Please describe the feature you'd like designed for mobile. Include: what user problem it solves, which platforms it targets (iOS, Android, or both), any platform-specific requirements or constraints you know about, what technical approach (if any) you're already considering, and anything already decided or ruled out."

Optional focus question: "Are there specific mobile concerns you want the team to focus on — offline behaviour, app store submission, a particular OS version, performance, or something else?"

## Output format

---

### 🎯 Project Owner — Problem Framing

[In-character framing: user problem, success criteria, constraints, mobile-specific user expectations, scope boundary]

---

### 🏗️ System Architect — Technical Analysis

[In-character analysis: approach options, structural implications, tradeoffs, recommendation, API and backend considerations]

---

### 📱 Mobile App Developer — Platform Analysis

[In-character analysis: target platforms and OS versions, app store policy implications, offline requirements, platform-specific APIs, CI/CD and distribution considerations]

---

### 👷 Senior Developer — Implementability Check

[In-character assessment: shared vs platform-specific code complexity, dependencies, effort realism, specification gaps]

---

### 🎨 UX Reviewer — Mobile Experience

[In-character evaluation: platform convention conformance, accessibility on mobile, interaction model, native feel]

---

### 😈 Devil's Advocate

[In-character challenge: platform assumptions, offline edge cases, scope fit for mobile, what might be wrong]

---

### 🔄 Cross-Examination

**Project Owner on DA's framing challenges:** [Response]

**System Architect on implementability and platform concerns:** [Response]

**Mobile App Developer + Senior Developer on platform-implementation conflicts:** [Response]

**UX Reviewer + Mobile App Developer on platform convention tensions:** [Response]

---

### ✅ Mobile Feature Specification (Project Owner + System Architect + Mobile App Developer)

**Problem statement and user goal:** [Confirmed or revised]

**Target platforms:** [iOS / Android / both, with minimum OS version]

**Agreed scope:** [What's in, including platform-specific inclusions]

**Out of scope:** [Explicitly excluded, including any deferred platform parity]

**Recommended technical approach:** [With platform-specific notes]

**Offline and connectivity behaviour:** [Required behaviour under degraded or absent network]

**Acceptance criteria:**
- The user can [...]
- On iOS: [any platform-specific criteria]
- On Android: [any platform-specific criteria]

**App store considerations:** [Policy risks, metadata requirements, required device testing before submission]

**Open questions:** [Must be resolved before implementation starts]

**Known risks:** [And how they will be managed]

**Readiness verdict:** Ready for implementation / Ready with conditions / Needs further design

[If DA has unresolved concerns: **Devil's Advocate note:** [...]]

---

## Example invocation

```
/mobile-feature-design

We want to add mobile boarding passes to our travel app on iOS and Android. Users should
be able to pull up their pass at the gate even with no signal, and it should update if the
gate or time changes while they're online. iOS should support Apple Wallet. Minimum
targets are iOS 16 and Android 11. Backend already exposes a bookings API; nothing decided
on local storage or push-update strategy.
```
