# DE W12 Data Brief

## Headline numbers
- Registrations: 1242 (-18% WoW)
- Spend: $138K (-19% WoW)
- CPA: $111 (-1% WoW)
- Brand regs: 716 (-21% WoW)
- NB regs: 526 (-13% WoW)

## ie%CCP
- This week: 58%
- Last week: 58%
- Target: 100%

## Registration drivers (what caused the WoW change?)
Primary driver: clicks (-11% WoW) more than CVR (-8% WoW)

Brand:
  Regs: 716 vs 906 LW (-21%)
  CVR: 2.60% vs 3.05% (-15%)
  Clicks: 27500 vs 29659 (-7%)
  CPA: $79 vs $77 (+3%)

Non-Brand:
  Regs: 526 vs 606 LW (-13%)
  CVR: 2.40% vs 2.36% (+2%)
  Clicks: 21928 vs 25706 (-15%)
  CPA: $156 vs $167 (-6%)

## 8-week trend
<!-- Data: market_trend("DE", weeks=8) -->

## YoY comparison
- Regs: 1242 TY vs 1360 LY (-9%)
- Spend: $138K TY vs $121K LY (+15%)
- Brand regs: -2% YoY
- NB regs: -16% YoY
- NB CPA: $156 vs $120 LY (+30%)
- WoW pattern: TY -18% vs LY -2% (same week)

## Monthly projection inputs
- Month: 2026 Mar (21/31 days elapsed, 10 remaining)
- MTD actuals: $467K spend, 4174 regs (2483 Brand, 1691 NB)
- OP2 targets: $658K spend, 6.1K regs
- OP2 pace check: at 68% through the month, linear OP2 pace would be 4.2K regs and $445K spend
- MTD vs OP2 pace: +1% regs, +5% spend
- Simple linear projection (ingester estimate, not accounting for seasonality/holidays): $664K spend, 5.9K regs, $112 CPA
- NOTE: Analyst should produce the actual projection accounting for weekday/weekend mix, holidays, LY patterns, and known upcoming changes.

## This year weekly trend (last 12 weeks)
<!-- Data: market_trend("DE", weeks=12) -->

## Last year same period (W8 to W16)
<!-- Data: db("SELECT * FROM weekly_metrics WHERE market='DE' AND week LIKE '2025%' ORDER BY week") -->

## Detected streaks
- NB CPC declining 3 consecutive weeks ($4.39 in W9 to $3.74 in W12)

## Daily breakdown
<!-- Data: db("SELECT * FROM daily_metrics WHERE market='DE' AND week='2026 W12' ORDER BY date") -->

⚠️ DATA LAG: last 2 days avg 32 regs vs weekday avg 236