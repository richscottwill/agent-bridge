<!-- DOC-0419 | duck_id: tool-integration-test-portfolio -->
# Integration Test Checklist: Asana Portfolio Management

## Overview
Manual integration test checklist covering all portfolio management features. Run each test against live Asana data. Mark ✅ when passing, ❌ when failing, ⏭️ when skipped.

---

## 1. Phase 1 Enhancement — My Tasks Deep Enrichment

- [ ] **1.1** Run AM-2. Verify Phase 1 Enhancement scans all incomplete My Tasks via `SearchTasksInWorkspace(assignee_any='1212732742544167', completed='false')`.
- [ ] **1.2** Verify tasks with empty Kiro_RW are identified and proposed entries use M/D brevity format (no leading zeros, <10 words after date).
- [ ] **1.3** Verify tasks with empty Next_Action are identified and proposed entries are imperative, <15 words.
- [ ] **1.4** Verify tasks with due_on set but start_on null get proposed start_on = max(today, due_on - 7).
- [ ] **1.5** Verify tasks with Routine set but Priority_RW null get proposed Priority_RW = "Not urgent".
- [ ] **1.6** Verify enrichment batch is presented to Richard with approve all / approve individually / skip options.
- [ ] **1.7** Approve one enrichment. Verify UpdateTask writes all fields in a single call. Verify audit log entry has `project: "My_Tasks"`.
- [ ] **1.8** Reject one enrichment. Verify no write occurs for that task.

## 2. Phase 1C — Portfolio Discovery (Step 1)

- [ ] **2.1** Verify `GetPortfolioItems('1212775592612914')` returns AU and MX.
- [ ] **2.2** Verify `GetPortfolioItems('1212762061512816')` returns ABPS portfolio children.
- [ ] **2.3** Verify all 5 managed projects are scanned: AU (`1212762061512767`), MX (`1212775592612917`), WW Testing (`1205997667578893`), WW Acquisition (`1206011235630048`), Paid App (`1205997667578886`).
- [ ] **2.4** If a new project appears in a portfolio, verify it's flagged for Richard and GIDs are recorded in asana-command-center.md.

## 3. Phase 1C — Per-Project Task Scan (Step 2)

- [ ] **3.1** Verify `GetTasksFromProject` is called for each managed project.
- [ ] **3.2** Verify only tasks where `assignee.gid === '1212732742544167'` (Richard) are processed for writes.
- [ ] **3.3** Verify Cross_Team_Tasks (non-Richard assignees) are read but never written to.

## 4. Phase 1C — Field Enrichment Check (Step 3)

- [ ] **4.1** Verify portfolio tasks with empty Kiro_RW get proposed entries in M/D brevity format.
- [ ] **4.2** Verify portfolio tasks with empty Next_Action get proposed entries.
- [ ] **4.3** Verify portfolio enrichment batch is grouped by project name under "PORTFOLIO ENRICHMENT" header.

## 5. Phase 1C — Date Window Checks (Step 4)

- [ ] **5.1** Verify near-due tasks (due_on within 0-2 days, not completed, not terminal section) get Priority_RW auto-set to Today.
- [ ] **5.2** Verify near-due escalation updates Kiro_RW with "M/D: Near-due. Priority escalated."
- [ ] **5.3** Verify overdue tasks (due_on < today, not completed, not terminal section) are flagged with "M/D: Overdue [N]d. Extend or close."
- [ ] **5.4** Verify tasks in terminal sections (Complete/Done) are excluded from date checks.
- [ ] **5.5** Verify overdue tasks are NOT auto-extended or auto-completed — decisions require Richard's approval.

## 6. Phase 1C — Status Update Staleness (Step 5)

- [ ] **6.1** Verify `GetStatusUpdatesFromObject` is called for each managed project.
- [ ] **6.2** Verify projects with last status update >14 days ago are flagged as stale.
- [ ] **6.3** Verify projects with exactly 14-day-old status updates are NOT flagged as stale.
- [ ] **6.4** Verify health color (green/yellow/red) is extracted from latest status update.

## 7. Phase 1C — Recurring Task Detection (AU + MX)

- [ ] **7.1** Complete a recurring task in AU (e.g., "Weekly Reporting"). Verify AM-2 detects it during Phase 1C.
- [ ] **7.2** Verify next instance is auto-created with correct dates: weekly +7d (start_on = due_on - 2), monthly same day next month (start_on = due_on - 5).
- [ ] **7.3** Verify new instance copies Routine, section membership, and project-specific fields (AU Priority, Task Progress).
- [ ] **7.4** Verify auto-created task is presented to Richard for approval before finalizing.
- [ ] **7.5** Reject an auto-created recurring task. Verify it is deleted.

## 8. Phase 1C — Cross-Team Blocker Detection (MX)

