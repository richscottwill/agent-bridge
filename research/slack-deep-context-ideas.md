# Slack Deep Context Ideas

*Ways to use Slack data — historical backfill, novel uses, and ongoing enrichment — to tighten the knowledge graph across the Body system.*

Created: 2026-04-01
Updated: 2026-04-01
Status: Phase 1 complete. Backlog triaged — see decision log below.

## Decision Log (2026-04-01)

All 25 ideas reviewed. 16 built in the original spec. 9 remaining triaged:

| Idea | Decision | Rationale |
|------|----------|-----------|
| #7 Competitive Intelligence Timeline | SKIPPED | LOW priority. Daily ingestion handles forward-looking case. 14 rows in competitors table sufficient for current ops. |
| #8 People Discovery / Shadow Network | ADDED → Steering scan #8 | Directly addresses #1 annual review gap (visibility). Finds channels/people discussing Richard outside his channels. |
| #10 Org Communication Graph | SKIPPED | Academically interesting but operationally thin. Visibility gaps already covered by #8 and quarterly audit. |
| #11 Response Time Calibration | SKIPPED | Almost entirely covered by DM Archaeology (avg_response_time_hours), quarterly audit (degradation flags), and proactive drafts (24h+ detection). |
| #12 Tribal Knowledge Extraction | ADDED → Steering scan #9 + monthly refresh | Demand-side wiki signal (what team doesn't know) vs supply-side (#7.2 catches Richard's explanations). Monthly refresh added to run-the-loop. |
| #13 Sentiment & Escalation Patterns | ADDED → Steering scan #10 | Longitudinal stress forecasting for predicted QA. Stakeholder escalation profiles + stress calendar. |
| #14 Channel Join Recommendations | SKIPPED | Technically infeasible (can't query other users' channel memberships via Slack MCP). Overlaps heavily with #8 People Discovery. |
| #16 Slack-Sourced Change Log Entries | ADDED → Steering scan #11 | Directly feeds WBR callout pipeline. Fills gaps between CSV exports. change_log is callout backbone. |
| #17 Experiment Backfill from Slack | ADDED → Steering scan #12 | experiments table has 0 rows. Feeds Level 2 (Drive WW Testing) directly. Lifecycle stitching from fragmented Slack threads. |

## Implementation Status

### Built in Original Spec (slack-deep-context tasks.md — all complete)
- ✅ #1 DM Archaeology → Steering scan #2
- ✅ #2 Richard's Slack Voice Corpus → Steering scan #3
- ✅ #3 Decision Mining → Steering scan #4
- ✅ #4 Project Timeline Reconstruction → Steering scan #5
- ✅ #5 Stakeholder Position Mapping → Steering scan #6
- ✅ #6 Pre-Meeting Context → Steering scan #7
- ✅ #9 Conversation Database → DuckDB tables + ingestion pipeline
- ✅ #15 DuckDB Schema → 4 tables in ps-analytics.duckdb
- ✅ #18 Morning Brief → rsw-channel → Hook prompt + daily post
- ✅ #19 rsw-channel Canvas/Dashboard → Pinned message (canvas not supported)
- ✅ #20 Intake Drop Zone → Hook prompt + intake file creation
- ✅ #21 Weekly Relationship Refresh → Enrichment in run-the-loop
- ✅ #22 Monthly Synthesis → Enrichment in run-the-loop
- ✅ #23 Quarterly Stakeholder Audit → Enrichment in run-the-loop
- ✅ #24 Slack-to-Wiki Pipeline → Enrichment in run-the-loop
- ✅ #25 Proactive Draft Suggestions → Enrichment in both hooks

### Added This Session (steering file scans — not yet executed)
- ⬜ #8 People Discovery → Steering scan #8 (backfill_scans.people_discovery)
- ⬜ #12 Tribal Knowledge → Steering scan #9 + monthly refresh (backfill_scans.tribal_knowledge)
- ⬜ #13 Sentiment Patterns → Steering scan #10 (backfill_scans.sentiment_patterns)
- ⬜ #16 Change Log Backfill → Steering scan #11 (backfill_scans.change_log_backfill)
- ⬜ #17 Experiment Backfill → Steering scan #12 (backfill_scans.experiment_backfill)

