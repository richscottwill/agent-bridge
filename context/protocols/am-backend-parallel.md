<!-- DOC-0329 | duck_id: protocol-am-backend-parallel -->
# AM-Backend Protocol — Parallel Architecture

Replaces the sequential am-backend.md with a parallel-first design. Ingestion fans out to 6 concurrent subagents. Processing runs sequentially after all ingestion completes.

---

## Why Parallel

Phase 1 (Data Collection) has independent data streams:
- Slack scan → reads Slack MCP, writes slack-digest.md + DuckDB
- Asana sync → reads Asana MCP, writes DuckDB + asana-digest.md
- Email scan → reads Outlook MCP, writes email-triage.md
- Hedy scan → reads Hedy MCP, writes hedy-digest.md + DuckDB signals

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
│   └─ If ps_analytics not attached: execute `ATTACH 'md:ps_analytics'` then `USE ps_analytics`
│
├─ Phase 1: PARALLEL INGESTION (6 subagents, ~4 min wall-clock)
│   │
│   ├─ Subagent A: Slack Ingestion (~5 min, longest)
│   │   ├─ list_channels (unreadOnly=true)
│   │   ├─ Apply depth rules + relevance filter
│   │   ├─ batch_get_conversation_history for each channel
│   │   ├─ DuckDB batch writes (signals.slack_messages)
│   │   ├─ THREAD REPLY FETCH: For messages with reply_count > 0 in today's ingestion,
│   │   │   call batch_get_thread_replies (batch up to 10 threads per call).
│   │   │   Insert all thread replies into signals.slack_messages with thread_ts set.
│   │   │   This ensures Richard's thread-level responses are captured for
│   │   │   signals.slack_unanswered accuracy. Priority: threads from Brandon/Kate/Lena first.
│   │   ├─ Produce slack-digest.md
│   │   ├─ RSW-channel intake
│   │   ├─ Proactive search (prichwil, brandoxy, kataxt)
│   │   ├─ Update slack-scan-state.json
│   │   ├─ DuckDB batch writes (signals.signal_tracker)
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
│   ├─ Subagent D: Loop Page Sync (~1 min)
│   │   ├─ Query docs.loop_pages for stale pages (>12h since last_ingested)
│   │   ├─ For each stale page: sharepoint_read_loop(loopUrl)
│   │   ├─ UPDATE docs.loop_pages with content_markdown, content_preview, word_count
│   │   └─ Update ops.data_freshness for loop_pages source
│   │   Protocol: ~/shared/context/protocols/loop-page-sync.md
│   │
│   └─ Subagent E: Hedy Meeting Sync (~1 min)
│       ├─ Pull recent meeting transcripts/recaps since last scan
│       ├─ Extract action items, decisions, topics from meetings
│       ├─ Classify by meeting series (stakeholder, team, manager, peer)
│       ├─ Produce hedy-digest.md
│       ├─ INSERT into signals.hedy_meetings (DuckDB)
│       └─ Feed extracted topics into signal_tracker for cross-channel reinforcement
│
├─ BARRIER: Wait for all subagents to complete
│   └─ If any subagent fails: log failure, continue with available data, flag in output
│
├─ Phase 2: SEQUENTIAL PROCESSING (orchestrator or single subagent, ~3 min)
│   │
│   ├─ Step 2A: Signal-to-Task Pipeline
│   │   ├─ Read slack-digest.md + email-triage.md + hedy-digest.md
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
│   ├─ Step 2D: Slack Decision Detection
│   │   └─ Scan slack-digest for decision keywords → queue for frontend
│   │
│   ├─ Step 2D.5: PS Metrics Sync (DuckDB → MotherDuck)
│   │   ├─ Run: `python3 ~/shared/tools/state-files/sync_metrics.py --execute`
│   │   ├─ Aggregates daily_metrics into weekly summaries for missing weeks
│   │   ├─ Writes to ps.metrics (EAV) and ps.weekly_actuals (wide)
│   │   ├─ Updates ops.data_freshness
│   │   ├─ Idempotent — skips if no new weeks detected
│   │   └─ Log: check stdout for sync count
│   │
│   └─ Step 2E: State File Generation
│       ├─ Read ~/shared/context/protocols/state-file-engine.md (generic engine)
│       ├─ For each registered state file where status = ACTIVE:
│       │   ├─ Load market-specific protocol (e.g., state-file-mx-ps.md)
│       │   ├─ Query MotherDuck ps.metrics for latest weekly data per market
│       │   ├─ Read slack-digest.md + email-triage.md for market-relevant signals
│       │   ├─ Read current state file .md (preserve static sections)
│       │   ├─ Generate JSON payload per placeholder schema
│       │   ├─ Patch local .md with new dynamic content
│       │   └─ Skip markets with no new data since last generation
│       ├─ Validate: `python3 ~/shared/tools/state-files/validate_state_files.py`
│       ├─ Convert: `python3 ~/shared/tools/state-files/convert_state_files.py`
│       └─ Log generation to DuckDB workflow_executions
│
├─ Phase 2.5: CONTEXT ENRICHMENT (orchestrator, ~4 min)
│   │   Protocol: ~/shared/context/protocols/context-enrichment.md
│   │
│   ├─ Step 2.5A: Meeting Series File Updates
│   │   ├─ Query meeting_analytics for sessions since last enrichment
│   │   ├─ Match sessions to series via Hedy topic_id → meeting_series
│   │   ├─ Pull rich context: GetSessionDetails + GetSessionToDos + GetSessionHighlights
│   │   ├─ Apply Multi-Source Ingestion Protocol (Hedy primary, email secondary)
│   │   ├─ Update ~/shared/wiki/meetings/*.md (Latest Session, Open Items, Running Themes)
│   │   ├─ UPDATE main.meeting_series (last_session_date, open_item_count)
│   │   └─ Max 5 series updates per run (manager > stakeholder > team > peer)
│   │
│   ├─ Step 2.5B: Relationship Activity Tracking
│   │   ├─ Compute weekly interaction counts per person from Slack + Email + Meetings
│   │   ├─ INSERT into main.relationship_activity
│   │   └─ Weights: Slack 1x, Email 2x, Meeting 3x
│   │
│   ├─ Step 2.5C: Wiki Candidate Detection
│   │   ├─ Query signals.wiki_candidates view (strength >= 3.0, spread >= 2, mentions >= 3)
│   │   ├─ Exclude topics with existing wiki articles or ABPS AI pipeline tasks
│   │   └─ Append candidates to ~/shared/context/active/am-signals-processed.json
│   │
│   ├─ Step 2.5D: Five Levels Tagging
│   │   ├─ Classify signals + tasks by Level (L1-L5) using topic pattern matching
│   │   └─ INSERT into main.five_levels_weekly (weekly heatmap of time allocation)
│   │
│   ├─ Step 2.5E: Project Timeline Events
│   │   ├─ Extract Tier 1-2 events (decisions, milestones, blockers, launches, escalations)
│   │   ├─ Tag with project_name + level
│   │   └─ INSERT into main.project_timeline (chronological narrative per project)
│   │
│   └─ Step 2.5F: Current.md Refresh
│       ├─ Update Active Projects with status changes from today's signals
│       ├─ Update Pending Actions (mark completed, add new from Hedy/email)
│       ├─ Update Key People last interaction dates
│       └─ Surgical updates only — read-before-write, max 10 action updates
│
├─ Phase 3: ENRICHMENT SCAN (orchestrator or single subagent, ~2 min)
│   │
│   ├─ Step 3A: My Tasks Enrichment
│   │   ├─ Query asana.asana_tasks (already synced in Phase 1B)
│   │   ├─ Apply 4 enrichment rules (Kiro_RW, Next Action, dates, Priority_RW)
│   │   └─ Queue proposals to ~/shared/context/active/am-enrichment-queue.json § my_tasks
│   │
│   └─ Step 3B: ABPS AI Content Scan
│       ├─ Intake triage detection (untriaged tasks in Intake section)
│       ├─ Pipeline state detection (In Progress, Review, Active)
│       ├─ Near-due escalation (AUTO-EXECUTE: 0-2 days → Today)
│       ├─ Overdue flagging (queue for frontend)
│       ├─ Refresh cadence check (Active + recurring frequency)
│       └─ Write ~/shared/context/active/am-abps-ai-state.json
│
├─ Phase 4: PORTFOLIO SCAN (orchestrator or single subagent, ~3 min)
│   │
│   ├─ Step 4A: Portfolio Discovery
│   │   ├─ GetPortfolioItems for ABIX PS + ABPS
│   │   └─ New project detection → queue flag
│   │
│   ├─ Step 4B: Per-Project Task Scan + Enrichment
│   │   ├─ For each project: scan tasks, filter to Richard
│   │   ├─ Apply 4 enrichment rules → queue to ~/shared/context/active/am-enrichment-queue.json § portfolio
│   │   ├─ Near-due escalation (AUTO-EXECUTE)
│   │   └─ Overdue flagging (queue)
│   │
│   ├─ Step 4C: Status Staleness
│   │   └─ GetStatusUpdatesFromObject per project → stale/current/never
│   │
│   ├─ Step 4D: Project-Specific Automation
│   │   ├─ Recurring task detection (AU + MX) → auto-create next instances
│   │   ├─ Cross-team blocker detection (MX) → queue blocker updates
│   │   ├─ Event countdown (Paid App) → queue escalation proposals
│   │   └─ Budget/PO tracking (MX + Paid App) → queue critical flags
│   │
│   ├─ Step 4E: Market Context Auto-Refresh (AUTO-EXECUTE)
│   │   ├─ Compile AU/MX project summaries
│   │   ├─ Compare against Context_Task content
│   │   └─ If Material_Change → read-before-write → UpdateTask(html_notes)
│   │
│   └─ Write ~/shared/context/active/am-portfolio-findings.json
│
├─ Phase 5: COMPILE OUTPUT (~10s)
│   ├─ Verify all 4 output files exist (MUST be in ~/shared/context/active/):
│   │   1. ~/shared/context/active/am-enrichment-queue.json
│   │   2. ~/shared/context/active/am-portfolio-findings.json
│   │   3. ~/shared/context/active/am-abps-ai-state.json
│   │   4. ~/shared/context/active/am-signals-processed.json
│   ├─ Verify intake files exist:
│   │   5. slack-digest.md
│   │   6. email-triage.md
│   │   7. asana-digest.md
│   │   8. asana-activity.md
│   │   9. hedy-digest.md
│   ├─ Verify state files generated (Step 2E output):
│   │   10. ~/shared/wiki/state-files/*-state.md (one per active market)
│   │   11. ~/shared/wiki/state-files/*-state.docx (one per active market)
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
│   │   Run: `python3 ~/shared/tools/state-files/refresh_data_freshness.py --sources asana_tasks,calendar_events,emails,slack_messages,signal_tracker,l1_streak,hedy_meetings`
│   └─ Log hook execution to DuckDB
│
├─ Phase 5.5: SHAREPOINT DURABILITY SYNC (~15s)
│   ├─ Execute ~/shared/context/protocols/sharepoint-durability-sync.md — AM section
│   ├─ Push: ~/shared/context/active/am-enrichment-queue.json → Kiro-Drive/system-state/
│   ├─ Push: ~/shared/context/active/am-portfolio-findings.json → Kiro-Drive/system-state/
│   ├─ Push: ~/shared/context/active/am-abps-ai-state.json → Kiro-Drive/system-state/
│   ├─ Push: ~/shared/context/active/am-signals-processed.json → Kiro-Drive/system-state/
│   ├─ Push: daily-brief-latest.md → Kiro-Drive/system-state/
│   ├─ Push: state files (.md + .docx per active market) → Kiro-Drive/state-files/
│   ├─ Non-blocking: if SharePoint fails, log warning and continue
│   └─ Log sync result to DuckDB workflow_executions
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

**Thread Reply Fetch Protocol (MANDATORY):**
After ingesting channel history, fetch thread replies to capture Richard's thread-level responses:

1. Query just-ingested messages for thread parents:
   ```sql
   SELECT DISTINCT ts, channel_id, channel_name, reply_count
   FROM signals.slack_messages
   WHERE reply_count > 0
     AND ingested_at >= CURRENT_TIMESTAMP - INTERVAL '1 hour'
   ORDER BY reply_count DESC
   ```
2. For each thread parent (batch up to 10 per call):
   ```
   batch_get_thread_replies(threads=[{channelId, threadTs}])
   ```
3. For each reply in the response, INSERT into signals.slack_messages:
   - `ts` = reply timestamp
   - `thread_ts` = parent message ts (the threadTs from the call)
   - `is_thread_reply` = TRUE
   - `is_richard` = TRUE if reply author is U040ECP305S
   - `richard_mentioned` = TRUE if reply text contains U040ECP305S
   - All other fields extracted normally (author, text, reactions, etc.)
4. Priority order: fetch threads from Brandon/Kate/Lena channels first (avoidance detection accuracy).
5. Cap: max 50 threads per run to stay within time budget (~1 min for thread fetch).
6. Skip threads already fully ingested (check: if slack_messages has rows with matching thread_ts AND is_thread_reply = TRUE AND count matches reply_count, skip).

This ensures signals.slack_unanswered.richard_replied is accurate — it can detect thread-level responses, not just channel-level.

**Writes:**
- ~/shared/context/intake/slack-digest.md (file)
- ~/shared/context/active/slack-scan-state.json (file)
- signals.slack_messages (DuckDB — includes thread replies)
- signals.signal_tracker (DuckDB)

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
1. Query ops.data_freshness for last scan date (DuckDB)
2. Pull emails across all folders since last scan date → **INSERT into signals.emails (DuckDB)** — primary deliverable
3. Pull calendar → **UPSERT into main.calendar_events (DuckDB)** — primary deliverable
4. Update ops.data_freshness
5. Write email-triage.md (file) — secondary output

**CRITICAL:** DuckDB writes are the PRIMARY output. The file (email-triage.md) is secondary fallback. Do NOT skip DuckDB writes. The sync protocol file has explicit SQL templates with column mappings — follow them exactly. Email scan covers ALL folders (inbox, sent, custom, subfolders) using `email_search` with a date window from the last successful scan. See email-calendar-duckdb-sync.md Step 1 for details.

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

**Does NOT touch:** Slack MCP, Asana MCP, Outlook MCP, Hedy MCP, any file outputs

---

### Subagent E: Hedy Meeting Sync

**Context files to load:**
- spine.md (tool access)
- memory.md (relationship graph for attendee context)
- signal-intelligence.md (topic extraction for cross-channel reinforcement)

**MCP servers used:** Hedy MCP, DuckDB MCP

**Execution order:**
1. Pull recent meeting recaps/transcripts since last AM scan (use Hedy MCP tools: list sessions, get recaps, get action items)
2. For each meeting: extract action items, decisions, topics, attendees
3. Classify by meeting series (stakeholder/team/manager/peer) using attendee names
4. INSERT meeting data into signals.hedy_meetings (DuckDB)
5. Extract topics → reinforce in signals.signal_tracker (DuckDB) with +1.0 weight (meeting mentions are high-signal)
6. Write hedy-digest.md (file)

**Writes:**
- signals.hedy_meetings (DuckDB — INSERT)
- signals.signal_tracker (DuckDB — UPDATE reinforcement only, shared with Subagent A but different source_channel values prevent conflicts)
- ops.data_freshness (DuckDB — UPDATE hedy_meetings row)
- ~/shared/context/intake/hedy-digest.md (file)

**Does NOT touch:** Slack MCP, Asana MCP, Outlook MCP, SharePoint MCP, any slack-*/asana-*/email-* files

