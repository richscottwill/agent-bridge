# Design Document: Asana Agent Integration

## Overview

Bidirectional integration between the agent system and Asana as the canonical command center. External sources (Slack, email, meetings, DuckDB) enrich Asana. Asana enriches the daily brief, EOD reconciliation, and agent context files.

## Components

### 1. Morning Routine (AM-1/2/3) — Asana as Source of Truth

**AM-1 Ingest:** SearchTasksInWorkspace → GetTaskDetails for due-soon/Today tasks → categorize by Routine field → store Morning_Snapshot → run Activity_Monitor on stories since last scan.

**AM-2 Triage + Command Center:** Four phases:
1. **Intake Processing:** Slack/email signals → create Asana tasks with Routine + Priority_RW. Check bucket caps (Sweep 5, Core 4, Engine Room 6, Admin 3). Flag over-cap for demotion.
2. **Curate the Day (the morning ritual):** The core of the morning routine. Pull all Today tasks, organize into the four blocks (Sweep/Core/Engine Room/Admin). For each task, enrich with: context summary (from Kiro_RW, description, recent comments, Slack signals), suggested next action, pre-drafted communication if the task involves sending/replying/confirming (drafted in Richard's voice), blocker status, and subtask progress. Identify THE HARD THING in Core. Enforce caps. Triage untriaged tasks. Present the curated day plan as a clean board with enriched task cards. Richard approves and adjusts.
3. **Interactive Command Center:** Execute Richard's directions against Asana in real-time. Supported operations: move tasks between Routine buckets (UpdateTask custom_fields), change due dates (UpdateTask due_on), change Priority_RW (Today/Urgent/Not urgent), create new tasks (CreateTask), write/update task descriptions (UpdateTask notes/html_notes), add comments (CreateTaskStory), complete tasks (UpdateTask completed=true), create subtasks (CreateTask with parent), reorder within buckets. Every approved change is executed immediately.
4. **Context Writes:** Write Kiro_RW for each triaged task. Update hands.md from final Asana state.

**AM-3 Brief:** Format daily brief from Asana state: bucket counts, task lists, overdue flags, activity signals, goal alerts. Post to email + rsw-channel.

### 2. EOD Reconciliation (EOD-2)

Pull current Asana state. Diff against Morning_Snapshot. Log completions to rw-tracker.md. Flag carry-forwards and update Kiro_RW. Detect new tasks assigned since morning.

**Daily Reset:** For tasks that had Priority_RW=Today in the morning but remain incomplete at EOD, demote to Priority_RW=Urgent (not Today) so the next morning starts with a clean slate. The AM-2 curation phase re-promotes tasks to Today as needed. This mirrors the old To-Do "My Day" auto-clear behavior.

**Recurring Task Management:** When a recurring task is marked complete during the day, verify the next instance exists in Asana. If Asana's native recurrence created it, confirm and note in Kiro_RW. If the task is manually duplicated (not using Asana recurrence), flag it: "Recurring task completed — next instance needed. Cadence: [weekly/monthly/bi-weekly]. Create now?" Known recurring tasks: Weekly Reporting, EU SSR Acq write-up, AU meetings agenda, MBR callout, ie%CCP calc, AU invoice, budget confirmation, Bi-monthly Flash, Individual Goals update, Bi-weekly with Adi.

**Weekly Scorecard Rollup (Friday EOD):** On Fridays, compile the weekly scorecard for rw-tracker.md from Asana completion data: strategic artifacts shipped (count tasks completed in Core with Importance_RW=Important), tools/automations built (count), hours on low-leverage work (estimate from Sweep/Admin task volume), meetings with clear output (cross-reference with meeting notes). Update the Weekly Scorecard section in rw-tracker.md.

**Blocker Registry:** Maintain a blocker registry in the EOD summary and hands.md. For each blocked task, track: task name, blocker description, blocker owner (person), date blocked, escalation path. Source blockers from Kiro_RW fields, Slack signals, and task comments. Surface in AM-2 curation: "2 blocked: MX Auto page on Vijeth (14d), Kingpin on Andes (8d)."

### 3. Goal_Updater (Monthly)

Triggered first business day of month. For each of 14 goals: GetGoal → pull metric values → cross-reference with completed tasks, DuckDB registration data, WBR metrics → draft status update with honest assessment → present to Richard → post on approval.

### 4. Activity_Monitor (Daily, within AM-1)

GetTaskStories for incomplete tasks since last scan timestamp. Classify stories: comment (surface text + author), due_date_changed (old → new + who), reassigned (new assignee + who). Persist last-scanned timestamps in ~/shared/context/active/asana-scan-state.json.

### 5. Context_Writer (On-demand + Periodic)

**Portfolio Notes:** Program-level onboarding doc. H1 portfolio name, H2 per market summary, H2 cross-market initiatives, H2 program metrics. Updated in-place monthly.

**Project Notes:** Market-level onboarding doc. Sections: Market Overview, Active Campaigns, Active Tests, Planned Work, Blockers, Key Metrics, Recent Decisions, Key Links. Updated in-place; Recent Decisions is append-only dated log.

**Task Level:** Descriptions enriched with structured context format. For tasks with empty descriptions, populate using this template:
```
STATUS: [current state — from Kiro_RW or agent assessment]
WHAT TO DO: [concrete next action]
KEY DETAILS:
- Project: [project name]
- Due: [date]
- Blockers: [if any, with owner]
- Related: [Slack threads, meeting notes, other tasks]
WHY IT MATTERS: [leverage assessment — which Five Level does this advance?]
```
Comments for execution context. Subtask completion summaries.

**Subtask Management:** During AM-2 curation, for tasks with subtasks: show X/Y complete, flag overdue subtasks, surface the next incomplete subtask as the suggested next action. During command center phase, support creating subtasks to decompose work ("break this into steps"). When all subtasks are complete, recommend closing the parent.

**Kiro_RW:** Agent scratchpad. Date-stamped, append-only, 500 char limit per entry. Written during AM-2 triage and EOD-2 reconciliation.

### 6. Cross-Enrichment Flows

| Source → Asana | How |
|----------------|-----|
| Slack signal → Task | AM-2 creates task with Routine/Priority from signal type |
| Slack thread → Task comment | Context_Writer adds cross-ref link |
| Slack decision → Project Notes | Context_Writer updates Recent Decisions section |
| Email action item → Task | AM-2 creates task from email triage |
| Meeting action item → Task comment | Context_Writer adds meeting context |
| DuckDB metrics → Goal update | Goal_Updater pulls registration counts for goal drafts |
| DuckDB metrics → Project Notes | Context_Writer updates Key Metrics section |
| WBR data → Goal status | Goal_Updater uses as evidence in monthly drafts |

| Asana → Destination | How |
|---------------------|-----|
| Task state → Daily brief | AM-3 reads buckets, overdue, activity |
| Task completions → rw-tracker.md | EOD-2 logs daily stats |
| Task state → hands.md | AM-2 refreshes Priority Actions from Asana |
| Goal progress → Daily brief | AM-3 includes at-risk/off-track goals |
| Task context → Slack draft | Agent drafts task-based reminders to rsw-channel |
| Task context → Email draft | Agent includes task status in reply drafts |
| Task buckets → Calendar | AM-3 creates Sweep/Core/Engine/Admin blocks |

### 7. Guardrail Layer

Pre-write check: verify task.assignee.gid === 1212732742544167 before any UpdateTask/CreateTaskStory/SetParentForTask. Block + draft for non-Richard tasks. Audit log all writes to ~/shared/context/active/asana-audit-log.jsonl.

### 8. Command Center Operations (AM-2 Interactive Phase)

The agent acts as Richard's task management co-pilot during AM-2. After processing intake signals, the agent presents the current task board and executes Richard's directions against Asana in real-time.

**Supported Operations:**

| Operation | Asana API | Example |
|-----------|-----------|---------|
| Move task to different Routine bucket | UpdateTask(custom_fields={"1213608836755502": "GID"}) | "Move invoice task to Admin" |
| Change due date | UpdateTask(due_on="YYYY-MM-DD") | "Push testing doc to Friday" |
| Change priority | UpdateTask(custom_fields={"1212905889837829": "GID"}) | "Make keyword gap fill Today" |
| Create new task | CreateTask(name, assignee, project, custom_fields, due_on) | "Add task: draft AEO POV outline, Core, due next Friday" |
| Write task description | UpdateTask(notes="text" or html_notes="<body>...") | "Add context to the F90 task about legal timeline" |
| Add comment | CreateTaskStory(task_gid, text or html_text) | "Comment on testing doc: blocked on Megan's input" |
| Complete task | UpdateTask(completed=true) | "Mark AU agenda done" |
| Create subtask | CreateTask(parent=task_gid, name, ...) | "Add subtask to F90: follow up with legal by Thursday" |
| Set importance | UpdateTask(custom_fields={"1212905889837865": "1212905889837866"}) | "Mark AEO research as Important" |
| Update Kiro_RW | UpdateTask(custom_fields={"1213915851848087": "text"}) | Agent writes context automatically |

**Agent-Initiated Proposals:**
The agent doesn't just wait for commands. Based on the morning data, it proposes:
- Overdue tasks: "X is 8 days overdue — do, delegate, or kill?"
- Bucket overflow: "Sweep has 7 tasks (cap 5) — demote these 2?"
- Untriaged tasks: "These 5 tasks have no Routine — suggested assignments: ..."
- Stale tasks: "No activity on Y in 14 days — still relevant?"
- Due date conflicts: "3 Core tasks due today — which is the hard thing?"

Richard approves, modifies, or gives new directions. Every approved change is executed immediately against Asana.

## Asana API Patterns

### Custom Field Writes
```
// Set Routine to Sweep
UpdateTask(task_gid, custom_fields={"1213608836755502": "1213608836755503"})

// Set Priority_RW to Today
UpdateTask(task_gid, custom_fields={"1212905889837829": "1212905889837830"})

// Write Kiro_RW
UpdateTask(task_gid, custom_fields={"1213915851848087": "2026-04-03: [context text]"})

// Set Importance_RW to Important
UpdateTask(task_gid, custom_fields={"1212905889837865": "1212905889837866"})
```

### Rich Text for Notes/Comments
```
// Task comment with cross-reference
CreateTaskStory(task_gid, html_text="<body><strong>Context from Slack</strong> ...")

// Project description update (Notes fallback if Notes tab not writable)
UpdateProject(project_gid, html_notes="<body><strong>AU — Paid Search</strong>...")
```

### Goal Status Pattern
```
// Read goal
GetGoal(goal_gid) → {metric: {current_number_value, target_number_value}, status}

// Post status update (via status update API or comment)
// Draft first, post on Richard's approval
```

## State Files

| File | Purpose | Updated By |
|------|---------|------------|
| ~/shared/context/active/asana-command-center.md | Field GIDs, capability map, protocol | Manual + design phase |
| ~/shared/context/active/asana-scan-state.json | Last-scanned timestamps per task for Activity_Monitor | AM-1 |
| ~/shared/context/active/asana-audit-log.jsonl | Write operation audit trail | Every Asana write |
| ~/shared/context/active/asana-morning-snapshot.json | Frozen AM-1 task state for EOD diff | AM-1 (write), EOD-2 (read) |
| ~/shared/context/active/rw-tracker.md | Weekly scorecard, daily task stats | EOD-2 |
| ~/shared/context/body/hands.md | Priority Actions snapshot | AM-2 |

## Five Levels Mapping

| Level | Asana Signals | Agent Action |
|-------|--------------|--------------|
| L1: Sharpen Yourself | Goal tracking tasks, streak data, artifact tasks | Annotate in brief, track consecutive weeks shipped |
| L2: Drive WW Testing | Test goals (MX/AU/Globalized), test tasks in WW Testing project | Surface test status, flag 0% goals |
| L3: Team Automation | Team task reads, meeting prep tasks | Pre-populate agendas, surface blocked team tasks |
| L4: Zero-Click Future | "Using AI for paid search" task, AEO research | Connect to POV work, track in Project Notes |
| L5: Agentic Orchestration | Kiro_RW as persistent memory, full AM→EOD loop | Self-referential: this integration IS Level 5 |

## Notes Tab Discovery

The agent will probe portfolio/project objects for writable Notes surfaces during initialization. Fallback chain: Notes tab → project description (html_notes) → pinned status update → pinned task with comments. Document findings in asana-command-center.md under "Surface Capabilities."
