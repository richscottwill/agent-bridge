# MPE Spec Rewrite — Diff Proposal

**Date**: 2026-04-22
**Author**: Richard + agent
**Status**: PROPOSAL — awaiting Richard sign-off before spec files are rewritten
**Purpose**: Show exactly what changes in requirements.md, design.md, and tasks.md if we adopt the Grok low-maintenance framing. Written so a non-technical owner can read it and say yes or no per section.

## The One-Sentence Change

Shrink v1 from "10 markets full + full Bayesian + CPC elasticity + 3-year multi-year + anomaly ML + rigorous per-market simulation" to "MX/US/AU full + regional templates + recency-weighted linear + 200/1000 Monte Carlo + 2-year cap + 3SD anomaly flag + manual MX-4/22 simulation checklist" — so a non-technical owner can ship it by May and maintain it alone afterward.

## Why

Current spec has 51 tasks, 15 requirements, targets all 10 markets for full fits, and demands rigorous automated pressure-testing per market. That is a research-team scope, not a one-person-owner scope. Two external investigations (Grok synthesis; Gemini architecture critique) independently flagged over-scoping. Grok's framing is buildable by May and maintainable solo. Gemini's is a framework rewrite that kills the SharePoint portability requirement — rejected except for one idea (Hill-function ceiling as infeasibility guardrail).

## Gate Principle Check

Every proposed change was checked against the 6 "How I Build" principles.

| Principle | Where it shows up in this rewrite |
|---|---|
| Routine as liberation | Quarterly refit runs via `kiro hook run mpe-refit` — one command, no thinking. Runbook is the daily routine. |
| Structural over cosmetic | Shrinking scope is structural. Adding tooltips is cosmetic. This rewrite is all structural. |
| Subtraction before addition | 51 tasks → 28. 15 requirements → 16 (added R0 Maintainability and R16 v1 Boundaries, but cut substance inside R2/R11/R12/R13/R15). 10 markets → 3 full + 7 fallback. |
| Protect the habit loop | Cue = quarterly refit prompt. Routine = hook. Reward = 1-page report. Invariant. What's inside changes without disturbing the loop. |
| Invisible over visible | Fallbacks are banners, not crashes. Parity tolerance widens silently. Owner never sees "PyMC version mismatch." |
| Reduce decisions, not options | Owner doesn't decide "is my JP fit good enough?" — system uses regional fallback with a banner. All presets still available. |

---

# requirements.md diff

## NEW — R0: Maintainability for Non-Technical Owner (Highest Priority)

The entire system SHALL be designed so a non-technical owner can:
- Understand every output in under 30 seconds via tooltips, lineage, and plain-English warnings.
- Run refits and acceptance tests via single CLI commands or Kiro hooks without debugging.
- Diagnose issues using only built-in runbooks and UI banners — no code reading.
- Extend to one new market in under 2 hours using templates and the data-audit script.
- Roll back a bad parameter version in under 5 minutes with zero data loss.

**Why new**: Current spec never names the owner constraint. Making it requirement zero means every downstream decision has to respect it.

## R2 — Nine-KPI Projection Engine (TIGHTENED)

**KEEP**: 9 KPIs, Brand/NB segmentation, target modes, infeasibility messaging, regional rollups.

**CHANGE**:
- v1 is limited to **3 full markets (MX, US, AU) + regional rollups (NA, EU5, WW)**.
- Other 7 markets (CA, UK, DE, FR, IT, ES, JP) use regional fallback curves + "data-limited" banner.
- **Remove**: full hierarchical Bayesian, cross-elasticity, macro overlays, Prophet/BSTS — explicitly out of v1.
- **Simplify math to**: recency-weighted linear regression (exponential decay half-life 52 weeks) + Monte Carlo sampling (200 samples UI / 1000 CLI).
- **Add**: hard performance budget — UI recompute under 150 ms median. Web Worker mandatory for Monte Carlo.
- **Add**: Hill-function ceiling check as infeasibility guardrail only (not as the fit). If requested spend exceeds 1.5× historical max, trigger HIGH_EXTRAPOLATION with constraint message.

**Why**: Recency-weighted linear + MC is explainable, debuggable, and owner-readable. Hierarchical Bayes is not. The Hill idea from Gemini becomes a guardrail, not a fit.

