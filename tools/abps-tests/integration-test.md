# ABPS AI Pipeline — End-to-End Integration Test

**Purpose:** Manual test procedure to validate the full ABPS AI pipeline from Intake through Active/Archive.
**Owner:** Richard Williams
**Last Updated:** 2026-04-03
**Traces:** Requirements 1–10 (all)

---

## Key GIDs Reference

| Resource | GID |
|----------|-----|
| ABPS AI - Content Project | `1213917352480610` |
| Richard (assignee) | `1212732742544167` |
| **Sections** | |
| Intake | `1213917352480612` |
| In Progress | `1213917923741223` |
| Review | `1213917923779848` |
| Active | `1213917968512184` |
| Archive | `1213917833240629` |
| **Custom Fields** | |
| Routine | `1213608836755502` |
| Priority_RW | `1212905889837829` |
| Kiro_RW | `1213915851848087` |
| Frequency | `1213921303350613` |
| Begin Date | `1213440376528542` |
| **Frequency Options** | |
| One-time | `1213921303350614` |
| Weekly | `1213921303350615` |
| Monthly | `1213921303350616` |
| Quarterly | `1213921303350617` |

---

## Pre-Test Setup

- [ ] Confirm ABPS AI - Content project exists and is accessible
- [ ] Confirm all 5 sections exist in the project

**Verify:**
```
GetProjectSections(project_gid="1213917352480610")
```
**Expected:** Returns sections: Intake, In Progress, Review, Active, Archive with GIDs matching the table above.

- [ ] Confirm Frequency custom field is attached to the project

**Verify:**
```
GetTasksFromProject(project_gid="1213917352480610", opt_fields="name,custom_fields.name,custom_fields.display_value")
```
**Expected:** Any returned task shows `Frequency` in its `custom_fields` array.

- [ ] Confirm `asana-command-center.md` has the `## ABPS AI Project` section with all GIDs recorded

**Verify:** Open `~/shared/context/active/asana-command-center.md` and confirm the ABPS AI Project section matches the GID table above.

**Requirements validated:** 1.1, 1.2, 1.3, 1.4, 1.5

---

## Test 1: Create a Test Task in Intake

### Step 1.1 — Create the task

Create a new task directly in Asana (manually or via API) in the Intake section:

```
CreateTask(
  name="Integration Test: AU Market Keyword Strategy Guide",
  notes="Create a comprehensive guide for AU market keyword strategy covering: negative keyword optimization, broad match expansion testing, and cross-market learnings from MX. This should help the team understand when to use each match type and how to evaluate keyword performance. Include recent Q1 2026 data.",
  project="1213917352480610",
  assignee="1212732742544167",
  start_on="",
  due_on=""
)
```

- [ ] Task created successfully
- [ ] Record the new task GID: `__________________`

### Step 1.2 — Verify task is in Intake section

```
GetTaskDetails(
  task_gid="<NEW_TASK_GID>",
  opt_fields="name,assignee.name,assignee.gid,memberships.section.name,memberships.section.gid,custom_fields.name,custom_fields.display_value,start_on,due_on,completed"
)
```

**Expected:**
- [ ] `assignee.gid` = `1212732742544167`
- [ ] Section = Intake (`1213917352480612`)
- [ ] `Routine` display_value = null/empty (untriaged)
- [ ] `Frequency` display_value = null/empty
- [ ] `start_on` = null (no Begin Date)
- [ ] `due_on` = null (no Due Date)
- [ ] `completed` = false

---

## Test 2: AM-2 Intake Triage

### Step 2.1 — Run AM-2 scan

Trigger the AM-2 hook (or manually invoke the triage logic). The agent should detect the new task as untriaged.

- [ ] AM-2 scan initiated

### Step 2.2 — Verify triage recommendations presented

The agent should present triage decisions for approval. Check that the agent recommends:

- [ ] A Routine bucket assignment (based on "keyword strategy guide" → likely a strategy or testing routine)
- [ ] A Priority_RW value
- [ ] A Frequency value (guide = likely "quarterly" or "one-time")
- [ ] A Work_Product type from {guide, reference, decision, playbook, analysis}
- [ ] A one-sentence scope statement

