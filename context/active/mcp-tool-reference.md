<!-- DOC-0354 | duck_id: protocol-mcp-tool-reference -->
# MCP Tool Reference

Last updated: 2026-04-02 (Thursday PT)
Config: ~/.kiro/settings/mcp.json

Every MCP server available to agents. Read before using any MCP tool.

---

## Quick Reference

| # | Server | Purpose | Access | Status |
|---|--------|---------|--------|--------|
| 1 | aws-outlook-mcp | Email, Calendar, To-Do | Full CRUD | Proven |
| 2 | ai-community-slack-mcp | Slack channels, DMs, search | Read + limited write | Proven |
| 3 | hedy | Meeting transcripts, topics, action items | Read + context updates | Proven |
| 4 | duckdb | PS Analytics database (SQL) | Read + Write | Proven |
| 5 | arcc | Security/compliance knowledge base | Read-only search | Proven |
| 6 | amazon-sharepoint-mcp | SharePoint/OneDrive, Loop pages | Read + Write | Proven |
| 7 | loop-mcp | Microsoft Loop pages | Read-only | Working |
| 8 | knowledge-discovery-mcp | KDS knowledge base Q&A | Read-only query | Working |
| 9 | radar-mcp | Radar | Unknown | Untested |
| 10 | search-marketing-agent-workspace-alpha-mcp | AgentCore Gateway for PS | Unknown | Untested |
| 11 | weblab-mcp | Weblab experiment data | Read-only | NEW 4/2 |
| 12 | xwiki-mcp | w.amazon.com wiki pages | Read + Write | NEW 4/2 |
| 13 | builder-mcp | Internal websites, Quip, code search, Taskei, pipelines | Read + some write | NEW 4/2 |
| 14 | taskei-p-mcp | Taskei task management | Unknown | NEW 4/2 |
| 15 | aaisd-redshift-mcp | Redshift queries | Unknown | Untested |
| P1 | power-aws-agentcore | Bedrock AgentCore | Agent deployment | Power, not daily use |

Pending: enterprise-asana-mcp (access requested, not yet granted).

---

## 1. aws-outlook-mcp

Email, Calendar, Microsoft To-Do. Full CRUD.

Tools (14, all auto-approved): email_search, email_read, email_inbox, email_send, email_reply, email_draft, email_folders, email_list_folders, todo_tasks, todo_lists, todo_checklist, calendar_view, calendar_meeting, calendar_search.

