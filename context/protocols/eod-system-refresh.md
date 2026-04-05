# EOD System Refresh Protocol

Phases ordered by criticality. Execute in order. Do not skip ahead.

All Asana writes follow the Guardrail Protocol in asana-command-center.md.

---

## Phase 1: Asana EOD Reconciliation

### Context Load
heart.md, changelog.md, current.md, gut.md, slack-scan-state.json, asana-command-center.md.

### Step 1 — Pull Current State
1. SearchTasksInWorkspace(assignee=1212732742544167, completed=false) → all incomplete tasks.
2. SearchTasksInWorkspace(assignee=1212732742544167, completed=true, completed_on=today) → tasks completed today.
3. Read morning snapshot: ~/shared/context/active/asana-morning-snapshot.json.

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

a. Read morning snapshot → portfolio_projects section.

b. For each managed project (AU, MX, WW Testing, WW Acq, Paid App): GetTasksFromProject → compare against morning stats.

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
1. Count words in each organ file (`~/shared/context/body/*.md`). Log to DuckDB `autoresearch_organ_health` (organ, word_count, date).
2. Query DuckDB for organ-level Bayesian priors from `autoresearch_experiments`. Flag any organ where COMPRESS posterior_mean > 0.7 (n > 5) — these have data-backed evidence they can shrink without accuracy loss.
3. Sum total body word count. Log it. No hard ceiling — the aggregate size-accuracy curve in DuckDB determines when the body is too large (accuracy plateaus or degrades as size increases).
4. Report only when priors suggest action: `🫁 Body: [X]w. [organ] has compression signal (COMPRESS prior: [X], n=[X]).` If no organ has a compression signal, skip report entirely.

### Maintenance
- Refresh ground truth in organs.
- Process intake/ files. Route Slack signals.
- Dashboard + focus update.

### Cascade
All organs. Skip <48h + minor changes. Volume control. Hot topics. People Watch.

---

## Phase 4: Recurring Task State Checks

Read ~/shared/context/active/recurring-task-state.json. For each task:
- Compute current_period from today's date and cadence (monthly=YYYY-MM, weekly=YYYY-WNN, quarterly=YYYY-QN).
- If last_run_period != current_period → task is DUE.
- Run all due tasks. After each, update last_run and last_run_period.

### Due Task Procedures
- **goal_updater** (monthly): Read asana-goal-updater-protocol.md. Execute Steps 1-8. Goal GIDs: 1213245014119128, 1213204514049680, 1213204514049684, 1213245014119125, 1213204514049688, 1213204514049691, 1213204514049694, 1213204514049706, 1213245014119131, 1213204514049667, 1213204514049671, 1213204514049810, 1213204514049812, 1213204514049830. Update children before parents. Draft-first.
- **meta_calibration_priors** (monthly): Prior-guided vs random comparison per meta-calibration-proposal.md.
- **meta_calibration_projections** (weekly): Audit last week's projection against actuals. Update au-projections.md.
- **meta_calibration_output_quality** (quarterly): Validate output-quality prior convergence.
- **coherence_audit** (monthly): Cross-organ dependency matrix, gap/stale/dupe detection.
- **weekly_scorecard** (weekly/Friday): Compile weekly stats for rw-tracker.md.
- **context_surface_refresh** (weekly): Update AU/MX pinned context tasks in Asana.
- **agent_bridge_sync** (weekly/Friday): Sync portable-body/ to GitHub.

### Due Task Procedure: wiki_lint (weekly)
Invoke the wiki-audit skill. The audit checks:
1. Orphan scan: files in ~/shared/artifacts/ not listed in wiki-index.md.
2. Stale content: articles past their update-trigger window or with outdated data references.
3. Broken cross-references: wikilinks pointing to archived/missing articles.
4. Missing frontmatter: articles missing required fields (title, status, audience, level, update-trigger, doc-type).
5. SITEMAP drift: compare SITEMAP.md article count against wiki-index.md.
6. wiki-index consistency: section header counts vs actual article counts.
7. **Signal-based freshness:** For each article, query signal_tracker for recent mentions of the article's topic. If recent_mentions > 3 AND article.updated > 14 days → flag as stale with active discussion. Per signal-intelligence.md Use Case 4.
8. **Idea sourcing:** Query `signal_wiki_candidates` view for topics with strong multi-channel signals but no matching wiki article. Report as organic wiki candidates.
Write results to ~/shared/context/wiki/health/health-YYYY-MM-DD.md and ~/shared/context/wiki/audits/audit-YYYY-MM-DD.md.
Report summary only: `📚 Wiki lint: [N] healthy, [N] stale, [N] orphaned, [N] broken refs. [N] wiki candidates from signals.` If all clean, skip report.

### Enrichments
- Weekly relationship (Friday). Wiki candidates (weekly). Wiki lint (weekly). Monthly synthesis (1st). Quarterly audit (90d).

---

## Phase 5: Housekeeping

**This phase is NOT expendable. Execute before experiments.**

- Git sync push: `git -C ~/shared add -A && git commit -m "EOD-2 [date]" && git push`
- Deduplicate MCP.
- Self-audit: cascade completeness, structural changes, coherence. Log to changelog.md.

---

## Phase 6: Experiments

**Last phase. Expendable if context is heavy.**

Delegate to Karpathy subagent. Do NOT run experiments yourself.

Invoke Karpathy subagent with context: heart.md, gut.md, karpathy.md, list of organs modified in Phases 1-3 (cooldown list).

The Karpathy subagent runs the autoresearch loop per heart.md protocol. The executing agent receives results and reports them.

If subagent invocation fails: skip experiments. Do not fall back to self-execution.

### Suggestions
Up to 3. Five Levels aligned, measurable, reversible.
