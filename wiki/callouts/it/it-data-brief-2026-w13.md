---
title: "IT W13 Data Brief"
status: FINAL
audience: amazon-internal
owner: Richard Williams
created: 2026-04-12
updated: 2026-04-12
---
<!-- DOC-0059 | duck_id: callout-it-data-brief-2026-w13 -->

# IT W13 Data Brief

## Headline numbers
- Registrations: 1357 (+8% WoW)
- Spend: $97K (+25% WoW)
- CPA: $72 (+16% WoW)
- Brand regs: 930 (+2% WoW)
- NB regs: 427 (+23% WoW)

## ie%CCP
- This week: 7157%
- Last week: 6189%
- Target: 100%

## Registration drivers (what caused the WoW change?)
Primary driver: clicks (+6% WoW) more than CVR (+2% WoW)

Brand:
  Regs: 930 vs 909 LW (+2%)
  CVR: 3.03% vs 2.81% (+8%)
  Clicks: 30676 vs 32307 (-5%)
  CPA: $30 vs $33 (-9%)

Non-Brand:
  Regs: 427 vs 346 LW (+23%)
  CVR: 1.73% vs 1.73% (flat)
  Clicks: 24711 vs 20025 (+23%)
  CPA: $162 vs $137 (+18%)

## 8-week trend
<!-- Data: market_trend("IT", weeks=8) -->

## YoY comparison
- Regs: 1357 TY vs 1326 LY (+2%)
- Spend: $97K TY vs $56K LY (+73%)
- Brand regs: +7% YoY
- NB regs: -7% YoY
- NB CPA: $162 vs $56 LY (+191%)
- WoW pattern: TY +8% vs LY +8% (same week)

## Monthly projection inputs
- Month: 2026 Mar (28/31 days elapsed, 3 remaining)
- MTD actuals: $367K spend, 5208 regs (3670 Brand, 1538 NB)
- Simple linear projection (ingester estimate, not accounting for seasonality/holidays): $409K spend, 5.8K regs, $71 CPA
- NOTE: Analyst should produce the actual projection accounting for weekday/weekend mix, holidays, LY patterns, and known upcoming changes.

## This year weekly trend (last 12 weeks)
<!-- Data: market_trend("IT", weeks=12) -->

## Last year same period (W9 to W17)
<!-- Data: db("SELECT * FROM weekly_metrics WHERE market='IT' AND week LIKE '2025%' ORDER BY week") -->

## Daily breakdown
<!-- Data: db("SELECT * FROM daily_metrics WHERE market='IT' AND week='2026 W13' ORDER BY date") -->
