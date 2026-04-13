# ES W15 Data Brief

## Headline numbers
- Registrations: 599 (+26% WoW)
- Spend: $40K (+33% WoW)
- CPA: $67 (+5% WoW)
- Brand regs: 356 (+25% WoW)
- NB regs: 243 (+29% WoW)

## ie%CCP
- This week: 64%
- Last week: 60%
- Target: 100%

## Registration drivers (what caused the WoW change?)
Primary driver: clicks (+35% WoW) more than CVR (-6% WoW)

Brand:
  Regs: 356 vs 285 LW (+25%)
  CVR: 2.35% vs 2.89% (-19%)
  Clicks: 15151 vs 9859 (+54%)
  CPA: $43 vs $31 (+37%)

Non-Brand:
  Regs: 243 vs 189 LW (+29%)
  CVR: 1.96% vs 1.80% (+9%)
  Clicks: 12391 vs 10519 (+18%)
  CPA: $103 vs $113 (-9%)

## 8-week trend
<!-- Data: market_trend("ES", weeks=8) -->

## YoY comparison
- Regs: 599 TY vs 556 LY (+8%)
- Spend: $40K TY vs $29K LY (+39%)
- Brand regs: +14% YoY
- NB regs: flat YoY
- NB CPA: $103 vs $75 LY (+37%)
- WoW pattern: TY +26% vs LY -3% (same week)

## Monthly projection inputs
- Month: 2026 Apr (11/30 days elapsed, 19 remaining)
- MTD actuals: $55K spend, 832 regs (496 Brand, 336 NB)
- OP2 targets: $123K spend, 2.0K regs
- OP2 pace check: at 37% through the month, linear OP2 pace would be 720 regs and $45K spend
- MTD vs OP2 pace: +16% regs, +22% spend
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
