# Requirements Document

## Introduction

This document defines the requirements for Slack Deep Context — a four-phase extension of the existing Slack Context Ingestion system (v3, live since 4/1) that transforms Slack from a real-time signal source into a persistent, queryable knowledge layer for the Body system.

The existing ingestion system reads Slack channels during morning routine and system refresh hooks, extracts signals (decisions, action items, status changes), and routes them to Body organs. That system is ephemeral — it reads, extracts, writes to organs, and discards the raw conversations. Slack Deep Context makes three structural changes:

1. **rsw-channel as Command Center** — Richard's private Slack channel (C0993SRL6FQ) becomes a live dashboard and mobile intake mechanism, meeting Richard where he already looks
2. **Conversation Database** — A persistent DuckDB store (slack_messages, slack_threads, slack_people, slack_topics in ps-analytics.duckdb) that makes historical Slack data queryable via SQL instead of live API calls
3. **Historical Backfill** — One-time deep scans of DM history, Richard's Slack voice, decision mining, project timelines, stakeholder positions, and pre-meeting context to fill knowledge gaps across the Body
4. **Ongoing Enrichment** — Periodic (weekly/monthly/quarterly) processes that keep the knowledge graph fresh: relationship graph refresh, synthesis reports, stakeholder audits, wiki pipeline, and proactive draft suggestions

Design principles governing this feature:
- **Routine as liberation** — rsw-channel daily brief and canvas eliminate the decision of where to look for status
- **Structural over cosmetic** — A conversation database changes what the system can answer, not how it looks
- **Subtraction before addition** — The conversation DB replaces live API calls with local SQL queries, reducing API dependency
- **Reduce decisions, not options** — Proactive draft suggestions make responding the path of least resistance
- **Invisible over visible** — Enrichment processes run periodically in the background; Richard sees better outputs, not new processes
- **Portability** — A new AI on a different platform can read the DuckDB and text files without Slack MCP access

Key constraints:
- Read-only on Slack per slack-guardrails.md, EXCEPT rsw-channel (C0993SRL6FQ) which allows post_message
- All outputs route through existing Body organs — no new organ files
- Conversation database lives in existing DuckDB (ps-analytics.duckdb)
- Word budgets from gut.md must be respected when writing to organs
- Canvas support requires technical validation — fall back to pinned messages if Slack MCP does not support canvas create/update

## Glossary

- **RSW_Channel**: Richard's private Slack channel (ID: C0993SRL6FQ), the only channel where post_message is permitted per slack-guardrails.md
- **Conversation_Database**: Four DuckDB tables (slack_messages, slack_threads, slack_people, slack_topics) in ps-analytics.duckdb that store structured Slack conversation data for local SQL querying
- **Daily_Brief_Post**: A condensed summary of the morning routine daily brief posted to RSW_Channel each morning
- **Live_Dashboard**: A Slack canvas (or pinned message fallback) in RSW_Channel showing current priorities, streak status, market one-liners, hot topics, pending responses, and Five Levels position
- **Intake_Drop_Zone**: The mechanism by which messages Richard drops into RSW_Channel from mobile are captured and routed to ~/shared/context/intake/ for processing
- **Backfill_Scan**: A one-time deep historical scan of Slack data targeting a specific knowledge gap (DM history, voice corpus, decisions, project timelines, stakeholder positions, or meeting context)
- **Voice_Corpus**: A collection of Richard's own Slack messages (from:@prichwil) analyzed for writing style patterns specific to Slack communication
- **Decision_Mining**: The process of searching historical Slack messages for decision language and extracting structured decision records
- **Relationship_Graph**: The section of memory.md that tracks key people, their communication patterns, tone, and interaction history
- **Enrichment_Process**: A periodic (non-daily) process that queries the Conversation_Database to produce synthesis, refresh relationship data, or generate content candidates
- **Slack_Ingester**: The existing module (v3) that reads Slack channels during morning routine and system refresh hooks
- **Body_System**: The 11-organ AI context system managing Richard's working context
- **Morning_Routine**: The daily hook that reads fresh organs, syncs Asana, drafts replies, refreshes To-Do, produces a daily brief, and sets calendar blocks
- **Autoresearch_Loop**: The system refresh hook that maintains ground truth, cascades changes to organs, and runs experiments
- **Slack_MCP**: The ai-community-slack-mcp MCP server providing read/write access to Slack
- **People_Watch**: The set of key people whose Slack messages are tracked regardless of channel, derived from memory.md
- **Canvas**: Slack's built-in document feature that can be pinned to a channel and updated programmatically
- **Pinned_Message**: A Slack message pinned to a channel, used as fallback if canvas operations are not supported by Slack_MCP

