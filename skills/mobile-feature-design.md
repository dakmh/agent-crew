# Skill: Mobile Feature Design

## Command

`/mobile-feature-design`

## Description

Shapes a feature into a buildable specification for mobile applications. Extends the standard feature design process with mobile-specific concerns: platform targeting, app store policy implications, offline behaviour, device and OS version constraints, and the distribution model differences between mobile and server-side software.

Takes a feature request or user story and returns an agreed scope, recommended technical approach (including platform-specific considerations), testable acceptance criteria, and a readiness verdict.

Assumes the *why* is established — this team focuses on the *what* and *how* at a level of fidelity sufficient for confident mobile implementation.

No external dependencies — context is provided by the user directly.

## Team

`agents/teams/feature-design.md`

This skill uses the Feature Design team with the Mobile App Developer and UX Reviewer activated as required members. The interaction model is extended with a mobile platform analysis step.

## Interaction model overrides

The standard Feature Design interaction model is extended as follows:

- After the System Architect's technical analysis, the **Mobile App Developer** contributes a platform analysis step before the Senior Developer's implementability check
- The **UX Reviewer** contributes after the Senior Developer's implementability check, focusing on mobile user flows and platform-native interaction patterns
- The synthesis step must address platform-specific scope explicitly (which platforms, which OS versions, what offline behaviour is required)

## Context gathering

When `/mobile-feature-design` is invoked:

1. If the user has included a feature description in the same message, use it directly
2. If invoked alone, prompt the user:

   > "Please describe the feature you'd like designed for mobile. Include: what user problem it solves, which platforms it targets (iOS, Android, or both), any platform-specific requirements or constraints you know about, what technical approach (if any) you're already considering, and anything already decided or ruled out."

3. Optionally ask: "Are there specific mobile concerns you want the team to focus on — offline behaviour, app store submission, a particular OS version, performance, or something else?"

Do not proceed until a feature description and target platform(s) have been provided.

## Execution

Run the extended Feature Design interaction model in order:

1. **[Project Owner]** — Restate the user problem and goal the feature serves, the success criteria, the known constraints, and the scope boundary as currently understood. Note any mobile-specific user expectations (offline use, push notifications, background behaviour).

2. **[System Architect]** — Evaluate technical approach options: what exists, what the structural implications of each are, what the tradeoffs are, and which approach is recommended. Flag any decisions that would be expensive to reverse, particularly those involving shared backend or API design that affects multiple clients.

3. **[Mobile App Developer]** — Analyse the feature from a mobile platform perspective: which platforms and OS versions are in scope, what app store policy implications exist, what offline and network-degraded behaviour is required, what platform-specific APIs or capabilities are needed, and what mobile CI/CD or distribution considerations arise from this feature.

4. **[Senior Developer]** — Assess implementability: hidden complexity across shared and platform-specific code, unresolved dependencies, effort realism, and what needs to be specified more precisely before a developer can start.

5. **[UX Reviewer]** — Evaluate the mobile user experience: do the proposed flows conform to platform conventions, are there accessibility considerations specific to mobile, and does the interaction model feel native to the platforms in scope?

6. **[Devil's Advocate]** — Challenge the feature design: is the problem framing correct? Are platform assumptions validated? Is the scope appropriate for a mobile context? Are offline and edge-connectivity scenarios accounted for or consciously deferred?

7. **[Cross-examination]** — Project Owner responds to scope and framing challenges; System Architect responds to implementability and platform concerns; Mobile App Developer and Senior Developer address any conflicts between platform requirements and implementation approach; UX Reviewer and Mobile App Developer address any platform-convention tensions.

8. **[Synthesis — Project Owner + System Architect + Mobile App Developer]** — Jointly produce the final feature specification.

Each persona must respond in character — voice, priorities, and concerns should reflect their definition in `agents/stable/`.

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
