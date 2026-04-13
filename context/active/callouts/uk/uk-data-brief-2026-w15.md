# UK W15 Data Brief

## Headline numbers
- Registrations: 1453 (flat WoW)
- Spend: $91K (+7% WoW)
- CPA: $63 (+7% WoW)
- Brand regs: 473 (flat WoW)
- NB regs: 980 (-1% WoW)

## ie%CCP
- This week: 53%
- Last week: 50%
- Target: 100%

## Registration drivers (what caused the WoW change?)
Primary driver: CVR (-1% WoW) more than clicks (flat WoW)

Brand:
  Regs: 473 vs 473 LW (flat)
  CVR: 3.61% vs 3.34% (+8%)
  Clicks: 13110 vs 14153 (-7%)
  CPA: $67 vs $65 (+3%)

Non-Brand:
  Regs: 980 vs 985 LW (-1%)
  CVR: 4.91% vs 5.24% (-6%)
  Clicks: 19955 vs 18805 (+6%)
  CPA: $60 vs $55 (+9%)

## 8-week trend
<!-- Data: market_trend("UK", weeks=8) -->

## YoY comparison
- Regs: 1453 TY vs 592 LY (+145%)
- Spend: $91K TY vs $48K LY (+89%)
- Brand regs: +29% YoY
- NB regs: +338% YoY
- NB CPA: $60 vs $104 LY (-42%)
- WoW pattern: TY flat vs LY -14% (same week)

## Monthly projection inputs
- Month: 2026 Apr (11/30 days elapsed, 19 remaining)
- MTD actuals: $138K spend, 2259 regs (747 Brand, 1512 NB)
- OP2 targets: $432K spend, 4.5K regs
- OP2 pace check: at 37% through the month, linear OP2 pace would be 1.6K regs and $158K spend
- MTD vs OP2 pace: +37% regs, -13% spend
- Simple linear projection (ingester estimate, not accounting for seasonality/holidays): $385K spend, 6.2K regs, $62 CPA
- NOTE: Analyst should produce the actual projection accounting for weekday/weekend mix, holidays, LY patterns, and known upcoming changes.

## Anomalies (>20% deviation from recent avg)
- brand cvr: above avg by 21% (current: 0.04, avg: 0.03)

## This year weekly trend (last 12 weeks)
<!-- Data: market_trend("UK", weeks=12) -->

## Last year same period (W11 to W19)
<!-- Data: db("SELECT * FROM weekly_metrics WHERE market='UK' AND week LIKE '2025%' ORDER BY week") -->

## Daily breakdown
<!-- Data: db("SELECT * FROM daily_metrics WHERE market='UK' AND week='2026 W15' ORDER BY date") -->
