<!-- DOC-0151 | duck_id: experiment-hands-modified-exp13 -->
# Hands — Execution & Tooling

*What gets done and how. Active tasks, dependencies, integrations, hooks, and the systems that turn decisions into action. The canonical action tracker.*

*Operating principle: Reduce decisions, not options. Every task should have a clear next action, a pre-written draft if it involves communication, and a due date that drives My Day. Richard opens his list and acts — he doesn't plan.*

Last updated: 2026-04-02 (loop run 16)
Sources: rw-tracker.md, To-Do lists, email scan, calendar scan, Slack ingestion, DM scan

---

## Priority Actions

<!-- Full task list: db("SELECT id, priority, description, due_date, status, blockers, category FROM task_queue WHERE status != 'DONE' ORDER BY priority, due_date") -->
<!-- Overdue: db("SELECT id, description, due_date, DATEDIFF('day', due_date, CURRENT_DATE) as days_overdue FROM task_queue WHERE due_date < CURRENT_DATE AND status NOT IN ('DONE','BLOCKED') ORDER BY due_date") -->

### Top 5 This Week (snapshot — refreshed each morning routine)
| # | Action | Due | Status |
|---|--------|-----|--------|
| P0 | **Testing Approach doc outline** — Kate Apr 16. THE HARD THING. | Apr 16 | NOT STARTED (12 workdays) |
| P1 | **Respond to Lena** — AU LP URL analysis + CPA overstating. Brandon offering support. | ASAP (2d) | NOT STARTED |
| P1 | **Reply to Stacey DM** — CA exclusion from Polaris 4/7 testing | ASAP (1d) | NOT STARTED |
| P1 | **Share ENG budget file with Andrew** — OP1 recalculation | ASAP (1d) | NOT STARTED |
| P1 | **Respond to Lorena** — Q2 expected spend for MX PO | ASAP (8d overdue) | NOT STARTED |

14 items overdue (oldest: PAM US PO, 31 days). 2 blocked (MX Auto page on Vijeth, Kingpin on Andes). 28 total tasks in queue.

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

## New Signals (since 4/1)
- 🆕 Brandon @mentioned Richard in ABIX (4/1 9:19pm): offering help on Lena's AU follow-up questions. Richard confirmed WW streams alignment. Brandon hasn't looked at Lena's req yet — LMK if help needed.
- 🆕 Stacey DM (4/1 11:38pm): Asking about CA exclusion from Polaris 50/50 testing on 4/7. Needs reply with rationale.
- 🆕 Andrew DM (4/1 9:18pm): Requesting ENG max budget calculation file (audience size × frequency). Brandon mentioned in Andrew's 1:1 for OP1 recalculation.
- 🆕 Lorena DM (4/1): Richard told her he'd update after current task. She replied "Thank you!" Positive signal but Q2 spend still not sent (8d overdue).
- 🆕 Vijeth completed ps-brand XF + Template (Asana 4/1). Alex confirmed all navs working. Polaris brand pages live for all GEOs.
- 🆕 JP Brand LP experiment: Stacey confirmed ref_= carry-over works. Targeting live 4/2. Brandon confirmed.
- 🆕 Kudoboard for Kate Vives: was due 4/1, now OVERDUE.
- 📅 TODAY 4/2: PSME Demo 8am, Deep Dive & Debate 9am (Brandon) + ACQ Promo OHs 9am (conflict), Richard/Brandon 1:1 12pm. Focus blocks: Sweep 8am, Core 9am, Engine Room 1pm, Admin 4pm.
- 📅 TOMORROW 4/3: AppTweak <> Amazon Business 11am. Finance actuals due EOD.

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
| 1 | Morning Routine (`rw-morning-routine`) | userTriggered | One-click: Asana sync → draft replies → To-Do refresh → daily brief → calendar blocks |
| 2 | Run the Loop (`run-the-loop`) | userTriggered | Maintenance → cascade to organs → optionally 1 experiment |
| 3 | Block Email Send | preToolUse | Blocks email_reply/send/forward unless only recipient is prichwil |
| 4 | Block Calendar Invite | preToolUse | Blocks calendar events with external attendees |
| 5 | Hedy Meeting Sync (`hedy-meeting-sync`) | userTriggered | Pulls latest Hedy sessions, analyzes Richard's communication patterns, updates context files |

**Morning Routine is the daily driver.** Run the Loop is for context refresh + experiments (can run independently or before the morning routine for deeper context).

### Asana Bridge (workaround)
- **Create tasks**: Email x@mail.asana.com (include Richard's email)
- **Read task updates**: Check Auto-Comms folder for Asana notification emails
- **Read meeting context**: Check Auto-meeting folder for Hedy recaps and Amazon Meetings Summary
- **Task ID extraction**: "View task" URLs in notifications contain `/task/{id}`. Stored in To-Do task bodies as `ASANA: {id}`.
- **Full protocol**: `~/shared/context/active/asana-sync-protocol.md`

---

## Tool & Automation Opportunities

| Tool | Status | Impact | Notes |
|------|--------|--------|-------|
| Campaign link generator | Backlog | Save time on promo URL updates | Would have saved time on AU sitelink update for Alexis |
| WBR auto-briefing | Proposed | Replace manual WBR coverage | Agent pulls traffic/conversion data, drafts callouts |
| Budget forecast helper | Proposed | Pre-fill RO spreadsheet from actuals + trend | Reduce manual budget spreadsheet time |
| Invoice/PO automation | Proposed | Route invoices without manual intervention | Carlos can own MX, AU should be process not person |
| Goal status updater | Proposed | Auto-generate Kingpin updates from campaign data | Never fall behind on goals again |
| Testing tracker | Proposed | Structured log of all tests + results | OP1 doc is narrative; this is operational |
| Competitive intel agent | Proposed | Monitor competitor ad copy and strategy shifts | Automated version of competitor-intel tracking |
| AI search landscape monitor | Proposed | Track Google AI Overviews, Bing Chat changes | Relevant to AEO/zero-click future |

---

## Integrations & Access

See spine.md → Tool Access & Integrations for full list of what the agent can/cannot access.
