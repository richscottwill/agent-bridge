# Daily Brief — Wednesday 2026-04-22 (PT)

**Mode:** am-triage + soul.md + Optional 2x2 Tool (var2). 2x2 invoked below in §2 — Testing Doc v5 vs Polaris scoping note had surface ambiguity; 2x2 resolved it cleanly.

**Structural context shift (not in prior brief):**
- **OOO Thu 4/23 – Fri 4/25.** Today is the LAST working day for 3 days. Anything that needs to move before Monday must move TODAY.
- **DuckDB `main.hard_thing_now` now ranks #1 = `polaris-brand-lp`** (score 4.05, incumbent since 4/20, 4-channel convergence, no Richard artifact on file). Testing Doc is no longer the tracked hard thing — it has fallen out of the top-3, likely because the signal-driven hard-thing refresh has no visibility into the 24-workday L1 streak. The L1 streak is still the live wound.

---

## 1. Priorities

1. **🔥 Testing Document v5 → Brandon. 10-min send. [L1]** — `main.l1_streak` = 1 workday at zero (reset 4/21 after Brandon 1:1 was cut to 4min). v5 has PUBLISH verdict (8.4/10) since 4/5. Apply 5 critic fixes, 2-sentence cover email, hit send. This is not a work session — it is the send that ends the 24-workday avoidance pattern. No calendar conflict today. **Ship before noon PT so it lands in Brandon's queue before OOO.**

2. **MX R&O reallocation email to Lorena + IECCP target confirmation with Brandon. [L2]** — MX pacing 🔴 128.8% regs / 🔴 150.1% spend. Lorena expects the IECCP-driven reallocation note; Brandon assigned it in 4/21 team sync. Sequence: Slack Brandon "IECCP 70 or 75?" (1 line), then draft email to Lorena once confirmed. Must leave Richard's hands today — OOO starts tomorrow.

3. **ABIX Handoff Doc Loop input. [L2]** — Brandon presenting to Kate THIS WEEK. Richard hasn't contributed yet (current.md open item, 4/13). Kate-visibility. 20-min input, Loop doc link already shared.

4. **Polaris Brand LP — one-page scoping note (not the full artifact). [L2]** — `hard_thing_now` rank=1 signal is real (4-channel convergence: Dwayne Brand LP consolidation, MCS-3004 Italy revert, Andrew CTA, -30% CVR narrative). But shipping a Polaris POV today competes with Testing Doc and loses the 2x2. Scope it instead: title + 3-sentence thesis + 3 open questions + owner list. Unblocks artifact work post-OOO and puts a Richard artifact on the board so the signal doesn't drift unanswered into next week.

5. **Brandon PAM budget Slack reply. [L2/Admin]** — 18.6d unanswered, blocks Paid App PO chain. Reply with PAM reg impact numbers from tracker. ≤10 min.

**Top-3 time-ordered queue:**
- **08:30–09:00 PT** — Apply 5 critic fixes to Testing Doc v5.
- **09:00–09:10 PT** — Send v5 to Brandon (THE send).
- **09:15–10:00 PT** — Slack Brandon IECCP 70/75; draft Lorena R&O email; send once Brandon confirms.

---

## 2. Leverage Move

**Send Testing Doc v5 before 10 AM PT today.**

**What it is:** A 10-minute copy-paste-send. v5 is PUBLISH-verdict since 4/5. Five critic fixes, two-sentence cover email, send.

**What it unblocks/multiplies:**
- Ends the 24-workday L1 streak at zero in a single action. No other task on today's list moves Level 1 at all.
- Puts Richard's strategic artifact in front of Brandon BEFORE a 3-day OOO, so Brandon can review and surface to Kate without Richard in the loop. That's leverage — work happens while Richard is out.
- Breaks the pattern that has defeated 23 prior workdays: the task always slides because a last-moment barrier emerges (4/21: laptop outage cut Brandon 1:1 to 4 min). Sending first thing AM, before any meeting or ticket, defeats the barrier-emergence pattern structurally.

**Why today specifically:** Three compounding reasons:
1. **OOO wall.** 4/23–4/25 is out. A Monday 4/28 send compounds into 26 workdays and guarantees this drags into next week's 1:1s without a fresh send.
2. **Calendar is empty.** No Brandon 1:1, no blockers on the calendar today. Zero excuses available.
3. **2x2 unambiguous (optional tool invoked).**

| Option | Impact | Friction | Cell |
|---|---|---|---|
| Testing Doc v5 send | High (L1, ends 24-workday streak, Kate-visible strategic artifact) | Low (10-min send, v5 ready) | **HI / LO — default** |
| Polaris POV artifact | High (rank=1 signal, L2/L4) | High (no draft, requires scoping + writing) | HI / HI — break down, don't ship today |
| ABIX Handoff Loop input | High (Kate visibility this week) | Medium | Today, not the ONE |
| MX R&O email | High (money moves) | Medium (IECCP gate + narrative) | Today, not the ONE |

