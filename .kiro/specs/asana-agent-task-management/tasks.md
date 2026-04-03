# Implementation Plan: Asana Agent Task Management (ABPS AI Project)

## Overview

Build the ABPS AI Project as an autonomous document factory inside Asana. Implementation follows a bottom-up build order: project structure → intake triage → multi-agent pipeline (5 stages) → date/cadence execution → hook integrations → wiki agent adaptations → guardrails → property-based tests → end-to-end validation. All agent logic lives in markdown prompt files and JSON configs. Property-based tests use Python with `hypothesis`.

## Tasks

- [ ] 1. Project setup and GID discovery
  - [x] 1.1 Create ABPS AI Project sections and record GIDs
    - Update `asana-command-center.md` with a new `## ABPS AI Project` section
    - Use `CreateProjectSection` to create: "Intake", "In Progress", "Review", "Active", "Archive"
    - Use `GetProjectSections` to read back section GIDs and record them in command center
    - Document the GID discovery protocol: `GetProjectSections` → `GetTaskDetails` → inspect `custom_fields`
    - _Requirements: 1.1, 1.2, 1.4, 1.5_

  - [x] 1.2 Create Frequency custom field and register GIDs
    - Create enum field "Frequency" with options: weekly, monthly, quarterly, one-time
    - Record Frequency field GID and all option GIDs in `asana-command-center.md`
    - Verify setup by reading back all sections and custom fields
    - _Requirements: 1.3, 1.4, 1.5_

- [x] 2. Checkpoint — Verify project structure
  - Ensure all sections exist, Frequency field is attached, all GIDs recorded in command center. Ask the user if questions arise.

- [ ] 3. Intake triage logic (wiki-editor)
  - [x] 3.1 Implement AM-2 Intake scan logic
    - Add ABPS_AI_Project scanning to AM-2 hook prompt
    - Filter: tasks in Intake section where Routine field is not set (untriaged indicator)
    - Use `GetTasksFromProject` + `GetTaskDetails` to read custom fields and dates
    - Present triage decisions to Richard for approval before executing
    - _Requirements: 2.1, 2.5, 10.3_

  - [x] 3.2 Implement wiki-editor triage field assignment
    - Analyze task name and description to determine: Routine bucket, Priority_RW, Frequency, Work_Product type
    - Work_Product types: guide, reference, decision, playbook, analysis
    - Write Kiro_RW entry with: triage date, assigned fields, Work_Product type, one-sentence scope statement
    - _Requirements: 2.2, 2.4_

  - [x] 3.3 Implement date default logic
    - If no Begin Date (`start_on`): set to today
    - If no Due Date (`due_on`): set to today + 7 calendar days
    - Note default dates in Kiro_RW
    - Tasks with existing dates retain original values
    - _Requirements: 2.3_

  - [x] 3.4 Implement post-triage section move and subtask creation
    - After Richard approves: move task to "In Progress" if Begin Date <= today
    - Leave in Intake with fields applied if Begin Date is in the future
    - Create research subtask: "📋 Research: [parent task name]" assigned to Richard
    - _Requirements: 2.6, 2.7_

  - [ ]* 3.5 Write property tests for intake triage (Properties 2, 3, 4, 5)
    - **Property 2: Intake filter returns only untriaged tasks**
    - **Property 3: Triage produces valid field assignments**
    - **Property 4: Missing dates receive correct defaults**
    - **Property 5: Date window determines section placement**
    - **Validates: Requirements 2.1, 2.2, 2.3, 2.6, 4.5, 7.7**

- [x] 4. Checkpoint — Intake triage working
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 5. Multi-agent pipeline — Stage 1: Research (wiki-researcher)
  - [x] 5.1 Implement research stage invocation
    - When a task enters its date window for the first time (no pipeline subtasks exist): initiate pipeline
    - Invoke wiki-researcher with: task description, Kiro_RW context, body organs, DuckDB, Slack, email, web sources
    - Post research brief as a pinned comment: `CreateTaskStory(html_text=..., is_pinned="true")`
    - Complete the "📋 Research: [name]" subtask
    - Log stage transition as comment with agent name and timestamp
    - _Requirements: 3.1 (Stage 1), 3.2, 3.7, 4.2_

  - [ ]* 5.2 Write property test for pipeline stage ordering (Property 7)
    - **Property 7: Pipeline stages execute in order**
    - **Validates: Requirements 3.1**

