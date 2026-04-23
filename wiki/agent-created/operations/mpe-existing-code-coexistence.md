# MPE Coexistence Audit — Existing Prediction Code

**Task**: Phase 0 Task 0.5 — audit existing `shared/tools/prediction/` code to confirm safe coexistence with new `mpe_*` modules.
**Date**: 2026-04-22
**Owner**: Richard Williams
**Purpose**: Document that adding the MPE engine does not break the WBR pipeline or any other existing tool.

## Existing prediction stack (reads and uses)

| File | Purpose | Consumers |
|---|---|---|
| `core.py` | `BayesianCore` — posterior update primitives | `bayesian_projector.py`, `engine.py` |
| `calibrator.py` | `Calibrator` — scoring + confidence adjustment | `engine.py`, `autonomy.py` |
| `ptypes.py` | Shared dataclasses (PriorState, PosteriorState, SegmentForecast, MarketProjection, PipelineResult, ScoringResult) | `wbr_pipeline.py`, `bayesian_projector.py`, `engine.py`, `autonomy.py`, `backfill_forecasts.py` |
| `models.py` | `ModelRegistry` — per-market-per-metric model selection | `engine.py` |
| `parser.py` | Natural-language question parser (market codes, metric keywords) | `engine.py`, tests |
| `formatter.py` | Output formatter, banned terms, confidence English | `engine.py`, tests |
| `config.py` | `MOTHERDUCK_TOKEN`, `MOTHERDUCK_DB`, `MARKETS`, `ML` | Most scripts |
| `engine.py` | `PredictionEngine` — routes natural-language questions → models → inference → logged predictions | `predict.py` (CLI), tests |
| `autonomy.py` | `AutonomyTracker` — predicts outcomes on user actions | `predict.py`, tests |
| `bayesian_projector.py` | `BayesianProjector` — week-ahead forecasts from `ps.performance` with seasonal priors, seasonal-prior self-update | `wbr_pipeline.py`, `populate_forecast_tracker.py`, `backfill_forecasts.py` |
| `wbr_pipeline.py` | 7-stage WBR orchestration (Ingest → Load → Score → Project → Callout → Dive Update → Report) | Run weekly |
| `populate_forecast_tracker.py` | Populates `ps-forecast-tracker.xlsx` from BayesianProjector outputs | Run after WBR |
| `backfill_forecasts.py` | Retroactive "what would we have predicted" forecasts | Ad-hoc |
| `project.py` / `project_full.py` | Legacy predecessors to `wbr_pipeline.py` | Transitional; `wbr_pipeline.py` is canonical now |

## New modules added by MPE v1 (proposed)

| File | Purpose | Why separate from existing |
|---|---|---|
| `mpe_engine.py` | Planning projections with target modes (spend / ieccp / regs). Takes user-supplied targets, solves for remaining variables. | Different use case from BayesianProjector. BP does posterior update against recent actuals for week-ahead live forecasts; MPE does target-mode solving for planning. No overlap. |
| `mpe_fitting.py` | Recency-weighted linear regression for CPA/CPC elasticity, seasonality, YoY trends. Regional fallback logic. | Fit orchestration is planning-specific. BP consumes `ps.seasonal_priors` but doesn't fit them. |
| `mpe_uncertainty.py` | Monte Carlo sampling (200 UI / 1000 CLI) for credible intervals. | BP produces point forecasts with posterior std; MPE adds full Monte Carlo over parameter posteriors for honest CIs. |
| `mpe_anomaly.py` | 3SD + regime tag anomaly detection at refit time. | New — no equivalent in existing stack. |
| `mpe_narrative.py` | Per-market + per-region stakeholder narrative generator. | New — no equivalent. |
| `refit_market_params.py` | Quarterly refit orchestrator. Writes new parameter_versions. | New. BP's `_update_seasonal_priors()` auto-updates seasonal priors but does not refit elasticity or YoY. |
| `data_audit.py` | Phase 0 data quality audit. | New — DONE 2026-04-22. |

## Coexistence risks (and mitigations)

