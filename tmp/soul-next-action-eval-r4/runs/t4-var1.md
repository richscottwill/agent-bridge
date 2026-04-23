# AM Brief — Wednesday 2026-04-22 (PT)
*Generated under: soul.md + am-triage.md § Daily Brief Output Format + Conditional NBA Mandate (var1)*

NBA Mandate status: **ACTIVE**. Triggers that fired:
- High-stakes decision (MX 🔴 150.1% spend vs OP2 — leadership-visible, >$50K R&O reallocation on the line).
- ≥3 viable competing moves (Polaris timeline artifact, MX decay-forecast, Kiro AU aggregator L3 pitch, PAM reg-impact reply, Testing Doc re-anchor).
- Hard thing pivot detected (incumbent reset from `testing-approach` → `polaris-brand-lp` on 2026-04-22 refresh with no Richard artifact on file).

---

## 1. Priorities

The hard thing is now **polaris-brand-lp** (`main.hard_thing_now` rank=1, score 4.05, mode=valuable-and-avoided, `last_richard_artifact_date = NULL`). Per am-triage: hard thing takes Priority #1.

1. **🔥 Create the Polaris Brand LP rollout timeline artifact [L2 — THE HARD THING].**
   One page. Markets × owners × dates, US/JP live, FR/IT/ES/CA dialed, AU/MX/DE/UK/ES-MX/CA queued. Anchors Italy P0 status, the DDD decisions (4/16), and Brandon's "single point of contact" call (4/14). Ship to Brandon before 1:1. This kills the incumbent hard thing — first Richard artifact on Polaris since signal surfaced 4/20.

2. **MX decay-forecast to Brandon by 10:00 PT [L2].**
   MX is 🔴 150.1% spend / 🔴 128.8% regs vs April OP2. Brandon is waiting on the R&O reallocation narrative (Lorena tomorrow, ABIx cc). Without a written decay curve, Lorena email is unanchored and the ~$800K release has no numeric basis.

3. **Confirm IECCP target 70% vs 75% with Brandon [L2].**
   Promised to Lorena today in MX sync. Binary. 30-second answer. Gates the Lorena email.

4. **Scope Kiro weekly AU change aggregator [L3].**
   Brandon explicit ask in overnight DMs. 5/5 AU handoff is T-13d. An L3 tool teammates actually use before handoff closes = the first concrete L3 win. Proof-of-concept scope, not build.

5. **Reply to Yun-Kang on MX NB -19% in WBR callout Quip [L1].**
   Blocks WBR publish. Pacing shows regs at 128.8% MTD — the weekly -19% is period-shape, not a demand shock. One paragraph.

**Top-3 time-ordered queue:**
- **10:00 PT** — MX decay-forecast note to Brandon (pacing narrative + IECCP ask).
- **Before 1:30 PT** — Polaris timeline one-pager to Brandon (the hard thing).
- **Before WBR cut** — Yun-Kang reply on MX -19%.

---

## 2. Leverage Move

**Scope the Kiro AU weekly change aggregator — today, 30 min, scope-only (no build).**

- What it is: one-page PRD naming the three inputs (Google Ads change history export, OCI flag state, ref tag taxonomy diff), the weekly cadence (Monday before AU sync), the owner (Richard), and one success metric (Alexis/Lena stop asking "what changed?").
- What it unblocks/multiplies: Brandon asked for this in overnight DMs. AU handoff is **5/5 — T-13d**. Shipping an L3 tool *before* the handoff (not after) flips the handoff narrative from "Richard hands off AU" to "Richard hands off AU *and leaves the team a tool*". That's the first concrete L3 win in the Five Levels ladder (L3 is currently NEXT, unstaffed).
- Why today: the window is closing. After 5/5, AU is Alexis's problem and the aggregator becomes a retrofit. Before 5/5, it's a parting artifact — structurally different story.
- Principle: **How-I-Build #2 (Structural over cosmetic).** This changes a default (Richard doing manual change-log pulls → automated aggregation) rather than reshuffling existing work. Also **#8 (Check device.md)** — this clears the 3+ instances/week bar (every Monday AU sync + every Lena escalation).
- NBA Check: passes — `device.md` confirms recurring friction, teammate adoption is explicit (Alexis + Lena are downstream consumers).

**Next Best Action: Open a new file `shared/tmp/kiro-au-change-aggregator-scope.md`, write the 1-page PRD (inputs / cadence / owner / success metric), send link to Brandon via DM with subject "Scoping the AU aggregator before 5/5" — 30 minutes, today.**

---

## 3. Friction to Remove

**Yesterday's flow broke because the Brandon 1:1 was the *only* send-window for the Testing Doc, and when the laptop died, the artifact slid.** Root cause: the system treats Brandon 1:1 as a default send-point for artifacts that could be sent any time. That's an anti-pattern — it couples strategic artifacts to a fragile 30-min meeting slot.

