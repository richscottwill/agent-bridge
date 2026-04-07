<!-- DOC-0359 | duck_id: protocol-signal-to-task-pipeline -->
# Signal-to-Task Pipeline

Extends AM-1 (Ingest) and AM-2 (Triage). Auto-creates Asana tasks from high-priority email and Slack signals.

**MCP Chain:** Outlook + Slack → Asana → DuckDB → Slack

---

## Step 1: High-Priority Email Signal Detection (AM-1)

During email scan, identify high-priority signals:

### Priority Senders (always high-priority)
- Brandon Munday (L7 manager)
- Kate Rundell (L8 director)
- Todd Heimes (L10 VP)
- Any skip-level stakeholder

### Action Language Detection
Subject or body contains: "action", "request", "need", "deadline", "urgent", "please", "follow up", "by [date]", "can you", "will you", "I need you to"

### Signal Classification
- **High priority**: From priority sender AND contains action language → auto-create task
- **Medium priority**: From priority sender OR contains action language → flag for AM-2 triage
- **Low priority**: FYI/informational → log but no task creation

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

## Step 3: Asana Deduplication Check

For each high-priority signal before task creation:

1. Extract key terms from signal (sender name + subject keywords or message topic)
2. Search: `SearchTasksInWorkspace(text="[sender] [key terms]", assignee_any="1212732742544167", completed=false)`
3. Check for matches within 7 days:
   - **Match found** (same sender + similar subject): `CreateTaskStory(task_gid, text="New signal from [source] on [date]: [excerpt]")` → action_taken = 'task_updated'
   - **No match**: Proceed to task creation → action_taken = 'task_created'

---

## Step 4: Asana Task Creation from Signals

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

## Step 5: Bucket Assignment

| Signal Content | Asana Bucket |
|---------------|-------------|
| Strategic request (testing, methodology, framework) | Core |
| Operational request (budget, invoice, campaign change) | Sweep |
| System/tool request (automation, data, reporting) | Engine Room |
| Administrative (scheduling, access, approvals) | Admin |

---

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

## Step 7: AM-2 Triage Summary (Slack DM)

After AM-2 triage completes, send summary:

```
self_dm(login="prichwil", text="📬 AM-2 Triage Complete
• New tasks: [N] (from [sources])
• Updated tasks: [N] (new signals on existing)
• Deferred: [N] (low priority, backlog)
• Dismissed: [N] (FYI only)")
```

---

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

## Workflow Observability

Log pipeline execution to `workflow_executions` in DuckDB:

```sql
INSERT INTO workflow_executions (execution_id, workflow_name, trigger_source, mcp_servers_involved, start_time)
VALUES ('signal_to_task_[timestamp]', 'signal_to_task', 'am-1', ARRAY['outlook', 'slack', 'asana', 'duckdb'], CURRENT_TIMESTAMP);
```
