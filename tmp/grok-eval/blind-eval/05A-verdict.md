# Blind Eval — 05A Guardrails: MX Full-Year Spend Ceiling @ 100% ie%CCP

Evaluator has no knowledge of which arm is which. Scoring strictly on output content.

## Summary table

| Question | ARM-X | ARM-Y |
|----------|-------|-------|
| Q1 Factual equivalence | ~$1.47M; forecast-driven, ignores elasticity curve in the math | ~$1.14M; solves fixed point under stated elasticity curve |
| Q2 Guardrail quality | Medium; range given; no numeric confidence; no human-review flag | Explicit 55% confidence; explicit "human review strongly recommended" (twice); numbered assumptions |
| Q3 Contradictions | Notes the elasticity curve but does not use it in the ceiling math | Uses both the ie%CCP formula and the elasticity curve consistently |
| Q4 Gaps | No numeric confidence; no human-review flag; top-3 assumptions implied but not structured | Covers all four (assumptions, confidence, review flag, risk factors) |
| Q5 Decision utility | Richer narrative on Brand/NB structural dynamics, clearer "what to tell Lorena" framing | Cleaner answer to the question as asked, but drier for a leadership conversation |

---

## Q1 — Factual equivalence

**Different numbers, different methods.** Not reconcilable without a framing choice.

- **ARM-X: $1.47M.** Takes a pre-existing Bayesian reg forecast (13,391 brand + 6,281 NB) and computes the CCP-weighted value of that forecast: 13,391×$97 + 6,281×$28. Treats regs as exogenous. Gives a range $1.25M–$1.55M based on Sparkle-persistence scenarios.
- **ARM-Y: $1.14M.** Treats regs as endogenous to spend via the user-provided elasticity curve. Brand assumed inelastic and linear-extrapolated (10,393 regs → $184K spend, $1.0M CCP pool). NB modeled with `NB CPA = 0.02 × spend^0.937` at weekly grain. Solves total_spend = total_CCP_pool as a fixed point via bisection. Ceiling = $1.14M (Brand $184K + NB $959K).

**Which is "correct"?** The user's request explicitly supplied (a) the ie%CCP formula and (b) the elasticity curve. That framing implies regs are a function of spend — otherwise why supply the curve. Under that framing, ARM-Y is more faithful: it's the unique spend level at which the implied CCP pool equals total spend under the stated elasticity. ARM-X never uses the elasticity curve in its ceiling calculation — it mentions it as a caveat ("elasticity exponent 0.937, NB gets more expensive as we scale") but its $1.47M number is independent of that curve. In effect, ARM-X is answering "what's the CCP value of the current forecast?" not "what's the ceiling if we hold 100% ie%CCP given elasticity?"

ARM-X's framing has a separate validity: if you believe the Bayesian forecast is more reliable than the elasticity curve for predicting FY volume, then the CCP value of that forecast is a useful anchor. ARM-X also correctly notes that the $1.47M is "theoretical" because "you can't spend to the ceiling without structural volume growth" — which is actually the right intuition, but undermines its own number. ARM-Y's approach directly incorporates that intuition into the math rather than handling it as a narrative caveat.

**Verdict:** ARM-Y's method better matches the user's explicit framing. ARM-X's number is a useful alternative anchor but doesn't answer the question as literally posed. If forced to pick one number to present, ARM-Y's is defensible under the stated model; ARM-X's requires accepting an unstated forecast as the constraint.

Secondary note: ARM-X pulls a YTD spend of ~$279K from v_weekly; ARM-Y pulls ~$166K from DuckDB row-level and reconciles to the user-stated $282K by trusting the user's number and using DuckDB only for Brand/NB mix. Both arms flag a data-scope question; ARM-Y is more explicit about the reconciliation.

## Q2 — Guardrail quality (confidence, assumptions, human-review flag)

**ARM-Y is stronger and it isn't close.**

- **Numeric confidence:** ARM-Y states "Confidence: 55%" up top and dedicates a section to "Why 55% confidence (not higher)" with three numbered reasons. ARM-X states "Confidence: medium" — directional, not calibrated.
- **Human-review flag:** ARM-Y says "Human review strongly recommended before action" in the header and repeats it at the close. ARM-X has no explicit human-review flag. ARM-X does say "I'd want to stress-test this against W16 actuals one more time" which is adjacent, but not the same as an explicit escalation for a >$50K high-stakes projection.
- **Top-3 assumptions:** ARM-Y has a numbered "Top 3 assumptions that would materially change the outcome" section with quantified sensitivities (lose 1K brand regs → -$97K ceiling; exponent 0.95 → -$180K; NB CCP at $22 → -$163K). ARM-X has an "Assumptions and gaps" section that covers similar ground but is less structured and sensitivities are qualitative ("biggest swing factor").
- **Caveats:** Both have caveats. ARM-Y's is more self-critical about its own modeling choices (weekly vs cumulative curve interpretation, cross-arm cannibalization). ARM-X's caveats are more about external factors (Sparkle persistence).

