# Asana MCP for Kiro

**Doc:** 08
**Audience:** Paid Acquisition teammates who use Asana + their Kiro agents
**Status:** FINAL
**Last updated:** 2026-04-17

## Environment Awareness (for your agent)

| Capability | Remote IDE (DevSpaces) | Local IDE (laptop Kiro) | AgentSpaces (chat) |
|---|---|---|---|
| Call Asana MCP tools (search, read, create/update tasks the user owns) | ✅ | ✅ | ✅ |
| Bulk task enrichment (20+ tasks in one pass) | ✅ | ✅ | ⚠️ Watch context budget |
| Sync Asana state to local files (DuckDB, state files) | ✅ persistent | ⚠️ laptop-only | ❌ No persistent filesystem |
| Run overdue-scan hooks on schedule | ✅ | ⚠️ Laptop-awake only | ❌ |

**Writes to tasks the user doesn't own (comments, status changes) require manual approval everywhere.** Environment doesn't change that.

---

Asana MCP gives your agent the ability to search, read, create, and update tasks in Asana. Skip this doc and the package if you don't use Asana.

**Hard rule reminder:** Your agent can freely create and update tasks **you own**. It cannot comment on, status-change, or modify tasks assigned to other people without manual approval. See `kiro-no-external-write-rule.md`.

## Setup

Add to your Kiro MCP config (`.kiro/settings/mcp.json` inside the workspace you opened, or `~/.kiro/settings/mcp.json` for user-level):

```json
{
  "mcpServers": {
    "enterprise-asana-mcp": {
      "command": "aim",
      "args": ["mcp", "start-server", "enterprise-asana-mcp"],
      "disabled": false,
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
    }
  }
}
```

**Notably NOT auto-approved:** all writes (`CreateTask`, `UpdateTask`, `CreateTaskStory`, `AddTagForTask`, etc.). You'll approve each write manually — which is the right default since Asana tasks surface to teammates through notifications.

Once you've been running for a while and you trust the pattern, you can add writes to autoApprove selectively — but only for operations where you own the target task.

## Starter prompts

Copy-paste any of these to try Asana. Rephrase however feels natural.

**What's on my plate**
- "Show me my overdue tasks. Group by project. For each, tell me what's needed to close it out."
- "What's in my Today section? What's in Upcoming?"
- "Pull all my tasks created this week, grouped by project."
- "What tasks is Brandon blocking on me? Pull comments on my incomplete tasks where he's mentioned."

**See across a project**
- "Show me all incomplete tasks in the 'Paid Search' project."
- "Who has the most open tasks in [project name]?"
- "What tasks were closed in [project] this week?"

**Fill in task context automatically**
- "Read my task 'Make changes AU/MX/PAM' and enrich the description with the latest context from my Slack and email."
- "For my top 5 overdue tasks, draft a next-action sentence I can paste into each task."

**Pull data in bulk**
- "Export my open tasks as a markdown checklist, grouped by due date."
- "Find tasks tagged 'Testing' that haven't been updated in 14 days."

## The PS routine convention

On the paid acq team (the way Richard tracks work), tasks are bucketed by routine via a custom field or tag:

| Routine | What belongs |
|---|---|
| **Sweep** | Low-friction recurring tasks. Fast, low-cognitive-load. |
| **Core** | The work that actually matters for Level 1/2 strategic output. |
| **Engine Room** | Team-multiplier work (tooling, enablement, documentation). |
| **Admin** | Finance, legal, HR, invoicing. Necessary evil. |
| **Wiki** | Writing or updating shared knowledge. |

If your agent knows these buckets, you can ask things like:

- "How many tasks do I have in Core vs Engine Room right now?"
- "What's overdue in my Admin bucket?"

You don't need to adopt this convention — but if you do, mention it in your personal steering file so your agent knows.

## Common patterns

### Overdue scan + next actions

> "List my overdue Asana tasks. For each, read the description and any comments, then propose a next action I can take today to move it forward."

### Weekly completion review

> "Which Asana tasks did I complete this week? Group by project and write a one-line summary of what got done."

### Task creation from email/Slack

Agent writes the task, you approve the creation:

> "I just got an email from Lena asking me to pull Q1 MX data by Friday. Create an Asana task for it in my Admin bucket due Friday."

### Cleanup pass

> "Find my Asana tasks that are: incomplete, created 30+ days ago, no comments or updates in the last 14 days. Propose for each whether to kill, demote to Backlog, or keep."

## Bulk write warning

If you add `UpdateTask` or `CreateTask` to autoApprove and then ask "update 50 tasks," you will hit Asana's rate limits and/or flood your project notifications. Batch rules:

- No more than 10 task writes per single request
- Space bulk operations 2+ seconds apart when possible
- If enriching >20 tasks, break into multiple turns — review agent output between batches

## Custom fields gotcha

Custom fields in Asana are **project-specific**. A field GID from one project will NOT work on a task in a different project. If your agent tries to update a custom field and gets an error, it's probably trying to use a field ID from the wrong project. Solution: read the target task first (`GetTaskDetails`) to get the correct field GIDs for that project.

Custom field value formats:
- **enum** → option GID, NOT the label
- **multi_enum** → comma-separated option GIDs
- **date** → `{"date": "YYYY-MM-DD"}` object, not a plain string
- **text** → plain string
- **number** → numeric string

## Failure modes

- **Timeout on task update** → Asana API is slow. Retry once. If it fails again, the task may be locked by another user editing it.
- **"Custom field not found"** → You're using a field ID from a different project. Read the target task first.
- **Comments not posting** → `CreateTaskStory` isn't auto-approved. That's intentional. Approve manually.
- **Bulk operations flooding notifications** → Back off. Paid acq uses Asana notifications for real alerts; don't train them to be noise.

## What not to use Asana MCP for

- **Don't comment on other people's tasks autonomously.** Those comments surface as notifications to the task owner. Equivalent to an email.
- **Don't change due dates on tasks you don't own.** Ask the owner first.
- **Don't delete tasks programmatically** (no delete tool exists in the current MCP, and that's the right call).
- **Don't use Asana MCP as a general knowledge base** — the Wiki is for that. Asana is for work state.
