<!-- DOC-0351 | duck_id: protocol-eod-system-refresh -->
# EOD System Refresh Protocol

Phases ordered by criticality. Execute in order. Do not skip ahead.

All Asana writes follow the Guardrail Protocol in asana-command-center.md.

---

## Phase 1: Asana EOD Reconciliation

### Context Load
heart.md, changelog.md, current.md, gut.md, slack-scan-state.json, asana-command-center.md.
DuckDB: All queries go through DuckDB MCP (`execute_query`). Do NOT use Python `duckdb.connect()` with MotherDuck tokens. The MCP server is already connected to `ps_analytics`. If a query fails, check MCP server status — do not fall back to direct Python connections.

### Step 0 — Asana Delta Sync to DuckDB
Execute the Delta Sync procedure from ~/shared/context/protocols/asana-duckdb-sync.md:
1. Pull today's completions → UPDATE asana_tasks
2. Detect new tasks since morning → INSERT into asana_tasks
3. Update daily snapshot in asana_task_history
4. Run coherence check (DuckDB vs hands.md, current.md, asana-command-center.md)
5. Query schema_changes for today's drift events → include in summary if any

After delta sync, DuckDB views are current. Use them for reconciliation below instead of re-querying Asana API.

### Step 1 — Pull Current State (via DuckDB + Time Travel)
1. Query DuckDB: `SELECT * FROM asana_tasks WHERE completed = FALSE AND deleted_at IS NULL` → all incomplete tasks.
2. Query DuckDB: `SELECT * FROM asana_tasks WHERE completed = TRUE AND completed_at::DATE = CURRENT_DATE` → tasks completed today.
3. **Time travel diff against morning state:** Instead of reading asana-morning-snapshot.json, clone the morning snapshot:
   ```sql
   -- Find today's most recent AM snapshot (created during AM-1)
   SELECT snapshot_name, created_ts FROM md_information_schema.database_snapshots
   WHERE database_name = 'ps_analytics' AND snapshot_name LIKE 'am_%'
   ORDER BY created_ts DESC LIMIT 1;
   -- Clone it for comparison
   CREATE DATABASE morning_state FROM ps_analytics (SNAPSHOT_NAME 'am_YYYYMMDD');
   ```
   Then diff:
   ```sql
   -- Tasks completed since morning
   SELECT c.task_gid, c.name FROM ps_analytics.main.asana_tasks c
   WHERE c.completed = TRUE AND c.task_gid IN (SELECT task_gid FROM morning_state.main.asana_tasks WHERE completed = FALSE);
   -- New tasks since morning
   SELECT c.task_gid, c.name FROM ps_analytics.main.asana_tasks c
   ANTI JOIN morning_state.main.asana_tasks m ON c.task_gid = m.task_gid;
   -- Priority changes since morning
   SELECT c.task_gid, c.name, m.priority_rw AS morning_priority, c.priority_rw AS current_priority
   FROM ps_analytics.main.asana_tasks c
   JOIN morning_state.main.asana_tasks m ON c.task_gid = m.task_gid
   WHERE c.priority_rw != m.priority_rw OR (c.priority_rw IS NULL) != (m.priority_rw IS NULL);
   ```
   Clean up after: `DROP DATABASE morning_state;`
   **Fallback:** If no AM snapshot exists (first run or snapshot missing), fall back to reading `~/shared/context/active/asana-morning-snapshot.json`.
4. Query DuckDB: `SELECT * FROM asana_overdue` → overdue tasks with days_overdue.
5. Query DuckDB: `SELECT * FROM asana_by_routine` → bucket distribution for cap checks.

### Step 2 — Daily Reset
For tasks that had Priority_RW=Today in the morning snapshot but remain incomplete:
- Demote to Priority_RW=Urgent: UpdateTask(custom_fields={'1212905889837829': '1212905889837831'})
- Update Kiro_RW: 'M/D: Carried fwd. [reason]. [next action].'
- Update Next action field with specific next step.
- This ensures tomorrow's AM-2 starts with a clean Today slate.

