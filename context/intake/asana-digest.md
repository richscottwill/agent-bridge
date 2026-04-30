# Asana Digest — 2026-04-30 (W18, Thursday)

**Sync run:** 2026-04-30 ~12:05 UTC | **Source:** SearchTasksInWorkspace + 4/6 portfolio pulls
**Total incomplete tasks:** 79 | **Today:** 27 | **Urgent:** 18 | **Not urgent/Backlog:** 34
**Overdue:** ~22 tasks (many flagged for kill-or-revive at today's Brandon 1:1)

---

## ⚠️ SCHEMA DRIFT — 2 project GIDs stale

Two portfolio project GIDs returned `424 Not a recognized ID` today:

- **MX** — `1212775592612917` (per asana-command-center.md)
- **AU** — `1212762061512767`

These were likely archived, merged, or renamed. **Incomplete tasks for both markets still appear in the SearchTasksInWorkspace results** (Richard is assignee), so the sync is not data-incomplete — we just can't enumerate by project. Action: run `AsanaSearch(query="AU Paid Search", resource_type="project")` and `AsanaSearch(query="MX", resource_type="project")` to re-discover; then update `shared/context/active/asana-command-center.md` + `shared/context/protocols/asana-duckdb-sync.md` portfolio tables. This is Engine Room cleanup — not urgent, but log in Asana as a sync-fix task.

---

## TOP — Due today (Thu 4/30)

1. **OP1 app acquisition projections — Peter sync Wed 4/30 2-3pm** (`1214384590122162`) — Due TODAY. Pull CPI + install-rate by market (DE/ES efficient), prep projections for 2-3pm Peter sync.
2. **MX Experiments ending 4/30** (`1214044682239823`) — 11d OD. Check MX Polaris Beauty+Auto experiment trend, extend test to 6 weeks if needed.
3. **MX Polaris NB LP Test (Beauty+Auto)** (`1214044682239817`) — Due 4/30. Reuse mechanic framework from Brand LP AU/MX test design.
4. **Cross-marketing Refmarker audit** (`1214044682239803`) — Due 4/30. Pull refmarker mapping from Google Ads for cross-marketing campaigns.
5. **DDD walkthrough with team** (`1214074477111007`) — 12d OD, rescheduled to today. Walk team through Polaris alt-measurement mechanic + MX NB LP test (15 min).

## Brandon 1:1 agenda (1:30pm PT today)

- **Polaris Br-pages QA consolidation** — new from Wed (Brandon DM + ab-paid-search-global thread). Richard is sole consolidator; needs feedback doc + timelines. See slack-digest.md.
- **PAM budget kill-or-revive** (`1213959904341162`) — 23d OD. Is "Extra $ for PAM" question still live or overtaken by Paid App PO motion?
- **Email overlay WW status** (`1213125740755931` + `1214137998394047` + `1214351597615320`) — Brandon ask from 4/17, 13d unaddressed. Clarify CAT vs MCS overlay status for Outbound Marketing Goals.
- **Enhanced Match FAQ for legal** (`1213964668984060`) — draft Enhanced Match FAQ for legal, building on LiveRamp context. Bundle with `1213875146955582` (Get EM details).
- **Kingpin MX kill decision** — 35d blocked on Andes data. Kill or escalate to ABMA leadership?

## High-signal due-this-week

- **Brand LP AU/MX test design — alt measurement (non-weblab)** (`1214330104198712`) — Due Tue 5/5. Richard owns non-weblab measurement for AU/MX Brand LP since these markets go to reg start. Decide mechanic (pre/post Adobe? holdout? staggered region ramp?) and document in SIM MCS-3004.
- **Adobe Analytics cross-check — MX Polaris Beauty LP test** (`1214365254391847`) — Due Fri 5/1.
- **Confirm /cp/beauty custom ref tags firing** (`1214372109571389`) — Due Fri 5/1. Ping Alex VanDerStuyf (MCS).
- **Build Adobe dashboard template for MCS-2553** (`1214153596141526`) — Due Sat 5/2.
- **ie%CCP calc — insert MX spend/regs** (`1213983077428492`) — Due Thu 5/1.
- **MBR callout** (`1213983342210449`) — Due Sat 5/2.
- **Send AU team invoice for prev month** (`1213917691068688`) — Due Sat 5/2. Monthly recurring from Yun reminder.
- **Google Ads MCC SSO admin** (`1214330091433878`) — Due Mon 5/4. SSO enforcement launches 5/4; confirm MCC ownership + adopt Teams workflow.

## Kill-or-revive / duplicate cleanup candidates

- **"It's time to update your goal(s)"** (`1214216689942612`) — 6d OD, DUPLICATE of `1213690904654138` (Monthly Individual Goals update). Keep one, close the other.
- **Email overlay WW rollout/testing** (`1213125740755931`) — Core Two, due 4/24, Brandon ask still stale. Surface at 1:1.
- **AU: check genbi campaign data** — completed 4/21 per prior snapshot; confirm closed.
- **Initial Testing** (`1213278917849558`) — generic name, completed 4/28; name unclear.
- **Look into ABMX Registration and Verification Enhancement** (`1214372021755042`) — Due 4/29, 1d OD, unclear next-action.

## Over-cap buckets (Routine_RW distribution)

| Routine | Active Count | Cap | Status |
|---------|-------------|-----|--------|
| Sweep | ~18 | 5 | OVER CAP (3.6x) |
| Core Two | ~10 | 4 | OVER CAP (2.5x) |
| Engine Room | ~18 | 6 | OVER CAP (3x) |
| Admin | ~14 | 3 | OVER CAP (4.6x) |
| Wiki | ~3 | — | within norms |
| No routine set | ~16 | — | triage needed |

**Every bucket is over cap.** This is structural — not one missed demotion pass. Richard needs a 30-min "WIP triage" block this week before adding new work.

## Coherence flags

- 2 stale project GIDs (MX + AU) per schema drift section above.
- PAM-related tasks (`1213959904341162`, `1214068215114017`, `1214068272596724`, `1212808474749819`) all tied to the same Brandon "Extra $ for PAM" question. Bundle as one decision at 1:1.
- WW weblab dial-up (`1213764961716427`) still Today priority but milestone (4/7) passed 14d ago. Close or reframe.
- "Make changes to AU/MX/PAM for the week" (`1214080130329568`) is 34d OD; stale weekly recurring — replace with fresh Fri 5/2 instance per next-action.

---

Synced: 2026-04-30 ~12:05 UTC | 79 incomplete tasks | 27 Today / 18 Urgent / 34 Not Urgent/Backlog
DuckDB: asana.asana_tasks UPSERT pending (schema drift will be logged to ops.schema_changes)
