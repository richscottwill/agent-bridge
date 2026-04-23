# Daily Brief — Wednesday 2026-04-22 (PT)

**⚠️ Ledger conflict flagged at top.** `main.hard_thing_now` was retrospectively corrected this morning (4/22 AM): Testing Approach v5 actually shipped 4/5 — the incumbent ledger had been inheriting it forward incorrectly 4/14–4/21. The current **rank 1 hard thing is `polaris-brand-lp`** (4.05 score, 4-channel signal spread, no Richard artifact on file). The daily-brief-latest.md file still lists Testing Doc for Kate as the hard thing — it's stale vs the corrected ledger. This brief uses the corrected ledger. Testing Doc moves to Core #2 as the visibility recovery action with Brandon, not the strategic hard thing.

---

## 1. Priorities

Top-3 time-ordered queue (clock-anchored where possible):

1. **10:00 PT — MX forecast to Brandon with decay narrative.** MX is 🔴 150.1% spend / 128.8% regs MTD. A 10 AM send without a decay narrative hands Brandon ammo for a question Richard can't answer live. This is the highest-urgency item of the day. **[L2 — Drive WW Testing / MX market ownership]**

2. **Before 1:30 PT — Polaris brand LP POV to Brandon.** This is the hard thing per `main.hard_thing_now` (rank 1, score 4.05, valuable-and-avoided, 4 channels: Dwayne Brand LP consolidation + MCS-3004 Italy revert + Andrew CTA work + -30% CVR narrative). 3d in the ledger with zero Richard artifact. Not a "work session" — a written POV with a recommendation, sent as a DM or Loop comment. Kills two birds: reclaims the narrative from Dwayne's consolidation effort AND is the Level 2 deliverable the system keeps flagging. **[L2 — Drive WW Testing]**

3. **Before WBR cut (EOD) — Reply to Yun-Kang on MX NB -19%.** 0.9d unanswered, blocks WBR publish. Pacing tie-in: the -19% story needs to coexist with the 150% spend story in the same callout. Yun shouldn't publish blind. **[L2]**

