# Requirements Document

## Introduction

This document defines the requirements for Slack Context Ingestion — adding Slack as a context source for the Body system alongside the existing Hedy (meetings), Outlook (email/calendar), and Asana (tasks) integrations. The Slack MCP server (`ai-community-slack-mcp`) provides read access to all channels, DMs, threads, user profiles, and search. The challenge is not access — it's intelligent filtering. Slack is high-volume, high-frequency, and most of it is noise. The system must extract what matters (team decisions, project status changes, stakeholder signals, action items directed at Richard, hot topics surfacing) and route it to the right organs without bloating the system or creating new routines Richard has to manage.

Design principles governing this feature:
- **Subtraction before addition** — Slack context should replace manual context-gathering, not add monitoring burden
- **Invisible over visible** — Existing hooks should just have better context; no new visible "Slack step"
- **Routine as liberation** — Integrate into existing hooks (morning routine, autoresearch loop), don't create new ones
- **Structural over cosmetic** — Change what the system knows by default, not how it looks
- **Reduce decisions, not options** — The system decides what's relevant; Richard reviews only what surfaces

## Glossary

- **Slack_Ingester**: The module that reads Slack channels, DMs, and threads via the Slack MCP server and produces structured context for the Body system
- **Relevance_Filter**: The subsystem that scores and filters Slack messages by relevance to Richard's active projects, people, and priorities
- **Channel_Registry**: A configuration file mapping Slack channels to priority tiers, associated organs, and scan frequency
- **Slack_Digest**: A compressed summary of relevant Slack activity produced per ingestion cycle
- **Signal**: A discrete unit of relevant Slack context (decision, action item, status change, escalation, or sentiment shift) extracted from messages
- **Body_System**: The 11-organ AI context system managing Richard's working context
- **Morning_Routine**: The daily hook that reads fresh organs, syncs Asana, drafts replies, refreshes To-Do, produces a daily brief, and sets calendar blocks
- **Autoresearch_Loop**: The system refresh hook that maintains ground truth, cascades changes to organs, and runs experiments
- **Slack_MCP**: The `ai-community-slack-mcp` MCP server providing read access to Slack
- **Priority_Channel**: A Tier 1 Slack channel (core PS team) scanned on every ingestion cycle
- **Watch_Channel**: A Tier 2 Slack channel (adjacent/interest) scanned on reduced cadence or keyword-triggered
- **People_Watch**: The set of key people whose Slack messages are tracked regardless of channel
- **Knowledge_Search**: The subsystem that searches large community Slack channels as a supplementary knowledge base for technical topics, internal tooling questions, troubleshooting, and best practices — distinct from project-context search (Requirement 9)
- **Community_Channel**: A high-membership Slack channel (1K+ members) used as a knowledge source for technical topics, not tied to Richard's projects but to the broader Amazon builder community

## Requirements

### Requirement 1: Channel Registry and Tiered Scanning

**User Story:** As a system operator, I want a channel registry that classifies Slack channels into priority tiers, so that the ingester focuses on high-value channels and ignores noise.

#### Acceptance Criteria

1. THE Channel_Registry SHALL define three tiers: Tier 1 (Priority_Channel — scanned every cycle), Tier 2 (Watch_Channel — scanned daily or keyword-triggered), and Tier 3 (archive/ignore — never scanned)
2. WHEN the Slack_Ingester runs, THE Slack_Ingester SHALL scan all Tier 1 channels for messages posted since the last scan timestamp
3. WHEN the Slack_Ingester runs, THE Slack_Ingester SHALL scan Tier 2 channels only if the scan interval for that channel has elapsed since its last scan
4. THE Channel_Registry SHALL store for each channel: channel ID, channel name, tier, associated organ targets, scan interval, and keyword triggers
5. WHEN a new channel is discovered via `list_channels`, THE Slack_Ingester SHALL classify the channel as Tier 3 by default until Richard or the system promotes it
6. THE Channel_Registry SHALL be a plain markdown or JSON file in `~/shared/context/active/` that a new AI on a different platform can read without MCP access

