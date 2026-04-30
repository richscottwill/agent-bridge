<!-- DOC-0359 | duck_id: protocol-signal-to-task-pipeline -->

# Signal-to-Task Pipeline

Extends AM-1 (Ingest) and AM-2 (Triage). Auto-creates Asana tasks from high-priority email and Slack signals.

**MCP Chain:** Outlook + Slack → Asana → DuckDB → Slack

---


### Step 2.5c — When "bullet in parent notes" is right

If the signal is smaller than a subtask (a detail, a reference, a reminder), `UpdateTask` the parent to append one bullet under an "### Active signals / notes" subheading. Format:

```
- [YYYY-MM-DD] [source]: [one-line summary with link]
```

This keeps the trail without inflating task count.


## Step 3: Asana Deduplication Check

For each high-priority signal before task creation:

1. Extract key terms from signal (sender name + subject keywords or message topic)
2. Search: `SearchTasksInWorkspace(text="[sender] [key terms]", assignee_any="1212732742544167", completed=false)`
3. Check for matches within 7 days:
   - **Match found** (same sender + similar subject): `CreateTaskStory(task_gid, text="New signal from [source] on [date]: [excerpt]")` → action_taken = 'task_updated'
   - **No match**: Proceed to task creation → action_taken = 'task_created'

---


### From Email Signals
```
CreateTask(
name: "[Sender Name]: [subject excerpt — max 80 chars]",
notes: "Email from [sender] on [date].\n\n[key excerpt — first 500 chars]\n\nSource: email [conversation_id]",
due_on: [suggested — explicit date from email > +3 business days],
project: [bucket from Step 5],
assignee: "1212732742544167"
)
```


### Step 2.5b — Parent program lookup

For each signal, check if a **program parent task** exists before creating a new top-level task. Use `SearchTasksInWorkspace(text="[program name]", assignee_any="1212732742544167", completed=false)` then make the new item a subtask via `SetParentForTask`.

| Signal topic | Preferred parent (search term or gid) | Notes |
|---|---|---|
| MX weekly ops (budget, invoice, LP, campaign change, MCS LP Review follow-ups) | MX project top-level or "MX weekly rollup" | Create a rollup task if none exists; prefer subtask over new task |
| AU weekly ops (LP switch, refmarker, agenda prep, handoff checks) | "AU meetings - Agenda" (recurring weekly) or AU project top-level | AU agenda is the right bucket for most Tue-sync items |
| Paid App PAM ops (budget, PO, campaign changes, pacing) | "Paid App" parent (1212988092117041) | Existing in-progress BAU workstream |
| Adi 1:1 prep items | "Come prepared: Bi-weekly with Adi to brainstorm usable AI" (1214055207544514) | Recurring bi-weekly parent |
| Brandon 1:1 prep items | Most recent Brandon-1:1 prep task; create one if none within 7 days | One prep task per 1:1 cycle |
| Dwayne Brand LP replies | Canonical "Reply to Dwayne" task (1214128635826241) | Has full draft + 7 asks + 2 UX tickets |
| F90 audience/media/legal chain | F90 parent (1212760973200434) | 9 existing subtasks |
| Wiki article writes | None — handled by wiki pipeline, not Asana (ABPS AI Content deprecated 2026-04-17) | Do not create tasks |
| ABPS AI Build system work | ABPS AI Build project (1213379551525587) | Per Active Development / Shipped sections |


### Signal Classification
- **High priority**: From priority sender AND contains action language → auto-create task
- **Medium priority**: From priority sender OR contains action language → flag for AM-2 triage
- **Low priority**: FYI/informational → log but no task creation

---


## Step 5: Bucket Assignment

| Signal Content | Asana Bucket |
|---------------|-------------|
| Strategic request (testing, methodology, framework) | Core |
| Operational request (budget, invoice, campaign change) | Sweep |
| System/tool request (automation, data, reporting) | Engine Room |
| Administrative (scheduling, access, approvals) | Admin |

---


## Step 2: High-Priority Slack Signal Detection (AM-1)

During Slack scan, identify actionable signals:

| Signal Type | Detection | Priority |
|------------|-----------|----------|
| DM to Richard | Any DM requiring response or action | High |
| @mention | @Richard in channel with action language | High |
| Thread reply | Reply to Richard's message with question/request | Medium |
| Channel mention | Richard's name (not @) in discussion | Low |

Action language in Slack: questions directed at Richard, requests, deadlines, "can you", "will you", "need", "please", "thoughts?", "what do you think?"

---


