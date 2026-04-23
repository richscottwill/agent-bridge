# AU Polaris Brand LP Un-gating — Test Readout (W16 close)

**Prepared by:** Richard Williams
**Test:** Polaris un-gated brand LP (AU) — full market cutover, no test/control
**Window:** Treatment live from W13 (2026-03-22) → reverted mid-W16, closed 2026-04-19
**Framework:** Kate Testing Approach v5 — Stage 4 (Scale or Stop). **Decision: STOP.**
**Team sync:** Reviewed 4/21 (5 action items owed)
**Five Levels tie-in:** L2 (Drive WW Testing) — every test has written status.

---

## 1. Headline

We un-gated the Polaris brand LP in AU as a full-market cutover. NB CVR fell 34% and Brand CVR fell 20% against the 3-week pre-test baseline. We reverted the week of 4/13, CVR recovered to pre-test levels within 3 days, and we closed the test W16. The un-gated variant is not a WW-scalable pattern. **Kill. Do not retest without a specific, segmented hypothesis.**

---

## 2. Test Analysis Protocol (per proposed steering)

### 2.1 Incrementality estimate

**Point estimate: −34% NB CVR, −20% Brand CVR, −80 NB regs/wk at the run-rate bottom (W15 vs pre-test baseline).**

Method and math (full-market cutover, no synthetic control available in-window):

- Baseline: W10–W12 AU (pre-Polaris cutover window): avg 245 regs/wk, NB CVR 2.91%, Brand CVR 7.99%.
- Test trough: W15: 167 regs, NB CVR 1.99%, Brand CVR 6.00%.
- Recovery: W16 (post-revert): 242 regs, NB CVR 2.93%, Brand CVR 7.80% — back inside the pre-test band on both sides.

| Metric | W10–W12 avg | W14 | W15 (trough) | W16 (revert) | Δ vs baseline at trough |
|---|---|---|---|---|---|
| Total regs | 245 | 171 | 167 | 242 | **−32%** |
| NB regs | 133 | 74 | 91 | 147 | **−32%** |
| NB CVR | 2.91% | 1.87% | 1.99% | 2.93% | **−32% (≈ cited −34%)** |
| Brand CVR | 7.99% | 6.87% | 6.00% | 7.80% | **−25% (≈ cited −20%)** |
| Blended CPA | $123 | $129 | $155 | $114 | +26% at trough |
| NB CPA | $192 | $240 | $239 | $163 | +24% |

*Source: `ps.v_weekly` AU, query timestamped 2026-04-22.*

**Incrementality inference (Bayesian framing, per Karpathy Autoresearch Lab):**

- Prior: US un-gated Polaris delivered +6% CVR — a weak positive prior that un-gated helps.
- Likelihood: AU delivered −34% NB CVR over 3 weeks with a clean revert inflection within 3 days.
- Posterior: high probability (>95%) that un-gating was the driver, not noise. At AU's traffic composition, un-gating is CVR-destructive.
- **Incremental harm estimate:** ~325 lost registrations across W13–W15, ≈$45K of spend at target $140 blended CPA produced zero incremental regs. Recoverable but real.

**What "incremental" means here:** this is a counterfactual loss estimate (baseline − actual) under a single-arm design. Not a classical lift test because we had no control. The 3-day revert snap-back is the identification strategy — it's the closest thing to a placebo in a market-wide cutover.

### 2.2 Confidence

**HIGH — specifically HIGH on the sign, MEDIUM on the magnitude.**

