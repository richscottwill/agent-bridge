# Requirements Document

## Introduction

Paid Search budget conversations today happen with ad-hoc Python scripts, stale mental models, and CCP assumptions that live in Richard's head or buried Quip docs. The MX conversation on 2026-04-22 (run in real time through Kiro) exposed how much latent rigor exists across the data layer (`ps.v_weekly`, `ps.forecasts`, `ps.market_constraints`) but cannot be composed into a defensible answer without writing custom code each time. Every market review — MX/Lorena, AU/Alexis, US/Andrew, EU5 — re-solves the same math from scratch.

The Market Projection Engine (MPE) codifies the projection methodology into a durable, reviewable system that produces defensible forecasts. **v1 covers all 10 markets with market-specific fits (MX, US, CA, UK, DE, FR, IT, ES, JP, AU) plus regional rollups (NA, EU5, WW). AU receives Southern Hemisphere handling because it is the only market below the equator — its seasonality is inverted and its data history is short.** This scope is viable because the audit confirmed 9 of 10 markets have 102-168 clean weeks; AU's 29 usable weeks are supplemented with AU-real-where-available plus NH-shifted-for-gaps. Every design decision must respect the non-technical owner constraint.

The engine is an L3 (Team Automation) artifact intended to be showcased to team and leadership. It must work offline once deployed (SharePoint, Symphony, standalone browser) and survive a platform migration. It must be **the** answer to "what would X spend produce?" for every supported scope, every time, every stakeholder — and it must keep working without an experienced engineer's attention.

This spec defines the engine, its parameters, the projection logic, the UI, the persistence model, and the quarterly maintenance process. Concrete fits for each market are downstream tasks executed against this spec.

## Glossary

- **Market_Projection_Engine (MPE)**: The complete system — parameter registry + projection logic + UI + persistence — defined by this spec.
- **Market**: One of ten paid search markets — US, CA, UK, DE, FR, IT, ES, JP, MX, AU.
- **Fully_Fit_Market**: Every market in v1 scope — US, CA, UK, DE, FR, IT, ES, JP, MX, AU — gets a market-specific fit. AU additionally uses Southern_Hemisphere_Handling because it is the only market below the equator (see R14 AU-specific requirement).
- **Southern_Hemisphere_Handling**: AU-specific seasonality treatment. AU's 52-week seasonality is built from AU-real data where available (clean subset of 2025-W24 onward) plus global (WW) seasonality shifted 26 weeks to account for inverted seasons. Per-week `lineage` field records whether the weight came from AU-real or NH-shifted. As AU data accumulates, the NH-shifted weeks get replaced at each quarterly refit.
- **Regime_Classification**: Every event in `ps.regime_changes` is classified as one of: long-term structural (`is_structural_baseline = TRUE`, new baseline for fitting), short-term transient (`half_life_weeks` set, decay the adjustment), or exclude-from-fit (`active = FALSE`, contaminated period). Classification is reviewed at every quarterly refit.
- **Region**: A derived rollup of markets — NA (US + CA), EU5 (UK + DE + FR + IT + ES), WW (all ten markets).
- **Scope**: A selection of one market OR one region for a projection run.
- **Time_Period**: One of five projection horizons — Week (single ISO week), Month (single calendar month), Quarter (Q1/Q2/Q3/Q4 of target year), Year (full fiscal year), Multi_Year (1-2 future fiscal years; 3-year is deferred to v1.1).
- **Projection_Run**: A single invocation of the MPE for one Scope × Time_Period × Input_Set producing a complete KPI output matrix.
- **KPI**: One of nine tracked metrics — Brand_Registrations, NB_Registrations, Brand_Spend, NB_Spend, Brand_Clicks, NB_Clicks, Brand_CPA (derived), NB_CPA (derived), ie%CCP (derived). Both CPAs and CPCs are modeled via elasticity curves so that at the margin, higher Spend produces higher CPA (diminishing returns on reg output) and higher CPC (bid inflation on click volume). CPC elasticity is fit when sufficient data supports it (see R2); otherwise derived from CPA with a fallback warning.
- **Segment**: Brand or NB (Nonbrand). Every KPI except ie%CCP has a Brand and NB variant. Regional rollups sum segments across constituent markets.
- **CCP**: Cost-per-Customer-Payback — a per-market, per-segment dollar value set by finance/leadership negotiation. Sourced from the Summary tab of `shared/uploads/sheets/CCP Q1'26 check yc.xlsx`, **column U ("FINAL ALIGNED")**, which is the post-negotiation canonical value. MX has Brand CCP $97.22 / NB CCP $27.59 per column U (rounds to $97 / $28). CCPs vary over time (see `ieccp_time_series`) and the engine SHALL respect the CCP in effect at each projection-target week.
- **ie%CCP**: `total_spend / (brand_regs × Brand_CCP + nb_regs × NB_CCP)` × 100. Expressed as a percentage. Target ceiling varies by market (MX 100%, JP 30-50%, US/CA/UK/DE/FR/IT/ES 50-65%, AU not tracked — efficiency strategy).
- **Elasticity_Curve**: Relationship between weekly Spend and weekly CPA or CPC per segment per market, fit from historical data. Used to predict CPA/CPC changes when Spend changes.
- **Recency_Weighted_Fit**: Parameter-fitting technique where historical data points are weighted by recency (exponential decay, half-life 52 weeks default). Enables the model to reflect recent regime shifts without discarding multi-year seasonality signal.
- **YoY_Growth_Trend**: Per-market multiplicative factor capturing structural year-over-year growth (separate from seasonality). Fit from 2-4 years of data with recency weighting. Drives multi-year projection and informs single-year full-year projections.
- **Bayesian_Credible_Interval**: Probabilistic uncertainty band around a projection output, derived from posterior distributions over engine parameters via Monte Carlo sampling. Distinct from MAPE-overlay error bands.
- **Anomaly_Detection**: Automated check during parameter refit that flags any parameter whose new value differs from the prior value by more than 3 standard deviations from the trailing distribution. Fires for historical-fit parameters, not negotiated ones (CCPs).
- **Seasonality_Shape**: 52-week normalized distribution of Registrations per segment per market. Used to distribute annual projections across weeks.
- **Parameter_Set**: Complete collection of per-market parameters required to produce a projection for that market. Stored in DuckDB `ps.market_projection_params`.
- **Regional_Fallback_Curve**: Pre-computed regional average elasticity curve (NA or EU5) applied to Fallback_Markets that lack sufficient market-specific data. Surfaces a data-limited banner whenever applied.
- **Target_Mode**: One of three constraint modes — Spend_Target, ieCCP_Target, Regs_Target. Each market declares which modes it supports via `supported_target_modes` (AU excludes ieccp; others support all three).
- **Scenario_Preset**: Named bundle of projection inputs applied with one click. Per-market, editable.
- **Saved_Projection**: Persisted Projection_Run — inputs, parameters-used, outputs, timestamp, author — stored as JSON for later recall, comparison, or handoff.
- **Parameter_Freshness**: Per-parameter timestamps driving staleness warnings in the UI.
- **Refit_Cadence**: Required frequency of parameter recomputation — Annual (CCPs, seasonality shape), Quarterly (CPA/CPC elasticity, baselines, YoY growth).
- **Validation_MAPE**: Mean Absolute Percentage Error computed against a holdout period (typically the most recent 12 weeks) when a parameter is refit.
- **Methodology_Manifest**: Machine-readable JSON block embedded in the HTML UI declaring every parameter used, every formula applied, and the expected output shape.
- **Portable_Artifact**: An HTML file that renders identically whether served from Kiro's `serve.py`, uploaded to SharePoint, embedded in Symphony, or opened from the filesystem. No external dependencies at render time beyond one CDN call for Chart.js.
- **Owner**: The non-technical employee who maintains the MPE long-term. Used throughout this spec to keep the owner-maintenance constraint in view.


