# DE W13 Data Brief

## Headline numbers
- Registrations: 654 (-46% WoW)
- Spend: $110K (-21% WoW)
- CPA: $168 (+45% WoW)
- Brand regs: 362 (-47% WoW)
- NB regs: 292 (-44% WoW)

## ie%CCP
- This week: 16759%
- Last week: 11528%
- Target: 100%

## Registration drivers (what caused the WoW change?)
Primary driver: CVR (-38% WoW) more than clicks (-12% WoW)

Brand:
  Regs: 362 vs 683 LW (-47%)
  CVR: 1.35% vs 2.48% (-46%)
  Clicks: 26902 vs 27500 (-2%)
  CPA: $129 vs $82 (+56%)

Non-Brand:
  Regs: 292 vs 517 LW (-44%)
  CVR: 1.74% vs 2.36% (-26%)
  Clicks: 16774 vs 21928 (-24%)
  CPA: $216 vs $159 (+36%)

## 8-week trend
<!-- Data: market_trend("DE", weeks=8) -->

## YoY comparison
- Regs: 654 TY vs 1306 LY (-50%)
- Spend: $110K TY vs $104K LY (+5%)
- Brand regs: -49% YoY
- NB regs: -51% YoY
- NB CPA: $216 vs $104 LY (+107%)
- WoW pattern: TY -46% vs LY -4% (same week)

## Monthly projection inputs
- Month: 2026 Mar (28/31 days elapsed, 3 remaining)
- MTD actuals: $576K spend, 4757 regs (2792 Brand, 1965 NB)
- Simple linear projection (ingester estimate, not accounting for seasonality/holidays): $623K spend, 5.0K regs, $124 CPA
- NOTE: Analyst should produce the actual projection accounting for weekday/weekend mix, holidays, LY patterns, and known upcoming changes.

## Anomalies (>20% deviation from recent avg)
- regs: below avg by 54% (current: 654.00, avg: 1410.71)
- cost: below avg by 32% (current: 109602.18, avg: 162122.99)
- cpa: above avg by 45% (current: 167.59, avg: 115.22)
- cvr: below avg by 45% (current: 0.01, avg: 0.03)
- brand regs: below avg by 57% (current: 362.00, avg: 836.14)
- nb regs: below avg by 49% (current: 292.00, avg: 574.57)
- brand cvr: below avg by 54% (current: 0.01, avg: 0.03)
- nb cvr: below avg by 30% (current: 0.02, avg: 0.02)
- cpc: below avg by 20% (current: 2.51, avg: 3.14)

## This year weekly trend (last 12 weeks)
<!-- Data: market_trend("DE", weeks=12) -->

## Last year same period (W9 to W17)
<!-- Data: db("SELECT * FROM weekly_metrics WHERE market='DE' AND week LIKE '2025%' ORDER BY week") -->

## Detected streaks
- CPA rising 3 consecutive weeks ($112 in W10 to $168 in W13)

## Daily breakdown
<!-- Data: db("SELECT * FROM daily_metrics WHERE market='DE' AND week='2026 W13' ORDER BY date") -->
