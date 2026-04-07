<!-- DOC-0329 | duck_id: protocol-am-backend-parallel -->
# AM-Backend Protocol — Parallel Architecture

Replaces the sequential am-backend.md with a parallel-first design. Ingestion fans out to 3 concurrent subagents. Processing runs sequentially after all ingestion completes.

---

## Why Parallel

Phase 1 (Data Collection) has 3 independent data streams:
- Slack scan → reads Slack MCP, writes slack-digest.md + DuckDB
- Asana sync → reads Asana MCP, writes DuckDB + asana-digest.md
- Email scan → reads Outlook MCP, writes email-triage.md

These have zero data dependencies. Running them sequentially wastes ~10 min.

Phase 2+ (Processing) depends on Phase 1 outputs:
- Signal-to-task needs Slack + email intake to exist
- Enrichment scan needs Asana sync to be complete
- Portfolio scan needs Asana sync + command center state
- ABPS AI scan needs Asana sync

Processing MUST wait for all ingestion to finish.

---

## Architecture

```
AM-Backend Hook (orchestrator)
│
├─ Phase 0: Schema Verification (orchestrator, ~10s)
│   └─ DuckDB quick check — database, schema, table count
│
├─ Phase 1: PARALLEL INGESTION (4 subagents, ~4 min wall-clock)
│   │
│   ├─ Subagent A: Slack Ingestion (~4 min, longest)
│   │   ├─ list_channels (unreadOnly=true)
│   │   ├─ Apply depth rules + relevance filter
│   │   ├─ Produce slack-digest.md
│   │   ├─ RSW-channel intake
│   │   ├─ Proactive search (prichwil, brandoxy, kataxt)
│   │   ├─ Update slack-scan-state.json
│   │   ├─ DuckDB batch writes (signals.slack_messages, signals.signal_tracker)
│   │   └─ Signal intelligence (topic extraction, FTS reinforcement, decay)
│   │
│   ├─ Subagent B1: Asana Sync + DuckDB (~3 min)
│   │   ├─ SearchTasksInWorkspace (Richard, incomplete)
│   │   ├─ GetTasksFromProject for each portfolio project (AU, MX, WW Testing, WW Acq, Paid App)
│   │   ├─ UPSERT into asana.asana_tasks
│   │   ├─ INSERT daily snapshot into asana.asana_task_history
│   │   ├─ Soft-delete stale tasks
│   │   ├─ Coherence check + schema drift detection
│   │   ├─ Produce asana-digest.md
│   │   └─ Morning snapshot (legacy JSON fallback)
│   │
│   ├─ Subagent B2: Asana Activity Monitor (~2 min)
│   │   ├─ Read asana-scan-state.json for last scan timestamps
│   │   ├─ GetTaskStories per incomplete task — detect teammate activity
│   │   ├─ Classify: comment_added, due_date_changed, reassigned
│   │   ├─ Produce asana-activity.md
│   │   └─ Update asana-scan-state.json
│   │   NOTE: Zero DuckDB writes. File-only output.
│   │
│   └─ Subagent C: Email Ingestion (~1 min, fastest)
│       ├─ email_inbox (unread)
│       ├─ Classify by sender priority (Brandon/Kate/Todd = HIGH)
│       ├─ Produce email-triage.md
│       ├─ INSERT into signals.emails (DuckDB)
│       ├─ Skip Auto-Comms folder
│       ├─ Pull today's calendar: calendar_view(start_date=today, view=day)
│       └─ UPSERT into main.calendar_events (DuckDB)
│
│   └─ Subagent D: Loop Page Sync (~1 min)
│       ├─ Query docs.loop_pages for stale pages (>12h since last_ingested)
│       ├─ For each stale page: sharepoint_read_loop(loopUrl)
│       ├─ UPDATE docs.loop_pages with content_markdown, content_preview, word_count
│       └─ Update ops.data_freshness for loop_pages source
│       Protocol: ~/shared/context/protocols/loop-page-sync.md
│
├─ BARRIER: Wait for all subagents to complete
│   └─ If any subagent fails: log failure, continue with available data, flag in output
│
├─ Phase 2: SEQUENTIAL PROCESSING (orchestrator or single subagent, ~3 min)
│   │
│   ├─ Step 2A: Signal-to-Task Pipeline
│   │   ├─ Read slack-digest.md + email-triage.md
│   │   ├─ High-priority signals → dedup check → CreateTask or AddComment
│   │   ├─ Log to signal_task_log in DuckDB
│   │   └─ Log pipeline execution to workflow_executions
│   │
│   ├─ Step 2B: Slack Conversation Enrichment
│   │   ├─ Acronym/project detection in slack-digest signals
│   │   ├─ KDS enrichment for unfamiliar terms (max 5 queries)
│   │   └─ Store knowledge_context in DuckDB (skip if KDS unreachable)
│   │
│   ├─ Step 2C: Bucket Cap Check + Flags
│   │   ├─ Query asana.asana_tasks for bucket counts
│   │   ├─ Over cap → queue demotion proposals
│   │   ├─ Today + no Routine → queue for triage
│   │   └─ Overdue 7+ days → queue kill-or-revive
│   │
│   └─ Step 2D: Slack Decision Detection
│       └─ Scan slack-digest for decision keywords → queue for frontend
│
├─ Phase 3: ENRICHMENT SCAN (orchestrator or single subagent, ~2 min)
│   │
│   ├─ Step 3A: My Tasks Enrichment
│   │   ├─ Query asana.asana_tasks (already synced in Phase 1B)
│   │   ├─ Apply 4 enrichment rules (Kiro_RW, Next Action, dates, Priority_RW)
│   │   └─ Queue proposals to am-enrichment-queue.json § my_tasks
│   │
│   └─ Step 3B: ABPS AI Content Scan
│       ├─ Intake triage detection (untriaged tasks in Intake section)
│       ├─ Pipeline state detection (In Progress, Review, Active)
│       ├─ Near-due escalation (AUTO-EXECUTE: 0-2 days → Today)
│       ├─ Overdue flagging (queue for frontend)
│       ├─ Refresh cadence check (Active + recurring frequency)
│       └─ Write am-abps-ai-state.json
│
├─ Phase 4: PORTFOLIO SCAN (orchestrator or single subagent, ~3 min)
│   │
│   ├─ Step 4A: Portfolio Discovery
│   │   ├─ GetPortfolioItems for ABIX PS + ABPS
│   │   └─ New project detection → queue flag
│   │
│   ├─ Step 4B: Per-Project Task Scan + Enrichment
│   │   ├─ For each project: scan tasks, filter to Richard
│   │   ├─ Apply 4 enrichment rules → queue to am-enrichment-queue.json § portfolio
│   │   ├─ Near-due escalation (AUTO-EXECUTE)
│   │   └─ Overdue flagging (queue)
│   │
│   ├─ Step 4C: Status Staleness
│   │   └─ GetStatusUpdatesFromObject per project → stale/current/never
│   │
│   ├─ Step 4D: Project-Specific Automation
│   │   ├─ Recurring task detection (AU + MX) → queue creation proposals
│   │   ├─ Cross-team blocker detection (MX) → queue blocker updates
│   │   ├─ Event countdown (Paid App) → queue escalation proposals
│   │   └─ Budget/PO tracking (MX + Paid App) → queue critical flags
│   │
│   ├─ Step 4E: Market Context Auto-Refresh (AUTO-EXECUTE)
│   │   ├─ Compile AU/MX project summaries
│   │   ├─ Compare against Context_Task content
│   │   └─ If Material_Change → read-before-write → UpdateTask(html_notes)
│   │
│   └─ Write am-portfolio-findings.json
│
├─ Phase 5: COMPILE OUTPUT (~10s)
│   ├─ Verify all 4 output files exist:
│   │   1. am-enrichment-queue.json
│   │   2. am-portfolio-findings.json
│   │   3. am-abps-ai-state.json
│   │   4. am-signals-processed.json
│   ├─ Verify intake files exist:
│   │   5. slack-digest.md
│   │   6. email-triage.md
│   │   7. asana-digest.md
│   │   8. asana-activity.md
│   ├─ Refresh l1_streak for today (read current hard thing from amcc.md or current.md):
│   │   ```sql
│   │   INSERT INTO main.l1_streak (tracker_date, workdays_at_zero, hard_thing_task_gid, hard_thing_name)
│   │   VALUES (CURRENT_DATE, [days], '[gid]', '[name]')
│   │   ON CONFLICT (tracker_date) DO UPDATE SET
│   │       hard_thing_task_gid = EXCLUDED.hard_thing_task_gid,
│   │       hard_thing_name = EXCLUDED.hard_thing_name,
│   │       notes = EXCLUDED.notes;
│   │   ```
│   │   Source the hard thing from amcc.md or current.md pending actions (first unchecked item marked as hard thing).
│   │   workdays_at_zero: carry forward from previous day's value (query MAX(tracker_date) < CURRENT_DATE).
│   ├─ Update data freshness for all synced tables:
│   │   ```sql
│   │   INSERT INTO ops.data_freshness (source_name, source_type, expected_cadence_hours, last_updated, last_checked, is_stale, downstream_workflows)
│   │   VALUES ('asana_tasks', 'duckdb_table', 12, NOW(), NOW(), false, ARRAY['am_triage','portfolio_scan','daily_tracker'])
│   │   ON CONFLICT (source_name) DO UPDATE SET last_updated = NOW(), last_checked = NOW(), is_stale = false;
│   │   ```
│   │   Repeat for: calendar_events, emails, slack_messages, signal_tracker, l1_streak.
│   └─ Log hook execution to DuckDB
│
└─ DONE — AM-Frontend can now run

---

## Subagent Specifications

### Subagent A: Slack Ingestion

**Context files to load:**
- spine.md (tool access)
- slack-channel-registry.json (channel config)
- slack-scan-state.json (last scan timestamps)
- signal-intelligence.md (topic extraction protocol)

**MCP servers used:** Slack MCP, DuckDB MCP

**Writes:**
- ~/shared/context/intake/slack-digest.md (file)
- ~/shared/context/active/slack-scan-state.json (file)
- signals.slack_messages (DuckDB)
- signals.signal_tracker (DuckDB)
- signals.slack_threads (DuckDB)

**Does NOT touch:** Asana MCP, Outlook MCP, any asana-* files

---

### Subagent B1: Asana Sync + DuckDB

**Context files to load:**
- spine.md (tool access)
- asana-command-center.md (GIDs, sections, custom fields)
- asana-duckdb-sync.md (sync protocol)

**MCP servers used:** Asana MCP, DuckDB MCP

**Writes:**
- asana.asana_tasks (DuckDB — UPSERT)
- asana.asana_task_history (DuckDB — INSERT)
- ~/shared/context/intake/asana-digest.md (file)
- ~/shared/context/active/asana-morning-snapshot.json (file, legacy)

**Does NOT touch:** Slack MCP, Outlook MCP, any slack-* files, asana-activity.md, asana-scan-state.json

---

### Subagent B2: Asana Activity Monitor

**Context files to load:**
- spine.md (tool access)
- asana-command-center.md (GIDs for task lookup)
- asana-activity-monitor-protocol.md (activity detection rules)
- asana-scan-state.json (last scan timestamps — READ then WRITE)

**MCP servers used:** Asana MCP (read-only: GetTaskStories)

**Writes:**
- ~/shared/context/intake/asana-activity.md (file)
- ~/shared/context/active/asana-scan-state.json (file — update timestamps)

**Does NOT touch:** DuckDB (zero writes), Slack MCP, Outlook MCP, asana-digest.md, asana-morning-snapshot.json

---

### Subagent C: Email + Calendar Ingestion

**Context files to load:**
- spine.md (tool access)
- memory.md (stakeholder priority list for sender classification)
- email-calendar-duckdb-sync.md (DuckDB sync protocol — MANDATORY, contains SQL templates)

**MCP servers used:** Outlook MCP, DuckDB MCP

**Execution order (from email-calendar-duckdb-sync.md):**
1. Pull emails → **INSERT into signals.emails (DuckDB)** — primary deliverable
2. Pull calendar → **UPSERT into main.calendar_events (DuckDB)** — primary deliverable
3. Update ops.data_freshness
4. Write email-triage.md (file) — secondary output

**CRITICAL:** DuckDB writes are the PRIMARY output. The file (email-triage.md) is secondary fallback. Do NOT skip DuckDB writes. The sync protocol file has explicit SQL templates with column mappings — follow them exactly.

**Writes:**
- signals.emails (DuckDB — INSERT/UPSERT) ← MUST happen
- main.calendar_events (DuckDB — UPSERT) ← MUST happen
- ops.data_freshness (DuckDB — UPDATE)
- ~/shared/context/intake/email-triage.md (file)

**Does NOT touch:** Slack MCP, Asana MCP, any slack-* or asana-* files or tables

---

### Subagent D: Loop Page Sync

**Context files to load:**
- loop-page-sync.md (sync protocol)

**MCP servers used:** SharePoint MCP (sharepoint_read_loop), DuckDB MCP

**Writes:**
- docs.loop_pages (DuckDB — UPDATE content)
- ops.data_freshness (DuckDB — UPDATE loop_pages row)

**Does NOT touch:** Slack MCP, Asana MCP, Outlook MCP, any file outputs

---

## Shared Resource Isolation

The key to safe parallelism: no two subagents write to the same file or DuckDB table.

| Resource | Subagent A (Slack) | Subagent B1 (Asana Sync) | Subagent B2 (Activity) | Subagent C (Email+Cal) | Subagent D (Loop) |
|----------|-------------------|-------------------------|----------------------|----------------------|-------------------|
| slack-digest.md | WRITE | — | — | — | — |
| asana-digest.md | — | WRITE | — | — | — |
| email-triage.md | — | — | — | WRITE | — |
| asana-activity.md | — | — | WRITE | — | — |
| slack-scan-state.json | WRITE | — | — | — | — |
| asana-scan-state.json | — | — | WRITE | — | — |
| asana-morning-snapshot.json | — | WRITE | — | — | — |
| signals.slack_messages | WRITE | — | — | — | — |
| signals.signal_tracker | WRITE | — | — | — | — |
| signals.emails | — | — | — | WRITE | — |
| asana.asana_tasks | — | WRITE | — | — | — |
| asana.asana_task_history | — | WRITE | — | — | — |
| main.calendar_events | — | — | — | WRITE | — |
| docs.loop_pages | — | — | — | — | WRITE |

Zero overlap across all 4 subagents. Safe to run in parallel.

---

## Failure Handling

| Failure | Impact | Mitigation |
|---------|--------|-----------|
| Subagent A (Slack) fails | No slack-digest.md | Phase 2 signal-to-task skips Slack signals. Frontend shows "Slack scan failed" in brief. |
| Subagent B1 (Asana Sync) fails | No DuckDB sync, no asana-digest | Phase 3-4 cannot run (depend on synced data). Frontend falls back to live Asana queries. |
| Subagent B2 (Activity) fails | No asana-activity.md | Frontend skips activity signals section. Non-critical — no downstream dependencies. |
| Subagent C (Email+Cal) fails | No email-triage.md, no calendar/email in DuckDB | Phase 2 signal-to-task skips email signals. Frontend falls back to live Outlook MCP for calendar. |
| DuckDB unreachable | Subagents A+B1 partially fail | Slack digest still written to file. Asana digest still written to file. DuckDB-dependent processing skipped. |
| Slack MCP rate limit | Subagent A slows/partial | Partial digest written. Missing channels flagged. |
| Asana MCP rate limit | Subagents B1+B2 slow | B1 and B2 both hit Asana API — potential contention. B1 (bulk reads) takes priority; B2 (per-task stories) is lower priority and can be retried. |

**Rule:** If Subagent B1 (Asana Sync) fails, skip Phases 3-4 entirely. The frontend can still run from live Asana API calls.

---

## Timing Estimates

| Phase | Sequential (current) | Parallel (proposed) |
|-------|---------------------|-------------------|
| Phase 0: Schema check | 10s | 10s |
| Phase 1: Ingestion | ~12 min (4+5+3) | ~4 min (max of 4 parallel: Slack 4m, Asana Sync 3m, Activity 2m, Email 1m) |
| Phase 2: Processing | ~3 min | ~3 min |
| Phase 3: Enrichment | ~2 min | ~2 min |
| Phase 4: Portfolio | ~3 min | ~3 min |
| Phase 5: Compile | 10s | 10s |
| **Total** | **~20 min** | **~12 min** |

Savings: ~8 min per morning run. Bounded by Slack scan (~4 min).

---

## Hook Trigger Change

The am-auto.kiro.hook prompt changes from "Run am-backend.md" to "Run am-backend-parallel.md":

```
"prompt": "Run the autonomous morning backend.\n\nRead and execute ~/shared/context/protocols/am-backend-parallel.md.\n\n..."
```

The hook still uses `invokeSubAgent` — the difference is that Phase 1 fires 3 subagents simultaneously instead of running them in sequence within a single agent turn.

---

## Migration Path

1. Test parallel ingestion with 2 subagents first (Slack + Asana). Email is lowest risk — add it third.
2. Verify no DuckDB write conflicts by checking table isolation.
3. Run one morning with parallel backend + frontend. Compare output quality against sequential baseline.
4. If clean: update am-auto.kiro.hook to reference am-backend-parallel.md.
5. Keep am-backend.md as fallback (rename to am-backend-sequential.md).
