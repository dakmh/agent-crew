# agent-crew Optimization Plan

**Status:** Phase 1 (deduplication) complete; Phases 2–3 pending
**Scope:** Full-repo analysis of personas, teams, modifiers, and skills; plus a model-routing
layer for Opus-default execution with selective Fable escalation.

---

## 1. Executive summary

The library is coherent and well-written at the level of individual files. Its problems are
almost all *between* files:

1. **Redundancy** — every skill restates its team's interaction model nearly verbatim, three
   separate indexes (CLAUDE.md, README.md, and the files themselves) must be kept in sync, and
   all nine skills repeat the same context-gathering and "respond in character" boilerplate.
   Drift has already started (see §2.1).
2. **Holes** — 4 of 12 teams are unreachable by any skill (including the flagship
   Implementation team), 6 of 24 personas belong to no team and no skill, the modifier
   targeting syntax (`[architect:cautious]`) references persona aliases that are defined
   nowhere, and there is no cheap single-persona invocation path.
3. **Inefficiency** — CLAUDE.md injects ~12 KB of index tables into *every* session whether or
   not a skill is used; a full skill run loads 25–40 KB of definitions before any analysis
   begins; and all interaction models are strictly sequential even where the team file itself
   describes the analyses as independent ("parallel review", "parallel analysis").
4. **No model awareness** — nothing in the system says which model should execute what. §5
   designs a routing layer: Opus as the default executor for all persona work, Fable escalation
   reserved for a small set of judgment-critical steps, with mandatory Opus fallback when Fable
   is unavailable or not permitted.

Recommended sequence: deduplicate first (Phase 1), fill the holes second (Phase 2), then add
the execution/model-routing layer (Phase 3). Phases 1–2 make Phase 3 dramatically cheaper
because routing rules attach to *steps in team files*, and Phase 1 makes team files the single
authority on steps.

---

## 2. Findings — redundancy

### 2.1 Skills restate team interaction models (highest-value fix)

All nine skills contain an `## Execution` section that reproduces the team file's interaction
model step by step, usually after declaring `Interaction model overrides: None`. The team file
and the skill file are two copies of the same procedure, and they are already diverging:

- `skills/release-planning.md` runs the Mobile App Developer *before* the Devil's Advocate;
  `agents/teams/release-management.md` lists Mobile App Developer *after* the DA (step 5 vs
  step 4). The skill also silently drops the team's **Gap resolution** step (team step 4).
- `skills/mobile-implementation-review.md` collapses the team's Integration → Resolution →
  Readiness Assessment (steps 3–5) into a single "Integration" step, dropping the explicit
  conflict-resolution round.
- `skills/security-review.md` restates the team's parallel-review steps but the team file also
  defines the P0–P3 tier table and output format — the one case where the split is done right
  (skill defers to team for format). Every other skill embeds its own output format.

**Fix:** make the team file the single source of truth for the interaction model. A skill's
`Execution` section shrinks to: (a) "run the team's default interaction model", (b) genuine
overrides only (mobile-feature-design legitimately has them), and (c) *task-specific emphasis*
per step where it adds information the team file can't have (e.g. release-planning's
app-store-specific step notes). Reconcile the two existing divergences explicitly while doing
this — decide which order/steps are correct and encode them once.

### 2.2 Triple index maintenance

Adding one persona today requires edits in three places: the persona file, the CLAUDE.md table,
and the README table (the most recent commit, adding 5 fabrication personas, updated CLAUDE.md
and README structure listing — this is the recurring tax). CLAUDE.md and README carry
near-identical tables of skills, teams, personas, and modifiers.

**Fix:** one index per audience, minimal overlap:

- **CLAUDE.md** (machine-facing, loaded every session): keep the three-layer explanation,
  session rules, conventions, and a *name → path* index only (one line per item, no
  descriptions — descriptions live in the files themselves, which Claude loads on demand).
  Target ≤ 4 KB, down from ~12 KB.
- **README.md** (human-facing): keeps the descriptive tables and quick-start. Accept that
  README descriptions can lag; only paths in CLAUDE.md are load-bearing.

### 2.3 Skill boilerplate

