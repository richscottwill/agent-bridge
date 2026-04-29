# CA W17 Data Brief

## Headline numbers
- Registrations: 696 (-7% WoW)
- Spend: $55K (-9% WoW)
- CPA: $79 (-2% WoW)
- Brand regs: 426 (flat WoW)
- NB regs: 270 (-16% WoW)

## ie%CCP
- This week: 56%
- Last week: 60%
- Target: 100%

## Registration drivers (what caused the WoW change?)
Primary driver: clicks (-5% WoW) more than CVR (-2% WoW)

Brand:
  Regs: 426 vs 428 LW (flat)
  CVR: 3.26% vs 3.29% (-1%)
  Clicks: 13087 vs 13025 (flat)
  CPA: $61 vs $66 (-7%)

Non-Brand:
  Regs: 270 vs 322 LW (-16%)
  CVR: 2.01% vs 2.16% (-7%)
  Clicks: 13426 vs 14941 (-10%)
  CPA: $107 vs $100 (+7%)

## 8-week trend
<!-- Data: market_trend("CA", weeks=8) -->

## YoY comparison
- Regs: 696 TY vs 440 LY (+58%)
- Spend: $55K TY vs $47K LY (+16%)
- Brand regs: +39% YoY
- NB regs: +101% YoY
- NB CPA: $107 vs $234 LY (-54%)
- WoW pattern: TY -7% vs LY +18% (same week)

## Monthly projection inputs
- Month: 2026 Apr (25/30 days elapsed, 5 remaining)
- MTD actuals: $200K spend, 2536 regs (1507 Brand, 1029 NB)
- OP2 targets: $214K spend, 2.4K regs
- OP2 pace check: at 83% through the month, linear OP2 pace would be 2.0K regs and $179K spend
- MTD vs OP2 pace: +24% regs, +12% spend
- Simple linear projection (ingester estimate, not accounting for seasonality/holidays): $239K spend, 3.0K regs, $79 CPA
- NOTE: Analyst should produce the actual projection accounting for weekday/weekend mix, holidays, LY patterns, and known upcoming changes.

## This year weekly trend (last 12 weeks)
<!-- Data: market_trend("CA", weeks=12) -->

## Last year same period (W13 to W21)
<!-- Data: db("SELECT * FROM weekly_metrics WHERE market='CA' AND week LIKE '2025%' ORDER BY week") -->

## Daily breakdown
<!-- Data: db("SELECT * FROM daily_metrics WHERE market='CA' AND week='2026 W17' ORDER BY date") -->