### Step 3 — Recurring Task Check
For each task completed today, check if it matches a known recurring pattern (Weekly Reporting, EU SSR Acq, AU meetings agenda, MBR callout, ie%CCP calc, AU invoice, budget confirmation, Bi-monthly Flash, Individual Goals update, Bi-weekly with Adi).
- If recurring: verify next instance exists (search by name + future due date).
- If missing: flag 'Recurring task [name] completed — next instance needed. Cadence: [X]. Create now?'
- If Richard approves: create next instance with same Routine + project.

### Step 4 — Update rw-tracker.md
- Tasks completed today (names + Routine buckets)
- Tasks carried forward
- New tasks received since morning
- Net delta
- Bucket counts

### Step 5 — Five Levels Breakdown
Classify each completed and carry-forward task by L1-L5 per asana-command-center.md mapping.
- Format: 'Five Levels today: L1: X, L2: Y, L3: Z, L4: W, L5: V.'
- Highlight zero-effort levels: 'No L1 effort today — streak at risk.'

### Step 6 — Blocker Registry
Scan Kiro_RW fields and recent comments for blocker mentions.
- Update hands.md blocker list: task name, blocker description, owner, date first detected, days blocked.
- Format: '2 blocked: [task] on [owner] (Nd), [task] on [owner] (Nd).'

### Step 7 — New Task Detection
Check for tasks assigned to Richard since morning. Flag any needing Routine/Priority triage.

### Step 8 — Update hands.md
Priority Actions from current Asana state (including blocker registry).

### Step 9 — State File Priority Patching
For each registered state file in `~/shared/context/protocols/state-file-engine.md` where status = ACTIVE:
1. Read the current state file .md from `~/shared/wiki/state-files/`
2. Filter today's reconciliation data to market-relevant tasks:
   - MX: tasks in MX project (GID from asana-command-center.md)
   - AU: tasks in AU project
   - WW Testing: tasks in WW Testing project
3. Regenerate ONLY the Strategic Priorities section:
   - Update priorities table with current deadlines and completion status
   - Update blocked items from the blocker registry (Step 6 output)
   - Update stakeholder actions from Asana comments and email signals
4. Patch the local .md file (touch ONLY Strategic Priorities + Blocked Items + Stakeholder Actions)
5. Validate: `python3 ~/shared/tools/state-files/validate_state_files.py`
6. Convert: `python3 ~/shared/tools/state-files/convert_state_files.py`
7. Log to DuckDB: `INSERT INTO workflow_executions (workflow_name, ...) VALUES ('state-file-eod-patch-[market]', ...)`

**Key constraint:** Do NOT regenerate State of Business, Lessons Learned, or Appendices. Those are AM-only. EOD only patches action-oriented sections.
Currently registered: MX (active), AU (planned), WW Testing (planned).

---

## Phase 2: Portfolio + ABPS AI Reconciliation

### ABPS AI Content Reconciliation

a. Pull ABPS AI state: GetTasksFromProject(project_gid='1213917352480610', opt_fields='name,assignee.name,due_on,completed,completed_at,memberships.section.name,custom_fields.name,custom_fields.display_value'). Compare against morning snapshot abps_ai section.

b. ABPS completions today: tasks completed today with section and pipeline stage. Include in rw-tracker: 'ABPS AI: [N] completed, [N] pipeline advances, [N] refreshes.'

c. Pipeline progress: detect stage advances (research→draft, draft→review, review→approved, approved→active/archive).

d. ABPS daily reset: same as My Tasks — demote Today→Urgent for incomplete ABPS tasks. Update Kiro_RW with carry-forward context.

e. Five Levels — ABPS AI: all ABPS work counts as L5. Include in summary.

f. Update rw-tracker with ABPS stats: completed, advances, refreshes, new_intake.

