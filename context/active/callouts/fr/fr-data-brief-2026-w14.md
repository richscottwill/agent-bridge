# FR W14 Data Brief

## Headline numbers
- Registrations: 1161 (-1% WoW)
- Spend: $66K (-4% WoW)
- CPA: $57 (-3% WoW)
- Brand regs: 474 (flat WoW)
- NB regs: 687 (-2% WoW)

## ie%CCP
- This week: 58%
- Last week: 60%
- Target: 100%

## Registration drivers (what caused the WoW change?)
Primary driver: clicks (-3% WoW) more than CVR (+2% WoW)

Brand:
  Regs: 474 vs 475 LW (flat)
  CVR: 2.16% vs 2.15% (flat)
  Clicks: 21982 vs 22064 (flat)
  CPA: $37 vs $36 (flat)

Non-Brand:
  Regs: 687 vs 700 LW (-2%)
  CVR: 2.75% vs 2.65% (+4%)
  Clicks: 24947 vs 26449 (-6%)
  CPA: $71 vs $74 (-4%)

## 8-week trend
<!-- Data: market_trend("FR", weeks=8) -->

## YoY comparison
- Regs: 1161 TY vs 1039 LY (+12%)
- Spend: $66K TY vs $40K LY (+65%)
- Brand regs: +15% YoY
- NB regs: +9% YoY
- NB CPA: $71 vs $43 LY (+66%)
- WoW pattern: TY -1% vs LY -4% (same week)

## Monthly projection inputs
- Month: 2026 Mar (31/31 days elapsed, 0 remaining)
- MTD actuals: $312K spend, 5086 regs (2172 Brand, 2914 NB)
- OP2 targets: $289K spend, 4.7K regs
- OP2 pace check: at 100% through the month, linear OP2 pace would be 4.7K regs and $289K spend
- MTD vs OP2 pace: +8% regs, +8% spend
- Simple linear projection (ingester estimate, not accounting for seasonality/holidays): $312K spend, 5.1K regs, $61 CPA
- NOTE: Analyst should produce the actual projection accounting for weekday/weekend mix, holidays, LY patterns, and known upcoming changes.

## This year weekly trend (last 12 weeks)
<!-- Data: market_trend("FR", weeks=12) -->

## Last year same period (W10 to W18)
<!-- Data: db("SELECT * FROM weekly_metrics WHERE market='FR' AND week LIKE '2025%' ORDER BY week") -->

## Daily breakdown
<!-- Data: db("SELECT * FROM daily_metrics WHERE market='FR' AND week='2026 W14' ORDER BY date") -->