## Requirements


### Requirement 1: Daily Brief Post to rsw-channel

**User Story:** As Richard, I want the morning routine to post a condensed daily brief to rsw-channel, so that I can glance at my daily status from Slack on mobile without opening email.

#### Acceptance Criteria

1. WHEN the Morning_Routine completes the daily brief generation, THE Morning_Routine SHALL post a condensed version of the daily brief to RSW_Channel via post_message
2. THE Daily_Brief_Post SHALL contain: top 3 priorities, calendar highlights for the day, pending action count (from hands.md), and aMCC streak status
3. THE Daily_Brief_Post SHALL not exceed 300 words to remain scannable on mobile
4. WHEN the Morning_Routine posts a new Daily_Brief_Post, THE Morning_Routine SHALL pin the new message so the latest brief is always accessible at the top of RSW_Channel
5. THE Morning_Routine SHALL post a new message each morning rather than editing a previous message, because Slack edit history creates confusion
6. IF the Morning_Routine fails to post to RSW_Channel due to a Slack_MCP error, THEN THE Morning_Routine SHALL log the error and continue the remaining routine steps without blocking

### Requirement 2: rsw-channel Live Dashboard

**User Story:** As Richard, I want a persistent live dashboard in rsw-channel showing current system status, so that I have a single-glance status page accessible from my phone.

#### Acceptance Criteria

1. THE Live_Dashboard SHALL display six sections: Today (top 3 priorities, calendar, pending action count), Streak (aMCC streak counter, hard thing status, days since last artifact), Markets (one-line status per market: AU, MX, US, EU5, JP, CA), Hot Topics (trending topics from slack-scan-state.json), Pending Responses (who is waiting on Richard, from hands.md and reaction checking), and Five Levels (current position and gate status)
2. WHEN the Morning_Routine completes, THE Morning_Routine SHALL update the Live_Dashboard with current data from Body organs
3. WHEN the Autoresearch_Loop completes, THE Autoresearch_Loop SHALL update the Live_Dashboard with refreshed data
4. WHEN Slack_MCP supports canvas create and update operations, THE Body_System SHALL implement the Live_Dashboard as a Canvas pinned to RSW_Channel
5. WHEN Slack_MCP does not support canvas create or update operations, THE Body_System SHALL implement the Live_Dashboard as a Pinned_Message in RSW_Channel that is updated by editing the existing message
6. THE Live_Dashboard content SHALL be generated from existing Body organ files (eyes.md, hands.md, amcc.md, brain.md, slack-scan-state.json) without requiring additional API calls beyond the Slack post/update

### Requirement 3: rsw-channel Mobile Intake Drop Zone

**User Story:** As Richard, I want to drop quick notes, links, and screenshots into rsw-channel from my phone and have the system pick them up, so that I can capture ideas and tasks on mobile without being at my computer.

#### Acceptance Criteria

1. WHEN the Morning_Routine or Autoresearch_Loop runs, THE Slack_Ingester SHALL scan RSW_Channel for new messages posted by Richard since the last scan
2. WHEN a new message from Richard is found in RSW_Channel, THE Slack_Ingester SHALL create a file in ~/shared/context/intake/ containing the message text, any attached links, and a timestamp
3. WHEN the intake file is created from an RSW_Channel message, THE Body_System SHALL process the intake file through the standard digestion protocol (gut.md) during the next cascade
4. WHEN Richard's RSW_Channel message contains a recognizable action item pattern (e.g., "remind me to", "follow up with", "todo:"), THE Slack_Ingester SHALL tag the intake file with [ACTION-RW] for priority routing to hands.md
5. THE Slack_Ingester SHALL distinguish between Richard's intake messages and system-posted messages (Daily_Brief_Post, Live_Dashboard updates) in RSW_Channel and SHALL process only Richard's messages as intake
6. WHEN Richard's RSW_Channel message contains a file attachment or image, THE Slack_Ingester SHALL download the file content via download_file_content and include it in the intake file


### Requirement 4: DuckDB Conversation Database Schema

