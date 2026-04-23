# Design Document — Market Projection Engine (MPE)

## Overview

The MPE is a three-layer system: **Parameter Layer** (DuckDB canonical source), **Engine Layer** (Python authoritative + JS mirror for UI interactivity), and **Interface Layer** (HTML UI, Python API, CLI). The engine produces identical outputs from any interface. Parameters are refit quarterly and the UI surfaces freshness automatically.

The design optimizes for four properties:
1. **Maintainability for a non-technical owner** (highest priority, per R0) — every component designed so a non-technical marketing manager can operate and extend the tool without debugging code.
2. **Rigor** — leadership-grade math that holds up to scrutiny.
3. **Portability** — works identically in SharePoint, Symphony, Kiro, filesystem.
4. **Durability** — quarterly refit prevents parameter drift; parity tests prevent Python/JS divergence.

Natural-language input is explicitly out of scope — Kiro itself is the conversation layer. Server-dependent frameworks (Streamlit, Reflex, Django, Flask) are rejected because they break R3 portability.

## Architecture

```
                        ┌─────────────────────────────────────┐
                        │         DUCKDB PARAMETER LAYER       │
                        │  ps.market_projection_params         │
                        │  ps.parameter_validation             │
                        │  ps.parameter_anomalies              │
                        │  ps.regional_narrative_templates     │
                        │  ps.projection_scores                │
                        │  ps.regime_changes (NEW or merged)   │
                        │  (reads: ps.v_weekly, ps.performance)│
                        └───────┬─────────────────────┬───────┘
                                │                      │
                          READ  │                READ  │
                                │                      │
                 ┌──────────────▼─────────┐  ┌─────────▼──────────┐
                 │  mpe_engine.py         │  │  refit_market_     │
                 │  mpe_fitting.py        │  │  params.py          │
                 │  mpe_uncertainty.py    │  │  mpe_anomaly.py     │
                 │  mpe_narrative.py      │  │  data_audit.py      │
                 │  (NEW, v1)             │  │  (quarterly hook)   │
                 └─┬────────────┬────────┘  └─────────────────────┘
                   │            │                 coexists with
                   │            │                 ┌────────────────┐
                   │            │                 │bayesian_       │
                   │            │                 │projector.py    │
                   │            │                 │core.py         │
                   │            │                 │calibrator.py   │
                   │            │                 │engine.py       │
                   │            │                 │wbr_pipeline.py │
                   │            │                 │(existing —     │
                   │            │                 │ week-ahead     │
                   │            │                 │ forecasts)     │
                   │            │                 └────────────────┘
                   │            │
                   │            │   EXPORT (build step)
                   │            ▼
                   │     ┌────────────────────────────────┐
                   │     │  projection-data.json          │
                   │     │  (MX/US/AU params + YTD +      │
                   │     │   seasonality + regional       │
                   │     │   fallback curves)             │
                   │     └──────────┬─────────────────────┘
                   │                │
                   │                │ LOADED BY
                   │                ▼
         CLI/API   │     ┌────────────────────────────────┐
                   │     │  projection.html               │
                   │     │  - Methodology Manifest (JSON) │
                   │     │  - mpe_engine.js + Web Worker  │
                   │     │  - Sliders / Presets / Target  │
                   │     │  - Charts / Gauge / Warnings   │
                   │     │  - "Explain this number"       │
                   │     │    tooltips + provenance modal │
                   │     └────────────┬───────────────────┘
                   │                  │
                   └──────────────────┤
                                      │
                                      ▼
                      ┌───────────────────────────────┐
                      │  Saved_Projections            │
                      │  shared/dashboards/data/      │
                      │  projections/{scope}/*.json   │
                      │  + SharePoint durability push │
                      └───────────────────────────────┘
```

## Relationship to Existing Prediction Code

The workspace already contains a Bayesian projection stack in `shared/tools/prediction/`:

| Existing file | Purpose | v1 decision |
|---|---|---|
| `bayesian_projector.py` | `BayesianProjector` class. Week-ahead forecasts for WBR pipeline. Uses posterior update against recent actuals. Contains `MARKET_STRATEGY` dict for all 10 markets. | **Keep unchanged.** Different use case (live week-ahead scoring). Migrate `MARKET_STRATEGY` values into `ps.market_projection_params` as `ieccp_target` and `supported_target_modes`. Do not re-type values. |
| `core.py` | `BayesianCore` posterior update logic. | **Keep.** Shared primitive. If `mpe_engine` needs weekly-seasonality sampling, live in `core.py`, not duplicated. |
| `engine.py` | `PredictionEngine` for natural-language question routing. | **Keep.** Different use case (NL Q&A). |
| `calibrator.py` | Prediction scoring + confidence adjustment. | **Keep.** Used by `engine.py` and `autonomy.py`. |
| `wbr_pipeline.py` | Uses `BayesianProjector` for WBR orchestration. | **No behavior regression.** v1 must not break WBR pipeline. |
| `populate_forecast_tracker.py` | Uses `BayesianProjector` for forecast tracker updates. | **No behavior regression.** |
| *(referenced but missing)* `mx_precise_projection.py` | Referenced in prior tasks.md as MX elasticity source. **Does not exist.** | **Ignore.** MX fit builds from scratch using `mpe_fitting.py` on `ps.v_weekly` / `ps.performance`. |

