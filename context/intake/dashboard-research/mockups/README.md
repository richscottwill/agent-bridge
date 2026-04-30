# Dashboard redesign mockups — handoff for kiro-server

**From:** kiro-local
**Date:** 2026-04-30
**Companion:** `../dashboard-redesign-report.html` (full 100-suggestion research report)

## What this is

10 high-fidelity static mockups of the Tier-1 changes from the full redesign report, with implementation-ready specs. Each mockup shows the target rendered state, specifies the file + selectors + data fields to change, and points to the cited design source (Amazon WBR / Stephen Few / Tufte / BoE fan chart / etc.).

## Files

| File | Purpose |
|---|---|
| `mockups.html` | Source — open in a browser to see all 10 mockups rendered |
| `screenshots/00-all-mockups-fullpage.png` | Full scroll of the mockups page for quick preview |
| `screenshots/m1-sticky-header.png` | M1 · sticky trust bar + week nav + title |
| `screenshots/m2-headline-exception.png` | M2 · WBR-style headline + conditional red exception banner |
| `screenshots/m3-kpi-sparklines.png` | M3 · 4-up KPI cards, each with inline sparkline or bullet |
| `screenshots/m4-bullet-chart.png` | M4 · Stephen Few bullet chart (shared component) |
| `screenshots/m5-reliability-diagram.png` | M5 · reliability diagram + signed-error bars |
| `screenshots/m6-small-multiples.png` | M6 · 12 markets × 6-week actuals-vs-OP2 small multiples |
| `screenshots/m7-612-chart.png` | M7 · Amazon 6-12 chart (6 wk weekly + 12 mo monthly) |
| `screenshots/m8-prior-week-thread.png` | M8 · 6-cell sparkline strip replacing text pager |
| `screenshots/m9-fan-chart.png` | M9 · MPE projection as fan (50/80/90 CI bands) |
| `screenshots/m10-waterfall-variance.png` | M10 · waterfall variance decomposition |

## Ship order (recommended)

Each commit is a standalone improvement. Pick any order that matches your current context; the numbering below is just the "if I had to pick one sequence" recommendation.

**Work split (agreed on bus thread 2026-04-30_dashboard-mockups-handoff):**
- **kiro-server takes:** M9 (fan chart + CI widths emission commit pair) + M5 (reliability diagram + signed-error bars).
- **kiro-local takes:** M1 (including unification + TOC collapse) + M3 (including shared `renderSparkline` / `renderBullet` helpers) + M7 (6-12 chart in `canon-chart.js`).
- **Either:** M2, M4, M6, M8, M10.

| # | Mockup | File(s) | Effort |
|---|---|---|---|
| 1 | M1 · sticky header + trust bar (+ WR/PE unification + TOC collapse) | `performance/weekly-review.html` + `projection.html` + new shared `renderTrustBar()` helper | 3-4h |
| 2 | M2 · headline + exception banner | `performance/weekly-review.html` | 1.5h |
| 3 | M3 · KPI cards with sparklines | `performance/weekly-review.html` + new `renderSparkline` / `renderBullet` helpers | 2h |
| 4 | M4 · bullet chart component | shared helper, consumers: WR KPI row (M3), MPE distance-to-target | 0h (ships with M3) |
| 5 | M5 · reliability diagram + signed bars | `performance/weekly-review.html` + `canon-chart.js` | 2.5h |
| 6 | M6 · small multiples | `performance/weekly-review.html` (new section) | 2h |
| 7 | M7 · 6-12 chart | `canon-chart.js` (new `mode: 'wbr612'`) | 3h |
| 8 | M8 · prior-week sparkline thread | `performance/weekly-review.html` — `renderThreadStrip()` | 1h |
| 9 | M9 · fan chart | `projection.html` | 2h |
| 10 | M10 · waterfall variance | `performance/weekly-review.html` — `renderVariance()` | 1.5h |

**Total: ~19-20h across 10 commits** (original 18h + 1-2h added to M1 for unification + TOC collapse per kiro-server feedback on thread 2026-04-30_dashboard-mockups-handoff post 003).

## Implementation spec summary per mockup

