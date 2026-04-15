<!-- DOC-0420 | duck_id: protocol-context-enrichment -->
# Context Enrichment Protocol — Phase 2.5

Runs after Phase 2 (signal processing) and before Phase 3 (task enrichment). Takes the raw ingested data from Phase 1 and flows it into richer context stores that compound over time.

**Principle:** Ingestion captures what happened. Enrichment captures what it means. Signals are short-form (topic slug + strength). Enrichment is long-form (narrative, chronology, relationships, wiki candidates).

---

## Value Weighting Framework

Not all ingested data deserves the same treatment. The enrichment phase applies a value weight to decide what gets short-form treatment (DuckDB row) vs long-form treatment (file update + DuckDB).

| Value Tier | Weight | Short-Form (DuckDB only) | Long-Form (file + DuckDB) | Examples |
|------------|--------|--------------------------|---------------------------|----------|
| **Tier 1: Decisions & Commitments** | 5.0 | signal_tracker row | Meeting series file update, current.md update, project timeline | Brandon: "cancel Kate meeting", "treat underspend as process failure", Lena: "full Polaris switch" |
| **Tier 2: Action Items & Deadlines** | 4.0 | signal_tracker row | Meeting series Open Items, Asana task cross-ref, current.md pending actions | "Richard: obtain TPS checklist from Abdul", "Year-One Optimization one-pager by Apr 16" |
| **Tier 3: Strategic Context & Insights** | 3.0 | signal_tracker row | Wiki article enrichment, meeting Running Themes, project context tasks | OP1 brainstorm themes, Google Summit AI-MAX insights, Jasper AI content strategy |
| **Tier 4: Relationship Signals** | 2.0 | relationship_activity row | memory.md staleness update (if >14d shift) | Brandon DM, Lena email, Lorena Slack thread, Adi sync |
| **Tier 5: Status Updates & FYI** | 1.0 | signal_tracker row only | None (short-form sufficient) | OCI CA launch confirmed, 3P Event Guidelines, team photos |

**Rule:** Tier 1-2 always get long-form treatment. Tier 3 gets long-form if it touches an active project or wiki article. Tier 4 always updates relationship_activity. Tier 5 stays short-form only.

---

## Step 2.5A: Meeting Series File Updates (~2 min)

