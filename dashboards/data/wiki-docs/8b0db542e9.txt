# AU W14 Data Brief

## Headline numbers
- Registrations: 170 (-18% WoW)
- Spend: $22K (-9% WoW)
- CPA: $130 (+11% WoW)
- Brand regs: 96 (-2% WoW)
- NB regs: 74 (-33% WoW)

## Registration drivers (what caused the WoW change?)
Primary driver: CVR (-15% WoW) more than clicks (-4% WoW)

Brand:
  Regs: 96 vs 98 LW (-2%)
  CVR: 6.80% vs 7.37% (-8%)
  Clicks: 1411 vs 1329 (+6%)
  CPA: $45 vs $41 (+9%)

Non-Brand:
  Regs: 74 vs 110 LW (-33%)
  CVR: 1.87% vs 2.60% (-28%)
  Clicks: 3951 vs 4228 (-7%)
  CPA: $240 vs $185 (+30%)

## 8-week trend
<!-- Data: market_trend("AU", weeks=8) -->

## Monthly projection inputs
- Month: 2026 Mar (31/31 days elapsed, 0 remaining)
- MTD actuals: $125K spend, 1032 regs (488 Brand, 544 NB)
- Simple linear projection (ingester estimate, not accounting for seasonality/holidays): $125K spend, 1.0K regs, $121 CPA
- NOTE: Analyst should produce the actual projection accounting for weekday/weekend mix, holidays, LY patterns, and known upcoming changes.

## Anomalies (>20% deviation from recent avg)
- regs: below avg by 33% (current: 170.00, avg: 255.00)
- cost: below avg by 33% (current: 22073.54, avg: 32996.30)
- cvr: below avg by 23% (current: 0.03, avg: 0.04)
- nb regs: below avg by 47% (current: 74.00, avg: 140.29)
- nb cvr: below avg by 37% (current: 0.02, avg: 0.03)
- cpc: below avg by 22% (current: 4.12, avg: 5.30)

## This year weekly trend (last 12 weeks)
<!-- Data: market_trend("AU", weeks=12) -->

## Detected streaks
- NB CPC declining 8 consecutive weeks ($6.82 in W6 to $4.50 in W14)

## Daily breakdown
<!-- Data: db("SELECT * FROM daily_metrics WHERE market='AU' AND week='2026 W14' ORDER BY date") -->
