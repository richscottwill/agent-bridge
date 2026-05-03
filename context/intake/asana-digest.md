# Asana Digest — 2026-05-03 13:32 UTC

**Scope:** B1 partial sync (orchestrator-side, post-schema-fix run).
**Total active tasks:** 82 (82 incomplete, 0 completed today).
**Schema drift:** AU + MX standalone projects confirmed archived/consolidated into ABIX. Registry patched in `asana-duckdb-sync.md`, `am-backend-parallel.md`, `asana-command-center.md`. Logged to `asana.schema_changes`.

## Bucket distribution (Richard-assigned)

| Bucket | Count | Cap | Over? |
|---|---|---|---|
| Engine Room | 12 | 6 | ⚠️ **6 over** |
| Core | 10 | 4 | ⚠️ **6 over** |
| Admin | 6 | 3 | ⚠️ **3 over** |
| Sweep | 2 | 5 | OK |
| Wiki | 0 | — | — |
| No routine | 36 | — | ⚠️ routing gap |

**Bucket caps violated.** 36 tasks have no Routine_RW — either need triage or are pinned-context tasks. Phase 2C will queue demotion proposals.

## Priority=Today but no Routine_RW (triage queue)
Auto-flagged during Phase 2. These need Richard to pick a bucket or demote.

## Overdue tasks (20 shown, 16 total past-due)

| Days OD | Name | Project | Priority | Routine |
|---|---|---|---|---|
| 39 | Make changes to AU/MX/PAM for the week | My Tasks | — | — |
| 33 | Paid App | WW Testing | Urgent | Engine Room |
| 27 | Reply to Brandon — PAM budget needs assessment | My Tasks | — | — |
| 26 | WW weblab dial-up (Richard) | WW Testing | Urgent | Core |
| 26 | Get Enhanced Match details | My Tasks | — | — |
| 24 | Deep Dive: Add IECCP FAQ to new account playbook | My Tasks | — | — |
| 24 | Deep Dive: Finalize market expansion playbook | My Tasks | — | — |
| 24 | Brandon 1:1: Set up automated monthly ASP reminders | My Tasks | — | — |
| 23 | Monthly: Individual Goals update | My Tasks | — | — |
| 20 | Paid App PO — Create Q2 + Amend Google PO to Q2 | Paid App | Urgent | Sweep |
| 16 | MCS LP Review: Connect with Lorena on paid social/PS synergy | MX (stale label) | Urgent | — |
| 16 | Sitelink Audit/Update | WW Testing | Urgent | — |
| 16 | PAM: Flag underspend risk to Brandon | My Tasks | — | — |
| 16 | MX Experiments ending 4/30, check sooner for trend | My Tasks | — | — |
| 15 | Email overlay WW rollout/testing | WW Testing | Urgent | Core |
| 15 | Resolve MX duplicate invoice — Diana ($56K, PO Q1) | My Tasks | — | — |
| 15 | PAM: Check US/EU spend pacing vs Q2 budget | My Tasks | — | — |
| 13 | AU handover: switched to max clicks 4/17 | My Tasks | Urgent | — |
| 11 | Brandon 1:1: Draft Enhanced Match FAQ for legal | My Tasks | — | — |
| 5 | MX/AU confirm budgets | My Tasks | — | — |

## High-signal tasks due next 7 days (5/3 – 5/10)

| Due | Name | Priority |
|---|---|---|
| 5/4 | Google Ads MCC SSO admin — confirm ownership by May 4 | Today |
| 5/4 | Convert promptSubmit hooks to userTriggered | Today |
| 5/4 | Follow up with Vijeth — /cp/auto-shop ref-tag overwrite fix | Today |
| 5/5 | WW Kw URL inclusion | Urgent |
| 5/5 | GenBI keyword-registration stitching fix with Mukesh (pre-AU handoff) | Urgent |
| 5/5 | Update Kingpin for MX | Urgent |
| 5/5 | Monthly - Confirm actual budgets | Urgent |
| 5/5 | Update on app extension for regular MX meetings | Urgent |
| 5/6 | WW Kw URL inclusion | Urgent |
| 5/6 | Brand LP AU/MX test design — non-weblab MCS vs Reg Start (HARD THING) | Urgent |
| 5/7 | Baloo Early Access — PS feedback consolidation | — |
| 5/8 | Resolve am-auto.md vs am-backend-parallel.md duplication | Not urgent |

## New tasks inserted to DuckDB this run (8)

Created since last full sync (Apr 29):
- WW Kw URL inclusion
- Move LR Negative to NA MCC
- Clarify CAT vs MCS email overlay status for Outbound Marketing Goals
- Baloo Early Access — PS feedback consolidation + follow-ups
- Resolve am-auto.md vs am-backend-parallel.md duplication
- Convert promptSubmit hooks to userTriggered
- MotherDuck sync audit — autoresearch schema frozen since 2026-04-17
- MPE US baseline — Option 2: add YoY-acceleration regressor

## B1 → B2 handoff

Task list written to `asana-task-list-b1.json` for B2 activity-monitor consumption.
