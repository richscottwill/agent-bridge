# Design Document — Market Projection Engine (MPE)

## Overview

The MPE is a three-layer system: **Parameter Layer** (DuckDB canonical source), **Engine Layer** (Python + parallel JS implementation of the projection math), and **Interface Layer** (HTML UI, Python API, CLI). The engine produces identical outputs from any interface. Parameters are refit on a documented cadence and the UI surfaces freshness automatically.

The design optimizes for three properties in tension: **rigor** (leadership-grade math that holds up to scrutiny), **portability** (works in SharePoint/Symphony/Kiro/filesystem), and **durability** (quarterly refit process that prevents parameter drift). Natural-language input is explicitly out of scope — Kiro itself is the conversation layer.

## Architecture

```
                        ┌─────────────────────────────────────┐
                        │         DUCKDB PARAMETER LAYER       │
                        │  ps.market_projection_params         │
                        │  ps.parameter_validation             │
                        │  ps.projection_scores                │
                        └───────┬─────────────────────┬───────┘
                                │                      │
                          READ  │                READ  │
                                │                      │
                 ┌──────────────▼─────────┐  ┌─────────▼──────────┐
                 │  mpe_engine.py         │  │  refit_market_     │
                 │  (pure Python, the     │  │  params.py          │
                 │   authoritative math)  │  │  (quarterly job)    │
                 └─┬────────────┬────────┘  └─────────────────────┘
                   │            │
                   │            │   EXPORT (build step)
                   │            ▼
                   │     ┌────────────────────────────────┐
                   │     │  projection-data.json          │
                   │     │  (parameters + YTD actuals +   │
                   │     │   seasonality + elasticity)    │
                   │     └──────────┬─────────────────────┘
                   │                │
                   │                │ LOADED BY
                   │                ▼
         CLI/API   │     ┌────────────────────────────────┐
                   │     │  projection.html               │
                   │     │  ┌─────────────────────────┐  │
                   │     │  │ Methodology Manifest     │  │
                   │     │  │ (agent-readable JSON)    │  │
                   │     │  └─────────────────────────┘  │
                   │     │  ┌─────────────────────────┐  │
                   │     │  │ mpe_engine.js            │  │
                   │     │  │ (ports Python math)      │  │
                   │     │  └─────────────────────────┘  │
                   │     │  ┌─────────────────────────┐  │
                   │     │  │ Sliders / Presets /      │  │
                   │     │  │ Target Modes / Charts    │  │
                   │     │  └─────────────────────────┘  │
                   │     └────────────┬───────────────────┘
                   │                  │
                   └──────────────────┤
                                      │
                                      ▼
                      ┌───────────────────────────────┐
                      │  Saved_Projections            │
                      │  shared/dashboards/data/      │
                      │  projections/{scope}/*.json   │
                      │                               │
                      │  Also pushed to SharePoint    │
                      │  Kiro-Drive/projections/      │
                      └───────────────────────────────┘
```

## Components and Interfaces

### Parameter Layer (DuckDB)

**Table: `ps.market_projection_params`**

