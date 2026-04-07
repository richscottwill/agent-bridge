<!-- DOC-0058 | duck_id: callout-it-data-brief-2026-w12 -->
# IT W12 Data Brief

## Headline numbers
- Registrations: 1273 (-12% WoW)
- Spend: $78K (-17% WoW)
- CPA: $61 (-6% WoW)
- Brand regs: 924 (-10% WoW)
- NB regs: 349 (-16% WoW)

## ie%CCP
- This week: 51%
- Last week: 54%
- Target: 100%

## Registration drivers (what caused the WoW change?)
Primary driver: CVR (-8% WoW) more than clicks (-4% WoW)

Brand:
  Regs: 924 vs 1028 LW (-10%)
  CVR: 2.86% vs 3.08% (-7%)
  Clicks: 32307 vs 33342 (-3%)
  CPA: $33 vs $37 (-12%)

Non-Brand:
  Regs: 349 vs 415 LW (-16%)
  CVR: 1.74% vs 1.96% (-11%)
  Clicks: 20025 vs 21124 (-5%)
  CPA: $136 vs $133 (+2%)

## 8-week trend
<!-- Data: market_trend("IT", weeks=8) -->

## YoY comparison
- Regs: 1273 TY vs 1225 LY (+4%)
- Spend: $78K TY vs $60K LY (+30%)
- Brand regs: +13% YoY
- NB regs: -14% YoY
- NB CPA: $136 vs $70 LY (+93%)
- WoW pattern: TY -12% vs LY -9% (same week)

## Monthly projection inputs
- Month: 2026 Mar (21/31 days elapsed, 10 remaining)
- MTD actuals: $270K spend, 3873 regs (2757 Brand, 1116 NB)
- OP2 targets: $384K spend, 5.6K regs
- OP2 pace check: at 68% through the month, linear OP2 pace would be 3.8K regs and $260K spend
- MTD vs OP2 pace: +3% regs, +4% spend
- Simple linear projection (ingester estimate, not accounting for seasonality/holidays): $381K spend, 5.7K regs, $67 CPA
- NOTE: Analyst should produce the actual projection accounting for weekday/weekend mix, holidays, LY patterns, and known upcoming changes.

## This year weekly trend (last 12 weeks)
<!-- Data: market_trend("IT", weeks=12) -->

## Last year same period (W8 to W16)
<!-- Data: db("SELECT * FROM weekly_metrics WHERE market='IT' AND week LIKE '2025%' ORDER BY week") -->

## Daily breakdown
<!-- Data: db("SELECT * FROM daily_metrics WHERE market='IT' AND week='2026 W12' ORDER BY date") -->