### Details

• Updated tasks: [N] (new signals on existing)
• Deferred: [N] (low priority, backlog)
• Dismissed: [N] (FYI only)")
```

---


### Step 2.5d — Confirm bar
Before calling `CreateTask`, the agent must answer in its own reasoning:
1. Does a parent program already exist for this signal? (If yes, subtask or notes-bullet.)
2. Is this Urgent + Important, OR externally-bound hard deadline?
3. Could this be consolidated with a signal-in-hand the same cycle? (If yes, batch into one parent write.)
If the agent cannot give a clear yes to standalone creation, default to subtask/bullet.
---
### From Slack Signals
```
CreateTask(
    name: "[Author]: [topic summary — max 80 chars]",
    notes: "Slack [DM/mention/thread] from [author] in [channel] on [date].\n\n[message text]\n\nLink: [slack_url]",
    due_on: [+3 business days default],
    project: [bucket from Step 5],
    assignee: "1212732742544167"
)
```

---


### Priority Senders (always high-priority)
- Brandon Munday (L7 manager)
- Kate Rundell (L8 director)
- Todd Heimes (L10 VP)
- Any skip-level stakeholder


## Workflow Observability

Log pipeline execution to `workflow_executions` in DuckDB:

```sql
INSERT INTO workflow_executions (execution_id, workflow_name, trigger_source, mcp_servers_involved, start_time)
VALUES ('signal_to_task_[timestamp]', 'signal_to_task', 'am-1', ARRAY['outlook', 'slack', 'asana', 'duckdb'], CURRENT_TIMESTAMP);
```

## Step 7: AM-2 Triage Summary (Slack DM)

After AM-2 triage completes, send summary:

```
self_dm(login="prichwil", text="📬 AM-2 Triage Complete
• New tasks: [N] (from [sources])

## Step 8: AM-2 Historical Context Enhancement

When triaging a signal, query DuckDB for related past conversations:

```sql
SELECT ts, channel_name, text_preview, timestamp
FROM slack_messages
WHERE author_name = '[signal_author]'
AND fts_main_slack_messages.match_bm25(ts, '[signal_keywords]') IS NOT NULL
AND timestamp > CURRENT_TIMESTAMP - INTERVAL '30 days'
ORDER BY timestamp DESC
LIMIT 5;
```

Include conversation history in triage context for better task creation.

---


## Step 2.5: Consolidation Check (MANDATORY — before creating any task)

**Principle: A new top-level task only earns its place if the signal is Urgent + Important (or externally-bound with a hard deadline that doesn't fit an existing parent). Everything else becomes a subtask, a bullet in an existing task's notes, or a comment.**

Why: Tasks have an Asana MCP cost per create/update. Standalone granular tasks fragment context, multiply bucket-cap pressure, and lose the parent-program narrative. Rolling weekly/operational items under a program parent keeps the agenda readable and reduces tool calls.


### Step 2.5a — Classify by urgency × importance × containment

| Urgent? | Important? | External hard deadline? | Action |
|---|---|---|---|
| Yes | Yes | — | **Standalone** (top-level task) |
| Yes | No | Yes (today/tomorrow, cross-team) | **Standalone** (one-off) |
| Yes | No | No | **Subtask** of the right parent |
| No | Yes | No | **Subtask** of the right parent |
| No | No | — | **Bullet in parent notes** OR skip entirely |

"Urgent" = due in ≤ 3 days OR blocking someone else.
"Important" = meaningfully advances L1-L5 OR stakeholder-visible (Brandon/Kate/Todd).


## Step 6: Signal-to-Task Logging (DuckDB)

For EVERY signal processed (regardless of action taken):

```sql
INSERT INTO signal_task_log (signal_source, signal_id, task_gid, action_taken, priority, created_at)
VALUES ('[email|slack_dm|slack_mention|slack_thread]', '[email_id or message_ts]',
    '[task_gid or NULL]', '[task_created|task_updated|deferred|dismissed]',
    '[high|medium|low]', CURRENT_TIMESTAMP)
ON CONFLICT (signal_source, signal_id) DO UPDATE SET
    task_gid = EXCLUDED.task_gid, action_taken = EXCLUDED.action_taken;
```

---


## Step 4: Asana Task Creation from Signals


### Action Language Detection
Subject or body contains: "action", "request", "need", "deadline", "urgent", "please", "follow up", "by [date]", "can you", "will you", "I need you to"


## Step 1: High-Priority Email Signal Detection (AM-1)

During email scan, identify high-priority signals:

