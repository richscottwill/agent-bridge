<!-- DOC-0011 | duck_id: callout-au-data-brief-2026-w13 -->
# AU W13 Data Brief

## Headline numbers
- Registrations: 207 (-16% WoW)
- Spend: $24K (-13% WoW)
- CPA: $118 (+3% WoW)
- Brand regs: 98 (-18% WoW)
- NB regs: 109 (-13% WoW)

## Registration drivers (what caused the WoW change?)
Primary driver: CVR (-12% WoW) more than clicks (-4% WoW)

Brand:
  Regs: 98 vs 119 LW (-18%)
  CVR: 7.37% vs 8.54% (-14%)
  Clicks: 1329 vs 1393 (-5%)
  CPA: $41 vs $37 (+10%)

Non-Brand:
  Regs: 109 vs 126 LW (-13%)
  CVR: 2.58% vs 2.87% (-10%)
  Clicks: 4228 vs 4392 (-4%)
  CPA: $187 vs $187 (flat)

## 8-week trend
<!-- Data: market_trend("AU", weeks=8) -->

## Monthly projection inputs
- Month: 2026 Mar (28/31 days elapsed, 3 remaining)
- MTD actuals: $115K spend, 944 regs (436 Brand, 508 NB)
- Simple linear projection (ingester estimate, not accounting for seasonality/holidays): $125K spend, 1.0K regs, $121 CPA
- NOTE: Analyst should produce the actual projection accounting for weekday/weekend mix, holidays, LY patterns, and known upcoming changes.

## Anomalies (>20% deviation from recent avg)
- regs: below avg by 21% (current: 207.00, avg: 262.00)
- cost: below avg by 32% (current: 24381.27, avg: 35610.43)
- nb regs: below avg by 25% (current: 109.00, avg: 146.14)
- cpc: below avg by 21% (current: 4.39, avg: 5.58)

## This year weekly trend (last 12 weeks)
<!-- Data: market_trend("AU", weeks=12) -->

## Detected streaks
- NB CPC declining 7 consecutive weeks ($6.82 in W6 to $4.81 in W13)

## Daily breakdown
<!-- Data: db("SELECT * FROM daily_metrics WHERE market='AU' AND week='2026 W13' ORDER BY date") -->
