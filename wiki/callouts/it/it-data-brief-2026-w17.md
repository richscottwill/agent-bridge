# IT W17 Data Brief

## Headline numbers
- Registrations: 1178 (+5% WoW)
- Spend: $81K (-17% WoW)
- CPA: $69 (-21% WoW)
- Brand regs: 817 (+8% WoW)
- NB regs: 361 (-1% WoW)

## ie%CCP
- This week: 52%
- Last week: 66%
- Target: 100%

## Registration drivers (what caused the WoW change?)
Primary driver: CVR (+15% WoW) more than clicks (-9% WoW)

Brand:
  Regs: 817 vs 754 LW (+8%)
  CVR: 3.06% vs 2.59% (+18%)
  Clicks: 26660 vs 29097 (-8%)
  CPA: $40 vs $57 (-29%)

Non-Brand:
  Regs: 361 vs 365 LW (-1%)
  CVR: 2.16% vs 1.99% (+9%)
  Clicks: 16699 vs 18342 (-9%)
  CPA: $135 vs $152 (-11%)

## 8-week trend
<!-- Data: market_trend("IT", weeks=8) -->

## YoY comparison
- Regs: 1178 TY vs 808 LY (+46%)
- Spend: $81K TY vs $62K LY (+32%)
- Brand regs: +62% YoY
- NB regs: +19% YoY
- NB CPA: $135 vs $124 LY (+9%)
- WoW pattern: TY +5% vs LY -24% (same week)

## Monthly projection inputs
- Month: 2026 Apr (25/30 days elapsed, 5 remaining)
- MTD actuals: $330K spend, 4086 regs (2778 Brand, 1308 NB)
- OP2 targets: $351K spend, 5.0K regs
- OP2 pace check: at 83% through the month, linear OP2 pace would be 4.2K regs and $293K spend
- MTD vs OP2 pace: -3% regs, +13% spend
- Simple linear projection (ingester estimate, not accounting for seasonality/holidays): $389K spend, 4.9K regs, $79 CPA
- NOTE: Analyst should produce the actual projection accounting for weekday/weekend mix, holidays, LY patterns, and known upcoming changes.

## Anomalies (>20% deviation from recent avg)
- nb cvr: above avg by 20% (current: 0.02, avg: 0.02)

## This year weekly trend (last 12 weeks)
<!-- Data: market_trend("IT", weeks=12) -->

## Last year same period (W13 to W21)
<!-- Data: db("SELECT * FROM weekly_metrics WHERE market='IT' AND week LIKE '2025%' ORDER BY week") -->

## Daily breakdown
<!-- Data: db("SELECT * FROM daily_metrics WHERE market='IT' AND week='2026 W17' ORDER BY date") -->
