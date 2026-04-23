# Test Readout — MX Polaris Gen4 Ad Copy (W13–W16)

**Test:** Gen4 "Business Pricing Exclusive" vs Gen3 control, 50/50, 4 weeks
**Design:** ≥5% incrementality @ 80% power
**Stakes:** ~$49K spend across both arms; scale decision affects MX Q2 copy rotation
**Protocol applied:** Test Analysis Protocol (performance-marketing-guide.md)
**Tool used:** Optional Friction-Impact 2x2 (applied to next-action selection)

---

## Observed Results

| Metric | Gen4 | Gen3 | Delta |
|---|---|---|---|
| Regs | 612 | 548 | +64 (+11.7%) |
| Spend | $24.8K | $24.6K | +$0.2K |
| CVR | 4.1% | 3.6% | +0.5pp (+13.9% rel.) |
| CPA | $40 | $45 | -$5 (-9.7%) |

**Math reconciles.** Implied sessions: ~14.9K Gen4 / ~15.2K Gen3.

---

## 1. Incrementality Estimate

**Point estimate: +11.7% regs / +13.9% CVR / -9.7% CPA** — Gen4 beat Gen3 well above the 5% MDE this test was powered to detect.

**Statistical significance (two-proportion z-test on CVR):** z ≈ 2.25, p ≈ 0.024 two-sided. Significant at 95%, not at 99%.

**Counterfactual framing:** Both arms ran concurrently in the same market at 50/50, so this is a clean A/B — no counterfactual reconstruction needed. Unlike single-arm cutover reads, we're not asking "what would have happened otherwise"; we ran it.

---

## 2. Confidence (split)

- **Sign confidence: HIGH (≥85%).** p=0.024, lift is ~2.4x the MDE, direction is consistent with a material creative win.
- **Magnitude confidence: MEDIUM (~60%).** Point estimate 11.7% regs lift, but 95% CI on CVR lift spans roughly +2% to +26%. Don't plan against "we'll get +12% forever." Plan against +5% to +10% in steady state.
- **Generalizability confidence: LOW-TO-MEDIUM (~40%).** MX-specific, 4 weeks, one creative variant. We do not know if this transfers to AU/US, to other ad groups, or holds past fatigue horizon. Treat as an MX-Polaris-campaign result, not a global ad copy insight.

---

## 3. Creative Fatigue Signal

**Cannot rule in or rule out from the rollup alone.** The readout gives 4-week aggregates — I need weekly CTR and CVR trend by arm to address Yun-Kang's W3 concern.

**What to check before scaling:**
- Weekly CVR trajectory for Gen4: flat/rising = no fatigue; declining W3→W4 = fatigue confirmed
- Weekly CTR for Gen4: declining CTR with stable CVR = impression-side fatigue (audience saturation)
- Frequency / impression share by week: if Gen4 saturated its addressable audience by W3, the aggregate lift is biased toward early weeks

**Yun-Kang's concern is legitimate and currently unaddressed.** Scaling without answering it risks baking fatigue into the rollout math.

---

## 4. Recommended Next Action

**Scale Gen4 to 100% of MX Polaris — conditional on a 2-hour fatigue check first.**

**Preconditions (do before flipping traffic):**
1. Pull weekly CTR/CVR by arm for W13–W16 from DuckDB (`ps.v_weekly` or the test platform rollup)
2. If Gen4 CVR W4 ≥ 90% of W1 CVR → scale, confidence high
3. If Gen4 CVR W4 < 90% of W1 → shorter rotation recommended; pair Gen4 with a Gen5 variant in queue to avoid burn

**Do not:**
- Generalize Gen4 copy pattern to other markets yet (AU/US). Queue a follow-on test in one market only, not parallel rollout.
- Re-run the same test. The result is significant; re-running burns spend to re-confirm what we know.

---

## Friction-Impact 2x2 (applied to next action)

| | Low Friction | High Friction |
|---|---|---|
| **High Impact** | **Scale Gen4 in MX after fatigue check** (2-hr query, clear decision rule) | Generalize Gen4 pattern to AU/US (requires new test design, translation, legal review) |
| **Low Impact** | Re-run test (wastes spend, confirms what we know) | Build a fatigue-detection dashboard from one test's data |

**Default: top-left.** Scale after the 2-hour fatigue check. Break the generalization question into a sequenced follow-on — don't bundle it into the scale decision.

---

## Soul Principles Check

- **Structural over cosmetic (#2):** The fatigue-check precondition is structural — it changes the decision rule, not the presentation. ✓
- **Subtraction before addition (#3):** Rejecting "re-run the test" and "build a fatigue dashboard" preserves focus on the one decision that matters. ✓
- **Human-in-the-loop on high-stakes (#7):** Spend is ~$49K across arms, scale decision is sub-$50K monthly but close. Flagging for Richard confirmation before traffic flip. ✓

---

## Tie to Five Levels

**L2 — Drive WW Testing.** Every test readout is L2 evidence. This one is a clean win with a real methodological gap (fatigue signal not addressed in the rollup). The gap itself is portable: the **testing-methodology.md** should require weekly breakdown in every readout template, not just aggregate. That's a process improvement worth capturing.

---

## Open Items / Human Review

- [ ] Pull weekly CTR/CVR by arm (W13–W16) — required before scale decision
- [ ] Confirm with Richard: flip MX Polaris to 100% Gen4 pending fatigue check? (Y/N)
- [ ] Decide: queue Gen4 pattern test for one additional market (AU preferred — smaller, faster read) or hold
- [ ] Capture "weekly breakdown required in readout" as a testing-methodology.md update

**Recommend human review before action** — scale decision affects Q2 MX copy rotation and sets precedent for how the team treats fatigue signals in future readouts.

---

**Top-3 assumptions this analysis rests on:**
1. The 50/50 split was clean (no targeting/bid bias between arms). If bid optimizer favored one arm, lift is inflated.
2. Sessions are approximately symmetric between arms (~15K each, implied from CVR). If Gen4 got materially more impressions due to higher CTR, relative CVR lift is still valid but absolute reg volume projection changes.
3. Yun-Kang's W3 fatigue concern was creative fatigue, not a different confounder (seasonality, competitor spend, MX holiday). Worth confirming with her directly when pulling the weekly data.

**Numeric confidence in recommendation: 75%.** The scale call is right conditional on the fatigue check passing. If fatigue check fails, recommendation flips to "short rotation + queue Gen5."
