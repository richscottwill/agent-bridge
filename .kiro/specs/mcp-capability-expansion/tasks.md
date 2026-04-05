# Tasks — MCP Capability Expansion

## Tier 1: Foundation (No New Dependencies)

- [ ] 1. DuckDB Schema Extensions
  - [ ] 1.1 Create unified_signals table with all fields (signal_id, source_mcp, source_id, author, author_alias, timestamp, content_preview, signal_type, raw_priority, computed_priority, cluster_id, disposition, disposition_task_gid)
  - [ ] 1.2 Create meeting_analytics table (session_id, meeting_name, meeting_date, duration_minutes, participant_count, action_item_count, richard_speaking_share, hedging_count, topics_discussed)
  - [ ] 1.3 Create data_freshness table and seed with all 16 monitored sources (10 market context files, 5 DuckDB tables, 1 SharePoint doc)
  - [ ] 1.4 Create health_alerts table (alert_id, alert_type, market, severity, message, context_data, slack_context, acknowledged)
  - [ ] 1.5 Create relationship_activity table (person_name, person_alias, week, slack_interactions, email_exchanges, meetings_shared, asana_collaborations, total_score, interaction_trend)
  - [ ] 1.6 Create competitive_signals table and competitive_intelligence view
  - [ ] 1.7 Create recurring_tasks table (task_name, project_name, cadence, last_completed_date, next_due_date, total_instances, on_time_instances, compliance_rate)
  - [ ] 1.8 Create workflow_executions table and workflow_reliability view
  - [ ] 1.9 Create publication_registry table (article_id, article_title, local_path, sharepoint_url, xwiki_page_id, sharepoint_status, xwiki_status, sync_status)
  - [ ] 1.10 Create builder_cache table (cache_key, source_tool, data, fetched_at, stale_after_hours)
  - [ ] 1.11 Create unified_signal_queue view with priority ordering (stakeholder_rank × type_weight × recency)
  - [ ] 1.12 Verify all tables and views are queryable via DuckDB MCP execute_query

- [ ] 2. Unified Signal Inbox Pipeline (Req 1)
  - [ ] 2.1 Implement signal extraction logic for Slack source — classify messages as request/fyi/blocker/decision and insert into unified_signals
  - [ ] 2.2 Implement signal extraction logic for Outlook source — classify emails and insert into unified_signals
  - [ ] 2.3 Implement signal extraction logic for Asana source — extract notifications and insert into unified_signals
  - [ ] 2.4 Implement signal extraction logic for Hedy source — extract action items and decisions from sessions and insert into unified_signals
  - [ ] 2.5 Implement priority computation function (stakeholder_rank × type_weight × recency) with stakeholder ranks from memory.md
  - [ ] 2.6 Implement signal clustering — link signals from same author within 48 hours with overlapping keywords via cluster_id
  - [ ] 2.7 Update AM-1 hook prompt to insert signals into unified_signals after each source scan
  - [ ] 2.8 Update AM-2 hook prompt to add Phase 0: query unified_signal_queue and triage in priority order
  - [ ] 2.9 Update AM-2 hook prompt to set disposition on each signal after triage (task_created, task_updated, deferred, dismissed)
  - [ ] 2.10 Add graceful degradation — if a source MCP is unreachable, log failure, process available sources, flag in AM-3 brief

- [ ] 3. Freshness Monitoring System (Req 5)
  - [ ] 3.1 Implement DuckDB table freshness check — query MAX(timestamp) for each monitored table and compare against expected_cadence_hours
  - [ ] 3.2 Implement context file freshness check — parse Last updated header from each market context file and compare against 14-day threshold
  - [ ] 3.3 Implement SharePoint document freshness check — query sharepoint_search for WBR dashboard last modified date
  - [ ] 3.4 Update EOD-2 hook prompt to run freshness checks during maintenance cascade
  - [ ] 3.5 Implement Slack DM freshness report — list stale sources with days since update, expected cadence, and affected downstream workflows
  - [ ] 3.6 Implement Monday WBR warning — if WBR data sources are stale on Monday, include warning in WBR watcher Slack notification

