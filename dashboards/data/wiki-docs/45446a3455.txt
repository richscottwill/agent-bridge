# MX W15 Data Brief

## Headline numbers
- Registrations: 515 (+69% WoW)
- Spend: $25K (+31% WoW)
- CPA: $49 (-23% WoW)
- Brand regs: 373 (+107% WoW)
- NB regs: 142 (+15% WoW)

## ie%CCP
- This week: 67%
- Last week: 97%
- Target: 100%

## Registration drivers (what caused the WoW change?)
Primary driver: CVR (+38% WoW) more than clicks (+23% WoW)

Brand:
  Regs: 373 vs 180 LW (+107%)
  CVR: 8.08% vs 5.75% (+41%)
  Clicks: 4614 vs 3132 (+47%)
  CPA: $14 vs $18 (-23%)

Non-Brand:
  Regs: 142 vs 124 LW (+15%)
  CVR: 1.32% vs 1.33% (flat)
  Clicks: 10752 vs 9349 (+15%)
  CPA: $142 vs $130 (+9%)

## 8-week trend
<!-- Data: market_trend("MX", weeks=8) -->

## YoY comparison
- Regs: 515 TY vs 154 LY (+234%)
- Spend: $25K TY vs $31K LY (-17%)
- Brand regs: +404% YoY
- NB regs: +78% YoY
- NB CPA: $142 vs $377 LY (-62%)
- WoW pattern: TY +69% vs LY -20% (same week)

## Monthly projection inputs
- Month: 2026 Apr (11/30 days elapsed, 19 remaining)
- MTD actuals: $36K spend, 702 regs (493 Brand, 209 NB)
- OP2 targets: $35K spend, 791.2857142857142 regs
- OP2 pace check: at 37% through the month, linear OP2 pace would be 290 regs and $13K spend
- MTD vs OP2 pace: +142% regs, +177% spend
- Simple linear projection (ingester estimate, not accounting for seasonality/holidays): $105K spend, 2.1K regs, $50 CPA
- NOTE: Analyst should produce the actual projection accounting for weekday/weekend mix, holidays, LY patterns, and known upcoming changes.

## Anomalies (>20% deviation from recent avg)
- regs: above avg by 57% (current: 515.00, avg: 327.86)
- cost: above avg by 24% (current: 25444.34, avg: 20591.83)
- cpa: below avg by 22% (current: 49.41, avg: 63.58)
- cvr: above avg by 28% (current: 0.03, avg: 0.03)
- brand regs: above avg by 77% (current: 373.00, avg: 210.29)
- nb regs: above avg by 21% (current: 142.00, avg: 117.57)
- brand cvr: above avg by 36% (current: 0.08, avg: 0.06)

## This year weekly trend (last 12 weeks)
<!-- Data: market_trend("MX", weeks=12) -->

## Last year same period (W11 to W19)
<!-- Data: db("SELECT * FROM weekly_metrics WHERE market='MX' AND week LIKE '2025%' ORDER BY week") -->

## Daily breakdown
<!-- Data: db("SELECT * FROM daily_metrics WHERE market='MX' AND week='2026 W15' ORDER BY date") -->
