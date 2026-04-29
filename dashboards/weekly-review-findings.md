# Weekly Review — Findings Backlog

Canonical status tracker for the weekly-review R1 sprint (Local Kiro review,
2026-04-28). Mirrors the `mpe-findings.md` pattern for the projection engine.

**Cadence:** one finding per commit. Status values: `open` | `in-progress` |
`done` | `verified` | `blocked` | `obsolete`.

**"done"** = landed on disk + regression green.
**"verified"** = Local Kiro pulled + walked the verification visually.

**Source bundles:**
- `~/shared/context/intake/weekly-review-r1-handoff-prompt.md` — 12 proposals (A1-A6, B1-B4, C1-C2) framing weekly-review as "the forecast grading rubric for the projection engine"
- `~/shared/context/intake/wbr-proposed-changes-mockup.html` — 13 proposals (correctness + duplication + density + UX)

Both bundles audited against live code + data before execution — audit notes
in "Reconciliation" section below.

---

## Reconciliation with live code (2026-04-28 audit)

Before executing I ran a live audit — Local Kiro's claims need grounding, per
the logged discipline "audit bundled specs against live code before executing."

**Verified claims:**
- `predictions_history` exists in `forecast-data.json` for all 12 markets incl. EU5 — A1 scorecard has its data.
- `brand_detail.lw_regs` + `nb_detail.lw_regs` exist in `callout-data.json` — A4 variance decomposition CAN derive WoW deltas.
- `metrics.regs_wow / spend_wow / cpa_wow` exist — since-last-week summary has fields.
- Line 762 weekly-review.html `wow > 0 ? 'good' : wow < -5 ? 'bad' : 'warn'` — wbr-#1 asymmetry bug is real.
- Line 446 `chartModeBtn` — wbr-#9 toggle is real; becomes moot after r1-A2 (toggle removed in favor of two panels).
- Line 786 `Year-End Pred` tile — real; r1-C2 + wbr-#6 agree it should go.
- Line 512 market filter uses intersection — wbr-#4 EU5 gap is real. Callout markets = 7, forecast markets = 12.
- `predictions_history[market][wk]` has richer shape than the spec assumed: `first_pred`, `latest_pred`, `actual`, `first_ci_lo/hi`, `latest_ci_lo/hi`, `error_pct`, `score` (HIT/MISS) — A1 is well-fed.

**Partial/conditional claims:**
- `callout.projections` is **empty `{}`** for current weeks (W17/W16) on all markets. Populated only on W15 and earlier. **A6 qPacing, r1-B4 OP2 pacing, r1-A4 variance** will render with empty-state fallbacks on current weeks until the next refresh populates projections. Not a blocker — empty states are part of each proposal's acceptance.

**Bundle overlaps resolved:**
- r1-B4 (OP2 pacing tile) + wbr-#6 (replace passive OP2 Target with vs-OP2 delta) + r1-C2 (remove YE Pred) → one commit replacing YE Pred with a directional OP2 pacing tile.
- r1-A2 (calibration first-class) + wbr-#10 (reduce calibration line count) → one commit promoting calibration AND defaulting to regs-only axis inside the new panel.
- r1-B1 (typography lock, rides MPE P5-12) + wbr-#12 (token sweep on local overrides) → one commit sweeping the .pred-lbl / .wr-proj-* / .wr-list local overrides to tokens. MPE P5-12 already shipped.
- wbr-#9 (chart mode toggle state) becomes moot after r1-A2 lands — drop wbr-#9.

---

## Ship order

Correctness + subtraction + density first, then differentiation, then polish.
Compounding-effect ordering so each commit's ground is stable before the next.

### Tier A — Correctness + subtraction (fast wins)

### WR-C1 · WoW threshold asymmetry + divide-by-zero guard (safeWoW)
- **Source:** wbr #1 + #13 (MED + HIGH merged)
- **Status:** done
- **Finding:** `renderKPIs` and `renderTable` use `wow > 0 ? 'good' : wow < -5 ? 'bad' : 'warn'` — asymmetric threshold. The `cls()` helper already uses symmetric ±5%. Also truthy guard fails on legitimate-zero priors.
- **Fix:** Introduce `safeWoW(cur, prev)` helper handling null / 0-prior / same-zero cases. Use `cls(rawPct, false)` for class assignment so thresholds match existing helper.
- **Verification:** With today's data, all WoW cells render identically (no current market has 0-prior or is in the ±0.5 to ±5 asymmetry range that would shift color). Helper protects against future metrics that could legitimately be 0-prior.
- **Commit:** `efd9082`