## Requirements

### Requirement 0: Maintainability for Non-Technical Owner (Highest Priority)

**User Story:** As Richard, a non-technical marketing manager who will own and maintain this tool alone after demo, I want every design decision to prioritize my ability to operate and extend the tool without writing or debugging code, so that the MPE keeps working for years without needing an experienced engineer's attention.

#### Acceptance Criteria

1. THE MPE SHALL be designed so a non-technical owner can understand every output in under 30 seconds via tooltips, lineage badges, and plain-English warnings.
2. THE MPE SHALL provide Kiro hooks for every recurring maintenance task (refit, parity check, acceptance test, demo prep) invocable via a single command with no code edits required.
3. THE MPE SHALL include an owner runbook covering daily use, weekly check, quarterly refit, "something looks wrong" diagnostic, rollback, and "how to add a new market." Every step SHALL be executable by the owner without reading code.
4. WHERE a component requires ongoing engineering effort to maintain (complex solvers, bespoke ML models, heavy CSS animation, framework migrations), THE MPE SHALL prefer a simpler, fallback-heavy design AND document the trade-off.
5. THE MPE SHALL allow a non-technical owner to roll back a bad parameter version in under 5 minutes with zero data loss.
6. THE MPE SHALL allow a non-technical owner to extend to one new market in 4-6 hours the first time (settling to 2 hours after 2-3 market additions) using templates and `data_audit.py`.
7. WHERE automation or a hook can replace an ongoing manual step, THE MPE SHALL prefer the automation.

### Requirement 1: Parameter registry as canonical source of truth

**User Story:** As Richard, I want every market's projection parameters stored in one queryable table with ownership, freshness, and lineage metadata, so that I know the math is grounded in current reality and cannot drift out of sync with finance or historical fits.

#### Acceptance Criteria

1. THE MPE SHALL maintain a DuckDB table `ps.market_projection_params` with one row per (market, parameter_name, parameter_version) tuple.
2. THE parameter registry SHALL include the following parameter families per market: Brand_CCP, NB_CCP, Brand_CPA_baseline, Brand_CPA_elasticity, NB_CPA_baseline, NB_CPA_elasticity, Brand_CPC_elasticity, NB_CPC_elasticity, Brand_seasonality_shape, NB_seasonality_shape, Brand_CPC, NB_CPC, Brand_YoY_growth, NB_YoY_growth, ie%CCP_target, ie%CCP_range, supported_target_modes, narrative_template, regime_change_breakpoints.
3. WHEN a parameter is updated, THE MPE SHALL write a new row with incremented `parameter_version` and timestamp `last_refit_at`, preserving prior rows for audit.
4. THE parameter registry SHALL include a `refit_cadence` column declaring "annual" or "quarterly."
5. THE parameter registry SHALL include a `source` column documenting where the value came from (finance_negotiation, historical_fit, manual_override, regional_fallback).
6. THE parameter registry SHALL include a `fallback_level` column taking one of: `market_specific`, `regional_fallback`, `prior_version`, `conservative_default`. This is surfaced on every UI output.
7. THE parameter registry SHALL include a `lineage` column containing a human-readable breadcrumb (e.g., "Finance CCP file column U → refit 2026-04-15 → validated against W14-W16 actuals").
8. IF a parameter's `last_refit_at` is older than its `refit_cadence` maximum (365 days for annual, 120 days for quarterly), THEN THE MPE SHALL surface the parameter as stale in any UI or projection run consuming it.
9. WHERE a market has insufficient historical data for a full market-specific fit (under 80 clean weeks OR r² below 0.35 on the elasticity fit), THE MPE SHALL fall back to the regional average curve (NA or EU5) AND declare the fallback explicitly with `fallback_level = 'regional_fallback'` AND show a data-limited banner in the UI.

