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
Sweep: 5, Core: 4, Engine Room: 6, Admin: 3. Over cap → flag lowest-priority for demotion.

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

## Phase 1B — ABPS AI Project Scan

Scan ABPS AI - Content project (GID: `1213917352480610`). The autonomous document factory.

### Guardrail Protocol
All writes MUST follow asana-command-center.md § Guardrail Protocol:
- PRE-WRITE: Verify assignee.gid === '1212732742544167'
- AUDIT LOG: Append to asana-audit-log.jsonl (extended format with project, pipeline_agent, pipeline_stage)
- READ-BEFORE-WRITE: Before html_notes updates, check for Richard's additions
- API FAILURE: Log → retry once → flag if retry fails

### Step 1 — Scan Intake for Untriaged Tasks
- GetTasksFromProject(project_gid='1213917352480610') → all incomplete tasks.
- GetTaskDetails for each → read custom fields, dates, section.
- FILTER: tasks in Intake section (GID: `1213917352480612`) where Routine (GID: `1213608836755502`) is NOT set.
- Skip tasks with Routine already set (already triaged).

### Step 2 — Analyze Each Untriaged Task
For each untriaged Intake task, prepare triage recommendations:
- Routine bucket (Sweep/Core/Engine Room/Admin)
- Priority_RW (Today/Urgent/Not urgent)
- Frequency (GID: `1213921303350613`): weekly/monthly/quarterly/one-time
  - One-time: `1213921303350614`
  - Weekly: `1213921303350615`
  - Monthly: `1213921303350616`
  - Quarterly: `1213921303350617`
- Work_Product type: guide, reference, decision, playbook, analysis
- Date defaults:
  - No start_on AND no due_on → Begin=today, Due=today+7
  - No start_on AND due_on set → Begin=today
  - start_on set AND no due_on → Due=today+7
  - Both set → keep originals
  - ASANA CONSTRAINT: start_on requires due_on
- One-sentence scope statement.

### Step 3 — Present Triage to Richard
Do NOT auto-execute. Present for approval:
```
📥 ABPS AI Intake — [N] untriaged task(s):

- TASK: [name] (GID: [gid])
  - Routine: [bucket]
  - Priority_RW: [level]
  - Frequency: [cadence]
  - Work_Product: [type]
  - Begin Date: [YYYY-MM-DD] [← default if applicable]
  - Due Date: [YYYY-MM-DD] [← default if applicable]
  - Scope: [one sentence]
- ACTION: Approve, adjust, or skip?
```

### Step 3B — Execute Approved Triage
Set Routine, Priority_RW, Frequency, Kiro_RW via UpdateTask(custom_fields={...}). Apply date defaults in same call. Append date default notation to Kiro_RW.

### Step 3C — Section Move + Research Subtask
After field writes:

**IF Begin Date <= today:**
1. Move to In Progress (section GID: `1213917923741223`)
2. Create research subtask: `CreateTask(name='📋 Research: [parent task name]', parent=task_gid, assignee='1212732742544167', project='1213917352480610')`
3. Update Kiro_RW: append '→ Moved to In Progress, research subtask created.'

**IF Begin Date > today:**
- Leave in Intake with fields applied.
- Update Kiro_RW: append '→ Stays in Intake (begin date future: [start_on]).'
- No subtask creation.

### Step 3D — Pipeline Stage 1: Research (wiki-researcher)
For tasks in In Progress (GID: `1213917923741223`):
1. GetSubtasksForTask → find incomplete '📋 Research: [name]' subtask.
2. IF incomplete research subtask exists AND Begin Date <= today:
   - Invoke wiki-researcher with: task GID, description, Kiro_RW, Work_Product type.
   - Researcher posts pinned comment: CreateTaskStory(html_text=..., is_pinned='true')
   - Completes research subtask.
   - Logs stage transition as comment.
   - Updates Kiro_RW: 'pipeline: research completed [date]'
3. IF research subtask already completed → skip.
4. IF no research subtask → check for later pipeline subtasks.

