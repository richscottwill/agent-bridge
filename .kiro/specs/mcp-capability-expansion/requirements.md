# Requirements Document

## Introduction

This document specifies requirements for expanding the capabilities of Richard's 12-MCP server ecosystem through cross-server synergies, process consolidation, and new automation patterns. The existing `mcp-integration-optimization` spec covers individual cross-MCP workflow wiring (meeting-to-task, signal-to-task, wiki enrichment). This spec operates at a higher level: identifying capability categories that emerge when MCPs are combined, collapsing multi-step manual processes into single automated flows, expanding data pipelines, building team-facing tools (Level 3), and establishing proactive monitoring. Each requirement maps to the Five Levels framework.

The spec is organized into three tiers:
- **Tier 1 (Now):** Achievable with current MCP setup, no new dependencies
- **Tier 2 (Soon):** Requires minor configuration or wiring but no new infrastructure
- **Tier 3 (AgentCore):** Requires internal AWS account for AgentCore resource provisioning

Current state: 6 MCPs are heavily used (Asana, Slack, Outlook, DuckDB, SharePoint, Hedy) in AM/EOD hooks and the WBR pipeline. 6 MCPs are connected but underutilized (Builder, XWiki, Knowledge Discovery, ARCC, Weblab, AgentCore). Cross-MCP workflows exist only in the morning routine and WBR pipeline. Most processes are single-MCP or manual.

Related specs:
- `.kiro/specs/mcp-integration-optimization/` — granular cross-MCP workflow wiring
- `.kiro/specs/agentcore-system-integration/` — AgentCore service-level integration
- `.kiro/specs/kiro-setup-optimization/` — steering, hooks, and skills configuration

## Glossary

- **MCP_Ecosystem**: The 12 active MCP servers in Richard's Kiro workspace, each exposing domain-specific tools
- **Cross_MCP_Synergy**: A capability that emerges only when two or more MCP servers are combined — impossible with any single server alone
- **Process_Consolidation**: Collapsing a multi-step manual workflow into a single automated flow using MCP combinations
- **Body_System**: Richard's 11-organ context management architecture in `~/shared/context/body/`
- **Five_Levels**: Sequential north star (L1: Sharpen → L2: Testing → L3: Team Automation → L4: Zero-Click → L5: Agentic Orchestration)
- **Morning_Routine**: AM-1 → AM-2 → AM-3 hook chain for daily ingestion, triage, and briefing
- **EOD_Routine**: EOD-1 → EOD-2 hook chain for meeting sync and system refresh
- **WBR_Pipeline**: Monday pipeline — SharePoint poll → DuckDB ingest → 10-market callout generation
- **Wiki_Pipeline**: 6-agent document pipeline (editor → researcher → writer → critic → librarian + concierge)
- **Karpathy_Loop**: Autoresearch experiment loop running during EOD-2
- **DuckDB_Analytics**: PS Analytics database (`ps-analytics.duckdb`) — market metrics, Slack messages, experiments, structured operational data
- **Signal_Router**: The nervous system component that classifies and routes signals from Slack, email, Asana, and meetings to appropriate organs
- **Builder_MCP**: Internal tool access — phonetool, code.amazon, wiki, Quip, Taskei, ticketing
- **XWiki_MCP**: Read/write access to w.amazon.com wiki pages
- **KDS_MCP**: Knowledge Discovery Service — internal knowledge base queries
- **ARCC_MCP**: Curated context search for governance, security, and organizational knowledge
- **AgentCore_MCP**: AWS Bedrock AgentCore — cloud browser, code interpreter, runtime, memory, gateway
- **Hedy_MCP**: Meeting transcripts, session details, highlights, todos
- **Weblab_MCP**: Weblab experiment management
- **Agent_Bridge**: Google Sheets/Docs async message bus for cross-platform context sharing
- **Team_Tool**: A tool, dashboard, or automated output that a non-technical teammate can use directly without agent interaction (Level 3)
- **Proactive_Monitor**: An automated check that detects issues (budget overruns, stale tasks, missed deadlines, competitor changes) before Richard discovers them manually
- **Unified_Inbox**: A consolidated view of actionable signals across Slack, email, Asana notifications, and meeting action items

## Requirements

### Requirement 1: Unified Signal Inbox Across All Communication Channels (Tier 1 — L1/L2)

**User Story:** As Richard, I want all actionable signals from Slack, email, Asana notifications, and meeting action items consolidated into a single prioritized queue in DuckDB, so that AM-2 triage operates on one unified stream instead of processing each source separately.

