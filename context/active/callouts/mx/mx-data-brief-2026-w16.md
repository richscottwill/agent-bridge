# MX W16 Data Brief

## Headline numbers
- Registrations: 510 (flat WoW)
- Spend: $27K (+7% WoW)
- CPA: $53 (+7% WoW)
- Brand regs: 395 (+8% WoW)
- NB regs: 115 (-19% WoW)

## ie%CCP
- This week: 70%
- Last week: 68%
- Target: 100%

## Registration drivers (what caused the WoW change?)
Primary driver: CVR (+1% WoW) more than clicks (-1% WoW)

Brand:
  Regs: 395 vs 367 LW (+8%)
  CVR: 7.88% vs 7.95% (-1%)
  Clicks: 5011 vs 4614 (+9%)
  CPA: $16 vs $14 (+8%)

Non-Brand:
  Regs: 115 vs 142 LW (-19%)
  CVR: 1.13% vs 1.32% (-15%)
  Clicks: 10195 vs 10752 (-5%)
  CPA: $183 vs $142 (+29%)

## 8-week trend
<!-- Data: market_trend("MX", weeks=8) -->

## YoY comparison
- Regs: 510 TY vs 172 LY (+197%)
- Spend: $27K TY vs $28K LY (-4%)
- Brand regs: +456% YoY
- NB regs: +14% YoY
- NB CPA: $183 vs $263 LY (-30%)
- WoW pattern: TY flat vs LY +12% (same week)

## Monthly projection inputs
- Month: 2026 Apr (18/30 days elapsed, 12 remaining)
- MTD actuals: $63K spend, 1205 regs (881 Brand, 324 NB)
- OP2 targets: $35K spend, 791.2857142857142 regs
- OP2 pace check: at 60% through the month, linear OP2 pace would be 474 regs and $21K spend
- MTD vs OP2 pace: +154% regs, +198% spend
- Simple linear projection (ingester estimate, not accounting for seasonality/holidays): $109K spend, 2.1K regs, $53 CPA
- NOTE: Analyst should produce the actual projection accounting for weekday/weekend mix, holidays, LY patterns, and known upcoming changes.

## Anomalies (>20% deviation from recent avg)
- regs: above avg by 47% (current: 510.00, avg: 347.57)
- cost: above avg by 26% (current: 27216.75, avg: 21559.75)
- cvr: above avg by 26% (current: 0.03, avg: 0.03)
- brand regs: above avg by 77% (current: 395.00, avg: 223.71)
- brand cvr: above avg by 30% (current: 0.08, avg: 0.06)

## This year weekly trend (last 12 weeks)
<!-- Data: market_trend("MX", weeks=12) -->

## Last year same period (W12 to W20)
<!-- Data: db("SELECT * FROM weekly_metrics WHERE market='MX' AND week LIKE '2025%' ORDER BY week") -->

## Daily breakdown
<!-- Data: db("SELECT * FROM daily_metrics WHERE market='MX' AND week='2026 W16' ORDER BY date") -->
