# No-External-Write Rule + MCP Safety Config

**Doc:** 02
**Audience:** Paid Acquisition teammates + their Kiro agents
**Status:** FINAL
**Last updated:** 2026-04-17

## Environment Awareness (for your agent)

The rule below applies identically across every environment — no exceptions. Environment only affects *where* the config file lives:

| Capability | Remote IDE (DevSpaces) | Local IDE (laptop Kiro) | AgentSpaces (chat) |
|---|---|---|---|
| Edit your Kiro MCP config (`.kiro/settings/mcp.json` inside the workspace you opened, or `~/.kiro/settings/mcp.json` for user-level) | ✅ (container-scoped config) | ✅ (laptop Kiro config) | ❌ Ask user to edit via Remote or Local IDE |
| Verify autoApprove list | ✅ Read the file directly | ✅ Read the file directly | ⚠️ Ask user to paste the file contents |
| Test the rule is working | ✅ Run verification prompts | ✅ Run verification prompts | ✅ Run verification prompts |

**The rule itself is environment-independent.** Writing-to-self is always safe; writing to others always needs manual approval, no matter where you're running.

---

## The rule

**Agents never send, post, reply, comment, or forward to anyone but the user themselves.**

All external communication goes through drafts. The user reviews and sends manually.

Writing to yourself is fine. Drafts are fine. Reads are fine. The line is external output — anything another human will receive from your account without you personally approving it.

## Why this exists

A rogue auto-send erodes trust faster than any amount of good agent output builds it. The first time your agent emails your VP the wrong summary, or posts to a team channel with half-cooked context, you lose permission to use Kiro for external comms for months. This rule keeps that from ever happening.

## Whitelist (writing to yourself is fine)

Auto-approve these freely:

- `self_dm` in Slack (DM to yourself)
- `create_draft` (Slack or email)
- Writing files to your personal OneDrive
- Creating calendar blocks on your own calendar
- Creating/updating your own Asana tasks
- Saving to `/workspace/` or `~/shared/` in DevSpaces

## Blacklist (never auto-approve)

These require manual user approval every single time:

### Slack
- `post_message` (unless the channelId is confirmed as user's self-DM channel)
- Posts to any channel — even "safe" ones

### Outlook
- `email_send`
- `email_reply`
- `email_forward`
- Creating/updating meetings that go to other attendees

### Asana
- `CreateTaskStory` (comments) on tasks the user doesn't own
- Status changes on tasks where user isn't the assignee or owner
- Task creation in projects the user doesn't own

### SharePoint / OneDrive
- Writing to any `siteUrl` other than the user's personal OneDrive
- Writing to shared team-site libraries
- Editing Loop docs or shared Office files that other people own

### Any MCP that posts to external systems
- Weblab changes
- Public-facing wiki edits
- Any ticket/SIM creation assigned to someone else

## Canonical MCP autoApprove lists

Paste these into your Kiro MCP config (`.kiro/settings/mcp.json` inside the workspace you opened, or `~/.kiro/settings/mcp.json` for user-level) as the `autoApprove` arrays for each server. These are the safe defaults — your agent can do plenty without being able to send anything externally.

### Slack

```json
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
```

Notably NOT on this list: `post_message`, `add_channel_members`, `create_channel`.

### Outlook

```json
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
```

Note: `email_draft` CAN be safely auto-approved IF you only use it with `operation: create` or `update`. It gets dangerous if you auto-approve the `send: true` parameter. Safest is to keep `email_draft` off autoApprove and manually approve each draft creation.

Notably NOT on this list: `email_send`, `email_reply`, `email_forward`, `calendar_meeting` (creates meetings that invite others).

### Asana

```json
"autoApprove": [
  "AsanaSearch",
  "GetCurrentUser",
  "GetProject",
  "GetProjectSections",
  "GetProjectTaskCount",
  "GetProjectsForTask",
  "GetTaskDetails",
  "GetTaskStories",
  "GetTasksFromProject",
  "GetUserTasks",
  "GetSubtasksForTask",
  "GetAllPortfolios",
  "GetPortfolioItems",
  "GetGoal",
  "GetStatusUpdate",
  "GetStatusUpdatesFromObject",
  "GetStoriesForTask",
  "SearchTasksInWorkspace"
]
```

Notably NOT on this list: `CreateTask`, `UpdateTask`, `CreateTaskStory`, `AddTagForTask`, `RemoveTagForTask`, `SetParentForTask`, `UpdateStory`. Writes require manual approval.

### SharePoint / OneDrive

```json
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
```

`sharepoint_write_file` is on this list because it defaults to personal OneDrive (writing to yourself = fine). Your agent still can't write to team sites without you passing `personal=false` + `siteUrl`, which is a manual parameter choice.

Notably NOT on this list: `sharepoint_delete_file`, `sharepoint_rename_folder` — destructive, keep manual.

## Verification checklist

After setting up your MCP config, verify the rule is holding by running these prompts and confirming your agent pauses for approval:

1. **Slack:** "Post a test message to #general saying hello." → Should ask for approval.
2. **Slack self-DM:** "Send a DM to myself with a note to buy milk." → Should proceed without asking.
3. **Outlook:** "Send an email to my manager saying I'll be out tomorrow." → Should ask for approval.
4. **Outlook draft:** "Draft an email to my manager saying I'll be out tomorrow and save to drafts." → Should proceed (or ask once — that's fine).
5. **Asana:** "Add a comment on Brandon's current task saying I'll handle it." → Should ask for approval.

If any of those proceed without asking on #1, #3, or #5, your autoApprove list has the wrong items. Fix and retest.

## If your agent posts something without asking

1. Delete/retract the post immediately via the original platform.
2. Check your `mcp.json` — you almost certainly have a write operation on the autoApprove list that shouldn't be.
3. Remove it. Restart Kiro.
4. Drop a note in `~/shared/wiki/intake/suggestions/` so the team can improve this doc.

## Steering file

Install this at your Kiro steering folder as `no-external-write-rule.md` (in `.kiro/steering/` inside your workspace, or `~/.kiro/steering/` for user-level) so the rule auto-loads into every conversation:

```markdown
---
inclusion: always
---

# No-External-Write Rule

Agents never send, post, reply, comment, or forward to anyone but the user themselves. All external communication goes through drafts. The user reviews and sends manually.

Whitelist (safe to do automatically):
- self_dm in Slack
- Draft creation (Slack drafts, email drafts)
- Writing files to personal OneDrive or ~/shared/
- Creating calendar blocks on user's own calendar
- Creating/updating tasks the user owns

Blacklist (always require user approval):
- Slack post_message to any channel
- email_send, email_reply, email_forward
- Comments or status changes on tasks the user doesn't own
- Writes to any SharePoint site other than personal OneDrive
- Any operation that surfaces to another human without user review

If a user request would require a blacklist operation, produce a draft instead and tell the user where it is and how to send it.
```

## Rules for good steering of this kind

- Keep it short — this steering loads into every conversation.
- State the rule, not the rationale.
- Be explicit about the whitelist and blacklist so the agent doesn't have to infer.
