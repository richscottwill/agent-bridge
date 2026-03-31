# ES W13 Data Brief

## Headline numbers
- Registrations: 645 (flat WoW)
- Spend: $38K (+17% WoW)
- CPA: $59 (+17% WoW)
- Brand regs: 364 (-8% WoW)
- NB regs: 281 (+12% WoW)

## ie%CCP
- This week: 5917%
- Last week: 5072%
- Target: 100%

## Registration drivers (what caused the WoW change?)
Primary driver: clicks (+8% WoW) more than CVR (-7% WoW)

Brand:
  Regs: 364 vs 394 LW (-8%)
  CVR: 2.60% vs 2.92% (-11%)
  Clicks: 13993 vs 13472 (+4%)
  CPA: $35 vs $29 (+22%)

Non-Brand:
  Regs: 281 vs 250 LW (+12%)
  CVR: 2.24% vs 2.25% (flat)
  Clicks: 12528 vs 11094 (+13%)
  CPA: $91 vs $86 (+6%)

## 8-week trend
<!-- Data: market_trend("ES", weeks=8) -->

## YoY comparison
- Regs: 645 TY vs 577 LY (+12%)
- Spend: $38K TY vs $21K LY (+84%)
- Brand regs: +16% YoY
- NB regs: +7% YoY
- NB CPA: $91 vs $50 LY (+82%)
- WoW pattern: TY flat vs LY +5% (same week)

## Monthly projection inputs
- Month: 2026 Mar (28/31 days elapsed, 3 remaining)
- MTD actuals: $155K spend, 2638 regs (1577 Brand, 1061 NB)
- Simple linear projection (ingester estimate, not accounting for seasonality/holidays): $171K spend, 2.9K regs, $59 CPA
- NOTE: Analyst should produce the actual projection accounting for weekday/weekend mix, holidays, LY patterns, and known upcoming changes.

## This year weekly trend (last 12 weeks)
<!-- Data: market_trend("ES", weeks=12) -->

## Last year same period (W9 to W17)
<!-- Data: db("SELECT * FROM weekly_metrics WHERE market='ES' AND week LIKE '2025%' ORDER BY week") -->

## Daily breakdown
<!-- Data: db("SELECT * FROM daily_metrics WHERE market='ES' AND week='2026 W13' ORDER BY date") -->