### Requirement 2: Relevance Filtering and Signal Extraction

**User Story:** As a system operator, I want the ingester to filter Slack messages by relevance and extract discrete signals, so that only actionable context reaches the Body organs.

#### Acceptance Criteria

1. WHEN the Slack_Ingester retrieves messages from a channel, THE Relevance_Filter SHALL score each message against Richard's active projects (from current.md), key people (from memory.md), and hot topics (from the Channel_Registry keyword list)
2. WHEN a message mentions Richard by name or alias (`prichwil`, `@Richard`), THE Relevance_Filter SHALL classify the message as high-relevance regardless of other scoring
3. WHEN a message contains a decision, action item assignment, deadline, escalation, or status change related to an active project, THE Relevance_Filter SHALL extract a Signal with type, source channel, author, timestamp, and content summary
4. WHEN a message scores below the relevance threshold, THE Relevance_Filter SHALL discard the message without writing it to any organ or digest
5. THE Relevance_Filter SHALL not require Richard to configure relevance rules manually — the filter SHALL derive relevance from existing Body context files (current.md, memory.md, hands.md)
6. IF a thread has more than 5 replies, THEN THE Slack_Ingester SHALL retrieve the full thread via `batch_get_thread_replies` before scoring, because thread context changes relevance

### Requirement 3: People Watch — Key Person Tracking

**User Story:** As a system operator, I want the ingester to track messages from key people across all channels, so that important signals from Richard's manager, stakeholders, and direct collaborators are never missed.

#### Acceptance Criteria

