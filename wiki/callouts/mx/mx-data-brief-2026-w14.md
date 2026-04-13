---
title: "MX W14 Data Brief"
status: FINAL
audience: amazon-internal
owner: Richard Williams
created: 2026-04-12
updated: 2026-04-12
---

# MX W14 Data Brief

## Headline numbers
- Registrations: 238 (-33% WoW)
- Spend: $19K (-16% WoW)
- CPA: $82 (+24% WoW)
- Brand regs: 137 (-36% WoW)
- NB regs: 101 (-28% WoW)

## ie%CCP
- This week: 126%
- Last week: 99%
- Target: 100%

## Registration drivers (what caused the WoW change?)
Primary driver: CVR (-28% WoW) more than clicks (-6% WoW)

Brand:
  Regs: 137 vs 213 LW (-36%)
  CVR: 4.37% vs 5.76% (-24%)
  Clicks: 3132 vs 3699 (-15%)
  CPA: $24 vs $21 (+16%)

Non-Brand:
  Regs: 101 vs 140 LW (-28%)
  CVR: 1.08% vs 1.46% (-26%)
  Clicks: 9349 vs 9618 (-3%)
  CPA: $159 vs $134 (+19%)

## 8-week trend
<!-- Data: market_trend("MX", weeks=8) -->

## YoY comparison
- Regs: 238 TY vs 192 LY (+24%)
- Spend: $19K TY vs $32K LY (-40%)
- Brand regs: +65% YoY
- NB regs: -7% YoY
- NB CPA: $159 vs $291 LY (-45%)
- WoW pattern: TY -33% vs LY +4% (same week)

## Monthly projection inputs
- Month: 2026 Mar (31/31 days elapsed, 0 remaining)
- MTD actuals: $96K spend, 1483 regs (920 Brand, 563 NB)
- Simple linear projection (ingester estimate, not accounting for seasonality/holidays): $96K spend, 1.5K regs, $64 CPA
- NOTE: Analyst should produce the actual projection accounting for weekday/weekend mix, holidays, LY patterns, and known upcoming changes.

## Anomalies (>20% deviation from recent avg)
- regs: below avg by 26% (current: 238.00, avg: 320.43)
- cpa: above avg by 31% (current: 81.59, avg: 62.41)
- cvr: below avg by 28% (current: 0.02, avg: 0.03)
- brand regs: below avg by 34% (current: 137.00, avg: 207.86)
- brand cvr: below avg by 25% (current: 0.04, avg: 0.06)

## This year weekly trend (last 12 weeks)
<!-- Data: market_trend("MX", weeks=12) -->

## Last year same period (W10 to W18)
<!-- Data: db("SELECT * FROM weekly_metrics WHERE market='MX' AND week LIKE '2025%' ORDER BY week") -->

## Detected streaks
- CPA rising 3 consecutive weeks ($58 in W11 to $82 in W14)

## Daily breakdown
<!-- Data: db("SELECT * FROM daily_metrics WHERE market='MX' AND week='2026 W14' ORDER BY date") -->
⚠️ DATA LAG: last 2 days avg 6 regs vs weekday avg 45