---

## Shared Resource Isolation

The key to safe parallelism: no two subagents write to the same file or DuckDB table.

| Resource | Subagent A (Slack) | Subagent B1 (Asana Sync) | Subagent B2 (Activity) | Subagent C (Email+Cal) | Subagent D (Loop) | Subagent E (Hedy) |
|----------|-------------------|-------------------------|----------------------|----------------------|-------------------|-------------------|
| slack-digest.md | WRITE | — | — | — | — | — |
| asana-digest.md | — | WRITE | — | — | — | — |
| email-triage.md | — | — | — | WRITE | — | — |
| asana-activity.md | — | — | WRITE | — | — | — |
| hedy-digest.md | — | — | — | — | — | WRITE |
| slack-scan-state.json | WRITE | — | — | — | — | — |
| asana-scan-state.json | — | — | WRITE | — | — | — |
| asana-morning-snapshot.json | — | WRITE | — | — | — | — |
| signals.slack_messages | WRITE (incl. thread replies) | — | — | — | — | — |
| signals.signal_tracker | WRITE | — | — | — | — | WRITE* |
| signals.emails | — | — | — | WRITE | — | — |
| signals.hedy_meetings | — | — | — | — | — | WRITE |
| asana.asana_tasks | — | WRITE | — | — | — | — |
| asana.asana_task_history | — | WRITE | — | — | — | — |
| main.calendar_events | — | — | — | WRITE | — | — |
| docs.loop_pages | — | — | — | — | WRITE | — |

*signal_tracker: Both A and E write to this table but with different source_channel values ('slack' vs 'hedy'). No row-level conflicts — safe for parallel execution.

---

## Failure Handling

| Failure | Impact | Mitigation |
|---------|--------|-----------|
| Subagent A (Slack) fails | No slack-digest.md | Phase 2 signal-to-task skips Slack signals. Frontend shows "Slack scan failed" in brief. |
| Subagent B1 (Asana Sync) fails | No DuckDB sync, no asana-digest | Phase 3-4 cannot run (depend on synced data). Frontend falls back to live Asana queries. |
| Subagent B2 (Activity) fails | No asana-activity.md | Frontend skips activity signals section. Non-critical — no downstream dependencies. |
| Subagent C (Email+Cal) fails | No email-triage.md, no calendar/email in DuckDB | Phase 2 signal-to-task skips email signals. Frontend falls back to live Outlook MCP for calendar. |
| Subagent D (Loop) fails | No Loop page refresh | Stale content persists. Non-critical — no downstream dependencies. |
| Subagent E (Hedy) fails | No hedy-digest.md, no meeting signals | Phase 2 signal-to-task skips Hedy signals. Frontend skips meeting recap section. Non-critical. |
| DuckDB unreachable | Subagents A+B1 partially fail | Slack digest still written to file. Asana digest still written to file. DuckDB-dependent processing skipped. |
| Slack MCP rate limit | Subagent A slows/partial | Partial digest written. Missing channels flagged. |
| Asana MCP rate limit | Subagents B1+B2 slow | B1 and B2 both hit Asana API — potential contention. B1 (bulk reads) takes priority; B2 (per-task stories) is lower priority and can be retried. |

**Rule:** If Subagent B1 (Asana Sync) fails, skip Phases 3-4 entirely. The frontend can still run from live Asana API calls.

---

## Timing Estimates

| Phase | Sequential (current) | Parallel (proposed) |
|-------|---------------------|-------------------|
| Phase 0: Schema check | 10s | 10s |
| Phase 1: Ingestion | ~12 min (4+5+3) | ~5 min (max of 6 parallel: Slack 5m incl threads, Asana Sync 3m, Activity 2m, Email 1m, Loop 1m, Hedy 1m) |
| Phase 2: Processing | ~3 min | ~3 min |
| Phase 2.5: Context Enrichment | — | ~4 min (meeting series 2m, relationship 30s, wiki candidates 15s, five levels 30s, timeline 30s, current.md 30s) |
| Phase 3: Enrichment | ~2 min | ~2 min |
| Phase 4: Portfolio | ~3 min | ~3 min |
| Phase 5: Compile | 10s | 10s |
| **Total** | **~20 min** | **~16 min** |

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