### Requirement 2: Nine-KPI projection engine with v1 scope boundary

**User Story:** As Richard or any team member, I want to produce projections for Registrations, Spend, and Clicks — split Brand vs NB — plus derived CPAs and ie%CCP, for any time period and any supported market or region, so that every stakeholder conversation works from the same numbers.

#### Acceptance Criteria

1. THE projection engine SHALL accept inputs: scope (market or region), time_period, target_mode, target_value, optional uplift modifiers per segment, optional parameter overrides.
2. THE projection engine SHALL produce output: week-by-week Brand_Registrations, NB_Registrations, Brand_Spend, NB_Spend, Brand_Clicks, NB_Clicks, plus derived Brand_CPA, NB_CPA, blended_CPA, ie%CCP; plus aggregated totals for the selected time_period.
3. THE projection engine SHALL lock YTD actual values for weeks already completed. Current-period actuals are never overwritten by projections.
4. WHEN target_mode is Spend_Target, THE engine SHALL distribute spend across weeks using Seasonality_Shape, compute per-week segment CPAs via Elasticity_Curves, and derive Registrations and Clicks.
5. WHEN target_mode is ieCCP_Target, THE engine SHALL iteratively solve for the total spend that yields the target ie%CCP given Brand and NB reg projections.
6. WHEN target_mode is Regs_Target, THE engine SHALL solve for the spend required to produce the target registration count, subject to Elasticity_Curve and ie%CCP feasibility checks.
7. WHEN scope is a Region (NA, EU5, WW), THE engine SHALL produce projections for each constituent market independently, sum segments across markets, AND report the regional blended ie%CCP using the regional-sum formula.
8. IF a target is infeasible (e.g., NB CPA curve cannot support the target regs at any realistic spend), THEN THE engine SHALL return an explicit infeasibility message identifying the binding constraint AND propose a closest-feasible alternative.
9. **v1 scope boundary**: The engine SHALL fit all 10 markets with market-specific parameters. AU additionally receives Southern_Hemisphere_Handling (R14) because its inverted seasonality and data-limited history require specialized gap-filling. Regional fallback remains available as a safety net for any market whose data becomes insufficient (e.g., a new market launch).
10. **Math constraint**: THE engine SHALL use recency-weighted linear regression (exponential decay, half-life 52 weeks default) for all fitted parameters. v1 SHALL NOT use hierarchical Bayesian, BSTS, Prophet, or any external ML library beyond numpy / scipy / scikit-learn.
11. **CPC elasticity**: THE engine SHALL fit CPC elasticity per market per segment when r² ≥ 0.3 on the fit. WHERE r² < 0.3, THE engine SHALL derive CPC from CPA elasticity (CPC = CPA × CVR) AND emit a `CPC_DERIVED_FROM_CPA` warning.
12. **Performance budget**: UI recompute SHALL complete in under 150 ms median on a typical enterprise laptop. Monte Carlo sampling in the browser SHALL use a Web Worker to avoid blocking the UI thread.
13. **Extrapolation guardrail**: IF requested Spend exceeds 1.5× the historical maximum quarterly spend for the scope, THEN THE engine SHALL emit HIGH_EXTRAPOLATION AND refuse the fit OR return a Hill-function ceiling estimate with a clear "extrapolation region" banner.

### Requirement 3: Portable, self-contained HTML UI

**User Story:** As Richard, I want the projection tool to live as a single HTML file I can open from the Kiro dashboard, upload to SharePoint, embed in Symphony, or send to Lorena as an attachment, so that anyone — human or agent — can access it without needing Kiro itself running.

#### Acceptance Criteria

1. THE MPE UI SHALL be delivered as a single HTML file (`shared/dashboards/projection.html`) with all CSS and JS inlined, except for a single Chart.js CDN reference.
2. THE HTML file SHALL render functionally identically whether served by `serve.py`, opened from a local filesystem, embedded via iframe in SharePoint, or embedded in Symphony.
3. THE HTML file SHALL load its parameters and baseline data from a companion JSON file (`shared/dashboards/data/projection-data.json`) served from the same origin, OR from an embedded `<script type="application/json">` block if served as a fully-standalone attachment.
4. THE HTML file SHALL include a machine-readable Methodology_Manifest so that agents can parse the page without running JS.
5. THE HTML file SHALL include a visible header showing title, parameter freshness date, data range (YTD weeks covered), fallback-level badges per active parameter, and owner.
6. THE HTML file SHALL include three input modes — Preset selector, Slider mode, Target mode. supported_target_modes for the selected scope SHALL constrain the Target mode options.
7. THE HTML file SHALL visualize outputs as: summary card with totals, week-by-week line chart for Registrations and Spend with credible-interval bands, stacked-area chart for Brand-vs-NB contribution, ie%CCP gauge showing current vs target.
8. THE HTML file SHALL NOT make any outbound API call at render time other than the Chart.js CDN.
9. THE HTML file SHALL emit Copy-as-JSON and Copy-as-markdown actions for persistence.
10. THE HTML file SHALL provide "Explain this number" tooltips on every KPI. Each tooltip SHALL state the formula, the data range, the fallback status, and a plain-English "what to tell Lorena" line. See `shared/wiki/agent-created/operations/mpe-explain-this-number-examples.md` (produced as part of Task 2.9).
11. THE HTML file SHALL NOT include in v1: command palette, natural-language input, Apple micro-animations, 3D visuals, any advanced tab beyond summary/charts/warnings/narrative/provenance.
12. THE HTML file SHALL NOT depend on Streamlit, Reflex, Django, Flask, or any server-dependent UI framework. Server-dependent frameworks break the SharePoint portability requirement.