**v1 adds NEW files** (no overlap with existing):
- `shared/tools/prediction/mpe_engine.py` — planning projections with target modes
- `shared/tools/prediction/mpe_fitting.py` — recency-weighted linear regression + regional fallback
- `shared/tools/prediction/mpe_uncertainty.py` — Monte Carlo credible intervals
- `shared/tools/prediction/mpe_anomaly.py` — 3SD + regime-tag anomaly detection
- `shared/tools/prediction/mpe_narrative.py` — per-market/region narrative generation
- `shared/tools/prediction/refit_market_params.py` — quarterly refit orchestrator
- `shared/tools/prediction/data_audit.py` — Phase 0 data quality audit
- `shared/dashboards/mpe_engine.js` — JS mirror
- `shared/dashboards/projection.html` — portable UI

The two engines (BayesianProjector for live forecasting, mpe_engine for planning) coexist without interdependency. A task in Phase 0 (Task 0.5) audits and confirms no behavior regression.

## Components and Interfaces

### Parameter Layer (DuckDB)

**Table: `ps.market_projection_params`** (extended)

```sql
CREATE TABLE ps.market_projection_params (
    market VARCHAR NOT NULL,
    parameter_name VARCHAR NOT NULL,
    parameter_version INTEGER NOT NULL,
    value_scalar DOUBLE,
    value_json JSON,
    refit_cadence VARCHAR NOT NULL,
    last_refit_at TIMESTAMP NOT NULL,
    last_validated_at TIMESTAMP,
    validation_mape DOUBLE,
    source VARCHAR NOT NULL,
    fallback_level VARCHAR NOT NULL DEFAULT 'market_specific',
    lineage VARCHAR,
    fitted_on_data_range VARCHAR,
    notes VARCHAR,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    PRIMARY KEY (market, parameter_name, parameter_version)
);

CREATE VIEW ps.market_projection_params_current AS
SELECT * FROM ps.market_projection_params
WHERE is_active = TRUE
AND parameter_version = (
  SELECT MAX(parameter_version)
  FROM ps.market_projection_params p2
  WHERE p2.market = ps.market_projection_params.market
  AND p2.parameter_name = ps.market_projection_params.parameter_name
  AND p2.is_active = TRUE
);
```

`fallback_level` is one of: `market_specific` | `regional_fallback` | `prior_version` | `conservative_default`. Surfaced in the UI on every output.

`lineage` is a human-readable breadcrumb like "Finance CCP file column U → refit 2026-04-15 → validated against 2026 W14-W16 actuals."

**Parameter catalog per market:**

| parameter_name | storage | refit_cadence | source options | notes |
|---|---|---|---|---|
| `brand_ccp` | scalar | annual | finance_negotiation, manual_override | From column U authoritative |
| `nb_ccp` | scalar | annual | finance_negotiation, manual_override | From column U authoritative |
| `brand_ccp_time_series` | json `{week_key: value}` | annual | historical_data | From IECCP tab |
| `nb_ccp_time_series` | json `{week_key: value}` | annual | historical_data | From IECCP tab |
| `brand_cpa_baseline` | scalar | quarterly | historical_fit, regional_fallback | |
| `nb_cpa_baseline` | scalar | quarterly | historical_fit, regional_fallback | |
| `brand_cpa_elasticity` | json `{a, b, r_squared, posterior}` | quarterly | historical_fit, regional_fallback | CPA = a × spend^b |
| `nb_cpa_elasticity` | json `{a, b, r_squared, posterior}` | quarterly | historical_fit, regional_fallback | CPA = a × spend^b |
| `brand_cpc_elasticity` | json `{a, b, r_squared, posterior, source: 'fit' \| 'derived_from_cpa'}` | quarterly | historical_fit, derived_from_cpa | Per R2.11 |
| `nb_cpc_elasticity` | json `{a, b, r_squared, posterior, source: 'fit' \| 'derived_from_cpa'}` | quarterly | historical_fit, derived_from_cpa | Per R2.11 |
| `brand_seasonality_shape` | json `{week_num: {weight, posterior}}` × 52 | annual | historical_fit, regional_fallback | |
| `nb_seasonality_shape` | json `{week_num: {weight, posterior}}` × 52 | annual | historical_fit, regional_fallback | |
| `brand_yoy_growth` | json `{mean, std, r_squared}` | quarterly | historical_fit, regional_fallback | |
| `nb_yoy_growth` | json `{mean, std, r_squared}` | quarterly | historical_fit, regional_fallback | |
| `brand_cpc` | scalar | quarterly | historical_fit | Current-level CPC |
| `nb_cpc` | scalar | quarterly | historical_fit | Current-level CPC |
| `ieccp_target` | scalar | annual | finance_negotiation, manual_override | Migrated from `MARKET_STRATEGY` dict |
| `ieccp_range` | json `{low, high}` | annual | finance_negotiation, manual_override | Migrated from `MARKET_STRATEGY` |
| `ieccp_target_time_series` | json `{week_key: target}` | annual | finance_negotiation | |
| `supported_target_modes` | json `["spend", "ieccp", "regs"]` subset | annual | manual_override | Migrated from `MARKET_STRATEGY` |
| `narrative_template` | json `{prose_template, sensitivity_language, so_what_framing}` | annual | manual_override | |
| `regime_change_breakpoints` | json `[{week_key, reason, effective_from}]` | quarterly | manual_override, detected | Includes MX 2025-W27 ceiling + MX 2026-W15 NB drop (provisional) |

