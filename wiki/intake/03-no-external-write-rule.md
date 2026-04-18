# No-External-Write Rule + MCP Safety Config

**Audience:** Kiro agents acting on behalf of Paid Acquisition teammates.
**Purpose:** Prevent the first "my agent emailed my VP" incident. This is a hard rule enforced by configuration, not discretion.
**Status:** READY

## The hard rule

Agents **never** send, post, reply, comment, or forward to anyone but the user themselves. Every external-facing write goes through a draft the user reviews and sends manually.

**Allowed (writing to self):**
- Personal OneDrive files
- Slack `self_dm` (DM to yourself)
- Own calendar blocks, own drafts folder
- Own Asana tasks, own notes, own comments on tasks you own
- Any file in `~/shared/`, `/workspace/`, local IDE workspace

**Forbidden without explicit user instruction in that turn:**
- Slack `post_message` (except to the user's own DM channel)
- Outlook `email_send`, `email_reply`, `email_forward`
- Asana `CreateTaskStory` (comments) on tasks the user doesn't own
- Loop writes to docs shared with others
- SharePoint writes outside the user's own OneDrive
- Any write to a channel, group, or distribution list

## Why configuration, not discretion

Relying on the agent to remember the rule in every context is fragile. Wrong prompt + one forgetful turn = embarrassing message sent. The fix is to strip dangerous tools from `autoApprove` so each write requires a visible click from the user.

## Canonical autoApprove lists

Copy these into `~/.kiro/settings/mcp.json`. Any write tool not listed requires manual approval in chat.

### SharePoint / OneDrive

```json
"amazon-sharepoint-mcp": {
  "autoApprove": [
    "sharepoint_search",
    "sharepoint_list_sites",
    "sharepoint_list_libraries",
    "sharepoint_list_files",
    "sharepoint_read_file",
    "sharepoint_read_loop",
    "sharepoint_resolve_url",
    "sharepoint_write_file",
    "sharepoint_create_folder"
  ]
}
```

**Note:** `sharepoint_write_file` and `sharepoint_create_folder` are auto-approved because the default target is your own OneDrive. The agent's protocol (see `02-agent-sharepoint-protocol.md`) enforces the `personal=true` default; writes to team sites still require you pass `personal=false` + `siteUrl` explicitly, which surfaces in chat.

### Slack

```json
"ai-community-slack-mcp": {
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
    "open_conversation"
  ]
}
```

**Explicitly NOT auto-approved:**
- `post_message` — can post anywhere you have access to
- `add_channel_members` — visible to members
- `create_channel` — creates team-visible channels
- `reaction_tool` — visible to everyone in the channel

### Outlook

```json
"aws-outlook-mcp": {
  "autoApprove": [
    "email_search",
    "email_read",
    "email_folders",
    "email_list_folders",
    "email_inbox",
    "email_contacts",
    "email_attachments",
    "email_categories",
    "calendar_view",
    "calendar_search",
    "calendar_availability",
    "calendar_room_booking",
    "calendar_shared_list",
    "todo_lists",
    "todo_tasks",
    "todo_checklist"
  ]
}
```

**Explicitly NOT auto-approved:**
- `email_send`, `email_reply`, `email_forward` — always manual
- `email_draft` — OK to auto-approve once you're confident, but start manual
- `email_move`, `email_update` — can hide or miscategorize emails
- `calendar_meeting` create/update/delete — affects others' calendars

### Asana

```json
"enterprise-asana-mcp": {
  "autoApprove": [
    "AsanaSearch",
    "GetCurrentUser",
    "GetAllPortfolios",
    "GetPortfolioItems",
    "GetProject",
    "GetProjectSections",
    "GetProjectTaskCount",
    "GetProjectsForTask",
    "GetStatusUpdate",
    "GetStatusUpdatesFromObject",
    "GetStoriesForTask",
    "GetSubtasksForTask",
    "GetTaskDetails",
    "GetTaskStories",
    "GetTasksFromProject",
    "GetUserTasks",
    "SearchTasksInWorkspace",
    "GetGoal"
  ]
}
```

**Explicitly NOT auto-approved (for new users):**
- `CreateTask` — OK once comfortable; can spam a project
- `UpdateTask` — affects task state others may track
- `CreateTaskStory` — comments visible to followers
- `UpdateStory` — edits comments
- `AddTagForTask`, `RemoveTagForTask`, `SetParentForTask` — structural changes

Experienced users may graduate Asana writes to auto-approve once they trust their agent.

### Loop, Weblab, Arcc, Knowledge Discovery

Keep disabled until needed. When enabled, auto-approve reads only.

## Verification checklist

Run through this after editing `mcp.json`:

1. **Restart MCP servers** — Kiro panel → MCP Servers → restart, or reload window.
2. **Ask your agent:** "What's in my inbox?" — should read without prompting approval.
3. **Ask your agent:** "Send an email to Brandon saying hi" — should surface an approval dialog or refuse and offer a draft. If it sends without asking, your config has `email_send` in `autoApprove`. Remove it.
4. **Ask your agent:** "Post a message to #ps-team saying hi" — same check. Should refuse or ask.
5. **Ask your agent:** "Save a note to my OneDrive" — should write without prompting (writing to self is allowed).

If any of the first two external-write tests auto-fires, your config needs fixing before you trust the agent.

## The draft-first pattern

When your agent needs to communicate externally, the workflow is:

1. Agent drafts the message (email, Slack post, Asana comment).
2. Agent surfaces the draft in chat and states where it will go.
3. Agent calls the `_draft` variant of the tool (e.g., `email_draft`, Slack `create_draft`) so the draft appears in your Outlook Drafts or Slack draft list.
4. You review in the real UI and hit send yourself.

This is the single safest pattern for team-facing communication. Every doc in this kit follows it.

## Exceptions

If you explicitly ask the agent to "send this email" or "post this to Slack" in the same turn, the agent will surface an approval dialog for the write — that's expected. The rule isn't "never write externally" — it's "never auto-write externally." The user click is the safety valve.

## If something goes wrong

If your agent posted or sent something you didn't intend:

1. Retract immediately (unsend email, delete Slack message — both have time windows).
2. Check `autoApprove` for the tool that fired. Remove it.
3. Restart MCP servers.
4. Report the pattern to Richard so we can update this doc.
