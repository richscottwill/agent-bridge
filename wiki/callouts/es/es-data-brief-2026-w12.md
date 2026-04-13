---
title: "ES W12 Data Brief"
status: FINAL
audience: amazon-internal
owner: Richard Williams
created: 2026-04-12
updated: 2026-04-12
---
<!-- DOC-0038 | duck_id: callout-es-data-brief-2026-w12 -->

# ES W12 Data Brief

## Headline numbers
- Registrations: 657 (-8% WoW)
- Spend: $33K (-19% WoW)
- CPA: $50 (-12% WoW)
- Brand regs: 405 (-8% WoW)
- NB regs: 252 (-9% WoW)

## ie%CCP
- This week: 47%
- Last week: 53%
- Target: 100%

## Registration drivers (what caused the WoW change?)
Primary driver: clicks (-10% WoW) more than CVR (+2% WoW)

Brand:
  Regs: 405 vs 438 LW (-8%)
  CVR: 3.01% vs 2.84% (+6%)
  Clicks: 13472 vs 15429 (-13%)
  CPA: $28 vs $34 (-19%)

Non-Brand:
  Regs: 252 vs 276 LW (-9%)
  CVR: 2.27% vs 2.33% (-2%)
  Clicks: 11094 vs 11870 (-7%)
  CPA: $85 vs $92 (-7%)

## 8-week trend
<!-- Data: market_trend("ES", weeks=8) -->

## YoY comparison
- Regs: 657 TY vs 548 LY (+20%)
- Spend: $33K TY vs $23K LY (+42%)
- Brand regs: +38% YoY
- NB regs: -1% YoY
- NB CPA: $85 vs $60 LY (+42%)
- WoW pattern: TY -8% vs LY -12% (same week)

## Monthly projection inputs
- Month: 2026 Mar (21/31 days elapsed, 10 remaining)
- MTD actuals: $116K spend, 2012 regs (1230 Brand, 782 NB)
- OP2 targets: $127K spend, 2.4K regs
- OP2 pace check: at 68% through the month, linear OP2 pace would be 1.6K regs and $86K spend
- MTD vs OP2 pace: +24% regs, +35% spend
- Simple linear projection (ingester estimate, not accounting for seasonality/holidays): $163K spend, 3.0K regs, $55 CPA
- NOTE: Analyst should produce the actual projection accounting for weekday/weekend mix, holidays, LY patterns, and known upcoming changes.

## This year weekly trend (last 12 weeks)
<!-- Data: market_trend("ES", weeks=12) -->

## Last year same period (W8 to W16)
<!-- Data: db("SELECT * FROM weekly_metrics WHERE market='ES' AND week LIKE '2025%' ORDER BY week") -->

## Detected streaks
- NB CPC declining 3 consecutive weeks ($2.34 in W9 to $1.93 in W12)

## Daily breakdown
<!-- Data: db("SELECT * FROM daily_metrics WHERE market='ES' AND week='2026 W12' ORDER BY date") -->
