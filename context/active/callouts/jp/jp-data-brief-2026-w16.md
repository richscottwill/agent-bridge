# JP W16 Data Brief

## Headline numbers
- Registrations: 544 (-7% WoW)
- Spend: $36K (-12% WoW)
- CPA: $65 (-6% WoW)
- Brand regs: 542 (-6% WoW)
- NB regs: 2 (-50% WoW)

## ie%CCP
- This week: 34%
- Last week: 36%
- Target: 100%

## Registration drivers (what caused the WoW change?)
Primary driver: CVR (-5% WoW) more than clicks (-1% WoW)

Brand:
  Regs: 542 vs 579 LW (-6%)
  CVR: 2.09% vs 2.22% (-6%)
  Clicks: 25930 vs 26082 (-1%)
  CPA: $64 vs $67 (-4%)

Non-Brand:
  Regs: 2 vs 4 LW (-50%)
  CVR: 0.25% vs 0.39% (-35%)
  Clicks: 791 vs 1034 (-24%)
  CPA: $442 vs $459 (-4%)

## 8-week trend
<!-- Data: market_trend("JP", weeks=8) -->

## YoY comparison
- Regs: 544 TY vs 500 LY (+9%)
- Spend: $36K TY vs $30K LY (+17%)
- Brand regs: +9% YoY
- NB regs: -50% YoY
- NB CPA: $442 vs $891 LY (-50%)
- WoW pattern: TY -7% vs LY -9% (same week)

## Monthly projection inputs
- Month: 2026 Apr (18/30 days elapsed, 12 remaining)
- MTD actuals: $101K spend, 1498 regs (1490 Brand, 8 NB)
- OP2 targets: $145K spend, 1.9K regs
- OP2 pace check: at 60% through the month, linear OP2 pace would be 1.2K regs and $87K spend
- MTD vs OP2 pace: +30% regs, +16% spend
- Simple linear projection (ingester estimate, not accounting for seasonality/holidays): $162K spend, 2.4K regs, $67 CPA
- NOTE: Analyst should produce the actual projection accounting for weekday/weekend mix, holidays, LY patterns, and known upcoming changes.

## This year weekly trend (last 12 weeks)
<!-- Data: market_trend("JP", weeks=12) -->

## Last year same period (W12 to W20)
<!-- Data: db("SELECT * FROM weekly_metrics WHERE market='JP' AND week LIKE '2025%' ORDER BY week") -->

## Detected streaks
- CPA declining 3 consecutive weeks ($87 in W13 to $65 in W16)

## Daily breakdown
<!-- Data: db("SELECT * FROM daily_metrics WHERE market='JP' AND week='2026 W16' ORDER BY date") -->
