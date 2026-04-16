# DE W15 Data Brief

## Headline numbers
- Registrations: 1212 (-7% WoW)
- Spend: $113K (+10% WoW)
- CPA: $93 (+18% WoW)
- Brand regs: 651 (-15% WoW)
- NB regs: 561 (+5% WoW)

## ie%CCP
- This week: 50%
- Last week: 41%
- Target: 100%

## Registration drivers (what caused the WoW change?)
Primary driver: CVR (-11% WoW) more than clicks (+5% WoW)

Brand:
  Regs: 651 vs 766 LW (-15%)
  CVR: 3.04% vs 3.26% (-7%)
  Clicks: 21420 vs 23501 (-9%)
  CPA: $61 vs $53 (+14%)

Non-Brand:
  Regs: 561 vs 536 LW (+5%)
  CVR: 2.97% vs 3.60% (-18%)
  Clicks: 18908 vs 14882 (+27%)
  CPA: $130 vs $115 (+13%)

## 8-week trend
<!-- Data: market_trend("DE", weeks=8) -->

## YoY comparison
- Regs: 1212 TY vs 1169 LY (+4%)
- Spend: $113K TY vs $142K LY (-21%)
- Brand regs: +2% YoY
- NB regs: +5% YoY
- NB CPA: $130 vs $175 LY (-26%)
- WoW pattern: TY -7% vs LY -6% (same week)

## Monthly projection inputs
- Month: 2026 Apr (11/30 days elapsed, 19 remaining)
- MTD actuals: $168K spend, 1870 regs (1026 Brand, 844 NB)
- OP2 targets: $606K spend, 5.7K regs
- OP2 pace check: at 37% through the month, linear OP2 pace would be 2.1K regs and $222K spend
- MTD vs OP2 pace: -11% regs, -24% spend
- Simple linear projection (ingester estimate, not accounting for seasonality/holidays): $473K spend, 5.2K regs, $92 CPA
- NOTE: Analyst should produce the actual projection accounting for weekday/weekend mix, holidays, LY patterns, and known upcoming changes.

## Anomalies (>20% deviation from recent avg)
- cost: below avg by 24% (current: 112633.98, avg: 147471.79)
- cpa: below avg by 24% (current: 92.93, avg: 121.83)
- nb cvr: above avg by 20% (current: 0.03, avg: 0.02)

## This year weekly trend (last 12 weeks)
<!-- Data: market_trend("DE", weeks=12) -->

## Last year same period (W11 to W19)
<!-- Data: db("SELECT * FROM weekly_metrics WHERE market='DE' AND week LIKE '2025%' ORDER BY week") -->

## Daily breakdown
<!-- Data: db("SELECT * FROM daily_metrics WHERE market='DE' AND week='2026 W15' ORDER BY date") -->
