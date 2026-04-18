# Asana ↔ To-Do Sync Protocol

Last updated: 2026-03-20

## Purpose
Syncs Asana task activity into Microsoft To-Do by scanning Outlook's Auto-Comms folder for Asana notification emails. This is a workaround because the agent cannot access Asana directly.

## Prerequisites
- **Outlook MCP** (`aws-outlook-mcp`) must be connected with these tools available:
  - `email_search` — search emails in a folder
  - `email_read` — read full email body
  - `todo_tasks` — CRUD on To-Do tasks
  - `todo_lists` — list To-Do lists

## Source Folder
- **Folder name:** Auto-Comms
- **Folder ID:** `AAMkAGQ5NmQwNGZkLWQ0NTAtNGY4Yy1hNjhlLTY0OTU1N2QzYTBhYwAuAAAAAAArsD3iy/SDRrGkcLnEuZ4GAQDAgFdLn8NBQbObwPn0M6aUAADuhyQpAAA=`
- **Contents:** Asana notification emails — task creation confirmations, assignment changes, comments, due date changes, completions.

## Procedure

### Step 1: Scan Auto-Comms for Unread Asana Emails
Use `email_search` with the Auto-Comms folder ID. Filter for unread emails or emails since the last sync date (check `LAST_SYNCED` in changelog.md).

```
email_search({
  folderId: "AAMkAGQ5NmQwNGZkLWQ0NTAtNGY4Yy1hNjhlLTY0OTU1N2QzYTBhYwAuAAAAAAArsD3iy/SDRrGkcLnEuZ4GAQDAgFdLn8NBQbObwPn0M6aUAADuhyQpAAA=",
  query: "from:asana",
  unreadOnly: true
})
```

If no unread filter is available, search for emails since the last sync date.

### Step 2: Read Each Email and Extract Asana Task ID
For each notification email, use `email_read` to get the full body.

**Extract the Asana task ID** from any "View task" URL in the email body:
- Regex: `app\.asana\.com.*/0/\d+/(\d+)` or `/task/(\d+)`
- The numeric ID at the end of the URL is the Asana task ID

**Extract from the email body:**
- Task name (usually the email subject or first heading)
- Project name (if present)
- Assignee
- Due date
- Comment text (for comment notifications)
- Action type: created, assigned, commented, completed, due date changed

### Step 3: Check To-Do Lists for Existing Match
Search all 5 To-Do lists for a task whose body contains `ASANA: {extracted_id}`.

**To-Do List IDs:**
| List | ID |
|------|-----|
| 🧹 Sweep | `AAMkAGQ5NmQwNGZkLWQ0NTAtNGY4Yy1hNjhlLTY0OTU1ADdkM2EwYWMALgAAAyuwPeLL9INGsaRwucS5ngYBAEas7LcSB6lEv39h0ciIq84AAAITTwAAAA==` → CORRECTED: `AAMkAGQ5NmQwNGZkLWQ0NTAtNGY4Yy1hNjhlLTY0OTU1N2QzYTBhYwAuAAAAAAArsD3iy-SDRrGkcLnEuZ4GAQCIgJPBFelsQrcja-dZLhI0AADUyESHAAA=` |
| 🎯 Core | `AAMkAGQ5NmQwNGZkLWQ0NTAtNGY4Yy1hNjhlLTY0OTU1N2QzYTBhYwAuAAAAAAArsD3iy-SDRrGkcLnEuZ4GAQCIgJPBFelsQrcja-dZLhI0AADUyESIAAA=` |
| ⚙️ Engine Room | `AAMkAGQ5NmQwNGZkLWQ0NTAtNGY4Yy1hNjhlLTY0OTU1N2QzYTBhYwAuAAAAAAArsD3iy-SDRrGkcLnEuZ4GAQCIgJPBFelsQrcja-dZLhI0AADUyESJAAA=` |
| 📋 Admin | `AAMkAGQ5NmQwNGZkLWQ0NTAtNGY4Yy1hNjhlLTY0OTU1N2QzYTBhYwAuAAAAAAArsD3iy-SDRrGkcLnEuZ4GAQCIgJPBFelsQrcja-dZLhI0AADUyESKAAA=` |
| 📦 Backlog | `AAMkAGQ5NmQwNGZkLWQ0NTAtNGY4Yy1hNjhlLTY0OTU1N2QzYTBhYwAuAAAAAAArsD3iy-SDRrGkcLnEuZ4GAQCIgJPBFelsQrcja-dZLhI0AADWyS4nAAA=` |

