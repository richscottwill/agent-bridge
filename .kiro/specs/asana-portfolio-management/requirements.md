# Requirements Document

## Introduction

This document specifies the requirements for the Asana Portfolio Management system — extending the agent's autonomous management from a single project (ABPS AI Content) to Richard's entire Asana workspace. The system covers three scopes: (1) My Tasks deep enrichment ensuring every task has Kiro_RW, Next action, dates, and Routine/Priority_RW; (2) portfolio-level scanning of ABIX PS (AU, MX) and ABPS (WW Testing, WW Acquisition, Paid App) child projects; and (3) project-specific workflow automation including recurring task auto-creation, cross-team blocker detection, event countdown automation, budget/PO tracking, and market context auto-refresh.

## Glossary

- **Agent**: The Kiro AI assistant operating within Richard's workspace, executing via AM-2 hooks and on-demand commands
- **Kiro_RW**: A text custom field (GID: `1213915851848087`) used as the agent's scratchpad on every task. Format: `M/D: <status in under 10 words>`
- **Next_Action**: A text custom field (GID: `1213921400039514`) containing the single most specific next step for a task. Format: imperative verb, under 15 words
- **Priority_RW**: An enum custom field (GID: `1212905889837829`) with options Today, Urgent, Not urgent
- **Routine**: An enum custom field (GID: `1213608836755502`) with options Sweep, Core Two, Engine Room, Admin
- **Begin_Date**: A date custom field (GID: `1213440376528542`) representing the execution window start (`start_on`)
- **Richard**: Richard Williams, the sole task owner (GID: `1212732742544167`). The agent only modifies tasks assigned to Richard
- **Terminal_Section**: A project section representing completed workflow states (Active, Archive for ABPS AI; Completed/Done for portfolio projects). Tasks in terminal sections are excluded from date checks
- **Enrichment_Batch**: A set of proposed field updates presented to Richard for approval before execution
- **Portfolio_Project**: A child project within the ABIX PS or ABPS portfolio
- **Cross_Team_Task**: A task in a portfolio project assigned to a teammate (not Richard). The agent reads but never modifies these
- **Recurring_Task**: A task that follows a repeating cadence (weekly, bi-monthly, monthly). When completed, the next instance is auto-created
- **Event_Task**: A Paid App task tied to a promotional event (Prime Day, BFCM, Back to School, PBBD, Gift Guide)
- **Budget_Task**: A task related to financial operations (PO, spend, invoice, reconciliation, actuals, forecast)
- **Context_Task**: A pinned task within a project whose html_notes serve as a living project summary maintained by the agent
- **Material_Change**: A change in project state significant enough to warrant a context task refresh (overdue count change, new blocker, task completion, near-due escalation, budget status change)
- **Stale_Status**: A project whose most recent status update was created more than 14 days ago
- **Brevity_Format**: The required Kiro_RW format: `M/D: <text>` where M/D has no leading zeros and text is under 10 words

## Requirements

### Requirement 1: My Tasks Field Enrichment

**User Story:** As Richard, I want every task in My Tasks to have complete Kiro_RW, Next_Action, and date fields, so that I can glance at any task and know its status and next step without opening it.

#### Acceptance Criteria

1. WHEN the Agent scans My Tasks during AM-2 Phase 1, THE Agent SHALL identify all incomplete tasks where Kiro_RW is empty or does not match Brevity_Format
2. WHEN the Agent scans My Tasks during AM-2 Phase 1, THE Agent SHALL identify all incomplete tasks where Next_Action is empty
3. WHEN a task has due_on set but start_on is null, THE Agent SHALL propose start_on equal to the later of today or due_on minus 7 calendar days
4. WHEN a task has Routine set but Priority_RW is null, THE Agent SHALL propose Priority_RW default of "Not urgent"
5. WHEN enrichment gaps are detected, THE Agent SHALL present all proposed field updates as an Enrichment_Batch to Richard for approval before executing any writes
6. WHEN Richard approves an Enrichment_Batch, THE Agent SHALL execute all approved field updates via UpdateTask and log each write to the audit trail
7. IF Richard rejects individual enrichment proposals, THEN THE Agent SHALL skip those proposals and execute only the approved ones

### Requirement 2: Kiro_RW Brevity Enforcement

**User Story:** As Richard, I want every Kiro_RW entry to follow the M/D brevity format consistently across all scopes, so that the field is glanceable and never cluttered with verbose entries.

#### Acceptance Criteria

