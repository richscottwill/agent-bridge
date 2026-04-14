<!-- DOC-0328 | duck_id: protocol-am-backend -->
# AM-Backend Protocol — Autonomous Data Collection + Processing

Fully autonomous. No interaction needed. Produces structured output files consumed by AM-Frontend.

All Asana writes follow the Guardrail Protocol in asana-command-center.md § Guardrail Protocol.

---

## Context Load
spine.md, current.md, slack-channel-registry.json, slack-scan-state.json, asana-command-center.md.

---

## Phase 1: Data Collection

Pure data collection. No drafting, no decisions, no organ writes.

### DuckDB Schema Verification
Run `~/shared/context/protocols/duckdb-schema-verification.md` quick check:
1. `SELECT current_database(), current_schema()` → must be `ps_analytics`, `main`
2. `SELECT database_name, type FROM duckdb_databases() WHERE database_name = 'ps_analytics'` → type must be `motherduck`
3. Quick table count: 46 tables + 39 views expected
4. If any missing → run ensure-schema.sql statements for missing tables
5. If database type is not `motherduck` → STOP and flag: MCP server not connected to MotherDuck

### Slack Scan
1. list_channels (unreadOnly=true). Sort by mention_count then section.
2. Apply depth rules. Relevance Filter (threshold 25).
3. batch_get_conversation_history for each channel.
4. DuckDB batch writes (signals.slack_messages).
5. THREAD REPLY FETCH: For messages with reply_count > 0 in today's ingestion,
   call batch_get_thread_replies (batch up to 10 threads per call).
   Insert all thread replies into signals.slack_messages with thread_ts set.
   Priority: threads from Brandon/Kate/Lena channels first. Cap: 50 threads/run.
6. Produce slack-digest in intake/.
7. RSW-CHANNEL INTAKE.
8. PROACTIVE SEARCH.
9. Update slack-scan-state.json.
10. DuckDB batch writes (signals.signal_tracker).

### Asana Full Sync to DuckDB
Execute ~/shared/context/protocols/asana-duckdb-sync.md:
1. Pull all incomplete tasks (Richard) + portfolio project tasks
2. UPSERT into asana_tasks table in DuckDB
3. Insert daily snapshot into asana_task_history
4. Soft-delete tasks no longer in Asana
5. Run coherence check (cross-reference DuckDB vs hands.md, current.md, asana-command-center.md)
6. Run schema drift detection (custom field changes, project changes, section changes)

### Morning Snapshot
```sql
CREATE SNAPSHOT am_YYYYMMDD OF ps_analytics;

INSERT INTO asana_task_history (snapshot_date, task_gid, project_name, section_name, due_on, completed, priority_rw, routine_rw)
SELECT CURRENT_DATE, task_gid, project_name, section_name, due_on, completed, priority_rw, routine_rw
FROM asana_tasks WHERE deleted_at IS NULL;
```

Legacy fallback: also write to `~/shared/context/active/asana-morning-snapshot.json`.

### Activity Monitor
Follow ~/shared/context/active/asana-activity-monitor-protocol.md.
1. Read asana-scan-state.json for last scan timestamps.
2. For each incomplete task, GetTaskStories to detect teammate activity. Skip Richard's stories.
3. Classify: comment_added (💬), due_date_changed (📅), reassigned (👤).
4. Write signals to intake/asana-activity.md.
5. Update asana-scan-state.json.

### Email Scan
Search all folders since last scan date (from ops.data_freshness). Produce email-triage in intake/. SKIP Auto-Comms folder Asana emails.

### Signal Intelligence
Per `~/shared/context/protocols/signal-intelligence.md`:
1. Extract topic keywords, normalize to slug.
2. FTS search slack_messages for reinforcement detection.
3. INSERT or UPDATE signal_tracker.
4. Run daily decay.
5. Query signal_trending view.

### Slack Conversation Enrichment
Execute Steps 1-3 from ~/shared/context/protocols/slack-conversation-intelligence.md:
1. Acronym/project detection in messages.
2. KDS enrichment for unfamiliar terms (max 5 queries).
3. Store KDS context in slack_messages.knowledge_context in DuckDB.
Skip if KDS unreachable — non-blocking.


