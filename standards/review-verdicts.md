# Standard: Review Verdicts

The three-tier verdict scale used by every team that closes with a verdict. The tier vocabulary is fixed so verdicts are comparable across teams, reviews, and time; what the verdict applies to (a proposal, a feature specification, an implementation, a release) is named by the team.

## The scale

| Verdict | Meaning | Requirements |
|---|---|---|
| **Proceed** | Every hard gate is met and there are no unresolved conditions. The work moves to its next stage as-is. | State what was measured, not just the conclusion. |
| **Proceed with conditions** | Sound overall, but enumerated conditions must be resolved. | Every condition names what must change, who owns it, and whether it must be resolved *before* proceeding or can be *tracked* during. A conditions verdict without enumerated, owned conditions is not a valid verdict — it is a Do not proceed wearing a softer label. |
| **Do not proceed** | A hard gate is unmet, or rework is required at the level of framing or design rather than detail. | The verdict must name what would change it — the specific gate, question, or rework that stands between here and Proceed. |

## Rules

- A verdict is a **measurement against criteria** the team has made explicit, not a judgment call by the synthesiser. If the criteria were never stated, state them in the verdict.
- **Hard gates cannot be conditioned away.** A "must fix before shipping" risk disposition (see `standards/risk-assessment.md`), a P0 finding (see `standards/code-review-severity.md`), or a release without a tested rollback mechanism is a Do not proceed — never a condition.
- **Name the action, keep the tier words.** Teams phrase the positive tier for their context — "Proceed to implementation", "Proceed with adoption", "Proceed with release" — but the tier structure and the words *Proceed / Proceed with conditions / Do not proceed* stay fixed.
- **Dissent does not change the verdict.** An unresolved dissent is appended after the verdict per `skills/_conventions.md`, not averaged into it.
- Domain sub-assessments (e.g. a security posture rating, a standards conformance rating) may accompany the verdict as inputs to it; they do not replace it.
