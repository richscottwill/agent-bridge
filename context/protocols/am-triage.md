<!-- DOC-0331 | duck_id: protocol-am-triage -->
# AM-Triage Protocol — Curate + Draft

Interactive phase. All proposals presented to Richard for approval before writing.

All Asana writes follow the Guardrail Protocol in asana-command-center.md § Guardrail Protocol.

---

## Context Load
spine.md, current.md, memory.md, richard-writing-style.md, hands.md, amcc.md, rw-tracker.md, asana-command-center.md, ALL intake/ files.

---

## Phase 1 — Process Intake

### Signal Routing
- Slack [ACTION-RW] signals → create Asana tasks if actionable (assign to Richard, set Routine + Priority_RW).
- Email signals → same routing.
- Asana digest → update hands.md Priority Actions.

### Admin Keyword Detection (override — runs BEFORE generic mapping)
Before applying the Signal-to-Routine mapping table below, check the signal text (task name, description, or source message) against the Admin keyword list. Matching is case-insensitive.

**Admin Keywords:** `budget`, `PO`, `purchase order`, `invoice`, `spend`, `R&O`, `reconciliation`, `actuals`, `forecast`, `compliance`

**Rule:** If the signal text matches ANY keyword (case-insensitive substring match), route directly to Routine_RW = Admin with Priority_RW = Today. This overrides the generic Signal-to-Routine mapping below — do not fall through to the table for matched signals.

Signals that do NOT match any Admin keyword continue to the Signal-to-Routine mapping table as normal.

### Admin Early-Start Due Date Enforcement
When AM-2 triage routes a task to Routine_RW = Admin (whether by keyword detection above or by the Signal-to-Routine mapping table below), apply the following due date enforcement:

- **IF task has no due date** (due_on IS NULL): flag to Richard: "Admin task [name] has no due date — set one?" Do not auto-assign a due date — Richard decides.
- **IF task has a due date AND no start date** (due_on IS SET, start_on IS NULL): auto-set start_on = due_on − 7 business days. This ensures the task surfaces in the Admin block a full week before it's due, shifting Admin from "do by deadline" to "start early."
- **IF task already has a start date** (start_on IS SET): do not modify. Existing start dates are preserved.

**Why 7 business days:** Budget confirmations, R&O submissions, and PO tasks require lead time — they involve cross-team coordination (Lorena, Andrew, Brandon) and cannot be completed in a single session. A 7-business-day window gives Richard a full work week to process them in the bounded Admin block (30 min/day) before the deadline.

**Calculation note:** 7 business days = 7 weekdays (Mon–Fri), skipping weekends. For example, a task due on a Friday would have start_on set to the previous Friday (not the previous Wednesday).

### Signal-to-Routine Mapping
| Signal Type | Routine | Priority_RW |
|-------------|---------|-------------|
| Quick reply/send/confirm | Sweep | Today |
| Strategic discussion/artifact/framework | Core | Urgent |
| Campaign/keyword/bid/spreadsheet | Engine Room | Today |
| Admin/budget/invoice/compliance | Admin | Today |
| Unclear/ambiguous | (none — Backlog) | Flag for triage |

### Slack Decision Detection
Detect keywords: 'decided', 'agreed', 'confirmed', 'approved', 'going with', 'final call', 'locked in'. For each: extract decision text, thread link, participants, date. Queue for Project Notes 'Recent Decisions' update. Present to Richard for approval before writing.

### Bucket Cap Check
Sweep: 5, Core: 4, Engine Room: 6, Admin: 3.

**Sweep, Core, Admin:** Over cap → flag lowest-priority for demotion (present to Richard).

**Engine Room: Auto-Demotion + Task Decomposition**

Engine Room cap is 6. When Engine Room exceeds cap, auto-demote (no approval needed) — the current system proposes but never executes because Richard defers the decision. Auto-execution removes that friction.

**Step 1 — Identify excess tasks:**
Query all incomplete Engine Room tasks, sorted by priority (lowest first), then by due date (no due date = lowest), then by creation date (oldest = lowest):

```
SELECT task_gid, name, due_on, priority_rw, created_at
FROM asana_tasks
WHERE routine_rw LIKE '%Engine Room%'
  AND completed = FALSE
ORDER BY
  CASE priority_rw
    WHEN 'Not urgent' THEN 1
    WHEN NULL THEN 2
    WHEN 'Today' THEN 3
    WHEN 'Urgent' THEN 4
    ELSE 0
  END ASC,
  CASE WHEN due_on IS NULL THEN 1 ELSE 0 END ASC,
  due_on ASC,
  created_at ASC
```

Tasks beyond position 6 in this sorted list are excess.

