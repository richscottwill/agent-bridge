# Blind Verdict — 05B: W17–W22 WW Regs Projection

**Evaluator context:** Blind. Scored without knowledge of which arm is control vs. treatment.
**Scope:** >$50K materiality, high-stakes forward projection for WBR / Brandon 1:1 use.

---

## Q1 — Factual equivalence

**Same underlying numbers? Mostly yes. Same methodology framing? No.**

Both arms pull the same `ps.forecasts` bayesian run and land on an identical raw point:
- Weekly points: 17,449 / 17,500 / 17,829 / 17,271 / 18,363 / 17,866
- 6-week raw total: **106,278**
- Conservative (summed) band: **59,049 – 123,630**

Where they diverge:
- **ARM-X** presents 106,278 as the central projection. It computes a *second* band via independent-RSS (~89k–117.5k 80% CI) and frames that as the defensible bet. It does not apply a bias correction.
- **ARM-Y** presents **~122,100 as the adjusted central projection** (model × 1.15) because it noticed the bayesian model systematically under-predicted W13–W16 actuals by 11–30%. It treats 106k as a floor.

**These are materially different headlines.** ARM-X says ~106k. ARM-Y says ~122k. The difference (~16k regs over 6 weeks) is well within the >$50K scope that matters. If ARM-Y's residual analysis is correct, ARM-X is understating by ~15%. If ARM-Y's correction is overreach (applying a 4-week bias on top of a model that already carries OCI priors), it could overstate.

**Verdict:** Same inputs, same raw point, but ARM-Y actively reinterprets the model output and ARM-X reports it near-as-is. Not factually equivalent at the headline level.

---

## Q2 — Quality (confidence, assumptions, uncertainty)

**ARM-Y is the better-constructed high-stakes projection.**

**Confidence bands:**
- ARM-X: Presents two bands (independent-RSS, conservative sum) and explains what each assumes. Good technical literacy. Adds a P10/P50/P90 summary. But leaves the model residual question unaddressed.
- ARM-Y: Explicitly diagnoses the summed band as "unrealistically pessimistic" and grounds its adjustment in observed residuals. States a numeric confidence score (60%) with a why-not-higher / why-not-lower split. Does *not* provide a proper independent-RSS or P10/P50/P90 — that's a gap.

**Assumption enumeration:**
- ARM-X: Has a caveats block (bayesian lower bounds, DE data continuity, no WW-level forecast, seasonality). Useful but reactive — lists risks, doesn't quantify sensitivity.
- ARM-Y: Has an explicit "Top 3 Assumptions That Would Materially Change the Outcome" block with directional sensitivity (±X% moves WW by ±Y). Names the US dominance (57% of WW), the OCI pacing for the 3 remaining markets, and the no-seasonality-break assumption. This is closer to how a >$50K bet should be framed.

**Forward uncertainty:**
- ARM-X: Three-scenario table with rough probabilities (50/35/15). Reasonable but the scenario bands overlap the point in ways that obscure action.
- ARM-Y: Ties uncertainty directly to the 3 live-last markets + US concentration + seasonality break. Asks a concrete clarifying question (which 3 markets are pending).

**Overall:** ARM-X is more technically thorough on CI math. ARM-Y is more honest about model bias and more decision-oriented on assumptions. For a >$50K forward projection, ARM-Y's structure (confidence score + top 3 assumptions + adjusted vs. floor) is the stronger guardrail pattern. ARM-X's probabilistic scenario table is nice but not a substitute for residual analysis.

**Edge:** ARM-Y, meaningfully.

---

## Q3 — Contradictions / misuse of data

**ARM-X:**
- States OCI is live at 100% in FR/IT/ES/JP/CA plus US baseline (= 6 markets). Then says "7/10 markets" per orchestrator framing. Then says "the 3 remaining are the APAC MCC–blocked tail (AU, UK, DE the likely gap)." That's internally inconsistent — if 6 live + US baseline = 7, and 3 are pending, which 3? Listing AU/UK/DE as "the likely gap" is a guess dressed as fact. AU is APAC but UK/DE are not. This reads like plausible-sounding framing without verification.
- Claims the point is "~10–15% above the W08–W16 WW actual mean (15.75k/wk)" — this is correct arithmetic but misses the more recent trend (W13–W16 is running materially higher than the W08–W16 mean, which ARM-Y catches).
- Does not flag that the model's own forecasts have been under-predicting recent WW actuals. That's a meaningful omission given the materiality.

**ARM-Y:**
- Explicitly says "I do not know which 3 markets are pending — please confirm." Honest admission rather than a guess.
- Cites W13–W16 residuals (−19%, −17%, −30%, −11%) as the justification for the 1.15× adjustment. If those residuals are real, the adjustment is evidence-based. If the residuals were pulled incorrectly (e.g., compared against forecasts from an older run rather than the same run), the adjustment is wrong. I cannot verify this from the artifact alone, but the reasoning is shown.
- Notes "did not layer a separate OCI uplift curve on top of the bias correction — the bias correction already absorbs most of the observed OCI effect." This is a defensible modeling choice and explicitly flagged rather than silently applied.
- Potential issue: ARM-Y's recommended adjusted range (106k–138k) uses the observed residual mean as a point correction but keeps the summed conservative band as the range. That's a mix-and-match that's not perfectly coherent. A cleaner treatment would re-derive a band under the corrected model.