## R3 — Portable HTML UI (SCOPED DOWN)

**KEEP**: single self-contained HTML, Chart.js CDN only, Methodology Manifest, multiple input modes, renders in Kiro/SharePoint/Symphony/filesystem.

**CHANGE**:
- **v1 core UI only**: scope selector (3 markets + 3 regions, others show "data-limited — using regional fallback" banner), time period, target mode (honors supported_target_modes), sliders + 4–6 presets per market, live debounced recompute, summary card + ie%CCP gauge + line chart with CI band + Brand/NB stacked + warnings panel + narrative block + provenance modal.
- **Remove from v1**: Apple micro-animations, command palette, 3D visuals, natural-language input in browser, advanced tabs.
- **Add**: "Explain this number" tooltip on every KPI (plain-English formula + data range + fallback status + "what to tell Lorena" line). See Explain_This_Number_Examples.md from Grok.

**Why**: Tooltips are the owner's support line. Command palette is engineering toy territory.

## R11 — Multi-Year (CAPPED)

**KEEP**: YoY growth trend per market per segment, recency weighting, LOW_CONFIDENCE_MULTI_YEAR warning.

**CHANGE**:
- **Cap multi-year at 2 years** in v1 (was 1-3). 3-year projections are marked "recommend 1-year only for now" with explicit banner.
- **Reason**: compounded uncertainty at 3 years produces bands so wide they're useless. Honest approach is to not offer it in v1.

## R12 — Bayesian Credible Intervals (SIMPLIFIED)

**KEEP**: Monte Carlo sampling, 50/70/90% intervals, separation into mpe_uncertainty.py module.

**CHANGE**:
- **Sample counts locked**: 200 for UI (Web Worker), 1000 for CLI. No user-tunable sample count in v1.
- **Remove MCMC upgrade path from v1 commitment**. Document as post-v1.1.
- **Acknowledge**: intervals will be slightly asymmetric due to elasticity posterior skew — tooltip explains this.

## R13 — Anomaly Detection (DRAMATICALLY SIMPLIFIED)

**KEEP**: runs on quarterly refit, flags anomalies for human review before activation, respects regime_changes table.

**CHANGE**:
- v1 is **3SD check + regime tag only**. No Isolation Forest, no BSTS, no LSTM, no hierarchical models.
- Thresholds tighten after 4 quarterly refits per market — liberal flagging in v1 is intentional, documented as "learning mode."

## R15 — Acceptance Test (DEMANDS REDUCED)

**KEEP**: per-market and per-region acceptance suite, save/load exact match, narrative conformance, XFAIL for data-limited markets.

**CHANGE**:
- **Automated core for MX / US / AU only** (was all 10 markets + 3 regions automated).
- Other 7 markets get regional fallback validation only.
- **MX 4/22 simulation is a documented manual checklist** (10 steps), run live in demo by owner — not automated. Trying to automate subjective steps like "why is this higher than my mental model?" is a known trap.

**Why**: Gemini didn't see this, Grok did: automating subjective stakeholder conversation is a research project.

## NEW — R16: Explicit v1 Boundaries (Scope Creep Shield)

v1 SHALL NOT include any of the following — each requires new spec + owner approval:

- Full 10-market fits (only MX/US/AU full + regional templates for others)
- Hierarchical Bayesian, BSTS, Prophet, Prophetverse, LightweightMMM, PyMC, any external ML library beyond numpy/scipy/scikit-learn
- Cross-elasticity between Brand and NB
- Macro/economic overlays
- Placement decay curves as first-class model (apply as uplift only)
- Advanced anomaly ML (Isolation Forest, autoencoders, LSTM)
- Command palette, Apple micro-animations, natural-language input in browser
- Auto-scheduled cron refit (manual hook only in v1)
- Slack notifications, email digests for refit reports (SharePoint push only)
- Streamlit/Reflex/any server-dependent UI framework (breaks SharePoint portability — R3 non-negotiable)

**Why**: Gemini's critique recommended Streamlit/Reflex which would break R3. This boundary prevents that conversation from happening again.

---

# design.md diff

## Architecture (UNCHANGED)

3-layer architecture (Parameter Layer / Engine Layer / Interface Layer) is correct and stays. Nothing in either investigation dislodges this.