**Proposed structural fix:** Add a rule to `am-triage.md` § Phase 2 — any task tagged Priority_RW=Urgent with "send", "ship", or "deliver" in the Next Action field must NOT have its execution scheduled against a meeting. It executes on the morning of the first clear block, independent of any calendar event. Meeting-coupled sends are the #1 cause of artifact slippage in the current streak data.

- Principle: **How-I-Build #2 (Structural over cosmetic)** and **#6 (Reduce decisions, not options)** — Richard can still hand-deliver in a meeting; the default just stops being "hold until meeting."
- Subtraction-before-addition check: this doesn't add a section. It adds one conditional to an existing phase. Subtracts the implicit "hold until 1:1" behavior.

---

## 4. Data Snapshot

**Streak + hard thing** (from `main.l1_streak` + `main.hard_thing_now`):
- Workdays at zero L1: **1** (reset 2026-04-22 after retro correction — Testing Approach v5 was shipped 4/5, incumbent ledger had been carrying it forward incorrectly 4/14–4/21).
- Hard thing: **polaris-brand-lp** (rank 1, score 4.05, mode=valuable-and-avoided, 4 channels, 0 Richard artifacts). Incumbent since 2026-04-20. 2nd: oci-rollout (3.1). 3rd: au-cpa-cvr (2.8, may fall off next refresh — partially addressed 4/21).

**MX + AU pacing vs OP2** (from `ps.monthly_pacing`, 2026-M04):
- **MX 🔴 regs 128.8% / 🔴 spend 150.1%** — both red, spend tier worse. 1,019 regs MTD vs 791 target; $52,661 spend MTD vs $35,085 target. Overpaced on both sides — the R&O reallocation narrative lives here.
- **AU 🔴 regs 38.2% / 🔴 spend 36.2%** — both red (>20pp under 100% pace). Max-clicks switch was 4/17–4/18; 4d in, account not checked. Combined with the -34% NB Polaris reversion, AU is underdelivering on both regs and spend.
- WW: no OP2 target loaded (`op2_regs_target IS NULL`) — data gap, not performance signal.

**Top-5 overdue Asana (assignee=Richard):**
1. Create FR accounts — **62d** (Engine Room, Not urgent — stale candidate, consider kill)
2. Source DE/IT/ES — **62d** (Engine Room, Not urgent — same)
3. WW redirect — Existing customer reporting in Adobe Ad Cloud — **45d** (no Routine, no Priority — kill candidate flagged 4/22 brief)
4. Make changes to AU/MX/PAM for the week — **29d** (no Routine — convert to weekly recurring or kill)
5. Paid App — **23d** (Engine Room, Urgent — blocked on Brandon PAM budget reply, 13d unanswered)

**System health:**
- DuckDB MotherDuck `ps_analytics` attached, current tables fresh (asana, ps, main, signals, ops all pulled within last 24h).
- ⚠️ `ops.data_freshness`: `loop_pages` is flagged stale (last updated 2026-04-21 14:07 UTC). SharePoint Loop auth — run `mwinit -f` on local to refresh.
- ⚠️ `hard-thing-refresh.py` still blocked on `motherduck_token` env var (noted 4/21, 4/22). Null-state shadow writes local; non-fatal but means the next refresh happens by hand.
- ⚠️ Hedy MCP not in subagent roster — no Hedy refresh this run. Historical meetings still queryable via `signals.hedy_meetings`.

---

## 5. Open Questions for Richard

1. **IECCP target — 70% or 75%?** Required before Lorena MX sync today. (binary)
2. **WW redirect task (45d overdue, no Routine, no Priority) — kill y/n?** Richard flagged it as kill candidate in yesterday's brief but didn't close. (binary)
3. **Polaris timeline artifact — ship as Quip one-pager or `.md` in wiki + SharePoint publish?** Quip = faster to Brandon; wiki = durable + searchable. (A/B)
4. **Kiro AU change aggregator — PRD today (30 min), or defer until after Polaris timeline ships?** Both are L2/L3 — only question is sequencing within today. (A/B)
5. **MX R&O reallocation — release ~$800K back to Mexico team as Brandon assigned, or gate on confirmed IECCP first?** If you answer Q1 first, Q5 collapses. (dependent binary)

---

## Next Best Action (NBA Mandate)

**Next Best Action: Write the Polaris Brand LP rollout one-pager (markets × owners × dates, 1 page max) and send to Brandon via DM before the 1:1 today. This is the hard thing and the first Richard artifact on the current top-ranked topic.**

---
Generated 2026-04-22 by agent under Conditional NBA Mandate (var1). Sources: soul.md · am-triage.md · current.md · `main.hard_thing_now` · `main.l1_streak` · `ps.monthly_pacing` · `asana.asana_tasks` · `ops.data_freshness` · daily-brief-latest.md (2026-04-22 v5.2.1).
