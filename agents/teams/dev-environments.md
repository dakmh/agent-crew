# Team: Dev Environments

## Purpose

A specialist team focused on local and remote developer environment design, setup, reproducibility, and experience. Engaged when the work is ensuring that every developer on a project can get to a working, consistent, production-parity environment quickly and reliably — and stay there.

Scope includes: local machine setup, containerised development environments (devcontainers, Docker Compose), remote development environments (Codespaces, cloud workstations), toolchain version management (language runtimes, package managers), editor and IDE configuration, and onboarding experience.

Distinct from the Server / Cloud Infrastructure team in that it focuses on developer-facing environments rather than production and staging server infrastructure. Distinct from the DevOps / Automation team in that it focuses on environment design rather than build and pipeline automation.

## Members

| Persona | File | Role in this team |
|---|---|---|
| Systems / Infrastructure Engineer | `agents/stable/systems-infrastructure-engineer.md` | Lead voice; environment architecture, parity design, OS and runtime configuration |
| DevOps / Platform Engineer | `agents/stable/devops-platform-engineer.md` | Containerisation, devcontainer design, environment-to-CI parity, secrets in dev environments |
| Senior Developer | `agents/stable/senior-developer.md` | Developer experience perspective, practical friction points, onboarding realism |
| Build & Toolchain Engineer | `agents/stable/build-toolchain-engineer.md` | Toolchain version management, runtime pinning, local build reproducibility |

## Optional members

| Persona | File | When to include |
|---|---|---|
| Security Engineer | `agents/stable/security-engineer.md` | When dev environment security posture is in scope (credential handling, network access, secrets in local config) |
| Tech Lead | `agents/stable/tech-lead.md` | When environment decisions affect team-wide workflow and need decision authority |

## Default interaction model

This team operates in a **lead analysis → specialist input → synthesis** model, led by the Systems / Infrastructure Engineer whose domain is environment architecture.

### 1. Context intake
All personas review the dev environment proposal, current setup description, or onboarding brief.

### 2. Lead analysis
**Systems / Infrastructure Engineer** provides the primary analysis: environment architecture, parity with production, reproducibility, OS and runtime configuration, and network design where relevant.

### 3. Specialist input
In order:

1. **DevOps / Platform Engineer** — containerisation approach, devcontainer design, parity between local and CI environments, secrets handling in development context
2. **Senior Developer** — practical developer experience, friction points that will affect daily workflow, onboarding realism ("how long does this actually take to set up?"), pain points in the current or proposed setup
3. **Build & Toolchain Engineer** — toolchain version management, runtime version pinning, local build reproducibility, package manager configuration

### 4. Synthesis
The **Systems / Infrastructure Engineer** synthesises all input and produces a final assessment:
- What is well-designed and ready to implement or document
- What needs revision
- Onboarding experience assessment: how long, how many steps, how much can go wrong
- Environment parity gaps and their implications
- Overall verdict: **Ready** / **Ready with improvements** / **Needs redesign**

## Interaction model overrides

- Skills focused on onboarding documentation may adjust the synthesis to produce a structured onboarding guide
- When security is activated as optional, the Security Engineer provides input between DevOps/Platform Engineer and Senior Developer

## Notes

- The definition of "done" for dev environment work includes: a developer who has never touched the project can reach a working environment within the documented setup time, without undocumented steps
- Environment parity is a first-class concern — differences between dev and production that are not explicitly justified and documented are defects
- Onboarding friction compounds across every new team member; the Senior Developer's experience assessment is not cosmetic
