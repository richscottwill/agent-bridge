<!-- DOC-0099 | duck_id: callout-us-data-brief-2026-w13 -->
# US W13 Data Brief

## Headline numbers
- Registrations: 8796 (+8% WoW)
- Spend: $583K (-3% WoW)
- CPA: $66 (-9% WoW)
- Brand regs: 2758 (+9% WoW)
- NB regs: 6038 (+7% WoW)

## ie%CCP
- This week: 6627%
- Last week: 7321%
- Target: 100%

## Registration drivers (what caused the WoW change?)
Primary driver: CVR (+4% WoW) more than clicks (+3% WoW)

Brand:
  Regs: 2758 vs 2531 LW (+9%)
  CVR: 4.12% vs 4.03% (+2%)
  Clicks: 66876 vs 62783 (+7%)
  CPA: $62 vs $71 (-13%)

Non-Brand:
  Regs: 6038 vs 5645 LW (+7%)
  CVR: 6.02% vs 5.67% (+6%)
  Clicks: 100320 vs 99545 (+1%)
  CPA: $68 vs $74 (-8%)

## 8-week trend
<!-- Data: market_trend("US", weeks=8) -->

## YoY comparison
- Regs: 8796 TY vs 4944 LY (+78%)
- Spend: $583K TY vs $560K LY (+4%)
- Brand regs: +22% YoY
- NB regs: +125% YoY
- NB CPA: $68 vs $137 LY (-50%)
- WoW pattern: TY +8% vs LY +4% (same week)

## Monthly projection inputs
- Month: 2026 Mar (28/31 days elapsed, 3 remaining)
- MTD actuals: $2.4M spend, 32833 regs (10231 Brand, 22602 NB)
- Simple linear projection (ingester estimate, not accounting for seasonality/holidays): $2.7M spend, 36.6K regs, $73 CPA
- NOTE: Analyst should produce the actual projection accounting for weekday/weekend mix, holidays, LY patterns, and known upcoming changes.

## This year weekly trend (last 12 weeks)
<!-- Data: market_trend("US", weeks=12) -->

## Last year same period (W9 to W17)
<!-- Data: db("SELECT * FROM weekly_metrics WHERE market='US' AND week LIKE '2025%' ORDER BY week") -->

## Detected streaks
- CPA declining 6 consecutive weeks ($93 in W7 to $66 in W13)

## Daily breakdown
<!-- Data: db("SELECT * FROM daily_metrics WHERE market='US' AND week='2026 W13' ORDER BY date") -->
