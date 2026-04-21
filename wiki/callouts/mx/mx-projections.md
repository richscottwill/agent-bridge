---
title: "MX Monthly Projections"
status: FINAL
audience: amazon-internal
owner: Richard Williams
created: 2026-04-12
updated: 2026-04-12
---
<!-- DOC-0080 | duck_id: callout-mx-projections -->

# MX Monthly Projections

Tracks weekly projections vs actuals. Updated each week by the analyst agents.
Calibration: Weighted MAPE (weight = days_elapsed / total_days). Score = 1 - WMAPE.
Indicators: ✅ within 5% | 🟢 beating CPA target | 🔴 outside 5%

---

## Mar 2026

OP2: 859 regs | $56,562 spend | $66 CPA

### Registrations

| Week | Days  | Projected | MTD   | vs OP2 |     |
| ---- | ----- | --------- | ----- | ------ | --- |
| W12  | 21/31 | 1,441     | 1,021 | +68%   | 🔴   |
| W13  | 28/31 | 1,500     | 1,370 | +75%   | 🔴   |

### Spend

| Week | Days  | Projected | MTD     | vs OP2 |     |
| ---- | ----- | --------- | ------- | ------ | --- |
| W12  | 21/31 | $90,000   | $63,104 | +59%   | 🔴   |
| W13  | 28/31 | $96,000   | $86,000 | +70%   | 🔴   |

### CPA

| Week | Days  | Projected | OP2 |     |
| ---- | ----- | --------- | --- | --- |
| W12  | 21/31 | $63       | $66 | ✅   |
| W13  | 28/31 | $64       | $66 | ✅   |

### Rationale
- W12: W12 daily rates (wkday 50, wkend 30) after W11 spike normalization. ie%CCP at 90%, on track for 95-100% EOM.
- W13 (analyst-adjusted): W12-W13 blended daily rates (Sat ~30, Sun ~45, Mon ~50). 3 remaining days est 125 regs. ie%CCP at 99% for W13, effectively at 100% ceiling. $96K/$1,500 = $64 CPA, $2 below OP2 target.

### Accuracy (after month closes)

| Week | Proj Regs | Actual | Error % | Weight | Wtd Error |
| ---- | --------- | ------ | ------- | ------ | --------- |
| —    | —         | —      | —       | —      | —         |

WMAPE: — | Calibration: —

---

## Apr 2026

OP2: 791 regs | $35,085 spend | $44 CPA

### Registrations

| Week | Days  | Projected | MTD   | vs OP2 |     |
| ---- | ----- | --------- | ----- | ------ | --- |
| W16  | 18/30 | 2,000     | 1,205 | +153%  | 🔴   |

### Spend

| Week | Days  | Projected | MTD     | vs OP2 |     |
| ---- | ----- | --------- | ------- | ------ | --- |
| W16  | 18/30 | $107,000  | $62,836 | +205%  | 🔴   |

### CPA

| Week | Days  | Projected | OP2 |     |
| ---- | ----- | --------- | --- | --- |
| W16  | 18/30 | $54       | $44 | 🔴   |

### Rationale
- W16 (market-analyst, 2026-04-20): W15-W16 blended daily rates — weekday 84.4 regs/$4,070 (10 pts), weekend 41.2 regs/$2,833 (5 pts) — applied to 12 remaining days (8 weekdays + 4 weekend, no MX holidays; May 1 is W18). Pure model yields 2,045 regs / $106.7K. Trimmed regs ~2% to 2,000 to reflect Sat 4/18 softness (31 regs) and 3-week NB CVR decline (1.47% → 1.38% → 1.32% → 1.13%). Spend held at $107K (NB will keep buying clicks at similar rate even if CVR softens). CPA $54 vs $44 OP2 — above target, but the relevant frame is +205% spend / +153% regs vs OP2 at 70% ie%CCP. OP2 predates Brand coverage scaling and is no longer the planning number for MX.

### Accuracy (after month closes)

| Week | Proj Regs | Actual | Error % | Weight | Wtd Error |
| ---- | --------- | ------ | ------- | ------ | --------- |
| —    | —         | —      | —       | —      | —         |

WMAPE: — | Calibration: —
