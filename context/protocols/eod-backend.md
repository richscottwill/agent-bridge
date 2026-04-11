<!-- DOC-0348 | duck_id: protocol-eod-backend -->
# EOD-Backend Protocol — Meeting Sync + Reconciliation + Maintenance

Fully autonomous. No interaction needed. Produces structured output for EOD-Frontend.

All Asana writes follow the Guardrail Protocol in asana-command-center.md.

**Constraint:** This hook runs as a direct agent turn (not subagent) because Phase 6 (Karpathy experiments) uses subagents for blind A/B/C eval, and subagents can't invoke their own subagents.

---

## Phase 1: Meeting Ingestion

### Context Load
meetings/README.md, current.md, nervous-system.md, memory.md, asana-command-center.md.

### Hedy Pull
- GetSessions (today), GetSessionDetails for each.
- Extract: highlights, todos, action items, speaking share, hedging count.

### Outlook + Email
- Auto-meeting folder scan.
- Email threads related to meetings.

### Meeting Series File Updates
For each session: ONE Latest Session entry, Open Items, Running Themes in meetings/ series files.

### Organ Updates (autonomous)
- memory.md: relationship updates from meeting dynamics.
- nervous-system.md: Loop 7 (meeting patterns), Loop 3 (pattern trajectory).
- current.md: people updates, new action items.
- device.md: delegation updates.

### Meeting-to-Task Pipeline
Per ~/shared/context/protocols/meeting-to-task-pipeline.md:
1. Extract action items from each session.
2. Richard's items → dedup check → CreateTask or AddComment.
3. Others' items → append to hands.md dependencies.
4. INSERT into DuckDB meeting_analytics + meeting_highlights.
5. Log to workflow_executions.

### Output
Queue for EOD-Frontend:
- Tasks created/updated from meetings.
- Dependencies logged.
- Meeting analytics summary.


---

## Phase 2: Asana EOD Reconciliation

### Context Load
heart.md, changelog.md, current.md, gut.md, asana-command-center.md.

### Step 0 — Delta Sync to DuckDB
Execute ~/shared/context/protocols/asana-duckdb-sync.md delta sync:
1. Pull today's completions → UPDATE asana_tasks.
2. Detect new tasks since morning → INSERT.
3. Update daily snapshot in asana_task_history.
4. Run coherence check.

### Step 1 — Time Travel Diff
```sql
SELECT snapshot_name FROM md_information_schema.database_snapshots
WHERE database_name = 'ps_analytics' AND snapshot_name LIKE 'am_%'
ORDER BY created_ts DESC LIMIT 1;

CREATE DATABASE morning_state FROM ps_analytics (SNAPSHOT_NAME 'am_YYYYMMDD');
```
Diff: completions since morning, new tasks, priority changes. Clean up: `DROP DATABASE morning_state;`

### Step 2 — Daily Reset (AUTO-EXECUTE)
Tasks with Priority_RW=Today in morning but still incomplete → demote to Urgent.
Update Kiro_RW: 'M/D: Carried fwd. [reason]. [next action].'
Queue carry-forward list for EOD-Frontend presentation.

### Step 3 — Recurring Task Auto-Creation (AUTO-EXECUTE)
For each task completed today, check against known recurring patterns.
If recurring and next instance missing → auto-create next instance with same Routine_RW + project + assignee.
Log each creation to audit trail. Include in EOD-Frontend summary (informational, not approval).

### Step 4 — Completion Section Moves (AUTO-EXECUTE)
Move completed tasks to terminal sections:
- AU Complete: `1213924252564467`
- MX Complete: `1213924047255341`
- WW Testing Complete: `1205997667578902`
- WW Acquisition Complete: `1206011240457091`
- Paid App Complete: `1205997667578889`
Log each move to audit trail.

### Step 5 — Blocker Registry
Scan Kiro_RW and comments for blocker mentions. Queue updates for EOD-Frontend.

### Step 6 — New Task Detection
Tasks assigned to Richard since morning needing triage. Queue for EOD-Frontend.

