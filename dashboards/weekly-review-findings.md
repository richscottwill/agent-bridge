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

Both bundles audited against live code + data before execution. 19 reconciled
findings shipped in 17 commits (WR-B3 verified-already-done, no commit).

---

## Sprint summary — shipped 2026-04-28

| # | Finding | Status | Commit |
|---|---|---|---|
| WR-C1 | safeWoW helper (symmetric WoW thresholds + 0-prior guard) | done | `efd9082` |
| WR-C2 | Two-timestamp collapse (single header freshness) | done | `edfea36` |
| WR-C3 | Callout headline de-duplication | done | `760e193` |
| WR-C4 | Regs/Pred column → vs-Pred delta | done | `6d5f486` |
| WR-C5 | Remove Projections sub-panel | done | `7c42d2e` |
| WR-C6 | KPI cleanup — drop YE Pred + add OP2 Pacing | done | `bac7382` |
| WR-C7 | EU5 member-market union (UK/DE/FR/IT/ES) | done | `b634b05` |
| WR-B1 | Metric controls as segmented control | done | `27f586f` |
| WR-B2 | Typography token sweep | done | `4d842d0` |
| WR-B3 | Now-line on default chart | done (already present in canon-chart.js) | n/a |
| WR-P1 | URL state + explicit latest-week default | done | `2de9a5c` |
| WR-P2 | Metric-tab persists per market | done | `0273fac` |
| WR-D1 | Forecast Hit Rate scorecard | done | `268cece` |
| WR-D2 | Calibration first-class panel + axis toggle | done | `97a8ca2` |
| WR-D3 | Callout narrative goes first | done | `982f523` |
| WR-D4 | Since-last-week auto-summary | done | `15ee67a` |
| WR-D5 | Three-question WBR framing | done | `f1dc7d2` |
| WR-D6 | Variance decomposition waterfall | done | `bb213f6` |
| WR-D7 | Prior-week thread strip | done | `a2ea608` |

Findings doc seeded in `c057d9f` (reconciliation + backlog).

---

## Reconciliation with live code (2026-04-28 audit)

Before executing I ran a live audit — Local Kiro's claims need grounding, per
the logged discipline "audit bundled specs against live code before executing."

**Verified claims:**
- `predictions_history` exists in `forecast-data.json` for all 12 markets incl. EU5 — A1 scorecard has its data.
- `brand_detail.lw_regs` + `nb_detail.lw_regs` exist in `callout-data.json` — A4 variance decomposition CAN derive WoW deltas.
- `metrics.regs_wow / spend_wow / cpa_wow` exist — since-last-week summary has fields.
- Line 762 weekly-review.html `wow > 0 ? 'good' : wow < -5 ? 'bad' : 'warn'` — wbr-#1 asymmetry bug was real.
- Line 446 `chartModeBtn` — wbr-#9 toggle was real; became moot after r1-A2 (toggle removed in favor of two panels).
- Line 786 `Year-End Pred` tile — real; r1-C2 + wbr-#6 agreed it should go.
- Line 512 market filter used intersection — wbr-#4 EU5 gap was real. Callout markets = 7, forecast markets = 12.
- `predictions_history[market][wk]` has richer shape than the spec assumed: `first_pred`, `latest_pred`, `actual`, `first_ci_lo/hi`, `latest_ci_lo/hi`, `error_pct`, `score` (HIT/MISS) — A1 is well-fed.

**Partial/conditional claims:**
- `callout.projections` is **empty `{}`** for current weeks (W17/W16) on all markets. Populated only on W15 and earlier. **WR-D5 qPacing and WR-C6 OP2 Pacing** have empty-state fallbacks on current weeks until the next refresh-callouts.py run populates them. Not a blocker — empty states shipped as part of the spec.

**Bundle overlaps resolved:**
- r1-B4 (OP2 pacing tile) + wbr-#6 (replace passive OP2 Target with vs-OP2 delta) + r1-C2 (remove YE Pred) → one commit (WR-C6) replacing YE Pred with a directional OP2 pacing tile.
- r1-A2 (calibration first-class) + wbr-#10 (reduce calibration line count) → one commit (WR-D2) promoting calibration AND defaulting to regs-only axis inside the new panel.
- r1-B1 (typography lock, rides MPE P5-12) + wbr-#12 (token sweep on local overrides) → one commit (WR-B2) sweeping the .pred-lbl / .wr-proj-* / .wr-list local overrides to tokens.
- wbr-#9 (chart mode toggle state) became moot after r1-A2 landed — dropped.

