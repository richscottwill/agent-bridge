# IT W18 Data Brief

## Headline numbers
- Registrations: 1183 (+2% WoW)
- Spend: $88K (+7% WoW)
- CPA: $74 (+6% WoW)
- Brand regs: 749 (-7% WoW)
- NB regs: 434 (+20% WoW)

## ie%CCP
- This week: 57%
- Last week: 52%
- Target: 100%

## Registration drivers (what caused the WoW change?)
Primary driver: clicks (+6% WoW) more than CVR (-4% WoW)

Brand:
  Regs: 749 vs 803 LW (-7%)
  CVR: 2.78% vs 3.01% (-8%)
  Clicks: 26905 vs 26660 (+1%)
  CPA: $37 vs $41 (-9%)

Non-Brand:
  Regs: 434 vs 362 LW (+20%)
  CVR: 2.28% vs 2.17% (+5%)
  Clicks: 19048 vs 16699 (+14%)
  CPA: $138 vs $135 (+2%)

## 8-week trend
<!-- Data: market_trend("IT", weeks=8) -->

## YoY comparison
- Regs: 1183 TY vs 964 LY (+23%)
- Spend: $88K TY vs $78K LY (+12%)
- Brand regs: +18% YoY
- NB regs: +33% YoY
- NB CPA: $138 vs $148 LY (-7%)
- WoW pattern: TY +2% vs LY +19% (same week)

## Monthly projection inputs
- Month: 2026 Apr (30/30 days elapsed, 0 remaining)
- MTD actuals: $400K spend, 5051 regs (3393 Brand, 1658 NB)
- OP2 targets: $351K spend, 5.0K regs
- OP2 pace check: at 100% through the month, linear OP2 pace would be 5.0K regs and $351K spend
- MTD vs OP2 pace: flat regs, +14% spend
- Simple linear projection (ingester estimate, not accounting for seasonality/holidays): $400K spend, 5.1K regs, $79 CPA
- NOTE: Analyst should produce the actual projection accounting for weekday/weekend mix, holidays, LY patterns, and known upcoming changes.

## Anomalies (>20% deviation from recent avg)
- nb cvr: above avg by 21% (current: 0.02, avg: 0.02)

## This year weekly trend (last 12 weeks)
<!-- Data: market_trend("IT", weeks=12) -->

## Last year same period (W14 to W22)
<!-- Data: db("SELECT * FROM weekly_metrics WHERE market='IT' AND week LIKE '2025%' ORDER BY week") -->

## Detected streaks
- Regs rising 3 consecutive weeks (965 in W15 to 1183 in W18)

## Daily breakdown
<!-- Data: db("SELECT * FROM daily_metrics WHERE market='IT' AND week='2026 W18' ORDER BY date") -->
