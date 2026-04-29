# UK W17 Data Brief

## Headline numbers
- Registrations: 1623 (+1% WoW)
- Spend: $120K (-4% WoW)
- CPA: $74 (-5% WoW)
- Brand regs: 522 (+9% WoW)
- NB regs: 1101 (-2% WoW)

## ie%CCP
- This week: 61%
- Last week: 66%
- Target: 100%

## Registration drivers (what caused the WoW change?)
Primary driver: CVR (+5% WoW) more than clicks (-3% WoW)

Brand:
  Regs: 522 vs 478 LW (+9%)
  CVR: 3.10% vs 2.91% (+6%)
  Clicks: 16858 vs 16417 (+3%)
  CPA: $81 vs $82 (-1%)

Non-Brand:
  Regs: 1101 vs 1126 LW (-2%)
  CVR: 4.87% vs 4.60% (+6%)
  Clicks: 22616 vs 24466 (-8%)
  CPA: $70 vs $75 (-7%)

## 8-week trend
<!-- Data: market_trend("UK", weeks=8) -->

## YoY comparison
- Regs: 1623 TY vs 596 LY (+172%)
- Spend: $120K TY vs $43K LY (+180%)
- Brand regs: +48% YoY
- NB regs: +351% YoY
- NB CPA: $70 vs $80 LY (-12%)
- WoW pattern: TY +1% vs LY +5% (same week)

## Monthly projection inputs
- Month: 2026 Apr (25/30 days elapsed, 5 remaining)
- MTD actuals: $381K spend, 5438 regs (1714 Brand, 3724 NB)
- OP2 targets: $401K spend, 4.5K regs
- OP2 pace check: at 83% through the month, linear OP2 pace would be 3.7K regs and $334K spend
- MTD vs OP2 pace: +45% regs, +14% spend
- Simple linear projection (ingester estimate, not accounting for seasonality/holidays): $467K spend, 6.6K regs, $71 CPA
- NOTE: Analyst should produce the actual projection accounting for weekday/weekend mix, holidays, LY patterns, and known upcoming changes.

## Anomalies (>20% deviation from recent avg)
- cost: above avg by 27% (current: 119605.25, avg: 94127.87)

## This year weekly trend (last 12 weeks)
<!-- Data: market_trend("UK", weeks=12) -->

## Last year same period (W13 to W21)
<!-- Data: db("SELECT * FROM weekly_metrics WHERE market='UK' AND week LIKE '2025%' ORDER BY week") -->

## Daily breakdown
<!-- Data: db("SELECT * FROM daily_metrics WHERE market='UK' AND week='2026 W17' ORDER BY date") -->
