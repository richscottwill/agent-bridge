<!-- DOC-0332 | duck_id: protocol-asana-activity-monitor-protocol -->
# Asana Activity Monitor Protocol

Last updated: 2026-04-03

## Purpose

Scan Richard's incomplete Asana tasks for teammate activity (comments, due date changes, reassignments) since the last scan. Write detected signals to `~/shared/context/intake/asana-activity.md` for AM-2/AM-3 consumption. Update scan state so subsequent runs only process new activity.

## When to Run

- During AM-1 (Morning Routine Ingest), after pulling incomplete tasks
- Can also be run manually on demand

## Prerequisites

- Asana MCP tools available: `SearchTasksInWorkspace`, `GetTaskStories`
- State file: `~/shared/context/active/asana-scan-state.json`
- Output file: `~/shared/context/intake/asana-activity.md`

## Constants

- Richard's Asana GID: `1212732742544167`
- Workspace GID: `8442528107068`

---

## Step-by-Step Procedure

### Step 1: Read Scan State

Read `~/shared/context/active/asana-scan-state.json`:
```json
{
  "last_scan_timestamp": "ISO 8601 or null",
  "per_task_timestamps": { "task_gid": "ISO 8601" },
  "last_updated": "ISO 8601 or null"
}
```

- If `last_scan_timestamp` is null, this is the first scan. Use 7 days ago as the lookback window.
- If `last_scan_timestamp` has a value, use it as the default cutoff for tasks not in `per_task_timestamps`.

### Step 2: Pull Incomplete Tasks

Call `SearchTasksInWorkspace`:
- `workspace_gid`: `8442528107068`
- `assignee_any`: `1212732742544167`
- `completed`: `false`

This returns all of Richard's incomplete tasks. Store the list for iteration.

### Step 3: Get Stories for Each Task

For each task in the list:

1. Look up the task's last-scanned timestamp:
   - If `per_task_timestamps[task_gid]` exists, use that timestamp
   - Otherwise, use `last_scan_timestamp` (or 7-day lookback if null)

2. Call `GetTaskStories`:
   - `task_gid`: the task's GID

3. Filter stories to only those with `created_at` after the task's last-scanned timestamp.

4. Skip stories authored by Richard (GID `1212732742544167`) — we only want teammate activity.

### Step 4: Classify Each Story

For each new story (after timestamp filter, excluding Richard's own):

**Comment Added** (`comment_added`):
- Condition: `resource_subtype` is `comment_added` OR story `type` is `comment`
- Extract: comment text, author name, task name, timestamp

**Due Date Changed** (`due_date_changed`):
- Condition: `resource_subtype` contains `due_date` OR story text mentions "changed the due date"
- Extract: old due date, new due date (parse from story text), who changed it, task name, timestamp

**Reassigned** (`reassigned`):
- Condition: `resource_subtype` is `assigned` OR story text mentions "assigned" or "reassigned"
- Extract: new assignee name, who reassigned, task name, timestamp

**Other changes** (section moves, custom field changes, etc.):
- Log but do not surface in the brief unless they match the three categories above

### Step 5: Handle Errors

If a `GetTaskStories` call fails (rate limit, API error, timeout):
- Log the error: task GID, error type, timestamp
- Skip the affected task
- Continue processing remaining tasks
- Note skipped tasks at the bottom of the output file

---

## Output Format

### Step 6: Write Signals to `~/shared/context/intake/asana-activity.md`

Overwrite the file each scan (signals are consumed by AM-3 and then archived).

Format:

```markdown
# Asana Activity Signals

Scan timestamp: YYYY-MM-DDTHH:MM:SSZ
Tasks scanned: [count]
Signals detected: [count]

---

## [YYYY-MM-DD]

### 💬 Comments

- **[Task Name]** — [Author Name] ([timestamp]):
  > [Comment text, first 200 chars]

### 📅 Due Date Changes

- **[Task Name]** — [Who changed it] ([timestamp]):
  Changed due date [old date → new date]

### 👤 Reassignments

- **[Task Name]** — [Who reassigned] ([timestamp]):
  Reassigned to [New Assignee Name]

---

## Errors / Skipped Tasks

- [task_gid]: [error description]
```

If no signals are detected, write:

```markdown
# Asana Activity Signals

Scan timestamp: YYYY-MM-DDTHH:MM:SSZ
Tasks scanned: [count]
Signals detected: 0

No new activity detected since last scan.
```

---

## State Update

### Step 7: Update `asana-scan-state.json`

After all tasks are processed:

```json
{
  "last_scan_timestamp": "[current ISO 8601 timestamp]",
  "per_task_timestamps": {
    "[task_gid]": "[timestamp of most recent story processed, or current time if no stories]",
    ...
  },
  "last_updated": "[current ISO 8601 timestamp]"
}
```

Rules:
- For each task that was scanned, set its `per_task_timestamps` entry to the `created_at` of the most recent story found, or the current scan timestamp if no new stories.
- Set `last_scan_timestamp` to the current time.
- Set `last_updated` to the current time.
- Tasks that were skipped due to errors retain their previous timestamp (or are omitted if they had none).

---

## Signal Classification Reference

| Story Attribute | Signal Type | Emoji | What to Surface |
|----------------|-------------|-------|-----------------|
| `resource_subtype: comment_added` | comment_added | 💬 | Comment text, author, task |
| Text contains "due date" change | due_date_changed | 📅 | Old → new date, who changed |
| `resource_subtype: assigned` | reassigned | 👤 | New assignee, who reassigned |
| Section move, tag change, etc. | (not surfaced) | — | Logged but not in brief |

## Integration with AM-3 Brief

The AM-3 hook reads `~/shared/context/intake/asana-activity.md` and includes the signals in the daily brief under the "Activity Signals" section. The brief template uses the emoji classifications directly:

- 💬 Comments awaiting response: [count]
- 📅 Due date changes: [count]  
- 👤 Reassignments: [count]

Each signal links back to the task name so Richard can act on it.
