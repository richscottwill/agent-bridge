# AM-Frontend Protocol — Brief + Triage + Command Center

Interactive phase. Reads pre-computed state from AM-Backend. Presents everything to Richard. Executes approved writes.

All Asana writes follow the Guardrail Protocol in asana-command-center.md § Guardrail Protocol.

---

## Context Load
body.md, spine.md, org-chart.md, rw-trainer.md, rw-task-prioritization.md, brain.md, eyes.md, device.md, gut.md, rw-tracker.md, hands.md, amcc.md, memory.md, richard-writing-style.md, asana-command-center.md.

Pre-computed state files (from AM-Backend):
- `~/shared/context/active/am-enrichment-queue.json`
- `~/shared/context/active/am-portfolio-findings.json`
- `~/shared/context/active/am-abps-ai-state.json`
- `~/shared/context/active/am-signals-processed.json`
- `~/shared/context/intake/slack-digest.md`
- `~/shared/context/intake/email-triage.md`
- `~/shared/context/intake/asana-digest.md`
- `~/shared/context/intake/asana-activity.md`

---

## Step 1: Daily Brief

### Brief Structure
1. TRAINER CHECK-IN
2. HEADS UP
3. SLACK OVERNIGHT
4. TODAY (from Asana)
5. SPEC SHEET
6. T-MINUS
7. aMCC
8. SYSTEM HEALTH

### TODAY Section (from DuckDB)
- Query: `SELECT * FROM asana_by_routine` → bucket counts
- Query: `SELECT * FROM asana_overdue ORDER BY days_overdue DESC` → overdue list
- Query: `SELECT * FROM asana_tasks WHERE priority_rw = 'Today' AND completed = FALSE AND deleted_at IS NULL ORDER BY routine_rw` → Today tasks
- Query: `SELECT * FROM asana_completion_rate` → trailing completion stats

Display:
- 🧹 Sweep: Routine=Sweep AND Priority_RW=Today. Name + due date + L1-L5 tag.
- 🎯 Core: Routine=Core AND Priority_RW=Today. THE HARD THING gets first slot.
- ⚙️ Engine Room: Routine=Engine Room AND Priority_RW=Today.
- 📋 Admin: Routine=Admin AND Priority_RW=Today.
- ⚠️ Overdue: Count + oldest task + days overdue.
- 📦 Needs Triage: Tasks with no Routine set.
- Bucket counts: Sweep X/5, Core X/4, Engine Room X/6, Admin X/3.

### Coherence Alerts
Include flags from AM-Backend coherence check. If zero: "✅ DuckDB ↔ Body coherence check passed."

### Five Levels Annotation
[L1]-[L5] tag per asana-command-center.md mapping.

### Activity Signals
Read intake/asana-activity.md: 💬 comments, 📅 due date changes, 👤 reassignments.

### Goal Alerts
If any goals at-risk or off-track: goal name, status, metric gap, recommended action.

### ABPS AI Document Factory
Read am-abps-ai-state.json: Intake count, In Progress pipeline stages, Review status, Active count, Archive count, alerts.

### Portfolio Status
Read am-portfolio-findings.json:
- Per-project: task count, overdue, near-due, health color, staleness.
- Budget Tasks: ⚡ if due within 3d, 🔴 CRITICAL if overdue.
- Cross-team blockers.

### Meeting Prep
For each meeting today, query signal_tracker for attendee topics (last 7 days). Include: "Brandon's hot topics: [list]."

### Friday Additions
- Calibration.
- Remind Agent Bridge Sync.


---

## Step 2: Output Channels

### Email Brief (AUTO-SEND)
Dark navy HTML email to prichwil@amazon.com. Full brief content formatted as styled HTML.

### Slack Brief
Post to rsw-channel (C0993SRL6FQ). Include Asana task context inline.

### Dashboard Update
Edit pinned message in rsw-channel.

### Calendar Blocks
Create time blocks via Outlook MCP calendar_meeting(operation='create'):
- Sweep: 15min × count
- Core: 45min × count
- Engine Room: 20min × count
- Admin: 15min × count
- Min 30min, max 3h per block.
- Flag overload if total exceeds available time.
- Skip blocks that overlap existing meetings.

