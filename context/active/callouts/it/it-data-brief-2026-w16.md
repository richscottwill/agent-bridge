# IT W16 Data Brief

## Headline numbers
- Registrations: 1136 (+17% WoW)
- Spend: $98K (-2% WoW)
- CPA: $86 (-16% WoW)
- Brand regs: 768 (+16% WoW)
- NB regs: 368 (+19% WoW)

## ie%CCP
- This week: 73%
- Last week: 87%
- Target: 100%

## Registration drivers (what caused the WoW change?)
Primary driver: CVR (+15% WoW) more than clicks (+2% WoW)

Brand:
  Regs: 768 vs 664 LW (+16%)
  CVR: 2.64% vs 2.44% (+8%)
  Clicks: 29097 vs 27172 (+7%)
  CPA: $56 vs $62 (-10%)

Non-Brand:
  Regs: 368 vs 308 LW (+19%)
  CVR: 2.01% vs 1.58% (+27%)
  Clicks: 18342 vs 19522 (-6%)
  CPA: $151 vs $191 (-21%)

## 8-week trend
<!-- Data: market_trend("IT", weeks=8) -->

## YoY comparison
- Regs: 1136 TY vs 1057 LY (+7%)
- Spend: $98K TY vs $79K LY (+24%)
- Brand regs: +7% YoY
- NB regs: +9% YoY
- NB CPA: $151 vs $134 LY (+13%)
- WoW pattern: TY +17% vs LY -8% (same week)

## Monthly projection inputs
- Month: 2026 Apr (18/30 days elapsed, 12 remaining)
- MTD actuals: $249K spend, 2936 regs (1983 Brand, 953 NB)
- OP2 targets: $351K spend, 5.0K regs
- OP2 pace check: at 60% through the month, linear OP2 pace would be 3.0K regs and $211K spend
- MTD vs OP2 pace: -3% regs, +18% spend
- Simple linear projection (ingester estimate, not accounting for seasonality/holidays): $417K spend, 4.9K regs, $85 CPA
- NOTE: Analyst should produce the actual projection accounting for weekday/weekend mix, holidays, LY patterns, and known upcoming changes.

## This year weekly trend (last 12 weeks)
<!-- Data: market_trend("IT", weeks=12) -->

## Last year same period (W12 to W20)
<!-- Data: db("SELECT * FROM weekly_metrics WHERE market='IT' AND week LIKE '2025%' ORDER BY week") -->

## Daily breakdown
<!-- Data: db("SELECT * FROM daily_metrics WHERE market='IT' AND week='2026 W16' ORDER BY date") -->