1. THE Agent SHALL write all Kiro_RW entries in the format `M/D: <status in under 10 words>` where M is the month with no leading zero and D is the day with no leading zero
2. WHEN the Agent encounters an existing Kiro_RW entry that uses YYYY-MM-DD format, bracket format [M/D], or exceeds 10 words after the date, THE Agent SHALL propose a corrected entry in Brevity_Format
3. WHEN the Agent writes a new Kiro_RW entry, THE Agent SHALL append it on a new line below existing content
4. WHILE the Kiro_RW field approaches the 500-character limit, THE Agent SHALL drop the oldest entries to make room for new ones
5. THE Agent SHALL apply the same Brevity_Format rule to Kiro_RW entries across My Tasks, ABPS AI Content, and all Portfolio_Projects without exception

### Requirement 3: Next Action Field Protocol

**User Story:** As Richard, I want every task modification to include an updated Next_Action field, so that I always know the single most specific thing to do next on any task.

#### Acceptance Criteria

1. WHEN the Agent modifies any field on a task (Kiro_RW, Priority_RW, Routine, dates, html_notes, completed), THE Agent SHALL also update the Next_Action field in the same operation or immediately after
2. THE Agent SHALL write Next_Action values as a single imperative sentence under 15 words
3. WHEN a task has incomplete subtasks, THE Agent SHALL derive the Next_Action from the first incomplete subtask
4. WHEN a task is overdue, THE Agent SHALL set Next_Action to "Decide: extend due date, reduce scope, or complete"
5. WHEN a task is near-due (due_on within 2 days), THE Agent SHALL set Next_Action to a specific completion instruction referencing the due date
6. THE Agent SHALL apply the Next_Action update rule uniformly across My Tasks, ABPS AI Content, and all Portfolio_Projects

### Requirement 4: Portfolio Discovery

**User Story:** As Richard, I want the agent to dynamically discover all child projects in my portfolios, so that new projects are automatically included in the management scope without manual configuration.

#### Acceptance Criteria

1. WHEN AM-2 Phase 1C executes, THE Agent SHALL call GetPortfolioItems for ABIX PS (GID: `1212775592612914`) and ABPS (GID: `1212762061512816`) to enumerate child projects
2. WHEN a child project is discovered that is not recorded in asana-command-center.md, THE Agent SHALL call GetProjectSections and sample a task for custom field discovery, then record the project profile
3. WHEN a new project is detected, THE Agent SHALL flag it for Richard in the daily brief with the message "New project detected in [portfolio]: [name]. GIDs recorded."
4. THE Agent SHALL store all discovered project profiles (sections, custom fields, pinned context task GID) in asana-command-center.md under the Portfolio Projects section
5. WHEN portfolio discovery runs multiple times against the same Asana state, THE Agent SHALL produce identical results without duplicating or corrupting existing project profiles

### Requirement 5: Cross-Project Task Scanning

**User Story:** As Richard, I want the agent to scan all portfolio project tasks and apply the same enrichment and date management rules as My Tasks, so that my entire workspace is managed consistently.

#### Acceptance Criteria

1. WHEN AM-2 Phase 1C executes, THE Agent SHALL scan all incomplete tasks in each Portfolio_Project
2. THE Agent SHALL filter scanned tasks to only process those assigned to Richard (assignee.gid equals `1212732742544167`)
3. THE Agent SHALL skip all Cross_Team_Tasks for write operations while still reading them for blocker detection
4. WHEN a Portfolio_Project task assigned to Richard has empty Kiro_RW or Next_Action, THE Agent SHALL propose enrichment following the same rules as My Tasks enrichment
5. THE Agent SHALL present portfolio enrichment proposals as a separate Enrichment_Batch grouped by project
6. THE Agent SHALL apply date window checks, near-due escalation, and overdue flagging to Portfolio_Project tasks using the same rules as My Tasks

### Requirement 6: Near-Due Escalation

**User Story:** As Richard, I want tasks approaching their due date to be automatically escalated to Today priority, so that I never miss a deadline because a task was buried in a lower priority bucket.

#### Acceptance Criteria

1. WHEN an incomplete task has due_on minus today equal to 0, 1, or 2 calendar days AND the task is not in a Terminal_Section, THE Agent SHALL set Priority_RW to Today (option GID: `1212905889837830`)
2. WHEN the Agent escalates a task to Today priority, THE Agent SHALL update Kiro_RW with "M/D: Near-due. Priority escalated."
3. WHEN the Agent escalates a task to Today priority, THE Agent SHALL update Next_Action with a specific completion instruction
4. THE Agent SHALL execute near-due escalation automatically without requiring Richard's approval, because escalation is a safety measure not a destructive change
5. THE Agent SHALL NOT trigger near-due escalation for tasks where due_on minus today is greater than 2 or less than 0

