# ES W16 Data Brief

## Headline numbers
- Registrations: 613 (+3% WoW)
- Spend: $38K (-6% WoW)
- CPA: $62 (-8% WoW)
- Brand regs: 364 (+3% WoW)
- NB regs: 249 (+3% WoW)

## ie%CCP
- This week: 59%
- Last week: 64%
- Target: 100%

## Registration drivers (what caused the WoW change?)
Primary driver: CVR (+15% WoW) more than clicks (-10% WoW)

Brand:
  Regs: 364 vs 353 LW (+3%)
  CVR: 2.63% vs 2.33% (+13%)
  Clicks: 13820 vs 15151 (-9%)
  CPA: $40 vs $43 (-9%)

Non-Brand:
  Regs: 249 vs 242 LW (+3%)
  CVR: 2.28% vs 1.95% (+17%)
  Clicks: 10943 vs 12391 (-12%)
  CPA: $95 vs $103 (-8%)

## 8-week trend
<!-- Data: market_trend("ES", weeks=8) -->

## YoY comparison
- Regs: 613 TY vs 453 LY (+35%)
- Spend: $38K TY vs $25K LY (+52%)
- Brand regs: +50% YoY
- NB regs: +18% YoY
- NB CPA: $95 vs $87 LY (+10%)
- WoW pattern: TY +3% vs LY -19% (same week)

## Monthly projection inputs
- Month: 2026 Apr (18/30 days elapsed, 12 remaining)
- MTD actuals: $93K spend, 1441 regs (857 Brand, 584 NB)
- OP2 targets: $108K spend, 2.0K regs
- OP2 pace check: at 60% through the month, linear OP2 pace would be 1.2K regs and $65K spend
- MTD vs OP2 pace: +22% regs, +43% spend
- Simple linear projection (ingester estimate, not accounting for seasonality/holidays): $158K spend, 2.5K regs, $64 CPA
- NOTE: Analyst should produce the actual projection accounting for weekday/weekend mix, holidays, LY patterns, and known upcoming changes.

## This year weekly trend (last 12 weeks)
<!-- Data: market_trend("ES", weeks=12) -->

## Last year same period (W12 to W20)
<!-- Data: db("SELECT * FROM weekly_metrics WHERE market='ES' AND week LIKE '2025%' ORDER BY week") -->

## Daily breakdown
<!-- Data: db("SELECT * FROM daily_metrics WHERE market='ES' AND week='2026 W16' ORDER BY date") -->
