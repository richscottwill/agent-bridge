# Requirements Document

## Introduction

Asana becomes the agent's command center — not just a task tracker, but the workspace where the agent creates, maintains, reviews, and refreshes work products autonomously. Richard assigns work by dropping ideas into an Intake section. A multi-agent pipeline (reusing the existing wiki team agents) triages, researches, drafts, reviews, and publishes documents directly inside Asana task descriptions. The agent self-manages the project: checking for due work during the morning routine, executing within date windows, refreshing on cadence, and using Asana's native features (subtasks, approvals, milestones, comments, sections) as workflow infrastructure.

This is the convergence of three existing systems: (1) the Asana command center protocol (My Tasks read/write), (2) the wiki agent pipeline (editor → researcher → writer → critic), and (3) the recurring task state system (cadence-based execution). The ABPS AI project unifies them into a single Asana-native workspace.

## Verified API Capabilities (from live probing, 2026-04-03)

### Confirmed Working via Enterprise Asana MCP

| Feature | Tool | Notes |
|---------|------|-------|
| Rich text in descriptions | `UpdateTask(html_notes)` | Allowed tags: `<body>`, `<strong>`, `<em>`, `<u>`, `<s>`, `<code>`, `<a href>`, `<ul>`, `<ol>`, `<li>`. Must wrap in `<body>` tags. |
| Rich text in comments | `CreateTaskStory(html_text)` | Same allowed tags as descriptions |
| Subtasks | `CreateTask(parent=task_gid)` | Full subtask creation with all fields |
| Milestones | `CreateTask(resource_subtype="milestone")` | Creates milestone tasks |
| Approvals | `CreateTask(resource_subtype="approval")` | Creates with `approval_status: "pending"`. Completing sets to `"approved"`. |
| Sections | `CreateProjectSection` / `GetProjectSections` | Create and read project sections |
| Custom fields | `UpdateTask(custom_fields={...})` | Read and write enum, text, date fields |
| Begin Date / Due Date | `start_on` / `due_on` | Standard date fields |
| Links | `<a href="url">text</a>` | Works in both descriptions and comments |
| Bullets and numbered lists | `<ul><li>` / `<ol><li>` | Works in both descriptions and comments |
| Pin comments | `CreateTaskStory(is_pinned="true")` | Pin important comments to top |
| Task completion | `UpdateTask(completed="true")` | Marks task done |
| Section moves | `UpdateTask(assignee_section=section_gid)` | Move tasks between sections |

### NOT Available via Enterprise Asana MCP

| Feature | Why | Workaround |
|---------|-----|------------|
| H1/H2/H3 headers | Asana API rejects `<h1>`, `<h2>`, etc. | Use `<strong>` for section titles. Visual hierarchy via bold + line breaks. |
| Block quotes | No `<blockquote>` support | Use `<em>` for quoted text |
| Multi-line code blocks | Only inline `<code>` works | Use inline code for short snippets. For longer code, use comments or linked files. |
| @mention notifications | Links to user profiles work but don't trigger native notifications | Use `<a href>` for visual mention + add user as follower for notification |
| Attachment upload | No attachment tool in MCP | Reference files by path or link |
| Asana Rules/Automations | UI-only configuration | Agent implements rule logic in hook prompts |
| Asana AI Assist | Native AI features not accessible via API | Agent IS the AI — this is what we're building |
| Followers management | No AddFollowers tool | Richard is auto-added as creator/assignee |
| Project creation | No CreateProject tool in MCP | Richard creates the project manually; agent manages everything inside it |

### HTML Formatting Guide for Work Products

Since Asana html_notes doesn't support semantic headers, use this formatting convention:

```html
<body>
<strong>DOCUMENT TITLE</strong>

<strong>Section One</strong>
Content paragraph here with <em>emphasis</em> and <a href="url">links</a>.

<ul>
<li>Bullet point one</li>
<li>Bullet point two</li>
</ul>

<strong>Section Two</strong>
More content. Use <code>inline code</code> for technical terms.

<strong>Next Steps</strong>
<ol>
<li>First action</li>
<li>Second action</li>
</ol>
</body>
```

## Glossary

