<!-- DOC-0050 | duck_id: callout-fr-data-brief-2026-w13 -->
# FR W13 Data Brief

## Headline numbers
- Registrations: 1191 (+4% WoW)
- Spend: $69K (+14% WoW)
- CPA: $58 (+10% WoW)
- Brand regs: 492 (+2% WoW)
- NB regs: 699 (+5% WoW)

## ie%CCP
- This week: 5821%
- Last week: 5316%
- Target: 100%

## Registration drivers (what caused the WoW change?)
Primary driver: clicks (+7% WoW) more than CVR (-3% WoW)

Brand:
  Regs: 492 vs 480 LW (+2%)
  CVR: 2.23% vs 2.14% (+4%)
  Clicks: 22063 vs 22423 (-2%)
  CPA: $35 vs $38 (-9%)

Non-Brand:
  Regs: 699 vs 664 LW (+5%)
  CVR: 2.64% vs 2.91% (-9%)
  Clicks: 26447 vs 22833 (+16%)
  CPA: $74 vs $64 (+17%)

## 8-week trend
<!-- Data: market_trend("FR", weeks=8) -->

## YoY comparison
- Regs: 1191 TY vs 1088 LY (+9%)
- Spend: $69K TY vs $34K LY (+106%)
- Brand regs: +3% YoY
- NB regs: +15% YoY
- NB CPA: $74 vs $35 LY (+116%)
- WoW pattern: TY +4% vs LY +6% (same week)

## Monthly projection inputs
- Month: 2026 Mar (28/31 days elapsed, 3 remaining)
- MTD actuals: $281K spend, 4609 regs (1995 Brand, 2614 NB)
- Simple linear projection (ingester estimate, not accounting for seasonality/holidays): $310K spend, 5.1K regs, $61 CPA
- NOTE: Analyst should produce the actual projection accounting for weekday/weekend mix, holidays, LY patterns, and known upcoming changes.

## This year weekly trend (last 12 weeks)
<!-- Data: market_trend("FR", weeks=12) -->

## Last year same period (W9 to W17)
<!-- Data: db("SELECT * FROM weekly_metrics WHERE market='FR' AND week LIKE '2025%' ORDER BY week") -->

## Daily breakdown
<!-- Data: db("SELECT * FROM daily_metrics WHERE market='FR' AND week='2026 W13' ORDER BY date") -->
