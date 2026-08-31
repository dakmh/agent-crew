# 2026-08-30 overnight run — source record and improvement plan

The compiled record of one unattended multi-hour agent run driven by agent-crew, and the plan that came out of it. Assembled 2026-08-30 from documents written in the `photo-culling` project and in this repo; the run itself was project work, but everything collected here is about *how the run was bounded, triggered, and reviewed*, which is agent-crew's concern rather than that project's.

| File | What it is | Origin |
|---|---|---|
| [01-setup-session-record.md](01-setup-session-record.md) | Factual record of the session that designed the run and wrote its prompt — plugin registration state, the discovery that no skill reaches the Implementation team, the substrate-threshold reasoning. | Written in this repo as `docs/reviews/2026-08-30-overnight-run-leadin.md`; moved. |
| [02-pre-run-review-session-record.md](02-pre-run-review-session-record.md) | Factual record of the session immediately before launch — a manual `/agent-crew:security-review` on `f9e8d6d`, the sandbox-guard remediation, and the environment mechanism that the run depended on. | `photo-culling/OVERNIGHT_LEADIN.md`; moved (was untracked there). |
| [03-postmortem.md](03-postmortem.md) | The postmortem: what happened, root causes, what worked, guidance for long runs, and three library observations with the measured evidence behind them. The primary input to the plan. | `photo-culling/LONG_AGENTIC_RUNS.md`; moved (`git rm` in that repo, uncommitted). |
| [04-run-log-copy.md](04-run-log-copy.md) | The run's own log, including the three `## agent-crew dogfooding notes` sections — substrate branch, convergence/divergence per run, and the library observations as first recorded. | Copy of `photo-culling/OVERNIGHT_LOG.md`, which stays there as that project's record. |
| [05-run-prompt-as-launched.md](05-run-prompt-as-launched.md) | The brief the run was launched with, preconditions and all. The raw material for the prompt template in the plan. | Copy of `photo-culling/OVERNIGHT_PROMPT.md`, which stays there (untracked). |
| [06-improvement-plan.md](06-improvement-plan.md) | **The deliverable.** Directives, tooling, helper scripts, prompt templates, and sequencing. | Written 2026-08-30. |

Not collected here, and referenced rather than copied: `photo-culling/WORK_PLAN.md`, the work plan the run executed against. It is project content — the plan cites it only as an example of the shape a long run needs its scope written in.

`photo-culling/OVERNIGHT_LOG.md` and `OVERNIGHT_PROMPT.md` remain in that project because the run was that project's work and its log is that project's record. `03-postmortem.md` and `02-pre-run-review-session-record.md` do not, because both say so themselves — the postmortem states its findings are not specific to that project, and the pre-run record was written for handoff here.