### Proactive Drafts
Query DuckDB for unanswered signals 24h+. Generate drafts to ~/shared/context/intake/drafts/.

---

## Step 3: Enrichment Batch Presentation

Read am-enrichment-queue.json. Present all proposals for approval.

### My Tasks Enrichment
```
📝 MY TASKS ENRICHMENT — [N] task(s) need field updates:

- [task name] (GID: [gid])
  - Kiro_RW: [proposed] (currently: [empty or value])
  - Next action: [proposed] (currently: empty)
  - Begin Date: [YYYY-MM-DD] (currently: unset)
  - Priority_RW: Not urgent (currently: empty)
- ACTION: Approve all, approve individually, or skip?
```

### Portfolio Enrichment
```
📝 PORTFOLIO ENRICHMENT — [N] task(s) need field updates:
  [grouped by project, same format as My Tasks]
```

### Execute Approved Enrichments
Combine all field writes into one UpdateTask per task. Log each to asana-audit-log.jsonl. On API failure → log → retry once → skip and flag.

---

## Step 4: ABPS AI Triage

Read am-abps-ai-state.json. Present untriaged Intake tasks for approval.

```
📥 ABPS AI Intake — [N] untriaged task(s):

- TASK: [name] (GID: [gid])
  - Routine: [bucket]
  - Priority_RW: [level]
  - Frequency: [cadence]
  - Work_Product: [type]
  - Begin Date: [YYYY-MM-DD]
  - Due Date: [YYYY-MM-DD]
  - Scope: [one sentence]
- ACTION: Approve, adjust, or skip?
```

### Execute Approved Triage
Set fields via UpdateTask. Apply date defaults. Section moves. Research subtask creation. Pipeline advancement (Steps 3B–3K from original am-triage.md Phase 1B).

---

## Step 5: Portfolio Findings + Alerts

Read am-portfolio-findings.json. Present:

```
📊 PORTFOLIO SCAN — [N] projects scanned:

[Portfolio Name] ([N] projects):
  - [Project]: [task_count] tasks ([overdue] overdue, [near_due] near-due)
    Status: [🟢/🟡/🔴] (last update: [date] — [stale/current])
    Enrichment needed: [N] tasks missing fields

⚠️ PORTFOLIO ALERTS:
  - Near-due: [tasks with project context]
  - Overdue: [tasks with project context]
  - Stale projects: [list with days since last update]
  - Cross-team blockers: [MX blockers]
  - Budget: [budget task alerts]
  - Recurring: [auto-creation proposals]
  - Event countdown: [Paid App escalation proposals]
```

### Overdue Kill-or-Revive Decisions
Present overdue tasks grouped by severity (30+d, 20-29d, 10-19d, 1-9d). For each: extend, kill, or delegate?

### Recurring Task Approval
Present auto-created recurring task proposals: 'Auto-created next [name] due [date]. Approve?' Delete if rejected.

---

## Step 6: Interactive Command Center

Present the curated task board. Execute Richard's directions in real-time.

### Supported Operations
- Move tasks between Routine buckets
- Change due dates
- Change Priority_RW (Today/Urgent/Not urgent)
- Create new tasks with Routine + Priority pre-set
- Write/update task descriptions (notes or html_notes)
- Add comments (CreateTaskStory)
- Complete tasks
- Create subtasks
- Set Importance_RW

### Agent-Initiated Proposals
Propose changes based on: overdue tasks, bucket overflows, untriaged items, stale tasks, due date conflicts. Richard approves, modifies, or gives new directions.

---

## Step 7: Triage Summary

Post summary to Richard's Slack DM:
```
self_dm(login="prichwil", text="📬 AM Triage Complete
• New tasks: [N] (from [sources])
• Updated tasks: [N] (new signals on existing)
• Enriched: [N] tasks with field updates
• Deferred: [N] (low priority, backlog)
• Dismissed: [N] (FYI only)")
```

---

## Log Hook Execution
```sql
INSERT INTO hook_executions (hook_name, execution_date, start_time, end_time, duration_seconds,
    phases_completed, asana_reads, asana_writes, slack_messages_sent, duckdb_queries, summary)
VALUES ('am-frontend', CURRENT_DATE, '[start]', '[end]', [duration],
    [phases], [reads], [writes], [slack_msgs], [queries], '[summary]');
```
