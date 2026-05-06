<!-- DOC-0329 | duck_id: protocol-am-backend-parallel -->



# AM-Backend Protocol — Parallel Architecture (v2, current)

**Current: v2 parallel with Asana-in-orchestrator constraint.** Hook: am-auto.kiro.hook v5.0.0.

**Evolution (Apr 2026):**
- v1 (pre-4/16): 5 subagents all parallel including Asana → Asana MCP failed from subagent context (ESD proxy token exchange unreliable from `invokeSubAgent`).
- v3 (morning 4/16): Reverted to sequential orchestrator-only. Reliable but slow (~15 min) and gave up parallelism where it worked (Slack, Email, Loop, Hedy all fine from subagents).
- **v2 (afternoon 4/16, current):** Reinstated parallel but moved Asana (B1 + B2) into the orchestrator. 4 subagents (Slack, Email, Loop, Hedy) run in parallel; Asana runs concurrently in the orchestrator. B2 runs after B1 (sequential within orchestrator) to avoid Asana API rate-limit contention.

**Rules (hard constraints):**
1. Asana MCP calls NEVER go to subagents. This is the failure that killed v1. Stays in orchestrator.
2. Slack / Email / Loop / Hedy MCP calls go to subagents. They work reliably from `invokeSubAgent`.
3. B2 (Activity Monitor) runs AFTER B1 (Sync) completes — both in orchestrator.
4. Subagents A, C, D, E have no shared-resource conflicts (see isolation table below).

---




## Phase 0: Pre-flight Checks (~10s)

Run before all other phases. Three quick checks that catch systemic issues early.

### 0.1 Schema Check