Every skill repeats the identical context-gathering scaffold ("1. If the user has included …
2. If invoked alone, prompt … 3. Optionally ask … Do not proceed until …"), the sentence "Each
persona must respond in character — voice, priorities, and concerns should reflect their
definition in `agents/stable/`…", the "No external dependencies" line, and the DA-dissent
footer convention.

**Fix:** extract a `skills/_conventions.md` covering: context-gathering protocol, in-character
requirement, optional-member activation protocol (currently only security-review spells one
out; feature-design and technical-discovery list optional members in the team file but the
skills never say how to activate them), dissent handling, and the output-format ownership rule
(team file owns format unless the skill overrides). Each skill then contains only its unique
prompt text and genuine deltas. Also standardise the `## Example invocation` section — today
only review-proposal and security-review have one; either all skills get one or none do.

### 2.4 Overlapping persona domains (sharpen, don't merge)

DevOps/Platform Engineer, Build & Toolchain Engineer, and Systems/Infrastructure Engineer share
roughly 40% of their concern surface (CI/CD, IaC, secrets handling, supply chain,
reproducibility, environment parity) — and they sit together on five teams, which produces
redundant passes. Security Engineer overlaps all three on secrets/supply-chain.

**Fix:** keep all four personas (their centers of gravity differ), but add a short
**"Defer to"** subsection to each: e.g. Build & Toolchain defers pipeline *infrastructure* to
Systems/Infra, deployment integration to DevOps/Platform, supply-chain *risk rating* to
Security. This is cheap, prevents four personas re-covering secrets management in one review,
and matches the instruction already present in devops-automation ("they do not re-cover ground
the Build & Toolchain Engineer has already addressed unless they disagree") — generalise that
rule into the persona files instead of restating it per team.

---

## 3. Findings — holes

### 3.1 Teams with no skill (4 of 12)

| Team | Reachable today? | Note |
|---|---|---|
| Implementation | ❌ | The feature-design team explicitly "hands off to the Implementation team" — but there is no `/implementation-review`. Mobile has one; general doesn't. Clear asymmetry. |
| DevOps / Automation | ❌ | |
| Dev Environments | ❌ | |
| Server / Cloud Infrastructure | ❌ | |

**Fix:** add `/implementation-review` as a first-class skill (parity with
`/mobile-implementation-review`, same shape). For the three specialist infra teams, do **not**
add three more near-identical skill files — that would recreate §2.1's duplication. Add one
parameterised skill, `/team-review <team>`, that loads any named team and runs its default
interaction model with the standard context-gathering protocol. Thin named aliases
(`/toolchain-review`, `/infra-review`) can be added later only if usage shows they're wanted.

### 3.2 Orphaned personas (6 of 24)

Digital Fabrication Engineer, Inkscape Extension Developer, Woodworking/Joinery Specialist,
2D Vector Graphics Engineer, 3D Vector Graphics Engineer, and — ironically for this document —
the Consolidation Architect appear in **no team and no skill**. They are unreachable through
the system's own invocation model.

**Fix:**
- Add a **Fabrication Design team** (Digital Fabrication Engineer lead, Woodworking/Joinery
  Specialist, 2D Vector Graphics Engineer, Devil's Advocate; optional: Inkscape Extension
  Developer, 3D Vector Graphics Engineer, Domain Expert) with a lead-analysis → specialist →
  stress-test → synthesis model, and a `/fabrication-review` skill. The five fabrication
  personas were clearly added for a real workload; give them a front door.
- Add **Consolidation Architect** as an optional member of Architecture Design (activate when
  the brief touches duplicated capability) and consider a `/consolidation-review` skill later.
  Alternatively fold reachability into `/consult` (§3.4).

### 3.3 Modifier/persona targeting syntax is undefined

`/review-proposal [architect:cautious] [dev:pragmatist]` — nothing defines what `architect` or
`dev` resolve to. `dev` could be Senior or Junior Developer; `architect` could be System
Architect, Staff/Principal, or Consolidation Architect. This is a specification hole in the
system's own invocation grammar.

**Fix:** add a canonical alias table (in CLAUDE.md conventions or `agents/modifiers/_targeting.md`):

| Alias | Persona |
|---|---|
| `architect` | System Architect |
| `staff` | Staff / Principal Engineer |
| `dev` | Senior Developer |
| `junior` | Junior Developer |
| `lead` | Tech Lead |
| `da` | Devil's Advocate |
| `po` | Project Owner |
| `pm` | Product Manager |
| `qa` | QA Engineer |
| `sec` | Security Engineer |
| `devops` | DevOps / Platform Engineer |
| `build` | Build & Toolchain Engineer |
| `sysinf` | Systems / Infrastructure Engineer |
| `standards` | Code Standards Reviewer |
| `ux` | UX Reviewer |
| `mobile` | Mobile App Developer |
| `release` | Release Manager |
| `domain` | Domain Expert |
| `consol` | Consolidation Architect |
| `fab` / `wood` / `2d` / `3d` / `inkex` | fabrication cluster |

Unknown aliases and mutually-exclusive modifier combinations are configuration errors Claude
must flag (the latter rule already exists; the former doesn't).

### 3.4 No lightweight invocation path

Every entry point is a full multi-persona ceremony. There is no way to ask one persona one
question — the cheapest thing available is the two-persona `/review-proposal` with
cross-examination and synthesis.

**Fix:** add `/consult <persona-alias>` — load one persona (plus modifiers), respond in
character, no interaction model, no structured output beyond the persona's own output
tendencies. This also makes the orphaned specialists (§3.2) individually reachable and is the
natural home for quick follow-up questions after a full team run.

---

## 4. Findings — inefficiency

### 4.1 Context cost

- **Per session:** CLAUDE.md (~12 KB, mostly tables) is injected into every session. §2.2 cuts
  this by ~two-thirds.
- **Per skill run:** skill + team + 4–7 personas ≈ 25–40 KB of definitions loaded before any
  analysis. §2.1/§2.3 trim the skill file's share. Persona files are the dominant remaining
  cost; they are well-written and worth their weight for full runs, so no cuts recommended
  there — but see §5.4 for how fan-out execution changes the calculus.

### 4.2 Sequential-only execution

Three team files describe their analyses as independent — security-standards-review
("parallel review"), implementation and mobile-development ("parallel analysis") — yet
everything runs as one long sequential generation in a single context. That is correct for the
*debate-shaped* teams (cross-examination requires seeing prior turns) but leaves real
parallelism on the table for the *fan-out-shaped* teams, and it means every persona's pass is
conditioned on the previous personas' output even when the team model explicitly says the
"independent view is the valuable input" — a mild anchoring defect, not just a speed issue.

**Fix (Phase 3):** define two execution modes as a documented convention:

- **Inline mode (default):** current behaviour. Zero orchestration overhead. Right for short
  briefs, debate-shaped models, and environments without subagent support.
- **Fan-out mode (opt-in, `[exec:fanout]` or skill default):** for parallel-review teams with
  large inputs (e.g. `/security-review` on a big diff), run each persona pass as a subagent
  (Claude Code Agent tool / Task tool) with only that persona's file + the shared context;
  integrator persona consolidates. Genuinely independent analyses, parallel wall-clock time,
  and each subagent's context stays small. Not worth it for small inputs — each subagent
  cold-starts and re-reads the shared context, so the break-even is roughly when the input
  under review is larger than the persona definitions.

Fan-out mode is also the natural attachment point for model routing (§5).

---

## 5. Model routing — Opus by default, Fable as escalation

### 5.1 Premise

Fable sits above Opus in capability and carries additional gating (availability, permissions,
and dual-use safety measures), so treat it as a scarce escalation resource, not a default.
Target state: **every persona pass runs on Opus unless a step is explicitly marked for
escalation**, and every escalation has a mandatory, output-identical Opus fallback.

The repo is model-agnostic markdown, so routing is expressed as *declarations* that the
executing Claude honours when it can (via subagent model selection in fan-out mode, or by
noting the advisory tier in inline mode) and ignores gracefully when it can't.

### 5.2 Tiers

Define once in a new `agents/models.md`:

| Tier | Model | Fallback | Used for |
|---|---|---|---|
| `standard` | Opus | — | Default for *everything*: persona passes, context gathering, formatting, synthesis on routine skills |
| `deep` | Fable (if available **and** permitted) | Opus, silently | Judgment-critical steps on high-stakes skills only (see 5.3) |
| `light` *(optional, defer)* | Haiku | Opus | Mechanical steps only (restating context, table formatting). Recommend **not** adopting initially — savings are small and quality risk in persona voice is real |

Rules:
- Fallback is silent and mandatory; the step's output contract is identical regardless of
  model, so downstream steps never depend on which tier actually ran.
- Escalation is **by step function, not by persona**. The Devil's Advocate is not "a Fable
  persona"; the *assumption-challenge step of an irreversible decision* is a Fable step.
- Never escalate more than 2 steps per skill run. If everything is deep, nothing is.

### 5.3 What actually benefits from Fable (the variation design)

The differences worth exploiting: Fable's edge is largest on steps that must (a) hold many
conflicting constraints simultaneously, (b) reason adversarially about what's *missing* rather
than checklist what's present, or (c) integrate long multi-voice context into a decision.
Domain-coverage passes (QA test matrix, DevOps pipeline checklist, standards conformance) are
breadth work where Opus is fully adequate — routing those to Fable buys little.

Per-skill defaults:

| Skill | `deep` steps (Fable, fallback Opus) | Rationale |
|---|---|---|
| `/architecture-design` | Devil's Advocate stress test; final synthesis | Hard-to-reverse decisions; synthesis must reconcile architect vs staff vs DA vs PO positions |
| `/technical-discovery` | Assumption challenge; joint synthesis | The whole point is reframing the problem — the step where marginal reasoning depth changes the answer |
| `/release-planning` | Go/no-go synthesis (Release Manager) | Single irreversible verdict integrating all criteria + risk acceptances; DA stays standard (it's evidence-checking, not reframing) |
| `/security-review` | Consolidation + P0–P3 prioritisation | Cross-finding interaction ("standards violation that is also a security risk") and severity judgment; the parallel reviews themselves stay standard. Note: Fable's dual-use safety measures may make it more conservative on exploit detail — acceptable for defensive review; the fallback covers the rest |
| `/project-planning` | *(none by default)* — `[model:deep]` opt-in on synthesis for multi-quarter roadmaps | Sprint planning doesn't warrant it; the team file's own override ("multi-quarter → scenario analysis") is the trigger |
| `/feature-design`, `/mobile-feature-design` | *(none)* | Feature-level, reversible; Opus throughout |
| `/review-proposal` | *(none)* | This is the lightweight path by design |
| `/implementation-review`, `/mobile-implementation-review` | *(none by default)*; integration step opt-in when verdict gates a release | |
| `/consult` (new) | *(none)*; whole run opt-in via `[model:deep]` | |

### 5.4 Mechanics

1. **`agents/models.md`** — tier definitions, fallback rules, escalation budget, and the
   per-skill default table above. Single source of truth.
2. **Team files** — no changes; steps stay model-agnostic (teams define *who and how*, not
   *what hardware*, consistent with existing conventions).
3. **Skill files** — one short `## Model routing` section each: which steps are `deep` by
   default, referencing `agents/models.md` for semantics. Skills already own task-specific
   configuration, so this is the right layer.
4. **Invocation overrides** — extend the existing bracket grammar: `[model:deep]` /
   `[model:standard]` (whole run), `[da:deep]` (per-step/persona, reusing §3.3 aliases).
   `[model:standard]` forces Fable off entirely — the "as allowed" control the user holds.
5. **Execution-mode interaction** — in **fan-out mode**, routing is literal: `deep` steps run
   as Fable subagents when the environment offers Fable, Opus otherwise. In **inline mode**,
   the session model runs everything; if the session itself is on Fable, the entire run is
   effectively deep (fine — routing is a floor-lowering mechanism for cost, not a ceiling);
   if the session is on Opus and a `deep` step is declared, Claude may spawn a single `deep`
   subagent for that step or simply proceed on Opus — both are compliant because fallback is
   always legal.
6. **CLAUDE.md** — one paragraph in conventions: "Skills may declare model routing per
   `agents/models.md`; honour it when the environment supports model selection, fall back to
   the session model otherwise. Never block a skill because a preferred model is unavailable."

This keeps the whole feature *advisory and degradable*: on a plain Claude session with no
subagent or model-selection capability, every skill still runs exactly as today.

---

## 6. Phased plan

### Phase 1 — Deduplicate (no behaviour change; do first)
1. Make team files authoritative for interaction models; shrink all 9 skill `Execution`
   sections to reference + genuine overrides + task-specific emphasis (§2.1).
   Reconcile the release-planning and mobile-implementation-review divergences explicitly.
2. Extract `skills/_conventions.md`; strip repeated boilerplate from all skills (§2.3);
   standardise optional-member activation and example-invocation sections.
3. Slim CLAUDE.md to explanation + rules + name→path index; README keeps descriptions (§2.2).
4. Add "Defer to" boundaries to the four overlapping infra/security personas (§2.4).

### Phase 2 — Fill holes
5. `/implementation-review` skill for the Implementation team (§3.1).
6. `/team-review <team>` parameterised skill covering the three specialist infra teams (§3.1).
7. Fabrication Design team + `/fabrication-review` skill; Consolidation Architect as optional
   member of Architecture Design (§3.2).
8. Persona alias table + unknown-alias error rule (§3.3).
9. `/consult <persona>` lightweight skill (§3.4).

### Phase 3 — Execution & model routing
10. Document inline vs fan-out execution modes; mark the three parallel teams as
    fan-out-eligible (§4.2).
11. Add `agents/models.md`, per-skill `## Model routing` sections, `[model:…]` grammar,
    CLAUDE.md convention paragraph (§5).

### Deliberately not doing
- Merging overlapping personas (distinct centers of gravity; boundaries fix is cheaper).
- Persona "digest" short forms (token savings don't justify voice degradation).
- A `light`/Haiku tier at launch (§5.2).
- Three separate infra skills (parameterised skill instead).

### Success measures
- Places to edit when adding a persona: 3 → 2 (file + one-line index).
- Places where an interaction model is defined: 2 → 1 per skill/team pair.
- CLAUDE.md session overhead: ~12 KB → ≤ 4 KB.
- Teams reachable by skill: 8/12 → 13/13; personas reachable: 18/24 → 24/24.
- Fable usage: 0 declared uses → ≤ 2 steps per run on 4 skills, always Opus-degradable.