```sql
CREATE TABLE ps.market_projection_params (
    market VARCHAR NOT NULL,
    parameter_name VARCHAR NOT NULL,
    parameter_version INTEGER NOT NULL,
    value_scalar DOUBLE,           -- for simple scalars (CCP, baseline CPA)
    value_json JSON,                -- for structured values (elasticity coefs, seasonality weights)
    refit_cadence VARCHAR NOT NULL, -- 'annual' or 'quarterly'
    last_refit_at TIMESTAMP NOT NULL,
    last_validated_at TIMESTAMP,
    validation_mape DOUBLE,
    source VARCHAR NOT NULL,        -- 'finance_negotiation', 'historical_fit', 'manual_override', 'regional_fallback'
    fitted_on_data_range VARCHAR,   -- e.g., '2024-W01 to 2026-W12'
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

**Parameter catalog per market:**

| parameter_name | storage | refit_cadence | source options |
|---|---|---|---|
| `brand_ccp` | scalar | annual | finance_negotiation, manual_override |
| `nb_ccp` | scalar | annual | finance_negotiation, manual_override |
| `brand_ccp_time_series` | json `{week_key: value}` (historical) | annual | historical_data (ieccp_tab) |
| `nb_ccp_time_series` | json `{week_key: value}` (historical) | annual | historical_data (ieccp_tab) |
| `brand_cpa_baseline` | scalar | quarterly | historical_fit |
| `nb_cpa_baseline` | scalar | quarterly | historical_fit |
| `brand_cpa_elasticity` | json `{a, b, r_squared, posterior}` for CPA = a × spend^b | quarterly | historical_fit, recency_weighted |
| `nb_cpa_elasticity` | json `{a, b, r_squared, posterior}` for CPA = a × spend^b | quarterly | historical_fit, recency_weighted, regional_fallback |
| `brand_cpc_elasticity` | json `{a, b, r_squared, posterior}` for CPC = a × spend^b | quarterly | historical_fit, recency_weighted |
| `nb_cpc_elasticity` | json `{a, b, r_squared, posterior}` for CPC = a × spend^b | quarterly | historical_fit, recency_weighted |
| `brand_seasonality_shape` | json `{week_num: {weight, posterior}}` × 52 | annual | historical_fit, recency_weighted |
| `nb_seasonality_shape` | json `{week_num: {weight, posterior}}` × 52 | annual | historical_fit, recency_weighted |
| `brand_yoy_growth` | json `{mean, std, r_squared}` | quarterly | historical_fit, recency_weighted |
| `nb_yoy_growth` | json `{mean, std, r_squared}` | quarterly | historical_fit, recency_weighted |
| `brand_cpc` | scalar | quarterly | historical_fit |
| `nb_cpc` | scalar | quarterly | historical_fit |
| `ieccp_target` | scalar | annual | finance_negotiation, manual_override |
| `ieccp_range` | json `{low, high}` | annual | finance_negotiation, manual_override |
| `ieccp_target_time_series` | json `{week_key: target}` | annual | finance_negotiation |
| `supported_target_modes` | json `["spend", "ieccp", "regs"]` subset | annual | manual_override |
| `narrative_template` | json `{prose_template, sensitivity_language, so_what_framing}` | annual | manual_override |
| `regime_change_breakpoints` | json `[{week_key, reason}]` | quarterly | manual_override, detected |

**Table: `ps.parameter_validation`** — one row per (market, parameter_name, parameter_version, validation_run_at) with holdout MAPE and validation sample range.

**Table: `ps.parameter_anomalies`** — one row per flagged anomaly: market, parameter_name, from_version, to_version, delta_pct, std_dev_distance, anomaly_category ('investigate' | 'expected-regime-change' | 'approved-by-reviewer'), reviewer, review_notes, resolved_at.

**Table: `ps.regional_narrative_templates`** — per-region (NA, EU5, WW) narrative templates distinct from per-market templates, to support Requirement 14.

**Table: `ps.projection_scores`** — populated by the "Score" action when a saved projection's period closes; records actual vs projected for each KPI.

### Engine Layer

**`shared/tools/prediction/mpe_engine.py`** — single canonical implementation.

**Supporting modules:**
- `mpe_fitting.py` — recency-weighted regression routines for elasticity, CPC elasticity, seasonality, YoY growth
- `mpe_uncertainty.py` — Bayesian credible interval computation via Monte Carlo parameter sampling
- `mpe_anomaly.py` — anomaly detection on new parameter versions
- `mpe_narrative.py` — per-market and per-region narrative generation

```python
@dataclass
class ProjectionInputs:
    scope: str                     # market code OR region code
    time_period: str               # 'W{NN}' | 'M{MM}' | 'Q{N}' | 'Y{YYYY}' | 'MY{N}' for multi-year
    target_mode: str               # 'spend' | 'ieccp' | 'regs'
    target_value: float
    brand_uplift_pct: float = 0.0
    nb_uplift_pct: float = 0.0
    nb_elasticity_override: Optional[dict] = None
    brand_cpa_override: Optional[float] = None
    parameter_snapshot_at: Optional[datetime] = None
    uncertainty_samples: int = 1000  # Monte Carlo samples for Bayesian CIs
    credibility_levels: list = (0.50, 0.70, 0.90)

@dataclass
class ProjectionOutputs:
    scope: str
    time_period: str
    target_mode: str
    target_value: float
    weeks: list[dict]              # includes credible intervals per metric
    totals: dict                    # includes credible intervals
    constituent_markets: list[dict] # for regional rollups
    parameters_used: dict
    warnings: list[str]             # HIGH_EXTRAPOLATION, LOW_CONFIDENCE, HIGH_UNCERTAINTY, etc.
    credible_intervals: dict        # {metric: {"50": (lo, hi), "70": (lo, hi), "90": (lo, hi)}}
    yoy_growth_applied: dict        # for multi-year projections
    methodology_version: str
    generated_at: datetime

