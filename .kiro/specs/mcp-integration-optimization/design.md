# Design Document: MCP Integration Optimization

## Overview

This spec wires Richard's 12 MCP servers into cross-server workflows that eliminate manual steps in existing pipelines and create new capabilities. The design focuses on practical plumbing — how specific MCP tools chain together, what data flows between them, and where the results land in DuckDB or the Body system.

The 12 requirements group into 4 implementation phases:

1. **Phase A — Core Pipeline Wiring** (Req 1, 4, 7, 11): Meeting-to-task, signal-to-task, meeting analytics, workflow observability. These extend existing AM/EOD hooks with cross-MCP steps.
2. **Phase B — WBR & Quip Integration** (Req 2, 9): Quip publishing via Builder MCP, WBR pipeline consolidation. Eliminates the manual copy-paste step.
3. **Phase C — Knowledge Enrichment** (Req 3, 8, 10, 12): KDS/ARCC enrichment, XWiki publishing, Slack conversation intelligence. Activates underutilized MCPs.
4. **Phase D — AgentCore Services** (Req 5, 6): Browser automation, sandboxed code interpreter. Blocked on internal AWS account.

Related specs (avoid overlap):
- `mcp-capability-expansion/` — higher-level capability categories, DuckDB schema extensions, unified signal inbox, monitoring systems
- `agentcore-system-integration/` — AgentCore service-level integration details
- `asana-portfolio-management/` — Asana task lifecycle and portfolio scanning

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Hook Integration                          │
│  AM-1 ──→ AM-2 ──→ AM-3          EOD-1 ──→ EOD-2               │
│  (ingest)  (triage)  (brief)      (meetings) (maintenance)      │
└──────┬────────┬────────┬────────────┬──────────┬────────────────┘
       │        │        │            │          │
┌──────▼────────▼────────▼────────────▼──────────▼────────────────┐
│                    Cross-MCP Workflows                           │
│                                                                  │
│  Signal→Task    Meeting→Task    WBR→Quip    Wiki→XWiki          │
│  (Slack+Email   (Hedy+Asana    (SP+DuckDB   (KDS+ARCC           │
│   +Asana+DB)     +Slack+DB)     +Builder     +XWiki+SP)         │
│                                  +Slack)                         │
└──────┬────────────────┬─────────────┬──────────┬────────────────┘
       │                │             │          │
