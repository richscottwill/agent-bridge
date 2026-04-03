# Implementation Plan: Asana Portfolio Management

## Overview

Extends the agent's autonomous management from a single project (ABPS AI Content) to Richard's entire Asana workspace. Implementation follows a bottom-up build order: foundation (discovery + GID registry), enrichment layer (My Tasks + cross-project), project-specific automation (recurring tasks, blockers, events, budget, context refresh), hook integration (AM-2, AM-3, EOD-2, guardrails), and validation (property tests + integration script).

All agent logic lives in markdown prompt files, JSON hook configs, and the asana-command-center.md protocol file. Property-based tests use Python with hypothesis in `shared/tools/abps-tests/`.

## Tasks

- [ ] 1. Portfolio Discovery + GID Registration in Command Center
  - [x] 1.1 Add Portfolio Projects section to `shared/context/active/asana-command-center.md`
    - Create the `## Portfolio Projects` section with subsections for ABIX PS and ABPS portfolios
    - For each known child project (AU, MX, WW Testing, WW Acquisition, Paid App), record: project GID, portfolio GID, owner, sections (discovered via GetProjectSections), custom fields (discovered via sample task GetTaskDetails), pinned context task GID, terminal sections, and active status
    - Include the GID Discovery Protocol for portfolio projects (GetPortfolioItems → GetProjectSections → sample task → record)
    - _Requirements: 4.1, 4.2, 4.4_
  - [x] 1.2 Add Paid App event calendar to `shared/context/active/asana-command-center.md`
    - Under the Paid App project profile, add the event calendar table: Prime Day (mid-June, 30d prep, 14d escalation), Back to School (late July, 21d prep, 10d escalation), PBBD (mid-October, 30d prep, 14d escalation), BFCM (late November, 45d prep, 21d escalation), Gift Guide (early December, 30d prep, 14d escalation)
    - Include event keyword list for task matching
    - _Requirements: 15.1_
  - [x] 1.3 Add known recurring task patterns to `shared/context/active/asana-command-center.md`
    - Under AU and MX project profiles, add recurring task pattern tables with task name patterns, cadence, and section
    - AU: Weekly Reporting, AU meetings Agenda (weekly), MBR callout (monthly), Bi-monthly Flash (bi-monthly)
    - MX: WBR (weekly), MBR (monthly), Bi-monthly Flash (bi-monthly), Kingpin (monthly)
    - _Requirements: 13.1_
  - [ ]* 1.4 Write property test for portfolio discovery idempotency (Property 12)
    - **Property 12: Portfolio discovery idempotency**
    - Test that running discovery twice against the same mock Asana state produces identical project profiles with no duplicates or corruption
    - Add to `shared/tools/abps-tests/test_portfolio.py`
    - **Validates: Requirements 4.5**

- [ ] 2. My Tasks Enrichment (Kiro_RW brevity fix, Next action, date gaps)
  - [x] 2.1 Write the Phase 1 Enhancement prompt block for the AM-2 hook
    - Add the `PHASE 1 ENHANCEMENT — MY TASKS DEEP ENRICHMENT` prompt block to `shared/.kiro/hooks/am-2-triage.kiro.hook` after existing Phase 1 task scanning
    - Include: Kiro_RW check (empty or non-brevity format → propose M/D: <10 words), Next action check (empty → propose imperative <15 words), date check (due_on set but start_on null → propose max(today, due_on - 7)), Priority_RW default (Routine set but Priority_RW null → propose "Not urgent")
    - Include enrichment batch presentation format with approve all / approve individually / skip options
    - Include execution logic for approved enrichments with audit logging (project="My_Tasks")
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 2.1, 2.2, 2.3, 2.4, 2.5, 3.1, 3.2, 20.1, 20.3, 20.4, 20.5_
  - [ ]* 2.2 Write property test for Kiro_RW brevity format validation (Property 1)
    - **Property 1: Kiro_RW brevity format validation**
    - Test that all agent-produced Kiro_RW entries match `^\d{1,2}/\d{1,2}: .+` with <10 words after colon, no YYYY-MM-DD, no brackets, no leading zeros
    - Add to `shared/tools/abps-tests/test_portfolio.py`
    - **Validates: Requirements 2.1, 2.2, 2.5**
  - [ ]* 2.3 Write property test for Kiro_RW append and truncation (Property 2)
    - **Property 2: Kiro_RW append and truncation**
    - Test that new entries append on new lines below existing content, and that oldest entries are dropped when approaching 500-char limit while preserving newest
    - Add to `shared/tools/abps-tests/test_portfolio.py`
    - **Validates: Requirements 2.3, 2.4**
  - [ ]* 2.4 Write property test for enrichment gap detection (Property 5)
    - **Property 5: Enrichment gap detection**
    - Test that tasks with any gap (empty Kiro_RW, empty Next_Action, missing start_on with due_on, Routine set but no Priority_RW) are identified, and fully-populated tasks are excluded
    - Add to `shared/tools/abps-tests/test_portfolio.py`
    - **Validates: Requirements 1.1, 1.2, 1.3, 1.4, 5.4**
  - [ ]* 2.5 Write property test for start date computation (Property 6)
    - **Property 6: Start date computation**
    - Test that proposed start_on = max(today, due_on - 7) for all tasks with due_on set and start_on null
    - Add to `shared/tools/abps-tests/test_portfolio.py`
    - **Validates: Requirements 1.3**

