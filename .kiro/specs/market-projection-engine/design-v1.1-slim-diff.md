# v1.1 Slim vs v1.1 Full — Diff

> **Purpose**: reconcile the existing `design-v1.1.md` (Full) with the Grok-proposed Slim implementation prompt. Decide which Slim simplifications to adopt, which Full elements to preserve, and what Phase 6 in `tasks.md` actually looks like before any code is written.
>
> **Status**: draft for Richard review. No code changes yet. Once this is approved, we write a single reconciled Phase 6 task list and start Phase 6.1.
>
> **Author context**: Full came from Richard + agent 2026-04-23 after the MX Y2026 @ 75% → $443K gap. Slim came from an external "Grok" AI round after Richard asked for something more pragmatic for a non-technical owner on a 3-4 week demo clock. This diff is agent-written, Richard-approved.

---

## TL;DR

Both docs agree on the big architecture move: Brand-Anchor + NB-Residual replaces the v1 top-down aggregate elasticity solver. They disagree on:

1. **Evidence streams in the Brand model** — Full uses 4 (seasonal + trend + regime + qualitative), Slim uses 3 (seasonal + trend + regime) with qualitative deferred to Phase 3.
2. **Locked-YTD behavior** — Slim requires it as a first-class feature in Phase 1. Full doesn't explicitly call it out as a solver input, though session-log 2026-04-23 already established it as a required principle.
3. **Phasing** — Full has 7 implementation sub-phases (6.1–6.7). Slim has 3 phases with Phase 1 as the only thing we start now.
4. **Solver branch scope in Phase 1** — Full builds all 4 NB solver branches at once in Phase 6.2. Slim builds 4 branches in Phase 2, with only `ieccp` wired through the main path in Phase 1.
5. **Fallback policy during rollout** — Slim keeps the v1 solver as hidden fallback for 2 weeks. Full explicitly deletes v1 when v1.1 ships ("maintaining two models doubles the maintenance burden without winning anything").
6. **Corporate-environment instructions** — Slim includes fake PyPI URLs and a `--network=host` note that don't apply to this environment.

Recommendation: **adopt Slim's phasing and Locked-YTD first-class treatment. Keep Full's 4-stream Brand model as the endgame, but ship 3-stream in Phase 1 and add qualitative in Phase 3. Reject Slim's fallback-retention policy — Full's delete-on-ship is the right call. Ignore Slim's corporate instructions.**

---

## What we keep from v1.1 Full (unchanged)

The following sections of `design-v1.1.md` are canonical and survive into the reconciled plan:

- **Model identity** (`brand_regs × brand_CPA` + `NBSolver(target, brand, params)`) — unchanged. This is the whole architectural move and both docs agree.
- **Four solver branches** (`ieccp`, `regs`, `spend`, `op2_efficient`) — identified in Full, named identically in Slim. All four ship, just in different phases.
- **Brand CPA as scalar-per-regime (not elasticity)** — Full position, Slim doesn't contradict. `brand_cpa_projected` stays as the deprecation path for `brand_cpa_elasticity`.
- **What v1 components stay** (Parameter Layer tables, Python/JS mirror, UI shell, quarterly refit, parity testing, NB CPA elasticity fit method, seasonality fit method, Mechanism A operational bounds, narrative pipeline, 5-regime-event exclusion logic, MC uncertainty) — all retained.
- **What v1 components get replaced** (top-down elasticity solver, Brand CPA elasticity fit, Brand CPC elasticity fit, Brand YoY growth scalar, `brand_spend_share` parameter, regional "percent of markets" rollup) — all deprecated in v1.1, same list in both docs.
- **Regional scope constraints** (NA = US+CA+MX, EU5 = UK+DE+FR+IT+ES, WW = 10 markets with AU excluded from ie%CCP denominator) — unchanged.
- **AU first-class handling** (`op2_efficient` default, SH hybrid seasonality retained, `polaris_retained` as AU-specific qualitative prior) — unchanged.
- **Validation plan** (Brand MAPE <20% on 12-week holdout, aggregate MAPE <25%, 5 acceptance scenarios including MX Y2026 @ 75% in the $800K–$1.2M range) — unchanged.
- **v1.2 deferrals** (probabilistic Brand uncertainty, cross-market spillover, auto regime detection, multi-year, cannibalization adjustment) — unchanged. "v1.4 structural Bayesian" from session-log 2026-04-23 is not scoped here; parked separately.
- **Principle: decision-support, not decision-maker** — the "engine is a thinking partner" stance is the whole point. Both docs agree, Full says it more explicitly.