**User Story:** As a system architect, I want a structured conversation database in DuckDB, so that historical Slack data is queryable via SQL without hitting the Slack API.

#### Acceptance Criteria

1. THE Conversation_Database SHALL add four tables to ps-analytics.duckdb: slack_messages (individual messages with author, channel, text, thread reference, relevance score, signal type), slack_threads (thread summaries with topic, participants, decisions, action items), slack_people (interaction tracking per person with message counts, response times, relationship tier), and slack_topics (topic clusters over time with channel count, participant count, status)
2. THE slack_messages table SHALL use the Slack message timestamp (ts) as primary key and SHALL store: ts, channel_id, channel_name, thread_ts, author_id, author_alias, author_name, text_preview (first 200 characters), full_text, is_richard (boolean), is_thread_reply (boolean), reply_count, reaction_count, richard_reacted (boolean), relevance_score, signal_type, and ingested_at
3. THE slack_threads table SHALL use thread_ts as primary key and SHALL store: thread_ts, channel_id, channel_name, topic_summary (one to two sentence synthesis), participant_aliases, message_count, decision_extracted, action_items, first_ts, last_ts, and ingested_at
4. THE slack_people table SHALL use user_id as primary key and SHALL store: user_id, alias, display_name, first_interaction, last_interaction, total_messages, dm_messages, channel_messages, channels_shared, avg_response_time_hours, relationship_tier, and ingested_at
5. THE slack_topics table SHALL use a composite primary key of (topic, week) and SHALL store: topic, week, channel_count, message_count, participant_count, key_participants, status (active/cooled/archived), related_project, and ingested_at
6. THE schema SQL SHALL be added to ~/shared/tools/data/schema.sql alongside existing table definitions so the full database schema remains documented in one file

### Requirement 5: Conversation Database Ingestion Pipeline

**User Story:** As a system operator, I want the existing Slack ingestion to populate the conversation database alongside its current organ routing, so that every scanned message is stored persistently for future querying.

#### Acceptance Criteria

1. WHEN the Slack_Ingester processes messages during morning routine or system refresh, THE Slack_Ingester SHALL insert each message into the slack_messages table in addition to its existing signal extraction and organ routing
2. WHEN the Slack_Ingester processes a thread, THE Slack_Ingester SHALL insert or update a row in the slack_threads table with a synthesized topic summary, participant list, and any extracted decisions or action items
3. WHEN the Slack_Ingester encounters a new author not yet in the slack_people table, THE Slack_Ingester SHALL insert a new row with initial interaction data
4. WHEN the Slack_Ingester encounters an existing author in the slack_people table, THE Slack_Ingester SHALL update the last_interaction date, increment message counts, and recalculate channels_shared
5. THE Slack_Ingester SHALL use DuckDB upsert operations (INSERT OR REPLACE) to handle messages that have been edited since the last scan
6. WHEN the Slack_Ingester detects a topic cluster (same topic in 3 or more channels within a week), THE Slack_Ingester SHALL insert or update a row in the slack_topics table
7. THE ingestion pipeline SHALL not slow down the existing morning routine or system refresh by more than 30 seconds per cycle — DuckDB writes SHALL be batched

### Requirement 6: Conversation Database Query Interface

**User Story:** As a system operator, I want agents and hooks to query the conversation database using SQL, so that historical Slack context is available for meeting prep, wiki research, and daily briefs without live API calls.

#### Acceptance Criteria

1. THE Conversation_Database SHALL be queryable via the existing DuckDB MCP Server (execute_query) and Python query interface (~/shared/tools/data/query.py)
2. WHEN the Wiki_Concierge searches for context on a topic, THE Wiki_Concierge SHALL query the Conversation_Database alongside published wiki articles
3. WHEN the Morning_Routine prepares meeting context, THE Morning_Routine SHALL query the Conversation_Database for recent messages from meeting participants
4. WHEN an agent needs to answer a question like "What did [person] say about [topic] in [time period]?", THE agent SHALL construct a SQL query against slack_messages filtered by author_alias, full_text search, and timestamp range
5. THE Conversation_Database SHALL support full-text search on the full_text column of slack_messages for keyword-based queries
6. WHEN the Conversation_Database is queried and returns results, THE results SHALL include source attribution (channel_name, author_alias, timestamp) so the agent can cite the original Slack context


### Requirement 7: DM Archaeology — Relationship Graph Enrichment

