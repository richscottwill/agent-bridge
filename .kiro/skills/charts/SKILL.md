---
name: charts
description: "Generate data visualization dashboards. Reads body organs and market data, produces standalone HTML. Triggers on chart, dashboard, visualize, show dashboard, generate charts."
---

# Charts (Data Visualization)

## Instructions

1. **Determine data source** — Identify which body organs or data files contain the metrics to visualize. Common sources: eyes.md (market data), brain.md (strategic metrics), DuckDB (ps-analytics.duckdb).
2. **Select chart type** — Based on the data and request, choose appropriate visualization: line charts for trends, bar charts for comparisons, tables for detailed breakdowns.
3. **Generate dashboard** — Run `scripts/generate.sh` to produce a standalone HTML dashboard file. Pass the data source and chart configuration as arguments.
4. **Review output** — Verify the generated HTML renders correctly and contains accurate data.
5. **Save artifact** — Save the dashboard to ~/shared/artifacts/reporting/ with a descriptive filename including the date.

## Notes

- The generate script wraps the Python chart generation tool at ~/shared/tools/progress-charts/generate.py.
- Dashboards should be standalone HTML (no external dependencies) for portability.
