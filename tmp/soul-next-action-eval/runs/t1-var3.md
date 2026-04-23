# US Full-Year Spend Ceiling — 100% ie%CCP + 10% CVR Lift

**Confidence: 55%. Human review strongly recommended before action.**

This is a >$50K projection → high-stakes-guardrails.md applies. Ceiling math uses the supplied CCPs and the OCI-driven 10% CVR lift assumption directly.

---

## Quick Sort (applied before starting)

- **Impact:** HIGH — ceiling number moves Brandon/Kate/Lorena budget conversations; >$50M magnitude; high-stakes-guardrails auto-triggered by filename.
- **Friction:** LOW — YTD data is in `ps.v_weekly`; CCPs supplied; no elasticity curve fit required (US doesn't have one yet in `ps.market_projection_params` — MPE still in design).
- **Verdict:** High Impact + Low Friction → **do now**. No reason to schedule or break up.

---

## The Number

**FY26 US spend ceiling at 100% ie%CCP with 10% OCI CVR lift = ~$79.2M**

vs.
- Current FY run-rate (W1–W16 annualized): **$33.2M**
- Theoretical headroom to the ceiling: **~$46M**
- Ceiling without the CVR lift: **$71.98M** (the 10% lift adds $7.2M to the ceiling)

At the strategic balanced range from `ps.market_projection_params` (US ie%CCP range 50–65%, not 100%), the equivalent spend targets are:
- 50% ie%CCP: **$39.6M**
- 57% ie%CCP (current forecast strategy): **$45.1M**
- 65% ie%CCP: **$51.5M**

The 100% ie%CCP ceiling is a theoretical max, not a recommended target. Current balanced strategy operates at roughly 46% YTD (below the 50–65% band).

---

## How the Number is Built

**YTD actuals (W1–W16, `ps.v_weekly WHERE market='US'`):**
- Brand: 42,637 regs @ $3.015M spend (CPA $70.70)
- NB: 93,999 regs @ $7.199M spend (CPA $76.59)
- Total: 136,636 regs @ $10.214M spend; blended CPA $74.75; YTD ie%CCP = **46.1%**

**CCPs (from `ps.market_projection_params` — matches Richard's input):**
- Brand CCP $412.51, NB CCP $48.52

**FY extrapolation (simple 52/16 annualization from YTD run-rate):**
- Baseline FY Brand regs: 138,570; FY NB regs: 305,497
- With 10% CVR lift: FY Brand 152,427; FY NB 336,046

**Ceiling = FY_regs × CCP per segment:**
- Brand ceiling: 152,427 × $412.51 = **$62.88M**
- NB ceiling: 336,046 × $48.52 = **$16.30M**
- **Total ceiling: $79.18M**

CVR lift is applied as a reg-volume multiplier at the same CPC (CVR lift → lower CPA → can buy more regs per dollar → at ceiling you spend the full CCP pool of the larger reg base). Consistent with how MX's guardrails run was modeled (`shared/tmp/grok-eval/blind-eval/05A-verdict.md`) minus the elasticity curve (US doesn't have one yet).

---

## Top 3 Assumptions That Would Materially Change This

1. **The 10% CVR lift actually materializes and flows through to reg volume, not just CPA.** If OCI lifts CVR 10% but CPCs rise to absorb it (classic auction dynamic), the reg base doesn't grow and the ceiling stays at **$71.98M, not $79.2M** (–$7.2M). Every 1% of CVR lift lost = –$720K off the ceiling.
2. **YTD W1–W16 linearly extrapolates to full year.** H2 seasonality in US is materially different from H1 (Q4 retail surge, Prime events, holiday competition). If H2 reg volume runs +15% vs H1 pace, ceiling rises to ~$85M. If H2 runs –10% (competitor squeeze or macro softness), ceiling drops to ~$71M. This is the single biggest swing factor because the ceiling is linear in FY regs.
3. **CCPs hold at $412.51 Brand / $48.52 NB through year-end.** These are Q1'26 values seeded 2026-04-23. Finance re-cuts NB CCP regularly. At NB CCP = $40 (–17%), NB ceiling drops from $16.3M to $13.4M → total ceiling ~$76.3M (–$2.9M). Brand CCP is more stable; re-cuts there are rare.

**Not modeled (would lower the ceiling if included):**
- No elasticity curve for US — I'm treating regs as linearly-extrapolated, not as a function of spend. If US NB has a steep exponent like MX's 0.937, pushing toward the ceiling would run into CPA inflation before reg volume gets there. The MPE fit for US (`.kiro/specs/market-projection-engine`) will close this gap; today's number is an upper bound under "regs are exogenous" framing.
- No segment mix constraint — this assumes we can deploy the full $46M headroom without hitting diminishing returns in either arm.

---

## Why 55% Confidence (Not Higher)

- **Missing US elasticity curve** — MX has one (`NB CPA = 0.02 × spend^0.937`); US does not. The ceiling is computed under "regs are exogenous" framing, which systematically overstates what's actually spendable. A fitted curve would almost certainly produce a lower, more realistic number.
- **H2 seasonality unmodeled** — 16 weeks of actuals is Q1 plus 4 weeks of Q2. No Q3/Q4 history in the window. US has strong seasonal patterns that a straight 52/16 annualization ignores.
- **OCI CVR lift is a stated assumption, not a measured lift** — if the 10% doesn't materialize or only partially lands, the lift component of the ceiling collapses first.

## Why Not Lower (i.e., why it's 55 and not 35)

- **CCPs and YTD data are solid** — `ps.v_weekly` W1–W16 is complete and the CCPs match the exact values Richard supplied ($412.51 / $48.52 confirmed from `ps.market_projection_params`).
- **The ceiling math itself is arithmetically correct under the stated assumptions** — at 100% ie%CCP, spend = CCP pool; this isn't contested.
- **The $79.2M is clearly labeled as a theoretical ceiling, not a recommended target.** Decision risk is in what someone does with the number, not the number itself.

---

## Human Review Strongly Recommended Before Action

Do not cite $79.2M as a committed or achievable FY spend target. It is an upper bound under strong assumptions, above the strategic operating range (US ie%CCP band is 50–65%, balanced strategy — per `ps.market_projection_params`). If this feeds a Brandon, Kate, or Lorena conversation, pair it with the $45.1M figure at 57% (current balanced strategy) so the stakeholder sees the realistic target alongside the theoretical ceiling.

---

## What Richard Should Do Next

**Pre-empt the question "so should we go after the $46M headroom?" before anyone else frames it for him.**

Concretely, pick one — **not all three**:

1. **(Recommended — High Impact, Low Friction)** Send Brandon a two-line note with the ceiling AND the balanced-strategy target side-by-side: "*FY US ceiling at 100% ie%CCP + 10% OCI CVR lift = $79.2M. Balanced-strategy target at 57% ie%CCP = $45.1M. Current run-rate $33.2M. Headroom is real but gated on H2 seasonality holding, CCPs not re-cut, and CVR lift flowing to reg volume not CPC — want to co-own the framing before it surfaces in planning.*" This is the Level-1 artifact move: ship the framing, don't wait to be asked.
2. **(High Impact, High Friction — schedule if you have bandwidth)** File a task for the MPE US fit (`ps.market_projection_params` US entry for brand/nb elasticity curves) — that's what turns this from a linear extrapolation into a defensible projection. Don't do it yourself; route to the MPE work stream.
3. **(Reject)** Don't spend time building a full sensitivity table or Monte Carlo on this today. The three assumptions above cover 95% of the swing and the number is theoretical. Low marginal value vs. option 1.

**Default:** Option 1, today, before EOD.
