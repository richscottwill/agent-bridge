<!-- DOC-0335 | duck_id: protocol-asana-goal-updater-protocol -->
# Asana Goal Updater Protocol


## Details

Last updated: 2026-04-03

## Purpose

Monthly protocol for updating all 14 of Richard's Asana goals with honest, evidence-based status assessments. Runs on the first business day of each month. Draft-first — never auto-post.

## Trigger

**When:** First business day of each month (detected during EOD-2 System Refresh).
**How:** EOD-2 checks `date +%d` and day-of-week. If today is the 1st (or the first weekday after the 1st), trigger the Goal Updater sequence.
**Fallback:** If missed, AM-2 on the next session flags "Goal updates overdue — last updated [date]."

[38;5;10m> [0m## Amazon FY26 Calendar Reference[0m[0m
[0m[0m
### Full Year[0m[0m
- FY26: Feb 2026 – Jan 2027[0m[0m
[0m[0m
### First Half (H1)[0m[0m
- H1 FY26: Feb – Jul 2026[0m[0m
- Q1 FY26: Feb – Apr 2026[0m[0m
- Q2 FY26: May – Jul 2026[0m[0m
[0m[0m
### Second Half (H2)[0m[0m
- H2 FY26: Aug 2026 – Jan 2027[0m[0m
- Q3 FY26: Aug – Oct 2026[0m[0m
- Q4 FY26: Nov 2026 – Jan 2027[0m[0m
[0m[0m
---
## The 14 Goals

### Registration Goals (numeric — pull from DuckDB)

| # | Goal | GID | Period | Target | Last Known | Pace |
|---|------|-----|--------|--------|------------|------|
| 1 | MX/AU paid search registrations (parent) | `1213245014119128` | FY26 | 100% | 18% | — |
| 2 | MX registrations | `1213204514049680` | FY26 | 11,100 | 2,167 (20%) | — |
| 3 | AU registrations | `1213204514049684` | FY26 | 12,906 | 2,231 (17%) | — |
| 13 | Paid App Installs | `1213204514049812` | FY26 | 435,000 | 120,621 (28%) | — |

### Testing Goals (milestone-based — pull from task completion)

| # | Goal | GID | Period | Target | Last Known | Status |
|---|------|-----|--------|--------|------------|--------|
| 4 | MX + AU market testing (parent) | `1213245014119125` | FY26 | 4 experiments | 0% | — |
| 5 | MX tests | `1213204514049688` | FY26 | 100% | 0% | 🟡 yellow |
| 6 | AU tests | `1213204514049691` | FY26 | 100% | 0% | 🟡 yellow |
| 7 | AU test 1: Brand LP | `1213204514049694` | Q1 FY26 | 100% | 0% | 🟡 Q1 ENDED |
| 8 | MX test 1: Brand LP | `1213204514049706` | Q1 FY26 | 100% | 0% | 🟡 Q1 ENDED |
| 9 | Globalized cross-market testing (parent) | `1213245014119131` | FY26 | 3 tests | 0% | 🟢 green |
| 14 | Paid App Tests | `1213204514049830` | FY26 | 3 tests | 0 | — |


#### Key Points
- Primary function: Testing Goals (milestone-based — pull from task completion)
- Referenced by other sections for context

### Project Goals (percentage-based — pull from task/project progress)

| # | Goal | GID | Period | Target | Last Known | Status |
|---|------|-----|--------|--------|------------|--------|
| 10 | WW in-context email overlay | `1213204514049667` | H1 FY26 | 100% | 0% | 🟢 green |
| 11 | PS redirect mapping | `1213204514049671` | H1 FY26 | 100% | 0% | 🟢 green |
| 12 | Paid App (parent) | `1213204514049810` | FY26 | 100% | 14% | 🟢 green |

---

## Step-by-Step Procedure

### Step 1: Pull Current Goal Data from Asana

For each of the 14 goals, call `GetGoal(goal_gid)` and extract:
- `metric.current_number_value` (current progress)
- `metric.target_number_value` (target)
- `status` (green/yellow/red)
- `status_updates` (last update date and text)
- `time_period` (FY26, Q1 FY26, H1 FY26)

```
Goal GIDs (in order):
1213245014119128, 1213204514049680, 1213204514049684,
1213245014119125, 1213204514049688, 1213204514049691,
1213204514049694, 1213204514049706, 1213245014119131,
1213204514049667, 1213204514049671, 1213204514049810,
1213204514049812, 1213204514049830
```

Store results in a working table: goal name, GID, current value, target value, % complete, last status, last update date.

### Step 2: Cross-Reference with Completed Tasks

Search for tasks completed in the prior calendar month that relate to each goal:

```
SearchTasksInWorkspace(
  workspace=8442528107068,
  assignee_any=1212732742544167,
  completed=true,
  completed_on.after=YYYY-MM-01,    // first day of prior month
  completed_on.before=YYYY-MM-DD    // last day of prior month
)
```

For each completed task, check project membership to map to goals:
- Tasks in AU project (1212762061512767) → AU registration goal, AU test goals
- Tasks in MX project (1212775592612917) → MX registration goal, MX test goals
- Tasks in Paid App project (1205997667578886) → Paid App goals
- Tasks in WW Testing project (1205997667578893) → Testing goals, email overlay, redirect mapping
- Tasks in PS-Owned Global Testing (1213279426031997) → Globalized testing goal
- Tasks mentioning "Brand LP" → Brand LP test goals (AU/MX)
- Tasks mentioning "email overlay" → WW email overlay goal
- Tasks mentioning "redirect" → PS redirect mapping goal

Compile per-goal: count of tasks completed, task names, and any milestone completions.

### Step 3: Pull DuckDB Registration Data

For numeric registration goals, query DuckDB for actual month-over-month data.

**Primary tables (when loaded):**
- `monthly_metrics` — market, month, regs, spend, cpa
- `daily_metrics` — market, date, regs (for MTD calculations)
- `weekly_metrics` — market, week, regs

**Note:** As of 2026-04-03, the DuckDB instance has schema definitions for these tables but they may need re-ingestion. If tables are empty or missing, fall back to the last known values from Asana goal metrics and flag "DuckDB data unavailable — using Asana metric values only."

**SQL queries for each numeric goal:**

```sql
-- MX registrations YTD (FY26 = Feb 2026 onwards)
SELECT SUM(regs) as ytd_regs
FROM monthly_metrics
WHERE market = 'MX' AND month >= '2026-02';

-- MX registrations for prior month only
SELECT regs as month_regs, spend, cpa
FROM monthly_metrics
WHERE market = 'MX' AND month = '{prior_month}';

-- AU registrations YTD
SELECT SUM(regs) as ytd_regs
FROM monthly_metrics
WHERE market = 'AU' AND month >= '2026-02';

-- AU registrations for prior month only
SELECT regs as month_regs, spend, cpa
FROM monthly_metrics
WHERE market = 'AU' AND month = '{prior_month}';

-- Paid App installs (if tracked in DuckDB — check for 'Paid App' or 'PAID_APP' market)
SELECT SUM(regs) as ytd_installs
FROM monthly_metrics
WHERE market IN ('Paid App', 'PAID_APP', 'paid_app') AND month >= '2026-02';
```

**Pace calculation:**
```
months_elapsed = current_month_number - 2  (FY26 starts Feb)
months_total = 12
expected_pct = months_elapsed / months_total
actual_pct = ytd_actual / annual_target
pace_ratio = actual_pct / expected_pct

if pace_ratio >= 0.90: on-track
if pace_ratio >= 0.70: at-risk
if pace_ratio < 0.70: off-track
```

### Step 4: Assess Each Goal

For each goal, determine status using this framework:

**Registration goals (numeric):**
- Compare YTD actual vs expected pace (linear interpolation of annual target)
- Calculate month-over-month delta (acceleration or deceleration)
- Factor in seasonality if known (e.g., Q4 holiday lift)
- Status: on-track (≥90% of pace), at-risk (70-89%), off-track (<70%)

**Testing goals (milestone):**
- Count experiments launched vs target
- For 0% goals: flag time elapsed vs time remaining
- Q1 goals at 0% with Q1 ended = automatic off-track/red
- FY26 goals at 0% with >2 months elapsed = at-risk minimum

**Project goals (percentage):**
- Map to related tasks and subtask completion rates
- For H1 goals at 0% with H1 half over = at-risk minimum
- Check for blockers in Kiro_RW fields of related tasks

**Special cases:**
- Goals 7 & 8 (Brand LP Q1): Q1 FY26 ended Apr 2026. If still 0%, these are off-track/red. Recommend: close as missed and roll forward to Q2, or document what happened.
- Goal 1 (parent MX/AU regs): Derived from goals 2 + 3. Calculate combined progress.
- Goal 4 (parent MX+AU testing): Derived from goals 5 + 6. Count total experiments across both.
- Goal 12 (parent Paid App): Derived from goals 13 + 14.

### Step 5: Draft Status Updates

For each goal, draft a status update using this template:

```
**[Month] Update — [Goal Name]**

Status: [🟢 On Track / 🟡 At Risk / 🔴 Off Track]

Progress: [current] / [target] ([X]%)
Prior month: [last month's value] → [this month's value] (+/- delta)
Pace: [on-track/at-risk/off-track] — [X]% of target with [Y]% of time elapsed

What happened this month:
- [Completed task 1]
- [Completed task 2]
- [Key metric movement]

[For at-risk/off-track only:]
What's needed to get back on track:
- [Action 1]
- [Action 2]

[For testing goals:]
Experiments: [X] of [Y] launched
- [Experiment name]: [status]

Next month focus:
- [Planned action 1]
- [Planned action 2]
```

**Tone:** Honest. No spin. If a goal is behind, say so and say why. Richard's manager and skip-level can see these. Credibility comes from accuracy, not optimism.

### Step 6: Present to Richard for Review

Present all 14 drafted updates in a single review session:

1. Show summary table first:
```
| Goal | Current | Target | % | Status | Change |
|------|---------|--------|---|--------|--------|
```

2. Then show each draft, grouped by category:
   - Registration goals (2, 3, 1, 13)
   - Testing goals (5, 6, 7, 8, 4, 9, 14)
   - Project goals (10, 11, 12)

3. For each draft, ask: "Approve / Edit / Skip"

4. Collect all approved drafts before posting any.

**CRITICAL: Never auto-post. Always draft-first. Richard reviews every update before it goes to Asana.**

### Step 7: Post Approved Updates to Asana For each approved update, post using the Asana status update mechanism: ```
// Option A: If CreateStatusUpdateForObject is available
CreateStatusUpdateForObject( parent=goal_gid, title="[Month] Update", text=approved_draft_text, status_type="on_track" | "at_risk" | "off_track"
) // Option B: If only GetGoal read + manual update available
// Present the approved text and instruct Richard to paste into Asana goal
// Log: "Posted to goal [GID] — [status]" or "Manual post needed — draft saved"
``` After posting, update the goal's metric value if DuckDB provided a newer number:
```
// If the Asana MCP supports updating goal metrics:
UpdateGoal(goal_gid, current_number_value=new_value)
``` Log all posts to `~/shared/context/active/asana-audit-log.jsonl`:
```json
{"timestamp": "ISO8601", "tool": "CreateStatusUpdateForObject", "goal_gid": "GID", "status": "on_track|at_risk|off_track", "result": "success|manual_needed"}
``` ### Step 8: Update Tracking Files

After all updates are posted:
1. Update `rw-tracker.md` with: "Goal updates posted [date]: [X] on-track, [Y] at-risk, [Z] off-track"
2. Update `asana-command-center.md` → Richard's Goals table with refreshed current values and statuses
3. Note the date of last goal update for next month's trigger check

---

## Data Source Priority

When multiple sources have conflicting data, use this priority:

1. **DuckDB** (most authoritative for registration numbers — sourced from actual campaign data)
2. **Asana goal metric values** (may be stale if not updated recently)
3. **Completed task evidence** (qualitative — shows work done, not necessarily metric movement)
4. **rw-tracker.md / WBR data** (weekly snapshots, useful for trend)
5. **Slack signals** (context only — not authoritative for metrics)

If DuckDB is unavailable or empty for a metric, use Asana's `current_number_value` and note: "Source: Asana goal metric (last updated [date]). DuckDB data not available."

---

## Insufficient Data Handling

If the agent cannot assemble enough evidence to assess a goal:

1. Flag the goal as "⚠️ Insufficient Data"
2. List what's missing: "No DuckDB data for MX regs" or "No completed tasks found for this goal"
3. Draft a minimal update: "No update available — [missing data description]. Manual input needed."
4. Present to Richard with the gap — he may have context the agent doesn't.

---

## Goal Hierarchy (Parent-Child Relationships)

```
MX/AU paid search registrations (1213245014119128)  ← PARENT
├── MX registrations (1213204514049680)
└── AU registrations (1213204514049684)

MX + AU market testing (1213245014119125)  ← PARENT
├── MX tests (1213204514049688)
│   └── MX test 1: Brand LP (1213204514049706)  [Q1 FY26]
└── AU tests (1213204514049691)
    └── AU test 1: Brand LP (1213204514049694)  [Q1 FY26]

Globalized cross-market testing (1213245014119131)  ← STANDALONE PARENT

WW in-context email overlay (1213204514049667)  ← STANDALONE
PS redirect mapping (1213204514049671)  ← STANDALONE

Paid App (1213204514049810)  ← PARENT
├── Paid App Installs (1213204514049812)
└── Paid App Tests (1213204514049830)
```

**Update order:** Always update children first, then parents. Parent status is derived from children.

---

## Five Levels Alignment

| Goal Category | Five Level | Rationale |
|---------------|-----------|-----------|
| Registration goals (1-3, 13) | L1: Sharpen Yourself | Core metric delivery — proves competence |
| Testing goals (4-9, 14) | L2: Drive WW Testing | Test methodology ownership |
| Project goals (10-12) | L2: Drive WW Testing | Cross-market project execution |
| Goal update process itself | L5: Agentic Orchestration | Autonomous monthly workflow |

---

## Monthly Checklist (for agent self-audit)

- [ ] All 14 goals retrieved via GetGoal
- [ ] DuckDB queried for MX regs, AU regs, Paid App installs (or flagged unavailable)
- [ ] Completed tasks from prior month retrieved and mapped to goals
- [ ] Pace calculations done for all numeric goals
- [ ] Q1 goals checked for period expiry
- [ ] H1 goals checked for mid-period progress
- [ ] All 14 drafts written with honest assessment
- [ ] Drafts presented to Richard in grouped format
- [ ] Only approved drafts posted to Asana
- [ ] Audit log updated for all posts
- [ ] rw-tracker.md updated with summary
- [ ] asana-command-center.md goal table refreshed
