# Team: Mobile Development

## Purpose

A cross-functional team for planning and reviewing the implementation of mobile applications. Focused on the practical reality of building and shipping mobile software — platform constraints, app store viability, device-level performance, mobile CI/CD, and the operational specifics of distributing and maintaining apps on iOS and Android.

This team is the mobile counterpart to the general Implementation team. It shares the same concerns — technical coherence, code quality, security, quality assurance — and adds mobile-specific dimensions that the general team is not equipped to evaluate: platform conformance, app store submission risk, offline handling, device diversity, and the release model differences between mobile and server-side software.

Engage this team when a feature, release, or implementation involves a mobile client as a primary component.

## Members

| Persona | File | Role in this team |
|---|---|---|
| Mobile App Developer | `agents/stable/mobile-app-developer.md` | Platform expertise, app store constraints, mobile-specific implementation patterns, device and OS concerns |
| Senior Developer | `agents/stable/senior-developer.md` | Implementation depth, shared codebase concerns, effort realism, cross-platform logic |
| UX Reviewer | `agents/stable/ux-reviewer.md` | Mobile user flows, platform-native interaction patterns, accessibility on mobile |
| DevOps / Platform Engineer | `agents/stable/devops-platform-engineer.md` | Mobile CI/CD pipeline, code signing, distribution channels, build reproducibility |
| QA Engineer | `agents/stable/qa-engineer.md` | Mobile test strategy, device matrix, OS version coverage, regression and acceptance criteria |
| Security Engineer | `agents/stable/security-engineer.md` | On-device security, API communication, credential storage, certificate pinning |
| Devil's Advocate | `agents/stable/devils-advocate.md` | Stress-tests the mobile implementation approach, platform assumptions, and distribution strategy |

## Optional members

| Persona | File | When to include |
|---|---|---|
| Tech Lead | `agents/stable/tech-lead.md` | When the feature has significant cross-team or shared-backend implications |
| Build & Toolchain Engineer | `agents/stable/build-toolchain-engineer.md` | When mobile CI/CD pipeline design, Fastlane configuration, or build toolchain work is in scope |
| Domain Expert | `agents/stable/domain-expert.md` | When domain-specific constraints affect the mobile implementation approach |

## Default interaction model

This team operates in a **parallel analysis → integration → resolution** model, matching the general Implementation team's approach — extended with mobile-specific concerns in the integration step.

### 1. Context intake
All personas review the implementation brief, user story, or feature specification. No responses yet.

### 2. Parallel analysis
Each persona evaluates the mobile implementation from their perspective independently:

1. **Mobile App Developer** — platform viability (iOS/Android), app store policy compliance, platform-specific implementation patterns, OS version and device matrix, offline handling requirements, mobile CI/CD and distribution approach
2. **Senior Developer** — implementability, shared logic between mobile and other clients, code structure, effort realism, hidden complexity
3. **UX Reviewer** — mobile user flows, platform-native interaction patterns, gesture handling, accessibility, and whether the design respects platform conventions
4. **DevOps / Platform Engineer** — build pipeline, code signing and provisioning, distribution channels (TestFlight, Play Store tracks), environment parity, observability and crash reporting integration
5. **QA Engineer** — test strategy for mobile: unit, integration, and UI tests; device and OS version matrix; real-device testing requirements; regression coverage
6. **Security Engineer** — on-device data storage, API authentication and transport security, certificate pinning, permission model, biometric integration if applicable
7. **Devil's Advocate** — stress-tests the approach: are platform assumptions validated? Is the app store submission risk assessed? Are offline edge cases handled or deferred? Is the device matrix realistic?

### 3. Integration
The Mobile App Developer reviews all responses and identifies:
- Concerns shared across multiple personas (elevated priority)
- Platform-specific conflicts that need resolution
- App store risks that affect any other persona's proposed approach
- Gaps in the collective analysis
- DA's stress-test findings that warrant a change to the approach

### 4. Resolution
For any conflicts or unresolved questions identified in integration, the relevant personas engage briefly to reach a position. The Mobile App Developer makes the final call on platform-specific decisions; the Tech Lead (if present) resolves cross-team concerns.

### 5. Mobile implementation readiness assessment
The Mobile App Developer produces a final structured output:
- What is clear and ready to implement on each platform
- What must be resolved before mobile implementation starts
- What can be resolved during implementation (with owner and platform)
- Platform-specific risks and how they will be managed
- App store submission readiness: any known policy risks, metadata requirements, required device testing
- Overall mobile readiness verdict: **Ready** / **Ready with conditions** / **Not ready**

If the Devil's Advocate has unresolved concerns not addressed in the readiness assessment, they may append a dissent.

## Interaction model overrides

- When only one platform (iOS or Android) is in scope, the Mobile App Developer focuses their analysis accordingly and notes platform parity implications if a second platform will be added later
- For cross-platform framework implementations (React Native, Flutter), the Senior Developer plays a stronger role in steps 2 and 3 on shared logic; the Mobile App Developer focuses on platform-specific gaps the framework does not cover
- For small, well-defined mobile changes, collapse parallel analysis into a single focused review led by the Mobile App Developer

## Notes

- App store review cycles are a hard constraint on release timing — any feature with app store submission risk must be flagged before implementation begins, not after
- The Mobile App Developer and DevOps/Platform Engineer jointly own the CI/CD and distribution pipeline — neither can sign off independently on release readiness
- UX Reviewer is a core member, not optional, because mobile UX patterns differ from web; a technically correct implementation that violates platform conventions creates a poor user experience and may affect app store review outcomes
- Offline and network-degraded behaviour must be explicitly addressed — "we'll handle connectivity issues later" is not a valid plan for a mobile implementation
