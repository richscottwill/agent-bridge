# Daily Brief — Wednesday May 6, 2026

**Generated:** 14:35 UTC (07:35 PDT) via manual am-backend-parallel Phases 1-5 (degraded-auth mode)
**Prior brief:** 2026-05-05 (Tuesday — `am-brief-2026-05-05.md`)
**Run mode:** DEGRADED — Midway cookie missing → Slack/Outlook/SharePoint all 401. Hedy + DuckDB fresh. Asana MCP not exposed this session (separate auth path).

---

## 🔴 Immediate — before anything else

**Run `mwinit`** (or `mwinit -o` on CloudDesktop). 2 consecutive AM runs have failed Slack/Outlook/SharePoint ingestion. ~40h of Slack + email backlog is queued, will ingest automatically on next run once cookie is refreshed.

---

## 🎯 Hard Thing — polaris-brand-lp 1-pager

**Task:** `1214330104198712` Brand LP AU/MX test design — alternate measurement (non-weblab) for MCS vs Reg Start. **Due today 5/6.**

**Context from 5/5 Brandon 1:1** (hedy:Qz26yMKVFzAWAiU99ZoD — already in topics/tests/polaris-brand-lp.md and meetings/brandon-sync.md):
- Brandon wants visibility. Scope has narrowed (AU exited 5/5, EU earlier, ABIX whittled). MX + WW project-manager role is where growth shows up or doesn't.
- Brandon specifically flagged "I don't know where you're making progress" as the framing Richard needs to invert.
- The 1-pager is visible progress — ship it.

**What moves it:** Non-weblab measurement framework (reftag CVR, sample sizes ~AU 245/wk, MX 551/wk, 4wks each, MDE 8-10%), z-test analysis, 6 sections, 90 min. Stage draft under `~/shared/wiki/staging/`.

---

## 📅 Today (Wed 5/6)

- **12:00 PT — Richard/Adi sync (25 min)** — AI tool workflow cadence
- **12:00 PT — App OP1 Internal Review (Brandon, 60 min)** — OP1 app acquisition; Peter likely leading
- **13:00 PT — Bi-Weekly Google + AB Performance Sync (Mike Babich, 30 min)** — APAC MCC access thread still open per 5/5 AU handover context

---

## 🗓️ Tomorrow (Thu 5/7)

- **09:00 PT — Paid Acq: Deep Dive & Debate (Brandon, 30 min)**
- **13:00 PT — Adobe Bi-Weekly (Suzane Huynh, 30 min)**

---

## 📊 W18 Performance Headlines (authoritative — xlsx synced 5/5 01:13 UTC)

| Market | Regs | vs Forecast | Flag |
|---|---|---|---|
| **WW** | 16,341 | — | CPA $79.90, healthiest weekly in recent memory |
| **US** | 8,908 | +25% vs p50, ABOVE CI | Overperformance; watch W19 for recalibration signal |
| **MX** | 659 | +44% vs p50, ABOVE CI | Sparkle halo (ended 4/30). W19 is post-Sparkle baseline |
| **AU** | 228 | exactly on p50 | Clean baseline at 5/5 handover to Megan |
| **JP** | 447 | -24% vs p50 | Only market below — GW seasonal |
| **DE** | 1,318 | ABOVE CI (+0.5%) | Top of band, watch W19 |
| **FR/IT/ES/UK/CA** | all above p50 | within or above CI | EU5 strong week |

**OP2 M05 W1 pacing:**
- MX at 67% of monthly target in W1 (Sparkle halo — expect compression)
- US at 29% of monthly target — on pace for ~125% of target
- AU at 19% — slightly behind pace (Megan now owns)
- DE/UK/FR/IT/ES/CA/JP all tracking 22-30% of monthly in W1

---

## 📬 Richard owes replies (backlog from last successful Slack scan 5/4 14:50)

| To | Topic | Days Old | Notes |
|---|---|---|---|
| **Brandon** | AU Transition doc review | 12d | Likely resolved via 5/5 handoff, but no explicit acknowledgement observed |
| **Brandon** | OP1 owners — flat YoY budget + Small SMB break-out | 5d | Affects MX/AU RoY reforecast |
| **Brandon** | MCS team follow-up summary | 5d | Yun-Kang + Andrew waiting |
| **Peter Ocampo** | PAM Prime Day plan | 10d | Budget + YoY + projections |
| **Mukesh Gupta** | GenBI data-scalability approach | 3d | Partial resolution promised in 5/5 MX sync (time-based paid-social/branded correlation analysis — next week) |
| **Vijeth Shetty** | ps-brand pages updates WW | 3d | Asana comment |
| **Megan Oshry** | Adobe Analytics access | 6d | Richard committed 5/5 to set up AdCloud export this week — in motion |

