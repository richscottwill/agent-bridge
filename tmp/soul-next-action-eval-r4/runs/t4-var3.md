# AM Brief — Wednesday 2026-04-22 (PT)

*Format: am-triage Daily Brief Output Format. High-Stakes Clarity Check fired (MX 150% spend triggered high-stakes-guardrails). Internal clarity answers shaped Priorities + Leverage Move.*

---

## ⚠️ Correction up front
The previous brief (daily-brief-latest.md, 06:40 PT) still frames Testing Doc for Kate as the hard thing and the streak as "24 workdays at zero." **The tracker corrected retrospectively overnight:** Testing Approach v5 shipped 4/5. Streak = 1. Hard thing = **polaris-brand-lp** (rank 1, incumbent since 4/20, zero Richard artifact, 4-channel signal). The brief below reflects the corrected state.

---

## 1. Priorities

Ordered. Hard thing goes first because rank=1 has zero Richard artifact.

1. **🔥 THE HARD THING — Polaris WW rollout timeline one-pager** `[L2]`
   - Single-point-of-contact role assigned by Brandon 4/14. Overdue in current.md. 4 channels converged on you in 72h: Dwayne (consolidated feedback reply drafted, needs send), MCS-3004 Italy revert, Andrew CTA work, -30% CVR narrative.
   - **Minimum viable today:** publish the one-pager (dates + owners + status per market) + send the Dwayne reply with the 5 FAQs. Both already drafted in task descriptions. This is a ship, not a write.
   - Stop if: it's 11am and nothing is out — narrow to the Dwayne reply alone and time-box the timeline for tomorrow. Non-negotiable: one Polaris artifact lands today.

2. **📊 MX forecast to Brandon — 10:00 PT** `[L2]`
   - MX pacing 🔴 150% spend / 🔴 128.8% regs. Brandon send requires decay narrative. **High-Stakes Clarity Check active — see Section 4 guardrail box below.** Do not send a final number without explicit confidence + top-3 assumptions + human-review flag.

3. **🧪 Email overlay reply to Brandon — MCS-2553** `[L2]`
   - 3d unaddressed in Outbound Marketing Goals. Reply with MCS-2553 as the path. 2-minute Slack. Due 4/24.

4. **📋 Yun-Kang WBR reply — MX NB -19%** `[L2]`
   - Blocks WBR publish. Reply BEFORE WBR cut today. Data already in ps.v_weekly.

5. **🤝 AU handoff doc update** `[L2/L3]`
   - Brandon email today: biweekly cadence + 5/5 framing. Kate-visible. Commit: update doc today, not this week.

**Top-3 time-ordered queue:**
- **10:00 PT** — MX forecast to Brandon (with clarity-check guardrails — Section 4)
- **By 12:00 PT** — Dwayne Polaris consolidated-feedback reply sent
- **By 17:00 PT** — Polaris WW timeline one-pager published + Yun-Kang WBR reply

---

## 2. Leverage Move

**Ship the Polaris rollout timeline one-pager today, not the email draft or the Slack reply.**

- **What it is:** A one-page table: market × status × dial-up date × owner × next-step. MX, AU, DE, UK, FR, IT, ES, JP, CA, US-ES + US/JP (already live).
- **What it unblocks:** Four people currently asking you the same question in four different channels — Dwayne (consolidation), Andrew (CTA), Alex (Italy revert), Stacey (CA exclusion). Publish once, answer everyone. Replaces ~6-8 individual threads this week.
- **Why today is the moment:** You're named single-point-of-contact (Brandon, 4/14). The incumbent-since date is 4/20 — two days of zero artifact on a rank-1 hard thing activates the amcc escalation pattern. Every day without a published timeline is another day the organization reinvents the Polaris status conversation in DMs.
- **Level:** L2 (Drive WW Testing, single-artifact surface) with L3 spillover (teammates stop asking, you stop re-explaining — closest thing to tooling without building tooling).

Not a Testing Approach-scale artifact. 60-90 min. This is what "smallest, highest-leverage action" looks like when the hard thing is a coordination artifact, not a strategy doc.

---

## 3. Friction to Remove

**Structural fix: hard-thing-refresh.py is blocked on motherduck_token missing — both 4/21 and 4/22.**

- The hard thing re-computation is what caught the Testing Doc → polaris-brand-lp correction. Without it, the daily brief ran on stale state this morning and mis-framed the streak as "24 workdays at zero."
- Principle embodied: **#1 Routine as liberation.** The morning routine's value is that it eliminates "what's the hard thing" as a decision Richard has to make. When the refresh is broken, that decision leaks back into Richard's attention.
- **Proposed structural change:** add motherduck_token to the devspaces environment secret store (one-time action), and add a pre-flight check to am-backend that fails loud (not silent fallback) if the token is missing. Subtraction-before-addition check: this replaces the current "silent fallback to stale tracker + null-state shadow" with an explicit fail — fewer paths through the code, not more.
- **Not cosmetic:** changes a default (silent stale vs loud fail), not a format.

