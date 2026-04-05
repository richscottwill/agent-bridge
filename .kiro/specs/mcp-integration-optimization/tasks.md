# Tasks — MCP Integration Optimization

## Phase A: Core Pipeline Wiring

- [x] 0. Asana State Sync to DuckDB (Foundation)
  - [x] 0.1 Create asana_tasks table in DuckDB — task_gid (PK), name, assignee_gid, project_name, project_gid, section_name, due_on, start_on, completed, completed_at, routine_rw, priority_rw, importance_rw, kiro_rw, next_action_rw, begin_date_rw, synced_at
  - [x] 0.2 Create asana_task_history table in DuckDB — snapshot_date, task_gid, project_name, section_name, due_on, completed, priority_rw, routine_rw (one row per task per day for trend analysis)
  - [x] 0.3 Implement full sync in AM-1 — SearchTasksInWorkspace(assignee=Richard, completed=false) + GetTasksFromProject for each portfolio project (AU, MX, WW Testing, WW Acq, Paid App, ABPS AI Content). UPSERT all tasks into asana_tasks. INSERT daily snapshot into asana_task_history.
  - [x] 0.4 Implement delta sync in EOD-2 — SearchTasksInWorkspace(completed=true, completed_on=today) to capture completions. UPDATE asana_tasks for completed tasks. Detect new tasks since morning (not in asana_tasks).
  - [x] 0.5 Create DuckDB views: asana_overdue (due_on < today AND NOT completed), asana_by_project (task counts per project), asana_by_routine (bucket distribution), asana_completion_rate (trailing 7/30 day completion rate from history)
  - [x] 0.6 Update AM-1 hook prompt to run full Asana sync to DuckDB before other processing
  - [x] 0.7 Update EOD-2 protocol to run delta sync and use DuckDB views for reconciliation instead of re-querying Asana API
  - [x] 0.8 Update AM-3 brief to pull bucket counts and overdue list from DuckDB views instead of morning snapshot JSON
  - [x] 0.9 Implement post-sync coherence check
  - [x] 0.10 Implement schema drift handling for Asana changes
  - [x] 0.11 Create schema_changes table in DuckDB

- [x] 1. Meeting-to-Action-Item Pipeline (Req 1)
  - [x] 1.1 Create meeting_analytics table in DuckDB with fields: session_id, meeting_name, meeting_date, duration_minutes, participant_count, action_item_count, richard_speaking_share, hedging_count, meeting_type, topics_discussed
  - [x] 1.2 Create meeting_highlights table in DuckDB with FTS index on content and speaker fields
  - [x] 1.3 Implement action item extraction logic in EOD-1 — parse Hedy session todos/highlights into structured action items with assignee detection
  - [x] 1.4 Implement Asana deduplication check — SearchTasksInWorkspace with key noun phrases from action item, match on same assignee + 2+ phrase overlap
  - [x] 1.5 Implement Asana task creation from action items — CreateTask with meeting name context, derived due date (explicit date > urgency signal > +3 business days default), appropriate project and Routine tag
  - [x] 1.6 Implement dependency logging for non-Richard action items — append to hands.md with person name, action item, and originating meeting
  - [x] 1.7 Implement Slack DM summary after all sessions processed — list tasks created, tasks updated (dedup), and dependencies logged
  - [x] 1.8 Update EOD-1 hook prompt with meeting-to-task automation section

- [x] 2. Signal-to-Task Pipeline (Req 4)
  - [x] 2.1 Create signal_task_log table in DuckDB (signal_source, signal_id, task_gid, action_taken, priority, created_at)
  - [x] 2.2 Implement high-priority email signal detection in AM-1 — identify emails from Brandon, Kate, Todd, or skip-level with action language
  - [x] 2.3 Implement high-priority Slack signal detection in AM-1 — identify DMs, @mentions, and thread replies requiring action
  - [x] 2.4 Implement Asana deduplication for signals — search for existing tasks from same sender + similar subject within 7 days
  - [x] 2.5 Implement Asana task creation from signals — CreateTask with source context (email subject/excerpt or Slack link/channel/author), bucket assignment (Core/Sweep/Engine Room/Admin)
  - [x] 2.6 Implement signal-to-task logging in DuckDB — INSERT into signal_task_log for every signal processed
  - [x] 2.7 Implement AM-2 triage summary Slack DM — list new tasks, updated tasks, deferred, and dismissed counts
  - [x] 2.8 Update AM-1 hook prompt with signal-to-task pipeline section
  - [x] 2.9 Update AM-2 hook prompt with triage summary generation

