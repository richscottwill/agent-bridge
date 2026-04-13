# DE W15 Data Brief

## Headline numbers
- Registrations: 1210 (-8% WoW)
- Spend: $113K (+10% WoW)
- CPA: $93 (+20% WoW)
- Brand regs: 650 (-17% WoW)
- NB regs: 560 (+4% WoW)

## ie%CCP
- This week: 50%
- Last week: 40%
- Target: 100%

## Registration drivers (what caused the WoW change?)
Primary driver: CVR (-12% WoW) more than clicks (+5% WoW)

Brand:
  Regs: 650 vs 779 LW (-17%)
  CVR: 3.03% vs 3.31% (-8%)
  Clicks: 21420 vs 23501 (-9%)
  CPA: $61 vs $52 (+17%)

Non-Brand:
  Regs: 560 vs 536 LW (+4%)
  CVR: 2.96% vs 3.60% (-18%)
  Clicks: 18908 vs 14882 (+27%)
  CPA: $130 vs $115 (+13%)

## 8-week trend
<!-- Data: market_trend("DE", weeks=8) -->

## YoY comparison
- Regs: 1210 TY vs 1170 LY (+3%)
- Spend: $113K TY vs $142K LY (-21%)
- Brand regs: +2% YoY
- NB regs: +5% YoY
- NB CPA: $130 vs $175 LY (-25%)
- WoW pattern: TY -8% vs LY -6% (same week)

## Monthly projection inputs
- Month: 2026 Apr (11/30 days elapsed, 19 remaining)
- MTD actuals: $168K spend, 1879 regs (1036 Brand, 843 NB)
- OP2 targets: $687K spend, 5.7K regs
- OP2 pace check: at 37% through the month, linear OP2 pace would be 2.1K regs and $252K spend
- MTD vs OP2 pace: -11% regs, -33% spend
- Simple linear projection (ingester estimate, not accounting for seasonality/holidays): $473K spend, 5.2K regs, $92 CPA
- NOTE: Analyst should produce the actual projection accounting for weekday/weekend mix, holidays, LY patterns, and known upcoming changes.

## Anomalies (>20% deviation from recent avg)
- cost: below avg by 24% (current: 112633.98, avg: 147471.79)
- cpa: below avg by 23% (current: 93.09, avg: 121.36)

## This year weekly trend (last 12 weeks)
<!-- Data: market_trend("DE", weeks=12) -->

## Last year same period (W11 to W19)
<!-- Data: db("SELECT * FROM weekly_metrics WHERE market='DE' AND week LIKE '2025%' ORDER BY week") -->

## Daily breakdown
<!-- Data: db("SELECT * FROM daily_metrics WHERE market='DE' AND week='2026 W15' ORDER BY date") -->
