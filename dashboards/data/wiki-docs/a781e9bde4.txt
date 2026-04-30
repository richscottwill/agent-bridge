# Outlook MCP for Kiro

**Doc:** 06
**Audience:** Paid Acquisition teammates + their Kiro agents
**Status:** FINAL
**Last updated:** 2026-04-17

## Environment Awareness (for your agent)

| Capability | Remote IDE (DevSpaces) | Local IDE (laptop Kiro) | AgentSpaces (chat) |
|---|---|---|---|
| Call Outlook MCP tools (email read/search, calendar view, drafts) | ✅ | ✅ | ✅ |
| Download email attachments to disk | ✅ to `/tmp/` | ✅ to `~/Downloads/` | ⚠️ Session-only |
| Parse attached .docx / .xlsx / .pdf | ✅ Python available | ✅ if Python installed | ❌ Punt to Remote or Local IDE |
| Open drafts in Outlook to send | ❌ No GUI; user opens Outlook Web | ✅ Outlook desktop app | ✅ User switches tabs |
| Run morning-brief hooks | ✅ Reliable | ⚠️ Only when laptop is awake | ❌ |

**If user asks you to parse an email attachment in AgentSpaces:** say something like *"I can read your emails here, but I can't open Excel spreadsheets, Word docs, or PDFs in this environment. If you want me to dig into an attachment, open Kiro on your laptop or your Remote IDE and ask me the same thing."*

---

- Outlook MCP gives your agent read access to your email and calendar, and the ability to create drafts (for you to send manually).
- It pairs well with Slack MCP — together they cover ~90% of PS communication triage.

**Hard rule reminder:** Your agent never sends, replies to, or forwards email without manual approval. Drafts only. See `kiro-no-external-write-rule.md`.

## Setup

Add to your Kiro MCP config (`.kiro/settings/mcp.json` inside the workspace you opened, or `~/.kiro/settings/mcp.json` for user-level):

```json
{
  "mcpServers": {
    "aws-outlook-mcp": {
      "command": "aim",
      "args": ["mcp", "start-server", "aws-outlook-mcp"],
      "env": {
        "OUTLOOK_MCP_ENABLE_WRITES": "true"
      },
      "disabled": false,
      "autoApprove": [
        "email_search",
        "email_read",
        "email_inbox",
        "email_folders",
        "email_list_folders",
        "email_contacts",
        "email_attachments",
        "email_categories",
        "email_update",
        "calendar_view",
        "calendar_search",
        "calendar_availability",
        "calendar_shared_list",
        "calendar_room_booking",
        "todo_lists",
        "todo_tasks",
        "todo_checklist"
      ]
    }
  }
}
```

First call triggers Midway auth.

**Notably NOT auto-approved:**
- `email_send`, `email_reply`, `email_forward` — external sends
- `email_draft` — safest kept manual, because of the `send: true` parameter footgun
- `calendar_meeting` — creates meetings that invite other people

- If you want email drafts to flow faster, you can add `email_draft` to autoApprove IF you never use `send: true` (always `operation: create` or `update`).
- Your call, but default is off.

## Starter prompts

- Copy-paste any of these to try Outlook.
- Rephrase to fit how you naturally ask.

**Catch up on your inbox**
- "Show me unread emails from the last 24 hours. For each: sender, subject, one-line summary, and whether I need to respond today."
- "Find emails from Brandon this week. Summarize what he's asked me."
- "Search my inbox for 'CA LP optimizations' — any attachments?"
- "Pull emails from external vendors (non-Amazon addresses) from the last 7 days."

**Calendar**
- "Show me tomorrow's calendar. For each meeting, pull any meeting notes from Loop or the invite body."
- "Do I have any conflicts this week?"
- "Who am I meeting most often this month?"
- "Find the WBR meeting for this week and tell me who's presenting."

**Draft an email (Kiro won't send it — you will)**
- "Draft an email to Brandon summarizing the Polaris template changes — save to drafts."
- "Draft a reply to this thread: [paste message URL or subject line]. Thank them and confirm next steps."
- "Draft a meeting recap to send to attendees from today's Polaris sync — save to drafts."

**Find an old email**
- "Find the email thread where Dwayne confirmed the AEM template update. Pull the most recent message."
- "Search sentitems for emails I sent to Lena in the last 2 weeks."

**Book a room or check availability**
- "Check availability between me, Brandon, and Lena tomorrow 9am–1pm PT."
- "Find a meeting room in SEA28 for Thursday 2pm that fits 6 people."

## Common patterns

### Morning triage chained with Slack

> "Triage my Slack and Outlook unread for the last 24 hours. For each item, flag: needs response today, can wait, FYI only. Group by channel/sender."
### Meeting prep

> "I've got a meeting with Brandon at 2pm. Pull the invite, any related emails from the last week, any Loop docs referenced, and give me a 5-point brief."

### Weekly report gathering

Paid acq folks often collect weekly updates across markets:

> "Find all emails marked with category 'WBR' from this week. Extract the key metrics and commentary per market."

### External vendor check-in

> "Which external vendors have I not replied to in 3+ days? Pull unanswered threads from non-Amazon domains."

## Search syntax tips

- Outlook search is natural language in the `query` field.
- Useful filters:.

- `subject: "..."` for exact subject match
- `from: person@amazon.com` for specific sender
- `hasattachments:yes`
- Date filters via `startDate` and `endDate` parameters (YYYY-MM-DD)
- `folder` parameter: `inbox`, `sentitems`, `drafts`, `archive`, `junkemail`, `deleteditems`

## Failure modes

- **"Cannot find email I just received"** → Outlook sync can lag 1–2 min. Wait or retry.
- **"Attachment download failed"** → Large attachments (>20MB) can time out. Open in Outlook Web directly.
- **Agent tries to send without asking** → Your autoApprove has `email_send` or `email_draft` with careless handling. Fix and restart.
- **"itemChangeKey invalid"** → You're trying to reply/forward an email using stale metadata. Re-read the email first to refresh the changeKey.
- **Calendar view returns empty** → Check the date range. Calendar tool treats dates as MM-DD-YYYY for `calendar_view`, ISO for others. Read the tool description.

## Calendar write rule

`calendar_meeting` is NOT on autoApprove because creating a meeting invites everyone on the attendee list — that's an external write. If you need to create meetings, approve each one manually. For personal-only blocks (no attendees), you can approve once and trust that pattern.

## Todo / Microsoft To-Do

- The `todo_*` tools let your agent manage your personal Microsoft To-Do lists.
- These ARE safe to auto-approve because they're writes to your own task lists — nobody else sees them.

Common pattern:

> "Create a To-Do task 'Follow up with Lena on MX budget' due tomorrow in my Today list."

## What not to use Outlook MCP for

- **Don't auto-send emails.** Even 'safe' ones. Drafts only.
- **Don't have your agent RSVP to meetings autonomously** (calendar_meeting rsvpResponse is a write that goes to the organizer).
- **Don't archive or delete emails in bulk without reviewing** — agent-parsed semantics can miss important context.
