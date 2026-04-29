# MX W17 Data Brief

## Headline numbers
- Registrations: 551 (+8% WoW)
- Spend: $26K (-6% WoW)
- CPA: $46 (-13% WoW)
- Brand regs: 416 (+6% WoW)
- NB regs: 135 (+17% WoW)

## ie%CCP
- This week: 58%
- Last week: 66%
- Target: 100%

## Registration drivers (what caused the WoW change?)
Primary driver: CVR (+11% WoW) more than clicks (-3% WoW)

Brand:
  Regs: 416 vs 394 LW (+6%)
  CVR: 8.61% vs 7.86% (+9%)
  Clicks: 4834 vs 5011 (-4%)
  CPA: $14 vs $16 (-13%)

Non-Brand:
  Regs: 135 vs 115 LW (+17%)
  CVR: 1.36% vs 1.13% (+20%)
  Clicks: 9954 vs 10195 (-2%)
  CPA: $147 vs $183 (-20%)

## 8-week trend
<!-- Data: market_trend("MX", weeks=8) -->

## YoY comparison
- Regs: 551 TY vs 192 LY (+187%)
- Spend: $26K TY vs $30K LY (-16%)
- Brand regs: +357% YoY
- NB regs: +34% YoY
- NB CPA: $147 vs $275 LY (-46%)
- WoW pattern: TY +8% vs LY +12% (same week)

## Monthly projection inputs
- Month: 2026 Apr (25/30 days elapsed, 5 remaining)
- MTD actuals: $88K spend, 1751 regs (1292 Brand, 459 NB)
- OP2 targets: $35K spend, 791.2857142857142 regs
- OP2 pace check: at 83% through the month, linear OP2 pace would be 659 regs and $29K spend
- MTD vs OP2 pace: +166% regs, +202% spend
- Simple linear projection (ingester estimate, not accounting for seasonality/holidays): $107K spend, 2.1K regs, $50 CPA
- NOTE: Analyst should produce the actual projection accounting for weekday/weekend mix, holidays, LY patterns, and known upcoming changes.

## Anomalies (>20% deviation from recent avg)
- regs: above avg by 44% (current: 551.00, avg: 381.71)
- cpa: below avg by 24% (current: 46.36, avg: 60.61)
- cvr: above avg by 33% (current: 0.04, avg: 0.03)
- brand regs: above avg by 63% (current: 416.00, avg: 255.29)
- brand cvr: above avg by 34% (current: 0.09, avg: 0.06)

## This year weekly trend (last 12 weeks)
<!-- Data: market_trend("MX", weeks=12) -->

## Last year same period (W13 to W21)
<!-- Data: db("SELECT * FROM weekly_metrics WHERE market='MX' AND week LIKE '2025%' ORDER BY week") -->

## Detected streaks
- Regs rising 3 consecutive weeks (302 in W14 to 551 in W17)

## Daily breakdown
<!-- Data: db("SELECT * FROM daily_metrics WHERE market='MX' AND week='2026 W17' ORDER BY date") -->