### Requirement 7: Overdue Task Flagging

**User Story:** As Richard, I want overdue tasks to be flagged in my daily brief with recommended actions, so that I can make kill-or-revive decisions quickly without hunting through projects.

#### Acceptance Criteria

1. WHEN an incomplete task has due_on less than today AND the task is not in a Terminal_Section, THE Agent SHALL flag the task as overdue in the daily brief
2. WHEN the Agent flags an overdue task, THE Agent SHALL update Kiro_RW with "M/D: Overdue [N]d. Extend or close." where N is the number of days overdue
3. WHEN the Agent flags an overdue task, THE Agent SHALL set Next_Action to "Decide: extend due date, reduce scope, or complete"
4. THE Agent SHALL NOT auto-extend due dates, auto-complete tasks, or auto-change scope on overdue tasks — these decisions require Richard's approval
5. THE Agent SHALL apply overdue flagging uniformly across My Tasks, ABPS AI Content, and all Portfolio_Projects

### Requirement 8: Status Update Staleness Detection

**User Story:** As Richard, I want to know when a project's status update is stale, so that I can keep project health reporting current.

#### Acceptance Criteria

1. WHEN AM-2 Phase 1C executes, THE Agent SHALL call GetStatusUpdatesFromObject for each Portfolio_Project
2. WHEN the most recent status update for a project was created more than 14 days ago, THE Agent SHALL flag the project as Stale_Status in the daily brief
3. WHEN a project has never had a status update, THE Agent SHALL flag it as "never updated" in the daily brief
4. THE Agent SHALL extract the health color (green, yellow, red) from the most recent status update and include it in the portfolio findings
5. WHEN the most recent status update was created exactly 14 days ago, THE Agent SHALL NOT flag the project as stale

### Requirement 9: Assignee Verification Guard

**User Story:** As Richard, I want the agent to never modify tasks assigned to other people, so that I maintain trust with my teammates and avoid unintended changes.

#### Acceptance Criteria

1. THE Agent SHALL verify assignee.gid equals `1212732742544167` before every write operation on any task across all scopes
2. IF a write operation targets a task not assigned to Richard, THEN THE Agent SHALL block the write, log it to the audit trail with result "blocked", and flag it in the daily brief
3. THE Agent SHALL enforce assignee verification at both the algorithm level and the guard-asana hook level for defense in depth
4. THE Agent SHALL read Cross_Team_Tasks for blocker detection purposes without attempting any write operations

### Requirement 10: Audit Trail Completeness

**User Story:** As Richard, I want every agent write operation logged with project context, so that I can trace any change back to its source and reason.

#### Acceptance Criteria

1. WHEN the Agent executes a write operation on a Portfolio_Project task, THE Agent SHALL append a JSON line to asana-audit-log.jsonl including the project field with the correct project identifier
2. THE Agent SHALL use these project identifiers: AU, MX, WW_Testing, WW_Acquisition, Paid_App, My_Tasks, ABPS_AI_Content
3. WHEN a write operation succeeds, THE Agent SHALL log result as "success"; WHEN it fails, THE Agent SHALL log result as "failure"
4. WHEN a write operation is blocked by assignee verification, THE Agent SHALL log result as "blocked"
5. THE Agent SHALL never overwrite or truncate the audit log — all entries are append-only

### Requirement 11: Terminal Section Exclusion

**User Story:** As Richard, I want tasks in completed workflow sections to be excluded from date checks and escalation, so that finished work doesn't generate false alerts.

#### Acceptance Criteria

1. THE Agent SHALL identify Terminal_Sections for each project during portfolio discovery (Active and Archive for ABPS AI; Completed, Done, or equivalent sections for Portfolio_Projects)
2. WHEN a task is in a Terminal_Section, THE Agent SHALL NOT trigger near-due escalation or overdue flagging for that task
3. WHEN a task is in a Terminal_Section, THE Agent SHALL still include it in task counts for the daily brief portfolio summary

### Requirement 12: Daily Brief Portfolio Section

**User Story:** As Richard, I want the daily brief to include a portfolio status section showing task counts, overdue counts, health colors, and alerts for every project, so that I get a unified view of my entire workspace each morning.

#### Acceptance Criteria

