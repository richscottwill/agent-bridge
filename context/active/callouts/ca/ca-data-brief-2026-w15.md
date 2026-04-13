# CA W15 Data Brief

## Headline numbers
- Registrations: 680 (+7% WoW)
- Spend: $56K (+11% WoW)
- CPA: $83 (+4% WoW)
- Brand regs: 422 (+5% WoW)
- NB regs: 258 (+11% WoW)

## ie%CCP
- This week: 58%
- Last week: 55%
- Target: 100%

## Registration drivers (what caused the WoW change?)
Primary driver: clicks (+7% WoW) more than CVR (+1% WoW)

Brand:
  Regs: 422 vs 401 LW (+5%)
  CVR: 3.09% vs 3.11% (-1%)
  Clicks: 13667 vs 12906 (+6%)
  CPA: $60 vs $56 (+8%)

Non-Brand:
  Regs: 258 vs 233 LW (+11%)
  CVR: 1.77% vs 1.71% (+3%)
  Clicks: 14610 vs 13633 (+7%)
  CPA: $120 vs $122 (-2%)

## 8-week trend
<!-- Data: market_trend("CA", weeks=8) -->

## YoY comparison
- Regs: 680 TY vs 442 LY (+54%)
- Spend: $56K TY vs $51K LY (+10%)
- Brand regs: +35% YoY
- NB regs: +98% YoY
- NB CPA: $120 vs $276 LY (-57%)
- WoW pattern: TY +7% vs LY -6% (same week)

## Monthly projection inputs
- Month: 2026 Apr (10/30 days elapsed, 20 remaining)
- MTD actuals: $78K spend, 938 regs (585 Brand, 353 NB)
- OP2 targets: $225K spend, 2.4K regs
- OP2 pace check: at 33% through the month, linear OP2 pace would be 815 regs and $75K spend
- MTD vs OP2 pace: +15% regs, +5% spend
- Simple linear projection (ingester estimate, not accounting for seasonality/holidays): $240K spend, 2.9K regs, $83 CPA
- NOTE: Analyst should produce the actual projection accounting for weekday/weekend mix, holidays, LY patterns, and known upcoming changes.

## This year weekly trend (last 12 weeks)
<!-- Data: market_trend("CA", weeks=12) -->

## Last year same period (W11 to W19)
<!-- Data: db("SELECT * FROM weekly_metrics WHERE market='CA' AND week LIKE '2025%' ORDER BY week") -->

## Daily breakdown
<!-- Data: db("SELECT * FROM daily_metrics WHERE market='CA' AND week='2026 W15' ORDER BY date") -->