Use `todo_tasks` to list tasks in each list and search bodies for the Asana ID string.

### Step 4a: Update Existing To-Do Task (Match Found)
If a To-Do task already contains `ASANA: {id}`:

1. Append new activity to the task body under a `SYNC LOG` section:
   ```
   --- SYNC LOG ---
   [2026-03-20] Comment from @username: "comment text"
   [2026-03-20] Due date changed to 2026-04-01
   [2026-03-20] Marked complete in Asana
   ```
2. Update `LAST_SYNCED: 2026-03-20` in the task body
3. If Asana task was marked complete, add a note but do NOT auto-complete the To-Do task (Richard decides)

### Step 4b: Create New To-Do Task (No Match)
If no existing To-Do task contains the Asana ID:

**Assignment Rules — which list gets the task:**

| Signal | List |
|--------|------|
| Quick reply, send, or forward needed | 🧹 Sweep |
| Strategic work, artifact creation, deep thinking | 🎯 Core |
| Google Ads execution, bid changes, campaign updates, keyword work | ⚙️ Engine Room |
| Invoice, PO, budget, compliance, admin | 📋 Admin |
| Blocked, future, low-priority, or unclear urgency | 📦 Backlog |

**Default:** If unclear, put in 📦 Backlog with a note asking Richard to triage.

**Task body format:**
```
STATUS: New from Asana (synced {today's date})
ASANA: {task_id}

WHAT TO DO:
{Brief description based on Asana task name and any context from the notification}

KEY DETAILS:
- Source: Asana notification ({notification type})
- Project: {project name if available}
- Assignee: {assignee if available}
- Due: {due date if available}

WHY IT MATTERS:
{Brief leverage assessment — or "Needs triage" if unclear}

--- SYNC LOG ---
[{today's date}] Created from Asana notification
LAST_SYNCED: {today's date}
```

### Step 5: Log Results to Changelog
Append to `~/shared/context/changelog.md`:

```
## {date} — Asana Sync
- Emails scanned: {count}
- New To-Do tasks created: {count} ({list names})
- Existing To-Do tasks updated: {count}
- Skipped (no actionable content): {count}
- Issues: {any errors or ambiguous notifications}
```

### Step 6: Report
Print a summary to chat:
- New tasks created (with names and assigned lists)
- Existing tasks updated (with what changed)
- Any issues or items needing Richard's attention

## Edge Cases

### Duplicate Prevention
- Always check ALL 5 lists before creating. Include completed tasks in the search (`showCompleted=true`).
- If the same Asana task ID appears in multiple To-Do tasks, flag it as a duplicate for Richard to resolve.
- If a To-Do task with the matching Asana ID is already marked **completed**, do NOT recreate it. Assume Richard took the action. Log as "skipped — already completed in To-Do."

### One-Directional Comment Visibility
- We only receive Asana notifications when **others comment/mention Richard**. We do NOT get notified when Richard comments on Asana tasks.
- A "reminder" notification (e.g., "Frank mentioned you yesterday") does NOT necessarily mean Richard hasn't acted — he may have replied directly in Asana and we wouldn't see it.
- Before creating a new task from a comment/mention notification, check if a To-Do task for that Asana ID was recently completed. If so, skip it.

### Comment-Only Notifications
- If the notification is just a comment on an existing task, update the existing To-Do task's SYNC LOG. Do not create a new task.

### Task Completion Notifications
- If Asana says a task is complete, add to SYNC LOG and note it. Do NOT auto-complete the To-Do task.
- Remind Richard: "This task was marked complete in Asana — close it in To-Do if done."

### Unrecognized Notification Types
- Log them in the sync report as "unrecognized" with the email subject line.
- Do not create To-Do tasks for notifications that don't map to actionable work.

### No Asana Task ID Found
- Some Asana emails (e.g., weekly digests, project summaries) don't contain a single task ID.
- Skip these and log as "skipped — no task ID."

## Frequency
- Run daily as part of AM-1: Ingest (first AM hook)
- Can also be triggered manually anytime
- AM-2: Triage reads To-Do state AFTER this sync runs

## Dependencies
- Must run BEFORE AM-2 (Triage + Draft) and EOD-2 (System Refresh)
- Output: Updated To-Do lists + changelog entry
- Consumers: AM-2 reads To-Do state; EOD-2 reads changelog for sync status
