---
inclusion: always
---

# Slack Communication Guardrails

## Messaging Rule

You may ONLY send Slack messages to Richard himself. This means:

1. **self_dm** — Always allowed. Use `self_dm` with login `prichwil` for notes, reminders, bookmarks.
2. **rsw-channel** (ID: `C0993SRL6FQ`) — Richard's private channel. Treat as equivalent to self. Posting here is always allowed.
3. **create_draft** — Always allowed. Drafts don't send anything — Richard reviews and sends manually.

## What is NOT allowed

- **post_message** to any channel other than `C0993SRL6FQ` (rsw-channel)
- **open_conversation** to DM anyone other than Richard
- **add_channel_members** — never without explicit Richard approval
- **create_channel** — never without explicit Richard approval

## When Richard asks you to message someone

Do NOT post directly. Instead:
1. Draft the message using `create_draft` with the target channel/thread
2. Tell Richard the draft is ready for review
3. Richard sends it manually

This mirrors the email rule: compose and draft, never send on Richard's behalf to others.

## Reading is unrestricted

All read operations (search, history, threads, channel info, user info, reactions, file downloads) are always allowed without restriction.

## Ingester Read Operations

During scheduled Slack ingestion (morning routine and system refresh hooks), the following read-only tools are permitted:
- `search` — keyword search across channels
- `batch_get_conversation_history` — retrieve channel messages
- `batch_get_thread_replies` — retrieve full thread context
- `batch_get_channel_info` — resolve channel metadata
- `batch_get_user_info` — resolve user names and profiles
- `reaction_tool` — read emoji reactions (get operation only)
- `download_file_content` — read shared files and canvases
- `list_channels` — discover channel membership

## Ingester Write Prohibitions

During ingestion cycles, the following tools are NEVER permitted:
- `post_message` — no posting to any channel during ingestion
- `open_conversation` — no opening new DM conversations during ingestion
- `add_channel_members` — no modifying channel membership during ingestion
- `create_channel` — no creating channels during ingestion

Exception: `self_dm` is permitted during ingestion to send status summaries to Richard's own DM (login: prichwil).

## Audit Logging

All Slack MCP tool invocations during ingestion cycles must be logged to `~/shared/context/active/slack-scan-state.json → tool_invocation_log` with timestamp, tool name, target channel, and result status.
