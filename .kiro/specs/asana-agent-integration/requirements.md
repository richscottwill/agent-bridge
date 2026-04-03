# Requirements Document

## Introduction

This document defines the requirements for the Asana Agent Integration layer — the system that connects Richard's agent ("The Body") to Asana as the canonical command center for task management, goal tracking, activity monitoring, and multi-level context writing. Asana replaces Microsoft To-Do as the source of truth. The integration spans six capability areas: monthly goal updates, activity feed monitoring, multi-level context writing, Notes tab utilization, morning routine integration, and EOD reconciliation. All write operations are constrained by the Asana guardrails (only Richard's tasks, draft-first for others, no project-level changes without approval).

## Glossary

- **Agent**: The Body — Richard's 11-organ AI agent system that executes morning routines, EOD reconciliation, and agentic workflows
- **Asana_MCP**: The Enterprise Asana MCP server providing API tools (GetTaskDetails, UpdateTask, CreateTask, SearchTasksInWorkspace, GetGoal, GetTaskStories, etc.)
- **Goal_Updater**: The agent subsystem responsible for pulling signals and drafting monthly goal status updates in Asana
- **Activity_Monitor**: The agent subsystem that reads task activity feeds (stories) to detect changes by teammates
- **Context_Writer**: The agent subsystem that writes structured context at portfolio, project, task, and Kiro_RW field levels
- **Morning_Routine**: The three-hook AM sequence: AM-1 (Ingest), AM-2 (Triage), AM-3 (Brief)
- **EOD_Reconciler**: The EOD-2 hook subsystem that compares morning snapshot to end-of-day state
- **Kiro_RW**: Custom text field (GID: `1213915851848087`) on Asana tasks used as the agent's persistent scratchpad
- **Routine_Bucket**: One of four task categories: Sweep (low-friction), Core (deep work), Engine Room (hands-on), Admin (wind-down)
- **Priority_RW**: Custom enum field on Asana tasks: Today, Urgent, Not urgent
- **Morning_Snapshot**: The frozen state of Richard's Asana tasks captured during AM-1, used as baseline for EOD comparison
- **Richard**: The task owner (Asana GID: `1212732742544167`) — all write operations are scoped to Richard's tasks
- **Workspace**: The amazon.com Asana workspace (GID: `8442528107068`)
- **My_Tasks**: Richard's user task list project (GID: `1212732838073807`)
- **Five_Levels**: Richard's strategic priority framework (Sharpen Yourself → Drive WW Testing → Team Automation → Zero-Click Future → Agentic Orchestration)

## Requirements

### Requirement 1: Monthly Goal Status Updates

**User Story:** As Richard, I want the agent to draft honest monthly status updates for all 14 Asana goals, so that goal tracking stays current without manual effort and reflects real progress signals.

#### Acceptance Criteria

1. WHEN the first business day of a new month arrives, THE Goal_Updater SHALL retrieve all 14 goals owned by Richard using GetGoal for each goal GID and compile current metric values, target values, and existing status
2. WHEN drafting a goal status update, THE Goal_Updater SHALL pull task completion data from Asana (tasks completed in the prior month that relate to the goal), WBR metrics from rw-tracker.md, and Slack signals from intake files to assemble an evidence-based assessment
3. WHEN a goal has a numeric metric (e.g., MX registrations target 11,100, AU registrations target 12,906, Paid App Installs target 435,000), THE Goal_Updater SHALL calculate the month-over-month delta and year-to-date pace, and flag whether the goal is on-track, at-risk, or off-track
4. WHEN a goal has a percentage-based metric at 0% with the time period partially elapsed (e.g., Q1 Brand LP tests), THE Goal_Updater SHALL flag the goal as at-risk and include a recommended action in the draft
5. THE Goal_Updater SHALL present all 14 drafted status updates to Richard for review before posting any update to Asana via CreateTaskStory or status update APIs
6. IF Richard approves a drafted status update, THEN THE Goal_Updater SHALL post the update to the corresponding goal in Asana using the appropriate status update tool
7. IF the Goal_Updater cannot retrieve sufficient data to assess a goal (e.g., missing WBR data, no related tasks found), THEN THE Goal_Updater SHALL flag the goal as "insufficient data" and list the missing signals in the draft

