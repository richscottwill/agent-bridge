# FR W15 Data Brief

## Headline numbers
- Registrations: 886 (-23% WoW)
- Spend: $61K (-8% WoW)
- CPA: $69 (+19% WoW)
- Brand regs: 359 (-23% WoW)
- NB regs: 527 (-23% WoW)

## ie%CCP
- This week: 70%
- Last week: 59%
- Target: 100%

## Registration drivers (what caused the WoW change?)
Primary driver: clicks (-16% WoW) more than CVR (-8% WoW)

Brand:
  Regs: 359 vs 465 LW (-23%)
  CVR: 2.01% vs 2.12% (-5%)
  Clicks: 17830 vs 21982 (-19%)
  CPA: $43 vs $37 (+14%)

Non-Brand:
  Regs: 527 vs 683 LW (-23%)
  CVR: 2.44% vs 2.74% (-11%)
  Clicks: 21594 vs 24947 (-13%)
  CPA: $86 vs $72 (+20%)

## 8-week trend
<!-- Data: market_trend("FR", weeks=8) -->

## YoY comparison
- Regs: 886 TY vs 947 LY (-6%)
- Spend: $61K TY vs $43K LY (+42%)
- Brand regs: -9% YoY
- NB regs: -5% YoY
- NB CPA: $86 vs $58 LY (+49%)
- WoW pattern: TY -23% vs LY -9% (same week)

## Monthly projection inputs
- Month: 2026 Apr (11/30 days elapsed, 19 remaining)
- MTD actuals: $96K spend, 1541 regs (631 Brand, 910 NB)
- OP2 targets: $254K spend, 4.1K regs
- OP2 pace check: at 37% through the month, linear OP2 pace would be 1.5K regs and $93K spend
- MTD vs OP2 pace: +2% regs, +3% spend
- Simple linear projection (ingester estimate, not accounting for seasonality/holidays): $261K spend, 3.9K regs, $66 CPA
- NOTE: Analyst should produce the actual projection accounting for weekday/weekend mix, holidays, LY patterns, and known upcoming changes.

## Anomalies (>20% deviation from recent avg)
- regs: below avg by 22% (current: 886.00, avg: 1134.86)
- brand regs: below avg by 24% (current: 359.00, avg: 474.57)
- nb regs: below avg by 20% (current: 527.00, avg: 660.29)

## This year weekly trend (last 12 weeks)
<!-- Data: market_trend("FR", weeks=12) -->

## Last year same period (W11 to W19)
<!-- Data: db("SELECT * FROM weekly_metrics WHERE market='FR' AND week LIKE '2025%' ORDER BY week") -->

## Daily breakdown
<!-- Data: db("SELECT * FROM daily_metrics WHERE market='FR' AND week='2026 W15' ORDER BY date") -->
