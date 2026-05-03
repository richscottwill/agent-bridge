# Daily Brief — Sunday May 3, 2026

**Generated:** 13:35 UTC (06:35 PT) via manual am-backend-parallel Phases 2-5 after schema drift fix
**Prior brief:** `am-brief-2026-05-01.md` (Friday)

---

## 🎯 Hard Thing #1 — polaris-brand-lp

**Signal:** Score 22.12, 14 mentions across 6 channels, 7 non-Richard authors. 13-day incumbent. Still #1 by a wide margin.

**Live task:** `1214330104198712` Brand LP AU/MX test design — alternate measurement (non-weblab) for MCS vs Reg Start. **Due Tuesday 5/6.**

**What moves it:** Write the v1 1-pager. 6 sections, 90 min. Non-weblab measurement framework with reftag CVR, sample sizes (AU 245/wk MX 551/wk, 4wks each, MDE 8-10%), z-test analysis. Cross-link to the consolidated Polaris feedback doc from Brandon's 4/29 coaching.

**Carry forward:** Polaris consolidated QA feedback doc from 4/29 still not visibly closed in Slack. Highest-leverage trust-earning item with Brandon.

---

## ⏰ This week — the 5 things that matter (Mon-Wed)

1. **Brandon 1:1 Tuesday 5/5** — kill-or-revive decision on PAM budget reply (27d OD) + weblab dial-up (26d OD) + EM FAQ (11d OD). Bundle these three.
2. **MCS Tech OP1 ideas reply to Brandon** — directly asked. OP1 intake deadline 5/5 (ambiguous 5/15 per Lina). Write 2 ideas before 5/5.
3. **AU formal handoff to Megan Tuesday 5/5** — handover doc + Google Ads access + GenBI stitching fix (due 5/5). Megan becomes AU POC.
4. **Brand LP AU/MX 1-pager (HARD THING)** — due 5/6. Kiro-block 9:30-11am Tuesday.
5. **Google Ads MCC SSO admin decision** — due Monday 5/4 (SSO enforcement launches 5/4). Look up MCC admin assignments, decide own-or-delegate.

---

## 📬 Richard owes a reply (5 items, all from this weekend)

| To | Topic | Source | Urgency |
|---|---|---|---|
| **Brandon** | MCS Tech OP1 ideas | dm-brandon 5/1 | Medium (5/5) |
| **Brandon** | MBET issue reporting | email 5/1 (PO #2D-19910168) | Medium |
| **Vijeth Shetty** | US Browse Category CTA greenlight | Asana 5/1 | Medium |
| **Mukesh Gupta** | Current PS data-pull approach for GenBI | mpdm-rasanmol 5/1 | Low (but L3 opportunity) |
| **Megan Oshry** | AU reftag + reg-database query | dm-meganos (carried from 4/29) | Medium |

---

## 📊 Task state

- **82 active tasks**, 16 overdue (Richard-assigned)
- **Bucket caps violated:** Engine Room 12/6, Core 10/4, Admin 6/3 — 15 over total. 36 tasks have no Routine_RW.
- **Top 3 overdue (39d, 33d, 27d):** Make changes to AU/MX/PAM (weekly recurring stale — close + recreate), Paid App (Engine Room, legacy workstream), Reply to Brandon PAM budget (decision at 5/5 1:1).

---

## 🔔 Signals that moved this week

- **Brandon's "Thanks guys!"** in ab-paid-search-global after Richard corrected AU 30% CVR stat. Trust signal intact.
- **CVR LP personalization stat converged at 15-20%** (Stacey/Adi). If Brandon reuses externally in QBR/OP1, Richard should know provenance.
- **Outlook MCP flaky** (Jesse Alcaraz active bug per agentspaces-interest) — impacts your Kiro workflow, worth knowing.
- **GTMO 1-click Auto CBR launching end of May** (US/CA/EU/JP) — L3 Team Automation template worth watching.

---

## 🛠 System state

**Ran today:**
- Phase 1 subagents A/C/D/E completed (Slack +27 msgs, Email +51, Loop 5/5, Hedy no-op)
- Schema drift fixed: AU/MX standalone GIDs archived, consolidated to ABIX in 3 protocol files
- B1 partial UPSERT: 14 task refreshes + 8 new inserts (total 82 active)
- B2 lean scan (no GetTaskStories — Slack/Email already covered the signal)
- Phase 2.5 enrichment: relationship_activity, five_levels_weekly, project_timeline (+4 events) all updated
- Phase 3 Kiro_RW enrichment on 7 high-priority tasks
- Phase 4 portfolio scan: 8 projects mapped, 11 tasks flagged with stale AU/MX labels (next sync fixes)
- hard_thing_candidates refreshed: polaris (22.12) / oci (8.15) / au-cpa-cvr (6.37)

**Broken but flagged (logged to asana.schema_changes):**
- `hard-thing-refresh.py` SyntaxError at line 115 — needs repair
- `sync_metrics.py` BinderException on ps.metrics ON CONFLICT — needs PK constraint fix
- Hard-thing computed directly from signal_tracker as workaround

**Next AM run:** Will do full Asana UPSERT with corrected project list. The stale "AU"/"MX" project_name in 11 rows will resolve on next pass.