### Requirement 2: Activity Feed Monitoring

**User Story:** As Richard, I want the agent to proactively monitor task activity feeds, so that I see teammate comments, due date changes, and reassignments without manually checking each task.

#### Acceptance Criteria

1. WHEN the Morning_Routine AM-1 hook executes, THE Activity_Monitor SHALL call GetTaskStories for each of Richard's incomplete tasks that have had activity since the last scan timestamp
2. WHEN a teammate adds a comment on one of Richard's tasks, THE Activity_Monitor SHALL surface the comment text, commenter name, and task name as a signal in the AM-3 daily brief
3. WHEN a task's due date is changed by someone other than Richard or the Agent, THE Activity_Monitor SHALL surface the old due date, new due date, who changed it, and task name in the AM-3 daily brief
4. WHEN a task is reassigned away from Richard by someone other than Richard, THE Activity_Monitor SHALL surface the reassignment (new assignee, task name, who reassigned) in the AM-3 daily brief
5. THE Activity_Monitor SHALL persist the last-scanned timestamp per task in a local state file so that subsequent scans only process new activity
6. IF the Activity_Monitor encounters a rate limit or API error from Asana_MCP during story retrieval, THEN THE Activity_Monitor SHALL log the error, skip the affected tasks, and continue processing remaining tasks

### Requirement 3: Multi-Level Context Writing — Portfolio Level

**User Story:** As Richard, I want the agent to write program-level context into portfolio status updates and descriptions, so that portfolio views reflect current strategic state.

#### Acceptance Criteria

1. WHEN Richard requests a portfolio status update, THE Context_Writer SHALL retrieve all projects in the portfolio using GetPortfolioItems, compile project-level status (on-track, at-risk, off-track), and draft a portfolio status summary
2. THE Context_Writer SHALL include in the portfolio status draft: count of projects by status, key milestones hit or missed in the period, and cross-project dependencies or blockers
3. THE Context_Writer SHALL present the drafted portfolio status to Richard for review before writing to Asana
4. IF a portfolio contains projects owned by teammates (not Richard), THEN THE Context_Writer SHALL use read-only access for those projects and clearly label teammate-owned project data as "read-only context" in the draft

### Requirement 4: Multi-Level Context Writing — Project Level

**User Story:** As Richard, I want the agent to write project-level context into project status updates and descriptions, so that each project reflects current progress and blockers.

#### Acceptance Criteria

1. WHEN Richard requests a project status update, THE Context_Writer SHALL retrieve project details using GetProject, task counts using GetProjectTaskCount, and recent task completions to draft a project status update
2. THE Context_Writer SHALL include in the project status draft: incomplete task count, tasks completed since last update, overdue tasks with age, and blockers detected from Kiro_RW fields or Slack signals
3. THE Context_Writer SHALL present the drafted project status to Richard for review before posting via the status update API
4. WHILE a project has tasks with Kiro_RW fields containing blocker notes, THE Context_Writer SHALL aggregate those blockers into the project status draft under a "Blockers" section

### Requirement 5: Multi-Level Context Writing — Task Level

**User Story:** As Richard, I want the agent to write specific task context into task descriptions, subtasks, and comments, so that each task carries enough context for Richard and collaborators to act without searching.

#### Acceptance Criteria

1. WHEN the Agent detects a task with an empty description and a non-empty Kiro_RW field, THE Context_Writer SHALL draft a task description incorporating the Kiro_RW context and present it to Richard for approval before updating via UpdateTask
2. WHEN Richard requests the Agent to add context to a specific task, THE Context_Writer SHALL pull cross-references from related tasks, Slack threads (via intake files), and meeting notes to compose a task comment via CreateTaskStory
3. WHEN a task has subtasks that are all completed, THE Context_Writer SHALL add a comment summarizing subtask completion status and recommend whether the parent task can be closed
4. IF the task is not assigned to Richard, THEN THE Context_Writer SHALL draft the comment text and present it to Richard for manual posting (draft-first guardrail)

