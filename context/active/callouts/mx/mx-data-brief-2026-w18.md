# MX W18 Data Brief

## Headline numbers
- Registrations: 669 (+24% WoW)
- Spend: $24K (-7% WoW)
- CPA: $36 (-25% WoW)
- Brand regs: 515 (+27% WoW)
- NB regs: 154 (+15% WoW)

## ie%CCP
- This week: 44%
- Last week: 59%
- Target: 100%

## Registration drivers (what caused the WoW change?)
Primary driver: CVR (+26% WoW) more than clicks (-2% WoW)

Brand:
  Regs: 515 vs 405 LW (+27%)
  CVR: 9.34% vs 8.38% (+12%)
  Clicks: 5511 vs 4834 (+14%)
  CPA: $10 vs $14 (-25%)

Non-Brand:
  Regs: 154 vs 134 LW (+15%)
  CVR: 1.70% vs 1.35% (+27%)
  Clicks: 9033 vs 9954 (-9%)
  CPA: $120 vs $148 (-19%)

## 8-week trend
<!-- Data: market_trend("MX", weeks=8) -->

## YoY comparison
- Regs: 669 TY vs 148 LY (+352%)
- Spend: $24K TY vs $27K LY (-10%)
- Brand regs: +625% YoY
- NB regs: +100% YoY
- NB CPA: $120 vs $326 LY (-63%)
- WoW pattern: TY +24% vs LY -23% (same week)

## Monthly projection inputs
- Month: 2026 Apr (30/30 days elapsed, 0 remaining)
- MTD actuals: $107K spend, 2244 regs (1674 Brand, 570 NB)
- OP2 targets: $35K spend, 791.2857142857142 regs
- OP2 pace check: at 100% through the month, linear OP2 pace would be 791 regs and $35K spend
- MTD vs OP2 pace: +184% regs, +205% spend
- Simple linear projection (ingester estimate, not accounting for seasonality/holidays): $107K spend, 2.2K regs, $48 CPA
- NOTE: Analyst should produce the actual projection accounting for weekday/weekend mix, holidays, LY patterns, and known upcoming changes.

## Anomalies (>20% deviation from recent avg)
- regs: above avg by 61% (current: 669.00, avg: 415.86)
- cpa: below avg by 38% (current: 35.61, avg: 57.56)
- cvr: above avg by 54% (current: 0.05, avg: 0.03)
- brand regs: above avg by 81% (current: 515.00, avg: 284.29)
- brand cvr: above avg by 36% (current: 0.09, avg: 0.07)
- nb cvr: above avg by 26% (current: 0.02, avg: 0.01)

## This year weekly trend (last 12 weeks)
<!-- Data: market_trend("MX", weeks=12) -->

## Last year same period (W14 to W22)
<!-- Data: db("SELECT * FROM weekly_metrics WHERE market='MX' AND week LIKE '2025%' ORDER BY week") -->

## Detected streaks
- Regs rising 4 consecutive weeks (302 in W14 to 669 in W18)

## Daily breakdown
<!-- Data: db("SELECT * FROM daily_metrics WHERE market='MX' AND week='2026 W18' ORDER BY date") -->
