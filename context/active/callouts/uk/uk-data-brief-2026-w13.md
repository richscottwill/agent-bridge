# UK W13 Data Brief

## Headline numbers
- Registrations: 1531 (+14% WoW)
- Spend: $86K (-5% WoW)
- CPA: $56 (-17% WoW)
- Brand regs: 577 (+31% WoW)
- NB regs: 954 (+6% WoW)

## ie%CCP
- This week: 5591%
- Last week: 6718%
- Target: 100%

## Registration drivers (what caused the WoW change?)
Primary driver: CVR (+17% WoW) more than clicks (-2% WoW)

Brand:
  Regs: 577 vs 442 LW (+31%)
  CVR: 3.37% vs 2.62% (+29%)
  Clicks: 17114 vs 16896 (+1%)
  CPA: $60 vs $75 (-20%)

Non-Brand:
  Regs: 954 vs 896 LW (+6%)
  CVR: 5.12% vs 4.58% (+12%)
  Clicks: 18647 vs 19580 (-5%)
  CPA: $54 vs $64 (-16%)

## 8-week trend
<!-- Data: market_trend("UK", weeks=8) -->

## YoY comparison
- Regs: 1531 TY vs 704 LY (+117%)
- Spend: $86K TY vs $47K LY (+82%)
- Brand regs: +26% YoY
- NB regs: +286% YoY
- NB CPA: $54 vs $71 LY (-24%)
- WoW pattern: TY +14% vs LY -1% (same week)

## Monthly projection inputs
- Month: 2026 Mar (28/31 days elapsed, 3 remaining)
- MTD actuals: $359K spend, 5626 regs (2091 Brand, 3535 NB)
- Simple linear projection (ingester estimate, not accounting for seasonality/holidays): $395K spend, 6.3K regs, $63 CPA
- NOTE: Analyst should produce the actual projection accounting for weekday/weekend mix, holidays, LY patterns, and known upcoming changes.

## This year weekly trend (last 12 weeks)
<!-- Data: market_trend("UK", weeks=12) -->

## Last year same period (W9 to W17)
<!-- Data: db("SELECT * FROM weekly_metrics WHERE market='UK' AND week LIKE '2025%' ORDER BY week") -->

## Daily breakdown
<!-- Data: db("SELECT * FROM daily_metrics WHERE market='UK' AND week='2026 W13' ORDER BY date") -->