Testing Doc v5 is the only option in the HI-Impact / LO-Friction cell. The 2x2 makes the call for you — stop debating, send it.

**Five Levels tie:** L1 (Sharpen Yourself). This is the level Richard's been "struggling" at per soul.md, and today is the cleanest shot in a week.

---

## 3. Friction to Remove

**Structural friction:** The "hard thing" tracker (`main.hard_thing_now`) is signal-driven — it reads Slack, Hedy, email, meeting topics to surface what teammates are converging on. It does NOT read the L1 streak or check whether Richard has a pending artifact send already in flight. Result: as of this morning, the tracker says `polaris-brand-lp` is rank=1 with "no Richard artifact," while the real wound is Testing Doc v5 sitting unsent for 17 days post-verdict. The two sources disagree on what "the hard thing" is.

**Proposed structural fix (routes to karpathy):** Add one rule to `hard-thing-selection.md`: **if `l1_streak.workdays_at_zero >= 3` AND an artifact exists in a `verdict=PUBLISH` state without an associated send, that artifact is force-ranked #1 until it ships.** The signal-driven scoring then resumes on whatever's left.

**Principle embodied:** #4 Protect the habit loop. The L1 streak is the cue-routine-reward loop being actively practiced. The tracker currently lets the loop be silently overwritten by fresher signal noise, which is the opposite of protection.

**Subtraction-before-addition check:** Not a new tool — a single rule in an existing selection file. No new table, no new cron. Adds one SQL guard to a function that already runs.

**Route to:** `karpathy` (owns `hard-thing-selection.md` per soul.md routing directory). Flag, don't implement.

---

## 4. Data Snapshot

**Streak + hard thing:**
- `main.l1_streak` 2026-04-22 → `workdays_at_zero=1`, `artifact_shipped=false`, `hard_thing_name=polaris-brand-lp` (this is the tracker's view, not the real wound — see §3).
- `main.hard_thing_now` rank=1 `polaris-brand-lp` (score 4.05, no Richard artifact, incumbent since 4/20). Rank 2 `oci-rollout` 3.1. Rank 3 `au-cpa-cvr` 2.8.
- **Real wound:** Testing Doc v5, 17 days post-PUBLISH verdict, still unsent. Tracker can't see it.

**Pacing vs OP2 (April MTD, `ps.monthly_pacing`):**
- **MX: 🔴 regs 128.8% / 🔴 spend 150.1%.** OVERSPENT, regs ahead too but spend/regs ratio drifting. Decay narrative required for any Brandon-facing forecast this week.
- **AU: 🟢 regs 38.2% / 🟢 spend 36.2%.** On pace for early month (within the ±10pp band given day-of-month).
- **WW:** pacing % not populated (target fields null in view).

**Top-5 overdue Asana (from `asana.asana_tasks`):**
| Task | Due | Days OD |
|---|---|---|
| Create FR accounts | 2026-02-20 | 62 |
| Source DE/IT/ES | 2026-02-20 | 62 |
| WW redirect — Existing customer reporting in Adobe Ad Cloud | 2026-03-09 | 45 |
| Page Creation — Duplicate Beauty and Auto page for MX | 2026-03-23 | 31 |
| Make changes to AU/MX/PAM for the week | 2026-03-25 | 29 |

Top three (62d, 62d, 45d) are kill-or-revive candidates. Flag to §5.

**Calendar today:** **EMPTY.** No Brandon 1:1, no meetings. Full focus block available. OOO 4/23–4/25.

**System health:**
- DuckDB MotherDuck `ps_analytics` live. `ops.data_freshness` schema changed (source → source_name); brief-generator SQL needs a lint pass — not blocking today.
- `hard-thing-refresh.py` blocked 2 days running (4/21 + 4/22) — `motherduck_token` env var missing on the refresh runner. Tracker values dated 4/20. Flag for fix on return from OOO.
- SharePoint Loop auth still expired per yesterday's brief.

---

## 5. Open Questions for Richard

1. **Testing Doc v5: send now, or one more critic pass first?** Recommend: send now. 17 days post-PUBLISH verdict, OOO tomorrow.  **y / n**
2. **IECCP target: 70 or 75?** Required to unblock the Lorena R&O email today. **70 / 75 / defer-until-Brandon-replies**
3. **Polaris Brand LP — ship the scoping note today, or defer to post-OOO?** Recommend: scoping note today (20 min), full POV after return. **today / post-OOO**
4. **WW redirect Adobe Ad Cloud task (45d overdue, no routine, no priority) — kill it?** Richard flagged as kill-candidate yesterday. **kill / revive / defer**
5. **Flag the hard-thing-tracker fix to karpathy now, or post-OOO?** Structural friction write-up is ready in §3. **now / post-OOO**

---

*Generated 2026-04-22 by soul+am-triage+var2. Format conforms to am-triage § Daily Brief Output Format (required post-2026-04-22 A/B test).*
