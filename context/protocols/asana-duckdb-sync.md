<!-- DOC-0334 | duck_id: protocol-asana-duckdb-sync -->
# Asana → DuckDB Sync Protocol

Canonical sync procedure for keeping DuckDB `asana_tasks` in lockstep with Asana. Two modes: full sync (AM-1) and delta sync (EOD-2). Both end with a coherence check and schema drift detection.

DB path: `/home/prichwil/shared/data/duckdb/ps-analytics.duckdb`

---

## Reference: GIDs

### Richard
- User GID: `1212732742544167`

### Portfolio Projects
| Project | GID |
|---------|-----|
| My Tasks | `1212732838073807` |
| ABPS AI Content | `1213917352480610` |
| AU | `1212762061512767` |
| MX | `1212775592612917` |
| WW Testing | `1205997667578893` |
| WW Acquisition | `1206011235630048` |
| Paid App | `1205997667578886` |

### Custom Field GIDs (column mapping)
| Column | Field GID | Type |
|--------|-----------|------|
| routine_rw | `1213608836755502` | enum |
| priority_rw | `1212905889837829` | enum |
| importance_rw | `1212905889837865` | enum |
| kiro_rw | `1213915851848087` | text |
| next_action_rw | `1213921400039514` | text |
| begin_date_rw | `1213440376528542` | date |

### Routine Enum Values
| GID | Name | Column Value |
|-----|------|-------------|
| `1213608836755503` | Sweep | Sweep |
| `1213608836755504` | Core | Core |
| `1213608836755505` | Engine Room | Engine Room |
| `1213608836755506` | Admin | Admin |
| `1213924412583429` | Wiki | Wiki |

Note: Asana UI shows parenthetical suffixes (e.g. "Sweep (Low-friction)") but
DuckDB always stores the short name. The ROUTINE_MAP below handles normalization.

### Priority Enum Values
| GID | Name | Column Value |
|-----|------|-------------|
| `1212905889837830` | Today | Today |
| `1212905889837831` | Urgent | Urgent |
| `1212905889837833` | Not urgent | Not urgent |

### Importance Enum Values
| GID | Name | Column Value |
|-----|------|-------------|
| `1212905889837866` | Important | Important |

---

## Full Sync (AM-1)

Run once per morning. Replaces stale DuckDB state with fresh Asana data.

### Step 1 — Pull All Incomplete Tasks (Richard)

```
SearchTasksInWorkspace(assignee_any="1212732742544167", completed=false, sort_by=due_date)
```

For each task returned, call:
```
GetTaskDetails(task_gid, opt_fields="name,due_on,start_on,completed,completed_at,assignee.gid,custom_fields.gid,custom_fields.name,custom_fields.display_value,custom_fields.enum_value.name,custom_fields.date_value,custom_fields.text_value,projects.name,projects.gid,memberships.section.name,notes,permalink_url")
```

### Step 2 — Pull Portfolio Project Tasks

For each project in the portfolio table above, call:
```
GetTasksFromProject(project_gid, opt_fields="name,due_on,start_on,completed,completed_at,assignee.gid,custom_fields.gid,custom_fields.name,custom_fields.display_value,custom_fields.enum_value.name,custom_fields.date_value,custom_fields.text_value,projects.name,projects.gid,memberships.section.name")
```

