# DE W16 Data Brief

## Headline numbers
- Registrations: 1550 (+29% WoW)
- Spend: $199K (+76% WoW)
- CPA: $128 (+37% WoW)
- Brand regs: 805 (+26% WoW)
- NB regs: 745 (+33% WoW)

## ie%CCP
- This week: 70%
- Last week: 51%
- Target: 100%

## Registration drivers (what caused the WoW change?)
Primary driver: clicks (+44% WoW) more than CVR (-11% WoW)

Brand:
  Regs: 805 vs 641 LW (+26%)
  CVR: 3.22% vs 2.99% (+8%)
  Clicks: 25015 vs 21420 (+17%)
  CPA: $52 vs $62 (-16%)

Non-Brand:
  Regs: 745 vs 559 LW (+33%)
  CVR: 2.24% vs 2.96% (-24%)
  Clicks: 33197 vs 18908 (+76%)
  CPA: $210 vs $130 (+61%)

## 8-week trend
<!-- Data: market_trend("DE", weeks=8) -->

## YoY comparison
- Regs: 1550 TY vs 1027 LY (+51%)
- Spend: $199K TY vs $150K LY (+32%)
- Brand regs: +38% YoY
- NB regs: +68% YoY
- NB CPA: $210 vs $228 LY (-8%)
- WoW pattern: TY +29% vs LY -12% (same week)

## Monthly projection inputs
- Month: 2026 Apr (18/30 days elapsed, 12 remaining)
- MTD actuals: $366K spend, 3400 regs (1817 Brand, 1583 NB)
- OP2 targets: $606K spend, 5.7K regs
- OP2 pace check: at 60% through the month, linear OP2 pace would be 3.4K regs and $363K spend
- MTD vs OP2 pace: -1% regs, +1% spend
- Simple linear projection (ingester estimate, not accounting for seasonality/holidays): $707K spend, 6.1K regs, $117 CPA
- NOTE: Analyst should produce the actual projection accounting for weekday/weekend mix, holidays, LY patterns, and known upcoming changes.

## Anomalies (>20% deviation from recent avg)
- regs: above avg by 27% (current: 1550.00, avg: 1221.14)
- cost: above avg by 41% (current: 198651.95, avg: 140407.79)
- nb regs: above avg by 43% (current: 745.00, avg: 521.00)
- brand cvr: above avg by 21% (current: 0.03, avg: 0.03)

## This year weekly trend (last 12 weeks)
<!-- Data: market_trend("DE", weeks=12) -->

## Last year same period (W12 to W20)
<!-- Data: db("SELECT * FROM weekly_metrics WHERE market='DE' AND week LIKE '2025%' ORDER BY week") -->

## Daily breakdown
<!-- Data: db("SELECT * FROM daily_metrics WHERE market='DE' AND week='2026 W16' ORDER BY date") -->