### Step 2.3 — Approve triage

- [ ] Richard approves the triage recommendations

### Step 2.4 — Verify field assignment

```
GetTaskDetails(
  task_gid="<NEW_TASK_GID>",
  opt_fields="name,custom_fields.name,custom_fields.display_value,start_on,due_on"
)
```

**Expected:**
- [ ] `Routine` is set (non-null)
- [ ] `Priority_RW` is set (non-null)
- [ ] `Frequency` is set to one of: weekly, monthly, quarterly, one-time
- [ ] `Kiro_RW` contains a date-stamped triage entry with: triage date, assigned fields, Work_Product type, scope statement

**Requirements validated:** 2.1, 2.2, 2.4, 2.5, 10.3

---

## Test 3: Date Defaults

### Step 3.1 — Verify date defaults applied

Since the test task was created with no Begin Date or Due Date:

```
GetTaskDetails(
  task_gid="<NEW_TASK_GID>",
  opt_fields="start_on,due_on,custom_fields.name,custom_fields.display_value"
)
```

**Expected:**
- [ ] `start_on` = today's date (YYYY-MM-DD format)
- [ ] `due_on` = today + 7 calendar days (YYYY-MM-DD format)
- [ ] `Kiro_RW` mentions that default dates were applied

**Requirements validated:** 2.3

---

## Test 4: Section Move (Post-Triage)

### Step 4.1 — Verify section move

Since Begin Date was set to today (which is <= today), the task should move to In Progress:

```
GetTaskDetails(
  task_gid="<NEW_TASK_GID>",
  opt_fields="memberships.section.name,memberships.section.gid"
)
```

**Expected:**
- [ ] Section = In Progress (`1213917923741223`)

### Step 4.2 — Verify research subtask created

```
GetSubtasksForTask(task_gid="<NEW_TASK_GID>")
```

**Expected:**
- [ ] A subtask exists named "📋 Research: Integration Test: AU Market Keyword Strategy Guide"
- [ ] Subtask is assigned to Richard (`1212732742544167`)
- [ ] Subtask `completed` = false

**Requirements validated:** 2.6, 2.7, 4.5, 7.5

---

## Test 5: Pipeline Stage 1 — Research (wiki-researcher)

### Step 5.1 — Verify research execution

The pipeline should initiate automatically after triage approval (task entered date window). Wait for the research stage to complete.

- [ ] Research stage initiated

### Step 5.2 — Verify research brief posted as pinned comment

```
GetStoriesForTask(task_gid="<NEW_TASK_GID>")
```

**Expected:**
- [ ] A pinned comment exists containing the research brief
- [ ] Comment includes source material, context from body organs, and relevant data
- [ ] Comment includes agent name and timestamp (stage transition log)

### Step 5.3 — Verify research subtask completed

```
GetSubtasksForTask(task_gid="<NEW_TASK_GID>")
```

**Expected:**
- [ ] "📋 Research: ..." subtask `completed` = true

### Step 5.4 — Verify Kiro_RW updated

```
GetTaskDetails(
  task_gid="<NEW_TASK_GID>",
  opt_fields="custom_fields.name,custom_fields.display_value"
)
```

**Expected:**
- [ ] `Kiro_RW` contains entry noting research stage started/completed

**Requirements validated:** 3.1 (Stage 1), 3.2, 3.7, 4.2, 7.2, 7.4

---

## Test 6: Pipeline Stage 2 — Draft (wiki-writer)

### Step 6.1 — Verify draft written to html_notes

```
GetTaskDetails(
  task_gid="<NEW_TASK_GID>",
  opt_fields="html_notes,memberships.section.name"
)
```

