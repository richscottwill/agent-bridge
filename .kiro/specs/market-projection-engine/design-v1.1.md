# Design Document — MPE v1.1 (Brand-Anchor / NB-Residual Architecture)

> **Status**: v1.1 re-architecture proposal, 2026-04-23. Supersedes the top-down elasticity model in `design.md` sections covering the target solver and parameter decomposition. v1 remains the historical record; v1.1 is the active design going forward.
>
> **Scope of this document**: the modeling layer and solver. The Parameter Layer, Engine/JS mirror pattern, portability properties, UI shell, quarterly refit cadence, and parity testing approach from v1 are retained unchanged — see `design.md` for those. What changes here is the mathematical identity the solver enforces and the Brand-side fit.

## Why v1.1 exists

v1 modeled Brand and NB as peer channels, each with its own CPA elasticity curve, with a fixed historical spend-share between them. The solver took a total spend or an aggregate ie%CCP target, allocated via spend-share, projected each channel independently through its elasticity curve, and summed the results.

This architecture produced defensible numbers under stable conditions and catastrophic numbers under regime change. The empirical break point was the MX Y2026 projection on 2026-04-23: at a 75% ie%CCP target the solver returned $443K spend against a domain-expert range of $800K–$1.2M. The gap wasn't a solver bug or a data issue — the model was solving the wrong problem. It was fitting aggregate local responsiveness across regime-incompatible weeks and treating Brand and NB symmetrically when they aren't symmetric in operations.

The deeper issue is that Brand and NB are not peers. Brand has trend momentum and seasonal rhythm, both learnable from multi-year history. NB is the lever operators move to hit targets (OP2, ie%CCP, regs). The model should reflect that asymmetry.

## Model identity

For any market and time period:

```
brand_regs            = BrandTrajectoryModel(market, time_period, qualitative_priors)
brand_CPA             = BrandCPAProjection(market, time_period)                         # ~constant per regime
brand_spend           = brand_regs × brand_CPA

# NB is the residual that hits the target:
nb_spend              = NBSolver(target_mode, target_value, brand_regs, brand_spend, market_params)
nb_regs               = nb_spend / nb_CPA(nb_spend)

total_spend           = brand_spend + nb_spend
total_regs            = brand_regs + nb_regs
blended_CPA           = total_spend / total_regs
ieccp                 = total_spend / (brand_regs × brand_CCP + nb_regs × nb_CCP)
```

The Brand projection is the anchor. It runs on its own logic — seasonality, trend, regimes, qualitative priors — independent of any target. The NB residual is solved given the Brand projection and the target constraint. This matches how the team reasons operationally: project Brand from fundamentals, then allocate NB spend to hit the desired ie%CCP / OP2 / regs target within operational bounds.

**ie%CCP is not in the equation as a driver.** It's a target outside the system, same category as OP2 spend targets or OP2 registration targets. The solver consumes it as a constraint and computes the NB spend that satisfies it. If the target is unreachable under operational bounds, the solver returns the closest-feasible answer with a warning — it does not silently compromise.

## Solver branches

The NB solver selects a branch based on `target_mode`:

| target_mode | Target value | Solver identity | Typical market |
|---|---|---|---|
| `ieccp` | Target ie%CCP (e.g. 1.00 = 100%) | `nb_spend` = value such that `ieccp_computed == target` | MX, EU5, JP, CA, US |
| `regs` | Target total regs | `nb_spend` = value such that `total_regs == target` (solver closes via NB CPA elasticity) | AU, also any market doing OP2 regs check |
| `spend` | Target total spend | `nb_spend = target − brand_spend` (no solver, direct) | Any market, scenario mode |
| `op2_efficient` | OP2 regs target, bounded by OP2 budget | Maximize regs toward OP2 target subject to `total_spend ≤ OP2 budget` | AU primary mode |

