# MPE Phase 6.4 — Viz Completion Handback

*2026-04-26. Phase 6.4 closes "works for all 10 markets made visible" plus
the Model View, scenario chip animated transitions, share PNG, and mobile
responsiveness.*

## What shipped

| Task | Status | Detail |
|---|---|---|
| 6.4.1 Small-multiples 2×5 grid | done | New "All 10 markets" view. Mini chart per market with YTD-actual/projection lines + headline (spend · regs) + ie%CCP/CPA meta. Click any card to drill in. All 10 render in <500ms. |
| 6.4.2 Regional heat-grid | done | "Distance to target" view. 2×5 grid colored by `abs(projected_ieccp − target)`: green ±5pp, yellow ±5–15pp, red >±15pp. Spend-only markets (AU/JP) colored by spend-vs-OP2. Regional NA/EU5/WW rollup strip below the grid. Click cell → drill in. |
| 6.4.3 ECharts eval + decision | done | Stayed on Plot + D3. Documented at `mpe-viz-library-choice.md`. No third library added. |
| 6.4.4 Model View sparklines | done | 4-tile block at top of right drawer: Brand trend slope, active campaign lifts, NB CPA elasticity, Locked YTD. Each tile has freshness badge (fresh/stale/ancient based on `last_refit_at`) + "Explain this" link opening a plain-English modal. |
| 6.4.5 Scenario chip animated transitions | done | Hover preview via `title` tooltips; chip click triggers hero-number flash (green down / red up relative to prev) + `chip-pop` animation. |
| 6.4.6 Shareable PNG summary card | done | Native `canvas.toBlob` render — no html2canvas dep. Produces 1200×630 PNG with hero spend + regs, context line, KPI row, scenario label, timestamp. Auto-downloads + copies to clipboard (if browser allows). |
| 6.4.7 Responsive breakpoints | done | Desktop ≥1200px / tablet 768–1199px (small-multiples goes 5×2) / mobile <768px (1-col, drawer full-width, 44px touch targets). |
| 6.4.8 Handback (this doc) | done | |

## 13 principles — revalidated after 6.4

All 13 principles still hold. Where 6.4 extended:
- **#2 Progressive disclosure** — deepened via Model View sparklines + "Explain this" modals
- **#9 Shareable summary card** — native canvas render, no dep
- **#10 Mobile/tablet responsive** — 2 breakpoints, 44px touch targets
- **#13 Small-multiples** — operational at 2×5 + distance-to-target heat-grid

## Test state

- **131/131 Python tests green** (Phase 6.1 + 6.2 + brand_trajectory + nb_residual + locked_ytd)
- **3/3 JS parity tests green** (annual scope; period-scoped outputs are new and not parity-tested against Python yet)
- JS sanity: all new IDs present, all functions wired, all 3 views render

## Data layer changes this phase

- `_fetch_ytd_weekly` now exports `brand_cost` + `nb_cost` (was $0; broke AU projections)
- `_fetch_op2_targets` now exposes monthly breakdown in addition to annual sum
- `V1_1_Slim.projectWithLockedYtd` accepts `periodWeeks: Set<int>` filter — scopes totals to selected period (W/M/Q/Y/MY all produce distinct outputs)
- `V1_1_Slim` output adds `year_weekly` (per-week arrays) + `annual_*` totals alongside period-scoped totals

## Known acceptable gaps for demo

- **MX Brand projection still ~300 regs/wk vs actual Brand ~380** — anchor 8-week window dilutes recent Sparkle signal. Chart seam smoothing visually masks this; underlying engine needs post-onset-only anchor OR higher regime weight in a later pass. Non-blocking for demo.
- **Narrated tooltips don't yet show per-market historical comparisons** — deferred to Phase 6.5 with qualitative priors.
- **Share card clipboard copy** only works on browsers with `ClipboardItem` support (Chrome, Edge, Safari ≥13.1). Download always works.

## 3-minute demo flow (run order)

1. Page loads → MX Y2026 @ 100% ie%CCP with animated arrival
2. Click **All 10 markets** view → spot-check every market side-by-side
3. Click **Distance to target** → see which markets are red/yellow/green vs OP2
4. Click any red/yellow cell → drilled into that market
5. Try period selector: Y2026 → Q2 → M04 → W17; numbers + chart highlight update
6. Try scenario chips: Mixed → Bayesian (hero flashes red/up) → Frequentist (flashes green/down) → No lift (big flash)
7. Open **Parameters** drawer → Model View sparklines visible; click "Explain this" on a tile
8. Switch to a region (NA / EU5 / WW) → rollup chart renders with constituent table
9. Click **Share** → PNG downloads, pasted into Slack thread

## Files changed this phase

- `shared/dashboards/projection.html` — view switcher, 3 view containers, drawer sparkline section
- `shared/dashboards/projection-app.js` — renderSmallMultiples, renderHeatGrid, renderSparkline, renderDrawerSparklines, animateHeroTransition, switchView, full canvas share card render
- `shared/dashboards/projection-design-system.css` — small-multiples grid, heat-cell classes, sparkline styles, flash animations, enhanced responsive breakpoints
- `shared/dashboards/export-projection-data.py` — brand_cost/nb_cost in YTD, op2 monthly breakdown
- `shared/dashboards/v1_1_slim.js` — periodWeeks filter, year_weekly arrays, annual_* totals
- `shared/dashboards/data/projection-data.json` — regenerated with new fields

## Next

**Richard review** before Phase 6.5. 6.5 scope is the qualitative priors YAML + 10-market validation + callout/WBR pipeline migration — post-demo work.

**Demo date: 2026-05-16.** 20 days out. Phase 6.3 + 6.4 UI surfaces are complete. Remaining demo-blockers (if any) need to come from Richard's hands-on review of the full flow above.