**User Story:** As Richard, I want the system to scan full DM history with People Watch contacts, so that the relationship graph in memory.md is enriched with communication patterns, tone evolution, and topic frequency beyond the 10 days of Hedy data.

#### Acceptance Criteria

1. WHEN a DM Archaeology Backfill_Scan is triggered, THE Slack_Ingester SHALL retrieve the full DM history with each People_Watch contact listed in the channel registry
2. FOR EACH DM conversation, THE Slack_Ingester SHALL extract: communication frequency, tone patterns, topic distribution, response latency averages, and how the contact's writing style differs when messaging Richard versus in channels
3. THE Backfill_Scan SHALL insert all retrieved DM messages into the slack_messages table in the Conversation_Database with is_richard flagged appropriately
4. THE Backfill_Scan SHALL update the slack_people table with enriched interaction data: total DM message counts, average response time, first and last interaction dates
5. WHEN the Backfill_Scan discovers a person who DMs Richard regularly but is not in the People_Watch list, THE Backfill_Scan SHALL flag the person as a candidate for People_Watch addition in slack-scan-state.json
6. THE Backfill_Scan SHALL produce a synthesis document routed to memory.md containing updated relationship graph entries with enriched tone notes, topic patterns, and communication style observations for each contact
7. THE Backfill_Scan SHALL respect gut.md word budgets when writing to memory.md — if memory.md is at capacity, the synthesis SHALL be stored in ~/shared/context/intake/ for deferred processing

### Requirement 8: Richard's Slack Voice Corpus

**User Story:** As a system architect, I want to extract Richard's Slack writing patterns from historical messages, so that drafted Slack messages match Richard's Slack register rather than his email register.

#### Acceptance Criteria

1. WHEN a Voice Corpus Backfill_Scan is triggered, THE Slack_Ingester SHALL retrieve all messages authored by Richard (from:@prichwil) over the past 12 months across all accessible channels and DMs
2. THE Backfill_Scan SHALL analyze Richard's Slack messages for: sentence length distribution, punctuation habits, emoji usage frequency and patterns, formality gradient (DMs versus channels versus threads), opening and closing patterns, escalation and de-escalation language, and register differences from richard-writing-style.md
3. THE Backfill_Scan SHALL insert all retrieved Richard messages into the slack_messages table with is_richard set to true
4. THE Backfill_Scan SHALL produce a voice analysis document at ~/shared/portable-body/voice/richard-style-slack.md containing Slack-specific writing patterns, with examples grouped by context (DM, channel, thread) and formality level
5. THE voice analysis document SHALL be structured so that any agent drafting a Slack message can load it alongside richard-writing-style.md to select the appropriate register
6. THE Backfill_Scan SHALL compare Slack voice patterns against the existing richard-writing-style.md and note significant differences (e.g., shorter sentences, more emoji, less formal closings) in the voice analysis document

### Requirement 9: Decision Mining — Brain Backfill

**User Story:** As Richard, I want the system to mine historical Slack conversations for decisions, so that brain.md decision log and the DuckDB decisions table are populated with institutional memory beyond the last 6 weeks.

#### Acceptance Criteria

1. WHEN a Decision Mining Backfill_Scan is triggered, THE Slack_Ingester SHALL search team channels for decision language patterns ("decided", "going with", "confirmed", "approved", "let's do", "final call", "we're not going to") over the past 12 months
2. FOR EACH detected decision, THE Backfill_Scan SHALL extract: who decided, what was decided, what alternatives were discussed, the channel and thread where the decision was made, and the date
3. THE Backfill_Scan SHALL insert each extracted decision into the DuckDB decisions table with decision_type, market (if applicable), description, rationale, made_by, and created_at
4. THE Backfill_Scan SHALL insert the source messages into the slack_messages table with signal_type set to "decision"
5. THE Backfill_Scan SHALL produce a synthesis of high-impact decisions (those affecting multiple markets or made by L7+ stakeholders) for routing to brain.md decision log
6. THE Backfill_Scan SHALL map extracted decisions to existing brain.md decision principles where applicable, noting which principle each decision reinforces or qualifies
7. THE Backfill_Scan SHALL respect gut.md word budgets for brain.md — only the highest-impact decisions SHALL be written to the organ, with the full set queryable in DuckDB


### Requirement 10: Project Timeline Reconstruction

**User Story:** As Richard, I want the system to reconstruct project timelines from historical Slack conversations, so that wiki articles have grounded chronologies and current.md reflects actual project history.