Note what's no longer needed: the `brand_spend_share` parameter is gone. Each channel's spend is computed from first principles (Brand from regs × CPA; NB from the residual). No aggregate spend-to-channel split required.


## Brand Trajectory Model

This is the component that most replaces v1. Instead of a single recency-weighted elasticity fit averaging across regimes, Brand regs are projected through a **blended-evidence fit** combining four explicit evidence streams with named weights.

### The four evidence streams

**1. Seasonal prior** (percentage-change shape from prior years)

Source: prior years' Brand weekly data, regime-filtered to exclude anomalous weeks.

Output: for each week-of-year `w`, a multiplier `seasonal[w]` relative to the same market's annual mean, expressed as a percentage change vs the prior week and vs the same week last year. This captures "Brand typically drops 11% W15/W16 before rebounding W17" — the annual rhythm.

Computation: for each prior year (minimum 2, ideally 3), compute per-week regs normalized to that year's mean. Average across years. Regime weeks with `end_date` in the past are included; active-structural weeks (Polaris baseline, Sparkle onset) are tagged and the seasonal multiplier is computed separately per regime segment when regime breaks exist within the year.

Stored in `ps.market_projection_params` as `brand_seasonal_prior` (JSON). Refit annually in January using the full prior-year history.

**2. Recent trend** (level and slope from current regime)

Source: last N weeks of the current regime, where N is the minimum of (weeks-since-latest-regime-event, 16).

Output: an intercept (current level of Brand regs per week, smoothed over last 4 weeks) and a slope (log-linear weekly growth rate). The intercept is the anchor; the slope reflects the near-term trajectory within the current regime.

Computation: OLS fit on the last N weeks, with a recency weighting (half-life 4 weeks — tighter than the seasonality fit because we want responsiveness here). Stored as `brand_recent_trend` (JSON). Refit weekly as part of the callout pipeline, not quarterly — this is where the engine stays current.

**3. Regime segments** (level shifts from `ps.regime_changes`)

Source: the regime_changes table, filtered to `market=X AND is_structural_baseline=TRUE AND active=TRUE`.

Output: for each structural regime event, a level-shift multiplier representing the step change in Brand baseline when that regime took effect. For example, Polaris INTL MX (2025-08-28) might show a Brand baseline ~1.4× its pre-launch level; Sparkle (2026-01-01, to be formalized as regime row) might show another 1.8× on top.

Computation: for each structural_baseline row, compare the 8-week Brand mean before and after the change_date. The ratio is the regime multiplier. Stored in `brand_regime_multipliers` (JSON) keyed by regime_id.

**4. Qualitative priors** (user-selectable forward scenarios)

Source: user input at projection time. Not stored as a parameter; passed through as part of the ProjectionInputs struct.

Output: a scenario-specific modifier applied to the projected Brand trajectory. Examples:
- `sparkle_sustained`: keep Sparkle-era level + slope through projection period (default)
- `sparkle_decays_12w`: apply exponential decay with half-life 6 weeks toward pre-Sparkle baseline
- `new_placement_landing`: step-up of X% at specified week
- `oci_coming`: level-shift of +Y% at specified week (for markets about to launch OCI)
- `polaris_retained` (AU-specific): skip the scheduled Polaris-reversion event

Each scenario is a named dict with a closed-form trajectory modifier. Documented in a YAML file (`shared/tools/prediction/qualitative_priors.yaml`) so the catalog is transparent and extensible without code changes.


### The blended fit

For each projection week `w` in the target period, Brand regs are computed as:

```
brand_regs[w]  =  annual_baseline
                × seasonal_multiplier[w]          × W_seasonal
                × recent_trend_multiplier[w]      × W_trend
                × regime_multiplier               × W_regime          # always 1.0 × W_regime if no regime event
                × qualitative_prior_multiplier[w] × W_qualitative
```

where the weights `W_seasonal`, `W_trend`, `W_regime`, `W_qualitative` sum to 1.0 and default to:

- `W_seasonal = 0.40`
- `W_trend = 0.40`
- `W_regime = 0.15`
- `W_qualitative = 0.05` (default — increases when user selects a non-default scenario)

**The weights are surfaced in the UI.** Richard can adjust them per projection run. Default weights reflect the stance "seasonality and recent trend carry equal weight; regime multipliers are real but typically already absorbed into recent trend if the event was weeks ago; qualitative priors are a planner override that gets dialed up deliberately, not by default." When a user selects a scenario like `sparkle_decays_12w`, the UI raises `W_qualitative` to 0.20 and rebalances the others.

The multiplicative structure means each stream scales the others. The annual baseline is set so that `brand_regs` summed across 52 weeks hits the full-year projection when all weights are at default and all multipliers are 1.0. Calibrated at refit time.

Implementation: `BrandTrajectoryModel` is a deterministic function taking (market, time_period, qualitative_prior_name, weights_override) and returning per-week regs. Pure function for easy testing. Outputs also include a **contribution breakdown** — "Brand W22 regs 1,038: 41% seasonal, 38% trend, 18% regime, 3% prior" — surfaced in the UI Parameters modal so you can see why a projection is what it is.

### Brand CPA projection

Brand CPA is materially more stable than NB CPA. In MX 2026, Brand CPA has stayed $15-25 across a 5× spend range ($3K to $6K weekly). It doesn't need an elasticity curve.

Projection: Brand CPA = rolling 8-week median of actual Brand CPA, by regime segment. Stored as `brand_cpa_projected` (scalar per market, refit weekly). A single value, not a function of spend.

If Brand CPA shifts structurally (new keyword strategy, major bidding change), the refit picks it up within 8 weeks. If the shift is large and sudden, a regime row is added and the projection segments.


## NB Residual Solver

Given `brand_regs` and `brand_spend` from the Brand Trajectory Model, solve for NB spend to hit the target.

### Branch: ie%CCP target

Solve for `nb_spend` such that:

```
ieccp_target = total_spend / (brand_regs × brand_CCP + nb_regs × nb_CCP)
```

where `total_spend = brand_spend + nb_spend` and `nb_regs = nb_spend / nb_CPA(nb_spend)`.

Using `nb_CPA(nb_spend) = exp(a + b × log(nb_spend))` from the NB CPA elasticity fit, this is a one-dimensional root-finding problem in `nb_spend`. Solve via bisection or Brent's method over the range `[min_weekly_nb_spend × n_weeks, max_weekly_nb_spend × n_weeks]` from `ps.market_constraints_manual` (Mechanism A bounds, retained from v1).

Operational bound behavior: if the target is unreachable under bounds (e.g. 75% ie%CCP requires NB spend below the floor), return the closest feasible NB spend and emit `TARGET_UNREACHABLE_UNDER_BOUNDS` with the computed actual ie%CCP. Do not compromise silently.

### Branch: regs target

Solve for `nb_spend` such that `brand_regs + nb_regs = target_regs`, same root-finding structure. Used for AU and for "how much spend to hit X OP2 regs" scenarios.

### Branch: spend target

Direct: `nb_spend = target_spend − brand_spend`. No solver needed. Used when user is running a scenario with a fixed total budget. Emit warning if `nb_spend < min_weekly_nb_spend × n_weeks` (spend allocation leaves NB under-funded).

### Branch: op2_efficient (AU default)

AU doesn't have an ie%CCP target. The goal is to hit OP2 regs efficiently within OP2 budget.

```
total_budget = OP2_spend_target              # from ps.targets
target_regs = OP2_regs_target                # from ps.targets
nb_spend_available = total_budget - brand_spend
nb_regs_at_budget = nb_spend_available / nb_CPA(nb_spend_available)
projected_regs = brand_regs + nb_regs_at_budget
```

Outputs include `regs_vs_op2` (projected vs target) and `spend_vs_op2` (budget utilization). AU's Key Performance Indicator is `projected_regs / OP2_regs_target` — efficiency-to-target.

