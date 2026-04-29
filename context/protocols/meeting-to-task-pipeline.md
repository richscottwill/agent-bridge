<!-- DOC-0355 | duck_id: protocol-meeting-to-task-pipeline -->
# Meeting-to-Task Pipeline

Extends EOD-1 Meeting Sync. After processing each Hedy session, extract action items and create Asana tasks.

**MCP Chain:** Hedy → Asana → Slack → DuckDB

---

## Step 1: Action Item Extraction

After pulling Hedy session details (GetSessionDetails), extract action items from:
- `todos` — items marked as action/task
- `highlights` — items with action language ("will do", "need to", "action:", "follow up")

For each action item, determine:
- **Assignee**: Parse for names. If Richard/prichwil mentioned → Richard's item. If another name → dependency item.
- **Description**: The full action item text
- **Due date signal**: Look for explicit dates, urgency words, or default to +3 business days

### Due Date Derivation
---

| Signal in Discussion | Due Date |
|---------------------|----------|
| Explicit date ("by Friday", "next week", "April 10") | Parse to calendar date |
| Urgency signal ("ASAP", "today", "urgent", "immediately") | Tomorrow |
| No date signal | +3 business days from meeting date |


## Step 2: Classify Action Items
For each extracted action item:
- **Richard's items** → Asana task creation path (Step 3)
- **Others' items** → Dependency logging path (Step 5)
- **No items found** → Log "no actions" in meeting series file,
## Step 2.5: Consolidation Check (MANDATORY — before creating any task)
**Principle: A new top-level task only earns its place if the action is Urgent + Important (or externally-bound with a hard deadline). Everything else becomes a subtask, a bullet in an existing task's notes, or a comment on a parent.**


Why: Tasks have an Asana MCP cost per create/update. Standalone granular tasks fragment the agenda, multiply bucket-cap pressure, and lose the program narrative. Rolling weekly/operational items under a program parent keeps the system readable and reduces tool calls.


### Step 2.5a — Classify by urgency × importance × containment

| Urgent? | Important? | External hard deadline? | Action |
|---|---|---|---|
| Yes | Yes | — | **Standalone** top-level task |
| Yes | No | Yes (cross-team, ≤ 2 days) | **Standalone** one-off |
| Yes | No | No | **Subtask** of the right parent |
| No | Yes | No | **Subtask** of the right parent |
| No | No | — | **Bullet in parent notes** OR skip |

"Urgent" = due in ≤ 3 days OR blocking someone else.
"Important" = meaningfully advances L1-L5 OR stakeholder-visible (Brandon/Kate/Todd).

### Step 2.5b — Parent program lookup

Before calling `CreateTask`, check the parent-program table in `~/shared/context/protocols/signal-to-task-pipeline.md` § Step 2.5b. Examples specific to meetings:

- **MX Paid Search Sync / MCS LP Review** action items → subtask of the matching MX program parent (or the in-scope MCS LP Review task). Don't create a new top-level task per meeting item.
- **AU meetings** action items → subtask of "AU meetings - Agenda" (the recurring weekly parent) OR subtask of the relevant AU program task.
- **Brandon 1:1 / Paid Acq Deep Dive** action items → subtask of the prep task for that 1:1.
- **Kate / stakeholder reviews** → usually warrant standalone (external visibility), but batch under a milestone task if multiple arrive from one meeting.
- **Hedy-captured "will follow up" items** with no deadline → bullet in parent notes, not a new task.

### Step 2.5c — When "bullet in parent notes" is right

For action items that are smaller than a subtask (a detail, a reference, a reminder), `UpdateTask` the parent to append one bullet under an "### Active signals / notes" subheading:

```
- [YYYY-MM-DD] [meeting_name] ([session_id]): [one-line summary]
```

### Step 2.5d — Confirm bar

Before each `CreateTask`, answer:
1. Does a parent program already exist for this action item? If yes → subtask or notes-bullet.
2. Is this Urgent + Important OR externally-bound? If no → not top-level.
3. Could multiple action items from this meeting be batched under one parent? If yes → batch.

Default to subtask or notes-bullet when in doubt.

---

## Step 3: Deduplication Check (Richard's items only)

For each of Richard's action items:

1. Extract 3-5 key noun phrases from the action item text
2. Search Asana: `SearchTasksInWorkspace(text="[key phrases]", assignee_any="1212732742544167", completed=false)`
3. Evaluate matches:
   - **Strong match** (2+ phrase overlap in name or description, same project): Add comment to existing task → `CreateTaskStory(task_gid, text="Reinforced in [meeting_name] on [date]: [action_item_text]")`
   - **Weak match** (1 phrase overlap): Create new task with note "Possible duplicate of [existing_task_gid] — verify."
   - **No match**: Create new task (Step 4)

---

## Step 4: Asana Task Creation

For each new action item assigned to Richard:

```
CreateTask(
    name: "[Meeting Name]: [action summary — max 80 chars]",
    notes: "From [meeting_name] on [date].\n\n[full action item text]\n\nSource: Hedy session [session_id]",
    due_on: [derived due date from Step 1],
    project: [appropriate project based on topic — use bucket assignment below],
    assignee: "1212732742544167"
)
```

### Bucket Assignment (project selection)

| Action Item Content | Asana Project/Bucket |
|-------------------|---------------------|
| Testing, methodology, framework, experiment | Core |
| Budget, invoice, campaign change, operational | Sweep |
| Automation, data, reporting, system, tool | Engine Room |
| Scheduling, access, approvals, admin | Admin |
| AU-specific | AU project |
| MX-specific | MX project |

If unclear, default to the project associated with the meeting series.

---

## Step 5: Dependency Logging (non-Richard items)

For action items assigned to others, append to `~/shared/context/body/hands.md` under the Priority Actions or Dependencies section:

```
- **[Person Name]**: [action item text] (from [meeting_name], [date])
```

---

## Step 6: Meeting Analytics Insertion

After processing each session, insert into DuckDB `meeting_analytics`:

```sql
INSERT INTO meeting_analytics (session_id, meeting_name, meeting_date, duration_minutes,
    participant_count, action_item_count, richard_speaking_share, hedging_count,
    meeting_type, topics_discussed)
VALUES ('[session_id]', '[meeting_name]', '[date]', [duration], [participants],
    [action_count], [speaking_share], [hedging_count], '[type]', ARRAY['[topic1]', '[topic2]']);
```

### Meeting Type Classification

| Participant Count | Recurring? | Type |
|------------------|-----------|------|
| 2 | Yes | 1on1 |
| 2 | No | adhoc_1on1 |
| 3-6 | Yes | group |
| 3-6 | No | review |
| 7+ | Any | standup |

---

## Step 7: Meeting Highlights Insertion

Store key quotes, decisions, and insights in DuckDB `meeting_highlights`:

```sql
INSERT INTO meeting_highlights (highlight_id, session_id, highlight_type, content, speaker, timestamp_offset)
VALUES ('[highlight_id]', '[session_id]', '[type]', '[content]', '[speaker]', [offset]);
```

Highlight types: `quote`, `decision`, `action`, `insight`

---

## Step 8: Slack DM Summary

After ALL sessions are processed, send a single summary DM:

```
self_dm(login="prichwil", text="📋 EOD-1 Meeting-to-Task Summary
• Sessions processed: [N]
• Tasks created: [N] — [task1 name] (due [date]), [task2 name] (due [date])
• Tasks updated (dedup): [N] — [task names]
• Dependencies logged: [N] — [person]: [action]
• No-action sessions: [N]")
```

If zero tasks created and zero dependencies, simplify to:
```
"📋 EOD-1: [N] sessions processed, no new action items."
```

---

## Workflow Observability

Log this pipeline execution to `workflow_executions` in DuckDB:

```sql
-- At start:
INSERT INTO workflow_executions (execution_id, workflow_name, trigger_source, mcp_servers_involved, start_time)
VALUES ('meeting_to_task_[timestamp]', 'meeting_to_task', 'eod-1', ARRAY['hedy', 'asana', 'slack', 'duckdb'], CURRENT_TIMESTAMP);

-- At end:
UPDATE workflow_executions SET end_time = CURRENT_TIMESTAMP, status = '[completed|partial|failed]',
    steps_completed = [N], steps_failed = [N],
    duration_seconds = EPOCH(CURRENT_TIMESTAMP - start_time)
WHERE execution_id = 'meeting_to_task_[timestamp]';
```