#### Acceptance Criteria

1. WHEN a Project Timeline Backfill_Scan is triggered for a specific project name (e.g., OCI, Polaris, Baloo, F90, ad copy overhaul, Walmart response), THE Slack_Ingester SHALL search all accessible channels for mentions of that project over its full lifecycle
2. FOR EACH project, THE Backfill_Scan SHALL extract: key milestones, who drove each milestone, timeline of decisions, blockers and how they were resolved, and channel sources
3. THE Backfill_Scan SHALL insert all project-related messages into the slack_messages table with the related project tagged in signal_type
4. THE Backfill_Scan SHALL produce a structured timeline document per project routed to ~/shared/context/intake/ for processing into wiki articles and current.md
5. THE timeline document SHALL include source attribution (channel, author, date) for each milestone so wiki articles can cite original Slack context
6. THE Backfill_Scan SHALL cross-reference extracted timelines with existing wiki article drafts and flag discrepancies between reconstructed and documented timelines

### Requirement 11: Stakeholder Position Mapping

**User Story:** As Richard, I want the system to map stakeholder communication patterns from historical Slack data, so that predicted QA in eyes.md and meeting prep are grounded in what stakeholders actually care about.

#### Acceptance Criteria

1. WHEN a Stakeholder Position Backfill_Scan is triggered, THE Slack_Ingester SHALL search for messages from key stakeholders (Kate Rundell, Brandon Munday, Lena Zak, Nick Georgijev) across all channels Richard is or was in, over the past 6 months
2. FOR EACH stakeholder, THE Backfill_Scan SHALL extract: topics they raise most frequently, language patterns when concerned versus satisfied, what they escalate versus let slide, and how their priorities shifted over time
3. THE Backfill_Scan SHALL insert all stakeholder messages into the slack_messages table and update the slack_people table with enriched interaction data
4. THE Backfill_Scan SHALL produce stakeholder position summaries routed to memory.md relationship graph entries and relevant meeting series files in ~/shared/context/meetings/
5. THE stakeholder position summaries SHALL include specific examples of escalation triggers and de-escalation patterns with source attribution
6. THE Backfill_Scan SHALL respect gut.md word budgets when writing to memory.md — if at capacity, summaries SHALL be stored in intake/ for deferred processing

### Requirement 12: Pre-Meeting Context from Slack History

**User Story:** As Richard, I want the system to extract Slack activity around recurring meeting times, so that meeting series files have months of surrounding context beyond the 10 days of Hedy data.

#### Acceptance Criteria

1. WHEN a Pre-Meeting Context Backfill_Scan is triggered, THE Slack_Ingester SHALL search for Slack messages within 2 hours before and after each recurring meeting time for the past 6 months
2. THE Backfill_Scan SHALL cross-reference meeting times from Richard's calendar with Slack activity to identify pre-meeting prep discussions and post-meeting follow-ups
3. FOR EACH meeting series, THE Backfill_Scan SHALL extract: topics discussed in Slack before the meeting, action items discussed in Slack after the meeting, and threads that reference meeting topics
4. THE Backfill_Scan SHALL insert meeting-adjacent messages into the slack_messages table with metadata linking them to the relevant meeting series
5. THE Backfill_Scan SHALL produce per-meeting-series context summaries routed to the corresponding meeting series files in ~/shared/context/meetings/
6. THE Backfill_Scan SHALL identify action items that were discussed in Slack but never formalized in meeting notes, flagging them for review


### Requirement 13: Weekly Relationship Graph Refresh

**User Story:** As a system operator, I want the relationship graph to auto-refresh weekly from the conversation database, so that People Watch stays current without manual maintenance.

#### Acceptance Criteria

1. WHEN the Friday system refresh runs, THE Enrichment_Process SHALL query the Conversation_Database for interaction counts per person over the trailing 7 days
2. WHEN a person not currently in People_Watch has 3 or more interactions with Richard in the trailing 7 days, THE Enrichment_Process SHALL flag the person as a candidate for People_Watch promotion in slack-scan-state.json
3. WHEN a People_Watch contact has had zero interactions with Richard for 60 or more days, THE Enrichment_Process SHALL flag the contact for potential demotion to dormant status
4. THE Enrichment_Process SHALL update the slack_people table with refreshed interaction counts, last_interaction dates, and relationship_tier values
5. THE Enrichment_Process SHALL produce a brief relationship delta summary (new candidates, dormant contacts, tier changes) routed to memory.md if changes are detected
6. WHEN no relationship changes are detected, THE Enrichment_Process SHALL skip the memory.md update entirely