**Gemini's "abandon JS UI, use Streamlit" recommendation is REJECTED** because it breaks R3 (SharePoint deployment, standalone filesystem render, no Python runtime at render time). This is the primary deployment requirement; no refactor that breaks it is acceptable.

## Parameter Registry (EXTENDED — SMALL)

**KEEP**: existing `ps.market_projection_params` schema, versioning, provenance.

**ADD these columns**:
- `fallback_level VARCHAR` — one of: `market_specific`, `regional_fallback`, `prior_version`, `conservative_default`
- `lineage VARCHAR` — human-readable breadcrumb: "Finance CCP file column U → refit 2026-04-15 → validated against W14-W16 actuals"

**Why**: every number in the UI needs to show where it came from. These columns make that cheap.

## mpe_fitting.py (SIMPLIFIED)

- Recency-weighted linear regression only (exponential decay, half-life 52 weeks configurable).
- Regional fallback logic: if market has fewer than 80 clean weeks OR r² below 0.35, fall back to NA/EU5 regional average + visible banner.
- Heavy file header: first 3 lines document "why this exists / how owner maintains it / what happens on failure."

## mpe_uncertainty.py (SIMPLIFIED)

- Monte Carlo 200 UI / 1000 CLI. Hard-coded. Not user-tunable in v1.
- Web Worker wrapper so UI thread never blocks on sampling.
- Document expected asymmetry in bands due to elasticity posterior skew.

## mpe_engine.py (UNCHANGED STRUCTURE)

Dataclasses and `project()` entry point stay. Additions:
- Warning taxonomy explicitly includes: `DATA_LIMITED`, `REGIONAL_FALLBACK`, `MAINTENANCE_MODE` (on top of existing HIGH_EXTRAPOLATION, LOW_CONFIDENCE, SEASONALITY_DOMINATED, HIGH_UNCERTAINTY, STALE_PARAMETERS, SETUP_REQUIRED, LOW_CONFIDENCE_MULTI_YEAR, VERY_WIDE_CI).
- Infeasibility response includes "closest feasible" suggestion.

## mpe_engine.js (REQUIREMENTS EASED)

- Parity tolerance **widened**: 0.1% for deterministic outputs, 2% for Monte Carlo CI outputs (Gemini was right that 0.1% cross-ecosystem parity is a trap for stochastic outputs).
- Web Worker wrapper for Monte Carlo sampling.

## Kiro Integration (NEW — FIRST CLASS)

**Steering file** at `.kiro/steering/mpe-low-maintenance.md` — enforces non-technical-owner language, forbids complex ML, caps scope.

**Hooks**:
- `mpe-refit.kiro.hook` — quarterly or on-demand. Runs data_audit + refit + anomaly check + owner-readable report.
- `mpe-parity.kiro.hook` — on save of engine files, runs parity tests. Blocks commit on failure.
- `mpe-acceptance-core.kiro.hook` — pre-commit or manual. Core acceptance for MX/US/AU.
- `mpe-demo-prep.kiro.hook` — before leadership demo. Builds SharePoint standalone, runs MX 4/22 simulation checklist, generates demo script.

**Why**: Hooks are the maintenance spine. They turn "I need to remember to refit quarterly" into "I ran the hook."

## Design Decisions (UPDATED)

- **D1 (Python authoritative, JS mirror) STAYS** — rejected Gemini's Streamlit/Reflex recommendation because it breaks R3.
- **D3 (SharePoint embedded-data pattern) STAYS** — confirmed by Gemini's critique of live-fetch.
- **D10 (Bayesian CIs via Monte Carlo) STAYS** but sample counts locked.
- **NEW D13**: Hill-function guardrail (not fit). When user requests spend beyond 1.5× historical max, engine triggers HIGH_EXTRAPOLATION and shows "closest feasible" ceiling. Rationale: Gemini correctly flagged log-linear can project impossible growth; this guardrail addresses it without forcing a full Hill fit.
- **NEW D14**: Data audit as Phase 0 gate. `data_audit.py` runs for all 10 markets before any fitting. Output tells owner which markets can support full fits and which use regional fallback. Prevents the "AU has 40 clean weeks, fit is garbage" surprise.

---

# tasks.md diff

## Shape change: 51 → 28 tasks

## Tasks KEPT (renumbered to Phase 0-5)