### Skipped (no action needed)
- ❌ #7 Competitive Intelligence Timeline
- ❌ #10 Org Communication Graph
- ❌ #11 Response Time Calibration
- ❌ #14 Channel Join Recommendations

---

## DEEP CONTEXT (Historical Backfill — One-Time)

These mine months of Slack history to fill gaps in what the system knows. Run once, route to existing organs.

### 1. DM Archaeology — Relationship Graph Enrichment
- Target organ: memory.md (relationship graph)
- Method: Pull full DM history with each People Watch person (Brandon, Alexis, Lena, Lorena, Adi, Yun, Andrew, Dwayne, Stacey, Kate, Carlos, Harjeet, Vijay, Caroline, Frank)
- Extract: Communication patterns, tone evolution over time, topic frequency, response latency, emoji/reaction habits, how they write vs how they write to Richard specifically
- Discover: People who DM Richard regularly but aren't in the relationship graph yet
- Why it matters: Every drafted communication uses the relationship graph for tone. Richer graph = better first drafts. Currently built from ~10 days of Hedy + a few emails.
- Priority: HIGH — highest signal-to-noise ratio of any backfill

### 2. Richard's Slack Voice Corpus
- Target: portable-body/voice/richard-style-slack.md
- Method: Pull all messages from:@prichwil over 6-12 months
- Extract: How Richard actually writes on Slack — sentence length, punctuation habits, emoji usage, formality gradient (DMs vs channels vs threads), how he opens/closes messages, how he escalates vs de-escalates
- Compare: Against richard-writing-style.md to see if Slack voice differs from email voice (it almost certainly does)
- Why it matters: When drafting Slack messages, the system should match Richard's Slack register, not his email register. Currently no Slack-specific voice data.
- Priority: HIGH — directly improves draft quality

### 3. Decision Mining — Brain Backfill
- Target organ: brain.md (decision log) + DuckDB decisions table (currently 0 rows)
- Method: Search team channels for decision language ("decided", "going with", "confirmed", "approved", "let's do", "final call", "we're not going to") over 12 months
- Extract: Who decided, what was decided, what alternatives were discussed, which principle it maps to
- Why it matters: Decision log has 10 entries from the last 6 weeks. Months of decisions live only in Slack threads. Backfilling creates institutional memory.
- Priority: MEDIUM — valuable but labor-intensive to synthesize

### 4. Project Timeline Reconstruction
- Target organ: current.md, eyes.md, wiki articles
- Method: Search for key project names over their full lifecycle: OCI (from first mention to today), Polaris (origin to rollout), Baloo (discovery to early access), F90 (legal SIMs to launch), ad copy overhaul (SP study to EU4 rollout), Walmart response (first appearance to current strategy)
- Extract: Key milestones, who drove what, timeline of decisions, blockers and how they were resolved
- Why it matters: Wiki articles are all DRAFT with reconstructed timelines. Slack threads have the actual chronology. This turns drafts into grounded docs.
- Priority: MEDIUM — feeds wiki articles and OP1 narrative

### 5. Stakeholder Position Mapping
- Target organ: memory.md, meeting series files
- Method: For each key stakeholder (Kate, Brandon, Lena, Nick Georgijev), search their messages in channels Richard is/was in over 6 months
- Extract: What topics they care about, what language they use when they're concerned vs satisfied, what they escalate vs let slide, how their priorities shifted over time
- Why it matters: Predicted QA in eyes.md is only as good as the stakeholder model. Historical Slack reveals what Kate actually asks about, not what Richard thinks she'll ask about.
- Priority: HIGH — directly improves meeting prep and predicted QA

### 6. Pre-Hedy Meeting Context
- Target: meeting series files (stakeholder/, team/, peer/, manager/)
- Method: Search for meeting-adjacent Slack activity — messages within 2 hours before/after recurring meeting times, threads that reference meeting topics
- Extract: Pre-meeting prep discussions, post-meeting follow-ups, action items that were discussed in Slack but never formalized
- Why it matters: Hedy integration started 3/23. Meeting series files have ~10 days of dynamics. Slack has months of the surrounding context.
- Priority: MEDIUM


