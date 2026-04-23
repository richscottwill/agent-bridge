# MX Polaris Gen4 Ad Copy Test — W13–W16 Readout

**Test:** Gen4 ("Business Pricing Exclusive") vs Gen3 control, 50/50 split
**Market:** MX, Polaris NB
**Duration:** W13–W16 (4 weeks), closed W16
**Spend:** $49.4K combined ($24.8K Gen4 / $24.6K Gen3)
**Design:** Detect ≥5% relative incrementality @ 80% power, α=0.05

---

## Topline

| Arm | Regs | Spend | CVR | CPA |
|-----|------|-------|-----|-----|
| Gen4 (treatment) | 612 | $24,800 | 4.10% | $40.52 |
| Gen3 (control) | 548 | $24,600 | 3.60% | $44.89 |
| **Delta** | **+64 (+11.7%)** | flat | **+0.50 pp / +13.9% rel** | **–$4.37 / –9.7%** |

Gen4 outperformed Gen3 on CVR and CPA over the full test window.

---

## Incrementality Estimate

- **Point estimate:** Gen4 drove +13.9% relative lift in CVR, or +75 incremental registrations vs a Gen3-only counterfactual at matched traffic (~14,927 sessions).
- **95% CI (relative):** [+1.7%, +27.5%] — the interval is wide but excludes zero.
- **Stat-sig:** Yes. Two-proportion z-test on CVR, z=2.26, **p=0.024** (two-sided).
- **Business translation (illustrative):** At a $100K/mo Polaris NB spend, Gen4 CPA ($40) produces ~240 more regs/mo than Gen3 CPA ($45) if the effect holds.

---

## Confidence: 45% (low-medium)

Three-way split per protocol:

- **Sign (high, ~85%):** Direction is robust. p=0.024, 95% CI excludes zero, CPA and CVR both move in the same direction, and the effect size (+13.9%) is large relative to the noise floor. Very unlikely this is a pure chance read in the wrong direction.
- **Magnitude (low, ~30%):** The CI is wide — [+1.7%, +27.5%]. **The test was badly underpowered for its stated design.** Detecting 5% rel at 80% power requires ~172K sessions/arm on a 3.6% baseline; we had ~15K. The actual MDE was +16.8% rel, meaning we're barely clearing the noise floor we could realistically detect. Any published magnitude ≥10% should be treated as an upper bound, not a point estimate.
- **Generalizability (low-medium, ~40%):** Single market (MX), single campaign type (Polaris NB), single creative refresh cycle. Gen4's message ("Business Pricing Exclusive") is pricing-led and may interact with MX-specific audience sensitivity to value messaging; we have no evidence it travels to US/EU5/JP/CA or to non-Polaris campaigns. Also: MX Polaris overall NB CVR dropped from 1.46% (W13) → 1.13% (W16), a 23% decline. The test arms are holding their internal split, but the category environment is softening.

**Why not higher:**
- Underpowered for the MDE the test was designed to detect
- No weekly Gen4 vs Gen3 CVR splits provided — cannot confirm the lift held in W16
- Category-level CVR softening in W15–W16 (market data) adds noise we can't isolate

**Why not lower:**
- Clean 50/50 split, equal spend, full 4-week run (not stopped early)
- Both CVR and CPA move together — internally consistent
- p=0.024 is not a marginal result

---

## Creative Fatigue Signal: **Plausible, Not Ruled Out**

Yun-Kang raised this in W15 (week 3 of the test). The aggregate readout can't answer it, and this is the single most important gap.

**What I checked (MX Polaris NB, market level, from `ps.v_weekly`):**

| Week | NB CVR | NB CTR | Pattern |
|------|--------|--------|---------|
| W13 | 1.46% | 13.1% | baseline |
| W14 | 1.33% | 13.8% | CVR –, CTR + |
| W15 | 1.32% | 14.8% | CVR flat, CTR + |
| W16 | 1.13% | 15.0% | **CVR –15%, CTR still +** |

This is the textbook creative-fatigue signature: **CTR rising (novelty keeps pulling clicks) while CVR falls (click quality degrades).** The market-level data includes both arms so it doesn't prove fatigue in Gen4 specifically, but it's directionally consistent with Yun-Kang's read.

