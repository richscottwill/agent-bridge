<!-- DOC-0330 | duck_id: protocol-am-frontend -->



# AM-Frontend Protocol — Brief + Triage + Command Center

Interactive phase. Reads pre-computed state from AM-Backend. Does the work, puts it where Richard will find it, tells him what's ready.

All Asana writes follow the Guardrail Protocol in asana-command-center.md § Guardrail Protocol.

---




## Agentic Execution Rules (L5 Pattern)

**CRITICAL: Steps 1–5 execute without pausing for human input.** Present the brief (Step 1), then immediately proceed through Steps 2–5. Do NOT stop after the brief to ask Richard questions, confirm priorities, or request decisions. The protocol has all the rules needed to make autonomous choices (routine ordering, urgency sorting, time estimates, enrichment rules). Step 6 (Interactive Command Center) is the ONLY point where Richard gives live directions — and only after Steps 1–5 are complete.

If you encounter ambiguity during Steps 1–5 (e.g., unclear whether a task is resolved, conflicting signals), make the best-available decision, note it in the brief or Slack DM, and move on. Richard can adjust in Step 6.

The agent DOES work, not just proposes it. For every task touched during AM-Frontend:

1. **Write real content into Asana task descriptions** — draft emails, MBR/WBR callouts, Kingpin goal updates, monthly goal text, meeting agendas, stakeholder replies. The task description should contain work product Richard can review and send, not a blank page.
2. **Create email drafts in Outlook** — when a task requires sending an email, draft it. Include context from all sources (Slack signals, meeting history, DuckDB data, Asana task state).
3. **Identify the smallest next action** — for every task, specify the single smallest thing Richard needs to do (e.g., "pull LP URL report from Google Ads, fill in draft, hit send"). This goes in Next-action_RW.
4. **Enrich from all sources** — cross-reference Slack signals, email threads, meeting notes, DuckDB data, and Asana task history to provide full context in task descriptions.
5. **Calendar blocks include task context** — every calendar block description should contain the specific tasks, their next actions, and any draft content references.
6. **Kill zombie tasks autonomously** — tasks 30+ days overdue with clear kill signals (paused accounts, completed dependencies, superseded work) get completed with Kiro_RW explanation.
7. **Tell Richard what you did** — post a Slack DM summary listing all work done, drafts created, tasks enriched, and the ordered list of smallest next actions.




## Draft Safety Rule
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
- `~/shared/context/active/am-wiki-state.json`
- `~/shared/context/active/am-signals-processed.json`
- `~/shared/context/intake/slack-digest.md`
- `~/shared/context/intake/email-triage.md`
- `~/shared/context/intake/asana-digest.md`
- `~/shared/context/intake/asana-activity.md`




### SharePoint Fallback (Cold Start / Missing Files)
If any pre-computed state file is missing locally (container restart, first run on new environment):
1. Check SharePoint `Kiro-Drive/system-state/` for the file via `sharepoint_read_file(inline=true)`.
2. If found and Modified timestamp is <24h old → use it. Write to local path for subsequent reads.
3. If not found or stale → skip gracefully. Frontend will fall back to live MCP queries.
4. Log: "SharePoint pull: [filename] recovered from Kiro-Drive" or "SharePoint pull: [filename] not available, using live queries."
See ~/shared/context/protocols/sharepoint-durability-sync.md for full pull logic.

DuckDB-first queries (use instead of live MCP when AM-Backend has synced):
- Tasks/overdue/buckets → `asana.asana_tasks`, `asana.overdue`, `asana.by_routine`
- Email triage → `signals.emails_actionable`, `signals.emails_unanswered`
- Calendar → `main.calendar_today`, `main.calendar_week`
- Slack signals → `signals.slack_messages`, `signals.signal_tracker`
- Audit trail → `asana.recent_audit`
- **Project chronology → `main.project_timeline` (decisions, milestones, blockers, launches per project)**
- **Relationship state → `main.relationship_activity` (weekly interaction counts, trends per person)**
- **Meeting context → `main.meeting_series` (latest session dates, open items, running themes)**
- **Wiki gaps → `signals.wiki_candidates` (strong cross-channel topics without articles)**
- **Level allocation → `main.five_levels_weekly` (weekly time distribution across L1-L5)**
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