1. WHEN AM-3 generates the daily brief, THE Agent SHALL include a Portfolio Status section listing each portfolio and its child projects
2. THE Agent SHALL display for each project: task count, overdue count, near-due count, health color, and last status update date
3. WHEN a project has Stale_Status, THE Agent SHALL display a warning indicator next to the project entry
4. THE Agent SHALL list all near-due tasks, overdue tasks, and stale projects in a consolidated alerts subsection
5. THE Agent SHALL include cross-team blocker alerts in the portfolio section when blockers are detected

### Requirement 13: Recurring Task Auto-Creation

**User Story:** As Richard, I want the agent to auto-create the next instance of recurring tasks when I complete one, so that I never have to manually recreate weekly agendas, MBR callouts, or other repeating work.

#### Acceptance Criteria

1. WHEN a completed task in AU or MX matches a known recurring pattern (task name contains "Weekly", "Bi-monthly", "Monthly", "WBR", "MBR", "Agenda", "Flash", or "Kingpin"), THE Agent SHALL detect it during AM-2 Phase 1C
2. WHEN a recurring task completion is detected, THE Agent SHALL compute the next due_on based on cadence: weekly adds 7 days, bi-monthly adds 14 days, monthly advances to the same day next month
3. WHEN creating the next recurring task instance, THE Agent SHALL set start_on based on cadence: weekly uses due_on minus 2, bi-monthly uses due_on minus 3, monthly uses due_on minus 5
4. WHEN creating the next recurring task instance, THE Agent SHALL copy the Routine, section membership, and project-specific custom fields (AU Priority GID: `1212762061512785`, Task Progress GID: `1212762061512790`) from the completed task
5. WHEN the Agent creates a recurring task instance, THE Agent SHALL present it to Richard for approval with the message "Auto-created next [task name] due [date]. Approve?"
6. IF Richard rejects the auto-created recurring task, THEN THE Agent SHALL delete the created task

### Requirement 14: Cross-Team Blocker Detection

**User Story:** As Richard, I want the agent to detect when teammate tasks in MX are overdue or stale and blocking my work, so that I can follow up proactively instead of discovering blockers too late.

#### Acceptance Criteria

1. WHEN AM-2 Phase 1C scans the MX project, THE Agent SHALL read all tasks including Cross_Team_Tasks to identify overdue teammate tasks
2. WHEN a Cross_Team_Task has due_on less than today AND is not completed, THE Agent SHALL flag it as a potential blocker
3. WHEN a Cross_Team_Task is flagged as a blocker, THE Agent SHALL check if any of Richard's tasks depend on or reference the blocked task through subtask relationships, task name cross-references, or same-section proximity
4. WHEN a correlated blocker is confirmed, THE Agent SHALL update Richard's blocked task Kiro_RW with "M/D: Blocked on [teammate] task. [N]d overdue."
5. WHEN a correlated blocker is confirmed, THE Agent SHALL update Richard's blocked task Next_Action with "Follow up with [teammate] on [blocker task name]"
6. THE Agent SHALL surface all cross-team blockers in the daily brief with teammate name, days overdue, and suggested follow-up action

### Requirement 15: Event Countdown Automation

**User Story:** As Richard, I want Paid App tasks to auto-escalate as promotional event dates approach, so that campaign preparation stays on track without me manually monitoring every deadline.

#### Acceptance Criteria

1. THE Agent SHALL maintain an event calendar for Paid App in asana-command-center.md listing each event name, approximate date, prep window, and escalation trigger
2. WHEN an event enters its prep window, THE Agent SHALL scan Paid App tasks whose names reference the event via keyword matching
3. WHEN an event-related task is in the "Backlog" section AND the event is within its prep window, THE Agent SHALL propose moving the task to "Prioritized"
4. WHEN an event-related task is in the "Prioritized" section AND the event is within its escalation trigger window, THE Agent SHALL propose moving the task to "In progress" and setting Priority_RW to Today
5. WHEN an event-related task is in the "Blocked" section AND the event is within its escalation trigger window, THE Agent SHALL flag it as a critical blocker in the daily brief
6. WHEN Richard creates a new task with an event keyword in the name, THE Agent SHALL propose a standardized subtask structure (Campaign brief, Budget confirmation, Creative assets, Campaign build, Post-event analysis) with due dates relative to the event date

### Requirement 16: Stale Task Triage

**User Story:** As Richard, I want the agent to identify severely stale tasks in Paid App and propose kill-or-revive decisions, so that the project doesn't accumulate zombie tasks that clutter my view.

#### Acceptance Criteria