### WR-C2 · Two-timestamp collapse
- **Source:** wbr #8 (LOW)
- **Status:** done
- **Finding:** Header `#dataTs` and footer `#genTs` say similar things; footer is page-render time (always now).
- **Fix:** Removed `#genTs` element + its JS write. Sharpened header to `Data as of Sun Apr 27 · Forecast through W17`.
- **Verification:** Only one timestamp on the page. Footer region is blank (element removed from HTML). `document.getElementById('genTs')` returns null.
- **Commit:** <filled after commit>

### WR-C3 · Callout headline de-duplication
- **Source:** wbr #3 (MED)
- **Status:** open
- **Finding:** Callout narrative renders `full_callout` which starts with the same text as `headline`. H3 says "W17 — US" (generic scaffolding) while headline is the real one-liner.
- **Fix:** H3 carries the headline. Meta line above gives market/week/period. Body strips headline prefix from `full_callout`.

### WR-C4 · Regs/Pred column collapse → vs-Pred delta
- **Source:** wbr #2 (HIGH)
- **Status:** open
- **Finding:** Weekly detail table shows `regs` and `pred` columns. For future weeks both render `pred_regs` — same number, two columns.
- **Fix:** Keep Regs (actual or pred for future). Replace Pred column with "vs Pred" delta (past rows show calibration %; future rows show —).

### WR-C5 · Remove Projections sub-panel from callout card
- **Source:** r1 C1 (REMOVE)
- **Status:** open
- **Finding:** Projections sub-panel in callout card duplicates what projection.html is for. Creates boundary confusion.
- **Fix:** Delete `#sec-projections` block + `renderProj` + `pc` functions + `.wr-proj-*` CSS + "Projections" TOC link. Projection data still feeds the OP2 Pacing tile (WR-C6) via a smaller extractor.

### WR-C6 · KPI tile cleanup — remove YE Pred + replace OP2 Target with OP2 Pacing
- **Source:** r1 C2 + r1 B4 + wbr #6 (merged)
- **Status:** open
- **Finding:** KPI row has Year-End Pred (projection-engine territory) and OP2 Target (passive — user does the pacing subtraction). Replace both with one directional OP2 Pacing tile.
- **Fix:** Remove YE Pred conditional block. Replace OP2 Target with a `vs OP2` tile: pct delta as headline, `+N regs ahead of M plan` subtitle, `cls()`-thresholded color. Pulls from `last.regs / last.op2_regs` (keeps existing wiring) AND/or `callout.projections.month_end.vs_op2_spend` for month-end pacing.

### WR-C7 · EU5 member-market gap (UK/DE/FR/IT/ES)
- **Source:** wbr #4 (MED)
- **Status:** open
- **Finding:** Market filter uses intersection of callout + forecast markets. Callouts only has 7; forecast has 12. UK/DE/FR/IT/ES never render as tabs.
- **Fix:** Use union. Mark forecast-only markets with `†` + dashed border. Selecting one renders KPIs / chart / table normally; callout section shows empty state.

### Tier B — Density + typography

### WR-B1 · Controls row rebalance (metric as segmented control)
- **Source:** wbr #7 (LOW)
- **Status:** open
- **Finding:** Metric tab row gets as much horizontal space as all 7 market tabs via `margin-left:auto`. Metric is secondary — should be tighter.
- **Fix:** Metric group uses connected 3-cell segmented control. Labels shortened (Regs / Cost / CPA).

### WR-B2 · Typography token sweep (local overrides → tokens)
- **Source:** r1 B1 + wbr #12 (merged; rides on MPE P5-12)
- **Status:** open
- **Finding:** MPE P5-12 introduced `--size-ui` but weekly-review has local overrides (`.pred-lbl` 10px, `.wr-proj-value` 20px, `.wr-proj-ci` 11px, `.wr-list li.important::before` 9px, a few inline styles).
- **Fix:** Sweep to `var(--size-*)` tokens. Add `--size-kpi-value: 20px` (or reuse `--size-section`) for the KPI-value case if needed. After WR-C5 lands, `.wr-proj-*` overrides are already gone.

### WR-B3 · Now-line on default chart (weekly-review only)
- **Source:** wbr #11 (MED)
- **Status:** open
- **Finding:** canon-chart.js defines `NOW_GREEN` but tracker + calibration modes never add it as an annotation. Seam between actual and prediction is subtle.
- **Fix:** Add `todayLine` annotation to tracker/calibration modes in canon-chart.js. Scope carefully — projection.html's scenario mode already has its own todayLine; don't double-add. Safe path: annotation only rendered when `opts.mode` is `default` or `calibration`.

### Tier C — State + polish

### WR-P1 · Week selector latest-default + URL state
- **Source:** r1 B3 (MED)
- **Status:** open
- **Finding:** `curWeek = CALLOUTS.weeks[0]` works by coincidence (weeks is newest-first). No URL state — can't deep-link.
- **Fix:** Pick latest week with both callout AND forecast data for `curMarket`. Read `?market=X&week=W17` on load. Write via `history.replaceState` on change.

