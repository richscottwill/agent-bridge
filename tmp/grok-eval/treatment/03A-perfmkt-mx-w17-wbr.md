---
title: "MX W17 (Apr 19 to Apr 25)"
status: DRAFT
audience: WBR (Kate + marketing leadership)
owner: Richard Williams
created: 2026-04-22
reporting_week: 2026-W17 (partial; 3 of 7 days actual at draft time)
---

# MX W17 (Apr 19 to Apr 25)

MX is tracking to 408 registrations (-20% WoW) on $22.9K spend (-16% WoW), $56 CPA (+5% WoW), and 73% ie%CCP (vs. 100% target). April projects at $102K spend and 1.9K regs at $54 CPA (vs. OP2: +141% regs, +191% spend).

WoW we are not pulling budgets back. Brand is normalizing after the W15-W16 a.com "Special Pricing for Business" placement, settling from 395 to ~286 regs as incremental clicks thin out. NB is steady at ~122 regs on flat spend, blended CVR near 3.3%. I am treating the Sparkle lift as persistent with gradual decay, per Lorena's 4/22 readout.

YoY we spent -24% with +113% registrations at a -64% CPA. Brand drove it, +214% regs on Sparkle-lifted exact-match impressions. NB is efficient underneath, +21% regs on -39% spend, NB CPA -60%.

Note: W17 is partial, confirming with Lorena and Andes Friday.

---

## Business review context (for WBR walkthrough)

**Context.** MX is a March 2025 launch market running under a 100% ie%CCP ceiling. W15-W16 stepped Brand regs from ~180 to ~395 after an a.com on-site placement went live. The question this week is whether that step-up holds or was pull-forward.

**What moved.** W17 regs -20% WoW, spend -16% WoW, CPA +5%. Month-to-date April 1,205 regs / $62.8K through 4/18, pacing 128.8% of OP2 registrations and 150.1% of OP2 spend for the pre-W17 portion. Full-month April projects to 1.9K regs / $102K / $54 CPA.

**Why.**
- Brand: Sparkle placement is self-regulating as the novelty tail decays. W15 (367), W16 (395), W17 est (286). `ps.market_constraints` flags this as "likely persistent with gradual decay" based on Lorena's 4/22 read.
- NB: Third consecutive NB CVR decline (1.47%, 1.38%, 1.32%, 1.13% through W16). W17 NB is holding flat; the slide is the watchpoint, not W17's WoW.
- Seasonality: W14 was Semana Santa (-33% measured). W15-W16 partial recovery base, now normalizing.

**Risks & mitigations.**
1. Sparkle durability. If the on-site placement is withdrawn or reranked, Brand regs could revert toward the pre-W15 ~180/wk baseline, which would pull April close to ~$85K / 1.5K regs (still well above OP2, but a $17K swing). Mitigation: Lorena owns the placement; I am in her weekly sync to hear the call in advance.
2. NB CVR slide. Three weeks of decline is structural if a fourth week confirms. NB SQR pull in flight this week to isolate query-mix drift, LP issues, or competitor IS change before buying more expensive NB clicks.
3. OP2 staleness. April is on track to close ~2.4x OP2 regs and ~2.9x OP2 spend. OP2 was set before the Sparkle lift and before the ie%CCP target shifted. Treating it as the planning baseline for Q2+ will mis-read the headroom.

**Recommendation (confidence: medium-high).** Hold W18 spend at $23-25K, flat to W17. Do not scale NB until the SQR is reviewed. Restate the April close on Monday once W17 actuals land. Flag the OP2 gap to Kate at the WBR as a planning-baseline question, not a performance question.

**Confidence notes.** W17 regs point estimate is 408, CI 245-420 from `ps.forecasts` bayesian_seasonal_brand_nb_split (run 2026-04-21). MX forecast hit rate is 63.6% (avg error 16.3%), so treat the point as indicative, not committed. If W17 lands below the CI floor (245), that is the first real signal Sparkle is pull-forward rather than persistent.

**This projection assumes:** (1) the a.com "Special Pricing for Business" placement remains live through W17-W18; (2) NB CPC stays near $2 (flat for three weeks); (3) no incremental budget release from Lorena this week. If any of these shift, the April close moves by ~$8-15K.

**Budget note (>$50K scope).** The April close projection of $102K spend is above the $50K human-review threshold. Recommend human review before action. Specifically, I would like Kate's POV at the WBR on whether to formalize the uplift in the Q2 planning baseline or continue to treat each month's beat as a one-off against OP2.

## Tough-but-fair questions to expect

1. "If we're running 2x OP2 on spend and 2.5x on regs, why are we not already scaling NB?" Answer: ie%CCP is at 73% blended but NB is the expensive side, and the three-week NB CVR slide tells me scaling now would lift CPA before diagnosing the cause. SQR pull this week is the gate.
2. "Is the Sparkle lift real or is this a pull-forward?" Answer: W17 is the first post-Semana Santa week without the novelty tailwind. If Brand lands at ~286 (current projection), the placement is structural. If it drifts back toward ~220, it was pull-forward. We will know Friday.

---

## Supplementary data

**Weekly trend (regs):** W10: 297 | W11: 389 | W12: 323 | W13: 350 | W14: 303 (Semana Santa) | W15: 509 | W16: 510 | W17 (projected): 408

**W17 projection source.** `ps.forecasts` bayesian_seasonal_brand_nb_split, run 2026-04-21. Regs 408 (CI 245-420). Cost $22.9K. Brand 286 / NB 122. Method note: last week's actuals (W16) ingested; CI reflects Sparkle-persistence uncertainty.

**Data caveat.** `ps.v_daily` max date is 2026-04-18. W17 figures use the forecast above plus 3 days of partial actuals. Final W17 restated after Friday sync with Lorena and Andes.

**Anomalies (W16 baseline).** Brand regs +77% above 7-week avg (395 vs 224). Continuation, not anomaly; Sparkle is the mechanism. Watchpoint carried into W17: NB CVR 3-week slide at 1.13%.

**W18 recommended spend.** $23-25K. Hold Brand at $5.8-6.1K (Sparkle self-regulates), hold NB at ~$17-19K pending SQR outcome. Implied blended ie%CCP 72-75%, within ceiling.

**W18 watch.**
- Sparkle durability: Brand settling at ~286 = structural; drift toward ~220 = pull-forward.
- NB CVR: any weekday reading back above 1.3% is the recovery signal.
- April close restatement after W17 actuals land.

**W18 optimization.**
- NB SQR pull this week before any NB scale-up.
- Confirm ie%CCP working target with Brandon (70% vs 75%) ahead of the MX R&O transfer conversation.
- Día del Trabajo (May 1, Fri): ~5% single-day suppression, minor.
- Apparel LP test queued after Beauty/Auto cycle (Lorena, 4/21 sync).