**Step 2 — Auto-demote excess tasks:**
For each excess task (auto-execute, no approval needed):
1. UpdateTask: clear Routine_RW — set to null (Backlog). `custom_fields: {'1213608836755502': null}`
2. UpdateTask: update Kiro_RW (GID: `1213915851848087`) — append: `"M/D: Demoted from Engine Room (cap enforcement). [reason: e.g., lowest priority, no due date]."`
   - M/D = current date in month/day format, no leading zeros.
3. Log write to asana-audit-log.jsonl per Guardrail Protocol.
4. Notify Richard of all demotions in the daily brief summary (batch, not per-task).

**Step 3 — BAU/Mandatory Task Decomposition:**
After demotion, check each demoted task for BAU/mandatory indicators:
- **Recurring:** task has a recurrence pattern, or matches a known recurring task in asana-command-center.md § Recurring Task Patterns
- **External stakeholders:** task name or description references teammates (Lorena, Andrew, Brandon, etc.) or cross-team dependencies
- **Business-critical tag:** Priority_RW was Urgent before demotion, or task is tagged with a business-critical label

**IF a demoted task is BAU/mandatory:**
1. Decompose the parent task into 2–3 smaller subtasks that represent the minimum viable work to keep the mandatory obligation moving.
2. For each subtask, identify the most related block based on the subtask's nature:
   - Quick send/confirm/reply actions → piggyback onto Sweep
   - Data pulls, spreadsheet updates → keep in Engine Room (if space) or Backlog
   - Budget/PO/invoice components → route to Admin
3. Create subtasks via CreateTask(parent=demoted_task_gid, assignee='1212732742544167') with appropriate Routine_RW for the target block.
4. Update each subtask's Kiro_RW: `"M/D: Decomposed from [parent task name] (Engine Room cap). Piggybacked onto [block]."`
5. Update the demoted parent's Kiro_RW: append `"Decomposed into [N] subtasks across [blocks]."`
6. Present decomposition to Richard in the daily brief: "Engine Room cap enforced. [parent task] demoted to Backlog but decomposed into [N] subtasks piggybacked onto [blocks] — mandatory work still gets through."

**IF a demoted task is NOT BAU/mandatory:**
- No decomposition. Task stays in Backlog until Richard manually retriages it.

**Preservation:** Engine Room cap value (6) is unchanged. Only the enforcement mechanism changes — from "propose and wait" to "auto-execute and notify." Tasks that remain within cap are untouched.

### Admin Escalation Check (SINGLE CHECKPOINT — AM-2 ONLY)
After bucket cap enforcement, check for overdue Admin tasks that need escalation to Sweep.

**Query:** All incomplete tasks where Routine_RW = 'Admin' AND days_overdue >= 3.

```
SELECT task_gid, name, due_on, DATEDIFF('day', due_on, CURRENT_DATE) AS days_overdue
FROM asana_tasks
WHERE routine_rw LIKE '%Admin%'
  AND completed = FALSE
  AND due_on IS NOT NULL
  AND DATEDIFF('day', due_on, CURRENT_DATE) >= 3
```

**For each matching task, auto-execute (no approval needed):**
1. UpdateTask: change Routine_RW from Admin to Sweep (custom_fields: `{'1213608836755502': '1213608836755503'}`).
2. UpdateTask: update Kiro_RW (GID: `1213915851848087`) — append: `"M/D: Escalated to Sweep (3d+ overdue)."`
   - M/D = current date in month/day format, no leading zeros (e.g., `4/14`, `12/1`).
3. Log write to asana-audit-log.jsonl per Guardrail Protocol.

**Threshold:** Exactly 3 days overdue. Tasks 1–2 days overdue stay in Admin. Tasks 3+ days overdue escalate.

**Scope:** This is the ONLY escalation checkpoint in the system. Per McKeown's Effortless principle, one simple check in AM-2 is better than triplicated logic across AM-auto and EOD. If Admin is in position 2 and routing is fixed, escalation should rarely fire — it's a safety net, not a primary mechanism.

**Preservation:** Admin tasks within their due date window (not overdue, or overdue < 3 days) remain in Admin with cap of 3. No premature escalation.

### Flags
- Priority_RW=Today but no Routine → flag for Richard.
- Overdue 7+ days with no activity → flag: do, delegate, or kill.

---

## Phase 1 Enhancement — My Tasks Deep Enrichment

After intake processing, scan ALL incomplete My Tasks for field completeness.

Call SearchTasksInWorkspace(assignee_any='1212732742544167', completed='false'). For each task, GetTaskDetails with opt_fields: name,assignee.gid,due_on,start_on,completed,custom_fields.name,custom_fields.display_value,custom_fields.gid,memberships.section.name.

### Four Enrichment Rules