**Table: `ps.parameter_validation`** — one row per (market, parameter_name, parameter_version, validation_run_at) with holdout MAPE and validation sample range.

**Table: `ps.parameter_anomalies`** — one row per flagged anomaly: market, parameter_name, from_version, to_version, delta_pct, std_dev_distance, anomaly_category (`investigate` | `expected-regime-change` | `approved-by-reviewer`), reviewer, review_notes, resolved_at.

**Table: `ps.regional_narrative_templates`** — per-region (NA, EU5, WW) narrative templates distinct from per-market.

**Table: `ps.projection_scores`** — populated by the "Score" action when a saved projection's period closes.

**Table: `ps.regime_changes`** — Task 1.3 audits whether this table exists or overlaps with `ps.market_constraints_manual`. If overlap, choose one as canonical and migrate. Schema: `(market, week_key, reason, effective_from, documented_by, documented_at, is_active)`.

**Existing tables read-only by MPE**:
- `ps.v_weekly` — weekly actuals for fitting
- `ps.performance` — used by `bayesian_projector.py`, also read by `mpe_fitting.py` for market-specific fits
- `ps.seasonal_priors` — existing seasonality reference
- `ps.forecasts` — existing short-horizon forecasts (cross-check)
- `ps.market_constraints_manual` — legacy constraint table; audit for regime-change overlap

### Engine Layer

**`shared/tools/prediction/mpe_engine.py`** — authoritative Python engine.

Dataclasses:

```python
@dataclass
class ProjectionInputs:
    scope: str                     # market code OR region code
    time_period: str               # 'W{NN}' | 'M{MM}' | 'Q{N}' | 'Y{YYYY}' | 'MY1' | 'MY2'
    target_mode: str               # 'spend' | 'ieccp' | 'regs'
    target_value: float
    brand_uplift_pct: float = 0.0
    nb_uplift_pct: float = 0.0
    nb_elasticity_override: Optional[dict] = None
    brand_cpa_override: Optional[float] = None
    parameter_snapshot_at: Optional[datetime] = None
    # sample counts are LOCKED per R12: 200 UI, 1000 CLI. Not user-tunable.
    credibility_levels: tuple = (0.50, 0.70, 0.90)

@dataclass
class ProjectionOutputs:
    scope: str
    time_period: str
    target_mode: str
    target_value: float
    weeks: list[dict]              # includes credible intervals per metric
    totals: dict                    # includes credible intervals
    constituent_markets: list[dict] # for regional rollups; each has fallback_level
    parameters_used: dict           # includes fallback_level + lineage per param
    warnings: list[str]             # full taxonomy below
    credible_intervals: dict
    yoy_growth_applied: dict        # for multi-year
    fallback_level_summary: str     # overall: 'all_market_specific' | 'some_regional_fallback' | 'all_regional_fallback'
    methodology_version: str
    generated_at: datetime

def project(inputs: ProjectionInputs) -> ProjectionOutputs: ...
def feasibility_check(inputs: ProjectionInputs) -> list[str]: ...
```

**Warning taxonomy** (comprehensive):
- `HIGH_EXTRAPOLATION` — spend > 1.5× historical max
- `LOW_CONFIDENCE` — elasticity MAPE > 40%
- `SEASONALITY_DOMINATED` — < 8 weeks YTD
- `HIGH_UNCERTAINTY` — 90% CI width > 2× central
- `STALE_PARAMETERS` — any param past refit_cadence
- `SETUP_REQUIRED` — missing params block projection
- `LOW_CONFIDENCE_MULTI_YEAR` — < 104 weeks of data for MY
- `VERY_WIDE_CI` — 2-year 90% CI > 3× central
- `DATA_LIMITED` — Fallback_Market active
- `REGIONAL_FALLBACK` — regional curve applied
- `MAINTENANCE_MODE` — refit in progress
- `CPC_DERIVED_FROM_CPA` — CPC elasticity r² < 0.3, fallback to CPA-derived