Verify DuckDB schemas expected by downstream phases exist: `ps.*`, `signals.*`, `main.*`, `asana.*`, `docs.*`, `ops.*`, `wiki.*`. If any target schema is missing, flag in the daily-brief header but continue (don't block).

### 0.2 Market Constraints Staleness (added 2026-05-06)

Run silently: `SELECT market, updated_at, DATE_DIFF('day', updated_at, CURRENT_TIMESTAMP) AS days_stale FROM ps.market_constraints_manual WHERE updated_at < CURRENT_TIMESTAMP - INTERVAL '60 days' ORDER BY updated_at`. If any rows return, include in the morning brief header: `⚠️ Market constraints stale: [market1 Nd], [market2 Nd]... — UPDATE on ps.market_constraints_manual before relying on governing_constraint / handoff_status / OCI fields`. If no rows, skip silently.

Moved here from per-turn promptSubmit hook on 2026-05-06 — per-turn check was ~120 tokens for a table that rarely changes. Daily cadence is sufficient. Ad-hoc check still available via `market-constraints-staleness-alert.kiro.hook` (userTriggered).

### 0.3 MCP Auth Smoke Test (if available)

Quick curl against a known-good auth endpoint to detect Midway cookie expiry before Phase 1 subagents fail mid-run. Non-blocking — flag in brief header if dead but continue.

---


## Timing Estimates

| Phase | Sequential (old) | Parallel v1 (broken) | Parallel v2 (current) |
|-------|-----------------|---------------------|----------------------|
| Phase 0: Schema check | 10s | 10s | 10s |
| Phase 1: Ingestion | ~12 min | ~5 min (but Asana failed) | ~5 min (max of: Slack 5m, Orch B1+B2 5m, Email 1m, Loop 1m, Hedy 1m) |
| Phase 2: Processing | ~3 min | ~3 min | ~3 min |
| Phase 2.5: Context Enrichment | — | ~4 min | ~4 min |
| Phase 3: Enrichment | ~2 min | ~2 min | ~2 min |
| Phase 4: Portfolio | ~3 min | ~3 min | ~3 min |
| Phase 5: Compile | 10s | 10s | 10s |
| **Total** | **~20 min** | **~16 min (with gaps)** | **~16 min (no gaps)** |

Key change: wall-clock time is the same (~16 min) but Asana data is now guaranteed fresh because it runs in the orchestrator where MCP access is reliable. The orchestrator runs B1+B2 concurrently with the 4 subagents, so no time is lost.

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




[38;5;10m> [0m### ORCHESTRATOR-OWNED: Asana Sync (B1) + Activity Monitor (B2)[0m[0m
[0m[0m
#### Execution Model[0m[0m
These run in the parent orchestrator agent — **not** as subagents.[0m[0m
[0m[0m
#### Why Not Subagents[0m[0m
Asana MCP (enterprise-asana-mcp) uses an ESD proxy that is unreliable from subagent contexts. This is a hard constraint learned from production (2026-04-16).
#### ORCHESTRATOR-OWNED: Asana Sync (B1) + Activity Monitor (B2) — Details





#### Step B1: Asana Sync + DuckDB (orchestrator, ~3 min)

**Context files to load:**
- asana-command-center.md (GIDs, sections, custom fields)
- asana-duckdb-sync.md (sync protocol)

**MCP tools used (orchestrator-direct):** SearchTasksInWorkspace, GetTaskDetails,
GetTasksFromProject, GetPortfolioItems — all via Asana MCP. execute_query via DuckDB MCP.

**Execution:**
1. SearchTasksInWorkspace(assignee_any="1212732742544167", completed=false, sort_by=due_date)
2. GetTaskDetails for each task (batch — opt_fields include custom_fields, projects, memberships)
3. GetTasksFromProject for 6 projects: My Tasks, WW Testing, WW Acquisition, Paid App, ABIX — plus any other portfolio projects discovered via GetPortfolioItems (ABPS portfolio GID `1212762061512816`)
4. Merge by task_gid, map custom fields, UPSERT into asana.asana_tasks
5. Soft-delete missing tasks
6. Daily snapshot to asana.asana_task_history
7. Coherence check (6 checks)
8. Schema drift detection

**Wiki articles are NOT tracked in Asana.** Article pipeline state lives in
~/shared/wiki/agent-created/ (source), SharePoint Documents/Artifacts/ (published),
and the Kiro dashboard Pipeline view. Do not add article-tracking projects to this sync.

**Writes:**
- asana.asana_tasks (DuckDB — UPSERT)
- asana.asana_task_history (DuckDB — INSERT)
- ~/shared/context/intake/asana-digest.md (file)
- ~/shared/context/active/asana-morning-snapshot.json (file, legacy)
- Also writes task list to ~/shared/context/active/asana-task-list-b1.json (handoff to B2)

**Does NOT touch:** Slack MCP, Outlook MCP, any slack-* files




#### Step B2: Asana Activity Monitor (orchestrator, ~2 min, AFTER B1)

**Context files to load:**
- asana-activity-monitor-protocol.md (activity detection rules)
- asana-scan-state.json (last scan timestamps — READ then WRITE)
- asana-task-list-b1.json (task list from B1 — avoids re-pulling from Asana)

**MCP tools used (orchestrator-direct):** GetTaskStories via Asana MCP.

**Rate Limit Mitigation:**
- Read task list from B1 output file (no SearchTasksInWorkspace call)
- Sort tasks by priority before scanning:
  1. Tasks with Brandon/Kate as collaborator or recent commenter (highest signal)
  2. Tasks due within 3 days
  3. Tasks with recent section moves
  4. Everything else (lowest priority)
- On 429 rate limit: wait 60s, retry once, then skip remaining tasks
- Log which tasks were scanned vs skipped for next-run prioritization

**Writes:**
- ~/shared/context/intake/asana-activity.md (file)
- ~/shared/context/active/asana-scan-state.json (file — update timestamps)

**Does NOT touch:** DuckDB (zero writes), Slack MCP, Outlook MCP, asana-digest.md

---




## Failure Handling

| Failure | Impact | Mitigation |
|---------|--------|-----------|
| Subagent A (Slack) fails | No slack-digest.md | Phase 2 signal-to-task skips Slack signals. Frontend shows "Slack scan failed" in brief. |
| Orchestrator B1 (Asana Sync) fails | No DuckDB sync, no asana-digest | Phase 3-4 cannot run (depend on synced data). Frontend falls back to live Asana queries. |
| Orchestrator B2 (Activity) fails | No asana-activity.md | Frontend skips activity signals section. Non-critical — no downstream dependencies. |
| Subagent C (Email+Cal) fails | No email-triage.md, no calendar/email in DuckDB | Phase 2 signal-to-task skips email signals. Frontend falls back to live Outlook MCP for calendar. |
| Subagent D (Loop) fails | No Loop page refresh | Stale content persists. Non-critical — no downstream dependencies. |
| Subagent E (Hedy) fails | No topic-log entries from today's meetings; signal_tracker misses meeting reinforcement | Phase 2 signal-to-task skips meeting signals. Topic docs simply lack today's meeting entries (recoverable next run). Frontend skips meeting recap section. Non-critical. |
| DuckDB unreachable | Subagent A + orchestrator B1 partially fail | Slack digest still written to file. Asana digest still written to file. DuckDB-dependent processing skipped. |
| Slack MCP rate limit | Subagent A slows/partial | Partial digest written. Missing channels flagged. |
| Asana MCP rate limit | Orchestrator B1+B2 slow | B2 runs AFTER B1 (sequential), reducing contention. B2 prioritizes high-value tasks. Rate-limited tasks logged for next run. |

**Rule:** If orchestrator B1 (Asana Sync) fails, skip Phases 3-4 entirely. The frontend can still run from live Asana API calls.
**Rule:** Asana MCP calls NEVER go to subagents. This is a hard constraint.

---




### MCP Reliability Constraint (2026-04-16 — learned from production)

**Asana MCP (enterprise-asana-mcp) is UNRELIABLE from subagents.** The ESD proxy
token exchange intermittently fails when called from `invokeSubAgent` contexts.
Slack, Outlook, DuckDB, and SharePoint MCP servers work reliably from subagents.

**Rule:** ALL Asana MCP calls MUST run in the orchestrator (parent agent), never in
subagents. This is a hard constraint, not a preference. Subagents that need Asana
data should receive it via file handoff from the orchestrator.




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




## Architecture




## Migration Path

1. ✅ v1 tested (2026-04-16): 5 subagents parallel. Asana MCP failed from subagent. Identified root cause.
2. ✅ v2 protocol written (2026-04-16): Asana moved to orchestrator. B2 sequential after B1. Hedy added.
3. NEXT: Run one morning with v2 architecture. Verify Asana data is fresh (not 24h stale).
4. If clean: update am-auto.kiro.hook to reference v2 prompt pattern.
5. Keep v1 failure documented in this file as a constraint (MCP Reliability section above).

### Subagent E: Hedy Meeting Sync → Topic Log Router

**Context files to load:**
- spine.md (tool access)
- memory.md (relationship graph for attendee context)
- signal-intelligence.md (topic extraction for cross-channel reinforcement)
- ~/shared/wiki/topics/INGEST-PROTOCOL.md (topic log ingest contract — source-of-truth)
- ~/shared/wiki/topics/_registry.md (registered topic slugs + aliases + hedy_topic_id → doc path mapping)

**MCP servers used:** Hedy MCP, DuckDB MCP

**Execution order:**
1. Pull recent meeting recaps/transcripts since last AM scan (Hedy MCP: GetSessions, GetSessionDetails, GetSessionToDos, GetSessionHighlights)
2. For each meeting:
   a. Extract what was said (direct quotes preferred), decisions as stated, actions as committed with owners + due dates, attendees
   b. Identify target topic docs using INGEST-PROTOCOL topic identification order (hedy_topic_id match from `_registry.md` → slug/alias match → related-slug match)
   c. For each target topic doc: prepend an H3 Log entry per the append contract (with `#### Source` citing `hedy:<session_id>`, `#### What was said / what happened`, `#### Decisions`, `#### Actions`, optional `#### Notes`)
   d. Prepend a daily line to `## Simplified Timeline` under the current ISO-week H4 header
   e. Move resolved items from Open Items to Closed Items — Audit Trail (append-only, never delete)
   f. Update `updated:` frontmatter to today (PT)
3. Reinforce `signals.signal_tracker` with extracted topics (+1.0 weight, source_channel='hedy') — the tracker remains the cross-channel topic index
4. Append unregistered candidates (≥3 distinct mentions or strategic one-offs) to `~/shared/wiki/topics/_discovery-queue.md`
5. If any topic doc accumulated ≥3 new entries since its last Summary refresh, emit a signal to the Summary-refresh debt file `~/shared/context/active/topic-log-summary-debt.json` (wiki-maintenance Stage 1 consumes it)

**Writes:**
- ~/shared/wiki/topics/<type>/<slug>.md (file — PREPEND Log entries, update Simplified Timeline, Open/Closed Items, `updated:`)
- ~/shared/wiki/topics/_discovery-queue.md (file — APPEND unregistered candidates)
- ~/shared/context/active/topic-log-summary-debt.json (file — UPDATE debt counters)
- signals.signal_tracker (DuckDB — UPDATE reinforcement only, source_channel='hedy')

**Does NOT write:**
- `signals.hedy_meetings` — DEPRECATED 2026-05-06. Do NOT insert.
- `main.meeting_analytics` / `main.meeting_highlights` / `main.meeting_series` — DEPRECATED 2026-05-06. Do NOT insert.
- `~/shared/context/intake/hedy-digest.md` — DEPRECATED 2026-05-06. Do NOT write.

**Does NOT touch:** Slack MCP, Asana MCP, Outlook MCP, SharePoint MCP, any slack-*/asana-*/email-* files

**Hedy as source:** Hedy MCP remains the transcript source of truth. Topic log entries cite the specific `hedy:<session_id>` so future readers can retrieve the full transcript on demand. We do NOT duplicate transcripts into topic logs — we synthesize exactly what was said with attribution.

---




## Shared Resource Isolation

The key to safe parallelism: no two concurrent writers touch the same file or DuckDB table.
B1 and B2 are sequential (orchestrator), so they don't conflict with each other.
Subagents A, C, D, E are parallel and isolated from each other AND from the orchestrator's Asana work.

| Resource | Subagent A (Slack) | Orchestrator B1 (Asana Sync) | Orchestrator B2 (Activity) | Subagent C (Email+Cal) | Subagent D (Loop) | Subagent E (Hedy) |
|----------|-------------------|-------------------------|----------------------|----------------------|-------------------|-------------------|
| slack-digest.md | WRITE | — | — | — | — | — |
| asana-digest.md | — | WRITE | — | — | — | — |
| email-triage.md | — | — | — | WRITE | — | — |
| asana-activity.md | — | — | WRITE | — | — | — |
| hedy-digest.md | — | — | — | — | — | WRITE |
| slack-scan-state.json | WRITE | — | — | — | — | — |
| asana-scan-state.json | — | — | WRITE | — | — | — |
| asana-morning-snapshot.json | — | WRITE | — | — | — | — |
| asana-task-list-b1.json | — | WRITE | READ | — | — | — |
| signals.slack_messages | WRITE (incl. thread replies) | — | — | — | — | — |
| signals.signal_tracker | WRITE | — | — | — | — | WRITE* |
| signals.emails | — | — | — | WRITE | — | — |
| signals.hedy_meetings | — | — | — | — | — | DEPRECATED 2026-05-06 — NO WRITES |
| wiki/topics/**/*.md | — | — | — | — | — | WRITE (PREPEND Log entries) |
| wiki/topics/_discovery-queue.md | — | — | — | — | — | WRITE (APPEND candidates) |
| context/active/topic-log-summary-debt.json | — | — | — | — | — | WRITE (UPDATE debt) |
| asana.asana_tasks | — | WRITE | — | — | — | — |
| asana.asana_task_history | — | WRITE | — | — | — | — |
| main.calendar_events | — | — | — | WRITE | — | — |
| docs.loop_pages | — | — | — | — | WRITE | — |

*signal_tracker: Both A and E write to this table but with different source_channel values ('slack' vs 'hedy'). No row-level conflicts — safe for parallel execution.

---




## Subagent Specifications




### Activity Monitor Rate Limiting Mitigation

**Problem:** Subagent B2 (Activity Monitor) calls `GetTaskStories` per task, hitting
Asana API rate limits (~28/100 tasks skipped per run). Running B2 concurrently with

**Fix:** B2 runs AFTER B1 completes (sequential, not parallel). B1 does bulk reads
reads (GetTaskStories) which are expensive. Running them sequentially avoids
re-pulling from Asana, saving one SearchTasksInWorkspace call.

the most important tasks were already scanned.

```
AM-Backend Hook (orchestrator)
├─ Phase 0: Schema Verification (orchestrator, ~10s)
│   └─ All DuckDB access via MCP `execute_query`. No direct Python duckdb.connect().
├─ Phase 1: MIXED INGESTION (~5 min wall-clock)
│   │
│   │  ┌─────────────────────────────────────────────────────────┐
│   │  │ PARALLEL BLOCK (fire simultaneously via invokeSubAgent) │
│   │  │                                                         │
│   │  │  Subagent C: Email + Calendar Ingestion (~1 min)        │
│   │  │  Subagent E: Hedy Meeting Sync (~1 min)                 │
│   │  └─────────────────────────────────────────────────────────┘
│   │
│   │  │  Step B1: Asana Sync + DuckDB (~3 min)                  │
│   │  │    ├─ SearchTasksInWorkspace (Richard, incomplete)      │
│   │  │    │    Paid App) — wiki articles are NOT tracked here  │
│   │  │    ├─ UPSERT into asana.asana_tasks                    │
│   │  │    ├─ Soft-delete stale tasks                           │
│   │  │    ├─ Coherence check + schema drift detection          │
│   │  │    ├─ Write asana-digest.md                             │
│   │  │    └─ Write asana-morning-snapshot.json (legacy)        │
│   │  │  Step B2: Asana Activity Monitor (~2 min, AFTER B1)     │
│   │  │    ├─ Read task list from B1 output (no re-pull)        │
│   │  │    ├─ GetTaskStories per task (batched, with backoff)   │
│   │  │    ├─ Classify: comment_added, due_date_changed,        │
│   │  │    │   reassigned                                       │
│   │  │    ├─ Write asana-activity.md                           │
│   │  └─────────────────────────────────────────────────────────┘
│   │  The orchestrator block and subagent block run concurrently.
│   │  B1 and B2 are sequential within the orchestrator block.
│   ├─ Subagent A: Slack Ingestion (~5 min, longest)
│   │   ├─ list_channels (unreadOnly=true)
│   │   ├─ Apply depth rules + relevance filter
│   │   ├─ THREAD REPLY FETCH: For messages with reply_count > 0 in today's ingestion,
│   │   ├─ Produce slack-digest.md
│   │   ├─ Proactive search (prichwil, brandoxy, kataxt)
│   │   ├─ Update slack-scan-state.json
│   │
│       ├─ email_search (all folders, date-bounded)
│       ├─ Classify by sender priority (Brandon/Kate/Todd = HIGH)
│       ├─ INSERT into signals.emails (DuckDB) ← PRIMARY
│       └─ Produce email-triage.md (secondary)
│
│   ├─ Subagent D: Loop Page Sync (~1 min)
│   │   ├─ UPDATE docs.loop_pages with content_markdown, content_preview, word_count
│   │   └─ Update ops.data_freshness for loop_pages source
│   │   Protocol: ~/shared/context/protocols/loop-page-sync.md
│   └─ Subagent E: Hedy Meeting Sync → Topic Log Router (~1-2 min)
│       ├─ Pull recent meeting transcripts/recaps since last scan (GetSessions, GetSessionDetails)
│       ├─ For each session: route to target topic docs via _registry.md
│       │    ├─ PREPEND H3 Log entry (with source cite, what-was-said, decisions, actions)
│       │    ├─ PREPEND daily line to Simplified Timeline under ISO-week H4 header
│       │    ├─ Move resolved items to Closed Items — Audit Trail
│       │    └─ Update frontmatter `updated:` to today (PT)
│       ├─ Feed extracted topics into signal_tracker (source_channel='hedy')
│       ├─ Append unregistered candidates to topics/_discovery-queue.md
│       └─ Update topic-log-summary-debt.json for ≥3-entry docs
│       Protocol: ~/shared/wiki/topics/INGEST-PROTOCOL.md
├─ BARRIER: Wait for all subagents AND orchestrator Asana block to complete
│   └─ If any subagent fails: log failure, continue with available data, flag in output
├─ Phase 2: SEQUENTIAL PROCESSING (orchestrator or single subagent, ~3 min)
│   │
│   │   ├─ Log to signal_task_log in DuckDB
│   │   └─ Log pipeline execution to workflow_executions
│   │
│   ├─ Step 2A.1: Hard-Thing Candidate Refresh
│   │   ├─ Run: `python3 ~/shared/tools/scripts/hard-thing-refresh.py`
│   │   ├─ Computes top-3 candidates with exponential decay + incumbent margin
│   │   ├─ Writes snapshot to main.hard_thing_candidates
│   │   ├─ Script ensures main.hard_thing_* tables exist (idempotent CREATE TABLE IF NOT EXISTS)
│   │   ├─ Non-fatal if motherduck_token missing — writes null-state snapshot, continues
│   │   ├─ Throttled to 15-min minimum between runs (exit 1 if throttled, non-fatal)
│   │   └─ Protocol: ~/shared/context/protocols/hard-thing-selection.md
│   ├─ Step 2B: Slack Conversation Enrichment
│   │   └─ Store knowledge_context in DuckDB (skip if KDS unreachable)
│   ├─ Step 2C: Bucket Cap Check + Flags
│   │   ├─ Query asana.asana_tasks for bucket counts
│   │   ├─ Over cap → queue demotion proposals
│   │   ├─ Today + no Routine → queue for triage
│   │   └─ Overdue 7+ days → queue kill-or-revive
│   │
│   ├─ Step 2D: Slack Decision Detection
│   │   └─ Scan slack-digest for decision keywords → queue for frontend
│   │
│   │   ├─ Run: `python3 ~/shared/tools/state-files/sync_metrics.py --execute`
│   │   ├─ Aggregates daily_metrics into weekly summaries for missing weeks
│   │   ├─ Updates ops.data_freshness
│   │
│   └─ Step 2E: State File Generation
│       ├─ Read ~/shared/context/protocols/state-file-engine.md (generic engine)
│       ├─ For each registered state file where status = ACTIVE:
│       │   ├─ Load market-specific protocol (e.g., state-file-mx-ps.md)
│       │   ├─ Query DuckDB via MCP for latest weekly data per market
│       │   ├─ Read slack-digest.md + email-triage.md for market-relevant signals
│       │   ├─ Generate JSON payload per placeholder schema
│       ├─ Validate: `python3 ~/shared/tools/state-files/validate_state_files.py`
│       └─ Log generation to DuckDB workflow_executions
│
│   │   Protocol: ~/shared/context/protocols/context-enrichment.md
│   │
│   ├─ Step 2.5A: Topic Log Meeting Series Sync (optional complement to Subagent E)
│   │   ├─ Subagent E has already prepended Hedy-sourced Log entries to test/market/initiative/project topic docs
│   │   ├─ This step additionally updates legacy ~/shared/wiki/meetings/*.md files for recurring-meeting series that have their own doc (brandon-sync, mx-paid-search-sync, weekly-paid-acq, etc.)
│   │   ├─ For each session whose `meeting_name` maps to a file in ~/shared/wiki/meetings/:
│   │   │    ├─ Pull rich context: GetSessionDetails + GetSessionToDos + GetSessionHighlights (Hedy MCP)
│   │   │    ├─ Prepend a "Latest Session" entry to the meeting series file
│   │   │    └─ Update Open Items + Running Themes per existing meeting-series conventions
│   │   └─ Meetings/ files remain as recurring-meeting logs; topics/ files are the cross-channel synthesis
│   ├─ Step 2.5B: Relationship Activity Tracking
│   │   └─ Weights: Slack 1x, Email 2x, Meeting 3x
│   │   ├─ Query signals.wiki_candidates view (strength >= 3.0, spread >= 2, mentions >= 3)
│   │   ├─ Exclude topics with existing wiki articles or ABPS AI pipeline tasks
│   │
│   ├─ Step 2.5D: Five Levels Tagging
│   │   ├─ Classify signals + tasks by Level (L1-L5) using topic pattern matching
│   │   └─ INSERT into main.five_levels_weekly (weekly heatmap of time allocation)
│   │
│   ├─ Step 2.5E: Topic Log Discovery Reconciliation
│   │   ├─ Read ~/shared/wiki/topics/_registry.md (registered slugs + aliases)
│   │   ├─ Query signals.signal_tracker for candidates: slugs with ≥3 mentions in last 60d not in registry
│   │   ├─ Append any new candidates to ~/shared/wiki/topics/_discovery-queue.md (dedup against existing queue)
│   │   ├─ Read ~/shared/context/active/topic-log-summary-debt.json — for any topic doc with debt ≥3, refresh Summary + Running Themes from last 5 Log entries (cite entry dates)
│   │   └─ Reset debt counter after refresh
│   │   Protocol: ~/shared/wiki/topics/INGEST-PROTOCOL.md
│   │
│   │   ├─ Extract Tier 1-2 events (decisions, milestones, blockers, launches, escalations)
│   │   ├─ Tag with project_name + level
│   │
│       ├─ Update Pending Actions (mark completed, add new from Hedy/email)
│
├─ Phase 3: ENRICHMENT SCAN (orchestrator or single subagent, ~2 min)
│   │   ├─ Query asana.asana_tasks (already synced in Phase 1B)
│   │   ├─ Apply 4 enrichment rules (Kiro_RW, Next Action, dates, Priority_RW)
│   │
│       ├─ Detect stale FINAL articles (updated >30 days)
│       ├─ Pull new-article candidates from signals.wiki_candidates
│       └─ Write ~/shared/context/active/am-wiki-state.json
│
│   ├─ Step 4A: Portfolio Discovery
│   │   ├─ GetPortfolioItems for ABIX PS + ABPS
│   │   └─ New project detection → queue flag
│   │
│   ├─ Step 4B: Per-Project Task Scan + Enrichment
│   │   └─ Overdue flagging (queue)
│   │   └─ GetStatusUpdatesFromObject per project → stale/current/never
│   │   ├─ Recurring task detection (AU + MX) → auto-create next instances
│   │   ├─ Cross-team blocker detection (MX) → queue blocker updates
│   │   ├─ Event countdown (Paid App) → queue escalation proposals
│   │   └─ Budget/PO tracking (MX + Paid App) → queue critical flags
│   │   ├─ Compare against Context_Task content
│   │
│   └─ Write ~/shared/context/active/am-portfolio-findings.json
│
│   │   1. ~/shared/context/active/am-enrichment-queue.json
│   │   3. ~/shared/context/active/am-wiki-state.json
│   │   4. ~/shared/context/active/am-signals-processed.json
│   ├─ Verify intake files exist:
│   │   7. asana-digest.md
│   ├─ Verify state files generated (Step 2E output):
│   │   11. ~/shared/wiki/state-files/*-state.docx (one per active market)
│   ├─ Refresh l1_streak for today (read current hard thing from amcc.md or current.md):
│   │   ```sql
│   │   ON CONFLICT (tracker_date) DO UPDATE SET
│   │       hard_thing_task_gid = EXCLUDED.hard_thing_task_gid,
│   │   Source the hard thing from amcc.md or current.md pending actions (first unchecked item marked as hard thing).
│   │   workdays_at_zero: carry forward from previous day's value (query MAX(tracker_date) < CURRENT_DATE).
│   ├─ Update data freshness for all synced tables:
│   │   Run: `python3 ~/shared/tools/state-files/refresh_data_freshness.py --sources asana_tasks,calendar_events,emails,slack_messages,signal_tracker,l1_streak,topic_logs`
│   └─ Log hook execution to DuckDB
│   ├─ Execute ~/shared/context/protocols/sharepoint-durability-sync.md — AM section
│   ├─ Push: ~/shared/context/active/am-enrichment-queue.json → Kiro-Drive/system-state/
│   ├─ Push: ~/shared/context/active/am-portfolio-findings.json → Kiro-Drive/system-state/
│   ├─ Push: ~/shared/context/active/am-wiki-state.json → Kiro-Drive/system-state/
│   ├─ Push: daily-brief-latest.md → Kiro-Drive/system-state/
│   ├─ Push: state files (.md + .docx per active market) → Kiro-Drive/state-files/
│   ├─ Non-blocking: if SharePoint fails, log warning and continue
└─ DONE — AM-Frontend can now run

---




## Hook Trigger Change

The am-auto.kiro.hook prompt must instruct the orchestrator to:
1. Fire 4 subagents (A, C, D, E) in parallel via invokeSubAgent
2. Run B1 (Asana Sync) directly in the orchestrator using Asana MCP tools
3. After B1 completes, run B2 (Activity Monitor) directly in the orchestrator
4. Wait for all 4 subagents to complete (barrier)
5. Proceed to Phase 2+

The hook prompt should include:
```
"prompt": "Run the autonomous morning backend using the PARALLEL architecture.\n\nRead and execute ~/shared/context/protocols/am-backend-parallel.md.\n\nCRITICAL: Asana MCP calls (B1 + B2) run in the ORCHESTRATOR, not subagents.\nFire 4 subagents (Slack, Email, Loop, Hedy) in parallel.\nRun Asana Sync (B1) directly, then Activity Monitor (B2) directly.\nWait for all to complete before Phase 2.\n\n..."
```

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




## Why Parallel (v2)

Phase 1 (Data Collection) has independent data streams with no cross-dependencies:
- Slack scan (Subagent A) → Slack MCP, signals.slack_messages, slack-digest.md
- Asana sync (Orchestrator B1) → Asana MCP, asana.asana_tasks, asana-digest.md
- Asana activity (Orchestrator B2, after B1) → Asana MCP, asana-activity.md
- Email + calendar (Subagent C) → Outlook MCP, signals.emails, main.calendar_events, email-triage.md
- Loop page sync (Subagent D) → SharePoint MCP, docs.loop_pages
- Hedy meetings (Subagent E) → Hedy MCP, `~/shared/wiki/topics/**/*.md` (Log entries), `~/shared/wiki/topics/_discovery-queue.md`, signals.signal_tracker (reinforcement only)

Wall-clock: max(Slack ~5min, Orchestrator B1+B2 ~5min, Email ~1min, Loop ~1min, Hedy ~1min) ≈ 5 min.

Phase 2+ (Processing) depends on Phase 1 outputs — runs sequentially after the ingestion barrier.

---





**Common failure:** Misinterpreting the scope of this section — it covers only Why Parallel (v2), not adjacent concerns.