**Expected:**
- [ ] `html_notes` contains ~500 word draft
- [ ] Draft wrapped in `<body>` tags
- [ ] Contains `<strong>` title
- [ ] Contains "Executive Summary" or equivalent bold section
- [ ] Contains 3-5 bold-headed content sections
- [ ] Contains "Next Steps" section
- [ ] Only uses allowed tags: `body`, `strong`, `em`, `u`, `s`, `code`, `a`, `ul`, `ol`, `li`
- [ ] NO disallowed tags: `h1`-`h6`, `blockquote`, `pre`, `table`, `img`, `div`, `span`, `p`, `br`

### Step 6.2 — Verify draft subtask created and completed

```
GetSubtasksForTask(task_gid="<NEW_TASK_GID>")
```

**Expected:**
- [ ] Subtask "✏️ Draft: Integration Test: AU Market Keyword Strategy Guide" exists
- [ ] Subtask `completed` = true

### Step 6.3 — Verify section moved to Review

```
GetTaskDetails(
  task_gid="<NEW_TASK_GID>",
  opt_fields="memberships.section.name,memberships.section.gid"
)
```

**Expected:**
- [ ] Section = Review (`1213917923779848`)

### Step 6.4 — Verify stage transition comment

```
GetStoriesForTask(task_gid="<NEW_TASK_GID>")
```

**Expected:**
- [ ] Comment exists logging draft stage completion with agent name (wiki-writer) and timestamp

**Requirements validated:** 3.1 (Stage 2), 3.2, 3.3, 3.4, 6.1, 6.2, 6.4, 7.2, 7.5

---

## Test 7: Pipeline Stage 3 — Review (wiki-critic)

### Step 7.1 — Verify critic review posted

```
GetStoriesForTask(task_gid="<NEW_TASK_GID>")
```

**Expected:**
- [ ] Comment exists with 5-dimension scoring: usefulness, clarity, accuracy, dual-audience, economy
- [ ] Each dimension scored 1-10
- [ ] Average score calculated
- [ ] Comment includes agent name (wiki-critic) and timestamp

### Step 7.2 — Verify approval path (if score >= 8)

If the critic scored the draft >= 8 average:

```
GetSubtasksForTask(task_gid="<NEW_TASK_GID>")
```

