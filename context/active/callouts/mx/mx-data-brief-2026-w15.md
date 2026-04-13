# MX W15 Data Brief

## Headline numbers
- Registrations: 504 (+112% WoW)
- Spend: $25K (+31% WoW)
- CPA: $50 (-38% WoW)
- Brand regs: 372 (+172% WoW)
- NB regs: 132 (+31% WoW)

## ie%CCP
- This week: 68%
- Last week: 126%
- Target: 100%

## Registration drivers (what caused the WoW change?)
Primary driver: CVR (+72% WoW) more than clicks (+23% WoW)

Brand:
  Regs: 372 vs 137 LW (+172%)
  CVR: 8.06% vs 4.37% (+84%)
  Clicks: 4614 vs 3132 (+47%)
  CPA: $14 vs $24 (-41%)

Non-Brand:
  Regs: 132 vs 101 LW (+31%)
  CVR: 1.23% vs 1.08% (+14%)
  Clicks: 10752 vs 9349 (+15%)
  CPA: $153 vs $159 (-4%)

## 8-week trend
<!-- Data: market_trend("MX", weeks=8) -->

## YoY comparison
- Regs: 504 TY vs 154 LY (+227%)
- Spend: $25K TY vs $31K LY (-17%)
- Brand regs: +403% YoY
- NB regs: +65% YoY
- NB CPA: $153 vs $377 LY (-59%)
- WoW pattern: TY +112% vs LY -20% (same week)

## Monthly projection inputs
- Month: 2026 Apr (10/30 days elapsed, 20 remaining)
- MTD actuals: $33K spend, 625 regs (449 Brand, 176 NB)
- OP2 targets: $34K spend, 791.2857142857142 regs
- OP2 pace check: at 33% through the month, linear OP2 pace would be 263 regs and $11K spend
- MTD vs OP2 pace: +137% regs, +196% spend
- Simple linear projection (ingester estimate, not accounting for seasonality/holidays): $106K spend, 2.1K regs, $51 CPA
- NOTE: Analyst should produce the actual projection accounting for weekday/weekend mix, holidays, LY patterns, and known upcoming changes.

## Anomalies (>20% deviation from recent avg)
- regs: above avg by 58% (current: 504.00, avg: 318.71)
- cost: above avg by 24% (current: 25444.34, avg: 20591.83)
- cpa: below avg by 24% (current: 50.48, avg: 66.06)
- cvr: above avg by 29% (current: 0.03, avg: 0.03)
- brand regs: above avg by 82% (current: 372.00, avg: 204.43)
- brand cvr: above avg by 40% (current: 0.08, avg: 0.06)

## This year weekly trend (last 12 weeks)
<!-- Data: market_trend("MX", weeks=12) -->

## Last year same period (W11 to W19)
<!-- Data: db("SELECT * FROM weekly_metrics WHERE market='MX' AND week LIKE '2025%' ORDER BY week") -->

## Daily breakdown
<!-- Data: db("SELECT * FROM daily_metrics WHERE market='MX' AND week='2026 W15' ORDER BY date") -->