### Requirement 14: Monthly Synthesis Report

**User Story:** As Richard, I want a monthly synthesis of what changed in my Slack world, so that I can spot trends that daily scans miss.

#### Acceptance Criteria

1. WHEN a monthly synthesis is triggered (first system refresh of each month), THE Enrichment_Process SHALL query the Conversation_Database for the trailing 30 days
2. THE monthly synthesis SHALL cover: topic trends (rising, falling, new), new people who appeared in Richard's conversations, channel activity shifts, and relationship graph changes
3. THE monthly synthesis SHALL route strategic shifts to brain.md, relationship changes to memory.md, and market context shifts to eyes.md, respecting gut.md word budgets for each organ
4. THE monthly synthesis document SHALL not exceed 500 words total across all organ updates
5. WHEN the monthly synthesis identifies a topic that trended for 3 or more weeks, THE Enrichment_Process SHALL flag the topic as a potential wiki article candidate in wiki demand-log.md

### Requirement 15: Quarterly Stakeholder Communication Audit

**User Story:** As Richard, I want a quarterly audit of my communication patterns with key stakeholders, so that I can course-correct visibility gaps before the next review cycle.

#### Acceptance Criteria

1. WHEN a quarterly audit is triggered (aligned with QBR prep), THE Enrichment_Process SHALL query the Conversation_Database for per-stakeholder communication data over the trailing 90 days
2. FOR EACH key stakeholder, THE quarterly audit SHALL produce: message volume (sent and received), average response time, topics discussed, channel overlap, and communication frequency trend
3. THE quarterly audit SHALL compare current-quarter communication patterns against the previous quarter and flag significant changes (e.g., response time increased by more than 50%, message volume dropped by more than 30%)
4. THE quarterly audit SHALL route findings to nervous-system.md (Loop 9 data) and memory.md (relationship graph updates), respecting gut.md word budgets
5. THE quarterly audit SHALL highlight the visibility gap metric — quantifying how Richard's communication centrality compares to peers based on available data

### Requirement 16: Slack-to-Wiki Pipeline

**User Story:** As Richard, I want the system to identify Slack threads where I gave detailed explanations, so that my best Slack content becomes wiki article candidates without manual effort.

#### Acceptance Criteria

1. WHEN the weekly enrichment runs, THE Enrichment_Process SHALL query the Conversation_Database for threads where Richard authored messages with more than 200 characters, sent 3 or more replies, and used explanatory language patterns
2. FOR EACH identified thread, THE Enrichment_Process SHALL extract: the topic, Richard's explanation content, the audience (who asked, who participated), and the thread link
3. THE Enrichment_Process SHALL add identified threads to ~/shared/context/wiki/demand-log.md as wiki article candidates with source attribution and a one-sentence summary
4. THE Enrichment_Process SHALL not create duplicate entries in demand-log.md — threads already logged SHALL be skipped
5. WHEN a thread is identified as a wiki candidate, THE Enrichment_Process SHALL check if a wiki article on the same topic already exists and note the overlap in the demand-log entry

### Requirement 17: Proactive Draft Suggestions

**User Story:** As Richard, I want the system to auto-draft responses to unanswered Slack messages, so that responding becomes a 30-second review-and-send instead of a 10-minute composition.

#### Acceptance Criteria

1. WHEN the system detects an unanswered message directed at Richard in Slack (no reaction from Richard, no reply, 24 or more hours old), THE Enrichment_Process SHALL generate a draft response
2. THE draft response SHALL use memory.md relationship graph tone notes for the specific person and richard-style-slack.md (once created) for Slack-appropriate register
3. THE draft response SHALL incorporate thread context from the Conversation_Database to ensure the response addresses the actual question or request
4. THE Enrichment_Process SHALL post the draft response to RSW_Channel with clear labeling: "[DRAFT for @person in #channel]: [draft text]"
5. THE Enrichment_Process SHALL use create_draft via Slack_MCP when available, falling back to RSW_Channel posting if create_draft is not supported for the target channel
6. THE Enrichment_Process SHALL not generate drafts for messages that Richard has acknowledged via emoji reaction — a reaction IS a response per the reaction checking semantics in the channel registry