### Step 3E — Pipeline Stage 2: Draft (wiki-writer)
For tasks in In Progress where research is complete but no draft subtask:
1. Verify pinned research comment exists (GetTaskStories, is_pinned=true).
2. Invoke wiki-writer with: task GID, description, pinned research, Kiro_RW, Work_Product type.
3. Writer loads style guides (richard-writing-style.md, richard-style-docs.md, richard-style-amazon.md).
4. Writes ~500w draft in html_notes (allowed tags: body, strong, em, u, s, code, a, ul, ol, li).
5. Draft structure: bold title, executive summary (2-3 sentences), 3-5 bold-headed sections, Next Steps.
6. Creates + completes '✏️ Draft: [name]' subtask.
7. Moves task to Review section (GID: `1213917923779848`).
8. Logs stage transition. Updates Kiro_RW.

### Step 3F — Pipeline Stage 3: Review (wiki-critic)
For tasks in Review (GID: `1213917923779848`) where draft is complete but no review subtask:
1. Invoke wiki-critic with: task GID, html_notes (draft), pinned research, Kiro_RW.
2. Scores 5 dimensions: usefulness, clarity, accuracy, dual-audience, economy (1-10 each).
3. Posts review as comment. Creates + completes '🔍 Review: [name]' subtask.
4. Decision:
   - **Average >= 8 (APPROVE):** Create approval subtask: `CreateTask(name='✅ Approve: [name]', resource_subtype='approval', parent=task_gid, assignee='1212732742544167', project='1213917352480610')`
   - **Average < 8, consecutive_sub8 < 2 (REVISE):** Post revision notes. Move back to In Progress. Increment consecutive_sub8 in Kiro_RW.
   - **Average < 8, consecutive_sub8 reaches 2 (ESCALATE):** Flag for Richard. No third revision attempt.
5. Threshold is exactly 8 — not 7.9, not 8.1.

### Step 3G — Pipeline Stage 4: Approval Detection
For tasks in Review with an approval subtask (resource_subtype='approval'):

**CASE A — APPROVED (completed === true):**
1. Read-before-write on html_notes (preserve Richard's additions).
2. Invoke wiki-writer for expansion (~500w → ~2000w). Load style guides.
3. Full doc structure: title, executive summary, context, analysis sections, recommendations, next steps with owners/dates.
4. Check Frequency field:
   - **One-time** (GID: `1213921303350614`): Move to Archive (GID: `1213917833240629`), mark completed. Do NOT register in recurring-task-state.json.
   - **Weekly/Monthly/Quarterly**: Move to Active (GID: `1213917968512184`). Register in recurring-task-state.json with key `abps_ai_{task_gid}`.
5. Log expansion. Update Kiro_RW.

**CASE B — PENDING (completed === false):**
- Check for Richard's comments after approval subtask creation → rejection signal.
- If rejection: move back to In Progress, complete the approval subtask, reset consecutive_sub8, log.
- If no comment: still pending, skip.

### Step 3H — Date Window Check
Scan triaged Intake tasks where Begin Date has arrived:
- start_on <= today AND NOT completed AND still in Intake → initiate pipeline (move to In Progress, create research subtask).
- start_on > today → skip.

### Step 3I — Near-Due Escalation
- due_on within 0-2 days AND NOT completed AND NOT in Active/Archive → set Priority_RW to Today (GID: `1212905889837830`).
- Update Kiro_RW: 'M/D: Near-due. Priority escalated.'
- Auto-execute (safety measure, no approval needed).

### Step 3J — Overdue Flagging
- due_on < today AND NOT completed AND no approved Approval subtask → flag as overdue.
- Update Kiro_RW: 'M/D: Overdue [N]d. Extend or close.'
- Recommend: extend due date, reduce scope, or kill.
- Include in daily brief.

### Step 3K — Refresh Cadence Check
For tasks in Active (GID: `1213917968512184`) with Frequency != one-time:
1. Read recurring-task-state.json → find entry `abps_ai_{task_gid}`.
2. Compute current_period (weekly=YYYY-WNN, monthly=YYYY-MM, quarterly=YYYY-QN).
3. If last_run_period != current_period → refresh is due.
4. Refresh: read current html_notes, invoke wiki-researcher for fresh context, invoke wiki-writer to update.
5. Add dated revision line: `<strong>Updated YYYY-MM-DD: [what changed]</strong>`
6. Post comment: '🔄 Refresh completed: [summary]'
7. Update recurring-task-state.json.

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

### Step 6 — Recurring Task Auto-Creation (AU + MX)
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
