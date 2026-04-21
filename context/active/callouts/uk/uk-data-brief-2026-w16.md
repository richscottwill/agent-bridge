# UK W16 Data Brief

## Headline numbers
- Registrations: 1644 (+15% WoW)
- Spend: $124K (+36% WoW)
- CPA: $75 (+19% WoW)
- Brand regs: 499 (+9% WoW)
- NB regs: 1145 (+18% WoW)

## ie%CCP
- This week: 66%
- Last week: 54%
- Target: 100%

## Registration drivers (what caused the WoW change?)
Primary driver: clicks (+24% WoW) more than CVR (-7% WoW)

Brand:
  Regs: 499 vs 458 LW (+9%)
  CVR: 3.04% vs 3.49% (-13%)
  Clicks: 16417 vs 13110 (+25%)
  CPA: $78 vs $69 (+14%)

Non-Brand:
  Regs: 1145 vs 972 LW (+18%)
  CVR: 4.68% vs 4.87% (-4%)
  Clicks: 24466 vs 19955 (+23%)
  CPA: $74 vs $61 (+22%)

## 8-week trend
<!-- Data: market_trend("UK", weeks=8) -->

## YoY comparison
- Regs: 1644 TY vs 567 LY (+190%)
- Spend: $124K TY vs $48K LY (+159%)
- Brand regs: +43% YoY
- NB regs: +423% YoY
- NB CPA: $74 vs $112 LY (-34%)
- WoW pattern: TY +15% vs LY -4% (same week)

## Monthly projection inputs
- Month: 2026 Apr (18/30 days elapsed, 12 remaining)
- MTD actuals: $262K spend, 3872 regs (1224 Brand, 2648 NB)
- OP2 targets: $401K spend, 4.5K regs
- OP2 pace check: at 60% through the month, linear OP2 pace would be 2.7K regs and $240K spend
- MTD vs OP2 pace: +44% regs, +9% spend
- Simple linear projection (ingester estimate, not accounting for seasonality/holidays): $474K spend, 6.7K regs, $71 CPA
- NOTE: Analyst should produce the actual projection accounting for weekday/weekend mix, holidays, LY patterns, and known upcoming changes.

## Anomalies (>20% deviation from recent avg)
- cost: above avg by 36% (current: 124000.66, avg: 91355.81)
- nb regs: above avg by 26% (current: 1145.00, avg: 907.14)

## This year weekly trend (last 12 weeks)
<!-- Data: market_trend("UK", weeks=12) -->

## Last year same period (W12 to W20)
<!-- Data: db("SELECT * FROM weekly_metrics WHERE market='UK' AND week LIKE '2025%' ORDER BY week") -->

## Detected streaks
- NB CPC rising 3 consecutive weeks ($2.74 in W13 to $3.47 in W16)
- CPA rising 3 consecutive weeks ($58 in W13 to $75 in W16)

## Daily breakdown
<!-- Data: db("SELECT * FROM daily_metrics WHERE market='UK' AND week='2026 W16' ORDER BY date") -->