- **Agent**: The Kiro AI assistant operating within the body system, executing work autonomously on Richard's behalf
- **ABPS_AI_Project**: An Asana project dedicated to agent-created and agent-maintained work products. Contains sections for workflow stages. Richard creates this project manually; the agent manages everything inside it.
- **Intake_Section**: A section within ABPS_AI_Project where Richard places new ideas, requests, and raw tasks for the agent to triage
- **Work_Product**: A document, analysis, framework, or other artifact that lives inside an Asana task's html_notes field. Drafts are ~500 words; full documents are ~2000 words.
- **Frequency_Field**: A custom enum field on Asana tasks with values: weekly, monthly, quarterly, one-time. Tells the agent how often to revisit and improve a Work_Product.
- **Date_Window**: The span between a task's Begin Date (start_on) and Due Date (due_on). The agent works on tasks only within their Date_Window.
- **Approval_Subtask**: An Asana task with resource_subtype="approval" created as a subtask of a Work_Product task. Richard approves or rejects. The agent reads the approval_status to determine next action.
- **Morning_Routine**: The AM-1/AM-2/AM-3 hook sequence that runs daily. AM-1 ingests, AM-2 triages and curates, AM-3 briefs.
- **Triage**: The process of moving a task from Intake_Section to the correct workflow section and applying custom field values.
- **Refresh_Cadence**: The schedule defined by Frequency_Field on which the agent revisits a completed Work_Product to update, improve, or extend it.
- **Recurring_Task_State**: The JSON file at ~/shared/context/active/recurring-task-state.json that tracks cadence-based task execution using period-based checks (not day-of-week).
- **Asana_Command_Center**: The existing protocol at ~/shared/context/active/asana-command-center.md that defines field GIDs, guardrails, and API patterns.
- **Guardrail_Layer**: The pre-write verification system that ensures the agent only modifies tasks assigned to Richard (GID 1212732742544167) and logs all writes to the audit log.
- **Pipeline_Agents**: The four wiki team agents (editor, researcher, writer, critic) reused for the Asana doc pipeline with adapted output surfaces.

## Requirements

### Requirement 1: ABPS AI Project Setup

**User Story:** As Richard, I want a dedicated Asana project for agent work products, so that the agent has a structured workspace where it creates and maintains documents autonomously, separate from My Tasks.

#### Acceptance Criteria

1. RICHARD SHALL manually create the ABPS AI project in Asana (no CreateProject tool available in MCP). THE Agent SHALL then configure the project's internal structure.
2. THE Agent SHALL create the following sections within ABPS_AI_Project using CreateProjectSection: "Intake", "In Progress", "Review", "Active", and "Archive"
3. THE Agent SHALL create a custom enum field named "Frequency" with options: "weekly", "monthly", "quarterly", "one-time" and attach it to ABPS_AI_Project
4. THE Agent SHALL record the ABPS_AI_Project GID, all section GIDs, and the Frequency_Field GID in Asana_Command_Center under a new "ABPS AI Project" section
5. THE Agent SHALL verify the project setup by reading back all sections and custom fields, confirming they match the expected configuration

### Requirement 2: Intake Triage (wiki-editor agent)

**User Story:** As Richard, I want to drop raw ideas into the Intake section and have the agent triage them automatically during the morning routine, so that I spend zero effort organizing agent work.

#### Acceptance Criteria

1. DURING AM-2 (Triage + Draft), THE Agent SHALL scan Intake_Section for tasks that have no Routine field set (untriaged indicator)
2. WHEN a new task is detected in Intake_Section, THE Agent (acting as wiki-editor) SHALL analyze the task name and description to determine: (a) Routine bucket based on content type, (b) Priority_RW based on urgency signals, (c) Frequency_Field based on whether the deliverable is recurring or one-time, (d) the type of Work_Product (guide, reference, decision, playbook, analysis)
3. IF a task in Intake_Section has no Begin Date, THEN THE Agent SHALL set Begin Date to today. IF no Due Date, THEN set Due Date to 7 calendar days from today. THE Agent SHALL note default dates in Kiro_RW.
4. WHEN the Agent triages a task, THE Agent SHALL write a Kiro_RW entry with: triage date, assigned fields, Work_Product type, and a one-sentence scope statement
5. THE Agent SHALL present all triage decisions to Richard during AM-2 for approval before executing moves and field changes
6. AFTER Richard approves, THE Agent SHALL move the task to "In Progress" if Begin Date <= today, or leave in Intake with fields applied if Begin Date is in the future
7. THE Agent SHALL create a research subtask under the triaged task, assigned to Richard, with the name pattern: "📋 Research: [parent task name]"

