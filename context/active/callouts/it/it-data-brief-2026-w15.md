# IT W15 Data Brief

## Headline numbers
- Registrations: 990 (-25% WoW)
- Spend: $100K (+5% WoW)
- CPA: $101 (+40% WoW)
- Brand regs: 675 (-22% WoW)
- NB regs: 315 (-30% WoW)

## ie%CCP
- This week: 85%
- Last week: 62%
- Target: 100%

## Registration drivers (what caused the WoW change?)
Primary driver: CVR (-18% WoW) more than clicks (-8% WoW)

Brand:
  Regs: 675 vs 868 LW (-22%)
  CVR: 2.48% vs 2.97% (-16%)
  Clicks: 27172 vs 29182 (-7%)
  CPA: $61 vs $31 (+93%)

Non-Brand:
  Regs: 315 vs 452 LW (-30%)
  CVR: 1.61% vs 2.07% (-22%)
  Clicks: 19522 vs 21836 (-11%)
  CPA: $187 vs $150 (+24%)

## 8-week trend
<!-- Data: market_trend("IT", weeks=8) -->

## YoY comparison
- Regs: 990 TY vs 1150 LY (-14%)
- Spend: $100K TY vs $78K LY (+29%)
- Brand regs: -9% YoY
- NB regs: -23% YoY
- NB CPA: $187 vs $124 LY (+51%)
- WoW pattern: TY -25% vs LY +1% (same week)

## Monthly projection inputs
- Month: 2026 Apr (11/30 days elapsed, 19 remaining)
- MTD actuals: $151K spend, 1824 regs (1228 Brand, 596 NB)
- OP2 targets: $399K spend, 5.0K regs
- OP2 pace check: at 37% through the month, linear OP2 pace would be 1.8K regs and $146K spend
- MTD vs OP2 pace: -1% regs, +3% spend
- Simple linear projection (ingester estimate, not accounting for seasonality/holidays): $421K spend, 4.5K regs, $93 CPA
- NOTE: Analyst should produce the actual projection accounting for weekday/weekend mix, holidays, LY patterns, and known upcoming changes.

## Anomalies (>20% deviation from recent avg)
- regs: below avg by 24% (current: 990.00, avg: 1303.14)
- cpa: above avg by 38% (current: 100.67, avg: 72.96)
- brand regs: below avg by 26% (current: 675.00, avg: 916.43)
- cpc: above avg by 21% (current: 2.13, avg: 1.76)

## This year weekly trend (last 12 weeks)
<!-- Data: market_trend("IT", weeks=12) -->

## Last year same period (W11 to W19)
<!-- Data: db("SELECT * FROM weekly_metrics WHERE market='IT' AND week LIKE '2025%' ORDER BY week") -->

## Daily breakdown
<!-- Data: db("SELECT * FROM daily_metrics WHERE market='IT' AND week='2026 W15' ORDER BY date") -->
