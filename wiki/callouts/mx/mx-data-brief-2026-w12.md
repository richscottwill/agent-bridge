<!-- DOC-0077 | duck_id: callout-mx-data-brief-2026-w12 -->
# MX W12 Data Brief

## Headline numbers
- Registrations: 330 (-16% WoW)
- Spend: $20K (-10% WoW)
- CPA: $61 (+7% WoW)
- Brand regs: 208 (-15% WoW)
- NB regs: 122 (-17% WoW)

## ie%CCP
- This week: 90%
- Last week: 85%
- Target: 100%

## Registration drivers (what caused the WoW change?)
Primary driver: CVR (-11% WoW) more than clicks (-6% WoW)

Brand:
  Regs: 208 vs 246 LW (-15%)
  CVR: 6.15% vs 6.79% (-9%)
  Clicks: 3384 vs 3623 (-7%)
  CPA: $20 vs $19 (+3%)

Non-Brand:
  Regs: 122 vs 147 LW (-17%)
  CVR: 1.38% vs 1.57% (-12%)
  Clicks: 8826 vs 9351 (-6%)
  CPA: $131 vs $121 (+9%)

## 8-week trend
<!-- Data: market_trend("MX", weeks=8) -->

## YoY comparison
- Regs: 330 TY vs 174 LY (+90%)
- Spend: $20K TY vs $31K LY (-35%)
- Brand regs: +271% YoY
- NB regs: +3% YoY
- NB CPA: $131 vs $260 LY (-50%)
- WoW pattern: TY -16% vs LY -12% (same week)

## Monthly projection inputs
- Month: 2026 Mar (21/31 days elapsed, 10 remaining)
- MTD actuals: $63K spend, 1021 regs (653 Brand, 368 NB)
- OP2 targets: $57K spend, 859 regs
- OP2 pace check: at 68% through the month, linear OP2 pace would be 581 regs and $38K spend
- MTD vs OP2 pace: +75% regs, +65% spend
- Simple linear projection (ingester estimate, not accounting for seasonality/holidays): $92K spend, 1.5K regs, $62 CPA
- NOTE: Analyst should produce the actual projection accounting for weekday/weekend mix, holidays, LY patterns, and known upcoming changes.

## Anomalies (>20% deviation from recent avg)
- nb regs: above avg by 20% (current: 122.00, avg: 101.57)

## This year weekly trend (last 12 weeks)
<!-- Data: market_trend("MX", weeks=12) -->

## Last year same period (W8 to W16)
<!-- Data: db("SELECT * FROM weekly_metrics WHERE market='MX' AND week LIKE '2025%' ORDER BY week") -->

## Daily breakdown
<!-- Data: db("SELECT * FROM daily_metrics WHERE market='MX' AND week='2026 W12' ORDER BY date") -->