### Requirement 4: Saved projections with full provenance

**User Story:** As Richard, I want every projection run I care about to save as a durable record with its inputs, parameters-used, and outputs, so that when Lorena asks "what did you tell me on 4/22?" I can retrieve the exact projection, and three months later I can compare my 4/22 projection against what actually happened.

#### Acceptance Criteria

1. THE MPE SHALL persist Saved_Projections as JSON files at `shared/dashboards/data/projections/{market_or_region}/{yyyy-mm-dd}-{slug}.json`.
2. A Saved_Projection JSON SHALL include: scope, time_period, target_mode, target_value, all inputs, the Parameter_Set snapshot at projection time, all outputs (weekly and aggregated), timestamp, author.
3. THE MPE SHALL provide a "Save" action that writes the file via `serve.py`, and a "Copy JSON" action for environments where file-write is unavailable (SharePoint, Symphony).
4. THE MPE SHALL provide a "Load saved projection" dropdown listing saved projections for the current scope, most-recent first.
5. WHEN a saved projection is loaded, THE MPE SHALL restore all inputs, apply them to the current parameter set, AND flag in plain English which parameters have changed since the save (e.g., "NB elasticity for MX was refit on 5/15 — your saved projection used the 4/22 curve, reloading produces different numbers").
6. THE MPE SHALL support a "Compare saved projections" view showing up to three saved projections side-by-side with deltas.
7. THE Saved_Projection JSON SHALL conform to a stable schema documented in the Methodology_Manifest.
8. WHEN a period covered by a Saved_Projection has closed, THE MPE SHALL support a "Score" action comparing projection vs actuals from `ps.v_weekly` and writing the scored record to `ps.projection_scores`.

### Requirement 5: Quarterly parameter refit as durable process

**User Story:** As Richard, I want the projection engine's parameters reviewed and refit on a predictable cadence so that when I show this to leadership, I can say "these numbers are current as of last week" with confidence, and three quarters from now the tool is not running on stale math.

#### Acceptance Criteria

1. THE MPE SHALL include a refit job (`shared/tools/prediction/refit_market_params.py`) that, for each Fully_Fit_Market, refits every quarterly parameter using the latest `ps.v_weekly` data, computes Validation_MAPE against the most recent 12-week holdout, AND writes the new parameter_version.
2. THE refit job SHALL be invocable manually AND SHALL be schedulable as a Kiro hook (`mpe-refit.kiro.hook`). v1 uses manual trigger; auto-schedule is deferred to v1.1.
3. THE refit job SHALL produce an owner-readable refit report at `shared/dashboards/data/refit-reports/{yyyy-mm-dd}.md` listing every parameter changed, MAPE delta, anomalies (with plain-English explanation), recommended actions, AND rollback instructions.
4. IF a parameter's new Validation_MAPE exceeds its prior Validation_MAPE by more than 10 percentage points, THEN THE refit job SHALL flag the parameter as a refit concern requiring owner approval before the new version is marked active.
5. THE MPE SHALL include an annual refit procedure documented in `shared/wiki/agent-created/operations/mpe-annual-refit-runbook.md` covering CCP refresh from finance, seasonality re-baselining, ie%CCP target reconfirmation, regime-change review.
6. WHEN a quarterly refit runs, THE refit report SHALL be pushed to SharePoint under `Kiro-Drive/system-state/mpe-refits/` for durability.
7. THE MPE UI SHALL display a "Parameters current as of YYYY-MM-DD" banner sourced from the most recent `last_refit_at` across all parameters used in the current projection.
8. THE refit job SHALL prompt the owner: "Any new regime changes since last quarter?" AND record the answer in `ps.regime_changes`. Known prior breakpoints (MX 2025-W27 ie%CCP ceiling, MX 2026-W15 NB drop provisional) SHALL be shown in the prompt.

### Requirement 6: Regional rollups with mathematical rigor

**User Story:** As Richard, when I project for EU5 or WW, I want the rollup computed from per-market projections — not from a blended market average — so that the regional ie%CCP correctly reflects each market's negotiated CCP and mix effects are honest.

#### Acceptance Criteria

1. THE MPE SHALL compute NA, EU5, and WW projections by producing independent per-market projections for each constituent market, then summing Brand_Registrations, NB_Registrations, Brand_Spend, NB_Spend, Brand_Clicks, NB_Clicks across markets.
2. THE regional blended ie%CCP SHALL be computed as `sum(market_spend) / sum(market_brand_regs × market_Brand_CCP + market_nb_regs × market_NB_CCP)` across constituent markets.
3. THE MPE SHALL NOT use a regional-average CCP shortcut for ie%CCP computation.
4. WHEN a regional projection is produced, THE MPE SHALL display per-market breakdown showing each market's contribution. For Fallback_Markets, THE breakdown SHALL display the `regional_fallback` badge next to that market's line.
5. WHEN a regional projection is applied with a target_mode, THE MPE SHALL allow the user to specify whether the target is imposed at the regional level (solve regional spend, distribute across markets proportionally) OR at the per-market level (each market independently solved).
6. Regional rollups SHALL preserve precision across scale differences (MX CCP $97 vs US CCP $412 — a 4x scale delta). Sum-then-divide SHALL be the only math applied.

