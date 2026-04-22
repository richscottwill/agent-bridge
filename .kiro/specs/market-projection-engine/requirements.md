# Requirements Document

## Introduction

Paid Search budget conversations today happen with ad-hoc Python scripts, stale mental models, and CCP assumptions that live in Richard's head or buried Quip docs. The MX conversation on 2026-04-22 (run in real time through Kiro) exposed how much latent rigor exists across the data layer (`ps.v_weekly`, `ps.forecasts`, `ps.market_constraints`) but cannot be composed into a defensible answer without writing custom code each time. Every market review — MX/Lorena, AU/Alexis, US/Andrew, EU5 — re-solves the same math from scratch.

The Market Projection Engine (MPE) codifies the projection methodology into a durable, reviewable, durable system that produces defensible forecasts for any market (US, CA, UK, DE, FR, IT, ES, JP, MX, AU) or regional rollup (NA, EU5, WW) across any time period (week, month, quarter, year) for any of nine KPIs (Brand Registrations, NB Registrations, Brand Spend, NB Spend, Brand Clicks, NB Clicks, Brand CPA, NB CPA, ie%CCP). The system exposes the math through three consumption patterns: machine-readable methodology for agents, interactive UI for humans, and programmatic API for downstream automation.

The engine is an L3 (Team Automation) artifact intended to be showcased to the team and leadership. It must work offline once deployed (SharePoint, Symphony, standalone browser) and survive a platform migration. It must be **the** answer to "what would X spend produce?" for every market, every time, every stakeholder.

This spec defines the engine, its parameters, the projection logic, the UI, the persistence model, and the quarterly maintenance process. Concrete fits for each market are downstream tasks executed against this spec.

## Glossary

