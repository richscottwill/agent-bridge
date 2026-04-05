# Requirements Document

## Introduction

This document specifies requirements for optimizing Richard's full MCP server ecosystem — 12 active servers that currently operate mostly in isolation. The opportunity is cross-MCP workflows: combining servers to create capabilities none can deliver alone, consolidating multi-step manual processes into single automated flows, and filling gaps in existing pipelines. This is not an AgentCore-only spec (that exists separately at `.kiro/specs/agentcore-system-integration/`). This covers the entire MCP surface area and how servers can be wired together to reduce Richard's manual steps, enrich the Body system's context, and advance all Five Levels.

Current state: The Body uses 6 MCPs heavily (Asana, Slack, Outlook, DuckDB, SharePoint, Hedy) in the AM/EOD hook chains. The remaining 6 (Builder, XWiki, Knowledge Discovery, ARCC, AgentCore, Weblab) are connected but underutilized. Cross-MCP workflows exist only in the morning routine (Slack + Asana + Outlook → intake) and WBR pipeline (SharePoint + DuckDB → callouts). Most other processes are single-MCP or manual.

## Glossary

- **MCP_Ecosystem**: The full set of 12 active MCP servers connected to Richard's Kiro workspace, each exposing tools for a specific domain
- **Cross_MCP_Workflow**: An automated process that chains tools from two or more MCP servers to produce an output that no single server could deliver alone
- **Body_System**: Richard's 11-organ context management architecture (`~/shared/context/body/`)
- **Morning_Routine**: The AM-1 → AM-2 → AM-3 sequential hook chain for daily ingestion, triage, and briefing
- **EOD_Routine**: The EOD-1 → EOD-2 sequential hook chain for meeting sync and system refresh
- **WBR_Pipeline**: The Monday WBR callout pipeline — polls SharePoint for new dashboard, ingests to DuckDB, runs 10-market callout generation
- **Wiki_Pipeline**: The 6-agent document pipeline (editor → researcher → writer → critic → librarian + concierge) that publishes to `~/shared/artifacts/`
- **Karpathy_Loop**: The autoresearch experiment loop that runs during EOD-2, applying and evaluating changes to body organs and style guides
- **Signal**: An actionable piece of information extracted from Slack, email, Asana, or meetings that requires routing to a task, reply, or context update
- **DuckDB_Analytics**: The PS Analytics database (`ps-analytics.duckdb`) storing market metrics, Slack messages, experiments, and structured operational data
- **Agent_Bridge**: The Google Sheets/Docs async message bus for cross-platform context sharing
- **Five_Levels**: Richard's sequential north star framework (L1: Sharpen Yourself → L2: Drive WW Testing → L3: Team Automation → L4: Zero-Click Future → L5: Agentic Orchestration)
- **Builder_MCP**: Internal tool access server — phonetool, code.amazon, wiki, Quip, Taskei, ticketing
- **XWiki_MCP**: Read/write access to w.amazon.com wiki pages
- **KDS_MCP**: Knowledge Discovery Service — queries internal knowledge bases
- **ARCC_MCP**: Curated context search for security/compliance and organizational knowledge
- **AgentCore_MCP**: AWS Bedrock AgentCore — cloud browser, code interpreter, runtime, memory, gateway
- **Hedy_MCP**: Meeting transcripts, session details, highlights, todos from Hedy bot
- **Quip_Document**: Amazon's collaborative document platform, accessible via Builder_MCP

## Requirements

### Requirement 1: Meeting-to-Action-Item Automation (Hedy + Asana + Slack)

**User Story:** As Richard, I want meeting action items to automatically become Asana tasks with Slack notifications, so that nothing falls through the cracks between a meeting ending and the next morning routine.

#### Acceptance Criteria

1. WHEN EOD-1 ingests a Hedy session containing action items assigned to Richard, THE Body_System SHALL create corresponding Asana tasks with the meeting name as context, the action item as the task description, and a due date derived from the meeting discussion
2. WHEN EOD-1 creates an Asana task from a Hedy action item, THE Body_System SHALL post a summary to Richard's Slack DM listing all new tasks created from that meeting session
3. WHEN a Hedy action item references another person (not Richard), THE Body_System SHALL log the item to `hands.md` as a dependency with the person's name and the originating meeting, without creating an Asana task
4. IF a Hedy action item duplicates an existing Asana task (matching description within the same project), THEN THE Body_System SHALL add a comment to the existing task referencing the meeting instead of creating a duplicate
5. WHEN a Hedy session contains no action items for Richard, THE Body_System SHALL skip task creation for that session and log the session as "no actions" in the meeting series file

### Requirement 2: WBR Pipeline Consolidation (SharePoint + DuckDB + Slack + Builder)

**User Story:** As Richard, I want the WBR callout pipeline to post finished callouts directly to the Pre-WBR Callouts Quip document and notify the team on Slack, so that the current manual copy-paste step is eliminated.

#### Acceptance Criteria

1. WHEN the WBR callout pipeline completes callout generation for all 10 markets, THE WBR_Pipeline SHALL write the formatted callouts to the Pre-WBR Callouts Quip document via Builder_MCP
2. WHEN the WBR_Pipeline writes callouts to Quip, THE WBR_Pipeline SHALL post a notification to Richard's Slack DM (self_dm) or rsw-channel with a summary of markets covered, key callouts, and a link to the Quip document
3. WHILE the WBR callout pipeline is running, THE WBR_Pipeline SHALL log each market's callout status (generated, skipped, error) to DuckDB_Analytics for pipeline reliability tracking
4. IF the Quip write fails, THEN THE WBR_Pipeline SHALL fall back to saving callouts as local markdown files and notify Richard via Slack DM with the failure reason and file locations
5. WHEN the WBR_Pipeline posts to Slack, THE WBR_Pipeline SHALL include a one-line summary per market highlighting the most significant WoW change (regs or spend)

### Requirement 3: Knowledge-Enriched Wiki Publishing (KDS + ARCC + XWiki + Wiki_Pipeline)

**User Story:** As Richard, I want wiki articles to be enriched with internal knowledge base content and published to w.amazon.com in addition to SharePoint, so that articles reach a wider audience and contain deeper organizational context.

#### Acceptance Criteria

1. WHEN the Wiki_Pipeline researcher agent gathers context for an article, THE Wiki_Pipeline SHALL query KDS_MCP for relevant internal knowledge and include sourced findings in the research brief
2. WHEN the Wiki_Pipeline researcher agent gathers context for an article, THE Wiki_Pipeline SHALL query ARCC_MCP for curated organizational context relevant to the article topic
3. WHEN the Wiki_Pipeline librarian publishes a FINAL-status article, THE Wiki_Pipeline SHALL publish the article to w.amazon.com via XWiki_MCP in addition to the existing SharePoint sync
4. WHEN the Wiki_Pipeline publishes to XWiki, THE Wiki_Pipeline SHALL format the article according to w.amazon.com wiki markup conventions, including proper category tags and cross-references
5. IF the XWiki publish fails, THEN THE Wiki_Pipeline SHALL log the failure, retain the SharePoint copy as the primary publication, and flag the article for manual XWiki publishing in the next EOD-2 run
6. THE Wiki_Pipeline SHALL maintain a publication registry in DuckDB_Analytics tracking each article's publication status across SharePoint and XWiki (published, pending, failed)

### Requirement 4: Cross-MCP Signal-to-Task Pipeline (Email + Slack + Asana + DuckDB)

**User Story:** As Richard, I want high-priority email and Slack signals to automatically create Asana tasks with full context, so that the AM-2 triage step produces actionable tasks without manual signal-to-task conversion.

#### Acceptance Criteria

1. WHEN AM-1 identifies a high-priority email signal (direct request from Brandon, Kate, or skip-level stakeholders), THE Morning_Routine SHALL create an Asana task in the appropriate bucket (Sweep, Core, Engine Room, Admin) with the email subject, sender, key excerpt, and a suggested due date
2. WHEN AM-1 identifies a high-priority Slack signal (direct mention, DM, or thread reply requiring action), THE Morning_Routine SHALL create an Asana task with the Slack message link, channel name, author, and action required
3. WHEN the Morning_Routine creates a task from a signal, THE Morning_Routine SHALL log the signal-to-task mapping in DuckDB_Analytics (signal_source, signal_id, task_gid, created_at, priority) for signal volume and response time analysis
4. IF a signal matches an existing open Asana task (same sender + similar subject within 7 days), THEN THE Morning_Routine SHALL add the new signal as a comment on the existing task instead of creating a duplicate
5. WHEN AM-2 completes triage, THE Morning_Routine SHALL post a triage summary to Richard's Slack DM listing new tasks created, existing tasks updated, and signals deferred to backlog

### Requirement 5: AgentCore Browser for Internal Tool Access (AgentCore + DuckDB)

**User Story:** As Richard, I want the AgentCore cloud browser to access internal tools requiring Midway authentication (WorkDocs, Google Ads UI, Adobe AMO), so that data currently requiring manual browser interaction can be ingested programmatically.

#### Acceptance Criteria