---

## Phase 2: Signal Routing + Task Processing

Process intake files. Create tasks from signals. Detect enrichment gaps. All auto-write operations execute here. Approval-required operations are queued for AM-Frontend.

### Signal-to-Task Pipeline
Per ~/shared/context/protocols/signal-to-task-pipeline.md:
- Email: for each email from Brandon, Kate, Todd, or skip-level with action language → dedup check → CreateTask if new, AddComment if existing → log to signal_task_log.
- Slack: for each DM or @mention requiring action → same flow.
- Log pipeline execution to workflow_executions in DuckDB.

### Signal Routing
- Slack [ACTION-RW] signals → create Asana tasks (Routine + Priority_RW per mapping).
- Email signals → same routing.
- Asana digest → queue hands.md update for AM-Frontend.

### Signal-to-Routine Mapping
| Signal Type | Routine | Priority_RW |
|-------------|---------|-------------|
| Quick reply/send/confirm | Sweep | Today |
| Strategic discussion/artifact/framework | Core | Urgent |
| Campaign/keyword/bid/spreadsheet | Engine Room | Today |
| Admin/budget/invoice/compliance | Admin | Today |
| Unclear/ambiguous | (none — Backlog) | Flag for triage |

### Slack Decision Detection
Detect keywords: 'decided', 'agreed', 'confirmed', 'approved', 'going with', 'final call', 'locked in'. Queue for AM-Frontend presentation.

### Bucket Cap Check
Sweep: 5, Core: 4, Engine Room: 6, Admin: 3. Over cap → queue demotion proposals for AM-Frontend.

### Flags
- Priority_RW=Today but no Routine → queue for AM-Frontend.
- Overdue 7+ days with no activity → queue kill-or-revive for AM-Frontend.

---

## Phase 3: My Tasks Enrichment Scan

Scan ALL incomplete My Tasks for field completeness. Queue proposals — do NOT write without approval (except auto-writes below).

Call SearchTasksInWorkspace(assignee_any='1212732742544167', completed='false'). For each task, GetTaskDetails with opt_fields: name,assignee.gid,due_on,start_on,completed,custom_fields.name,custom_fields.display_value,custom_fields.gid,memberships.section.name.

### Four Enrichment Rules

**1. Kiro_RW Check** (GID: `1213915851848087`)
- IF empty/null OR not M/D brevity format → queue proposal.
- Format: `M/D: <text under 10 words>`. No leading zeros.

**2. Next Action Check** (GID: `1213921400039514`)
- IF empty/null → queue proposal.
- Format: imperative verb, single sentence, <15 words.

**3. Date Check** (Begin Date GID: `1213440376528542`)
- IF due_on set but start_on null → queue proposal: start_on = max(today, due_on - 7 days).

**4. Priority_RW Default** (GID: `1212905889837829`)
- IF Routine set but Priority_RW null → queue proposal: "Not urgent" (GID: `1212905889837833`).

### Output
Write enrichment proposals to `~/shared/context/active/am-enrichment-queue.json`:
```json
{
  "my_tasks": [
    {"task_gid": "...", "task_name": "...", "proposals": {"kiro_rw": "...", "next_action": "...", "start_on": "...", "priority_rw": "..."}}
  ],
  "portfolio": {},
  "generated_at": "ISO-8601"
}
```

---

## Phase 4: ABPS AI Content Scan

Scan ABPS AI - Content project (GID: `1213917352480610`).

### Step 1 — Scan Intake for Untriaged Tasks
- GetTasksFromProject → all incomplete tasks.
- FILTER: Intake section (GID: `1213917352480612`) where Routine_RW is NOT set.

### Step 2 — Analyze Each Untriaged Task
Prepare triage recommendations (Routine, Priority_RW, Frequency, Work_Product, dates, scope). Queue for AM-Frontend.

### Step 3 — Pipeline State Detection
For tasks in In Progress, Review, Active:
- Detect pipeline stage (research pending, draft pending, review pending, approval pending, refresh due).
- Queue pipeline actions for AM-Frontend presentation.