- [ ] 4. Budget and Task Health Monitoring (Req 8)
  - [ ] 4.1 Implement daily budget overrun detection — query daily_metrics for AU/MX where daily spend > 120% of target
  - [ ] 4.2 Implement monthly pacing check — compute MTD spend vs monthly budget, flag if projected > 105%
  - [ ] 4.3 Implement abandoned overdue task detection — query Asana for tasks overdue > 7 days with no Kiro_RW update in 5 days
  - [ ] 4.4 Implement metric anomaly detection — compare current week vs trailing 4-week average, flag > 15% WoW change
  - [ ] 4.5 Implement contextual Slack enrichment for anomalies — search Slack for messages explaining the metric change
  - [ ] 4.6 Implement at-risk project flagging — detect 3+ overdue tasks in same project, suggest triage block
  - [ ] 4.7 Update AM-1 hook prompt to run budget checks after data is available
  - [ ] 4.8 Update AM-3 hook prompt to include health alerts summary section

- [ ] 5. Recurring Task Lifecycle Management (Req 11)
  - [ ] 5.1 Implement recurring task detection — query Asana for recently completed tasks matching recurring patterns (Weekly, Monthly, WBR, MBR, Agenda, Flash, Kingpin)
  - [ ] 5.2 Implement next instance date computation — weekly +7d, biweekly +14d, monthly +30d with start_on offset
  - [ ] 5.3 Implement duplicate prevention — check for existing incomplete task with same name in same project within cadence window before creating
  - [ ] 5.4 Implement next instance creation via Asana MCP — CreateTask with same project, routine, and computed dates
  - [ ] 5.5 Implement missed recurrence detection — check if expected due date passed without completion or new instance
  - [ ] 5.6 Implement compliance tracking — update recurring_tasks table with on_time/total counts and compliance_rate
  - [ ] 5.7 Implement low compliance flagging — flag tasks with compliance_rate < 70% over trailing 8 instances as candidates for delegation/automation/elimination
  - [ ] 5.8 Update EOD-2 hook prompt to run recurring task lifecycle check during maintenance cascade
  - [ ] 5.9 Add Slack DM notification for auto-created instances and missed recurrences

- [ ] 6. Meeting Intelligence Pipeline (Req 2)
  - [ ] 6.1 Implement Slack context enrichment — extract topic keywords from Hedy session, query Slack for related threads, attach to meeting record
  - [ ] 6.2 Implement action item deduplication — cross-reference extracted action items against open Asana tasks before creating new tasks
  - [ ] 6.3 Implement Asana task creation from meeting action items — CreateTask with meeting name as context, action as description, derived due date
  - [ ] 6.4 Implement Slack threaded reply after task creation — post in relevant channel linking new task and tagging assignee
  - [ ] 6.5 Implement meeting analytics insertion — INSERT into meeting_analytics with session_id, duration, participants, action_items, speaking_share, topics
  - [ ] 6.6 Implement organ routing — route decisions to brain.md, data points to eyes.md, relationship signals to memory.md, communication patterns to nervous-system.md
  - [ ] 6.7 Update EOD-1 hook prompt to run full meeting intelligence pipeline for each Hedy session

- [ ] 7. Stakeholder Communication Drafting (Req 3)
  - [ ] 7.1 Implement draft trigger detection — identify Asana tasks requiring stakeholder updates (due approaching, blocker resolved, status change)
  - [ ] 7.2 Implement multi-source context assembly — gather task context (Asana), meeting context (Hedy/DuckDB), communication history (Slack/DuckDB), stakeholder prefs (memory.md)
  - [ ] 7.3 Implement draft generation and storage — save drafts to ~/shared/context/intake/drafts/ with metadata header (recipient, channel, urgency, source_task_gid)
  - [ ] 7.4 Implement draft staleness detection — check if source data changed since draft generation, flag stale drafts for regeneration
  - [ ] 7.5 Implement recipient whitelist enforcement — only generate drafts for Brandon, Kate, Lena, Lorena, Andrew, Stacey, Adi, Dwayne
  - [ ] 7.6 Update AM-2 hook prompt to generate drafts during Phase 2
  - [ ] 7.7 Update AM-3 hook prompt to include draft queue summary

