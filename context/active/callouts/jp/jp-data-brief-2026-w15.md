# JP W15 Data Brief

## Headline numbers
- Registrations: 595 (-2% WoW)
- Spend: $41K (-11% WoW)
- CPA: $68 (-10% WoW)
- Brand regs: 591 (-1% WoW)
- NB regs: 4 (-43% WoW)

## ie%CCP
- This week: 35%
- Last week: 39%
- Target: 100%

## Registration drivers (what caused the WoW change?)
Primary driver: CVR (-2% WoW) more than clicks (flat WoW)

Brand:
  Regs: 591 vs 599 LW (-1%)
  CVR: 2.27% vs 2.39% (-5%)
  Clicks: 26082 vs 25046 (+4%)
  CPA: $66 vs $59 (+12%)

Non-Brand:
  Regs: 4 vs 7 LW (-43%)
  CVR: 0.39% vs 0.33% (+17%)
  Clicks: 1034 vs 2116 (-51%)
  CPA: $459 vs $1,519 (-70%)

## 8-week trend
<!-- Data: market_trend("JP", weeks=8) -->

## YoY comparison
- Regs: 595 TY vs 547 LY (+9%)
- Spend: $41K TY vs $33K LY (+23%)
- Brand regs: +9% YoY
- NB regs: +33% YoY
- NB CPA: $459 vs $1,217 LY (-62%)
- WoW pattern: TY -2% vs LY +10% (same week)

## Monthly projection inputs
- Month: 2026 Apr (11/30 days elapsed, 19 remaining)
- MTD actuals: $65K spend, 971 regs (965 Brand, 6 NB)
- OP2 targets: $145K spend, 1.9K regs
- OP2 pace check: at 37% through the month, linear OP2 pace would be 703 regs and $53K spend
- MTD vs OP2 pace: +38% regs, +23% spend
- Simple linear projection (ingester estimate, not accounting for seasonality/holidays): $175K spend, 2.6K regs, $68 CPA
- NOTE: Analyst should produce the actual projection accounting for weekday/weekend mix, holidays, LY patterns, and known upcoming changes.

## Anomalies (>20% deviation from recent avg)
- regs: above avg by 21% (current: 595.00, avg: 493.71)
- brand regs: above avg by 21% (current: 591.00, avg: 490.29)

## This year weekly trend (last 12 weeks)
<!-- Data: market_trend("JP", weeks=12) -->

## Last year same period (W11 to W19)
<!-- Data: db("SELECT * FROM weekly_metrics WHERE market='JP' AND week LIKE '2025%' ORDER BY week") -->

## Daily breakdown
<!-- Data: db("SELECT * FROM daily_metrics WHERE market='JP' AND week='2026 W15' ORDER BY date") -->