---

## Order of work (shipped)

1. ✅ WR-C1 safeWoW
2. ✅ WR-C2 timestamp collapse
3. ✅ WR-C3 headline de-dup
4. ✅ WR-C4 Regs/Pred column → vs-Pred delta
5. ✅ WR-C5 remove Projections sub-panel
6. ✅ WR-C6 KPI tile cleanup (YE Pred + OP2 Target → OP2 Pacing)
7. ✅ WR-C7 EU5 member-market union
8. ✅ WR-B1 controls row rebalance
9. ✅ WR-B2 typography token sweep
10. ✅ WR-B3 now-line on default chart (already-done verification)
11. ✅ WR-P1 URL state + latest-week default
12. ✅ WR-P2 metric-tab persist per market
13. ✅ WR-D1 Forecast Hit Rate scorecard
14. ✅ WR-D2 calibration first-class + axis toggle
15. ✅ WR-D3 narrative first
16. ✅ WR-D4 since-last-week summary
17. ✅ WR-D5 three-question framing
18. ✅ WR-D6 variance decomposition
19. ✅ WR-D7 prior-week thread

**Sprint closed** — 19 / 19 shipped.

## Known follow-ups (out of sprint scope)

- **canon-chart.js light-theme polish:** the tracker/calibration render path still has hardcoded dark-theme axis tick colors (`#666` / `#1f222b`) and `color: '#4ade80'` on the nowLine label. Contrast is adequate on the light background but not polished. Low priority; pick up in a dedicated chart-polish commit.
- **Current-week projections populate:** WR-C6 OP2 Pacing and WR-D5 qPacing will remain in their weekly-fallback form on W17/W16 until `refresh-callouts.py` runs and populates `callout.projections.month_end.vs_op2_spend` for the current weeks. Pipeline concern, not code.

---

## R2 proposals (Local Kiro, 2026-04-28) — forecasting-platform research pass

Second-round ideas grounded in research on Good Judgment Open, Polymarket,
Metaculus, and Robinhood Advanced Charts. Source file:
`~/shared/context/intake/weekly-review-r2-handoff-prompt.md` (pasted into
the 2026-04-28 session; not yet in repo).

All R2 items are `open-R2` — research-grounded proposals awaiting Richard's
go-ahead. Not shipped. Data-dependency audit done against live payloads;
gating notes flag items that need pipeline work before shipping.

### WR-A7 · Relative forecast error (benchmark against naive baseline)
- **Source:** R2 (GJO Brier-relative pattern)
- **Priority:** MED · **Effort:** 45 min · **Depends on:** WR-D1
- **Data:** forecast-data.json weekly actuals + predictions_history — sufficient.
- **Status:** open-R2

### WR-A8 · Event annotations on trend chart
- **Source:** R2 (Polymarket context-overlay critique)
- **Priority:** HIGH · **Effort:** 1h (+ pipeline work for structured events)
- **Data audit:** `callout.external_factors` is list of `{text, important}` objects (5 items for US/W17). **Prose only — no structured `{week, label, kind}` triples.** Pinning to specific weeks would require either parsing week references out of prose (fragile) or extending `refresh-callouts.py` to emit structured events. **Gated on callout-pipeline schema extension.**
- **Status:** open-R2 (partially gated)

### WR-A9 · Forecast aging visualization (prediction trajectory per week)
- **Source:** R2 (GJO daily-Brier pattern)
- **Priority:** LOW · **Effort:** 2h + backend
- **Data audit:** `predictions_history[market][wk].regs.n_preds = 1` for all current rows; `first_date == latest_date`. **The week-by-week forecast evolution Local Kiro proposed isn't supported today.** Needs `predictions_history[market][wk]` to become an array of `{date, pred}` snapshots or a separate `prediction_snapshots` table. **Gated on forecast pipeline extension — correctly flagged by Local Kiro.**
- **Status:** open-R2 (gated — schema work required)

