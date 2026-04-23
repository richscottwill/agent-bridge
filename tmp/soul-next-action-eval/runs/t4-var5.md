# AM Brief — Wednesday 2026-04-22 (PT)

*Generated under: soul.md + am-triage.md (Daily Brief Output Format) + Leverage Cascade (var5). Hard thing corrected this morning per `main.hard_thing_now` — Testing Approach v5 shipped 4/5; incumbent ledger had been inheriting it incorrectly through 4/21. New rank 1: **polaris-brand-lp** (valuable-and-avoided, 4 channels, no Richard artifact).*

---

## 1. Priorities

1. 🔥 **Polaris Brand LP — ship the rollout timeline one-pager.** [L2 — THE HARD THING] Rank 1 in `main.hard_thing_now`. Four channels lit (Dwayne consolidation, MCS-3004 Italy revert, Andrew CTA, −30% CVR narrative) and zero Richard artifact on record since incumbent_since 4/20. This is the new avoidance pattern — don't let it become another 23-day slide.
2. **MX forecast → Brandon by 10:00 PT** with decay narrative. [L2] Pacing is 🔴 150.1% spend / 🔴 128.8% regs. No send until decay is explained; "overspend plus hot reg pace" is not a brief you mail without a story.
3. **Testing Doc v5 — close the loop.** [L1] Doc shipped 4/5 per amcc.md. Confirm with Brandon it's landed and ask one question that moves it toward Kate: "Is v5 ready for me to forward to Kate, or are you taking it in?" Clears the ambiguity that kept it as the phantom hard-thing for 16 workdays.
4. **Yun-Kang reply — MX NB regs −19%.** [L2] Blocks WBR publish. 0.9d old. 10-min reply from `ps.v_weekly` + change log.
5. **ABIX handoff doc input** before Brandon takes it to Kate this week. [L1] Kate-visible, still OPEN.

**Top-3 time-ordered queue:**
- **10:00 PT** — MX forecast + decay narrative → Brandon
- **Before 1:30 PT 1:1** — Polaris rollout timeline draft (one page, dates + owners) → ready to walk through live
- **Before WBR cut** — Yun-Kang MX −19% reply

---

## 2. Leverage Move

**Write the Polaris Brand LP rollout timeline one-pager today. Walk Brandon through it in the 1:30 PT 1:1.**

**What it is:** A single-page doc — markets × dates × owners × status — covering AU, MX, DE, UK, JP, FR, IT, ES, CA, US-ES. Lock Italy revert timeline. Lock the benefit-cards / sub-header / FAQ / closing-CTA specs from the 4/16 DDD. Name a PoC per market.

**What it unblocks / multiplies:**
- Brandon designated Richard single-point-of-contact for global Polaris 4/14. No artifact yet = that designation is ambient, not load-bearing.
- Italy ref-tag P0 is mid-revert with Alex. MCS-3004 has a SIM. A timeline anchors both into one visible thread rather than five Slack threads.
- Four channels of signal are currently flowing into Richard's inbox with nowhere to point. The one-pager becomes the reply surface for Dwayne, Andrew, Stacey, Alex.
- L3 side-effect: this is the structural context an AU-change-aggregator-style tool would wrap around. Build the doc first, tool second.

**Why today:** Brandon 1:1 at 1:30 PT. You missed the 4/21 window to laptop failure. The meeting happens or it doesn't — the document going into it changes whether "Polaris PoC" stays real or drifts. And `hard_thing_now` just surfaced it as rank 1 this morning. Don't let a brand-new top-ranked hard thing accrue a streak.