- [x] 3. Checkpoint — Verify My Tasks enrichment
  - Ensure all property tests pass (`cd shared/tools/abps-tests && python -m pytest test_portfolio.py -v`), ask the user if questions arise.

- [ ] 4. Cross-Project Task Scanning (AU, MX, Paid App, WW Testing, WW Acquisition)
  - [x] 4.1 Write the Phase 1C prompt block for the AM-2 hook — Steps 1-3 (discovery + scan + enrichment)
    - Add `PHASE 1C — PORTFOLIO PROJECT SCAN` to `shared/.kiro/hooks/am-2-triage.kiro.hook` after Phase 1B
    - Step 1: Portfolio discovery via GetPortfolioItems for ABIX PS and ABPS, new project detection and GID recording
    - Step 2: Per-project task scan via GetTasksFromProject + GetTaskDetails, filter to Richard's tasks only (assignee.gid === 1212732742544167), skip Cross_Team_Tasks for writes
    - Step 3: Field enrichment check (Kiro_RW, Next action, dates) with proposals queued for batch presentation
    - Include portfolio enrichment batch format grouped by project name under "PORTFOLIO ENRICHMENT" header
    - _Requirements: 4.1, 4.2, 4.3, 5.1, 5.2, 5.3, 5.4, 5.5, 20.2, 20.3_
  - [ ]* 4.2 Write property test for assignee guard enforcement (Property 10)
    - **Property 10: Assignee guard enforcement**
    - Test that writes to tasks with assignee !== Richard are blocked, logged as "blocked", and flagged; Cross_Team_Tasks are read-only
    - Add to `shared/tools/abps-tests/test_portfolio.py`
    - **Validates: Requirements 9.1, 9.2, 9.4, 5.2, 5.3**
  - [ ]* 4.3 Write property test for enrichment approval gate (Property 7)
    - **Property 7: Enrichment approval gate**
    - Test that no writes execute before approval, partial approvals write only approved items, rejected items remain unchanged
    - Add to `shared/tools/abps-tests/test_portfolio.py`
    - **Validates: Requirements 1.5, 1.6, 1.7, 13.5, 20.5**