- [x] 3. Meeting Data Analytics (Req 7)
  - [x] 3.1 Implement meeting analytics insertion in EOD-1 — INSERT into meeting_analytics after each Hedy session with all fields including meeting_type classification
  - [x] 3.2 Implement meeting highlights insertion — store key quotes, decisions, and insights with speaker attribution in meeting_highlights table
  - [x] 3.3 Implement weekly communication trend computation in EOD-2 — average speaking share by meeting type, hedging trend, action item rate for trailing 4 weeks
  - [x] 3.4 Implement coaching signal detection — flag group meeting speaking share below 15% for 3+ consecutive weeks in EOD-2 Slack DM
  - [x] 3.5 Update EOD-1 hook prompt to insert meeting analytics and highlights after each session
  - [x] 3.6 Update EOD-2 hook prompt to run weekly trend computation and coaching signal check (weekly cadence)

- [x] 4. Workflow Observability (Req 11)
  - [x] 4.1 Create workflow_executions table and workflow_reliability view in DuckDB
  - [x] 4.2 Implement workflow logging pattern — start event, step completion increments, step failure logging, end event with duration
  - [x] 4.3 Add workflow logging to meeting-to-task pipeline (EOD-1)
  - [x] 4.4 Add workflow logging to signal-to-task pipeline (AM-1/AM-2)
  - [x] 4.5 Add workflow logging to WBR pipeline (wbr-watcher.sh)
  - [x] 4.6 Implement degradation detection in EOD-2 — query workflow_reliability for workflows with <80% success rate over 7 days
  - [x] 4.7 Implement EOD-2 workflow summary — include total runs, success rate, average duration, and degraded workflow alerts in Slack DM
  - [x] 4.8 Update EOD-2 hook prompt with workflow observability section

## Phase B: WBR & Quip Integration

- [ ] 5. WBR Quip Reading + Slack Notification (Req 2, 9)
  - [x] 5.1 Create quip_registry table in DuckDB and seed with known Quip document URLs (Pre-WBR Callouts, MX Sync, change logs)
  - [x] 5.2 Test Builder MCP Quip read access — verify ReadInternalWebsites can access the Pre-WBR Callouts Quip document and return parseable content
  - [x] 5.3 Implement Quip context reading for WBR pipeline — read Pre-WBR Callouts Quip to check what's already posted, avoid duplicate analysis
  - [x] 5.4 Implement Quip change log reading — read change log Quip docs during WBR pipeline to provide campaign change context to the callout writer
  - [x] 5.5 Implement Slack notification — post to Richard's DM (self_dm) or rsw-channel with market highlights after callouts are generated (Richard still manually posts to Quip)
  - [x] 5.6 Implement per-market WoW summary in Slack notification — one line per market with most significant change (regs or spend)
  - [x] 5.7 Implement pipeline status logging — log each market's callout status (generated, skipped, error) to DuckDB
  - [x] 5.8 Update WBR watcher script with Quip reading, Slack notification, and observability steps

## Phase C: Knowledge Enrichment

- [x] 6. Knowledge-Enriched Wiki Publishing (Req 3, 10)
  - [x] 6.1 Create publication_registry table in DuckDB (article_id, article_title, local_path, sharepoint_url, xwiki_page_id, sharepoint_status, xwiki_status, sync_status, timestamps)
  - [x] 6.2 Implement KDS query integration in wiki-researcher — extract topic keywords, query KDS, include relevant findings (relevance >= 7/10) in research brief with source attribution
  - [x] 6.3 Implement ARCC query integration in wiki-researcher — query ARCC for governance/organizational context, include relevant findings in research brief
  - [x] 6.4 Implement markdown-to-XWiki markup converter — handle headings, bold, italic, lists, code blocks, links, tables
  - [x] 6.5 Implement XWiki publishing in wiki-librarian — create/update page under PaidSearch/{ArticleTitle} namespace with category tags from artifacts/index.md
  - [x] 6.6 Implement publication registry updates — INSERT/UPDATE publication_registry after each SharePoint and XWiki publish
  - [x] 6.7 Implement divergence detection — query publication_registry for articles where SharePoint and XWiki timestamps differ by >24 hours, update XWiki to match
  - [ ] 6.8 Implement XWiki publish failure handling — log failure, retain SharePoint copy, flag for retry on next sync run

- [x] 7. Automated Context Enrichment (Req 8)
  - [x] 7.1 Create enrichment_log table in DuckDB (query_text, source, result_count, relevant_count, routed_to, queried_at)
  - [x] 7.2 Implement query generation from current.md — extract active project names and topics, generate 3-5 KDS queries per run
  - [x] 7.3 Implement KDS query execution during EOD-2 — query KDS for each generated query, score relevance (0-10) against project context
  - [x] 7.4 Implement intake file creation for relevant findings — save findings with relevance >= 7 to ~/shared/context/intake/kds-{date}-{topic}.md
  - [x] 7.5 Implement organ routing for KDS findings — route strategic insights to brain.md, market data to eyes.md, relationship context to memory.md
  - [ ] 7.6 Implement enrichment logging — INSERT into enrichment_log for every query executed
  - [ ] 7.7 Implement query refinement on 3 consecutive empty runs — regenerate queries from updated current.md, log refinement
  - [ ] 7.8 Update EOD-2 hook prompt with context enrichment section