1. THE People_Watch SHALL maintain a list of Slack user IDs for key people derived from memory.md relationship graph entries
2. WHEN a People_Watch person posts a message in any scanned channel, THE Relevance_Filter SHALL boost the relevance score for that message
3. WHEN Brandon Munday (Richard's manager) posts in any channel, THE Relevance_Filter SHALL classify the message as high-relevance regardless of content
4. WHEN a People_Watch person posts in a channel Richard is not a member of, THE Slack_Ingester SHALL still capture the Signal if the channel is Tier 1 or Tier 2
5. THE People_Watch list SHALL update automatically when memory.md relationship graph entries are added or removed, without requiring manual configuration
6. WHEN a new person appears in Slack conversations with Richard more than 3 times in a week, THE Slack_Ingester SHALL flag the person as a candidate for People_Watch addition

### Requirement 4: Slack Digest Production

**User Story:** As a system operator, I want the ingester to produce a compressed Slack digest per cycle, so that downstream processes (morning routine, autoresearch loop) can consume Slack context without reading raw messages.

#### Acceptance Criteria

1. WHEN the Slack_Ingester completes a scan cycle, THE Slack_Ingester SHALL produce a Slack_Digest file in `~/shared/context/intake/` containing all extracted Signals grouped by topic
2. THE Slack_Digest SHALL contain for each Signal: signal type (decision, action-item, status-change, escalation, mention, topic-update), source channel, author, timestamp, content summary (one to two sentences), and target organ recommendation
3. THE Slack_Digest SHALL not exceed 500 words per cycle to prevent organ bloat
4. WHEN no relevant Signals are found in a scan cycle, THE Slack_Ingester SHALL not produce a Slack_Digest file
5. THE Slack_Digest SHALL be plain markdown readable by any AI without MCP access or Slack connectivity
6. WHEN the Slack_Digest contains action items directed at Richard, THE Slack_Digest SHALL flag those items with a `[ACTION-RW]` prefix for priority routing to hands.md

### Requirement 5: Organ Routing and Context Cascade

**User Story:** As a system operator, I want Slack signals routed to the correct Body organs during the autoresearch loop cascade, so that Slack context enriches existing organs rather than creating new files.

#### Acceptance Criteria

1. WHEN the Autoresearch_Loop processes a Slack_Digest, THE Body_System SHALL route each Signal to the organ specified in the Signal's target organ recommendation
2. WHEN a Signal contains a project status change, THE Body_System SHALL update current.md with the new status information
3. WHEN a Signal contains a new action item for Richard, THE Body_System SHALL add the item to hands.md priority actions
4. WHEN a Signal contains relationship-relevant information (new person, tone shift, stakeholder position change), THE Body_System SHALL update memory.md relationship graph
5. WHEN a Signal contains market metrics or competitive intelligence, THE Body_System SHALL update eyes.md or write to the DuckDB analytics database
6. THE Body_System SHALL not create new organ files for Slack context — all Slack signals SHALL be absorbed into existing organs
7. WHEN a Signal has been routed to an organ, THE Body_System SHALL delete the processed Slack_Digest from intake/ to prevent reprocessing

### Requirement 6: Morning Routine Integration

**User Story:** As Richard, I want the morning routine daily brief to include relevant overnight Slack activity, so that I start the day knowing what happened in Slack without opening Slack first.

#### Acceptance Criteria

1. WHEN the Morning_Routine runs, THE Morning_Routine SHALL invoke the Slack_Ingester to scan for messages posted since the previous morning routine
2. WHEN the Slack_Ingester produces a Slack_Digest during the morning routine, THE Morning_Routine SHALL include a "Slack Overnight" section in the daily brief containing the top 5 Signals by relevance score
3. WHEN the "Slack Overnight" section contains action items directed at Richard, THE Morning_Routine SHALL add those items to the To-Do refresh step
4. THE "Slack Overnight" section SHALL not exceed 150 words in the daily brief to protect the existing brief format
5. WHEN no relevant Slack activity occurred overnight, THE Morning_Routine SHALL omit the "Slack Overnight" section entirely rather than showing an empty section
6. THE Morning_Routine SHALL not add a new user-visible step for Slack — the Slack scan SHALL execute as part of the existing organ-reading phase

### Requirement 7: Autoresearch Loop Integration

**User Story:** As a system operator, I want the autoresearch loop to ingest Slack context during its maintenance phase, so that organ updates reflect the latest Slack signals without a separate hook.

#### Acceptance Criteria

1. WHEN the Autoresearch_Loop runs Phase 1 (maintenance), THE Autoresearch_Loop SHALL invoke the Slack_Ingester as a data source alongside email and calendar scanning
2. WHEN the Autoresearch_Loop cascades changes to organs in Phase 2, THE Autoresearch_Loop SHALL include Slack-sourced Signals in the cascade input
3. THE Autoresearch_Loop SHALL not create a separate phase or step for Slack ingestion — Slack SHALL be one of multiple data sources in the existing maintenance phase
4. WHEN the Slack_Ingester encounters a rate limit or API error from the Slack_MCP, THE Autoresearch_Loop SHALL log the error and continue with other data sources without failing the entire loop run
5. THE Autoresearch_Loop SHALL track the last successful Slack scan timestamp in a state file so that subsequent runs pick up where the previous run left off

### Requirement 8: Scan State and Deduplication

**User Story:** As a system operator, I want the ingester to track scan state and deduplicate messages, so that the same Slack message is never processed twice across multiple ingestion cycles.

#### Acceptance Criteria

1. THE Slack_Ingester SHALL maintain a scan state file recording the last processed message timestamp per channel
2. WHEN the Slack_Ingester scans a channel, THE Slack_Ingester SHALL request only messages with timestamps newer than the last processed timestamp for that channel
3. WHEN the Slack_Ingester encounters a message it has already processed (by message timestamp and channel ID), THE Slack_Ingester SHALL skip the message without producing a duplicate Signal
4. WHEN the scan state file does not exist (first run or cold start), THE Slack_Ingester SHALL scan only the most recent 24 hours of messages per channel to avoid ingesting historical noise
5. THE scan state file SHALL be a plain JSON file in `~/shared/context/active/` that persists across sessions
6. WHEN the Slack_Ingester processes a message that is an edit of a previously processed message, THE Slack_Ingester SHALL update the existing Signal rather than creating a duplicate

### Requirement 9: Slack Search for On-Demand Context

**User Story:** As Richard, I want the system to search Slack on demand when preparing for meetings or drafting communications, so that the latest Slack context is available without waiting for the next scan cycle.

#### Acceptance Criteria

1. WHEN an agent prepares for a meeting with a specific person, THE Body_System SHALL search Slack for recent messages from that person using the `search` tool with the person's name or alias
2. WHEN an agent drafts a communication about an active project, THE Body_System SHALL search Slack for the project name or key terms to surface the latest discussion context
3. THE on-demand Slack search SHALL return results filtered by the same Relevance_Filter used in scheduled scans
4. WHEN on-demand search results contain Signals not yet captured by scheduled scans, THE Body_System SHALL add those Signals to the next Slack_Digest for organ processing
5. THE on-demand search SHALL not modify the scan state file — scheduled scans and on-demand searches SHALL operate independently

### Requirement 10: DM Monitoring for Direct Requests

**User Story:** As Richard, I want the system to monitor my Slack DMs for direct requests and action items, so that messages sent to me in Slack are captured with the same reliability as email.

#### Acceptance Criteria

1. WHEN the Slack_Ingester runs, THE Slack_Ingester SHALL scan Richard's DM conversations with People_Watch contacts for new messages
2. WHEN a DM contains a direct request or action item for Richard, THE Slack_Ingester SHALL extract a Signal with type `action-item` and flag it with `[ACTION-RW]`
3. WHEN a DM contains information relevant to an active project, THE Slack_Ingester SHALL extract a Signal and route it to the appropriate organ
4. THE Slack_Ingester SHALL respect the Slack communication guardrails — all DM scanning SHALL be read-only operations
5. WHEN a DM conversation has not had new messages since the last scan, THE Slack_Ingester SHALL skip that conversation without making API calls

### Requirement 11: Hot Topic Detection

**User Story:** As a system operator, I want the ingester to detect emerging hot topics across channels, so that Richard is alerted to new issues before they become urgent.

#### Acceptance Criteria

1. WHEN the same topic (keyword cluster or project name) appears in 3 or more channels within a 24-hour window, THE Slack_Ingester SHALL flag the topic as a hot topic in the Slack_Digest
2. WHEN a hot topic is detected, THE Slack_Digest SHALL include a summary of the topic with source channels, key participants, and a one-sentence synthesis
3. WHEN a hot topic relates to an active project in current.md, THE Slack_Ingester SHALL boost the relevance score of all messages in that topic cluster
4. WHEN a previously detected hot topic has had no new messages for 48 hours, THE Slack_Ingester SHALL mark the topic as cooled and stop boosting its relevance
5. THE hot topic detection SHALL operate on the Slack_Ingester's extracted Signals, not on raw message text, to avoid false positives from casual keyword mentions

### Requirement 12: Guardrail Compliance

**User Story:** As a system operator, I want the Slack ingester to comply with all existing Slack communication guardrails, so that the system never sends messages or modifies channels on Richard's behalf.

#### Acceptance Criteria

1. THE Slack_Ingester SHALL use only read operations from the Slack_MCP: `search`, `batch_get_conversation_history`, `batch_get_thread_replies`, `batch_get_channel_info`, `batch_get_user_info`, `reaction_tool`, `download_file_content`, and `list_channels`
2. THE Slack_Ingester SHALL not invoke `post_message`, `open_conversation`, `add_channel_members`, or `create_channel` during any ingestion cycle
3. WHEN the Slack_Ingester identifies an action item that requires a Slack response from Richard, THE Slack_Ingester SHALL add the item to hands.md with a note to respond via Slack, not attempt to draft or send a response
4. THE Slack_Ingester SHALL be permitted to use `self_dm` to send ingestion status summaries to Richard's own DM
5. THE Slack_Ingester SHALL log all Slack MCP tool invocations to the scan state file for audit purposes

### Requirement 13: Portability and Cold Start

**User Story:** As a system architect, I want the Slack ingestion configuration and state to be portable plain-text files, so that the system survives a platform move with nothing but text files.

#### Acceptance Criteria

1. THE Channel_Registry SHALL be a plain markdown or JSON file that documents channel names, IDs, tiers, and scan configuration in human-readable format
2. THE scan state file SHALL be a plain JSON file that a new AI can read to understand what has been scanned and when
3. THE Slack_Digest format SHALL be plain markdown with no dependencies on MCP tools, Slack API, or specific agent implementations
4. WHEN the system cold-starts on a new platform without Slack MCP access, THE Body_System SHALL continue functioning with stale Slack context — no organ SHALL fail because Slack data is unavailable
5. THE Slack_Ingester SHALL document its configuration, scan logic, and organ routing rules in a README file within the ingester's directory

### Requirement 14: Volume Control and Bloat Prevention

**User Story:** As a system architect, I want hard limits on how much Slack context enters the Body system per cycle, so that Slack's high volume does not bloat organs beyond their word budgets.

#### Acceptance Criteria

1. THE Slack_Digest SHALL enforce a hard cap of 500 words per ingestion cycle
2. WHEN the Relevance_Filter produces more Signals than fit within the word cap, THE Relevance_Filter SHALL rank Signals by relevance score and include only the top-ranked Signals
3. WHEN Slack-sourced content is cascaded to an organ, THE Body_System SHALL check the organ's word budget (from gut.md) before writing and compress or defer content if the organ is at capacity
4. THE Slack_Ingester SHALL track cumulative words added to each organ from Slack sources per week and report the total in the scan state file
5. WHEN cumulative Slack-sourced words for an organ exceed 20% of that organ's word budget in a single week, THE Slack_Ingester SHALL reduce the scan frequency for channels feeding that organ until the next weekly reset

### Requirement 15: Slack as Knowledge Base for Technical Topics

**User Story:** As Richard, I want the system to proactively search large community Slack channels when I ask about internal tooling, AI frameworks, or Amazon-specific technical topics, so that I benefit from the collective knowledge of thousands of Amazonians without manually searching Slack.

#### Acceptance Criteria

1. WHEN an agent encounters a question about MCP servers, CLI tools, Kiro features, AgentSpaces, Bedrock, or Amazon internal tooling that the agent cannot fully answer from its own knowledge, THE Body_System SHALL search Community_Channels via the Slack_MCP `search` tool for relevant discussions, solutions, and troubleshooting threads
2. THE Channel_Registry SHALL maintain a Community_Channel list for Knowledge_Search, including at minimum: `agentspaces-interest` (C0A1JD8FCUV, 15K+ members), `amazon-builder-genai-power-users` (C08GJKNC3KM, 35K+ members), `cps-ai-win-share-learn` (C09LU3K7KS8, 5K+ members), `bedrock-agentcore-interest` (C096H6QNW6M, 7K+ members), `abma-genbi-analytics-interest` (C0A1J4QG3CY, 141 members), and `andes-workbench-interest` (C096T4SK3EY, 20K+ members)
3. WHEN the Knowledge_Search returns relevant threads, THE Body_System SHALL retrieve full thread replies via `batch_get_thread_replies` to capture answers and follow-up context, not just the initial question
4. WHEN the Knowledge_Search finds a solution or best practice in a community thread, THE Body_System SHALL present the answer to Richard with attribution (author, channel, timestamp, thread link) so Richard can verify and follow up
5. THE Knowledge_Search SHALL operate independently from the scheduled Slack_Ingester scans — Knowledge_Search queries SHALL be triggered on demand by the agent's reasoning process, not by scan cycles
6. WHEN the Knowledge_Search retrieves results, THE Body_System SHALL filter results by recency (prefer threads from the last 90 days) and engagement (prefer threads with replies over unanswered questions)
7. THE Knowledge_Search SHALL not write results to Body organs or produce Slack_Digests — results SHALL be presented directly to Richard in the conversation context as supplementary evidence
8. WHEN the agent searches a Community_Channel for a topic and finds no relevant results, THE Body_System SHALL note the gap and proceed with its own knowledge rather than reporting a failed search to Richard