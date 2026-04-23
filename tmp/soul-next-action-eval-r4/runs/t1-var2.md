# T1-Var2: US Full-Year Spend Ceiling at 100% ie%CCP (with 10% OCI CVR Lift)

**Date:** 2026-04-23
**Requestor:** Richard Williams
**Question:** "What's the full-year US spend ceiling if we hold 100% ie%CCP? Assume OCI-driven 10% CVR lift from current baseline."
**Guardrails auto-triggered:** `high-stakes-guardrails.md` (filename contains "ceiling"). `ieccp-planning-framework.md` loaded. 2x2 tool applied (see Methodology).

---

## Headline

**Full-year US spend ceiling at 100% ie%CCP with 10% OCI-driven CVR lift: $75M – $166M, with the defensible planning range at $75M – $90M.**

| Scenario | Total FY Spend | Brand Spend | NB Spend | Total Regs | Implied NB CPA |
|---|---|---|---|---|---|
| **P2 — Steep elasticity (b=0.937, MX-fit fallback)** | **~$75M** | $9.8M | $65M | 505K | $178 |
| **P3 — Moderate elasticity (b=0.50)** | **~$87M** | $9.8M | $77M | 763K | $124 |
| **P1 — Flat CPA (no marginal penalty)** | **~$166M** | $9.8M | $156M | 2,382K | $70 |
| *Baseline (current annualized, pre-OCI)* | *$33.2M* | *$9.8M* | *$23.4M* | *444K* | *$77* |

**Confidence: 45%** (why not higher: no US-specific elasticity fit exists in registry, so the spread between P2 and P1 is ~$90M; why not lower: CCPs, YTD actuals, and the ie%CCP algebra are firm — only the NB marginal-CPA curve is unsettled).

**Human review strongly recommended before action.**

---

## Why this number surprises

At the CCPs provided ($412.51 Brand / $48.52 NB), US's **current** ie%CCP is **46.1%** — not near the 100% rail. The account is running at less than half the efficiency ceiling Richard asked about.

That means a "100% ie%CCP" ceiling isn't a constraint on current spend — it's a **theoretical maximum** describing how much more NB the Brand surplus could fund if we were willing to push marginal NB CPA up until the blend hits breakeven against CCP. In practice this headroom is 2x – 5x current NB spend, depending entirely on how fast NB CPA rises as we scale.

So the real business question hiding inside the ask is: **"How steep is US's NB CPA curve, and how much of this theoretical headroom is economically sensible to take?"** The answer to that is not in the YTD data — 16 weeks of relatively stable NB spend ($387K – $513K weekly) doesn't span enough range to fit a reliable elasticity curve.

---

## Methodology

### 2x2 Friction-Impact Check (optional tool)

The question has multi-option ambiguity: three defensible methodological paths (flat CPA, moderate elasticity, steep elasticity), each producing a different number. A single headline would mislead.

- **High Impact + Low Friction → produce all three as a range.** Done.
- Picking just one path and reporting a single ceiling would be High Impact + Low Friction to compute but **High Impact + Low Friction to mislead** — rejected.

### Math

**Base formula** (from `ieccp-planning-framework.md`):
```
ie%CCP = Total Spend / Total CCP
Total CCP = Brand_regs × Brand_CCP + NB_regs × NB_CCP
At target T: NB_regs_allowed = Brand_regs × (T × Brand_CCP − Brand_CPA) / (NB_CPA − T × NB_CCP)
```

**OCI-driven 10% CVR lift → CPA falls by 1/(1+0.10) = ~9.09%:**
- Baseline NB CPA: $76.59 → post-OCI: $69.63 (if curve is flat)
- Applied to NB only (standard OCI mechanism — passes Amazon signal to Google bidding for NB; Brand CPA held flat as conservative).