- [ ] 5. Date Window Checks + Near-Due Escalation + Overdue Flagging
  - [x] 5.1 Write the Phase 1C prompt block — Step 4 (date window checks)
    - Add Step 4 to the Phase 1C block in `shared/.kiro/hooks/am-2-triage.kiro.hook`
    - Near-due: due_on within 0-2 days AND not completed AND not terminal section → auto-set Priority_RW to Today, update Kiro_RW and Next action
    - Overdue: due_on < today AND not completed AND not terminal section → flag, update Kiro_RW with "M/D: Overdue [N]d. Extend or close.", set Next action to decision prompt
    - Terminal section exclusion: tasks in discovered terminal sections skip date checks
    - Near-due escalation executes automatically (safety measure); overdue resolution requires approval
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 7.1, 7.2, 7.3, 7.4, 7.5, 11.1, 11.2, 11.3_
  - [ ]* 5.2 Write property test for near-due escalation with terminal section exclusion (Property 8)
    - **Property 8: Near-due escalation with terminal section exclusion**
    - Test: due_on within 0-2 days + not terminal + not completed → Priority_RW = Today; due_on > 2 days or < 0 → no escalation; terminal section → no escalation
    - Add to `shared/tools/abps-tests/test_portfolio.py`
    - **Validates: Requirements 6.1, 6.2, 6.3, 6.4, 6.5, 11.2**
  - [ ]* 5.3 Write property test for overdue flagging without auto-resolution (Property 9)
    - **Property 9: Overdue flagging without auto-resolution**
    - Test: overdue + not terminal → flagged with correct N days; agent never auto-extends, auto-completes, or auto-changes scope
    - Add to `shared/tools/abps-tests/test_portfolio.py`
    - **Validates: Requirements 7.1, 7.2, 7.4, 7.5**
  - [ ]* 5.4 Write property test for Next_Action co-modification (Property 3)
    - **Property 3: Next_Action co-modification**
    - Test that every field write (Kiro_RW, Priority_RW, dates, etc.) also updates Next_Action in the same or immediately following operation
    - Add to `shared/tools/abps-tests/test_portfolio.py`
    - **Validates: Requirements 3.1, 3.6**
  - [ ]* 5.5 Write property test for Next_Action format validation (Property 4)
    - **Property 4: Next_Action format validation**
    - Test: single sentence, <15 words, imperative verb; tasks with incomplete subtasks derive from first incomplete subtask
    - Add to `shared/tools/abps-tests/test_portfolio.py`
    - **Validates: Requirements 3.2, 3.3, 3.5**

- [ ] 6. Status Update Staleness Detection
  - [x] 6.1 Write the Phase 1C prompt block — Step 5 (status staleness)
    - Add Step 5 to the Phase 1C block in `shared/.kiro/hooks/am-2-triage.kiro.hook`
    - Call GetStatusUpdatesFromObject for each portfolio project
    - Parse created_at from most recent status update; if >14 days → flag as stale; if exactly 14 days → NOT stale
    - Extract health color (green/yellow/red) from latest update
    - Flag projects with no status updates ever as "never updated"
    - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5_
  - [ ]* 6.2 Write property test for status staleness threshold (Property 13)
    - **Property 13: Status staleness threshold**
    - Test: >14 days → stale; exactly 14 days → not stale; never updated → flagged; health color accurately extracted
    - Add to `shared/tools/abps-tests/test_portfolio.py`
    - **Validates: Requirements 8.2, 8.4, 8.5**

- [x] 7. Checkpoint — Verify cross-project scanning and date checks
  - Ensure all property tests pass (`cd shared/tools/abps-tests && python -m pytest test_portfolio.py -v`), ask the user if questions arise.

- [ ] 8. Recurring Task Auto-Creation (AU + MX)
  - [x] 8.1 Add recurring task detection and auto-creation logic to the Phase 1C prompt block
    - Add recurring task detection to `shared/.kiro/hooks/am-2-triage.kiro.hook` Phase 1C
    - Detection: completed tasks in AU/MX matching keywords (Weekly, Bi-monthly, Monthly, WBR, MBR, Agenda, Flash, Kingpin)
    - Date computation: weekly +7d (start_on = due_on - 2), bi-monthly +14d (start_on = due_on - 3), monthly same day next month (start_on = due_on - 5)
    - CreateTask with same name, assignee=Richard, same project, computed dates, copy Routine + section + project-specific fields (AU Priority GID: 1212762061512785, Task Progress GID: 1212762061512790)
    - Present to Richard for approval; delete if rejected
    - _Requirements: 13.1, 13.2, 13.3, 13.4, 13.5, 13.6_
  - [ ]* 8.2 Write property test for recurring task date computation (Property 14)
    - **Property 14: Recurring task date computation**
    - Test: weekly → +7d/start -2; bi-monthly → +14d/start -3; monthly → same day next month/start -5
    - Add to `shared/tools/abps-tests/test_portfolio.py`
    - **Validates: Requirements 13.2, 13.3**
  - [ ]* 8.3 Write property test for recurring task field preservation (Property 15)
    - **Property 15: Recurring task field preservation**
    - Test: new instance copies Routine, section, and project-specific custom fields from completed task
    - Add to `shared/tools/abps-tests/test_portfolio.py`
    - **Validates: Requirements 13.4**
  - [ ]* 8.4 Write property test for recurring task pattern detection (Property 16)
    - **Property 16: Recurring task pattern detection**
    - Test: task names with recurring keywords → detected; task names without → not detected
    - Add to `shared/tools/abps-tests/test_portfolio.py`
    - **Validates: Requirements 13.1**

