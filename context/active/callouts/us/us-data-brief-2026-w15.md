# US W15 Data Brief

## Headline numbers
- Registrations: 9236 (+22% WoW)
- Spend: $678K (+2% WoW)
- CPA: $73 (-17% WoW)
- Brand regs: 2696 (+29% WoW)
- NB regs: 6540 (+20% WoW)

## ie%CCP
- This week: 46%
- Last week: 58%
- Target: 100%

## Registration drivers (what caused the WoW change?)
Primary driver: CVR (+24% WoW) more than clicks (-1% WoW)

Brand:
  Regs: 2696 vs 2091 LW (+29%)
  CVR: 4.21% vs 3.35% (+25%)
  Clicks: 64107 vs 62371 (+3%)
  CPA: $67 vs $80 (-16%)

Non-Brand:
  Regs: 6540 vs 5468 LW (+20%)
  CVR: 6.18% vs 4.99% (+24%)
  Clicks: 105900 vs 109472 (-3%)
  CPA: $76 vs $92 (-17%)

## 8-week trend
<!-- Data: market_trend("US", weeks=8) -->

## YoY comparison
- Regs: 9236 TY vs 4986 LY (+85%)
- Spend: $678K TY vs $541K LY (+25%)
- Brand regs: +15% YoY
- NB regs: +148% YoY
- NB CPA: $76 vs $138 LY (-45%)
- WoW pattern: TY +22% vs LY -1% (same week)

## Monthly projection inputs
- Month: 2026 Apr (10/30 days elapsed, 20 remaining)
- MTD actuals: $966K spend, 12634 regs (3658 Brand, 8976 NB)
- OP2 targets: $2.8M spend, 31.1K regs
- OP2 pace check: at 33% through the month, linear OP2 pace would be 10.4K regs and $944K spend
- MTD vs OP2 pace: +22% regs, +2% spend
- Simple linear projection (ingester estimate, not accounting for seasonality/holidays): $2.9M spend, 39.0K regs, $74 CPA
- NOTE: Analyst should produce the actual projection accounting for weekday/weekend mix, holidays, LY patterns, and known upcoming changes.

## This year weekly trend (last 12 weeks)
<!-- Data: market_trend("US", weeks=12) -->

## Last year same period (W11 to W19)
<!-- Data: db("SELECT * FROM weekly_metrics WHERE market='US' AND week LIKE '2025%' ORDER BY week") -->

## Daily breakdown
<!-- Data: db("SELECT * FROM daily_metrics WHERE market='US' AND week='2026 W15' ORDER BY date") -->