### NB CPA elasticity (retained)

The NB CPA elasticity fit (log-linear, recency-weighted, regime-filtered) is retained from v1. It's the right tool for NB because NB *is* responsive to spend changes in a way Brand isn't. The v1 fit method stays — the thing that changes is how the fit's output is used. It's no longer the primary driver of NB regs; it's the closure equation for the NB residual solver.


## Regional Aggregation

Regional projections (NA, EU5, WW) are built up from per-market projections, same as v1. Changes for v1.1:

**Default mode: per-market local optimization, summed.** Each market hits its own ie%CCP target. Regional totals = sum of per-market. Regional ie%CCP is computed post-hoc from summed CCP-weighted regs. This is the default because it respects Lorena-style per-market stewardship: each market's lever is moved to hit that market's target.

**Optional mode: region-level ie%CCP target with cross-market rebalance.** User specifies a regional ie%CCP target. The engine solves for NB spend per market such that the regional weighted ie%CCP hits the target, while minimizing deviation from each market's home ie%CCP target. Implemented as constrained optimization (scipy.optimize); non-trivial to do well. Phase 2 of v1.1, not in the initial build.

Regional Brand projections stay straightforward — sum per-market Brand trajectories. No special regional Brand modeling.

### Regional scope constraints

- `NA` = {US, CA}. Both have ie%CCP tracking. MX is tracked standalone (reported as its own unit, not rolled into NA) because ABPS reporting treats MX/LATAM as a separate column from North America. Reaffirmed 2026-04-25 — production code `REGION_CONSTITUENTS['NA'] = ['US', 'CA']` is canonical; the earlier draft of this doc incorrectly folded MX into NA.
- `EU5` = {UK, DE, FR, IT, ES}. All five have ie%CCP — full support.
- `WW` = {all 10 markets including AU and JP}. AU has no ie%CCP. Regional ie%CCP calculation excludes AU from numerator and denominator (existing behavior from v1 R6.6 / D16 regional rollup). AU shows up in the regional total spend and regs but not in the ie%CCP ratio.

## AU handling

AU is a first-class citizen in v1.1 with its own solver branch rather than a special case bolted on top.

- Target mode defaults to `op2_efficient` (not ie%CCP, not spend, not regs — a specifically-AU mode).
- Supported target modes: `op2_efficient`, `regs`, `spend`. Not `ieccp`.
- Seasonality uses the Southern Hemisphere hybrid logic from v1 (AU-real weeks + NH-shifted-26 fallback). Retained unchanged.
- Brand trajectory model applies with no structural differences — AU has Brand regs, they follow seasonality, they trend, they have regimes (Polaris launch date, hypothetical retention).
- Qualitative prior `polaris_retained` is AU-specific and lets the planner override the scheduled Polaris-reversion regime event.

## Migration from v1

### What v1 components stay

Retained unchanged:
- Parameter Layer tables (ps.market_projection_params, ps.parameter_validation, ps.parameter_anomalies, ps.projection_scores, ps.regime_changes, ps.market_constraints_manual)
- Python/JS mirror pattern, portability guarantees
- UI shell: projection.html, target triad, provenance modal, Chart.js stacked chart
- Quarterly refit cadence via `kiro hook run mpe-refit`
- Parity testing framework (Python ↔ JS numerical agreement)
- NB CPA elasticity fit method (log-linear, recency-weighted, regime-filtered)
- Seasonality fit method (recency-weighted annual shape, though consumed differently now)
- Mechanism A operational bounds (min/max weekly spend per segment)
- Narrative generation pipeline and strategy-type templates
- 5-regime-event exclusion logic in `_fetch_weekly`
- Credible intervals via Monte Carlo (mpe_uncertainty.py)


### What v1 components get replaced

