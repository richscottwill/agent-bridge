# AM Brief — Wednesday 2026-04-22 (PT)
_Format: am-triage.md Daily Brief Output Format. One-Move Rule (var2) applied at the end._

> ⚠️ **Signal shift flagged.** `main.hard_thing_now` rank 1 flipped overnight from **Testing Document for Kate** to **polaris-brand-lp** (score 4.05, 4 channels, 5 authors, null Richard artifact, reinforced 4/21 by Dwayne Brand LP consolidation + MCS-3004 Italy revert + Andrew CTA + -30% CVR narrative). The daily-brief-latest.md still names Testing Doc as the hard thing — it's stale by one refresh. Per the Daily Brief Output Format rule ("rank=1 with no Richard artifact = Priority #1"), today's Priority #1 is **Polaris**, not the Testing Doc. Both are in scope — see below.

---

## 1. Priorities

1. 🔥 **Polaris WW Brand LP — produce the Richard artifact today [L2, THE HARD THING]**
   Rank 1 in `main.hard_thing_now`. No Richard artifact on file. You've been single-point-of-contact since 4/14 and the signal is reinforcing every day (Dwayne consolidated feedback, MCS-3004 Italy revert mid-flight, Andrew CTA work, -30% CVR narrative, 4/16 DDD decisions on benefit cards / localized sub-header / FAQs / closing CTA). The specific artifact: **the one-page Polaris WW rollout timeline with dates + owners** that's been on Pending Actions since 3/20. That's the missing document the system keeps scoring. 60–90 min. Pull the DDD decisions and the MCS-3004 status into a single page. This is the L2 move Kate will see.

2. 🔥 **Testing Document for Kate v5 → Brandon before the 1:30 PM 1:1 [L1, second-hard-thing]**
   24 workdays at zero. v5 has PUBLISH verdict (8.4/10) since 4/5. Laptop killed 4/21 — no excuse today. **10-minute send, not a work session.** Apply the 5 critic fixes, 2-sentence cover note, send. If you skip this for Polaris, the streak resets at 25 and Brandon walks into the 1:1 asking why.

3. ⚙️ **MX forecast to Brandon by 10:00 AM PT [L2]**
   MX is 🔴 128.8% regs / 🔴 150.1% spend — OVERSPENT. Brandon expects a decay narrative before he responds on the PAM US $ question (18.6d unanswered). Without this, the PAM conversation can't close.

4. 📋 **Yun-Kang: MX NB regs -19% reply before WBR cut [L2]**
   Blocks WBR publish. Quip: Global Acq WBR Callouts, 0.9d. 10-minute reply.

5. 📋 **AU handoff doc update — biweekly cadence + 5/5 framing [L2]**
   Brandon's explicit 4/21 1:1 commitment. Slack receipt. T-13d.

