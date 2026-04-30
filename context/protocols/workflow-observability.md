<!-- DOC-0363 | duck_id: protocol-workflow-observability -->

# Workflow Observability Protocol

Cross-cutting concern

**MCP Chain:** Any workflow → DuckDB → Slack

---

## Workflow Logging Pattern

Every cross-MCP workflow MUST follow this logging pattern:


### At Workflow Start ```sql INSERT INTO workflow_executions (execution_id, workflow_name, trigger_source, mcp_servers_involved, start_time) VALUES ('{name}_{timestamp}', '{name}', '{trigger}', ARRAY['{mcp1}', '{mcp2}'], CURRENT_TIMESTAMP); ``` ### At Each Step Completion
```sql
UPDATE workflow_executions SET steps_completed = steps_completed + 1
WHERE execution_id = '{id}';
```


### On Step Failure
```sql
UPDATE workflow_executions SET steps_failed = steps_failed + 1,
 error_details = '{\"step_name\": \"{step}\", \"error\": \"{message}\"}'::JSON
WHERE execution_id = '{id}';
```


### At Workflow End
```sql
UPDATE workflow_executions SET end_time = CURRENT_TIMESTAMP,
 status = '{completed|partial|failed}',
 duration_seconds = EPOCH

#### At Workflow End — Details

WHERE execution_id = '{id}';
```


### At Workflow End — Details

Status rules:
- `completed`
- `partial`
- `failed`

---


## Registered Workflows

|--------------|---------------|---------|
| `meeting_to_task` | Hedy, Asana, Slack, DuckDB | EOD-1 |
| `signal_to_task` | Outlook, Slack, Asana, DuckDB | AM-1/AM-2 |
| `wiki_enriched_publish` | KDS, ARCC, XWiki, SharePoint | Wiki pipeline |
| `context_enrichment` | KDS, ARCC, DuckDB | EOD-2 |
| `slack_intelligence` | Slack, KDS, DuckDB | AM-1 |


## Degradation Detection (EOD-2)

Run during EOD-2 system refresh:

```sql
SELECT workflow_name, success_rate, total_runs, avg_duration_s
FROM workflow_reliability
WHERE success_rate < 80 AND total_runs >= 3;
```

If results → include in EOD-2 Slack DM:
```
⚠️ Degraded workflows:
• {workflow}: {success_rate}% success. Most common failure: {error}
```

---


## EOD-2 Workflow Summary
Include in system refresh report:
```sql
SELECT
COUNT AS total_runs,
COUNT FILTER AS successes,
COUNT FILTER AS failures,
ROUND , 1) AS avg_duration_s
FROM workflow_executions
WHERE DATE = CURRENT_DATE;
```
Format:
```
🔧 Workflow Summary :
• Total runs: [N] | Success: [N] | Failed: [N]
• Avg duration: [X]s
• Degraded: [list or "none"]
```