1. WHEN a Paid App task has due_on less than today minus 30 days AND is not completed, THE Agent SHALL classify it as severely stale
2. WHEN a severely stale task references a past event, THE Agent SHALL recommend archiving it
3. WHEN a severely stale task references budget or PO work, THE Agent SHALL recommend extending the due date or escalating
4. WHEN a severely stale task does not match event or budget patterns, THE Agent SHALL recommend a kill-or-revive decision
5. THE Agent SHALL present all stale task triage recommendations to Richard as a batch with task name, days overdue, recommendation, and reason
6. WHEN Richard makes a decision on a stale task, THE Agent SHALL execute the decision (archive, extend, or complete)

### Requirement 17: Budget and PO Tracking

**User Story:** As Richard, I want budget-related tasks across MX and Paid App to receive special attention and earlier escalation, so that financial deadlines are never missed.

#### Acceptance Criteria

1. THE Agent SHALL classify tasks as Budget_Tasks when the task name contains "budget", "PO", "spend", "invoice", "reconciliation", "actuals", or "forecast"
2. WHEN a Budget_Task has due_on within 3 calendar days, THE Agent SHALL set Priority_RW to Today regardless of the standard 2-day near-due threshold
3. WHEN a Budget_Task is overdue, THE Agent SHALL flag it as critical in the daily brief with higher visibility than standard overdue tasks
4. THE Agent SHALL include a dedicated Budget Tasks subsection in the daily brief listing all active Budget_Tasks across MX and Paid App with their status and due dates
5. WHEN a Paid App "monthly actuals" task approaches its due date, THE Agent SHALL check for a corresponding Brandon update task and propose creating one if it does not exist

### Requirement 18: Market Context Auto-Refresh

**User Story:** As Richard, I want the pinned context tasks in AU and MX to be automatically refreshed with current project state, so that I always have an up-to-date project summary without manually maintaining it.

#### Acceptance Criteria

1. WHEN AM-2 Phase 1C completes scanning a project, THE Agent SHALL compile a project summary including active task count, overdue count, near-due count, current blockers, upcoming deadlines (next 7 days), recent completions (last 7 days), recurring task status, and budget task status
2. WHEN the compiled summary contains a Material_Change compared to the current Context_Task content, THE Agent SHALL update the Context_Task html_notes with the new summary
3. WHEN updating a Context_Task, THE Agent SHALL follow the read-before-write protocol to preserve any content Richard has added
4. WHEN no Material_Change is detected, THE Agent SHALL skip the Context_Task update to avoid noise
5. THE Agent SHALL refresh AU and MX Context_Tasks daily during AM-2, and other project Context_Tasks weekly
6. WHEN updating a Context_Task, THE Agent SHALL use the standard HTML structure with allowed tags only (body, strong, em, ul, ol, li, a, code)

### Requirement 19: API Failure Handling

**User Story:** As Richard, I want the agent to handle API failures gracefully with a single retry and clear flagging, so that transient errors don't break the morning scan and persistent errors get my attention.

#### Acceptance Criteria

1. WHEN an Asana API call fails during any operation, THE Agent SHALL log the failure to the audit trail and retry once after a 2-second pause
2. IF the retry succeeds, THEN THE Agent SHALL log result as "retry_success" and continue normal operation
3. IF the retry fails, THEN THE Agent SHALL log result as "retry_failure", skip the affected task for the current cycle, and flag it in the daily brief
4. THE Agent SHALL NOT attempt more than one retry per failed API call
5. WHEN a read operation fails (GetTaskDetails, GetSubtasksForTask), THE Agent SHALL skip the task for the current scan cycle without blocking other tasks
6. WHEN an audit log write fails, THE Agent SHALL write to stderr and continue operation without blocking the pipeline

### Requirement 20: Enrichment Batch Presentation

**User Story:** As Richard, I want enrichment proposals presented in a clear, actionable format grouped by scope, so that I can quickly approve or reject changes without reading through individual task details.

#### Acceptance Criteria

1. WHEN the Agent has enrichment proposals for My Tasks, THE Agent SHALL present them under a "MY TASKS ENRICHMENT" header with task count
2. WHEN the Agent has enrichment proposals for Portfolio_Projects, THE Agent SHALL present them under a "PORTFOLIO ENRICHMENT" header grouped by project name
3. THE Agent SHALL display for each proposed enrichment: task name, task GID, current field value (or "empty"), and proposed new value
4. THE Agent SHALL offer Richard the options to approve all, approve individually, or skip the entire batch
5. WHEN Richard approves enrichments, THE Agent SHALL execute all approved writes in a single pass and confirm completion

