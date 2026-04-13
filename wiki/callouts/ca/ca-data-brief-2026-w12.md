---
title: "CA W12 Data Brief"
status: FINAL
audience: amazon-internal
owner: Richard Williams
created: 2026-04-12
updated: 2026-04-12
---
<!-- DOC-0019 | duck_id: callout-ca-data-brief-2026-w12 -->

# CA W12 Data Brief

## Headline numbers
- Registrations: 698 (-7% WoW)
- Spend: $53K (+1% WoW)
- CPA: $76 (+9% WoW)
- Brand regs: 468 (-11% WoW)
- NB regs: 230 (+2% WoW)

## ie%CCP
- This week: 50%
- Last week: 44%
- Target: 100%

## Registration drivers (what caused the WoW change?)
Primary driver: CVR (-6% WoW) more than clicks (-2% WoW)

Brand:
  Regs: 468 vs 527 LW (-11%)
  CVR: 3.51% vs 3.71% (-5%)
  Clicks: 13315 vs 14197 (-6%)
  CPA: $54 vs $48 (+12%)

Non-Brand:
  Regs: 230 vs 226 LW (+2%)
  CVR: 1.74% vs 1.77% (-2%)
  Clicks: 13247 vs 12786 (+4%)
  CPA: $121 vs $119 (+1%)

## 8-week trend
<!-- Data: market_trend("CA", weeks=8) -->

## YoY comparison
- Regs: 698 TY vs 455 LY (+53%)
- Spend: $53K TY vs $46K LY (+15%)
- Brand regs: +47% YoY
- NB regs: +69% YoY
- NB CPA: $121 vs $224 LY (-46%)
- WoW pattern: TY -7% vs LY -11% (same week)

## Monthly projection inputs
- Month: 2026 Mar (21/31 days elapsed, 10 remaining)
- MTD actuals: $155K spend, 2095 regs (1406 Brand, 689 NB)
- OP2 targets: $228K spend, 2.6K regs
- OP2 pace check: at 68% through the month, linear OP2 pace would be 1.8K regs and $155K spend
- MTD vs OP2 pace: +19% regs, flat spend
- Simple linear projection (ingester estimate, not accounting for seasonality/holidays): $231K spend, 3.1K regs, $75 CPA
- NOTE: Analyst should produce the actual projection accounting for weekday/weekend mix, holidays, LY patterns, and known upcoming changes.

## This year weekly trend (last 12 weeks)
<!-- Data: market_trend("CA", weeks=12) -->

## Last year same period (W8 to W16)
<!-- Data: db("SELECT * FROM weekly_metrics WHERE market='CA' AND week LIKE '2025%' ORDER BY week") -->

## Daily breakdown
<!-- Data: db("SELECT * FROM daily_metrics WHERE market='CA' AND week='2026 W12' ORDER BY date") -->