**Phase 0 — Data & Scope Foundation (NEW — 4 tasks)**
- 0.1 `data_audit.py` for all 10 markets with plain-English report per market
- 0.2 Hard-code v1 scope boundaries (UI shows 3 markets + 3 regions; others get data-limited banner)
- 0.3 Steering file + 3 core hooks (refit, parity, acceptance-core)
- 0.4 Owner runbook skeleton (daily / weekly / quarterly / diagnostic / escalation)

**Phase 1 — Core Engine (11 tasks)**
- 1.1 Parameter registry schema (with fallback_level + lineage columns)
- 1.2 Seed CCPs (column U) + IECCP time-series for MX/US/AU
- 1.3 Seed MX regime breakpoints + refit prompt
- 1.4 mpe_fitting.py (recency-weighted linear + regional fallback + heavy comments)
- 1.5 Fit MX parameters full suite + MX-specific notes doc
- 1.6 mpe_uncertainty.py (MC 200/1000, Web Worker friendly)
- 1.7 mpe_engine.py core (all target modes, feasibility, warning taxonomy with DATA_LIMITED)
- 1.8 Extend time periods (cap Multi-Year at 2 years)
- 1.9 Regional rollup (MX+US+AU only)
- 1.10 Unit tests (MX edge cases + solver stability)
- 1.11 CLI entry point

**Phase 2 — UI + Portability (10 tasks)**
- 2.1 export-projection-data.json for MX/US/AU + YTD + seasonality (target under 500 KB)
- 2.2 mpe_engine.js with Web Worker for MC, 2% CI tolerance
- 2.3 projection.html skeleton (core UI only)
- 2.4 Wire sliders + 6 presets + debounced recompute
- 2.5 Save/Load + "parameters changed since save" diff
- 2.6 Basic narrative (template + key drivers bullets, MX/US/AU specific)
- 2.7 Portability testing (Kiro serve, SharePoint standalone, filesystem)
- 2.8 Add to Kiro dashboard nav + SharePoint upload
- 2.9 "Explain this number" tooltips + provenance modal for every KPI
- 2.10 Excellent empty states + data-limited banners

**Phase 3 — US + AU Fits + Regional Templates (4 tasks — was 11)**
- 3.1 Fit US parameters (full v1 suite)
- 3.2 Fit AU parameters (efficiency mode, no ie%CCP, special narrative)
- 3.3 Seed regional narrative templates (mix-effect language)
- 3.4 Validate regional rollup end-to-end with real parameters

**Phase 4 — Durability Light (4 tasks — was 5)**
- 4.1 Simple anomaly detection (3SD + regime tag) + refit_market_params.py
- 4.2 Wire refit as Kiro hook + owner-friendly report
- 4.3 Parameter freshness banner + staleness logic
- 4.4 Final owner runbook (all sections complete)

**Phase 5 — Acceptance & Demo Prep (5 tasks — was 7)**
- 5.1 Core automated acceptance for MX/US/AU
- 5.2 Documented manual MX 4/22 simulation checklist (10 steps, run live)
- 5.3 Run full acceptance + produce report
- 5.4 Leadership demo script (90-second MX reproduction)
- 5.5 Wiki article + SharePoint publish + cold-start test

**Total: 28 tasks.**

## Tasks REMOVED (23 tasks)

All removed tasks are labeled "Post-v1.1 — requires new spec + owner approval":

- Individual fits for CA, UK, DE, FR, IT, ES, JP (7 tasks removed — these markets use regional fallback)
- Full automated acceptance simulation across all 10 markets (keep automated for 3, manual checklist for MX only)
- DE equivalent of MX 4/22 simulation (manual MX-only)
- Scheduled cron refit, Slack notifications (manual hook only)
- Symphony iframe publish task (unclear if still live — defer to post-demo)
- Separate per-market narrative fits for the 7 fallback markets (templates only)
- Additional anomaly variants beyond 3SD (post-v1.1)
- Advanced pre-commit gate wiring (basic gate only in v1)

## Tasks CHANGED