**Key consideration:** This section's content is critical for accurate operation. Cross-reference with related sections for full context.
### HEADS UP Section (from DuckDB + digests)
Cross-reference slack-digest.md `[ACTION-RW]` items with structured DuckDB views:
```sql
-- Unanswered Slack mentions by priority (thread-aware)
SELECT author_name, priority, days_old, channel_name, text_preview
FROM signals.slack_unanswered
WHERE richard_replied = FALSE
ORDER BY priority, days_old DESC;

-- Unanswered emails needing response
SELECT sender_name, priority, days_old, subject
FROM signals.emails_unanswered
WHERE action_needed = 'respond'
ORDER BY priority, days_old DESC;
```
Surface any item with days_old >= 3 as 🔴 CRITICAL. Items 1-2 days as 🟡 HIGH.
Include reply_time_hours context for recently-answered items if pattern is concerning (e.g., avg reply > 48h to a stakeholder).




### TODAY Section (from DuckDB)
- Query: `SELECT * FROM asana_by_routine` → bucket counts
- Query: `SELECT * FROM asana_overdue ORDER BY days_overdue DESC` → overdue list
- Query: `SELECT * FROM asana_tasks WHERE priority_rw = 'Today' AND completed = FALSE AND deleted_at IS NULL ORDER BY routine_rw` → Today tasks
- Query: `SELECT * FROM asana_completion_rate` → trailing completion stats

Display (block order: Sweep → Admin → Core → Engine Room):
- 🧹 Sweep: Routine=Sweep AND Priority_RW=Today. Name + due date + L1-L5 tag.
  - **Escalation marker:** Any task in Sweep whose Kiro_RW contains "Escalated to Sweep" (set by AM-2 Admin Escalation Check) SHALL be rendered with an `⚠️ ADMIN ESCALATION` prefix before the task name. These are Admin tasks auto-promoted to Sweep because they were 3+ days overdue — they need visibility as former Admin items, not just generic Sweep tasks.
- 📋 Admin (⏱️ 30-min time bound): Routine=Admin AND Priority_RW=Today.
  - **Time bound:** The Admin block is bounded to 30 minutes maximum. If tasks remain after 30 minutes, carry forward to tomorrow's Admin block — do NOT bleed into Core time. This protects the flow conditions (Csikszentmihalyi) for Core: clear goals, no interruptions, bounded challenge.
  - **Habit loop reward:** After Admin block completes (all tasks done OR 30-min bound reached), surface in the brief and Slack DM: `"✅ Admin clear. [N] tasks done. Core block starts now."` This is the immediate feedback Csikszentmihalyi requires for flow entry and the reward Duhigg requires for habit formation. [N] = count of Admin tasks with Priority_RW=Today.
- 🎯 Core: Routine=Core AND Priority_RW=Today. THE HARD THING gets first slot.
- ⚙️ Engine Room: Routine=Engine Room AND Priority_RW=Today.
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
Query DuckDB via MCP (`execute_query`) for forecast and OP2 pacing context:
- `SELECT * FROM ps.market_status` — latest actuals + forecast + OP2 per market
- `SELECT * FROM ps.monthly_pacing` — MTD regs/spend vs OP2 target
- `SELECT market, hit_rate, mean_error_pct, ci_width_adjustment FROM ps.calibration_state` — engine calibration

Display in brief:
- 📊 Pacing: AU {pacing_regs_pct}% regs / {pacing_cost_pct}% spend vs OP2 | MX {pacing_regs_pct}% / {pacing_cost_pct}%
- 🎯 Forecast accuracy: {hit_rate}% hit rate (last 20 predictions)
- If any market pacing < 80% or > 120%: flag as ⚠️ pacing alert




### Goal Alerts
If any goals at-risk or off-track: goal name, status, metric gap, recommended action.




