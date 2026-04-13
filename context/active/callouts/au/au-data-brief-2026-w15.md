# AU W15 Data Brief

## Headline numbers
- Registrations: 166 (-2% WoW)
- Spend: $26K (+17% WoW)
- CPA: $156 (+20% WoW)
- Brand regs: 76 (-21% WoW)
- NB regs: 90 (+22% WoW)

## Registration drivers (what caused the WoW change?)
Primary driver: CVR (-10% WoW) more than clicks (+9% WoW)

Brand:
  Regs: 76 vs 96 LW (-21%)
  CVR: 6.00% vs 6.80% (-12%)
  Clicks: 1267 vs 1411 (-10%)
  CPA: $53 vs $45 (+19%)

Non-Brand:
  Regs: 90 vs 74 LW (+22%)
  CVR: 1.97% vs 1.87% (+5%)
  Clicks: 4562 vs 3951 (+15%)
  CPA: $242 vs $240 (+1%)

## 8-week trend
<!-- Data: market_trend("AU", weeks=8) -->

## Monthly projection inputs
- Month: 2026 Apr (11/30 days elapsed, 19 remaining)
- MTD actuals: $38K spend, 250 regs (120 Brand, 130 NB)
- OP2 targets: $145K spend, 1.1K regs
- OP2 pace check: at 37% through the month, linear OP2 pace would be 392 regs and $53K spend
- MTD vs OP2 pace: -36% regs, -28% spend
- Simple linear projection (ingester estimate, not accounting for seasonality/holidays): $108K spend, 701 regs, $154 CPA
- NOTE: Analyst should produce the actual projection accounting for weekday/weekend mix, holidays, LY patterns, and known upcoming changes.

## Anomalies (>20% deviation from recent avg)
- regs: below avg by 29% (current: 166.00, avg: 232.29)
- cpa: above avg by 21% (current: 155.59, avg: 129.12)
- cvr: below avg by 27% (current: 0.03, avg: 0.04)
- brand regs: below avg by 29% (current: 76.00, avg: 106.71)
- nb regs: below avg by 28% (current: 90.00, avg: 125.57)
- nb cvr: below avg by 29% (current: 0.02, avg: 0.03)

## This year weekly trend (last 12 weeks)
<!-- Data: market_trend("AU", weeks=12) -->

## Detected streaks
- CPA rising 3 consecutive weeks ($115 in W12 to $156 in W15)
- Regs declining 3 consecutive weeks (244 in W12 to 166 in W15)

## Daily breakdown
<!-- Data: db("SELECT * FROM daily_metrics WHERE market='AU' AND week='2026 W15' ORDER BY date") -->