### Requirement 7: Dual-audience consumability (human interactive, agent programmatic)

**User Story:** As either Richard using the UI or an agent querying the projection programmatically, I want consistent access to the same math, parameters, and outputs, so that the answer to "what's our MX Q2 projection at 75% ie%CCP" is identical whether I click through the UI or an agent pulls it.

#### Acceptance Criteria

1. THE MPE SHALL expose a Python API (`shared/tools/prediction/mpe_engine.py`) with a single entry point `project(scope, time_period, target_mode, target_value, **inputs)` returning the same output schema as the HTML UI's JSON output.
2. THE Python API SHALL be importable by sibling tools AND SHALL NOT require the UI to be running.
3. THE HTML UI SHALL internally call the same logic (ported to JS) that the Python API uses, with a parity test suite. Tolerance: 0.1% for deterministic outputs, 2% for Monte Carlo credible interval outputs (sampling noise inherent).
4. THE MPE SHALL include a CLI entry point (`python3 -m shared.tools.prediction.mpe_engine --market MX --period 2026-Q2 --target ieCCP:75`) producing JSON to stdout.
5. THE Methodology_Manifest embedded in the HTML SHALL be the single source of truth for output schema.
6. THE MPE SHALL document in the Methodology_Manifest how an agent consumes the projection (JSON paths for parameter values, output values, caveats) so an LLM agent reading raw HTML can extract the answer without running JS.
7. THE Python engine SHALL coexist with the existing `bayesian_projector.py` stack in `shared/tools/prediction/`. `bayesian_projector.py` continues to serve `wbr_pipeline.py` for week-ahead forecasting; `mpe_engine.py` serves planning projections with target modes. Shared primitives live in `core.py`.

### Requirement 8: Leadership-grade narrative output

**User Story:** As Richard preparing to showcase this to Brandon/Kate/leadership, I want the tool to produce a stakeholder-ready summary that leads with the "so what" and backs it with rigor, so that I can use a single projection run as the basis for a paragraph in a WBR callout, an email to Lorena, or a slide in an OP1 deck.

#### Acceptance Criteria

1. THE MPE SHALL include a "Generate narrative" action producing a 2-4 paragraph stakeholder summary following Richard's writing style (data-forward, no em-dashes, per-market specificity, explicit "so what").
2. THE narrative SHALL state: scope, time period, target, central projection (regs, spend, ie%CCP), confidence range or sensitivity, AND at least one explicit caveat or risk.
3. THE narrative SHALL cite parameter freshness date AND YTD data range informing the projection.
4. THE narrative template SHALL be editable in the Parameter_Set (per-market and per-region tone) AND SHALL follow richard-writing-style + richard-style-amazon steering files.
5. THE narrative SHALL explicitly call out when the projection is near a constraint ceiling, when a parameter is stale, OR when the target is infeasible.
6. THE narrative for a Fallback_Market SHALL state the fallback explicitly (e.g., "UK projection uses the EU5 regional fallback curve; CI is wider than for fully-fit markets").

### Requirement 9: Safety guardrails for projection quality

**User Story:** As Richard, I want the projection engine to refuse to produce a number when the inputs don't support one, and to warn me loudly when something's off, so that I never hand Lorena a confident-looking number built on a broken foundation.

#### Acceptance Criteria

1. IF a Fully_Fit_Market's parameters are missing or all stale beyond `refit_cadence`, THEN THE MPE SHALL refuse to produce a projection AND SHALL display which parameters must be refit.
2. IF a target_value is outside the historically-observed range for that market (spend exceeds 1.5× historical maximum quarterly), THEN THE MPE SHALL produce the projection with a HIGH_EXTRAPOLATION prefix AND apply the Hill-function guardrail.
3. IF an Elasticity_Curve's Validation_MAPE exceeds 40%, THEN THE MPE SHALL label the output LOW_CONFIDENCE AND expand reported error bands.
4. IF fewer than 8 weeks of YTD actuals are available, THEN THE MPE SHALL lean on prior-year seasonality AND label the projection SEASONALITY_DOMINATED.
5. WHEN any guardrail fires, THE MPE SHALL surface the warning in the UI banner, in Copy-as-JSON, in Copy-as-markdown, AND in the narrative.
6. WHEN a Fallback_Market is projected, THE MPE SHALL always surface a DATA_LIMITED banner explaining the fallback source (NA or EU5 regional curve).

### Requirement 10: Deployment and discoverability

**User Story:** As the team or leadership looking for the projection tool, I want to find it in the places I already look — the Kiro dashboard nav, SharePoint Artifacts, and a wiki article — so that once this ships, I do not need to be told where it lives.

#### Acceptance Criteria

