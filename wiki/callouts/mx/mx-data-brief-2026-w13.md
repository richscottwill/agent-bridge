---
title: "MX W13 Data Brief"
status: FINAL
audience: amazon-internal
owner: Richard Williams
created: 2026-04-12
updated: 2026-04-12
---
<!-- DOC-0078 | duck_id: callout-mx-data-brief-2026-w13 -->

# MX W13 Data Brief

## Headline numbers
- Registrations: 354 (+9% WoW)
- Spend: $23K (+15% WoW)
- CPA: $66 (+6% WoW)
- Brand regs: 214 (+5% WoW)
- NB regs: 140 (+15% WoW)

## ie%CCP
- This week: 6559%
- Last week: 6176%
- Target: 100%

## Registration drivers (what caused the WoW change?)
Primary driver: clicks (+9% WoW) more than CVR (flat WoW)

Brand:
  Regs: 214 vs 204 LW (+5%)
  CVR: 5.79% vs 6.03% (-4%)
  Clicks: 3698 vs 3384 (+9%)
  CPA: $21 vs $20 (+3%)

Non-Brand:
  Regs: 140 vs 122 LW (+15%)
  CVR: 1.46% vs 1.38% (+5%)
  Clicks: 9618 vs 8826 (+9%)
  CPA: $134 vs $131 (+2%)

## 8-week trend
<!-- Data: market_trend("MX", weeks=8) -->

## YoY comparison
- Regs: 354 TY vs 185 LY (+91%)
- Spend: $23K TY vs $34K LY (-32%)
- Brand regs: +182% YoY
- NB regs: +28% YoY
- NB CPA: $134 vs $309 LY (-57%)
- WoW pattern: TY +9% vs LY +6% (same week)

## Monthly projection inputs
- Month: 2026 Mar (28/31 days elapsed, 3 remaining)
- MTD actuals: $86K spend, 1370 regs (863 Brand, 507 NB)
- Simple linear projection (ingester estimate, not accounting for seasonality/holidays): $96K spend, 1.5K regs, $63 CPA
- NOTE: Analyst should produce the actual projection accounting for weekday/weekend mix, holidays, LY patterns, and known upcoming changes.

## Anomalies (>20% deviation from recent avg)
- cost: above avg by 24% (current: 23219.39, avg: 18718.75)
- nb regs: above avg by 33% (current: 140.00, avg: 105.43)

## This year weekly trend (last 12 weeks)
<!-- Data: market_trend("MX", weeks=12) -->

## Last year same period (W9 to W17)
<!-- Data: db("SELECT * FROM weekly_metrics WHERE market='MX' AND week LIKE '2025%' ORDER BY week") -->

## Daily breakdown
<!-- Data: db("SELECT * FROM daily_metrics WHERE market='MX' AND week='2026 W13' ORDER BY date") -->