### Step 10B — Completion Section Moves

For each task completed today across all managed projects:
1. Check if the task is in a non-terminal section (i.e., not already in a Complete section).
2. If yes, move it to the project's terminal section via AddTaskToSection or section membership update.
3. Terminal section GID map:
   - AU Complete: `1213924252564467`
   - MX Complete: `1213924047255341`
   - WW Testing Complete: `1205997667578902`
   - WW Acquisition Complete: `1206011240457091`
   - Paid App Complete: `1205997667578889`
4. Log each section move in the audit trail: `{"tool":"SectionMove","task_gid":"...","from_section":"...","to_section":"Complete","project":"...","result":"success"}`.
5. Skip tasks that are already in a terminal section or have no project membership.

### Portfolio Project Reconciliation

a. Use the morning time travel clone (from Step 1) or query `asana_task_history` for morning snapshot data. If the morning_state database is still attached, use it directly. Otherwise query:
```sql
SELECT * FROM asana_task_history WHERE snapshot_date = CURRENT_DATE;
```

b. For each managed project (AU, MX, WW Testing, WW Acq, Paid App): query `asana_tasks WHERE project_name = '[project]'` → compare against morning history.

c. Surface changes: tasks completed, new overdue, enrichment coverage changes, recurring tasks created, blocker changes.

d. Portfolio EOD output:
```
📊 PORTFOLIO EOD:
- Completed: [N] tasks across [projects]
- New overdue: [N] tasks
- Enrichment: [N] fields filled (coverage: [morning]% → [current]%)
- Recurring: [N] new instances
- Blockers: [N] new, [N] resolved
```

e. Update rw-tracker: 'Portfolio: completed=[N], new_overdue=[N], enriched=[N], recurring=[N]'

### Context Surface Refresh (weekly, or on significant changes)
- Update AU context task (GID: `1213917747438931`) html_notes with current state.
- Update MX context task (GID: `1213917639688517`) html_notes with current state.
- Read-before-write. Keep under 4000 chars. M/D date stamps. Recent Decisions is append-only.
- Frequency: every Friday EOD, or on major decision/status change.

### Weekly Scorecard (Friday only)
Compile for rw-tracker.md: strategic artifacts shipped (Core + Important completed this week), tools built, low-leverage hours (Sweep+Admin volume), meetings with clear output.

---

## Phase 3: Organ Cascade + Maintenance

### Compression Audit
Before any organ updates, observe and log body size:
1. Count words in each organ file (`~/shared/context/body/*.md`). Log to DuckDB `organ_word_counts` (organ_name, measured_date, word_count) AND `body_size_history` (with Bayesian prior signals):
   ```sql
   INSERT INTO organ_word_counts (organ_name, measured_date, word_count) VALUES ('[organ]', CURRENT_DATE, [count])
   ON CONFLICT (organ_name, measured_date) DO UPDATE SET word_count = EXCLUDED.word_count;
   
   INSERT INTO body_size_history (measured_date, organ_name, word_count, add_prior_mean, compress_prior_mean, at_ceiling, has_compression_signal)
   SELECT CURRENT_DATE, '[organ]', [count],
       (SELECT alpha/(alpha+beta) FROM autoresearch_priors WHERE organ='[organ]' AND technique='ADD'),
       (SELECT alpha/(alpha+beta) FROM autoresearch_priors WHERE organ='[organ]' AND technique='COMPRESS'),
       (SELECT alpha/(alpha+beta) < 0.3 AND n_experiments >= 5 FROM autoresearch_priors WHERE organ='[organ]' AND technique='ADD'),
       (SELECT alpha/(alpha+beta) > 0.7 AND n_experiments >= 5 FROM autoresearch_priors WHERE organ='[organ]' AND technique='COMPRESS')
   ON CONFLICT (measured_date, organ_name) DO UPDATE SET word_count = EXCLUDED.word_count,
       add_prior_mean = EXCLUDED.add_prior_mean, compress_prior_mean = EXCLUDED.compress_prior_mean,
       at_ceiling = EXCLUDED.at_ceiling, has_compression_signal = EXCLUDED.has_compression_signal;
   ```
