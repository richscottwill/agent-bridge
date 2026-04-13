---
title: "UK W14 Data Brief"
status: FINAL
audience: amazon-internal
owner: Richard Williams
created: 2026-04-12
updated: 2026-04-12
---

# UK W14 Data Brief

## Headline numbers
- Registrations: 1482 (-1% WoW)
- Spend: $85K (flat WoW)
- CPA: $58 (flat WoW)
- Brand regs: 489 (-11% WoW)
- NB regs: 993 (+5% WoW)

## ie%CCP
- This week: 48%
- Last week: 46%
- Target: 100%

## Registration drivers (what caused the WoW change?)
Primary driver: clicks (-8% WoW) more than CVR (+8% WoW)

Brand:
  Regs: 489 vs 548 LW (-11%)
  CVR: 3.46% vs 3.20% (+8%)
  Clicks: 14153 vs 17114 (-17%)
  CPA: $63 vs $63 (flat)

Non-Brand:
  Regs: 993 vs 945 LW (+5%)
  CVR: 5.28% vs 5.07% (+4%)
  Clicks: 18805 vs 18648 (+1%)
  CPA: $55 vs $54 (+1%)

## 8-week trend
<!-- Data: market_trend("UK", weeks=8) -->

## YoY comparison
- Regs: 1482 TY vs 694 LY (+114%)
- Spend: $85K TY vs $48K LY (+78%)
- Brand regs: +14% YoY
- NB regs: +276% YoY
- NB CPA: $55 vs $75 LY (-26%)
- WoW pattern: TY -1% vs LY -1% (same week)

## Monthly projection inputs
- Month: 2026 Mar (31/31 days elapsed, 0 remaining)
- MTD actuals: $397K spend, 6225 regs (2251 Brand, 3974 NB)
- Simple linear projection (ingester estimate, not accounting for seasonality/holidays): $397K spend, 6.2K regs, $64 CPA
- NOTE: Analyst should produce the actual projection accounting for weekday/weekend mix, holidays, LY patterns, and known upcoming changes.

## This year weekly trend (last 12 weeks)
<!-- Data: market_trend("UK", weeks=12) -->

## Last year same period (W10 to W18)
<!-- Data: db("SELECT * FROM weekly_metrics WHERE market='UK' AND week LIKE '2025%' ORDER BY week") -->

## Daily breakdown
<!-- Data: db("SELECT * FROM daily_metrics WHERE market='UK' AND week='2026 W14' ORDER BY date") -->