- [ ] 9. Cross-Team Blocker Detection (MX)
  - [x] 9.1 Add cross-team blocker detection logic to the Phase 1C prompt block
    - Add MX-specific blocker detection to `shared/.kiro/hooks/am-2-triage.kiro.hook` Phase 1C
    - Read all MX tasks including Cross_Team_Tasks (never write to them)
    - Flag teammate tasks that are overdue (due_on < today AND not completed)
    - Correlate blockers with Richard's tasks via subtask relationships, name cross-references, or same-section proximity
    - Update Richard's blocked task Kiro_RW: "M/D: Blocked on [teammate] task. [N]d overdue."
    - Update Richard's blocked task Next_Action: "Follow up with [teammate] on [blocker task name]"
    - Surface all blockers in daily brief with teammate name, days overdue, suggested action
    - _Requirements: 14.1, 14.2, 14.3, 14.4, 14.5, 14.6_
  - [ ]* 9.2 Write property test for cross-team blocker detection and response (Property 17)
    - **Property 17: Cross-team blocker detection and response**
    - Test: overdue teammate tasks flagged; correlated blockers update Richard's Kiro_RW and Next_Action; all blockers surfaced in brief; no writes to teammate tasks
    - Add to `shared/tools/abps-tests/test_portfolio.py`
    - **Validates: Requirements 14.2, 14.3, 14.4, 14.5, 14.6**

- [ ] 10. Event Countdown Automation (Paid App)
  - [x] 10.1 Add event countdown and stale task triage logic to the Phase 1C prompt block
    - Add Paid App-specific event countdown to `shared/.kiro/hooks/am-2-triage.kiro.hook` Phase 1C
    - Read event calendar from asana-command-center.md; for each event within prep window, scan tasks by keyword match
    - Escalation: Backlog → Prioritized (prep window), Prioritized → In progress + Priority_RW=Today (escalation trigger), Blocked + escalation trigger → critical blocker flag
    - Stale task triage: tasks overdue >30 days → classify (event-related → archive, budget-related → extend/escalate, other → kill-or-revive), present batch to Richard
    - Promo event template: new event task detected → propose standardized subtask structure (Campaign brief, Budget confirmation, Creative assets, Campaign build, Post-event analysis) with relative due dates
    - _Requirements: 15.2, 15.3, 15.4, 15.5, 15.6, 16.1, 16.2, 16.3, 16.4, 16.5, 16.6_
  - [ ]* 10.2 Write property test for event countdown escalation (Property 18)
    - **Property 18: Event countdown escalation**
    - Test: Backlog + prep window → propose Prioritized; Prioritized + escalation trigger → propose In progress + Today; Blocked + escalation trigger → critical flag
    - Add to `shared/tools/abps-tests/test_portfolio.py`
    - **Validates: Requirements 15.2, 15.3, 15.4, 15.5**
  - [ ]* 10.3 Write property test for stale task triage classification (Property 19)
    - **Property 19: Stale task triage classification**
    - Test: >30d overdue → severely stale; event-related → archive; budget-related → extend/escalate; other → kill-or-revive
    - Add to `shared/tools/abps-tests/test_portfolio.py`
    - **Validates: Requirements 16.1, 16.2, 16.3, 16.4**

- [ ] 11. Budget/PO Tracking (MX + Paid App)
  - [x] 11.1 Add budget task detection and escalation logic to the Phase 1C prompt block
    - Add budget tracking to `shared/.kiro/hooks/am-2-triage.kiro.hook` Phase 1C
    - Classify Budget_Tasks by keyword match (budget, PO, spend, invoice, reconciliation, actuals, forecast)
    - Budget near-due threshold: 3 days (not standard 2); overdue budget tasks flagged as critical
    - Paid App monthly actuals: check for corresponding Brandon update task, propose creation if missing
    - _Requirements: 17.1, 17.2, 17.3, 17.4, 17.5_
  - [ ]* 11.2 Write property test for budget task escalation threshold (Property 20)
    - **Property 20: Budget task escalation threshold**
    - Test: Budget_Tasks use 3-day threshold instead of 2; overdue budget tasks flagged as critical with higher visibility
    - Add to `shared/tools/abps-tests/test_portfolio.py`
    - **Validates: Requirements 17.1, 17.2, 17.3**