**Supporting modules**:

`mpe_fitting.py` — recency-weighted linear regression (exponential decay, half-life 52 weeks configurable). Regional fallback logic: if market has < 80 clean weeks OR r² < 0.35, fall back to NA / EU5 regional average. CPC elasticity: fit when r² ≥ 0.3, else derive from CPA. Heavy file header explains "why / how to maintain / what happens on failure" in plain English.

`mpe_uncertainty.py` — Monte Carlo sampling. **200 samples UI, 1000 CLI, hard-coded.** Web Worker wrapper so UI thread never blocks. Documents expected asymmetry (wider on upside due to elasticity posterior skew).

`mpe_anomaly.py` — 3SD + regime tag. Window: last 4 quarterly refits. Respects `ps.regime_changes` to classify as `expected-regime-change` vs `investigate`. Testable in isolation with synthetic anomalies.

`mpe_narrative.py` — per-market + per-region templates. Follows richard-writing-style. No em-dashes. Data-forward. Explicit "so what." Fallback_Market narratives state the fallback explicitly.

`data_audit.py` — Phase 0 gate. Produces per-market report: clean weeks after regime filters, spend range for elasticity, % missing CCP weeks, recommended fallback level. Owner-readable output, no code to interpret.

`refit_market_params.py` — quarterly refit orchestrator. For each Fully_Fit_Market: refit quarterly params, compute MAPE on 12-week holdout, run anomaly detection, write new parameter_version with `is_active=false` for anomaly-flagged params, emit refit report. Prompts owner to confirm regime changes since last quarter.

### JavaScript Mirror

**`shared/dashboards/mpe_engine.js`** mirrors the Python engine.

Parity tolerance: **0.1% for deterministic outputs, 2% for Monte Carlo CI outputs**. The 0.1% cross-ecosystem float parity expectation for deterministic math is achievable; stochastic output parity is not and pretending otherwise produces endless false-failure cycles.

Monte Carlo sampling runs in a Web Worker so UI recompute stays under 150 ms median (R2.12). Main thread handles parameter sampling setup and interval computation; worker runs the sample loop.

### Interface Layer

**`shared/dashboards/projection.html`** structure:

```
<head>
  <script id="mpe-methodology" type="application/json">{...}</script>
  <script id="mpe-parameters" type="application/json">{...}</script>  <!-- standalone mode only -->
</head>
<body>
  <header>
    <h1>Market Projection Engine</h1>
    <div class="freshness-banner">Parameters current as of 2026-04-22 (MX, US, AU)</div>
    <div class="fallback-summary-banner">
      MX US AU: market-specific fits | CA UK DE FR IT ES JP: regional fallback (wider CIs)
    </div>
  </header>

  <section class="controls">
    <div class="scope-selector">
      <!-- Fully_Fit_Markets highlighted; Fallback_Markets show data-limited badge -->
    </div>
    <div class="time-period-selector"><!-- W/M/Q/Y/MY1/MY2 --></div>
    <div class="input-mode-tabs">
      <tab>Preset</tab><tab>Sliders</tab><tab>Target</tab>
    </div>
    <div class="input-panel">
      <!-- supported_target_modes honored; AU hides ieCCP -->
    </div>
  </section>

  <section class="outputs">
    <div class="summary-card"><!-- totals with CI ranges --></div>
    <div class="ieccp-gauge"><!-- current vs target --></div>
    <div class="chart-regs-spend"><!-- line + CI band --></div>
    <div class="chart-brand-nb-stacked"></div>
    <div class="constituent-markets-table"><!-- regional only, per-market badges --></div>
    <div class="warnings-panel"><!-- warning taxonomy --></div>
    <div class="narrative-block"><!-- generated on demand --></div>
    <div class="provenance-modal"><!-- click any KPI for full lineage --></div>
  </section>

  <section class="actions">
    <button>Save projection</button>
    <button>Copy as JSON</button>
    <button>Copy as markdown</button>
    <button>Generate narrative</button>
    <button>Score against actuals</button>
  </section>

  <section class="saved-projections"></section>
</body>
```

**"Explain this number" tooltips** attached to every KPI. Each states: formula, data range, fallback status, and a plain-English "what to tell Lorena" line. Examples in `shared/wiki/agent-created/operations/mpe-explain-this-number-examples.md` (Task 2.9).