### Risk 1: MARKET_STRATEGY dict duplication
**Current state**: `bayesian_projector.py` has `MARKET_STRATEGY` hardcoded for all 10 markets (AU efficiency, MX ieccp_bound, JP brand_dominant, others balanced).
**Risk**: if MPE migrates these values into `ps.market_projection_params` and the two drift, week-ahead forecasts (BP) and planning projections (MPE) would report different ie%CCP targets for the same market.
**Mitigation**: Phase 1 Task 1.1 SQL seeds `ps.market_projection_params` from the existing `MARKET_STRATEGY` dict values. Add a test that asserts the two match on import. If `bayesian_projector.py` ever changes the dict, the test fails loudly.
**Alternative considered**: make BP read from `ps.market_projection_params` instead of its hardcoded dict. Rejected for v1 — that would change BP's behavior and require WBR regression testing. Post-v1.1 activity.

### Risk 2: Seasonal prior sharing (ps.seasonal_priors)
**Current state**: BP reads `ps.seasonal_priors` and writes auto-updates. Separate schema from `ps.market_projection_params`.
**Risk**: MPE's own `brand_seasonality_shape` and `nb_seasonality_shape` (fit by `mpe_fitting.py`) could diverge from the seasonal factors BP uses for week-ahead.
**Mitigation (v1)**: MPE's seasonality is Brand/NB-split; BP's is total. Different granularity. They can coexist. Document the divergence in both code headers.
**Mitigation (v1.1)**: Consolidate onto MPE's Brand/NB-split seasonality, have BP aggregate. Post-v1 activity.

### Risk 3: Shared DuckDB connection patterns
**Current state**: Each script opens its own `duckdb.connect(MOTHERDUCK_DB)`. No connection pooling.
**Risk**: None significant — MotherDuck handles concurrent connections fine.
**Mitigation**: MPE follows the same pattern. `data_audit.py` opens its own connection, releases on exit.

### Risk 4: Import cycle
**Current state**: BP imports from `core.py`, `ptypes.py`. MPE modules import from `core.py` and (proposed) `ptypes.py` — no direct import of BP.
**Risk**: None. MPE does not import BP.
**Mitigation**: Task 1.7 (mpe_engine.py) enforces "no import from bayesian_projector."

### Risk 5: WBR pipeline regression
**Current state**: `wbr_pipeline.py` calls BP end-to-end weekly. MPE adds no new calls to this flow.
**Risk**: If MPE accidentally writes to `ps.performance` or `ps.forecasts` (BP's output tables), BP's scoring stage could corrupt.
**Mitigation**: MPE writes only to new tables (`ps.market_projection_params`, `ps.parameter_validation`, `ps.parameter_anomalies`, `ps.regional_narrative_templates`, `ps.projection_scores`). Confirmed in Task 1.1 DDL. No overlap with BP's output tables.
**Verification**: After Task 1.1 schema creation, run `wbr_pipeline.py` end-to-end against test data. Confirm behavior identical to pre-MPE state.

## Vaporware reference in prior spec

The prior tasks.md referenced `mx_precise_projection.py` in Task 5 as the source of the MX elasticity curve. **This file does not exist** in the workspace. The 2026-04-22 spec rewrite removed that reference. Task 1.5 now reads "Fit MX parameters from scratch using mpe_fitting.py against ps.v_weekly / ps.performance."

Confirmed via filesystem check 2026-04-22: no file named `mx_precise_projection*.py` exists under `shared/tools/prediction/`.

## Decision

**Coexistence is safe.** v1 ships MPE as additive modules alongside the existing stack. `wbr_pipeline.py`, `bayesian_projector.py`, and all downstream consumers continue to work unchanged.

Task 1.1 includes a verification step: after schema creation and seeding, run `wbr_pipeline.py` against test data and confirm no behavior regression. This is the gating step before starting Phase 3 market fits.

Post-v1.1 activity: consolidate `MARKET_STRATEGY` into the registry and have BP read from it, eliminating the duplication risk.