### Wiki Pipeline Status
Read `am-wiki-state.json` (from AM-Backend Phase 3B: `build-wiki-index.py` + `signals.wiki_candidates` + SharePoint artifacts cache). Surface:
- Pipeline counts (draft / review / final / active / published) — one line
- Stale article count (if >0)
- Wiki candidates with quality_score >= 10.0 that are **not yet covered** by any local article

**Note:** The `ABPS AI - Content` Asana project is deprecated as of 2026-04-17. Do not query or write to it. Wiki work is tracked in DuckDB `wiki.publication_registry`, the Kiro dashboard (`shared/dashboards/wiki-search.html` Pipeline view), `~/shared/wiki/agent-created/`, and SharePoint `Documents/Artifacts/`.

```
📚 WIKI CANDIDATES (uncovered topics from cross-channel signals):
- [topic] — quality: [X], channels: [N], authors: [N]
  → No existing article. Route to wiki-editor agent if still strong next week.
```




### Portfolio Status
Read am-portfolio-findings.json:
- Per-project: task count, overdue, near-due, health color, staleness.
- Budget Tasks: ⚡ if due within 3d, 🔴 CRITICAL if overdue.
- Cross-team blockers.




### Meeting Prep
Query DuckDB for today's calendar: `SELECT * FROM main.calendar_today ORDER BY start_time`.
For each meeting, query signal_tracker for attendee topics (last 7 days). Include: "Brandon's hot topics: [list]."
If main.calendar_today is empty (sync hasn't run), fall back to live: calendar_view(start_date=today, view=day).

**Enriched meeting prep (from Phase 2.5 outputs):**
- Query `main.meeting_series` for the matching series file → include latest session summary, open items, running themes
- Query `main.relationship_activity` for each attendee → include interaction trend and recent touchpoint count
- Query `main.project_timeline` for events involving the attendee → include recent decisions and commitments
- Read the meeting series file from `~/shared/wiki/meetings/` for full narrative context
- This replaces the previous pattern of only loading signal_tracker topics — now the agent has the full meeting history, relationship state, and project chronology for each attendee




### Friday Additions
- Calibration.
- Remind Agent Bridge Sync.


---




## Step 2: Output Channels

**Proceed immediately after Step 1 — do not pause for human input.** The brief has been presented; now execute.




### Email Brief (AUTO-SEND)
Dark navy HTML email to prichwil@amazon.com. Full brief content formatted as styled HTML.




### Slack Brief
Post to rsw-channel (C0993SRL6FQ). Include Asana task context inline.
- **Admin block completion reward:** After the Admin section, include: `"✅ Admin clear. [N] tasks done. Core block starts now."` where [N] = count of Admin tasks with Priority_RW=Today. This surfaces the habit loop reward (Duhigg) in the channel Richard checks first.




### Dashboard Update
Edit pinned message in rsw-channel.




### Calendar Blocks
Query DuckDB for today's meetings: `SELECT * FROM main.calendar_today ORDER BY start_time`.
If calendar_today is empty, fall back to live: calendar_view(start_date=today, view=day).

**Per-Task Block Rules (mandatory):**
1. Create ONE calendar block per Today-priority task — never group tasks into bucket blocks.
2. Each block: minimum 15 minutes, maximum 1.5 hours.
3. Block order follows the routine sequence: 🧹 Sweep first → 📋 Admin (30 min max) → 🎯 Core → ⚙️ Engine Room last.
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
6. **Admin block hard cap:** The Admin calendar block SHALL NOT exceed 30 minutes. If total Admin task time estimates exceed 30 minutes, include only what fits within 30 minutes (highest urgency first) and note remaining tasks as "carry forward to tomorrow's Admin block." This protects Core's flow window (Csikszentmihalyi).
7. Block body must contain: task context (what, why, who's waiting), specific next action, cross-references to related signals/meetings, and any prep notes.
8. **Admin block completion message:** The Admin calendar block description SHALL end with the habit loop reward template: `"✅ Admin clear. [N] tasks done. Core block starts now."` where [N] = number of Admin tasks scheduled in the block. This fires the cue-routine-reward chain (Duhigg) and signals flow entry readiness (Csikszentmihalyi).
9. Skip blocks that would overlap existing meetings — fit around fixed calendar.
10. Flag overload if total block time exceeds available time between meetings.
11. Delete any previous day's work blocks before creating new ones (clean slate each morning).

Create time blocks via Outlook MCP calendar_meeting(operation='create') in gaps between existing meetings.




### Proactive Drafts
Query DuckDB for unanswered signals 24h+:
```sql
-- Unanswered Slack mentions (thread-aware)
SELECT author_name, priority, days_old, reply_time_hours, text_preview, channel_name
FROM signals.slack_unanswered
WHERE richard_replied = FALSE
ORDER BY priority, days_old DESC;

-- Unanswered emails
SELECT sender_name, priority, days_old, subject
FROM signals.emails_unanswered
WHERE action_needed = 'respond'
ORDER BY priority, days_old DESC;
```
For each unanswered signal 24h+, generate draft reply to ~/shared/context/intake/drafts/.
Use relationship_activity for tone calibration (warm vs formal based on interaction trend).

---




## Step 3: Enrichment Execution (Agentic)

Read am-enrichment-queue.json. Execute enrichment autonomously — don't ask, do.

**MANDATORY COMPLETION RULE:** Enrich ALL tasks with missing Kiro_RW or Next-action_RW — not just the top 10 from the backend proposals. Query Asana live for every incomplete task missing either field and enrich it. The enrichment queue proposals are a starting point; the agent must go beyond them to achieve zero gaps. Ignore the `approval_required` flag in the JSON — enrichment is always autonomous. If Asana data is stale, run a fresh pull first (SearchTasksInWorkspace), then enrich. Do not defer enrichment for staleness — fix the staleness, then enrich. Report total enriched count in the Slack DM triage summary.




### Context Enrichment Queries (run ONCE before enriching any tasks)

Before writing Kiro_RW or Next_Action_RW on any task, load richer context from Phase 2.5 outputs:

```sql
-- Project timeline: recent decisions and events per project (last 14 days)
SELECT project_name, event_date, event_type, summary, people_involved
FROM main.project_timeline
WHERE event_date >= CURRENT_DATE - INTERVAL '14 days'
ORDER BY project_name, event_date DESC;

-- Relationship activity: who's active this week, interaction trends
SELECT person_name, person_alias, slack_interactions, email_exchanges, meetings_shared, total_score, interaction_trend
FROM main.relationship_activity
WHERE week = DATE_TRUNC('week', CURRENT_DATE)::DATE
ORDER BY total_score DESC;

-- Wiki candidates: strong signal topics that could inform task context
SELECT topic, total_strength, channel_spread, unique_authors, quality_score
FROM signals.wiki_candidates
ORDER BY quality_score DESC LIMIT 10;

-- Meeting series: latest session context per series (for tasks tied to meeting outcomes)
SELECT series_id, meeting_name, last_session_date, open_item_count, running_themes
FROM main.meeting_series
WHERE last_session_date >= CURRENT_DATE - INTERVAL '14 days'
ORDER BY last_session_date DESC;
```

Use this context when writing enrichment content:
- **Kiro_RW**: Include relevant project_timeline events. E.g., "4/6: Brandon decided data-led approach for AU LP. 4/8: OP1 workshop — LiveRamp is F90 play."
- **Next_Action_RW**: Reference the most recent decision or commitment. E.g., "Pull AU CVR data per Brandon 4/6 decision — share with Brandon + Dwayne."
- **html_notes drafts**: When drafting emails or Slack replies, check relationship_activity for interaction trend and meeting_series for latest session context. A draft to Lorena (trend: "warming", 5 touchpoints) should be warmer than a draft to a cold contact.
- **Task descriptions**: Cross-reference wiki_candidates — if a task's topic matches a strong wiki candidate, note it: "📚 This topic is a wiki candidate (quality: X). Consider documenting learnings."




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




## Step 4: Wiki Callout (one-line readiness check)

Compressed 2026-04-21 per karpathy verdict. The full wiki triage (stale articles, SharePoint drift, new-article routing) is now handled by the weekly `wiki-maintenance.kiro.hook`. AM-Frontend's job is a single surfaced line, not a decision point.

Query both sources and emit one line. If both return empty, emit nothing.

```sql
-- Pipeline state
SELECT COUNT(*) FILTER (WHERE stage='draft') AS draft,
       COUNT(*) FILTER (WHERE stage='review') AS review,
       COUNT(*) FILTER (WHERE stage='final') AS final_stage,
       COUNT(*) FILTER (WHERE stage='published') AS published
FROM wiki.publication_registry;

-- Top uncovered candidate
SELECT topic, ROUND(quality_score, 1) AS quality
FROM signals.wiki_candidates
WHERE coverage_status = 'uncovered' OR coverage_status IS NULL
ORDER BY quality_score DESC LIMIT 1;
```

Output format:
```
📚 Wiki: [N] in pipeline (draft/review/final/published). Top uncovered candidate: [topic] (quality [X]).
```

If the pipeline query returns all-zero counts AND the candidate query returns no rows, emit nothing. No routing, no action, no decision. Weekly wiki-maintenance handles the rest.

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




### Recurring Task Summary (informational)
List auto-created recurring tasks: '[name] → next due [date] ✅'. No approval needed — auto-created by backend.

---




## Step 6: Dashboard Refresh — Command Center, Forecast Tracker, WBR Callouts

**Proceed immediately after Step 5 — do not pause for human input.** The command center is the set of dashboards Richard uses to monitor performance and make decisions. Refresh all of them with the latest data.




### 6A. Run Full Dashboard Pipeline

Execute `python3 ~/shared/dashboards/refresh-all.py` which runs in sequence:
1. `extract-ly-data.py` → extracts daily data into ps-forecast-tracker.xlsx
2. `refresh-forecast.py` → builds `data/forecast-data.json` (weekly actuals, predictions, CI bands, OP2 targets for all 10 markets)
3. `refresh-callouts.py` → builds `data/callout-data.json` (WBR callout narratives, metrics, brand/NB detail, projections, anomalies for all markets)
4. `generate-command-center.py` → builds `data/command-center-data.json` (block state, overdue tasks, signals, emails from AM-auto outputs)

If any script fails, log the error and continue with remaining scripts. Report failures in the triage summary (Step 7).




### 6B. Populate Actionable Intelligence Sections

After the dashboard pipeline runs, the agent populates four intelligence sections in `command-center-data.json`. These replace the old overdue/emails/slack/pacing grid with decision-ready intelligence.

**Data sources for each section:**




#### Commitments — Things I Said I Would Do

**Integrity principle:** Richard wants to be a man of integrity — accountable to his own words first, then to what others ask. Breaking your own promise is worse than missing someone else's request. This distinction is permanent and applies to every future run.

**Ordering rule (mandatory for every run):**
1. **Richard said it** (`said_by: "richard"`) — things Richard explicitly volunteered or committed to in meetings, Slack, or email. These come first, always. Scan transcripts for Richard's voice saying "I will", "I'll", "let me", "I'm going to", "I'm putting that down", "I can do that."
2. **Others asked — manager** (`said_by: "other"`, `asker_weight: "manager"`) — things Brandon asked Richard to do. Brandon's asks carry the most weight after Richard's own words.
3. **Others asked — stakeholder** (`said_by: "other"`, `asker_weight: "stakeholder"`) — things Kate, Lena, Lorena, or other key stakeholders asked.
4. **Others asked — peer** (`said_by: "other"`, `asker_weight: "peer"`) — things Yun, Stacey, Andrew, Adi, or other peers asked.

Within each group, sort by: overdue severity (days_old DESC), then relationship importance.

**Asker weight hierarchy:** Brandon (L7 manager) > Kate (L8 skip-level) > Lena/Lorena (market stakeholders) > Stacey/Andrew/Adi/Yun (peers).

**Required fields per commitment:** `text`, `source`, `person`, `days_old`, `overdue`, `said_by` ("richard" or "other"), `asker_weight` (for "other" items: "manager", "stakeholder", "peer"), `quote` (verbatim — Richard's own words if he said it, the asker's words if they asked).

**Data sources:**
- **Hedy meeting transcripts** (last 7 days): Scan `user_todos` and cleaned transcripts. Distinguish Richard's voice from others — only tag `said_by: "richard"` when Richard is the speaker.
- **Slack messages** (last 14 days): Query `signals.slack_messages` where `author_name = 'Richard Williams'` for commitment language.
- **Asana tasks with Kiro_RW containing dates**: Tasks where Richard committed to a specific action by a date.
- **Email sent items**: Check for promises made in replies.

For each commitment, record all required fields above. The dashboard renders Richard's commitments first, then a visual "Others asked" divider, then others' asks grouped by weight.




#### 🔄 Delegate — Things I Could Hand Off
Identify tasks Richard is doing that someone else could own:
- Tasks in Engine Room that are BAU/recurring and have a natural owner (e.g., AU team post-handoff, Yun for MX).
- Tasks where someone else flagged the issue (e.g., Yun found broken images → Yun should submit the SIM).
- Tasks that are below Richard's level (L5 doing L3 work) per the Five Levels framework.
- Tasks where a teammate has more context or access.

For each: `task`, `to` (suggested delegate), `reason`.




#### 📢 Communicate — Things to Share with Team
Extract information Brandon shared with Richard that the team should know:
- **Brandon 1:1 decisions**: Org changes, strategy shifts, timeline updates, stakeholder feedback.
- **Weekly meeting outcomes**: Format changes (OCI Flash), reporting cadence changes (IECCP quarterly), compliance checks (Polaris markets).
- **Signals from Kate/Todd**: Anything from skip-level that affects team direction.
- **Cross-team context**: What other teams are doing that affects PS (MCS, ABMA, Legal).

For each: `text`, `context` (source meeting + why it matters).




#### ⭐ Differentiate — Things That Set Me Apart
Surface high-leverage actions from career conversations and Brandon's coaching:
- **Annual review growth areas**: What Brandon said Richard needs to do differently (3/24 meeting).
- **Comp review signals**: What drove the 10.5% increase, what would drive more (4/6 meeting).
- **Brandon's explicit coaching**: "One voice should be you", "proactive sharing of results", "earning trust through regimented mechanisms".
- **Promo criteria**: What "walk on water" looks like, what artifacts to ship, what visibility to create.
- **Current opportunities**: Tasks that, if done well, would demonstrate above-and-beyond performance.

For each: `action` (specific thing to do), `why` (Brandon's words or career logic).

**JSON key:** `differentiate` (in `command-center-data.json`).

**Execution:** The agent reads Hedy session details, DuckDB signals, and Asana task state to populate these sections. The `generate-command-center.py` script handles the static data (blocks, tasks); the agent enriches with the four intelligence sections after the script runs.




### 6C. Verify Dashboard Data Freshness

After pipeline completes, verify output files exist and are current:
- `data/forecast-data.json` — check `max_week` matches current week
- `data/callout-data.json` — check `generated` timestamp is today
- `data/command-center-data.json` — check `generated` timestamp is today

If any file is stale or missing, flag in the brief: "⚠️ Dashboard [name] failed to refresh — [reason]."




### 6D. Interactive Adjustments (Richard-directed, if needed)

After dashboards are refreshed, Richard may give live directions:
- Move tasks between Routine buckets
- Change due dates or Priority_RW
- Create new tasks with Routine + Priority pre-set
- Write/update task descriptions
- Add comments (CreateTaskStory)
- Complete tasks, create subtasks, set Importance_RW
- Re-run a specific dashboard script with different parameters
- Trigger WBR callout pipeline for a specific market

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
