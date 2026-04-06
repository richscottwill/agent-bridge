# AM-Auto Protocol — Ingest + Brief

Two autonomous phases. No interaction needed. State passes between phases via files.

---

## Phase 1: Ingest

Pure data collection. No drafting, no decisions, no organ writes.

### Context Load
spine.md, current.md, slack-channel-registry.json, slack-scan-state.json, asana-command-center.md.

### DuckDB Schema Verification (before any queries)
Run `~/shared/context/protocols/duckdb-schema-verification.md` quick check:
1. `SELECT current_database(), current_schema()` → must be `ps_analytics`, `main`
2. `SELECT database_name, type FROM duckdb_databases() WHERE database_name = 'ps_analytics'` → type must be `motherduck`
3. Quick table count: 46 tables + 39 views expected
4. If any missing → run ensure-schema.sql statements for missing tables
5. If database type is not `motherduck` → STOP and flag: MCP server not connected to MotherDuck

### Slack Scan
1. list_channels (unreadOnly=true). Sort by mention_count then section.
2. Apply depth rules. Relevance Filter (threshold 25).
3. Produce slack-digest in intake/.
4. RSW-CHANNEL INTAKE.
5. PROACTIVE SEARCH.
6. Update slack-scan-state.json.
7. DuckDB batch writes.

### Asana Pull
1. SearchTasksInWorkspace: assignee_any=1212732742544167, completed=false, sort_by=due_date.
2. For each task, GetTaskDetails with opt_fields: name,due_on,completed,custom_fields.name,custom_fields.display_value,custom_fields.enum_value.name,projects.name,notes,permalink_url.
3. Categorize by Routine field:
   - Sweep: `1213608836755503`
   - Core Two: `1213608836755504`
   - Engine Room: `1213608836755505`
   - Admin: `1213608836755506`
   - Backlog: no Routine set
4. Flag: Priority_RW=Today tasks, overdue tasks, tasks with no Routine (needs triage).
5. Write asana-digest to intake/ with categorized task list.
6. Check for new tasks since last scan (Recently Assigned section or created in last 24h).

### Morning Snapshot (DuckDB + MotherDuck Time Travel)

After Asana pull completes and `asana_tasks` is populated, create a MotherDuck named snapshot as the frozen morning baseline:

```sql
-- Create morning snapshot for time travel (EOD-2 will diff against this)
CREATE SNAPSHOT am_YYYYMMDD OF ps_analytics;
```

Also insert today's task history snapshot for long-term trend analysis:
```sql
INSERT INTO asana_task_history (snapshot_date, task_gid, project_name, section_name, due_on, completed, priority_rw, routine_rw)
SELECT CURRENT_DATE, task_gid, project_name, section_name, due_on, completed, priority_rw, routine_rw
FROM asana_tasks WHERE deleted_at IS NULL;
```

**Legacy fallback:** Also write to `~/shared/context/active/asana-morning-snapshot.json` until all consumers are migrated to DuckDB queries. The JSON snapshot will be deprecated once EOD-2 time travel reconciliation is verified stable.

```json
{
  "snapshot_date": "YYYY-MM-DD",
  "scan_time": "ISO-8601",
  "bucket_counts": {"sweep": N, "core": N, "engine_room": N, "admin": N, "backlog": N},
  "over_cap": ["buckets exceeding caps"],
  "today_tasks": ["GIDs where Priority_RW=Today"],
  "overdue_tasks": ["GIDs where due_on < today"],
  "total_incomplete": N,
  "total_overdue": N,
  "hard_thing": {"task_gid": "...", "name": "...", "days_overdue": N, "workdays_at_zero": N}
}
```

### Log Hook Execution
After all Phase 1 steps complete, log this AM-Auto run:
```sql
INSERT INTO hook_executions (hook_name, execution_date, start_time, end_time, duration_seconds,
    phases_completed, asana_reads, asana_writes, slack_messages_sent, duckdb_queries, summary)
VALUES ('am-auto', CURRENT_DATE, '[start]', '[end]', [duration],
    [phases], [reads], [writes], [slack_msgs], [queries], '[summary]');
```

### Activity Monitor
Follow ~/shared/context/active/asana-activity-monitor-protocol.md.

1. Read ~/shared/context/active/asana-scan-state.json for last scan timestamps.
2. For each incomplete task, call GetTaskStories to detect teammate activity since last scan. Skip stories by Richard (GID 1212732742544167).
3. Classify: comment_added (💬), due_date_changed (📅), reassigned (👤).
4. Write signals to ~/shared/context/intake/asana-activity.md (overwrite each scan).
5. Update asana-scan-state.json with new timestamps.
6. On API failure: log error, skip task, continue.

### Email Scan
Catalog unread. Produce email-triage in intake/. SKIP Auto-Comms folder Asana emails.

### Signal Intelligence (after all channel ingestion)
Per `~/shared/context/protocols/signal-intelligence.md`:
1. For each ingested message/email/task comment, extract topic keywords and normalize to slug.
2. FTS search slack_messages for reinforcement detection (BM25 > 2.0 = reinforcement, not new).
3. INSERT or UPDATE signal_tracker: new topics get strength=1.0, reinforcements get +0.5 (Slack), +1.0 (Email), +0.75 (Asana).
4. Run daily decay: `UPDATE signal_tracker SET signal_strength = signal_strength * 0.9 WHERE last_decayed < now - 20h`. Deactivate signals below 0.1.
5. Query signal_trending view — include trending topics (2+ mentions in 7 days) in Phase 1 output.

