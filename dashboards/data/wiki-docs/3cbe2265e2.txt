# MPE Viz — Library Choice

*Authored 2026-04-26 after Phase 6.3 + 6.4.1/6.4.2 ship. Decision: stay on
Observable Plot + D3. ECharts not adopted.*

## What we shipped on

- **Observable Plot** 0.6.17 via jsDelivr CDN
- **D3** 7.9.0 via jsDelivr CDN (primarily `d3.bisector` + `d3.extent` + `d3.timeFormat`)
- Single-file standalone HTML, no build step, Kiro-dashboard-embeddable

## Surfaces covered

| Surface | Plot marks used | Verdict |
|---|---|---|
| Primary projection chart (6.3.3) | `line`, `ruleX`, `ruleY`, `rect`, `dot`, `text`, `areaY` | clean fit; dashed spend overlay works as sibling `line` mark with `strokeDasharray` |
| Small-multiples 2×5 (6.4.1) | 10 × `{line + ruleX}` mini-charts | renders all 10 in <400ms; no perf issue |
| Heat-grid (6.4.2) | pure CSS grid — no Plot needed | trivially fast; color semantics in CSS classes |
| Sparklines in drawer (6.4.4) | hand-rolled SVG `<polyline>` | 60-char function, no library overhead |

## Where Plot fell short and we routed around it

1. **Dual y-axes** — Plot doesn't natively support independent left/right scales.
   Worked around by scaling the spend series to fit the regs y-domain and
   noting the scaling factor in the legend + tooltip showing raw $.
2. **Custom tooltips** — Plot's built-in `tip` mark is good but verbose; for
   the narrated-tooltip UX we route mouse events through a D3 bisector on an
   SVG overlay. Clean enough.
3. **Performance on 10-mini-charts grid** — fine at 240×80px. Would re-evaluate
   if we scale to 50+ charts.

## Why not ECharts

- Adding a third library (Plot + D3 + ECharts) violates subtraction principle
- ECharts' biggest wins (small-multiples `grid` component, heat-calendar) are
  solved adequately with Plot + CSS-grid at our current scale
- Plot's declarative API lines up well with the "every mark is data" mental
  model we want the engine to project through
- Standalone-embed constraint: ECharts CDN bundle is 900KB vs Plot's 210KB

## When to reconsider

- Small-multiples scales to 30+ per view (regional breakdowns at market-segment level)
- Need calendar heatmap / treemap / sankey primitives
- Plot+D3 tooltip interactions become a maintenance burden

## Files

- `shared/dashboards/projection.html` — CDN script tags
- `shared/dashboards/projection-app.js` — all Plot + D3 usage
- `shared/dashboards/projection-design-system.css` — CSS-grid for heat-grid
