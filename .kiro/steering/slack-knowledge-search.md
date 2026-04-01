---
inclusion: manual
---

# Slack Knowledge Search

## Two Search Modes

There are two distinct ways the system searches Slack:

### 1. Proactive Search (scheduled — runs during ingestion)
- Defined in `slack-channel-registry.json → proactive_searches`
- Runs keyword queries during morning routine and system refresh alongside channel scans
- Catches signals from channels Richard isn't in, DMs, and cross-org threads
- Results go through the same relevance filter as channel messages → routed to organs
- Queries cover: key people (from:@brandoxy, etc.), active projects (OCI, Polaris, Baloo), interests (Kiro, GenBI, AgentSpaces), and org affiliation (Amazon Business, paid acquisition)
- This is NOT knowledge search — it's signal detection. It writes to organs.

### 2. Knowledge Search (on-demand — triggered by conversation)
- Triggered by Richard's questions or agent reasoning during live chat
- Searches community channels for technical knowledge, best practices, and community experience
- Results are presented in conversation, NOT written to organs
- This file governs knowledge search behavior

## When to Use Knowledge Search

Search community Slack channels when:
1. Richard asks about MCP servers, CLI tools, Kiro features, AgentSpaces, Bedrock,
   or Amazon internal tooling that you cannot fully answer from your own knowledge
2. You encounter a technical question where community experience would add value
3. Richard explicitly asks "what are people saying about X" or "search Slack for X"

## How to Search

1. Use the `search` tool with the topic as query
2. Filter by community channels listed in slack-channel-registry.json → community_channels
3. Prefer threads from the last 90 days
4. Prefer threads with replies over unanswered questions
5. For relevant threads, retrieve full replies via `batch_get_thread_replies`

## How to Present Results

- Include attribution: author, channel, timestamp, thread link
- Present as supplementary evidence in the conversation, not as authoritative answers
- Let Richard verify and follow up

## What NOT to Do

- Do NOT write Knowledge Search results to Body organs or produce Slack Digests
- Do NOT modify scan state — Knowledge Search operates independently from scheduled scans
- Do NOT report failed searches to Richard — note the gap internally and proceed with your own knowledge

## Community Channels

Maintained in slack-channel-registry.json → community_channels section.
Minimum set: agentspaces-interest, amazon-builder-genai-power-users,
cps-ai-win-share-learn, bedrock-agentcore-interest, abma-genbi-analytics-interest,
andes-workbench-interest.
