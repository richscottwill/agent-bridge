# MPE Changelog

Architectural-level audit trail. Session-log interleaves unrelated topics;
this file tracks only MPE architecture moves.

---

## v1.1 Slim — shipped 2026-04-23 through 2026-04-26

**Core move**: Top-down elasticity solver → Brand-Anchor + NB-Residual + Locked-YTD.

**Why**: v1 solved for a spend envelope then allocated Brand/NB via `brand_spend_share`, which conflated two independent market facts (Brand economics driven by campaign lifts + seasonality; NB economics driven by spend curves). When MX Sparkle campaign landed W14 2026 and stepped Brand regs from ~200 → ~400 per week, v1's elasticity-fit anchor averaged that against pre-Sparkle data and produced a ~$900K Y2026 @ 75% ie%CCP projection that leadership dismissed.

**New architecture**:
- **Brand-Anchor** (`shared/tools/prediction/brand_trajectory.py`) — per-market Brand regs projected from seasonal × trend × regime-stream multipliers on a recent-actuals anchor. Regime stream normalized at anchor reference week (2026-04-26 rework) to prevent double-counting.
- **NB-Residual** (`shared/tools/prediction/nb_residual_solver.py`) — solves NB spend to hit the user's target (ie%CCP, spend, regs, or op2_efficient). Four branches. Target-relational bounds (±500bps for ie%CCP).
- **Locked-YTD** (`shared/tools/prediction/locked_ytd.py`) — YTD actuals treated as immutable; RoY projected only. Prevents projections from contradicting already-locked data.
- **Regime fit state** (`shared/tools/prediction/fit_regime_state.py` + `ps.regime_fit_state`) — per-regime peak_multiplier, fitted_half_life_weeks, decay_status, confidence. Weekly hook refreshes state.

**Regional semantics** (v5 refactor): regions are **rollups**, not drivers. Per-market targets can differ from regional aggregate. `target_mode='ieccp'` rejected at region scope.

**Per-market committed ie%CCP targets** (v4 refactor):
- MX = 100%, US/CA/UK/DE/FR/IT/ES = 65%, JP + AU = spend-only (no ie%CCP target).
- NA rollup = 65.0%, EU5 = 65.0%, WW = 63.9% (mixed targets).

**Qualitative priors catalog** (`qualitative_priors.yaml`, Phase 6.5.1) — 4th Brand evidence stream. 8 scenarios catalogued; W_qualitative = 0.20 on explicit select, 0.00 default.

**Scenario chip taxonomy** (2026-04-26): replaced per-market brand-named chips (Sparkle sustained / Polaris persist / etc) with four methodology stances: **Current plan (Mixed)**, **Frequentist**, **Bayesian**, **No lift**. Zero per-market maintenance; self-documenting. MX Y2026 @ 100% ie%CCP monotonic spread: No lift $1.31M → Frequentist $1.56M → Mixed $1.79M → Bayesian $2.48M.

**Pipeline migration** (Phase 6.5.5): WBR hook now calls `write_v1_1_slim_forecasts.py` as Stage 4b in parallel with `BayesianProjector`. Both methods coexist in `ps.forecasts`; retirement of Bayesian gated on 4+ scoring cycles of comparative MAPE.

**Anchor rework** (2026-04-26): anchor is now a recent-actuals mean, not a pre-first-regime baseline. Fixed the MX W15–W17 discontinuity where projections dropped to ~250 regs right after actuals stepped to ~380.

**Viz layer**: Observable Plot 0.6.17 + D3 7.9.0 via CDN. Standalone HTML render — no build step. Three views: single market / all 10 markets (2×5) / distance-to-target heat-grid. Scenario chip animated transitions. Native-canvas PNG share card (no html2canvas dep). Responsive to tablet + mobile.

**Validation** (Phase 6.5.2): 10-market 12-week holdout backtest. 8/10 markets meet Brand MAPE <22% gate (MX + JP excluded due to regime-crossings in holdout window). Report: `shared/wiki/agent-created/operations/mpe-v1-1-slim-validation-report.md`.

**Test state**: 131/131 Python tests + 3/3 JS parity green.

**Files created**:
- `prediction/brand_trajectory.py`
- `prediction/nb_residual_solver.py`
- `prediction/locked_ytd.py`
- `prediction/regime_confidence.py`
- `prediction/fit_regime_state.py`
- `prediction/qualitative_priors.{yaml,py}`
- `prediction/backtest_v1_1_slim.py`
- `prediction/feedback_triage.py`
- `prediction/write_v1_1_slim_forecasts.py`
- `dashboards/v1_1_slim.js` (JS mirror)
- `dashboards/projection-design-system.css`
- `mpe_schema_v{3..7}.sql`

**Files deleted**:
- `prediction.mpe_engine._solve_ieccp_target` + `_solve_regs_target` (v1 primary solvers)

**Key session-log entries**: 2026-04-23 architecture decision, 2026-04-25 Phase 6.3 handback, 2026-04-26 Phase 6.4 handback + Phase 6.5 scenarios.

---

## v1.0 — original, 2025-Q4 → 2026-04-22

**Core**: top-down elasticity solver. CPA ≈ exp(a) × spend^b with `brand_spend_share` allocating total to Brand/NB.

**Ship state**: reached Phase 0 + Phase 1 + Phase 2 + Phase 3.MX complete. All Phase 3 per-market and Phase 4/5 tasks superseded by v1.1 Slim refactor.

**Why replaced**: unable to represent campaign-lift Brand dynamics that stepped independent of spend (MX Sparkle, JP OCI). Anchor + lift architecture emerged as cleaner decomposition.

---

## v1.2 — placeholder roadmap

- Skeleton posterior (Level 1 Bayesian) — explicit priors on Brand trend slope, regime peak, NB elasticity `b`.
- BOCPD (Bayesian online change-point detection) — replace hand-curated `ps.regime_changes` onsets with automatic regime detection.
- Probabilistic decay curves — replace single-point `half_life_weeks` with posterior over decay-life.
- **Tooling**: NumPyro (JAX) primary, PyMC+Bambi prototyping layer. CausalImpact-style viz already live in 6.3.3 counterfactual overlay.

## v1.3 — hierarchical priors

- Joint posterior across markets.
- Data-sparse markets (AU, JP) borrow from EU5/NA peers.

## v1.4 — parked for later

- Autonomous skeleton switching.
- Self-diagnosis of model drift.

**Dates deliberately omitted.** Sequencing only.
