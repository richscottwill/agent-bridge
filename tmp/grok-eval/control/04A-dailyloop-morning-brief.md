# AM Brief — Wednesday 2026-04-22 (PT)

Richard — here's today's brief. Read the trainer check-in first, then the pacing line, then act.

## 1. TRAINER CHECK-IN
- **Streak:** 24 workdays at zero. The laptop died mid-1:1 yesterday — fine, that's reality. But the v5 was ready the night before and you didn't send it. The outage is the excuse, not the cause.
- **Hard thing:** Testing Document for Kate. v5 sitting on the shelf. This is a **10-minute send**, not a work session. Apply the 5 critic fixes, write a 2-sentence cover, attach, send — *before* the 1:30 PT 1:1 with Brandon.
- **Reality check:** 24 workdays of "tomorrow." That's not a project, that's an avoidance pattern. Today it breaks, or we add a day to the counter and the gap widens. Send first, everything else second.

## 2. HEADS UP — Critical unanswered

🔴 **CRITICAL (>3d, Brandon):**
- **Brandon — "Extra $ available in US for PAM — needs reg impact vetting"** (#ab-paid-search-app, **18.6d stale**). Blocks the Paid App PO chain. Reply with PAM reg impact from the tracker.
- **Brandon — Monthly callout comments in Loop** (#ab-paid-search-global, 6.8d). **HARD DEADLINE Fri 4/24 12pm PT.** Answer each Loop comment inline.
- **Brandon — Measure EM impact subtask (F90 LR Enhanced Match)** — assigned 4/21, prereq is EM details from tech PM.

🟡 **HIGH (1-2d):**
- **Yun-Kang — MX NB regs -19% — why?** (Quip: Global Acq WBR Callouts). **Blocks WBR publish.** Reply before WBR goes out.
- **AU HandOff Doc Final Review** (Brandon email today). Commit: biweekly cadence + 5/5 final handoff framing.
- **refmarker mapping audit PoC** (Brandon fwd from Kristine, 20d original). Designate a PoC — 5 min task.

## 3. SLACK OVERNIGHT
- 40 msgs ingested (38 Brandon DM + 1 `ab-marketing-ai` babel-system OSS share + 1 Quip bot).
- Brandon 1:1 lock-ins: biweekly AU cadence, **5/5 final handoff**, no scheduled AU calls after.
- Brandon explicit ask: **"Scope Kiro weekly AU change aggregator"** — L3 tool opportunity before 5/5. This is the kind of leverage work you keep saying you want.
- Kate offsite: Alexis in, Lena out → possible 3-way session with Brandon.

## 4. TODAY — Task Buckets

**Priority_RW = Today (Asana):**
- 🧹 Sweep: 0/5
- 📋 Admin: 1/3 (⏱️ 30-min cap)
- 🎯 Core: 1/4 (hard thing in slot 1)
- ⚙️ Engine Room: 1/6
- No Routine: 1 (in enrichment queue)

### 📋 Admin (30-min time bound)
1. **Reply to Dwayne — Brand LP consolidated feedback** (2d overdue). Canonical reopened after mis-close. 7-ask draft + 2 UX ticket specs in description. Send Mon reply with 5 FAQs (2 TBD) + Andrew CTA pull. [L1]

*After Admin: close it out. Core starts.*

### 🎯 Core — hard thing FIRST
1. 🔥 **Testing Document for Kate** (due 4/01, **21d overdue**, Urgent). v5 ready. Apply 5 critic fixes → 2-sentence cover → send to Brandon **before 1:30 PT**. **[L2 — THE HARD THING]**
2. **Email overlay WW rollout/testing** (due 4/24). Brandon's overlay ask unaddressed 3d in Outbound Marketing Goals. Reply with MCS-2553 as the path. [L1]

### ⚙️ Engine Room
1. **Weekly Reporting — Global WBR sheet** (2d overdue, Urgent). W15 data pull not started. Populate Paid App column before tomorrow AM. [L1]

### ⚠️ Top-5 Overdue (by severity)
- WW redirect — Existing customer reporting in Adobe Ad Cloud (**44d**) — kill candidate, stop carrying it.
- Make changes to AU/MX/PAM for the week (28d) — convert to recurring, stop re-creating weekly.
- Paid App (22d, Urgent) — blocked on Brandon PAM budget.
- **Testing Document for Kate (21d) — THE HARD THING** (see Core).
- Respond to Lena — AU LP URL analysis (19d). You said this went overnight — confirm + close.

### 📦 Needs Triage
7 tasks in `am-enrichment-queue.json` awaiting routing (goal updates, PAM reply, EM details, IECCP FAQ).

## 5. SPEC SHEET
- **ONE thing:** v5 Testing Doc → Brandon **before 1:30 PT**.
- **TWO must-do:** (1) MX forecast to Brandon **10am PT**, (2) AU handoff doc update.
- **THREE backlog-clears:** (1) Yun-Kang WBR reply, (2) Brandon PAM Slack reply, (3) refmarker PoC designate.

## 6. T-MINUS
- **5/2 (T-10d):** MBR callout due (MX/AU, Urgent, Admin).
- **5/5 (T-13d):** AU final handoff + monthly budget confirmation. Kiro AU change aggregator should be live.
- **5/21 (T-29d):** Bi-monthly Flash.

## 7. PACING vs OP2
- **MX:** 🔴 128.8% regs / **150.1% spend** — OVERSPENT. Forecast decay required BEFORE the 10am Brandon send. You can't send pacing at 150% without a narrative — Brandon will ask.
- **AU:** 🟢 38.2% regs / 36.2% spend — on pace for early-month. No narrative needed.

Tied into **Yun-Kang's MX NB -19%** question — same market, same story. One reply covers both if you're sharp.

## 8. aMCC
- Hard thing: Testing Document for Kate (L8 skip-level audience, v5 ready).
- Avoidance pattern: 24 workdays. You said "10-min send" on 4/21 EOD, laptop died, task slid. Pattern is clear — the barrier emerges at the last moment. The fix is structural: **send v5 before Brandon 1:1, not during or after.**
- Priority rule today: hard thing goes FIRST in Core. Nothing else in Core opens until v5 is sent.

## 9. SYSTEM HEALTH
- ✅ DuckDB (MotherDuck `ps_analytics`): fresh as of 2026-04-22 13:30Z — all schemas healthy.
- ⚠️ Hedy MCP: not in subagent roster, no refresh today. Last meetings still queryable via `signals.hedy_meetings` (latest 4/21).
- ⚠️ SharePoint Loop: auth expired — `mwinit -f` on local to refresh the 5 Loop pages (~24h stale).
- ⚠️ Karpathy Phase 6: nested `invokeSubAgent` blocked blind eval this run. Logged as BLOCKER. Priors untouched. `richard-style-email` reverted to baseline (818w).
- ⚠️ `motherduck_token` env var missing for `hard-thing-refresh.py` — null-state shadow written locally, non-fatal.

## 10. TODAY'S TOP-3 ACTION QUEUE (time-ordered)
1. **10:00 PT** — MX forecast to Brandon with decay narrative (150% spend — must explain).
2. **Before 1:30 PT** — Testing Doc v5 to Brandon. **The hard thing.** Non-negotiable.
3. **Before WBR cut** — Reply to Yun-Kang on MX NB -19% drop.

---

**One-line read:** Hard thing is a 10-minute send, not a work session. MX is on fire (150% spend), and the Yun-Kang question is the same story. Send v5 first, handle MX second, everything else third.

---
Generated by am-backend v5.2.1 + am-frontend v3.0.0 on 2026-04-22 06:40 PT. State files: `~/shared/context/active/am-*.json`.