### Phase 1 Output
Report: channels scanned, signals extracted, Asana tasks by bucket + overdue count, snapshot written, activity signals detected, emails triaged, trending signals.

---

## Phase 3: Brief + Blocks

Produces the daily brief, dashboard, and calendar blocks from Phase 1 + Phase 2 output.

### Context Load
body.md, spine.md, org-chart.md, rw-trainer.md, rw-task-prioritization.md, brain.md, eyes.md, device.md, gut.md, rw-tracker.md, hands.md (fresh), amcc.md (fresh), slack-scan-state.json, asana-command-center.md, ~/shared/context/intake/asana-activity.md.
DuckDB is the primary data source for all task analytics — query `asana_tasks`, `asana_overdue`, `asana_by_routine`, `asana_by_project` views directly. The JSON morning snapshot is legacy fallback only.

### Brief Structure
1. TRAINER CHECK-IN
2. HEADS UP
3. SLACK OVERNIGHT
4. TODAY (from Asana — see below)
5. SPEC SHEET
6. T-MINUS
7. aMCC
8. SYSTEM HEALTH

### TODAY Section (from DuckDB asana_tasks + Asana views)
Pull bucket counts and overdue list from DuckDB views instead of morning snapshot JSON:
- Query: `SELECT * FROM asana_by_routine` → bucket counts for Sweep/Core/Engine Room/Admin/Backlog
- Query: `SELECT * FROM asana_overdue ORDER BY days_overdue DESC` → overdue list with days_overdue
- Query: `SELECT * FROM asana_tasks WHERE priority_rw = 'Today' AND completed = FALSE AND deleted_at IS NULL ORDER BY routine_rw` → Today tasks by bucket
- Query: `SELECT * FROM asana_completion_rate` → trailing completion stats for SYSTEM HEALTH section

Display:
- 🧹 Sweep: Routine=Sweep AND Priority_RW=Today. Name + due date + L1-L5 tag.
- 🎯 Core: Routine=Core AND Priority_RW=Today. THE HARD THING gets first slot.
- ⚙️ Engine Room: Routine=Engine Room AND Priority_RW=Today.
- 📋 Admin: Routine=Admin AND Priority_RW=Today.
- ⚠️ Overdue: Count + oldest task + days overdue (from asana_overdue view).
- 📦 Needs Triage: Tasks with no Routine set (routine_rw IS NULL in asana_tasks).
- Bucket counts: Sweep X/5, Core X/4, Engine Room X/6, Admin X/3 (from asana_by_routine view).

### ⚠️ Coherence Alerts
Include any flags from the AM-1 full sync coherence check (stale references, unflagged overdue, empty projects, over-cap buckets, enrichment gaps, completed-but-still-listed). If zero flags: "✅ DuckDB ↔ Body coherence check passed."

### Five Levels Annotation
For each task in TODAY, append [L1]-[L5] tag per asana-command-center.md mapping:
- Goal/Kingpin → L1
- WW Testing/PS-Owned/Paid App/PS ENG/AU/MX → L2
- Team meeting prep/cross-team → L3
- AI/AEO/zero-click → L4
- Agentic loop/Kiro system → L5
- Default → L2

### Activity Signals
Read ~/shared/context/intake/asana-activity.md:
- 💬 Comments awaiting response: count + task name, commenter, preview.
- 📅 Due date changes: count + task name, old→new, who.
- 👤 Reassignments: count + task name, new assignee, who.
- If 0 signals: "No teammate activity since last scan."

### ⚠️ Goal Alerts
Read asana-command-center.md for goal data. If any goals at-risk or off-track: goal name, status, metric gap, recommended action.

### 🏭 ABPS AI Document Factory
Read asana-morning-snapshot.json → abps_ai section:
- 📥 Intake: count awaiting triage
- 🔨 In Progress: count + each with pipeline stage and name
- 👀 In Review: count + each with review status and name
- ✅ Active: count of living documents
- 📦 Archive: count of completed one-time documents
- Pipeline detail per task: stage, due date
- Alerts: overdue, near-due, entering window this week, refresh due, flagged for Richard

### 📊 Portfolio Status
Query DuckDB: `SELECT * FROM asana_by_project` → task counts per project (total, incomplete, completed, overdue).

ABIX PS:
- AU: task count, overdue, near-due — Health: 🟢/🟡/🔴 (from asana_by_project view) [⚠️ STALE if >14d]
- MX: same format

ABPS / Managed Projects:
- WW Testing, WW Acquisition, Paid App: same format

Alerts: near-due tasks, overdue tasks, stale projects, cross-team blockers.

💰 Budget Tasks: active Budget_Tasks across MX and Paid App. ⚡ if due within 3d. 🔴 CRITICAL if overdue.

### Output Channels
- Dark navy HTML email AUTO-SEND.
- Slack: Brief to rsw-channel. Focus update if changes. Include Asana task context inline: '[Task Name] (due [date], [Routine], [status])'.
- Dashboard: Edit pinned message C0993SRL6FQ.
- Calendar: Create time blocks sized by bucket counts. Sweep=15min×count, Core=45min×count, Engine Room=20min×count, Admin=15min×count. Min 30min, max 3h. Flag overload if total exceeds available time.
- Meeting prep: For each meeting today, query signal_tracker for attendee topics (last 7 days) per signal-intelligence.md Use Case 5. Include in brief: "Brandon's hot topics: [list]. Shared topics with Richard: [list]."

### Friday Additions
- Calibration.
- Remind Agent Bridge Sync.

### Proactive Drafts
DuckDB unanswered 24h+.
