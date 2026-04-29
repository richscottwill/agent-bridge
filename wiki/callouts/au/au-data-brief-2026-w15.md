# AU W15 Data Brief

## Headline numbers
- Registrations: 168 (-1% WoW)
- Spend: $26K (+17% WoW)
- CPA: $154 (+18% WoW)
- Brand regs: 77 (-20% WoW)
- NB regs: 91 (+23% WoW)

## Registration drivers (what caused the WoW change?)
Primary driver: CVR (-9% WoW) more than clicks (+9% WoW)

Brand:
  Regs: 77 vs 96 LW (-20%)
  CVR: 6.08% vs 6.80% (-11%)
  Clicks: 1267 vs 1411 (-10%)
  CPA: $53 vs $45 (+18%)

Non-Brand:
  Regs: 91 vs 74 LW (+23%)
  CVR: 1.99% vs 1.87% (+7%)
  Clicks: 4562 vs 3951 (+15%)
  CPA: $239 vs $240 (flat)

## 8-week trend
<!-- Data: market_trend("AU", weeks=8) -->

## Monthly projection inputs
- Month: 2026 Apr (11/30 days elapsed, 19 remaining)
- MTD actuals: $38K spend, 252 regs (121 Brand, 131 NB)
- OP2 targets: $148K spend, 1.1K regs
- OP2 pace check: at 37% through the month, linear OP2 pace would be 392 regs and $54K spend
- MTD vs OP2 pace: -36% regs, -30% spend
- Simple linear projection (ingester estimate, not accounting for seasonality/holidays): $108K spend, 708 regs, $153 CPA
- NOTE: Analyst should produce the actual projection accounting for weekday/weekend mix, holidays, LY patterns, and known upcoming changes.

## Anomalies (>20% deviation from recent avg)
- regs: below avg by 28% (current: 168.00, avg: 232.29)
- cvr: below avg by 26% (current: 0.03, avg: 0.04)
- brand regs: below avg by 28% (current: 77.00, avg: 106.71)
- nb regs: below avg by 28% (current: 91.00, avg: 125.57)
- nb cvr: below avg by 28% (current: 0.02, avg: 0.03)

## This year weekly trend (last 12 weeks)
<!-- Data: market_trend("AU", weeks=12) -->

## Detected streaks
- CPA rising 3 consecutive weeks ($115 in W12 to $154 in W15)
- Regs declining 3 consecutive weeks (244 in W12 to 168 in W15)

## Daily breakdown
<!-- Data: db("SELECT * FROM daily_metrics WHERE market='AU' AND week='2026 W15' ORDER BY date") -->
