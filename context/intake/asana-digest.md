# Asana Digest — April 16, 2026

## ⚠️ Sync Limitation
**Partial sync only.** The Asana MCP server could not be called from the subagent context (ESD proxy requires Kiro runtime MCP client). DuckDB data is from the April 15 sync (last synced 2026-04-15T13:52:36Z — 24h stale). The parent agent should run a fresh Asana pull via SearchTasksInWorkspace + GetTasksFromProject and UPSERT into DuckDB to complete the sync.

## Summary
- Total active incomplete tasks (DuckDB): 105
- Soft-deleted: 63
- Due today (Apr 16): 2
  - Deep Dive: Year-One Optimization one-pager | Core | Today
  - Verify IT tax fix — check closed invoices + reissued ones | Admin | Today
- Newly overdue (from yesterday): 3
  - Look over AU landing page switch | AU | Engine Room | Today → 1d overdue
  - MX Automotive page | MX | Engine Room | Today → 1d overdue
  - Prep for MX LP optimization call | Sweep | Today → 1d overdue
- Overdue 3+ days: 4
  - Paid App (workstream) | 16d overdue | Engine Room | Urgent
  - Testing Document for Kate | 15d overdue | Core | Urgent — THE HARD THING
  - WW weblab dial-up (Richard) | 9d overdue | Core | Urgent
  - Paid App PO — Create Q2 + Amend Google PO to Q2 | 3d overdue | Sweep | Urgent

## By Block (Routine_RW)
### 🧹 Sweep (3/5 cap)
- Paid App PO — Create Q2 + Amend Google PO to Q2 | due: 4/13 ⚠️ 3d OVERDUE | Urgent
- Prep for MX LP optimization call | due: 4/15 ⚠️ 1d OVERDUE | Today
- Bi-monthly Flash | due: 5/21 | Not urgent

### 📋 Admin (3/3 cap) — AT CAP
- Verify IT tax fix — check closed invoices + reissued ones | due: 4/16 | Today
- Cross-marketing Refmarker audit | due: 4/30 | Urgent
- Monthly - Confirm actual budgets | due: 5/5 | Urgent

### 🎯 Core Two (10/4 cap) ⚠️ OVER CAP (+6)
- Testing Document for Kate | due: 4/1 ⚠️ 15d OVERDUE | Urgent — THE HARD THING
- Deep Dive: Year-One Optimization one-pager | due: 4/16 | Today
- WW weblab dial-up (Richard) | due: 4/7 ⚠️ 9d OVERDUE | Urgent
- Email overlay WW rollout/testing | due: 4/18 | Urgent
- AB Customer Redirect | due: none | Urgent
- WW keyword gap fill based on market-level ASINs | due: none | Urgent
- F90 | due: 4/30 | Not urgent
- Promo Test | due: none | Not urgent
- AppsFlyer setup (tentative date) | due: 7/1 | Not urgent
- 📋 Paid App — Project Context (Kiro) | pinned reference

### ⚙️ Engine Room (5/6 cap)
- Paid App (workstream) | due: 3/31 ⚠️ 16d OVERDUE | Urgent
- Look over AU landing page switch | due: 4/15 ⚠️ 1d OVERDUE | Today
- MX Automotive page | due: 4/15 ⚠️ 1d OVERDUE | Today
- Weekly Reporting - Global WBR sheet | due: 4/20 | Not urgent
- Create campaign for new vs. all | due: none | Not urgent

### 📦 Backlog (84 tasks)
- 84 tasks without Routine_RW assignment (wiki articles, tools, recurring items, context docs)

## Coherence Alerts (10 issues)
1. ⚠️ **hands.md stale reference**: "Lorena Q2 expected spend" — task is soft-deleted in DuckDB
2. ⚠️ **Overdue 3+ days**: Paid App (16d), Testing Document for Kate (15d), WW weblab dial-up (9d), Paid App PO (3d)
3. ⚠️ **Empty projects**: WW Acquisition (0 tasks), ABPS AI (0 tasks) — possible sync gap
4. ⚠️ **Over cap**: Core at 10/4 — needs triage (6 tasks over cap)
5. ⚠️ **Enrichment gaps**: 46 tasks missing Kiro_RW, 47 tasks missing Next_Action

## Schema Drift
No schema changes detected today.

## Snapshot
- Daily snapshot for 2026-04-16: 105 rows (carried from yesterday's data)
- Previous snapshots: 2026-04-15 (168 rows), 2026-04-14 (100 rows), 2026-04-13 (116 rows)

## Action Items for Parent Agent
The following steps require Asana MCP access (not available to subagent):

1. **Fresh Asana Pull**: Call `SearchTasksInWorkspace(assignee_any="1212732742544167", completed=false, sort_by=due_date)` and `GetTaskDetails` for each task with full opt_fields
2. **Project Pulls**: Call `GetTasksFromProject` for each portfolio project (My Tasks, ABPS AI Content, AU, MX, WW Testing, WW Acquisition, Paid App)
3. **UPSERT**: Merge fresh data into `asana.asana_tasks` using the UPSERT SQL from the sync protocol
4. **Soft-Delete**: Mark tasks in DuckDB not in the fresh pull
5. **Re-snapshot**: Update `asana.asana_task_history` for today with fresh data

---
Synced: 2026-04-16T14:20:00Z (DuckDB-only, stale Asana data from 4/15)
Source: DuckDB asana.asana_tasks (105 active incomplete) — NO fresh Asana pull
Limitation: Asana MCP ESD proxy not accessible from subagent context