**Verdict:** ARM-X has a factual slip (AU/UK/DE guess as the pending markets) and misses the under-prediction signal. ARM-Y's bias correction is aggressive but shown-and-defended. ARM-Y also handles the "which 3 markets" gap more honestly.

**Edge:** ARM-Y, though not clean — its bias correction warrants human scrutiny before citing in an artifact.

---

## Q4 — Gaps

Checking the 5 guardrails expected for >$50K scope:

| Guardrail | ARM-X | ARM-Y |
|---|---|---|
| Confidence score | Implicit (scenario probabilities) — no single number | ✅ Explicit **60%**, with why-not-higher/lower |
| Top-3 assumptions | Partial — caveats listed, not ranked as material drivers | ✅ Explicit "Top 3 Assumptions" section with directional sensitivity |
| Human review flag | ❌ Not explicit | ✅ "Human review strongly recommended before action" + concrete next steps |
| Material risks | ✅ DE continuity, OCI regression, seasonality | ✅ OCI pacing, US concentration, seasonality break |
| Caveats | ✅ Four listed | ✅ Three listed (scoring gap, no WW-native forecast, data-source freshness) |
| Methodology reproducibility | ✅ SQL shown | Partial — method described, no SQL shown |

**ARM-X gaps:** No explicit confidence score, no explicit human-review flag, assumptions not ranked for materiality.
**ARM-Y gaps:** No reproducible SQL, no P10/P50/P90 summary, mix-and-match of adjusted point with unadjusted band.

**Edge:** ARM-Y on guardrail coverage. ARM-X on reproducibility (SQL block is a nice touch that ARM-Y lacks).

---

## Q5 — Decision utility (Brandon 1:1 / WBR)

**For a Brandon 1:1:**
- ARM-X gives Richard a clean P10/P50/P90 number (95k / 106k / 117k) that drops straight into a conversation. If Brandon asks "what's the band," ARM-X has it. The scenario table is also conversation-ready.
- ARM-Y forces Richard to pick between the raw model point (106k) and the adjusted point (122k), and to defend the 1.15× correction. If Brandon pushes on the adjustment, Richard needs to be able to walk through residual math on the fly. That's harder.

**For a WBR narrative:**
- ARM-X gives a defensible number that matches what the model says. Safer from a "the forecast says X" standpoint.
- ARM-Y gives a more honest number that matches where actuals have actually been trending. More accurate if residuals hold, more exposed if they revert.

**Richard's posture (L5, legitimizing PS as strategic partners, evidence-based):**
- ARM-Y's structure — explicit confidence, ranked assumptions, human-review flag, honest "I don't know which 3 markets" — is the pattern of a strategic partner doing a >$50K bet. ARM-X's pattern is the pattern of a careful analyst reporting model output. Both are valid, but the soul context (legitimize PS as strategic, evidence-based, push on assumptions) favors ARM-Y's framing.
- That said, ARM-Y's bias correction is the kind of move that needs defending. If Richard hasn't personally verified the residuals, citing 122k in a leadership artifact is exposed. ARM-Y's "human review strongly recommended" is doing real work here.

**For WBR specifically:** The guardrail principle matters more than the headline number. ARM-Y's structure (confidence + assumptions + review flag) *is* the guardrail. ARM-X's structure is the projection with risk framing bolted on.

**Edge:** ARM-Y for strategic-artifact use, with the caveat that Richard must personally validate the residual analysis before citing 122k anywhere external. ARM-X is safer for "just repeat the model output" use cases, but that's not a >$50K-scope posture.

---

## Summary

| Dimension | Edge |
|---|---|
| Q1 Factual equivalence | Not equivalent. ARM-Y reframes the headline via bias correction. |
| Q2 Quality | **ARM-Y** |
| Q3 Contradictions | **ARM-Y** (ARM-X has a guessed AU/UK/DE pending-markets list and misses residuals) |
| Q4 Gaps | **ARM-Y** on guardrails; ARM-X on SQL reproducibility |
| Q5 Decision utility | **ARM-Y** for a >$50K WBR / 1:1 posture |

**Overall:** ARM-Y is the stronger artifact for the stated scope (>$50K, high-stakes, guardrails applied). Its bias-correction move is aggressive and requires Richard to personally validate before citing externally — but the structure (confidence score, ranked assumptions, human-review flag, honest gaps) is how you de-risk a forward projection at this materiality.

ARM-X is cleaner analytically (two CI methods, P10/P50/P90, SQL shown) but misses the recent-residual signal that should have triggered a second look. For a strategic partner legitimizing the PS team, reporting the raw model when the model has been 11–30% low for a month is the wrong move.

**If forced to pick one for the Brandon 1:1 on current OCI pacing:** ARM-Y, with the explicit instruction that Richard must eyeball the W13–W16 residual table himself before citing 122k.
