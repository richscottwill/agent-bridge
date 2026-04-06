# EOD-Frontend Protocol — Summary + Decisions + Report

Interactive (light-touch). Reads pre-computed state from EOD-Backend. Presents summary and collects decisions.

---

## Context Load
Pre-computed state files (from EOD-Backend):
- `~/shared/context/active/eod-reconciliation.json`
- `~/shared/context/active/eod-maintenance.json`
- `~/shared/context/active/eod-experiments.json`
- rw-tracker.md (updated by backend), hands.md (updated by backend)

---

## Step 1: EOD Summary

Present the day's results:

```
📊 EOD Summary — [date]

✅ Completed: [N] tasks
  [list with Routine bucket + L1-L5 tag]

⏩ Carried Forward: [N] tasks (demoted Today → Urgent)
  [list with reason + next action]

🆕 New Since Morning: [N] tasks
  [list — flag any needing triage]

📈 Five Levels: L1: [N], L2: [N], L3: [N], L4: [N], L5: [N]
  [highlight zero-effort levels: "No L1 effort — streak at risk."]

🔒 Blockers: [N] active
  [task, owner, days blocked]
```

---

## Step 2: Decisions Needed

### Recurring Task Approval
From eod-reconciliation.json → recurring_proposals:
```
🔄 Recurring task completed — next instance needed:
- [task name]: cadence [X], next due [date]. Create? (approve/skip)
```

### Carry-Forward Decisions
Any tasks that need more than a simple demote — extend due date? Kill? Delegate?

### Blocker Updates
New blockers detected — confirm and add to registry?

---

## Step 3: Portfolio + ABPS AI Summary

```
📊 PORTFOLIO EOD:
- Completed: [N] tasks across [projects]
- New overdue: [N]
- Enrichment: coverage [morning]% → [current]%
- Recurring: [N] new instances
- Blockers: [N] new, [N] resolved

🏭 ABPS AI:
- Completed: [N], Pipeline advances: [N], Refreshes: [N]
```

---

## Step 4: System Health

### Workflow Health
From eod-maintenance.json:
```
🔧 Workflows (24h): [total] runs, [success_rate]% success, avg [duration]s. [failures] failures.
[⚠️ Degraded: workflow_name at X% success if any]
```

### Compression Audit
From eod-maintenance.json:
```
🫁 Body: [X]w total. [any compression signals]
```

### Communication Analytics (Friday)
```
📞 Communication trends (4-week):
- Group meetings: avg [X]% speaking share
- Hedging: [trend]
- Action items: [trend]
[⚠️ Coaching signal if active]
```

### Context Enrichment
```
🧠 Context enrichment: [N] queries, [M] relevant findings.
```

---

## Step 5: Experiment Results

From eod-experiments.json (if experiments ran):
```
🧪 Karpathy: [N] experiments run
- [experiment summaries]
- Suggestions: [up to 3]
```

---

## Step 6: Slack DM Summary

Post to Richard's Slack DM:
```
self_dm(login="prichwil", text="📊 EOD Summary — [date]
✅ [N] completed | ⏩ [N] carried fwd | 🆕 [N] new
📈 L1:[N] L2:[N] L3:[N] L4:[N] L5:[N]
🔒 [N] blockers | 🔧 Workflows: [rate]% success
🧪 [N] experiments | 📚 Wiki: [status]
💾 Git pushed. Changelog updated.")
```

---

## Log Hook Execution
```sql
INSERT INTO hook_executions (hook_name, execution_date, start_time, end_time, duration_seconds,
    phases_completed, asana_reads, asana_writes, slack_messages_sent, duckdb_queries, summary)
VALUES ('eod-frontend', CURRENT_DATE, '[start]', '[end]', [duration],
    [phases], [reads], [writes], [slack_msgs], [queries], '[summary]');
```