**Methodology Manifest** example:
```json
{
  "mpe_version": "1.0.0",
  "v1_scope": {
    "fully_fit_markets": ["MX", "US", "AU"],
    "fallback_markets": ["CA", "UK", "DE", "FR", "IT", "ES", "JP"],
    "regions": ["NA", "EU5", "WW"],
    "multi_year_cap": 2
  },
  "formulas": {
    "ieccp": "total_spend / (brand_regs × brand_ccp + nb_regs × nb_ccp) × 100",
    "cpa_elasticity": "CPA = a × weekly_spend^b",
    "cpc_elasticity_when_fit": "CPC = a × weekly_spend^b (r² ≥ 0.3)",
    "cpc_elasticity_when_derived": "CPC = CPA × CVR (r² < 0.3, warning: CPC_DERIVED_FROM_CPA)",
    "regional_ieccp": "sum(market_spend) / sum(market_brand_regs × brand_ccp + market_nb_regs × nb_ccp) × 100"
  },
  "output_schema": { /* ... */ },
  "parameters_used": { /* snapshot */ },
  "data_sources": ["ps.v_weekly", "ps.performance", "ps.market_projection_params"]
}
```

**`shared/dashboards/serve.py` endpoints** (added):
- `POST /api/save-projection`
- `GET /api/list-projections?scope=MX`
- `GET /api/load-projection?path=...`
- `POST /api/score-projection`

**CLI entry point**:
```bash
python3 -m shared.tools.prediction.mpe_engine \
  --market MX --period 2026-Q2 --target ieCCP:75 --format json
python3 -m shared.tools.prediction.mpe_engine \
  --region EU5 --period MY2 --target spend:5000000 --format markdown
```

## Kiro Integration (First Class)

Kiro hooks are the primary automation spine. They turn "owner needs to remember to refit quarterly" into "owner runs one hook."

**Steering file: `.kiro/steering/mpe-low-maintenance.md`**

Enforces non-technical-owner language, forbids complex ML, caps v1 scope. Every Kiro-generated output against this spec passes through this steering. Full content in Task 0.3.

**Hooks: `.kiro/hooks/`**

1. `mpe-refit.kiro.hook` — manual trigger, runs `data_audit.py` then `refit_market_params.py` then anomaly check. Produces owner-readable markdown report. Blocks activation of anomaly-flagged parameters until owner approves.
2. `mpe-parity.kiro.hook` — fires on save of `mpe_engine.py` or `mpe_engine.js`. Runs parity tests. Blocks commit on failure with owner-readable explanation.
3. `mpe-acceptance-core.kiro.hook` — manual trigger or pre-commit. Runs core automated acceptance for MX/US/AU + regional rollups. Logs report to `shared/dashboards/data/acceptance-test-reports/`.
4. `mpe-demo-prep.kiro.hook` — pre-demo. Builds SharePoint standalone, prepares MX 4/22 manual checklist, generates 90-second demo script.

Hook file schemas follow the Kiro hook schema in the environment rules.

## Data Models

### Saved_Projection JSON schema

```json
{
  "saved_at": "2026-04-22T17:45:00-07:00",
  "saved_by": "richard",
  "scope": "MX",
  "time_period": "Y2026",
  "target_mode": "ieccp",
  "target_value": 75.0,
  "inputs": {
    "brand_uplift_pct": 15.0,
    "nb_uplift_pct": 0.0
  },
  "parameters_snapshot": {
    "brand_ccp": {"value": 97.22, "fallback_level": "market_specific", "lineage": "Finance col U 2026-Q1"},
    "nb_ccp": {"value": 27.59, "fallback_level": "market_specific", "lineage": "Finance col U 2026-Q1"},
    "brand_cpa_elasticity": {"a": 0.15, "b": 0.92, "r_squared": 0.87, "fallback_level": "market_specific"},
    "nb_cpa_elasticity": {"a": 0.02, "b": 0.937, "r_squared": 0.91, "fallback_level": "market_specific"},
    "nb_cpc_elasticity": {"source": "derived_from_cpa", "r_squared_original_fit": 0.22},
    "regime_breakpoints": ["2025-W27 ieccp_ceiling", "2026-W15 nb_drop_provisional"]
  },
  "outputs": {
    "weeks": [ /* week-by-week with CI per metric */ ],
    "totals": {
      "brand_regs": 12664,
      "nb_regs": 4972,
      "total_regs": 17636,
      "brand_spend": 253287,
      "nb_spend": 772581,
      "total_spend": 1025868,
      "blended_cpa": 58.17,
      "ieccp": 75.0,
      "credible_intervals": {
        "total_regs": {"50": [17100, 18200], "70": [16600, 18700], "90": [15800, 19500]}
      }
    },
    "constituent_markets": null
  },
  "warnings": ["CPC_DERIVED_FROM_CPA"],
  "fallback_level_summary": "all_market_specific",
  "methodology_version": "1.0.0",
  "mpe_version_at_save": "1.0.0",
  "narrative": "For the MX market in 2026...",
  "slug": "mx-y2026-75pct-moderate-placement"
}
```

## Error Handling

**Infeasible targets**:
```json
{
  "outcome": "INFEASIBLE",
  "binding_constraint": "nb_cpa_elasticity",
  "explanation": "Target regs of 25,000 require NB spend of $3.2M at predicted CPA $210, which exceeds the historically-observed NB spend range by 180%. Consider lower target or review whether placement effects shift the elasticity curve.",
  "closest_feasible": {
    "target_mode": "regs",
    "target_value": 20500,
    "ieccp": 78.2,
    "total_spend": 2100000
  }
}
```