1. THE MPE UI SHALL be accessible from the Kiro dashboard `index.html` nav as a top-level tab labeled "Projections".
2. THE MPE UI SHALL be published to SharePoint `Kiro-Drive/Artifacts/strategy/projection-engine.html` with the companion JSON data file.
3. THE MPE SHALL have a wiki article at `shared/wiki/agent-created/operations/market-projection-engine.md` documenting purpose, usage, methodology at a glance, and where to find the tool in each environment.
4. THE wiki article SHALL be published to SharePoint via the existing sharepoint-sync process.
5. THE agent-bridge repository SHALL include the MPE spec and wiki article (Cold_Start_Safe) so a new agent on another platform can reconstitute intent.

### Requirement 11: Multi-year projection capped at 2 years in v1

**User Story:** As Richard preparing OP1 or multi-year strategic conversations, I want the engine to project 1-2 years forward using recency-weighted historical data so that the model understands how each market has naturally grown. 3-year projections are deferred to v1.1 because compounded uncertainty at 3 years produces bands so wide they are useless.

#### Acceptance Criteria

1. THE MPE SHALL support Multi_Year time_period option producing projections for 1 or 2 future fiscal years. 3-year projections SHALL NOT be produced in v1.
2. THE MPE SHALL maintain a YoY_Growth_Trend parameter per market per segment, fit from 2-4 years of historical `ps.v_weekly` data, refit quarterly.
3. THE YoY_Growth_Trend fit SHALL use recency-weighted regression (exponential decay half-life 52 weeks) so recent years dominate but prior years still inform.
4. WHEN a Multi_Year projection is requested, THE engine SHALL apply YoY_Growth_Trend multiplicatively across years while preserving within-year seasonality shape.
5. IF a market has fewer than 104 weeks of data, THEN THE engine SHALL emit LOW_CONFIDENCE_MULTI_YEAR AND fall back to flat YoY (no growth).
6. WHERE structural change is documented (regime breakpoint in `ps.regime_changes`), THE MPE SHALL allow the user to exclude pre-breakpoint history from the YoY fit.
7. THE engine SHALL report YoY_Growth_Trend confidence (strong / moderate / weak) based on r² and data-range sufficiency.
8. IF 2-year 90% CI width exceeds 3× central estimate, THEN THE engine SHALL emit VERY_WIDE_CI AND recommend "single-year projection only" to the user.
9. WHERE the user requests a 3-year projection in v1, THE UI SHALL display "3-year projections are not available in v1. Single and 2-year projections are supported. 3-year lands in v1.1 once we have seen how 2-year intervals behave in practice."

### Requirement 12: Bayesian credible intervals with locked sample counts

**User Story:** As Richard or any stakeholder reading a projection, I want every output KPI to carry an explicit uncertainty range reflecting model-parameter uncertainty, so that I can honestly say "regs will land between X and Y with 70% credibility" instead of "regs will be Z."

#### Acceptance Criteria

1. THE MPE SHALL model each fitted parameter with a posterior distribution from its historical fit.
2. WHEN a projection is produced, THE engine SHALL propagate parameter uncertainty via Monte Carlo sampling. Sample counts are LOCKED in v1: **200 samples for UI, 1000 samples for CLI**. Sample count is NOT user-tunable in v1.
3. THE engine output SHALL include 50%, 70%, and 90% credible intervals for Registrations, Spend, Clicks, CPA, and ie%CCP at each time grain.
4. THE credible intervals SHALL be visualized as shaded bands around line charts and as "X to Y" ranges on summary cards.
5. WHERE 90% CI width exceeds 2× central estimate, THE MPE SHALL emit HIGH_UNCERTAINTY AND surface which parameter posterior drives the width.
6. THE credible interval computation SHALL live in `mpe_uncertainty.py` separate from core engine, so it can be improved without touching core logic.
7. Python and JS credible interval outputs SHALL match within 2% (sampling noise is inherent; 0.1% parity is not expected).
8. WHERE a parameter's posterior is effectively a point estimate (a negotiated CCP), THE engine SHALL treat it as fixed, not sample from it.
9. Credible intervals will be slightly asymmetric due to elasticity posterior skew (wider on upside). Tooltips SHALL explain this.
10. MCMC-based posterior estimation SHALL NOT ship in v1. Monte Carlo sampling from fit-derived posteriors is the v1 approach; MCMC is deferred to v1.1+.

### Requirement 13: Anomaly detection on parameter refits — 3SD + regime tag only

**User Story:** As Richard relying on the quarterly refit to keep parameters current, I want the refit job to loudly flag any parameter whose value has shifted unexpectedly between versions, so that a data bug or mis-fit does not silently corrupt every downstream projection.

#### Acceptance Criteria

1. WHEN the quarterly refit job produces a new parameter_version, THE job SHALL compare the new value against the trailing distribution of prior versions (default window: last 4 quarterly refits).
2. IF the new value is more than 3 standard deviations from the trailing mean, THEN THE refit job SHALL flag the parameter as an anomaly candidate.
3. Anomaly-flagged parameters SHALL NOT be marked active until the owner approves them via the refit report.
4. THE refit report SHALL include an "Anomalies" section with: prior values, new value, delta, SD distance, AND a plain-language explanation ("DE NB CPA elasticity jumped from 0.92 to 1.34 — a 60-SD move — suggesting a regime change or fit failure").
5. Anomaly detection SHALL apply to historical-fit parameters (elasticity coefficients, CPA/CPC baselines, seasonality weights, YoY trends) AND SHALL NOT apply to negotiated parameters (CCPs, ie%CCP targets).
6. WHERE a regime change is known to have occurred, THE MPE SHALL allow the owner to document it in `ps.regime_changes` AND mark anomalies in the same period as "expected-anomaly" instead of "investigate-anomaly."
7. THE anomaly module SHALL be testable in isolation with synthetic anomalies (both true-positive and false-positive).
8. v1 SHALL NOT include: Isolation Forest, BSTS, LSTM, autoencoders, hierarchical models, or any external ML library beyond numpy / scipy / scikit-learn. 3SD + regime tag is the v1 approach. Thresholds tighten after 4 quarterly refits per market; v1 is "learning mode" with liberal flagging.

