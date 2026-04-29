---
inclusion: manual
---



# Asana Guardrails

When interacting with Asana MCP tools, follow these rules. The core principle: auto-write on Richard's own stuff, draft-first for anything that touches others.



## Ownership Boundaries



### Richard's Portfolios
- ABIX PS (GID: `1212775592612914`)
- ABPS (GID: `1212762061512816`)
- Paid App (inferred from project membership)
- Testing (inferred from project membership)



### Richard's Projects
- AU (GID: `1212762061512767`)
- MX (GID: `1212775592612917`)
- Paid App (GID: `1205997667578886`)
- My Tasks (GID: `1212732838073807`)



### Richard's Goals
- Globalized cross-market testing (GID: `1213245014119131`)
- MX + AU market testing (GID: `1213245014119125`)
- MX/AU paid search registrations (GID: `1213245014119128`)
- Paid App (GID: `1213204514049810`)
- All child goals of the above



### Ownership Test
A task is "Richard's" if ALL of these are true:
1. Assigned to Richard (GID: `1212732742544167`)
2. NOT assigned to or associated with others (no co-assignee, not in a project owned by someone else outside the list above)
3. Belongs to one of Richard's projects listed above, OR is in "My Tasks" and not in other non-Richard projects

---



## Auto-Write Whitelist (no approval needed)

These operations execute immediately during hooks and on-demand sessions. No draft-first required.



### Custom Fields on My Tasks
- **Kiro_RW** (GID: `1213915851848087`) — agent scratchpad, append-only, 500 char limit
  - Example: Kiro_RW** (GID: `1213915851848087`) — agent scratchpad, appe...
- **Routine** (GID: `1213608836755502`) — bucket assignment (Sweep/Core/Engine Room/Admin)
- **Priority_RW** (GID: `1212905889837829`) — Today/Urgent/Not urgent (includes daily reset demotions)
- **Begin Date** (GID: `1213440376528542`) — scheduling
- **Completed** — marking tasks complete
- **Subtasks** — creating subtasks on Richard's tasks
- **Attachments** — adding attachments to Richard's tasks



### Routine Field Assignment for Untriaged Tasks
- When a task has Priority_RW=Today but no Routine, and the signal-to-Routine mapping is unambiguous → auto-assign Routine



### Due Date Changes on Recurring Tasks
- When a recurring task is completed and the next instance is created, set the due date using deterministic cadence math (weekly +7d, monthly +1mo, bi-weekly +14d)



### Task/Subtask Creation from Slack Signals
- When Slack [ACTION-RW] signals map to a new task via the signal-to-Routine mapping → auto-create with Routine + Priority_RW pre-set
- Dedup check: before creating, search for existing task with matching name. If found, skip creation and update Kiro_RW instead
- INTAKE FUNNEL: If Slack, email, or meetings surface something Richard should be tracking that doesn't exist anywhere in Asana → create it in My Tasks with Routine + Priority + Kiro_RW context. The agent is the intake funnel — nothing falls through the cracks.



### Audit Log Writes
- Always auto-write. Logging never requires approval.



### Task Descriptions
- Auto-write on tasks assigned to Richard where the description is EMPTY or was previously written by the agent
- If the description contains content written by others (teammates, stakeholders), do NOT overwrite — use Kiro_RW or CreateTaskStory for additional context instead
- Check: if notes/html_notes is non-empty and doesn't contain "Kiro agent" or agent-written markers, treat as other-authored → append via comment only
- This applies across ALL projects including WW Testing — the rule is about authorship, not project ownership
- If the task is attached to a project NOT in Richard's ownership list → still write descriptions if assigned to Richard and description is empty



### Comments on Tasks
- Auto-write on tasks in Richard's projects (AU, MX, Paid App, My Tasks)
- If the task is in a project not owned by Richard → BLOCK, draft-first



### Project / Portfolio Notes
- Auto-write on Richard's projects (AU, MX, Paid App) and portfolios (ABIX PS, ABPS)
- Project description (html_notes), status updates, Notes tabs — all auto-write for Richard's projects



### Goal Status Updates
- Auto-write on Richard's goals listed above (Globalized testing, MX+AU testing, MX/AU regs, Paid App) and their child goals
- Draft-first for any goal not in the list



### My Tasks — Full Access
- Write to Notes tab in My Tasks
- Update any tab, view, or surface in My Tasks
- All custom field writes on tasks in My Tasks (Kiro_RW, Routine, Priority_RW, Begin Date, Importance_RW, Notes-Task, etc.)

---



## Blacklist (never write — always block)

These operations are ALWAYS blocked regardless of context. Log with result "blocked" and present as draft.

- **Task descriptions** on tasks assigned to or associated with others
- **Comments** on tasks in projects not owned by Richard
- **Status changes** (completed, custom field changes) on tasks assigned to others
- **Notes/descriptions** on projects or portfolios not owned by Richard
- **Subtask creation** on tasks assigned to others
- **Due date changes** on tasks assigned to others
- **Any write** to a task where assignee.gid ≠ `1212732742544167`
- **Any write** to a project/portfolio not in Richard's ownership list above
- **Reassigning tasks** — never reassign any task, ever
- **Creating projects or sections** — never without explicit Richard approval
- **Deleting anything** — never delete tasks, subtasks, comments, or projects

---

## Guardrail Check Sequence (every write)

```
1. Identify target object (task GID, project GID, goal GID)
2. Determine object type (task, project, portfolio, goal)
3. CHECK BLACKLIST FIRST:
   - Is the task assigned to someone other than Richard? → BLOCK
   - Is the project/portfolio not in Richard's ownership list? → BLOCK
   - Is this a delete or reassign operation? → BLOCK
4. CHECK WHITELIST:
   - Does the operation match an auto-write rule above? → EXECUTE immediately
5. DEFAULT (not in whitelist or blacklist):
   - DRAFT-FIRST → present to Richard for approval
6. LOG every operation (auto-write, blocked, or draft-approved) to audit trail
```

---



## Read Access — Unrestricted

All read operations are allowed without authorization checks:
GetTaskDetails, GetTaskStories, SearchTasksInWorkspace, GetGoal, GetPortfolioItems, GetProject, GetProjectSections, GetStatusUpdatesFromObject, GetSubtasksForTask, GetProjectTaskCount, AsanaSearch, GetStoriesForTask, GetSubtasksForTask, GetAllPortfolios

---



## Audit Logging — MANDATORY

Log EVERY Asana write operation to `~/shared/context/active/asana-audit-log.jsonl`:
- Format: one JSON object per line
- Schema: `{"timestamp": "ISO-8601", "tool": "ToolName", "task_gid": "GID", "fields_modified": ["field1"], "result": "success|error|blocked|auto-write", "rule": "whitelist|blacklist|draft-approved"}`
- For auto-writes, set result to "auto-write" and rule to "whitelist"
- For blocked writes, set result to "blocked" and rule to "blacklist" with reason
- Audit log is append-only — never delete or overwrite entries

---



## Key Reference


#[[file:~/shared/context/active/asana-command-center.md]]
Use asana-command-center.md for all GID lookups — portfolio GIDs, project GIDs, goal GIDs, custom field GIDs, and Richard's user GID.

- Audit log: `~/shared/context/active/asana-audit-log.jsonl`
