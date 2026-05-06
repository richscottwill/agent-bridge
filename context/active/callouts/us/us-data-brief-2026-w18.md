# US W18 Data Brief

## Headline numbers
- Registrations: 8629 (-7% WoW)
- Spend: $729K (flat WoW)
- CPA: $85 (+8% WoW)
- Brand regs: 2505 (-7% WoW)
- NB regs: 6124 (-7% WoW)

## ie%CCP
- This week: 55%
- Last week: 50%
- Target: 100%

## Registration drivers (what caused the WoW change?)
Primary driver: CVR (-13% WoW) more than clicks (+7% WoW)

Brand:
  Regs: 2505 vs 2700 LW (-7%)
  CVR: 3.78% vs 4.26% (-11%)
  Clicks: 66310 vs 63393 (+5%)
  CPA: $75 vs $72 (+4%)

Non-Brand:
  Regs: 6124 vs 6573 LW (-7%)
  CVR: 4.93% vs 5.76% (-14%)
  Clicks: 124181 vs 114031 (+9%)
  CPA: $88 vs $81 (+9%)

## 8-week trend
<!-- Data: market_trend("US", weeks=8) -->

## YoY comparison
- Regs: 8629 TY vs 5562 LY (+55%)
- Spend: $729K TY vs $622K LY (+17%)
- Brand regs: +11% YoY
- NB regs: +85% YoY
- NB CPA: $88 vs $122 LY (-28%)
- WoW pattern: TY -7% vs LY -3% (same week)

## Monthly projection inputs
- Month: 2026 Apr (30/30 days elapsed, 0 remaining)
- MTD actuals: $3.0M spend, 39530 regs (11543 Brand, 27987 NB)
- OP2 targets: $2.8M spend, 31.1K regs
- OP2 pace check: at 100% through the month, linear OP2 pace would be 31.1K regs and $2.8M spend
- MTD vs OP2 pace: +27% regs, +6% spend
- Simple linear projection (ingester estimate, not accounting for seasonality/holidays): $3.0M spend, 39.5K regs, $76 CPA
- NOTE: Analyst should produce the actual projection accounting for weekday/weekend mix, holidays, LY patterns, and known upcoming changes.

## This year weekly trend (last 12 weeks)
<!-- Data: market_trend("US", weeks=12) -->

## Last year same period (W14 to W22)
<!-- Data: db("SELECT * FROM weekly_metrics WHERE market='US' AND week LIKE '2025%' ORDER BY week") -->

## Detected streaks
- CPA rising 5 consecutive weeks ($68 in W13 to $85 in W18)

## Daily breakdown
<!-- Data: db("SELECT * FROM daily_metrics WHERE market='US' AND week='2026 W18' ORDER BY date") -->