**What I can't check without the weekly test splits:**
- Whether the +13.9% aggregate lift is driven by strong W13–W14 performance that converged to control by W16. A wearout pattern (Gen4: 4.6% → 4.4% → 3.8% → 3.6%) produces an identical 4-week average to a stable lift.
- Whether Gen4 CPA in W16 alone was still below Gen3 or had already caught up.

**If we had weekly splits, the decision tree would be:**
- Lift stable across all 4 weeks → scale Gen4 with confidence.
- Lift concentrated in W13–W14, gone by W16 → Gen4 is a novelty effect; don't scale without a refresh cadence.
- Lift growing over time → underpowered win, consider extending the test.

Right now we don't know which branch we're on. **That is the blocker on the scale decision.**

---

## Recommended Next Action

**Do not scale Gen4 beyond current allocation yet.** One-line version: the aggregate is real but we can't tell if it survived week 4, and the design couldn't cleanly detect the effect size we got.

**Two-step path forward:**

1. **This week — pull weekly Gen4 vs Gen3 splits (CVR, CPA, CTR by week × arm).**
   - If the lift held in W16 → proceed to step 2 as a scale plan.
   - If the lift decayed in W15–W16 → Gen4 is a novelty effect; re-plan as a rotation/refresh cadence rather than a new evergreen.
   - Owner: Richard + Yun-Kang. ~1 day of work.

2. **Based on step 1, either:**
   - **(If lift held)** Scale Gen4 to 100% in MX Polaris NB for W18–W21 as a holdout-style follow-up. Set an explicit kill criterion: CVR drops below W13 Gen4 level (4.1%) for 2 consecutive weeks → pause and refresh. Re-evaluate monthly.
   - **(If lift decayed)** Keep Gen4 in rotation at 40–50% with Gen3 and a new Gen5 variant as a 3-way test. Hypothesis for Gen5: pricing angle + different proof point (SMB segment or volume). Design for ~30K sessions/arm minimum (still underpowered for 5% rel, but gets us to a detectable ~12% rel MDE on this baseline).

**What I'd push back on:**
- Calling this a "win" without the weekly splits. The 4-week aggregate is not a scale decision by itself.
- Extrapolating to other markets. MX pricing messaging has its own dynamics (FX, value-messaging sensitivity) — any read-through to US/EU5/JP/CA needs its own test.
- Using this test as precedent for "4 weeks, $25K per arm is enough." It was underpowered for its own design. Future ad-copy tests on this baseline CVR need either longer runs or higher spend to actually deliver 5% MDE detection.

---

## Assumptions that would change the call

Per high-stakes protocol, the three assumptions most likely to change the outcome:

1. **Weekly splits show the lift held through W16** → confidence on magnitude jumps from ~30% to ~60%; scale recommendation flips to "yes, with kill criterion." This is the single biggest lever.
2. **The 23% W13→W16 NB CVR decline at market level reflects audience/category softening, not test interaction** → if the category is decaying and Gen4 just decayed slower, the "incremental" read overstates true lift. Directional impact: magnitude confidence drops another 5–10 pts.
3. **Gen4 creative was served evenly across audience segments and device types** → if impression distribution drifted (e.g., Gen4 over-indexed on mobile where CVR is structurally higher), the lift is partly a mix effect, not a copy effect. Would need impression share by segment to rule out.

---

## L2 Tie-in

This is L2 evidence (Drive WW Testing). Regardless of the scale call, the readout itself — with explicit confidence split, power-check against design, and fatigue rule-in/out — is the kind of written test status that should become the MX template. If we decide to scale, that's L2 → L1 flywheel. If we decide to retest, the protocol itself (power-check up front, weekly splits tracked, kill criterion pre-registered) is the artifact.

---

**Human review strongly recommended before action.** Specifically: pull the weekly splits before any scale decision, and confirm with Yun-Kang whether her W15 fatigue flag was directional intuition or tied to specific weekly numbers she's already seen.

---

*Analysis: two-proportion z-test on CVR (sessions back-solved from regs/CVR), 95% CIs via normal approximation and delta method on log relative risk, power check using standard two-sample proportion formula @ α=0.05, 80% power. Raw: Gen4 612/14,927, Gen3 548/15,222, z=2.26, p=0.024, CI_rel=[+1.7%, +27.5%], required n/arm for 5% rel MDE = 171,988, actual MDE = +16.8% rel.*
