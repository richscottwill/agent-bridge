# Blind Eval — 03B AU Brand Test Readout

**Evaluator:** blind to arm identity. Scored ARM-X vs ARM-Y on 5 questions using architecture-eval-protocol.md rubric (PASS / REGRESS / NEUTRAL, evaluator calls the better arm per question).

**Inputs evaluated:**
- ARM-X: `shared/tmp/grok-eval/treatment/03B-perfmkt-au-brand-test.md`
- ARM-Y: `shared/tmp/grok-eval/control/03B-perfmkt-au-brand-test.md`

---

## Q1 — Factual equivalence

**Same incrementality estimate?** Broadly yes. Both land on the same core numbers:
- NB CVR −34%, Brand CVR −20% at trough (W15)
- W16 recovery back above pre-test band
- Blended CPA ≈$114 post-revert, ≈$154 at trough
- Cost of the test ≈$45K, ≈325 (Y) or ≈235 (X) regs lost

**Discrepancies:**
- **Baseline window differs.** ARM-X uses a 3-week pre-test baseline (W10–W12, avg 245 regs/wk, NB CVR 2.91%, Brand CVR 7.99%). ARM-Y uses an 8-week pre-test baseline (W8–W12, avg 249 regs/wk, NB CVR 2.85%, Brand CVR 7.46%). Same direction, slightly different anchor. ARM-Y's 8-week baseline is the more defensible choice for a single-arm market-cutover read; ARM-X's 3-week baseline is shorter and more vulnerable to pre-test noise.
- **Reg-loss magnitude differs.** ARM-X says "~235 regs lost (conservative lower bound)"; ARM-Y says "~325 regs lost." Both arrive at ≈$45K spend-without-return. The ~325 figure matches the math more cleanly against an 8-week baseline.
- **Test start framing.** ARM-X says treatment went live W13 (2026-03-22). ARM-Y says Polaris brand LP migration completed 3/5 and CVR compression visible from W13. Both are consistent with the input context (migration 3/5, revert 4/18), but ARM-Y is more accurate to the "~6 weeks" test window framing.

**Same next-action recommendation?** Yes. Both recommend:
- KILL un-gated on AU; do not retest without specific preconditions
- Move AU to gated Polaris (US template) after ref tag audit
- Ship gated by default on MX / EU4 / JP / CA; un-gated becomes per-market opt-in
- Keyword-intent segmentation before any un-gated retest
- Institutionalize 2-week / >20% CVR revert trigger (Enidobi alert, 4/16 DDD commitment)

The three preconditions for retest (stable gated baseline, ref tag audit, intent segmentation) are identical in substance across arms.

**Verdict: NEUTRAL.** Same conclusions, same next actions. ARM-Y's baseline choice is slightly more defensible; ARM-X's incremental-harm math is more explicit (Bayesian framing, explicit posterior).

---

## Q2 — Quality (stronger test readout)

Scoring criteria per prompt: incrementality + confidence + next action + creative fatigue signal + testing framework use.

**Incrementality:**
- ARM-X: explicit section (2.1) with point estimate, method, Bayesian framing (prior/likelihood/posterior), counterfactual framing, explicit acknowledgment that this is a counterfactual loss under a single-arm design with revert-as-identification strategy. Strong.
- ARM-Y: reports the numbers and the recovery math, notes "clean rebound = clean attribution," but does not frame incrementality explicitly as a counterfactual loss estimate and does not articulate the identification strategy. Solid but less rigorous.

**Confidence:**
- ARM-X: explicit section (2.2) separating sign vs magnitude vs generalizability, with quantified calibration bets ("95% to net-negative, 70% to −25% to −40% band, 30% to MX directional repeat"). This is textbook Bayesian calibration and maps cleanly to autoresearch-style decision making.
- ARM-Y: does not explicitly separate sign / magnitude / generalizability confidence. Implied in prose but not structured.

**Next action:**
- ARM-X: structured with three retest preconditions, explicit "NOT recommending" list, "AM recommending" list, timeline (Now / Next / Process change). Reads as a decision document.
- ARM-Y: covers the same ground with three retest preconditions, "NOT recommending" / "AM recommending" split, Now / Next / Process. Slightly more concise. Roughly equivalent quality.