- Old task 2 (seed CCPs for all 10 markets) → new task 1.2 (seed CCPs for MX/US/AU only). Other markets keep pointer to column U but no fit.
- Old task 4 (mpe_fitting.py with log-linear) → new task 1.4 (recency-weighted linear + regional fallback as first-class, heavy header comments)
- Old task 6 (Bayesian uncertainty with 1000 samples, tunable) → new task 1.6 (200 UI / 1000 CLI, locked, Web Worker)
- Old task 35 (anomaly detection module) → new task 4.1 (3SD + regime tag, no ML)
- Old tasks 40-43 (acceptance test suite, per-market + per-region + MX+DE simulation) → collapsed into 5.1/5.2

## Timeline Impact

- **Old plan**: 51 tasks, 18-22 dev-days of effort, demo "unclear by May," full production unlikely before July
- **New plan**: 28 tasks, 18-22 dev-days of effort (Kiro acceleration assumed), demo-ready by **2026-05-16** (Friday before showcase week)

Same effort, sharper deliverable.

---

# Risks NOT addressed in the rewrite

Per the prior session: neither Grok nor Gemini handled the "add a 4th market later" problem honestly. Grok says 2 hours; reality is 4-6 hours the first few times, settling to 2 hours after pattern maturity. This rewrite acknowledges that in the Owner Runbook (Phase 4 task 4.4) rather than promising fantasy timelines.

**Open design questions that stay open** (documented in design.md, not blockers for rewrite):
1. Refit cadence for elasticity — quarterly hard + monthly MAPE monitor with ad-hoc trigger on regression
2. CPC elasticity fallback — if r² below 0.3, derive from CPA elasticity
3. Anomaly detection sensitivity — 3SD in v1; tighten after 4 quarters of data per market
4. Multi-year compounded uncertainty — capped at 2 years with banner; 3-year deferred
5. Regime-change documentation — refit prompt asks owner to confirm no new breakpoints missing

---

# Acceptance Gate for this Rewrite

Richard must confirm:
- [ ] Scope cut from 10 markets full → 3 full + 7 regional fallback is acceptable
- [ ] Multi-year cap at 2 years (was 3) is acceptable
- [ ] MX 4/22 simulation becomes manual checklist (was automated) is acceptable
- [ ] No Prophetverse / PyMC / LightweightMMM / Streamlit / Reflex in v1 is acceptable
- [ ] Hill function as guardrail only (not fit) is acceptable
- [ ] Adding 4th market later is 4-6 hours first time, not 2 hours, is acceptable honesty
- [ ] Demo-ready target of 2026-05-16 is acceptable

If all checked, agent proceeds to rewrite the three spec files in one pass. If any rejected, we revise the diff before touching files.

---

# Addendum — Self-Inspection Findings (2026-04-22, after v1 diff)

Agent inspected its own v1 diff against the workspace and the three existing spec files. Seven holes found. This addendum documents them so the spec rewrite incorporates them, and so Richard sees the reasoning (not just the conclusions).

## Finding 1: Integration with existing prediction code was not handled

**What I missed**: The workspace already has a working Bayesian projection stack that the diff did not acknowledge.

**What actually exists** (verified 2026-04-22):
- `shared/tools/prediction/bayesian_projector.py` — `BayesianProjector` class with `MARKET_STRATEGY` profile for all 10 markets (MX ieccp_bound, AU efficiency, JP brand_dominant, US/CA/UK/DE/FR/IT/ES balanced). Already handles historical fetch from `ps.performance`, seasonal priors from `ps.seasonal_priors`, and produces `MarketProjection` dataclasses.
- `shared/tools/prediction/core.py` — `BayesianCore` with posterior update logic.
- `shared/tools/prediction/engine.py` — `PredictionEngine` for natural-language question routing.
- `shared/tools/prediction/calibrator.py` — prediction scoring and confidence adjustment.
- `shared/tools/prediction/wbr_pipeline.py` — imports `BayesianProjector`; orchestrates the WBR flow.
- `shared/tools/prediction/populate_forecast_tracker.py` — imports `BayesianProjector` for forecast tracker updates.

**What does NOT exist** (contrary to current tasks.md):
- `mx_precise_projection.py` — referenced in current task 5 as the source of the MX elasticity curve. Does not exist. Task 5 is pointing at vaporware.