#### Acceptance Criteria

1. WHEN AM-1 completes ingestion from Slack (via Slack MCP), email (via Outlook MCP), Asana notifications (via Enterprise Asana MCP), and meeting action items (via Hedy MCP), THE Signal_Router SHALL insert each signal into a `unified_signals` table in DuckDB_Analytics with fields: signal_id, source_mcp, source_id, author, timestamp, content_preview, signal_type (request, FYI, blocker, decision, action_item), and raw_priority
2. WHEN AM-2 begins triage, THE Morning_Routine SHALL query the `unified_signals` table ordered by computed priority (stakeholder rank × signal_type weight × recency) instead of processing each source sequentially
3. WHEN a signal from one source references the same topic as a signal from another source (same author + overlapping keywords within 48 hours), THE Signal_Router SHALL link the signals in DuckDB_Analytics as a signal_cluster with a shared cluster_id
4. WHEN AM-2 completes triage, THE Morning_Routine SHALL update each signal record in DuckDB_Analytics with disposition (task_created, task_updated, deferred, dismissed) and the associated Asana task_gid if applicable
5. IF a signal source (Slack, Outlook, Hedy, or Asana) is unreachable during AM-1, THEN THE Signal_Router SHALL log the failure, process available sources, and flag the missing source in the AM-3 daily brief

### Requirement 2: End-to-End Meeting Intelligence Pipeline (Tier 1 — L1/L5)

**User Story:** As Richard, I want meeting transcripts from Hedy to flow through context enrichment, action item extraction, Asana task creation, Slack follow-up, and DuckDB analytics in a single automated pipeline, so that the current 4-step manual process (read transcript → extract actions → create tasks → message people) becomes zero-click.

#### Acceptance Criteria

1. WHEN EOD-1 processes a Hedy session, THE Body_System SHALL query Slack MCP for any thread context related to the meeting topic (matching channel + keywords from the meeting agenda) and attach the Slack context to the meeting record
2. WHEN the Body_System extracts action items from a Hedy session, THE Body_System SHALL cross-reference each action item against open Asana tasks (via Enterprise Asana MCP) to detect duplicates before creating new tasks
3. WHEN the Body_System creates an Asana task from a meeting action item, THE Body_System SHALL post a threaded reply in the relevant Slack channel (via Slack MCP) linking the new task and tagging the assignee
4. WHEN EOD-1 completes meeting processing, THE Body_System SHALL insert structured meeting analytics into DuckDB_Analytics (session_id, duration, participant_count, action_item_count, richard_speaking_share, topics_discussed) for Loop 9 trend analysis
5. WHEN a meeting involves a decision that maps to an active project in `current.md`, THE Body_System SHALL update the relevant organ (brain.md for decisions, eyes.md for data points, memory.md for relationship signals) via the standard intake routing

### Requirement 3: Automated Stakeholder Communication Drafting (Tier 1 — L1/L3)

**User Story:** As Richard, I want the system to auto-draft Slack messages and email replies based on Asana task context and meeting history, so that the AM-2 triage step produces ready-to-send drafts instead of just task descriptions.

#### Acceptance Criteria

1. WHEN AM-2 identifies an Asana task requiring a stakeholder update (due date approaching, blocker resolved, or status change), THE Morning_Routine SHALL draft a Slack message or email reply using context from the task description (Asana MCP), recent meeting discussions about the topic (Hedy MCP), and the stakeholder's communication preferences (memory.md)
2. WHEN the Morning_Routine drafts a communication, THE Morning_Routine SHALL save the draft to `~/shared/context/intake/drafts/` with metadata (recipient, channel, urgency, source_task_gid) for Richard's review
3. WHEN Richard approves a draft, THE Body_System SHALL send the message via the appropriate MCP (Slack MCP for Slack messages, Outlook MCP for emails) and log the send event in DuckDB_Analytics
4. IF a draft references data that has changed since the draft was generated (task completed, new meeting occurred), THEN THE Body_System SHALL flag the draft as stale and regenerate it with current context
5. THE Morning_Routine SHALL generate drafts only for communications where the recipient is in Richard's direct stakeholder list (Brandon, Kate, Lena, Lorena, Andrew, Stacey, Adi, Dwayne) — not for unknown or external recipients

### Requirement 4: WBR Pipeline Full Automation with Quip Publishing (Tier 1 — L2/L5)

**User Story:** As Richard, I want the WBR callout pipeline to run end-to-end from dashboard detection through callout generation to Quip publishing and Slack notification, so that the Monday WBR process requires zero manual steps after Richard downloads the dashboard file.