- [ ] 12. Market Context Auto-Refresh (AU + MX)
  - [x] 12.1 Add context task refresh logic to the Phase 1C prompt block
    - Add context refresh to `shared/.kiro/hooks/am-2-triage.kiro.hook` Phase 1C
    - After scanning each project: compile summary (active count, overdue, near-due, blockers, upcoming deadlines, recent completions, recurring status, budget status)
    - Compare against current Context_Task content; if Material_Change detected → read-before-write → UpdateTask(html_notes)
    - Use standard HTML structure with allowed tags only (body, strong, em, ul, ol, li, a, code)
    - AU and MX: daily refresh; other projects: weekly
    - Skip update if no material change
    - _Requirements: 18.1, 18.2, 18.3, 18.4, 18.5, 18.6_
  - [ ]* 12.2 Write property test for context task conditional refresh (Property 21)
    - **Property 21: Context task conditional refresh**
    - Test: Material_Change → update; no change → no write; read-before-write preserves Richard's additions; only allowed HTML tags used
    - Add to `shared/tools/abps-tests/test_portfolio.py`
    - **Validates: Requirements 18.1, 18.2, 18.3, 18.4, 18.6**

- [x] 13. Checkpoint — Verify project-specific automation
  - Ensure all property tests pass (`cd shared/tools/abps-tests && python -m pytest test_portfolio.py -v`), ask the user if questions arise.

- [ ] 14. AM-2 Hook Updates (Phase 1 Enhancement + Phase 1C + Step 6 presentation)
  - [x] 14.1 Write the Phase 1C Step 6 — unified portfolio findings presentation
    - Add Step 6 to the Phase 1C block in `shared/.kiro/hooks/am-2-triage.kiro.hook`
    - Present portfolio scan summary: per-portfolio project list with task count, overdue count, near-due count, status health, staleness
    - Present portfolio enrichment batch grouped by project
    - Present portfolio alerts: near-due tasks, overdue tasks, stale projects, cross-team blockers, budget alerts
    - Include recurring task auto-creation proposals and stale task triage recommendations
    - _Requirements: 5.5, 5.6, 12.4, 12.5, 20.2_
  - [x] 14.2 Wire Phase 1 Enhancement and Phase 1C into the AM-2 hook execution flow
    - Update `shared/.kiro/hooks/am-2-triage.kiro.hook` to ensure Phase 1 Enhancement runs after existing Phase 1, Phase 1C runs after Phase 1B, and Phase 2 (Interactive Command Center) runs last
    - Verify the hook prompt references all GIDs from asana-command-center.md Portfolio Projects section
    - Ensure the hook prompt includes API failure handling: log → retry once → flag if retry fails (Requirement 19)
    - _Requirements: 19.1, 19.2, 19.3, 19.4, 19.5, 19.6_
  - [ ]* 14.3 Write property test for API retry limit (Property 22)
    - **Property 22: API retry limit**
    - Test: exactly one retry after 2s pause; read failure → skip task; audit log write failure → continue pipeline
    - Add to `shared/tools/abps-tests/test_portfolio.py`
    - **Validates: Requirements 19.1, 19.4, 19.5, 19.6**

- [ ] 15. AM-3 Brief Portfolio Section
  - [x] 15.1 Add Portfolio Status section to the AM-3 brief hook
    - Update `shared/.kiro/hooks/am-3-brief.kiro.hook` to include the Portfolio Status section after existing ABPS AI Document Factory section
    - Display per-portfolio project list: task count, overdue count, near-due count, health color (🟢/🟡/🔴), last status update date
    - Stale projects: warning indicator next to project entry
    - Consolidated alerts subsection: near-due tasks, overdue tasks, stale projects, cross-team blockers
    - Budget Tasks subsection: all active Budget_Tasks across MX and Paid App with status and due dates
    - _Requirements: 12.1, 12.2, 12.3, 12.4, 12.5, 17.4_
  - [ ]* 15.2 Write property test for brief portfolio content completeness (Property 23)
    - **Property 23: Brief portfolio content completeness**
    - Test: each project shows task count, overdue count, near-due count, health color, last update date; stale projects have warning; blockers in alerts subsection
    - Add to `shared/tools/abps-tests/test_portfolio.py`
    - **Validates: Requirements 12.2, 12.3, 12.5**
  - [ ]* 15.3 Write property test for enrichment proposal completeness (Property 24)
    - **Property 24: Enrichment proposal completeness**
    - Test: each proposal shows task name, GID, current value (or "empty"), proposed value; portfolio enrichments grouped by project
    - Add to `shared/tools/abps-tests/test_portfolio.py`
    - **Validates: Requirements 20.3, 20.2**

