<!-- DOC-0330 | duck_id: protocol-am-frontend -->
# AM-Frontend Protocol — Brief + Triage + Command Center

Interactive phase. Reads pre-computed state from AM-Backend. Does the work, puts it where Richard will find it, tells him what's ready.

All Asana writes follow the Guardrail Protocol in asana-command-center.md § Guardrail Protocol.

---

## Agentic Execution Rules (L5 Pattern)

The agent DOES work, not just proposes it. For every task touched during AM-Frontend:

1. **Write real content into Asana task descriptions** — draft emails, MBR/WBR callouts, Kingpin goal updates, monthly goal text, meeting agendas, stakeholder replies. The task description should contain work product Richard can review and send, not a blank page.
2. **Create email drafts in Outlook** — when a task requires sending an email, draft it. Include context from all sources (Slack signals, meeting history, DuckDB data, Asana task state).
3. **Identify the smallest next action** — for every task, specify the single smallest thing Richard needs to do (e.g., "pull LP URL report from Google Ads, fill in draft, hit send"). This goes in Next-action_RW.
4. **Enrich from all sources** — cross-reference Slack signals, email threads, meeting notes, DuckDB data, and Asana task history to provide full context in task descriptions.
5. **Calendar blocks include task context** — every calendar block description should contain the specific tasks, their next actions, and any draft content references.
6. **Kill zombie tasks autonomously** — tasks 30+ days overdue with clear kill signals (paused accounts, completed dependencies, superseded work) get completed with Kiro_RW explanation.
7. **Tell Richard what you did** — post a Slack DM summary listing all work done, drafts created, tasks enriched, and the ordered list of smallest next actions.

## Draft Safety Rule

ALL email drafts MUST follow this rule — no exceptions:
- **To:** prichwil@amazon.com ONLY
- **CC/BCC:** empty
- **Subject prefix:** "DRAFT — " followed by the intended subject
- **Body top:** Bold line stating intended recipients: "INTENDED RECIPIENTS: To: [email] | CC: [email, email]"
- **Never put real recipients in To/CC/BCC fields.** Richard reviews and re-addresses manually before sending.

---

## Context Load
body.md, spine.md, org-chart.md, rw-trainer.md, rw-task-prioritization.md, brain.md, eyes.md, device.md, gut.md, rw-tracker.md, hands.md, amcc.md, memory.md, richard-writing-style.md, asana-command-center.md.

Pre-computed state files (from AM-Backend):
- `~/shared/context/active/am-enrichment-queue.json`
- `~/shared/context/active/am-portfolio-findings.json`
- `~/shared/context/active/am-abps-ai-state.json`
- `~/shared/context/active/am-signals-processed.json`
- `~/shared/context/intake/slack-digest.md`
- `~/shared/context/intake/email-triage.md`
- `~/shared/context/intake/asana-digest.md`
- `~/shared/context/intake/asana-activity.md`

DuckDB-first queries (use instead of live MCP when AM-Backend has synced):
- Tasks/overdue/buckets → `asana.asana_tasks`, `asana.overdue`, `asana.by_routine`
- Email triage → `signals.emails_actionable`, `signals.emails_unanswered`
- Calendar → `main.calendar_today`, `main.calendar_week`
- Slack signals → `signals.slack_messages`, `signals.signal_tracker`
- Audit trail → `asana.recent_audit`
- Staleness check: if `MAX(synced_at) < CURRENT_TIMESTAMP - INTERVAL '12 hours'`, auto-refresh from live MCP AND update DuckDB inline before proceeding.

---

## Step 1: Daily Brief

### Brief Structure
1. TRAINER CHECK-IN
2. HEADS UP
3. SLACK OVERNIGHT
4. TODAY (from Asana)
5. SPEC SHEET
6. T-MINUS
7. aMCC
8. SYSTEM HEALTH

### TODAY Section (from DuckDB)
- Query: `SELECT * FROM asana_by_routine` → bucket counts
- Query: `SELECT * FROM asana_overdue ORDER BY days_overdue DESC` → overdue list
- Query: `SELECT * FROM asana_tasks WHERE priority_rw = 'Today' AND completed = FALSE AND deleted_at IS NULL ORDER BY routine_rw` → Today tasks
- Query: `SELECT * FROM asana_completion_rate` → trailing completion stats

