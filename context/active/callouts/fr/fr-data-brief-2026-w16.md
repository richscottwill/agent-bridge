# FR W16 Data Brief

## Headline numbers
- Registrations: 1037 (+18% WoW)
- Spend: $69K (+14% WoW)
- CPA: $67 (-4% WoW)
- Brand regs: 451 (+29% WoW)
- NB regs: 586 (+11% WoW)

## ie%CCP
- This week: 67%
- Last week: 71%
- Target: 100%

## Registration drivers (what caused the WoW change?)
Primary driver: CVR (+11% WoW) more than clicks (+6% WoW)

Brand:
  Regs: 451 vs 350 LW (+29%)
  CVR: 2.34% vs 1.96% (+19%)
  Clicks: 19295 vs 17830 (+8%)
  CPA: $42 vs $44 (-3%)

Non-Brand:
  Regs: 586 vs 527 LW (+11%)
  CVR: 2.59% vs 2.44% (+6%)
  Clicks: 22661 vs 21594 (+5%)
  CPA: $85 vs $86 (-1%)

## 8-week trend
<!-- Data: market_trend("FR", weeks=8) -->

## YoY comparison
- Regs: 1037 TY vs 897 LY (+16%)
- Spend: $69K TY vs $45K LY (+55%)
- Brand regs: +25% YoY
- NB regs: +9% YoY
- NB CPA: $85 vs $62 LY (+37%)
- WoW pattern: TY +18% vs LY -5% (same week)

## Monthly projection inputs
- Month: 2026 Apr (18/30 days elapsed, 12 remaining)
- MTD actuals: $165K spend, 2565 regs (1071 Brand, 1494 NB)
- OP2 targets: $224K spend, 4.1K regs
- OP2 pace check: at 60% through the month, linear OP2 pace would be 2.5K regs and $134K spend
- MTD vs OP2 pace: +4% regs, +23% spend
- Simple linear projection (ingester estimate, not accounting for seasonality/holidays): $283K spend, 4.3K regs, $65 CPA
- NOTE: Analyst should produce the actual projection accounting for weekday/weekend mix, holidays, LY patterns, and known upcoming changes.

## This year weekly trend (last 12 weeks)
<!-- Data: market_trend("FR", weeks=12) -->

## Last year same period (W12 to W20)
<!-- Data: db("SELECT * FROM weekly_metrics WHERE market='FR' AND week LIKE '2025%' ORDER BY week") -->

## Daily breakdown
<!-- Data: db("SELECT * FROM daily_metrics WHERE market='FR' AND week='2026 W16' ORDER BY date") -->
