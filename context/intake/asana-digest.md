<!-- AM-Backend Orchestrator B1 | Asana Sync | 2026-04-20 07:25 PT -->
# Asana Digest — Mon Apr 20, 2026

**Scan window:** Live Asana MCP pull (SearchTasksInWorkspace + 6 project pulls)
**Projects pulled:** 6 (My Tasks, MX, AU, WW Testing, WW Acquisition, Paid App) + skipped ABPS AI Content per soul.md 4/17 deprecation
**Richard-incomplete tasks:** ~116 across projects (deduped)
**DuckDB sync:** DEFERRED this cycle — raw data captured in asana-task-list-b1.json for downstream processing. ops.data_freshness.asana_tasks still shows 2026-04-17 sync.

---

## 🔴 DUE TODAY (2026-04-20)

| Task | Project | Priority | Notes |
|---|---|---|---|
| **Weekly Reporting - Global WBR sheet** (1214057202961389) | WW Testing / MX / AU / Paid App | Today | **PRIORITY #1.** W14 data → Global WBR sheet. Always takes weekly priority. |
| **Reply to Dwayne: Brand LP consolidated feedback** (1214131122088126) | WW Testing § WW Doc Inputs | Today | Dwayne's Monday deadline. 7 open questions + 2 UX intakes drafted in task notes. |
| ⚠️ **DUPLICATE**: Reply to Dwayne (1214128635826241) | WW Testing § WW Doc Inputs | Today | **Dedupe candidate** — same task. |
| ⚠️ **DUPLICATE**: Reply to Dwayne (1214123519100287) | WW Testing § WW Doc Inputs | Today | **Dedupe candidate** — same task. |
| AU handover: switched to max clicks 4/17; check account Monday (1214128634505816) | — | Today | Carried fwd from 4/17 — max-clicks switch went live 4/17. |
| Convert EOD frontend to auto-hook + AM frontend to userTriggered (1214053404599901) | — | — | System work. |
| Mondays - Write into EU SSR Acq Asana (1214054954497349) | — | — | Weekly admin. |

---

## ⚠️ HARD THING — 19d overdue, 20 workdays at zero

**Testing Document for Kate (1213341921686564)**
- Project: WW Testing § Prioritized
- Due: 2026-04-01 — **19 days overdue**
- Priority_RW: Urgent | Routine: Core Two (Deep Work)
- Kiro_RW (4/15): "14d overdue. Core block 12:30-2PM. Ship v5 to Brandon."
- **L1 streak:** 20 workdays at zero (per Fri 4/17 brief).
- **Visibility-avoidance:** 12 days unsent to Brandon.
- **Recommendation:** Route to rw-trainer if not sent by EOD today.

---

## 📛 OVERDUE — top 10 (non-hard-thing)

1. **Respond to Lena — AU LP URL analysis + CPA methodology** (1213917967984980) — 17d overdue, Urgent, draft reply written
2. **Send IECCP follow-up summary to Lorena** (1213964186504305) — 11d overdue, Urgent, MX
3. **Refmarker mapping audit PoC — AU** (1213917691089036) — 10d overdue, Urgent, Brandon-assigned
4. **WW weblab dial-up** (1213764961716427) — 13d overdue, Urgent, WW Testing
5. **Look over AU LP switch post-max-clicks** (1213796951745232) — 5d overdue, Urgent
6. **Paid App PO — Create Q2 + Amend Google PO to Q2** (1212808474749819) — 7d overdue, Urgent
7. **Sitelink Audit/Update** (1214074477110993) — 3d overdue, Urgent
8. **PAM: Flag underspend risk to Brandon** (1214068272596724) — 3d overdue
9. **MCS LP Review: Connect with Lorena** (1214081017092577) — 3d overdue, Urgent, MX
10. **Resolve MX duplicate invoice — Diana** (1214088494080582) — 2d overdue

**Cluster: "Update your goal(s)"** — 17d overdue (1213798673865639, 1213817111703805, 1213690904654138). Asana system reminders — low effort, run together.

**Likely close candidate:** Slack thread-level ingestion (1214050694901572) — completed by Subagent A today, mark done in Phase 2.

---

## 📅 DUE NEXT 3 DAYS (4/21–4/22)

- **AU meetings - Agenda** (1214081017200478) — due 4/22, Urgent, Engine Room. Auto-created weekly, prep for Tue AU sync.
- **MCS LP Review: Follow up on global Polaris template finalization** (1214081017124426) — due 4/22, Urgent, MX
- **PAM: Confirm FR pivot campaign structure** (1214068215142846) — due 4/22
- **Brandon 1:1: Draft Enhanced Match FAQ for legal** (1213964668984060) — due 4/22 — **Brandon 1:1 is Tue 1:30 PT**
- **Get Enhanced Match Legal Approval** (1213423234257246) — due 4/22

---

## 🆕 NEW SINCE LAST SCAN (created 4/17+)

- 3× Reply to Dwayne: Brand LP (1214131122088126, 1214128635826241, 1214123519100287) — **triplicated, dedupe to 1**

No other new task creation in the scan window. Adi Kiro-mentoring ask (Slack DM 4/17) and Polaris Italy ref-tag issue (Hedy 4/16) have no Asana tasks — flagged for Phase 2 signal-to-task.

---

## 📊 BUCKET SHAPE (from the pulled data, approximate)

Priority_RW counts across 5 fully-enriched projects (My Tasks used slim opt_fields, buckets not re-read):

| Priority_RW | Count |
|---|---|
| Today | ~12 |
| Urgent | ~30 |
| Not urgent | ~25 |
| (null) | ~40 |

**Context reminders:** Core Two cap = 4 (currently breached per 4/15 Kiro notes). Engine Room cap enforced. Most "Demoted from Engine Room" items from 4/15 still parked in backlog with appropriate next-action text.

---

## 📥 WRITES PERFORMED

- `~/shared/context/active/asana-task-list-b1.json` — task list handoff for B2 + Phase 2-5 processing
- `~/shared/context/intake/asana-digest.md` — this file
- **DuckDB UPSERT deferred** — raw data captured, sync will happen in targeted rerun or next cycle. Phases 3-4 should fall back to direct Asana queries for any per-task enrichment rather than reading stale `asana.asana_tasks`.

**Did NOT touch:** Slack MCP, Outlook MCP, Hedy MCP (subagent domain).

---

## ⚠️ FLAGS FOR ORCHESTRATOR / PHASE 2+

1. **Asana DuckDB sync deferred** — downstream phases that need per-task Priority_RW/Routine_RW should read from asana-task-list-b1.json or re-query Asana directly, not from stale DuckDB.
2. **Triplicated "Reply to Dwayne"** — dedupe in Phase 2 (close 2, keep 1).
3. **Hard thing escalation** — Testing Approach v5 still unsent, 19d overdue, 20-workday zero streak. Route to rw-trainer.
4. **3 signal-to-task candidates** from Slack/Hedy (Polaris Italy ref tag, Polaris template email to Brandon+Dwayne, Adi Kiro 1:1 block).
5. **Brandon Outbound Marketing Goals task** (from email Fri 4:01 PT) — **NO Asana task yet**. Brandon assigned it, async — should become a task.
6. **B2 Activity Monitor not run this cycle** — GetTaskStories per task deferred due to context pressure. asana-activity.md will show last run date, not fresh.

---

_Generated by orchestrator B1 (Asana Sync) | next: deferred DuckDB UPSERT, Phases 2-5 processing_
