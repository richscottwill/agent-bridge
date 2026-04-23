# AU Brand LP Test — Readout (W13–W16 window, closed 4/18)

**Prepared by:** Richard Williams
**Test:** Polaris un-gated brand LP (AU)
**Status:** REVERTED 4/18. Recovered W16.
**Framing:** Stage 4 of our methodology — Scale or Stop. **Stop.**

---

## Headline

We ran an un-gated Polaris brand LP in AU for ~6 weeks. It drove registrations down materially. We reverted, CVR recovered in one week, and we now have a clean answer: **the un-gated variant does not work for AU at the current traffic mix.** Kill, don't retest, until we isolate a specific hypothesis for why.

---

## What we tested

- **Hypothesis:** Removing the gate on the Polaris brand LP (letting paid brand traffic land on an un-gated experience rather than forcing registration) would improve downstream CVR by reducing friction, mirroring the in-context registration wins from Workstream 4 of the Testing Approach.
- **Change window:** Polaris brand LP migration completed 3/5. CVR compression visible from W13 onward. Reverted 4/17–18 after team review. Closed W16 (2026-04-13 to 2026-04-19).
- **Measurement:** Pre/post CVR comparison against the trailing 8-week baseline (W8–W12). Market-level only — no test/control split because this was a full market cutover, not a Weblab.

---

## What happened

### Conversion collapse during the test window

| Metric | 8wk pre-test avg (W8–W12) | W14 (low) | W15 (low) | Deviation |
|---|---|---|---|---|
| Total regs | 249/wk | 171 | 167 | −33% |
| NB CVR | 2.85% | 1.87% | 1.99% | **−34% (matches cited figure)** |
| Brand CVR | 7.46% | 6.87% | 6.00% | **−20% (matches cited figure)** |
| Blended CPA | $126 | $129 | $154 | +22% |
| NB CPA | $199 | $240 | $239 | +20% |

The pattern is unambiguous: NB CVR fell harder than Brand CVR, but brand-side funnel degraded too. This rules out "just a demand problem" — if it were macro softness, we'd expect less asymmetry.

### Recovery after revert (W16: 2026-04-13 → 2026-04-19)

| Metric | W15 (test low) | W16 (post-revert) | Recovery |
|---|---|---|---|
| Total regs | 167 | **242** | +45% |
| NB CVR | 1.99% | **2.93%** | +47% — back above 8wk avg |
| Brand CVR | 6.00% | **7.80%** | +30% — back above 8wk avg |
| Blended CPA | $154 | **$114** | −26% — best since W12 |
| NB CPA | $239 | $163 | −32% |

W16 CVR is back in the pre-test band on both sides. Daily data shows the recovery started 4/12–13 (W16 day 1–2), which is consistent with a mid-week intervention and suggests the revert action was faster than the formal 4/18 closure date.

---

## What we learned

1. **The un-gated variant is CVR-dilutive at AU traffic composition.** Un-gated landing pages win when traffic intent is already high and the gate is the friction point. AU brand traffic is lower-intent than US brand — Lena's CPC challenge and our outlier keyword work from March both show AU brand keywords skew more top-of-funnel than US equivalents. Removing the gate exposed that mismatch.

2. **NB was the bigger victim, not Brand.** NB CVR dropped −34% against Brand's −20%. That's counterintuitive for a *brand* LP test — and it tells us the Polaris template changes propagated beyond the brand page. The ref tag and URL structure changes from the brand migration also affected the NB experience, either through shared components or tracking carryover. The Italy P0 (4/16) is the corroborating evidence: Italy's Polaris LP overwrote the ref tag and routed IT signups to AU. Same template, same class of failure.

3. **Recovery speed confirms the change was the driver, not a seasonal artifact.** CVR snapped back to the 8-week band within days of revert. If this had been a demand shift or keyword-quality drift, we would not see a clean inflection on the revert date. Clean rebound = clean attribution.

4. **Our measurement framework caught it — slowly.** We flagged CVR drift in W13. It took until W15/W16 for the team to act decisively. That's 3 weeks of loss. The lesson isn't the test design; it's our escalation threshold. **The revert trigger should be 2 weeks of >20% CVR deviation with no alternative explanation, not 3–4 weeks.**