#### Acceptance Criteria

1. WHEN the WBR watcher detects a new dashboard file on SharePoint (via SharePoint MCP), THE WBR_Pipeline SHALL ingest the data to DuckDB_Analytics, run the 10-market callout pipeline, and write formatted callouts to the Pre-WBR Callouts Quip document (via Builder MCP)
2. WHEN the WBR_Pipeline writes callouts to Quip, THE WBR_Pipeline SHALL preserve the existing Quip document structure and append the new week's callouts in the appropriate section with a week number header
3. WHEN the WBR_Pipeline completes Quip publishing, THE WBR_Pipeline SHALL post a summary to the designated Slack channel (via Slack MCP) with market highlights and a link to the Quip document
4. WHILE the WBR_Pipeline executes, THE WBR_Pipeline SHALL log each step's status (dashboard_detected, data_ingested, callouts_generated, quip_published, slack_notified) with timestamps to DuckDB_Analytics for pipeline reliability tracking
5. IF any step in the WBR_Pipeline fails, THEN THE WBR_Pipeline SHALL continue executing independent downstream steps, save partial results locally, and notify Richard via Slack DM with the failure point and recovery instructions
6. WHEN the WBR_Pipeline ingests change log data from Google Sheets (via Agent Bridge), THE WBR_Pipeline SHALL cross-reference change log entries against the dashboard data in DuckDB to surface changes that explain WoW metric movements in the callouts

### Requirement 5: Automated Data Freshness Monitoring and Alerting (Tier 1 — L2/L5)

**User Story:** As Richard, I want the system to proactively detect stale data across all sources (DuckDB tables, market context files, SharePoint documents, Asana tasks) and alert via Slack before staleness causes downstream errors, so that data quality issues are caught before they affect callouts, briefs, or decisions.

#### Acceptance Criteria

1. WHEN EOD-2 runs, THE Body_System SHALL query DuckDB_Analytics for the last ingest timestamp of each data source (daily_metrics, weekly_metrics, change_log, slack_messages, callout_scores) and flag any source where the last ingest exceeds its expected freshness window (daily sources > 36 hours, weekly sources > 8 days)
2. WHEN EOD-2 runs, THE Body_System SHALL check modification dates of all 10 market context files in `~/shared/context/active/callouts/` (via filesystem) and flag any file older than 14 days as stale
3. WHEN EOD-2 runs, THE Body_System SHALL query SharePoint MCP for the last modified date of key shared documents (WBR dashboard, change log) and flag documents that have not been updated within their expected cadence
4. WHEN the Body_System detects stale data, THE Body_System SHALL post a freshness report to Richard's Slack DM (via Slack MCP) listing each stale source, days since last update, expected cadence, and the downstream workflows affected
5. WHEN the Body_System detects that a data source feeding the WBR_Pipeline is stale on a Monday, THE Body_System SHALL include a warning in the WBR watcher's Slack notification indicating which callout markets may have incomplete data

### Requirement 6: Knowledge Base Auto-Maintenance Pipeline (Tier 2 — L3/L5)

**User Story:** As Richard, I want the wiki pipeline enriched with Knowledge Discovery and ARCC context, published to both SharePoint and XWiki, and monitored for staleness, so that the knowledge base stays current and reaches the widest internal audience without manual maintenance.

#### Acceptance Criteria

1. WHEN the Wiki_Pipeline researcher agent gathers context for an article, THE Wiki_Pipeline SHALL query KDS_MCP for relevant internal knowledge and ARCC_MCP for governance and organizational context, including sourced findings in the research brief
2. WHEN the Wiki_Pipeline librarian publishes a FINAL-status article, THE Wiki_Pipeline SHALL publish to w.amazon.com via XWiki_MCP in addition to the existing SharePoint sync, converting markdown to XWiki markup format
3. WHEN the weekly wiki_lint task runs during EOD-2, THE Body_System SHALL query KDS_MCP for recent organizational changes relevant to existing articles and flag articles whose content contradicts or is superseded by new knowledge
4. WHEN the wiki_lint task identifies a stale article with active Slack discussion (signal_tracker recent_mentions > 3 AND article updated > 14 days), THE Body_System SHALL create an Asana task (via Enterprise Asana MCP) in the Backlog bucket for article refresh with the Slack discussion links as context
5. THE Body_System SHALL maintain a publication registry in DuckDB_Analytics tracking each article's status across three channels (local markdown, SharePoint, XWiki) with last_published timestamps and sync status (in_sync, diverged, pending)
6. IF an XWiki or SharePoint publish fails, THEN THE Body_System SHALL retain the local markdown as the source of truth, log the failure to DuckDB_Analytics, and retry on the next sync run