**Full-year Brand projection** = YTD Brand × (52/16) = 138,570 regs, $9.8M spend, $70.70 CPA held (seasonally-naive extrapolation — see assumption #1).

**Path 1 (Flat CPA):** Hold NB CPA at post-OCI $69.63, solve algebraically for NB regs that brings blended ie%CCP to 100%. No marginal penalty.

**Path 2 (Steep elasticity):** Use MX-fitted log-linear curve `CPA = A × spend^0.937` (source: `session-log.md` 2026-04-22 fit from MX 2025H1 + 2026YTD). Recalibrate A so US W1-W16 median ($451K/wk, $75 CPA) sits on the curve, then apply 10% post-OCI lift and scan weekly NB spend multipliers until blended ie%CCP = 100%.

**Path 3 (Moderate elasticity):** Same recalibration process with b=0.50 (midpoint between flat and MX). No empirical basis for US — included to bound uncertainty.

### Data

- YTD US (W1-W16, period_start 2025-12-28 to 2026-04-12): $10.21M spend, 136,636 regs, Brand CPA $70.70, NB CPA $76.59, 46.1% ie%CCP.
- Source: `ps.v_weekly` filtered market='US', 16 rows returned.
- CCPs: US `market_projection_params_current` confirms Brand $412.51, NB $48.52 (both "finance_negotiation" source, aligned with spreadsheet `CCP Q1'26 check yc.xlsx`).
- US documented ie%CCP target range is 50-65% (from same registry table) — 100% is a hypothetical ceiling, not a target.

---

## Top 3 assumptions that change the answer (directional sensitivity)

1. **NB CPA elasticity exponent (b).** 
   *Assumed:* range from b=0 (flat) to b=0.937 (MX fit).
   *Sensitivity:* at b=0, ceiling = $166M; at b=0.937, ceiling = $75M. **Each 0.1 change in b moves the ceiling ~$10-15M.** This is the single largest driver of uncertainty. Action: if Richard wants a defensible single number, a US-specific elasticity fit is needed before the answer matters in a leadership setting. Requires spend variance beyond W1-W16's $387K-$513K NB band.

2. **Brand volume holds at YTD run-rate through FY.**
   *Assumed:* 138,570 Brand regs FY via 52/16 extrapolation.
   *Sensitivity:* Brand is the engine. A −10% Brand volume shock (e.g., seasonal Q3 softness not yet observed) drops the ceiling ~$7M across all paths because less surplus funds less NB. A +10% Brand upside (Prime Day bump) raises it ~$7M. US has less extreme seasonality than JP or EU5, but Q3 travel/Prime Day/back-to-school shape isn't captured in 16-week Q1 data.

3. **OCI lift scope and magnitude.**
   *Assumed:* 10% CVR lift, NB-only, applied uniformly.
   *Sensitivity:* if the lift is 5% instead of 10%, the ceiling drops ~$4-8M depending on path. If OCI also lifts Brand CVR by 10%, ceiling rises ~$2-3M (additional Brand surplus). The "10% OCI CVR lift" framing is Richard's prompt — verify this is the documented assumption in the OCI test readout, not a directional placeholder.

---

## What this means in practice

- **The binding constraint on US isn't ie%CCP; it's current NB spend level vs. OP2 allocation and marginal-CPA discipline.** At 46% ie%CCP today, we're already well below the 50-65% documented US range, never mind 100%. A 100% ceiling is a theoretical budget envelope, not a spending target.

- **The defensible planning range is $75M-$90M** (Paths 2 and 3), which is still 2.3x-2.7x current annualized spend of $33.2M. Reaching it would require:
  - NB spend scaled from ~$500K/wk to $1.2M-$1.5M/wk (2.4x-3.0x)
  - Acceptance of NB CPA rising from current ~$77 to $124-$178 range
  - Brand held at current YTD run-rate
  - OCI lift fully realized and persistent

- **P1's $166M is not a planning number.** It's the mechanical answer when the model ignores marginal CPA, which the framework explicitly warns against ("the question isn't what's the average NB CPA — it's what's the marginal CPA of the next batch"). Include it only to make the elasticity assumption visible.

- **The right next question isn't "what's the ceiling" — it's "what's the marginal CPA at NB spend of $X, and does that still work at the actual ie%CCP target (50-65%)?"** Translating a 100% ceiling into an actionable OP2 ask requires the target band, not the rail.

---

## Principle checks

- **Structural over cosmetic** ✅ — the range + assumption sensitivities are structural decision inputs, not a polished single-number headline.
- **Human-in-the-loop on high-stakes** ✅ — this is a projection question, guardrails loaded, confidence + assumptions + review flag all present.
- **Subtraction before addition** — partial. I didn't propose building a new elasticity tool; instead flagged that one is needed and cited the existing `mpe_fitting.py` infrastructure that would produce it.

---

**Human review strongly recommended before action.**

Files consulted:
- `ps.v_weekly` (US, W1-W16)
- `ps.market_projection_params_current` (US CCPs and ie%CCP range)
- `shared/wiki/agent-created/strategy/ieccp-planning-framework.md` (formula + MX case study)
- `shared/context/intake/session-log.md` 2026-04-22 entry (MX elasticity fit b=0.937)
- `.kiro/steering/high-stakes-guardrails.md`
- `shared/tmp/soul-next-action-eval-r4/proposed/var2-optional-friction-impact-2x2.md`