def project(inputs: ProjectionInputs) -> ProjectionOutputs: ...
def feasibility_check(inputs: ProjectionInputs) -> list[str]: ...
def narrative(outputs: ProjectionOutputs) -> str: ...
```

**JavaScript port: `shared/dashboards/mpe_engine.js`** — mirror implementation validated against Python via test suite.

**Test suite: `shared/tools/prediction/tests/test_mpe_parity.py`**
- 20 canonical test cases covering each market, each target_mode, each time_period
- Python produces outputs, JS produces outputs (via headless browser run), assertion that they match within 0.1%

### Interface Layer

**`shared/dashboards/projection.html`**

Structure:
```
<head>
  <script id="mpe-methodology" type="application/json">{...}</script>
  <script id="mpe-parameters" type="application/json">{...}</script>  <!-- if standalone mode -->
</head>
<body>
  <header>
    <h1>Market Projection Engine</h1>
    <div class="freshness-banner">Parameters current as of 2026-04-22 (MX)</div>
  </header>
  
  <section class="controls">
    <div class="scope-selector">...</div>
    <div class="time-period-selector">...</div>
    <div class="input-mode-tabs">
      <tab>Preset</tab><tab>Sliders</tab><tab>Target</tab>
    </div>
    <div class="input-panel">...</div>
  </section>
  
  <section class="outputs">
    <div class="summary-card">...</div>
    <div class="ieccp-gauge">...</div>
    <div class="chart-regs-spend">...</div>
    <div class="chart-brand-nb-stacked">...</div>
    <div class="constituent-markets-table">...</div>
    <div class="warnings-panel">...</div>
  </section>
  
  <section class="actions">
    <button>Save projection</button>
    <button>Copy as JSON</button>
    <button>Copy as markdown</button>
    <button>Generate narrative</button>
    <button>Score against actuals</button>
  </section>
  
  <section class="saved-projections">...</section>
</body>
```

**Methodology_Manifest example**:
```json
{
  "mpe_version": "1.0.0",
  "formulas": {
    "ieccp": "total_spend / (brand_regs × brand_ccp + nb_regs × nb_ccp)",
    "nb_cpa": "a × weekly_nb_spend^b",
    "regional_ieccp": "sum(market_spend) / sum(market_brand_regs × brand_ccp + market_nb_regs × nb_ccp)"
  },
  "output_schema": {
    "weeks": [{"wk": "int", "brand_regs": "float", ...}],
    "totals": {"brand_regs": "float", ...}
  },
  "parameters_used": { /* snapshot */ },
  "data_sources": ["ps.v_weekly", "ps.market_projection_params"]
}
```

**`shared/dashboards/serve.py` endpoints** (added):
- `POST /api/save-projection` → writes JSON to `shared/dashboards/data/projections/{scope}/{timestamp}-{slug}.json`
- `GET /api/list-projections?scope=MX` → returns list of saved projection filenames for scope
- `GET /api/load-projection?path=...` → returns the Saved_Projection JSON
- `POST /api/score-projection` → triggers scoring against actuals, writes to `ps.projection_scores`

**CLI entry point**:
```bash
python3 -m shared.tools.prediction.mpe_engine \
  --market MX \
  --period 2026-Q2 \
  --target ieCCP:75 \
  --format json
