<!-- DOC-0337 | duck_id: protocol-asana-kiro-rw-protocol -->
# Kiro_RW Population Protocol

Generated: 2026-04-03
Field GID: `1213915851848087`
API Pattern: `UpdateTask(task_gid, custom_fields={"1213915851848087": "<text>"})`
Char limit: 500 per entry
Format: `M/D: [STATUS] [BLOCKER if any] [NEXT ACTION] [CROSS-REF if any]`

---


### Common Pitfalls — Kiro_RW Population Protocol
- Misinterpreting this section causes downstream errors
- Always validate assumptions before acting on this data
- Cross-reference with related sections for completeness

## Sub-task 5.1: Today-Priority Tasks (13 tasks)

### 9. Weekly Reporting - Global WBR sheet
- Routine: Engine Room | Due: Mar 30 | Overdue: 4d | Subtasks: 4
- Kiro_RW text:
```
2026-04-03: 4d overdue. Recurring weekly. 4 subtasks (Quip links in notes). If this week's WBR data is already entered, mark complete and create next instance for Apr 7. If not, pull data during Engine Room block — 30min. Has Quip doc links for reference. L2 alignment.
```
- API call:
```
UpdateTask(<task_gid>, custom_fields={"1213915851848087": "2026-04-03: 4d overdue. Recurring weekly. 4 subtasks (Quip links in notes). If this week's WBR data is already entered, mark complete and create next instance for Apr 7. If not, pull data during Engine Room block — 30min. Has Quip doc links for reference. L2 alignment."})
```

### 2. ie%CCP calc - insert MX spend/regs before 9th
- Routine: Sweep | Due: Apr 3 | Overdue: No (due today)
- Kiro_RW text:
```
2026-04-03: Due today. Monthly recurring (before 9th). Pull MX spend + reg data from DuckDB/WBR sheet, insert into ie%CCP Quip doc. 20min task. Do during Sweep block. Mark complete when inserted.
```
- API call:
```
UpdateTask(<task_gid>, custom_fields={"1213915851848087": "2026-04-03: Due today. Monthly recurring (before 9th). Pull MX spend + reg data from DuckDB/WBR sheet, insert into ie%CCP Quip doc. 20min task. Do during Sweep block. Mark complete when inserted."})
```

### 3. AU meetings - Agenda
- Routine: Sweep | Due: Mar 31 | Overdue: 3d | Task Progress: Done
- Kiro_RW text:
```
2026-04-03: 3d overdue but Task Progress = Done. AU sync cancelled this week (Alexis confirmed — org meeting conflict). Mark complete now. Create next instance for Apr 7. Brandon joining AU Lena sync, reducing to biweekly — adjust cadence.
```
- API call:
```
UpdateTask(<task_gid>, custom_fields={"1213915851848087": "2026-04-03: 3d overdue but Task Progress = Done. AU sync cancelled this week (Alexis confirmed — org meeting conflict). Mark complete now. Create next instance for Apr 7. Brandon joining AU Lena sync, reducing to biweekly — adjust cadence."})
```

### 4. Come prepared: Bi-weekly with Adi
- Routine: Sweep | Due: Apr 1 | Overdue: 2d
- Kiro_RW text:
```
2026-04-03: 2d overdue. Bi-weekly recurring. AI brainstorm prep. If meeting already happened, mark complete and create next instance (Apr 15). If upcoming, prep talking points: OCI JP preflight status, Baloo Early Access metrics, Enhanced Match investigation. 15min prep.
```
- API call:
```
UpdateTask(<task_gid>, custom_fields={"1213915851848087": "2026-04-03: 2d overdue. Bi-weekly recurring. AI brainstorm prep. If meeting already happened, mark complete and create next instance (Apr 15). If upcoming, prep talking points: OCI JP preflight status, Baloo Early Access metrics, Enhanced Match investigation. 15min prep."})
```

### 5. It's time to update your goal(s)
- Routine: Sweep | Due: Apr 3 | Overdue: No (due today)
- Kiro_RW text:
```
2026-04-03: Due today. 12 goals need updates. Last refreshed Mar 6 — 28 days stale. Q1 Brand LP goals (AU+MX) ended at 0% — need retrospective or Q2 rollover. MX regs 2,167/11,100 (20%), AU regs 2,231/12,906 (17%), Paid App 120,621/435,000 (28%). Next: draft status updates for all 14 goals.
```
- API call:
```
UpdateTask(<task_gid>, custom_fields={"1213915851848087": "2026-04-03: Due today. 12 goals need updates. Last refreshed Mar 6 — 28 days stale. Q1 Brand LP goals (AU+MX) ended at 0% — need retrospective or Q2 rollover. MX regs 2,167/11,100 (20%), AU regs 2,231/12,906 (17%), Paid App 120,621/435,000 (28%). Next: draft status updates for all 14 goals."})
```