- [ ] 8. WBR Full Automation (Req 4)
  - [ ] 8.1 Test Builder MCP Quip write capability — verify ReadInternalWebsites can access Quip and identify write tools
  - [ ] 8.2 Implement Quip document structure reading — read existing Pre-WBR Callouts doc, identify section structure
  - [ ] 8.3 Implement Quip callout publishing — append new week's callouts to correct section preserving existing structure
  - [ ] 8.4 Implement change log cross-reference — join change_log entries with dashboard data to explain WoW metric movements
  - [ ] 8.5 Implement team Slack notification — post to team channel with market highlights and Quip document link
  - [ ] 8.6 Implement pipeline observability — log each step to workflow_executions with timestamps and status
  - [ ] 8.7 Implement graceful failure handling — continue independent steps on failure, save partial results, notify Richard via Slack DM
  - [ ] 8.8 Update WBR watcher script to include Quip publishing and Slack notification steps

## Tier 2: Expansion (Minor Config/Wiring)

- [ ] 9. Competitive Intelligence (Req 10)
  - [ ] 9.1 Configure competitor list in a queryable format (DuckDB table or config file)
  - [ ] 9.2 Implement Slack mention tagging — during AM-1 Slack scan, check messages against competitor list and insert into competitive_signals
  - [ ] 9.3 Implement impression share trend computation — compute weekly changes from competitors table, flag > 5pp WoW increase
  - [ ] 9.4 Implement KDS competitive query — query KDS for recent competitive intelligence during WBR callout generation
  - [ ] 9.5 Implement competitive shift alert — post Slack DM with competitor name, market, metric change, and correlated Slack threads
  - [ ] 9.6 Update AM-1 hook prompt to tag competitor mentions during Slack scan
  - [ ] 9.7 Update WBR callout pipeline to include competitive context from competitive_intelligence view

- [ ] 10. Relationship Intelligence (Req 9)
  - [ ] 10.1 Implement weekly Slack interaction count — query DuckDB slack_messages for message counts per person per week
  - [ ] 10.2 Implement weekly email exchange count — query Outlook MCP for email exchanges per person per week
  - [ ] 10.3 Implement weekly meeting co-attendance count — query meeting_analytics for shared sessions per person per week
  - [ ] 10.4 Implement weekly Asana collaboration count — query Asana for task collaborations per person per week
  - [ ] 10.5 Implement total score computation and insert into relationship_activity table
  - [ ] 10.6 Implement cooling detection — flag persons with 3 consecutive zero-score weeks after being active (score > 5) for prior 4 weeks
  - [ ] 10.7 Implement intensifying detection — flag persons with score > 3x trailing 4-week average
  - [ ] 10.8 Implement memory.md auto-update — update relationship entries with last_interaction_date and interaction_trend from DuckDB data
  - [ ] 10.9 Update EOD-2 hook prompt to run relationship intelligence computation during maintenance cascade