### Requirement 3: Multi-Agent Document Pipeline

**User Story:** As Richard, I want documents to go through a research → draft → review → approval pipeline using the existing wiki team agents, so that work products are well-researched, well-written, and quality-checked before I see them.

#### Acceptance Criteria

1. THE pipeline SHALL follow this sequence for each Work_Product task:
   - Stage 1 (Research — wiki-researcher): Gather source material from body system organs, DuckDB, Slack signals, Asana task context, and web sources. Post the research brief as a pinned comment on the task.
   - Stage 2 (Draft — wiki-writer): Read the research comment and Richard's original idea in the task description. Write a ~500 word draft in html_notes using the Asana HTML formatting guide. Move task to "Review" section.
   - Stage 3 (Review — wiki-critic): Read the draft in html_notes. Score on 5 dimensions (usefulness, clarity, accuracy, dual-audience, economy). Post the review as a comment. IF score >= 8: create an Approval_Subtask for Richard. IF score < 8: post revision notes as a comment and return to Stage 2.
   - Stage 4 (Approval — Richard): Richard reviews the draft and either approves the Approval_Subtask or posts feedback as a comment.
   - Stage 5 (Expansion — wiki-writer): After approval, expand the Work_Product to ~2000 words in html_notes. Move task to "Active" section.
2. EACH pipeline stage SHALL be logged as a comment on the task with the agent name and timestamp, creating a visible audit trail in Asana
3. THE wiki-writer SHALL adapt its output for Asana HTML constraints: use `<strong>` for section titles instead of markdown headers, use `<ul>`/`<ol>` for lists, use `<a href>` for links, use `<em>` for emphasis
4. THE wiki-writer SHALL follow Richard's writing style guides (richard-writing-style.md, richard-style-docs.md, richard-style-amazon.md) when producing Work_Products
5. THE wiki-critic SHALL use the same 5-dimension scoring (usefulness, clarity, accuracy, dual-audience, economy) and the same 8/10 threshold as the wiki pipeline
6. IF the wiki-critic scores a draft below 8 twice consecutively, THE Agent SHALL flag the task for Richard's attention in the daily brief rather than continuing to iterate autonomously
7. THE wiki-researcher SHALL have access to all MCP tools (DuckDB, Slack, email, Asana, web search) for gathering source material

### Requirement 4: Date Window Execution

**User Story:** As Richard, I want the agent to start and finish work based on Begin Date and Due Date, so that I control the agent's work schedule by setting dates on tasks.

#### Acceptance Criteria

1. DURING AM-2, THE Agent SHALL identify all ABPS_AI_Project tasks where Begin Date <= today AND the task is not completed AND the task is not in "Active" or "Archive" sections
2. WHEN a task enters its Date_Window for the first time, THE Agent SHALL initiate the pipeline (Requirement 3) starting with Stage 1 (Research)
3. IF a task's Due Date is within 2 calendar days AND the Work_Product has not reached "Review" stage, THEN THE Agent SHALL escalate the task to Priority_RW=Today and flag it in the daily brief
4. IF a task's Due Date has passed AND the Work_Product is not approved, THEN THE Agent SHALL flag the task as overdue in the daily brief and write a Kiro_RW entry noting the overdue status and recommended action (extend due date, reduce scope, or kill)
5. THE Agent SHALL NOT work on tasks whose Begin Date is in the future, even if they are in "In Progress" section

### Requirement 5: Refresh Cadence

**User Story:** As Richard, I want the agent to revisit and improve completed documents on a regular schedule, so that work products stay current without me having to remember to ask.

#### Acceptance Criteria