- **Market_Projection_Engine (MPE)**: The complete system — parameter registry + projection logic + UI + persistence — defined by this spec.
- **Market**: One of ten paid search markets — US, CA, UK, DE, FR, IT, ES, JP, MX, AU.
- **Region**: A derived rollup of markets — NA (US + CA), EU5 (UK + DE + FR + IT + ES), WW (all ten markets).
- **Scope**: A selection of one market OR one region for a projection run.
- **Time_Period**: One of five projection horizons — Week (single ISO week), Month (single calendar month), Quarter (Q1/Q2/Q3/Q4 of target year), Year (full fiscal year), Multi_Year (1-3 future fiscal years — e.g., for OP1 planning).
- **Projection_Run**: A single invocation of the MPE for one Scope × Time_Period × Input_Set producing a complete KPI output matrix.
- **KPI**: One of nine tracked metrics — Brand_Registrations, NB_Registrations, Brand_Spend, NB_Spend, Brand_Clicks, NB_Clicks, Brand_CPA (derived), NB_CPA (derived), ie%CCP (derived). Registrations, Spend, and Clicks are primary; CPAs are derived from Spend/Registrations; ie%CCP is derived from the CCP formula. Both CPAs and CPCs are modeled via elasticity curves so that at the margin, higher Spend produces both higher CPA (diminishing returns on reg output) and higher CPC (bid inflation on click volume).
- **Segment**: Brand or NB (Nonbrand). Every KPI except ie%CCP has a Brand and NB variant. Regional rollups sum segments across constituent markets.
- **CCP**: Cost-per-Customer-Payback — a per-market, per-segment dollar value set by finance/leadership negotiation. Sourced from the Summary tab of `shared/uploads/sheets/CCP Q1'26 check yc.xlsx`, **column U ("FINAL ALIGNED")**, which is the post-negotiation canonical value (not Sheet2 which holds Q1 static pre-negotiation values). MX has Brand CCP $97.22 / NB CCP $27.59 per column U (rounds to $97 / $28, matching Richard's stated 2026-04-22 negotiation). CCPs are inputs to the ie%CCP formula, not projected. CCP values vary over time (see `ieccp_time_series` in the parameter registry, sourced from WW dashboard IECCP tab) and the engine SHALL respect the CCP that was in effect at each projection-target week.
- **ie%CCP**: `total_spend / (brand_regs × Brand_CCP + nb_regs × NB_CCP)` × 100. Expressed as a percentage. Target ceiling varies by market (MX = 100%, JP = 30-50%, US/CA/UK/DE/FR/IT/ES = 50-65% per existing project.py, AU = not tracked — efficiency strategy).
- **Elasticity_Curve**: The relationship between weekly Spend (Brand or NB) and weekly CPA or CPC (Brand or NB), fit per market from historical data. Used to predict CPA/CPC changes when Spend changes. Four curves per market: Brand_CPA_elasticity, NB_CPA_elasticity, Brand_CPC_elasticity, NB_CPC_elasticity.
- **Recency_Weighted_Fit**: A parameter-fitting technique where historical data points are weighted by recency (e.g., exponential decay with a half-life of 52 weeks). Enables the model to reflect recent regime shifts (placement launches, CCP renegotiations, strategy changes) without discarding the multi-year seasonality signal. Applied to all elasticity curves and growth-trend parameters.
- **YoY_Growth_Trend**: A per-market multiplicative factor capturing structural growth year-over-year (separate from seasonality). Fit from 2-4 years of historical data with recency weighting. Drives multi-year projection and informs single-year full-year projections.
- **Bayesian_Credible_Interval**: A probabilistic uncertainty band around a projection output, derived from posterior distributions over the engine parameters. Distinct from MAPE-overlay error bands. Propagates parameter uncertainty through the engine to produce "X% credible" intervals for each output KPI.
- **Anomaly_Detection**: Automated check during parameter refit that flags any parameter whose new value differs from the prior value by more than a market-specific threshold (default 3 standard deviations from the prior's recent distribution). Fires for historical-fit parameters (CPA baselines, elasticity coefficients, CPCs, growth trends), not negotiated parameters (CCPs).
- **Seasonality_Shape**: A 52-week normalized distribution of Registrations per segment per market, derived from prior-year actuals. Used to distribute annual projections across weeks.
- **Parameter_Set**: The complete collection of per-market parameters (CCPs, elasticity curves, seasonality shapes, CPC values, baseline CPAs) required for the engine to produce a projection for that market. Stored in DuckDB `ps.market_projection_params`.
- **Projection_Input**: A user-supplied value that modifies the base projection — a slider movement, a target constraint (e.g., "target 75% ie%CCP"), an uplift assumption (e.g., "+15% Brand from placement"), or a scenario preset.
- **Target_Mode**: One of three constraint modes — Spend_Target (fix total spend, compute everything else), ieCCP_Target (fix ie%CCP, compute spend and regs), or Regs_Target (fix total regs, compute spend and ie%CCP).
- **Scenario_Preset**: A named bundle of projection inputs (e.g., "Conservative", "Moderate", "Aggressive" or "Placement-Persists", "Placement-Decays", "Base-Case-No-Placement") that users can apply with one click. Presets are per-market and editable.
- **Saved_Projection**: A persisted Projection_Run — inputs, parameters-used, outputs, timestamp, author — stored as JSON for later recall, comparison, or handoff.
- **Parameter_Freshness**: A per-parameter timestamp (`last_refit_at`, `last_validated_at`) that drives staleness warnings. A parameter older than its refresh cadence surfaces a warning in the UI.
- **Refit_Cadence**: The required frequency of parameter recomputation — Annual (CCPs, seasonality shape), Quarterly (CPA baselines, elasticity curves, CPCs).
- **Validation_MAPE**: Mean Absolute Percentage Error computed against a holdout period (typically the most recent 12 weeks) when a parameter is refit. Stored in `ps.parameter_validation`.
- **Methodology_Manifest**: A machine-readable JSON block embedded in the HTML UI that declares every parameter used, every formula applied, and the expected output shape. Enables agents to consume the projection engine without running JS.
- **Portable_Artifact**: An HTML file that renders identically and functions fully when served from Kiro's `serve.py`, uploaded to SharePoint, embedded in Symphony, or opened directly from the filesystem with no external dependencies at render time beyond a single CDN call for the chart library.

## Requirements

### Requirement 1: Parameter registry as canonical source of truth

**User Story:** As Richard, I want every market's projection parameters (CCPs, elasticity, seasonality, CPC, CPA baselines) stored in one queryable table with ownership and freshness metadata, so that I know the math is grounded in current reality and can't drift out of sync with what finance negotiated.

#### Acceptance Criteria

1. THE MPE SHALL maintain a DuckDB table `ps.market_projection_params` containing one row per (market, parameter_name, parameter_version) tuple.
2. THE parameter registry SHALL include the following parameter families for each market: Brand_CCP, NB_CCP, Brand_CPA_baseline, Brand_CPA_elasticity, NB_CPA_baseline, NB_CPA_elasticity, Brand_seasonality_shape (52 weekly weights), NB_seasonality_shape (52 weekly weights), Brand_CPC, NB_CPC, ie%CCP_target, ie%CCP_range (low, high).
3. WHEN a parameter is updated, THE MPE SHALL write a new row with incremented `parameter_version` and timestamp `last_refit_at`, preserving the prior row for audit.
4. THE parameter registry SHALL include a `refit_cadence` column declaring "annual" or "quarterly" for each parameter.
5. THE parameter registry SHALL include a `source` column documenting where the value came from (finance_negotiation, historical_fit, manual_override, etc.).
6. IF a parameter's `last_refit_at` is older than the maximum age permitted by `refit_cadence` (365 days for annual, 120 days for quarterly), THEN THE MPE SHALL surface the parameter as stale in any UI or projection run that consumes it.
7. WHERE a market has insufficient historical data to fit an Elasticity_Curve (< 40 data points spanning a range of spend levels), THE MPE SHALL fall back to the regional average curve (NA or EU5) AND declare the fallback explicitly in the projection output.

### Requirement 2: Nine-KPI projection engine with segment split

**User Story:** As Richard or any team member, I want to produce projections for Registrations, Spend, and Clicks — split Brand vs NB — plus ie%CCP, for any time period and any market or region, with derived CPAs falling out of the math consistently, so that every stakeholder conversation works from the same numbers.

#### Acceptance Criteria

1. THE projection engine SHALL accept inputs: (market OR region), time_period, target_mode, target_value, optional uplift modifiers per segment, optional parameter overrides.
2. THE projection engine SHALL produce output: week-by-week values for Brand_Registrations, NB_Registrations, Brand_Spend, NB_Spend, Brand_Clicks, NB_Clicks, plus derived Brand_CPA, NB_CPA, blended_CPA, and ie%CCP; plus aggregated totals for the selected time_period.
3. THE projection engine SHALL lock YTD actual values for weeks already completed (i.e., the current period's actuals are never overwritten by projections).
4. WHEN the target_mode is Spend_Target, THE engine SHALL distribute spend across weeks using the Seasonality_Shape, compute per-week segment CPAs via Elasticity_Curves, and derive Registrations and Clicks.
5. WHEN the target_mode is ieCCP_Target, THE engine SHALL iteratively solve for the total spend that yields the target ie%CCP given the Brand and NB reg projections.
6. WHEN the target_mode is Regs_Target, THE engine SHALL solve for the spend required to produce the target registration count, subject to Elasticity_Curve and ie%CCP feasibility checks.
7. WHEN the scope is a Region (NA, EU5, WW), THE engine SHALL produce projections for each constituent market independently, then sum segments across markets for regional rollups, AND report the regional blended ie%CCP using the regional-sum formula.
8. IF the engine detects that a target is infeasible given constraints (e.g., NB CPA curve cannot support the target regs at any realistic spend), THEN THE engine SHALL return an explicit infeasibility message identifying which parameter is the binding constraint.

### Requirement 3: Portable, self-contained HTML UI

**User Story:** As Richard, I want the projection tool to live as a single HTML file I can open from the Kiro dashboard, upload to SharePoint, embed in Symphony, or send to Lorena as an attachment, so that anyone — human or agent — can access it without needing Kiro itself running.

#### Acceptance Criteria

1. THE MPE UI SHALL be delivered as a single HTML file (`shared/dashboards/projection.html`) with all CSS and JS inlined, except for a single Chart.js CDN reference.
2. THE HTML file SHALL render functionally identically whether served by `serve.py`, opened from a local filesystem, embedded via iframe in SharePoint, or embedded in Symphony.
3. THE HTML file SHALL load its parameters and baseline data from a companion JSON file (`shared/dashboards/data/projection-data.json`) served from the same origin, OR from an embedded `<script type="application/json">` block if served as a fully-standalone attachment.
4. THE HTML file SHALL include a machine-readable Methodology_Manifest (a `<script type="application/json" id="mpe-methodology">` block) containing parameter values used, formulas applied, and output shape, so that agents can parse the page without running JS.
5. THE HTML file SHALL include human-readable metadata in a visible header: title, last parameter refresh date, source data range (YTD weeks covered), and author/owner.
6. THE HTML file SHALL include three input modes — Preset selector (drop-down of Scenario_Presets), Slider mode (sliders for each input), and Target mode (pick target_mode and enter value).
7. THE HTML file SHALL visualize outputs as (a) summary card with key totals, (b) week-by-week line chart for Registrations and Spend, (c) stacked-area chart for Brand-vs-NB contribution, (d) ie%CCP gauge showing current vs target.
8. THE HTML file SHALL NOT make any outbound API call at render time other than the Chart.js CDN.
9. THE HTML file SHALL emit a "Copy as JSON" action that produces a Saved_Projection JSON blob for persistence (via clipboard).
10. THE HTML file SHALL emit a "Copy as markdown summary" action producing a stakeholder-friendly summary (regs, spend, ie%CCP, key caveats).

### Requirement 4: Saved projections with full provenance

**User Story:** As Richard, I want every projection run I care about to save as a durable record with its inputs, parameters-used, and outputs, so that when Lorena asks "what did you tell me on 4/22?" I can retrieve the exact projection, and so that I can compare my 4/22 projection against the actual result three months later.

#### Acceptance Criteria

1. THE MPE SHALL persist Saved_Projections as JSON files at `shared/dashboards/data/projections/{market_or_region}/{yyyy-mm-dd}-{slug}.json`.
2. A Saved_Projection JSON SHALL include: scope (market/region), time_period, target_mode, target_value, all inputs, the Parameter_Set snapshot at projection time, all outputs (weekly and aggregated), timestamp, author.
3. THE MPE SHALL provide a "Save" action in the UI that writes the file via a file-write endpoint in `serve.py`, and a "Copy JSON" action for environments where file-write is unavailable (SharePoint/Symphony).
4. THE MPE SHALL provide a "Load saved projection" dropdown in the UI that lists saved projections for the currently-selected scope, most-recent first.
5. WHEN a saved projection is loaded, THE MPE SHALL restore all inputs, apply them to the current parameter set, and flag any parameters that have changed since the save (e.g., "NB elasticity for DE was refit on 5/15 — your saved projection used the 4/22 curve, reloading with current curve produces different numbers").
6. THE MPE SHALL support a "Compare saved projections" view showing up to three saved projections side-by-side with deltas.
7. THE Saved_Projection JSON SHALL be grep-able for agents — every field keyed with a stable schema documented in the Methodology_Manifest.
8. WHEN a period covered by a Saved_Projection has closed (e.g., a projection for Q2 made in April, and it's now July), THE MPE SHALL support a "Score" action that compares the projection to actual values from `ps.v_weekly` and writes the scored record to `ps.projection_scores`.

### Requirement 5: Quarterly parameter refit as durable process

**User Story:** As Richard, I want the projection engine's parameters to be reviewed and refit on a predictable cadence so that when I show this to leadership next month, I can say "these numbers are current as of last week" with confidence, and so that three quarters from now the tool isn't running on stale math.

#### Acceptance Criteria

1. THE MPE SHALL include a refit job (`shared/tools/prediction/refit_market_params.py`) that, for each market, refits every quarterly parameter using the latest `ps.v_weekly` data, computes Validation_MAPE against the most recent 12-week holdout, and writes the new parameter_version to `ps.market_projection_params`.
2. THE refit job SHALL be invocable manually and SHALL also be schedulable as a hook with quarterly frequency (configurable).
3. THE refit job SHALL produce a refit report at `shared/dashboards/data/refit-reports/{yyyy-mm-dd}.md` listing every parameter changed, the MAPE delta, and any parameters that failed validation thresholds.
4. IF a parameter's new Validation_MAPE exceeds its prior Validation_MAPE by more than 10 percentage points, THEN THE refit job SHALL flag that parameter as a "refit concern" requiring human review before the new version is marked active.
5. THE MPE SHALL include an annual refit procedure documented in a runbook (`shared/wiki/agent-created/operations/mpe-annual-refit-runbook.md`) covering CCP refresh from finance, seasonality re-baselining, ie%CCP target reconfirmation.
6. WHEN a quarterly refit runs, THE refit report SHALL be pushed to SharePoint under `Kiro-Drive/system-state/mpe-refits/` for durability.
7. THE MPE UI SHALL display a "Parameters current as of YYYY-MM-DD" banner at the top, sourced from the most recent `last_refit_at` across all parameters used in the current projection.

### Requirement 6: Regional rollups with mathematical rigor

**User Story:** As Richard, when I project for EU5 or WW, I want the rollup to be computed from per-market projections — not from a blended market average — so that the regional ie%CCP correctly reflects each market's negotiated CCP and the mix effects are honest.

#### Acceptance Criteria

1. THE MPE SHALL compute NA, EU5, and WW projections by producing independent per-market projections for each constituent market, then summing Brand_Registrations, NB_Registrations, Brand_Spend, NB_Spend, Brand_Clicks, and NB_Clicks across markets.
2. THE regional blended ie%CCP SHALL be computed as: `sum(market_spend) / sum(market_brand_regs × market_Brand_CCP + market_nb_regs × market_NB_CCP)` across constituent markets.
3. THE MPE SHALL NOT use a regional-average CCP shortcut for ie%CCP computation. Each market's CCP is applied to that market's reg counts.
4. WHEN a regional projection is produced, THE MPE SHALL also display the per-market breakdown showing each market's contribution to regional totals.
5. WHEN a regional projection is applied with a target_mode other than the per-market natural projection, THE MPE SHALL allow the user to specify whether the target (e.g., "WW at 75% ie%CCP") is imposed at the regional level (solve regional spend to hit regional ie%CCP, distributing across markets proportionally) OR at the per-market level (each market independently solved).

### Requirement 7: Dual-audience consumability (human interactive, agent programmatic)

**User Story:** As either Richard using the UI or an agent querying the projection programmatically, I want consistent access to the same math, the same parameters, and the same outputs, so that the answer to "what's our MX Q2 projection at 75% ie%CCP" is identical whether I click through the UI or an agent pulls it from the data layer.

#### Acceptance Criteria

1. THE MPE SHALL expose a Python API (`shared/tools/prediction/mpe_engine.py`) with a single entry point `project(scope, time_period, target_mode, target_value, **inputs)` returning the same output schema as the HTML UI's JSON output.
2. THE Python API SHALL be importable by any sibling tool (wbr_pipeline.py, refresh-callouts.py, ad-hoc scripts) and SHALL NOT require the UI to be running.
3. THE HTML UI SHALL internally call the same logic (ported to JS) that the Python API uses, with a test suite validating that both produce identical outputs for a canonical set of 20 test cases.
4. THE MPE SHALL include a CLI entry point (`python3 -m shared.tools.prediction.mpe_engine --market MX --period 2026-Q2 --target ieCCP:75`) producing JSON output to stdout, so that shell-based agents and workflows can consume projections.
5. THE Methodology_Manifest embedded in the HTML SHALL be the single source of truth for the output schema — the Python API and the HTML UI both conform to it, and the test suite validates conformance.
6. THE MPE SHALL document in the Methodology_Manifest how an agent can consume the projection — specifically, the JSON path to parameter values, output values, and caveats — so that an LLM agent reading the raw HTML can extract the answer without running JavaScript.

### Requirement 8: Leadership-grade narrative output

**User Story:** As Richard preparing to showcase this to Brandon/Kate/leadership, I want the tool to produce a stakeholder-ready summary that leads with the "so what" and backs it with rigor, so that I can use a single projection run as the basis for a paragraph in a WBR callout, an email to Lorena, or a slide in an OP1 deck.

#### Acceptance Criteria

1. THE MPE SHALL include a "Generate narrative" action that produces a 2-4 paragraph stakeholder summary following Richard's writing style (data-forward, no em-dashes, per-market specificity, explicit "so what").
2. THE narrative SHALL state: the scope, the time period, the target, the central projection (regs, spend, ie%CCP), the confidence range or sensitivity, and at least one explicit caveat or risk.
3. THE narrative SHALL cite the parameter freshness date and the YTD data range informing the projection.
4. THE narrative template SHALL be editable in the Parameter_Set (so per-market narrative tone can vary) and follow the richard-writing-style + richard-style-amazon steering files.
5. THE narrative SHALL explicitly call out when the projection is near a constraint ceiling (ie%CCP within 5% of target), when a parameter is stale, or when the target is infeasible.

### Requirement 9: Safety guardrails for projection quality

**User Story:** As Richard, I want the projection engine to refuse to produce a number when the inputs don't support one, and to warn me loudly when something's off, so that I never hand Lorena a confident-looking number that's built on a broken foundation.

#### Acceptance Criteria

1. IF a market's parameters are missing or all parameters are stale beyond their refit_cadence, THEN THE MPE SHALL refuse to produce a projection for that market and SHALL display which parameters must be refit before projections are possible.
2. IF a target_value is outside the historically-observed range for that market (e.g., spend 3× the highest historical quarterly spend), THEN THE MPE SHALL produce the projection but SHALL prefix the output with a HIGH_EXTRAPOLATION warning.
3. IF an Elasticity_Curve's Validation_MAPE exceeds 40%, THEN THE MPE SHALL produce projections using that curve but SHALL label the output as LOW_CONFIDENCE and expand the reported error bands accordingly.
4. IF fewer than 8 weeks of YTD actuals are available for the current year (e.g., early-year projections), THEN THE MPE SHALL rely more heavily on prior-year seasonality and SHALL label the projection as SEASONALITY_DOMINATED.
5. WHEN any guardrail fires, THE MPE SHALL surface the warning both in the UI (visible banner) and in any Copy-as-JSON / Copy-as-markdown output.

### Requirement 10: Deployment and discoverability

**User Story:** As the team or leadership looking for the projection tool, I want to find it in the places I already look — the Kiro dashboard nav, SharePoint Artifacts, and a wiki article — so that once this ships, I don't need to be told where it lives.

#### Acceptance Criteria

1. THE MPE UI SHALL be accessible from the Kiro dashboard `index.html` nav as a top-level tab labeled "Projections".
2. THE MPE UI SHALL be published to SharePoint `Kiro-Drive/Artifacts/strategy/projection-engine.html` with the companion JSON data file.
3. THE MPE SHALL have a wiki article at `shared/wiki/agent-created/operations/market-projection-engine.md` documenting purpose, usage, methodology at a glance, and where to find the tool in each environment.
4. THE wiki article SHALL be published to SharePoint via the existing sharepoint-sync process.
5. THE agent-bridge repository SHALL include the MPE spec and wiki article (Cold_Start_Safe), so that a new agent on another platform can reconstitute the intent even if the HTML tool itself is environment-specific.

### Requirement 11: Multi-year projection with recency-weighted YoY trend

**User Story:** As Richard preparing OP1 or multi-year strategic conversations, I want the engine to project 1-3 years forward using recency-weighted historical data so that the model understands how each market has naturally grown and applies that growth (not just current-year seasonality) to future years.

#### Acceptance Criteria

1. THE MPE SHALL support a Multi_Year time_period option producing projections for 1, 2, or 3 future fiscal years (configurable).
2. THE MPE SHALL maintain a YoY_Growth_Trend parameter per market per segment (Brand, NB), fit from 2-4 years of historical `ps.v_weekly` data.
3. THE YoY_Growth_Trend fit SHALL use recency-weighted regression with an exponential decay half-life (default 52 weeks) so that recent years dominate but prior years still inform the trend.
4. WHEN a Multi_Year projection is requested, THE engine SHALL apply YoY_Growth_Trend multiplicatively across years while preserving within-year seasonality shape.
5. THE YoY_Growth_Trend parameter SHALL be refit quarterly alongside other historical parameters.
6. IF a market has fewer than 104 weeks of data (2 years), THEN THE engine SHALL emit a LOW_CONFIDENCE_MULTI_YEAR warning and fall back to flat YoY (no growth).
7. WHERE structural change is detected in a market's history (e.g., a regime shift like MX 2025 H1→H2), THE MPE SHALL allow the user to specify a break-point after which prior history is excluded from the YoY_Growth_Trend fit.
8. THE engine SHALL report YoY_Growth_Trend confidence explicitly (strong / moderate / weak) in the output based on r_squared and data-range sufficiency.

### Requirement 12: Bayesian credible intervals on projection outputs

**User Story:** As Richard or any stakeholder reading a projection, I want every output KPI to carry an explicit uncertainty range reflecting model-parameter uncertainty, so that I can honestly say "regs will land between X and Y with 70% credibility" instead of "regs will be Z."

#### Acceptance Criteria

1. THE MPE SHALL model each fitted parameter (elasticity coefficients, CPA baselines, CPC baselines, seasonality weights, YoY trend) with a posterior distribution from its historical fit.
2. WHEN a projection is produced, THE engine SHALL propagate parameter uncertainty via Monte Carlo sampling (default 1000 samples) to produce Bayesian_Credible_Intervals for every output KPI.
3. THE engine output SHALL include 50%, 70%, and 90% credible intervals for Registrations, Spend, Clicks, CPA, and ie%CCP at each time grain (week, month, quarter, year, multi-year).
4. THE credible intervals SHALL be visualized in the UI as shaded bands around line charts and as "X — Y" ranges on summary cards.
5. WHERE credible intervals are extremely wide (90% interval width > 2× the central estimate), THE MPE SHALL emit a HIGH_UNCERTAINTY warning and surface which parameter's posterior is driving the width.
6. THE credible interval computation SHALL be a separate module (`mpe_uncertainty.py`) so it can be improved, replaced, or disabled without touching the core engine.
7. THE Python and JS implementations of credible intervals SHALL be validated by the parity test suite with tolerance widened to 2% (sampling noise is inherent).
8. WHERE a parameter's posterior is effectively a point estimate (no uncertainty, e.g., a negotiated CCP), THE engine SHALL treat it as fixed and not sample from it.

### Requirement 13: Anomaly detection on parameter refits

**User Story:** As Richard relying on the quarterly refit to keep parameters current, I want the refit job to loudly flag any parameter whose value has shifted unexpectedly between versions, so that a data bug or a mis-fit doesn't silently corrupt every downstream projection.

#### Acceptance Criteria

1. WHEN the quarterly refit job produces a new parameter_version, THE job SHALL compare the new value against the trailing distribution of prior versions for that same parameter.
2. IF the new value is more than 3 standard deviations away from the trailing mean (default window: last 4 quarterly refits), THEN THE refit job SHALL flag the parameter as an anomaly candidate.
3. Anomaly-flagged parameters SHALL NOT be marked active in `ps.market_projection_params` until Richard (or a designated reviewer) approves them.
4. THE refit report SHALL include an "Anomalies" section listing every flagged parameter with: prior values, new value, delta, standard-deviation distance, and a plain-language explanation (e.g., "DE NB CPA elasticity coefficient jumped from 0.92 to 1.34 — a 60-std-dev move — suggesting a regime change or fit failure").
5. Anomaly detection SHALL apply to historical-fit parameters (CPA baselines, elasticity coefficients, CPCs, seasonality weights, YoY trends) and SHALL NOT apply to negotiated parameters (CCPs, ie%CCP targets).
6. WHERE a regime change is known to have occurred (e.g., a placement launch, a campaign strategy change), THE MPE SHALL allow the user to document the regime change in `ps.regime_changes` AND mark anomalies in the same period as "expected-anomaly" instead of "investigate-anomaly".
7. THE anomaly detection module SHALL be testable in isolation — the test suite SHALL include synthetic anomalies (both true-positive and false-positive) and validate that the detector catches/rejects them correctly.

### Requirement 14: Per-market supported target modes and per-market/region narrative templates

**User Story:** As Richard producing stakeholder output, I want each market and each region to have its own narrative template reflecting its strategic context (MX = ie%CCP-bound, AU = efficiency-first, JP = Brand-dominant, regional rollups = mix interpretation), so that the narrative output is decision-ready rather than generic.

#### Acceptance Criteria

1. THE `ps.market_projection_params` registry SHALL include a `supported_target_modes` parameter per market listing which target modes are valid (e.g., AU supports `spend` and `regs` but not `ieccp`; MX supports all three).
2. THE MPE UI SHALL dynamically show or hide target-mode options based on the selected market's `supported_target_modes`.
3. THE MPE SHALL store a `narrative_template` parameter per market AND per region in `ps.market_projection_params`, each containing a per-context prose template.
4. THE narrative template SHALL accept placeholders for projection outputs, parameter freshness, confidence levels, and strategic framing (e.g., ie%CCP-bound vs efficiency vs brand-dominant).
5. WHEN the engine generates narrative for a region (NA/EU5/WW), THE engine SHALL use the regional template, NOT a concatenation of per-market narratives.
6. THE regional narrative template SHALL explicitly surface mix effects — e.g., "EU5 delivered X regs with DE +A% and IT -B% driving the mix shift" — rather than reporting only the aggregate.
7. THE UI SHALL allow the user to preview any market's or region's narrative template before running a projection, so the output shape is predictable.
8. Each per-market narrative template SHALL be no longer than 300 words in expanded form and MUST follow richard-writing-style (no em-dashes, data-forward, explicit "so what").


### Requirement 15: Rigorous end-to-end acceptance test per market and region

**User Story:** As Richard preparing to showcase this to leadership, I want the acceptance test to simulate the kinds of conversations I actually have with Lorena, Yun-Kang, Andrew, and Stacey so that every market can withstand the same pressure-testing I put the MX projection through on 2026-04-22.

#### Acceptance Criteria

1. THE MPE SHALL include an acceptance test suite that runs the full "stakeholder conversation simulation" for each market (US, CA, UK, DE, FR, IT, ES, JP, MX, AU) and each region (NA, EU5, WW), per the test script below.
2. For each market and region, THE acceptance test SHALL execute the following sequence and assert expected behavior at each step:
   - (a) Load YTD actuals and current parameters. Verify parameter freshness < refit_cadence for all historical-fit parameters.
   - (b) Run base projection for each of Week (next), Month (current), Quarter (current), Year (current), Multi_Year (1 year forward). Assert no errors, no infeasibility.
   - (c) Apply Spend_Target equal to 2× annual OP2 budget. Assert the engine emits HIGH_EXTRAPOLATION and produces Bayesian CI widths > 2× central estimate, triggering HIGH_UNCERTAINTY.
   - (d) Apply ieCCP_Target at the market's configured target (MX 100%, EU5-markets 50-65%, etc.) for the annual scope. Assert the resulting spend is within 2× of prior-year actual annual spend (sanity envelope).
   - (e) Apply Regs_Target equal to 1.5× prior-year actual regs. Assert the engine either converges to a feasible spend OR returns structured infeasibility identifying the binding constraint.
   - (f) Apply a Brand uplift of +30% (simulating a placement launch). Assert Brand regs projection increases proportionally while NB projections remain within prior uncertainty bands.
   - (g) Apply a NB CPA elasticity override with doubled slope (simulating unusually poor efficiency). Assert the engine re-solves and that NB spend in the output shifts appropriately.
   - (h) Save the projection from step (d). Reload it. Assert all inputs, parameters, and outputs match exactly.
   - (i) Modify a parameter to a stale or missing state. Re-run projection. Assert the engine surfaces the staleness/missing warning in UI, JSON, and markdown output.
   - (j) Run the narrative generator for the projection from step (d). Assert the narrative is 2-4 paragraphs, contains no em-dashes, cites parameter freshness, and includes at least one explicit caveat.
3. For each regional scope (NA, EU5, WW), THE acceptance test SHALL additionally execute:
   - (k) Run projection with regional-level target mode (e.g., "EU5 at 60% ie%CCP"). Assert mathematical correctness of the sum-then-divide formula against hand-computed expected values.
   - (l) Run projection with per-market-level target mode applied uniformly (e.g., "every EU5 market at its own ie%CCP target"). Assert regional output is the sum of independent per-market solutions.
   - (m) Assert that regional narrative output specifically calls out mix effects (per Requirement 14.6).
4. THE acceptance test SHALL simulate the back-and-forth iterative refinement observed in the MX 2026-04-22 session for at least MX and one other market (e.g., DE). The simulation SHALL include:
   - Initial projection request
   - Challenge: "why is my projection higher than the user's mental model of $X?"
   - Parameter correction (simulate swapped CCPs being corrected)
   - Formula correction (simulate blended vs reg-weighted)
   - Regime-shift identification (e.g., 2025 H1 vs H2 regime change)
   - Seasonality refinement (Brand as demand-clean baseline)
   - CPA elasticity fit
   - Week-by-week re-run
   - Error-band application (both symmetric and asymmetric)
   - Marginal-regs sanity check
   - Final recommendation within defensible range
5. THE acceptance test SHALL assert that each of the above iterative challenges either (a) produces a changed output consistent with the refinement, or (b) produces a documented "cannot improve further" response explaining why the current projection is already calibrated.
6. THE acceptance test suite SHALL run in under 15 minutes for the full matrix and in under 2 minutes for a single-market quick-check (`pytest shared/tools/prediction/tests/test_acceptance.py -k MX`).
7. THE acceptance test results SHALL be logged to `shared/dashboards/data/acceptance-test-reports/{yyyy-mm-dd}-{market}.md` with pass/fail details per step, so that any degradation between test runs is auditable.
8. THE acceptance test SHALL be a pre-commit requirement for changes touching the engine core (`mpe_engine.py`, `mpe_engine.js`, `ps.market_projection_params` schema).
9. WHERE a market lacks sufficient historical data to pass all steps (e.g., a market with < 104 weeks of data), THE acceptance test SHALL allow those steps to be marked XFAIL with an explicit reason recorded in the registry.
10. THE acceptance test suite SHALL itself be reviewed quarterly alongside the refit job, so that new stakeholder-conversation patterns get added to the test as they emerge in real work.