### WR-A10 · Scrub-the-chart interaction (cross-page lens)
- **Source:** R2 (Robinhood Advanced Charts)
- **Priority:** HIGH · **Effort:** 2h · **Depends on:** WR-D2, WR-D3, WR-D5
- **Approach:** hovering a chart week swaps KPI row / three-question cards / variance table / callout headline to that week's values. Release → return to selected week. Structural unlock — page becomes an interactive lens instead of a static view. Highest demo value per Local Kiro.
- **Data:** all callout weeks present in CALLOUTS.callouts[market]; no backend work needed.
- **Status:** open-R2

### WR-A11 · Specialized layouts per market archetype
- **Source:** R2 (Polymarket specialized-interface critique)
- **Priority:** MED · **Effort:** 1.5h · **Depends on:** WR-D1, WR-C6
- **Approach:** JP/AU show spend-discipline scorecard (YTD spend vs OP2 spend, CPC trends) instead of regs forecast hit rate. Three market archetypes: regs-and-efficiency (US/EU5/CA/MX), spend-only (JP/AU), rollups (WW/EU5).
- **Status:** open-R2

### WR-B5 · Cross-market accuracy leaderboard strip
- **Source:** R2 (GJO challenge-style leaderboard)
- **Priority:** MED · **Effort:** 1h · **Depends on:** WR-D1
- **Data audit:** predictions_history covers all 12 markets — **fully implementable now.**
- **Approach:** compact horizontal strip above market tabs showing each market's 6-week in-CI rate. Green ≥80%, red ≤50%. Answers "can I trust this market's projection?" in one glance for Kate.
- **Status:** open-R2 (ready to ship)

### WR-B6 · Period-state background tint on callout card
- **Source:** R2 (Robinhood color-state semantics)
- **Priority:** LOW · **Effort:** 20 min + pipeline
- **Data audit:** `callout.period` is plain text range ('Apr 19–25') — **no structured state flag.** Q-close / holiday / refit / normal distinction would need pipeline to emit something like `period_state: 'q_close' | 'holiday' | 'refit' | 'normal'`. **Gated on pipeline.**
- **Status:** open-R2 (gated)

### WR-C3 · Progressive disclosure — collapse secondary panels by default
- **Source:** R2 (Polymarket mobile-first principle)
- **Priority:** MED · **Effort:** 30 min · **Depends on:** R1 verified clean
- **Approach:** wrap Brand+NB cards behind "Channel detail" disclosure, wrap Context+Drivers+Stakeholders behind "Context" disclosure. Cold-load shows thread → narrative → 3Q → KPIs → 2 charts → variance only — the full WBR arc on one screen.
- **Status:** open-R2

### R2 recommended ship order (from Local Kiro)
1. WR-A10 scrub-the-chart (HIGH, 2h) — structural unlock
2. WR-A8 event annotations (HIGH, 1h + pipeline for structured events)
3. WR-C3 progressive disclosure (MED, 30 min)
4. WR-A7 relative error (MED, 45 min)
5. WR-A11 specialized layouts (MED, 1.5h)
6. WR-B5 accuracy leaderboard (MED, 1h — ready-to-ship, ungated)
7. WR-B6 period-state tint (LOW, 20 min + pipeline)
8. WR-A9 forecast aging (LOW, 2h + schema work — gated)

**Ready-to-ship without backend work (priority order):**
A10 → A7 → C3 → A11 → B5 → none-of-the-three-gated

**Gated on pipeline work:** A8 (structured events), A9 (prediction snapshots), B6 (period state flag).

---

## R1 verification probe (2026-04-28)

Static structural analysis written to
`~/shared/context/intake/weekly-review-r1-live-probe.txt`. 19/19 R1 findings
pass static checks (1 verification-only for WR-B3 confirmed in canon-chart.js).
Live browser probe pending — Local Kiro's chrome-devtools-mcp lock on
Richard's Windows side, not clearable from DevSpaces. Static analysis covers
15 of 19 checklist items directly; the other 4 (scrollHeight, viewport,
`getBoundingClientRect` positions, distinct computed font-sizes) need a real
browser.

**One follow-up commit triggered by probe:** `2e14a8d` WR-B2 follow-through
swapped the last literal `24px` (`.wr-score-value` from WR-D1 scorecard)
to `var(--size-section)`. Zero literal-px font-sizes remain in
weekly-review.html.

---

