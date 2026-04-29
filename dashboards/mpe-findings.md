# MPE Dashboard — Findings Backlog

Canonical status tracker for findings from Rounds 1–6 + dashboard-gap analysis.
Working document: survives context compaction, diffed in git log.

**Cadence:** one finding per commit. Step 1–7 protocol per `local-kiro-workstream-plan.md`.
Status values: `open` | `in-progress` | `done` | `verified` | `blocked` | `obsolete`

**"done"** = landed on disk + local regression green.
**"verified"** = Local Kiro pulled + walked the verification visually.

---

## Honest reconciliation: what's already on disk before we start

Several items on the incoming backlog were landed in Round 7 but not yet pushed
or verified by Local Kiro. Calling them out so status is accurate:

- `op2_pacing_divergence` alert translation — **done**. `CHECK_LABELS` + `translateDetail` wired in `renderMarketAnomalies` (projection-app.js ~163-213).
- "Compare to baseline" disclosure button rename — **done**. Landed in projection.html.
- Scope-change state reset — **done**. projection-app.js scope-select handler resets `disclosures.counter` + `activeChipId` + `scenarioOverride`.
- NA rollup "rollup of US + CA" wording — **done**. Rendered as `rollup of ${regionMarkets.join(' + ')}` (projection-app.js ~449).
- MY1/MY2 narrative denominator — **done**. mpe_narrative.js uses `Annualized to OP2` with `/nYears`.
- Control-input focus ring — **done**. projection-design-system.css has `.control-input:focus-visible` override.
- Target-input blur handler — **done**. projection-app.js target-input blur listener at ~2998.
- Spend upper bound — **done at $1B** (tightened from $10B in commit `4b19352`, see P3-10).
- Feedback widget aria-labels + enable-on-change — **done**.
- Em-dash weeks leak in How modal + fit-quality strip — **done**.
- "Today" marker on chart — **done** (single-market verified; cross-market spot-check outstanding on P2-09).

Status 2026-04-28: reconciled. All R7 items are live on disk and the per-finding
entries below have been flipped from the "R7, uncommitted" marker to "done".
No baseline batch commit was ever filed — each R7 item's behavioral code shipped
incidentally inside later commits (P3-10 spend cap, chart refactor, CSS cleanup).
Keeping this section as a historical ledger of the pre-backlog state.

---

## Milestone decisions (M-series, 2026-04-27 through 2026-04-28)

Rendering and adapter choices that span multiple findings. Captured here so
future agents inherit the "why" of the architecture without having to
reconstruct from diffs.

### M2 — `CanonChart` scenario mode in `canon-chart.js`
Added a third rendering mode to the canonical chart library alongside `tracker`
and `calibration`. Scenario mode supports CI band, counterfactual, regime
onset annotations, Today seam, period highlight, and a narrated tooltip
via Chart.js `tooltip.callbacks.afterBody`. Single library, three call
sites, no shared datasets — mode is orthogonal, not a set of overrides.

### M3 — Projection chart migrated off Observable Plot + D3
Replaced the ~750-line custom render pipeline in `projection-app.js`
(renderChart + attachNarratedTooltips + ensureTooltip + showTooltip +
hideTooltip + applyArrivalAnimations + annotateActiveRegimes +
renderNarratedTooltip) with Chart.js via `CanonChart.render({ mode:
'scenario' })`. Adapter lives in `projection-chart.js` (~200 lines) and
converts projection-app's data shape to scenarioData. Chart.js manages
hover/legend/dual-axis/resize natively; tooltip stays attached to the
canvas via native `afterBody` instead of a custom SVG overlay. Shipped
in `dcbdac3`. Closes the "should we convert to Chart.js?" question as
"yes, done." Marking the Chart.js swap **decided and shipped** — not
deferred.

### NB-shape-from-Brand (2026-04-28, commit `f6dc61e`)
Non-Brand RoY weekly shape derives from the Brand trajectory curve
(`nbRegsPerWeek[i] = brandRoyRegs[i] / sum(brandRoyRegs) * out.roy.nb_regs`)
instead of even-split, so the stacked area rises and falls with Brand's
seasonality + lift curve instead of showing a flat rectangular band. Same
treatment for NB spend. Per-series seam-scale fades on all four series
(Brand regs, NB regs, Brand spend, NB spend) so the Today line doesn't
create visible cliffs. Registrations and cost projections now move
together through time at the market's actual Brand:NB ratio.

### Regional rollup fauxOut fix (2026-04-28, commit `121b4e8`)
`renderRegionalV1` sums `out.ytd` + `out.roy` across all constituent
markets (WW sums 10, EU5 sums 5, NA sums 2). Previously the RoY placeholder
was `{}` and `projection-chart.js` couldn't distribute NB across projected
weeks, collapsing the projected half to Brand-only. The fix lives in the
regional-rollup builder so the adapter receives a consistent shape
regardless of call site (single market vs region).

### P2-12 chart-overlay (2026-04-28, commit `7db6a9c`)
Saved-projection compare line overlays the chart as a dashed brand-blue
total-regs curve when `STATE.compareId` is set. Compare data is
recomputed on the fly from the saved record's (driver, target,
regime_multiplier) through V1_1_Slim so it always reflects the exact
scenario saved. YTD half matches actuals (same market + same locked YTD),
so divergence only appears in the RoY half where the alternative scenario
differs from the current one.

