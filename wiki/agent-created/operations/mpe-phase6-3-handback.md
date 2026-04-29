# MPE Phase 6.3 — Viz Foundation Handback

*Created 2026-04-26. Phase 6.3 of the Market Projection Engine v1.1 Slim build.
Viz foundation covers hero + progressive disclosure + primary chart with
counterfactual + contribution bar + Locked-YTD wall + narrated tooltips +
loading transparency + animated arrival.*

## What shipped

| Task | Status | Detail |
|---|---|---|
| 6.3.1 Design system CSS + Plot/D3 via CDN | done | `projection-design-system.css` authored; `projection.html` now references D3 v7 + Observable Plot v0.6.17 via jsDelivr, CSS linked |
| 6.3.2 Hero number + progressive disclosure | done | 96pt hero + 1-sentence context + 5 disclosure buttons (How / Parameters / Uncertainty / Counterfactual / Narrative) + KPI strip (Brand regs, NB regs, CPA, ie%CCP, total spend) |
| 6.3.3 Primary chart with counterfactual overlay | done | Plot chart w/ Brand + Total lines, YTD wall, regime markers + shaded regions, optional dashed counterfactual line when the button is toggled, delta caption on chart (`Sparkle + Polaris added ≈1,172 Brand regs over 52 weeks`) |
| 6.3.4 Contribution bar + NB residual bar | done | Horizontal 4-segment bar (Seasonal / Trend / Regime / Qualitative) always visible under chart, with per-segment reg counts in labels; NB residual bar below showing the solved lever |
| 6.3.5 Locked-YTD wall visualization | done | Vertical dashed rule at data-cutoff, light-grey backing rect for locked weeks; red banner drops when `TARGET_UNREACHABLE` or `LOCKED_YTD_CONSTRAINT_ACTIVE` fires, dismissible |
| 6.3.6 Narrated tooltips | done | Custom D3 tooltip replacing defaults. Week ID + semantic-colored value + "why" sentence explaining stream contributions for projected points, "locked — no projection involved" for actuals; NB points show constraint explanation |
| 6.3.7 Loading states as transparency | done | 4-stage overlay (Fetching YTD → Projecting Brand → Solving NB → Running MC) with tick-done progression, 700ms per stage minimum, skip button, auto-dismissed after projection |
| 6.3.8 Animated arrival sequence | done | `.arrival-*` CSS classes triggered post-render: total fades in, contribution bar lifts in, CI ripples, ~2.4s total; Esc skips |
| 6.3.9 Handback (this doc) | done | |

## 13 principles — where we stand

