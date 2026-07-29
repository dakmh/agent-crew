# Standard: Risk Assessment

How risks are rated, who rates them, what may be done with them, and what a valid risk acceptance looks like. Applies wherever teams surface risk — design, planning, implementation, infrastructure, and release contexts.

For findings produced by code review, classification follows `standards/code-review-severity.md`; this standard governs risk everywhere else, and its disposition scale is the vocabulary teams use when deciding what to *do* about a risk of any origin.

## Rating: likelihood × impact

Every risk is rated on two axes, each **Low / Medium / High**, stated together and grounded in a concrete scenario — who or what triggers it, and what happens. "An attacker could theoretically..." is not a rating; "an unauthenticated user can reach this endpoint, exfiltrate the data, and we have no audit log — high likelihood, high impact" is.

## Ownership: score vs. flag

- Any persona may **flag** a risk in their domain — naming the risk is everyone's job.
- **Scoring** (the likelihood/impact rating) belongs to the persona who owns risk assessment on the team — the Security Engineer for security risks. Specialists flag, they don't score; the scorer adds the rating and any threat-model implications the flag missed.
- One risk, one rating — if a risk has already been enumerated, add to its assessment rather than re-listing it.

## Disposition scale

Every rated risk gets exactly one disposition:

| Disposition | Meaning | Constraint |
|---|---|---|
| **Must fix before shipping** | A hard gate. | Cannot be accepted, conditioned, or monitored away — non-negotiable blocker. Forces a Do not proceed verdict (`standards/review-verdicts.md`) until resolved. |
| **Should fix soon** | Does not block the current increment. | Only valid if tracked and scheduled with an owner — untracked "soon" is a disguised acceptance. |
| **Accept and document** | Conscious acceptance. | Requires a complete acceptance record (below). |
| **Monitor** | Low likelihood or impact today; may change. | Requires a named signal: what is being watched, and the threshold that reopens the risk. "We'll monitor it" without a signal is not a disposition. |

## Risk acceptance record

An acceptance is only valid as a complete record:

- **Risk** — the concrete scenario, with its likelihood/impact rating
- **Rationale** — why shipping with it is acceptable
- **Mitigation** — what reduces likelihood or impact in the meantime
- **Owner** — who is accountable for it
- **Review trigger** — what event or date revisits the acceptance

"We know about this and are shipping anyway because X, with mitigation Y" is a valid position. "We didn't check" is not an acceptance — unexamined risk is not accepted risk, and may not be recorded as one.