### Requirement 14: Per-market target modes, per-scope narratives, AU Southern Hemisphere handling

**User Story:** As Richard producing stakeholder output, I want each market to have its own target-mode palette and narrative template, and I want AU to be modeled honestly as a Southern Hemisphere market rather than forced to use NH seasonality, so that every output reflects the market's actual strategic and physical context.

#### Acceptance Criteria

1. THE `ps.market_projection_params` registry SHALL include a `supported_target_modes` parameter per market listing valid target modes (AU supports spend and regs; MX supports all three; others follow MARKET_STRATEGY migrated from `bayesian_projector.py`).
2. THE MPE UI SHALL dynamically show or hide target-mode options based on the selected scope's `supported_target_modes`.
3. THE MPE SHALL store a `narrative_template` parameter per market AND per region. Templates are editable in the registry.
4. THE narrative template SHALL accept placeholders for projection outputs, parameter freshness, confidence levels, strategic framing.
5. WHEN the engine generates narrative for a region, THE engine SHALL use the regional template, NOT a concatenation of per-market narratives.
6. THE regional narrative template SHALL explicitly surface mix effects ("EU5 delivered X regs with DE +A% and IT -B% driving the mix shift") rather than reporting only aggregates.
7. THE UI SHALL allow the user to preview any scope's narrative template before running a projection.
8. Each per-market narrative template SHALL be no longer than 300 words expanded AND MUST follow richard-writing-style.

**AU Southern Hemisphere handling (AU-specific):**

9. THE engine SHALL apply Southern_Hemisphere_Handling to AU only. No other market has this treatment in v1.
10. AU seasonality SHALL be built as a hybrid per-week: use AU-specific weight where AU has ≥ 2 usable weeks for that calendar week number AND those weeks are not in an excluded regime window; otherwise use WW seasonality shifted 26 weeks (inverted for Southern Hemisphere).
11. Each week's weight in `brand_seasonality_shape` and `nb_seasonality_shape` SHALL carry a `provenance` sub-field: `"au_actual"` or `"nh_shifted_w{N}"` indicating the source week in the NH calendar.
12. THE narrative for AU SHALL state the hybrid explicitly: "AU seasonality uses {M} weeks of AU-specific data plus {52-M} weeks of Northern Hemisphere signal shifted 26 weeks. Credible intervals are wider than for markets with full annual history. Expect convergence by {refit_quarter_when_au_has_52_weeks}."
13. AU elasticity SHALL use WW regional elasticity curves as the base, adjusted for AU's observed Brand-to-NB ratio and spend-to-regs level. This is a level shift, not a curve shape shift.
14. AU parameter records SHALL set `fallback_level = 'southern_hemisphere_hybrid'` for seasonality and `fallback_level = 'regional_fallback'` for elasticity until AU has 80+ clean weeks.
15. AU regime classification (structural vs transient vs excluded) is locked as of 2026-04-22:
    - 2025-06-10 PS launch: `active = FALSE` — excluded, market-birth marker
    - 2026-01-01 Adobe bid strategies: `is_structural_baseline = TRUE`, `active = TRUE` — new baseline
    - 2026-02-01 bid stabilization: `active = FALSE` — merged observation, not a separate regime
    - 2026-03-26 Polaris LP (reverted): `is_structural_baseline = FALSE`, `half_life_weeks = 0`, `active = TRUE` — exclude weeks 13-15 of 2026 from fit; no long-term effect

### Requirement 15: Acceptance test — automated core for MX/US/AU + manual MX-4/22 simulation

**User Story:** As Richard preparing to showcase this to leadership, I want the acceptance test to guarantee the Fully_Fit_Markets survive pressure-testing, AND I want the MX 2026-04-22 pressure-test conversation reproducible in the UI as a live demo, so leadership sees rigor without me needing to automate subjective stakeholder conversation.

#### Acceptance Criteria

1. THE MPE SHALL include an automated acceptance test suite (`tests/test_acceptance.py`) for MX, US, AU AND regional rollups NA, EU5, WW.
2. For each Fully_Fit_Market AND each region, THE acceptance test SHALL execute:
   - (a) Parameter freshness check
   - (b) Base projections W/M/Q/Y/MY with no errors, no unexpected infeasibility
   - (c) Spend_Target at 2× annual OP2 → HIGH_EXTRAPOLATION + HIGH_UNCERTAINTY fire correctly
   - (d) ieCCP_Target at configured level → sanity envelope (spend within 2× prior-year actual)
   - (e) Regs_Target at 1.5× prior-year → convergence OR structured infeasibility with binding constraint
   - (f) Brand +30% uplift → Brand regs projection increases proportionally; NB stays in prior bands
   - (g) NB elasticity doubled slope override → NB spend shifts appropriately
   - (h) Save/reload exact match
   - (i) Stale-parameter surface test
   - (j) Narrative output conformance (2-4 paragraphs, no em-dashes, cites freshness, includes caveat)
3. For each region, THE acceptance test SHALL additionally execute:
   - (k) Regional-level target mode → sum-then-divide validation against hand-computed expected values
   - (l) Per-market target mode → regional output equals sum of independent per-market solutions
   - (m) Regional narrative surfaces mix effects explicitly