Secondary priorities (not on the clock but non-negotiable today):
- **Testing Doc v5 → Brandon** (Core #2) — already PUBLISH verdict since 4/5 per amcc.md. This is a recovery-of-visibility send, not the hard thing. 10-min cover note + attach v5. If it doesn't go today, Brandon has zero artifact from Richard between 4/17 and the next 1:1. **[L1 — Sharpen Yourself / streak recovery]**
- **AU handoff doc update** — biweekly cadence + 5/5 framing per yesterday's 1:1 lock-ins. Committed to Brandon overnight. Short. **[L2]**

## 2. Leverage Move

**Scope and draft the AU weekly change aggregator today — even just a one-page design doc, not code.**

Brandon explicitly asked for this in yesterday's DM: "Scope Kiro weekly AU change aggregator." The window is 13 days to 5/5 handoff. Three reasons today is the right moment:

1. **It's a live ask from the skip-chain, not a Richard invention.** Brandon asked. That eliminates the "would anyone adopt it" risk that kills most L3 attempts — Brandon has already signaled adoption intent.
2. **It's the one L3 play with a forcing function.** The 5/5 AU handoff is a hard deadline. If the aggregator ships before 5/5, Brandon's team inherits a tool on day one, not an email. That's the "one tool adopted" metric for Level 3.
3. **5-principle check:** it passes #1 (reduces decision load for whoever inherits AU), #2 (structural — changes the default for how AU weekly reviews happen), #3 (subtracts the weekly manual scan), #6 (makes the right choice — using the aggregator — path of least resistance). Violates none. Device.md check: 3+ instances/week friction, teammate-adoption-plausible. ✅

What to produce today: a one-page scope doc with (a) data sources (DuckDB `ps.v_weekly` AU + Adobe AMO + change log CSVs), (b) output artifact (what Brandon actually sees — Loop? Slack digest? .xlsx?), (c) cadence trigger, (d) handoff-to-code plan. Don't build. Scope.

**Connection to Five Levels:** L3 activation. The other priorities this week all advance L2 (WW testing, market ownership). None advance L3. That's the imbalance this fixes.

## 3. Friction to Remove

**Structural change: pre-load the Brandon 10 AM MX forecast as a drafted Slack DM by 08:30 PT, not as a "compose when ready" task.**

Yesterday's 4-minute truncated 1:1 and 23-workday streak pattern are both symptoms of the same structural defect: **critical sends are classified as "work" rather than as "pre-loaded fires."** The Testing Doc is not unsent because it isn't written — it's PUBLISH-verdict since 4/5. It's unsent because the send step is unbounded ("when I get to it") rather than pre-composed and triggered.

**Proposal:** Extend the am-backend hook to pre-draft the Brandon send text for any `Priority_RW=Today + Core` task with status `ready-to-send` in Kiro_RW. Drop the pre-draft into `shared/context/active/brandon-drafts/YYYY-MM-DD-<task-slug>.md` during the 06:40 PT brief run. Richard copy-pastes; no composition load at 10 AM.

**Principle:** #2 Structural over cosmetic (altering pre-loaded content, not format) + #6 Reduce decisions, not options (the draft doesn't prevent rewriting — it makes sending the path of least resistance). Device.md check: Testing Doc, MX forecast, PAM reply, Yun WBR reply — 4 instances this week alone of "ready send delayed by composition friction." ✅

**Subtraction-before-addition check:** this adds a drafts folder and one hook step. What gets removed? The daily-brief's "TODAY'S TOP-3 ACTION QUEUE" section (Section 10) becomes redundant once the drafts exist — the drafts ARE the queue. Remove Section 10 when drafts are live.

## 4. Data Snapshot

**Streak & hard thing:**
- L1 streak: **1 workday at zero** (retroactively corrected 4/22 AM — was incorrectly 23d). Last Richard artifact shipped: Testing Approach v5 → karpathy 4/5.
- Hard thing (rank 1): **polaris-brand-lp**, score 4.05, incumbent since 4/20, zero Richard artifact. Runners-up: oci-rollout (3.10), au-cpa-cvr (2.80, partially addressed 4/21).

**MX + AU pacing vs OP2** (from `ps.monthly_pacing`, 2026-M04 MTD):
- **MX**: 🔴 regs 128.8% / 🔴 spend **150.1%** — both >+20pp from pace. Overspending and over-delivering regs, but cost ratio is broken. This is what the 10 AM Brandon send has to explain.
- **AU**: 🟢 regs 38.2% / 🟢 spend 36.2% — within ±10pp of early-month pace. Clean.

**Top-5 overdue Asana tasks** (from `asana.asana_tasks`, Richard-assigned, due < today):
1. Create FR accounts — **62d** (Engine Room, Not urgent — kill or archive candidate)
2. Source DE/IT/ES — **62d** (Engine Room, Not urgent — same)
3. WW redirect / Adobe Ad Cloud — **45d** (no routine, no priority — kill candidate per daily brief)
4. Make changes to AU/MX/PAM for the week — **29d** (recurring — convert or delete)
5. Paid App — **23d** (Engine Room, Urgent — blocked on Brandon PAM budget reply)

**System health:**
- DuckDB `ps_analytics`: fresh as of 2026-04-22T13:30Z (ops/signals/asana/ps/main).
- ⚠️ Hedy MCP: not in subagent roster today — no meeting-refresh capacity.
- ⚠️ SharePoint Loop: auth expired, `mwinit -f` needed to refresh 5 Loop pages (~24h stale).
- ⚠️ `motherduck_token` env var still missing for `hard-thing-refresh.py` — null-state shadow written locally both 4/21 and 4/22. The retrospective correction was made manually, not via the refresh script. Fix the token or the ledger will drift again.

## 5. Open Questions for Richard

Five binary/multiple-choice decisions, each answerable in <30s:

1. **Accept the corrected hard thing?** `polaris-brand-lp` is rank 1 per the ledger, not Testing Doc. If you accept, today's #2 priority is a written Polaris POV to Brandon. If you reject, we go back to Testing Doc as the hard thing and the ledger gets re-corrected. **y / n / revert-ledger**

2. **Kill the 44d WW redirect Adobe Ad Cloud task?** 45 days overdue, no routine, no priority set, flagged as kill candidate. **kill / keep / defer-1-week**

3. **Kill the 62d FR accounts + Source DE/IT/ES tasks?** Both 62d overdue, Engine Room, Not urgent. No signal activity in months. **kill-both / keep-both / keep-FR-only**

4. **AU aggregator scope today — Loop doc, Slack digest, or .xlsx output?** Pick one so the scope doc has a target artifact. **Loop / Slack / xlsx / Richard picks after reading Brandon's ask again**

5. **Pre-drafted Brandon send folder — approve the structural change?** Extends am-backend to write drafts into `brandon-drafts/`. No new tools; one hook step added, Section 10 of daily brief removed. **y / n**

---

## What to do next

Right now (before 08:30 PT): open Polaris-brand-lp channels (Dwayne's consolidation thread + MCS-3004 Italy revert + Andrew CTA) and start the written POV. This is the hard thing. 10 minutes of reading, 20 minutes of writing, one DM to Brandon before the 10 AM MX forecast goes.

Then 10 AM: MX forecast with decay narrative.
Then before 1:30 PT: Testing Doc v5 cover note + attach, send to Brandon. Recovery send, not strategic.
Then AU aggregator scope doc (1 page, 30 min).
Then Yun-Kang reply before WBR cut.

Answer the 5 open questions above before end of session so the system can execute.

---
*Generated 2026-04-22 per am-triage Daily Brief Output Format. Ledger conflict with daily-brief-latest.md flagged in header.*
