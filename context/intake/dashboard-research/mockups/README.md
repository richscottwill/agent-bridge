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

| # | Mockup | File(s) | Effort |
|---|---|---|---|
| 1 | M1 · sticky header + trust bar | `performance/weekly-review.html` | 2h |
| 2 | M2 · headline + exception banner | `performance/weekly-review.html` | 1.5h |
| 3 | M3 · KPI cards with sparklines | `performance/weekly-review.html` + new `renderSparkline` / `renderBullet` helpers | 2h |
| 4 | M4 · bullet chart component | shared helper, consumers: WR KPI row (M3), MPE distance-to-target | 0h (ships with M3) |
| 5 | M5 · reliability diagram + signed bars | `performance/weekly-review.html` + `canon-chart.js` | 2.5h |
| 6 | M6 · small multiples | `performance/weekly-review.html` (new section) | 2h |
| 7 | M7 · 6-12 chart | `canon-chart.js` (new `mode: 'wbr612'`) | 3h |
| 8 | M8 · prior-week sparkline thread | `performance/weekly-review.html` — `renderThreadStrip()` | 1h |
| 9 | M9 · fan chart | `projection.html` | 2h |
| 10 | M10 · waterfall variance | `performance/weekly-review.html` — `renderVariance()` | 1.5h |

**Total: ~18h across 10 commits.**

## Implementation spec summary per mockup

### M1 — Sticky header + trust bar (absorbs filters)
- **Replace:** `.wr-leaderboard` + `.wr-controls` + `#regionTabs` + `#submarketTabs` + `#metricTabs` + `#weekSelect` → single `<header class="wr-stick">` with title / trust-bar / week-nav.
- **Data:** trust pills use existing `renderAccuracyLeaderboard()` derivation; class mapping `on` ≥5/6 · `mid` 3-4/6 · `off` ≤2/6 · `na` insufficient.
- **EU5 drill-down:** keep UK/DE/FR/IT/ES as independent pills in the trust bar (they're already there) — no separate sub-market row needed.
- **Sticky CSS:** `position: sticky; top: 0; z-index: 20; backdrop-filter: blur(4px)`.
- **Drop `curMetric` entirely.** KPI row locks to default per market via existing `defaultMetricForMarket()`. All three metrics shown as side-by-side cards (see M3).

### M2 — Headline + exception banner
- **Replace:** current narrative prose in `renderCalloutNarrative()` with a deterministic one-sentence template:
  `"{market} drove {regs} regs ({wow}% WoW) on {spend_pct}% spend. {top_channel} led the lift ({top_pct}); {other_channel} {dir} ({other_pct}). Pacing {op2_pct}% vs OP2."`
- **Exception condition:** `predictions_history[market].latest.score === 'MISS'` OR `abs(error_pct) > 15` OR `in_ci_rate_6w < 0.5`.
- **Only renders when triggered.** On routine weeks the banner disappears entirely; the saved vertical goes to the chart above the fold.
- **Diagnosis field:** pulled from `callout.forecast_diagnosis`. May need a callout pipeline stub (one string per market-week). Default to generic "Baseline gap, not regime-related" if absent.

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
- **Per panel Y scale:** independent — compute extent from both series per-market so the two lines fit each panel. (Cross-market comparison happens through pattern matching, not absolute Y alignment.)
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

## Open questions / things I couldn't answer from local

1. **`forecast_diagnosis` pipeline field (M2)** — does the callout pipeline already emit a diagnosis string per market-week, or do we need to add one? If adding, where's the right place in `refresh-callouts.py`?
2. **Monthly rollup helper (M7)** — does a weekly→monthly aggregation function already exist server-side in the forecast writer? If yes, we should reuse; if no, this is a small addition to `export-projection-data.py` or the dashboard-side helper.
3. **`ci_50` / `ci_80` / `ci_90` exposure (M9)** — does `projection-data.json` already carry the multiple CI widths, or just the 90%? If only 90%, we need the scenario routines to emit all three.

If you've got answers on any of these, drop them on the bus thread this post triggers.

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