- [ ] **8.1** Verify all MX tasks are read, including Cross_Team_Tasks.
- [ ] **8.2** Verify overdue teammate tasks (due_on < today, not completed) are flagged as potential blockers.
- [ ] **8.3** Verify correlated blockers update Richard's task Kiro_RW with "M/D: Blocked on [teammate] task. [N]d overdue."
- [ ] **8.4** Verify correlated blockers update Richard's task Next_Action with follow-up instruction.
- [ ] **8.5** Verify NO writes are made to teammate tasks.
- [ ] **8.6** Verify blockers appear in daily brief with teammate name, days overdue, and suggested action.

## 9. Phase 1C — Event Countdown Automation (Paid App)

- [ ] **9.1** Verify event calendar is read from asana-command-center.md.
- [ ] **9.2** For an event within its prep window: verify Backlog tasks with event keywords get proposed move to Prioritized.
- [ ] **9.3** For an event within its escalation trigger: verify Prioritized tasks get proposed move to In progress + Priority_RW=Today.
- [ ] **9.4** For a Blocked task within escalation trigger: verify it's flagged as critical blocker.
- [ ] **9.5** Create a new task with event keyword. Verify standardized subtask structure is proposed (Campaign brief, Budget confirmation, Creative assets, Campaign build, Post-event analysis).

## 10. Phase 1C — Budget Task Tracking (MX + Paid App)

- [ ] **10.1** Verify tasks with budget keywords (budget, PO, spend, invoice, reconciliation, actuals, forecast) are classified as Budget_Tasks.
- [ ] **10.2** Verify Budget_Tasks use 3-day near-due threshold (not standard 2-day).
- [ ] **10.3** Verify overdue Budget_Tasks are flagged as critical with higher visibility.
- [ ] **10.4** Verify Budget Tasks subsection appears in daily brief.

## 11. Phase 1C — Context Task Refresh (AU + MX)

- [ ] **11.1** Verify context task summary is compiled after scanning each project.
- [ ] **11.2** Verify Material_Change detection: update only when significant changes exist.
- [ ] **11.3** Verify read-before-write: Richard's additions to context tasks are preserved.
- [ ] **11.4** Verify no update when no material change detected.

## 12. AM-3 Brief — Portfolio Status Section

- [ ] **12.1** Run AM-3. Verify Portfolio Status section appears after ABPS AI Document Factory section.
- [ ] **12.2** Verify each project shows: task count, overdue count, near-due count, health color (🟢/🟡/🔴), last status update date.
- [ ] **12.3** Verify stale projects have ⚠️ warning indicator.
- [ ] **12.4** Verify consolidated alerts subsection lists near-due, overdue, stale projects, and cross-team blockers.
- [ ] **12.5** Verify Budget Tasks subsection lists active Budget_Tasks across MX and Paid App.

## 13. EOD-2 — Portfolio Reconciliation

- [ ] **13.1** Run EOD-2. Verify portfolio reconciliation section appears.
- [ ] **13.2** Verify comparison against morning snapshot portfolio_projects data.
- [ ] **13.3** Verify surfaces: tasks completed today, new overdue, enrichment coverage changes, recurring tasks created, blocker changes.

## 14. Audit Hook — Project Field

- [ ] **14.1** Trigger a portfolio write (e.g., update a task in AU). Verify audit log entry includes `"project": "AU"`.
- [ ] **14.2** Verify audit log entries include task_name field.
- [ ] **14.3** Verify project identifiers match allowed set: AU, MX, WW_Testing, WW_Acquisition, Paid_App, My_Tasks, ABPS_AI_Content.
- [ ] **14.4** Verify append-only behavior — previous entries are not overwritten.

## 15. Guard-Asana — Portfolio Coverage

- [ ] **15.1** Attempt to write to a teammate's task in MX. Verify guard-asana blocks the write with ACCESS DENIED.
- [ ] **15.2** Verify blocked write is logged with `result: "blocked"`.
- [ ] **15.3** Write to Richard's task in a portfolio project. Verify guard-asana grants ACCESS GRANTED.
- [ ] **15.4** Verify defense-in-depth: Phase 1C algorithm filters to Richard's tasks AND guard-asana hook enforces assignee check.

## 16. Morning Snapshot — Extended Schema

- [ ] **16.1** After AM-2 completes, verify `asana-morning-snapshot.json` contains `my_tasks_enrichment` section with: total_incomplete, missing_kiro_rw, missing_next_action, missing_routine, missing_dates, enrichment_coverage_pct.
- [ ] **16.2** Verify `portfolio_projects` section contains per-project stats under abix_ps (au, mx) and managed_projects (ww_testing, ww_acquisition, paid_app).
- [ ] **16.3** Verify each project has: richard_task_count, overdue_count, near_due_count, missing_fields_count, last_status_update, status_health, status_stale.

## 17. API Failure Handling

- [ ] **17.1** Simulate API failure (e.g., invalid GID). Verify failure is logged to audit trail.
- [ ] **17.2** Verify exactly one retry after 2-second pause.
- [ ] **17.3** Verify failed task is skipped for current cycle and flagged in daily brief.
- [ ] **17.4** Verify read failure skips task without blocking other tasks.

---

## Test Execution Log

| Date | Tester | Tests Run | Pass | Fail | Skip | Notes |
|------|--------|-----------|------|------|------|-------|
| | | | | | | |
