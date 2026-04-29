# FR W17 Data Brief

## Headline numbers
- Registrations: 1067 (+4% WoW)
- Spend: $68K (-2% WoW)
- CPA: $64 (-5% WoW)
- Brand regs: 477 (+8% WoW)
- NB regs: 590 (+1% WoW)

## ie%CCP
- This week: 55%
- Last week: 59%
- Target: 100%

## Registration drivers (what caused the WoW change?)
Primary driver: CVR (+12% WoW) more than clicks (-7% WoW)

Brand:
  Regs: 477 vs 440 LW (+8%)
  CVR: 2.60% vs 2.28% (+14%)
  Clicks: 18311 vs 19295 (-5%)
  CPA: $39 vs $43 (-10%)

Non-Brand:
  Regs: 590 vs 585 LW (+1%)
  CVR: 2.87% vs 2.58% (+11%)
  Clicks: 20546 vs 22661 (-9%)
  CPA: $83 vs $85 (-2%)

## 8-week trend
<!-- Data: market_trend("FR", weeks=8) -->

## YoY comparison
- Regs: 1067 TY vs 873 LY (+22%)
- Spend: $68K TY vs $36K LY (+91%)
- Brand regs: +39% YoY
- NB regs: +12% YoY
- NB CPA: $83 vs $51 LY (+64%)
- WoW pattern: TY +4% vs LY -3% (same week)

## Monthly projection inputs
- Month: 2026 Apr (25/30 days elapsed, 5 remaining)
- MTD actuals: $233K spend, 3621 regs (1539 Brand, 2082 NB)
- OP2 targets: $224K spend, 4.1K regs
- OP2 pace check: at 83% through the month, linear OP2 pace would be 3.4K regs and $186K spend
- MTD vs OP2 pace: +6% regs, +25% spend
- Simple linear projection (ingester estimate, not accounting for seasonality/holidays): $282K spend, 4.4K regs, $64 CPA
- NOTE: Analyst should produce the actual projection accounting for weekday/weekend mix, holidays, LY patterns, and known upcoming changes.

## Anomalies (>20% deviation from recent avg)
- brand cvr: above avg by 23% (current: 0.03, avg: 0.02)

## This year weekly trend (last 12 weeks)
<!-- Data: market_trend("FR", weeks=12) -->

## Last year same period (W13 to W21)
<!-- Data: db("SELECT * FROM weekly_metrics WHERE market='FR' AND week LIKE '2025%' ORDER BY week") -->

## Detected streaks
- NB CPC rising 3 consecutive weeks ($1.96 in W14 to $2.40 in W17)

## Daily breakdown
<!-- Data: db("SELECT * FROM daily_metrics WHERE market='FR' AND week='2026 W17' ORDER BY date") -->