### WR-P2 · Metric-tab persist per market (localStorage)
- **Source:** r1 B2 (MED)
- **Status:** open
- **Finding:** `curMetric = 'regs'` is module-level and resets every reload. JP/AU are spend-only; regs is degenerate there.
- **Fix:** `metricByMarket` map in localStorage. JP/AU default to `cost` on first visit.

### Tier D — Differentiation (forecast grading rubric)

### WR-D1 · Forecast Hit Rate scorecard (new top section)
- **Source:** r1 A1 (ADD)
- **Status:** open
- **Finding:** Weekly review lacks the one analytical capability projection engine can't have — grading the forecast. Scorecard surfaces first-pred error, latest-pred error, in-CI rate across last N weeks.
- **Fix:** `#sec-scorecard` above KPI row. 3 tiles computed from `predictions_history[market][wk]`. Auto-narrative summarizing the three numbers. Empty state: "Not enough history — need 3+ weeks of predictions to score the model."

### WR-D2 · Promote calibration chart to first-class panel (with axis toggle)
- **Source:** r1 A2 + wbr #10 (merged)
- **Status:** open
- **Finding:** Calibration chart is hidden behind `chartModeBtn` toggle. It's the most valuable chart on the page and nobody sees it. When promoted, calibration needs regs-only default (current "both axes" is 7 lines — over Richard's 3-line budget).
- **Fix:** Two panels — "What happened" (default mode) and "How did we do" (calibration mode). `chartModeBtn` removed. Calibration panel has its own regs-only / spend-only / both axis toggle, defaulting to regs-only. `buildCalibrationDatasets` accepts `axisFilter` param.

### WR-D3 · Callout narrative goes first
- **Source:** r1 A3 (HIGH)
- **Status:** open
- **Finding:** Narrative is buried at the bottom, behind the tracker section + a divider. Leader's first read should be the narrative.
- **Fix:** Move `#sec-callout` immediately after `.wr-controls`, before scorecard + KPIs. Brand/NB + External + Drivers + Stakeholders remain at the bottom. Remove "Callout context for selected week" divider.

### WR-D4 · Since-last-week auto-summary
- **Source:** wbr #5 (HIGH)
- **Status:** open
- **Finding:** Leader's #1 question is "what changed since last week?" Dashboard has every data point but makes the reader parse it out of the narrative prose.
- **Fix:** Two-line summary above the callout narrative. Regs / Spend / CPA WoW deltas + optional divergence callout (Brand softens while NB grows).

### WR-D5 · Three-question framing (customer / business / pacing)
- **Source:** r1 A6 (HIGH)
- **Status:** open
- **Finding:** KPI row has no narrative through-line. Amazon WBR convention asks three ordered questions — customer experience → business performance → pacing to target.
- **Fix:** Three cards below the callout narrative. 8-14 words each. Content derived from `callout.metrics + brand_detail + nb_detail + projections.month_end.vs_op2_spend`. Empty-state for pacing when `projections` is `{}` (current weeks).

### WR-D6 · Variance decomposition panel
- **Source:** r1 A4 (ADD)
- **Status:** open
- **Finding:** Narrative describes what changed; dashboard doesn't visually decompose it. Kate asks for this verbally.
- **Fix:** `#sec-variance` after narrative. Waterfall table: prior-week base → NB delta → Brand delta → residual → current-week total. Positive green, negative red. Empty state when only one channel's data is present.

### WR-D7 · Prior-week thread strip
- **Source:** r1 A5 (ADD)
- **Status:** open
- **Finding:** Each week stands alone — no context of the two prior weeks. Reader has to click back to see the trend.
- **Fix:** 3-card strip above the callout narrative. Current + 2 prior weeks. Current highlighted with brand-blue border. Refreshes on market/week change.

---

## Order of work

Execute top-to-bottom. When a finding is blocked, mark the reason in-place
and move to the next. Never silently skip.

1. WR-C1 safeWoW
2. WR-C2 timestamp collapse
3. WR-C3 headline de-dup
4. WR-C4 Regs/Pred column → vs-Pred delta
5. WR-C5 remove Projections sub-panel
6. WR-C6 KPI tile cleanup (YE Pred + OP2 Target → OP2 Pacing)
7. WR-C7 EU5 member-market union
8. WR-B1 controls row rebalance
9. WR-B2 typography token sweep
10. WR-B3 now-line on default chart
11. WR-P1 URL state + latest-week default
12. WR-P2 metric-tab persist per market
13. WR-D1 Forecast Hit Rate scorecard
14. WR-D2 calibration first-class + axis toggle
15. WR-D3 narrative first
16. WR-D4 since-last-week summary
17. WR-D5 three-question framing
18. WR-D6 variance decomposition
19. WR-D7 prior-week thread
