# JP W18 Data Brief

## Headline numbers
- Registrations: 425 (-24% WoW)
- Spend: $28K (-15% WoW)
- CPA: $65 (+11% WoW)
- Brand regs: 422 (-24% WoW)
- NB regs: 3 (+50% WoW)

## ie%CCP
- This week: 29%
- Last week: 26%
- Target: 100%

## Registration drivers (what caused the WoW change?)
Primary driver: clicks (-20% WoW) more than CVR (-4% WoW)

Brand:
  Regs: 422 vs 557 LW (-24%)
  CVR: 2.26% vs 2.22% (+2%)
  Clicks: 18675 vs 25108 (-26%)
  CPA: $60 vs $56 (+8%)

Non-Brand:
  Regs: 3 vs 2 LW (+50%)
  CVR: 0.12% vs 0.13% (-8%)
  Clicks: 2508 vs 1537 (+63%)
  CPA: $707 vs $777 (-9%)

## 8-week trend
<!-- Data: market_trend("JP", weeks=8) -->

## YoY comparison
- Regs: 425 TY vs 373 LY (+14%)
- Spend: $28K TY vs $26K LY (+8%)
- Brand regs: +15% YoY
- NB regs: -40% YoY
- NB CPA: $707 vs $647 LY (+9%)
- WoW pattern: TY -24% vs LY -19% (same week)

## Monthly projection inputs
- Month: 2026 Apr (30/30 days elapsed, 0 remaining)
- MTD actuals: $153K spend, 2333 regs (2321 Brand, 12 NB)
- OP2 targets: $145K spend, 1.9K regs
- OP2 pace check: at 100% through the month, linear OP2 pace would be 1.9K regs and $145K spend
- MTD vs OP2 pace: +22% regs, +6% spend
- Simple linear projection (ingester estimate, not accounting for seasonality/holidays): $153K spend, 2.3K regs, $66 CPA
- NOTE: Analyst should produce the actual projection accounting for weekday/weekend mix, holidays, LY patterns, and known upcoming changes.

## Anomalies (>20% deviation from recent avg)
- cost: below avg by 30% (current: 27581.14, avg: 39545.30)

## This year weekly trend (last 12 weeks)
<!-- Data: market_trend("JP", weeks=12) -->

## Last year same period (W14 to W22)
<!-- Data: db("SELECT * FROM weekly_metrics WHERE market='JP' AND week LIKE '2025%' ORDER BY week") -->

## Detected streaks
- NB CPC declining 4 consecutive weeks ($5.02 in W14 to $0.85 in W18)

## Daily breakdown
<!-- Data: db("SELECT * FROM daily_metrics WHERE market='JP' AND week='2026 W18' ORDER BY date") -->
