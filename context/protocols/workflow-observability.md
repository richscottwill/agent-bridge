# Workflow Observability Protocol

Cross-cutting concern — every cross-MCP workflow logs execution data to DuckDB.

**MCP Chain:** Any workflow → DuckDB → Slack (on failure/degradation)

---

## Workflow Logging Pattern

Every cross-MCP workflow MUST follow this logging pattern:

### At Workflow Start
```sql
INSERT INTO workflow_executions (execution_id, workflow_name, trigger_source, mcp_servers_involved, start_time)
VALUES ('{name}_{timestamp}', '{name}', '{trigger}', ARRAY['{mcp1}', '{mcp2}'], CURRENT_TIMESTAMP);
```

### At Each Step Completion
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
    duration_seconds = EPOCH(CURRENT_TIMESTAMP - start_time)
WHERE execution_id = '{id}';
```

Status rules:
- `completed` — all steps succeeded
- `partial` — some steps failed but workflow continued
- `failed` — critical step failed, workflow aborted

---

## Registered Workflows

| Workflow Name | MCPs Involved | Trigger |
|--------------|---------------|---------|
| `meeting_to_task` | Hedy, Asana, Slack, DuckDB | EOD-1 |
| `signal_to_task` | Outlook, Slack, Asana, DuckDB | AM-1/AM-2 |
| `wbr_quip_publish` | SharePoint, DuckDB, Builder, Slack | WBR watcher |
| `wiki_enriched_publish` | KDS, ARCC, XWiki, SharePoint | Wiki pipeline |
| `context_enrichment` | KDS, ARCC, DuckDB | EOD-2 |
| `slack_intelligence` | Slack, KDS, DuckDB | AM-1 |

---

## Degradation Detection (EOD-2)

Run during EOD-2 system refresh:

```sql
SELECT workflow_name, success_rate, total_runs, avg_duration_s
FROM workflow_reliability
WHERE success_rate < 80 AND total_runs >= 3;
```

If results → include in EOD-2 Slack DM:
```
⚠️ Degraded workflows (7-day window):
• {workflow}: {success_rate}% success ({total_runs} runs). Most common failure: {error}
```

---

## EOD-2 Workflow Summary

Include in system refresh report:

```sql
SELECT
    COUNT(*) AS total_runs,
    COUNT(*) FILTER (WHERE status = 'completed') AS successes,
    COUNT(*) FILTER (WHERE status = 'failed') AS failures,
    ROUND(AVG(duration_seconds), 1) AS avg_duration_s
FROM workflow_executions
WHERE DATE(start_time) = CURRENT_DATE;
```

Format:
```
🔧 Workflow Summary (today):
• Total runs: [N] | Success: [N] | Failed: [N]
• Avg duration: [X]s
• Degraded: [list or "none"]
```