- [ ] 16. EOD-2 Reconciliation Portfolio Section
  - [x] 16.1 Add portfolio reconciliation to the EOD-2 hook
    - Update `shared/.kiro/hooks/eod-2-system-refresh.kiro.hook` to include portfolio task reconciliation
    - Compare morning snapshot portfolio_projects data against current state
    - Surface: tasks completed today across portfolio projects, new overdue tasks since morning, enrichment coverage changes, recurring tasks created, blocker status changes
    - _Requirements: 5.6, 12.1_

- [ ] 17. Guardrail Updates
  - [x] 17.1 Update audit hook to include project field for portfolio writes
    - Update `shared/.kiro/hooks/audit-asana-writes.kiro.hook` to include the `project` field in audit log entries
    - Project identifiers: AU, MX, WW_Testing, WW_Acquisition, Paid_App, My_Tasks, ABPS_AI_Content
    - Extended format includes: task_name, project, pipeline_agent (null for portfolio), pipeline_stage (null for portfolio)
    - Ensure append-only behavior — no overwrites or truncation
    - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5_
  - [x] 17.2 Verify guard-asana hook covers portfolio project tasks
    - Review `shared/.kiro/hooks/guard-asana.kiro.hook` to confirm assignee verification applies to all portfolio project writes
    - Ensure defense-in-depth: both algorithm-level (Phase 1C prompt) and hook-level (guard-asana) enforce assignee === Richard
    - Blocked writes must log result="blocked" and flag in daily brief
    - _Requirements: 9.1, 9.2, 9.3, 9.4_
  - [ ]* 17.3 Write property test for audit log correctness (Property 11)
    - **Property 11: Audit log correctness**
    - Test: portfolio writes include correct project identifier from allowed set; result field accurate; append-only behavior
    - Add to `shared/tools/abps-tests/test_portfolio.py`
    - **Validates: Requirements 10.1, 10.2, 10.3, 10.4, 10.5**

- [ ] 18. Update Morning Snapshot Schema
  - [x] 18.1 Extend `shared/context/active/asana-morning-snapshot.json` schema
    - Add `my_tasks_enrichment` section: total_incomplete, missing_kiro_rw, missing_next_action, missing_routine, missing_dates, enrichment_coverage_pct
    - Add `portfolio_projects` section with abix_ps and abps subsections, each containing per-project stats: richard_task_count, overdue_count, near_due_count, missing_fields_count, last_status_update, status_health, status_stale
    - Update AM-2 hook to populate these sections during Phase 1 Enhancement and Phase 1C
    - _Requirements: 12.2, 5.6_

- [x] 19. Checkpoint — Verify hook integration and guardrails
  - Ensure all property tests pass (`cd shared/tools/abps-tests && python -m pytest test_portfolio.py -v`), ask the user if questions arise.

- [ ] 20. Integration Test Script
  - [x] 20.1 Create integration test checklist at `shared/tools/abps-tests/integration-test-portfolio.md`
    - Dry-run AM-2 Phase 1 Enhancement: verify enrichment proposals generated for tasks with missing fields
    - Dry-run AM-2 Phase 1C: verify portfolio discovery returns all 5 child projects, task scan filters to Richard only, date checks fire correctly, status staleness detected
    - Dry-run AM-3: verify Portfolio Status section appears with correct format
    - Dry-run EOD-2: verify portfolio reconciliation section appears
    - Verify audit log entries include project field for portfolio writes
    - Verify guard-asana blocks writes to teammate tasks in portfolio projects
    - Verify recurring task detection for known AU/MX patterns
    - Verify cross-team blocker detection in MX
    - Verify event countdown logic for Paid App
    - Verify budget task 3-day escalation threshold
    - Verify context task refresh with material change detection
    - _Requirements: all_

- [x] 21. Final Checkpoint
  - Ensure all property tests pass, all hook prompts are syntactically valid, and the integration test checklist is complete. Ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation
- Property tests validate universal correctness properties using Python + hypothesis in `shared/tools/abps-tests/`
- All "code" in this workspace is markdown prompt text and JSON config — implementation means writing/editing these files
- The AM-2 hook is the primary execution surface; most tasks add prompt blocks to it
- Existing Phase 1 (My Tasks basic scan) and Phase 1B (ABPS AI Content pipeline) must remain unaffected
