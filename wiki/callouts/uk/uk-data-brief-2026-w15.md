# UK W15 Data Brief

## Headline numbers
- Registrations: 1449 (flat WoW)
- Spend: $91K (+7% WoW)
- CPA: $63 (+7% WoW)
- Brand regs: 469 (+1% WoW)
- NB regs: 980 (flat WoW)

## ie%CCP
- This week: 53%
- Last week: 50%
- Target: 100%

## Registration drivers (what caused the WoW change?)
Primary driver: CVR (flat WoW) more than clicks (flat WoW)

Brand:
  Regs: 469 vs 466 LW (+1%)
  CVR: 3.58% vs 3.29% (+9%)
  Clicks: 13110 vs 14153 (-7%)
  CPA: $67 vs $66 (+2%)

Non-Brand:
  Regs: 980 vs 984 LW (flat)
  CVR: 4.91% vs 5.23% (-6%)
  Clicks: 19955 vs 18805 (+6%)
  CPA: $60 vs $55 (+9%)

## 8-week trend
<!-- Data: market_trend("UK", weeks=8) -->

## YoY comparison
- Regs: 1449 TY vs 592 LY (+145%)
- Spend: $91K TY vs $48K LY (+89%)
- Brand regs: +27% YoY
- NB regs: +338% YoY
- NB CPA: $60 vs $104 LY (-42%)
- WoW pattern: TY flat vs LY -14% (same week)

## Monthly projection inputs
- Month: 2026 Apr (11/30 days elapsed, 19 remaining)
- MTD actuals: $138K spend, 2248 regs (737 Brand, 1511 NB)
- OP2 targets: $401K spend, 4.5K regs
- OP2 pace check: at 37% through the month, linear OP2 pace would be 1.6K regs and $147K spend
- MTD vs OP2 pace: +36% regs, -6% spend
- Simple linear projection (ingester estimate, not accounting for seasonality/holidays): $385K spend, 6.2K regs, $62 CPA
- NOTE: Analyst should produce the actual projection accounting for weekday/weekend mix, holidays, LY patterns, and known upcoming changes.

## Anomalies (>20% deviation from recent avg)
- brand cvr: above avg by 20% (current: 0.04, avg: 0.03)

## This year weekly trend (last 12 weeks)
<!-- Data: market_trend("UK", weeks=12) -->

## Last year same period (W11 to W19)
<!-- Data: db("SELECT * FROM weekly_metrics WHERE market='UK' AND week LIKE '2025%' ORDER BY week") -->

## Daily breakdown
<!-- Data: db("SELECT * FROM daily_metrics WHERE market='UK' AND week='2026 W15' ORDER BY date") -->
