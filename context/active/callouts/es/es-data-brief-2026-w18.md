# ES W18 Data Brief

## Headline numbers
- Registrations: 575 (+1% WoW)
- Spend: $33K (+9% WoW)
- CPA: $58 (+8% WoW)
- Brand regs: 358 (flat WoW)
- NB regs: 217 (+1% WoW)

## ie%CCP
- This week: 47%
- Last week: 43%
- Target: 100%

## Registration drivers (what caused the WoW change?)
Primary driver: CVR (+10% WoW) more than clicks (-9% WoW)

Brand:
  Regs: 358 vs 357 LW (flat)
  CVR: 3.19% vs 3.02% (+6%)
  Clicks: 11221 vs 11823 (-5%)
  CPA: $40 vs $33 (+23%)

Non-Brand:
  Regs: 217 vs 214 LW (+1%)
  CVR: 2.78% vs 2.37% (+17%)
  Clicks: 7816 vs 9020 (-13%)
  CPA: $88 vs $89 (-1%)

## 8-week trend
<!-- Data: market_trend("ES", weeks=8) -->

## YoY comparison
- Regs: 575 TY vs 362 LY (+59%)
- Spend: $33K TY vs $23K LY (+42%)
- Brand regs: +91% YoY
- NB regs: +24% YoY
- NB CPA: $88 vs $103 LY (-14%)
- WoW pattern: TY +1% vs LY -26% (same week)

## Monthly projection inputs
- Month: 2026 Apr (30/30 days elapsed, 0 remaining)
- MTD actuals: $150K spend, 2483 regs (1502 Brand, 981 NB)
- OP2 targets: $108K spend, 2.0K regs
- OP2 pace check: at 100% through the month, linear OP2 pace would be 2.0K regs and $108K spend
- MTD vs OP2 pace: +26% regs, +39% spend
- Simple linear projection (ingester estimate, not accounting for seasonality/holidays): $150K spend, 2.5K regs, $61 CPA
- NOTE: Analyst should produce the actual projection accounting for weekday/weekend mix, holidays, LY patterns, and known upcoming changes.

## Anomalies (>20% deviation from recent avg)
- cvr: above avg by 23% (current: 0.03, avg: 0.02)
- nb cvr: above avg by 29% (current: 0.03, avg: 0.02)
- cpc: above avg by 20% (current: 1.75, avg: 1.46)

## This year weekly trend (last 12 weeks)
<!-- Data: market_trend("ES", weeks=12) -->

## Last year same period (W14 to W22)
<!-- Data: db("SELECT * FROM weekly_metrics WHERE market='ES' AND week LIKE '2025%' ORDER BY week") -->

## Daily breakdown
<!-- Data: db("SELECT * FROM daily_metrics WHERE market='ES' AND week='2026 W18' ORDER BY date") -->