**Stale parameters**: UI banner + output warning list + methodology manifest staleness metadata.

**Missing parameters**: engine returns `SETUP_REQUIRED` response listing which parameters must be fit.

**Cross-environment JSON loading**: if served standalone (no `serve.py`), HTML embeds `projection-data.json` content into `<script id="mpe-parameters" type="application/json">` via a pre-deployment build step. No CORS exposure.

## Testing Strategy

### Python unit tests (`shared/tools/prediction/tests/`)
- `test_mpe_engine.py` — 40+ unit tests covering each target_mode, each Fully_Fit_Market, edge cases (zero regs, extreme spend, infeasibility, regime breakpoints).
- `test_mpe_fitting.py` — recency-weighted fit, regional fallback trigger, CPC r² branch.
- `test_mpe_uncertainty.py` — MC sample count lock, band asymmetry.
- `test_mpe_anomaly.py` — synthetic anomalies (true-positive, false-positive, regime-tagged).
- `test_parameter_registry.py` — write / read / versioning / fallback_level.
- `test_regional_rollups.py` — sum-then-divide correctness against hand-computed expected.

### JS/Python parity tests (`tests/test_mpe_parity.py`)
- 30 canonical test cases in `shared/tools/prediction/tests/parity_cases.json`.
- Python runs via `mpe_engine.py`. JS runs via playwright/puppeteer headless.
- Tolerance: 0.1% deterministic, 2% Monte Carlo CI.
- Runs on every change to engine files via `mpe-parity.kiro.hook`.

### Acceptance tests (`tests/test_acceptance.py`)
- Core suite: MX, US, AU, NA, EU5, WW. Steps (a)-(m) per R15.
- Run time: < 15 minutes full, < 2 minutes single-market.
- Pre-commit gate for engine changes.
- MX 2026-04-22 simulation is a 10-step **manual** checklist documented at `shared/wiki/agent-created/operations/mpe-mx-422-simulation.md`. Owner runs live in demo.

### Integration tests
- End-to-end: open HTML, run projection, save, close, reload, verify exact match.
- SharePoint compatibility: upload HTML + data file, render in SharePoint preview, verify interactivity.
- Symphony compatibility: iframe embed, verify functionality.
- Standalone filesystem: open from disk, no outbound calls except Chart.js CDN.

## Deployment Architecture

### Environments
1. **Kiro dashboard** (primary) — `http://localhost:8000/projection.html`. File-write via `serve.py`.
2. **SharePoint** — `Kiro-Drive/Artifacts/strategy/projection-engine.html` + companion JSON. No file-write (Copy-JSON only).
3. **Symphony** — iframe or standalone upload (same as SharePoint mode).
4. **Standalone file** — opens from disk, parameters embedded.

### Build pipeline
```
refit_market_params.py  (quarterly hook)
  │
  ▼
ps.market_projection_params  (DuckDB)
  │
  ▼
export_projection_data.py  (build step)
  │
  ├─► shared/dashboards/data/projection-data.json  (Kiro dashboard reads via fetch)
  │
  └─► shared/dashboards/projection-standalone.html  (data embedded; SharePoint push)
```

Export size target: under 500 KB for the JSON. Parameters for 3 full markets + 7 fallback pointers + 52-week seasonality + YTD actuals is well under this.

## Design Decisions

### D1: Python is authoritative, JS is a mirror
Python runs headless refit jobs, integrates with sibling tools, produces CLI output for agent workflows. JS makes the HTML interactive. Parity tests prevent drift. **Streamlit / Reflex / Django / Flask are explicitly rejected** because they break R3 portability (SharePoint deployment, standalone filesystem render).

### D2: Parameters stored in DuckDB with versioning
Enables audit ("what params did we use on 4/22?"), rollback, and A/B comparison. Simpler than git-tracked files because queryable.

### D3: SharePoint deployment uses embedded-data pattern, not live-fetch
SharePoint CORS and auth make live-fetch unreliable. Embedding parameters in the HTML via a build step means SharePoint artifacts are self-sufficient. Tradeoff: SharePoint version is a snapshot. Acceptable given quarterly refit cadence.

### D4: Natural language input explicitly deferred to Kiro chat
In-page LM would require agent runtime in the browser. Kiro chat is where that lives.

### D5: Regional rollup computes per-market then sums, never averages
CCPs differ dramatically (MX Brand $97 NB $28 vs US Brand $412 NB $49). Averaging CCPs silently mis-attributes reg counts to the wrong denominator. Sum-then-divide is the only defensible approach.

### D6: Quarterly refit is the durability spine
Without this, the tool becomes a snapshot that decays. Refit job + validation + SharePoint refit report turns "we have a projection tool" into "we have a projection process."