**1. Kiro_RW Check** (GID: `1213915851848087`)
- IF empty/null OR not M/D brevity format → propose entry.
- Format: `M/D: <text under 10 words>`. No leading zeros. Today's date.
- Example: `4/15: Active. Due Friday. No blockers.`

**2. Next Action Check** (GID: `1213921400039514`)
- IF empty/null → propose entry.
- Format: imperative verb, single sentence, <15 words.
- Example: `Send AU invoice to finance by EOD Friday`

**3. Date Check** (Begin Date GID: `1213440376528542`)
- IF due_on set but start_on null → propose start_on = max(today, due_on - 7 days).
- ASANA CONSTRAINT: start_on requires due_on.

**4. Priority_RW Default** (GID: `1212905889837829`)
- IF Routine (GID: `1213608836755502`) is set but Priority_RW is null → propose "Not urgent" (GID: `1212905889837833`).

### Enrichment Batch Presentation

```
📝 MY TASKS ENRICHMENT — [N] task(s) need field updates:

- [task name] (GID: [gid])
  - Kiro_RW: [proposed] (currently: [empty or value])
  - Next action: [proposed] (currently: empty)
  - Begin Date: [YYYY-MM-DD] (currently: unset)
  - Priority_RW: Not urgent (currently: empty)
- ACTION: Approve all, approve individually, or skip?
```

Only show fields that need enrichment per task.

### Execute Approved Enrichments
Combine all field writes into one UpdateTask per task. Log each to asana-audit-log.jsonl with project='My_Tasks'. On API failure → log → retry once after 2s → skip and flag if retry fails.

---

## Phase 1B — Wiki Article Pipeline Review

Wiki articles live in `~/shared/wiki/agent-created/` and the Kiro dashboard Pipeline view (`shared/dashboards/wiki-search.html`). **Do not create, update, or comment on Asana tasks for article work.**

### Step 1 — Read Wiki Pipeline State
Load `~/shared/context/active/am-wiki-state.json` (written by AM-Backend Phase 4). It contains:
- Stale FINAL articles (updated >30 days ago)
- SharePoint drift (local FINAL is newer than `Documents/Artifacts/*.docx`)
- New-article candidates from signals
- Articles with broken cross-references or missing frontmatter

### Step 2 — Present Findings
```
📚 WIKI PIPELINE — [N] items:
- Stale FINAL articles: [count] (open in dashboard to review)
- SharePoint drift: [count] articles need re-publish
- New-article candidates: [top 3 by signal strength]
- Health flags: [count] broken refs, [count] missing frontmatter
- ACTION: Open dashboard Pipeline view to triage?
```

### Step 3 — Execute Richard's Directions
- **Open dashboard:** Remind Richard the Pipeline view lives at `shared/dashboards/wiki-search.html` and supports drag-free status bumps (DRAFT → REVIEW → FINAL) via the arrow buttons on each card.
- **Promote to FINAL:** Update the article's frontmatter `status: FINAL` and trigger SharePoint publish via librarian.
- **Start a new article:** Create the .md file in `~/shared/wiki/agent-created/[category]/[slug].md` with the standard frontmatter template. Do NOT create an Asana task.
- **Archive:** Move to `~/shared/wiki/agent-created/archive/` and update frontmatter `status: ARCHIVED`.

---

## Phase 1C — Portfolio Project Scan

Scan all child projects under ABIX PS and ABPS portfolios for Richard's tasks.

### Step 1 — Portfolio Discovery
- GetPortfolioItems(portfolio_gid='1212775592612914') → ABIX PS children (AU, MX).
- GetPortfolioItems(portfolio_gid='1212762061512816') → ABPS children.
- For new projects not in asana-command-center.md: discover sections + custom fields, flag for Richard, update command center.

### Step 2 — Per-Project Task Scan
For each child project (AU, MX, WW Testing, WW Acq, Paid App):
- GetTasksFromProject → all incomplete tasks.
- GetTaskDetails with opt_fields: name,assignee.gid,due_on,start_on,completed,custom_fields.name,custom_fields.display_value,custom_fields.gid,memberships.section.name.
- FILTER: Only tasks where assignee.gid === '1212732742544167'. Skip Cross_Team_Tasks for writes.

### Step 3 — Field Enrichment Check
Same 4 rules as My Tasks enrichment (Kiro_RW, Next action, dates, Priority_RW). Queue proposals for batch presentation grouped by project.

### Step 4 — Date Window Checks
- start_on <= today AND NOT completed AND NOT terminal section → in execution window.
- due_on within 0-2 days AND NOT completed → NEAR-DUE ESCALATION. Auto-set Priority_RW=Today. Update Kiro_RW + Next action.
- due_on < today AND NOT completed → OVERDUE. Flag. Update Kiro_RW: 'M/D: Overdue [N]d. Extend or close.'
- Terminal sections per project: see asana-command-center.md § Portfolio Projects.