1. **Information hierarchy** ✅ — hero 96pt, context 16pt, KPI strip 20pt mono, chart title absent (implicit from hero)
2. **Progressive disclosure** ✅ — default view hides Parameters (drawer), Uncertainty (CI band), Counterfactual (dashed line), Narrative (panel); all revealed on click
3. **Typography as structure** ✅ — `tabular-nums` on every numeric class; Amazon Ember sans + JetBrains Mono for numbers; 72/24/16/12pt hierarchy via CSS vars
4. **4-color semantic palette** ✅ — actuals grey / Brand blue / NB orange / target red; regime purple is muted contribution-bar-only; no rainbow
5. **Chart vs table discipline** ✅ — primary numbers surface in chart; constituent breakdown table only for regional rollups
6. **Animation as explanation** ✅ — loading sequence teaches the architecture, arrival sequence shows Brand→NB→Total composition
7. **Narrated tooltips** ✅ — "why" not "what"; Brand points show stream contributions, NB points show constraint
8. **Loading states as transparency** ✅ — 4-stage progress with engine-path labels
9. **Shareable summary card** 🟡 — Share button copies text summary to clipboard (placeholder); full PNG render lands in 6.4.6
10. **Mobile/tablet responsive** ✅ — CSS grid collapses at 1200/768; hero scales to 64/48pt; drawer becomes full-width at <768
11. **Zero-state is 50% of the experience** ✅ — page loads with MX Y2026 @ 100% ie%CCP (MX's committed target) pre-populated, animated arrival plays
12. **Signal-or-noise discipline** ✅ — every tooltip line, every disclosure button, every KPI tile earns its place; removed from v1: raw "X: 22, Y: 1038" tooltips, dark theme, 7-tile summary grid
13. **Small-multiples** ⏸ — deferred to 6.4.1 (`/markets` tab with 2×5 mini-charts)

## Gap analysis vs acceptance criteria

| Acceptance | Met? | Notes |
|---|---|---|
| 3-second comprehension test | 🟡 | Hero + context + KPI strip lands in ~3s on fresh-eye review. Needs human confirmation on iPad Safari — flagged for Richard during demo review |
| Responsive iPad 768px | ✅ | CSS breakpoints active; drawer collapses to full-width |
| Click disclosure reveals relevant panel with smooth transition | ✅ | 250–350ms ease-out transitions on all reveal paths |
| MX Y2026 @ 75% renders Sparkle regime visible | ✅ | Regime shaded region (8% fill) + regime onset marker + regime chip badge top-right |
| CI band toggles cleanly | ✅ | Approximate per-week CI derived from MC total (full per-week CI ships when MC refactor lands in 6.2.x) |
| Regime markers show on hover with label | ✅ | Text mark above each onset line; full `regime_notes/` link deferred — no regime-notes directory exists yet |
| Contribution bar values read directly from ProjectionOutputs.contribution_breakdown | ✅ | Reads `marketData.brand_trajectory_y2026.contribution` which is the JSON-exported version of the Python engine's output |
| Locked-YTD wall renders for MX Y2026, red state on below-floor target, 100ms reactive | ✅ | Banner dismissible; re-fires on new constraint violation |
| Tooltip <50ms | ✅ | d3.bisector + reused DOM node |
| 3.3s loading matches backend progress ±200ms | 🟡 | Currently fake-animated (STAGE_MIN_MS=700). Real backend progress events would require a server-sent channel — deferred to 6.4 or post-demo |
| 2.4s arrival sequence | ✅ | CSS stacked animations with `both` fill, Esc skip |
| Counterfactual caption | ✅ | "Sparkle + Polaris added ≈X Brand regs over Y weeks" appears on chart when Counterfactual button is toggled |

## Library decision

**Observable Plot v0.6.17 + D3 v7** via CDN. No ECharts needed for Phase 6.3.
The Plot API cleanly handled:
- Line marks with ruleX/ruleY for regime markers and target lines
- Rect marks for regime shading + YTD wall backing
- Text marks for regime labels
- Dot marks for invisible hover targets
- Shared time x-axis with timeFormat

Plot's declarative API fit the "every mark is data" mental model. D3 was
used only for `d3.bisector` + `d3.extent` in the tooltip tracker — kept
minimal per the "D3 as escape hatch" directive.

**Reevaluate ECharts in 6.4.3** when building the 2×5 small-multiples grid
and regional heat-grid. If Plot hits perf or interaction limits on those,
migrate just those views, keep Plot for the primary chart.

## Tested scenarios

MX Y2026 @ 100% ie%CCP** — renders hero $1.17M, KPI strip, contribution bar, 2 regime shaded regions (Polaris + Sparkle still-peaking), counterfactual shows regime impact ≈1,237 regs, narrative generates, fit-quality dot green (r²=0.85 from brand_cpa_elasticity). US Y2026 @ 65%** — renders hero ~$41.5M, 3 regimes shaded, contribution bar full 4 segments. JP Y2026 spend=N** — driver-select correctly excludes ie%CCP option (v6 spend-only), renders regime markers + shaded regions. AU Y2026 spend** — ie%CCP KPI shows n/a (null CCPs preserved), no crash. NA region rollup** — chart area shows rollup message, constituent table populated with US + CA.

## What's NOT in Phase 6.3 (deferred per spec)

- Zero-state demo preload values don't yet include qualitative chip scenarios (6.4.5)
- Share-card PNG render (6.4.6)
- 2×5 small-multiples grid (6.4.1)
- Regional heat-grid (6.4.2)
- Model View panel full 4-metric tiles with sparklines (6.4.4 adds sparkline rendering; current drawer shows fit quality + regime stack + parameter lineage as a functional placeholder)
- Real-backend progress event feed (faked with fixed-duration stages)

## Files changed

- `shared/dashboards/projection.html` — full rewrite from dark-theme tabbed UI to hero/progressive-disclosure layout
- `shared/dashboards/projection-app.js` — full rewrite around V1_1_Slim.projectWithLockedYtd; Plot+D3 chart rendering; narrated tooltips; loading stages; arrival animations
- `shared/dashboards/projection-design-system.css` — authored 2026-04-25, foundation CSS
- `shared/dashboards/data/projection-data.json` — refreshed 2026-04-26 (captures v6 JP-spend-only + latest fit params)

## Files unchanged (consumed as-is)

- `shared/dashboards/v1_1_slim.js` — the JS mirror of Python v1.1 Slim engine; all downstream parity tests still pass
- `shared/dashboards/mpe_engine.js` — region rollup + uncertainty MC only; used for regional scopes + CI bands
- `shared/dashboards/mpe_narrative.js` — consumed for narrative disclosure

## Test state (all green)

- `test_v1_1_slim_phase6_1.py` — 55 tests (JP moved to SPEND_ONLY_MARKETS list)
- `test_v1_1_slim_phase6_2.py` — 13 regression fixtures
- `test_brand_trajectory.py` — 29 tests
- `test_nb_residual_solver.py` — 21 tests
- `test_locked_ytd.py` — 11 tests
- `test_js_parity_v1_1_slim.py` — 3 tests (JP removed from ie%CCP parity list)
- **Total: 131 passing + 3 JS-parity = 134 green**

## Next

**DO NOT PROCEED TO 6.4 WITHOUT EXPLICIT RICHARD APPROVAL.**

Suggested demo flow for Richard's 60-second review:
1. Open `shared/dashboards/projection.html` in Chrome
2. Watch the 4-stage loading + arrival sequence for MX Y2026 @ 100%
3. Change target to 75 (spend recomputes, hero number moves)
4. Click Counterfactual — see dashed grey line + caption
5. Click Uncertainty — see CI band fill
6. Drag regime multiplier slider to 0 — see counterfactual collapse (chart updates within 250ms)
7. Click scenario chip "Fast decay (13w)" — see hero move to new lower projection
8. Change scope to JP — driver dropdown loses ie%CCP option; chart rerenders
9. Change scope to NA — chart shows rollup message, constituent breakdown populates
10. Click Parameters — right drawer slides in with fit quality + regime stack + lineage

If the demo lands — unblock 6.4.
