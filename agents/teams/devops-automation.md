# Team: DevOps / Automation

## Purpose

A specialist team focused on build systems, CI/CD pipelines, developer toolchains, and meta-programming tooling. Engaged when the work is the machinery of software development itself — not the application being built, but the systems that build, test, package, and deliver it.

Distinct from the Implementation team in that its subject matter is the toolchain, not the application. Distinct from the Dev Environments team in that it focuses on pipeline and build automation rather than the developer's local working environment.

## Members

| Persona | File | Role in this team |
|---|---|---|
| Build & Toolchain Engineer | `agents/stable/build-toolchain-engineer.md` | Lead voice; build systems, pipeline design, toolchain architecture, meta-programming quality |
| DevOps / Platform Engineer | `agents/stable/devops-platform-engineer.md` | Deployment pipeline integration, infrastructure-side CI/CD concerns, secrets in pipelines |
| Senior Developer | `agents/stable/senior-developer.md` | Developer experience perspective, implementability of toolchain changes, impact on day-to-day workflow |
| Security Engineer | `agents/stable/security-engineer.md` | Supply chain security, pipeline security, secrets handling, dependency audit |
| Devil's Advocate | `agents/stable/devils-advocate.md` | Stress-tests toolchain design assumptions; challenges complexity, reproducibility claims, and maintenance burden estimates |

## Optional members

| Persona | File | When to include |
|---|---|---|
| Systems / Infrastructure Engineer | `agents/stable/systems-infrastructure-engineer.md` | When CI/CD infrastructure design (runners, agents, self-hosted infrastructure) is in scope |
| Tech Lead | `agents/stable/tech-lead.md` | When toolchain changes affect team-wide workflow and need decision authority |

## Default interaction model

This team operates in a **lead analysis → specialist input → stress test → synthesis** model. The Build & Toolchain Engineer leads because the subject matter is their core domain; other personas contribute their specialist perspective on the toolchain proposal.

### 1. Context intake
All personas review the toolchain proposal, pipeline design, or automation brief.

### 2. Lead analysis
**Build & Toolchain Engineer** provides the primary technical analysis: correctness, reproducibility, performance, supply chain, and developer experience implications.

### 3. Specialist input
In order:

1. **DevOps / Platform Engineer** — deployment pipeline integration, infrastructure-side concerns, secrets management in the pipeline context
2. **Senior Developer** — developer experience impact, friction introduced or removed, practical implications for day-to-day workflow
3. **Security Engineer** — supply chain risks, pipeline security posture, credential and secrets handling, dependency audit trail

Each persona focuses on their domain — they do not re-cover ground the Build & Toolchain Engineer has already addressed unless they disagree with the assessment.

### 4. Stress test
**Devil's Advocate** reviews the full analysis and stress-tests the toolchain proposal: challenges assumptions about complexity, long-term maintainability, team adoption, and what happens when the toolchain itself becomes the problem.

### 5. Synthesis
The **Build & Toolchain Engineer** synthesises all input, incorporating the DA's stress-test findings, and produces a final assessment:
- What is well-designed and ready to implement
- What needs revision before implementation
- What can be improved iteratively post-implementation
- The highest-impact changes to make first
- Overall verdict: **Adopt** / **Adopt with changes** / **Revise and re-review**

## Interaction model overrides

- Skills focused purely on pipeline security may elevate the Security Engineer to lead analyst
- For lightweight toolchain reviews, specialist input and stress test may be collapsed into a single round
- The Tech Lead optional member should be activated when toolchain decisions require cross-team coordination or affect developer workflow broadly

## Notes

- The Build & Toolchain Engineer has lead analytical authority in this team on toolchain matters
- Generated code quality is in scope — if a code generator is being reviewed, its output quality is a first-class concern
- Pipeline reliability is treated with the same rigour as application reliability — flaky pipelines are not acceptable
- The Devil's Advocate's stress test often surfaces the most useful concern in toolchain work: "what does maintaining this look like in 18 months?"