### 7. Competitive Intelligence Timeline
- Target: eyes.md (competitive landscape) + DuckDB competitors table (14 rows)
- Method: Search for competitor names (Walmart Business, weareuncapped, shop-pro.jp, Amazon Global Logistics) across all channels over 12 months
- Extract: First appearance dates, team reactions, strategy discussions, IS data shared in threads
- Why it matters: Competitors table is sparse. Slack threads contain the real-time reactions and data points that never made it to a spreadsheet.
- Priority: LOW — useful but competitors table is secondary to core operations

### 8. People Discovery — Shadow Network
- Target: memory.md (relationship graph), people_watch in channel registry
- Method: Search for prichwil mentions across ALL of Slack (not just Richard's channels) over 6 months
- Extract: Who talks about Richard when he's not in the room? Which channels discuss his work? Who references his projects?
- Why it matters: Proactive search does this daily but only looks back 3 days. A deep scan reveals the full shadow network — people and channels Richard should know about.
- Priority: MEDIUM — could surface career-relevant visibility signals


---

## NOVEL IDEAS (Beyond Backfill)

### 9. Slack Conversation Database (Persistent Searchable Store)
- Target: NEW — DuckDB table(s) + wiki-searchable index
- Concept: Instead of searching Slack live every morning routine (API calls, rate limits, transient results), build a local conversation database. Ingest threads once, store them structured in DuckDB, and search locally forever.
- Schema concept:
  - `slack_messages` — ts, channel_id, channel_name, author_id, author_alias, text, thread_ts, reply_count, reactions, is_richard, relevance_score, ingested_at
  - `slack_threads` — thread_ts, channel_id, channel_name, participant_aliases, message_count, topic_summary, decision_extracted, action_items, first_message_ts, last_message_ts
  - `slack_people` — user_id, alias, display_name, first_seen, last_seen, message_count, dm_count, channels_shared, relationship_tier
  - `slack_topics` — topic, first_seen, last_seen, channels, participants, signal_count, status (active/cooled/archived)
- Why it matters: Right now every scan is ephemeral — we read Slack, extract signals, write to organs, delete the digest. The raw conversations are gone. A persistent store means we can re-query historical context without hitting the Slack API again. "What did Brandon say about OCI in January?" becomes a local SQL query, not a Slack search.
- Integration: Wiki concierge could search this DB alongside published articles. Morning routine reads from local DB instead of (or in addition to) live Slack API. Reduces API dependency and rate limit risk.
- Feeds: Every other idea on this list. Once conversations are in DuckDB, all the backfill ideas become SQL queries instead of Slack API calls.
- Priority: HIGH — this is infrastructure that makes everything else cheaper

### 10. Org Communication Graph (Network Analysis)
- Target: memory.md, brain.md, nervous-system.md
- Method: From the conversation database (idea #9), build a communication graph: who talks to whom, how often, in which channels, about what topics
- Extract: Richard's communication centrality (is he a hub or a spoke?), information flow patterns (who knows things first?), cluster detection (which groups form around which topics?)
- Novel insight: Map where Richard is ABSENT from conversations he should be in. If Brandon and Kate discuss testing in a channel Richard isn't in, that's a visibility gap the system should flag.
- Why it matters: Annual Review says visibility is the #1 growth area. A communication graph quantifies the gap and shows exactly where to insert yourself.
- Priority: MEDIUM — powerful but depends on idea #9 being built first


### 11. Response Time Calibration
- Target: nervous-system.md (new calibration data), memory.md (relationship graph)
- Method: For each People Watch person, measure Richard's average response time to their DMs and @mentions over 6 months
- Extract: Who does Richard respond to fastest? Who gets left on read? Are there patterns (fast on AU, slow on admin)?
- Novel insight: Cross-reference with the aMCC avoidance patterns. Does Richard's response latency correlate with task difficulty? Does he respond fast to easy asks and slow to hard ones?
- Why it matters: Response time IS a signal of priority and relationship health. If Lena's messages sit for 3 days while Adi gets same-day replies, that's a stakeholder management problem the system should surface.
- Priority: LOW — interesting but niche

### 12. Tribal Knowledge Extraction (Wiki Demand Signals)
- Target: wiki demand-log.md, wiki articles
- Method: Search for question patterns in team channels: "does anyone know", "how do we", "where is the", "what's the process for", "who owns"
- Extract: Recurring questions (these are wiki article candidates), who asks them (audience for the wiki), who answers them (subject matter experts to interview)
- Novel insight: The questions people ask repeatedly in Slack are the exact gaps in team documentation. This turns Slack into a wiki roadmap.
- Why it matters: Wiki has 35 draft articles but no demand validation. This tells you which articles people actually need.
- Priority: MEDIUM — directly feeds wiki roadmap

### 13. Sentiment & Escalation Patterns
- Target: brain.md (decision principles), nervous-system.md
- Method: Track emotional tone in team channels over time — when does language shift from neutral to urgent? What topics trigger escalation language?
- Extract: Escalation triggers (what makes Brandon write in all caps?), de-escalation patterns (what calms stakeholders down?), seasonal stress patterns (WBR weeks, QBR prep, OP planning)
- Why it matters: Predicted QA in eyes.md could include a "stress forecast" — if it's WBR week and AU numbers are down, predict escalation from Lena.
- Priority: LOW — novel but speculative

### 14. Channel Join Recommendations (Proactive Discovery)
- Target: channel registry, current.md
- Method: Analyze which channels People Watch contacts are in that Richard is NOT in. Cross-reference with project keywords.
- Extract: Channels where Richard's work is discussed but he has no presence. Channels where his stakeholders are active.
- Why it matters: Proactive search catches mentions, but being IN the channel means you see the full context, not just search hits.
- Priority: LOW — quick win, low effort


---

## DUCKDB STRUCTURING (Making Slack Data Queryable)

### 15. Slack Schema for DuckDB (Foundation)
- New tables to add to ps-analytics.duckdb:
```sql
-- Core message store
CREATE TABLE slack_messages (
    ts VARCHAR PRIMARY KEY,
    channel_id VARCHAR NOT NULL,
    channel_name VARCHAR,
    thread_ts VARCHAR,
    author_id VARCHAR NOT NULL,
    author_alias VARCHAR,
    author_name VARCHAR,
    text_preview VARCHAR,        -- first 200 chars (not full text — portability)
    full_text VARCHAR,           -- full message for search
    is_richard BOOLEAN,
    is_thread_reply BOOLEAN,
    reply_count INTEGER DEFAULT 0,
    reaction_count INTEGER DEFAULT 0,
    richard_reacted BOOLEAN DEFAULT FALSE,
    relevance_score INTEGER,
    signal_type VARCHAR,         -- decision, action-item, status-change, etc.
    ingested_at TIMESTAMP DEFAULT current_timestamp
);

-- Thread summaries (synthesized, not raw)
CREATE TABLE slack_threads (
    thread_ts VARCHAR PRIMARY KEY,
    channel_id VARCHAR NOT NULL,
    channel_name VARCHAR,
    topic_summary VARCHAR,       -- 1-2 sentence synthesis
    participant_aliases VARCHAR, -- comma-separated
    message_count INTEGER,
    decision_extracted VARCHAR,  -- null if no decision
    action_items VARCHAR,        -- null if none
    first_ts TIMESTAMP,
    last_ts TIMESTAMP,
    ingested_at TIMESTAMP DEFAULT current_timestamp
);

-- People interaction tracking
CREATE TABLE slack_people (
    user_id VARCHAR PRIMARY KEY,
    alias VARCHAR,
    display_name VARCHAR,
    first_interaction DATE,
    last_interaction DATE,
    total_messages INTEGER DEFAULT 0,
    dm_messages INTEGER DEFAULT 0,
    channel_messages INTEGER DEFAULT 0,
    channels_shared INTEGER DEFAULT 0,
    avg_response_time_hours DOUBLE,
    relationship_tier VARCHAR,   -- always_high, boosted, candidate, none
    ingested_at TIMESTAMP DEFAULT current_timestamp
);

-- Topic clusters over time
CREATE TABLE slack_topics (
    topic VARCHAR,
    week VARCHAR,
    channel_count INTEGER,
    message_count INTEGER,
    participant_count INTEGER,
    key_participants VARCHAR,
    status VARCHAR DEFAULT 'active',
    related_project VARCHAR,     -- links to current.md project name
    ingested_at TIMESTAMP DEFAULT current_timestamp,
    PRIMARY KEY (topic, week)
);
```
- Why: Makes every other idea on this list a SQL query. "Who mentioned OCI in January?" "How many DMs did Richard exchange with Lena last quarter?" "What topics peaked in W8?" All answerable without touching the Slack API.
- Priority: HIGH — build this first, then populate via backfill ideas

### 16. Slack-Sourced Change Log Entries
- Target: DuckDB change_log table (currently 477 rows from CSVs)
- Method: Extract status changes and launches from historical Slack ("launched", "live", "dialed up", "switched", "migrated") and insert as change_log rows with source='slack'
- Why: Change log is the backbone of WBR callouts. Slack-sourced entries fill gaps between CSV exports.
- Priority: MEDIUM

### 17. Experiment Backfill from Slack
- Target: DuckDB experiments table (currently 0 rows)
- Method: Search for test/experiment language ("testing", "weblab", "A/B", "control vs", "results show", "lift of") in team channels
- Extract: Experiment name, hypothesis, start/end dates, results, decisions made
- Why: The experiments table is empty. Slack threads contain the actual test discussions that never got formalized.
- Priority: MEDIUM — feeds Level 2 (Drive WW Testing) directly


---

## RSW-CHANNEL AS COMMAND CENTER

### 18. Morning Routine → rsw-channel Daily Brief Post
- Target: rsw-channel (C0993SRL6FQ) — Richard's private channel
- Concept: After the morning routine builds the daily brief email, ALSO post a condensed version to rsw-channel. This gives Richard a Slack-native daily brief he can glance at on mobile without opening email.
- Format: Single message with key sections — top 3 priorities, calendar highlights, pending actions count, streak status
- Update behavior: Post new each morning (not edit — Slack's edit history is messy). Pin the latest one so it's always at the top.
- Why it matters: Richard checks Slack more than email. Meeting him where he already is. (Principle: reduce decisions, not options — the brief is already built, just put it where he'll see it.)
- Guardrails: rsw-channel is explicitly allowed for post_message per slack-guardrails.md.
- Priority: HIGH — trivial to implement, high daily value

### 19. rsw-channel Canvas — Live Dashboard
- Target: rsw-channel canvas (Slack's built-in document feature)
- Concept: Create a Slack canvas pinned to rsw-channel that serves as a live dashboard. Updated by the morning routine and system refresh. Always current.
- Sections:
  - **Today** — top 3 priorities, calendar, pending action count
  - **Streak** — aMCC streak counter, hard thing status, days since last artifact
  - **Markets** — one-line status per market (AU, MX, US, EU5, JP, CA)
  - **Hot Topics** — from scan state, what's trending in Slack
  - **Pending Responses** — who's waiting on Richard (from hands.md + Slack reaction checking)
  - **Five Levels** — current position, gate status
- Why it matters: A canvas is persistent (unlike messages that scroll away), editable by the system, and visible in Slack's sidebar. It becomes the single-glance status page Richard can check from his phone.
- Technical: Slack MCP has download_file_content for reading canvases. Writing/updating canvases may require the Slack API's canvas methods — need to check if the MCP server supports canvas writes. If not, we could use a pinned message that gets updated instead.
- Priority: HIGH — if canvas writes are supported. MEDIUM if we have to fall back to pinned messages.

### 20. rsw-channel as Intake Drop Zone
- Concept: Richard can drop quick notes, links, screenshots into rsw-channel from his phone. The morning routine or system refresh scans rsw-channel for new messages from Richard and routes them to intake/ for processing.
- Why it matters: Currently, getting something into the system requires being at the computer (AgentSpaces). rsw-channel becomes a mobile intake mechanism. "Remind me to follow up with Lena about CPA" → dropped in rsw-channel → picked up by morning routine → routed to hands.md.
- Already partially working: rsw-channel is Tier 1 in the channel registry. But the current ingestion treats it like any other channel. This idea makes it a deliberate intake channel with special routing.
- Priority: MEDIUM — requires minor ingestion logic change


---

## ONGOING ENRICHMENT (Not One-Time, Not Daily — Periodic)

### 21. Weekly Relationship Graph Refresh from Slack
- Cadence: Weekly (Friday system refresh)
- Method: Query the conversation database (idea #9) for interaction counts per person over the trailing 7 days. Auto-promote candidates who hit the 3+ interaction threshold. Auto-demote people who haven't interacted in 60 days.
- Why: People Watch is currently manually derived. This makes it self-maintaining.
- Priority: MEDIUM — depends on idea #9

### 22. Monthly "What Changed" Synthesis
- Cadence: Monthly
- Method: Query conversation database for topic trends, new people, channel activity shifts. Produce a one-page "What changed in Richard's Slack world this month" synthesis.
- Route to: brain.md (strategic shifts), memory.md (relationship changes), eyes.md (market context shifts)
- Why: The daily scan catches signals. The monthly synthesis catches trends. Different timescale, different insights.
- Priority: LOW — nice to have

### 23. Quarterly Stakeholder Communication Audit
- Cadence: Quarterly (aligned with QBR prep)
- Method: From conversation database, produce per-stakeholder communication report: message volume, response times, topics discussed, sentiment trajectory, channel overlap
- Route to: nervous-system.md (Loop 9 data), memory.md (relationship graph updates)
- Why: Annual Review said visibility is the #1 gap. This quantifies it quarterly so Richard can course-correct before the next review.
- Priority: MEDIUM — directly addresses the career growth gap

### 24. Slack-to-Wiki Pipeline (Automatic Article Candidates)
- Cadence: Weekly
- Method: From conversation database, identify threads where Richard gave detailed explanations (long messages, multiple replies, teaching tone). These are wiki article candidates — Richard already wrote the content, it just needs to be formalized.
- Route to: wiki demand-log.md with thread links
- Why: Richard's best explanations happen in Slack threads and never get documented. This captures them before they scroll into oblivion.
- Priority: MEDIUM — feeds Level 1 (artifact shipping) with minimal new effort

### 25. Proactive Draft Suggestions from Slack Context
- Concept: When the system detects an unanswered question or request directed at Richard in Slack (via reaction checking — no reaction, no reply, 24h+ old), auto-draft a response using memory.md tone + the thread context, and drop it in rsw-channel or as a Slack draft.
- Why: Reduces the friction of responding. Richard's biggest response delays are on messages that require thought. A pre-written draft turns a 10-minute composition into a 30-second review-and-send.
- Principle: Reduce decisions, not options. The draft doesn't prevent Richard from writing his own — it just makes responding the path of least resistance.
- Priority: HIGH — directly addresses response latency patterns in nervous-system.md

---

## EXECUTION ORDER (Recommended)

If building these out, the dependency chain suggests:

**Already built (original spec):**
1. ~~#15 DuckDB Schema~~ ✅
2. ~~#9 Conversation Database~~ ✅
3. ~~#1 DM Archaeology~~ ✅
4. ~~#2 Richard's Slack Voice~~ ✅
5. ~~#18 Morning Brief → rsw-channel~~ ✅
6. ~~#19 rsw-channel Canvas~~ ✅ (pinned message fallback)
7. ~~#5 Stakeholder Position Mapping~~ ✅
8. ~~#25 Proactive Draft Suggestions~~ ✅
9. ~~#3 Decision Mining~~ ✅
10. ~~#12 Tribal Knowledge Extraction~~ ✅ (steering scan + monthly refresh)

**Next to execute (new scans, recommended order):**
11. #16 Change Log Backfill — feeds callout pipeline immediately, highest operational value
12. #17 Experiment Backfill — shares search results with #16, feeds Level 2
13. #8 People Discovery — one-time visibility baseline, independent of other scans
14. #12 Tribal Knowledge — demand signals for wiki roadmap
15. #13 Sentiment Patterns — enrichment layer, lowest urgency of the new scans

---

## NOTES

- All backfill ideas are READ-ONLY on Slack (per guardrails). No messages sent, no channels joined.
- All outputs route through existing organs — no new files in the body.
- The conversation database (#9) is the keystone. Build it first and everything else becomes a SQL query. ✅ Built.
- rsw-channel ideas (#18-20) are allowed per slack-guardrails.md — it's Richard's private channel. ✅ Built.
- Canvas support (#19) validated — not supported. Pinned message fallback implemented. ✅ Done.
- Steering file: `~/.kiro/steering/slack-deep-context.md` — 12 backfill scans total (7 original + 5 added 2026-04-01).
- Scan state: `~/shared/context/active/slack-scan-state.json` — all 12 scans tracked in backfill_scans.
- 4 ideas skipped (#7, #10, #11, #14) — can be revisited if circumstances change.