```

## Data Models

### Saved_Projection JSON schema

```json
{
  "saved_at": "2026-04-22T17:45:00Z",
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
    "brand_ccp": 97,
    "nb_ccp": 28,
    "brand_cpa_elasticity": {"a": 0.15, "b": 0.92, "r_squared": 0.87},
    "nb_cpa_elasticity": {"a": 0.02, "b": 0.937, "r_squared": 0.91},
    "brand_seasonality_shape": {...},
    "nb_seasonality_shape": {...},
    "ieccp_target": 100
  },
  "outputs": {
    "weeks": [...],
    "totals": {
      "brand_regs": 12664,
      "nb_regs": 4972,
      "total_regs": 17636,
      "brand_spend": 253287,
      "nb_spend": 772581,
      "total_spend": 1025868,
      "blended_cpa": 58.17,
      "ieccp": 75.0
    },
    "constituent_markets": null
  },
  "warnings": [],
  "methodology_version": "1.0.0",
  "mpe_version_at_save": "1.0.0",
  "narrative": "For the MX market in 2026...",
  "slug": "mx-y2026-75pct-moderate-placement"
}
```

## Error Handling

**Infeasible targets** — return a structured infeasibility response with the binding constraint identified:
```json
{
  "outcome": "INFEASIBLE",
  "binding_constraint": "nb_cpa_elasticity",
  "explanation": "Target regs of 25,000 require NB spend of $3.2M at predicted CPA $210, which exceeds the historically-observed NB spend range by 180%. Consider lower target or reviewing whether placement effects shift the elasticity curve.",
  "closest_feasible": {
    "target_mode": "regs",
    "target_value": 20500,
    "...": "..."
  }
}
```

**Stale parameters** — UI banner + output warning list + methodology manifest includes staleness metadata so downstream agents know to re-query.

**Missing parameters for a market** — engine returns a "SETUP_REQUIRED" response listing which parameters must be fit before projections are possible for that market.

**Cross-environment JSON loading** — if served standalone (no `serve.py`), the HTML embeds `projection-data.json` content into a `<script type="application/json" id="mpe-parameters">` block via a pre-deployment build step.

## Testing Strategy

### Python unit tests (`shared/tools/prediction/tests/`)
- `test_mpe_engine.py`: 50+ unit tests covering each target_mode, each market, edge cases (zero regs, extreme spend, infeasibility)
- `test_parameter_registry.py`: parameter write/read/versioning/fallback logic
- `test_regional_rollups.py`: regional math correctness against hand-computed expected values

### JS/Python parity tests (`tests/test_mpe_parity.py`)
- Canonical 20 test cases executed in both Python and JS (via headless browser)
- Outputs must match within 0.1% tolerance
- Run on every commit that touches either engine

### Validation tests (`tests/test_validation.py`)
- Every quarterly refit produces new MAPE
- Refit job fails loudly if any parameter's MAPE regresses more than 10pp

### Integration tests
- End-to-end: open HTML, run projection, save, close, reload, verify exact match
- SharePoint compatibility: upload HTML + data file, render in SharePoint preview, verify interactivity

## Deployment Architecture

### Environments
1. **Kiro dashboard** (primary) — `http://localhost:8000/projection.html`, file-write via serve.py
2. **SharePoint** — `Kiro-Drive/Artifacts/strategy/projection-engine.html` + `projection-data.json` sibling, no file-write (Copy-JSON only)
3. **Symphony** — embedded via iframe or standalone upload (same as SharePoint mode)
4. **Standalone file** — downloaded from any of the above, opens in browser, parameters embedded in page

### Build pipeline
```
refit_market_params.py       (weekly/quarterly hook)
  │
  ▼
ps.market_projection_params  (DuckDB)
  │
  ▼
export_projection_data.py    (build step)
  │
  ├─► shared/dashboards/data/projection-data.json
  │   (Kiro dashboard reads this via AJAX)
  │
  └─► shared/dashboards/projection-standalone.html
      (projection.html with data embedded; pushed to SharePoint)
```

## Design Decisions

### D1: Python is the authoritative engine, JS is a mirror
**Rationale**: Python runs headless refit jobs, integrates with wbr_pipeline.py, and produces CLI output for agent workflows. JS exists to make the HTML interactive. Parity tests prevent drift.

### D2: Parameters stored in DuckDB with versioning
**Rationale**: Enables audit (what params did we use on 4/22?), rollback if a refit breaks things, and A/B comparison of parameter sets. Simpler than git-tracked files because queryable.

### D3: SharePoint deployment uses embedded-data pattern, not live-fetch
**Rationale**: SharePoint CORS policies and auth make live-fetch unreliable. Embedding parameters in the HTML via a build step means SharePoint artifacts are self-sufficient. Tradeoff: SharePoint version is a snapshot — needs redeployment when parameters change. Acceptable given quarterly refit cadence.

### D4: Natural language input explicitly deferred to Kiro chat
**Rationale**: In-page LM would require agent runtime in the browser. Kiro chat is where that lives. UI supports slider + preset + target modes which cover 95% of use cases.

### D5: Regional rollup computes per-market then sums, never averages
**Rationale**: CCPs differ dramatically per market (MX Brand $90 NB $30, US Brand $424 NB $50, UK Brand $238 NB $60 per 2026 W1 file). Averaging CCPs for a regional blend silently mis-attributes reg counts to the wrong denominator. Sum-then-divide is the only defensible approach.

### D6: Quarterly refit is the durability spine
**Rationale**: Without this, the tool becomes a snapshot that decays. The refit job + validation + SharePoint refit report turns "we have a projection tool" into "we have a projection process."

