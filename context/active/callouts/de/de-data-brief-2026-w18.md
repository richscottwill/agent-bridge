# DE W18 Data Brief

## Headline numbers
- Registrations: 1302 (-13% WoW)
- Spend: $174K (-18% WoW)
- CPA: $133 (-5% WoW)
- Brand regs: 677 (-12% WoW)
- NB regs: 625 (-14% WoW)

## ie%CCP
- This week: 61%
- Last week: 64%
- Target: 100%

## Registration drivers (what caused the WoW change?)
Primary driver: clicks (-9% WoW) more than CVR (-5% WoW)

Brand:
  Regs: 677 vs 769 LW (-12%)
  CVR: 2.93% vs 3.03% (-3%)
  Clicks: 23125 vs 25415 (-9%)
  CPA: $73 vs $69 (+5%)

Non-Brand:
  Regs: 625 vs 727 LW (-14%)
  CVR: 1.97% vs 2.09% (-6%)
  Clicks: 31773 vs 34705 (-8%)
  CPA: $199 vs $216 (-8%)

## 8-week trend
<!-- Data: market_trend("DE", weeks=8) -->

## YoY comparison
- Regs: 1302 TY vs 942 LY (+38%)
- Spend: $174K TY vs $148K LY (+17%)
- Brand regs: +22% YoY
- NB regs: +61% YoY
- NB CPA: $199 vs $255 LY (-22%)
- WoW pattern: TY -13% vs LY -4% (same week)

## Monthly projection inputs
- Month: 2026 Apr (30/30 days elapsed, 0 remaining)
- MTD actuals: $720K spend, 5861 regs (3072 Brand, 2789 NB)
- OP2 targets: $606K spend, 5.7K regs
- OP2 pace check: at 100% through the month, linear OP2 pace would be 5.7K regs and $606K spend
- MTD vs OP2 pace: +2% regs, +19% spend
- Simple linear projection (ingester estimate, not accounting for seasonality/holidays): $720K spend, 5.9K regs, $123 CPA
- NOTE: Analyst should produce the actual projection accounting for weekday/weekend mix, holidays, LY patterns, and known upcoming changes.

## This year weekly trend (last 12 weeks)
<!-- Data: market_trend("DE", weeks=12) -->

## Last year same period (W14 to W22)
<!-- Data: db("SELECT * FROM weekly_metrics WHERE market='DE' AND week LIKE '2025%' ORDER BY week") -->

## Daily breakdown
<!-- Data: db("SELECT * FROM daily_metrics WHERE market='DE' AND week='2026 W18' ORDER BY date") -->