2. Query the `prior_convergence` view for budget signals:
   ```sql
   SELECT organ, technique, posterior_mean, n_experiments, budget_signal
   FROM prior_convergence WHERE budget_signal IN ('AT_CEILING', 'COMPRESS_SIGNAL');
   ```
3. Sum total body word count. Log it. No hard ceiling — the `organ_size_accuracy` view tracks the size-accuracy curve.
4. Report only when priors suggest action: `🫁 Body: [X]w. [organ] has compression signal (COMPRESS prior: [X], n=[X]).` If no organ has a compression signal, skip report entirely.

### Workflow Observability Check
Before organ updates, assess cross-MCP pipeline health:

1. **Degradation detection:** Query DuckDB for workflows with <80% success rate over 7 days:
```sql
SELECT workflow_name, success_rate, total_runs, avg_duration_s, last_run
FROM workflow_reliability
WHERE success_rate < 80 AND total_runs >= 3;
```
If results → flag in EOD-2 Slack DM:
```
⚠️ Degraded workflows (7-day window):
• {workflow}: {success_rate}% success ({total_runs} runs)
```

2. **Workflow summary:** Query overall execution stats:
```sql
SELECT
    COUNT(*) AS total_runs,
    ROUND(COUNT(*) FILTER (WHERE status = 'completed') * 100.0 / NULLIF(COUNT(*), 0), 1) AS success_rate,
    ROUND(AVG(duration_seconds), 1) AS avg_duration_s,
    COUNT(*) FILTER (WHERE status = 'failed') AS failures
FROM workflow_executions
WHERE start_time > CURRENT_TIMESTAMP - INTERVAL '24 hours';
```
Include in system refresh report:
```
🔧 Workflows (24h): {total_runs} runs, {success_rate}% success, avg {avg_duration_s}s. {failures} failures.
```

3. If no workflow_executions data exists yet, skip silently — no error.

### Maintenance
- Refresh ground truth in organs.
- Process intake/ files. Route Slack signals.
- Dashboard + focus update.

### Context Enrichment (KDS/ARCC)
Execute `~/shared/context/protocols/context-enrichment.md`:
1. Read current.md → extract active project names and topics
2. Generate 3-5 KDS queries from active projects
3. Execute KDS queries, score relevance (0-10) against project context
4. For findings with relevance >= 7: create intake files at `~/shared/context/intake/kds-{date}-{topic}.md`
5. Route findings: strategic → brain.md, market data → eyes.md, relationships → memory.md
6. Log all queries to enrichment_log in DuckDB
7. If 3 consecutive runs returned 0 relevant results: regenerate queries from updated current.md
8. Include enrichment summary in EOD-2 report: `🧠 Context enrichment: {N} queries, {M} relevant findings.`

If KDS is unreachable, skip enrichment and continue — this is non-blocking.

### Cascade
All organs. Skip <48h + minor changes. Volume control. Hot topics. People Watch.

---

## Phase 4: Recurring Task State Checks

Query DuckDB `recurring_task_state` table instead of reading JSON file. For each task:
```sql
SELECT task_key, cadence, last_run, last_run_period, description
FROM recurring_task_state;
```
- Compute current_period from today's date and cadence (monthly=YYYY-MM, weekly=YYYY-WNN, quarterly=YYYY-QN).
- If last_run_period != current_period → task is DUE.
- Run all due tasks. After each, update DuckDB:
  ```sql
  UPDATE recurring_task_state SET last_run = CURRENT_DATE, last_run_period = '[period]',
      updated_at = CURRENT_TIMESTAMP, notes = '[notes]' WHERE task_key = '[key]';
  ```
