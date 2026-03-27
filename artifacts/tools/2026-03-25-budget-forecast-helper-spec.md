---
title: Budget Forecast Helper Spec
status: DRAFT
audience: amazon-internal
level: 3
owner: Richard Williams
created: 2026-03-25
updated: 2026-03-25
update-trigger: R&O cycle changes, dashboard ingester updates, OP2 plan refresh
---

# Budget Forecast Helper — Tool Spec

---

## Problem

Every R&O cycle requires Richard to manually pull actuals from Google Ads, compare to plan, calculate variance, and input into the finance spreadsheet. This is recurring, low-leverage, and error-prone.

## Proposed Solution

A script that takes the weekly dashboard Excel export and auto-generates R&O input values: actuals vs plan, variance, trend-based forecast for remaining months.

## Input
- WW Dashboard Excel (weekly drop)
- OP2 plan numbers (static, entered once)
- Month boundaries

## Output
- Per-market: MTD actuals, projected month-end, variance vs OP2
- Summary table ready to paste into finance template
- Flags: markets trending >10% over/under plan

## Logic
1. Sum weekly actuals within the current month
2. Project remaining days using trailing 4-week average daily spend
3. Compare projected month-end to OP2 plan
4. Flag variances >10%

This eliminates 30-60 minutes of manual work per R&O cycle and reduces error risk. The trailing 4-week average is a conservative projection method — it won't predict spikes but it won't overproject either.

## Implementation
- Python script extending the existing dashboard ingester
- Input: same Excel format the ingester already reads
- Output: R&O summary table (markdown or CSV)

## Next Steps
- [ ] Define OP2 plan numbers per market per month
- [ ] Extend ingester to calculate MTD + projection
- [ ] Test with March data
- [ ] Share output format with finance for validation

Step 1 (OP2 numbers) is the blocker. Without the plan baseline, the tool can't calculate variance. Get this from finance first.


## Sources
- Tool proposed in device.md — source: ~/shared/context/body/device.md → Tool Factory → #5 (proposed)
- Dashboard ingester as foundation — source: ~/shared/context/body/device.md → Dashboard Ingester (BUILT)
- R&O as recurring admin task — source: ~/shared/context/body/hands.md → Admin tasks (PAM R&O)
- Level 3 goal — source: ~/shared/context/body/brain.md → Five Levels → Level 3

<!-- AGENT_CONTEXT
machine_summary: "Tool spec for a budget forecast helper that auto-generates R&O input values from the weekly dashboard Excel export. Extends the existing dashboard ingester. Blocked on OP2 plan numbers from finance. Saves 30-60 min per R&O cycle."
key_entities: ["R&O", "OP2", "dashboard ingester", "budget forecast", "finance template", "variance flags"]
action_verbs: ["calculate", "project", "flag", "extend", "validate"]
update_triggers: ["R&O cycle changes", "dashboard ingester updates", "OP2 plan refresh", "tool built"]
-->