### Step 4 — Near-Due Escalation (AUTO-EXECUTE)
- due_on within 0-2 days AND NOT completed AND NOT in Active/Archive → set Priority_RW to Today.
- Update Kiro_RW: 'M/D: Near-due. Priority escalated.'
- This is a safety measure — executes without approval.

### Step 5 — Overdue Flagging
- due_on < today AND NOT completed → queue overdue flag for AM-Frontend.
- Compute days overdue, recommended action.

### Step 6 — Refresh Cadence Check
For Active tasks with Frequency != one-time: check recurring-task-state.json. Queue refresh actions for AM-Frontend.

---

## Phase 5: Portfolio Project Scan

Scan all child projects under ABIX PS and ABPS portfolios.

### Step 1 — Portfolio Discovery
- GetPortfolioItems for ABIX PS (`1212775592612914`) and ABPS (`1212762061512816`).
- New projects → discover sections + custom fields, queue flag for AM-Frontend.

### Step 2 — Per-Project Task Scan
For each project (AU, MX, WW Testing, WW Acq, Paid App):
- GetTasksFromProject → GetTaskDetails.
- FILTER: assignee.gid === '1212732742544167'. Skip Cross_Team_Tasks for writes.

### Step 3 — Field Enrichment Check
Same 4 rules as My Tasks. Queue proposals grouped by project → am-enrichment-queue.json.

### Step 4 — Date Window Checks + Near-Due Escalation (AUTO-EXECUTE)
- Near-due (0-2 days, not terminal): auto-set Priority_RW=Today, update Kiro_RW + Next action.
- Overdue (due < today, not terminal): queue flag for AM-Frontend.
- Terminal sections per project: see asana-command-center.md § Portfolio Projects.

### Step 5 — Status Update Staleness
- GetStatusUpdatesFromObject for each project.
- >14 days → stale. Exactly 14 → NOT stale. Never updated → flag.
- Extract health color.

### Step 6 — Recurring Task Auto-Creation (AU + MX) (AUTO-EXECUTE)
Detect completed tasks matching known patterns (asana-command-center.md § Recurring Task Patterns).
- Compute next dates. Auto-create next instance with same Routine_RW + project + assignee.
- Log each creation to audit trail. Include in AM-Frontend summary (informational, not approval).

### Step 7 — Cross-Team Blocker Detection (MX)
- Read all MX tasks including Cross_Team_Tasks (NEVER write).
- Flag overdue teammate tasks. Correlate with Richard's tasks.
- Queue blocker updates for AM-Frontend approval.

### Step 8 — Event Countdown (Paid App)
- Read event calendar. Check prep/escalation windows.
- Queue escalation proposals for AM-Frontend.

### Step 9 — Budget/PO Tracking (MX + Paid App)
- Classify Budget_Tasks. 3-day near-due threshold.
- Queue critical flags for AM-Frontend.

### Step 10 — Market Context Auto-Refresh (AU + MX)
- Compile project summary. Compare against Context_Task content.
- If Material_Change → read-before-write → UpdateTask(html_notes). AUTO-EXECUTE (context refresh is non-destructive).
- Skip if no material change.
- Context Task GIDs: AU=`1213917747438931`, MX=`1213917639688517`.

---

## Phase 6: Compile Output

Write all computed state to structured files for AM-Frontend consumption.

### Output Files
1. `~/shared/context/active/am-enrichment-queue.json` — all enrichment proposals (My Tasks + Portfolio)
2. `~/shared/context/active/am-portfolio-findings.json` — portfolio scan results (task counts, overdue, near-due, staleness, blockers, budget alerts)
3. `~/shared/context/active/am-abps-ai-state.json` — ABPS AI Content pipeline state
4. `~/shared/context/active/am-signals-processed.json` — signal routing results (tasks created, deferred, dismissed)
5. Intake files (slack-digest.md, email-triage.md, asana-digest.md, asana-activity.md) — already written in Phase 1

### Log Hook Execution
```sql
INSERT INTO hook_executions (hook_name, execution_date, start_time, end_time, duration_seconds,
    phases_completed, asana_reads, asana_writes, slack_messages_sent, duckdb_queries, summary)
VALUES ('am-backend', CURRENT_DATE, '[start]', '[end]', [duration],
    [phases], [reads], [writes], [slack_msgs], [queries], '[summary]');
```