- [ ] 11. Knowledge Base Auto-Maintenance (Req 6)
  - [ ] 11.1 Implement KDS query integration in wiki-researcher — query KDS for relevant internal knowledge during article research
  - [ ] 11.2 Implement ARCC query integration in wiki-researcher — query ARCC for governance and organizational context
  - [ ] 11.3 Implement markdown-to-XWiki markup converter (headings, lists, tables, code blocks, links)
  - [ ] 11.4 Implement XWiki publishing in wiki-librarian — publish FINAL articles to w.amazon.com under PaidSearch namespace
  - [ ] 11.5 Implement publication registry tracking — update publication_registry in DuckDB after each publish (SharePoint + XWiki)
  - [ ] 11.6 Implement weekly wiki lint — query KDS for organizational changes, cross-reference with article content, flag stale articles
  - [ ] 11.7 Implement Asana task creation for stale articles with active Slack discussion (>3 mentions in 14 days + article >14 days old)
  - [ ] 11.8 Implement XWiki publish failure handling — retain local markdown, log failure, retry on next sync

- [ ] 12. Team-Facing Reports (Req 7)
  - [ ] 12.1 Implement weekly WBR summary HTML report generation from DuckDB weekly_metrics (10 markets, key metrics, WoW changes)
  - [ ] 12.2 Implement monthly performance summary HTML report from DuckDB monthly_metrics
  - [ ] 12.3 Implement SharePoint upload for reports — upload to designated shared folder
  - [ ] 12.4 Implement Slack team notification after report upload — post link and one-line highlight
  - [ ] 12.5 Implement fallback to local save on SharePoint upload failure
  - [ ] 12.6 Wire weekly report generation to WBR pipeline completion trigger
  - [ ] 12.7 Wire monthly report generation to first-business-day-of-month trigger in EOD-2

- [ ] 13. Builder MCP Data Extraction (Req 12)
  - [ ] 13.1 Implement phonetool org data retrieval — query Builder MCP for person's role, team, manager and cache in builder_cache (7-day TTL)
  - [ ] 13.2 Implement Taskei/SIM ticket enrichment — detect ticket references in Slack signals, query Builder MCP for status/assignee/priority, cache (24-hour TTL)
  - [ ] 13.3 Implement internal wiki content retrieval — detect code.amazon/w.amazon.com links, retrieve content via Builder/XWiki MCP, store summary in DuckDB
  - [ ] 13.4 Implement cache-first query pattern — check builder_cache TTL before making MCP calls
  - [ ] 13.5 Implement graceful failure handling — log Builder MCP query failures, continue without enrichment data

## Integration and Validation

- [ ] 14. Hook Prompt Updates
  - [ ] 14.1 Update AM-1 hook with signal insertion, competitor tagging, and budget check additions
  - [ ] 14.2 Update AM-2 hook with Phase 0 unified triage, stakeholder drafting, and abandoned task detection
  - [ ] 14.3 Update AM-3 hook with health alerts, freshness warnings, and draft queue summary sections
  - [ ] 14.4 Update EOD-1 hook with meeting intelligence pipeline (Slack enrichment, analytics insertion, organ routing, Asana task creation)
  - [ ] 14.5 Update EOD-2 hook with freshness monitoring, relationship intelligence, recurring task lifecycle, wiki lint, and workflow reliability summary
  - [ ] 14.6 Update WBR watcher with Quip publishing, Slack notification, change log cross-reference, and anomaly detection steps

- [ ] 15. Validation and Testing
  - [ ] 15.1 Run AM-1 with signal insertion enabled — verify signals from all 4 sources land in unified_signals with correct fields
  - [ ] 15.2 Run AM-2 with unified triage — verify priority ordering produces correct signal sequence
  - [ ] 15.3 Run EOD-1 with meeting intelligence — verify Hedy sessions produce meeting_analytics records and Asana tasks
  - [ ] 15.4 Run EOD-2 with freshness monitoring — verify stale sources are detected and Slack alert is sent
  - [ ] 15.5 Run EOD-2 with recurring task check — verify completed recurring tasks trigger next instance creation
  - [ ] 15.6 Run WBR pipeline with Quip publishing — verify callouts appear in Quip document with correct structure
  - [ ] 15.7 Query workflow_reliability view — verify all cross-MCP workflows are logging execution data
  - [ ] 15.8 Query competitive_intelligence view — verify competitor mentions are being tagged and aggregated