### Requirement 7: Team-Facing Automated Reports via SharePoint (Tier 2 — L3)

**User Story:** As Richard, I want automated weekly and monthly reports generated from DuckDB data and published to a shared SharePoint folder, so that teammates (Brandon, Stacey, Adi, Dwayne) can access current performance data without asking Richard or running queries.

#### Acceptance Criteria

1. WHEN the weekly WBR callout pipeline completes, THE Body_System SHALL generate a formatted HTML report summarizing all 10 markets' key metrics (regs, spend, CPA, WoW changes) from DuckDB_Analytics and upload the report to a designated SharePoint folder (via SharePoint MCP)
2. WHEN the first business day of each month occurs, THE Body_System SHALL generate a monthly performance summary from DuckDB_Analytics (monthly_metrics table) covering all managed markets and upload the report to SharePoint
3. WHEN the Body_System uploads a report to SharePoint, THE Body_System SHALL post a notification to the team Slack channel (via Slack MCP) with a link to the SharePoint report and a one-line summary of the most significant finding
4. THE Body_System SHALL generate reports using the Eyes Chart agent's HTML generation capability (Chart.js), producing self-contained HTML files that render without external dependencies
5. IF the SharePoint upload fails, THEN THE Body_System SHALL save the report locally to `~/shared/artifacts/reports/` and notify Richard via Slack DM with the file path and failure reason

### Requirement 8: Proactive Budget and Task Health Monitoring (Tier 1 — L1/L2)

**User Story:** As Richard, I want the system to proactively detect budget overruns, stale Asana tasks, missed deadlines, and anomalous metric movements across all managed markets, so that issues are surfaced before they become problems requiring escalation.

#### Acceptance Criteria

1. WHEN AM-1 runs, THE Morning_Routine SHALL query DuckDB_Analytics for the latest daily spend data across AU and MX and flag any market where daily spend exceeds 120% of the daily budget target or where cumulative monthly spend is pacing above 105% of the monthly budget
2. WHEN AM-1 runs, THE Morning_Routine SHALL query Enterprise Asana MCP for tasks assigned to Richard that are overdue by more than 7 days and have no Kiro_RW update in the last 5 days, flagging these as "abandoned overdue" in the daily brief
3. WHEN the WBR_Pipeline ingests new weekly data, THE Body_System SHALL run anomaly detection on DuckDB_Analytics comparing the current week against the trailing 4-week average for each market's regs and spend, flagging any market with a WoW change exceeding 15%
4. WHEN the Body_System detects a budget overrun or metric anomaly, THE Body_System SHALL check Slack MCP for recent messages in the relevant market channel that might explain the change (campaign launches, bid changes, competitor activity) and include the context in the alert
5. WHEN the Body_System detects 3 or more overdue tasks in the same Asana project, THE Body_System SHALL flag the project as "at risk" in the AM-3 daily brief and suggest a triage block in the calendar (via Outlook MCP)

### Requirement 9: Cross-Channel Relationship Intelligence (Tier 2 — L1/L3)

**User Story:** As Richard, I want the system to build and maintain a relationship activity graph by combining Slack interactions, email exchanges, meeting co-attendance, and Asana task collaboration data, so that memory.md's relationship context is data-driven rather than manually maintained.

#### Acceptance Criteria

1. WHEN EOD-2 runs the maintenance cascade, THE Body_System SHALL query DuckDB_Analytics (Slack messages), Outlook MCP (recent emails), Hedy MCP (meeting participants), and Enterprise Asana MCP (task collaborators) to compute a weekly interaction score for each person in Richard's stakeholder network
2. WHEN the Body_System computes interaction scores, THE Body_System SHALL store the results in a `relationship_activity` table in DuckDB_Analytics with fields: person_name, person_alias, week, slack_interactions, email_exchanges, meetings_shared, asana_collaborations, total_score
3. WHEN a person's interaction score drops to zero for 3 consecutive weeks after being active (score > 5) for the prior 4 weeks, THE Body_System SHALL flag the relationship as "cooling" in the EOD-2 summary and suggest a check-in
4. WHEN a person's interaction score spikes (3x their trailing 4-week average), THE Body_System SHALL flag the relationship as "intensifying" and check if there are unresolved Asana tasks or pending email replies involving that person
5. THE Body_System SHALL update memory.md's relationship entries with last_interaction_date and interaction_trend (active, cooling, intensifying, dormant) derived from the DuckDB_Analytics data, replacing manual relationship tracking