- Also update the JSON file as fallback: `~/shared/context/active/recurring-task-state.json` (keep in sync until fully deprecated).
- Quick check view: `SELECT * FROM recurring_tasks_due WHERE is_due = TRUE;`

### Due Task Procedures
- **goal_updater** (monthly): Read asana-goal-updater-protocol.md. Execute Steps 1-8. Goal GIDs: 1213245014119128, 1213204514049680, 1213204514049684, 1213245014119125, 1213204514049688, 1213204514049691, 1213204514049694, 1213204514049706, 1213245014119131, 1213204514049667, 1213204514049671, 1213204514049810, 1213204514049812, 1213204514049830. Update children before parents. Draft-first.
- **meta_calibration_priors** (monthly): Prior-guided vs random comparison per meta-calibration-proposal.md.
- **meta_calibration_projections** (weekly): Audit last week's projection against actuals. Update au-projections.md.
- **meta_calibration_output_quality** (quarterly): Validate output-quality prior convergence.
- **coherence_audit** (monthly): Cross-organ dependency matrix, gap/stale/dupe detection.
- **weekly_scorecard** (weekly/Friday): Compile weekly stats for rw-tracker.md.
- **context_surface_refresh** (weekly): Update AU/MX pinned context tasks in Asana.
- **agent_bridge_sync** (weekly/Friday): Sync shared/ to GitHub.

### Due Task Procedure: wiki_lint (weekly)
Invoke the wiki-audit skill. The audit checks:
1. Orphan scan: files in ~/shared/wiki/ not listed in wiki-index.md.
2. Stale content: articles past their update-trigger window or with outdated data references.
3. Broken cross-references: wikilinks pointing to archived/missing articles.
4. Missing frontmatter: articles missing required fields (title, status, audience, level, update-trigger, doc-type).
5. SITEMAP drift: compare SITEMAP.md article count against wiki-index.md.
6. wiki-index consistency: section header counts vs actual article counts.
7. **Signal-based freshness:** For each article, query signal_tracker for recent mentions of the article's topic. If recent_mentions > 3 AND article.updated > 14 days → flag as stale with active discussion. Per signal-intelligence.md Use Case 4.
8. **Idea sourcing:** Query `signal_wiki_candidates` view for topics with strong multi-channel signals but no matching wiki article. Report as organic wiki candidates.
Write results to ~/shared/wiki/health/health-YYYY-MM-DD.md and ~/shared/wiki/audits/audit-YYYY-MM-DD.md.
Report summary only: `📚 Wiki lint: [N] healthy, [N] stale, [N] orphaned, [N] broken refs. [N] wiki candidates from signals.` If all clean, skip report.

### Communication Analytics (weekly)
Execute ~/shared/context/protocols/communication-analytics.md:
- Compute weekly communication trends from meeting_analytics (trailing 4 weeks)
- Check coaching signal: group meeting speaking share < 15% for 3+ consecutive weeks
- Include trends in system refresh report
- If coaching signal active: flag in EOD-2 Slack DM

### Enrichments
- Weekly relationship (Friday). Wiki candidates (weekly). Wiki lint (weekly). Monthly synthesis (1st). Quarterly audit (90d).

---

## Phase 5: Housekeeping

**This phase is NOT expendable. Execute before experiments.**

- **DuckDB daily snapshot (via MCP):** Create a named snapshot for time travel and audit using `execute_query`:
  ```sql
  CREATE SNAPSHOT eod_YYYYMMDD OF ps_analytics;
  ```
  Use today's date (e.g., `eod_20260406`). This enables tomorrow's AM-1 to diff against today's EOD state. Named snapshots persist until explicitly dropped — clean up snapshots older than 30 days:
  ```sql
  -- List old snapshots
  SELECT snapshot_name, created_ts FROM md_information_schema.database_snapshots
  WHERE database_name = 'ps_analytics' AND snapshot_name LIKE 'eod_%'
  AND created_ts < CURRENT_TIMESTAMP - INTERVAL '30 days';
  -- Drop old ones (if any): ALTER SNAPSHOT old_name SET snapshot_name = '';
  ```