1. WHEN the WBR_Pipeline needs the WW Dashboard xlsx, THE AgentCore_MCP Browser_Service SHALL navigate to WorkDocs, authenticate via Midway, and download the file to the ingestion input directory
2. WHEN the AgentCore Browser downloads a file from an internal tool, THE Body_System SHALL validate the file (non-zero size, expected format) before passing it to downstream processing
3. IF the AgentCore Browser fails to authenticate or download, THEN THE Body_System SHALL fall back to the current SharePoint polling mechanism and notify Richard via Slack DM
4. WHEN the AgentCore Browser accesses an internal tool, THE Body_System SHALL log the access event (tool_name, url, timestamp, success/failure, file_size) to DuckDB_Analytics for reliability tracking
5. WHERE AgentCore Browser access is configured for Google Ads UI, THE Body_System SHALL extract campaign performance snapshots and store them in DuckDB_Analytics for trend analysis without requiring Richard to manually export reports

### Requirement 6: Sandboxed Data Analysis (AgentCore Code Interpreter + DuckDB)

**User Story:** As Richard, I want data analysis scripts to run in AgentCore's sandboxed code interpreter instead of directly on DevSpaces, so that experimental analysis cannot affect the production workspace.

#### Acceptance Criteria

1. WHEN a data analysis task requires Python execution against DuckDB_Analytics data, THE Body_System SHALL export the relevant data subset as Parquet and execute the analysis in AgentCore Code_Interpreter_Service
2. WHEN the Code_Interpreter_Service completes an analysis, THE Body_System SHALL return results (tables, charts, summaries) to the requesting workflow and log execution metadata (runtime, data_size, script_hash) to DuckDB_Analytics
3. IF the Code_Interpreter_Service execution fails or times out, THEN THE Body_System SHALL fall back to local Python execution on DevSpaces and log the failure reason
4. THE Body_System SHALL use the Code_Interpreter_Service for all Karpathy_Loop data experiments that involve statistical analysis or model fitting, keeping the production DuckDB database read-only during experiments
5. WHEN the Code_Interpreter_Service produces a visualization, THE Body_System SHALL save the output to `~/shared/research/` with a descriptive filename and timestamp

### Requirement 7: Meeting Data Analytics Pipeline (Hedy + DuckDB + Slack)

**User Story:** As Richard, I want Hedy meeting data stored in DuckDB for communication pattern analysis over time, so that the nervous system's Loop 9 (Meeting Communication) has queryable historical data instead of relying on file-based snapshots.

#### Acceptance Criteria

1. WHEN EOD-1 processes a Hedy session, THE Body_System SHALL insert a structured record into DuckDB_Analytics containing session_id, meeting_name, date, duration_minutes, richard_speaking_share, total_participants, action_item_count, and hedging_count
2. WHEN the DuckDB_Analytics meeting table accumulates 4 or more weeks of data, THE Body_System SHALL compute weekly communication trend metrics (average speaking share by meeting type, hedging trend, action item generation rate) during EOD-2
3. WHILE the nervous system Loop 9 evaluates communication patterns, THE Body_System SHALL query DuckDB_Analytics for the trailing 4-week trend instead of parsing meeting series files
4. WHEN a weekly communication trend shows Richard's group meeting speaking share below 15% for 3 consecutive weeks, THE Body_System SHALL flag the pattern in the EOD-2 Slack DM summary as a coaching signal
5. THE Body_System SHALL store Hedy session highlights and key quotes in DuckDB_Analytics for full-text search, enabling retrieval of past meeting context by topic or participant

### Requirement 8: Automated Context Enrichment (KDS + ARCC + DuckDB)

**User Story:** As Richard, I want the Body system's context files to be automatically enriched with relevant internal knowledge, so that organs contain organizational context without Richard manually searching knowledge bases.

#### Acceptance Criteria

1. WHEN EOD-2 runs the maintenance cascade, THE Body_System SHALL query KDS_MCP for recent knowledge relevant to Richard's active projects (from `current.md`) and save new findings to `~/shared/context/intake/` for processing
2. WHEN the Body_System identifies a new finding from KDS_MCP, THE Body_System SHALL check for relevance against the active project list and discard findings with no clear connection to current work
3. WHEN EOD-2 processes intake files containing KDS findings, THE Body_System SHALL route relevant findings to the appropriate organ (brain.md for strategic insights, eyes.md for market data, memory.md for relationship context)
4. THE Body_System SHALL track all KDS and ARCC queries in DuckDB_Analytics (query_text, source, result_count, relevance_score, routed_to) to measure enrichment value over time
5. IF KDS or ARCC returns no relevant results for 3 consecutive EOD-2 runs, THEN THE Body_System SHALL adjust query terms based on changes in `current.md` active projects and log the query refinement

### Requirement 9: Builder MCP Quip Integration for Recurring Documents (Builder + DuckDB)

**User Story:** As Richard, I want the system to read from and write to Quip documents via Builder MCP, so that recurring documents (WBR callouts, meeting notes, status updates) can be auto-populated without manual copy-paste.

