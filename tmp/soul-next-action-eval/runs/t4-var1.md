# AM Brief — Wednesday 2026-04-22 (PT)
## Run: t4-var1 (Next Best Action Filter applied)

Source: `shared/context/intake/daily-brief-latest.md` + `shared/context/active/current.md` + `main.hard_thing_now` + `ps.monthly_pacing`. Format: am-triage.md § Daily Brief Output Format. Filter: `var1-next-best-action-filter.md`.

---

## 1. Priorities

1. **🔥 Testing Document v5 → Brandon (before 1:30 PT 1:1)** — L2 + L1. **THE HARD THING.** 23 workdays at zero. v5 has PUBLISH verdict (8.4/10) since 4/5. Apply 5 critic fixes, 2-sentence cover, send. This is a 10-min send, not a work session.
2. **MX forecast to Brandon, 10:00 PT** — L2. MX pacing 150.1% spend / 128.8% regs vs OP2. Must ship with decay narrative. Stakes >$50K → high-stakes guardrails apply (numeric confidence, top-3 assumptions, human-review flag before send).
3. **Reply to Yun-Kang on MX NB regs −19% (before WBR cut)** — L2. Blocks WBR publish. Quip thread, 0.9d open.
4. **Reply to Brandon — PAM reg impact in #ab-paid-search-app** — L2. 18.6d unanswered, blocks Paid App PO chain. Pull numbers from PAM tracker.
5. **AU handoff doc update (biweekly cadence + 5/5 framing)** — L2. Brandon lock-in from yesterday's 1:1. Also queues the L3 "AU change aggregator" Brandon explicitly scoped.

**Top-3 time-ordered queue:**
- **10:00 PT** — MX forecast to Brandon (decay narrative, high-stakes guardrails)
- **Before 1:30 PT** — Testing Doc v5 to Brandon (hard thing)
- **Before WBR cut** — Yun-Kang MX −19% reply

---

## 2. Leverage Move

**Send Testing Doc v5 to Brandon before the 1:30 PT 1:1.**

- **What it is:** Apply the 5 critic fixes already identified in the 4/21 EOD log, write a 2-sentence cover, hit send. v5 is already in PUBLISH state (8.4/10). The work is done — the only remaining action is transmission.
- **What it unblocks / multiplies:**
  - Resets L1 streak from 23 workdays at zero → 0. Every subsequent L1 ship compounds off that reset, not off a broken streak.
  - Moves Testing Approach from "Richard's private WIP" to "Kate-visible strategic artifact" — the core L2 play for the quarter.
  - Removes the top cognitive tax from every Brandon 1:1 going forward (stops being "still working on it" for the 24th time).
  - Frees capacity to work the 7 other pending items (ABIX handoff, Italy P0, Enidobi alert, SIM updates, AU follow-ups) without the hard-thing debt sitting on top.
- **Why today is the right moment:** Yesterday's 1:1 collapsed to 4min from a laptop issue — that's the second consecutive "last-moment barrier" pattern. The brief calls it out explicitly: *"barrier emerges at the last moment, task slides."* The fix is to send BEFORE the 1:1, not during it. Send by noon PT and the 1:30 meeting opens with "v5 is in your inbox" instead of "still coming."