### D7: Nine KPIs with CPC elasticity via r² ≥ 0.3 branch
R2.11 codifies the decision. When CPC fit r² ≥ 0.3, fit directly. When r² < 0.3, derive from CPA with `CPC_DERIVED_FROM_CPA` warning. Keeps CPC elasticity as a first-class output without forcing a bad fit.

### D8: Methodology Manifest as first-class output
Agent consumability is a stated requirement. Embedding a JSON manifest that declares formulas + parameters + output schema means an LLM reading the raw HTML can extract the answer without running JS. Difference between "human tool" and "human + agent tool."

### D9: Multi-year via recency-weighted YoY growth trend, capped at 2 years
Multi-year is explicitly capped at 2 years in v1 (R11). 3-year was in the original spec but compounded uncertainty produces bands too wide to be useful. Revisit in v1.1 once 2-year intervals are observed in practice.

### D10: Bayesian credible intervals via Monte Carlo, locked sample counts
200 UI / 1000 CLI, hard-coded. Separation into `mpe_uncertainty.py` means the approach can be upgraded without touching core. Tradeoff: sampling noise inherent; parity widens to 2% for CI outputs.

### D11: Anomaly detection at refit time, 3SD + regime tag only
Detecting at refit catches fit failures and regime shifts before they propagate. Flagging at projection time would be too late. v1 uses 3SD + regime tag only — no ML. Thresholds tighten after 4 quarterly refits per market.

### D12: CCP sourcing from column U authoritative
Column U ("FINAL ALIGNED") in `CCP Q1'26 check yc.xlsx` is the post-negotiation canonical value. Sheet2 is pre-negotiation static — do not read. This prevents the "Richard swapped CCPs in his head" error from 2026-04-22.

### D13: Hill-function guardrail for extrapolation, not elasticity fit
Gemini investigation flagged that log-linear extrapolation can project impossible growth. v1 addresses this as a **guardrail**, not a fit. When requested spend exceeds 1.5× historical max, the engine triggers HIGH_EXTRAPOLATION and applies a Hill-function ceiling estimate with a visible "extrapolation region" banner. Full Hill-function fit is deferred to v1.1 if leadership requests.

### D14: Phase 0 `data_audit.py` is a mandatory gate
Before any fitting starts, `data_audit.py` runs for all 10 markets producing a plain-English report. Output tells the owner which markets can support full fits and which must use regional fallback. **Validated 2026-04-22: 9 of 10 markets support full fits (102-168 clean weeks); AU has 29 clean weeks so needs SH-hybrid handling.** Prevents the "AU has 40 clean weeks, the fit is garbage, why is the model broken" surprise later.

### D15: Coexistence with existing Bayesian projection stack
`bayesian_projector.py` serves `wbr_pipeline.py` for live week-ahead forecasting. `mpe_engine.py` serves planning projections with target modes. Different use cases. v1 does not rip-and-replace. Task 0.5 audits for behavior regression risk. `MARKET_STRATEGY` dict values from `bayesian_projector.py` migrate to `ps.market_projection_params` (do not re-type).

### D16: Southern Hemisphere handling for AU (hybrid per-week seasonality)
AU is the only market below the equator in v1 scope. Its seasonality is inverted (AU winter ≠ NH winter) so reusing WW or EU5 seasonality directly would systematically mis-forecast every AU quarter. The AU-specific fix: **hybrid per-week seasonality** built from AU-real weeks where available (≥ 2 usable weeks per calendar week number after regime exclusion) plus WW seasonality shifted 26 weeks for the gaps. Each week's weight carries a `provenance` sub-field (`au_actual` or `nh_shifted_w{N}`) so the narrative can state exactly which weeks are real vs shifted. As AU accumulates data, NH-shifted weeks are replaced at each quarterly refit. AU elasticity uses WW regional curve as base with level shift. `fallback_level = 'southern_hemisphere_hybrid'` for seasonality until AU has 80 clean weeks. Rationale: honest about data limitation, improves quarter-over-quarter, demo-able. Rejected alternatives: (a) shift NH directly — ignores AU-real signal; (b) pure regional fallback — discards the ~30 weeks of AU-real data we have; (c) custom hardcoded SH retail template — not data-driven, owner cannot verify.

