---
title: "JP W14 Data Brief"
status: FINAL
audience: amazon-internal
owner: Richard Williams
created: 2026-04-12
updated: 2026-04-12
---

# JP W14 Data Brief

## Headline numbers
- Registrations: 613 (+12% WoW)
- Spend: $46K (-4% WoW)
- CPA: $75 (-14% WoW)
- Brand regs: 606 (+12% WoW)
- NB regs: 7 (-12% WoW)

## ie%CCP
- This week: 39%
- Last week: 45%
- Target: 100%

## Registration drivers (what caused the WoW change?)
Primary driver: CVR (+13% WoW) more than clicks (-1% WoW)

Brand:
  Regs: 606 vs 540 LW (+12%)
  CVR: 2.42% vs 2.21% (+10%)
  Clicks: 25046 vs 24468 (+2%)
  CPA: $58 vs $62 (-6%)

Non-Brand:
  Regs: 7 vs 8 LW (-12%)
  CVR: 0.33% vs 0.27% (+22%)
  Clicks: 2116 vs 2961 (-29%)
  CPA: $1,519 vs $1,754 (-13%)

## 8-week trend
<!-- Data: market_trend("JP", weeks=8) -->

## YoY comparison
- Regs: 613 TY vs 498 LY (+23%)
- Spend: $46K TY vs $30K LY (+53%)
- Brand regs: +22% YoY
- NB regs: +600% YoY
- NB CPA: $1,519 vs $2,805 LY (-46%)
- WoW pattern: TY +12% vs LY +29% (same week)

## Monthly projection inputs
- Month: 2026 Mar (31/31 days elapsed, 0 remaining)
- MTD actuals: $183K spend, 2252 regs (2230 Brand, 22 NB)
- Simple linear projection (ingester estimate, not accounting for seasonality/holidays): $183K spend, 2.3K regs, $81 CPA
- NOTE: Analyst should produce the actual projection accounting for weekday/weekend mix, holidays, LY patterns, and known upcoming changes.

## Anomalies (>20% deviation from recent avg)
- regs: above avg by 30% (current: 613.00, avg: 470.71)
- cost: above avg by 28% (current: 45775.61, avg: 35660.89)
- brand regs: above avg by 29% (current: 606.00, avg: 468.29)
- brand cvr: above avg by 21% (current: 0.02, avg: 0.02)

## This year weekly trend (last 12 weeks)
<!-- Data: market_trend("JP", weeks=12) -->

## Last year same period (W10 to W18)
<!-- Data: db("SELECT * FROM weekly_metrics WHERE market='JP' AND week LIKE '2025%' ORDER BY week") -->

## Detected streaks
- NB CPC rising 4 consecutive weeks ($1.65 in W10 to $5.02 in W14)

## Daily breakdown
<!-- Data: db("SELECT * FROM daily_metrics WHERE market='JP' AND week='2026 W14' ORDER BY date") -->
