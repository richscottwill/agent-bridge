---
title: "US Monthly Projections"
status: FINAL
audience: amazon-internal
owner: Richard Williams
created: 2026-04-12
updated: 2026-04-20
---
<!-- DOC-0100 | duck_id: callout-us-projections -->

# US Monthly Projections

Tracks weekly projections vs actuals. Updated each week by the analyst agents.
Calibration: Weighted MAPE (weight = days_elapsed / total_days). Score = 1 - WMAPE.
Indicators: ✅ within 5% | 🟢 beating CPA target | 🔴 outside 5%

---

## Mar 2026

OP2: 30,517 regs | $2,744,318 spend | $90 CPA

### Registrations

| Week | Days  | Projected | MTD    | vs OP2 |     |
| ---- | ----- | --------- | ------ | ------ | --- |
| W12  | 21/31 | 34,900    | 24,222 | +14%   | 🔴   |
| W13  | 28/31 | 35,400    | 32,833 | +16%   | 🔴   |

### Spend

| Week | Days  | Projected  | MTD        | vs OP2 |     |
| ---- | ----- | ---------- | ---------- | ------ | --- |
| W12  | 21/31 | $2,650,000 | $1,843,456 | -3%    | ✅   |
| W13  | 28/31 | $2,660,000 | $2,426,000 | -3%    | ✅   |

### CPA

| Week | Days  | Projected | OP2 |     |
| ---- | ----- | --------- | --- | --- |
| W12  | 21/31 | $76       | $90 | 🟢   |
| W13  | 28/31 | $75       | $90 | 🟢   |

### Rationale
- W12: W11-W12 blended daily rates (weekday 1,250, weekend 900). -3% late-March softness. CPA 5-week decline streak supports efficiency.
- W13: W12-W13 blended weekday avg ~1,290, weekend ~970. -3% end-of-month conservatism. 6th consecutive CPA decline. 3 remaining days (1 weekend, 2 weekday). No holidays.

### Accuracy (after month closes)

| Week | Proj Regs | Actual | Error % | Weight | Wtd Error |
| ---- | --------- | ------ | ------- | ------ | --------- |
| —    | —         | —      | —       | —      | —         |

WMAPE: — | Calibration: —

---

## Apr 2026

OP2: 31,076 regs | $2,831,154 spend | $91 CPA

### Registrations

| Week | Days  | Projected | MTD    | vs OP2 |     |
| ---- | ----- | --------- | ------ | ------ | --- |
| W16  | 18/30 | 38,810    | 23,867 | +25%   | 🔴   |

### Spend

| Week | Days  | Projected  | MTD        | vs OP2 |     |
| ---- | ----- | ---------- | ---------- | ------ | --- |
| W16  | 18/30 | $2,890,000 | $1,730,308 | +2%    | ✅   |

### CPA

| Week | Days  | Projected | OP2 |     |
| ---- | ----- | --------- | --- | --- |
| W16  | 18/30 | $74       | $91 | 🟢   |

### Rationale
- W16: 12 days remaining, 8 weekdays + 4 weekend. Blended W15-W16 daily rates (weekday ~1,335, weekend ~1,115) with small conservatism (weekday ~1,310) for NB CVR drifting back toward 5.5% rather than rebounding to the W14-W15 peak of 6.3%. No US holidays remaining (next is Memorial Day May 25). W16 NB CVR (5.89%) already showed reversion from W14-W15 (6.31-6.38%). If W17 NB CVR recovers to 6.0%+, April lands closer to 39,500 regs.

### Accuracy (after month closes)

| Week | Proj Regs | Actual | Error % | Weight | Wtd Error |
| ---- | --------- | ------ | ------- | ------ | --------- |
| —    | —         | —      | —       | —      | —         |

WMAPE: — | Calibration: —