- [ ] 6. Multi-agent pipeline — Stage 2: Draft (wiki-writer)
  - [x] 6.1 Implement draft stage invocation
    - wiki-writer reads: research pinned comment, Richard's original idea in task description, style guides
    - Write ~500w draft in `html_notes` using Asana HTML formatting guide
    - Use only allowed tags: `<body>`, `<strong>`, `<em>`, `<u>`, `<s>`, `<code>`, `<a href>`, `<ul>`, `<ol>`, `<li>`
    - Draft structure: bold title, executive summary (2-3 sentences), 3-5 bold-headed sections, "Next Steps" section
    - Create and complete subtask "✏️ Draft: [name]"
    - Move task to "Review" section
    - Log stage transition as comment
    - _Requirements: 3.1 (Stage 2), 3.2, 3.3, 3.4, 6.1, 6.2, 6.4_

  - [ ]* 6.2 Write property tests for draft output (Properties 1, 6, 16)
    - **Property 1: HTML output contains only allowed tags**
    - **Property 6: Pipeline subtasks follow naming convention**
    - **Property 16: Work product drafts contain required structural elements**
    - **Validates: Requirements 3.3, 6.1, 2.7, 7.2, 8.1, 6.2, 6.3**

- [ ] 7. Multi-agent pipeline — Stage 3: Review (wiki-critic)
  - [x] 7.1 Implement critic review stage
    - wiki-critic reads `html_notes` (the draft) and research comment
    - Score on 5 dimensions: usefulness, clarity, accuracy, dual-audience, economy
    - Post review as comment with scores and feedback
    - IF average score >= 8: create Approval subtask (`CreateTask(resource_subtype="approval", parent=task_gid, assignee=1212732742544167)`) named "✅ Approve: [name]"
    - IF score < 8: post revision notes as comment, return to Stage 2 (wiki-writer revises)
    - Create and complete subtask "🔍 Review: [name]"
    - Track consecutive sub-8 count in Kiro_RW
    - IF 2 consecutive sub-8 scores: stop iterating, flag for Richard in daily brief
    - Log stage transition as comment
    - _Requirements: 3.1 (Stage 3), 3.2, 3.5, 3.6, 7.2, 10.7, 10.8_

  - [ ]* 7.2 Write property tests for critic scoring (Properties 8, 9)
    - **Property 8: Critic score determines approval path**
    - **Property 9: Two consecutive sub-8 scores trigger escalation**
    - **Validates: Requirements 3.5, 3.6, 10.7, 10.8**

- [ ] 8. Multi-agent pipeline — Stage 4: Approval detection
  - [x] 8.1 Implement approval detection in AM-2 scan
    - For tasks in Review section: `GetSubtasksForTask` → find subtask with `resource_subtype="approval"`
    - If approval subtask `completed === true`: proceed to Stage 5 (expansion)
    - If `completed === false`: still pending, skip
    - Detect rejection: check for Richard's comments after approval subtask creation → treat as revision request → return to Stage 2
    - Update Kiro_RW with approval/rejection status
    - _Requirements: 3.1 (Stage 4), 7.1, 10.4_

  - [ ]* 8.2 Write property test for approval gate (Property 22)
    - **Property 22: Expansion requires approved Approval subtask**
    - **Validates: Requirements 10.4**

- [ ] 9. Multi-agent pipeline — Stage 5: Expansion (wiki-writer)
  - [x] 9.1 Implement expansion after approval
    - wiki-writer expands Work_Product from ~500w to ~2000w in `html_notes`
    - Full document structure: bold title, executive summary, context, detailed analysis sections, recommendations, next steps with owners/dates
    - Read current `html_notes` first (read-before-write) to preserve any Richard additions
    - Move task to "Active" section
    - Log expansion as comment with agent name and timestamp
    - _Requirements: 3.1 (Stage 5), 3.2, 3.3, 6.3, 6.5, 10.5_

  - [ ]* 9.2 Write property test for read-before-write (Property 17)
    - **Property 17: Read-before-write preserves existing content**
    - **Validates: Requirements 6.5, 10.5**

- [x] 10. Checkpoint — Full pipeline working
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 11. Date window execution
  - [x] 11.1 Implement date window checks in AM-2
    - Filter: tasks where `start_on <= today AND NOT completed AND NOT in Active/Archive`
    - For tasks entering window for first time (no pipeline subtasks): initiate pipeline
    - Agent SHALL NOT work on tasks with future Begin Date
    - _Requirements: 4.1, 4.2, 4.5_

  - [x] 11.2 Implement near-due escalation
    - If Due Date within 2 calendar days AND task not in Review AND not completed: set Priority_RW to "Today"
    - Flag in daily brief
    - _Requirements: 4.3_

  - [x] 11.3 Implement overdue flagging
    - If Due Date < today AND not completed AND no approved Approval subtask: flag as overdue
    - Write Kiro_RW entry with recommended action: extend due date, reduce scope, or kill
    - Include in daily brief
    - _Requirements: 4.4_

  - [ ]* 11.4 Write property tests for date window logic (Properties 10, 11, 12)
    - **Property 10: Date window filter identifies correct tasks**
    - **Property 11: Near-due tasks are escalated**
    - **Property 12: Overdue tasks are flagged**
    - **Validates: Requirements 4.1, 4.3, 4.4**

