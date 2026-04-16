# IT W15 Data Brief

## Headline numbers
- Registrations: 981 (-25% WoW)
- Spend: $100K (+5% WoW)
- CPA: $102 (+41% WoW)
- Brand regs: 671 (-22% WoW)
- NB regs: 310 (-31% WoW)

## ie%CCP
- This week: 86%
- Last week: 62%
- Target: 100%

## Registration drivers (what caused the WoW change?)
Primary driver: CVR (-19% WoW) more than clicks (-8% WoW)

Brand:
  Regs: 671 vs 865 LW (-22%)
  CVR: 2.47% vs 2.96% (-17%)
  Clicks: 27172 vs 29182 (-7%)
  CPA: $61 vs $31 (+94%)

Non-Brand:
  Regs: 310 vs 451 LW (-31%)
  CVR: 1.59% vs 2.07% (-23%)
  Clicks: 19522 vs 21836 (-11%)
  CPA: $190 vs $150 (+26%)

## 8-week trend
<!-- Data: market_trend("IT", weeks=8) -->

## YoY comparison
- Regs: 981 TY vs 1151 LY (-15%)
- Spend: $100K TY vs $78K LY (+29%)
- Brand regs: -9% YoY
- NB regs: -25% YoY
- NB CPA: $190 vs $124 LY (+53%)
- WoW pattern: TY -25% vs LY +1% (same week)

## Monthly projection inputs
- Month: 2026 Apr (11/30 days elapsed, 19 remaining)
- MTD actuals: $151K spend, 1811 regs (1221 Brand, 590 NB)
- OP2 targets: $351K spend, 5.0K regs
- OP2 pace check: at 37% through the month, linear OP2 pace would be 1.8K regs and $129K spend
- MTD vs OP2 pace: -2% regs, +17% spend
- Simple linear projection (ingester estimate, not accounting for seasonality/holidays): $421K spend, 4.5K regs, $94 CPA
- NOTE: Analyst should produce the actual projection accounting for weekday/weekend mix, holidays, LY patterns, and known upcoming changes.

## Anomalies (>20% deviation from recent avg)
- regs: below avg by 25% (current: 981.00, avg: 1301.57)
- cpa: above avg by 39% (current: 101.60, avg: 73.06)
- brand regs: below avg by 27% (current: 671.00, avg: 915.29)
- cpc: above avg by 21% (current: 2.13, avg: 1.76)

## This year weekly trend (last 12 weeks)
<!-- Data: market_trend("IT", weeks=12) -->

## Last year same period (W11 to W19)
<!-- Data: db("SELECT * FROM weekly_metrics WHERE market='IT' AND week LIKE '2025%' ORDER BY week") -->

## Daily breakdown
<!-- Data: db("SELECT * FROM daily_metrics WHERE market='IT' AND week='2026 W15' ORDER BY date") -->
