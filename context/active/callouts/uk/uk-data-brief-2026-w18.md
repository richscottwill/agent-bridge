# UK W18 Data Brief

## Headline numbers
- Registrations: 1315 (-17% WoW)
- Spend: $90K (-25% WoW)
- CPA: $68 (-10% WoW)
- Brand regs: 495 (flat WoW)
- NB regs: 820 (-24% WoW)

## ie%CCP
- This week: 52%
- Last week: 63%
- Target: 100%

## Registration drivers (what caused the WoW change?)
Primary driver: clicks (-14% WoW) more than CVR (-3% WoW)

Brand:
  Regs: 495 vs 495 LW (flat)
  CVR: 2.89% vs 2.94% (-1%)
  Clicks: 17113 vs 16858 (+2%)
  CPA: $82 vs $86 (-4%)

Non-Brand:
  Regs: 820 vs 1080 LW (-24%)
  CVR: 4.85% vs 4.78% (+2%)
  Clicks: 16912 vs 22616 (-25%)
  CPA: $59 vs $71 (-17%)

## 8-week trend
<!-- Data: market_trend("UK", weeks=8) -->

## YoY comparison
- Regs: 1315 TY vs 604 LY (+118%)
- Spend: $90K TY vs $39K LY (+129%)
- Brand regs: +22% YoY
- NB regs: +312% YoY
- NB CPA: $59 vs $85 LY (-30%)
- WoW pattern: TY -17% vs LY +1% (same week)

## Monthly projection inputs
- Month: 2026 Apr (30/30 days elapsed, 0 remaining)
- MTD actuals: $448K spend, 6380 regs (2062 Brand, 4318 NB)
- OP2 targets: $401K spend, 4.5K regs
- OP2 pace check: at 100% through the month, linear OP2 pace would be 4.5K regs and $401K spend
- MTD vs OP2 pace: +42% regs, +12% spend
- Simple linear projection (ingester estimate, not accounting for seasonality/holidays): $448K spend, 6.4K regs, $70 CPA
- NOTE: Analyst should produce the actual projection accounting for weekday/weekend mix, holidays, LY patterns, and known upcoming changes.

## This year weekly trend (last 12 weeks)
<!-- Data: market_trend("UK", weeks=12) -->

## Last year same period (W14 to W22)
<!-- Data: db("SELECT * FROM weekly_metrics WHERE market='UK' AND week LIKE '2025%' ORDER BY week") -->

## Daily breakdown
<!-- Data: db("SELECT * FROM daily_metrics WHERE market='UK' AND week='2026 W18' ORDER BY date") -->
