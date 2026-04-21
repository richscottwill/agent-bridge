# US W16 Data Brief

## Headline numbers
- Registrations: 9109 (-3% WoW)
- Spend: $679K (flat WoW)
- CPA: $75 (+3% WoW)
- Brand regs: 3041 (+16% WoW)
- NB regs: 6068 (-10% WoW)

## ie%CCP
- This week: 43%
- Last week: 47%
- Target: 100%

## Registration drivers (what caused the WoW change?)
Primary driver: CVR (-2% WoW) more than clicks (-1% WoW)

Brand:
  Regs: 3041 vs 2631 LW (+16%)
  CVR: 4.64% vs 4.10% (+13%)
  Clicks: 65597 vs 64107 (+2%)
  CPA: $61 vs $69 (-11%)

Non-Brand:
  Regs: 6068 vs 6755 LW (-10%)
  CVR: 5.89% vs 6.38% (-8%)
  Clicks: 102964 vs 105900 (-3%)
  CPA: $81 vs $74 (+10%)

## 8-week trend
<!-- Data: market_trend("US", weeks=8) -->

## YoY comparison
- Regs: 9109 TY vs 4735 LY (+92%)
- Spend: $679K TY vs $530K LY (+28%)
- Brand regs: +41% YoY
- NB regs: +135% YoY
- NB CPA: $81 vs $143 LY (-43%)
- WoW pattern: TY -3% vs LY -5% (same week)

## Monthly projection inputs
- Month: 2026 Apr (18/30 days elapsed, 12 remaining)
- MTD actuals: $1.7M spend, 23867 regs (7162 Brand, 16705 NB)
- OP2 targets: $2.8M spend, 31.1K regs
- OP2 pace check: at 60% through the month, linear OP2 pace would be 18.6K regs and $1.7M spend
- MTD vs OP2 pace: +28% regs, +2% spend
- Simple linear projection (ingester estimate, not accounting for seasonality/holidays): $2.9M spend, 39.5K regs, $73 CPA
- NOTE: Analyst should produce the actual projection accounting for weekday/weekend mix, holidays, LY patterns, and known upcoming changes.

## Anomalies (>20% deviation from recent avg)
- brand regs: above avg by 20% (current: 3041.00, avg: 2532.57)

## This year weekly trend (last 12 weeks)
<!-- Data: market_trend("US", weeks=12) -->

## Last year same period (W12 to W20)
<!-- Data: db("SELECT * FROM weekly_metrics WHERE market='US' AND week LIKE '2025%' ORDER BY week") -->

## Detected streaks
- NB CPC rising 3 consecutive weeks ($4.12 in W13 to $4.80 in W16)
- CPA rising 3 consecutive weeks ($68 in W13 to $75 in W16)

## Daily breakdown
<!-- Data: db("SELECT * FROM daily_metrics WHERE market='US' AND week='2026 W16' ORDER BY date") -->