**Principles embodied:** Routine as liberation (stop re-deciding), Subtraction before addition (no edits — send what's ready), Protect the habit loop (send is the routine; this is the cue).

**Five Levels tie:** L1 (Sharpen yourself — artifact ships) AND L2 (Drive WW Testing — the artifact IS the testing methodology).

---

## 3. Friction to Remove

**Structural friction: "Send before the 1:1, not during it."**

Pattern across last 2 weeks: Testing Doc v5 is ready → Richard plans to discuss/send it *in* the next Brandon 1:1 → 1:1 gets truncated, canceled, or displaced → send slides another day. This has now happened twice in a row (4/14 and 4/21). The send is being coupled to the meeting as a trigger, and the meeting is an unreliable trigger.

**Structural change:** Decouple the send from the meeting. Pre-load the email draft into Outlook by 11:00 PT with subject + 2-sentence body + v5 attached. Schedule it to send at 12:00 PT unconditionally. The 1:30 PT 1:1 then becomes discussion of a received artifact, not the delivery mechanism for it.

**Principle:** Reduce decisions, not options (the send happens by default; Richard can still cancel but doesn't have to remember). Structural over cosmetic (changing the trigger, not the content).

**device.md check:** This is one structural change for one recurring pattern — not a tool. Don't build anything. Just draft + schedule.

---

## 4. Data Snapshot

**Streak + hard thing (`main.l1_streak` + `main.hard_thing_now`):**
- Workdays at zero: **24** (tracker latest 4/5 at 17; +7 workdays since, no artifact shipped; reset 4/21 from truncated 1:1)
- Hard thing rank 1: **polaris-brand-lp** (score 4.05, `valuable-and-avoided`, 4 channels, no Richard artifact on file, incumbent since 4/20 — still #1 after 2 refresh cycles)
- Rank 2: oci-rollout (3.10), Rank 3: au-cpa-cvr (2.80, partially addressed 4/21, may drop next refresh)
- **Note:** `hard_thing_now` flags **polaris-brand-lp** as the avoided signal. The daily brief currently frames **Testing Doc for Kate** as the hard thing. These are not the same artifact. Testing Doc is the stated L2 artifact; Polaris is the signal-driven one. Both need to ship. Testing Doc is today's send; Polaris rollout timeline (one-pager, owners, dates) is the next artifact to queue. Open question #2 below.

**Pacing vs OP2 (`ps.monthly_pacing` 2026-M04):**
- **MX**: 🔴 regs 128.8% / 🔴 spend 150.1% — overspent, forecast decay required before 10am Brandon send
- **AU**: 🟡 regs 38.2% / 🟡 spend 36.2% — on pace for early-month (Day 22 of 30 → ~73% expected; AU running cold at ~half expected, flag if month-end falls below 80%)

**Top-5 overdue Asana (from current.md pending list + brief):**
1. PAM US PO — 45d
2. WW redirect / Adobe Ad Cloud — 44d (kill candidate)
3. PAM R&O — 36d
4. Kingpin Goals MX — 31d (blocked on Andes)
5. Make changes to AU/MX/PAM for the week — 28d (convert to recurring)

**System health:**
- ✅ DuckDB: `ps_analytics` fresh as of 2026-04-22T13:30Z
- ⚠️ Hedy MCP: unavailable in subagent roster — no refresh today (signals.hedy_meetings still queryable, latest 4/21)
- ⚠️ SharePoint Loop: auth expired, `mwinit -f` needed on local (5 loop pages ~24h stale)
- ⚠️ `motherduck_token` env var missing on hard-thing-refresh.py — null-state shadow written locally, non-fatal
- ⚠️ Karpathy Phase 6: invokeSubAgent nested-call limitation blocks blind eval execution — logged as BLOCKER

---

## 5. Open Questions for Richard

1. **Send Testing Doc v5 at 12:00 PT unconditionally (scheduled send), or hold for live discussion?** → y/n
2. **`main.hard_thing_now` flags polaris-brand-lp as rank-1 avoided signal, but the daily brief frames Testing Doc as the hard thing. Which is today's hard thing — Testing Doc (ship v5), Polaris (draft rollout one-pager), or both (Testing Doc AM, Polaris PM)?** → A / B / C
3. **MX forecast for Brandon 10am: ship with written numeric confidence + top-3 assumptions per high-stakes-guardrails, or verbal on the call?** → Written / Verbal
4. **Kill the WW redirect / Adobe Ad Cloud reporting task (44d overdue)?** → Kill / Keep
5. **"Make changes to AU/MX/PAM for the week" (28d) — convert to weekly recurring (Engine Room) or retire?** → Recurring / Retire

---

## Next Best Action Filter — Applied

Running the filter on the proposed leverage move (**Send Testing Doc v5 before 1:30 PT**):

1. **Does this advance one of the Five Levels?** ✅ Yes — L1 (artifact ships, streak resets) and L2 (Testing Approach is *the* WW testing methodology artifact). Direct, not derivative.
2. **Is this the highest-leverage move available right now?** ✅ Yes. Comparison:
   - vs MX forecast (also L2, due 10am): MX forecast is earlier in the day but smaller in strategic weight — it's a single-period submission. Testing Doc is the quarter's defining L1/L2 artifact. Both ship today; Testing Doc is the higher-leverage move.
   - vs Polaris rollout one-pager (rank-1 avoided signal): Not drafted yet; no version exists. Testing Doc v5 is already at PUBLISH state — send-ready. Leverage of "ship a done artifact" > "start a new one."
   - vs PAM Slack reply (unblocks PO chain): Reversible in 5min. Lower leverage per minute than Testing Doc's compounding effect on streak + Kate visibility.
3. **Does this reduce future decisions or friction?** ✅ Yes. Removes the recurring "when do I send v5" decision. Ends the 23-workday incumbent. Unblocks every subsequent Brandon 1:1 from the "still coming" overhead.
4. **Is this within current context load?** ✅ Yes. v5 exists. 5 critic fixes already identified. No new organ loads required. Total: open v5, apply 5 edits, attach, cover, send.

**Filter verdict:** Proceed. Proposed leverage move survives all 4 gates.

**High-stakes check:** Testing Doc send is strategic but not >$50K in spend/forecast terms — standard guardrails sufficient, no numeric-confidence block required. MX forecast IS >$50K → high-stakes guardrails MUST apply (see Open Question #3).

---

## Next Step

**Draft Testing Doc v5 email to Brandon now. Pre-load in Outlook by 11:00 PT. Schedule send for 12:00 PT. Then work MX forecast with high-stakes guardrails for the 10:00 PT send.**

Shall I draft the cover email and the MX forecast framing, or are you handling those directly?