---

## What Slim simplifies vs Full

### 1. Brand trajectory: 3-stream in Phase 1, 4-stream by Phase 3

**Full (design-v1.1.md):**
```
brand_regs[w] = annual_baseline
              × seasonal_multiplier[w]          × W_seasonal          (0.40)
              × recent_trend_multiplier[w]      × W_trend             (0.40)
              × regime_multiplier               × W_regime            (0.15)
              × qualitative_prior_multiplier[w] × W_qualitative       (0.05)
```

**Slim:**
```
brand_regs = baseline × seasonality_factor × trend_multiplier
# regime + qualitative added in Phase 3
```

**Reconciled position**: ship 2-stream (seasonal + trend) in Phase 1 per Slim's template, add regime multiplier in Phase 2 per Slim's Phase 2 scope, add qualitative priors in Phase 3.

**Why**: the 2-stream version is testable against MX immediately with seasonality already fit in v1. Regime multiplier requires reading `ps.regime_changes` which is well-understood infrastructure. Qualitative priors need a YAML catalog and UI controls which are Phase 3 anyway. Weights remain at Full's defaults (0.40/0.40/0.15/0.05), just with `W_qualitative` routed to 0 until Phase 3.

**Risk**: 2-stream Brand in Phase 1 against MX may undershoot for a Sparkle-era market. Mitigate by running the Phase 1 check on MX Y2026 @ 75% and confirming the number lands in the $800K–$1.2M range using Locked-YTD (see below). If it doesn't, regime multiplier moves from Phase 2 to Phase 1.

---

### 2. Locked-YTD becomes a first-class Phase 1 requirement

**Full**: Locked-YTD isn't explicitly named in `design-v1.1.md`. The doc focuses on the model identity and solver branches. However, session-log 2026-04-23 established that the MPE solver had been silently projecting below YTD actuals (producing $431K when YTD was already $279K at ie%CCP ~99%, making the remaining 36 weeks require a physically impossible spend profile).

**Slim**: Locked-YTD is Deliverable 1 in Phase 1 via `project_with_locked_ytd()`. The function detects whenever a projection time period covers weeks in the past and locks those to actuals, only projecting forward weeks.

**Reconciled position**: **adopt Slim's first-class treatment.** This is the single-biggest correctness fix in the session-log record and it should not live as an implicit principle. We amend `design-v1.1.md` to formalize Locked-YTD as a required solver pre-step:

> Before the solver runs, the engine partitions the projection period into `locked_weeks` (weeks that fall within YTD actuals per the data cutoff) and `open_weeks` (remaining-of-year). The solver's NB residual is computed only over `open_weeks`, with `locked_weeks` NB spend and NB regs taken from `ps.v_weekly` actuals. Total projection is `locked + open`. The solver never reduces spend below `sum(locked) + min_remaining_nb_spend`.

**Warning**: `LOCKED_YTD_CONSTRAINT_ACTIVE` fires when the solver would have otherwise produced a lower-spend answer but is bounded by the YTD floor. Includes "weeks locked" count and "spend floor" dollar value.

---

### 3. Phasing: 3 phases, Phase 1 only

