# ES W17 Data Brief

## Headline numbers
- Registrations: 578 (-5% WoW)
- Spend: $31K (-20% WoW)
- CPA: $53 (-16% WoW)
- Brand regs: 361 (+1% WoW)
- NB regs: 217 (-13% WoW)

## ie%CCP
- This week: 43%
- Last week: 52%
- Target: 100%

## Registration drivers (what caused the WoW change?)
Primary driver: clicks (-16% WoW) more than CVR (+13% WoW)

Brand:
  Regs: 361 vs 359 LW (+1%)
  CVR: 3.05% vs 2.60% (+18%)
  Clicks: 11823 vs 13820 (-14%)
  CPA: $32 vs $40 (-20%)

Non-Brand:
  Regs: 217 vs 249 LW (-13%)
  CVR: 2.41% vs 2.28% (+6%)
  Clicks: 9020 vs 10943 (-18%)
  CPA: $87 vs $95 (-8%)

## 8-week trend
<!-- Data: market_trend("ES", weeks=8) -->

## YoY comparison
- Regs: 578 TY vs 488 LY (+18%)
- Spend: $31K TY vs $28K LY (+9%)
- Brand regs: +54% YoY
- NB regs: -14% YoY
- NB CPA: $87 vs $84 LY (+5%)
- WoW pattern: TY -5% vs LY +8% (same week)

## Monthly projection inputs
- Month: 2026 Apr (25/30 days elapsed, 5 remaining)
- MTD actuals: $124K spend, 2010 regs (1209 Brand, 801 NB)
- OP2 targets: $108K spend, 2.0K regs
- OP2 pace check: at 83% through the month, linear OP2 pace would be 1.6K regs and $90K spend
- MTD vs OP2 pace: +23% regs, +37% spend
- Simple linear projection (ingester estimate, not accounting for seasonality/holidays): $146K spend, 2.4K regs, $60 CPA
- NOTE: Analyst should produce the actual projection accounting for weekday/weekend mix, holidays, LY patterns, and known upcoming changes.

## This year weekly trend (last 12 weeks)
<!-- Data: market_trend("ES", weeks=12) -->

## Last year same period (W13 to W21)
<!-- Data: db("SELECT * FROM weekly_metrics WHERE market='ES' AND week LIKE '2025%' ORDER BY week") -->

## Daily breakdown
<!-- Data: db("SELECT * FROM daily_metrics WHERE market='ES' AND week='2026 W17' ORDER BY date") -->