## R2 consolidated (Local Kiro cold-load probe, 2026-04-29)

Second review round — Local Kiro cleared the chrome-devtools-mcp lock and ran
live probes across WW/US/EU5/JP. Found 3 bugs, 10 nit-polish items, 4
structural moves (in addition to the 8 R2 research ideas already seeded).

Source files:
- `~/shared/context/intake/weekly-review-r1-verification-results.md` — 12 pass / 2 partial / 0 fail + Bug 1-3 root causes
- `~/shared/context/intake/weekly-review-r2-consolidated-mockup.html` — 23 findings with probe evidence + code snippets
- `~/shared/context/intake/weekly-review-r2-consolidated-preview.png` — rendered preview

**Data-dependency audit (live) before execution:**
- Bug 1 (three-Q empty on WW): `c.market_breakdown` that Local Kiro's fix uses **doesn't exist** in callout-data.json. WW rollup brand_detail/nb_detail carry only {regs, regs_yoy, regs_vs4wk} — no `cpa_wow / cvr_wow / lw_regs`. Per-country markets carry the full field set. Real fix: use `metrics.cpa_yoy` + `metrics.cpa_vs4wk` for card 1 on WW, derive card-2 WoW from prev-week callout lookup (WW W16 metrics exist).
- Bug 2 (variance empty on WW): WW brand_detail has no `lw_regs`. Fix: aggregate per-country brand/nb lw_regs + regs across the 10 per-country markets. Totals land within ~1% of WW metrics.regs (verified: Brand 7,143 + NB 10,185 = 17,328 vs WW metrics 17,484, residual 156 regs).
- Bug 3 (section-freshness 404): root cause is regex in `resolveManifestPath()` — assumes URLs contain `/dashboards/` but localhost:8080 serves `~/shared/dashboards/` at root so URLs don't carry that prefix. Regex match fails → depth 0 → page-relative `data/` → 404 on `/performance/data/`. Fix: depth from `location.pathname.split('/').filter(Boolean).length - 1`.

### Bugs (Tier A — Sprint 1)

### WR-B1-1 · Three-question cards 1+2 empty on WW rollup
- **Source:** R2 consolidated #1 (BUG)
- **Priority:** HIGH · **Effort:** 30 min · **Depends on:** none
- **Status:** open
- **Fix:** rollup branch in `renderThreeQ` synthesizes card 1 from `metrics.cpa_yoy + cpa_vs4wk`, card 2 from `metrics.regs` + YoY + dominant-channel (Brand vs NB) from metrics.

### WR-B1-2 · Variance waterfall empty on WW rollup
- **Source:** R2 consolidated #2 (BUG)
- **Priority:** HIGH · **Effort:** 45 min · **Depends on:** none
- **Status:** open
- **Fix:** aggregate per-country brand_detail.lw_regs + nb_detail.lw_regs across the 10 member markets of the rollup for WoW decomposition. Residual catches the mix shift.

### WR-B1-3 · section-freshness.json 404 (cosmetic)
- **Source:** R2 consolidated #3 (BUG — cosmetic)
- **Priority:** MED · **Effort:** 10 min · **Depends on:** none
- **Status:** open
- **Fix:** `resolveManifestPath()` uses regex that assumes `/dashboards/` in URL. Compute depth from `location.pathname.split('/').filter(Boolean).length - 1` instead.

### Polish (Tier B — Sprint 2)

### WR-P3 · `.sec-panel` computed padding is 0px
- **Source:** R2 consolidated #4 (polish)
- **Priority:** HIGH · **Effort:** 10 min · **Depends on:** none
- **Status:** open
- **Fix:** Add `.sec-panel { padding: var(--gap-lg) var(--gap-xl) }` so cards match MPE's 20px/24px content breathing room.

### WR-P4 · 152px dead gap between sec-scorecard and sec-trend
- **Source:** R2 consolidated #5 (polish)
- **Priority:** HIGH · **Effort:** 15 min · **Depends on:** WR-S2
- **Status:** open
- **Fix:** Grid container auto-height with `align-items: start`. Also addressed structurally by WR-S2 (side-by-side scorecard+KPIs).