### Requirement 18: Backfill Data Routing to Existing Organs

**User Story:** As a system architect, I want all backfill data to route through existing Body organs and the conversation database, so that no new organ files are created and the system stays within its architectural constraints.

#### Acceptance Criteria

1. THE Body_System SHALL route all Backfill_Scan outputs to existing organs: relationship data to memory.md, decisions to brain.md, market/project data to eyes.md and current.md, meeting context to meeting series files, voice data to portable-body/voice/
2. THE Body_System SHALL not create new organ files in ~/shared/context/body/ for any Slack Deep Context feature
3. WHEN a Backfill_Scan produces output that exceeds an organ's word budget, THE Body_System SHALL store the excess in ~/shared/context/intake/ with a tag indicating the target organ and defer processing to the next compression cycle
4. THE Body_System SHALL insert all raw backfill messages into the Conversation_Database regardless of whether the synthesized output fits in organ word budgets — the database is the complete record, organs hold the compressed view
5. WHEN a Backfill_Scan updates an organ, THE Body_System SHALL include a [Slack Backfill: date range, scan type] attribution tag so the source of the data is traceable

### Requirement 19: Guardrail Compliance for Deep Context

**User Story:** As a system operator, I want all Slack Deep Context operations to comply with slack-guardrails.md, so that the system maintains read-only behavior on all channels except rsw-channel.

#### Acceptance Criteria

1. THE Slack_Ingester SHALL use only read operations (search, batch_get_conversation_history, batch_get_thread_replies, batch_get_channel_info, batch_get_user_info, reaction_tool, download_file_content, list_channels) for all Backfill_Scan and Enrichment_Process operations
2. THE Body_System SHALL use post_message only to RSW_Channel (C0993SRL6FQ) for Daily_Brief_Post, Live_Dashboard updates, intake acknowledgments, and draft suggestions
3. THE Body_System SHALL use create_draft for proactive draft suggestions targeting channels other than RSW_Channel
4. THE Body_System SHALL log all Slack MCP tool invocations during backfill and enrichment operations to slack-scan-state.json tool_invocation_log with timestamp, tool name, target, and result
5. IF a Backfill_Scan encounters rate limits from the Slack API, THEN THE Backfill_Scan SHALL pause, log the rate limit event, and resume after the rate limit window expires rather than failing the entire scan

### Requirement 20: Portability and Cold Start for Deep Context

**User Story:** As a system architect, I want the conversation database and all deep context outputs to be portable, so that a new AI on a different platform can access the full knowledge graph without Slack MCP access.

#### Acceptance Criteria

1. THE Conversation_Database SHALL reside in the existing ps-analytics.duckdb file, which is a single portable file requiring no server
2. THE Conversation_Database schema SHALL be documented in ~/shared/tools/data/schema.sql alongside all other table definitions
3. THE voice analysis document (richard-style-slack.md) SHALL be plain markdown readable by any AI without Slack access
4. WHEN the system cold-starts without Slack MCP access, THE Body_System SHALL query the Conversation_Database for historical context instead of making live Slack API calls
5. THE Conversation_Database SHALL support Parquet export via the existing db_export_parquet() function for backup and cross-platform portability
6. ALL Backfill_Scan synthesis documents routed to organs SHALL be self-contained plain text with source attribution — no Slack API calls required to understand the content

### Requirement 21: Canvas Technical Validation

**User Story:** As a system architect, I want to validate whether Slack MCP supports canvas operations before implementing the live dashboard, so that the implementation uses the best available mechanism.

#### Acceptance Criteria

1. BEFORE implementing the Live_Dashboard, THE Body_System SHALL test whether the Slack_MCP server supports canvas creation (creating a new canvas in RSW_Channel) and canvas update (modifying canvas content)
2. WHEN canvas operations are supported, THE Body_System SHALL implement the Live_Dashboard as a Canvas pinned to RSW_Channel
3. WHEN canvas operations are not supported, THE Body_System SHALL implement the Live_Dashboard as a Pinned_Message in RSW_Channel using message formatting (Slack mrkdwn) for structure
4. THE validation result SHALL be documented in the slack-ingestion-README.md so future development knows the canvas capability status
5. WHEN the fallback Pinned_Message approach is used, THE Body_System SHALL update the pinned message content by editing the existing message rather than posting new messages, to keep RSW_Channel uncluttered
