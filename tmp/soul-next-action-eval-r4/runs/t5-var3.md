# t5-var3 — High-Stakes Clarity Check (var3) on "45 min between meetings"

**Variant active:** soul.md + `shared/tmp/soul-next-action-eval-r4/proposed/var3-high-stakes-clarity-check.md`
**Timestamp:** 2026-04-22 midday PT
**Request:** "I've got 45 minutes between meetings — what should I work on?"

---

## Clarity Check trigger evaluation

Variant rule: activates **only** on tasks that trigger `high-stakes-guardrails.md`, **or** when preparing a recommendation with material business impact. Does not apply to routine/low-stakes work.

| Trigger condition | Fired? | Reasoning |
|---|---|---|
| Projection / forecast / test readout >$50K | **YES** | Top-3 action #1 in today's brief is MX forecast to Brandon at 10am PT with pacing at 150.1% spend. MX monthly burn >>$50K. Forecast decay narrative is a projection. If the recommendation routes Richard to this, guardrails apply. |
| Final business review | **No** | No MBR/WBR cut in this 45-min window. MBR callout is T-10d (5/2). |
| Material business impact on the recommendation itself | **YES (secondary)** | The *recommendation* of which slot to use 45 min on has material impact: Brandon 10am send is a time-boxed forecast commit, Kate-visible Testing Doc is 23 workdays at zero streak. Wrong call = another reset. |

**Result: Clarity Check FIRED.** Both questions applied internally below, and they shaped the final output.

---

## Internal application of the two Clarity Check questions

**Q1 — Single most important signal in the current context?**
The 10:00 PT MX forecast to Brandon. MX is pacing 150.1% spend (OVERSPENT, red), forecast decay is *required* before the send, and the brief pins it as Top-3 #1. It is a high-stakes projection (guardrails apply) with an external time box (10am PT). Everything else in the 45-min slot — including the Testing Doc send — has a later deadline (1:30 PT). The forecast has the earliest irrecoverable deadline.

**Q2 — Smallest, highest-leverage action that directly addresses it?**
Write and send the MX forecast email to Brandon with: (a) current MTD actuals (regs + spend vs OP2), (b) decay narrative explaining the 150.1% spend pace, (c) revised month-end projection with explicit numeric confidence (per high-stakes-guardrails.md), (d) top-3 assumptions, (e) human-review flag. Pull numbers from `ps.v_daily WHERE market='MX' AND period_start BETWEEN first-of-month AND today`. 45 min is enough if the email is scoped to decay-only — not a rewrite.

---

## Recommendation (what to work on in the next 45 min)

**Do: MX forecast email to Brandon. Ship before 10:00 PT.**

1. **Minutes 0–5** — Query `ps.v_daily` for MX MTD regs + spend + CPA. Cross-check against `ps.monthly_pacing` (150.1% spend figure). Note the top-3 drivers of overspend (likely CPC inflation, auction pressure, or volume — the daily rows will tell you).
2. **Minutes 5–25** — Write the decay narrative: what changed, why spend outpaced regs, what the revised month-end projection looks like. Apply high-stakes-guardrails.md: explicit numeric confidence (e.g., "70% CI on $X end-of-month spend"), top-3 assumptions named, human-review flag on the projection.
3. **Minutes 25–40** — Draft the email to Brandon. Use richard-style-email. Keep under 200 words. Lead with the number, then the decay, then the ask (IECCP 70 vs 75 confirmation — it's already on today's list and gates the R&O reallocation to Lorena).
4. **Minutes 40–45** — Send. Log the send. Move on.

**Do NOT spend this slot on the Testing Doc.** The doc has a 1:30 PT window, not a 10:00 AM window. Mixing them risks both slipping. The pattern from 4/21 (laptop outage consumed the send window) is exactly what happens when the hard thing gets queued behind a time-boxed commit. Sequence matters.

**After 10am send, the Testing Doc is the next hard thing** — it is still the #1 avoidance pattern (24 workdays at zero, v5 PUBLISH verdict since 4/5). Protect the 1:30 PT window for it.

---

## Guardrail / principle checks (soul.md "How I Build")

- **Principle 7 (human-in-the-loop on high-stakes):** FIRED. MX forecast is a projection with >$50K impact. Required behavior applies — explicit numeric confidence, top-3 assumptions, human-review flag. Called out in the Q2 action.
- **Principle 1 (routine as liberation):** Aligned. 10am send is a recurring commit; the routine says do it in the morning slot, not fit around it.
- **Principle 3 (subtraction before addition):** Aligned. Not proposing a tool, template, or new section — just the send.
- **Principle 8 (check device.md before proposing tools):** N/A (no tool recommended).
- **Agent voice:** direct per soul.md. No softening on the 24-workday streak reality or on the sequencing risk.

---

## Five Levels mapping

- MX forecast send: **L2** (Drive WW Testing — pacing discipline is the operational substrate that lets testing claims survive scrutiny).
- Testing Doc (deferred to 1:30 window): **L1** (Sharpen Yourself — consecutive weeks shipped).
- Both are active levels. Sequencing L2 before L1 in this 45-min slot is correct only because L2 has an earlier hard deadline today.

---

## What I did NOT recommend and why

- **Testing Doc v5 send in this window** — wrong deadline match. 1:30 PT window protects it better and v5 is already ready (10-min send, not a work session).
- **WW Sitelink Audit / AU handoff doc / refmarker PoC** — none of these have a 45-min hard deadline today. Lower leverage than the 10am forecast commit.
- **Admin 30-min block (Dwayne reply)** — Admin is capped at 30 min/day and is not the most important signal in the current context. Defer to end of day.

---

## Verdict

Clarity Check fired (high-stakes guardrails triggered on the underlying projection). Two-question framing changed the output — without it, the default would have pointed at the Testing Doc (the streak-anchored hard thing), which has a later deadline today and would have cost the MX forecast window. The check caught the sequencing risk.

**Action: MX forecast email → Brandon → before 10:00 PT. Testing Doc goes next, in the 1:30 PT slot.**
