# Hands — Execution & Tooling

*What gets done and how. Active tasks, dependencies, integrations, hooks, and the systems that turn decisions into action. The canonical action tracker.*

*Operating principle: Reduce decisions, not options. Every task should have a clear next action, a pre-written draft if it involves communication, and a due date that drives My Day. Richard opens his list and acts — he doesn't plan.*

Last updated: 2026-04-04 (EOD-2 run 20)
Sources: rw-tracker.md, Asana My Tasks, ABPS AI Content, Slack scan, DM scan

---

## Priority Actions

<!-- Full task list: db("SELECT id, priority, description, due_date, status, blockers, category FROM task_queue WHERE status != 'DONE' ORDER BY priority, due_date") -->
<!-- Overdue: db("SELECT id, description, due_date, DATEDIFF('day', due_date, CURRENT_DATE) as days_overdue FROM task_queue WHERE due_date < CURRENT_DATE AND status NOT IN ('DONE','BLOCKED') ORDER BY due_date") -->

### Top 5 This Week (snapshot — refreshed EOD 4/4)
| # | Action | Due | Status |
|---|--------|-----|--------|
| P0 | **Testing Approach doc outline** — Kate Apr 16. THE HARD THING. 16 workdays at zero. | Apr 16 | NOT STARTED |
| P1 | **Refmarker mapping audit PoC — AU** — Lena initiated, Brandon PoC'd Richard. High visibility. | Due 4/7 | NOT STARTED |
| P1 | **Respond to Lena** — AU LP URL analysis + CPA overstating. Brandon offering support. | OVERDUE (4/3) | NOT STARTED |
| P1 | **Share ENG budget file with Andrew** — OP1 recalculation | OVERDUE (4/4) | NOT STARTED |
| P1 | **Respond to Lorena** — Q2 expected spend for MX PO | OVERDUE (10d) | NOT STARTED |

16 items overdue (oldest: PAM US PO, 34d). 2 blocked (MX Auto page on Vijeth 16d, Kingpin on Andes 19d). ~96 total tasks in My Tasks.

### Blocker Registry (EOD 4/4)
| Task | Blocker | Owner | First Detected | Days Blocked |
|------|---------|-------|----------------|-------------|
| MX Automotive page | Footer component | Vijeth | 2026-03-20 | 16 |
| Kingpin Goals MX | Andes data unavailable | Andes team | 2026-03-17 | 19 |

## Recurring Execution Work (Google Ads: MX, AU, Paid App)

**Daily:** Spend pacing + anomaly check across MX, AU ($140 CPA target), Paid App.
**Weekly (post-WBR):** WW Dashboard review (flag >10% WoW), MX search terms + competitor IS, AU CPA vs target + OCI readiness, Paid App benchmarks. Update Pre-WBR Callouts Quip if covering for Dwayne.

---

## Dependencies
- Testing Approach doc → no blockers, just start
- Polaris timeline → no blockers
- MX Auto page → blocked by Vijeth footer
- Kingpin Goals → blocked by Andes data
- MX/AU budgets → blocked by R&O tasks

## New Signals (EOD-2 4/4)
- ✅ Daily reset: 8 Today tasks demoted to Urgent with Kiro_RW carry-forward + Next action set.
- ✅ Completed: Flash topics due today (stale 18d close-out).
- ✅ Recurring check: Flash topics not a recurring pattern — no next instance needed.
- ⏳ Refmarker audit PoC — AU (Sweep): due 4/7, begin 4/6. Monday priority.
- ⏳ Refmarker audit PoC — AU (Engine Room): due 4/10, begin 4/9.
- ⏳ Lorena: Q2 MX spend — OVERDUE (10d). Monday.
- ⏳ Lena: AU LP URL analysis — OVERDUE (1d).
- ⏳ Andrew: ENG budget file — OVERDUE (due 4/4). Monday.
- ⚠️ No L1 effort today — 16 workdays at zero. Testing Approach is the hard thing.
- 📅 MONDAY 4/7: Clean Today slate. Polaris weblab dial-up 4/6-4/7. CA OCI launch. Refmarker audit begins.

---

## Task List Structure (Microsoft To-Do)

| List | Purpose | Cap |
|------|---------|-----|
| 🧹 Sweep | Quick unblocking: send, confirm, triage | 5 |
| 🎯 Core | Strategic: test designs, frameworks, stakeholder docs | 4 |
| ⚙️ Engine Room | Hands-on: campaign builds, keyword changes, bids | 6 |
| 📋 Admin | Budget, POs, invoices, compliance, goal updates | 3 |
| 📦 Backlog | Deferred/blocked/future with justification | — |