Replaced in v1.1:
- **Top-down elasticity solver** — `_solve_ieccp_target` in current mpe_engine.py. Replaced by `BrandTrajectoryModel` + `NBResidualSolver` (new modules). The v1 solver is deleted when v1.1 ships, not kept as a fallback — maintaining two models doubles the maintenance burden without winning anything.
- **Brand CPA elasticity fit** (`brand_cpa_elasticity` parameter) — deprecated. Replaced by `brand_cpa_projected` (scalar per regime segment). Brand CPA was never meaningfully elastic in the spend ranges we operate in.
- **Brand CPC elasticity fit** — deprecated. Brand CPC is projected from recent run-rate the same way Brand CPA is.
- **Brand YoY growth scalar** — deprecated. Year-over-year signal now lives in the seasonal-prior evidence stream (as percentage-change shape), combined with recent-trend evidence, not as a standalone growth multiplier.
- **`brand_spend_share` parameter** — deprecated. Brand/NB split is no longer an aggregate property; it emerges from the solver.
- **Regional "percent of markets" rollup** — replaced by sum-then-divide with proper AU handling on the regional ie%CCP denominator.

### New parameters introduced

Added in v1.1 to `ps.market_projection_params`:
- `brand_seasonal_prior` (JSON) — per-week percentage-change shape, computed from prior years, annual refit
- `brand_recent_trend` (JSON) — current-regime level + slope, weekly refit during callout pipeline
- `brand_regime_multipliers` (JSON) — level-shift multipliers keyed by regime_id, refit on regime row insert/update
- `brand_cpa_projected` (scalar) — rolling median Brand CPA per regime segment, weekly refit
- `brand_trajectory_weights` (JSON) — default blend weights `{W_seasonal, W_trend, W_regime, W_qualitative}` per market. User overrides are scoped per-projection, not persisted.

### User-facing changes

- **Projection UI shows the contribution breakdown.** When projecting MX Y2026 at 100% ie%CCP, the user sees: Brand = 11,200 regs (45% seasonal / 42% trend / 10% regime / 3% prior), NB = 6,400 regs solved via NB elasticity to hit ie%CCP 100%. Each component is inspectable.
- **Qualitative scenario picker** is a new UI control on the projection page. Default is `current_regime_continues`. Users can switch to `sparkle_decays_12w`, `new_placement_landing`, etc. The Parameters modal surfaces the selected scenario + its trajectory modifier.
- **Blend weight sliders** in an "Advanced" section of the input panel. Default hidden; expandable when the user wants to stress-test how much their seasonal prior is driving the number.
- **"Why this number" explanation** surfaces the blended-evidence breakdown as a one-paragraph prose rendering in the narrative block. The goal is to let Brandon or Lorena read the projection and understand the mix of evidence behind it, without needing to open the modal.


## Validation Plan

The v1.1 model gets validated the same way v1 does (12-week holdout MAPE per segment), but the accountability target is different:

- **Brand projection MAPE < 20%** on 12-week holdout across all 10 markets. This is the core claim: the blended-evidence Brand model beats naive recency and naive prior-year anchoring.
- **Aggregate projection MAPE < 25%** on 12-week holdout, measured on `total_regs` given actual spend. The NB solver takes actual spend as input and we check whether projected regs match observed.
- **Regime-crossing holdouts** are called out separately. We don't claim the model handles regime transitions perfectly — we claim it handles them better than v1 by making the regime segmentation explicit rather than implicit in a fit window.

### Test scenarios for acceptance

1. **MX Y2026 @ 75% ie%CCP** returns a spend in the $800K–$1.2M range (the domain-expert range that v1 missed). If the model still returns $443K or $1.5M, something is wrong with the Brand trajectory or the solver.
2. **MX Q3 2025 backtest with W26-cutoff** (just before the ie%CCP gate flip): project forward 12 weeks under `ieccp_gate_flipping` qualitative prior. Compare to actuals. This tests the qualitative-prior mechanism.
3. **AU Y2026 @ OP2 efficient** returns a regs projection within ±15% of OP2 regs target, at spend ≤ OP2 budget. If AU is projected to miss OP2 by 50% under its budget, the model needs an `efficiency_shortfall` warning.
4. **Regional rollup**: NA regional projection at regional ie%CCP = 100% returns per-market NB allocations that reconcile exactly to the region total (numerical closure test).
5. **Qualitative scenario sensitivity**: MX Y2026 under `sparkle_decays_12w` returns a lower total regs than under `sparkle_sustained` (directionality test, not an exact-number test).