This is a 10-minute fix. Do it before close today so tomorrow's brief is on fresh data.

---

## 4. Data Snapshot

### Streak + Hard Thing (corrected 2026-04-22 AM)
- **Streak:** 1 day (Testing Approach v5 shipped 4/5 — was incorrectly inheriting forward 4/14–4/21)
- **Hard thing (rank 1):** polaris-brand-lp — score 4.05, valuable-and-avoided, 4 channels, incumbent since 4/20, zero Richard artifact
- **Rank 2:** oci-rollout (score 3.1)
- **Rank 3:** au-cpa-cvr (score 2.8 — borderline, Lena reply overnight may drop it off next refresh)

### Pacing (ps.monthly_pacing, 2026-M04 MTD)

**🔴 MX — HIGH-STAKES CLARITY CHECK ACTIVE (>$50K impact):**
- Regs: 128.8% (1,019 actual vs 791 pace-target)
- **Spend: 🔴 150.1% ($52,661 actual vs $35,085 pace-target) — overspend**
- Required before Brandon send at 10am:
  - [ ] Explicit numeric confidence score (not "medium")
  - [ ] Top-3 assumptions that would change the decay number (ie%CCP exponent, NB/brand mix, IECCP target 70 vs 75)
  - [ ] "Human review strongly recommended before action" line
  - [ ] IECCP target confirmed with Brandon (70 vs 75) BEFORE Lorena email — gates R&O reallocation
- Confirm IECCP target with Brandon at top of 1:1, don't infer.

**🟢 AU:**
- Regs: 38.2% / Spend: 36.2% — on pace for early-month (day 22 of 30 = 73% of month; AU runs back-loaded so this is normal).

### Top-5 overdue Asana tasks
1. Create FR accounts — 62d
2. Source DE/IT/ES — 62d
3. WW redirect / Existing customer reporting in Adobe Ad Cloud — 45d (kill candidate)
4. Make changes to AU/MX/PAM for the week — 29d (convert to recurring)
5. Paid App — 23d (blocked on Brandon PAM budget reply)

*Note: Testing Document for Kate still shows 22d overdue in Asana — the task wasn't marked complete when v5 shipped 4/5. Housekeeping: close the Asana task today (L1 hygiene, not the hard thing).*

### System health
- ✅ DuckDB MotherDuck: ps_analytics attached, ops/signals/asana/ps/main fresh as of 13:30Z
- ⚠️ Hedy MCP: unavailable in subagent roster — no meeting refresh today
- ⚠️ SharePoint Loop: auth expired — `mwinit -f` needed on local
- ⚠️ hard-thing-refresh.py: motherduck_token env var missing — see Section 3 for fix
- ⚠️ Karpathy Phase 6: invokeSubAgent nested-call limitation — blind eval blocked

---

## 5. Open Questions for Richard

1. **IECCP target 70 or 75?** Gates MX R&O reallocation + forecast decay math. Binary. 30 seconds with Brandon at top of 1:1.
2. **Polaris timeline format — Quip table or one-page .md?** .md is faster to ship (60 min) and lives in wiki. Quip is more stakeholder-readable. Recommend: ship .md today, upgrade to Quip tomorrow if Brandon asks.
3. **WW redirect task (45d overdue) — kill, or re-scope?** It's a kill candidate in current.md. If kill, do it in today's Admin block and recover 1 cap slot.
4. **Dwayne reply — send as-is (already drafted) or one more pass?** Draft is in task description. Recommend: send as-is, 8-minute copy-paste. Perfectionism on a reply is the exact pattern amcc flags.
5. **Add motherduck_token to devspaces secrets today, or file a Kiro-infra ticket?** 10 min local vs ~2 days ticket queue. Recommend: local today.

---

## Five Levels tie-back
- **L1 (Sharpen — consistent artifact):** Polaris timeline one-pager = today's L1 artifact. Streak goes 1 → 2 if shipped.
- **L2 (Drive WW Testing):** Polaris WW is the single largest L2 surface area right now. MX forecast send is L2 execution.
- **L3 (Team automation):** No direct L3 today. Brandon's "Scope Kiro weekly AU change aggregator" ask is queued — do not start until L1 artifact lands.
- **L4 / L5:** Not in scope today.

## Protocol alignment check (per soul.md "How I Build")
- ✅ #1 Routine as liberation — priorities ordered, decision eliminated
- ✅ #2 Structural over cosmetic — friction item is structural (env var + fail-loud default)
- ✅ #3 Subtraction before addition — friction fix removes a silent-fallback path
- ✅ #7 Human-in-the-loop on high-stakes — MX forecast guardrail box explicit
- ⚠️ #8 Don't build before investigating — no new tools proposed today; motherduck_token fix is configuration, not new tooling

---
Generated 2026-04-22 by am-triage protocol. Clarity Check (var3) fired on MX high-stakes trigger. Tracker override applied: hard thing = polaris-brand-lp (not Testing Doc).