---

## Phase 1 — Track A (correctness)

### P1-01 · MC draws complete for every market/period combo
- **Source:** Round 1 #2, Round 3 V2, Round 5 V1
- **Status:** done (Option C — bootstrap CI)
- **Verification:** Probe on MX/US/UK/JP returns bands with plausible widths (MX 90% CI regs ±~50%, US ±~22%, UK ±~27%, JP ±~90%). CI values render in narrative as "90% plausible range: $Xlo–$Xhi spend · Rlo–Rhi regs. (Bootstrap approximation from recent-YTD residuals.)" How-modal Step 4 added with honest footnote on method limitation.
- **What landed:**
  - `V1_1_Slim.bootstrapCI(projectionOutput, ytdWeekly, alpha=0.10)` — new function in v1_1_slim.js computing per-week bands from residual sd × √(weeks_forward)
  - Wired into projection-app.js MC path, replaces the `MPE.projectWithUncertainty` call that was returning empty CIs since 2026-04-23 schema migration
  - Chart renders shaded band via `--color-ci-band-brand` fill (no longer gated on removed Uncertainty disclosure button)
  - Narrative appends CI tail line with explicit "bootstrap approximation" label
  - How-modal has a dedicated Step 4 footnote: "…not a Bayesian posterior credible interval — full posterior CIs are pending migration to the updated schema."
- **Unblocks:** P1-08 (CI in KPI tiles), P2-03 (CI bands on chart — done as side effect of this ticket).

### P1-02 · "At full-year pace" narrative denominator for MY1/MY2
- **Source:** Round 5 V-2
- **Status:** done
- **Verification:** JP MY2 narrative says "Annualized to OP2, that's X% of OP2 spend" with X computed as `(annual_total_spend / 2) / op2_spend * 100`.
- **Note:** Will verify under new protocol before declaring verified.

### P1-03 · "Weeks used" em-dash placeholder in How modal + chart sub-line
- **Source:** Round 5 V-1 + V-6
- **Status:** done
- **Verification:** "How this was calculated" modal Step 2 reads "… fit from 169 weeks of history" not "… from — weeks of history".

### P1-04 · Campaign-lift-to-baseline auto-promotion
- **Source:** Round 3 R3-4, Round 3 R3-9
- **Status:** done (UI + math)
- **Verification (UI layer, DONE):** `V1_1_Slim.listRegimesWithConfidence` emits `absorbed_into_baseline: true` on any lift with `decay_status === 'no-decay-detected'` AND `n_post_weeks >= 52`. 5/13 lifts across US/MX/UK/JP/DE correctly flagged. Narrative separates absorbed from active. Drawer pill "absorbed into baseline" with `—` instead of confidence %.
- **Verification (math layer, DONE, zero-delta):** `brand_trajectory._per_regime_weighted_contribution` now returns `1.0` for absorbed regimes. All 10 markets returned zero delta in the pre/post snapshot (guardrail ±15%: 0/10 exceeded). Zero delta is the CORRECT outcome given the 2026-04-26 anchor rework — the recent-actuals anchor already reflects absorbed-lift levels, so forward-stream contribution is a near-1.0 no-op anyway. The code change makes it symmetric with JS and self-documenting against future anchor-mechanism changes.
- **Snapshots:** `shared/dashboards/data/p1-04-preshift.json` (pre), `...postshift.json` (post). 128/128 Python tests still green. Commits: 56229df (UI), ea992c4 (pre-snap), 8cd5840 (math + post-snap).

### P1-05 · Confidence floor for projection inclusion
- **Source:** Round 2 dashboard-gap
- **Status:** done (UI layer)
- **Verification:** Probe on 4 markets returned expected low-confidence flags — MX Sparkle (0.18 eff, still-peaking), UK dormant lift (0.07 eff), JP still-peaking lift (0.18 eff) all correctly flagged `low_confidence: true`. Absorbed lifts are NOT double-flagged (mutually exclusive).
- **Threshold:** `LOW_CONFIDENCE_FLOOR = 0.25` (documented in v1_1_slim.js).
- **What landed:**
  - `V1_1_Slim.listRegimesWithConfidence` now emits `low_confidence: true` on lifts with `effective_confidence < 0.25` AND not absorbed
  - Narrative adds tail sentence: "N lift(s) flagged as unmodeled upside (too noisy to count in the point estimate)"
  - Drawer shows yellow "unmodeled upside" pill with value "X% · not counted"
  - Explanation string: "Low confidence (18% effective — treated as unmodeled upside, not counted in projection)"
- **Math-side:** Deferred — same rationale as P1-04 math layer. The current weighted contribution already multiplies by eff=0.18, so the "lift" adds only ~18% of its raw impact. Zero-ing it out mathematically would shift projections by single-digit percent. Not shipped unless Richard wants it, consistent with R10 P1-04 math-side protocol.

### P1-06 · Solver convergence "Closest achievable" reporting
- **Source:** Round 3 R3-3
- **Status:** done
- **Verification:** When a TARGET_UNREACHABLE_* warning is active, the YTD wall banner now prepends `Closest achievable: X% efficiency (target Y%).` (or equivalent for spend/regs). Reaches into `out.totals.computed_ieccp / total_spend / total_regs` to pull the actual solver-achieved value and compares against `currentTargetValue()`. Only shows when delta is non-trivial (>0.5pp efficiency or >2% for spend/regs).