- [x] 8. Slack Conversation Intelligence (Req 12)
  - [x] 8.1 Implement acronym/project detection in AM-1 Slack scan — identify internal terms (OCI, IECCP, AEO, CPC, ROAS, etc.) in messages
  - [x] 8.2 Implement KDS enrichment for unfamiliar terms — query KDS for context on detected internal references, attach knowledge_context to DuckDB record
  - [x] 8.3 Implement historical conversation retrieval — combined query pattern using DuckDB FTS (slack_messages) + KDS for organizational context with source attribution
  - [x] 8.4 Implement AM-2 triage context enhancement — query DuckDB for related past messages from same author + similar topic within 30 days, include in triage context
  - [x] 8.5 Update AM-1 hook prompt with Slack enrichment steps
  - [x] 8.6 Update AM-2 hook prompt with historical context retrieval during triage

## Phase D: AgentCore Services (Blocked — requires internal AWS account)

- [ ] 9. AgentCore Browser Automation (Req 5)
  - [ ] 9.1 Create browser_access_log table in DuckDB (tool_name, url, session_id, success, file_size_bytes, error_message, accessed_at)
  - [ ] 9.2 Implement WorkDocs dashboard download via AgentCore browser — create session, navigate, authenticate via Midway, download xlsx, validate file
  - [ ] 9.3 Implement fallback to SharePoint polling on browser failure — detect auth/download failure, fall back to existing mechanism, notify via Slack DM
  - [ ] 9.4 Implement browser access logging — INSERT into browser_access_log for every access attempt
  - [ ] 9.5 Implement Google Ads UI campaign snapshot extraction — navigate to campaign overview, extract metrics, store in DuckDB
  - [x] 9.6 Update WBR watcher to use AgentCore browser as primary download method with SharePoint as fallback

- [x] 10. Sandboxed Code Interpreter (Req 6)
  - [x] 10.1 Implement Parquet export for Code Interpreter — export relevant DuckDB data subsets as Parquet files for upload
  - [x] 10.2 Implement Code Interpreter session management — create session, upload data, execute analysis, download results
  - [x] 10.3 Implement result retrieval and storage — save visualizations to ~/shared/research/ with descriptive filenames, log execution metadata to DuckDB
  - [ ] 10.4 Implement fallback to local Python execution on Code Interpreter failure
  - [ ] 10.5 Integrate Code Interpreter with Karpathy Loop — route statistical experiments (Bayesian prior updates, A/B analysis) to sandboxed environment

## Integration and Validation

- [x] 11. Hook Prompt Integration
  - [x] 11.1 Consolidate all AM-1 additions (signal-to-task detection, Slack enrichment, acronym detection) into a single coherent AM-1 hook prompt update
  - [x] 11.2 Consolidate all AM-2 additions (triage summary, historical context, draft queue) into a single coherent AM-2 hook prompt update
  - [x] 11.3 Consolidate all EOD-1 additions (meeting-to-task, meeting analytics, highlights) into a single coherent EOD-1 hook prompt update
  - [x] 11.4 Consolidate all EOD-2 additions (workflow observability, communication trends, context enrichment, coaching signals) into a single coherent EOD-2 hook prompt update
  - [x] 11.5 Update WBR watcher script with all additions (Quip publishing, Slack notification, observability)

- [ ] 12. Validation
  - [ ] 12.1 Run EOD-1 with meeting-to-task enabled — verify Hedy sessions produce Asana tasks and meeting_analytics records
  - [ ] 12.2 Run AM-1/AM-2 with signal-to-task enabled — verify high-priority signals create Asana tasks and log to signal_task_log
  - [ ] 12.3 Run WBR pipeline with Quip publishing — verify callouts appear in Quip document with correct formatting
  - [ ] 12.4 Run wiki pipeline with KDS/ARCC enrichment — verify research briefs include sourced findings
  - [ ] 12.5 Run EOD-2 with context enrichment — verify KDS findings land in intake/ and enrichment_log is populated
  - [ ] 12.6 Query workflow_reliability view — verify all cross-MCP workflows are logging execution data correctly
  - [ ] 12.7 Query meeting_analytics for communication trends — verify weekly trend computation produces correct results
  - [ ] 12.8 Test Slack conversation retrieval — query DuckDB FTS for a known past conversation topic and verify results include source attribution