### D17: Regime classification (structural vs transient vs excluded)
Every row in `ps.regime_changes` must be classified. The schema already has `is_structural_baseline` (BOOLEAN) and `half_life_weeks` (INTEGER) to express this. v1 decision tree:
- **Long-term structural** (`is_structural_baseline = TRUE`, `active = TRUE`): market permanently moved. Include post-event data as the new baseline. Example: US 2025-09-29 OCI 100%, MX 2025-08-28 Polaris INTL launch, DE 2025-10-01 OCI 100%, AU 2026-01-01 Adobe bid strategies, IT 2026-02-18 PAM pause.
- **Short-term transient** (`is_structural_baseline = FALSE`, `half_life_weeks` set, `active = TRUE`): one-time or recurring event; effect decays. Include in fit but decay the adjustment. Example: MX Semana Santa (half_life=1, annual recurring), US 2026-03-16 promo CPC spike (half_life=2), WW 2026-01-30 MCS redirect (half_life=1), MX 2026-W15 NB drop (half_life=2, confidence=0.5 pending Yun-Kang resolution).
- **Excluded from fit** (`active = FALSE`): contaminated period, partial phase superseded by later event, or observation note. Keep the record for audit, do not use in fitting. Example: AU 2025-06-10 PS launch (no prior baseline), AU 2026-02-01 stabilization (merged into Jan), UK 2025-06-27 OCI 25% (superseded by 7/01 100%).
- **Special short-term-excluded** (`is_structural_baseline = FALSE`, `half_life_weeks = 0`, `active = TRUE`): the event occurred but was reverted or failed. Exclude the affected weeks from the fit window but preserve the record. Example: AU 2026-03-26 Polaris LP reverted 4/13 (exclude 2026-W13-W15).

Classification reviewed at every quarterly refit. Owner confirms with a prompt. AU classifications locked as of 2026-04-22 per R14.15.

## Open Questions

1. **Refit cadence for elasticity** — quarterly is spec'd, but MX 2025 H1→2026 regime shift and the 2026-W15 NB drop suggest some markets may need monthly monitoring. Propose: quarterly hard refit + monthly MAPE monitoring that triggers ad-hoc refit if MAPE regresses >5pp.

2. **CPC elasticity r² threshold** — R2.11 sets 0.3. Validate on MX/US/AU fits in Task 1.5/3.1/3.2 and tune if needed. Document in refit report.

3. **Anomaly detection sensitivity tuning** — default 3SD. First 4 quarterly refits per market will be noisy as the trailing distribution builds. v1 logs anomalies liberally; thresholds tighten after observation.

4. **2-year credible intervals compound** — uncertainty widens. R11.8 emits VERY_WIDE_CI when 2-year 90% CI > 3× central. If this fires often, cap at 1-year in v1.1 and hold 2-year for a later version.

5. **`ps.regime_changes` vs `ps.market_constraints_manual`** — Task 1.3 audits. If overlap, choose one as canonical and migrate. Document the decision in the refit runbook.

6. **MX 2026-W15 NB drop provisional breakpoint** — added now per owner direction (do not wait for Yun-Kang investigation). Confirm at first refit. May be upgraded from "provisional" to "confirmed" or removed if the drop resolves as normal noise.

## Revision History

- 2026-04-22 initial draft.
- 2026-04-22 revised: CPC elasticity, multi-year, Bayesian CIs, anomaly detection, per-market/region narratives, rigorous acceptance test.
- 2026-04-22 **rewrite per low-maintenance framing** (Grok synthesis + self-inspection):
  - v1 scope narrowed to MX/US/AU fully fit + CA/UK/DE/FR/IT/ES/JP regional fallback
  - Multi-year capped at 2 years (was 3)
  - Monte Carlo sample counts locked (200 UI / 1000 CLI)
  - CPC elasticity uses r² ≥ 0.3 branch (option c); fallback to CPA-derived
  - MX 4/22 simulation is a manual 10-step checklist, not automated
  - MX 2026-W15 NB drop added as provisional regime breakpoint
  - Hill-function is a guardrail only (D13), not the elasticity fit
  - Coexistence with `bayesian_projector.py` stack explicit (D15)
  - Kiro hooks are first-class, not afterthoughts
  - Streamlit/Reflex/Django/Flask explicitly rejected (R16.10)
  - Added new design decisions D13, D14, D15

- 2026-04-22 **v1 scope expanded after Phase 0 data audit**:
  - All 10 markets get market-specific fits (previously MX/US/AU fully fit + 7 fallback)
  - AU uses Southern_Hemisphere_Handling per D16 — hybrid seasonality with per-week lineage
  - All regime events in `ps.regime_changes` classified per D17 (structural / transient / excluded / reverted)
  - AU regime classification locked as of 2026-04-22: bid strategies structural, Feb 2026 merged into Jan, Polaris reverted = short-term-excluded
  - MX 2026-W15 NB drop inserted into `ps.regime_changes` with confidence=0.5, half_life=2, to be reclassified at first refit based on W16+ signal
  - Removed Fully_Fit_Market / Fallback_Market glossary distinction — all markets are Fully_Fit in v1; fallback remains as safety net
  - New R14.9-R14.15 AU-specific requirements
  - New D16 (SH handling) and D17 (regime classification) design decisions
  - R16.1 reframed: no longer "don't do full fits for 7 markets" but "don't default to regional fallback when ≥ 80 clean weeks are available"
  - R16.14 new: SH handling is AU-only in v1; a future BR/ZA launch requires its own spec
