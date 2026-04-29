# US W17 Data Brief

## Headline numbers
- Registrations: 9450 (+6% WoW)
- Spend: $726K (+7% WoW)
- CPA: $77 (+1% WoW)
- Brand regs: 2817 (-3% WoW)
- NB regs: 6633 (+10% WoW)

## ie%CCP
- This week: 49%
- Last week: 45%
- Target: 100%

## Registration drivers (what caused the WoW change?)
Primary driver: clicks (+5% WoW) more than CVR (flat WoW)

Brand:
  Regs: 2817 vs 2898 LW (-3%)
  CVR: 4.44% vs 4.42% (+1%)
  Clicks: 63393 vs 65597 (-3%)
  CPA: $69 vs $64 (+8%)

Non-Brand:
  Regs: 6633 vs 6038 LW (+10%)
  CVR: 5.82% vs 5.86% (-1%)
  Clicks: 114031 vs 102964 (+11%)
  CPA: $80 vs $82 (-2%)

## 8-week trend
<!-- Data: market_trend("US", weeks=8) -->

## YoY comparison
- Regs: 9450 TY vs 5716 LY (+65%)
- Spend: $726K TY vs $585K LY (+24%)
- Brand regs: -1% YoY
- NB regs: +131% YoY
- NB CPA: $80 vs $134 LY (-40%)
- WoW pattern: TY +6% vs LY +21% (same week)

## Monthly projection inputs
- Month: 2026 Apr (25/30 days elapsed, 5 remaining)
- MTD actuals: $2.5M spend, 33117 regs (9814 Brand, 23303 NB)
- OP2 targets: $2.8M spend, 31.1K regs
- OP2 pace check: at 83% through the month, linear OP2 pace would be 25.9K regs and $2.4M spend
- MTD vs OP2 pace: +28% regs, +4% spend
- Simple linear projection (ingester estimate, not accounting for seasonality/holidays): $3.0M spend, 39.9K regs, $75 CPA
- NOTE: Analyst should produce the actual projection accounting for weekday/weekend mix, holidays, LY patterns, and known upcoming changes.

## This year weekly trend (last 12 weeks)
<!-- Data: market_trend("US", weeks=12) -->

## Last year same period (W13 to W21)
<!-- Data: db("SELECT * FROM weekly_metrics WHERE market='US' AND week LIKE '2025%' ORDER BY week") -->

## Detected streaks
- CPA rising 4 consecutive weeks ($68 in W13 to $77 in W17)

## Daily breakdown
<!-- Data: db("SELECT * FROM daily_metrics WHERE market='US' AND week='2026 W17' ORDER BY date") -->