**Cascade reasoning:**
- Step 1 (current brief's Leverage Move): The existing brief pointed at Testing Doc v5. Invalidated — v5 shipped 4/5.
- Step 2 (highest Five Levels opportunity in current.md): Polaris WW rollout dominates current.md — 4 distinct project threads, Kate-visible, Brandon-led, no one-pager.
- Step 4 final filter — smaller move that's even higher leverage? **Yes, and I'm recommending it:** don't try to make it perfect. Ship a v1 before 1:30 today, 1 page, dates and owners only. Spec refinements go in v2 after Brandon reacts. The smallest viable artifact beats the comprehensive one that doesn't exist.

**Principle check:** Structural over cosmetic (#2) — this creates the default surface for Polaris coordination. Subtraction before addition (#3) — replaces 4+ Slack threads with one doc. Reduce decisions, not options (#6) — Brandon gets something to react to instead of composing from scratch.

---

## 3. Friction to Remove

**Structural change:** Wire `hard_thing_now` refresh into the AM hook as a blocking step, not an advisory. Today's brief almost went out with stale rank-1 data because `motherduck_token` has been missing for `hard-thing-refresh.py` on 4/21 and 4/22. The refresh happened manually this morning via signal recompute; if it hadn't, the brief would still be chasing Testing Doc v5.

**Fix:** Add a pre-brief check — if `main.hard_thing_now.refresh_at` is >12h old, halt brief generation and surface the token failure. Don't generate a brief with stale hard-thing data. The whole daily system pivots on rank 1 being right.

**Principle:** Invisible over visible (#5) + Structural over cosmetic (#2). This is defaults and gates, not cosmetics. The agent made a bad call for 7 workdays (4/14–4/21) because the incumbent ledger inherited Testing Doc forward while the signal system said otherwise. That's an infrastructure problem, not a motivation problem.

**Device.md check:** This is not a new tool — it's a gate on an existing one (`hard-thing-refresh.py`). No build, just a failure mode fix. ✅

---

## 4. Data Snapshot

**Streak + hard thing:**
- Streak: **1 workday at zero** (reset 2026-04-22 — Testing Approach v5 completion 4/5 now correctly attributed)
- Rank 1 hard thing: **polaris-brand-lp** (score 4.05, 4 channels, 5 unique authors, no Richard artifact)
- Rank 2: oci-rollout (3.10)
- Rank 3: au-cpa-cvr (2.80 — borderline; partially addressed 4/21 via Lena reply)

**Pacing (April 2026, MTD):**
- **MX** 🔴 regs 128.8% / 🔴 spend **150.1%** — OVERSPENT. Decay required before 10am Brandon send.
- **AU** 🟡 regs 38.2% / 🟡 spend 36.2% — early-month, below 100% pace but not outside ±20pp from calendar-fraction expected. Watch post-max-clicks switch (4d since switch, still not checked).
- **US** 🟢 regs 59.5% / 🟢 spend 47.9% — on pace.
- WW totals unattributed (no OP2 target on file).

*Tier convention: 🔴 = >±20pp from calendar pace, 🟡 = ±10–20pp, 🟢 = within ±10pp. AU at ~day 22/30 = 73% calendar pace → 38% regs is ~35pp below, but Richard's standing read is "on pace for early-month" — flagging for his judgment.*

**Top-5 overdue Asana tasks:**
1. Create FR accounts — 62d
2. Source DE/IT/ES — 62d
3. WW redirect — Existing customer reporting in Adobe Ad Cloud — 45d (kill candidate, no routine set)
4. Page Creation — Duplicate Beauty and Auto page for MX — 31d
5. Make changes to AU/MX/PAM for the week — 29d (convert to recurring)

**System health:**
- DuckDB: ps_analytics attached, ops/signals/asana/ps/main fresh as of 2026-04-22T13:30Z ✅
- ⚠️ `motherduck_token` env var missing for `hard-thing-refresh.py` — manual recompute required this AM (2nd day in a row)
- ⚠️ Hedy MCP: not in subagent roster — no refresh this run (signals.hedy_meetings latest 4/21)
- ⚠️ SharePoint Loop: auth expired, `mwinit -f` needed on local for 5 loop pages (~24h stale)
- ⚠️ Karpathy Phase 6: nested-call limitation still blocking blind eval

---

## 5. Open Questions for Richard

1. **Polaris rollout timeline — ship v1 before 1:30 PT 1:1, yes or no?** (Recommended: yes, one page, dates + owners, v2 after Brandon reacts.)
2. **Testing Doc v5 status — forward to Kate yourself, or ask Brandon to take it?** (Resolves the 16-day ambiguity about what "done" means on this.)
3. **WW redirect Adobe Ad Cloud task (45d overdue, no routine) — kill or revive?** 
4. **AU post-max-clicks check — do it today or push to tomorrow?** (4 days since switch; overpacing risk but AU pacing is not red yet.)
5. **`motherduck_token` — can you re-export on local and push to SSH env? Or should I flag this to the system owner?** (Two straight days of manual hard-thing refresh.)

---

## Next Step

Open a new file: `shared/wiki/agent-created/strategy/polaris-brand-lp-rollout-timeline.md`. Draft v1 in the next 45 minutes — markets × dates × owners × status, one page. Walk Brandon through it at 1:30 PT. That's the move.
