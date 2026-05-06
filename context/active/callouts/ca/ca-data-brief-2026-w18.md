# CA W18 Data Brief

## Headline numbers
- Registrations: 677 (-1% WoW)
- Spend: $51K (-7% WoW)
- CPA: $75 (-6% WoW)
- Brand regs: 410 (-2% WoW)
- NB regs: 267 (-1% WoW)

## ie%CCP
- This week: 54%
- Last week: 57%
- Target: 100%

## Registration drivers (what caused the WoW change?)
Primary driver: clicks (-3% WoW) more than CVR (+1% WoW)

Brand:
  Regs: 410 vs 417 LW (-2%)
  CVR: 2.98% vs 3.19% (-6%)
  Clicks: 13736 vs 13087 (+5%)
  CPA: $61 vs $62 (-2%)

Non-Brand:
  Regs: 267 vs 269 LW (-1%)
  CVR: 2.21% vs 2.00% (+10%)
  Clicks: 12085 vs 13426 (-10%)
  CPA: $98 vs $107 (-9%)

## 8-week trend
<!-- Data: market_trend("CA", weeks=8) -->

## YoY comparison
- Regs: 677 TY vs 466 LY (+45%)
- Spend: $51K TY vs $45K LY (+13%)
- Brand regs: +21% YoY
- NB regs: +110% YoY
- NB CPA: $98 vs $225 LY (-57%)
- WoW pattern: TY -1% vs LY +6% (same week)

## Monthly projection inputs
- Month: 2026 Apr (30/30 days elapsed, 0 remaining)
- MTD actuals: $238K spend, 3009 regs (1791 Brand, 1218 NB)
- OP2 targets: $214K spend, 2.4K regs
- OP2 pace check: at 100% through the month, linear OP2 pace would be 2.4K regs and $214K spend
- MTD vs OP2 pace: +23% regs, +11% spend
- Simple linear projection (ingester estimate, not accounting for seasonality/holidays): $238K spend, 3.0K regs, $79 CPA
- NOTE: Analyst should produce the actual projection accounting for weekday/weekend mix, holidays, LY patterns, and known upcoming changes.

## This year weekly trend (last 12 weeks)
<!-- Data: market_trend("CA", weeks=12) -->

## Last year same period (W14 to W22)
<!-- Data: db("SELECT * FROM weekly_metrics WHERE market='CA' AND week LIKE '2025%' ORDER BY week") -->

## Detected streaks
- CPA declining 3 consecutive weeks ($85 in W15 to $75 in W18)

## Daily breakdown
<!-- Data: db("SELECT * FROM daily_metrics WHERE market='CA' AND week='2026 W18' ORDER BY date") -->