**Full** — 7 sub-phases under Phase 6:
- 6.1 Build `BrandTrajectoryModel`
- 6.2 Build `NBResidualSolver` with all 4 branches
- 6.3 Replace v1 solver in engine + JS mirror
- 6.4 Extend parameter registry (new fields + deprecate old)
- 6.5 UI (contribution breakdown, scenario picker, weight sliders)
- 6.6 Validation on all 10 markets
- 6.7 Migrate live pipelines (callouts, WBR, Lorena)

**Slim** — 3 phases:
- Phase 1: Locked-YTD + 2-stream Brand + wire into engine (hidden v1 fallback)
- Phase 2: NB Residual Solver (all 4 branches) + regime multiplier
- Phase 3: UI + qualitative scenario picker + parameter registry updates

**Reconciled position**: **adopt Slim's 3-phase compression** for demo-clock reasons (3-4 weeks vs 7 phases). Each Slim phase maps to a Full bundle:
- Slim Phase 1 = Full 6.1 (partial: 2-stream) + 6.3 (partial: `ieccp` branch only) + new Locked-YTD scope
- Slim Phase 2 = Full 6.1 (complete: add regime multiplier) + 6.2 (full: all 4 branches) + 6.4 (partial: needed parameters)
- Slim Phase 3 = Full 6.5 (UI + scenario picker) + 6.4 (complete: all parameter fields) + 6.6 (validation) + 6.7 (pipeline migration)

This is a straight re-grouping, not a scope cut (except for qualitative-priors-in-Phase-3 and 2-stream-first).

---

### 4. Solver branch sequencing

**Full**: "Phase 6.2 — Build `NBResidualSolver` with all four branches, tested independently." All four branches in one phase.

**Slim**: Phase 1 wires `ieccp` through the main path only. All four branches come in Phase 2.

**Reconciled position**: **adopt Slim's split**. `ieccp` is the demo-critical branch (MX Y2026 @ 75% is the acceptance test). `op2_efficient` matters for AU but AU ships later. `spend` is trivial. `regs` is a bisection like `ieccp`. Building all four in Phase 2 is fine.

**Caveat**: `spend` branch is so simple (direct subtraction of Brand spend from total budget) that it should go in Phase 1 as a sanity-check / escape-hatch even though it's not the demo path. Costs 10 lines.

---

### 5. Fallback policy: delete-on-ship vs 2-week retention

**Full**: "The v1 solver is deleted when v1.1 ships, not kept as a fallback — maintaining two models doubles the maintenance burden without winning anything."

**Slim**: "Keep old solver as hidden fallback for 2 weeks."

**Reconciled position**: **reject Slim's fallback retention. Keep Full's delete-on-ship.**

Reasons:
- Maintaining two solvers for 2 weeks means debugging two solvers every time an output looks wrong. Non-technical owner can't triage which solver produced which number.
- The Phase 1 acceptance test (MX Y2026 @ 75% in $800K–$1.2M range) is a go/no-go gate. If v1.1 fails that test, we don't ship — there's no "fall back to v1" scenario because v1 is already known to produce $443K in that scenario.
- Parity testing in both docs compares Python ↔ JS for the SAME model, not v1 ↔ v1.1.
- "Hidden fallback" is a violation of soul.md principle #5 (invisible over visible) in the wrong direction — it introduces hidden behavior that can confuse the owner.

**Mitigation if v1.1 has issues post-ship**: git revert the v1.1 PR. Standard software hygiene, not dual-model maintenance.

---

### 6. Corporate-environment instructions

**Slim**:
```bash
pip install --index-url https://your-internal-pypi.amazon.com/simple/ --trusted-host your-internal-pypi.amazon.com
```
Plus "mount `.aws` and `.ssh` folders in devcontainer" and "Use `--network=host` only if it doesn't break corporate policy."

**Reconciled position**: **ignore.** MPE is a DuckDB + Python tool running in DevSpaces. No pip installs are required for the v1.1 build (all deps are in the existing devspace image). The Slim prompt was written by an AI that doesn't know this environment. Session-log 2026-04-22 noted the prompt had "fake PyPI URL" as a red flag.