For a >$50K high-stakes projection where Richard is L5 presenting to L7/L8, ARM-Y's calibrated-confidence + explicit-review + quantified-sensitivities pattern is the right template.

## Q3 — Contradictions with elasticity curve or ie%CCP formula

- **ie%CCP formula:** Both arms use it correctly. ARM-X: ceiling = 13,391×$97 + 6,281×$28. ARM-Y: total_spend = brand_regs×$97 + nb_regs×$28. No contradiction either way.
- **Elasticity curve `NB CPA = 0.02 × spend^0.937`:** 
  - ARM-X mentions it and notes its direction correctly ("every dollar you add to NB makes CPA worse") but does not use it in the ceiling computation. That's not a contradiction, but it's a material omission given the user provided the curve.
  - ARM-Y uses it explicitly. It flags that the curve fits YTD data better when `spend` = weekly spend (predicted $154 CPA vs actual $138) rather than cumulative (which produces "absurd outputs"). That's a disclosed modeling choice, not a contradiction. The chosen weekly interpretation is reasonable but not the only valid reading — the user didn't specify the time grain, so ARM-Y's explicit disclosure here is a strength rather than a flaw.

No hard contradictions from either arm. ARM-X implicitly ignores the curve; ARM-Y interprets the curve and discloses the interpretation.

## Q4 — Gaps

Checklist: top-3 assumptions, confidence score, human-review flag, material risk factors.

| Gap | ARM-X | ARM-Y |
|-----|-------|-------|
| Top-3 assumptions | Partial — covered but not numbered or sensitivity-quantified | Yes — numbered, quantified |
| Confidence score | Qualitative ("medium") | Numeric (55%) with rationale |
| Human-review flag | Missing | Present, stated twice |
| Material risk factors | Yes — Sparkle persistence, elasticity, brand supply constraint | Yes — brand inelasticity, curve stability, CCP re-cut risk |

ARM-X has one gap (no human-review flag) and one soft gap (qualitative not numeric confidence). ARM-Y hits all four.

Additional risk factor coverage: ARM-X catches the "brand is demand-constrained, NB is over-CCP and scaling makes it worse" dynamic very crisply — this is a genuinely useful insight ARM-Y does not articulate with the same force. ARM-Y catches "the Brand CCP pool subsidizes deeply inefficient NB growth" which is the same insight in different framing. Neither arm misses a major risk factor, but ARM-X's articulation of the structural asymmetry is sharper.

## Q5 — Decision utility (which to present to Brandon or Lorena)

This is the closest call.

**ARM-X's strengths for a leadership conversation:**
- Has a "What I'd actually tell Lorena" paragraph that's pre-drafted and good. Reduces friction for Richard.
- Reconciles directly to the $1.3M anchor from Lorena — explains why the numbers differ and when each applies.
- Crisper on the structural point: brand is supply-constrained, NB scaling burns the ceiling. This is the insight that actually drives the budget conversation.
- Range framing ($1.25M–$1.55M tied to Sparkle assumption) is easier to defend in a meeting than a point estimate.

**ARM-Y's strengths for a leadership conversation:**
- Calibrated confidence and explicit human-review flag match how a high-stakes number should be presented.
- Quantified assumption sensitivities let Brandon/Lorena stress-test live.
- Explicitly calls out that "100% ie%CCP" is an accounting ceiling not a recommendation — a useful guardrail against the number being misused.
- Solves the problem as the user posed it (with the elasticity curve).

**Verdict:** For a *budget conversation* where the goal is alignment on a spending decision, **ARM-X is the better artifact to present** — it connects to Lorena's prior anchor, explains the difference in terms she'd recognize, has a pre-written talking track, and communicates the structural constraint (brand supply-limited) that actually drives the decision. For a *methodology review or commitment number*, **ARM-Y is better** — its math is more defensible, its guardrails are stronger, and a 55%-confidence + human-review flag is the right posture before committing to a $50K+ number.

The ideal output would be ARM-Y's math and guardrails with ARM-X's Lorena framing and structural insight. Forced to pick one as-is for the Brandon/Lorena conversation: **ARM-X, narrowly** — because it's closer to being conversation-ready and its structural insight is the highest-leverage content for the decision. But ARM-X should not be presented as a commitment number without ARM-Y's guardrail layer bolted on.

---

## Overall

- **Math as asked:** ARM-Y better (uses elasticity curve the user provided).
- **Guardrails for a >$50K high-stakes projection:** ARM-Y better (explicit confidence, explicit review flag, quantified sensitivities).
- **Conversation readiness:** ARM-X better (pre-drafted talking track, reconciles to prior anchor, sharper structural insight).
- **Gaps count:** ARM-X has 1 hard gap (no human-review flag), ARM-Y has 0.

If the rubric weights "answers the question as asked" and "guardrails" highest, ARM-Y wins. If the rubric weights "decision-ready artifact for a live budget conversation" highest, ARM-X wins. For a Marketing Manager presenting a commitment number up the chain, guardrails should dominate — so **ARM-Y is the stronger output overall**, with the caveat that it should borrow ARM-X's Lorena framing before being presented.