---

## 🧾 Commitments from 5/5 Brandon 1:1 (Qz26yMKVFzAWAiU99ZoD)

- **Submit OP1 automation request** connecting Google Ads data directly (bypass Adobe) — EOW (5/8)
- **Re-engage LiveRamp on F90 TPS approval** — 5/7; Brandon explicit call-out ("I sat in your queue for quite some time")
- **Timestamped Asana progress notes on major tasks** — ongoing, review 5/12

---

## 🧾 Commitments from 5/5 MX sync (FKZWlEQGcW5S2tv3FCav)

- Update monthly sheet with March + projections for QBR — EOW
- Confirm R&O budget transition timing with finance BOC — 5/10
- Time-based paid social vs branded search correlation analysis — next week
- Adobe Analytics journey flow analysis — next week
- Add OP1 journey test documentation to OP1 doc — 5/15

---

## 🧾 Commitments from 5/5 AU handover (j7nQYyfUFwwAbzM6LGZv) — Richard-side

- Set up Adobe AdCloud reporting exports (weekly start) — this week
- Paste change log historical entries + RefTag structure example in handover Quip — post-call
- Confirm Megan is on AB Paid Search Flash distribution — post-call

---

## 📈 Top signals (7d, DuckDB)

1. **polaris-brand-lp** (2.73) — 8 reinforcements, Brandon + Yun-Kang, cross-channel. The hard thing.
2. **oci-rollout** (2.69) — 4 reinforcements, quiet week
3. **au-cpa-cvr** (2.36) — now a Megan concern, not Richard's primary
4. **au-transition** (2.07) — closing out via 5/5 handover
5. **op1-forecast-flat-budget** (2.07) — Brandon-sourced, OP1 tech intake deadline 5/15
6. **op1-strategy** (1.95) — 5 reinforcements cross-channel
7. **mcs-coordination-ownership** (1.50) — Brandon's explicit ask for Richard single-point-of-contact

---

## 🗂️ Topic log work completed this run

- 4 Hedy sessions routed to topic docs + meeting series files (2026-05-06 protocol: topic logs replace deprecated hedy-digest.md / signals.hedy_meetings / main.meeting_*)
- Meeting series files updated: brandon-sync (already done earlier), weekly-paid-acq (already done), **mx-paid-search-sync (added 5/5 entry this run)**, **au-paid-search-sync (added 5/5 handover + 4/28 pre-handover this run)**
- 6 topic docs at Summary-refresh debt ≥3: baloo-shop-subdomain, mcs-polaris-migration, brandon-sync, weekly-paid-acq, mx-paid-search-sync, au-paid-search-sync — wiki-maintenance will refresh these

---

## ⚠️ What's stale / unknown

- **Slack / Email / Calendar / SharePoint / Loop:** 40-73h stale pending `mwinit`
- **Asana:** 3 days stale (last DuckDB sync 5/3 13:36 UTC). 5/5 Brandon 1:1 kill-or-revive outcomes on PAM/EM tasks not captured. Asana MCP not exposed in current orchestrator model context either — tools would need to be made available.
- **Hard thing candidates table:** last refresh 5/3. Polaris still #1 by wide margin; no recompute needed to be confident.

---

## 🔁 Open items that have rolled multiple runs

- WW sitelink audit (19d overdue, `1214074477110993`)
- Email overlay WW rollout (18d overdue, `1213125740755931`)
- Paid App Q2 PO + amend Google PO (23d overdue, `1212808474749819`) — blocked on 5/5 Brandon PAM kill-or-revive outcome
- Enhanced Match FAQ for legal (14d overdue, `1213964668984060`) — blocked on Enhanced Match details (29d overdue, `1213875146955582`)
- AU handover tasks (multiple) — mark complete or transfer to Megan post-5/5 handoff

---

**State files produced:** am-signals-processed.json, am-enrichment-queue.json, am-portfolio-findings.json, am-wiki-state.json — all under `~/shared/context/active/`.