---

### 7. Miscellaneous Slim additions to adopt

**Slim**: "Every new function must have clear comments explaining what it does in plain English."

**Reconciled position**: **adopt.** This is consistent with `mpe_fitting.py`'s existing "Heavy file header documents why/how/failure per R0 non-technical-owner guidance" pattern. Makes it easier for Richard to read the engine without help.

**Slim**: "Every new output must have a clear 'Explain this' tooltip or comment."

**Reconciled position**: **adopt as Phase 3 UI requirement.** Not Phase 1 (CLI output doesn't need tooltips), but the contribution-breakdown UI in Phase 3 should show "Explain this number" on each multiplier, mirroring the existing v1 pattern of "Explain this" tooltips on Brand CCP, NB elasticity, etc.

**Slim**: "Test every new component against real MX data immediately."

**Reconciled position**: **adopt.** This is a restatement of Full's acceptance test scenarios (MX Y2026 @ 75% in $800K–$1.2M). Every phase ends with an MX run and a before/after diff.

**Slim**: "Do not implement the full v1.4 structural Bayesian system yet. This is v1.1 Slim only."

**Reconciled position**: **adopt verbatim.** v1.4 is parked per Richard's 2026-04-23 confirmation that "v1.4 isn't officially scoped yet." Session-log entry captures the v1.4 design questions (target commitment, math ownership, v1.4 composes vs obsoletes v1.1) for a future session.

---

## New concepts introduced by Slim (not in v1.1 Full)

### Locked-YTD + RoY projection
Already covered above. Formalized in the reconciled plan as a required pre-solver step.

### Contribution breakdown as Phase 1 deliverable
**Full**: contribution breakdown is in Phase 6.5 UI work ("Brand W22 regs 1,038: 41% seasonal, 38% trend, 18% regime, 3% prior").

**Slim**: `BrandTrajectoryModel` returns a `contribution` dict as part of its core output in Phase 1.

**Reconciled position**: **Slim's approach is better.** Make contribution a first-class return value of `BrandTrajectoryModel`, surfaced in the CLI output even before UI lands. This means every MX Y2026 run from Phase 1 forward shows "Brand 11,200 regs = 45% seasonal + 42% trend + 13% regime (+ 0% qualitative)" and the decomposition is available for debugging.

### "Explain this" as a portable principle
Slim promotes the "Explain this" tooltip from the v1 UI ("Explain this Brand CCP") to a general principle for every new output field.

**Reconciled position**: **adopt** — but only where it maps cleanly. CLI output doesn't need it (markdown rendering is already explanatory). UI outputs do. Parameter registry entries already have `provenance` fields which serve the same purpose.

---

## Phasing comparison (side-by-side)

| Scope item | Full Phase | Slim Phase (v2) | Reconciled |
|---|---|---|---|
| `BrandTrajectoryModel` (seasonal) | 6.1 | Phase 1 | **Phase 1** |
| `BrandTrajectoryModel` (+ trend) | 6.1 | Phase 1 | **Phase 1** |
| `BrandTrajectoryModel` (+ regime) | 6.1 | Phase 1 (promoted) | **Phase 1** |
| `BrandTrajectoryModel` (+ qualitative) | 6.1 | Phase 3 | **Phase 3** |
| `NBResidualSolver` `ieccp` branch | 6.2 | Phase 1 | **Phase 1** |
| `NBResidualSolver` `spend` branch | 6.2 | Phase 1 | **Phase 1** |
| `NBResidualSolver` `regs` branch | 6.2 | Phase 2 | **Phase 2** |
| `NBResidualSolver` `op2_efficient` branch | 6.2 | Phase 2 | **Phase 2** |
| Locked-YTD partitioning | (implicit) | Phase 1 | **Phase 1** (first-class) |
| Contribution breakdown in output | 6.5 | Phase 1 | **Phase 1** (CLI-first) |
| Engine v1 solver swap + delete | 6.3 / 6.7 | Phase 1 | **Phase 1** |
| Parameter registry — new Brand fields | 6.4 | Phase 1 (needed for regime) | **Phase 1** |
| Multi-market validation (MX + EU5 + AU) | 6.6 | Phase 1 (continuous) | **Phase 1** (continuous) |
| UI contribution panel | 6.5 | Phase 3 | **Phase 3** |
| UI scenario picker | 6.5 | Phase 3 | **Phase 3** |
| UI weight sliders | 6.5 | (not specified) | **Phase 3** |
| Qualitative priors catalog (YAML) | 6.5 | Phase 3 | **Phase 3** |
| 10-market validation sign-off | 6.6 | Phase 3 | **Phase 3** |
| Pipeline migration (callouts, WBR, Lorena) | 6.7 | Phase 3 | **Phase 3** |

**Timeline under reconciled**: Phase 1 ≈ 1.5 weeks (bigger than original estimate because regime was promoted in + multi-market validation runs continuously), Phase 2 ≈ 1 week, Phase 3 ≈ 1-2 weeks. Total 3-4 weeks, matching Slim's stated timeline and leaving buffer before 2026-05-16 demo.

---

## Open questions — RESOLVED 2026-04-23

Richard's decisions, per the updated market-neutral Slim prompt:

1. **Qualitative priors in Phase 3** — CONFIRMED. Locked-YTD + 3-stream is sufficient for Phase 1 to hit the $800K–$1.2M range for MX Y2026 @ 75%. Qualitative priors land in Phase 3.

2. **3-stream from the start** — CONFIRMED. Regime multiplier is PROMOTED from Phase 2 to Phase 1. Phase 1 ships Brand = Seasonal + Trend + Regime (3-stream). Qualitative = 4th stream added in Phase 3.

3. **`spend` branch in Phase 1** — CONFIRMED.

4. **Delete v1 on ship** — CONFIRMED. No dual-maintenance period.

5. **AU / `op2_efficient` in Phase 2** — CONFIRMED. MX is the Phase 1 primary demo market, but **Phase 1 acceptance tests run against MX + EU5 (representative member: DE) + AU** to catch market-neutrality issues early. AU's `op2_efficient` solver branch waits until Phase 2.

**New in the market-neutral Slim prompt**: validation discipline tightens to "Test every new component against real data from multiple markets (start with MX, then EU5 and AU)." This replaces the v1.1 Full stance of "MX first, then Phase 6.6 does 10-market validation" — multi-market validation becomes continuous, not a separate phase.

---

## Status — APPROVED 2026-04-23

Richard approved this diff (with Q2 promotion: regime multiplier moves into Phase 1) via the market-neutral Slim prompt update. Phase 6 task breakdown now lands in `tasks.md`. Execution starts with Phase 6.1 only; stop for review before Phase 6.2.

## Recommended path forward

1. **Amend `design-v1.1.md`** with the Locked-YTD section (small, ~30 lines) and a note that v1.1 Slim phasing supersedes the 7-phase 6.1–6.7 breakdown. Retain the design doc as the architectural-rationale record.
2. **Append `tasks.md` Phase 6** with three sub-phases (6.1 / 6.2 / 6.3 mapping to Slim Phase 1 / 2 / 3), each broken into specific tasks with acceptance criteria.
3. **Execute Phase 6.1 only**, stop after the MX + DE + AU acceptance tests run, show before/after numbers, wait for Richard review.

Phase 6 task breakdown is ~120 lines appended to the existing `tasks.md` (739 lines → ~860 lines). Then we code.

---

*Doc owner: Richard Williams. Drafted 2026-04-23 agent, pending Richard review. Supersedes Grok's external `Kiro-v1-1-Slim-Implementation-Prompt.md` as the authoritative v1.1 Slim plan if approved.*