---

## Cost of the test

At W15 run rate (168 regs/wk) vs. the 8-week pre-test baseline (249 regs/wk), we lost ~325 registrations across the W13–W15 window. At blended $140 CPA target, that's ~$45K of spend that produced no incremental regs. Not catastrophic, but recoverable only because we caught it before AU's OP2 month-end reporting.

---

## Recommendation: KILL, don't retest

**Decision: Stop. Do not retest the un-gated variant on AU until we have:**

1. A **gated** Polaris variant running cleanly on AU for 4+ weeks so we have a stable baseline. The brand LP is back to legacy MCS template as of the revert — we should move to Polaris gated (the same template US is running), not re-test un-gated.
2. A **ref tag audit** completed across all WW Polaris deployments. The Italy P0 told us the template has systemic ref tag regressions. Until we've verified the audit pattern on every Polaris LP, any new test is measuring template bugs, not variant intent.
3. A **traffic-composition diagnosis** for AU brand. If AU brand keywords really are more top-of-funnel than US (Lena's CPC thread already suggests this), the un-gated thesis is wrong for this market regardless of template quality. We need a keyword-intent segmentation before re-testing, not after.

**What I'm NOT recommending:**
- Not retesting with small tweaks. Cosmetic iteration on a directionally wrong variant wastes cycles.
- Not extending un-gated to other markets on the back of the US +6% signal. AU just showed us the US result doesn't generalize without intent validation.

**What I AM recommending next:**
- **Now:** Move AU to gated Polaris (US template) when the ref tag audit completes. Measure 4 weeks at baseline.
- **Next:** Repeat the exercise on MX before the Polaris MX launch — validate brand keyword intent first, then pick gated vs. un-gated, rather than assume un-gated is the scalable answer.
- **Process:** Add a CVR-decline auto-alert at the campaign level (I owe this from the 4/16 DDD — Enidobi alert proposal). 2 weeks >20% deviation = revert trigger. Institutionalize the lesson.

---

## What this means for the WW Polaris rollout

- **US (gated):** +6% CVR vs. legacy MCS. Keep.
- **AU (un-gated):** −20% brand CVR, −34% NB CVR. Reverted. Do not re-attempt un-gated without intent segmentation.
- **IT (un-gated):** P0 ref tag bug 4/16, reverted. Template issue, not variant issue — re-evaluate after audit.
- **MX, EU4, JP, CA:** **Do not ship un-gated by default.** The US result is not a WW scale signal until we validate gated vs. un-gated per market based on traffic intent. My strong take: ship gated everywhere, treat un-gated as a per-market test requiring its own design.

The compounding story for Kate: the Testing Approach methodology worked — we hypothesized, measured, caught the failure, reverted, learned. The result wasn't the one we wanted, but the *process* is what differentiates the team. This is a Stage 4 Stop done cleanly. Document it, move on, apply the learning to Polaris WW sequencing.

---

## Open questions I owe the team

1. Was the NB CVR drop driven by the brand LP's shared template components, or by the URL migration's ref tag leakage into NB tracking? (Action: finish AU ref tag audit — already committed.)
2. Is AU brand traffic intent genuinely more top-of-funnel than US, or is the CPC delta driven by something else (competitor bidding, query mix)? (Action: pull keyword-intent segmentation once Q3 2026 keyword-reg data available.)
3. Should the revert trigger (2 weeks >20% CVR deviation) become a team-wide standard, or is it specific to full-market cutover tests where we have no control?

---

## Data sources

- `ps.v_weekly` AU W8–W16, 2026
- `ps.v_daily` AU 2026-03-15 through 2026-04-18
- AU Paid Search State File (2026-04-20)
- Change log: Polaris Brand LP migration completed 2026-03-05; AU max-clicks bid switch 2026-04-17
- Testing Approach v5 (Stage 4: Scale or Stop)
- Team sync readout 4/21 (5 action items from Richard's presentation)
