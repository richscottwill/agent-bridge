# CA W16 Data Brief

## Headline numbers
- Registrations: 778 (+13% WoW)
- Spend: $60K (+7% WoW)
- CPA: $77 (-5% WoW)
- Brand regs: 455 (+9% WoW)
- NB regs: 323 (+20% WoW)

## ie%CCP
- This week: 57%
- Last week: 58%
- Target: 100%

## Registration drivers (what caused the WoW change?)
Primary driver: CVR (+14% WoW) more than clicks (-1% WoW)

Brand:
  Regs: 455 vs 419 LW (+9%)
  CVR: 3.49% vs 3.07% (+14%)
  Clicks: 13025 vs 13667 (-5%)
  CPA: $62 vs $61 (+1%)

Non-Brand:
  Regs: 323 vs 270 LW (+20%)
  CVR: 2.16% vs 1.85% (+17%)
  Clicks: 14941 vs 14610 (+2%)
  CPA: $100 vs $115 (-13%)

## 8-week trend
<!-- Data: market_trend("CA", weeks=8) -->

## YoY comparison
- Regs: 778 TY vs 372 LY (+109%)
- Spend: $60K TY vs $48K LY (+27%)
- Brand regs: +74% YoY
- NB regs: +191% YoY
- NB CPA: $100 vs $302 LY (-67%)
- WoW pattern: TY +13% vs LY -16% (same week)

## Monthly projection inputs
- Month: 2026 Apr (18/30 days elapsed, 12 remaining)
- MTD actuals: $146K spend, 1889 regs (1125 Brand, 764 NB)
- OP2 targets: $214K spend, 2.4K regs
- OP2 pace check: at 60% through the month, linear OP2 pace would be 1.5K regs and $129K spend
- MTD vs OP2 pace: +29% regs, +13% spend
- Simple linear projection (ingester estimate, not accounting for seasonality/holidays): $249K spend, 3.2K regs, $77 CPA
- NOTE: Analyst should produce the actual projection accounting for weekday/weekend mix, holidays, LY patterns, and known upcoming changes.

## Anomalies (>20% deviation from recent avg)
- nb regs: above avg by 29% (current: 323.00, avg: 249.57)

## This year weekly trend (last 12 weeks)
<!-- Data: market_trend("CA", weeks=12) -->

## Last year same period (W12 to W20)
<!-- Data: db("SELECT * FROM weekly_metrics WHERE market='CA' AND week LIKE '2025%' ORDER BY week") -->

## Daily breakdown
<!-- Data: db("SELECT * FROM daily_metrics WHERE market='CA' AND week='2026 W16' ORDER BY date") -->