Display:
- 🧹 Sweep: Routine=Sweep AND Priority_RW=Today. Name + due date + L1-L5 tag.
- 🎯 Core: Routine=Core AND Priority_RW=Today. THE HARD THING gets first slot.
- ⚙️ Engine Room: Routine=Engine Room AND Priority_RW=Today.
- 📋 Admin: Routine=Admin AND Priority_RW=Today.
- ⚠️ Overdue: Count + oldest task + days overdue.
- 📦 Needs Triage: Tasks with no Routine set.
- Bucket counts: Sweep X/5, Core X/4, Engine Room X/6, Admin X/3.

### Coherence Alerts
Include flags from AM-Backend coherence check. If zero: "✅ DuckDB ↔ Body coherence check passed."

### Five Levels Annotation
[L1]-[L5] tag per asana-command-center.md mapping.

### Activity Signals
Read intake/asana-activity.md: 💬 comments, 📅 due date changes, 👤 reassignments.

### Forecast Pacing (from WBR Pipeline)
Query MotherDuck for forecast and OP2 pacing context:
- `SELECT * FROM ps.market_status` — latest actuals + forecast + OP2 per market
- `SELECT * FROM ps.monthly_pacing` — MTD regs/spend vs OP2 target
- `SELECT market, hit_rate, mean_error_pct, ci_width_adjustment FROM ps.calibration_state` — engine calibration

Display in brief:
- 📊 Pacing: AU {pacing_regs_pct}% regs / {pacing_cost_pct}% spend vs OP2 | MX {pacing_regs_pct}% / {pacing_cost_pct}%
- 🎯 Forecast accuracy: {hit_rate}% hit rate (last 20 predictions)
- If any market pacing < 80% or > 120%: flag as ⚠️ pacing alert

### Goal Alerts
If any goals at-risk or off-track: goal name, status, metric gap, recommended action.

### ABPS AI Document Factory
Read am-abps-ai-state.json: Intake count, In Progress pipeline stages, Review status, Active count, Archive count, alerts.

### Portfolio Status
Read am-portfolio-findings.json:
- Per-project: task count, overdue, near-due, health color, staleness.
- Budget Tasks: ⚡ if due within 3d, 🔴 CRITICAL if overdue.
- Cross-team blockers.

