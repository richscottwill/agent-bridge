---
title: "CA W14 Data Brief"
status: FINAL
audience: amazon-internal
owner: Richard Williams
created: 2026-04-12
updated: 2026-04-12
---

# CA W14 Data Brief

## Headline numbers
- Registrations: 643 (-18% WoW)
- Spend: $51K (-2% WoW)
- CPA: $79 (+19% WoW)
- Brand regs: 409 (-24% WoW)
- NB regs: 234 (-5% WoW)

## ie%CCP
- This week: 54%
- Last week: 43%
- Target: 100%

## Registration drivers (what caused the WoW change?)
Primary driver: CVR (-15% WoW) more than clicks (-3% WoW)

Brand:
  Regs: 409 vs 536 LW (-24%)
  CVR: 3.17% vs 3.81% (-17%)
  Clicks: 12906 vs 14061 (-8%)
  CPA: $55 vs $45 (+22%)

Non-Brand:
  Regs: 234 vs 246 LW (-5%)
  CVR: 1.72% vs 1.84% (-7%)
  Clicks: 13633 vs 13359 (+2%)
  CPA: $121 vs $114 (+7%)

## 8-week trend
<!-- Data: market_trend("CA", weeks=8) -->

## YoY comparison
- Regs: 643 TY vs 469 LY (+37%)
- Spend: $51K TY vs $52K LY (-2%)
- Brand regs: +19% YoY
- NB regs: +86% YoY
- NB CPA: $121 vs $289 LY (-58%)
- WoW pattern: TY -18% vs LY +2% (same week)

## Monthly projection inputs
- Month: 2026 Mar (31/31 days elapsed, 0 remaining)
- MTD actuals: $229K spend, 3228 regs (2156 Brand, 1072 NB)
- Simple linear projection (ingester estimate, not accounting for seasonality/holidays): $229K spend, 3.2K regs, $71 CPA
- NOTE: Analyst should produce the actual projection accounting for weekday/weekend mix, holidays, LY patterns, and known upcoming changes.

## This year weekly trend (last 12 weeks)
<!-- Data: market_trend("CA", weeks=12) -->

## Last year same period (W10 to W18)
<!-- Data: db("SELECT * FROM weekly_metrics WHERE market='CA' AND week LIKE '2025%' ORDER BY week") -->

## Daily breakdown
<!-- Data: db("SELECT * FROM daily_metrics WHERE market='CA' AND week='2026 W14' ORDER BY date") -->
⚠️ DATA LAG: last 2 days avg 7 regs vs weekday avg 126
