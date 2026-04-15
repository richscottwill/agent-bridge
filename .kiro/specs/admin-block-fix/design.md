# Admin Block Failure Bugfix Design

## Overview

The Admin block has produced zero completions since March 1, 2026. Two compounding failures cause this: (1) Admin is sequenced 4th/last in the daily block order (Sweep → Engine Room → Core → Admin), so it's never reached after cognitive energy is depleted; (2) 74% of admin-type tasks (budget, PO, R&O, invoice, spend) are either untagged (Routine_RW = null) or misrouted to non-Admin blocks, so even a properly sequenced Admin block would be mostly empty.

The fix reorders blocks to Sweep → Admin → Core → Engine Room (placing Admin in the 2nd position where it becomes a protected routine per Duhigg's habit loop — cue: Sweep complete, routine: Admin block, reward: clear queue before deep work), adds keyword-based routing for admin-type signals during AM-2 triage, normalizes 3 non-standard Routine_RW values, introduces a 3-day overdue auto-escalation from Admin to Sweep (single checkpoint in AM-2 only — per McKeown's Effortless principle of removing friction rather than building elaborate recovery mechanisms), enforces early-start due dates on Admin tasks (begin date = due_on - 7 business days so tasks surface a week before they're due), adds a 30-minute time bound on the Admin block to protect Core's flow window (Csikszentmihalyi), adds a concrete habit loop reward ("✅ Admin clear" confirmation after block completion per Duhigg), addresses Engine Room overcapacity via auto-demotion and task decomposition (22 open vs cap of 6), surfaces the 66 null-Routine_RW tasks for manual triage by Richard, and removes deprecated Microsoft To-Do references from hands.md.

## Glossary

- **Bug_Condition (C)**: The compound condition where Admin block sequencing (4th position) and routing failures (74% misrouted) prevent admin-type tasks from being completed
- **Property (P)**: Admin tasks are reached before cognitive depletion (2nd position), correctly routed via keyword detection, and escalated when overdue 3+ days
- **Preservation**: Sweep, Core, and Engine Room routing logic, existing Routine_RW enum values, the 4-block model, AM-1/AM-2/AM-3 hook structure, and all non-admin task flows remain unchanged
- **Block sequence**: The ordered list of execution blocks in hands.md that determines which category of work Richard tackles first each day. Current: Sweep → Engine Room → Core → Admin. Fixed: Sweep → Admin → Core → Engine Room. The reorder follows Cal Newport's principle of batching shallow work into a dedicated, bounded block, and Duhigg's habit loop principle of protecting the cue-routine-reward sequence
- **Routine_RW**: Asana custom field (GID: `1213608836755502`) that maps tasks to blocks. Enum values: Sweep (`1213608836755503`), Core Two (`1213608836755504`), Engine Room (`1213608836755505`), Admin (`1213608836755506`), Wiki (`1213924412583429`)
- **Signal-to-Routine mapping**: The table in am-triage.md and am-auto.md that determines which block a new signal is routed to during AM-2 triage
- **Admin-type keywords**: budget, PO, invoice, spend, R&O, reconciliation, actuals, forecast, compliance, purchase order — terms that indicate a task belongs in Admin regardless of how it was initially categorized
- **Deep work vs shallow work (Newport)**: Deep work is cognitively demanding, produces high value, and requires uninterrupted focus (Core block). Shallow work is logistical, necessary but low-cognitive-demand, and should be batched (Admin block). The block sequence should protect deep work by ensuring shallow work is completed in a bounded slot, not left as residual
- **System 1 / System 2 (Kahneman)**: System 1 is fast, automatic, effortless. System 2 is slow, deliberate, energy-intensive, and depletes through the day. Admin tasks require just enough System 2 attention that they can't run on autopilot — but the current sequence places them where System 2 is most depleted
- **Habit loop (Duhigg)**: Cue → Routine → Reward. The Admin block needs a reliable cue (Sweep completion), a bounded routine (process admin queue), and a reward (clear queue before deep work). The current system breaks this loop by placing Admin after deep work, where the cue never fires
- **Essentialism (McKeown)**: Design systems so the essential gets done by default. Admin is essential (teammates are blocked) but not strategic — it needs structural protection, not willpower
- **Flow (Csikszentmihalyi)**: Flow requires challenge-skill balance and uninterrupted focus. Admin doesn't produce flow but can interrupt it. Completing Admin before Core creates better conditions for flow during strategic work

## Bug Details

### Bug Condition

The bug manifests when Richard's daily execution reaches the Admin block. Because Admin is positioned 4th (last) in the block sequence, it is consistently skipped after Sweep, Engine Room, and Core consume available time and cognitive energy. Compounding this, the AM-2 triage protocol fails to route 74% of admin-type tasks to the Admin block — they remain untagged (Routine_RW = null, the largest category at 66 tasks) or are misrouted to Sweep or non-standard Routine_RW values.

**Formal Specification:**
```
FUNCTION isBugCondition(task)
  INPUT: task of type AsanaTask with fields {name, routine_rw, due_on, keywords}
  OUTPUT: boolean

  LET isAdminType := task.keywords INTERSECT {'budget', 'PO', 'invoice', 'spend', 'R&O',
         'reconciliation', 'actuals', 'forecast', 'compliance', 'purchase order'} IS NOT EMPTY

  LET isSequencingVictim := task.routine_rw == 'Admin' 
         AND blockPosition('Admin') == 4  -- last position
         AND task.completed == FALSE

  LET isMisrouted := isAdminType
         AND task.routine_rw NOT IN {'Admin', 'Admin (Wind-down)'}
         -- includes null, 'Sweep (Low-friction)', or any non-Admin value

  LET isNonStandard := task.routine_rw IN {'Sweep (Low-friction)', 
         'Admin (Wind-down)', 'Engine Room (Excel and Google ads)'}

  RETURN isSequencingVictim OR isMisrouted OR isNonStandard
END FUNCTION
```

### Examples

- **Sequencing victim**: "Paid App PO - Create Q2 + Amend Google PO" — correctly tagged Routine_RW = Admin, 1 day overdue, but Admin block never reached → 0 completions since March 1
- **Misrouted to Sweep**: "Provide Lorena Q2 expected spend for MX PO" — tagged Sweep (Low-friction), 10 days overdue, blocks Lorena's PO submission. Contains keyword "spend" + "PO" → should be Admin
- **Untagged (null)**: "R&O for MX/AU" — Routine_RW = null, no due date, blocks team budget planning. Contains keyword "R&O" → should be Admin with enforced due date
- **Untagged (null)**: "Raise PO for Q2 instead of increasing to FY" — Routine_RW = null, no due date. Contains keyword "PO" → should be Admin
- **Non-standard value**: "MBR callout" — tagged "Admin (Wind-down)", 12 days overdue, blocks AU reporting. Non-standard value fragments routing
- **Engine Room overcapacity**: 22 open tasks vs cap of 6 — structural overflow crowds all other blocks

## Expected Behavior

### Preservation Requirements

**Unchanged Behaviors:**
- Sweep block continues to handle quick unblocking (send, confirm, triage) with a cap of 5
- Core block continues to handle strategic work (test designs, frameworks, stakeholder docs) with a cap of 4
- Engine Room block continues to handle hands-on work (campaign builds, keyword changes, bids) with a cap of 6
- The 4-block model (Sweep, Core, Engine Room, Admin) is preserved — no new blocks introduced
- Existing Routine_RW enum values in Asana remain unchanged — no new enum options added
- AM-1 ingest (Slack scan, Asana sync, email scan) continues without disruption
- AM-3 brief generation continues to surface all block categories
- EOD-2 system refresh (daily reset, reconciliation, organ cascade) continues unchanged
- Tasks without Routine_RW continue to be treated as Backlog requiring triage
- Mouse/manual task management in Asana continues to work — all changes are to agent protocol files, not Asana configuration
- Wiki routing (Routine_RW = Wiki) is unaffected

**Scope:**
All tasks that do NOT match admin-type keywords and are NOT in the Admin block are completely unaffected by this fix. The block resequencing changes execution order but not routing logic for Sweep, Core, or Engine Room tasks.

## Theoretical Framework

The block resequencing and routing fixes are grounded in five frameworks from Richard's preferred authors:

- **Deep work / shallow work distinction (Cal Newport)**: Deep work requires sustained, undistracted System 2 attention (Kahneman). Shallow work — email, admin, logistics — is necessary but should be batched into dedicated blocks rather than scattered or left to fill remaining time. The block sequence should protect deep work (Core) by scheduling shallow work (Admin) in a deliberate, bounded slot rather than leaving it as the residual that never gets reached
- **Habit loop (Duhigg)**: Every routine has a cue, a routine, and a reward. The Admin block's cue (post-Sweep transition), routine (process admin queue), and reward (clear queue before deep work) must be structurally invariant. The current system breaks the loop by placing Admin after deep work, where the cue never fires
- **System 1 / System 2 (Kahneman)**: System 2 is effortful, energy-intensive, and depletes through the day. Admin tasks require just enough System 2 attention (checking numbers, confirming amounts) that they can't run on System 1 autopilot — but they're placed in the slot where System 2 is most depleted. Moving Admin earlier ensures System 2 capacity is available
- **Essentialism (McKeown)**: The essentialist designs systems so the essential gets done by default, not by heroic effort. Admin is essential (teammates are blocked without it) but not strategic — it needs structural protection, not willpower. "If you don't prioritize your life, someone else will"
- **Flow (Csikszentmihalyi)**: Flow requires challenge-skill balance and uninterrupted focus. Admin tasks don't produce flow — they interrupt it. Placing Admin before Core (deep work) means Richard enters Core with a clear queue and no lingering admin guilt, creating better conditions for flow state during strategic work

## Hypothesized Root Cause

Based on the quantitative evidence and protocol analysis, the root causes are:

1. **Block Sequencing Defect (hands.md)**: The Task List Structure table in hands.md lists blocks as Sweep → Core → Engine Room → Admin. The AM-3 brief renders blocks in this order. Richard's daily execution follows this sequence, placing Admin last where System 2 (Kahneman) is depleted and the habit loop (Duhigg) for Admin never fires — the cue (transition from prior block) is consumed by fatigue, not by the Admin routine. This is the primary structural cause of 0 completions.

2. **Signal-to-Routine Mapping Gap (am-triage.md, am-auto.md)**: The mapping table routes "Admin/budget/invoice/compliance" signals to Admin, but the keyword matching is too narrow. Tasks containing "PO", "spend", "R&O", "reconciliation", "actuals", "forecast" are not caught — they fall through to null (Backlog) or get manually tagged to Sweep. This explains why 17 of 23 admin-type tasks are misrouted.

3. **Non-Standard Routine_RW Values (Asana data)**: Three non-standard values exist in the Routine_RW field — "Sweep (Low-friction)", "Admin (Wind-down)", "Engine Room (Excel and Google ads)". These are the display names of the enum options in Asana (GIDs `1213608836755503`, `1213608836755506`, `1213608836755505` respectively). The parenthetical suffixes are cosmetic labels in Asana's UI, not routing errors in the protocol. However, the protocols reference canonical short names (Sweep, Admin, Engine Room) while Asana returns the full display names. Any string-matching logic must account for both forms.

4. **No Escalation Mechanism**: Neither am-triage.md nor eod-system-refresh.md contains logic to promote overdue Admin tasks to Sweep. The 7-day stale flag in AM-2 is a generic "do, delegate, or kill" prompt — not a structural escalation that moves the task to an earlier block.

5. **No Due Date Enforcement for Admin Tasks**: AM-2 triage creates tasks with Priority_RW = Today but does not enforce due dates on admin-type tasks. R&O for MX/AU and PAM R&O have no due dates, making them invisible to any time-based escalation or overdue detection.

6. **Engine Room Cap Violation**: Engine Room has 22 open tasks against a cap of 6. The cap check in AM-2 flags "lowest-priority for demotion" but doesn't auto-execute — it queues for Richard's approval, which gets deferred along with everything else.

## Correctness Properties

Property 1: Bug Condition - Admin Block Reaches Execution

_For any_ daily execution where the block sequence is applied, the Admin block SHALL execute in the 2nd position (after Sweep, before Core), ensuring admin-type tasks are reached while System 2 capacity (Kahneman) is still available and the habit loop (Duhigg) fires reliably — not in the depleted end-of-day slot where the cue-routine-reward chain is broken.

**Validates: Requirements 2.1, 2.2**

Property 2: Bug Condition - Admin-Type Tasks Correctly Routed

_For any_ incoming signal or untriaged task whose name or description contains admin-type keywords (budget, PO, invoice, spend, R&O, reconciliation, actuals, forecast, compliance, purchase order), the AM-2 triage protocol SHALL route it to Routine_RW = Admin with an enforced due date, rather than leaving it as null or routing to another block.

**Validates: Requirements 2.4, 2.6, 2.7**

Property 3: Bug Condition - Overdue Admin Tasks Escalate to Sweep

_For any_ Admin task that is overdue by 3 or more days, the system SHALL auto-escalate it by changing Routine_RW to Sweep for the next day's execution, ensuring it surfaces in the highest-priority block rather than waiting for the Admin block.

**Validates: Requirements 2.3, 2.5, 2.8**

Property 4: Preservation - Non-Admin Task Routing Unchanged

_For any_ task that does NOT match admin-type keywords and is NOT in the Admin block, the fixed routing logic SHALL produce the same Routine_RW assignment as the original logic, preserving all existing Sweep, Core, Engine Room, and Wiki routing behavior.

**Validates: Requirements 3.1, 3.2, 3.3, 3.6, 3.7**

Property 5: Preservation - Hook Structure and Existing Flows Unchanged

_For any_ AM-1/AM-2/AM-3/EOD-2 hook execution, the fixed protocols SHALL continue to perform all existing functions (Slack scan, Asana sync, email scan, enrichment, portfolio scan, brief generation, daily reset) without disruption from the block reordering or routing changes.

**Validates: Requirements 3.5, 3.8**

## Fix Implementation

### Changes Required

Assuming our root cause analysis is correct:

**File**: `~/shared/context/body/hands.md`

**Section**: Task List Structure

**Specific Changes**:
1. **Reorder block table**: Change from Sweep → Core → Engine Room → Admin to Sweep → Admin → Core → Engine Room. The table row order and emoji numbering must reflect the new execution sequence. This is the single highest-impact change — it moves Admin from position 4 (never reached) to position 2 (early-afternoon trough).

---

**File**: `~/shared/context/protocols/am-triage.md`

**Section**: Signal-to-Routine Mapping + new Admin Keyword Detection section

**Specific Changes**:
2. **Expand admin keyword detection**: Add a keyword-matching step before the Signal-to-Routine mapping table. When a signal's text matches any of: `budget`, `PO`, `purchase order`, `invoice`, `spend`, `R&O`, `reconciliation`, `actuals`, `forecast`, `compliance` — route to Admin regardless of other signal characteristics. This overrides the generic mapping.

3. **Add early-start due date enforcement for Admin tasks**: When AM-2 triage routes a task to Admin and the task has no due date, flag to Richard: "Admin task [name] has no due date — set one?" When a due date exists or is set, auto-set start_on = due_on - 7 business days so the task surfaces in the Admin block a full week before it's due. This shifts Admin from "do by deadline" to "start early" — ensuring budget confirmations and R&O submissions are worked on in advance, not at the last minute.

4. **Add 3-day overdue Admin escalation (AM-2 only)**: After the Bucket Cap Check, add an Admin Escalation Check: query all Admin tasks where days_overdue >= 3. For each, auto-execute Routine_RW change from Admin to Sweep. Update Kiro_RW: "M/D: Escalated to Sweep (3d+ overdue)." This is the ONLY escalation checkpoint — per McKeown's Effortless principle, a single simple check is better than triplicated logic across AM-2, AM-auto, and EOD. If Admin is in position 2 and routing is fixed, escalation should rarely fire.

5. **Add escalation marker to AM-3 brief**: When Admin tasks are escalated to Sweep, the AM-3 brief SHALL include them in the Sweep section with an ⚠️ ADMIN ESCALATION prefix, not just in the Admin section.

5b. **Add Admin block time bound (30 minutes)**: Add a note in am-triage.md that the Admin block is bounded to 30 minutes maximum. If tasks remain after 30 minutes, carry forward to tomorrow's Admin block — do NOT bleed into Core time. This protects the flow conditions (Csikszentmihalyi) for Core: clear goals, no interruptions, bounded challenge.

5c. **Add concrete habit loop reward**: After Admin block completes (all tasks done or 30-min bound reached), the AM-3 brief or Slack self-DM SHALL surface: "✅ Admin clear. [N] tasks done. Core block starts now." This is the immediate feedback Csikszentmihalyi requires for flow entry and the reward Duhigg requires for habit formation.

---

**File**: `~/shared/context/protocols/am-auto.md`

**Section**: Signal-to-Routine Mapping + Phase 3 enrichment

**Specific Changes**:
6. **Mirror keyword detection in AM-Backend**: Add the same admin keyword detection logic from am-triage.md to am-auto.md's Signal Routing section (Phase 2). This ensures autonomous signal processing also catches admin-type tasks.

**NOTE: Escalation logic is NOT mirrored in AM-auto or EOD.** Per McKeown's Effortless principle, the 3-day overdue escalation lives in AM-2 only. If Admin is in position 2 and routing is fixed, escalation should rarely fire. One simple checkpoint beats three redundant ones.

---

**File**: `~/shared/context/body/hands.md`

**Section**: Task List Structure (Microsoft To-Do)

**Specific Changes**:
7. **Remove Microsoft To-Do references**: Richard no longer uses Microsoft To-Do. Remove the "Microsoft To-Do" subtitle, the To-Do List IDs comment block, and any To-Do-specific language. The block structure is Asana-native via Routine_RW. This is subtraction before addition (McKeown).

---

**File**: `~/shared/context/protocols/am-auto.md` and `~/shared/context/protocols/am-triage.md`

**Section**: Engine Room cap enforcement

**Specific Changes**:
8. **Engine Room auto-demotion + task decomposition**: Change Engine Room cap enforcement from "propose demotion" to "auto-demote lowest-priority tasks beyond cap to Backlog, notify Richard." Additionally, when Engine Room tasks are large/complex BAU tasks, the AM hooks SHALL attempt to decompose them into smaller subtasks that can be piggybacked onto related work in other blocks. This ensures mandatory BAU work still gets through even when the parent task is demoted — the subtasks survive in the relevant block.

---

**File**: Asana tasks (via UpdateTask API)

**One-time data cleanup**:
9. **Normalize non-standard Routine_RW values**: The 3 non-standard values ("Sweep (Low-friction)", "Admin (Wind-down)", "Engine Room (Excel and Google ads)") are actually the canonical Asana enum display names. Verify that protocol string-matching handles both short names and full display names. If any tasks have been manually set to a value not in the enum (which would be impossible via Asana UI), flag them.

10. **Route untagged admin-type tasks**: For the 17 identified misrouted/untagged admin-type tasks, batch-update Routine_RW to Admin. Set start_on = due_on - 7 business days for those with due dates. For those missing due dates, flag to Richard for manual date setting.

10b. **Surface 66 null-Routine_RW tasks for manual triage**: Query all tasks with null Routine_RW and present the full list to Richard for manual triage. The agent does NOT auto-assign these — Richard decides which block each belongs in. This addresses the systemic triage gap (66 tasks = 66 unmade decisions per Kahneman's decision fatigue framework).

11. **Engine Room auto-demotion + decomposition**: For Engine Room's 22 tasks (cap: 6), auto-demote the 16 lowest-priority tasks to Backlog (notify Richard). For any demoted task that is BAU/mandatory, decompose into smaller subtasks and piggyback them onto related work in other blocks so the essential work still gets through.

## Testing Strategy

### Validation Approach

The testing strategy follows a two-phase approach: first, surface counterexamples that demonstrate the bug on unfixed code (protocols), then verify the fix works correctly and preserves existing behavior. Since this is a protocol/configuration bug (not a code bug), "testing" means validating protocol behavior through DuckDB queries and Asana state inspection.

### Exploratory Bug Condition Checking

**Goal**: Surface counterexamples that demonstrate the bug BEFORE implementing the fix. Confirm or refute the root cause analysis.

**Test Plan**: Query DuckDB and Asana to verify the bug conditions exist as hypothesized. Run these checks on the UNFIXED protocols to observe failures and confirm root cause.

**Test Cases**:
1. **Zero Admin completions**: Query `SELECT COUNT(*) FROM asana_tasks WHERE routine_rw LIKE '%Admin%' AND completed = TRUE AND completed_at >= '2026-03-01'` — expect 0 (will confirm sequencing failure)
2. **Misrouted admin-type tasks**: Query tasks with budget/PO/R&O/invoice/spend keywords where routine_rw != 'Admin' — expect 17+ results (will confirm routing failure)
3. **Null Routine_RW dominance**: Query `SELECT COUNT(*) FROM asana_tasks WHERE routine_rw IS NULL AND completed = FALSE` — expect 66 (will confirm triage gap)
4. **Engine Room overcapacity**: Query `SELECT COUNT(*) FROM asana_tasks WHERE routine_rw LIKE '%Engine Room%' AND completed = FALSE` — expect 22 (will confirm cap violation)
5. **Missing due dates on admin-type tasks**: Query admin-keyword tasks where due_on IS NULL — expect R&O for MX/AU, PAM R&O, and others

**Expected Counterexamples**:
- Admin completion rate = 0% since March 1 (sequencing failure confirmed)
- 17+ admin-type tasks with wrong or null Routine_RW (routing failure confirmed)
- Possible causes: block position (4th), narrow keyword matching, no escalation mechanism

### Fix Checking

**Goal**: Verify that for all inputs where the bug condition holds, the fixed protocols produce the expected behavior.

**Pseudocode:**
```
FOR ALL task WHERE isBugCondition(task) DO
  result := applyFixedProtocols(task)
  ASSERT expectedBehavior(result)
  -- Admin block is in position 2
  -- Admin-type keywords route to Admin
  -- Overdue 3+ days escalates to Sweep
  -- Due dates are enforced
END FOR
```

**Test Cases**:
1. **Block sequence verification**: Read hands.md after fix → verify block order is Sweep(1) → Admin(2) → Core(3) → Engine Room(4)
2. **Keyword routing verification**: Simulate AM-2 triage with signals containing "PO", "budget", "R&O", "invoice", "spend" → verify all route to Admin
3. **Escalation verification**: Query Admin tasks with days_overdue >= 3 after EOD-2 runs → verify Routine_RW changed to Sweep
4. **Due date enforcement**: Create Admin task without due date via AM-2 → verify due_on is auto-set to today + 5 business days
5. **Brief escalation marker**: Run AM-3 after escalation → verify ⚠️ ADMIN ESCALATION appears in Sweep section

### Preservation Checking

**Goal**: Verify that for all inputs where the bug condition does NOT hold, the fixed protocols produce the same result as the original protocols.

**Pseudocode:**
```
FOR ALL task WHERE NOT isBugCondition(task) DO
  ASSERT applyOriginalProtocols(task) = applyFixedProtocols(task)
END FOR
```

**Testing Approach**: Property-based testing is recommended for preservation checking because:
- It generates many task configurations automatically across the input domain
- It catches edge cases where routing changes might accidentally affect non-admin tasks
- It provides strong guarantees that Sweep, Core, and Engine Room behavior is unchanged

**Test Plan**: Observe behavior on UNFIXED protocols first for non-admin tasks, then verify identical behavior after fix.

**Test Cases**:
1. **Sweep routing preservation**: Verify "quick reply/send/confirm" signals still route to Sweep with cap of 5
2. **Core routing preservation**: Verify "strategic discussion/artifact/framework" signals still route to Core with cap of 4
3. **Engine Room routing preservation**: Verify "campaign/keyword/bid/spreadsheet" signals still route to Engine Room with cap of 6
4. **AM-1 ingest preservation**: Verify Slack scan, Asana sync, email scan produce identical output before and after fix
5. **EOD-2 daily reset preservation**: Verify Today → Urgent demotion still works for non-Admin tasks
6. **Wiki routing preservation**: Verify Wiki-tagged tasks are unaffected

### Unit Tests

- Verify block sequence order in hands.md matches Sweep → Admin → Core → Engine Room
- Verify admin keyword list is complete and case-insensitive
- Verify 3-day threshold is exactly 3 (not 2, not 4)
- Verify due date default is 5 business days (not calendar days)
- Verify escalation changes Routine_RW but preserves all other task fields
- Verify non-admin tasks with "budget" in unrelated context (e.g., "time budget for testing") are handled correctly — keyword matching should consider Routine_RW context

### Property-Based Tests

- Generate random task configurations (varying Routine_RW, keywords, due dates, overdue days) and verify: admin-type tasks always route to Admin, non-admin tasks never change routing, 3-day overdue always escalates, due dates always enforced
- Generate random signal types and verify: Signal-to-Routine mapping produces identical results for non-admin signals before and after fix
- Generate random block execution sequences and verify: Admin always executes in position 2

### Integration Tests

- Full AM-1 → AM-2 → AM-3 cycle with mixed admin and non-admin signals: verify correct routing, brief generation, and escalation markers
- Full EOD-2 cycle with overdue Admin tasks: verify escalation executes and Kiro_RW is updated
- One-time data cleanup: verify all 17 misrouted tasks are correctly re-routed and due dates set
- Engine Room triage: verify cap enforcement proposal is generated for 16 excess tasks