┌──────▼────────────────▼─────────────▼──────────▼────────────────┐
│                     DuckDB Analytics                             │
│  signal_task_log │ meeting_analytics │ workflow_executions       │
│  enrichment_log  │ quip_registry     │ publication_registry      │
│  meeting_highlights (FTS)            │ slack_messages (FTS)      │
└─────────────────────────────────────────────────────────────────┘
```

## Components and Interfaces

### Component 1: Meeting-to-Action-Item Pipeline (Req 1)

Extends EOD-1 to extract Hedy action items and create Asana tasks with Slack notification.

**MCP Chain:** Hedy → Asana → Slack

**Pipeline Sequence:**

```
EOD-1 Hook (existing)
│
├─ Step 1: GetSessions(date=today) via Hedy MCP
│   └─ For each session: GetSessionDetails(session_id)
│       └─ Extract: highlights, todos, action_items
│
├─ Step 2: Action Item Classification
│   ├─ Richard's items → Asana task creation path
│   ├─ Others' items → hands.md dependency logging
│   └─ No items → log "no actions" in meeting series file
│
├─ Step 3: Deduplication Check (for Richard's items)
│   └─ SearchTasksInWorkspace(query=action_description, assignee=Richard)
│       ├─ Match found → AddComment(task_gid, "Reinforced in [meeting] on [date]")
│       └─ No match → proceed to creation
│
├─ Step 4: Asana Task Creation
│   └─ CreateTask(
│       name: "[Meeting Name]: [action summary]",
│       notes: "From [meeting] on [date].\n\n[full action item text]",
│       due_on: [derived from discussion or +3 business days default],
│       projects: [appropriate project based on topic],
│       custom_fields: { Priority_RW: "Urgent", Routine: [mapped bucket] }
│   )
│
├─ Step 5: Slack Notification
│   └─ self_dm(login="prichwil", text="📋 [Meeting Name] — [N] tasks created:\n• [task1] (due [date])\n• [task2] (due [date])")
│
└─ Step 6: Dependency Logging (for others' items)
    └─ Append to hands.md:
       "- **[Person]**: [action item] (from [meeting], [date])"
```

**Due Date Derivation Logic:**

| Signal in Discussion | Due Date |
|---------------------|----------|
| Explicit date mentioned ("by Friday", "next week") | Parse to calendar date |
| Urgency signal ("ASAP", "today", "urgent") | Tomorrow |
| No date signal | +3 business days from meeting date |

**Deduplication Matching:**

Search Asana with the action item's key noun phrases (extracted from the action text). A match requires:
- Same assignee (Richard)
- Task name or description contains 2+ matching key phrases
- Task is in the same project or has no project

If match confidence is low (only 1 phrase match), create the task but add a note: "Possible duplicate of [existing_task_gid] — verify."

**EOD-1 Hook Prompt Addition:**

```
=== MEETING-TO-TASK AUTOMATION ===
After processing each Hedy session:
1. Extract all action items (todos, highlights marked as action)
2. For each item assigned to Richard:
   a. Search Asana for duplicates: SearchTasksInWorkspace(query="[key phrases]", assignee="1212732742544167")
   b. If duplicate: AddComment on existing task
   c. If new: CreateTask with meeting context, derived due date
3. For items assigned to others: append to hands.md dependencies
4. After all sessions: self_dm summary of tasks created
5. Log session to meeting series file with action count
```

### Component 2: Signal-to-Task Pipeline (Req 4)

Extends AM-1/AM-2 to auto-create Asana tasks from high-priority email and Slack signals.

**MCP Chain:** Outlook + Slack → Asana → DuckDB → Slack

**High-Priority Signal Detection:**

| Source | High-Priority Criteria |
|--------|----------------------|
| Email (Outlook) | From: Brandon, Kate, Todd, or skip-level. Subject contains: "action", "request", "need", "deadline", "urgent" |
| Slack (DM) | Any DM to Richard requiring a response or action |
| Slack (mention) | @Richard in a channel with action language |
| Slack (thread) | Reply to Richard's message with a question or request |

**Bucket Assignment Logic:**

| Signal Content | Asana Bucket |
|---------------|-------------|
| Strategic request (testing, methodology, framework) | Core |
| Operational request (budget, invoice, campaign change) | Sweep |
| System/tool request (automation, data, reporting) | Engine Room |
| Administrative (scheduling, access, approvals) | Admin |

**Signal-to-Task Mapping in DuckDB:**

```sql
CREATE TABLE IF NOT EXISTS signal_task_log (
    signal_source VARCHAR NOT NULL,     -- 'email', 'slack_dm', 'slack_mention', 'slack_thread'
    signal_id VARCHAR NOT NULL,         -- email_id or message_ts
    task_gid VARCHAR,                   -- created or updated Asana task
    action_taken VARCHAR NOT NULL,      -- 'task_created', 'task_updated', 'deferred', 'dismissed'
    priority VARCHAR,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (signal_source, signal_id)
);
```

**AM-1 Hook Prompt Addition:**

```
=== SIGNAL-TO-TASK PIPELINE ===
During email scan:
  For each email from [Brandon, Kate, Todd, or skip-level]:
    If email contains action request:
      1. SearchTasksInWorkspace(query="[subject keywords]", assignee=Richard) — dedup check
      2. If no match: CreateTask(name="[sender]: [subject excerpt]", notes="Email from [sender] on [date].\n\n[key excerpt]", due_on=[suggested], projects=[bucket])
      3. Log to signal_task_log via DuckDB

During Slack scan:
  For each DM or @mention requiring action:
    1. SearchTasksInWorkspace — dedup check (same author + similar topic within 7 days)
    2. If match: AddComment(task_gid, "New signal from [channel] on [date]: [excerpt]")
    3. If no match: CreateTask with Slack link, channel, author, action required
    4. Log to signal_task_log
```

**AM-2 Triage Summary (Slack DM):**

```
📬 AM-2 Triage Complete
• New tasks: [N] (from [sources])
• Updated tasks: [N] (new signals on existing)
• Deferred: [N] (low priority, backlog)
• Dismissed: [N] (FYI only)
```

### Component 3: Meeting Data Analytics (Req 7)

Stores Hedy meeting data in DuckDB for Loop 9 communication pattern analysis.

**MCP Chain:** Hedy → DuckDB → Slack (alerts)

**DuckDB Schema:**

```sql
CREATE TABLE IF NOT EXISTS meeting_analytics (
    session_id VARCHAR PRIMARY KEY,
    meeting_name VARCHAR NOT NULL,
    meeting_date DATE NOT NULL,
    duration_minutes INTEGER,
    participant_count INTEGER,
    action_item_count INTEGER,
    richard_speaking_share DOUBLE,
    hedging_count INTEGER DEFAULT 0,
    meeting_type VARCHAR,               -- '1on1', 'group', 'standup', 'review'
    topics_discussed VARCHAR[],
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS meeting_highlights (
    highlight_id VARCHAR PRIMARY KEY,
    session_id VARCHAR NOT NULL REFERENCES meeting_analytics(session_id),
    highlight_type VARCHAR NOT NULL,    -- 'quote', 'decision', 'action', 'insight'
    content TEXT NOT NULL,
    speaker VARCHAR,
    timestamp_offset INTEGER,           -- seconds into meeting
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**FTS Index on Highlights:**

```sql
-- Enable full-text search on meeting highlights
INSTALL fts;
LOAD fts;
PRAGMA create_fts_index('meeting_highlights', 'highlight_id', 'content', 'speaker');
```

**Meeting Type Classification:**

| Participant Count | Recurring? | Type |
|------------------|-----------|------|
| 2 | Yes | 1on1 |
| 2 | No | adhoc_1on1 |
| 3-6 | Yes | group |
| 3-6 | No | review |
| 7+ | Any | standup |

**Weekly Trend Computation (EOD-2, weekly):**

```sql
-- Communication trends for Loop 9
SELECT
    meeting_type,
    DATE_TRUNC('week', meeting_date) AS week,
    ROUND(AVG(richard_speaking_share), 2) AS avg_speaking_share,
    ROUND(AVG(hedging_count), 1) AS avg_hedging,
    ROUND(AVG(action_item_count), 1) AS avg_actions,
    COUNT(*) AS meeting_count
FROM meeting_analytics
WHERE meeting_date >= CURRENT_DATE - INTERVAL '28 days'
GROUP BY meeting_type, DATE_TRUNC('week', meeting_date)
ORDER BY week DESC, meeting_type;
```

**Coaching Signal Detection:**

```sql
-- Flag group meetings with speaking share < 15% for 3+ consecutive weeks
WITH weekly_group AS (
    SELECT
        DATE_TRUNC('week', meeting_date) AS week,
        AVG(richard_speaking_share) AS avg_share
    FROM meeting_analytics
    WHERE meeting_type IN ('group', 'review', 'standup')
    AND meeting_date >= CURRENT_DATE - INTERVAL '28 days'
    GROUP BY DATE_TRUNC('week', meeting_date)
),
consecutive AS (
    SELECT week, avg_share,
        ROW_NUMBER() OVER (ORDER BY week) -
        ROW_NUMBER() OVER (PARTITION BY (avg_share < 0.15) ORDER BY week) AS grp
    FROM weekly_group
)
SELECT COUNT(*) AS consecutive_low_weeks
FROM consecutive
WHERE avg_share < 0.15
GROUP BY grp
HAVING COUNT(*) >= 3;
```

If this query returns results → include in EOD-2 Slack DM:
```
⚠️ Group meeting speaking share below 15% for [N] consecutive weeks. Loop 9 coaching signal active.
```

### Component 4: Workflow Observability (Req 11)

Cross-cutting concern — every cross-MCP workflow logs execution data to DuckDB.

**MCP Chain:** Any workflow → DuckDB → Slack (on failure/degradation)

**DuckDB Schema:**

```sql
CREATE TABLE IF NOT EXISTS workflow_executions (
    execution_id VARCHAR PRIMARY KEY,
    workflow_name VARCHAR NOT NULL,
    trigger_source VARCHAR,
    mcp_servers_involved VARCHAR[],
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP,
    status VARCHAR DEFAULT 'running',    -- 'running', 'completed', 'partial', 'failed'
    steps_completed INTEGER DEFAULT 0,
    steps_failed INTEGER DEFAULT 0,
    duration_seconds DOUBLE,
    error_details JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE VIEW workflow_reliability AS
SELECT
    workflow_name,
    COUNT(*) AS total_runs,
    COUNT(*) FILTER (WHERE status = 'completed') AS successes,
    ROUND(COUNT(*) FILTER (WHERE status = 'completed') * 100.0 / NULLIF(COUNT(*), 0), 1) AS success_rate,
    ROUND(AVG(duration_seconds), 1) AS avg_duration_s,
    MAX(start_time) AS last_run
FROM workflow_executions
WHERE start_time > CURRENT_TIMESTAMP - INTERVAL '7 days'
GROUP BY workflow_name;
```

**Workflow Registration:**

Each cross-MCP workflow gets a standard name:

| Workflow Name | MCPs Involved | Trigger |
|--------------|---------------|---------|
| `meeting_to_task` | Hedy, Asana, Slack | EOD-1 |
| `signal_to_task` | Outlook, Slack, Asana, DuckDB | AM-1/AM-2 |
| `wbr_quip_publish` | SharePoint, DuckDB, Builder, Slack | WBR watcher |
| `wiki_enriched_publish` | KDS, ARCC, XWiki, SharePoint | Wiki pipeline |
| `context_enrichment` | KDS, ARCC, DuckDB | EOD-2 |
| `slack_intelligence` | Slack, KDS, DuckDB | AM-1 |

**Logging Pattern (added to each workflow):**

```
-- At workflow start:
INSERT INTO workflow_executions (execution_id, workflow_name, trigger_source, mcp_servers_involved, start_time)
VALUES ('{name}_{timestamp}', '{name}', '{trigger}', ARRAY['{mcp1}', '{mcp2}'], CURRENT_TIMESTAMP);

-- At each step completion:
UPDATE workflow_executions SET steps_completed = steps_completed + 1 WHERE execution_id = '{id}';

-- On step failure:
UPDATE workflow_executions SET steps_failed = steps_failed + 1,
    error_details = '{step_name}:{error_message}'::JSON WHERE execution_id = '{id}';

-- At workflow end:
UPDATE workflow_executions SET end_time = CURRENT_TIMESTAMP, status = '{status}',
    duration_seconds = EPOCH(CURRENT_TIMESTAMP - start_time) WHERE execution_id = '{id}';
```

**Degradation Detection (EOD-2):**

```sql
SELECT workflow_name, success_rate, total_runs
FROM workflow_reliability
WHERE success_rate < 80 AND total_runs >= 3;
```

If results → Slack DM:
```
⚠️ Degraded workflows (7-day window):
• {workflow}: {success_rate}% success ({total_runs} runs). Most common failure: {error}
```

### Component 5: WBR Quip Publishing (Req 2, 9)

Extends the WBR pipeline to publish callouts to Quip via Builder MCP and notify via Slack.

**MCP Chain:** SharePoint → DuckDB → Builder (Quip) → Slack

**Builder MCP Quip Access:**

Builder MCP exposes `ReadInternalWebsites` which can access Quip documents. The workflow:

1. Read current Quip document structure to identify the insertion point
2. Format callouts in Quip-compatible HTML
3. Write callouts to the appropriate section

```
// Step 1: Read existing document
ReadInternalWebsites(url="https://quip-amazon.com/{doc_id}")
// Parse response to find the section for current week

// Step 2: Format callouts
// Each market callout formatted as:
// ## W{NN} — {Market}
// {callout_body}
// Key change: {most_significant_wow_change}

// Step 3: Write to Quip (via Builder MCP's write capability if available,
// or via ReadInternalWebsites with POST-like interaction)
```

**Quip Document Registry (DuckDB):**

```sql
CREATE TABLE IF NOT EXISTS quip_registry (
    doc_name VARCHAR PRIMARY KEY,
    quip_url VARCHAR NOT NULL,
    last_updated TIMESTAMP,
    update_frequency VARCHAR,           -- 'weekly', 'monthly', 'ad_hoc'
    last_content_hash VARCHAR
);

-- Seed with known documents
INSERT INTO quip_registry VALUES
('Pre-WBR Callouts', 'https://quip-amazon.com/{doc_id}', NULL, 'weekly', NULL);
```

**Fallback on Quip Write Failure:**

```
IF Quip write fails:
  1. Save callouts to ~/shared/artifacts/reporting/wbr-callouts-w{NN}.md
  2. self_dm(login="prichwil", text="⚠️ Quip write failed: {error}. Callouts saved to ~/shared/artifacts/reporting/wbr-callouts-w{NN}.md")
  3. Log failure to workflow_executions
```

**Slack Team Notification:**

```
post_message(channel="{team_channel}", text="📊 W{NN} WBR Callouts Published
Markets: AU, MX, US, CA, JP, UK, DE, FR, IT, ES
Highlights:
• AU: Regs {+/-X}% WoW ({driver})
• MX: Spend {+/-X}% WoW ({driver})
• [most significant 3-4 markets]
📄 Quip: {quip_url}")
```

**WBR Watcher Integration:**

Add steps 6-8 to the existing `wbr-watcher.sh` kiro-cli prompt:

```
=== STEP 6: QUIP PUBLISHING ===
Read the Pre-WBR Callouts Quip document via Builder MCP.
Identify the insertion point for W{NN} callouts.
Write formatted callouts preserving existing document structure.
If Quip write fails: save locally, notify Richard, continue to Step 7.

=== STEP 7: SLACK TEAM NOTIFICATION ===
Post to team channel with market highlights and Quip link.
Include one-line summary per market with most significant WoW change.

=== STEP 8: PIPELINE OBSERVABILITY ===
Log pipeline execution to workflow_executions in DuckDB.
Include: steps completed, steps failed, duration, MCP servers used.
```

### Component 6: Knowledge-Enriched Wiki Publishing (Req 3, 10)

Extends the wiki pipeline with KDS/ARCC research and XWiki dual-publishing.

**MCP Chain:** KDS + ARCC → Wiki Pipeline → XWiki + SharePoint → DuckDB

**Wiki Researcher Extension:**

The wiki-researcher agent currently gathers context from local files and SharePoint. Add two new research steps:

```
=== KDS RESEARCH ===
Extract 3-5 topic keywords from the article brief.
Query: knowledge_discovery_search(query="{keywords}", limit=5)
For each result:
  - Assess relevance to article topic (0-10 scale)
  - If relevance >= 7: include in research brief with source attribution
  - Format: "[KDS] {finding_summary} (Source: {source_title})"

=== ARCC RESEARCH ===
Query: search_arcc(query="{keywords}")
For each result:
  - Assess relevance to article topic
  - If relevant: include governance/organizational context
  - Format: "[ARCC] {finding_summary} (Source: {source_title})"
```

**XWiki Publishing (Librarian Extension):**

After SharePoint sync succeeds, publish to XWiki:

```
// Step 1: Convert markdown to XWiki markup
Conversion rules:
  # Heading     → = Heading =
  ## Heading    → == Heading ==
  ### Heading   → === Heading ===
  **bold**      → **bold**
  *italic*      → //italic//
  - list item   → * list item
  1. ordered    → 1. ordered
  `code`        → {{code}}code{{/code}}
  [text](url)   → [[text>>url]]
  | table |     → | table

// Step 2: Determine namespace
Namespace: PaidSearch/{ArticleTitle} (spaces replaced with hyphens)
Category tags from ~/shared/artifacts/index.md artifact category

// Step 3: Publish
xwiki_create_page(space="PaidSearch", title="{article_title}", content="{xwiki_markup}")
OR
xwiki_update_page(space="PaidSearch", title="{article_title}", content="{xwiki_markup}")

// Step 4: Update publication registry
INSERT INTO publication_registry (article_id, article_title, local_path, xwiki_page_id, xwiki_status, xwiki_last_published)
VALUES ('{id}', '{title}', '{path}', '{page_id}', 'published', CURRENT_TIMESTAMP)
ON CONFLICT (article_id) DO UPDATE SET xwiki_status='published', xwiki_last_published=CURRENT_TIMESTAMP;
```

**Publication Registry (DuckDB):**

```sql
CREATE TABLE IF NOT EXISTS publication_registry (
    article_id VARCHAR PRIMARY KEY,
    article_title VARCHAR NOT NULL,
    local_path VARCHAR NOT NULL,
    sharepoint_url VARCHAR,
    xwiki_page_id VARCHAR,
    sharepoint_status VARCHAR DEFAULT 'pending',
    xwiki_status VARCHAR DEFAULT 'pending',
    sharepoint_last_published TIMESTAMP,
    xwiki_last_published TIMESTAMP,
    sync_status VARCHAR DEFAULT 'pending',  -- 'in_sync', 'diverged', 'pending'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Divergence Detection (during sync runs):**

```sql
SELECT article_id, article_title,
    sharepoint_last_published, xwiki_last_published,
    CASE
        WHEN sharepoint_last_published > xwiki_last_published THEN 'sharepoint_ahead'
        WHEN xwiki_last_published > sharepoint_last_published THEN 'xwiki_ahead'
        ELSE 'in_sync'
    END AS divergence
FROM publication_registry
WHERE sharepoint_status = 'published' AND xwiki_status = 'published'
AND ABS(EPOCH(sharepoint_last_published - xwiki_last_published)) > 86400;
```

### Component 7: Automated Context Enrichment (Req 8)

Queries KDS/ARCC during EOD-2 to enrich Body organs with organizational knowledge.

**MCP Chain:** KDS + ARCC → DuckDB (logging) → Intake files → Organ routing

**Query Generation from current.md:**

```
// Read current.md active projects section
// Extract project names and key topics
// Generate 3-5 queries:
//   "Amazon Business Paid Search {project_name}"
//   "{topic} best practices Amazon"
//   "{market} paid search strategy"
```

**Enrichment Pipeline (EOD-2):**

```
=== CONTEXT ENRICHMENT ===
1. Read ~/shared/context/active/current.md → extract active project list
2. For each project, generate 1-2 KDS queries
3. Execute: knowledge_discovery_search(query="{query}", limit=3)
4. For each result:
   a. Score relevance (0-10) against project context
   b. If relevance >= 7:
      - Save to ~/shared/context/intake/kds-{date}-{topic}.md
      - Format: "# KDS Finding: {title}\nSource: {source}\nRelevance: {project}\n\n{summary}"
5. Log all queries to DuckDB:
   INSERT INTO enrichment_log (query_text, source, result_count, relevant_count, routed_to, queried_at)
6. If 3 consecutive runs return 0 relevant results:
   - Regenerate queries from updated current.md
   - Log query refinement
```

**Enrichment Log (DuckDB):**

```sql
CREATE TABLE IF NOT EXISTS enrichment_log (
    log_id VARCHAR PRIMARY KEY DEFAULT gen_random_uuid()::VARCHAR,
    query_text VARCHAR NOT NULL,
    source VARCHAR NOT NULL,            -- 'kds', 'arcc'
    result_count INTEGER DEFAULT 0,
    relevant_count INTEGER DEFAULT 0,
    routed_to VARCHAR,                  -- 'brain', 'eyes', 'memory', 'none'
    queried_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Organ Routing Rules:**

| Finding Type | Target Organ | Example |
|-------------|-------------|---------|
| Strategic insight, org change, leadership direction | brain.md | "New PS strategy for EU expansion" |
| Market data, performance benchmark, competitor intel | eyes.md | "JP paid search CPA benchmarks" |
| Person info, team change, relationship context | memory.md | "New MarTech lead for APAC" |
| Process, compliance, governance | intake (for manual routing) | "Updated data retention policy" |

### Component 8: Slack Conversation Intelligence (Req 12)

Enriches Slack messages with KDS context and enables historical conversation retrieval.

**MCP Chain:** Slack → KDS → DuckDB (FTS)

**AM-1 Slack Enrichment:**

The existing AM-1 Slack scan already stores messages. This component adds:

1. **Acronym/project detection:** Scan message text for internal acronyms (OCI, IECCP, AEO, CPC, ROAS, etc.) and project names
2. **KDS enrichment:** For messages containing unfamiliar terms or referencing internal tools, query KDS for context
3. **Knowledge context attachment:** Store the KDS context alongside the message in DuckDB

```
// During AM-1 Slack scan, for each message with internal references:
IF message contains internal acronym/project not in known_terms:
    result = knowledge_discovery_search(query="{term} Amazon", limit=1)
    IF result.relevant:
        UPDATE slack_messages SET knowledge_context = '{result.summary}'
        WHERE ts = '{message.ts}'
```

**Historical Conversation Retrieval:**

The existing FTS index on `slack_messages` already supports BM25 retrieval. This component adds a combined query pattern:

```sql
-- When Richard asks about a past conversation:
-- Step 1: Search Slack messages
SELECT ts, channel_name, author_name, text_preview,
    fts_main_slack_messages.match_bm25(ts, '{search_terms}') AS score
FROM slack_messages
WHERE score IS NOT NULL
ORDER BY score DESC
LIMIT 10;

-- Step 2: Search KDS for organizational context
-- knowledge_discovery_search(query="{search_terms}", limit=3)

-- Step 3: Combine results with source attribution
```

**AM-2 Triage Context Enhancement:**

When triaging a signal, query for related past conversations:

```sql
-- Find related past messages from same author on similar topic
SELECT ts, channel_name, text_preview, timestamp
FROM slack_messages
WHERE author_name = '{signal_author}'
AND fts_main_slack_messages.match_bm25(ts, '{signal_keywords}') IS NOT NULL
AND timestamp > CURRENT_TIMESTAMP - INTERVAL '30 days'
ORDER BY timestamp DESC
LIMIT 5;
```

Include these in the triage context so AM-2 has conversation history when creating tasks.

### Component 9: AgentCore Browser Automation (Req 5)

**Status: Blocked on internal AWS account (Isengard)**

When unblocked, the AgentCore browser enables Midway-authenticated access to internal tools.

**MCP Chain:** AgentCore Browser → DuckDB (logging) → downstream pipelines

**WorkDocs Dashboard Download:**

```
// Replace SharePoint polling with direct WorkDocs download:
1. browser_create_session() → session_id
2. browser_navigate(session_id, url="https://workdocs.amazon.com/{folder}")
3. browser_authenticate(session_id) → Midway auth
4. browser_click(session_id, selector="[data-file='{dashboard_filename}']")
5. browser_download(session_id) → file_path
6. Validate: file_size > 0, extension == .xlsx
7. Move to ~/shared/tools/dashboard-ingester/input/
8. browser_close_session(session_id)
```

**Fallback:** If AgentCore browser fails → fall back to SharePoint polling (existing mechanism).

**Google Ads UI Extraction (future):**

```
// Campaign performance snapshot:
1. browser_navigate to Google Ads UI
2. Navigate to campaign overview for AU/MX
3. Extract: impressions, clicks, spend, conversions, CPA
4. Store in DuckDB daily_metrics or a new google_ads_snapshots table
```

**Access Logging:**

```sql
CREATE TABLE IF NOT EXISTS browser_access_log (
    access_id VARCHAR PRIMARY KEY DEFAULT gen_random_uuid()::VARCHAR,
    tool_name VARCHAR NOT NULL,
    url VARCHAR NOT NULL,
    session_id VARCHAR,
    success BOOLEAN NOT NULL,
    file_size_bytes INTEGER,
    error_message VARCHAR,
    accessed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Component 10: Sandboxed Code Interpreter (Req 6)

**Status: Blocked on internal AWS account (Isengard)**

When unblocked, routes data analysis to AgentCore's sandboxed environment.

**MCP Chain:** DuckDB (export) → AgentCore Code Interpreter → DuckDB (results) + ~/shared/research/

**Execution Pattern:**

```
1. Export relevant data subset:
   COPY (SELECT * FROM {table} WHERE {filter}) TO '/tmp/export.parquet' (FORMAT PARQUET);

2. Upload to Code Interpreter:
   code_interpreter_create_session() → session_id
   code_interpreter_upload_file(session_id, file_path='/tmp/export.parquet')

3. Execute analysis:
   code_interpreter_execute(session_id, code="""
   import pandas as pd
   import matplotlib.pyplot as plt
   df = pd.read_parquet('export.parquet')
   # ... analysis code ...
   plt.savefig('output.png')
   result = df.describe().to_dict()
   """)

4. Retrieve results:
   code_interpreter_download_file(session_id, 'output.png')
   → Save to ~/shared/research/{descriptive_name}_{timestamp}.png

5. Log execution:
   INSERT INTO code_interpreter_log (script_hash, runtime_ms, data_size_bytes, output_files)
```

**Karpathy Loop Integration:**

For statistical experiments (Bayesian prior updates, A/B test analysis):
- Export experiment data as Parquet
- Run analysis in Code Interpreter (read-only on production data)
- Return results to Karpathy for decision-making

## Correctness Properties

### Property 1: Meeting Action Item Completeness
FOR ALL Hedy sessions with action items assigned to Richard, the count of (Asana tasks created + existing tasks commented + items logged as dependencies) SHALL equal the total action item count from the session.

### Property 2: Signal Deduplication Consistency
FOR ALL signals processed by the signal-to-task pipeline, IF a signal matches an existing Asana task (same sender + similar subject within 7 days), THEN the pipeline SHALL add a comment to the existing task AND NOT create a new task.

### Property 3: Workflow Execution Logging Completeness
FOR ALL cross-MCP workflow executions, the workflow_executions table SHALL contain exactly one record with steps_completed + steps_failed equal to the total steps attempted.

### Property 4: Publication Registry Sync Status
FOR ALL articles in the publication_registry, IF sharepoint_status = 'published' AND xwiki_status = 'published' AND both timestamps are within 24 hours, THEN sync_status SHALL be 'in_sync'.

### Property 5: Meeting Analytics Data Integrity
FOR ALL records in meeting_analytics, richard_speaking_share SHALL be between 0.0 and 1.0 inclusive, AND duration_minutes SHALL be greater than 0.

### Property 6: Enrichment Query Refinement
IF enrichment_log shows 3 consecutive EOD-2 runs with relevant_count = 0 for all queries, THEN the next run SHALL use different query terms derived from the current version of current.md.

## Failure Modes and Mitigations

| Failure | Impact | Mitigation |
|---------|--------|-----------|
| Hedy MCP unreachable during EOD-1 | No meeting-to-task automation | Skip meeting processing, log gap, retry next EOD-1 |
| Asana MCP unreachable during task creation | Action items not captured | Save action items to intake/ for manual processing |
| Builder MCP Quip write fails | Callouts not published to Quip | Save locally, notify via Slack DM, manual copy-paste |
| KDS/ARCC returns no results | No enrichment for that run | Log empty result, continue without enrichment |
| XWiki publish fails | Article only on SharePoint | Retain local + SharePoint, retry next sync |
| DuckDB write fails | Observability gap | Log to local file as fallback, alert via Slack |
| AgentCore browser auth fails | Can't access WorkDocs | Fall back to SharePoint polling |
| Signal dedup false positive | Legitimate new task not created | Low confidence matches create task with "possible duplicate" note |
| Signal dedup false negative | Duplicate task created | EOD-2 reconciliation catches duplicates during Asana scan |