### WR-P5 · TOC link order doesn't match rendered order
- **Source:** R2 consolidated #6 (polish)
- **Priority:** MED · **Effort:** 10 min · **Depends on:** none
- **Status:** open
- **Fix:** Reorder `.wr-toc` anchor list to match rendered order post-D3 narrative-first: Callout → Variance → KPIs → Scorecard → Trend → Calibration → Detail → Channels → Context.

### WR-P6 · Narrative card uses H3 for body prose (screen-reader issue)
- **Source:** R2 consolidated #7 (polish / a11y)
- **Priority:** MED · **Effort:** 15 min · **Depends on:** none
- **Status:** open
- **Fix:** Change `.wr-callout-headline` from H3 to a paragraph with bold weight. H3s should be navigable landmarks, not body prose.

### WR-P7 · Heading hierarchy skips H2
- **Source:** R2 consolidated #8 (a11y)
- **Priority:** MED · **Effort:** 15 min · **Depends on:** WR-P6
- **Status:** open
- **Fix:** Promote section titles (Scorecard, KPIs, Trend panels, etc.) to H2 so the page hierarchy reads H1 → H2 (section) → H3 (sub-block) properly.

### WR-P8 · Zero semantic landmarks (no `header`, `main`, `nav`, `aside`)
- **Source:** R2 consolidated #9 (a11y)
- **Priority:** MED · **Effort:** 20 min · **Depends on:** none
- **Status:** open
- **Fix:** Wrap `.wr-header` in `<header>`, content in `<main>`, TOC in `<nav>`. Thread strip gets `role="region" aria-label="Recent weeks"`.

### WR-P9 · Canvas missing aria-label + role="img"
- **Source:** R2 consolidated #10 (a11y)
- **Priority:** MED · **Effort:** 10 min · **Depends on:** none
- **Status:** open
- **Fix:** `<canvas id="trendChart" role="img" aria-label="Weekly registrations + OP2">` and analogous for calibrationChart.

### WR-P10 · Week selector `<select>` has no accessible label
- **Source:** R2 consolidated #11 (a11y)
- **Priority:** MED · **Effort:** 5 min · **Depends on:** none
- **Status:** open
- **Fix:** Add `aria-label="Week"` to `#weekSelect`, OR wrap in a `<label>`.

### WR-P11 · Thread strip lacks `role="group"` + aria-label
- **Source:** R2 consolidated #12 (a11y)
- **Priority:** LOW · **Effort:** 5 min · **Depends on:** none
- **Status:** open
- **Fix:** `<div class="wr-thread-strip" role="group" aria-label="Recent weeks">`.

### WR-P12 · Calibration H3 swallows axis toggle (nested, not adjacent)
- **Source:** R2 consolidated #13 (a11y + structure)
- **Priority:** LOW · **Effort:** 10 min · **Depends on:** none
- **Status:** open
- **Fix:** Move the `.wr-chart-axis-toggle` outside the H3; use a flex header row so h3 + toggle are siblings.

### Structural (Tier C — Sprint 1 + 2)

### WR-S1 · Progressive disclosure on secondary panels
- **Source:** R2 consolidated #14 (structure)
- **Priority:** HIGH · **Effort:** 30 min · **Depends on:** none
- **Status:** open
- **Fix:** Wrap `#sec-detail`, `#sec-channels`, `#sec-context` in `<details>` tags collapsed by default. Page lands under ~1,800px cold. Full WBR arc above the fold.

### WR-S2 · Scorecard + KPIs side-by-side
- **Source:** R2 consolidated #15 (structure)
- **Priority:** MED · **Effort:** 20 min · **Depends on:** none
- **Status:** open
- **Fix:** Grid-layout `#sec-scorecard` and KPI row in a 2-col layout at wide viewport. Eliminates the 152px vertical gap and matches how Kate reads "where are we vs how good is the forecast" in one glance.

### WR-S3 · Brand/NB channel cards show empty rows on WW rollup
- **Source:** R2 consolidated #16 (structure)
- **Priority:** LOW · **Effort:** 30 min · **Depends on:** none
- **Status:** open
- **Fix:** On rollup markets (WW/EU5/NA), channel cards show "Channel breakdown not available on rollup — see per-market views" OR a synthesized table of which markets contribute most to Brand vs NB totals.