### Requirement 6: Kiro_RW Agent Scratchpad

**User Story:** As Richard, I want the agent to use the Kiro_RW custom field as persistent task-level memory, so that context survives across sessions and other agents can read it.

#### Acceptance Criteria

1. WHEN the Morning_Routine AM-2 hook triages a task, THE Agent SHALL write a Kiro_RW entry containing: current status assessment, detected blockers, recommended next action, and any cross-references to Slack threads or meeting notes
2. WHEN the EOD_Reconciler processes a task that was not completed during the day, THE Agent SHALL update the Kiro_RW field with carry-forward context: why it was not completed (if detectable), and the recommended next action date
3. THE Agent SHALL write Kiro_RW values using UpdateTask with custom_fields parameter `{"1213915851848087": "<text>"}` and limit each entry to 500 characters to stay within Asana field display limits
4. THE Agent SHALL prepend a date stamp (YYYY-MM-DD) to each Kiro_RW write so that the most recent context is identifiable
5. IF a Kiro_RW field already contains content, THEN THE Agent SHALL append the new entry below the existing content (separated by a newline and date stamp) rather than overwriting, preserving the context history

### Requirement 7: Portfolio & Project Notes as Canonical Market Onboarding Context

**User Story:** As Richard, I want the agent to maintain Asana's portfolio-level and project-level Notes as living onboarding documents for each market, so that anyone new to AU, MX, or any market can open the Notes and immediately understand what's running, what's planned, what's blocked, who owns what, key metrics, and recent decisions — without asking Richard.

#### Acceptance Criteria

