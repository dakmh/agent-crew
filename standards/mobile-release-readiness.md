# Standard: Mobile Release Readiness

The submission readiness checklist and review-window risk calculus for releases that ship through an app store. Cited by mobile and release teams and skills instead of restating the checklist inline.

## Why mobile releases are different

App store review inserts a **24–72 hour window** between a fix being ready and the fix reaching users — even for a defect discovered minutes after submission. Expedited review is an exception process granted at the store's discretion, not a plan. This latency changes the risk calculus for every known defect at submission time: a defect that would be acceptable in a web release (fixable within the hour) may be a blocker in a submitted binary.

## Submission readiness checklist

- **Store compliance** — app store policy risks assessed for the changes being shipped; metadata, assets, and privacy declarations (privacy manifest / data safety form) prepared and current
- **Signing & distribution** — certificates and provisioning valid; correct distribution channel configured (TestFlight / Play tracks); CI/CD produces signed, reproducible release builds
- **Device & OS coverage** — real-device testing completed across the supported OS version range and a representative device matrix; simulator-only validation is not completion
- **Offline & degraded network** — behaviour under no connectivity and poor connectivity explicitly verified, not deferred
- **Observability** — crash reporting and analytics instrumented and verified in the release build configuration
- **Phased rollout** — percentage schedule defined with escalation criteria and halt criteria
- **Recovery** — a rollback strategy that works within store constraints: server-side flags to disable shipped features, an emergency patch submission path, and a force-upgrade policy if one applies

## Known defects at submission

Every risk acceptance in a mobile release (per `standards/risk-assessment.md`) must account for the review-window latency: the mitigation must be one that works *without* shipping a new binary (server-side flag, config change, support communication), or the acceptance must explicitly absorb the 24–72 hour exposure. An acceptance whose only mitigation is "we'll patch it quickly" is not valid for a store-distributed release.