### M1 — Sticky header + trust bar (absorbs filters; unified across WR + PE; TOC collapsed)
- **Replace:** `.wr-leaderboard` + `.wr-controls` + `#regionTabs` + `#submarketTabs` + `#metricTabs` + `#weekSelect` → single `<header class="wr-stick">` with title / trust-bar / week-nav.
- **Shared helper (new):** `renderTrustBar(markets, selectedMarket, onSelect)` — extracted as a shared module so **both** `weekly-review.html` and `projection.html` consume identical DOM + styles. Per suggestion #075 in the full report ("market health bar on PE and forecast trust bar on WR must render identically. Same pill shape, same color stops, same hover affordance, same click-to-select behavior."). Ships with M1, not a follow-up.
- **TOC collapse (per #014 + #067):** the 40px always-visible Jump-to strip collapses into a "Sections ▾" hover menu inside the sticky header. Frees top-of-fold on every page load. Optional T3 follow-up: vim-style `g then c` shortcut + `?` help overlay.
- **URL-state back-compat:** stale `?metric=regs` params in backlinks from email/Slack must be silently ignored (not 404). Preserve `?market=X&week=W17` behavior exactly.
- **Data:** trust pills use existing `renderAccuracyLeaderboard()` derivation; class mapping `on` ≥5/6 · `mid` 3-4/6 · `off` ≤2/6 · `na` insufficient.
- **EU5 drill-down:** keep UK/DE/FR/IT/ES as independent pills in the trust bar (they're already there) — no separate sub-market row needed.
- **Sticky CSS:** `position: sticky; top: 0; z-index: 20; backdrop-filter: blur(4px)`.
- **Drop `curMetric` entirely.** KPI row locks to default per market via existing `defaultMetricForMarket()`. All three metrics shown as side-by-side cards (see M3).

### M2 — Headline + exception banner (with recommended action)
- **Replace:** current narrative prose in `renderCalloutNarrative()` with a deterministic one-sentence template:
  `"{market} drove {regs} regs ({wow}% WoW) on {spend_pct}% spend. {top_channel} led the lift ({top_pct}); {other_channel} {dir} ({other_pct}). Pacing {op2_pct}% vs OP2."`
- **Exception condition:** `predictions_history[market].latest.score === 'MISS'` OR `abs(error_pct) > 15` OR `in_ci_rate_6w < 0.5`.
- **Only renders when triggered.** On routine weeks the banner disappears entirely; the saved vertical goes to the chart above the fold.
- **Diagnosis field:** pulled from `callout.forecast_diagnosis` (new; added server-side in same commit — see deterministic classification tree in thread 2026-04-30_dashboard-mockups-handoff post 002).
- **Recommended action (per #008 + #010 in full report — T1, "the single biggest gap" vs projection engine):** banner also carries a one-line prescribed action with pre-composed draft. Template: `"If miss > 20% → Draft Brandon note"` with click-to-open draft pre-filled with week, metric, miss %, and the diagnosis sentence. Projection engine's "Trust this projection less this week → Switch to Pessimistic" is the existing pattern to mirror. Banner without a recommended action = a half-built banner.

### M3 — KPI cards with sparklines
- **File:** `renderKPIs()` around line 2420 of `weekly-review.html`.
- **4 cards:** Latest regs (+ sparkline), vs OP2 (+ bullet), CPA (+ sparkline), YTD regs (numeric only). No global metric filter.
- **New shared helper:** `renderSparkline(values, color, w=72, h=18)` returning SVG string; endpoint dot always filled. Used by M3, M6 (optional), M8.
- **CSS:** `font-variant-numeric: tabular-nums` on every big-number class site-wide (one line; kills misaligned digits across every table and tile).

### M4 — Bullet chart component
- **New shared helper:** `renderBullet({ actual, target, bands, width, label })` returning HTML+SVG string.
- **Default bands:** `[[0, 0.8, 'bad'], [0.8, 0.95, 'warn'], [0.95, 1.2, 'good']]` as fractions of target; override per context (CPA inverts).
- **Accessibility:** `role="meter"`, `aria-valuemin/max/now`, plain-English `aria-label`.
- **Consumers:** WR vs-OP2 KPI card (M3), MPE distance-to-target tab, any progress-vs-plan tile.

### M5 — Reliability diagram + signed-error bars
- **Replace:** `#scorecardRow` 4 cards with two SVG panels side by side + compact box-score footer row.
- **Left panel:** reliability diagram. X = predicted regs, Y = actual regs, dots = last 6 graded weeks, dashed diagonal = perfect calibration, translucent polygon = ±1σ CI band.
- **Right panel:** signed-error column chart. Zero line + CI band as translucent rect behind; bars fill from zero, saturated when outside CI.
- **Keep the 4 existing numbers** (first-err / latest-err / in-CI / skill vs naive) as a comma-separated footer strip under the two panels — the visuals are primary now, the numbers are confirmation.

### M6 — Small multiples
- **New section** after scorecard: 12 markets × (actual line + OP2 line) in a CSS Grid with `repeat(auto-fill, minmax(180px, 1fr))`.
- **Per panel:** 6-week window. Actual = accent; OP2 = muted. No axes, no legends per panel — title + YoY % is the only text.
- **Per panel Y scale: SHARED across all panels** — this corrects an error in the v1 mockup spec which said "independent Y per panel." Shared Y is what the full research report (#043) and richard-style-wbr.md both call for, and it's the whole point of small multiples: cross-market pattern recognition requires the eye to compare magnitudes, not just shapes. Tufte + Juice Analytics + Datawrapper all align on this. The exception: if the CPA variant ever ships (CPA ranges 10× across markets), that single metric can use log-scale or panel-independent Y as an explicit opt-in. For regs, spend, and YoY percent — shared Y, period.
- **Click behavior:** selecting a panel calls a shared `selectMarket(mk)` helper. Same code path as M1 trust-bar pill click.

### M7 — Amazon 6-12 chart
- **New render mode in `canon-chart.js`:** `mode: 'wbr612'`.
- **Layout:** two SVG panels side by side with ~20px gap. Left: 6 weeks weekly. Right: 12 months monthly. **Different Y axes per panel** (Commoncog: "same Y hides the real relationship between short and long-term").
- **Data:** left = `FORECAST.weekly[market].slice(-6)`; right = monthly rollup of `FORECAST.weekly[market]` for 12 months (new helper `monthlyRollup(weeklyArr)`).
- **Decorations:** prior-year ghost line (faded pink) on both panels; OP2 plan as dashed line; green triangles at target weeks; endpoint labels (no legend).
- **Box score footer:** fixed 5-cell strip — WoW %, YoY %, vs OP2 %, 4wk avg, 13wk avg. Same order every week.

### M8 — Prior-week thread as sparkline strip
- **Replace:** current text pager (`renderThreadStrip()`) with 6-7 cells, each a 64×24 SVG.
- **Per cell:** shows intra-week forecast drift or a flat line; red stroke = MISS, green = HIT. Label = week id, value = signed error %.
- **Pending week:** greyed, dashed line, label "pending".
- **Click:** scrub narrative + 3Q + variance to that week (same as WR-A10 chart scrub). KPIs, scorecard, small multiples stay on `curWeek`.

### M9 — Fan chart (MPE)
- **Replace:** text "90% range: $515K–$2.17M" string + the current single projection line.
- **Three fills:** 90% (outermost, lightest) → 80% → 50% (innermost, darkest) behind the central projection line.
- **Data:** extract `ci_50`, `ci_80`, `ci_90` from `v1_1_slim.js` scenario routines as arrays of `{x, lo, hi}`.
- **Historical actuals:** darker solid line on the left of a now-line dashed vertical.
- **Reference:** Bank of England fan charts (1996 convention) — canonical.

### M10 — Waterfall variance decomposition
- **Replace:** current `renderVariance()` driver/WoW/share table with a horizontal waterfall SVG.
- **Shape:** prior week bar (muted) → +/−channel floating bars → +/−residual floating bar → current week bar (accent). Dashed connectors between tops/bottoms.
- **Data:** already derived. Residual = `current_regs − prior_regs − Δbrand − Δnb`.
- **Keep tooltip:** "share of total Δ" on hover.
- **Rollup fallback:** preserve the WR-B1-2 aggregate-across-member-markets path for WW/EU5/NA.

## Open questions — all resolved by kiro-server on 2026-04-30

All three original open questions have answers from kiro-server on thread `2026-04-30_dashboard-mockups-handoff` post 002:

1. **`forecast_diagnosis` field (M2):** new field, added in `refresh-callouts.py` around line 814. Deterministic classification tree reading from `predictions_history[market][wk]` and `ps.regime_changes`. Ships in same commit as M2. Fallback `"Diagnosis unavailable"` when upstream data missing.
2. **Monthly rollup (M7):** already exists at `FORECAST.monthly[market]` in `forecast-data.json`. M7's right panel consumes it directly — no JS helper needed. `ly_monthly` (prior-year monthly ghost line) needs a ~10-line addition to `refresh-forecast.py`; kiro-server will ship in the M7 commit.
3. **CI widths (M9):** currently only 90% in `projection-data.json`. Kiro-server will emit 50/80/90 in a standalone commit before M9 so the JSON is ready when kiro-local pulls for the fan chart. Monte Carlo samples already computed; ~10 lines to expose percentiles.

## Verification probe for each commit

```bash
# 1. Start dashboard server from the right root
cd agent-bridge/dashboards/ && python3 serve.py

# 2. Open in a real browser:
open "http://localhost:8080/performance/weekly-review.html?market=US&week=W17"

# 3. Compare visually against mockups/screenshots/mN-*.png
# 4. Cycle through all 12 markets via the trust bar
# 5. Scroll 2000px down; confirm sticky header stays pinned
# 6. When M8 lands: keyboard J/K navigates weeks, / focuses market picker, ? opens shortcuts
```

## Why this exists

Richard asked for visual references kiro-server can implement against. Text specs alone under-specify; Figma-style mockups over-commit to pixel details that don't matter. This lives in the middle: static HTML/SVG that renders anywhere, real W17 US data so the density is production-accurate, each mockup anchored to a cited source in the research report.

---

Compiled by kiro-local, 2026-04-30. All numbers are real W17 US values. Companion: `../dashboard-redesign-report.html`.