### Step 5 — Status Update Staleness
- GetStatusUpdatesFromObject for each project.
- >14 days since last update → flag as stale.
- Exactly 14 days → NOT stale.
- Never updated → flag as "never updated".
- Extract health color (green/yellow/red).

### Step 6 — Recurring Task Auto-Creation (AU + MX) (AUTO-EXECUTE)
Detect completed tasks matching known recurring patterns (see asana-command-center.md § Recurring Task Patterns):
- Weekly: due_on = prev + 7d, start_on = due_on - 2d
- Bi-monthly: due_on = prev + 14d, start_on = due_on - 3d
- Monthly: due_on = same day next month, start_on = due_on - 5d
- Copy Routine, section, project-specific fields.
- Present to Richard: 'Auto-created next [name] due [date]. Approve?'
- Delete if rejected.

### Step 7 — Cross-Team Blocker Detection (MX)
- Read all MX tasks including Cross_Team_Tasks (NEVER write to them).
- Flag overdue teammate tasks (due_on < today AND not completed).
- Correlate with Richard's tasks via subtask relationships, name cross-references, same-section proximity.
- Update Richard's blocked task Kiro_RW: 'M/D: Blocked on [teammate] task. [N]d overdue.'
- Update Next action: 'Follow up with [teammate] on [blocker task name]'

### Step 8 — Event Countdown (Paid App)
Read event calendar from asana-command-center.md § Paid App Event Calendar.
- Event within prep window: Backlog tasks → propose move to Prioritized.
- Event within escalation trigger: Prioritized → propose In progress + Priority_RW=Today. Blocked → critical flag.
- Stale task triage: >30d overdue → classify (event-related → archive, budget → extend, other → kill-or-revive). Present batch.
- New event task detected → propose subtask template (Campaign brief, Budget confirmation, Creative assets, Campaign build, Post-event analysis).

### Step 9 — Budget/PO Tracking (MX + Paid App)
- Classify Budget_Tasks by keywords: budget, PO, spend, invoice, reconciliation, actuals, forecast.
- Budget near-due threshold: 3 days (not standard 2).
- Overdue budget tasks → flag as critical.
- Paid App monthly actuals → check for Brandon update task, propose if missing.

### Step 10 — Market Context Auto-Refresh (AU + MX)
- Compile project summary: active count, overdue, near-due, blockers, upcoming deadlines (7d), recent completions (7d), recurring status, budget status.
- Compare against current Context_Task content. If Material_Change → read-before-write → UpdateTask(html_notes).
- AU/MX: daily refresh. Other projects: weekly.
- Skip if no material change.
- Allowed HTML tags only.
- Context Task GIDs: AU=`1213917747438931`, MX=`1213917639688517`.

### Step 11 — Present Portfolio Findings
```
📊 PORTFOLIO SCAN — [N] projects scanned:

[Portfolio Name] ([N] projects):
  - [Project]: [task_count] tasks ([overdue] overdue, [near_due] near-due)
    Status: [🟢/🟡/🔴] (last update: [date] — [stale/current])
    Enrichment needed: [N] tasks missing fields

📝 PORTFOLIO ENRICHMENT — [N] task(s) need field updates:
  [grouped by project, same format as My Tasks enrichment]

⚠️ PORTFOLIO ALERTS:
  - Near-due: [tasks with project context]
  - Overdue: [tasks with project context]
  - Stale projects: [list with days since last update]
  - Cross-team blockers: [MX blockers]
  - Budget: [budget task alerts]
```

---

## Phase 2 — Interactive Command Center

Present the curated task board. Execute Richard's directions in real-time.

### Supported Operations
- Move tasks between Routine buckets
- Change due dates
- Change Priority_RW (Today/Urgent/Not urgent)
- Create new tasks with Routine + Priority pre-set
- Write/update task descriptions (notes or html_notes)
- Add comments (CreateTaskStory)
- Complete tasks
- Create subtasks
- Set Importance_RW

### Agent-Initiated Proposals
Propose changes based on: overdue tasks, bucket overflows, untriaged items, stale tasks, due date conflicts. Richard approves, modifies, or gives new directions.

---

## Log Hook Execution

After Phase 2 completes (or Richard ends the session):
```sql
INSERT INTO hook_executions (hook_name, execution_date, start_time, end_time, duration_seconds,
    phases_completed, asana_reads, asana_writes, slack_messages_sent, duckdb_queries, summary)
VALUES ('am-triage', CURRENT_DATE, '[start]', '[end]', [duration],
    [phases], [reads], [writes], [slack_msgs], [queries], '[summary]');
```
