# CA W13 Data Brief

## Headline numbers
- Registrations: 812 (+19% WoW)
- Spend: $52K (-2% WoW)
- CPA: $64 (-17% WoW)
- Brand regs: 565 (+25% WoW)
- NB regs: 247 (+7% WoW)

## ie%CCP
- This week: 6404%
- Last week: 7754%
- Target: 100%

## Registration drivers (what caused the WoW change?)
Primary driver: CVR (+16% WoW) more than clicks (+3% WoW)

Brand:
  Regs: 565 vs 451 LW (+25%)
  CVR: 4.02% vs 3.39% (+19%)
  Clicks: 14061 vs 13315 (+6%)
  CPA: $42 vs $56 (-24%)

Non-Brand:
  Regs: 247 vs 230 LW (+7%)
  CVR: 1.85% vs 1.74% (+6%)
  Clicks: 13359 vs 13247 (+1%)
  CPA: $113 vs $121 (-6%)

## 8-week trend
<!-- Data: market_trend("CA", weeks=8) -->

## YoY comparison
- Regs: 812 TY vs 459 LY (+77%)
- Spend: $52K TY vs $49K LY (+7%)
- Brand regs: +76% YoY
- NB regs: +79% YoY
- NB CPA: $113 vs $240 LY (-53%)
- WoW pattern: TY +19% vs LY +1% (same week)

## Monthly projection inputs
- Month: 2026 Mar (28/31 days elapsed, 3 remaining)
- MTD actuals: $207K spend, 2886 regs (1950 Brand, 936 NB)
- Simple linear projection (ingester estimate, not accounting for seasonality/holidays): $230K spend, 3.2K regs, $71 CPA
- NOTE: Analyst should produce the actual projection accounting for weekday/weekend mix, holidays, LY patterns, and known upcoming changes.

## Anomalies (>20% deviation from recent avg)
- brand regs: above avg by 23% (current: 565.00, avg: 459.86)
- brand cvr: above avg by 24% (current: 0.04, avg: 0.03)

## This year weekly trend (last 12 weeks)
<!-- Data: market_trend("CA", weeks=12) -->

## Last year same period (W9 to W17)
<!-- Data: db("SELECT * FROM weekly_metrics WHERE market='CA' AND week LIKE '2025%' ORDER BY week") -->

## Daily breakdown
<!-- Data: db("SELECT * FROM daily_metrics WHERE market='CA' AND week='2026 W13' ORDER BY date") -->