**Decision for v1**:
- `bayesian_projector.py` stays. Different use case (week-ahead forecasts for WBR pipeline scoring, uses posterior update against recent actuals).
- `mpe_engine.py` / `mpe_fitting.py` / `mpe_uncertainty.py` are NEW for v1. Different use case (planning projections with target modes and sliders, no live posterior update against actuals, decoupled from WBR pipeline).
- The two coexist. wbr_pipeline.py keeps using BayesianProjector. Kiro dashboard projection.html uses the new mpe_engine.
- Shared primitives live in `core.py` where reasonable. If `mpe_engine` and `bayesian_projector` both need weekly-seasonality sampling, that lives in `core.py`, not duplicated.
- Existing `MARKET_STRATEGY` dict in bayesian_projector.py is the source of truth for ie%CCP targets per market — migrate into `ps.market_projection_params` as `ieccp_target` and `supported_target_modes`. Do not re-type values. Cross-reference in fit task (1.5, 3.1, 3.2).

**Task change**: Add Task 0.5 "Audit existing prediction code. Document overlap with proposed mpe_engine. Migrate `MARKET_STRATEGY` dict to parameter registry. Confirm no behavior regression in wbr_pipeline.py."

**Also**: Remove the vaporware reference from task 5. Rewrite as "Fit MX parameters from scratch using mpe_fitting.py on ps.performance data."

## Finding 2: The "same effort" claim was wrong

I said old plan and new plan are both 18-22 dev-days. That was sloppy.

**Honest estimate**:
- Old plan (51 tasks, 10-market fits, full Bayesian, 3-year multi-year, automated per-market simulation): ~32-38 dev-days, probably doesn't hit May.
- New plan (28 tasks, 3-market full + fallback, recency-weighted linear, 2-year cap, manual MX simulation): ~15-18 dev-days with Kiro acceleration.
- Difference is real. The rewrite is a genuine simplification, not a reorganization.

**Fix in final tasks.md**: Change the "Same effort, sharper deliverable" line to "Estimated 15-18 dev-days vs old estimated 32-38 — roughly half the scope, half the effort, same demo window achievable."

## Finding 3: "Demo-ready by 2026-05-16" is tight, not guaranteed

Calendar math: 2026-04-22 to 2026-05-16 = 24 calendar days, ~17 working days. 28 tasks in 17 working days = 1.6 tasks/day average.

Realistic path:
- Week 1 (4/28 - 5/2): Phase 0 + start Phase 1 core engine. 7-8 tasks.
- Week 2 (5/5 - 5/9): Complete Phase 1, start Phase 2 UI. 8-9 tasks.
- Week 3 (5/12 - 5/16): Phase 3 fits (US, AU, regional), Phase 4 refit infrastructure, Phase 5 acceptance + demo prep. 12-13 tasks.

**Where it breaks**:
- If MX fit produces r² < 0.35 on any elasticity curve, that's a regional fallback path that needs separate validation. Absorbs half a day.
- If portability testing reveals SharePoint/Symphony CORS issues, that's real debugging time. Unknown.
- If Richard is pulled into MX NB drop work (currently live — see yun-kang MX NB drop draft open in editor), fitting time suffers.

**Fix**: Label demo date as "target, aggressive but achievable" in spec. Add mitigation: Phase 0 + Phase 1 MUST complete by end of Week 1 or the demo slips to following week. Flag this as a hard checkpoint.

## Finding 4: CPC elasticity decision was left implicit

The existing R2 says "nine KPIs including Brand/NB Clicks" and "both CPAs and CPCs are modeled via elasticity curves." My diff kept 9 KPIs but never stated whether CPC elasticity gets its own fit in v1.

**Options**:
- **(a)** Fit CPC elasticity separately for MX/US/AU in v1. Requires sufficient CPC variance in history. MX has it (range of spend levels post-regime). US likely yes. AU unclear.
- **(b)** Derive CPC from CPA elasticity in v1 (CPC = CPA × CVR × (1 - brand_click_overlap_factor)). Simpler but loses elasticity nuance.
- **(c)** Fit (a) when r² ≥ 0.3, fall back to (b) when r² < 0.3. Most defensible.

**Pick**: (c). Matches Gemini's open question #2 resolution in existing design.md. Adds one conditional branch to mpe_fitting.py and one warning type (`CPC_DERIVED_FROM_CPA`).

**Fix**: Update Task 1.4 (mpe_fitting.py) to include the r² ≥ 0.3 branch for CPC. Add warning type to taxonomy.

