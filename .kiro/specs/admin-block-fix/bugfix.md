# Bugfix Requirements Document

## Introduction

Admin tasks — specifically R&O submissions, budget confirmations, and PO management — are systematically failing because the Admin block is positioned last (4th) in Richard's daily work sequence: Sweep → Engine Room → Core → Admin. By the time Admin is reached, cognitive energy is depleted and available time is consumed by earlier blocks. This is a structural sequencing defect, not a discipline problem. The result: teammates (Lorena, Andrew) are blocked, POs are 37+ days overdue, and R&O submissions are 22+ days overdue.

The fix targets the block ordering in hands.md, the Routine_RW routing logic in the AM triage protocols, and the morning routine hooks — ensuring Admin tasks get structural protection against being crowded out, without adding new tools or complexity.

## Quantitative Evidence (DuckDB: asana.asana_tasks, 2026-04-14)

### Admin Block Completion Rate
- Admin tasks completed since March 1: **0** (zero completions across all Admin-tagged tasks)
- Admin tasks currently open: **4** (plus 1 tagged "Admin (Wind-down)")
- Admin tasks currently overdue: **1** formally, but see misrouting below

### Admin-Type Tasks Misrouted or Untagged
Of 23 budget/PO/R&O/invoice/spend tasks found in Asana, only **4 are tagged Routine_RW = Admin**. The remaining **17 are untagged (null) or misrouted** to other blocks:
- "Provide Lorena Q2 expected spend for MX PO" → Sweep (Low-friction), 10 days overdue
- "R&O for MX/AU" → null (no Routine_RW), no due date
- "PAM R&O" → null, no due date
- "Share ENG max budget calculation file with Andrew" → null, no due date
- "MX/AU confirm budgets" → null (2 instances), one 14 days until due
- "Raise PO for Q2 instead of increasing to FY" → null, no due date
- "Raise PO for US PAM for $70K underreported amount" → null, no due date
- "Reply to Brandon - PAM budget needs assessment" → null, no due date
- "Reply to Brandon — MX budget line / underspend risk" → null, no due date
- "Send AU team invoice for prev month" → Sweep, no due date
- "ie%CCP calc - insert MX spend/regs before 9th" → null (3 instances)

### Overdue Severity by Block (all open tasks)
| Block | Open | Overdue | Avg Days Overdue | Max Days Overdue |
|-------|------|---------|-----------------|-----------------|
| Engine Room | 22 | 6 | 21.8 | 53 |
| Sweep | 7 | 3 | 7.7 | 11 |
| Sweep (Low-friction) | 3 | 3 | 8.0 | 10 |
| null (untagged) | 66 | 3 | 13.7 | 22 |
| Core | 10 | 2 | 10.0 | 13 |
| Admin (Wind-down) | 1 | 1 | 12.0 | 12 |
| Admin | 4 | 1 | 1.0 | 1 |

### Non-Standard Routine_RW Values (fragmentation)
The system has 3 non-standard Routine_RW values that fragment routing:
- "Sweep (Low-friction)" — 3 tasks (should be Sweep)
- "Admin (Wind-down)" — 1 task (should be Admin)
- "Engine Room (Excel and Google ads)" — 1 task (should be Engine Room)

### Key Overdue Admin-Type Tasks (team-blocking)
| Task | Routine_RW | Days Overdue | Blocked Person |
|------|-----------|-------------|----------------|
| MBR callout | Admin (Wind-down) | 12 | Team (AU reporting) |
| Provide Lorena Q2 expected spend | Sweep (Low-friction) | 10 | Lorena (MX PO submission) |
| ie%CCP calc - insert MX spend/regs | null | 5 | Team (MX forecasting) |
| Paid App PO - Create Q2 + Amend Google PO | Admin | 1 | Team (Paid App billing) |
| R&O for MX/AU | null | no due date set | Team (budget planning) |
| PAM R&O | null | no due date set | Team (PAM budget planning) |

### Root Cause Summary
The bug has two compounding failures:
1. **Sequencing failure:** Admin block is 4th/last → never reached → 0 completions since March 1
2. **Routing failure:** 17 of 23 admin-type tasks (74%) are either untagged or misrouted to non-Admin blocks, meaning even if Admin executed properly, most budget/PO/R&O work wouldn't be in it

## Bug Analysis

### Current Behavior (Defect)

1.1 WHEN the daily block sequence is Sweep → Engine Room → Core → Admin THEN Admin tasks are consistently reached last, after cognitive energy and available time are depleted by earlier blocks

1.2 WHEN Admin tasks (R&O submissions, budget confirmations, PO management) are assigned Routine_RW = Admin THEN they are deferred day after day because the Admin block executes in the end-of-day slot where System 2 (Kahneman) is depleted — the brain defaults to System 1 avoidance, and shallow-work tasks that require even minimal deliberate attention get skipped entirely

