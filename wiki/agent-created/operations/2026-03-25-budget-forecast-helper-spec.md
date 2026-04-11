<!-- DOC-0424 | duck_id: tool-spec-budget-forecast-helper-spec -->
---
title: Budget Forecast Helper Spec
status: DRAFT
audience: amazon-internal
level: 3
owner: Richard Williams
created: 2026-03-25
updated: 2026-04-04
update-trigger: R&O cycle changes, dashboard ingester updates, OP2 plan refresh
---

# Budget Forecast Helper - Tool Spec

---

## Problem Statement

Every R&O (Revenue & Operations) cycle requires Richard to manually pull actuals from Google Ads, compare to the OP2 plan, calculate variance, and input into the finance spreadsheet. This process takes 30-60 minutes per cycle, recurs monthly (sometimes more frequently during budget reviews), and is error-prone because it involves manual data entry across multiple sources.

The errors matter. A wrong variance calculation can trigger unnecessary budget conversations with finance, or worse, mask a real overspend that should have been flagged. The process is also a time trap: it is low-leverage work (Level 1 admin, not Level 2 strategic) that consistently displaces higher-value tasks. The rw-tracker has flagged invoice and budget work as a recurring mediocrity pattern for 4+ weeks.

The dashboard ingester already reads the weekly WW Dashboard Excel export and generates per-market callout data. Extending it to produce R&O input values is a natural evolution — same input data, different output format.

---

## Proposed Solution

A Python script that extends the existing dashboard ingester to auto-generate R&O input values: MTD actuals vs OP2 plan, variance, and trend-based forecast for remaining months. The output is a summary table ready to paste into the finance template.

### Input

| Source | Format | Frequency | Notes |
|--------|--------|-----------|-------|
| WW Dashboard Excel | .xlsx (weekly drop) | Weekly | Same file the ingester already reads |
| OP2 plan numbers | Static config (entered once) | Per planning cycle | Per-market, per-month targets |
| Month boundaries | Derived from date | Automatic | Current month start/end dates |

The OP2 plan numbers are the only new input. Everything else is already available through the dashboard ingester pipeline.

### Output

The tool produces three outputs:

**1. Per-Market R&O Summary**

| Market | MTD Actuals | Projected Month-End | OP2 Plan | Variance | Variance % | Flag |
|--------|------------|--------------------|---------|---------|-----------|----|
| US | $2.1M | $2.7M | $2.5M | +$200K | +8% | |
| AU | $120K | $155K | $160K | -$5K | -3% | |
| MX | $52K | $68K | $55K | +$13K | +24% | OVER |

**2. Variance Flags**

Markets trending >10% over or under plan are flagged automatically. This is the early warning system — it surfaces the markets that need attention before finance asks.

**3. Trend Projection**

The projection uses a trailing 4-week average daily spend to estimate month-end:

```
Projected Month-End = MTD Actuals + (Avg Daily Spend x Remaining Days)
```

The trailing 4-week average is a conservative projection method. It will not predict spikes (promo events, seasonal surges) but it will not overproject either. For markets with known upcoming events (Prime Day, Hot Sale), Richard can apply a manual adjustment factor.

---

## Technical Design

### Architecture

```
WW Dashboard Excel (.xlsx)
    |
    v
Dashboard Ingester (existing)
    |
    v
Parsed market data (JSON)
    |
    v
Budget Forecast Module (NEW)
    |
    +---> R&O Summary Table (markdown or CSV)
    +---> Variance Flags (markdown)
    +---> Trend Projection (markdown)
```

The budget forecast module reads the same parsed JSON that the callout pipeline uses. No new data parsing required — just a new output format.

### OP2 Plan Configuration

OP2 plan numbers are stored in a simple config file:

```json
{
  "us": {"jan": 2500000, "feb": 2400000, "mar": 2600000},
  "au": {"jan": 150000, "feb": 160000, "mar": 155000},
  "mx": {"jan": 50000, "feb": 55000, "mar": 60000}
}
```

This file is entered once per planning cycle and updated only when OP2 is revised. It is the single source of truth for plan numbers — no more looking up targets in scattered spreadsheets.

### Projection Logic

