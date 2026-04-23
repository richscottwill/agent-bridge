# MX Polaris Gen4 Ad Copy Test — W13–W16 Readout

**Active steering:** soul.md + performance-marketing-guide.md + One-Move Rule (var2)
**Spend in scope:** $49.4K total. Above $50K threshold is borderline — treating as high-stakes, human review recommended before scaling.

## Headline
Gen4 ("Business Pricing Exclusive") beat Gen3 control by +13.9% relative CVR (4.1% vs 3.6%), –9.7% CPA ($40 vs $45), two-sided p = 0.024. Result is statistically significant at the pre-registered 5% threshold, but the 95% CI on relative lift [+1.7%, +27.5%] straddles the designed MDE (≥5%), so the lower bound sits just above the stopping rule — not a decisive win.

## 1) Incrementality Estimate
- **Point estimate:** +13.9% relative CVR lift (+0.5 pp absolute), –9.7% CPA.
- **95% CI (relative lift):** [+1.7%, +27.5%]. Lower bound barely clears the +5% MDE.
- **Absolute reg delta:** +64 regs on matched spend ($24.8K vs $24.6K).
- **Caveat:** 50/50 split with matched spend cleans out most allocation bias. No obvious external shocks called out for MX during W13–W16, but should verify against `ps.v_weekly WHERE market='MX'` to rule out seasonality confound before scaling.

## 2) Confidence
- **Sign:** HIGH. Z = 2.26, p = 0.024, CI excludes zero. Direction is real.
- **Magnitude:** MEDIUM. CI is wide (+1.7% to +27.5%) and centered above the designed MDE, but the lower tail is close enough that a +5% true effect is plausible. Test was sized for ≥5% detection at 80% power and the observation is near 2σ — consistent with a real but not-fully-pinned effect.
- **Generalizability:** MEDIUM–LOW. Single market (MX), single quarter, single copy variant vs single control. "Business Pricing Exclusive" messaging may be MX-specific (pricing-sensitivity context) — do not assume transferability to AU/US/EU5 without retest.

## 3) Creative Fatigue Signal — Yun-Kang's Week 3 Concern
- **Data needed to rule in/out:** weekly CTR and CVR trend by week for each arm (W13, W14, W15, W16). If Gen4 CVR is declining W→W while Gen3 is flat, fatigue is ruling in. If Gen4 CVR is stable or rising, fatigue is ruled out.
- **Not in the readout as provided.** The 4-week aggregate does not discriminate. Before scaling, I need weekly-trend decomposition — this is the single most important data gap.
- **Why it matters:** if fatigue is real, the +13.9% is an average over a decaying curve, meaning scaled performance will be below the point estimate. If fatigue is absent, the +13.9% is conservative (new reach will dilute less).

## 4) Recommended Next Action (with confidence)
**Do NOT full-scale to 100% Gen4 yet.** Two reasons:
- CI lower bound (+1.7%) is below the designed MDE (+5%). We have a directional win but not a decisive one relative to the stopping rule.
- Creative fatigue signal is unresolved. Scaling a fatiguing asset locks in the decay.

**Recommend:** shift to 80/20 Gen4/Gen3 while pulling weekly CTR/CVR decomposition + testing a Gen5 refresh variant in the 20% slot to de-risk fatigue. Re-read at W20.

**Confidence in this recommendation:** MEDIUM–HIGH. The statistical read is real; the operational caveats (fatigue, generalizability) warrant staged rollout rather than full cutover.

**Recommend human review before action** — spend in scope borders the $50K high-stakes threshold and full-scale decision affects MX OP2 pacing.

## Tough-but-fair questions Richard should expect
- "Your CI lower bound is below your designed MDE — why are you calling this a win?"
- "Yun-Kang raised fatigue in week 3 and you shipped a 4-week aggregate. Where's the weekly decomp?"
- "Does 'Business Pricing Exclusive' transfer to AU or is this MX-only? What's your read-across plan?"

## Top 3 assumptions
1. Spend was actually matched and unbiased across arms week-over-week (need to verify W-by-W).
2. No external MX-specific shock (competitor, seasonality, macro) during W13–W16 that co-moves with variant assignment.
3. Registration definition and attribution window are identical between arms.

---

**Next Best Action: Pull weekly CTR/CVR decomposition by arm (W13–W16) from DuckDB before making the scale/hold call — the fatigue question is the blocker and the aggregate hides it.**
