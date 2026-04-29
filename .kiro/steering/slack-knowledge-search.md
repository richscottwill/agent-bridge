---
inclusion: fileMatch
fileMatchPattern: ["hooks/*slack*"]
---

# Slack Knowledge Search

## Two Search Modes

There are two distinct ways the system searches Slack:

### 1. Ingestion + Proactive Search (scheduled — runs during morning routine and system refresh)
- **Channel ingestion:** Every cycle, call `list_channels` to get Richard's full channel list. His sidebar sections (WW Testing, AB PS, AB, AI, Channels) determine scan depth. All DMs with new messages get full ingestion. No static channel list — Slack is the source of truth.
- **Proactive search:** Goes BEYOND Richard's channel list. Permanent queries (prichwil, "Richard Williams", from:@brandoxy, from:@kataxt) always run. Dynamic queries are constructed fresh each cycle based on today's context — projects, meetings, pending actions, hot topics.
- **Reaction checking:** For messages tagging Richard, check emoji reactions to determine if he's already acknowledged them.
- Strategy defined in `slack-channel-registry.json` (ingestion rules, search framework, reaction semantics, people watch).
- This is signal detection. It writes to organs via the digest.

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


> **Example:** A typical use of this section involves reading the above rules and applying them to the current context.
## How to Search

1. Use the `search` tool with the topic as query
2. Community channels are in Richard's channel list under the "AI" and "Channels" sections — use those as primary search targets
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
