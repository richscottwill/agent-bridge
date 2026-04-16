# ES W15 Data Brief

## Headline numbers
- Registrations: 599 (+26% WoW)
- Spend: $40K (+33% WoW)
- CPA: $67 (+6% WoW)
- Brand regs: 354 (+24% WoW)
- NB regs: 245 (+29% WoW)

## ie%CCP
- This week: 64%
- Last week: 60%
- Target: 100%

## Registration drivers (what caused the WoW change?)
Primary driver: clicks (+35% WoW) more than CVR (-7% WoW)

Brand:
  Regs: 354 vs 285 LW (+24%)
  CVR: 2.34% vs 2.89% (-19%)
  Clicks: 15151 vs 9859 (+54%)
  CPA: $43 vs $31 (+37%)

Non-Brand:
  Regs: 245 vs 190 LW (+29%)
  CVR: 1.98% vs 1.81% (+9%)
  Clicks: 12391 vs 10519 (+18%)
  CPA: $102 vs $112 (-9%)

## 8-week trend
<!-- Data: market_trend("ES", weeks=8) -->

## YoY comparison
- Regs: 599 TY vs 556 LY (+8%)
- Spend: $40K TY vs $29K LY (+39%)
- Brand regs: +13% YoY
- NB regs: +1% YoY
- NB CPA: $102 vs $75 LY (+36%)
- WoW pattern: TY +26% vs LY -3% (same week)

## Monthly projection inputs
- Month: 2026 Apr (11/30 days elapsed, 19 remaining)
- MTD actuals: $55K spend, 834 regs (495 Brand, 339 NB)
- OP2 targets: $108K spend, 2.0K regs
- OP2 pace check: at 37% through the month, linear OP2 pace would be 720 regs and $40K spend
- MTD vs OP2 pace: +16% regs, +38% spend
- Simple linear projection (ingester estimate, not accounting for seasonality/holidays): $164K spend, 2.5K regs, $67 CPA
- NOTE: Analyst should produce the actual projection accounting for weekday/weekend mix, holidays, LY patterns, and known upcoming changes.

## This year weekly trend (last 12 weeks)
<!-- Data: market_trend("ES", weeks=12) -->

## Last year same period (W11 to W19)
<!-- Data: db("SELECT * FROM weekly_metrics WHERE market='ES' AND week LIKE '2025%' ORDER BY week") -->

## Detected streaks
- CPA rising 3 consecutive weeks ($51 in W12 to $67 in W15)

## Daily breakdown
<!-- Data: db("SELECT * FROM daily_metrics WHERE market='ES' AND week='2026 W15' ORDER BY date") -->
