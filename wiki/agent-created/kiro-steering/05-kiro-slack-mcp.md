# Slack MCP for Kiro

**Doc:** 05
**Audience:** Paid Acquisition teammates + their Kiro agents
**Status:** FINAL
**Last updated:** 2026-04-17

## Environment Awareness (for your agent)

| Capability | Remote IDE (DevSpaces) | Local IDE (laptop Kiro) | AgentSpaces (chat) |
|---|---|---|---|
| Call Slack MCP tools (search, read, drafts, self-DM) | ✅ | ✅ | ✅ |
| Download file attachments to disk | ✅ to `/tmp/` | ✅ to laptop | ⚠️ Session-only, no persistent path |
| Post drafts for user to review in Slack app | ✅ (user opens Slack in browser/app) | ✅ (Slack desktop app) | ✅ (user switches to Slack tab) |
| Run hooks that triage Slack daily | ✅ Container persists | ⚠️ Only when laptop is on | ❌ No hooks |

**The hard rule (`post_message` requires manual approval) is enforced by autoApprove list, not by environment.** Works identically everywhere.

---

Slack MCP gives your agent read access to your Slack workspace and the ability to draft messages (for you to send manually). It is probably the highest-leverage MCP after OneDrive for daily PS work — inbox triage, thread lookup, finding files teammates sent, weekly summary of what's happening.

**Hard rule reminder:** Your agent never posts to channels or DMs other people without manual approval. Drafts and `self_dm` only. See `kiro-no-external-write-rule.md` for the full rule.

## Setup

Add to your Kiro MCP config (`.kiro/settings/mcp.json` inside the workspace you opened, or `~/.kiro/settings/mcp.json` for user-level):

```json
{
  "mcpServers": {
    "ai-community-slack-mcp": {
      "command": "aim",
      "args": ["mcp", "start-server", "ai-community-slack-mcp"],
      "disabled": false,
      "autoApprove": [
        "search",
        "list_channels",
        "batch_get_conversation_history",
        "batch_get_thread_replies",
        "batch_get_channel_info",
        "batch_get_user_info",
        "get_channel_sections",
        "download_file_content",
        "list_drafts",
        "lists_items_list",
        "lists_items_info",
        "self_dm",
        "create_draft",
        "batch_set_last_read",
        "open_conversation",
        "reaction_tool"
      ]
    }
  }
}
```

First call triggers auth. Follow the prompts. Cookie caches for the session.

**Notably NOT auto-approved:** `post_message`, `add_channel_members`, `create_channel`. These require manual approval every time. Keep it that way.

## Starter prompts

Copy and paste any of these into your Kiro chat to try Slack. No setup required once the server's running. These are meant to sound the way you'd actually ask — feel free to rephrase.

**Catch up on what you missed**
- "Summarize my unread Slack messages from the last 24 hours. Group by channel."
- "What's happening in #ps-au-mx this week? Pull the main threads."
- "List channels with unread mentions, sorted by mention count."

**Find something specific**
- "Find Slack messages where Brandon mentioned 'Polaris' in the last 2 weeks."
- "Search Slack for the CA LP optimizations deck Adi sent."
- "What did Yun say about ad copy testing recently?"

**Draft a reply or message (Kiro won't send it — you will)**
- "Draft a reply to the top message in this thread: [paste URL]"
- "Draft a Slack message to post in #ps-team thanking Adi for the MX LP work — don't send, just draft."
- "Send a DM to myself as a reminder to follow up with Lena tomorrow about the MX budget."

**Get the gist of a long thread**
- "Pull the full thread at [paste Slack message URL] and tell me the decision."
- "Who's currently waiting on me in my DMs?"

## Common patterns

### Morning inbox triage

Every morning, ask:

> "Scan my unread Slack messages. For each: tell me who sent it, summarize the ask in one line, and flag whether I need to respond today. Don't draft replies yet."

Then selectively ask your agent to draft replies to the ones that matter.

### Finding the file someone sent you

Slack search returns both messages and files. If a teammate shared a deck, Excel, or PDF:

> "Find the file '[filename]' in my Slack DMs from [person]."

Or by topic:

> "Search Slack for 'pacing Excel' in my DMs and list any file attachments."

### Summarizing a channel while you were out

> "I was out Monday–Wednesday. Summarize what happened in #ps-au-mx during that time. Group by topic and flag anything that needs my input."

### Weekly retrospective

> "Pull messages I sent across all channels this week. Summarize what I was working on, who I collaborated with, and any open loops."

## Search modifier cheatsheet

Slack search supports modifiers. Your agent can use these directly:

| Modifier | What it does | Example |
|---|---|---|
| `in:#channel` | Search within a channel | `Polaris in:#ps-ww` |
| `from:@alias` | Messages from a person | `MX LP from:@brandonm` |
| `with:@alias` | DMs/threads with a person | `budget with:@lenac` |
| `before:date` / `after:date` / `on:date` | Time ranges | `after:2026-04-01` |
| `has::emoji:` | Messages with a reaction | `has::eyes:` |
| `is:thread` | Only threaded replies | `is:thread error` |
| `is:saved` / `has:pin` | Saved or pinned items | `is:saved` |
| `-in:` / `-from:` | Exclude | `-in:#general` |

Example: `Polaris from:@brandonm after:2026-04-01 -in:#random` = all of Brandon's Polaris mentions since April 1, excluding the #random channel.

## Failure modes

- **"I can't see that channel"** → your account isn't in the channel. Slack MCP only sees what you see. Join the channel or ask someone to add you.
- **"Draft didn't show up"** → drafts live in Slack's drafts list, not as messages. Click the pencil/compose icon in Slack to find them.
- **Agent tries to post without asking** → your `autoApprove` has `post_message` on it. Remove it. Restart.
- **Search returns nothing for a known message** → Slack search index has lag (~5 min). Retry, or fall back to `batch_get_conversation_history` with a time range.

## What not to use Slack MCP for

- **Don't use it to auto-post status updates.** Post manually so you actually read what's going out.
- **Don't use it to bulk-react with emojis to look engaged.** Either engage or don't.
- **Don't use it to auto-reply while you're in meetings.** Drafts are fine; auto-sends are not.
