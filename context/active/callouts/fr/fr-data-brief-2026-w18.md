# FR W18 Data Brief

## Headline numbers
- Registrations: 1061 (+2% WoW)
- Spend: $65K (-4% WoW)
- CPA: $61 (-6% WoW)
- Brand regs: 425 (-6% WoW)
- NB regs: 636 (+9% WoW)

## ie%CCP
- This week: 54%
- Last week: 57%
- Target: 100%

## Registration drivers (what caused the WoW change?)
Primary driver: CVR (+9% WoW) more than clicks (-6% WoW)

Brand:
  Regs: 425 vs 453 LW (-6%)
  CVR: 2.33% vs 2.47% (-6%)
  Clicks: 18275 vs 18311 (flat)
  CPA: $44 vs $41 (+6%)

Non-Brand:
  Regs: 636 vs 585 LW (+9%)
  CVR: 3.51% vs 2.85% (+23%)
  Clicks: 18126 vs 20546 (-12%)
  CPA: $73 vs $84 (-13%)

## 8-week trend
<!-- Data: market_trend("FR", weeks=8) -->

## YoY comparison
- Regs: 1061 TY vs 810 LY (+31%)
- Spend: $65K TY vs $35K LY (+85%)
- Brand regs: +31% YoY
- NB regs: +31% YoY
- NB CPA: $73 vs $54 LY (+36%)
- WoW pattern: TY +2% vs LY -7% (same week)

## Monthly projection inputs
- Month: 2026 Apr (30/30 days elapsed, 0 remaining)
- MTD actuals: $284K spend, 4403 regs (1848 Brand, 2555 NB)
- OP2 targets: $224K spend, 4.1K regs
- OP2 pace check: at 100% through the month, linear OP2 pace would be 4.1K regs and $224K spend
- MTD vs OP2 pace: +7% regs, +27% spend
- Simple linear projection (ingester estimate, not accounting for seasonality/holidays): $284K spend, 4.4K regs, $65 CPA
- NOTE: Analyst should produce the actual projection accounting for weekday/weekend mix, holidays, LY patterns, and known upcoming changes.

## Anomalies (>20% deviation from recent avg)
- nb cvr: above avg by 30% (current: 0.04, avg: 0.03)

## This year weekly trend (last 12 weeks)
<!-- Data: market_trend("FR", weeks=12) -->

## Last year same period (W14 to W22)
<!-- Data: db("SELECT * FROM weekly_metrics WHERE market='FR' AND week LIKE '2025%' ORDER BY week") -->

## Detected streaks
- NB CPC rising 4 consecutive weeks ($1.96 in W14 to $2.57 in W18)
- CPA declining 3 consecutive weeks ($70 in W15 to $61 in W18)
- Regs rising 3 consecutive weeks (870 in W15 to 1061 in W18)

## Daily breakdown
<!-- Data: db("SELECT * FROM daily_metrics WHERE market='FR' AND week='2026 W18' ORDER BY date") -->
