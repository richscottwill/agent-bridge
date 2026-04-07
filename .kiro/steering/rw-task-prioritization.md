---
inclusion: fileMatch
fileMatchPattern: ["hooks/am-*", "hooks/eod-*"]
---

# Task Prioritization — Backlog → Active Lists

This file defines how to decide which tasks move from 📦 Backlog into the four active lists (🧹 Sweep, 🎯 Core, ⚙️ Engine Room, 📋 Admin) during the morning routine.

## Guiding Principle

Active lists = what Richard could realistically work on this week. Backlog = genuinely blocked or future items ONLY. If a task is due this week or overdue, it MUST be in an active list — not backlog. Use due dates to drive visibility:
- Due TODAY → appears in "My Day" (highest visibility, do first)
- Due this week → visible in upcoming view
- Overdue → set due date to TODAY immediately

The 4 active lists map to 4 daily calendar blocks:
- 🧹 Sweep → low-friction block (morning, 20-30 min)
- 🎯 Core → deep work block (largest gap, 30-60 min)
- ⚙️ Engine Room → execution block (afternoon, 30-45 min)
- 📋 Admin → wind-down block (end of day, 20-30 min)

## Prioritization Layers (evaluate in order)

### Layer 1: Due Dates (baseline)
- Overdue → surface immediately
- Due today or tomorrow → surface immediately
- Due this week but not yet surfaced → flag in "Due This Week" section of daily brief, pull into active list if action is needed in the next 48 hours

### Layer 2: Calendar Pressure
- Read today's and tomorrow's calendar
- If a meeting involves a stakeholder tied to a backlog task, surface that task
  - Examples: MX sync with Lorena → pull MX Beauty confirmation; Brandon 1:1 → pull anything needing his input; AU sync → pull AU-related backlog items
- If a meeting requires a deliverable or pre-read, the prep task surfaces the day before

### Layer 3: Email & Slack Signals
- Scan inbox (last 24 hours) for messages that reference or relate to backlog tasks
- Someone pinging you about a task = implicit deadline, surface it
- New asks from stakeholders that map to existing backlog tasks → update and surface those tasks rather than creating duplicates
- Check Auto-Comms folder for Asana notifications (task comments, status changes, new assignments)
- Check Auto-meeting folder for meeting summaries (Hedy recaps + Amazon Meetings Summary) — surface action items and decisions from meetings Richard attended

### Layer 4: Weekly Callouts & Performance Data
- Read the latest AU and MX weekly callout docs (~/shared/wiki/callouts/)
- If performance data shows a problem (traffic drop, CPA spike, reg decline), surface related backlog tasks
- If a market is performing well, deprioritize reactive tasks for that market — focus on scaling what's working

### Layer 5: Strategic Priorities (always-on filter)
#[[file:~/shared/context/body/brain.md]]
brain.md contains the live strategic priorities (Three Pillars). At least one task from each pillar should be represented in the active lists at all times. If an active list has zero tasks tied to one of these pillars, scan Backlog for the highest-leverage task in that pillar and pull it forward.

### Layer 6: Blocked vs. Unblocked
- Tasks explicitly blocked (legal approval, Tech dependency, waiting on someone) stay in Backlog unless:
  - An email or Asana notification signals the blocker cleared
  - The task has a downstream dependency that's now urgent
- When a blocker clears, surface the task AND its downstream chain

### Layer 7: Trainer Lens (tiebreaker and override)
When multiple tasks compete for a spot, apply the rw-trainer.md framework:
- **Strategic artifacts > tactical execution** — a test design doc beats a sitelink update
- **Compounding work > one-and-done work** — a playbook beats a single campaign build
- **Visibility work > invisible work** — Kingpin updates, Kate-facing docs, and team frameworks beat internal cleanup
- **Automation opportunities > manual repetition** — if a task keeps recurring, flag it as a tool candidate and deprioritize the manual version
- Ask: "Will this matter in 30 days?" If no, it's a quick win at best — don't let it take a Core or Engine Room slot over something that compounds.

## List Placement Rules

When surfacing a task from Backlog, place it in the right list:

| List | What goes here |
|------|---------------|
| 🧹 Sweep | Quick unblocking actions: send a message, confirm details, ping someone, triage decisions, meeting prep |
| 🎯 Core | Strategic work: test designs, frameworks, stakeholder docs, cross-functional initiatives |
| ⚙️ Engine Room | Hands-on execution: campaign builds, keyword changes, bid adjustments, account changes |
| 📋 Admin | Budget, POs, invoices, compliance, process/admin tasks, goal updates (Kingpin), R&O/forecast input |

## Capacity Guardrails

