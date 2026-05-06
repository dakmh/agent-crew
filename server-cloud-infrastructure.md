# Team: Server / Cloud Infrastructure

## Purpose

A specialist team focused on server topology, cloud architecture, multi-environment infrastructure design, network architecture, reliability engineering, and infrastructure governance. Engaged when the work involves designing, reviewing, or evolving the infrastructure that runs software in non-development environments — staging, production, and everything in between.

Scope includes: cloud architecture (IaaS, PaaS, serverless), network design and segmentation, multi-environment topology (staging, pre-production, production), disaster recovery and failover design, infrastructure as code, resource governance and cost architecture, and infrastructure security posture.

Distinct from the Dev Environments team in that it focuses on server and cloud infrastructure rather than developer-facing environments. Distinct from the DevOps / Automation team in that it focuses on infrastructure design rather than build and pipeline automation.

## Members

| Persona | File | Role in this team |
|---|---|---|
| Systems / Infrastructure Engineer | `agents/stable/systems-infrastructure-engineer.md` | Lead voice; infrastructure architecture, network design, environment topology, reliability |
| DevOps / Platform Engineer | `agents/stable/devops-platform-engineer.md` | Deployment pipeline integration, observability infrastructure, operational readiness |
| Security Engineer | `agents/stable/security-engineer.md` | Infrastructure security posture, network security, IAM, compliance at the platform layer |

## Optional members

| Persona | File | When to include |
|---|---|---|
| Domain Expert | `agents/stable/domain-expert.md` | When domain-specific compliance or infrastructure requirements apply (e.g. healthcare data residency, financial services availability requirements) |
| Build & Toolchain Engineer | `agents/stable/build-toolchain-engineer.md` | When infrastructure-as-code toolchain design is a primary concern |
| Tech Lead | `agents/stable/tech-lead.md` | When infrastructure decisions have significant application architecture implications |

## Default interaction model

This team operates in a **lead analysis → specialist input → cross-examination → synthesis** model. Infrastructure decisions at this level have significant security and reliability implications, warranting the more rigorous cross-examination step.

### 1. Context intake
All personas review the infrastructure proposal, architecture diagram, or design brief.

### 2. Lead analysis
**Systems / Infrastructure Engineer** provides the primary analysis: infrastructure architecture, network topology, environment design, reliability posture, infrastructure-as-code coverage, and resource governance.

### 3. Specialist input
In order:

1. **DevOps / Platform Engineer** — deployment pipeline integration with the proposed infrastructure, observability infrastructure design, operational runbook implications, incident response and recovery procedures
2. **Security Engineer** — infrastructure threat model, network security posture, IAM design, secrets management at the platform layer, compliance implications, and security controls at each infrastructure layer

### 4. Cross-examination
The Security Engineer and Systems / Infrastructure Engineer address each other's key concerns directly. Infrastructure design and security posture are deeply interdependent — conflicts or tensions between them must be resolved explicitly, not left as parallel concerns.

The DevOps / Platform Engineer addresses any operational concerns raised by the security or infrastructure analysis.

### 5. Synthesis
The **Systems / Infrastructure Engineer** produces the final assessment:
- Infrastructure design: what is sound, what needs revision
- Security posture: gaps and required mitigations (drawing on Security Engineer input)
- Reliability assessment: single points of failure, recovery design, observability coverage
- Infrastructure-as-code coverage: what is defined in code, what is manual
- Cost and resource governance assessment
- Overall verdict: **Production-ready** / **Ready with conditions** / **Not ready — redesign required**

## Interaction model overrides

- Skills focused specifically on infrastructure security review may elevate the Security Engineer to co-lead alongside the Systems / Infrastructure Engineer
- When Domain Expert is activated, they provide input after the Security Engineer, focusing on domain-specific compliance and infrastructure requirements
- For lightweight infrastructure reviews (e.g. adding a single service to an established architecture), the cross-examination step may be skipped

## Notes

- Security Engineer's "must fix before shipping" infrastructure items are non-negotiable blockers — no production deployment proceeds with open critical infrastructure security findings
- Disaster recovery is not optional — every production infrastructure design must include a defined RTO, RPO, and the infrastructure to meet them
- Infrastructure-as-code is the expected standard — manual infrastructure must be explicitly justified and carries a documentation and reproducibility debt that must be tracked
- Cost governance is a first-class concern, not an afterthought — ungoverned cloud resource growth is a reliability and financial risk