**Expected:**
- [ ] Approval subtask exists: "✅ Approve: Integration Test: AU Market Keyword Strategy Guide"
- [ ] `resource_subtype` = "approval"
- [ ] Assigned to Richard (`1212732742544167`)
- [ ] `completed` = false (pending Richard's approval)

### Step 7.3 — Verify review subtask

**Expected:**
- [ ] Subtask "🔍 Review: Integration Test: AU Market Keyword Strategy Guide" exists
- [ ] Subtask `completed` = true

### Step 7.4 — (If score < 8) Verify revision loop

If the critic scored < 8:
- [ ] Revision notes posted as comment
- [ ] wiki-writer revises the draft
- [ ] wiki-critic re-reviews
- [ ] If 2 consecutive sub-8 scores: task flagged for Richard, no further iteration

**Requirements validated:** 3.1 (Stage 3), 3.2, 3.5, 3.6, 7.2, 10.7, 10.8

---

## Test 8: Pipeline Stage 4 — Approval

### Step 8.1 — Richard approves

Complete the approval subtask in Asana (mark it done):

```
UpdateTask(
  task_gid="<APPROVAL_SUBTASK_GID>",
  completed="true"
)
```

- [ ] Approval subtask marked complete

### Step 8.2 — Verify approval detected

On next AM-2 scan (or manual trigger), the agent should detect the completed approval:

```
GetSubtasksForTask(task_gid="<NEW_TASK_GID>")
```

**Expected:**
- [ ] Approval subtask `completed` = true
- [ ] `Kiro_RW` updated with approval status

**Requirements validated:** 3.1 (Stage 4), 7.1, 10.4

---

## Test 9: Pipeline Stage 5 — Expansion (wiki-writer)

### Step 9.1 — Verify expansion to ~2000 words

```
GetTaskDetails(
  task_gid="<NEW_TASK_GID>",
  opt_fields="html_notes,memberships.section.name,memberships.section.gid"
)
```

**Expected:**
- [ ] `html_notes` expanded to ~2000 words
- [ ] Contains: bold title, executive summary, context section, detailed analysis sections, recommendations, next steps with owners/dates
- [ ] Only allowed HTML tags used
- [ ] Any content Richard added before expansion is preserved (read-before-write)

### Step 9.2 — Verify section moved to Active

**Expected:**
- [ ] Section = Active (`1213917968512184`)

### Step 9.3 — Verify expansion comment

```
GetStoriesForTask(task_gid="<NEW_TASK_GID>")
```

**Expected:**
- [ ] Comment logging expansion with agent name (wiki-writer) and timestamp

**Requirements validated:** 3.1 (Stage 5), 3.2, 3.3, 6.3, 6.5, 7.5, 10.4, 10.5

---

## Test 10: Section Move Verification (Full Lifecycle)

### Step 10.1 — Verify complete section progression

Review the task's history to confirm it moved through all expected sections:

```
GetTaskStories(task_gid="<NEW_TASK_GID>")
```

**Expected section progression:**
- [ ] Intake → In Progress (after triage approval, Begin Date <= today)
- [ ] In Progress → Review (after wiki-writer completes ~500w draft)
- [ ] Review → Active (after Richard approves + wiki-writer expands to ~2000w)

Each section move should have a corresponding comment in the task's story feed.

**Requirements validated:** 7.5, 8.2

---

## Test 11: Audit Log Verification

### Step 11.1 — Check audit log entries

Open `~/shared/context/active/asana-audit-log.jsonl` and filter for the test task GID.

**Verify each write operation has a log entry:**

```bash
grep "<NEW_TASK_GID>" ~/shared/context/active/asana-audit-log.jsonl
```

**Expected entries (one per write operation):**

| # | tool | pipeline_agent | pipeline_stage | fields_modified | result |
|---|------|---------------|----------------|-----------------|--------|
| 1 | UpdateTask | wiki-editor | triage | Routine, Priority_RW, Frequency, Kiro_RW, start_on, due_on | success |
| 2 | CreateTask | wiki-editor | triage | (research subtask creation) | success |
| 3 | UpdateTask | wiki-editor | triage | assignee_section (move to In Progress) | success |
| 4 | CreateTaskStory | wiki-researcher | research | (pinned research brief) | success |
| 5 | UpdateTask | wiki-researcher | research | (complete research subtask) | success |
| 6 | UpdateTask | wiki-writer | draft | html_notes | success |
| 7 | CreateTask | wiki-writer | draft | (draft subtask creation) | success |
| 8 | UpdateTask | wiki-writer | draft | assignee_section (move to Review) | success |
| 9 | CreateTaskStory | wiki-critic | review | (review comment) | success |
| 10 | CreateTask | wiki-critic | review | (approval subtask creation) | success |
| 11 | UpdateTask | wiki-writer | expansion | html_notes | success |
| 12 | UpdateTask | wiki-writer | expansion | assignee_section (move to Active) | success |

**For each entry, verify:**
- [ ] `timestamp` is ISO 8601 format
- [ ] `tool` matches the Asana API tool used
- [ ] `task_gid` matches the test task
- [ ] `task_name` matches the test task name
- [ ] `project` = "ABPS_AI_Project"
- [ ] `pipeline_agent` identifies which wiki agent acted
- [ ] `pipeline_stage` identifies the pipeline stage
- [ ] `fields_modified` lists what changed
- [ ] `result` = "success" for all entries

**Requirements validated:** 9.3, 10.2

---

## Test 12: Recurring Task State Registration

### Step 12.1 — Check registration (non-one-time tasks)

If the test task's Frequency was set to weekly, monthly, or quarterly:

```bash
cat ~/shared/context/active/recurring-task-state.json | python3 -m json.tool | grep "abps_ai_<NEW_TASK_GID>"
```

**Expected:**
- [ ] Entry exists with key `abps_ai_<NEW_TASK_GID>`
- [ ] `cadence` matches the Frequency field value (weekly/monthly/quarterly)
- [ ] `last_run` = today's date (YYYY-MM-DD)
- [ ] `last_run_period` = correct period for today (e.g., "2026-W14" for weekly, "2026-04" for monthly, "2026-Q2" for quarterly)
- [ ] `description` = "ABPS AI: Integration Test: AU Market Keyword Strategy Guide — refresh work product"

### Step 12.2 — Check non-registration (one-time tasks)

If the test task's Frequency was set to one-time:

```bash
cat ~/shared/context/active/recurring-task-state.json | python3 -m json.tool | grep "abps_ai_<NEW_TASK_GID>"
```

**Expected:**
- [ ] NO entry exists for this task GID
- [ ] Task should be in Archive section and marked completed (see Test 13)

**Requirements validated:** 5.6, 9.2

---

## Test 13: One-Time Task Archival (if Frequency = one-time)

If the test task was triaged as one-time:

### Step 13.1 — Verify archival

```
GetTaskDetails(
  task_gid="<NEW_TASK_GID>",
  opt_fields="completed,memberships.section.name,memberships.section.gid"
)
```

**Expected:**
- [ ] Section = Archive (`1213917833240629`)
- [ ] `completed` = true

**Requirements validated:** 5.5, 8.3

---

## Test 14: Kiro_RW Entries at Each Stage

### Step 14.1 — Verify Kiro_RW contains entries for every modification

```
GetTaskDetails(
  task_gid="<NEW_TASK_GID>",
  opt_fields="custom_fields.name,custom_fields.display_value"
)
```

Read the `Kiro_RW` field value. It should contain date-stamped entries for:

- [ ] Triage: date, assigned fields, Work_Product type, scope statement
- [ ] Date defaults applied (if applicable)
- [ ] Pipeline: research started
- [ ] Pipeline: research completed
- [ ] Pipeline: draft started
- [ ] Pipeline: draft completed / moved to Review
- [ ] Pipeline: review score and outcome
- [ ] Pipeline: approved (after Richard approves)
- [ ] Pipeline: expansion completed / moved to Active
- [ ] Registration in recurring-task-state.json (if non-one-time)

**Note:** Kiro_RW has a ~500 char limit. Entries may be truncated with oldest removed. Verify the most recent entries are present.

**Requirements validated:** 2.4, 7.6, 8.5

---

## Test 15: AM-3 Brief Includes ABPS AI Status

### Step 15.1 — Trigger AM-3 brief

Run the AM-3 hook (or manually trigger brief generation).

### Step 15.2 — Verify ABPS AI section in brief

The daily brief should include an `abps_ai` section with:

- [ ] `intake_count` — number of tasks in Intake
- [ ] `in_progress` — tasks currently in pipeline
- [ ] `in_review` — tasks awaiting critic/approval
- [ ] `active_count` — number of Active tasks
- [ ] `archive_count` — number of Archived tasks
- [ ] Pipeline stages in progress (which tasks are at which stage)
- [ ] Upcoming tasks entering date window this week
- [ ] Overdue tasks (if any)
- [ ] Refresh tasks due this period (if any)

### Step 15.3 — Verify morning snapshot

```bash
cat ~/shared/context/active/asana-morning-snapshot.json | python3 -m json.tool
```

**Expected:**
- [ ] `abps_ai` key exists in the snapshot JSON
- [ ] Contains section counts and pipeline status

**Requirements validated:** 8.6, 9.4, 9.7

---

## Test 16: EOD-2 Reconciliation Includes ABPS AI

### Step 16.1 — Trigger EOD-2

Run the EOD-2 hook at end of day.

### Step 16.2 — Verify ABPS AI in EOD stats

- [ ] EOD-2 output includes ABPS task completions
- [ ] EOD-2 output includes pipeline progress summary
- [ ] `rw-tracker.md` daily stats include ABPS AI activity

**Requirements validated:** 9.5

---

## Test 17: Assignee Guardrail

### Step 17.1 — Create a task assigned to someone else

Create a task in the ABPS AI project assigned to a different user (or unassigned):

```
CreateTask(
  name="Guardrail Test: Wrong Assignee",
  notes="This task tests the assignee guardrail.",
  project="1213917352480610"
)
```

(Do NOT set assignee to Richard)

### Step 17.2 — Verify agent blocks writes

When AM-2 scans this task, the agent should:

- [ ] Detect that `assignee.gid` ≠ `1212732742544167`
- [ ] Block all write operations on this task
- [ ] Log with `result="blocked"` in audit log

**Verify:**
```bash
grep "Guardrail Test" ~/shared/context/active/asana-audit-log.jsonl
```

**Expected:**
- [ ] Entry with `result` = "blocked"
- [ ] Alert flagged in daily brief

### Step 17.3 — Clean up

Delete or reassign the guardrail test task.

**Requirements validated:** 10.1

---

## Test 18: Read-Before-Write Preservation

### Step 18.1 — Add content to a task manually

Before the agent writes/updates `html_notes`, manually add some content to the test task:

```
UpdateTask(
  task_gid="<NEW_TASK_GID>",
  html_notes="<body><strong>Richard's Note</strong> This is content I added manually that the agent must preserve.</body>"
)
```

### Step 18.2 — Trigger agent update

Trigger a refresh or pipeline stage that writes to `html_notes`.

### Step 18.3 — Verify preservation

```
GetTaskDetails(
  task_gid="<NEW_TASK_GID>",
  opt_fields="html_notes"
)
```

**Expected:**
- [ ] Richard's manually added content ("Richard's Note") is still present in `html_notes`
- [ ] Agent's new content is integrated around Richard's additions

**Requirements validated:** 6.5, 10.5

---

## Test Summary Checklist

| Test | Description | Requirements | Pass? |
|------|-------------|-------------|-------|
| 1 | Create test task in Intake | 1.1-1.5 | ☐ |
| 2 | AM-2 intake triage | 2.1, 2.2, 2.4, 2.5, 10.3 | ☐ |
| 3 | Date defaults | 2.3 | ☐ |
| 4 | Section move + research subtask | 2.6, 2.7, 4.5, 7.5 | ☐ |
| 5 | Research stage (wiki-researcher) | 3.1, 3.2, 3.7, 4.2, 7.2, 7.4 | ☐ |
| 6 | Draft stage (wiki-writer) | 3.1, 3.2, 3.3, 3.4, 6.1, 6.2, 6.4, 7.2, 7.5 | ☐ |
| 7 | Review stage (wiki-critic) | 3.1, 3.2, 3.5, 3.6, 7.2, 10.7, 10.8 | ☐ |
| 8 | Approval (Richard) | 3.1, 7.1, 10.4 | ☐ |
| 9 | Expansion (wiki-writer) | 3.1, 3.2, 3.3, 6.3, 6.5, 7.5, 10.4, 10.5 | ☐ |
| 10 | Section progression | 7.5, 8.2 | ☐ |
| 11 | Audit log entries | 9.3, 10.2 | ☐ |
| 12 | Recurring task state | 5.6, 9.2 | ☐ |
| 13 | One-time archival | 5.5, 8.3 | ☐ |
| 14 | Kiro_RW at each stage | 2.4, 7.6, 8.5 | ☐ |
| 15 | AM-3 brief includes ABPS | 8.6, 9.4, 9.7 | ☐ |
| 16 | EOD-2 includes ABPS | 9.5 | ☐ |
| 17 | Assignee guardrail | 10.1 | ☐ |
| 18 | Read-before-write | 6.5, 10.5 | ☐ |

---

## Notes

- Run tests sequentially — each test depends on the state created by previous tests (Tests 1-14 are a single pipeline run).
- Tests 15-18 can be run independently after the pipeline completes.
- For the one-time archival test (Test 13), you may want to create a second test task with Frequency=one-time if the first task was triaged as recurring.
- The audit log grep commands assume the task GID is unique in the log. If running multiple tests, filter by timestamp range as well.
- If any test fails, check `Kiro_RW` on the task and `asana-audit-log.jsonl` for error details before re-running.