**Top-3 time-ordered queue:**
- **10:00 AM PT** — MX forecast + decay narrative to Brandon.
- **Before 1:30 PM PT** — Testing Doc v5 to Brandon (send, don't rework).
- **Before WBR cut (afternoon)** — Yun-Kang MX NB -19% reply.
- **Core block (60–90 min, before 1:1)** — Polaris one-page rollout timeline drafted.

---

## 2. Leverage Move

**Polaris WW rollout one-pager — treat it as the single document that makes you the WW owner, not a task to check off.**

- **What it is:** One page. Dates + owners + status per market (US ✅, JP ✅, CA ✅ 4/7, IT 🚨 revert in flight, DE 🟡 weblab, AU/UK/FR/ES next, MX 🟡 early test). Benefit cards, localized sub-header, FAQ changes, closing CTA — folded in from the 4/16 DDD.
- **What it unblocks / multiplies:**
  - You stop answering the same Polaris status questions 4 different ways in 4 different Slack threads.
  - Alex (Andes), Stacey, Dwayne, Vijeth all get one artifact to reference — pre-loaded content → structural intervention, not cosmetic.
  - Kate visibility: Polaris is a Brandon-driven WW initiative and the artifact is the thing she'll see if/when it reaches her.
  - It's the Richard artifact the hard-thing tracker is literally asking for. Ship it and the signal collapses.
- **Why today:** Polaris hit rank 1 overnight with a 4.05 score (4 channels, 5 unique authors) — the signal is still hot and will fade once MCS-3004 Italy revert completes. Day the signal is loudest = day the artifact lands best. Also: Brandon 1:1 is today, and the one-pager fits into "here's what I shipped this week" cleanly.
- **Level:** L2 (WW testing methodology, WW owner narrative). Indirectly funds L3 (future Polaris-monitoring tool teammates could adopt).

---

## 3. Friction to Remove

**Structural fix:** Make the "Today's ONE thing" field in the AM brief **read from `main.hard_thing_now` rank=1 directly, not from a hand-maintained daily-brief template.**

- **Friction detected:** Today's daily-brief-latest.md says the hard thing is Testing Doc. `main.hard_thing_now` says it's Polaris. The brief lagged the data layer by one refresh. If I trust the brief, I work the wrong hard thing. If I trust the query, I override the brief. That's a decision I shouldn't be making at 06:40 AM.
- **Why it's structural, not cosmetic:** This changes the default source-of-truth wiring, not the layout. Principle #2 (Structural over cosmetic) + Principle #6 (Reduce decisions, not options).
- **Proposed change:** In `shared/context/intake/daily-brief-latest.md` generation, Section 1 "Trainer Check-In" and Section 7 "aMCC" both pull the hard-thing string from `SELECT topic, last_richard_artifact_date FROM main.hard_thing_now WHERE rank=1`. If `last_richard_artifact_date IS NULL`, that topic is THE hard thing — full stop. If the hard_thing_refresh.py job fails (as it did 4/21 + 4/22 — motherduck_token missing), surface that in Section 8 System Health as a blocker, don't silently fall back to yesterday's string.
- **Subtraction check (Principle 3):** This doesn't add a new section. It removes the human-authored "Hard thing:" line from the template and replaces it with a query. Net removal.
- **Who owns it:** karpathy owns `hard-thing-selection.md` — route the change request there. I'm not editing the protocol unilaterally.

---

## 4. Data Snapshot

**Streak + Hard thing:**
- `main.l1_streak` (2026-04-22): **1 workday at zero.** Streak reset from 23 → 1 overnight (artifact_shipped = false). Pattern: the tracker treats the Polaris signal-flip as a fresh counter, not a continuation of the Testing Doc count. Both are at zero.
- Hard thing (rank 1): **polaris-brand-lp**, score 4.05, no Richard artifact, incumbent since 2026-04-20.
- Hard thing (rank 2): **oci-rollout**, score 3.10.
- Hard thing (rank 3): **au-cpa-cvr**, score 2.80 (Richard partial artifact 4/21 — may fall off next refresh).

**Pacing vs OP2 (ps.monthly_pacing, 2026-M04):**
- 🔴 **MX — regs 128.8% / spend 150.1%** (overspent both sides, tiers diverge).
- 🔴 **AU — regs 38.2% / spend 36.2%** (well below 🟡 floor of 80pp for the period — tier 🔴 "under" by the ±20pp rule, but early-month — functionally healthy, flag as "on pace for early-month" per existing daily brief narrative).
- Context: WW pacing cols are null (expected — WW is a rollup).

**Top-5 overdue Asana:**
| # | Task | Due | Days overdue |
|---|------|-----|--------------|
| 1 | Create FR accounts | 2026-02-20 | 62d — kill-or-revive candidate |
| 2 | Source DE/IT/ES | 2026-02-20 | 62d — kill-or-revive candidate |
| 3 | WW redirect — Existing customer reporting in Adobe Ad Cloud | 2026-03-09 | 45d — **kill candidate per brief** |
| 4 | Page Creation — Duplicate Beauty & Auto page for MX | 2026-03-23 | 31d |
| 5 | Make changes to AU/MX/PAM for the week | 2026-03-25 | 29d — convert to recurring |

**System health:**
- DuckDB `ps_analytics`: fresh (2026-04-22 13:30Z).
- Hedy MCP: unavailable in subagent roster — no meeting refresh today.
- SharePoint Loop: auth expired, `mwinit -f` on local to refresh 5 loop pages.
- `hard-thing-refresh.py`: **motherduck_token env var missing 2 days running** — tracker writing local null-state shadows. BLOCKER for automated refresh. Non-fatal but will drift the hard-thing signal if unresolved by Friday.
- Karpathy Phase 6: invokeSubAgent nesting limitation blocks blind eval execution — priors untouched, richard-style-email reverted to baseline.

---

## 5. Open Questions for Richard

1. **Is the one-pager the right Polaris artifact?** (y = timeline+owners one-page doc; n = something else — then what?)
2. **Testing Doc v5 send order today: before or after the Polaris one-pager?** (before = protects L1 streak at a 10-min cost; after = lets you batch the Polaris thinking first — risk of the 1:30 PM deadline slipping).
3. **Kill the 44d WW redirect Adobe Ad Cloud reporting task?** (y/n — brief has already flagged it as kill candidate twice).
4. **PAM US $ to Brandon — send after MX forecast (10am) or after 1:1 (1:30pm)?** (Slack is 18.6d unanswered; Brandon explicitly tied it to reg-impact vetting — the 10am forecast is the prerequisite).
5. **Does karpathy get the ticket to wire `main.hard_thing_now` rank=1 into daily-brief generation?** (y/n — this is the Section 3 structural fix).

---

**Next Best Action: Write the Polaris WW rollout one-pager (timeline + owners + status per market, folding in the 4/16 DDD decisions) in a 60–90 minute Core block _after_ sending Testing Doc v5 to Brandon in the first 10 minutes of the day. Polaris is the hard thing rank 1 with no artifact; the Testing Doc send is the 10-minute cost that protects the L1 streak and cleans the 1:30 PM 1:1 ground. Two sends before noon: v5 (10 min) and then Polaris in flight.**