<!-- To-Do List IDs (for MCP tool calls):
Sweep: AAMkAGQ5NmQwNGZkLWQ0NTAtNGY4Yy1hNjhlLTY0OTU1N2QzYTBhYwAuAAAAAAArsD3iy-SDRrGkcLnEuZ4GAQCIgJPBFelsQrcja-dZLhI0AADUyESHAAA=
Core: AAMkAGQ5NmQwNGZkLWQ0NTAtNGY4Yy1hNjhlLTY0OTU1N2QzYTBhYwAuAAAAAAArsD3iy-SDRrGkcLnEuZ4GAQCIgJPBFelsQrcja-dZLhI0AADUyESIAAA=
Engine Room: AAMkAGQ5NmQwNGZkLWQ0NTAtNGY4Yy1hNjhlLTY0OTU1N2QzYTBhYwAuAAAAAAArsD3iy-SDRrGkcLnEuZ4GAQCIgJPBFelsQrcja-dZLhI0AADUyESJAAA=
Admin: AAMkAGQ5NmQwNGZkLWQ0NTAtNGY4Yy1hNjhlLTY0OTU1N2QzYTBhYwAuAAAAAAArsD3iy-SDRrGkcLnEuZ4GAQCIgJPBFelsQrcja-dZLhI0AADUyESKAAA=
Backlog: AAMkAGQ5NmQwNGZkLWQ0NTAtNGY4Yy1hNjhlLTY0OTU1N2QzYTBhYwAuAAAAAAArsD3iy-SDRrGkcLnEuZ4GAQCIgJPBFelsQrcja-dZLhI0AADWyS4nAAA=
-->

## Key Outlook Folders
| Folder | ID |
|--------|-----|
| Auto-Comms (Asana) | `AAMkAGQ5NmQwNGZkLWQ0NTAtNGY4Yy1hNjhlLTY0OTU1N2QzYTBhYwAuAAAAAAArsD3iy/SDRrGkcLnEuZ4GAQDAgFdLn8NBQbObwPn0M6aUAADuhyQpAAA=` |
| Auto-meeting       | `AAMkAGQ5NmQwNGZkLWQ0NTAtNGY4Yy1hNjhlLTY0OTU1N2QzYTBhYwAuAAAAAAArsD3iy/SDRrGkcLnEuZ4GAQCIgJPBFelsQrcja/dZLhI0AAC3dkeCAAA=` |
| Goal: Paid Acquisition | `AQMkAGQ5NmQwNGZkLWQ0NTAtNGY4Yy1hNjhlLTY0OTU1ADdkM2EwYWMALgAAAyuwPeLL9INGsaRwucS5ngYBAEas7LcSB6lEv39h0ciIq84AAAITTwAAAA==` |
| AP (Invoices) | `AAMkAGQ5NmQwNGZkLWQ0NTAtNGY4Yy1hNjhlLTY0OTU1N2QzYTBhYwAuAAAAAAArsD3iy/SDRrGkcLnEuZ4GAQDAgFdLn8NBQbObwPn0M6aUAADuhyQcAAA=` |

---

## Hook System (daily execution)

| # | Hook | Trigger | Purpose |
|---|------|---------|---------|
| AM-1 | Ingest (`am-1-ingest`) | userTriggered | Slack scan + Asana sync + email scan → intake files |
| AM-2 | Triage + Draft (`am-2-triage`) | userTriggered | Process intake → update tasks + draft replies |
| AM-3 | Brief + Blocks (`am-3-brief`) | userTriggered | Daily brief + Slack posts + dashboard + calendar blocks |
| EOD-1 | Meeting Sync (`eod-1-meeting-sync`) | userTriggered | Hedy + Outlook → meetings/ series files |
| EOD-2 | System Refresh (`eod-2-system-refresh`) | userTriggered | Maintenance cascade + experiments + git sync |
| 1 | WBR: Weekly Callouts (`wbr-callouts`) | userTriggered | Full 10-market callout pipeline |
| 2 | Sync to SharePoint (`sharepoint-sync`) | userTriggered | Wiki → SharePoint via OneDrive |
| 3 | PS Audit (`ps-audit`) | userTriggered | Paid search audit pipeline |
| 4 | Agent Bridge Sync (`agent-bridge-sync`) | userTriggered | Sync portable-body/ to GitHub |
| — | Guard: Email | preToolUse | Blocks email send unless only recipient is prichwil |
| — | Guard: Calendar | preToolUse | Blocks calendar events with external attendees |

**AM-1→2→3 is the daily driver.** EOD-1→2 runs after meetings. Each hook loads only what it needs — failure is isolated.

### Asana (Enterprise Asana MCP — LIVE)
- **Full read/write access** via Enterprise Asana MCP. SearchTasksInWorkspace, GetTaskDetails, UpdateTask, CreateTask, CreateTaskStory, GetTaskStories, SetParentForTask, GetGoal, etc.
- **Command center protocol**: `~/shared/context/active/asana-command-center.md`
- **Guardrails**: Only modify tasks assigned to Richard (GID 1212732742544167). Audit all writes to `asana-audit-log.jsonl`.
- **AM-2 writes**: Kiro_RW context, task creation from signals, bucket moves, due date changes, completions, comments.
- **EOD-2 writes**: Carry-forward Kiro_RW, daily reset (Today → Urgent), blocker registry updates.

---

## Tool & Automation Opportunities

| Tool | Status | Impact |
|------|--------|--------|
| Campaign link generator | Backlog | AU/MX sitelink URL construction |
| WBR auto-briefing | Proposed | Agent drafts callouts from data |
| Budget forecast helper | Proposed | Pre-fill RO from actuals + trend |
| Invoice/PO automation | Proposed | Route without manual intervention |
| Goal status updater | Proposed | Auto-generate Kingpin from campaign data |
| Testing tracker | Proposed | Structured test log (operational, not narrative) |
| Competitive intel agent | Proposed | Monitor competitor ad copy shifts |
| AI search landscape monitor | Proposed | Track AI Overviews, zero-click changes |

---

## Integrations & Access

See spine.md → Tool Access & Integrations for full list of what the agent can/cannot access.