### Meeting Prep
Query DuckDB for today's calendar: `SELECT * FROM main.calendar_today ORDER BY start_time`.
For each meeting, query signal_tracker for attendee topics (last 7 days). Include: "Brandon's hot topics: [list]."
If main.calendar_today is empty (sync hasn't run), fall back to live: calendar_view(start_date=today, view=day).

### Friday Additions
- Calibration.
- Remind Agent Bridge Sync.


---

## Step 2: Output Channels

### Email Brief (AUTO-SEND)
Dark navy HTML email to prichwil@amazon.com. Full brief content formatted as styled HTML.

### Slack Brief
Post to rsw-channel (C0993SRL6FQ). Include Asana task context inline.

### Dashboard Update
Edit pinned message in rsw-channel.

### Calendar Blocks
Query DuckDB for today's meetings: `SELECT * FROM main.calendar_today ORDER BY start_time`.
If calendar_today is empty, fall back to live: calendar_view(start_date=today, view=day).

**Per-Task Block Rules (mandatory):**
1. Create ONE calendar block per Today-priority task — never group tasks into bucket blocks.
2. Each block: minimum 15 minutes, maximum 1.5 hours.
3. Block order follows the routine sequence: 🧹 Sweep first → 🎯 Core → ⚙️ Engine Room → 📋 Admin last.
4. Within each routine, order by urgency: overdue first, then by due date ascending.
5. Time estimates must be realistic for a human doing the actual work:
   - Quick Slack reply / confirm / triage: 15 min
   - Email reply requiring data lookup: 20 min
   - Agenda prep / meeting prep: 15 min
   - Data pull + spreadsheet update: 30 min
   - Strategic doc editing / writing: 45 min–1.5 hr
   - Campaign build / keyword work: 30–45 min
   - Budget/PO/invoice review: 20–30 min
   - Test design / framework drafting: 45 min–1.5 hr
6. Block body must contain: task context (what, why, who's waiting), specific next action, cross-references to related signals/meetings, and any prep notes.
7. Skip blocks that would overlap existing meetings — fit around fixed calendar.
8. Flag overload if total block time exceeds available time between meetings.
9. Delete any previous day's work blocks before creating new ones (clean slate each morning).

Create time blocks via Outlook MCP calendar_meeting(operation='create') in gaps between existing meetings.

### Proactive Drafts
Query DuckDB for unanswered signals 24h+. Generate drafts to ~/shared/context/intake/drafts/.

---

## Step 3: Enrichment Execution (Agentic)

Read am-enrichment-queue.json. Execute enrichment autonomously — don't ask, do.

### For each task needing enrichment:
1. Read task details (GetTaskDetails) for current state and context
2. Write Kiro_RW in brevity format: `M/D: <status in under 10 words>`
3. Write Next-action_RW: imperative verb, under 15 words, the smallest next step
4. Write real content into html_notes:
   - If task requires an email → draft the email in the task description + create Outlook draft (to prichwil only, intended recipients in body)
   - If task requires a WBR/MBR/Kingpin/monthly goal → write the actual callout/goal text
   - If task requires a Slack reply → write the draft message in the task description
   - If task requires a document → write the outline or first draft
5. Set missing dates: start_on = max(today, due_on - 7) if due_on set but start_on null
6. Set Priority_RW default: "Not urgent" if Routine set but Priority_RW null
7. Log each write to asana-audit-log.jsonl

### Portfolio Enrichment
Same pattern, grouped by project. Filter to Richard's tasks only.

### On API failure → log → retry once → skip and flag in Slack DM.

---

## Step 4: ABPS AI Triage

Read am-abps-ai-state.json. Present untriaged Intake tasks for approval.

```
📥 ABPS AI Intake — [N] untriaged task(s):

- TASK: [name] (GID: [gid])
  - Routine: [bucket]
  - Priority_RW: [level]
  - Frequency: [cadence]
  - Work_Product: [type]
  - Begin Date: [YYYY-MM-DD]
  - Due Date: [YYYY-MM-DD]
  - Scope: [one sentence]
- ACTION: Approve, adjust, or skip?
```

### Execute Approved Triage
Set fields via UpdateTask. Apply date defaults. Section moves. Research subtask creation. Pipeline advancement (Steps 3B–3K from original am-triage.md Phase 1B).

---

## Step 5: Portfolio Findings + Alerts

Read am-portfolio-findings.json. Present:

```
📊 PORTFOLIO SCAN — [N] projects scanned:

[Portfolio Name] ([N] projects):
  - [Project]: [task_count] tasks ([overdue] overdue, [near_due] near-due)
    Status: [🟢/🟡/🔴] (last update: [date] — [stale/current])
    Enrichment needed: [N] tasks missing fields

⚠️ PORTFOLIO ALERTS:
  - Near-due: [tasks with project context]
  - Overdue: [tasks with project context]
  - Stale projects: [list with days since last update]
  - Cross-team blockers: [MX blockers]
  - Budget: [budget task alerts]
  - Recurring: [auto-creation proposals]
  - Event countdown: [Paid App escalation proposals]
```

### Overdue Kill-or-Revive Decisions
Present overdue tasks grouped by severity (30+d, 20-29d, 10-19d, 1-9d). For each: extend, kill, or delegate?

### Recurring Task Approval
Present auto-created recurring task proposals: 'Auto-created next [name] due [date]. Approve?' Delete if rejected.

---

## Step 6: Interactive Command Center

Available for Richard's live directions after the agent has already done its autonomous work. The agent has already enriched tasks, written drafts, created calendar blocks, and killed zombies. This step is for Richard to give additional directions or adjustments.

### Agent-Initiated Actions (done before Richard speaks)
- Enrich all tasks with content, drafts, and next actions
- Kill zombie tasks (30+ days overdue with clear kill signals)
- Create calendar blocks with task-specific context
- Draft emails and Slack messages for overdue communications
- Write MBR/WBR/Kingpin content into task descriptions

### Supported Operations (Richard-directed)
- Move tasks between Routine buckets
- Change due dates
- Change Priority_RW (Today/Urgent/Not urgent)
- Create new tasks with Routine + Priority pre-set
- Write/update task descriptions (notes or html_notes)
- Add comments (CreateTaskStory)
- Complete tasks
- Create subtasks
- Set Importance_RW

---

## Step 7: Triage Summary

Post summary to Richard's Slack DM:
```
self_dm(login="prichwil", text="📬 AM Triage Complete
• New tasks: [N] (from [sources])
• Updated tasks: [N] (new signals on existing)
• Enriched: [N] tasks with field updates
• Deferred: [N] (low priority, backlog)
• Dismissed: [N] (FYI only)")
```

---

## Log Hook Execution
```sql
INSERT INTO hook_executions (hook_name, execution_date, start_time, end_time, duration_seconds,
    phases_completed, asana_reads, asana_writes, slack_messages_sent, duckdb_queries, summary)
VALUES ('am-frontend', CURRENT_DATE, '[start]', '[end]', [duration],
    [phases], [reads], [writes], [slack_msgs], [queries], '[summary]');
```
