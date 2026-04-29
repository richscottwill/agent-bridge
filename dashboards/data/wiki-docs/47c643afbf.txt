# FR W15 Data Brief

## Headline numbers
- Registrations: 886 (-23% WoW)
- Spend: $61K (-8% WoW)
- CPA: $69 (+19% WoW)
- Brand regs: 356 (-23% WoW)
- NB regs: 530 (-22% WoW)

## ie%CCP
- This week: 70%
- Last week: 59%
- Target: 100%

## Registration drivers (what caused the WoW change?)
Primary driver: clicks (-16% WoW) more than CVR (-8% WoW)

Brand:
  Regs: 356 vs 464 LW (-23%)
  CVR: 2.00% vs 2.11% (-5%)
  Clicks: 17830 vs 21982 (-19%)
  CPA: $43 vs $37 (+15%)

Non-Brand:
  Regs: 530 vs 682 LW (-22%)
  CVR: 2.45% vs 2.73% (-10%)
  Clicks: 21594 vs 24947 (-13%)
  CPA: $86 vs $72 (+20%)

## 8-week trend
<!-- Data: market_trend("FR", weeks=8) -->

## YoY comparison
- Regs: 886 TY vs 947 LY (-6%)
- Spend: $61K TY vs $43K LY (+42%)
- Brand regs: -10% YoY
- NB regs: -4% YoY
- NB CPA: $86 vs $58 LY (+48%)
- WoW pattern: TY -23% vs LY -9% (same week)

## Monthly projection inputs
- Month: 2026 Apr (11/30 days elapsed, 19 remaining)
- MTD actuals: $96K spend, 1540 regs (628 Brand, 912 NB)
- OP2 targets: $224K spend, 4.1K regs
- OP2 pace check: at 37% through the month, linear OP2 pace would be 1.5K regs and $82K spend
- MTD vs OP2 pace: +2% regs, +17% spend
- Simple linear projection (ingester estimate, not accounting for seasonality/holidays): $261K spend, 3.9K regs, $66 CPA
- NOTE: Analyst should produce the actual projection accounting for weekday/weekend mix, holidays, LY patterns, and known upcoming changes.

## Anomalies (>20% deviation from recent avg)
- regs: below avg by 22% (current: 886.00, avg: 1132.00)
- brand regs: below avg by 25% (current: 356.00, avg: 473.00)

## This year weekly trend (last 12 weeks)
<!-- Data: market_trend("FR", weeks=12) -->

## Last year same period (W11 to W19)
<!-- Data: db("SELECT * FROM weekly_metrics WHERE market='FR' AND week LIKE '2025%' ORDER BY week") -->

## Daily breakdown
<!-- Data: db("SELECT * FROM daily_metrics WHERE market='FR' AND week='2026 W15' ORDER BY date") -->