**Input:** hedy-digest.md, meeting_analytics, meeting_highlights, Hedy MCP (GetSessionDetails for new sessions)
**Output:** Updated ~/shared/wiki/meetings/*.md files, updated main.meeting_series

### Procedure

1. Query meeting_analytics for sessions since last enrichment run:
```sql
SELECT ma.session_id, ma.meeting_name, ma.meeting_date, ma.duration_minutes,
       ma.action_item_count, ma.topics_discussed,
       ms.series_id, ms.file_path, ms.last_session_date
FROM main.meeting_analytics ma
LEFT JOIN main.meeting_series ms ON ma.session_id IN (
    SELECT session_id FROM main.meeting_analytics 
    WHERE meeting_date > ms.last_session_date
)
WHERE ma.meeting_date > COALESCE(
    (SELECT MAX(last_session_date) FROM main.meeting_series), 
    CURRENT_DATE - INTERVAL '7 days'
)
ORDER BY ma.meeting_date;
```

2. For each new session not yet in its series file:
   a. Match session to series via Hedy topic_id → meeting_series.hedy_topic_id
   b. If no match: check meeting_name against series file names (fuzzy)
   c. If still no match: log as unmatched for manual routing

3. For each matched session, pull rich context:
   a. GetSessionDetails(sessionId) — get recap, meeting_minutes, cleaned_transcript
   b. GetSessionToDos(sessionId) — get action items
   c. GetSessionHighlights(sessionId) — get key moments
   d. Query meeting_highlights for decisions already extracted

4. Apply the Multi-Source Ingestion Protocol from meetings/README.md:
   a. Hedy is primary source
   b. Check email threads (±2 days) for pre/post meeting context
   c. Synthesize ONE clean summary per the README cleaning rules

5. Update the series file:
   a. Read current file content (read-before-write)
   b. Move current "Latest Session" to "Previous Session" (compress if >3 deep)
   c. Write new "Latest Session" with: date, duration, key discussion points, decisions, action items
   d. Update "Open Items" — close completed, add new
   e. Update "Running Themes" if patterns shift

6. Update DuckDB:
```sql
UPDATE main.meeting_series 
SET last_session_date = '{date}', 
    open_item_count = {count},
    running_themes = ARRAY[{themes}],
    updated_at = CURRENT_TIMESTAMP
WHERE series_id = '{series_id}';
```

### Scope Control
- Max 5 series file updates per run (prioritize by: manager > stakeholder > team > peer)
- Skip sessions older than 14 days (they should have been caught by EOD-1)
- If Hedy MCP is unavailable, use meeting_analytics + meeting_highlights from DuckDB (already ingested)

---

## Step 2.5B: Relationship Activity Tracking (~30s)

**Input:** signals.slack_messages, signals.emails, main.meeting_analytics, asana activity
**Output:** main.relationship_activity (DuckDB)

### Procedure

Compute weekly interaction counts per person from all ingested sources:

```sql
INSERT INTO main.relationship_activity (person_name, person_alias, week, 
    slack_interactions, email_exchanges, meetings_shared, asana_collaborations, 
    total_score, interaction_trend)
WITH slack_counts AS (
    SELECT author_name as person, COUNT(*) as cnt
    FROM signals.slack_messages 
    WHERE synced_at >= CURRENT_DATE - INTERVAL '7 days'
    AND author_name != 'Richard Williams'
    GROUP BY author_name
),
email_counts AS (
    SELECT sender_name as person, COUNT(*) as cnt
    FROM signals.emails
    WHERE synced_at >= CURRENT_DATE - INTERVAL '7 days'
    GROUP BY sender_name
),
meeting_counts AS (
    -- Use meeting_series attendees + meeting_analytics dates
    SELECT unnest(ms.attendees) as person, COUNT(*) as cnt
    FROM main.meeting_analytics ma
    JOIN main.meeting_series ms ON true  -- join via topic matching
    WHERE ma.meeting_date >= CURRENT_DATE - INTERVAL '7 days'
    GROUP BY person
)
SELECT 
    COALESCE(s.person, e.person, m.person) as person_name,
    NULL as person_alias,
    DATE_TRUNC('week', CURRENT_DATE)::DATE as week,
    COALESCE(s.cnt, 0) as slack_interactions,
    COALESCE(e.cnt, 0) as email_exchanges,
    COALESCE(m.cnt, 0) as meetings_shared,
    0 as asana_collaborations,
    COALESCE(s.cnt, 0) + COALESCE(e.cnt, 0) * 2 + COALESCE(m.cnt, 0) * 3 as total_score,
    'new' as interaction_trend
FROM slack_counts s
FULL OUTER JOIN email_counts e ON s.person = e.person
FULL OUTER JOIN meeting_counts m ON COALESCE(s.person, e.person) = m.person
ON CONFLICT DO NOTHING;
```

**Scoring weights:** Slack = 1x (high volume, low signal), Email = 2x (lower volume, higher intent), Meeting = 3x (highest signal — shared time).

---

## Step 2.5C: Wiki Candidate Detection (~15s)

**Input:** signals.signal_tracker (already populated by Phase 1 + 2)
**Output:** Logged to am-signals-processed.json for frontend surfacing

The `signals.wiki_candidates` view already exists and auto-computes from signal_tracker:
```sql
-- Topics with strength >= 3.0, channel_spread >= 2, mentions >= 3
SELECT * FROM signals.wiki_candidates;
```

### Procedure
1. **Slug normalization pass** (run BEFORE querying the view):
   - Query all active topics: `SELECT DISTINCT topic FROM signals.signal_tracker WHERE is_active`
   - Identify slug variants that refer to the same concept (e.g., "Brand LP Polaris Transition", "polaris-lp-testing", "polaris-lp-revert" → all should be "polaris-brand-lp")
   - UPDATE mismatched slugs to the canonical form (lowercase-hyphenated, project-scoped)
   - Canonical slug rules: `{project-or-topic}-{subtopic}` — e.g., `polaris-brand-lp`, `mx-budget-ieccp`, `au-cpa-cvr`, `oci-rollout`, `liveramp-enhanced-match`
   - This is critical because Slack ingestion uses display names ("Brand LP Polaris Transition") while Hedy uses slugs ("polaris-lp-testing"). Without normalization, the same topic fragments across rows and never reaches the quality threshold.
2. Query the view: `SELECT * FROM signals.wiki_candidates`
3. Cross-reference against wiki.publication_registry — exclude topics that already have articles
4. Cross-reference against ABPS AI Content project tasks — exclude topics already in pipeline
5. Remaining = genuine wiki gaps. Append to am-signals-processed.json under `wiki_candidates` key
6. If any candidate has quality_score >= 10.0: flag as "strong candidate" for frontend

---

## Step 2.5D: Five Levels Tagging (~30s)

**Input:** signals.signal_tracker, main.meeting_analytics, asana.asana_tasks
**Output:** main.five_levels_weekly (DuckDB)

### Level Classification Rules

| Signal/Topic Pattern | Level | Rationale |
|---------------------|-------|-----------|
| Testing, test design, weblab, A/B, experiment | L2 | Drive WW Testing |
| AU, MX, market-specific, CPA, CPC, keyword, bid, campaign | L2 | Market execution |
| Kate doc, Testing Approach, framework, methodology | L1 | Sharpen Yourself (artifact) |
| Tool, automation, script, dashboard, Kiro workflow | L3 | Team Automation |
| AEO, AI Overviews, zero-click, AI search, GenAI search | L4 | Zero-Click Future |
| Agent, MCP, orchestration, autonomous, Kiro power | L5 | Agentic Orchestration |
| OCI, Polaris, LP, landing page, brand page | L2 | Testing/execution |
| Budget, PO, invoice, admin, compliance | L1 | Sharpen Yourself (admin) |
| OP1, strategy, vision, roadmap | L1-L2 | Strategic planning |

### Procedure

```sql
INSERT INTO main.five_levels_weekly (week_start, level, level_name, 
    tasks_completed, tasks_active, hours_estimated, artifacts_shipped, streak_weeks, notes)
SELECT 
    DATE_TRUNC('week', CURRENT_DATE)::DATE,
    level_num,
    level_name,
    completed_count,
    active_count,
    NULL, -- hours_estimated (not tracked yet)
    0, -- artifacts_shipped (updated by EOD)
    0, -- streak_weeks (computed separately)
    topic_list
FROM (
    -- Count tasks per level from asana
    SELECT 1 as level_num, 'Sharpen Yourself' as level_name,
        SUM(CASE WHEN completed THEN 1 ELSE 0 END) as completed_count,
        SUM(CASE WHEN NOT completed THEN 1 ELSE 0 END) as active_count,
        STRING_AGG(DISTINCT name, ', ' ORDER BY name) FILTER (WHERE NOT completed) as topic_list
    FROM asana.asana_tasks 
    WHERE deleted_at IS NULL 
    AND (name ILIKE '%testing approach%' OR name ILIKE '%framework%' OR name ILIKE '%admin%' OR routine_rw LIKE '%Admin%')
    -- ... similar for L2-L5
)
ON CONFLICT DO NOTHING;
```

This is approximate — the real value comes from accumulating weekly snapshots over time to show where Richard's time actually goes.

---

## Step 2.5E: Project Timeline Events (~30s)

**Input:** All Phase 1 sources (Slack, Email, Hedy, Asana)
**Output:** DuckDB table (needs creation: main.project_timeline)

### Schema (create if not exists)
```sql
CREATE TABLE IF NOT EXISTS main.project_timeline (
    event_id VARCHAR PRIMARY KEY,
    project_name VARCHAR NOT NULL,
    event_date DATE NOT NULL,
    event_type VARCHAR NOT NULL, -- decision, milestone, blocker, status_change, escalation, launch
    summary VARCHAR NOT NULL,
    source_channel VARCHAR, -- slack, email, hedy, asana
    source_id VARCHAR,
    people_involved VARCHAR[],
    level_tag INTEGER, -- 1-5
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Procedure
Extract Tier 1-2 events from today's ingestion:
- Decisions from meeting_highlights (type='decision')
- Milestones from Asana (completed tasks in Milestones sections)
- Blockers from Slack (threads with "blocked", "waiting on", "can't proceed")
- Status changes from email (subject contains "update", "status", "progress")
- Launches from Slack (OCI CA launch today, weblab dial-ups)
- Escalations from email/Slack (Brandon/Kate involvement on a topic)

Each event gets a project_name tag (AU, MX, WW Testing, Polaris, OCI, etc.) and a level_tag.

**This builds the chronological narrative arc per project that's currently scattered across intake files.**

---

## Step 2.5F: Current.md Refresh (~30s)

**Input:** All Phase 1-2 outputs
**Output:** Updated ~/shared/context/active/current.md

### Procedure
1. Read current.md (read-before-write)
2. Update "Active Projects" section with any status changes detected:
   - New Slack decisions → update project status
   - Completed Asana tasks → mark as done
   - New blockers → add to project notes
3. Update "Pending Actions" section:
   - Check completed items against Asana (completed=true) → mark [x]
   - Add new action items from hedy-digest (Tier 2 items)
   - Add new action items from email-triage (action_needed='respond')
   - Update overdue counts
4. Update "Key People" last interaction dates from relationship_activity
5. Do NOT rewrite the entire file — surgical updates only (read-before-write pattern)

### Scope Control
- Only update sections where data has changed
- Max 10 pending action updates per run
- Skip if current.md was updated within the last 4 hours (avoid thrashing)

---

## Execution Summary

| Step | Time | DuckDB Writes | File Writes | Value |
|------|------|---------------|-------------|-------|
| 2.5A: Meeting Series | ~2 min | meeting_series UPDATE | meetings/*.md | Long-form meeting context that compounds |
| 2.5B: Relationship Activity | ~30s | relationship_activity INSERT | None | Auto-computed staleness, replaces manual memory.md tracking |
| 2.5C: Wiki Candidates | ~15s | None (view query) | am-signals-processed.json append | Surfaces organic wiki article ideas from cross-channel signals |
| 2.5D: Five Levels | ~30s | five_levels_weekly INSERT | None | Weekly heatmap of where time goes vs where it should go |
| 2.5E: Project Timeline | ~30s | project_timeline INSERT | None | Chronological narrative arc per project |
| 2.5F: Current.md Refresh | ~30s | None | current.md | Keeps live state file fresh instead of frozen |
| **Total** | **~4 min** | **4 tables** | **≤6 files** | |

---

## Dependencies

- Requires Phase 1 complete (all ingestion data available)
- Requires Phase 2A-2D complete (signal routing done, so we know which signals are new vs reinforced)
- Phase 3+ can proceed after 2.5 completes (no circular dependencies)

## Error Handling

- If Hedy MCP unavailable for 2.5A: use DuckDB meeting_analytics + meeting_highlights (already ingested). Series files get a lighter update.
- If a meeting series file doesn't exist for a session: log as "unmatched session" in am-signals-processed.json. Don't create new series files automatically — queue for Richard.
- If current.md update fails: log error, continue. Current.md is important but not blocking.
- If project_timeline table doesn't exist: CREATE it (schema above). First run bootstraps.

## Portability Note

All outputs are either DuckDB tables (portable via MotherDuck) or plain markdown files (portable by definition). No hooks, MCP, or subagent access required to read the outputs. A new AI on a different platform can pick up any series file or query any DuckDB table and understand the context cold.