#### Acceptance Criteria

1. WHEN the WBR callout pipeline completes, THE Body_System SHALL write the formatted callouts to the Pre-WBR Callouts Quip document using Builder_MCP's Quip access tools
2. WHEN the Body_System writes to a Quip document, THE Body_System SHALL preserve existing content structure and append new content in the appropriate section rather than overwriting the entire document
3. THE Body_System SHALL maintain a Quip document registry in DuckDB_Analytics mapping document names to Quip IDs, last_updated timestamps, and update frequency
4. IF a Quip write operation fails, THEN THE Body_System SHALL retry once after 30 seconds, and if the retry fails, save the content locally and notify Richard via Slack DM
5. WHEN the Body_System reads a Quip document for context (e.g., reading the change log or team status), THE Body_System SHALL cache the content locally with a staleness threshold of 4 hours to avoid redundant API calls

### Requirement 10: XWiki as Secondary Publishing Channel (XWiki + SharePoint + Wiki_Pipeline)

**User Story:** As Richard, I want wiki articles published to both SharePoint and w.amazon.com, so that articles reach the broader Amazon audience on w.amazon.com while maintaining the existing SharePoint archive.

#### Acceptance Criteria

1. WHEN the SharePoint sync hook runs for FINAL-status articles, THE Body_System SHALL also publish each article to w.amazon.com via XWiki_MCP
2. WHEN the Body_System publishes to XWiki, THE Body_System SHALL convert the article from markdown to XWiki markup format, preserving headings, lists, tables, and inline formatting
3. THE Body_System SHALL maintain a dual-publication status tracker in DuckDB_Analytics recording each article's SharePoint URL, XWiki page ID, and sync status (in_sync, sharepoint_only, xwiki_only, diverged)
4. IF an article is updated on SharePoint after initial XWiki publication, THEN THE Body_System SHALL detect the divergence during the next sync run and update the XWiki version to match
5. WHEN the Body_System publishes to XWiki for the first time, THE Body_System SHALL create the page under a consistent namespace (e.g., `PaidSearch/[ArticleTitle]`) with category tags matching the article's artifact category from `~/shared/artifacts/index.md`

### Requirement 11: Cross-MCP Workflow Observability (DuckDB + Slack)

**User Story:** As Richard, I want all cross-MCP workflows to log execution data to DuckDB and surface failures via Slack, so that pipeline reliability is measurable and failures are immediately visible.

#### Acceptance Criteria

1. WHEN any cross-MCP workflow begins execution, THE Body_System SHALL log a start event to DuckDB_Analytics (workflow_name, start_time, trigger_source, mcp_servers_involved)
2. WHEN any cross-MCP workflow completes, THE Body_System SHALL log a completion event to DuckDB_Analytics (workflow_name, end_time, status, steps_completed, steps_failed, duration_seconds)
3. IF any cross-MCP workflow step fails, THEN THE Body_System SHALL log the failure details (step_name, mcp_server, error_message, retry_count) and continue executing remaining independent steps
4. WHEN EOD-2 runs, THE Body_System SHALL query DuckDB_Analytics for the day's workflow execution summary and include it in the system refresh report (total runs, success rate, average duration, failures)
5. IF a cross-MCP workflow's success rate drops below 80% over a 7-day window, THEN THE Body_System SHALL flag the workflow in the EOD-2 Slack DM as degraded and include the most common failure reason

### Requirement 12: Slack-to-DuckDB Conversation Intelligence (Slack + DuckDB + KDS)

**User Story:** As Richard, I want Slack conversations enriched with internal knowledge context and stored in DuckDB, so that the system can surface relevant past discussions and organizational knowledge when processing new signals.

#### Acceptance Criteria

1. WHEN AM-1 ingests Slack messages, THE Body_System SHALL store structured message records in DuckDB_Analytics with channel_name, author, timestamp, message_text, thread_id, and signal_priority
2. WHEN a Slack message references an internal tool, project, or acronym, THE Body_System SHALL query KDS_MCP for context and attach a knowledge_context field to the DuckDB record
3. WHEN AM-2 triages a signal, THE Body_System SHALL query DuckDB_Analytics for related past Slack messages (same author + similar topic within 30 days) and include the conversation history in the triage context
4. THE Body_System SHALL maintain a full-text search index on the Slack messages table in DuckDB_Analytics using the existing FTS extension, enabling BM25-ranked retrieval by topic, author, or channel
5. WHEN Richard asks about a past conversation or decision, THE Body_System SHALL query both DuckDB_Analytics (Slack messages) and KDS_MCP (organizational knowledge) to provide a comprehensive answer with source attribution