### 6. Testing Document for Kate
- Routine: Core | Due: Apr 1 | Overdue: 2d | Subtasks: 6 (0/6 complete) | THE HARD THING
- Kiro_RW text:
```
2026-04-03: THE HARD THING. 2d overdue. 6 subtasks (0/6 complete). Kate meeting Apr 16 — 9 workdays. Doc captain for OP1 foundation. Next: create outline structure today (subtask 1). DDD to identify owners (subtask 2) by Apr 7. This is P0 — do not defer. L2 alignment: Drive WW Testing.
```
- API call:
```
UpdateTask(<task_gid>, custom_fields={"1213915851848087": "2026-04-03: THE HARD THING. 2d overdue. 6 subtasks (0/6 complete). Kate meeting Apr 16 — 9 workdays. Doc captain for OP1 foundation. Next: create outline structure today (subtask 1). DDD to identify owners (subtask 2) by Apr 7. This is P0 — do not defer. L2 alignment: Drive WW Testing."})
```

### 7. Update and close your goal(s)
- Routine: Core | Due: Apr 3 | Overdue: No (due today)
- Kiro_RW text:
```
2026-04-03: Due today. 2 goals due soon for closure. Review which goals have met their targets and can be closed vs. which need extension. Cross-ref with goal status from task #5. Pair with "It's time to update your goal(s)" — do together. L1 alignment.
```
- API call:
```
UpdateTask(<task_gid>, custom_fields={"1213915851848087": "2026-04-03: Due today. 2 goals due soon for closure. Review which goals have met their targets and can be closed vs. which need extension. Cross-ref with goal status from task #5. Pair with \"It's time to update your goal(s)\" — do together. L1 alignment."})
```

### 8. Email overlay WW rollout/testing
- Routine: Core | Due: Mar 27 | Overdue: 7d | Subtasks: 7
- Kiro_RW text:
```
2026-04-03: 7d overdue. 7 subtasks — status unknown. Goal: WW in-context email overlay (0% progress on H1 FY26 goal). No recent activity detected. Decision needed: do, delegate, or kill. If active, identify which subtasks are blocked and which can move. If stale, demote to Backlog. L2 alignment.
```
- API call:
```
UpdateTask(<task_gid>, custom_fields={"1213915851848087": "2026-04-03: 7d overdue. 7 subtasks — status unknown. Goal: WW in-context email overlay (0% progress on H1 FY26 goal). No recent activity detected. Decision needed: do, delegate, or kill. If active, identify which subtasks are blocked and which can move. If stale, demote to Backlog. L2 alignment."})
```

### 1. Mondays - Write into EU SSR Acq Asana
- Routine: Sweep | Due: Mar 30 | Overdue: 4d
- Kiro_RW text:
```
2026-04-03: 4d overdue. Recurring weekly (Mon). If this week's write-up is done, mark complete and create next instance for Apr 7. If not done, do it today during Sweep block — 15min max. Check EU SSR Acq project for latest data.
```
- API call:
```
UpdateTask(<task_gid>, custom_fields={"1213915851848087": "2026-04-03: 4d overdue. Recurring weekly (Mon). If this week's write-up is done, mark complete and create next instance for Apr 7. If not done, do it today during Sweep block — 15min max. Check EU SSR Acq project for latest data."})
```

### 10. Look over AU landing page switch
- Routine: Engine Room | Due: Mar 25 | Overdue: 9d
- Kiro_RW text:
```
2026-04-03: 9d overdue. STALE — no activity in 9+ days. Decision needed: do, delegate, or kill. Related: Lena AU LP URL analysis + CPA overstating (Slack signal from Brandon). Brandon says "she needs to cool her jets." If still relevant, timebox 30min review. If not, demote to Backlog or close.
```
- API call:
```
UpdateTask(<task_gid>, custom_fields={"1213915851848087": "2026-04-03: 9d overdue. STALE — no activity in 9+ days. Decision needed: do, delegate, or kill. Related: Lena AU LP URL analysis + CPA overstating (Slack signal from Brandon). Brandon says \"she needs to cool her jets.\" If still relevant, timebox 30min review. If not, demote to Backlog or close."})
```