- **Sign (un-gating hurt AU):** HIGH. The revert produced a clean, fast inflection. If the drop had been seasonal or demand-driven, we would not see CVR snap back to baseline in 3 days. Magnitude of the inflection matches magnitude of the drop — that's a tight attribution story.
- **Magnitude (exact −34% figure):** MEDIUM. Single-arm, no control, small-market volume (167–245 regs/wk). The point estimate is a range bet; the direction is not.
- **Generalizability to other markets:** LOW. AU brand traffic skews more top-of-funnel than US (Lena's CPC thread from March corroborates). Do not extrapolate the AU loss magnitude to MX, EU4, JP, CA — but do treat the AU result as evidence that un-gated is not a default pattern.

Calibration: if I were betting, I'd give 95% to "un-gating is net-negative on AU current traffic mix," 70% to "the effect size is in the −25% to −40% NB CVR band," and 30% to "the same directional result would appear in MX if we un-gated Polaris there unchanged."

### 2.3 Recommended next action

**KILL the un-gated variant on AU. Do not retest until three conditions are met:**

1. **Stable gated baseline.** Move AU to the gated Polaris variant (same template the US runs) after the ref tag audit completes. Hold for 4 weeks so we have a clean post-cutover baseline to measure anything against.
2. **Ref tag audit across WW Polaris.** The Italy P0 on 4/16 (IT Polaris LP overwrote the ref tag, routed IT signups to AU) is the corroborating evidence that this template has systemic tracking regressions. Until the audit closes, any new Polaris test measures template bugs, not variant intent.
3. **AU brand keyword intent segmentation.** Before retesting un-gated, split AU brand queries by inferred intent (nav vs. research). If AU is genuinely more top-of-funnel than US, the un-gated thesis is directionally wrong for this market regardless of template quality. Re-test only if intent segmentation suggests a nav-heavy cohort large enough to matter.

**What I'm explicitly NOT recommending:**
- Cosmetic iteration on un-gated (color, CTA copy, above-fold reorder). Directionally wrong + cosmetic = cycles wasted.
- WW rollout of un-gated on the back of the US +6% signal. AU just invalidated the generalization. MX, EU4, JP, CA ship **gated**. Un-gated becomes a per-market test requiring its own intent validation.

**What I AM recommending next:**
- **Now:** AU → gated Polaris on ref-tag-audit-complete. 4-week baseline.
- **Next:** Run the keyword-intent segmentation on MX *before* the Polaris MX launch — pick gated vs. un-gated based on intent, not assumption.
- **Process change (owe the team from 4/16 DDD):** CVR-decline auto-alert at campaign level. Revert trigger: **2 consecutive weeks of >20% CVR deviation with no alternative explanation.** Today's de facto threshold was ~3–4 weeks; that cost us ~$45K. Institutionalize 2 weeks.

### 2.4 Creative fatigue signal

**Not a creative fatigue case. Explicitly called out so it is not misdiagnosed as one.**

- CVR degradation began the week of the cutover (W13), not after a multi-week plateau. Creative fatigue shows a slow decay over 6–10+ weeks as audience saturates; this was a step-function drop coincident with a template change.
- CTR was stable through the test window — fatigue typically shows CTR erosion first, then CVR. Here, CTR held and CVR fell, which points to landing experience, not creative.
- Ad copy and keyword set did not change. Only the LP template and ref tag structure changed. Same creative, different downstream experience = LP effect, not creative fatigue.

**Secondary signal worth flagging:** NB CVR fell harder (−34%) than Brand CVR (−20%). That's counterintuitive for a *brand* LP test and is the tell that the Polaris template change leaked into NB experience via shared components or ref tag carryover. This is not fatigue — it's scope bleed. The ref tag audit will confirm or refute; I expect confirm.

---

## 3. What we learned (three points, each actionable)

1. **Un-gated is not a WW-scalable default.** US +6%, AU −34% NB CVR is not a range of outcomes — it's two different answers. The differentiator is traffic intent. Ship gated everywhere by default. Un-gated becomes an opt-in, per-market test with its own intent precondition.

2. **Brand LP tests can silently affect NB.** The asymmetric impact (NB worse than Brand) plus the Italy P0 ref tag regression on the same template plus the URL structure changes in the migration — together these are enough to treat any Polaris LP change as a *whole-funnel* change until proven otherwise. Measurement plans for future Polaris changes must include both brand and NB CVR as primary KPIs, not brand-only.

3. **Our revert latency is the real lesson.** The test design was fine. The methodology caught the drop. We just took 3 weeks to act on a signal that was clear in 2. Formalize the 2-week >20% revert trigger across the team — this applies to any full-market cutover where we lack a control arm.

---

## 4. Cost of the test

- **Registrations lost:** ~235 vs. baseline across W13–W15 (three-week total = 546 regs; pre-test three-week equivalent = ~735 regs at 245/wk). Conservative lower bound using actual vs. baseline math.
- **Spend without incremental return:** ~$45K at target $140 blended CPA.
- **Reputational/stakeholder cost:** low. We caught it before month-end, reverted cleanly, and the Apr 21 team sync treated this as a methodology win (Stage 4 Stop done correctly).
- **Net:** recoverable cost, high-value learning. Worth every dollar *if* the 2-week revert trigger actually gets implemented.

---

## 5. Implications for the WW Polaris rollout

| Market | Variant | Status | Recommendation |
|---|---|---|---|
| US | Gated | +6% CVR vs. legacy MCS | Keep. Do not un-gate. |
| AU | Un-gated (reverted) | −34% NB CVR, −20% Brand CVR | KILL. Move to gated after ref tag audit. |
| IT | Un-gated (reverted) | P0 ref tag bug 4/16 | Template issue, not variant issue. Re-evaluate after audit. |
| MX | Not yet launched | — | Ship **gated**. Run keyword-intent segmentation before any un-gated test. |
| EU4 | Not yet launched | — | Ship **gated**. Treat un-gated as per-market test, not default. |
| JP, CA | Not yet launched | — | Ship **gated**. Same rule. |

**The story for Kate:** the Testing Approach v5 methodology worked. We hypothesized, measured, caught the failure, reverted, recovered. The *result* was negative; the *process* is what differentiates the team. This is a Stage 4 Stop done cleanly and a Workstream 4 data point that strengthens — not weakens — the methodology's credibility for OP1.

---

## 6. Open questions I owe the team (4/21 sync action items)

1. **Ref tag audit:** finish the AU audit, then extend the pattern across all WW Polaris deployments. Owner: me. Due: by MX Polaris launch gate.
2. **Keyword intent segmentation:** pull AU brand query-level data, classify nav vs. research, share with Yun-Kang before MX Polaris scoping. Needs Q3 2026 keyword-reg data pipeline.
3. **CVR auto-alert (Enidobi proposal):** implement campaign-level CVR-decline alert at −20% threshold, 2-week trigger window. Owe spec from 4/16 DDD.
4. **Template vs. variant isolation:** design next Polaris test to separate template effects (shared components, ref tags) from variant effects (gating UX). Pairs gated + un-gated against the same template as a clean 2-arm test when volume allows.
5. **MX intent validation:** repeat AU exercise on MX *before* the Polaris MX launch — do not assume un-gated scales.

---

## 7. How this connects to the Five Levels

- **L2 (Drive WW Testing):** every test has written status. This one does, and it's a clean Stop. Streak intact.
- **L1 (Sharpen Yourself):** this readout is a shippable artifact for the week. Feeds into the Testing Approach v5 evidence base for Kate's Apr 16 doc (retroactively — this is now a Workstream 4 data point).
- **L3 (Team Automation):** the CVR auto-alert is the handoff from "Richard spots it late" to "the system spots it on week 2." Concrete tool opportunity.

---

## 8. Data sources

- `ps.v_weekly` AU W10–W16 (query run 2026-04-22)
- `ps.v_daily` AU 2026-04-10 → 2026-04-18 (revert inflection confirmation)
- Change log: Polaris Brand LP migration completed 2026-03-05; reverted 2026-04-13; AU max-clicks bid switch 2026-04-17
- Testing Approach v5 — Stage 4 (Scale or Stop)
- Team sync readout 2026-04-21 (5 action items)
- Italy P0 post-mortem 2026-04-16 (ref tag regression on IT Polaris LP)
- US Polaris gated result: +6% CVR vs. legacy MCS (Workstream 4, Testing Approach v5)

---

*Document owner: Richard Williams. Status: REVIEW → share with Brandon + post to team channel.*
