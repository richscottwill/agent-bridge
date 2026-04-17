<!-- DOC-0349 | duck_id: protocol-eod-frontend -->
# EOD-Frontend Protocol — Summary + Decisions + Report

Interactive (light-touch). Reads pre-computed state from EOD-Backend. Presents summary and collects decisions.

---

## HARD GATE — Backend Completion Check (MANDATORY)

**Before presenting ANY frontend output, verify all three backend JSON files exist with today's date:**

1. Check `~/shared/context/active/eod-reconciliation.json` — must exist, `generated` field must be today's date.
2. Check `~/shared/context/active/eod-maintenance.json` — must exist, `generated` field must be today's date.
3. Check `~/shared/context/active/eod-experiments.json` — must exist, `generated` field must be today's date.

**If ANY file is missing or stale:**
- Do NOT proceed to Step 1.
- Do NOT present a partial summary.
- Instead, go back and complete the missing backend phase that produces the missing file.
- If the backend phase genuinely cannot run (tool unavailable, MCP down), create the JSON with `{"generated": "YYYY-MM-DD", "status": "skipped", "reason": "[specific reason]"}` so the skip is explicit and visible.

**If all three files pass the gate**, read the eod-phase-tracker.md checklist. If any backend phase shows ❌ or is unchecked, the first line of the EOD summary MUST be:
```
⚠️ INCOMPLETE RUN — Phases [list] were skipped: [reasons]
```
This warning goes BEFORE the task table, not buried in System Health.

---

## Context Load
Pre-computed state files (from EOD-Backend):
- `~/shared/context/active/eod-reconciliation.json`
- `~/shared/context/active/eod-maintenance.json`
- `~/shared/context/active/eod-experiments.json`
- rw-tracker.md (updated by backend), hands.md (updated by backend)

### SharePoint Fallback (Cold Start / Missing Files)
If any pre-computed state file is missing locally (container restart between backend and frontend):
1. Check SharePoint `Kiro-Drive/system-state/` for the file via `sharepoint_read_file(inline=true)`.
2. If found and Modified timestamp is <24h old → use it.
3. If not found → this triggers the HARD GATE above. Go complete the backend phase.
4. Log recovery to DuckDB workflow_executions.
See ~/shared/context/protocols/sharepoint-durability-sync.md for full pull logic.

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

### Recurring Task Summary (informational)
From eod-reconciliation.json → recurring_created:
```
🔄 Recurring tasks auto-created:
- [task name]: next due [date] ✅
```
(Auto-created by backend. No approval needed.)

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
💾 Git pushed. SharePoint synced. Changelog updated.")
```

---

## Log Hook Execution
```sql
INSERT INTO hook_executions (hook_name, execution_date, start_time, end_time, duration_seconds,
    phases_completed, asana_reads, asana_writes, slack_messages_sent, duckdb_queries, summary)
VALUES ('eod-frontend', CURRENT_DATE, '[start]', '[end]', [duration],
    [phases], [reads], [writes], [slack_msgs], [queries], '[summary]');
```