### WR-S4 · Weekly detail scroll-within-scroll trap
- **Source:** R2 consolidated #17 (structure)
- **Priority:** LOW · **Effort:** 15 min · **Depends on:** WR-S1
- **Status:** open
- **Fix:** Remove `max-height: 520px; overflow: auto` on `.wr-table-scroll`. Once WR-S1 wraps in `<details>`, the table flows inline at full height when expanded.

---

---

## Sprint 1+2 complete (2026-04-29)

All 17 R2-consolidated findings shipped. Mapping:

| Finding | Status | Commit |
|---|---|---|
| WR-B1-1 three-Q rollup-aware | done | `de341a2` |
| WR-B1-2 variance rollup aggregate | done | `988e402` |
| WR-B1-3 section-freshness path | done | `2ee99bc` |
| WR-P3 .sec-panel padding shared | done | `d368f4d` |
| WR-P4 scorecard/KPI 152px gap | done (via WR-S2) | `552bbdb` |
| WR-P5 TOC order | done | `7dc8b3e` |
| WR-P6 callout h3 → p | done | `80deb63` |
| WR-P7 heading hierarchy | done (via P6 + landmarks) | `80deb63` |
| WR-P8 semantic landmarks | done | `80deb63` |
| WR-P9 canvas role/aria | done | `80deb63` |
| WR-P10 week select aria-label | done | `80deb63` |
| WR-P11 thread strip role/aria | done | `80deb63` |
| WR-P12 calib H3/toggle split | done | `80deb63` |
| WR-S1 progressive disclosure | done | `d72c00e` |
| WR-S2 KPI+scorecard side-by-side | done | `552bbdb` |
| WR-S3 rollup channel cards | done | `ecef1c8` |
| WR-S4 table scroll-within-scroll | done (pair of WR-S1) | `d72c00e` |

Sprint 3 (WR-A7 through WR-C3 — 6 R2 research ideas) deferred until Richard
greenlights. Three items (A8/A9/B6) remain pipeline-gated per prior audit.

Probe-flagged follow-up that slipped through R1 typography sweep:
commit `2e14a8d` swapped `.wr-score-value` 24px literal to `var(--size-section)`.

---

## Sprint 3 complete (2026-04-30)

All 5 ready-to-ship R2 research ideas landed in one pass.

| Finding | Status | Notes |
|---|---|---|
| WR-C3 progressive disclosure split | done | Split prior one-disclosure block into two: `#calloutChannelsWrap` (Brand + NB) and `#calloutContextWrap` (external factors, drivers, stakeholders). TOC anchors updated. Legacy `#calloutGrid` retained hidden as error-sink. |
| WR-B5 accuracy leaderboard | done | New `.wr-leaderboard` strip above controls. Per-market pills show `hits/graded` in-CI rate over last 6 weeks, color-banded green ≥80%/amber 60-79%/red <60%/grey insufficient. Pills click-through to that market. |
| WR-A7 relative forecast error | done | 4th scorecard tile "Skill vs naive" = 1 − MAE_model / MAE_naive (drift-1 baseline). Positive = model beats naive. Grid now `repeat(4, 1fr)` collapsing to 2×2 under 900px, 1×4 under 500px. Added to scorecard auto-narrative. |
| WR-A11 specialized layouts | done | `ARCHETYPE` map classifies markets: regs-and-efficiency (US/EU5/CA/MX/UK/DE/FR/IT/ES), spend-only (JP/AU), rollup (WW/EU5/NA). Spend-only applies `body.wr-arch-spend` class which highlights the scorecard and prefixes its title with "Spend-discipline view ·". Default metric for JP/AU was already `cost` via existing `defaultMetricForMarket`. |
| WR-A10 scrub-the-chart | done | Hovering the trend chart sets `scrubWeek`, re-renders callout narrative + three-question cards + variance table against the hovered week. Mouseleave returns to `curWeek`. Fixed overlay badge at top of viewport shows active scrub state. Ungated panels (KPIs, scorecard, leaderboard, table) stay on `curWeek` since their semantics are cumulative/market-wide, not weekly. |