### Step 7 — Five Levels Classification
Classify completed + carry-forward tasks by L1-L5. Compute daily effort distribution.

### Step 8 — Portfolio + ABPS AI Reconciliation
a. ABPS AI Content: completions, pipeline advances, refreshes, daily reset.
b. Portfolio projects: compare against morning state. Surface changes.
c. Context surface refresh (weekly or on significant changes): AU (`1213917747438931`), MX (`1213917639688517`).

### Output
Write to `~/shared/context/active/eod-reconciliation.json`:
```json
{
  "completed_today": [...],
  "carried_forward": [...],
  "new_tasks": [...],
  "recurring_proposals": [...],
  "blocker_updates": [...],
  "five_levels": {"l1": N, "l2": N, "l3": N, "l4": N, "l5": N},
  "portfolio_changes": {...},
  "abps_ai_changes": {...}
}
```

---

## Phase 3: Organ Cascade + Maintenance

### Compression Audit
1. Count words in each organ. Log to DuckDB organ_word_counts + body_size_history.
2. Query prior_convergence for budget signals.
3. Report only when priors suggest action.

### Workflow Observability Check
1. Query workflow_reliability for degraded workflows (<80% success, >=3 runs).
2. Query workflow_executions for 24h summary.
3. Queue alerts for EOD-Frontend.

### Communication Analytics (weekly — Friday only)
Execute ~/shared/context/protocols/communication-analytics.md:
- Weekly trends from meeting_analytics (trailing 4 weeks).
- Coaching signal: group speaking share < 15% for 3+ consecutive weeks.
- Queue results for EOD-Frontend.

### Context Enrichment (KDS/ARCC)
Execute ~/shared/context/protocols/context-enrichment.md:
1. Read current.md → extract active projects.
2. Generate 3-5 KDS queries.
3. Score relevance, create intake files for findings >= 7.
4. Log to enrichment_log in DuckDB.
Non-blocking — skip if KDS unreachable.

### Organ Cascade
All organs. Skip <48h + minor changes. Volume control. Hot topics. People Watch. Process intake/ files.

---

## Phase 4: Recurring Task State Checks

Query DuckDB recurring_task_state. For each due task, execute its procedure:
- goal_updater (monthly), meta_calibration_priors (monthly), meta_calibration_projections (weekly), coherence_audit (monthly), weekly_scorecard (Friday), context_surface_refresh (weekly), agent_bridge_sync (Friday), wiki_lint (weekly).

Update DuckDB + JSON fallback after each.

---

## Phase 5: Housekeeping

**Not expendable. Execute before experiments.**

- MotherDuck EOD snapshot: `CREATE SNAPSHOT eod_YYYYMMDD OF ps_analytics;`
- Clean up snapshots > 30 days.
- DuckDB daily_tracker insert (completed, carried, new, delta, buckets, levels, hard thing).
- DuckDB l1_streak insert.
- Steering integrity check.
- Git sync: `git -C ~/shared add -A && git commit -m "EOD [date]" && git push`
- Self-audit: cascade completeness, structural changes, coherence.
- Log to changelog.md.
- Log hook execution to hook_executions in DuckDB.

---

## Phase 6: Experiments

**Not expendable. Run every EOD.**

Invoke Karpathy via loop script: `bash ~/shared/tools/scripts/karpathy-loop.sh [target_total] "[cooldown_organs]"`

First-experiment verification mandatory: confirm CLI sub-agents are actually invoked, results come from separate processes, output is correct. Only then let batch run unattended.

If Karpathy CLI fails: skip experiments. Do not fall back to self-execution.

### Suggestions
Up to 3. Five Levels aligned, measurable, reversible.

---

## Phase 7: Compile Output

Write all computed state to structured files for EOD-Frontend:
1. `~/shared/context/active/eod-reconciliation.json` — reconciliation results
2. `~/shared/context/active/eod-maintenance.json` — organ cascade results, workflow health, enrichment summary
3. `~/shared/context/active/eod-experiments.json` — Karpathy experiment results (if any)
4. Updated rw-tracker.md, hands.md, changelog.md (already written in earlier phases)