Merge results with Step 1 by task_gid (deduplicate — a task may appear in both Richard's assignments and a project).

### Step 3 — Map Custom Fields to Columns

For each task, extract custom field values by GID:

```python
FIELD_MAP = {
    '1213608836755502': 'routine_rw',      # enum → use enum_value.name
    '1212905889837829': 'priority_rw',      # enum → use enum_value.name
    '1212905889837865': 'importance_rw',    # enum → use enum_value.name
    '1213915851848087': 'kiro_rw',          # text → use text_value
    '1213921400039514': 'next_action_rw',   # text → use text_value
    '1213440376528542': 'begin_date_rw',    # date → use date_value.date
}

# For enum fields, map to short names:
ROUTINE_MAP = {
    'Sweep (Low-friction)': 'Sweep',
    'Sweep': 'Sweep',
    'Core Two (Deep Work)': 'Core',
    'Core': 'Core',
    'Engine Room (Excel and Google ads)': 'Engine Room',
    'Engine Room': 'Engine Room',
    'Admin (Wind-down)': 'Admin',
    'Admin': 'Admin',
    'Wiki': 'Wiki',
}
# Always normalize to short name. Asana API returns the full display name;
# DuckDB stores only the short name. Both forms map to the same value.
# Priority and Importance: use display name as-is (Today, Urgent, Not urgent, Important)
```

Any custom field GID NOT in FIELD_MAP → store in `flex_fields` JSON column as `{gid: {name, value}}`.

### Step 4 — UPSERT into asana_tasks

For each task:
```sql
INSERT INTO asana_tasks (task_gid, name, assignee_gid, project_name, project_gid, section_name,
    due_on, start_on, completed, completed_at, routine_rw, priority_rw, importance_rw,
    kiro_rw, next_action_rw, begin_date_rw, flex_fields, synced_at)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?::JSON, CURRENT_TIMESTAMP)
ON CONFLICT (task_gid) DO UPDATE SET
    name = EXCLUDED.name,
    assignee_gid = EXCLUDED.assignee_gid,
    project_name = EXCLUDED.project_name,
    project_gid = EXCLUDED.project_gid,
    section_name = EXCLUDED.section_name,
    due_on = EXCLUDED.due_on,
    start_on = EXCLUDED.start_on,
    completed = EXCLUDED.completed,
    completed_at = EXCLUDED.completed_at,
    routine_rw = EXCLUDED.routine_rw,
    priority_rw = EXCLUDED.priority_rw,
    importance_rw = EXCLUDED.importance_rw,
    kiro_rw = EXCLUDED.kiro_rw,
    next_action_rw = EXCLUDED.next_action_rw,
    begin_date_rw = EXCLUDED.begin_date_rw,
    flex_fields = EXCLUDED.flex_fields,
    deleted_at = NULL,
    synced_at = CURRENT_TIMESTAMP;
```

Note: `deleted_at = NULL` on UPSERT — if a previously soft-deleted task reappears, it's restored.

### Step 5 — Soft-Delete Missing Tasks

After UPSERT, mark tasks that were in DuckDB but NOT in the Asana pull:
```sql
UPDATE asana_tasks
SET deleted_at = CURRENT_TIMESTAMP
WHERE task_gid NOT IN ({synced_gids_list})
  AND deleted_at IS NULL
  AND completed = FALSE;
```

Only soft-delete incomplete tasks that vanished. Completed tasks stay as-is.

### Step 6 — Daily Snapshot to asana_task_history

Insert one row per task for today's date (append-only, never update):
```sql
INSERT INTO asana_task_history (snapshot_date, task_gid, project_name, section_name, due_on, completed, priority_rw, routine_rw)
SELECT CURRENT_DATE, task_gid, project_name, section_name, due_on, completed, priority_rw, routine_rw
FROM asana_tasks
WHERE deleted_at IS NULL
ON CONFLICT (snapshot_date, task_gid) DO NOTHING;
```

### Step 7 — Run Coherence Check
See "Coherence Check" section below.

### Step 8 — Run Schema Drift Detection
See "Schema Drift Handling" section below.

---

## Delta Sync (EOD-2)

Lightweight end-of-day update. Captures completions and new tasks without a full re-pull.

### Step 1 — Pull Today's Completions
```
SearchTasksInWorkspace(assignee_any="1212732742544167", completed=true, completed_on="{today_YYYY-MM-DD}")
```

For each completed task:
```sql
UPDATE asana_tasks
SET completed = TRUE,
    completed_at = CURRENT_TIMESTAMP,
    synced_at = CURRENT_TIMESTAMP
WHERE task_gid = ?;
```

### Step 2 — Detect New Tasks

Pull current incomplete tasks:
```
SearchTasksInWorkspace(assignee_any="1212732742544167", completed=false)
```

Compare against DuckDB:
```sql
SELECT task_gid FROM asana_tasks WHERE deleted_at IS NULL AND completed = FALSE;
```

Any task_gid in Asana but NOT in DuckDB → new task since morning. For each new task:
1. GetTaskDetails (same opt_fields as full sync Step 1)
2. INSERT into asana_tasks (same UPSERT pattern)
3. Flag in EOD-2 summary: "New task detected: [name] ([project])"

### Step 3 — Update Daily Snapshot

```sql
INSERT INTO asana_task_history (snapshot_date, task_gid, project_name, section_name, due_on, completed, priority_rw, routine_rw)
SELECT CURRENT_DATE, task_gid, project_name, section_name, due_on, completed, priority_rw, routine_rw
FROM asana_tasks
WHERE deleted_at IS NULL
ON CONFLICT (snapshot_date, task_gid) DO UPDATE SET
    completed = EXCLUDED.completed,
    priority_rw = EXCLUDED.priority_rw,
    routine_rw = EXCLUDED.routine_rw;
```

### Step 4 — Run Coherence Check
See below.

---

## Coherence Check

Run after every sync (both full and delta). Cross-references DuckDB state against Body system context files.

### Check 1 — Stale References in hands.md
Read `~/shared/context/body/hands.md` → Priority Actions section.
Extract task names mentioned. For each, search:
```sql
SELECT task_gid, name, completed, deleted_at
FROM asana_tasks
WHERE name ILIKE '%{task_name_fragment}%'
  AND deleted_at IS NULL AND completed = FALSE;
```
If no match → flag: "⚠️ hands.md references '[task_name]' but no matching active task in DuckDB."

### Check 2 — Unflagged Overdue Tasks
```sql
SELECT name, project_name, due_on, DATEDIFF('day', due_on, CURRENT_DATE) AS days_overdue
FROM asana_overdue
WHERE days_overdue >= 3;
```
Cross-reference against hands.md and current.md pending actions. If an overdue task (3+ days) isn't mentioned in either file → flag: "⚠️ [name] is {days_overdue}d overdue but not flagged in hands.md or current.md."

### Check 3 — Empty Projects
```sql
SELECT project_name, project_gid
FROM asana_by_project
WHERE incomplete = 0 AND project_gid IS NOT NULL;
```
Cross-reference against asana-command-center.md project list. If a known project has zero incomplete tasks → flag: "⚠️ [project_name] has 0 incomplete tasks in DuckDB — possible sync gap."

### Check 4 — Over-Cap Buckets
```sql
SELECT routine_bucket, total_tasks
FROM asana_by_routine;
```
Compare against caps from asana-command-center.md:
- Sweep: 5
- Core: 4
- Engine Room: 6
- Admin: 3

If total_tasks > cap → flag: "⚠️ [bucket] at {count}/{cap} — over cap."

### Check 5 — Enrichment Gaps
```sql
SELECT COUNT(*) AS empty_kiro,
    (SELECT COUNT(*) FROM asana_tasks WHERE next_action_rw IS NULL AND completed = FALSE AND deleted_at IS NULL) AS empty_next_action
FROM asana_tasks
WHERE kiro_rw IS NULL AND completed = FALSE AND deleted_at IS NULL;
```
If either count > 5 → flag: "⚠️ {count} tasks missing Kiro_RW context" or "⚠️ {count} tasks missing Next_Action."

### Check 6 — Completed Tasks Still Active in current.md
Read `~/shared/context/active/current.md` → Pending Actions section.
For each unchecked item, search:
```sql
SELECT task_gid, name, completed, completed_at
FROM asana_tasks
WHERE name ILIKE '%{action_fragment}%'
  AND completed = TRUE;
```
If match → flag: "⚠️ current.md still lists '[action]' as pending but task is completed in Asana."

### Output
Collect all flags. Include in:
- AM-3 brief (after full sync): under "⚠️ Coherence Alerts" section
- EOD-2 summary (after delta sync): under "System Health" section

If zero flags: "✅ DuckDB ↔ Body coherence check passed."

---

## Schema Drift Handling

Run during full sync (AM-1) only. Detects changes to Asana's custom fields, projects, and sections.

### Custom Field Drift

During Step 3 of full sync, for each task processed:
1. Collect all custom_fields GIDs from the API response.
2. Compare against FIELD_MAP keys.
3. If a GID is in FIELD_MAP but missing from the task → no action (field just not set on this task).
4. If a GID is NOT in FIELD_MAP and NOT already in flex_fields from a previous sync:
   - Store in flex_fields JSON column.
   - Log to schema_changes:
     ```sql
     INSERT INTO schema_changes (change_type, entity_name, old_value, new_value, detected_at)
     VALUES ('field_added', '{field_name}', NULL, '{field_gid}', CURRENT_TIMESTAMP);
     ```
   - Append to asana-command-center.md custom field table (if not already listed).

5. If a known FIELD_MAP GID has a different display_name than expected:
   - Log rename:
     ```sql
     INSERT INTO schema_changes (change_type, entity_name, old_value, new_value, detected_at)
     VALUES ('field_renamed', '{field_gid}', '{old_name}', '{new_name}', CURRENT_TIMESTAMP);
     ```
   - Update asana-command-center.md field name. DuckDB column stays the same (keyed on GID).

### Project Drift

During portfolio discovery, compare projects returned by GetPortfolioItems against the portfolio table above.

- New project (GID not in table):
  ```sql
  INSERT INTO schema_changes (change_type, entity_name, old_value, new_value, detected_at)
  VALUES ('project_added', '{project_name}', NULL, '{project_gid}', CURRENT_TIMESTAMP);
  ```
  Add to sync scope. Append to asana-command-center.md portfolio section.

- Missing project (GID in table but not returned):
  ```sql
  INSERT INTO schema_changes (change_type, entity_name, old_value, new_value, detected_at)
  VALUES ('project_archived', '{project_name}', '{project_gid}', NULL, CURRENT_TIMESTAMP);
  ```
  Stop syncing. Do NOT delete historical data from asana_tasks or asana_task_history.

### Section Drift

During sync, if a task's section_name doesn't match any known section for that project (per asana-command-center.md):
```sql
INSERT INTO schema_changes (change_type, entity_name, old_value, new_value, detected_at)
VALUES ('section_added', '{project_name}', NULL, '{section_name}', CURRENT_TIMESTAMP);
```
Update asana-command-center.md section list for that project.

### Task Soft Deletes

Tasks in asana_tasks that no longer appear in Asana API results:
```sql
UPDATE asana_tasks SET deleted_at = CURRENT_TIMESTAMP
WHERE task_gid NOT IN ({synced_gids}) AND deleted_at IS NULL AND completed = FALSE;
```
Historical data in asana_task_history is never deleted.

### EOD-2 Schema Change Summary

During EOD-2, query recent changes:
```sql
SELECT change_type, entity_name, old_value, new_value, detected_at
FROM schema_changes
WHERE detected_at >= CURRENT_DATE
ORDER BY detected_at;
```
Include in EOD-2 summary if any rows returned: "🔄 Schema changes detected today: [list]"

---

## DuckDB Views Reference

These views are pre-created and available for any protocol to query:

| View | Purpose | Key Columns |
|------|---------|-------------|
| `asana_overdue` | Tasks past due, not completed | name, project_name, due_on, days_overdue |
| `asana_by_project` | Task counts per project | project_name, total_tasks, incomplete, overdue |
| `asana_by_routine` | Bucket distribution (short names: Sweep, Core, Engine Room, Admin, Wiki) | routine_rw, task_count |
| `asana_completion_rate` | Trailing 7/30 day completion stats | avg_daily_completions_7d, total_completed_7d, etc. |

---

## Error Handling

- **Asana API failure**: Log error, skip that project/task, continue with remaining. Do NOT mark tasks as deleted on API failure.
- **DuckDB write failure**: Log to `~/shared/context/intake/duckdb-error-{date}.md`. Continue with remaining operations.
- **Partial sync**: If some projects succeed and others fail, UPSERT what we have. Flag partial sync in coherence check output.
- **Rate limiting**: If Asana returns 429, wait 60 seconds and retry once. If still failing, skip and log.
