# AM Brief — Wednesday 2026-04-22 (PT)

Streak: 24 workdays at zero. The hard thing is still the Testing Document for Kate. v5 has been ready since 4/21 EOD. Today is a 10-minute send, not a work session. Send v5 BEFORE the 1:30 PM Brandon 1:1, not during.

---

## Priorities

Top three, ordered, with trigger times:

1. **10:00 PT — MX forecast to Brandon with decay narrative.** MX pacing is 🔴 128.8% regs / **150.1% spend** vs OP2. Overspent. Narrative must explain the decay; a number-only send will bounce back.
2. **Before 1:30 PM PT — Testing Document v5 → Brandon.** Apply the 5 critic fixes, 2-sentence cover, hit send. **THE HARD THING.** 24-workday avoidance streak ends today or it doesn't.
3. **Before WBR cut — Reply to Yun-Kang on MX NB -19% drop.** Blocks WBR publish. 0.9d old.

Two must-do behind the top three: (a) AU handoff doc update with biweekly cadence + 5/5 handoff framing, (b) Brandon PAM reg-impact reply (18.6d unanswered, blocking Paid App PO chain).

## Leverage Move

**Send the Testing Document.** This is the only L2 move on the board today and it funds L3 onward. 23 workdays of "tomorrow, after one more fix" is not preparation — it's avoidance. v5 is done. The critic's 5 fixes are scoped. There is no work left to do on it, only a send.

Secondary L2 move: scope the Kiro weekly AU change aggregator. Brandon explicitly asked 4/21. If it exists by 5/5, the handoff has a tool attached to it — that's the L3 wedge. Don't start it today. Note it, queue it, protect the hard-thing block.

## Friction to Remove

- **Laptop reset risk.** 4/21 send was killed by a 4-minute laptop outage during Brandon 1:1. Send v5 at **11:00 PT from a working session**, not wedged against the 1:30 meeting. Remove the last-moment barrier before it appears.
- **Hedy MCP offline in subagent roster.** No Hedy refresh today. Query `signals.hedy_meetings` directly if a meeting recap is needed; don't wait for the enrichment hook.
- **SharePoint Loop auth expired.** `mwinit -f` on local when you get there. Loop pages ~24h stale (Brandon 1:1 notes, MBR doc). Not blocking today, but do it before Friday's monthly callout deadline.
- **motherduck_token missing** for hard-thing-refresh.py. Non-fatal, but the shadow-state is local-only — don't trust the tracker widget until this is restored.
- **Karpathy Phase 6 blocked** by invokeSubAgent nested-call limitation. File reverted to baseline. Not your problem today; logged.

## Data Snapshot

**Pacing (ps.monthly_pacing, MTD):**
- MX: 🔴 128.8% regs / 150.1% spend — overspent, decay required before 10am send.
- AU: 🟢 38.2% regs / 36.2% spend — on pace, early-month.

**Streak & Hard Thing (main.l1_streak, main.hard_thing_now):**
- Streak: **24 workdays at zero.** Reset 4/21 (laptop).
- Rank 1: Testing Document for Kate (L2, 21d overdue, v5 ready).

**Task state (asana.asana_tasks, Priority_RW=Today):**
- Sweep 0/5, Admin 1/3, Core 1/4 (hard thing), Engine 1/6, No-Routine 1.
- Top overdue: WW redirect (44d — kill candidate), AU/MX/PAM weekly (28d — convert to recurring), Paid App (22d, blocked on Brandon PAM), **Testing Doc (21d, hard thing)**, Lena AU LP (19d — confirm sent, close).

**Signals (signals.slack_unanswered / signals.emails_unanswered):**
- 🔴 Brandon PAM $ (18.6d), Brandon monthly callout Loop (6.8d, Fri 12pm PT hard deadline), Brandon EM impact subtask (no due date, prereq on tech PM).
- 🟡 Yun-Kang MX NB -19% (0.9d), AU HandOff Final Review (today), refmarker PoC (20d, 5-min designate).

**T-minus:** MBR callout 5/2 (T-10d). AU handoff + monthly budget 5/5 (T-13d).

## Open Questions for Richard

1. **MX decay narrative — your call or team pull?** MTD spend at 150% OP2 is not a "just decay the forecast" send. Do you want to pull Yun-Kang in on the reply, or own the narrative solo to Brandon at 10am?
2. **Paid App PAM reply — send today or hold?** Brandon's ask is 18.6d old. Reg-impact numbers are in the tracker. If it's a 10-minute send like the Testing Doc, it goes today — confirm?
3. **WW redirect — kill it?** 44 days overdue. Flagging for closure. Confirm and I'll draft the closeout comment.
4. **AU change aggregator — scope today or Monday?** Brandon asked 4/21. Today's calendar is full; Monday is the realistic scoping window. Confirm the defer so it doesn't bleed into the hard-thing block.
5. **AU/MX/PAM weekly changes — convert to recurring?** 28d overdue because it's a weekly task being tracked as one-off. Confirm and I'll restructure in Asana.

---

**One thing today:** v5 Testing Doc → Brandon before 1:30 PM. Everything else is negotiable. That is not.