## Finding 5: DuckDB table introductions were not made explicit

The current design.md introduces new tables (`ps.market_projection_params`, `ps.parameter_validation`, `ps.parameter_anomalies`, `ps.regional_narrative_templates`, `ps.projection_scores`, `ps.regime_changes`). My diff kept them all. Did not note interaction with existing `ps.market_constraints_manual` (verified empty/clean today — no rows > 60 days stale) or `ps.performance` or `ps.seasonal_priors` (used by bayesian_projector.py).

**Fix in final design.md**:
- Declare new tables explicitly as "NEW for v1."
- Declare existing tables consumed read-only: `ps.performance`, `ps.seasonal_priors`, `ps.v_weekly`, `ps.market_constraints_manual` (for regime breakpoints), `ps.forecasts` (for cross-checking).
- State that `ps.regime_changes` may already exist or overlap with `ps.market_constraints_manual` — audit and decide which is canonical in Task 1.3.

## Finding 6: MX NB drop context was ignored

Richard has `shared/context/intake/drafts/2026-04-22-yun-kang-mx-nb-drop.md` open. MX NB is actively under discussion with Yun-Kang today. The rewrite treats MX fit as a clean quarterly task, but if MX NB is in a regime change right now, the 2026-W15/W16 data points are the beginning of a new breakpoint, not noise.

**Fix**: Add to Task 1.3 (seed MX regime breakpoints) — "Include provision for 2026 Q2 MX NB regime shift currently under investigation (yun-kang-mx-nb-drop). May need a 2026-W15 breakpoint in addition to the 2025-W27 ie%CCP ceiling breakpoint. Confirm with owner at fit time."

## Finding 7: Acceptance gate checklist was too soft

My v1 diff checklist asked Richard to tick boxes without tradeoff statements. "Hill function as guardrail only is acceptable" doesn't give him enough to meaningfully consent.

**Fix**: Replace checklist with tradeoff-aware version:

- [ ] Cut 10 markets full → 3 full + 7 regional fallback. **Tradeoff**: can't produce market-specific fits for CA/UK/DE/FR/IT/ES/JP on day 1; those markets show "using regional fallback — wider CIs" banner. **Recovery**: adding a market post-v1 is 4-6 hours templated work.
- [ ] Multi-year cap at 2 years. **Tradeoff**: can't produce 3-year OP1 preview in v1. **Recovery**: 3-year lands in v1.1 once we've seen how 2-year intervals behave in practice.
- [ ] MX 4/22 simulation manual (10-step checklist). **Tradeoff**: the "rigorous acceptance" name in R15 becomes softer; demo requires owner running the checklist live. **Recovery**: each checklist step has a passing criterion the agent can validate on-demand.
- [ ] No Prophetverse / PyMC / LightweightMMM / Streamlit / Reflex. **Tradeoff**: math is less sophisticated than a research-grade MMM. **Recovery**: if leadership wants research-grade, that's a separate v2 spec with an engineer in the loop.
- [ ] Hill function as guardrail only. **Tradeoff**: elasticity curves still extrapolate unrealistically in the fit region; Hill kicks in only as ceiling. **Recovery**: if projections at-ceiling are common, upgrade to full Hill fit in v1.1.
- [ ] "Add 4th market" is 4-6 hours first time (settling to 2 hours). **Tradeoff**: promises of 2-hour addition in Grok synthesis are optimistic for the first few. **Recovery**: honest runbook timing.
- [ ] Demo-ready 2026-05-16 is aggressive but achievable with Phase 0 + Phase 1 complete by 5/2. **Tradeoff**: if MX fit hits problems in week 1, demo slips. **Recovery**: hard checkpoint at end of week 1; if Phase 1 core engine isn't green, escalate.

## Rewrite order (updated)

Given the addendum, the rewrite of the three spec files proceeds:
1. requirements.md first (adds R0 + R16, tightens R2/R11/R12/R13/R15, removes CPC-fit-always assumption).
2. design.md second (integration plan section, new Design Decisions D13 + D14 + D15 for existing-code coexistence).
3. tasks.md last (adds Task 0.5, removes mx_precise reference, adds CPC r² branch, fixes MX regime task, adds checkpoint at week 1).

Agent awaits Richard's acceptance of the tradeoff-aware checklist before proceeding.