4. THE **MX 2026-04-22 simulation** SHALL be a documented 10-step manual checklist (in `shared/wiki/agent-created/operations/mpe-mx-422-simulation.md`) run live in the demo by the owner. The checklist steps:
   1. Initial projection (MX, Q2, ieCCP 75, Moderate preset)
   2. Mental-model challenge — Brand vs NB breakdown
   3. CCP correction — override Brand to $97 and watch gauge
   4. Formula correction — "Explain ieCCP" tooltip shows reg-weighted formula
   5. Regime-shift identification — provenance modal shows 2025-W27 ceiling activation AND 2026-W15 NB drop (provisional)
   6. Seasonality refinement — 52-week weights with posterior uncertainty
   7. CPA elasticity fit — double NB slope override
   8. Week-by-week re-run — W1 vs W13 of Q2 scrubbing
   9. Error-band toggle — 90% CI shows asymmetric bands
   10. Marginal-regs sanity — +$50k Brand scrubber
5. Automated simulation of subjective stakeholder steps is explicitly OUT of v1. Attempting to automate "why is this higher than my mental model?" is a known trap.
6. THE acceptance test suite SHALL run in under 15 minutes for the full automated matrix AND under 2 minutes for a single-market quick-check.
7. THE acceptance test results SHALL log to `shared/dashboards/data/acceptance-test-reports/{yyyy-mm-dd}-{scope}.md`.
8. THE acceptance test SHALL be a pre-commit gate for changes touching `mpe_engine.py`, `mpe_engine.js`, or `ps.market_projection_params` schema.
9. WHERE a Fallback_Market lacks sufficient data to pass all steps, those steps SHALL be marked XFAIL with explicit reason.
10. THE acceptance test suite SHALL be reviewed quarterly alongside the refit job so new stakeholder-conversation patterns get added as they emerge.

### Requirement 16: Explicit v1 Boundaries (Scope Creep Shield)

**User Story:** As Richard, I want the spec to hard-code what v1 will NOT do, so that future conversations with Kiro or any agent do not re-litigate scope decisions every time we open the project.

#### Acceptance Criteria

v1 SHALL NOT include any of the following. Each requires a new spec and owner approval:

1. Using regional fallback as the default for any market with ≥ 80 clean weeks of market-specific data (use market-specific fits when the data supports them).
2. Hierarchical Bayesian, BSTS, Prophet, Prophetverse, LightweightMMM, PyMC, NumPyro, or any external ML library beyond numpy / scipy / scikit-learn.
3. Cross-elasticity between Brand and NB (spend in one segment affecting the other's curve).
4. Macro or economic overlays.
5. Placement decay curves as a first-class model (apply as uplift only).
6. Advanced anomaly ML (Isolation Forest, autoencoders, LSTM).
7. Command palette, Apple-level micro-animations, 3D visuals, natural-language input in the browser.
8. Auto-scheduled cron refit. v1 uses manual hook trigger.
9. Slack notifications or email digests for refit reports. v1 pushes to SharePoint only.
10. Streamlit, Reflex, Django, Flask, or any server-dependent UI framework. These break the R3 portability requirement.
11. MCMC-based posterior estimation. v1 uses Monte Carlo sampling from fit-derived posteriors.
12. 3-year Multi_Year projections. v1 caps at 2 years.
13. Automated simulation of subjective stakeholder-conversation steps (the MX 4/22 "why is this higher than my mental model?" steps). These run as a manual checklist in the demo.
14. Extending Southern_Hemisphere_Handling to markets not below the equator. AU is the only AU-treatment target in v1. A future BR or ZA launch requires its own spec update.

## Revision History

- 2026-04-22 initial draft.
- 2026-04-22 revised per initial Richard feedback: CPC elasticity, multi-year, Bayesian CIs, anomaly detection, per-market/region narratives, rigorous acceptance test added.
- 2026-04-22 **rewrite per low-maintenance framing** (Grok synthesis + self-inspection): added R0 Maintainability, R16 v1 Boundaries; restricted to MX/US/AU fully fit + CA/UK/DE/FR/IT/ES/JP regional fallback; capped Multi_Year at 2 years; locked Monte Carlo samples at 200 UI / 1000 CLI; CPC elasticity uses r² ≥ 0.3 branch (option c) falling back to CPA-derived; manual MX 4/22 simulation checklist replaces automated subjective steps; added MX 2026-W15 NB drop provisional breakpoint; 3SD anomaly detection only; acknowledged coexistence with existing `bayesian_projector.py` stack.

- 2026-04-22 **v1 scope expanded per owner direction**: All 10 markets get market-specific fits (previously scoped to MX/US/AU fully fit + 7 fallback). Data audit (`data_audit.py`) confirmed 9 of 10 markets have 102-168 clean weeks; earlier conservative scope was based on owner-maintenance concern, which is mitigated by making each market fit a templated operation (data_audit → mpe_fitting → validate → commit). AU adds Southern_Hemisphere_Handling (R14.9-R14.15) because it is the only market below the equator. AU regime classification locked (R14.15): Adobe bid strategies (2026-01-01) promoted to structural baseline; Feb 2026 stabilization merged into Jan regime; Polaris LP (2026-03-26, reverted 4/13) classified as short-term excluded. MX 2026-W15 NB drop (Yun-Kang investigation) added to `ps.regime_changes` with confidence=0.5 (provisional), half_life_weeks=2 — reclassify at first refit.
