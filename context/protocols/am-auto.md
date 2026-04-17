<!-- DOC-0327 | duck_id: protocol-am-auto -->
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
2. `SELECT database_name, type FROM duckdb_databases() WHERE database_name = 'ps_analytics'` → confirm connected
3. Quick table count: 46 tables + 39 views expected
4. If any missing → run ensure-schema.sql statements for missing tables
5. All DuckDB access goes through DuckDB MCP (`execute_query`). Do NOT use Python `duckdb.connect()` with MotherDuck tokens.

### Slack Scan
1. list_channels (unreadOnly=true). Sort by mention_count then section.
2. Apply depth rules. Relevance Filter (threshold 25).
3. Produce slack-digest in intake/.
4. RSW-CHANNEL INTAKE.
5. PROACTIVE SEARCH.
6. Update slack-scan-state.json.
7. DuckDB batch writes.

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

### Admin Keyword Detection (override — runs BEFORE generic mapping)
Before applying the Signal-to-Routine mapping table below, check the signal text (task name, description, or source message) against the Admin keyword list. Matching is case-insensitive.

**Admin Keywords:** `budget`, `PO`, `purchase order`, `invoice`, `spend`, `R&O`, `reconciliation`, `actuals`, `forecast`, `compliance`

**Rule:** If the signal text matches ANY keyword (case-insensitive substring match), route directly to Routine_RW = Admin with Priority_RW = Today. This overrides the generic Signal-to-Routine mapping below — do not fall through to the table for matched signals.

Signals that do NOT match any Admin keyword continue to the Signal-to-Routine mapping table as normal.

**NOTE:** Escalation logic (3-day overdue Admin → Sweep) is NOT applied here. Escalation lives in AM-2 only (am-triage.md § Admin Escalation Check). Per McKeown's Effortless principle, one simple checkpoint beats triplicated logic.

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
5. `~/shared/context/active/am-command-center-intel.json` — actionable intelligence for Command Center dashboard (commitments, delegate, communicate, differentiate)
6. Intake files (slack-digest.md, email-triage.md, asana-digest.md, asana-activity.md) — already written in Phase 1

### Command Center Intel Generation
Compile `am-command-center-intel.json` from signals collected in Phases 1-5. This file powers the four Actionable Intelligence cards on the Command Center dashboard.

**Commitments** — promises Richard made or others made to him. Sources:
- Slack signals where action = "respond" (someone asked Richard to do something)
- Asana unanswered comments (someone is waiting on Richard)
- Overdue tasks blocking teammates (implicit commitment)
- Format: `{text, source, person, said_by (richard|other), days_old, status (not_started|in_progress|done), context, quote?}`

**Delegate** — tasks Richard should hand off. Sources:
- Overdue kill-or-revive candidates marked DELEGATE
- Tasks in projects Richard doesn't own (Cross_Team_Tasks)
- Format: `{task, to, reason, context}`

**Communicate** — messages Richard needs to send. Sources:
- Unanswered Slack questions from Brandon/Kate/skip-level
- Pending status updates (project staleness flags)
- Meeting prep items requiring pre-communication
- Format: `{text, audience, context}`

**Differentiate** — highest-leverage actions that set Richard apart. Sources:
- THE HARD THING from amcc.md (always slot 1 if active)
- Critical enrichment proposals with strategic impact
- Brandon/Kate requests that demonstrate strategic thinking
- Format: `{action, why, status (not_started|in_progress|done), context}`

**Rules:**
- Max 8 commitments, 4 delegate, 4 communicate, 4 differentiate
- Deduplicate against existing items (match on text similarity)
- Carry forward non-done items from previous day's file (read before write)
- Mark items done when corresponding Asana task is completed or Slack reply detected

### Log Hook Execution
```sql
INSERT INTO hook_executions (hook_name, execution_date, start_time, end_time, duration_seconds,
    phases_completed, asana_reads, asana_writes, slack_messages_sent, duckdb_queries, summary)
VALUES ('am-backend', CURRENT_DATE, '[start]', '[end]', [duration],
    [phases], [reads], [writes], [slack_msgs], [queries], '[summary]');
```

---

## Phase 6.1: Dashboard Refresh

Run the full dashboard refresh pipeline to update all Command Center views:

```bash
python3 ~/shared/dashboards/refresh-all.py
```

This executes in sequence:
1. `extract-ly-data.py` — pull daily data from WW Dashboard Excel → `_Daily_Data` sheet
2. `refresh-forecast.py` — read `_Data` + `_Daily_Data` → `data/forecast-data.json`
3. `refresh-callouts.py` — read forecast JSON + callout markdown → `data/callout-data.json`
4. `generate-command-center.py` — read AM output files → `data/command-center-data.json`
   - Also syncs commitments to DuckDB `main.commitment_ledger` (text-hash dedup, 30-day rolling)
   - Also reads `data/ledger-actions.json` for user feedback (done/dismissed/restored) and applies to DuckDB
   - Also writes `~/shared/context/active/ledger-feedback-queue.json` with cascade instructions

Non-blocking: if any step fails, log warning and continue to Phase 6.2.

The Command Center index page (`~/shared/dashboards/index.html`) auto-loads these JSON files:
- `data/callout-data.json` → WW Summary + Market Table
- `data/command-center-data.json` → Daily Blocks + Actionable Items
- `data/forecast-data.json` → Forecast Tracker dashboard

---

## Phase 6.2: Ledger Feedback Cascade

Process user feedback from the Command Center Integrity Ledger. Read `~/shared/context/active/ledger-feedback-queue.json`.

For each pending item where `cascaded` is false:

### Asana Cascade
If `cascade_actions` contains `system: "asana"`:
- **complete_task**: SearchTasksInWorkspace(text=search_text, completed='false'). If found, UpdateTask(completed='true') + CreateTaskStory with the user's note.
- **add_comment**: SearchTasksInWorkspace(text=search_text). If found, CreateTaskStory with the dismissal reason.

### Slack Cascade
If `cascade_actions` contains `system: "slack"`:
- **suggest_reply**: Queue a draft reply suggestion for AM-Frontend. Do NOT auto-send — present the note as a draft for Richard to review.

### After Processing
- Set `cascaded: true` on each processed item.
- Write updated queue back to the file.
- Log cascade results to `ops.workflow_executions` in DuckDB.

Non-blocking: if any cascade fails, log warning, mark as `cascade_failed`, and continue.

---

## Phase 6.5: SharePoint Durability Sync

Execute ~/shared/context/protocols/sharepoint-durability-sync.md — AM section.

Push key output artifacts to OneDrive for cross-device access:
- am-enrichment-queue.json → Kiro-Drive/system-state/
- am-portfolio-findings.json → Kiro-Drive/system-state/
- am-command-center-intel.json → Kiro-Drive/system-state/
- daily-brief-latest.md → Kiro-Drive/system-state/
- command-center-data.json → Kiro-Drive/system-state/

Non-blocking: if SharePoint fails, log warning and continue.
