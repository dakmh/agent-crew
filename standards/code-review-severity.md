# Standard: Code Review Severity

Classification standard for code review findings. Any team or skill that produces review findings references this standard rather than defining its own scale, so classifications stay consistent across commits, PRs, and review sessions.

Findings carry two labels: a **P-value** (P0–P4) as a quick-to-sort priority key, and a **verbal tier** (Blocker–Info) as the severity classification. The two map one-to-one; the P-value is shorthand for the tier, not an independent judgment.

## Core principle

Grade each finding independently against the absolute criteria below. Do not adjust severity based on what else appears in the same review. A Blocker is a Blocker in a clean PR and in a chaotic one.

## Security findings

For **known CVEs/CWEs**: look up the identifier in [NVD](https://nvd.nist.gov/) and report the CVSS base score and vector string directly. Do not assign a team label — the published score is the severity.

For **design-level security concerns** (no specific CVE number): identify the closest [CWE weakness category](https://cwe.mitre.org/), then score the specific instance using a CVSS calculator by evaluating:

- Attack Vector (Network / Adjacent / Local / Physical)
- Attack Complexity (Low / High)
- Privileges Required (None / Low / High)
- User Interaction (None / Required)
- Confidentiality / Integrity / Availability Impact (None / Low / High)

Report the resulting score and justify each vector component. CVSS base score interpretation: 0.0 = None, 0.1–3.9 = Low, 4.0–6.9 = Medium, 7.0–8.9 = High, 9.0–10.0 = Critical.

### P-value assignment for security findings

The CVSS score is the severity; the P-value is the sort key derived from it. Default mapping: 9.0–10.0 → P0, 7.0–8.9 → P1, 4.0–6.9 → P2, 0.1–3.9 → P3, observation with no score → P4. If actual exposure in context justifies moving a finding off the default (e.g. a High-scored issue on a code path that is unreachable in this deployment), state the adjustment and the reason alongside the score — never silently.

## Code quality severity scale

Each tier is defined by objective impact criteria, not by comparison to other findings in the review.

| P | Tier | Definition | Criteria | Decision question | Action |
|---|------|-----------|----------|-------------------|--------|
| **P0** | **Blocker** | Will likely cause production failure with near-certainty | Production crash or data loss under normal operation; race condition that triggers under load; failure for a whole class of inputs or users | "Is it a matter of *when*, not *if*, this breaks production?" | Must fix before merge |
| **P1** | **Critical** | Causes incorrect behavior under predictable conditions, or compounds risk across future changes | Wrong output or silent failure under realistic inputs; breaks a contract other components depend on; tech debt that directly impedes the next several changes in this area | "Will a developer hit this without doing anything unusual?" | Fix in this review cycle |
| **P2** | **Major** | Degrades maintainability or leaves a trap for future developers | Correct but hard to reason about in ways that slow future changes; pattern violation creating inconsistency risk; missing abstraction that forces duplication if the pattern is followed elsewhere | "Will the next developer in this area be slowed down or confused?" | Address soon; track if deferred |
| **P3** | **Minor** | Low-impact issue with negligible effect on correctness or maintainability | Naming clarity; formatting inconsistency; minor documentation gap; style deviation with no semantic consequence | "Would this matter if left for another year?" | Log; fix in future maintenance |
| **P4** | **Info** | Observation requiring no action | Noted but not recommending a change; a question about intent; a future consideration worth recording | — | No action required |