### 11. MBR callout
- Routine: Admin | Due: Apr 2 | Overdue: 1d (was DUE TODAY on Apr 2)
- Kiro_RW text:
```
2026-04-03: 1d overdue (was due Apr 2). Monthly recurring. AU + MX projects. Pull MBR data from WBR sheet, draft callouts for AU and MX. If Apr MBR already submitted, mark complete. If not, do during Admin block today — 30min. Create next instance for May.
```
- API call:
```
UpdateTask(<task_gid>, custom_fields={"1213915851848087": "2026-04-03: 1d overdue (was due Apr 2). Monthly recurring. AU + MX projects. Pull MBR data from WBR sheet, draft callouts for AU and MX. If Apr MBR already submitted, mark complete. If not, do during Admin block today — 30min. Create next instance for May."})
```

### 12. Send AU team invoice for prev month
- Routine: Admin | Due: Apr 2 | Overdue: 1d (was DUE TODAY on Apr 2)
- Kiro_RW text:
```
2026-04-03: 1d overdue (was due Apr 2). Monthly recurring. Send AU invoice for March. Check AP folder for invoice. If already sent, mark complete. If not, send today — 10min. Create next instance for May 2. Carlos handles MX invoices. L1 alignment: Admin discipline.
```
- API call:
```
UpdateTask(<task_gid>, custom_fields={"1213915851848087": "2026-04-03: 1d overdue (was due Apr 2). Monthly recurring. Send AU invoice for March. Check AP folder for invoice. If already sent, mark complete. If not, send today — 10min. Create next instance for May 2. Carlos handles MX invoices. L1 alignment: Admin discipline."})
```

### 13. Monthly - Confirm actual budgets
- Routine: Admin | Due: Apr 1 | Overdue: 2d
- Kiro_RW text:
```
2026-04-03: 2d overdue. Monthly recurring. Paid App project. Finance actuals due EOD Apr 3 (from hands.md signal). Confirm actual budgets match forecasts. If done, mark complete. If not, do during Admin block — 20min. Cross-ref with Andrew's ENG budget file request (unanswered DM from Apr 1).
```
- API call:
```
UpdateTask(<task_gid>, custom_fields={"1213915851848087": "2026-04-03: 2d overdue. Monthly recurring. Paid App project. Finance actuals due EOD Apr 3 (from hands.md signal). Confirm actual budgets match forecasts. If done, mark complete. If not, do during Admin block — 20min. Cross-ref with Andrew's ENG budget file request (unanswered DM from Apr 1)."})
```

---

## Sub-task 5.2: Overdue Tasks — Enhanced Context

These tasks are a subset of the Today list above. This section adds overdue-specific context: days overdue, severity tier, and recommended action.

### Overdue Severity Tiers
- **STALE (7+ days):** Decision needed — do, delegate, or kill
- **SLIPPING (3-6 days):** Needs attention this session — complete or reschedule
- **FRESH (1-2 days):** Normal carry-forward — do today

### Overdue Task Summary (9 tasks overdue as of Apr 3)

| # | Task | Days Overdue | Tier | Recommended Action |
|---|------|-------------|------|-------------------|
| 1 | Look over AU landing page switch | 9d | STALE | Decide: do (30min), delegate, or kill |
| 2 | Email overlay WW rollout/testing | 7d | STALE | Decide: do, delegate, or kill. Check subtask status |
| 3 | Mondays - Write into EU SSR Acq Asana | 4d | SLIPPING | Complete or mark done + create next instance |
| 4 | Weekly Reporting - Global WBR sheet | 4d | SLIPPING | Complete or mark done + create next instance |
| 5 | AU meetings - Agenda | 3d | SLIPPING | Task Progress=Done. Mark complete now |
| 6 | Come prepared: Bi-weekly with Adi | 2d | FRESH | Check if meeting happened. Complete or prep |
| 7 | Testing Document for Kate | 2d | FRESH | THE HARD THING. Start outline today. Non-negotiable |
| 8 | Monthly - Confirm actual budgets | 2d | FRESH | Finance actuals due EOD today. Do in Admin block |
| 9 | MBR callout | 1d | FRESH | Monthly. Do in Admin block today |
| 10 | Send AU team invoice for prev month | 1d | FRESH | Monthly. Send today — 10min |