- [ ] 12. Refresh cadence
  - [x] 12.1 Implement recurring-task-state.json registration
    - When task moves to Active with Frequency != "one-time": register in `recurring-task-state.json`
    - Key format: `abps_ai_{task_gid}`
    - Entry: `{ cadence, last_run, last_run_period, description: "ABPS AI: {task_name} — refresh work product" }`
    - _Requirements: 5.6, 9.2_

  - [x] 12.2 Implement period computation
    - Weekly: `YYYY-WNN` (ISO week number)
    - Monthly: `YYYY-MM`
    - Quarterly: `YYYY-QN` (Q1=Jan-Mar, Q2=Apr-Jun, Q3=Jul-Sep, Q4=Oct-Dec)
    - Compare `last_run_period` against `current_period` — if different, refresh is due
    - _Requirements: 5.2_

  - [x] 12.3 Implement refresh execution in AM-2
    - Check Active section tasks with Frequency != "one-time" against recurring-task-state.json
    - When refresh due: read current `html_notes`, invoke wiki-researcher for fresh context, invoke wiki-writer to update
    - Add dated revision line: `<strong>Updated [YYYY-MM-DD]: [what changed]</strong>`
    - Post comment: "🔄 Refresh completed: [summary]"
    - Update `recurring-task-state.json` with current date and period
    - _Requirements: 5.1, 5.2, 5.3, 5.4_

  - [x] 12.4 Implement one-time task archival
    - After approval + expansion for Frequency="one-time": move to "Archive", mark completed
    - Do NOT register in recurring-task-state.json
    - Do NOT include in refresh checks
    - _Requirements: 5.5, 8.3_

  - [ ]* 12.5 Write property tests for refresh cadence (Properties 13, 14, 15, 18)
    - **Property 13: Period computation is correct for all cadences**
    - **Property 14: Recurring state registration round-trip**
    - **Property 15: One-time tasks archive after expansion**
    - **Property 18: Refresh updates include dated revision note**
    - **Validates: Requirements 5.2, 5.3, 5.4, 5.5, 5.6, 8.3, 9.2**

- [x] 13. Checkpoint — Date window and refresh working
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 14. AM-2 hook update
  - [x] 14.1 Extend AM-2 prompt with ABPS_AI_Project scanning
    - Add full ABPS scan sequence to AM-2 hook: intake scan, date window check, overdue check, refresh check
    - Scan runs alongside existing My Tasks scan
    - Include all findings in AM-2 output for Richard's review
    - _Requirements: 9.1_

- [ ] 15. AM-3 brief update
  - [x] 15.1 Include ABPS_AI_Project status in daily brief
    - Add `abps_ai` section to morning snapshot: intake_count, in_progress, in_review, active_count, archive_count
    - Include pipeline stages in progress, upcoming tasks entering window this week, overdue tasks, refresh tasks due
    - Classify ABPS work as Level 5 (Agentic Orchestration) in Five Levels breakdown
    - _Requirements: 8.6, 9.4, 9.7_

- [ ] 16. EOD-2 reconciliation update
  - [x] 16.1 Include ABPS_AI_Project in EOD stats
    - Add ABPS task completions and pipeline progress to EOD-2 reconciliation
    - Include in rw-tracker.md daily stats
    - _Requirements: 9.5_

- [ ] 17. Wiki agent adaptations for Asana pipeline
  - [x] 17.1 Update wiki-editor agent with Asana triage instructions
    - Add Asana-specific section: output to Kiro_RW instead of editorial calendar, triage via custom fields instead of file-based assignment
    - Document Work_Product type classification logic for Asana tasks
    - _Requirements: 3.1, 9.6_

  - [x] 17.2 Update wiki-researcher agent with Asana output surface
    - Add Asana-specific section: post research brief as pinned comment (`CreateTaskStory(html_text, is_pinned="true")`) instead of `wiki/research/{slug}-research.md`
    - Document context sources: task description, Kiro_RW, body organs, DuckDB, Slack, email, web
    - _Requirements: 3.1, 3.7, 9.6_

  - [x] 17.3 Update wiki-writer agent with Asana HTML output
    - Add Asana-specific section: write to `html_notes` instead of `wiki/staging/{slug}.md`
    - Include Asana HTML formatting guide: `<strong>` for headers, allowed tags only, `<body>` wrapper
    - Include draft template (~500w) and full document template (~2000w)
    - Load style guides: richard-writing-style.md, richard-style-docs.md, richard-style-amazon.md
    - _Requirements: 3.1, 3.3, 3.4, 6.1, 6.4, 9.6_

  - [x] 17.4 Update wiki-critic agent with Asana review output
    - Add Asana-specific section: post review as comment instead of `wiki/reviews/{slug}-review.md`
    - Document 5-dimension scoring, 8/10 threshold, approval subtask creation logic
    - Document 2-consecutive-sub-8 escalation rule
    - _Requirements: 3.1, 3.5, 3.6, 9.6_