## Open questions deferred to v1.2

- **Probabilistic uncertainty on Brand trajectory.** v1.1 Monte Carlo uses the NB elasticity posterior covariance for NB regs CIs, but the Brand projection is currently deterministic (four weighted evidence streams, no uncertainty propagation). v1.2 could treat the weights themselves as random variables drawn from user-specified priors and propagate through.
- **Cross-market spillover.** When MX Sparkle lifts Brand, does LATAM see a spillover? Currently no — each market is modeled independently. v1.2 could support a shared latent-demand factor across markets in the same region.
- **Automatic regime detection.** Today regimes are manually inserted into `ps.regime_changes`. v1.2 could propose candidate regime events from changepoint detection on the weekly data, requiring operator confirmation before activation.
- **Multi-year projections (MY2/MY3).** v1.1 focuses on sub-year and annual projections. The VERY_WIDE_CI warning from v1 (R11.8) is retained. v1.2 could introduce a proper multi-year growth model with structural assumptions about maturation, OCI trajectories, etc.
- **Cannibalization adjustment.** When Brand grows significantly (Sparkle), some NB searches shift to Brand. v1.1 treats this as implicit in the NB CPA elasticity curve — higher spend → higher NB CPA partly because Brand absorbed cheap searches. v1.2 could model a small Brand-to-NB cannibalization factor explicitly.

## Principle: decision-support, not decision-maker

The model's job is to keep planning decisions grounded in data, not to replace judgment. The blended-evidence Brand trajectory is designed so that a planner looking at the output can immediately see:
- What the prior-year seasonal shape says
- What recent weeks are trending
- What regime events have shifted the baseline
- What qualitative assumption the planner is layering on top

When the planner's intuition disagrees with the model, the UI makes the disagreement legible — "I think Brand will drop 8% W22, but the model says +2% because last year's seasonality was flat there; the regime multiplier is 1.15 and the trend slope is weak." The planner can adjust weights, swap qualitative prior, and see what it takes to make the model match their view.

The engine is a thinking partner. If it produces a number a domain expert says is wrong, the expert is usually right and the engine is showing you which evidence stream is misrepresenting reality. That's the whole point.

## Implementation Phasing

v1.1 build lives in a new Phase 6 in `tasks.md` (see that file for the broken-down tasks). High-level sequence:

1. **Phase 6.1**: Build `BrandTrajectoryModel` module as standalone, tested against a synthetic market, then against MX 2025 backtest.
2. **Phase 6.2**: Build `NBResidualSolver` with all four branches, tested independently.
3. **Phase 6.3**: Replace v1 solver in `mpe_engine.py` and `mpe_engine.js` (both paths swapped together to keep parity).
4. **Phase 6.4**: Extend parameter registry and fit pipeline for new `brand_seasonal_prior` / `brand_recent_trend` / `brand_regime_multipliers` / `brand_cpa_projected` parameters. Deprecate and drop v1-only parameters.
5. **Phase 6.5**: UI — contribution breakdown, qualitative scenario picker, blend weight sliders, "why this number" narrative.
6. **Phase 6.6**: Validation pass on all 10 markets. Acceptance test battery runs green.
7. **Phase 6.7**: Migrate live callout pipeline + WBR callouts + Lorena email pipeline to the v1.1 engine. Retire v1 code.

Estimate: 3-4 weeks of focused work. Demo date not on the critical path since v1.1 is a post-demo improvement, not the demo blocker.