1.3 WHEN Admin tasks accumulate as overdue (PAM US PO: 37+ days, PAM R&O: 22+ days, Lorena Q2 MX spend: 8+ days, Andrew ENG budget file: overdue, MX/AU budget confirmations: 7+ days) THEN teammates who depend on Richard's inputs are blocked and cannot proceed with their own work

1.4 WHEN the AM-2 triage protocol routes budget/invoice/compliance signals to Admin with Priority_RW = Today THEN those tasks still do not get completed because the Admin block's position in the sequence (4th) means "Today" priority within Admin is meaningless if Admin itself is never reached

1.5 WHEN the AM-3 daily brief surfaces Admin tasks in the 📋 Admin section THEN there is no escalation mechanism to promote critically overdue Admin tasks into earlier blocks (Sweep or Core) where they would actually get executed

### Expected Behavior (Correct)

2.1 WHEN the daily block sequence is reordered THEN Admin SHALL execute in the 2nd position (after Sweep, before Core), following Cal Newport's principle that shallow work (admin, email, logistics) should be batched into a dedicated block and scheduled deliberately rather than left to fill remaining gaps — and Duhigg's habit loop principle that the cue (post-Sweep transition) and reward (clear admin queue) must be structurally protected to make the routine automatic. The Admin block SHALL be time-bounded to 30 minutes maximum to protect Core's flow window (Csikszentmihalyi). Upon Admin block completion, the system SHALL surface a concrete reward signal: "✅ Admin clear. [N] tasks done. Core block starts now." (Duhigg habit loop reward)

2.2 WHEN Admin tasks (R&O submissions, budget confirmations, PO management) are assigned Routine_RW = Admin THEN they SHALL be reached before cognitive energy is depleted, because Admin executes earlier in the daily sequence

2.3 WHEN an Admin task becomes overdue by 3+ days THEN the system SHALL auto-escalate it by promoting it to the Sweep block (quick unblocking) for the next day, ensuring it surfaces in the highest-priority execution slot rather than waiting for the Admin block

2.4 WHEN the AM-2 triage protocol routes a budget/PO/R&O signal THEN the triage logic SHALL set start_on = due_on - 7 business days so the task surfaces in the Admin block a full week before it's due — shifting Admin from "do by deadline" to "start early." For tasks with no due date, the system SHALL flag to Richard: "Admin task [name] has no due date — set one?" The 3-day overdue escalation to Sweep SHALL exist in AM-2 only (not triplicated across AM-auto and EOD) per McKeown's Effortless principle

2.5 WHEN the AM-3 daily brief is generated THEN it SHALL flag any Admin tasks overdue by 3+ days with a distinct escalation marker (⚠️ ADMIN ESCALATION) and include them in the Sweep section of the brief, not just the Admin section

2.6 WHEN R&O submissions are due THEN they SHALL be completed by their due dates, with the structural block ordering ensuring Admin tasks are not perpetually deferred

2.7 WHEN budget confirmations are requested THEN they SHALL be sent within 2 business days of the request, enforced by the auto-escalation to Sweep if the 2-day window is breached

2.8 WHEN PO-related tasks are active THEN they SHALL never exceed 7 days overdue, enforced by the 3-day overdue escalation rule promoting them out of Admin into Sweep

### Unchanged Behavior (Regression Prevention)

3.1 WHEN tasks are categorized as Sweep (quick unblocking: send, confirm, triage) THEN the system SHALL CONTINUE TO route them to the Sweep block with a cap of 5 tasks

3.2 WHEN tasks are categorized as Core (strategic: test designs, frameworks, stakeholder docs) THEN the system SHALL CONTINUE TO route them to the Core block with a cap of 4 tasks

3.3 WHEN tasks are categorized as Engine Room (hands-on: campaign builds, keyword changes, bids) THEN the system SHALL CONTINUE TO route them to the Engine Room block with a cap of 6 tasks

3.4 WHEN Admin tasks are not overdue (within their due date window) THEN the system SHALL CONTINUE TO keep them in the Admin block with a cap of 3 tasks, without premature escalation to other blocks

3.5 WHEN the AM-1/AM-2/AM-3 morning routine hooks execute THEN they SHALL CONTINUE TO perform all existing functions (Slack scan, Asana sync, email scan, enrichment, portfolio scan, brief generation) without disruption from the block reordering

3.6 WHEN the four block categories (Sweep, Core, Engine Room, Admin) are used for task classification THEN the system SHALL CONTINUE TO use these same categories — no new block types shall be introduced

3.7 WHEN the Routine_RW field in Asana maps tasks to blocks THEN the system SHALL CONTINUE TO use the existing Routine_RW enum values (Sweep, Core Two, Engine Room, Admin, Wiki) without adding new enum options

3.8 WHEN tasks are in the Backlog (no Routine_RW set) THEN the system SHALL CONTINUE TO treat them as deferred/blocked/future items requiring triage before entering a block
