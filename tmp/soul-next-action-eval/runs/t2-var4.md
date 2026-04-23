# MX Polaris Gen4 Ad Copy Test — W13–W16 Readout

**Active steering:** soul.md + performance-marketing-guide.md + Context-Action Trigger (var4)
**Framework:** performance-marketing-guide.md → Test Analysis Protocol (4-part). Staged reference: `shared/wiki/agent-created/testing/testing-methodology.md`.
**Spend in scope:** $49.4K over the test; scale decision governs ~$50K/month forward. Borderline high-stakes — human confirmation required before rollout (soul.md #7).

---

## Context → Action Trigger (applied before analysis)

**Q1. What is the single most important thing this context is telling me right now?**

The headline lift (+11.7% regs, +13.9% CVR, p≈0.024) looks like a win, but two signals in the context make the aggregate misleading: (a) the 95% CI lower bound on relative CVR lift is roughly +1.7% — *below* the pre-registered +5% MDE the test was powered to detect; and (b) Yun-Kang flagged creative fatigue in W3 and nothing in the readout resolves it. A 4-week aggregate hides the weekly decay curve. Scaling off this readout alone would lock in a possibly decaying asset at a magnitude we can't defend.

**Q2. What is the smallest, highest-leverage action that directly addresses it?**

Pull the W13→W16 weekly CTR and CVR trend by arm from DuckDB (`ps.v_weekly WHERE market='MX'` or ad-platform export) before making any scale/hold call. That single query resolves the fatigue question, and the fatigue answer gates the scale decision. Nothing else on the analysis path matters until that's in hand.

→ Proceeding to the four-part protocol with this action as the anchor.

---

## Inputs

| Arm | Regs | Spend | CVR | CPA | Implied clicks |
|---|---|---|---|---|---|
| Gen4 ("Business Pricing Exclusive") | 612 | $24.8K | 4.1% | $40 | ~14,927 |
| Gen3 (control) | 548 | $24.6K | 3.6% | $45 | ~15,222 |
| **Delta** | **+64 (+11.7%)** | +$0.2K (flat) | **+0.5pp (+13.9% rel)** | **−$5 (−11.1%)** | −295 |

---

## 1. Incrementality estimate

- **Point estimate:** +13.9% relative CVR lift, −11.1% CPA, +64 regs on matched spend.
- **Two-proportion z-test** (CVR 4.1% vs 3.6%, n ≈ 14.9K / 15.2K): SE(diff) ≈ 0.00222, z ≈ 2.26, **p ≈ 0.024** (two-sided). Significant at α=0.05.
- **95% CI on relative CVR lift:** roughly **[+1.7%, +27.5%]**. Clears zero; lower bound sits just above zero and *below* the designed +5% MDE.
- **Counterfactual framing:** concurrent 50/50 split — control arm *is* the counterfactual. No reconstruction needed.

Reads as a directional win that technically clears p<0.05 but barely clears the designed detection threshold at the lower bound. Call it real, don't call it large.

## 2. Confidence

| Dimension | Confidence | Reasoning |
|---|---|---|
| **Sign** | High (~90%) | p=0.024, CI excludes zero, CPA delta corroborates direction. |
| **Magnitude** | Medium–Low (~45%) | CI spans +1.7% to +27.5%. Point estimate almost certainly regresses on re-run. Durable effect plausibly ~+5–8%, not +14%. |
| **Generalizability** | Low–Medium (~35%) | Single market, single variant pair, single 4-week window. "Business Pricing Exclusive" may be MX-pricing-context-specific — do not extrapolate to AU/US/EU5 without a parallel test. |

## 3. Creative fatigue signal (Yun-Kang W3)

**Status: UNRESOLVED from the readout as provided.** The 4-week aggregate doesn't discriminate. To rule in or rule out:

- Gen4 weekly CTR trajectory W13→W16 (flat/declining = fatigue ruling in)
- Gen4 weekly CVR trajectory W13→W16 (same)
- Gen4 frequency / impression share trend
- Week-over-week lift delta — if Gen4's advantage is front-loaded and narrows toward control by W16, fatigue is real and the aggregate overstates durable lift

**Weak inference:** Yun-Kang flagged it W3; if fatigue were severe, the aggregate likely wouldn't have cleared p<0.05. Best guess is mild-to-moderate fatigue, not test-breaking. But "probably fine" isn't good enough for a $50K/month forward decision. Needs the weekly pull.

## 4. Recommended next action

**Do NOT scale to 100% yet. Staged next step:**

1. **This week (pre-decision):** Pull W13→W16 weekly CTR/CVR by arm. This is the Q2 action — nothing else gates on anything else.
2. **If weekly trend is stable or improving for Gen4:** Scale to 100% Gen4 on MX Polaris. Project forward lift at **+5–8% (conservative, not +14%)** — roughly +35–55 incremental regs/week at current spend pace.
3. **If weekly trend shows narrowing/decay by W16:** Shift to 80/20 Gen4/Gen3, queue a Gen5 refresh in the 20% slot, re-read at W20. Do not lock in a decaying asset at full scale.
4. **Parallel:** Queue Gen5 now regardless — next variant in the hopper so the next test is ready when Gen4 fatigues.
5. **Generalization:** Do NOT assume AU/US/EU5 lift. Run a Gen4-equivalent in AU (highest-leverage given hands-on coverage) before recommending WW rollout.

**Human review required:** Forward monthly spend affected is ~$50K — at the high-stakes threshold. Recommend Richard confirm the scale decision explicitly after the fatigue check resolves. Analysis does not auto-trigger rollout.

**Tie to Five Levels:** L2 (WW Testing). Log this in the testing dashboard (`ps-testing-dashboard.xlsx`) with written status regardless of outcome.

---

## Top 3 assumptions (top risks if wrong)

1. 50/50 split delivered as designed — not just budgeted. If delivery skewed by platform optimization, CVR comparison holds but spend comparison is suspect.
2. Gen4 and Gen3 ran against the same targeting, bidding, and landing page. If anything downstream differed mid-flight, result is confounded.
3. No MX-specific market event in W13–W16 (holiday, competitor promo, AB promo co-moving with variant rotation). Yun-Kang was watching — if he'd seen a macro confound he'd likely have flagged it alongside fatigue.

## Tough-but-fair questions Richard should expect

- "Your CI lower bound is below your designed MDE — why are you calling this a win?"
- "Yun-Kang raised fatigue in W3 and you're reading a 4-week aggregate. Where's the weekly decomp?"
- "Does 'Business Pricing Exclusive' transfer to AU, or is this MX pricing-context-specific?"

---

## Next step

**Pull W13→W16 weekly CTR/CVR by arm from DuckDB (`ps.v_weekly WHERE market='MX'` filtered to Polaris test tagging, or ad-platform export). The fatigue answer gates the scale decision. Target: before EOD Monday. Bring the weekly trend to Richard for the scale/hold call — do not auto-execute.**