### D7: Nine KPIs with CPC elasticity modeled (not deferred)
**Rationale**: Richard explicitly asked for Registrations + Spend + Clicks with Brand/NB split. CPC is modeled elastically (like CPA) because at high spend, bid inflation affects CPC meaningfully. Clicks = Spend / CPC(spend) flows naturally through the engine when CPC is a function of spend.

### D8: Methodology Manifest as first-class output
**Rationale**: Agent consumability is a stated requirement. Embedding a JSON manifest that declares formulas + parameters + output schema means an LLM reading the raw HTML can extract the answer without running JS. This is the difference between "human tool" and "human + agent tool."

### D9: Multi-year via recency-weighted YoY growth trend
**Rationale**: Richard has multi-year historical data and wants to use it. Recency weighting (exponential decay half-life 52 weeks) ensures recent years dominate while distant years still inform. This is more defensible than either naive CAGR (ignores recent shifts) or pure trailing-year (discards structural history). Trend is fit per-market per-segment separately from seasonality so mix effects are preserved.

### D10: Bayesian credible intervals via Monte Carlo sampling
**Rationale**: Every fitted parameter has uncertainty; combining them additively loses the nuance. Monte Carlo (1000 samples default) produces honest credibility bands. Separation into `mpe_uncertainty.py` means the approach can be upgraded (e.g., to proper MCMC) without touching the core engine. Tradeoff: sampling introduces noise; the parity test tolerance widens to 2% for CI outputs.

### D11: Anomaly detection on parameter refits, not on projections
**Rationale**: Detecting anomalies at refit time catches fit failures and regime shifts before they propagate to downstream projections. Flagging at projection time would be too late. Anomalies require human review before the new version is marked active — this is an explicit human-in-the-loop gate, not an auto-accept. Pairs with `ps.regime_changes` so documented shifts don't generate false-positive alerts.

### D12: CCP sourcing from WW dashboard and CCP check file — column U is authoritative
**Rationale**: CCPs live in the Summary tab of `shared/uploads/sheets/CCP Q1'26 check yc.xlsx`, **column U ("FINAL ALIGNED")** is the post-negotiation canonical value, not Sheet2 (which is Q1 static / pre-negotiation). Seeding task reads column U for each market×segment. AU has no CCP (efficiency strategy) — `supported_target_modes` reflects this. MX FINAL ALIGNED = $97.22 Brand / $27.59 NB (rounds to $97 / $28, matching Richard's stated negotiated values). A documented source-of-truth for CCPs prevents the "Richard swapped them in his head" error we hit in the 4/22 session — the answer is always column U.

## Open Questions

1. **Refit job frequency for elasticity curves** — quarterly is spec'd, but MX's 2025 H1 → 2026 regime shift suggests some markets may need monthly monitoring. Propose: quarterly hard refit + monthly MAPE monitoring that triggers ad-hoc refit if MAPE regresses.

2. **CPC elasticity data coverage** — CPC elasticity requires varied historical spend levels to fit. For markets that have been operating at stable spend, the CPC curve may be underfit. Propose: fall back to CPA-elasticity-derived CPC when CPC fit has r² < 0.3.

3. **Anomaly detection sensitivity tuning** — default is 3 standard deviations. MX 2025 H1 → H2 regime shift would have been a 5+ SD move on NB CPA. First few refits may produce many anomalies as we learn typical variance ranges per market. Propose: v1 logs anomalies liberally; thresholds tighten after 4 quarterly refits per market.

4. **Multi-year credible intervals compound** — uncertainty widens rapidly across years. 3-year CIs may be so wide as to be useless. Propose: emit VERY_WIDE_CI warning when 3-year 90% interval spans more than 3× central; consider capping multi-year to 2 years by default.

5. **Regime-change breakpoints** — manual documentation required for known shifts (placement launches, strategy changes). How do we prevent these from being forgotten? Propose: prompt at each refit to confirm no new breakpoints are missing; pair with `ps.project_timeline` events to surface candidates.

## Revision History

- 2026-04-22 initial draft.
- 2026-04-22 revised per Richard feedback: moved CPC elasticity, multi-year, Bayesian CIs, and anomaly detection into v1 scope; added per-market + per-region narrative templates and supported_target_modes; wired CCP sourcing to WW dashboard IECCP tab + Q1'26 check file; rigorous acceptance test that simulates the MX 4/22 back-and-forth. New requirements R11 (multi-year + YoY), R12 (Bayesian CIs), R13 (anomaly detection), R14 (per-market/region narrative + supported_target_modes), R15 (rigorous acceptance test).
