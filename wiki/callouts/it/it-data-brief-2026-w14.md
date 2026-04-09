# IT W14 Data Brief

## Headline numbers
- Registrations: 1334 (-1% WoW)
- Spend: $95K (-2% WoW)
- CPA: $71 (-1% WoW)
- Brand regs: 879 (-5% WoW)
- NB regs: 455 (+8% WoW)

## ie%CCP
- This week: 61%
- Last week: 61%
- Target: 100%

## Registration drivers (what caused the WoW change?)
Primary driver: clicks (-8% WoW) more than CVR (+8% WoW)

Brand:
  Regs: 879 vs 924 LW (-5%)
  CVR: 3.01% vs 3.01% (flat)
  Clicks: 29182 vs 30676 (-5%)
  CPA: $31 vs $30 (+2%)

Non-Brand:
  Regs: 455 vs 423 LW (+8%)
  CVR: 2.08% vs 1.71% (+22%)
  Clicks: 21836 vs 24711 (-12%)
  CPA: $149 vs $163 (-9%)

## 8-week trend
<!-- Data: market_trend("IT", weeks=8) -->

## YoY comparison
- Regs: 1334 TY vs 1208 LY (+10%)
- Spend: $95K TY vs $55K LY (+73%)
- Brand regs: +5% YoY
- NB regs: +23% YoY
- NB CPA: $149 vs $76 LY (+97%)
- WoW pattern: TY -1% vs LY -9% (same week)

## Monthly projection inputs
- Month: 2026 Mar (31/31 days elapsed, 0 remaining)
- MTD actuals: $411K spend, 5675 regs (3973 Brand, 1702 NB)
- Simple linear projection (ingester estimate, not accounting for seasonality/holidays): $411K spend, 5.7K regs, $72 CPA
- NOTE: Analyst should produce the actual projection accounting for weekday/weekend mix, holidays, LY patterns, and known upcoming changes.

## Anomalies (>20% deviation from recent avg)
- nb regs: above avg by 21% (current: 455.00, avg: 375.57)

## This year weekly trend (last 12 weeks)
<!-- Data: market_trend("IT", weeks=12) -->

## Last year same period (W10 to W18)
<!-- Data: db("SELECT * FROM weekly_metrics WHERE market='IT' AND week LIKE '2025%' ORDER BY week") -->

## Daily breakdown
<!-- Data: db("SELECT * FROM daily_metrics WHERE market='IT' AND week='2026 W14' ORDER BY date") -->
