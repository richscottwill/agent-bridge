# DE W14 Data Brief

## Headline numbers
- Registrations: 1348 (+111% WoW)
- Spend: $102K (-7% WoW)
- CPA: $76 (-56% WoW)
- Brand regs: 802 (+129% WoW)
- NB regs: 546 (+89% WoW)

## ie%CCP
- This week: 39%
- Last week: 92%
- Target: 100%

## Registration drivers (what caused the WoW change?)
Primary driver: CVR (+140% WoW) more than clicks (-12% WoW)

Brand:
  Regs: 802 vs 350 LW (+129%)
  CVR: 3.41% vs 1.30% (+162%)
  Clicks: 23501 vs 26902 (-13%)
  CPA: $51 vs $133 (-62%)

Non-Brand:
  Regs: 546 vs 289 LW (+89%)
  CVR: 3.67% vs 1.72% (+113%)
  Clicks: 14882 vs 16777 (-11%)
  CPA: $113 vs $218 (-48%)

## 8-week trend
<!-- Data: market_trend("DE", weeks=8) -->

## YoY comparison
- Regs: 1348 TY vs 1250 LY (+8%)
- Spend: $102K TY vs $95K LY (+7%)
- Brand regs: +11% YoY
- NB regs: +3% YoY
- NB CPA: $113 vs $99 LY (+14%)
- WoW pattern: TY +111% vs LY -4% (same week)

## Monthly projection inputs
- Month: 2026 Mar (31/31 days elapsed, 0 remaining)
- MTD actuals: $624K spend, 5386 regs (3171 Brand, 2215 NB)
- OP2 targets: $746K spend, 6.1K regs
- OP2 pace check: at 100% through the month, linear OP2 pace would be 6.1K regs and $746K spend
- MTD vs OP2 pace: -12% regs, -16% spend
- Simple linear projection (ingester estimate, not accounting for seasonality/holidays): $624K spend, 5.4K regs, $116 CPA
- NOTE: Analyst should produce the actual projection accounting for weekday/weekend mix, holidays, LY patterns, and known upcoming changes.

## Anomalies (>20% deviation from recent avg)
- cost: below avg by 34% (current: 102418.22, avg: 155684.14)
- cpa: below avg by 39% (current: 75.98, avg: 125.12)
- cvr: above avg by 39% (current: 0.04, avg: 0.03)
- brand cvr: above avg by 26% (current: 0.03, avg: 0.03)
- nb cvr: above avg by 56% (current: 0.04, avg: 0.02)

## This year weekly trend (last 12 weeks)
<!-- Data: market_trend("DE", weeks=12) -->

## Last year same period (W10 to W18)
<!-- Data: db("SELECT * FROM weekly_metrics WHERE market='DE' AND week LIKE '2025%' ORDER BY week") -->

## Daily breakdown
<!-- Data: db("SELECT * FROM daily_metrics WHERE market='DE' AND week='2026 W14' ORDER BY date") -->