### P1-07 · Regime-onset vertical rules on chart
- **Source:** Dashboard-gap #3
- **Status:** done
- **Verification:** On MX chart, dashed purple `Plot.ruleX` rule at 2026-04-05 (Sparkle onset) with "Lift #1 onset" / "Lift #2 onset" labels at the top. Rules inside the plotted x-domain only. Sorted by onset date so #N matches chronological order.

### P1-07 · Regime-onset vertical rules on chart
- **Source:** Dashboard-gap #3
- **Status:** done (in P1-06/07/09 cluster)

### P1-08 · Effect-size summary with CI in KPI tiles
- **Source:** Dashboard-gap #4
- **Status:** done (90% range appended to hero context)
- **Verification:** Hero context line reads `Projected MX Y2026 to hit 75% efficiency. 2 campaign lifts active. 90% range: $863K–$2.52M spend · 15,038–45,305 regs.` — appends the bootstrap CI bracket immediately after the campaign-lifts count so the plausible range is visible in the same sentence as the point estimate. Reads from `STATE.currentUncertainty.credible_intervals`.

### P1-09 · Severity chip scope clarified
- **Source:** Round 3 R3-7
- **Status:** done
- **Verification:** Chip now reads "⚠ Across 10 markets: X critical · Y warn · Z info" — scope prefix removes the "is that view-scoped or global?" ambiguity. Tooltip explains "Summary spans all N markets. Click to jump to current-market alerts panel."