**Creative fatigue signal:**
- ARM-X: explicit section (2.4) addressing fatigue head-on — rules it out with three pieces of evidence (step-function drop on cutover, CTR stable, ad copy unchanged). Flags secondary signal (NB fell harder than Brand → scope bleed, not fatigue). This is exactly what the eval prompt asks for.
- ARM-Y: **does not address creative fatigue at all.** The word "fatigue" does not appear. This is a meaningful gap — it's one of the four named criteria in the eval prompt.

**Testing framework use:**
- ARM-X: explicit Kate Testing Approach v5 / Stage 4 (Scale or Stop) tag in the header, Workstream 4 reference, Five Levels tie-in (L1, L2, L3). Actively positions this as a Stage 4 Stop "done cleanly" for Kate's OP1 evidence base.
- ARM-Y: references "Stage 4 of our methodology — Scale or Stop" and Testing Approach v5, but lighter on Workstream 4 / Five Levels integration. No L1/L3 tie-in.

**Verdict: PASS for ARM-X.** ARM-X is the stronger test readout. It hits all four of the eval prompt's named criteria (incrementality + confidence + next action + creative fatigue) with structured, quantified content. ARM-Y hits three of four — it misses creative fatigue entirely, which is the easiest gap to score against it.

---

## Q3 — Contradictions with data or framework principles

**ARM-X:**
- Baseline (W10–W12): 245 regs/wk, NB CVR 2.91%, Brand CVR 7.99%. Trough (W15): 167 regs, NB CVR 1.99% (−32%, text says −34%). Brand CVR 6.00% (−25%, text says −20%). The table honestly shows −32% and −25% then notes "≈ cited −34%" and "≈ cited −20%" — i.e., the cited headline figures don't exactly match the 3-week baseline math in the table. This is acknowledged transparently but is a mild tension.
- Claims `ps.v_weekly` AU W10–W16 as source. Consistent with data-routing conventions.
- Posterior claim ">95% un-gating was the driver" is a judgment call, framed as Bayesian — defensible under Testing Approach v5 framing.

**ARM-Y:**
- Baseline (W8–W12): 249 regs/wk, NB CVR 2.85%, Brand CVR 7.46%. Trough (W15): 167 regs, NB CVR 1.99% (−30%, text says −34%), Brand CVR 6.00% (−20%, matches). NB CVR −34% doesn't exactly match the 8-week baseline either (2.85 → 1.99 is −30%); the table header just says "matches cited figure" without showing the arithmetic. This is less transparent than ARM-X's version, where the discrepancy is visible on the page.
- W16 recovery dates: "Daily data shows the recovery started 4/12–13 (W16 day 1–2)" — this is a forward-looking claim that should be verified against daily data. Plausible but not sourced in the doc itself.
- Otherwise consistent with input framing and Testing Approach.

**Framework principles (Testing Approach v5 / Five Levels):**
- Both correctly frame this as Stage 4 Stop.
- Both correctly avoid the "cosmetic iteration" trap.
- Both correctly resist generalizing US +6% to WW.
- Neither contradicts the testing framework. ARM-X tie-in to L1/L2/L3 is more explicit but not a correctness issue.

**Verdict: NEUTRAL.** Both have minor arithmetic-vs-headline tensions that are common in mixed-baseline single-arm reads. ARM-X surfaces the tension on the page; ARM-Y glosses over it. Neither materially contradicts data or framework. Slight transparency edge to ARM-X.

---

## Q4 — Gaps

Scoring against the four gap axes in the eval prompt: creative fatigue analysis, Bayesian framing, kill/retest preconditions, Five Levels tie-in.

| Gap axis | ARM-X | ARM-Y |
|---|---|---|
| Creative fatigue analysis | **Present** — dedicated section, rules it out with 3 pieces of evidence, flags scope-bleed secondary signal | **Missing** — not addressed |
| Bayesian framing | **Present** — explicit prior / likelihood / posterior, quantified calibration bets | **Partial** — "clean rebound = clean attribution" is Bayesian in spirit but not structured |
| Kill/retest preconditions | **Present** — 3 explicit preconditions, structured | **Present** — 3 explicit preconditions, structured |
| Five Levels tie-in | **Present** — L2 in header, L1/L2/L3 dedicated section | **Missing** — no Five Levels reference |