- **DuckDB daily tracker insert:** After all reconciliation is complete, insert today's summary:
  ```sql
  INSERT INTO daily_tracker (tracker_date, completed_count, carried_forward_count, new_tasks_count, net_delta,
      bucket_sweep, bucket_core, bucket_engine, bucket_admin, bucket_backlog,
      total_incomplete, total_overdue, l1_effort, l2_effort, l3_effort, l4_effort, l5_effort,
      hard_thing_status, workdays_at_zero, blocker_count, abps_completed, portfolio_completed, notes)
  VALUES (CURRENT_DATE, [completed], [carried], [new], [delta],
      [sweep], [core], [engine], [admin], [backlog],
      [incomplete], [overdue], [l1], [l2], [l3], [l4], [l5],
      '[status]', [days], [blockers], [abps], [portfolio], '[notes]');
  ```

- **DuckDB L1 streak insert:**
  ```sql
  INSERT INTO l1_streak (tracker_date, workdays_at_zero, hard_thing_task_gid, hard_thing_name)
  VALUES (CURRENT_DATE, [days], '[gid]', '[name]');
  ```

- **Steering integrity check (before staging):** Read `~/.kiro/steering/context/steering-integrity.md`. Verify no files from the Deleted Files table exist in `~/.kiro/steering/`. If found, delete them before staging. Verify all steering files have front matter with an explicit inclusion mode.
- Git sync push: `git -C ~/shared add -A && git commit -m "EOD-2 [date]" && git push`
- Deduplicate MCP.
- Self-audit: cascade completeness, structural changes, coherence. Log to changelog.md.
- **Log hook execution:**
  ```sql
  INSERT INTO hook_executions (hook_name, execution_date, start_time, end_time, duration_seconds,
      phases_completed, phases_failed, asana_reads, asana_writes, slack_messages_sent, duckdb_queries, summary)
  VALUES ('eod-refresh', CURRENT_DATE, '[start]', '[end]', [duration],
      [completed], [failed], [reads], [writes], [slack_msgs], [queries], '[summary]');
  ```

---

## Phase 6: Experiments

**Not expendable. Run every EOD-2.**

Invoke Karpathy via the loop script: `bash ~/shared/tools/karpathy-loop.sh "[cooldown_organs]" [max_batches]`

The loop script launches Karpathy CLI in batches of ~10 experiments, relaunching with fresh context windows until Bayesian priors exhaust eligible targets. No artificial experiment cap — the priors ARE the stopping mechanism (heart.md Step 6). The max_batches param (default 20) is a safety limit against infinite loops, not a target. Karpathy signals exhaustion by writing /tmp/karpathy-exhausted. Two consecutive empty batches also trigger a stop.

**First-experiment verification (mandatory for ALL CLI agent pipelines):** Whenever launching a CLI agent batch that invokes other CLI agents (autoresearch eval agents, wiki pipeline agents, or any ad-hoc multi-agent workflow), monitor the first experiment/task through to completion. Confirm:
1. CLI sub-agents are actually invoked (shell tool calls with `kiro-cli chat --agent` visible)
2. Results come back from separate processes (not self-scored or self-completed)
3. Output and decisions are correct
Only then let the batch run unattended. If the first iteration self-scores or skips the CLI invocation, stop and fix the prompt. This applies to autoresearch, wiki pipelines, and any future multi-agent workflow.

Karpathy CLI agent receives context: heart.md, gut.md, karpathy.md, list of organs modified in Phases 1-3 (cooldown list).

If Karpathy CLI invocation fails: skip experiments. Do not fall back to self-execution.

### Suggestions
Up to 3. Five Levels aligned, measurable, reversible.
