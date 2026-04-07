<!-- DOC-0068 | duck_id: callout-jp-data-brief-2026-w13 -->
# JP W13 Data Brief

## Headline numbers
- Registrations: 557 (+29% WoW)
- Spend: $47K (+30% WoW)
- CPA: $85 (+1% WoW)
- Brand regs: 549 (+28% WoW)
- NB regs: 8 (+167% WoW)

## ie%CCP
- This week: 8520%
- Last week: 8455%
- Target: 100%

## Registration drivers (what caused the WoW change?)
Primary driver: CVR (+17% WoW) more than clicks (+11% WoW)

Brand:
  Regs: 549 vs 429 LW (+28%)
  CVR: 2.24% vs 1.97% (+14%)
  Clicks: 24468 vs 21786 (+12%)
  CPA: $61 vs $70 (-13%)

Non-Brand:
  Regs: 8 vs 3 LW (+167%)
  CVR: 0.27% vs 0.10% (+172%)
  Clicks: 2961 vs 3015 (-2%)
  CPA: $1,754 vs $2,189 (-20%)

## 8-week trend
<!-- Data: market_trend("JP", weeks=8) -->

## YoY comparison
- Regs: 557 TY vs 386 LY (+44%)
- Spend: $47K TY vs $28K LY (+67%)
- Brand regs: +44% YoY
- NB regs: +60% YoY
- NB CPA: $1,754 vs $495 LY (+255%)
- WoW pattern: TY +29% vs LY -10% (same week)

## Monthly projection inputs
- Month: 2026 Mar (28/31 days elapsed, 3 remaining)
- MTD actuals: $162K spend, 2035 regs (2018 Brand, 17 NB)
- Simple linear projection (ingester estimate, not accounting for seasonality/holidays): $182K spend, 2.3K regs, $80 CPA
- NOTE: Analyst should produce the actual projection accounting for weekday/weekend mix, holidays, LY patterns, and known upcoming changes.

## Anomalies (>20% deviation from recent avg)
- cost: above avg by 41% (current: 47457.31, avg: 33585.97)
- cpc: above avg by 26% (current: 1.73, avg: 1.37)

## This year weekly trend (last 12 weeks)
<!-- Data: market_trend("JP", weeks=12) -->

## Last year same period (W9 to W17)
<!-- Data: db("SELECT * FROM weekly_metrics WHERE market='JP' AND week LIKE '2025%' ORDER BY week") -->

## Detected streaks
- NB CPC rising 3 consecutive weeks ($1.65 in W10 to $4.74 in W13)

## Daily breakdown
<!-- Data: db("SELECT * FROM daily_metrics WHERE market='JP' AND week='2026 W13' ORDER BY date") -->
