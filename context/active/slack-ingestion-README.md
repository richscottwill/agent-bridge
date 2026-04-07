<!-- DOC-0362 | duck_id: protocol-slack-ingestion-README -->
# Slack Context Ingestion - README

Read-only Slack context source for the Body system. Extracts decisions, action items, status changes, escalations, and hot topics from Slack channels and routes them to existing organs. No new hooks, agents, or organ files.

## Configuration Files

| File | Location | Purpose |
|------|----------|--------|
| Channel Registry | ~/shared/context/active/slack-channel-registry.json | Channel tiers, People Watch, community channels |
| Scan State | ~/shared/context/active/slack-scan-state.json | Timestamps, hot topics, volume tracking, audit log |
| Knowledge Search | ~/.kiro/steering/slack-knowledge-search.md | On-demand community channel search rules |
| Slack Guardrails | ~/.kiro/steering/slack-guardrails.md | Read-only enforcement, ingester rules |

## Tiered Scanning

| Tier | Behavior | Examples |
|------|----------|--------|
| 1 (Priority) | Scanned every cycle | ab-paid-search-global, ab-ps_jp, ab-paid-search-oci, rsw-channel |
| 2 (Watch) | Scanned on interval or keyword trigger | baloo-search-and-mcs (24h), ext-apptweak (48h) |
| 3 (Ignore) | Never scanned | Default for new channels |

Community channels (agentspaces-interest, amazon-builder-genai-power-users, etc.) are knowledge-search-only.

## Relevance Filter

Scoring model (points additive, threshold: 25):

| Factor | Points | Source |
|--------|--------|--------|
| Direct mention (prichwil, @Richard) | +100 | Message text |
| Manager message (Brandon Munday) | +100 | People Watch |
| People Watch boosted contact | +30 | Channel registry |
| Active project keyword | +25 | current.md |
| Channel keyword trigger | +20 | Channel registry |
| Tier 1 channel | +15 | Channel registry |
| Decision language | +20 | Pattern match |
| Action assignment | +25 | Pattern match |
| Deadline language | +15 | Pattern match |
| Escalation language | +20 | Pattern match |
| Hot topic cluster | +15 | Scan state |
| Thread > 5 replies | +10 | Thread metadata |

Score < 25: discard. 25-99: include if within word cap. 100+: always include.

## Signal Types

| Type | Triggers | Example |
|------|----------|--------|
| decision | decided, approved, confirmed | Going with DE + FR for first weblab wave |
| action-item | @prichwil, Richard to, can you | Richard, prep AU CPC data by Thursday |
| status-change | launched, completed, blocked | Polaris weblab confirmed for April 7 |
| escalation | escalated, urgent, blocker | APAC MCC access blocked |
| mention | prichwil, @Richard | Richard had a good point about... |
| topic-update | 3+ channels, 24h window | Cross-channel OCI timeline convergence |

## Organ Routing

| Signal Type | Primary Organ | Secondary Organ |
|-------------|--------------|----------------|
| decision | brain.md | current.md |
| action-item | hands.md | current.md |
| status-change | current.md | eyes.md |
| escalation | current.md | hands.md |
| mention | current.md | - |
| topic-update | current.md | brain.md |
| Relationship info | memory.md | - |
| Market metrics | eyes.md | - |

All Slack-sourced facts include [Slack: #channel, author, date] attribution tag.

## Digest Format

- File: ~/shared/context/intake/slack-digest-{YYYY-MM-DD-HHmm}.md
- Hard cap: 500 words per cycle
- [ACTION-RW] prefix for Richard's action items
- No digest if zero relevant signals
- Transient: processed during intake digestion, then deleted

## Volume Control

1. Per-cycle: 500 word digest cap
2. Per-organ: check gut.md word budget before writing; compress or defer if at capacity
3. Per-week: cumulative tracking. If >20% of organ budget from Slack, reduce scan frequency

Ceilings: Memory 700w/week, Brain 500w, Eyes 500w, Hands 400w, current.md flag at 500w.

## Hot Topic Detection

- Trigger: same topic in signals from 3+ channels within 24 hours
- Boost: +15 relevance (+25 if related to active project)
- Cooling: no new signals for 48h, move to cooled, stop boosting

## People Watch

- Derived from memory.md Relationship Graph (auto-refresh during system refresh)
- always_high_relevance: Brandon Munday (manager) +100
- boosted: contacts with interaction in last 60 days +30
- New person detection: 3+ interactions in 7 days, flagged as candidate

## Knowledge Search (On-Demand)

- Triggered when agent hits knowledge gap on internal tooling, MCP, Kiro, etc.
- Searches community channels (35K+ members in amazon-builder-genai-power-users, etc.)
- Prefers threads from last 90 days with replies
- Results in conversation with attribution, NOT written to organs
- Independent from scheduled scans
- Steering: ~/.kiro/steering/slack-knowledge-search.md (manual inclusion)

## Integration Points

- Morning Routine: Slack scan in CONTEXT LOAD (item 9). Slack Overnight in daily brief (150 word cap, omitted if no activity).
- System Refresh: Slack ingestion in Phase 1. Signal routing in Phase 2 Cascade.
- No new hooks, phases, or steps.

## Cold Start and Error Handling

- Missing scan state: scan last 24h only
- Slack MCP unavailable: hooks run normally without Slack
- Rate limits: log, skip remaining channels, resume next cycle
- All tool invocations logged for audit

## Canvas Capability Status

**Validated: 2026-04-01** — The ai-community-slack-mcp server does NOT support canvas create or update operations. Available tools include `download_file_content` (which can read existing canvases) but there is no `canvas_create`, `canvas_update`, or equivalent tool.

**Impact:** The Live Dashboard in rsw-channel is implemented as a **pinned message** (not a canvas). Updates are done via message editing (`post_message` for initial post, then editing the pinned message). The message timestamp is stored in `slack-scan-state.json → dashboard.message_ts` for future edits.

**Re-check cadence:** If the Slack MCP server adds canvas tools in a future update, the dashboard can be migrated to a canvas. Check tool list periodically.

## Guardrails

- Read-only ONLY during ingestion
- Never: post_message, open_conversation, add_channel_members, create_channel
- Permitted: self_dm for status summaries to Richard
