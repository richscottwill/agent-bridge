# CA W15 Data Brief

## Headline numbers
- Registrations: 698 (-13% WoW)
- Spend: $56K (+11% WoW)
- CPA: $81 (+28% WoW)
- Brand regs: 427 (-14% WoW)
- NB regs: 271 (-12% WoW)

## ie%CCP
- This week: 57%
- Last week: 45%
- Target: 100%

## Registration drivers (what caused the WoW change?)
Primary driver: CVR (-19% WoW) more than clicks (+7% WoW)

Brand:
  Regs: 427 vs 495 LW (-14%)
  CVR: 3.12% vs 3.84% (-19%)
  Clicks: 13667 vs 12906 (+6%)
  CPA: $60 vs $45 (+32%)

Non-Brand:
  Regs: 271 vs 309 LW (-12%)
  CVR: 1.85% vs 2.27% (-18%)
  Clicks: 14610 vs 13633 (+7%)
  CPA: $114 vs $92 (+24%)

## 8-week trend
<!-- Data: market_trend("CA", weeks=8) -->

## YoY comparison
- Regs: 698 TY vs 442 LY (+58%)
- Spend: $56K TY vs $51K LY (+10%)
- Brand regs: +37% YoY
- NB regs: +108% YoY
- NB CPA: $114 vs $276 LY (-59%)
- WoW pattern: TY -13% vs LY -5% (same week)

## Monthly projection inputs
- Month: 2026 Apr (11/30 days elapsed, 19 remaining)
- MTD actuals: $85K spend, 1128 regs (686 Brand, 442 NB)
- OP2 targets: $214K spend, 2.4K regs
- OP2 pace check: at 37% through the month, linear OP2 pace would be 897 regs and $79K spend
- MTD vs OP2 pace: +26% regs, +8% spend
- Simple linear projection (ingester estimate, not accounting for seasonality/holidays): $238K spend, 3.0K regs, $79 CPA
- NOTE: Analyst should produce the actual projection accounting for weekday/weekend mix, holidays, LY patterns, and known upcoming changes.

## This year weekly trend (last 12 weeks)
<!-- Data: market_trend("CA", weeks=12) -->

## Last year same period (W11 to W19)
<!-- Data: db("SELECT * FROM weekly_metrics WHERE market='CA' AND week LIKE '2025%' ORDER BY week") -->

## Daily breakdown
<!-- Data: db("SELECT * FROM daily_metrics WHERE market='CA' AND week='2026 W15' ORDER BY date") -->
