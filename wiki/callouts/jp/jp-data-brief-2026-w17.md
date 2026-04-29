# JP W17 Data Brief

## Headline numbers
- Registrations: 555 (+10% WoW)
- Spend: $33K (-8% WoW)
- CPA: $59 (-17% WoW)
- Brand regs: 553 (+10% WoW)
- NB regs: 2 (flat WoW)

## ie%CCP
- This week: 26%
- Last week: 32%
- Target: 100%

## Registration drivers (what caused the WoW change?)
Primary driver: CVR (+11% WoW) more than clicks (flat WoW)

Brand:
  Regs: 553 vs 501 LW (+10%)
  CVR: 2.20% vs 1.93% (+14%)
  Clicks: 25108 vs 25930 (-3%)
  CPA: $56 vs $69 (-19%)

Non-Brand:
  Regs: 2 vs 2 LW (flat)
  CVR: 0.13% vs 0.25% (-49%)
  Clicks: 1537 vs 791 (+94%)
  CPA: $777 vs $442 (+76%)

## 8-week trend
<!-- Data: market_trend("JP", weeks=8) -->

## YoY comparison
- Regs: 555 TY vs 458 LY (+21%)
- Spend: $33K TY vs $29K LY (+14%)
- Brand regs: +21% YoY
- WoW pattern: TY +10% vs LY -8% (same week)

## Monthly projection inputs
- Month: 2026 Apr (25/30 days elapsed, 5 remaining)
- MTD actuals: $133K spend, 1998 regs (1988 Brand, 10 NB)
- OP2 targets: $145K spend, 1.9K regs
- OP2 pace check: at 83% through the month, linear OP2 pace would be 1.6K regs and $120K spend
- MTD vs OP2 pace: +25% regs, +11% spend
- Simple linear projection (ingester estimate, not accounting for seasonality/holidays): $157K spend, 2.4K regs, $65 CPA
- NOTE: Analyst should produce the actual projection accounting for weekday/weekend mix, holidays, LY patterns, and known upcoming changes.

## Anomalies (>20% deviation from recent avg)
- cpa: below avg by 24% (current: 58.80, avg: 77.37)

## This year weekly trend (last 12 weeks)
<!-- Data: market_trend("JP", weeks=12) -->

## Last year same period (W13 to W21)
<!-- Data: db("SELECT * FROM weekly_metrics WHERE market='JP' AND week LIKE '2025%' ORDER BY week") -->

## Detected streaks
- NB CPC declining 3 consecutive weeks ($5.02 in W14 to $1.01 in W17)
- CPA declining 4 consecutive weeks ($87 in W13 to $59 in W17)

## Daily breakdown
<!-- Data: db("SELECT * FROM daily_metrics WHERE market='JP' AND week='2026 W17' ORDER BY date") -->