Active lists hold everything due this week or overdue. No caps — but the calendar blocks enforce focus:
- 🧹 Sweep: quick tasks. Max 2 per calendar block. If more exist, create multiple Sweep blocks.
- 🎯 Core: deep work. The hard thing always lives here. 1-2 tasks per block.
- ⚙️ Engine Room: execution. Batch related work. 2-3 tasks per block.
- 📋 Admin: wind-down. 2-3 tasks per block.

## Backlog Rules (STRICT)

Backlog is ONLY for:
- Tasks genuinely blocked by an external dependency (name the blocker)
- Tasks scheduled for a future date (not this week)
- Reference-only items (not actionable tasks)
- Tasks with no due date AND no urgency signal

If a task is overdue or due this week, it CANNOT be in backlog. Move it to the appropriate active list and set the due date to reflect real urgency. Overdue items get due date = TODAY.

## Task Management Agency

The morning routine agent has FULL authority over To-Do tasks:
- DELETE and RE-CREATE tasks in different lists (this is how to move between lists — the API doesn't support direct moves)
- CHANGE due dates freely to reflect real urgency
- REWRITE titles to be clearer (drop stale prefixes like [BACKLOG], [OVERDUE], [THIS WEEK])
- REWRITE bodies with updated context from the day's email/calendar/Asana scan
- CREATE new tasks when signals reveal untracked work
- COMPLETE tasks confirmed done via email/Asana
- The hard thing from amcc.md should always be due TODAY in Core

Don't ask permission for any of this. Use judgment. If something is stale, duplicated, or misplaced — fix it.

### HARD RULE: Over-Capacity Escalation
If any list exceeds its cap for more than 1 day, the morning routine MUST:
1. Flag it as a 🚨 TRAINER ESCALATION in the tracker — not a note, a callout
2. Make clearing the overflow the #1 priority in the daily brief, above all other work
3. Assign time estimates to each overdue item so Richard can see the total cost
4. Block calendar time for clearing them — suggest a specific window
5. Do NOT allow strategic work to be prioritized over clearing an over-capacity list. You cannot build on a crumbling foundation.

The trainer failed Richard by letting Admin sit at 5/3 for 2 weeks. That stops now.

## Backlog Task Format

Every task in the Backlog must justify WHY it's not being actively worked on. The bar is higher for important (🔴/🟡) tasks.

Title format: `[priority emoji] [task name] — [reason in backlog]`
Examples:
- `🟡 Build MX Beauty campaign — waiting on Lorena confirmation`
- `🔴 Email overlay WW rollout — blocked by Tech scoping`
- `🟢 AppsFlyer setup — scheduled Q3`
- `🟡 AI Max test design — scheduled 3/28, after AEO POV ships`

Valid backlog reasons:
- `blocked by [person/team/dependency]` — something external is preventing progress
- `waiting on [person] confirmation` — you've sent the ball, waiting for it back
- `scheduled [date/week]` — deliberately deferred to a specific time
- `lower priority than [active task]` — explicitly deprioritized in favor of something else
- `no due date, future planning` — genuinely not time-sensitive
- `reference only` — not an actionable task, just context

For 🔴 tasks in Backlog, the reason must be strong:
- "No due date" is NOT a valid reason for a 🔴 task to sit in Backlog
- If a 🔴 task has been in Backlog for 2+ weeks without a blocker, escalate it in the daily brief

Body format for Backlog tasks:
```
WHY BACKLOG: [1-2 sentences explaining why this isn't active right now. For important tasks, explain what would need to change for it to surface.]

CONTEXT: [Brief background]

WHEN TO SURFACE: [What trigger would move this to an active list — date, blocker clearing, email signal, etc.]

ASANA: [ID if applicable]
```

## Task Body Format

Every task in the active lists should have a rich body with this structure:

```
TRAINER: [1-2 sentence trainer commentary - why this matters, how it connects to today's other tasks, leverage assessment]

CONTEXT: [What you need to know - background, who's involved, what happened last]

WHAT TO DO:
1. [Specific action step]
2. [Specific action step]
3. [Specific action step]

DRAFT MESSAGE: [If this task involves sending a message, email, or Slack - include a READY-TO-SEND draft in Richard's voice. He should be able to copy-paste and hit send. This is the highest-value part of the task body.]

LINKS/REFS: [Relevant Quip docs, SIMs, spreadsheets, email threads]

ASANA: [Asana task ID if applicable - close in Asana when done]
```

The TRAINER section at the top is critical - it should:
- Relate this task to the other tasks on today's list (e.g., "Do this BEFORE the Brandon 1:1 so you can report status")
- Call out if this is high-leverage or low-leverage and why
- Suggest a timebox if it's admin/low-leverage work
- Flag dependencies or sequencing with other active tasks

The DRAFT MESSAGE section is equally critical:
- Every task that involves communication MUST have a draft
- Written in Richard's voice (direct, concise, casual with colleagues, professional cross-team)
- Include the specific ask, relevant data points, and a clear next step
- Richard should never have to write a message from scratch for a task the trainer created

## Recurring Task Auto-Generation

The morning routine should automatically create these tasks when it detects the corresponding calendar event or date trigger. If the task already exists in an active list, skip creation.

### Weekly (create Monday morning or day before meeting)
| Task | List | Trigger | Notes |
|------|------|---------|-------|
| Update weekly callouts — AU, MX, Paid App | 🧹 Sweep | Calendar: "Reminder: Update Weekly Callouts" | 30 min timebox. Quip: https://quip-amazon.com/MMgBAzDrlVou |
| Prep Brandon 1:1 agenda | 🧹 Sweep | Calendar: "Richard/Brandon 1:1" | Populate agenda from current week's active tasks, overdue items, and decisions needed |
| Prep AU Paid Search Sync | 🧹 Sweep | Calendar: "AB AU Paid Search Sync" (day before) | Pull AU data, prep talking points, surface AU-related backlog items |
| Update WW tests tracker | 🎯 Core | Every Tuesday | Status update on all active/planned WW tests: email overlay, redirect, promo, AI Max, OCI rollout, etc. Ties to annual goals. |
| Make changes to AU/MX/PAM for the week | ⚙️ Engine Room | Every Monday | Batch all account changes into one Engine Room block |

### Biweekly (create when calendar event detected)
| Task | List | Trigger | Notes |
|------|------|---------|-------|
| Prep MX Paid Search Sync | 🧹 Sweep | Calendar: "MX Paid Search Sync" (day before) | Pull MX data, prep talking points |
| Prep Adi AI brainstorm | 🧹 Sweep | Calendar: "Bi-weekly with Adi" (day before) | Bring AI/automation ideas |

### Monthly (create when date approaches)
| Task | List | Trigger | Notes |
|------|------|---------|-------|
| Update Kingpin Goals | 📋 Admin | 1st of each month (or when Dwayne flags) | Pull data from Andes, update Kingpin |
| R&O budget input | 📋 Admin | When finance emails about RO cycle | Timebox 30 min |

### Auto-population rules for meeting prep tasks:
- The body should include: meeting time, key attendees, and a dynamically generated agenda based on:
  - Active tasks that involve the meeting's attendees
  - Overdue items that need escalation
  - Decisions pending from the attendee
  - Recent email/Slack signals involving the attendee
- Example: Brandon 1:1 prep should auto-include any tasks where Brandon is a decision-maker, plus overdue items to report on

## Task Calendar Block Rules

When building calendar blocks during the morning routine or ad-hoc:

1. **Only show future events.** Get the current system time (`date`) BEFORE pulling the calendar. Filter out any meetings or blocks that have already ended.
2. **Start the block from NOW.** The first entry should be the next upcoming event or task window, not the start of the day.
3. **Interleave tasks into open gaps.** Place task blocks in the gaps between remaining meetings, ordered by priority.
4. **Show estimated end-of-day.** After the last task block, note the projected finish time.

### Calendar Block Body Standard (MANDATORY)
Every calendar block body MUST follow the same structure as To-Do task bodies. The body is HTML format and must include:

```html
<h3>TRAINER</h3>
<p>[1-2 sentences: why this matters, how it connects to today's other tasks, leverage assessment, timebox guidance]</p>

<h3>CONTEXT</h3>
<p>[Background: who's involved, what happened last, relevant data, stakeholder context]</p>

<h3>WHAT TO DO</h3>
<ol>
<li>[Specific action step]</li>
<li>[Specific action step]</li>
</ol>

<h3>DRAFT MESSAGE</h3> (if the task involves sending a message)
<p>[Ready-to-send draft in Richard's voice. Copy-paste and hit send.]</p>

<h3>LINKS</h3>
<ul>
<li>[Relevant Quip docs, SIMs, spreadsheets, email threads]</li>
</ul>
```

For blocks containing multiple tasks, separate each task with `<hr>` and give each its own CONTEXT, WHAT TO DO, and DRAFT MESSAGE sections.

The goal: when Richard opens the calendar event, he has everything he needs to execute without searching for context.

## End-of-Day Return

Tasks that were surfaced but not touched for 2 consecutive days should be evaluated:
- Still relevant for this week? Keep but flag.
- Blocked or deprioritized? Return to Backlog with a note.
- The goal is to prevent the active lists from becoming stale again.

## Trainer Commentary

During the morning routine, after surfacing tasks, include a brief Trainer Check-In:
- "You have [X] strategic tasks and [Y] tactical tasks today. Ratio check: are you spending enough time on work that compounds?"
- Flag if Richard is drifting toward low-leverage comfort zone work
- Call out if a high-leverage Backlog task has been sitting untouched for 2+ weeks
- Celebrate if the active list is well-balanced across the three pillars