1. DURING AM-2, THE Agent SHALL check all tasks in the "Active" section that have a Frequency_Field value other than "one-time"
2. THE Agent SHALL determine refresh due dates using the period-based check in Recurring_Task_State: compute current_period from today's date and cadence (weekly=YYYY-WNN, monthly=YYYY-MM, quarterly=YYYY-QN), compare against last_run_period. IF last_run_period != current_period, the refresh is due.
3. WHEN a refresh is due, THE Agent SHALL: (a) read the current html_notes content, (b) gather fresh context from body system organs, DuckDB, and recent Slack/email signals, (c) update the Work_Product with current information, improvements, or corrections, (d) add a dated revision note at the top of the document, (e) post a comment noting what was updated and why
4. WHEN the Agent completes a refresh, THE Agent SHALL update the corresponding entry in Recurring_Task_State with the current date and period
5. IF a Frequency_Field value is "one-time", THEN THE Agent SHALL move the task to "Archive" after approval and final expansion, and not schedule any refresh
6. THE Agent SHALL register each Active task with a Frequency in Recurring_Task_State when the task first moves to Active

### Requirement 6: Work Product Authoring Standards

**User Story:** As Richard, I want documents written in my voice and meeting Amazon writing standards, so that work products are immediately usable without rewriting.

#### Acceptance Criteria

1. THE Agent SHALL write all Work_Products as HTML content in html_notes using the verified Asana HTML tags only: `<body>`, `<strong>`, `<em>`, `<u>`, `<s>`, `<code>`, `<a href>`, `<ul>`, `<ol>`, `<li>`
2. DRAFT Work_Products (~500 words) SHALL include: bold title, executive summary (2-3 sentences), 3-5 key sections with bold headers, and a "Next Steps" section
3. FULL Work_Products (~2000 words) SHALL include: bold title, executive summary, detailed analysis sections with bold headers, supporting data or evidence, recommendations with reasoning, and next steps with owners and dates
4. THE Agent SHALL load and follow the relevant style guides before writing: richard-writing-style.md (core voice), richard-style-docs.md (document structure), richard-style-amazon.md (leadership-facing norms)
5. THE Agent SHALL preserve any existing content in html_notes that Richard has added, reading current content before writing and integrating rather than overwriting
6. WHEN updating a Work_Product during a refresh cycle, THE Agent SHALL add a bold dated revision line at the top: `<strong>Updated [YYYY-MM-DD]: [what changed]</strong>`
7. THE Agent SHALL connect every metric to registrations, OPS, or customer experience per the Amazon writing norms. Data without interpretation SHALL NOT appear in Work_Products.

### Requirement 7: Asana-Native Workflow Features

**User Story:** As Richard, I want the agent to use Asana's native features (subtasks, approvals, milestones, comments) as workflow infrastructure, so that the project is fully functional within Asana without external dependencies.

#### Acceptance Criteria

1. THE Agent SHALL use Approval subtasks (resource_subtype="approval") as the human-in-the-loop gate between draft and expansion. Richard approves by completing the approval subtask.
2. THE Agent SHALL use subtasks for pipeline stages: "📋 Research: [name]" for research, "✏️ Draft: [name]" for drafting, "🔍 Review: [name]" for critic review. Each subtask is completed when its stage finishes.
3. THE Agent SHALL use milestones (resource_subtype="milestone") for significant project-level events: "🎯 First 10 Active docs", "🎯 All markets documented", etc.
4. THE Agent SHALL use comments (CreateTaskStory) for: research briefs (pinned), critic reviews, revision notes, refresh logs, and pipeline stage transitions. Comments create the audit trail.
5. THE Agent SHALL use sections as workflow stages: Intake → In Progress → Review → Active → Archive. Section moves are the primary status indicator.
6. THE Agent SHALL use Kiro_RW custom field for agent-internal context: triage decisions, pipeline state, refresh history, error logs. This is the agent's scratchpad — not visible in the main task view unless Richard checks the custom field.
7. THE Agent SHALL use Begin Date (start_on) and Due Date (due_on) as the execution window. The agent does not work on tasks outside their date window.

### Requirement 8: Agent Self-Management