```python
# Trailing 4-week average daily spend
avg_daily = sum(last_4_weeks_spend) / 28

# Remaining days in month
remaining = month_end_date - today

# Projection
projected_month_end = mtd_actuals + (avg_daily * remaining)

# Variance
variance = projected_month_end - op2_plan
variance_pct = variance / op2_plan * 100

# Flag
flag = "OVER" if variance_pct > 10 else "UNDER" if variance_pct < -10 else ""
```

---

## Validation Plan

Before declaring the tool ready for use:

| Test | Expected Result | Pass Criteria |
|------|----------------|---------------|
| March US data | Projected month-end within 5% of actual March close | Projection accuracy |
| March AU data | Projected month-end within 10% of actual March close | Smaller market = wider tolerance |
| Variance flags | US and MX flagged if >10% over/under | Flag logic correct |
| Edge case: month start (day 1-3) | Projection uses prior month's daily average | Handles insufficient MTD data |
| Edge case: promo week | Projection may overestimate if promo spend is temporary | Known limitation, documented |

---

## Blockers and Dependencies

| Dependency | Status | Impact |
|-----------|--------|--------|
| OP2 plan numbers per market per month | NOT AVAILABLE | Cannot calculate variance without plan baseline |
| Dashboard ingester (existing) | BUILT | Foundation is ready |
| March actuals for validation | AVAILABLE | Can validate immediately |

**The OP2 plan numbers are the blocker.** Without the plan baseline, the tool cannot calculate variance. Richard needs to get these from finance. This is a one-time data collection task, but it requires a finance contact to provide the numbers in a structured format.

---

## Impact Estimate

| Metric | Current | With Tool | Improvement |
|--------|---------|-----------|-------------|
| Time per R&O cycle | 30-60 min | 5 min (run script + review) | 85-90% reduction |
| Error rate | 1-2 per quarter (manual entry) | 0 (automated calculation) | 100% reduction |
| Proactive flagging | None (reactive to finance questions) | Automatic (>10% variance flagged) | New capability |
| Cycles per year | 12-15 | 12-15 | Same frequency, less effort |

Annual time savings: ~8-12 hours. More importantly, the proactive flagging changes the dynamic with finance from reactive ("why did you overspend?") to proactive ("MX is trending 24% over plan — here is why and here is the plan").

---

## Next Steps

1. [ ] Get OP2 plan numbers from finance (per market, per month) - THIS IS THE BLOCKER
2. [ ] Extend dashboard ingester to calculate MTD + projection
3. [ ] Test with March data (validate projection accuracy)
4. [ ] Share output format with finance for feedback
5. [ ] If adopted, add to morning routine as monthly trigger

---

## Sources
- Tool proposed in device.md - source: ~/shared/context/body/device.md -> Tool Factory -> #5 (proposed)
- Dashboard ingester as foundation - source: ~/shared/context/body/device.md -> Dashboard Ingester (BUILT)
- R&O as recurring admin task - source: ~/shared/context/body/hands.md -> Admin tasks (PAM R&O)
- Level 3 goal - source: ~/shared/context/body/brain.md -> Five Levels -> Level 3
- Invoice/budget work as mediocrity pattern - source: ~/shared/context/active/rw-tracker.md -> Mediocrity Patterns
- ie%CCP framework for budget context - source: ~/shared/artifacts/strategy/2026-03-30-ieccp-planning-framework.md

<!-- AGENT_CONTEXT
machine_summary: "Tool spec for a budget forecast helper that auto-generates R&O input values from the weekly dashboard Excel export. Extends the existing dashboard ingester. Produces per-market MTD actuals, projected month-end, variance vs OP2, and automatic flags for markets >10% over/under plan. Blocked on OP2 plan numbers from finance. Saves 30-60 min per R&O cycle and eliminates manual entry errors. Changes finance dynamic from reactive to proactive."
key_entities: ["R&O", "OP2", "dashboard ingester", "budget forecast", "finance template", "variance flags", "trailing 4-week average"]
action_verbs: ["calculate", "project", "flag", "extend", "validate"]
update_triggers: ["R&O cycle changes", "dashboard ingester updates", "OP2 plan refresh", "tool built"]
-->