Guardrails:
- preToolUse hook blocks email_send/reply/forward to anyone except prichwil@amazon.com
- preToolUse hook blocks calendar events with external attendees
- email_draft is always safe (doesn't send)
- Personal calendar blocks are allowed

Gotchas:
- CLI invocation returns triple-nested JSON (parse 3 times)
- HTML bodies with special chars need cat-pipe method (write to temp file first)
- Always use timeout on CLI calls

Key IDs: See bottom of this file for Outlook folder IDs and To-Do list IDs.

---

## 2. ai-community-slack-mcp

Slack read access (channels, DMs, search, threads, files) plus limited write.

Tools (auto-approved reads): search, list_channels, batch_get_conversation_history, batch_get_thread_replies, batch_get_channel_info, batch_get_user_info, get_channel_sections, reaction_tool, download_file_content, list_drafts, lists_items_list, lists_items_info, self_dm, post_message, batch_set_last_read.

Additional tools (require approval): create_draft, open_conversation, add_channel_members, create_channel.

Guardrails (per slack-guardrails.md):
- post_message ONLY to C0993SRL6FQ (rsw-channel) or self_dm to prichwil
- create_draft is always allowed (Richard reviews before sending)
- NEVER post_message to any other channel
- NEVER open_conversation to DM anyone other than Richard
- NEVER add_channel_members or create_channel without explicit approval
- All read operations are unrestricted

Config: Channel registry at ~/shared/context/active/slack-channel-registry.json. Scan state at ~/shared/context/active/slack-scan-state.json. Section-based depth: WW Testing/AB PS = full, AB/AI = standard, Channels = light.

---

## 3. hedy

Meeting transcripts, recaps, action items, speaker analysis, topics, session contexts. Remote MCP via npx mcp-remote.

Tools (14, all auto-approved): GetSessions, GetSessionDetails, GetSessionHighlights, GetSessionToDos, GetHighlights, GetHighlightDetails, GetToDos, GetAllTopics, GetTopicDetails, GetTopicSessions, ListSessionContexts, GetSessionContext, UpdateSessionContext, UpdateTopic.

Usage pattern:
1. GetSessions (limit=1) to find newest recording
2. GetSessionDetails (sessionId) for full transcript/recap/todos
3. Save to ~/shared/context/intake/ for processing

No activation step needed. Tools prefixed mcp_hedy_ and available directly.

Limitations:
- Only captures meetings where Hedy bot was present
- Transcript quality varies with audio quality and speaker count
- Remote connection via npx can be slow on first call

---

## 4. duckdb

PS Analytics database. All structured paid search data: daily/weekly/monthly metrics (10 markets), IECCP, projections, callout scores, competitors, OCI status, change logs, anomalies.

Tools (4, all auto-approved): execute_query, list_databases, list_tables, list_columns.

DB path: ~/shared/tools/data/ps-analytics.duckdb
Python CLI: python3 ~/shared/tools/data/query.py "SQL"
Python import: from query import db, market_trend, market_week, projection, callout_scores

Active tables: daily_metrics, weekly_metrics, monthly_metrics, ieccp, projections, callout_scores, experiments, ingest_log, change_log, anomalies, competitors, oci_status, slack_messages, agent_actions, agent_observations.

Schema export: ~/shared/tools/data/schema.sql (auto-generated after ingestion).
Portability: Single file, no server. Rebuild instructions at ~/shared/tools/data/RECONSTRUCTION.md.

---

## 5. arcc

Agent Ready Curated Context. Security and compliance knowledge base search.

Tools (1, auto-approved): search_arcc.

Also supports: contentIds lookup for full document retrieval, comment_arcc for feedback.

Usage: MANDATORY first call when request involves credentials, user data, network rules, file paths, or infrastructure (per pilot-steering.md). Query ARCC before examining code.

Scoped to 9 namespaces (configured in args).

---

## 6. amazon-sharepoint-mcp

SharePoint and OneDrive. Files, folders, lists, Loop pages. Read and write.

Tools: sharepoint_search, sharepoint_list_sites, sharepoint_list_libraries, sharepoint_list_files, sharepoint_read_file, sharepoint_write_file, sharepoint_create_folder, sharepoint_rename_folder, sharepoint_delete_file, sharepoint_read_loop, sharepoint_list_lists, sharepoint_list_fields, sharepoint_list_items, sharepoint_list_views, sharepoint_list_view_fields, sharepoint_create_list, sharepoint_delete_list, sharepoint_create_field, sharepoint_update_field, sharepoint_delete_field, sharepoint_create_item, sharepoint_update_item, sharepoint_delete_item.

Auto-approved: sharepoint_search, sharepoint_read_loop.

Used by: SharePoint Sync tool (wiki articles to OneDrive). Config: ~/shared/tools/sharepoint-sync/config.yaml.
Local mirror: c:/Users/prichwil/OneDrive - amazon.com/Artifacts/wiki-sync (Windows machine).

Gotchas:
- libraryName is the library TITLE (e.g., "Documents"), NOT the URL path ("Shared Documents")
- Use sharepoint_list_libraries first to get correct title
- Loop pages use sharepoint_read_loop, not sharepoint_read_file

---

## 7. loop-mcp

Microsoft Loop page reader. Converts Loop pages to markdown.

Tools: read_loop (auto-approved).

Accepts Loop URLs (https://loop.cloud.microsoft/p/...) and SharePoint Loop URLs (https://*.sharepoint.com/:fl:/...).

Overlap: amazon-sharepoint-mcp also has sharepoint_read_loop. Either works for Loop pages.

---

## 8. knowledge-discovery-mcp

Knowledge Discovery Service (KDS). AI-generated answers from curated knowledge bases.

Tools: QuerySync (auto-approved), Feedback.

Requires: conversationId (UUID v4), sessionId (UUID v4), useCase, customerId, question.

Use cases are tenant-scoped. The available use cases depend on what's been configured for Richard's access. Useful for querying internal knowledge bases that have been onboarded to KDS.

---

## 9. radar-mcp

Status: Untested. No auto-approved tools. Installed via toolbox registry.

Needs investigation to determine what tools are available and whether they're relevant to PS work.

---

## 10. search-marketing-agent-workspace-alpha-mcp

AgentCore Gateway for Search Marketing. Lambda-backed MCP tools.

Status: Untested. No auto-approved tools. Remote MCP config.

Likely provides PS-specific tools via AgentCore. Needs investigation to determine available tools and access.

---

## 11. weblab-mcp (NEW 4/2)

Weblab experimentation platform. Read-only access to experiment data.

Tools (4): check_weblab_taa (TAA alarm status via WSTLake Athena), weblab_details (experiment metadata via WeblabAPI), weblab_allocations (treatment allocations via WeblabAPI), weblab_activation_history (change history via WeblabAPI).

Authentication: Midway cookie.

Relevance to Richard's work:
- Polaris Brand LP weblabs (JP 50/50, AU/EU dial-ups)
- Baloo weblabs (early access, public launch)
- OCI weblabs (EU3, JP)
- Any future A/B tests the PS team runs

Use cases:
- Check allocation state before/after dial-up changes
- Verify treatment configs match what was requested
- Pull activation history to track when changes were made
- Monitor TAA alarms for experiment health

Docs: https://w.amazon.com/bin/view/Weblab/MCP
Issues: https://issues.amazon.com/issues/create?assignedFolder=d9f99943-607b-4f73-a718-26855f8ce15d

---

## 12. xwiki-mcp (NEW 4/2)

Read and write wiki pages on w.amazon.com.

Tools: get_wiki_page (read), put_wiki_page (create/update).

get_wiki_page: path parameter like "MyTeam/MyPage" maps to w.amazon.com/bin/view/MyTeam/MyPage.
put_wiki_page: path, content (XWiki syntax xwiki/2.1), optional title and syntax.

Relevance: Team processes, OCI implementation guides, internal documentation that lives on w.amazon.com. Could feed wiki-concierge with broader search capability beyond Richard's own wiki pipeline.

Docs: https://w.amazon.com/bin/view/Users/joshcw/XWikiMcp

---

## 13. builder-mcp (NEW 4/2)

Amazon Software Builder MCP. Massive toolset for internal Amazon development workflows.

Key tool groups relevant to Richard:

Reading internal websites (ReadInternalWebsites):
- Quip documents (quip-amazon.com/ID)
- Phonetool (employee lookup)
- Taskei tasks (taskei.amazon.dev/tasks/TASK_ID)
- SIM tickets (issues.amazon.com/issues/ISSUE_ID)
- Wiki pages (w.amazon.com/bin/view/PATH)
- Meetings (meetings.amazon.com/calendar/find/LOGIN)
- Code reviews (code.amazon.com/reviews/CR-XXXXXXXX)
- Paste (paste.amazon.com)
- Oncall (oncall.corp.amazon.com)
- Apollo environments
- Pipelines (pipelines.amazon.com)
- Kingpin goals

Quip editing (QuipEditor):
- Read documents with structure analysis
- Add/edit/delete content at specific locations
- Create new documents
- Supports markdown and HTML

Internal search (InternalSearch):
- Domains: ALL, WIKI, BUILDER_HUB, PHONETOOL, SAGE_HORDE, BROADCAST, INSIDE, POLICY, EMAIL_LIST, and more
- KQL query syntax with filters

Code search (InternalCodeSearch):
- Search code across Amazon repositories
- Code snippets and repository search

Taskei integration (TaskeiGetTask, TaskeiListTasks, TaskeiCreateTask, TaskeiUpdateTask, TaskeiGetRooms, TaskeiGetRoomResources):
- Full CRUD on Taskei tasks/SIM issues
- List tasks with filters (status, assignee, room, sprint, labels)
- Create and update tasks with all fields
- Get room resources (labels, sprints, kanban boards, workflow steps)

Pipeline tools (GetPipelinesRelevantToUser, GetPipelineHealth, GetPipelineDetails):
- Pipeline status and health metrics
- Failed builds, deployments, tests
- Pending approvals

Apollo tools (ApolloReadActions):
- Environment and stage details
- Deployment history and changes
- Capacity information

Oncall tools (OncallReadActions):
- Search teams, list user teams
- Get shifts and schedules
- Generate oncall reports

Ticketing (TicketingReadActions, TicketingWriteActions):
- Search SIM-T tickets
- Get ticket details with threads
- Create and update tickets
- Add comments

Workspace tools (BrazilWorkspace, WorkspaceGitDetails, CRRevisionCreator, CrCheckout):
- Brazil workspace management
- Git operations
- Code review creation

Build tools (BrazilBuildAnalyzerTool, BrazilPackageBuilderAnalyzerTool):
- Build failure analysis
- Package builder diagnostics

Mechanic tools (MechanicDiscoverTools, MechanicDescribeTool, MechanicRunTool):
- Host operations, AWS resource management
- CloudWatch logs, EC2, ECS operations

Other: SimAddComment, WorkspaceSearch, SearchAcronymCentral, GetSasRisks, GetSasCampaigns, ReadRemoteTestRun.

Limitations:
- No auto-approved tools (each call needs approval unless added)
- Very large toolset; most tools are engineering-focused
- Richard's primary use: Quip reading, internal search, Taskei tickets, phonetool lookups

---

## 14. taskei-p-mcp (NEW 4/2)

Dedicated Taskei MCP server. Status: installed but untested.

May overlap with builder-mcp's Taskei tools. Needs investigation to determine if it offers additional capabilities or is redundant.

---

## 15. aaisd-redshift-mcp

Redshift query server. Status: untested.

Potentially useful if Richard needs to query Redshift data directly (e.g., AAISD analytics). Needs investigation.

---

## P1. power-aws-agentcore (Kiro Power)

Bedrock AgentCore. Build, test, deploy AI agents. Not daily-use tooling. Relevant only if Richard moves to Level 5 (Agentic Orchestration) and needs to deploy agents to AWS infrastructure.

---

## Pending Installations

| Server | Status | What it does | When to install |
|--------|--------|-------------|-----------------|
| enterprise-asana-mcp | ✅ Live | Native Asana read/write — command center for task management | Connected |

---

## Key IDs

### Outlook Folders
| Folder | ID |
|--------|-----|
| Auto-Comms (Asana) | AAMkAGQ5NmQwNGZkLWQ0NTAtNGY4Yy1hNjhlLTY0OTU1N2QzYTBhYwAuAAAAAAArsD3iy/SDRrGkcLnEuZ4GAQDAgFdLn8NBQbObwPn0M6aUAADuhyQpAAA= |
| Auto-meeting | AAMkAGQ5NmQwNGZkLWQ0NTAtNGY4Yy1hNjhlLTY0OTU1N2QzYTBhYwAuAAAAAAArsD3iy/SDRrGkcLnEuZ4GAQCIgJPBFelsQrcja/dZLhI0AAC3dkeCAAA= |
| Goal: Paid Acquisition | AQMkAGQ5NmQwNGZkLWQ0NTAtNGY4Yy1hNjhlLTY0OTU1ADdkM2EwYWMALgAAAyuwPeLL9INGsaRwucS5ngYBAEas7LcSB6lEv39h0ciIq84AAAITTwAAAA== |
| AP (Invoices) | AAMkAGQ5NmQwNGZkLWQ0NTAtNGY4Yy1hNjhlLTY0OTU1N2QzYTBhYwAuAAAAAAArsD3iy/SDRrGkcLnEuZ4GAQDAgFdLn8NBQbObwPn0M6aUAADuhyQcAAA= |

### To-Do Lists
| List | ID |
|------|-----|
| Sweep | AAMkAGQ5NmQwNGZkLWQ0NTAtNGY4Yy1hNjhlLTY0OTU1N2QzYTBhYwAuAAAAAAArsD3iy-SDRrGkcLnEuZ4GAQCIgJPBFelsQrcja-dZLhI0AADUyESHAAA= |
| Core | AAMkAGQ5NmQwNGZkLWQ0NTAtNGY4Yy1hNjhlLTY0OTU1N2QzYTBhYwAuAAAAAAArsD3iy-SDRrGkcLnEuZ4GAQCIgJPBFelsQrcja-dZLhI0AADUyESIAAA= |
| Engine Room | AAMkAGQ5NmQwNGZkLWQ0NTAtNGY4Yy1hNjhlLTY0OTU1N2QzYTBhYwAuAAAAAAArsD3iy-SDRrGkcLnEuZ4GAQCIgJPBFelsQrcja-dZLhI0AADUyESJAAA= |
| Admin | AAMkAGQ5NmQwNGZkLWQ0NTAtNGY4Yy1hNjhlLTY0OTU1N2QzYTBhYwAuAAAAAAArsD3iy-SDRrGkcLnEuZ4GAQCIgJPBFelsQrcja-dZLhI0AADUyESKAAA= |
| Backlog | AAMkAGQ5NmQwNGZkLWQ0NTAtNGY4Yy1hNjhlLTY0OTU1N2QzYTBhYwAuAAAAAAArsD3iy-SDRrGkcLnEuZ4GAQCIgJPBFelsQrcja-dZLhI0AADWyS4nAAA= |

### Slack Channels (guardrailed)
| Channel | ID | Write Access |
|---------|-----|-------------|
| rsw-channel | C0993SRL6FQ | YES (only channel with write) |
| All others | various | READ ONLY |

---

## Tool Selection Guide

| I need to... | Use this server | Tool |
|-------------|----------------|------|
| Search/read email | aws-outlook-mcp | email_search, email_read |
| Draft an email | aws-outlook-mcp | email_draft |
| Check calendar | aws-outlook-mcp | calendar_view |
| Create focus block | aws-outlook-mcp | calendar_meeting |
| Manage To-Do tasks | aws-outlook-mcp | todo_tasks |
| Search Slack | ai-community-slack-mcp | search |
| Read Slack channel | ai-community-slack-mcp | batch_get_conversation_history |
| Read Slack thread | ai-community-slack-mcp | batch_get_thread_replies |
| Draft Slack message | ai-community-slack-mcp | create_draft |
| Get meeting transcript | hedy | GetSessionDetails |
| Query PS metrics | duckdb | execute_query |
| Check security policy | arcc | search_arcc |
| Read SharePoint file | amazon-sharepoint-mcp | sharepoint_read_file |
| Read Loop page | loop-mcp or amazon-sharepoint-mcp | read_loop |
| Check weblab status | weblab-mcp | weblab_details, weblab_allocations |
| Check weblab history | weblab-mcp | weblab_activation_history |
| Read w.amazon.com wiki | xwiki-mcp | get_wiki_page |
| Read Quip document | builder-mcp | QuipEditor |
| Search internal docs | builder-mcp | InternalSearch |
| Look up employee | builder-mcp | ReadInternalWebsites (phonetool) |
| Read Taskei ticket | builder-mcp | TaskeiGetTask |
| Create Taskei ticket | builder-mcp | TaskeiCreateTask |
| Search code | builder-mcp | InternalCodeSearch |

---

## Auto-Approve Recommendations

Servers with no auto-approved tools require manual approval per call. Consider adding auto-approve for frequently used read-only tools:

- weblab-mcp: all 4 tools are read-only, safe to auto-approve
- xwiki-mcp: get_wiki_page is read-only, safe to auto-approve
- builder-mcp: ReadInternalWebsites, InternalSearch, QuipEditor (read mode), TaskeiGetTask, TaskeiListTasks are read-only and high-frequency for Richard's work

Richard should decide which to auto-approve based on usage patterns.