### Requirement 10: Competitive Intelligence Automation (Tier 2 — L2/L4)

**User Story:** As Richard, I want the system to automatically gather competitive intelligence from Slack discussions, Knowledge Discovery, and DuckDB market data, so that competitive context is available for WBR callouts and strategic decisions without manual research.

#### Acceptance Criteria

1. WHEN AM-1 scans Slack channels, THE Signal_Router SHALL identify messages mentioning competitor names (Walmart, Staples, Grainger, Uline, and configured competitor list) and tag them as competitive_signal in DuckDB_Analytics
2. WHEN the WBR_Pipeline generates callouts, THE WBR_Pipeline SHALL query DuckDB_Analytics for competitive_signals from the past 7 days and KDS_MCP for recent competitive intelligence, including relevant findings in the market callout context
3. WHEN DuckDB_Analytics contains competitor impression share data (from the competitors table), THE Body_System SHALL compute weekly trend changes and flag any market where a competitor's impression share increased by more than 5 percentage points WoW
4. WHEN the Body_System detects a significant competitive shift, THE Body_System SHALL post an alert to Richard's Slack DM with the competitor name, market, metric change, and any correlated Slack discussion threads
5. THE Body_System SHALL maintain a `competitive_signals` view in DuckDB_Analytics aggregating Slack mentions, impression share changes, and KDS findings by competitor and market, queryable for ad-hoc competitive analysis

### Requirement 11: Automated Recurring Task Lifecycle Management (Tier 1 — L1/L5)

**User Story:** As Richard, I want the system to fully manage the lifecycle of recurring Asana tasks — detecting completion, creating next instances, verifying cadence compliance, and alerting on missed recurrences — so that the EOD-2 recurring task check requires no manual intervention.

#### Acceptance Criteria

1. WHEN EOD-2 detects a completed recurring task (via Enterprise Asana MCP), THE Body_System SHALL automatically create the next instance with the correct due date (derived from cadence), same project membership, same Routine tag, and a Kiro_RW note referencing the completed instance
2. WHEN the Body_System creates a recurring task instance, THE Body_System SHALL verify the new task does not duplicate an existing future instance (same name + due date within the cadence window) before creation
3. WHEN a recurring task's expected due date passes without the task being completed or a new instance existing, THE Body_System SHALL flag the missed recurrence in the EOD-2 Slack DM summary with the task name, expected cadence, and days overdue
4. THE Body_System SHALL maintain a `recurring_tasks` table in DuckDB_Analytics tracking each recurring task's name, cadence, last_completed_date, next_due_date, and compliance_rate (completed on time / total instances) for trend analysis
5. WHEN a recurring task's compliance_rate drops below 70% over the trailing 8 instances, THE Body_System SHALL flag the task in the EOD-2 summary as a candidate for delegation, automation, or elimination per the leverage assessment framework

### Requirement 12: Builder MCP Internal Tool Data Extraction (Tier 2 — L2/L5)

**User Story:** As Richard, I want the system to extract structured data from internal tools accessible via Builder MCP (phonetool for org charts, Taskei for tickets, code.amazon for documentation) and store it in DuckDB for cross-referencing with other data sources, so that internal tool data is queryable alongside market metrics and Slack signals.

#### Acceptance Criteria

1. WHEN the Body_System needs to resolve a person's role, team, or manager for relationship context, THE Body_System SHALL query Builder MCP's phonetool access to retrieve the person's current organizational information and cache it in DuckDB_Analytics
2. WHEN the Body_System processes a Slack signal referencing a Taskei ticket or SIM, THE Body_System SHALL query Builder MCP to retrieve the ticket status, assignee, and priority, attaching the structured data to the signal record in DuckDB_Analytics
3. WHEN the Body_System encounters an internal wiki reference (code.amazon or w.amazon.com link) in a Slack message or email, THE Body_System SHALL retrieve the page content via Builder MCP or XWiki MCP and store a content summary in DuckDB_Analytics for full-text search
4. THE Body_System SHALL cache Builder MCP query results in DuckDB_Analytics with a staleness threshold of 7 days for org data and 24 hours for ticket data, avoiding redundant API calls
5. IF a Builder MCP query fails or returns no results, THEN THE Body_System SHALL log the failure and continue processing without the enrichment data, noting the gap in the signal record