Additional gaps to check:
- **Implications for WW rollout table:** both present, equivalent quality.
- **Cost of test:** both present; ARM-X adds reputational/stakeholder dimension.
- **Open questions / action items:** both present; ARM-X links to specific DDD/meeting commitments more explicitly (5 action items from 4/21 sync, tied to owners and due dates).
- **Data sources:** both present; ARM-X includes Italy P0 post-mortem and US Polaris result as evidence sources. ARM-Y includes the AU state file. Both defensible.

**Verdict: PASS for ARM-X.** ARM-Y has two material gaps (creative fatigue, Five Levels tie-in) and a partial gap on Bayesian framing. ARM-X covers all four axes explicitly.

---

## Q5 — Decision utility (which would Richard share with Brandon / Kate?)

Criteria: which doc actually drives decisions for the team and up the org?

**ARM-X pros:**
- Opens with a clear "STOP" decision, then delivers structured evidence.
- Bayesian calibration language ("95% / 70% / 30%") is the dialect of the Testing Approach v5 and autoresearch framing Kate is driving.
- Explicit table for WW rollout implications with per-market recommendation — easy for Brandon to lift into a WW sync or for Kate to use in the OP1 Testing Approach narrative.
- Five Levels tie-in positions the readout as L2 evidence and L1 artifact output — this is how Richard is supposed to be framing strategic work for Brandon/Kate.
- Explicit Workstream 4 data-point framing — directly feeds Kate's 4/16 Testing Approach doc retroactively.
- "The story for Kate" paragraph is written like a leadership talking point, not a data dump.
- Minor risk: the Bayesian framing section is dense. Brandon/Kate likely skim past "posterior >95%" unless they're already fluent.

**ARM-Y pros:**
- Slightly tighter prose, easier cold read.
- 8-week baseline is more statistically defensible if challenged in review.
- "The compounding story for Kate" paragraph is written well and is equivalent in thrust to ARM-X's version.

**ARM-Y cons:**
- No creative fatigue discussion — someone in the team review will ask, and the readout will be on the defensive.
- No Five Levels framing — misses the Richard-specific coaching context that Brandon uses in 1:1s.
- Bayesian framing only implicit. Less legible as Testing Approach v5 exemplar.

**Which would Richard share?**

Both are shippable. ARM-X is the one to send to Kate because it explicitly ties to the Testing Approach v5 methodology she's championing, it handles the creative-fatigue objection before it's raised, and it gives her a ready-to-lift paragraph for the Workstream 4 narrative. ARM-Y is the one to send to a fast reader who wants the bottom line — Brandon might prefer it for a quick 1:1 readout, but even there the Five Levels tie-in in ARM-X is closer to how Richard is being coached to frame his work.

**Verdict: PASS for ARM-X.** Stronger decision utility for the two named stakeholders (Brandon, Kate). ARM-Y is serviceable but would lose on direct comparison in the team review because of the creative-fatigue gap.

---

## Summary

| Question | Winner | Call |
|---|---|---|
| Q1 Factual equivalence | Tie | NEUTRAL |
| Q2 Quality (stronger readout) | ARM-X | PASS for ARM-X |
| Q3 Contradictions | Tie (slight transparency edge ARM-X) | NEUTRAL |
| Q4 Gaps | ARM-X | PASS for ARM-X |
| Q5 Decision utility | ARM-X | PASS for ARM-X |

**Overall: ARM-X is the stronger output on 3 of 5 dimensions; NEUTRAL on the other 2.** Per the architecture eval protocol rubric (APPROVED = 0 REGRESS, at least 1 PASS), if ARM-X is the "after" architecture, the change is **APPROVED**. If ARM-Y is the "after," the change is **REJECTED** (3 REGRESS from ARM-X's baseline on Q2, Q4, Q5).

**Key differentiator:** ARM-X explicitly covers all four of the named evaluation axes (incrementality, confidence, next action, creative fatigue) plus Five Levels tie-in, and uses structured Bayesian framing. ARM-Y misses creative fatigue and Five Levels entirely. Same underlying numbers, same next action, different discipline in framing.

**Non-differentiators:** Both arms get the core answer right (kill un-gated on AU, don't retest without preconditions, ship gated on remaining markets, 2-week revert trigger). A reader who only needs the answer is well-served by either. A reader who needs to *defend* the answer in a Kate-level review is better served by ARM-X.