**Still open (pipeline-gated):**
- **WR-A8** event annotations on trend chart — needs `refresh-callouts.py` to emit structured `events: [{week, label, kind}]` per market instead of prose `external_factors`.
- **WR-A9** forecast aging visualization — needs `predictions_history[market][wk]` to become an array of `{date, pred}` snapshots. Prior session (2026-04-29) wired DELETE-INSERT snapshotting in `write_v1_1_slim_forecasts.py` but the export path still collapses to one `latest_pred` per week.
- **WR-B6** period-state background tint — needs `refresh-callouts.py` to emit `period_state` enum (`q_close` / `holiday` / `refit` / `normal`).

All three are backend work, not weekly-review HTML edits.

---

## Sprint 3 pipeline-gated items shipped (2026-04-30 afternoon)

| Finding | Status | Notes |
|---|---|---|
| WR-A9 forecast aging | done | Gate was stale — snapshotting had already landed 2026-04-29. `predictions_history` already had 34-38 weeks/market with `n_preds>1`. Added a 6-week drift strip inside the scorecard showing first/latest/actual bars per week. Commit `aa7d4d9`. |
| WR-A8 event annotations | done | Added `extract_event_weeks` parser in `refresh-callouts.py` that walks `external_factors` text, extracts `W\d+` tokens, classifies into `streak`/`shift`/`note` kinds, emits structured `events: [{id, weeks, text, kind, important}]` per callout. Dashboard passes these to `CanonChart.render` as `eventAnnotations`, which draws kind-colored dashed verticals on the trend chart with staggered labels. Live: 73 events generated across 76 market-weeks. |
| WR-B6 period-state tint | done | Added `compute_period_state` in `refresh-callouts.py` that classifies each week as `refit` (has `ps.regime_changes` row, half_life>0, not structural_baseline) > `holiday` (market-specific lookup) > `q_close` (W13/26/39/52) > `normal`. Dashboard applies `.period-refit` / `.period-holiday` / `.period-q_close` class to `.wr-callout-main` with gradient tint + left border, plus a pill badge next to the market/week meta. Live: 12 q_close + 3 refit + 61 normal. |
| (regression fix) | done | Restored `mode: 'error'` on the "How did we do" chart. Commit `6db6182` (karpathy W18 batch catch-up) silently reverted it to `mode: 'calibration'` along with matching header/aria-label strings. Same class of karpathy regression that broke 13 hooks — content-quality evaluator missed a semantic regression (chart type change). Flagged for karpathy-file-type-awareness steering extension. |

**All 8 R2 findings now shipped. Sprint 3 fully closed.**

---

## M1 shipped (2026-04-30)

First of the 10 mockup-driven redesigns landing from the dashboard-research report.
See `context/intake/dashboard-research/mockups/README.md` for full M1-M10 spec + ship order.

| Finding | Status | Notes |
|---|---|---|
| M1 · Sticky header + trust bar + TOC collapse | done | Single `.wr-stick` row replaces the prior `.wr-leaderboard` + `.wr-controls` + `#regionTabs` + `#submarketTabs` + `#metricTabs` vertical stack. Trust bar (12 pills, one per market) now IS the region filter — green ≥5/6 in-CI / amber 3-4/6 / red ≤2/6 / grey insufficient. Click-to-select wired via new shared `window.TrustBar.renderTrustBar()` helper at `dashboards/shared/trust-bar.js` + companion `trust-bar.css`. EU5 drill-down works natively — UK/DE/FR/IT/ES are independent pills in the bar. TOC collapsed into `<details>` "Sections ▾" dropdown per #014 (frees ~40px top-of-fold). Week prev/next + select kept in the sticky right-edge. Legacy DOM hooks (#regionTabs, #metricTabs, #submarketTabs, #leaderboardPills, #accuracyLeaderboard) kept hidden for script compatibility until M3 retires the metric-filter wiring. Verified: sticky at scrollY=2000, click on MX pill switches market + URL, Sections menu opens with 10 anchor links, console clean. |

**Follow-ups:**
- **MPE side of #075 unification:** `projection.html` still renders its own `.market-pulse-strip`. The new `TrustBar` helper is designed to be consumed from MPE too (pluggable `computeState` per page — WR supplies `computeForecastTrust`, MPE will supply a distance-to-target equivalent). Not shipped in this commit to keep it reviewable; planned as a follow-up in the same M1 scope.
- **Legacy DOM removal:** the hidden `#regionTabs`, `#submarketTabs`, `#metricTabs` divs stay until M3 lands. `init()` still writes to them. No user-visible effect.
