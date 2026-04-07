<!-- DOC-0177 | duck_id: intake-learnings-am2-enrichment-2026-04-04 -->
# Learnings — AM-2 Enrichment Session (2026-04-04)

## Field Naming Convention: _RW = Agent Auto-Write

Richard renamed all agent-managed fields to include `_RW` suffix. This is the structural signal for which fields the agent owns.

**Rule:** Any field containing `_RW` in its name is auto-write. No approval needed. Write on every task modification.

| Field | GID | Type |
|-------|-----|------|
| Routine_RW | `1213608836755502` | enum (Sweep, Core Two, Engine Room, Admin, Wiki) |
| Priority_RW | `1212905889837829` | enum (Today, Urgent, Not urgent) |
| Importance_RW | `1212905889837865` | enum (Important) |
| Begin-Date_RW | `1213440376528542` | date |
| Kiro_RW | `1213915851848087` | text |
| Next-action_RW | `1213921400039514` | text |

**No _RW fields should ever be empty on any incomplete task.** The agent fills them proactively without asking.

## Wiki Routine

Richard created a new Routine_RW option: **Wiki** (GID: `1213924412583429`). All ABPS AI Content document factory tasks use Wiki instead of Core Two. This separates content pipeline work from Richard's actual deep work.

## Enrichment Execution Lessons

1. **Don't cherry-pick.** When Richard says "fill all blanks," that means ALL tasks — My Tasks, portfolio projects, AND ABPS AI Content/Build. I kept missing tasks because I was doing partial passes.

2. **ABPS AI Content tasks are real tasks.** They show up in My Tasks view. They need _RW fields just like everything else. I initially treated them as "pipeline backlog that doesn't need enrichment" — wrong.

3. **Check every Routine bucket.** Richard sees tasks grouped by Routine_RW. If a task has no Routine_RW, it falls into "No value" — which is visible clutter. Every task needs a bucket.

4. **Kiro_RW format is M/D only.** Never YYYY-MM-DD. I kept writing the wrong format and had to fix it multiple times. Burn this in: `4/4: <text under 10 words>`.

5. **Batch efficiently.** When enriching 30+ tasks with the same pattern (Wiki + Not urgent + pipeline Kiro_RW + pipeline Next-action_RW), batch 10 at a time in parallel. Don't check each one individually first.

## Monthly Actuals Cadence

Richard set a recurring rule: Monthly confirm actuals due on the 5th of each month, unless it falls on a weekend (then next Monday). Current instance: 5/5 (Monday).

## Stale Task Decisions

- Flash topics (18d overdue): **Killed.** Cadence moved on.
- Source DE/IT/ES: **Renamed** (was "Source keywords for DE/IT/ES Apple account, and implement"). Apple accounts paused.
- PAM US PO (34d overdue): **Extended to 4/11.** Still relevant. Added note: check Google + Apple Q2 PO approved.

## Cross-Reference: asana-command-center.md

All field name references in asana-command-center.md were updated to match the new _RW names. 16 string replacements across tables, inherited field lists, protocol sections, and the task audit. Wiki option GID added to Routine_RW enum listing.

## For Future AM-2 Runs

- On every enrichment pass, scan ALL 97 incomplete tasks — not just the ones that look like they need it.
- Content tasks default to: Routine_RW=Wiki, Priority_RW=Not urgent, Kiro_RW="4/D: Content. [name]. [level]. Pipeline.", Next-action_RW="Await wiki-editor triage for pipeline entry".
- Build tasks default to: Routine_RW=Core Two, Priority_RW=Not urgent, with task-specific Kiro_RW and Next-action_RW.
- Context/pinned tasks (📌) already have fields from earlier enrichment — skip unless blank.

## Session Log Entry

[2026-04-04] Topic: Crystallize learnings from full AM-2 enrichment marathon | Actions: Created learnings-am2-enrichment-2026-04-04.md in intake/ documenting: _RW naming convention (6 fields, all auto-write), Wiki Routine_RW option (GID 1213924412583429), enrichment execution lessons (don't cherry-pick, scan all 97 tasks, M/D format only, batch 10 at a time), monthly actuals cadence (5th unless weekend), stale task decisions, command center update summary, and future AM-2 defaults for Content/Build/Context tasks. | Decisions: This file feeds the next intake cycle to update organs (device.md for recurring rules, hands.md for task patterns, heart.md for experiment learnings).
