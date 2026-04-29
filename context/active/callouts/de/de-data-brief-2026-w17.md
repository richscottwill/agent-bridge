# DE W17 Data Brief

## Headline numbers
- Registrations: 1541 (+3% WoW)
- Spend: $211K (+6% WoW)
- CPA: $137 (+3% WoW)
- Brand regs: 801 (+5% WoW)
- NB regs: 740 (+2% WoW)

## ie%CCP
- This week: 62%
- Last week: 61%
- Target: 100%

## Registration drivers (what caused the WoW change?)
Primary driver: clicks (+3% WoW) more than CVR (flat WoW)

Brand:
  Regs: 801 vs 766 LW (+5%)
  CVR: 3.15% vs 3.06% (+3%)
  Clicks: 25415 vs 25015 (+2%)
  CPA: $67 vs $55 (+21%)

Non-Brand:
  Regs: 740 vs 729 LW (+2%)
  CVR: 2.13% vs 2.20% (-3%)
  Clicks: 34705 vs 33197 (+5%)
  CPA: $213 vs $215 (-1%)

## 8-week trend
<!-- Data: market_trend("DE", weeks=8) -->

## YoY comparison
- Regs: 1541 TY vs 978 LY (+58%)
- Spend: $211K TY vs $157K LY (+34%)
- Brand regs: +42% YoY
- NB regs: +80% YoY
- NB CPA: $213 vs $256 LY (-17%)
- WoW pattern: TY +3% vs LY -5% (same week)

## Monthly projection inputs
- Month: 2026 Apr (25/30 days elapsed, 5 remaining)
- MTD actuals: $577K spend, 4865 regs (2563 Brand, 2302 NB)
- OP2 targets: $606K spend, 5.7K regs
- OP2 pace check: at 83% through the month, linear OP2 pace would be 4.8K regs and $505K spend
- MTD vs OP2 pace: +2% regs, +14% spend
- Simple linear projection (ingester estimate, not accounting for seasonality/holidays): $728K spend, 6.0K regs, $122 CPA
- NOTE: Analyst should produce the actual projection accounting for weekday/weekend mix, holidays, LY patterns, and known upcoming changes.

## Anomalies (>20% deviation from recent avg)
- regs: above avg by 25% (current: 1541.00, avg: 1234.43)
- cost: above avg by 49% (current: 210725.06, avg: 141435.20)
- nb regs: above avg by 38% (current: 740.00, avg: 536.43)
- cpc: above avg by 20% (current: 3.51, avg: 2.91)

## This year weekly trend (last 12 weeks)
<!-- Data: market_trend("DE", weeks=12) -->

## Last year same period (W13 to W21)
<!-- Data: db("SELECT * FROM weekly_metrics WHERE market='DE' AND week LIKE '2025%' ORDER BY week") -->

## Detected streaks
- CPA rising 3 consecutive weeks ($80 in W14 to $137 in W17)

## Daily breakdown
<!-- Data: db("SELECT * FROM daily_metrics WHERE market='DE' AND week='2026 W17' ORDER BY date") -->
