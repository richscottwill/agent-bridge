---
inclusion: manual
---

# Slack Knowledge Search

## When to Search

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
- Do NOT search community channels during scheduled ingestion scans — they are knowledge sources only

## Community Channels

Maintained in slack-channel-registry.json → community_channels section.
Minimum set: agentspaces-interest, amazon-builder-genai-power-users,
cps-ai-win-share-learn, bedrock-agentcore-interest, abma-genbi-analytics-interest,
andes-workbench-interest.