- [ ] 18. Guardrail implementation
  - [x] 18.1 Implement assignee verification
    - Every write operation on ABPS_AI_Project tasks: `GetTaskDetails` first, verify `assignee.gid === "1212732742544167"`
    - If not Richard's task: block write, log with `result="blocked"`, alert in brief
    - _Requirements: 10.1_

  - [x] 18.2 Extend audit log for ABPS pipeline
    - Append JSON line to `asana-audit-log.jsonl` for every write operation
    - Extended fields: `project`, `pipeline_agent`, `pipeline_stage`, `task_name`, `notes`
    - Format per design: `{ timestamp, tool, task_gid, task_name, project, pipeline_agent, pipeline_stage, fields_modified, result, notes }`
    - _Requirements: 9.3, 10.2_

  - [x] 18.3 Implement read-before-write pattern for html_notes
    - Before any `UpdateTask(html_notes)`: read current content via `GetTaskDetails`
    - Check if Richard added content since last agent write (compare against Kiro_RW timestamp)
    - If Richard added content: preserve it, integrate agent content around it
    - _Requirements: 10.5, 6.5_

  - [x] 18.4 Implement API failure retry logic
    - On API failure: log to audit log, write Kiro_RW entry, retry exactly once
    - If retry fails: flag task for manual attention in daily brief
    - No more than one retry per failure
    - _Requirements: 10.6_

  - [ ]* 18.5 Write property tests for guardrails (Properties 19, 20, 21, 23, 24, 25)
    - **Property 19: Kiro_RW is updated on every task modification**
    - **Property 20: Every write operation produces an audit log entry**
    - **Property 21: Assignee verification blocks non-Richard writes**
    - **Property 23: API failure triggers retry then escalation**
    - **Property 24: Each pipeline stage produces a comment**
    - **Property 25: Section membership is consistent with pipeline state**
    - **Validates: Requirements 7.6, 8.5, 9.3, 10.1, 10.2, 10.6, 3.2, 7.4, 7.5, 8.2**

- [x] 19. Checkpoint — All guardrails and integrations working
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 20. Property-based test infrastructure
  - [x] 20.1 Set up Python test project with hypothesis
    - Create `~/shared/tools/abps-tests/` directory
    - Create `requirements.txt` with `hypothesis`, `pytest`
    - Create test generators: `arbTaskName`, `arbHtmlContent`, `arbDate`, `arbCadence`, `arbTask`, `arbCriticScore`, `arbPipelineState`, `arbAssigneeGid`
    - Create `conftest.py` with shared fixtures
    - _Requirements: Design — Testing Strategy_

  - [ ]* 20.2 Implement all 25 property-based tests
    - Each test tagged: `# Feature: asana-agent-task-management, Property {N}: {title}`
    - Minimum 100 iterations per property
    - Tests organized by component: `test_intake.py`, `test_pipeline.py`, `test_dates.py`, `test_cadence.py`, `test_guardrails.py`, `test_html.py`
    - **Properties 1-25 as defined in design document**
    - **Validates: All requirements via correctness properties**

- [ ] 21. End-to-end validation
  - [x] 21.1 Create integration test script
    - Create a test task in Intake section with name and description
    - Run full AM-2 scan: verify triage, field assignment, date defaults
    - Verify pipeline stages: research → draft → review → approval → expansion
    - Verify section moves: Intake → In Progress → Review → Active
    - Verify audit log entries for each write operation
    - Verify recurring-task-state.json registration for non-one-time tasks
    - Verify Kiro_RW entries at each stage
    - _Requirements: All (1-10)_

- [x] 22. Final checkpoint — Full system validated
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Implementation language: Python with `hypothesis` for property-based tests
- Agent logic lives in markdown prompt files (`.kiro/agents/wiki-team/`) and hook prompts
- State lives in JSON files (`recurring-task-state.json`, `asana-audit-log.jsonl`, `asana-morning-snapshot.json`)
- Configuration lives in `asana-command-center.md`
- Each task references specific requirements for traceability
- Property tests validate universal correctness properties from the design document
- Checkpoints ensure incremental validation at logical break points