1. WHEN the Agent writes program-level context, THE Context_Writer SHALL write to the portfolio or project Notes tab (not to local files or Slack) using Asana's rich text formatting with headers (H1, H2, H3) so that the content is navigable in Asana's outline view
2. THE Context_Writer SHALL structure project-level Notes (e.g., AU, MX) as a market onboarding document using this header hierarchy:
   - H1: Market name (e.g., "AU — Paid Search")
   - H2: Market Overview (what this market is, registration targets, efficiency guardrails, key stakeholders and their roles)
   - H2: Active Campaigns & Accounts (account structure, budget, current bid strategies, key settings)
   - H2: Active Tests & Experiments (what's running, hypothesis, status, expected completion)
   - H2: Planned Work (what's next, dependencies, timelines)
   - H2: Blockers & Risks (what's stuck, who owns the unblock, escalation path)
   - H2: Key Metrics & Targets (registration targets, CPA guardrails, pacing vs. plan)
   - H2: Recent Decisions & Changes (dated log of significant decisions, with rationale)
   - H2: Key Links (dashboards, Quip docs, Slack channels, Google Ads accounts, relevant SIMs)
3. THE Context_Writer SHALL structure portfolio-level Notes (e.g., ABIX PS, ABPS) as a program-level onboarding document with: H1 for the portfolio, H2 for each market project summarized, H2 for cross-market initiatives, H2 for program-level metrics and goals
4. WHEN the Goal_Updater or Context_Writer generates a monthly or weekly summary, THE Context_Writer SHALL update the relevant Notes sections in-place (refreshing current state) rather than appending dated entries, so the document always reads as a current onboarding doc. A separate "Recent Decisions & Changes" section SHALL serve as the dated running log.
5. WHEN Richard requests a summary of a portfolio or project, THE Context_Writer SHALL first read the existing Notes content and present the most recent state before generating updates
6. THE Context_Writer SHALL present all Notes content drafts to Richard for review before writing to Asana
7. IF the Asana_MCP does not support writing to portfolio or project Notes directly, THEN THE Agent SHALL discover the available write surface (e.g., project description field, status updates, or a pinned task within the project) and use the best available alternative, documenting the limitation
8. THE Context_Writer SHALL ensure that the Notes content is written in plain, professional language that a new team member or stakeholder could understand without prior context about Richard's agent system or internal tooling

### Requirement 7b: Notes Tabs Discovery and Utilization

**User Story:** As Richard, I want the agent to discover and utilize all available Notes tabs and views within My Tasks, portfolios, and projects, so that no usable Asana surface goes unexplored.

#### Acceptance Criteria

1. WHEN the Agent first initializes the Asana integration, THE Agent SHALL probe each portfolio, project, and My Tasks for available Notes tabs, Dashboard tabs, Files tabs, and other view types by querying the Asana_MCP
2. THE Agent SHALL document the discovered capabilities (which objects support Notes, which support status updates, which support custom fields) in the asana-command-center.md file under a "Surface Capabilities" section
3. WHEN a Notes tab is available at the My Tasks level, THE Context_Writer SHALL use it for Richard's personal operational notes (e.g., weekly priorities, decision log, parking lot items) separate from task-level data
4. IF a Notes tab or view is not available or not writable for a given object, THEN THE Agent SHALL log the limitation and fall back to the next best surface (status updates → pinned task comments → Kiro_RW fields)

### Requirement 8: Morning Routine Integration — AM-1 Ingest

**User Story:** As Richard, I want AM-1 to pull all incomplete Asana tasks directly, so that the morning routine starts with a complete, current task picture.

#### Acceptance Criteria

1. WHEN the AM-1 hook executes, THE Morning_Routine SHALL call SearchTasksInWorkspace with `assignee_any=1212732742544167` and `completed=false` to retrieve all of Richard's incomplete tasks
2. WHEN tasks are retrieved, THE Morning_Routine SHALL enrich each task with custom field values (Routine, Priority_RW, Importance_RW, Kiro_RW, Begin Date) by calling GetTaskDetails for tasks due within 14 days or flagged as Today/Urgent
3. THE Morning_Routine SHALL categorize each task into a Routine_Bucket based on the Routine custom field value: Sweep (GID `1213608836755503`), Core (GID `1213608836755504`), Engine Room (GID `1213608836755505`), Admin (GID `1213608836755506`), or Backlog (no Routine set)
4. THE Morning_Routine SHALL flag tasks with Priority_RW = Today that have no Routine value as "needs triage"
5. THE Morning_Routine SHALL flag tasks overdue by 7 or more days as "stale — decision needed: do, delegate, or kill"
6. THE Morning_Routine SHALL store the complete task snapshot as the Morning_Snapshot for use by the EOD_Reconciler

### Requirement 9: Morning Routine Integration — AM-2 Triage

**User Story:** As Richard, I want AM-2 to triage tasks into Routine buckets with cap enforcement, so that each day has a realistic, bounded workload.

#### Acceptance Criteria

1. WHEN the AM-2 hook executes, THE Morning_Routine SHALL read the categorized task list from AM-1 and check each Routine_Bucket against its cap: Sweep (5), Core (4), Engine Room (6), Admin (3)
2. WHEN a Routine_Bucket exceeds its cap, THE Morning_Routine SHALL identify the lowest-priority tasks in that bucket (by Priority_RW, then by due date) and flag them for demotion to Backlog
3. WHEN the AM-2 hook identifies tasks flagged as "needs triage" (Today priority but no Routine), THE Morning_Routine SHALL suggest a Routine assignment based on task name, project membership, and any existing Kiro_RW context
4. WHEN Richard approves a triage suggestion, THE Morning_Routine SHALL update the task's Routine custom field in Asana via UpdateTask
5. THE Morning_Routine SHALL write Kiro_RW context for each triaged task during AM-2 processing, including status assessment and recommended next action

### Requirement 10: Morning Routine Integration — AM-3 Brief

**User Story:** As Richard, I want AM-3 to surface a daily brief with bucket counts, overdue flags, and activity signals, so that I start each day with a clear operational picture.

#### Acceptance Criteria

1. WHEN the AM-3 hook executes, THE Morning_Routine SHALL generate a daily brief containing: task counts per Routine_Bucket for Today-priority tasks, list of tasks per bucket, overdue task count with the oldest task name and days overdue, and Backlog tasks needing triage count
2. THE Morning_Routine SHALL include Activity_Monitor signals in the daily brief: teammate comments awaiting response, due date changes, and reassignments detected since the previous morning
3. THE Morning_Routine SHALL include goal progress signals: any goals flagged as at-risk or off-track from the most recent Goal_Updater assessment
4. WHEN the daily brief is generated, THE Morning_Routine SHALL format the brief using the established template: 🧹 Sweep, 🎯 Core, ⚙️ Engine Room, 📋 Admin sections with ⚠️ Overdue and 📦 Backlog sections
5. IF the total Today-priority task count exceeds 18 (sum of all bucket caps), THEN THE Morning_Routine SHALL include a warning that the day is overloaded and recommend tasks to defer

### Requirement 11: EOD Reconciliation

**User Story:** As Richard, I want EOD-2 to compare the morning snapshot to end-of-day state, so that completions are logged, carry-forwards are flagged, and new tasks are caught.

#### Acceptance Criteria

1. WHEN the EOD-2 hook executes, THE EOD_Reconciler SHALL pull Richard's current incomplete tasks from Asana and compare them against the Morning_Snapshot captured during AM-1
2. WHEN a task present in the Morning_Snapshot is now marked complete, THE EOD_Reconciler SHALL log the completion in rw-tracker.md with task name, completion date, and Routine_Bucket
3. WHEN a task had Priority_RW = Today in the Morning_Snapshot but remains incomplete at EOD, THE EOD_Reconciler SHALL flag the task as a carry-forward and update its Kiro_RW field with carry-forward context
4. WHEN a task appears in the current Asana state but was not present in the Morning_Snapshot, THE EOD_Reconciler SHALL flag the task as "new since morning" and include it in the EOD summary with source (who assigned it, which project)
5. THE EOD_Reconciler SHALL generate an EOD summary containing: tasks completed today (count and names), carry-forward tasks (count and names), new tasks received (count and names), and net task delta for the day
6. THE EOD_Reconciler SHALL update rw-tracker.md with the daily task statistics: completed count, carry-forward count, new task count, and net delta

### Requirement 12: Guardrail Enforcement

**User Story:** As Richard, I want all Asana write operations to enforce the established guardrails, so that the agent never modifies teammate tasks or makes unauthorized changes.

#### Acceptance Criteria

1. BEFORE any UpdateTask, CreateTaskStory, or SetParentForTask call, THE Agent SHALL verify that the target task is assigned to Richard (GID: `1212732742544167`) by checking the task's assignee field
2. IF a write operation targets a task not assigned to Richard, THEN THE Agent SHALL block the operation, log the attempted violation, and present the intended change to Richard as a draft for manual execution
3. THE Agent SHALL log every Asana write operation (tool name, task GID, fields modified, timestamp) to an audit trail file for traceability
4. BEFORE any CreateTask call, THE Agent SHALL set the assignee to Richard and verify the target project is one Richard has membership in
5. THE Agent SHALL treat all read operations (GetTaskDetails, GetTaskStories, SearchTasksInWorkspace, GetGoal, GetPortfolioItems, GetProject) as unrestricted and not require additional authorization checks

### Requirement 13: Five Levels Alignment Signals

**User Story:** As Richard, I want the agent to tag task and goal activity with Five Levels alignment, so that I can see which level each action advances.

#### Acceptance Criteria

1. WHEN the Morning_Routine generates the daily brief, THE Agent SHALL annotate each task with its Five_Levels alignment (L1-L5) based on project membership and task content: goal tracking and streak tasks map to L1, test-related tasks map to L2, team visibility tasks map to L3, AI/AEO research tasks map to L4, and full agentic loop tasks map to L5
2. WHEN the Goal_Updater drafts a monthly goal status, THE Goal_Updater SHALL include the Five_Levels alignment for each goal in the draft
3. WHEN the EOD_Reconciler generates the EOD summary, THE EOD_Reconciler SHALL include a Five_Levels breakdown: count of tasks completed per level, highlighting which levels received effort and which received none
