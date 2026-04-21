---
title: "JP Monthly Projections"
status: FINAL
audience: amazon-internal
owner: Richard Williams
created: 2026-04-12
updated: 2026-04-12
---
<!-- DOC-0069 | duck_id: callout-jp-projections -->

# JP Monthly Projections

Tracks weekly projections vs actuals. Updated each week by the analyst agents.
Calibration: Weighted MAPE (weight = days_elapsed / total_days). Score = 1 - WMAPE.
Indicators: ✅ within 5% | 🟢 beating CPA target | 🔴 outside 5%

---

## Mar 2026

OP2: 2,360 regs | $164,435 spend | $70 CPA

### Registrations

| Week | Days  | Projected | MTD   | vs OP2 |     |
| ---- | ----- | --------- | ----- | ------ | --- |
| W12  | 21/31 | 2,020     | 1,502 | -14%   | 🔴   |
| W13  | 28/31 | 2,250     | 2,035 | -5%    | 🔴   |

### Spend

| Week | Days  | Projected | MTD      | vs OP2 |     |
| ---- | ----- | --------- | -------- | ------ | --- |
| W12  | 21/31 | $160,000  | $114,112 | -3%    | ✅   |
| W13  | 28/31 | $175,000  | $162,000 | +7%    | 🔴   |

### CPA

| Week | Days  | Projected | OP2 |     |
| ---- | ----- | --------- | --- | --- |
| W12  | 21/31 | $79       | $70 | 🔴   |
| W13  | 28/31 | $78       | $70 | 🔴   |

### Rationale
- W12: Fiscal year-end suppression: -15% weekdays Mar 24-28, -25% Mar 31. MHLW gap structural. Competitors adding Brand click pressure.
- W13: W13 was post-MHLW high watermark (557 regs). 3 remaining days (1 weekend, 2 weekday). Mar 31 fiscal year-end: -40% suppression applied. Mon Mar 30: -15% pre-close softness. Spend surged +30% WoW on budget increases; CPA flat at $85 despite volume recovery.

### Accuracy (after month closes)

| Week | Proj Regs | Actual | Error % | Weight | Wtd Error |
| ---- | --------- | ------ | ------- | ------ | --------- |
| —    | —         | —      | —       | —      | —         |

WMAPE: — | Calibration: —


---

## Apr 2026

OP2: 1,920 regs | $144,561 spend | $75 CPA

### Registrations

| Week | Days  | Projected | MTD   | vs OP2 |     |
| ---- | ----- | --------- | ----- | ------ | --- |
| W16  | 18/30 | 2,470     | 1,498 | +29%   | 🟢   |

### Spend

| Week | Days  | Projected | MTD      | vs OP2 |     |
| ---- | ----- | --------- | -------- | ------ | --- |
| W16  | 18/30 | $165,000  | $100,796 | +14%   | 🔴   |

### CPA

| Week | Days  | Projected | OP2 |     |
| ---- | ----- | --------- | --- | --- |
| W16  | 18/30 | $67       | $75 | 🟢   |

### Rationale
- W16: Post-FY normalization continuing. MTD anchored to `ps.v_monthly` (1,498 regs / $100,796 through Apr 18). W15-W16 weekday avg ~95 regs/$6.5K, weekend ~46 regs/$2.5K. 12 days remaining: 7 clean weekdays + 1 GW bridge (Apr 30, -5%) + Apr 29 Showa Day (-18%, LY W18 measured -18.6%) + 3 weekends. Brand CPC falling -10% WoW two weeks running, expected to hold through W17. JP pacing +29% vs OP2 regs at -11% vs OP2 CPA. Golden Week W18 falls in May.

### Accuracy (after month closes)

| Week | Proj Regs | Actual | Error % | Weight | Wtd Error |
| ---- | --------- | ------ | ------- | ------ | --------- |
| —    | —         | —      | —       | —      | —         |

WMAPE: — | Calibration: —