**User Story:** As Richard, I want the agent to create its own tasks, update status, and complete work without my intervention, so that the agent operates as an autonomous worker within the ABPS AI project.

#### Acceptance Criteria

1. THE Agent SHALL create subtasks for each pipeline stage when a task enters the pipeline, providing visibility into progress
2. THE Agent SHALL move tasks between sections as work progresses, using section moves as the primary status mechanism
3. WHEN a one-time Work_Product is approved and expanded, THE Agent SHALL move the task to "Archive" section and mark it as completed
4. WHEN the Agent identifies a new document that should be created (from body system signals, meeting notes, or Slack discussions), THE Agent SHALL create a task in Intake_Section with a description of the proposed Work_Product and flag it for Richard's approval in the daily brief
5. THE Agent SHALL write a Kiro_RW entry on every task it modifies, documenting what action was taken, which pipeline agent acted, and why
6. DURING AM-3 (Brief), THE Agent SHALL include a summary of ABPS_AI_Project status: tasks in each section, pipeline stages in progress, upcoming tasks entering their Date_Window this week, overdue tasks, and refresh tasks due this period

### Requirement 9: Integration with Existing Systems

**User Story:** As Richard, I want the ABPS AI project to work seamlessly with the existing morning routine, EOD reconciliation, recurring task state, and wiki pipeline, so that this is an extension of the current system rather than a parallel one.

#### Acceptance Criteria

1. THE Agent SHALL check ABPS_AI_Project during AM-2 alongside My Tasks — scanning Intake for new tasks, checking date windows, and identifying refresh-due Active tasks
2. THE Agent SHALL register all ABPS_AI_Project cadence-tracked tasks in Recurring_Task_State with entries following the existing schema: cadence, last_run, last_run_period, description
3. THE Agent SHALL log all Asana write operations on ABPS_AI_Project tasks to ~/shared/context/active/asana-audit-log.jsonl following the existing audit log format
4. THE Agent SHALL include ABPS_AI_Project tasks in the AM-1 morning snapshot (asana-morning-snapshot.json) as a separate section alongside My Tasks data
5. THE Agent SHALL include ABPS_AI_Project task completions and pipeline progress in the EOD-2 reconciliation and rw-tracker.md daily stats
6. THE Agent SHALL use the same wiki team agent definitions (.kiro/agents/wiki-team/) for the pipeline, with Asana-specific adaptations documented in the agent prompts: output to html_notes instead of staging files, research briefs as comments instead of research/ files, reviews as comments instead of reviews/ files
7. THE Agent SHALL classify ABPS_AI_Project work as Level 5 (Agentic Orchestration) in the Five Levels breakdown, since this is autonomous agent workflow

### Requirement 10: Guardrails and Safety

**User Story:** As Richard, I want the agent to operate safely within the ABPS AI project with full audit trails and human-in-the-loop gates, so that I can trust the agent to work autonomously.

#### Acceptance Criteria

1. THE Agent SHALL verify that every task it modifies in ABPS_AI_Project is assigned to Richard (GID 1212732742544167) before executing any write operation
2. THE Agent SHALL append a JSON record to asana-audit-log.jsonl for every write operation, including: timestamp, tool name, task GID, pipeline_agent (which wiki agent acted), fields modified, and result status
3. THE Agent SHALL present all triage decisions to Richard during AM-2 for approval before executing moves and field changes
4. THE Agent SHALL NOT expand a draft to full length without Richard's explicit approval via the Approval_Subtask mechanism
5. WHEN the Agent writes or updates html_notes, THE Agent SHALL first read the current content via GetTaskDetails to avoid overwriting Richard's additions
6. IF an Asana API call fails, THEN THE Agent SHALL log the failure, write a Kiro_RW entry, retry once, and if still failing, flag the task for manual attention in the daily brief
7. THE wiki-critic SHALL enforce the 8/10 quality threshold — no Work_Product reaches Richard for approval unless it scores 8+ on the critic's 5-dimension review
8. IF the pipeline produces 2 consecutive sub-8 drafts for the same task, THE Agent SHALL stop iterating and present the task to Richard with the critic's feedback for manual direction