## What's not in this document

- Specific pseudocode for the Brent's method NB solver (standard numerical method, cited at implementation time)
- Exact blend weight defaults per market (Phase 6.1 task, calibrated from backtest)
- YAML schema for qualitative priors (Phase 6.5 task)
- UI wireframes for the contribution breakdown display (Phase 6.5 task)

These belong in the tasks.md entries and in the implementation PRs, not in the high-level design doc.

---
*Document owner: Richard Williams. Drafted 2026-04-23 after the MX Y2026 @ 75% failure made the v1 architectural gap concrete. Supersedes the top-down elasticity architecture in `design.md` for new projection work starting Phase 6.*



---

## Destination arc — v1.2 → v1.4 (sequencing, no dates)

Amended 2026-04-26 after Phase 6.5.8.

v1.1 Slim is structurally **frequentist** (point estimates, Monte-Carlo CI band around deterministic projections). The Bayesian layers below expand the uncertainty treatment and the structural priors in sequence. Dates deliberately omitted — each layer only ships once the prior one has stabilized against real forecast-scoring signal from the v1.1 feedback bar.

### v1.2 — Skeleton posterior + change-point detection

- **Skeleton posterior (Level 1 Bayesian)**: explicit priors on Brand trend slope, regime peak multiplier, NB elasticity exponent `b`. Posteriors updated from each weekly fit cycle. The "skeleton" is the flat parameter-list structure — no hierarchy across markets yet.
- **BOCPD (Bayesian online change-point detection)**: replace the hand-curated `ps.regime_changes` onset dates with an automatic detector that proposes candidate onsets from the weekly series. Richard reviews + accepts/rejects via the feedback triage queue (6.5.4 pattern extended).
- **Probabilistic decay curves**: the current `half_life_weeks` is a point estimate. v1.2 replaces it with a posterior over decay-life, so projections with a wide decay posterior produce wider CI bands — quantifying "we don't know how fast this lifts fades."

### v1.3 — Hierarchical priors

- **Joint posterior across markets**. A prior on "typical OCI lift magnitude" gets shared across US/UK/DE/etc., so individual markets with little post-OCI data (FR, ES post-2026-03-30) borrow from peers.
- **Data-sparse markets** (AU 29 weeks of history, JP low-NB-CV): hierarchical pooling means AU's trend slope is pulled toward the WW median when its own fit is noisy. Phase 6.1 JS `listRegimesWithConfidence` already does per-regime confidence decay; v1.3 generalizes this to cross-market pooling.

### v1.4 — parked

- **Autonomous skeleton switching**: the model swaps between skeleton structures (say, Brand-Anchor + NB-Residual vs joint Brand×NB elasticity) based on which fits current data best. Parked because it requires better drift-detection than we have today.
- **Self-diagnosis of model drift**: the engine tells the user "my projections have been systematically 10% too high for the last 4 weeks — consider regenerating priors."

### Tooling signal

- **NumPyro (JAX)** — primary for v1.2+ posterior work. Fast, jit-compiled, well-supported.
- **PyMC + Bambi** — prototyping layer. Slower but more introspectable; use for sanity-check duplicate fits before moving to NumPyro.
- **Uber Orbit** — closest analog for the "regression + regime + seasonality" decomposition. Reference implementation for hierarchical priors v1.3.
- **CausalImpact-style counterfactual viz** — already live in Phase 6.3.3 chart overlay (dashed "without campaign lifts" line + delta caption). Phase 6.5 formalizes this pattern.

### Reconfirmed stance

**v1.1 Slim stays structurally frequentist.** Every ship of v1.2+ is an additive layer on top of v1.1, not a rewrite. The anchor + regime stream + Locked-YTD decomposition is the long-lived architecture; only the uncertainty quantification and the prior-sharing expand.

This is tracked in `.kiro/specs/market-projection-engine/CHANGELOG.md` under the v1.2 / v1.3 / v1.4 placeholder sections.