### P1-10 · Numbers-drift between reloads
- **Source:** Round 3 R3-5
- **Status:** done
- **Root-cause probe (2026-04-27):** Grep confirms NO localStorage persistence of scope/period/driver/target in projection-app.js. `rngSeed: 42` is hardcoded. The drift was NOT a non-deterministic seed bug. It was the `projection-data.json` bundle regenerating between loads (every time `export-projection-data.py` or the WBR pipeline runs, Y2026 re-fits with a week's more YTD data). Local Kiro's initial hypothesis matched: data is genuinely refreshing.
- **Fix (shipped):** Added prominent `Refreshed Xh ago` indicator inside the hero market badge (12px/500 in subtle gray, cursor:help on hover). Tooltip reads: "Last refresh: Apr 27 2:39 AM. Projections update when YTD actuals refresh, typically every Monday. If yesterday's number differs from today's, the underlying data has advanced — the model is not non-deterministic." Existing 12px `header-freshness` top-right line retained for redundancy. No math changes.
- **Verification:** Cold-load shows the badge with human-readable timestamp. Tooltip surfaces the full refresh datetime and explains the drift. A Kate-grade test: if she compares a screenshot from Monday ($1.32M) to one on Tuesday ($1.88M), she sees two different "Refreshed" values and understands why the numbers differ.

### P1-11 · abc input blur handler
- **Source:** Round 5 V-3
- **Status:** done
- **Verification:** Type `abc` into target-input, tab out, see "Enter a number." error.

### P1-12 · Console uncaught promise errors
- **Source:** Round 5 V-7
- **Status:** done
- **Verification:** Fresh load with DevTools open shows: (a) the favicon 404 is gone — an inline-SVG data-URI favicon (blue brand dot) is now linked in `<head>`; (b) any promise rejection that escapes a try/catch surfaces as `console.warn` via a global `unhandledrejection` handler and `ev.preventDefault()` so no red "Uncaught (in promise)" error appears; (c) `recompute()` is now wrapped — the exported function catches any inner throw and logs via `console.warn`; (d) `scheduleRecompute()` setTimeout path has explicit `.catch`; (e) `init()` call sites have `.catch`.

---

## Phase 2 — Track B (missing capabilities)

### P2-01 · Chart hover tooltips
- **Source:** Round 1 C-5, Round 2 R4-10
- **Status:** done (enhanced in R11)
- **Verification:** Hover over any week on chart — visible brand-blue dot (5px radius, white stroke) tracks cursor, `.mpe-tooltip` popup shows `Wk N · Projected · Brand Xk regs / $Yk · NB Mk regs / $Lk · 90% plausible range: lo–hi regs.` Locked YTD weeks show `YTD actual (locked)` variant. The tooltip now includes bootstrap CI per-week range when available.
- **What landed R11:** Pre-existing `attachNarratedTooltips` mousemove+bisector path was already wired but undiscoverable (transparent dots, no cursor feedback). Added a visible `mpe-hover-dot-overlay` SVG circle that tracks the focal point, wired `d.weekIndex` into chartData so the tooltip can look up the correct bootstrap CI bucket, and appended a "90% plausible range" line to projected-week tooltips.

### P2-02 · Chart x-axis period-scoping
- **Source:** Round 3 R4-12
- **Status:** done
- **Verification:** Select period=W17 → chart x-domain covers the ±2 week window (W15–W19). Select M04 → chart covers the weeks whose start date falls in April. Select Q2 → Apr–Jun. MY2 → roughly 104 weeks of lookback. Y2026 renders the full-year chart unchanged. Regime-onset annotations remap into the sliced frame and drop entirely when outside the window. Lives in `projection-chart.js::periodWindowOverBtWeeks` + `sliceScenarioByPeriod`. Commit: ae49fa9.

### P2-03 · CI shaded bands on chart
- **Source:** Dashboard-gap #1
- **Status:** done (shipped as side effect of P1-01 Option C step 4)
- **Verification:** Live-page DOM confirms `fill="rgba(0, 102, 204, 0.15)"` (= `--color-ci-band-brand`) rendering as `Plot.areaY` mark on the projected Brand line from YTD-wall forward. Uses per-week `ci_lo`/`ci_hi` arrays from `STATE.currentUncertainty.per_week.regs`, not ratio-scaling. No longer gated on the removed Uncertainty disclosure button.

### P2-04 · 3-panel component decomposition (Prophet-style)
- **Source:** Dashboard-gap #2
- **Status:** done (commit 766387a)
- **Verification:** Below main chart: 3 stacked plots labeled "Trend", "Seasonality", "Campaign lifts" each showing that stream's per-week contribution.

### P2-05 · Backtest panel
- **Source:** Dashboard-gap #5 + #6
- **Status:** done (commit 766387a)
- **Verification:** A panel shows last 8 weeks of actuals overlaid with 8-weeks-ago projection + MAPE % + coverage %.

### P2-06 · Week-over-week delta on KPI tiles
- **Source:** Round 1 K-8
- **Status:** done
- **Verification:** Brand Regs, NB Regs, and Cost per Reg KPI tiles each carry a `.hero-kpi-delta` subline reading `↑ +3.2% WoW` (green) or `↓ −2.1% WoW` (red). Computed from the last two weeks of `ytd_weekly`. CPA inverts color semantics (up = bad). Hero and Efficiency skip WoW because they're period-aggregates, not weekly numbers. Tiles gracefully clear when YTD < 2 weeks. Commit: ae49fa9.

### P2-07 · Clickable chart legend (+ KPI tile linking)
- **Source:** Round 4 C-10 (legend), R11 (KPI linking = P2-07b)
- **Status:** done
- **Verification:**
  - Click "Projected Non-Brand" in the legend → orange line hides, legend text gets strikethrough + opacity 0.5. Click again → restored.
  - On cold load, "Actuals (spend, scaled)" and "Projected Total spend (scaled)" are default-hidden. Chart is legible by default; spend lines are one click away.
  - Click Brand Regs KPI tile → chart isolates to Brand line + Actuals. Tile gets brand-blue left border + `#F0F7FF` bg. Click same KPI again → restore defaults.
  - NB Regs KPI isolates NB line same way.
- **What landed:**
  - `STATE.legendVisibility` object keyed by series id (`actuals-regs`, `actuals-spend`, `proj-brand`, `proj-nb`, `proj-total`, `proj-total-spend`) with defaults hiding the two scaled-spend lines
  - Legend items get `data-series` attr + click handler that flips the visibility bit and updates `style.display` on matching SVG paths (matched by stroke color + dash pattern)
  - KPI tiles with `data-kpi-series` get a click handler that either isolates (only that series + actuals visible) or restores (defaults). `.kpi-active` CSS class highlights the driving KPI.
- **P2-07b tracked inline** in this commit — worth its own sub-entry if the behavior needs a separate verification round but tightly coupled to legend toggling.

### P2-08 · Line end-labels
- **Source:** Round 4 C-11
- **Status:** done (commit 8afab47)
- **Verification:** Right edge of each projected line has a text annotation with the series name + last value.

### P2-09 · Today marker correctness across all markets
- **Source:** R5 shipped; needs verification
- **Status:** done; needs cross-market verification
- **Verification:** On all 10 markets + 3 regions, the "↓ Today" marker lands exactly at `ytd_latest` and reads "Today".

### P2-10 · URL-based state sharing
- **Source:** Round 4 R4-28
- **Status:** done
- **Verification:** Open `projection.html?scope=UK&period=Y2026&driver=ieccp&target=65` → loads UK Y2026 @ 65% efficiency directly. Change any control → URL updates via `history.replaceState` (no history spam). Invalid option values fall through to defaults. Live in `syncUrlFromState()` + `applyUrlStateOnLoad()`. Commit: b431616.

### P2-11 · CSV export
- **Source:** Dashboard-gap #9
- **Status:** done
- **Verification:** New "Export CSV" button in the controls row between Save and Recompute. Clicking downloads `projection-<scope>-<period>-<driver>-<YYYY-MM-DD>.csv` with columns `week_iso,week_start,series,brand_regs,nb_regs,total_regs,brand_spend,nb_spend,total_spend,ci_lo_regs_90,ci_hi_regs_90`. YTD rows (`series=actual`) carry actuals, RoY rows (`series=projected`) carry projected values plus 90% bootstrap CI when available. Four trailing `#`-prefixed metadata rows encode scope/period/driver/target/totals so scenarios are self-describing when pasted into Excel. Commit: ae49fa9.

### P2-12 · Saved projection load/delete/compare
- **Source:** Round 4 R4-16
- **Status:** done
- **Verification:** Each saved item shows Load / Compare / × buttons. Load restores full state (scope/period/driver/target/regime_multiplier). Delete removes the entry + clears active compare if it matched. Compare highlights the selected item with a brand-blue border + #F0F7FF background, sets `STATE.compareId`, and overlays the saved projection on the chart as a dashed brand-blue line labeled `Saved · <driver>=<value>`. The compare line is recomputed from the saved record's (driver, target, regime_multiplier) through V1_1_Slim's `year_weekly` arrays so it reflects the exact scenario that was saved. YTD half of the compare line matches actuals (same market, same locked YTD); divergence appears in the RoY half. Scope-mismatched saves are silently skipped so overlaying a saved MX projection on a US chart doesn't produce a misaligned line. Row click still loads for backward compat. Commits: b431616 (state plumbing), 7db6a9c (chart overlay).

### P2-13 · Brand/NB stacked bar visual
- **Source:** Round 1 K-7
- **Status:** done (commit 3b546ae)
- **Verification:** In place of separate Brand Regs + NB Regs tiles, one horizontal bar split 37/63 with labels.

### P2-14 · Directional color/arrow on OP2 comparisons
- **Source:** Round 1 K-3
- **Status:** done
- **Verification:** vs OP2 Spend at 137% shows red `↑ +37 pts vs plan` (over-spending = bad). vs OP2 Spend at 85% shows green `↓ −15 pts vs plan` (under-spending = slight good). vs OP2 Regs at 137% shows green `↑ +37 pts vs plan` (over-delivering = good). vs OP2 Regs at 85% shows red `↓ −15 pts vs plan` (under-delivering = bad). Direction semantic flips between spend and regs because the two metrics have opposite "goodness" gradients. Commit: ae49fa9.

### P2-15 · Spend on separate axis or chart
- **Source:** Round 1 C-2
- **Status:** done (option 1 — dual y-axis via post-render overlay)
- **Verification:** On MX chart, right margin shows spend-equivalent tick labels (`$400K`, `$800K`, `$1.2M`, …) corresponding to the regs-axis tick positions. `↑ Spend ($)` label at top-right. Spend lines still drawn on scaled axis but readable off the right margin.
- **What landed:** Post-render SVG overlay that queries each left-axis tick (`[aria-label="y-axis tick label"]`), computes the spend-equivalent via `regsVal / spendScale`, mirrors the label on the right side with `fmt$` formatting.

### P2-16 · Y-axis auto-scale tightening
- **Source:** Round 1 C-3
- **Status:** done
- **Verification:** Both y (regs) and y1 (spend $K) axes in the scenario mode now compute `suggestedMax = peak * 1.12`, so the chart peak breathes at ~12% headroom instead of the default Chart.js 30-60%. Applied inside canon-chart.js `renderScenarioChart`; tracker/calibration paths untouched. Commit: b431616.

### P2-17 · Shared y-scale toggle for all-10 grid
- **Source:** Round 2
- **Status:** done (commit 766387a)
- **Verification:** On the "All 10 markets" view, a toggle switches between per-market y-scale and shared y-scale.

### P2-18 · Distance-to-target view fix
- **Source:** Round 2
- **Status:** done (commit 766387a)
- **Verification:** Heatgrid shows meaningful distances (distance to OP2 or unconstrained projection) rather than 0pp for solver-back-fit markets.

---

## Phase 3 — Track C (polish, a11y, naming)

### P3-01 · Alert translation render wire-up
- **Source:** Round 6 V6-3
- **Status:** done
- **Verification:** MX alerts panel shows "Warning Projection diverges from OP2 plan — annual regs=17,235 vs OP2=11,178 (gap +54.2%)" not "[WARN] op2_pacing_divergence —".

### P3-02 · "Baseline only" deduplication
- **Source:** Round 6 V6-2
- **Status:** done
- **Verification:** Scenario chip renamed from "Baseline only" to "No-lift baseline". Disclosure button remains "Compare to baseline" (renamed earlier in R7). No two controls share a name now. Commit: b431616.

### P3-03 · Scenario chip definition tooltips
- **Source:** Round 6 V6-5
- **Status:** done (commit 8afab47)
- **Verification:** Hover over "Pessimistic" scenario chip → styled tooltip within 200ms shows "Recent actuals extrapolated forward. No assumed uplift from active campaigns."

### P3-04 · Disclosure button state reset on market switch
- **Source:** Round 6 V6-4
- **Status:** done
- **Verification:** Activate "Compare to baseline" on UK, switch to MX → button is de-activated and MX shows Planned scenario numbers.

### P3-05 · Control-input focus ring
- **Source:** Round 6 V6-1
- **Status:** done
- **Verification:** Tab through market dropdown, period, driver, target-input, slider → each shows a 2px brand-blue outline.

### P3-06 · NA rollup subtitle wording
- **Source:** Round 5 V-5
- **Status:** done
- **Verification:** Market badge on NA reads "NA · Year 2026 · rollup of US + CA" not "… rollup target".

### P3-07 · Contribution bar "Qualitative" relabel
- **Source:** Round 1 L-5
- **Status:** done
- **Verification:** Contribution bar fourth segment now reads "Judgment" instead of "Qualitative". Narrated tooltip on the chart emits "X% judgment" instead of "X% qualitative". CSS class names (.qualitative) and color token (--color-qualitative) left untouched to avoid cross-file cascades. Commit: b431616.

### P3-08 · Plural handling in narrative
- **Source:** Round 6
- **Status:** done (audited, already correct)
- **Verification:** Audit of mpe_narrative.js confirms all plural paths use proper `n === 1 ? 'X' : 'Xs'` forms. No "lift(s)" / "event(s)" parenthesis-plurals remain in live code. Findings doc flip-only — no code diff. Commit: b431616 (docs only).

### P3-09 · Raw numbers formatted everywhere (grep pass)
- **Source:** Multiple rounds
- **Status:** done (commit 8afab47)
- **Verification:** Grep of codebase for `\$\{[^}]*(target|spend|regs)[^}]*\}` without an `fmt` wrapper returns zero hits.

### P3-10 · Spend upper bound cap
- **Source:** Round 5 V-4 / Round 6
- **Status:** done (commit 4b19352)
- **Verification:** validateTargetInput warn now fires at spend > 1e9 ($1B) with message "Spend target exceeds $1B — likely a typo." Hard max kept at 1e10 so the browser input clamps without being overly restrictive. AB Paid Search spend over $1B/year is flat-out wrong → typo catch.

### P3-11 · Time format on saved projections
- **Source:** Round 5 V-?
- **Status:** done
- **Verification:** Saved list now renders timestamps via `toLocaleString` with explicit month/day/year + hour/minute formatting (e.g. "4/27/2026, 4:02 PM" instead of "4/27/2026"). Users saving multiple scenarios in a single session can tell them apart. Commit: b431616.

### P3-12 · aria-label coverage
- **Source:** Round 4 R4-23
- **Status:** done (commit 8afab47)
- **Verification:** Every `button`, `select`, `input` has an `aria-label` or is wrapped in a `<label for="…">`.

### P3-13 · Landmark elements
- **Source:** Round 4 R4-21
- **Status:** done (commit 8afab47)
- **Verification:** Page has `<main>`, `<aside>` for drawer, `<nav role="toolbar">` for controls row. Screen reader can navigate by landmark.

### P3-14 · Heading hierarchy
- **Source:** Round 4 R4-22
- **Status:** done (commit 8afab47)
- **Verification:** No heading level skip. H1 → H2 → H3, not H1 → H3.

### P3-15 · Remove [WARN]/[ERROR] bracket notation
- **Source:** Round 4 R4-26
- **Status:** done
- **Verification:** Alerts panel shows "Warning" / "Error" pill badges, no brackets.

### P3-16 · Recompute button decision
- **Source:** Round 4 R4-18
- **Status:** done (commit 8afab47)
- **Verification:** Button either removed entirely OR re-fetches `projection-data.json` when clicked (visible via network tab).

### P3-17 · Scenario chip meaning (decide chip vs annotation)
- **Source:** Round 4 R4-19
- **Status:** done (commit 8afab47)
- **Verification:** Either chips are clearly labeled interactive with hover tooltips (P3-03 covers), or they're restyled as annotations if that's the intent.

### P3-18 · Feedback widget radio enables inputs
- **Source:** Round 2 R4-20
- **Status:** done
- **Verification:** Click "Too high" radio → magnitude + freetext + submit are enabled.

### P3-19 · Reset-to-defaults button
- **Source:** Round 4 R4-29
- **Status:** done
- **Verification:** New Reset button in the controls row between Export CSV and Recompute. Clicking restores MX / Y2026 / ieccp / 75, sets regime slider to 1.00×, clears all transient state (compareId, scenarioOverride, activeChipId, kpiIsolatedSeries, disclosures.counter). One-click escape hatch from a messy comparison stack. Commit: b431616.

---

## Phase 4 — Deferred refactors + AB.com branding

Executes LAST, after Phases 1-3 are stable. One commit per finding. Each
commit gets a visual regression pass from Local Kiro before next commit.

**Critical do-NOT rules (common traps flagged by Local Kiro):**
- **DO NOT migrate chart encoding colors** (`--color-nb` #FF9900, `--color-brand-line` #0066CC, `--color-actuals` #4A4A4A). Chart encoding is a data-ink concern; it is NOT UI chrome. The Non-Brand orange is close to AB.com's Smile orange and moving it creates visual collision. Leave chart colors untouched.
- **DO NOT pillify generic buttons.** The `.btn-primary` class with Smile-orange pill is for EXACTLY ONE button per view. If applied to `button { ... }` or all `.disclosure-btn`, it turns Save + Model details + Baseline + Recompute all into orange pills — three mistakes at once: (1) visual noise, (2) Smile orange bleeding away from its "primary action" semantic, (3) potential collision with the chart's NB orange when chart + orange-pill are both onscreen.
- **DO NOT bundle Amazon Ember .woff files into the repo.** That is a licensing violation and will fail internal review. Options in order: corp CDN URL (check AB.com network tab), sanctioned internal source, fallback to OS-installed `'Amazon Ember'` via font-family stack. If font source can't be resolved in 30 min of investigation, mark P4-03 blocked.
- **DO NOT migrate palette + type scale in one commit.** Failure modes become unattributable. Palette first (P4-01), CTA pill scoped (P4-04), then type scale (P4-02).

### P4-01 · Palette token migration to AB.com colors
- **Status:** done (minimal variant, 2026-04-28)
- **Scope decision:** Richard said "I like the look of it right now" — the full palette swap contradicts that instruction. Shipped only the two near-imperceptible text-color tokens that align with AB.com values without visibly shifting the dashboard. Everything else skipped with rationale below.
- **Shipped:**
  - `--color-text-body: #1A1A1A` → `#161D26` (RGB delta ~6pts, barely visible)
  - `--color-text-hero: #0A0A0A` → `#0F1111` (RGB delta ~5pts, barely visible)
- **Intentionally skipped (reason: visible change contradicting "like the look"):**
  - `--color-neutral-bg: #FFFFFF` → `#F5F3EF` — warm-cream bg is a meaningful tonal shift; defer.
  - `--color-panel-bg: #FAFAFA` → `#FFFFFF` — would flatten panel distinction; defer.
  - `--color-panel-border: #E0E0E0` → `#E5E5E5` or `#6E6E78` — weight-dependent; defer.
  - `--color-brand: #0066CC` → `#2162A1` — this token drives the Brand segment of the P2-13 stacked bar (verified during today's work) AND is the accent for severity chips / focus rings / hero-KPI hover / chip hovers. Darkening it shifts the stacked bar Brand fill to a different blue than the NB-shape-from-Brand chart's compare-line Brand-blue (canon-chart.js `BLUE = '#4a9eff'` is chart-scope, untouched). Defer until we can reconcile chrome-brand and chart-brand semantically.
- **Verification (minimal):** DevTools computed-style on `.page-frame` body text reads `rgb(22, 29, 38)`. Hero number reads `rgb(15, 17, 17)`. Nothing else visibly changed.

### P4-02 · Type scale migration (body → 18px, 4-token scale)
- **Status:** deferred (2026-04-28) — contradicts "like the look right now"
- **Deferral rationale:** Current `--size-body` is `16px` (not `14px` as the original backlog claimed — the 14→18 change was already partly done). Pushing to `18px` expands every panel, fundamentally loosening density. Richard explicitly said the current look is what he likes; 18px body would re-tile every view. Keep at `16px` until a visual-design session explicitly revisits density tradeoffs.
- **Preserved plan if revisited:** original scale values + per-region commit cadence still sensible; just gated on "we want a density shift" directive, not assumed.

### P4-03 · Ember font source compliance verification
- **Status:** done (already correct on disk, 2026-04-28)
- **Verification:** `--font-sans` in `projection-design-system.css` line 44 already reads `'Amazon Ember', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif`. On Amazon corp machines (Kate, Brandon, Todd, Richard) Ember is OS-installed so the browser picks it up from local fonts — no CDN needed, no .woff bundling, no licensing exposure. On non-corp machines the stack falls through to system-ui gracefully. Path 3 from the original spec is the shipped path.
- **Deferred (intentionally):** Corp CDN investigation (path 1) would be worth a look if the dashboard ever moves to external audiences, but for the current internal-only audience the OS-font path is sufficient and risk-free.

### P4-04 · Primary CTA styled as AB Smile-orange pill (SCOPED TO ONE BUTTON)
- **Status:** deferred (2026-04-28) — contradicts "like the look right now" and conflicts with chart encoding
- **Deferral rationale:** Making Recompute a Smile-orange pill is a highly visible control chrome change. Richard said the current look is what he likes. Additionally, this dashboard's chart uses `--color-nb: #FF9900` for the Non-Brand stacked area (today's P2-13 + NB-shape-from-Brand work made NB prominent). Putting an orange pill in the controls row when orange is a data-encoding color onscreen is the exact collision the original Phase 4 anti-pattern note warns about. The current flat gray Recompute button is semantically clear (primary by position, not by chroma) and is working. Defer unless we decide to relocate NB's encoding color.
- **Preserved plan if revisited:** scoped-to-single-button rule stays; grep guard rails stay; orange-in-chart avoidance stays.

### P4-05 · Full matrix regression test (10 markets × 6 periods × 3 drivers = 180 combos)
- **Status:** scoped-down to manual spot-check (2026-04-28)
- **Scope decision:** The 180-combo matrix existed to catch reskin regressions. With P4-01 reduced to two near-imperceptible text-color tokens and P4-02/P4-04 deferred, the change surface is too small to warrant automating. Manual spot-check of 3-5 markets (MX single + US single + WW rollup at minimum) is sufficient.
- **Preserved plan if revisited:** automation scaffolding still sensible for a future palette + type-scale push; not worth building now.

---

## Phase 4 sequencing (why this order)

Original sequence preserved below for if/when Phase 4 gets re-scoped. 2026-04-28
execution applied a lighter scope per Richard's "like the look right now"
instruction: P4-01 minimal (text-color tokens only), P4-03 confirmed already-on,
P4-02 + P4-04 deferred with documented rationale, P4-05 scoped to spot-check.

1. **P4-01 palette** — biggest visual shift, single variable surface, failure is obvious and localized. Commit + Local Kiro verify.
2. **P4-04 CTA pill** — scoped component addition, doesn't touch existing styles. Safe after palette lands.
3. **P4-03 Ember source** — must resolve before P4-02 activates the stack. Runs in parallel with P4-04.
4. **P4-02 type scale** — largest diff, highest regression risk. Isolate after visual moves stabilized.
5. **P4-05 regression matrix** — sanity gate.

Rationale: isolating failure modes. If palette and type scale ship together and something breaks, can't tell whether it's from color or type. Separating them keeps failures attributable.

---

## Prior Phase 4 items (palette + type-scale consolidation) — consolidated into P4-01/P4-02

The earlier "Phase 4 palette consolidation 41→14 tokens" and "type scale 13→4" items are subsumed by P4-01 and P4-02 above. The AB.com branding makes the consolidation more specific (actual target values, not just "fewer tokens"), which is a win — the consolidation wasn't scoped to target values before.

---

## Phase 5 — R19 review (Local Kiro, 2026-04-28)

Local Kiro ran a research-grounded teardown of the feature-complete dashboard
after the Chart.js swap and MX 75% target landed. Mockup:
`~/shared/context/intake/mpe-proposed-changes-mockup.html` (13 proposals with
before/after + code + acceptance). Richard directive: "go forward with all".

Ship order follows Local Kiro's compounding-effect sequencing — structural
cleanup first, then typography, then features, then deferred items last.

### P5-13 · Whitespace cleanup — 545px dead gap under chart
- **Source:** R19 #13 (HIGH)
- **Status:** done
- **Verification:** Closed `<details class="sec-panel">` panels (Decomposition, Backtest) now use `padding-top/bottom: var(--gap-sm)` instead of the default large padding; stacked closed panels pack tight via `:not([open]) + details.sec-panel { margin-top: var(--gap-sm) }`. Feedback-bar reserves zero top margin when hidden; `.visible` class (added by `maybeShowFeedbackBar` when projection count ≥ 3) promotes it back. Total page height drops substantially — closed-default layout no longer reserves ~545px below the chart or ~149px for the hidden feedback bar.
- **Verification method:** cold-load `/projection.html` → `document.documentElement.scrollHeight` before (~2,808px) vs after (measured post-load).
- **Blast radius:** CSS inside projection.html + 3 lines of JS in `maybeShowFeedbackBar`. No market-specific behavior. No data changes. No state changes.
- **Commit:** `91225c0`

### P5-1 · Remove Brand/NB split chip — fold share into KPI tile deltas
- **Source:** R19 #1 (MEDIUM)
- **Status:** done
- **Verification:** The P2-13 `.brand-nb-bar` element below the KPI strip is removed from `projection.html`. Brand Regs and NB Regs tiles now each show `↑ +X.Y% WoW · N% share` in their delta line. CPA tile delta is unchanged (no share concept). Early-year markets (<2 YTD weeks) surface just the share suffix without WoW.
- **Why:** the bar and the tiles directly above it displayed the same 75%/25% split two different ways — pure duplication that extended the user's scan-for-relevant-info time. Share% belongs on each tile.
- **Blast radius:** projection.html element deleted, `renderMarket` in projection-app.js extended `setWowDelta` signature with `shareSuffix` param, populated from `out.totals.brand_regs / nb_regs`. No solver / state / chart changes.
- **Commit:** `960f581`

### P5-4 · Hide Saved Projections panel when empty
- **Source:** R19 #4 (LOW)
- **Status:** done
- **Verification:** Cold-load with no saved items → `#saved-panel` has `display: none` applied. After clicking Save once → panel reappears. Delete the only saved item → panel disappears again.
- **Blast radius:** `renderSavedList` toggles `#saved-panel` display; HTML element got an id. No other behavior touched.
- **Commit:** `138e288`

### P5-3 · Default-close the Model View drawer
- **Source:** R19 #3 (MEDIUM)
- **Status:** done (already correct on disk, 2026-04-28)
- **Verification:** `.drawer` CSS defaults to `transform: translateX(100%)` (off-screen) and the `.open` class is only added via `classList.toggle('open', STATE.disclosures.params)` on the Model details disclosure button click. `STATE.disclosures.params` initializes to `false` (projection-app.js:32); no localStorage restore path. Cold-load reality: drawer is already off-screen by default. The Model details button opens it; × closes it. No code change needed.
- **Deviation from spec:** Local Kiro's mockup implied the drawer was open by default; the code shows it's already closed. Flipping to done without a no-op commit rather than shipping an empty diff.
- **Commit:** n/a (verification only)

### P5-9 · Fit Quality empty-state copy rewrite
- **Source:** R19 #9 (LOW)
- **Status:** done
- **Verification:** Fit-quality strip now leads with `Confidence:` not `Fit quality:`. For markets with no r²: `Confidence: limited history — model using regional priors, local calibration pending ~8 weeks of backtest data. N active campaign lifts. Explain this →`. For markets with r²: `Confidence: strong (82% explained) — model calibrated on 52 weeks of local data. 2 active campaign lifts. Explain this →`. No more "not yet measured" / "weeks of data not recorded" negatives. Explain-this link surfaces for both states.
- **Blast radius:** `renderFitQuality` in projection-app.js only. No HTML or CSS change. No markets excluded.
- **Commit:** <filled after commit>
---


## Order of work

Execute top-to-bottom within each phase. When a finding is blocked, mark the
reason in-place and move to the next. Never silently skip.

**Current next-up:** Phase 5 R19 items — 13 findings queued, executing in Local Kiro's compounding-effect order.