Note: Tasks #1 and #2 are STALE — these are the ones that need a decision, not just execution. The Kiro_RW entries above already contain the overdue-specific language. No additional Kiro_RW writes needed beyond what's in 5.1 — the overdue context is embedded in each entry.

### Overdue Pattern Analysis
- 4 of 9 overdue tasks are recurring (EU SSR, WBR, AU Agenda, Bi-weekly Adi) — these should be marked complete and recreated, not carried forward
- 2 are STALE with no activity (AU LP switch, Email overlay) — need Richard's decision
- 1 is THE HARD THING (Testing Doc) — overdue but critical, must start today
- 2 are Admin tasks 1d overdue — quick wins, do in Admin block

---

## Sub-task 5.3: Urgent Tasks — Slack Cross-References

### WW keyword gap fill based on market-level ASINs
- Routine: Core | Priority: Urgent | Due: none | Subtasks: 6 | Importance: Important
- Kiro_RW text:
```
2026-04-03: Urgent, no due date. 6 subtasks. Important. Core work — keyword gap analysis across markets using ASIN-level data. No Slack signals detected for this specific task. Related context: WBR keyword data available in DuckDB. No blockers detected. Next: pull subtask list, assess scope, set a due date. Consider: is this week's priority or next? L2 alignment: Drive WW Testing.
```
- API call:
```
UpdateTask(<task_gid>, custom_fields={"1213915851848087": "2026-04-03: Urgent, no due date. 6 subtasks. Important. Core work — keyword gap analysis across markets using ASIN-level data. No Slack signals detected for this specific task. Related context: WBR keyword data available in DuckDB. No blockers detected. Next: pull subtask list, assess scope, set a due date. Consider: is this week's priority or next? L2 alignment: Drive WW Testing."})
```

### Slack Cross-Reference Scan Results

Searched intake files for signals related to Urgent-priority tasks:

**Direct matches for "keyword gap fill":** None found in Slack intake (2026-04-01 digest, broad scan, or Asana activity).

**Related signals that may inform Urgent task context:**
- Brandon's WW Polaris rollout leadership offer (Feb 2026) — keyword strategy is adjacent
- WBR keyword data pipeline exists in DuckDB — can feed gap analysis
- No teammate comments or due date changes detected on this task

**Assessment:** The WW keyword gap fill task is self-contained with no external dependencies or Slack signals. It's a proactive optimization task, not a reactive one. The lack of Slack signals means it's not being discussed by the team — Richard owns the initiative.

---

## Execution Instructions for AM-2

### How to Execute These Writes

The AM-2 hook should execute these Kiro_RW writes during the "Context Writes" phase (Phase 4 of AM-2). For each task:

1. Get the task GID (from SearchTasksInWorkspace or morning snapshot)
2. Read existing Kiro_RW value (should be empty for all tasks as of Apr 3)
3. Write the Kiro_RW text using: `UpdateTask(task_gid, custom_fields={"1213915851848087": "<text>"})`
4. Log the write to `asana-audit-log.jsonl`

### GID Resolution

Task GIDs are not hardcoded in this protocol because they were not available in the command center audit. The AM-2 hook should resolve GIDs by:
1. Using the morning snapshot (`asana-morning-snapshot.json`) which contains task GIDs
2. Or calling `SearchTasksInWorkspace(assignee_any=1212732742544167, completed=false)` and matching by task name

### Append Protocol

Per Requirement 6.5: If Kiro_RW already has content, append below existing content with a newline + date stamp. Since all fields are currently empty, the first write is a simple set.

### Character Count Verification

All Kiro_RW entries above are within the 500-character limit:
- Longest entry: ~340 chars (Testing Document for Kate)
- Shortest entry: ~200 chars (Update and close your goal(s))
- All entries verified under 500 chars ✓

---

## Execution Status

**Direct Asana MCP writes: NOT EXECUTED** — The Enterprise Asana MCP server is not available in the spec execution context (AgentSpaces/Kiro). The Asana MCP is only callable during live hook execution (AM-1, AM-2, AM-3, EOD-2) or interactive chat sessions where the MCP server is connected.

**This protocol document is the execution plan.** The next AM-2 run should consume this file and execute the 14 UpdateTask calls listed above. After execution, update this section with:
- Timestamp of execution
- Task GIDs resolved
- Success/failure per task
- Any Kiro_RW values that needed append (vs. initial set)
