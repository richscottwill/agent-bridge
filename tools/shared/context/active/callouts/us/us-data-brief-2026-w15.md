# US W15 Data Brief

## Headline numbers
- Registrations: 9523 (flat WoW)
- Spend: $678K (+2% WoW)
- CPA: $71 (+2% WoW)
- Brand regs: 2723 (+3% WoW)
- NB regs: 6800 (-2% WoW)

## ie%CCP
- This week: 45%
- Last week: 46%
- Target: 100%

## Registration drivers (what caused the WoW change?)
Primary driver: clicks (-1% WoW) more than CVR (+1% WoW)

Brand:
  Regs: 2723 vs 2642 LW (+3%)
  CVR: 4.25% vs 4.24% (flat)
  Clicks: 64107 vs 62371 (+3%)
  CPA: $66 vs $63 (+5%)

Non-Brand:
  Regs: 6800 vs 6922 LW (-2%)
  CVR: 6.42% vs 6.32% (+2%)
  Clicks: 105900 vs 109472 (-3%)
  CPA: $73 vs $72 (+1%)

## 8-week trend
<!-- Data: market_trend("US", weeks=8) -->

## YoY comparison
- Regs: 9523 TY vs 4986 LY (+91%)
- Spend: $678K TY vs $541K LY (+25%)
- Brand regs: +16% YoY
- NB regs: +158% YoY
- NB CPA: $73 vs $138 LY (-47%)
- WoW pattern: TY flat vs LY -1% (same week)

## Monthly projection inputs
- Month: 2026 Apr (11/30 days elapsed, 19 remaining)
- MTD actuals: $1.1M spend, 14927 regs (4237 Brand, 10690 NB)
- OP2 targets: $2.8M spend, 31.1K regs
- OP2 pace check: at 37% through the month, linear OP2 pace would be 11.4K regs and $1.0M spend
- MTD vs OP2 pace: +31% regs, +1% spend
- Simple linear projection (ingester estimate, not accounting for seasonality/holidays): $2.9M spend, 40.8K regs, $71 CPA
- NOTE: Analyst should produce the actual projection accounting for weekday/weekend mix, holidays, LY patterns, and known upcoming changes.

## This year weekly trend (last 12 weeks)
<!-- Data: market_trend("US", weeks=12) -->

## Last year same period (W11 to W19)
<!-- Data: db("SELECT * FROM weekly_metrics WHERE market='US' AND week LIKE '2025%' ORDER BY week") -->

## Daily breakdown
<!-- Data: db("SELECT * FROM daily_metrics WHERE market='US' AND week='2026 W15' ORDER BY date") -->
