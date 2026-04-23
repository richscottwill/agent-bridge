# T2 Blind Eval — MX Polaris Gen4 Ad Copy Test Readout

**Task:** Readout on a 4-week 50/50 A/B test, recommend launch/iterate/kill. Medium-stakes — decision could shift $1–2M of MX spend if wrong. A good readout names the lift but also the residual risk (p-value, CI, fatigue, split cleanliness, generalizability).

## Summary Table

| Criterion | ARM-A | ARM-B | ARM-C | ARM-D |
|---|---|---|---|---|
| 1. Clarity of NBA | 9 | 9 | 8 | 9 |
| 2. Decision Quality | 10 | 8 | 8 | 8 |
| 3. Adherence to Richard's principles | 8 | 8 | 9 | 7 |
| 4. Overall usefulness for this task | 10 | 8 | 8 | 8 |
| 5. META — always-on cost | 7 | 6 | 9 | 6 |
| **Total (50)** | **44** | **39** | **42** | **38** |

**Ranking:** ARM-A > ARM-C > ARM-B > ARM-D.

---

## Per-Arm Commentary

### ARM-A — 44/50 (strongest readout)

**Evidence of quality:**
- Only arm that catches the power-design mismatch: "Detecting 5% relative lift on a 3.6% baseline at 80% power requires ~170K clicks/arm. Actual: ~15K/arm." That's the right methodological read — the test was ~10× underpowered on sample, and the observed +14% effect is what *could* be detected, not what the test was designed to detect. The others run the z-test correctly but don't interrogate whether the original power calc was honest.
- Gives a numeric confidence (55%) with explicit why-not-higher / why-not-lower.
- Top-3 assumptions carry sensitivity labels (high/medium/low) — other arms list assumptions without telling you which one to worry about.
- Recommends scale **with a 2-week validation window + a kill-switch rule** (CVR < 3.8% at full traffic → revert). This is a decision procedure, not a vague "monitor."
- Flags Legal/Brand check on "Business Pricing Exclusive" as a pricing-adjacent claim. Others miss this entirely.
- Names what's missing from the data drop (weekly CVR series) before treating the decision as actionable.

**Weaknesses:**
- Longest of the four. Readout-as-published would need compression for Brandon/Kate forum.
- META score: the heavy Clarity Check + high-stakes scaffolding is worth it here but would be overkill on "what do I eat for lunch." Less always-on-friendly than ARM-C.

**The call:** Launch with validation window. Most rigorous.

---

### ARM-B — 39/50

**Evidence of quality:**
- Confidence split across Sign/Magnitude/Generalizability is clean (95/55/40). Matches how an experienced analyst would think about it.
- Table of 3 options (Scale / Scale+queue Gen5 / Extend) is useful for a team forum — lets a reader see what was considered and rejected.
- Recommended action is Option B (scale + queue Gen5 refresh), which pre-empts fatigue rather than reacting to it. Sound thinking.
- NBA mandate check at the top is a reasonable procedural gate.

**Weaknesses:**
- Doesn't catch the power-design mismatch the way ARM-A does.
- The "Conditional NBA Mandate" framing is ceremony — it adds structure at the top of the doc that doesn't appear to change the substance of the output. If it fires on every test readout anyway, it's not doing discriminating work.
- Next action is a data request ("pull weekly breakout from Yun-Kang"), not a decision. The user asked for launch/iterate/kill — ARM-B answers "pending."
- Creative generalizability caveat is good ("Spanish-language pricing narrative may not port") but dropped without a follow-on ask.

**The call:** Gated scale. Reasonable but reserves judgment more than the data warrants.

---

### ARM-C — 42/50 (the quiet baseline)

**Evidence of quality:**
- Confidence split (Sign 90% / Magnitude 55% / Generalizability 40%) is well-calibrated. Gives a planning number: "Plan for ~+5–8% sustained, not +12%." That's exactly the kind of discount an experienced marketer applies.
- Cites the actual DuckDB source (`ps.v_weekly`) and the testing-methodology.md wiki — shows the readout plugs into the system rather than floating as a one-off.
- Explicitly flags the $50K human-review threshold and cites Soul principle #7 plus `high-stakes-guardrails.md` by name. Best citation discipline of the four.
- Suggests an AU parallel test before WW rollout — concrete next step for generalization question.
- Recommendation is clear: "SCALE WITH GUARDRAILS — conditional on fatigue check," sequenced across 4 numbered steps. The gate is a specific deliverable (weekly trend pull), not a vague "watch it."
- Tight and readable — closest to the target length for a published readout.
- META: the structure here (inputs → 4 required elements → assumptions → spend impact → next step) would work on nearly any analytical task without feeling heavy. Highest always-on value.

**Weaknesses:**
- Doesn't catch the power-design mismatch (says CI lower bound "sits just above the 5% MDE floor" but doesn't note that the power calc itself was probably wrong given the MX click volume).
- Doesn't specify kill-switch thresholds the way ARM-A does.
- "Plan for +5–8% sustained" is a judgment call that deserves a one-sentence justification (why that range?).

**The call:** Scale with guardrails + fatigue check gate. Best-balanced output.

---

### ARM-D — 38/50

**Evidence of quality:**
- Stats and confidence split are correct (85/60/40) and numeric overall confidence (75%) is given.
- Specific fatigue-check threshold: "Gen4 CVR W4 ≥ 90% of W1 CVR → scale." That's a clean decision rule, comparable to ARM-A's kill-switch.
- Checklist at the end ("Open Items / Human Review") is actionable.
- Correctly pushes back on "re-run the test" as wasteful.

**Weaknesses:**
- The Friction-Impact 2x2 is decorative here. It lands the same recommendation the prose already gave and doesn't change the analysis. That's ceremony, not signal.
- Soul Principles Check section is performative — reads as compliance theater rather than surfacing a principle-level concern. ARM-A and ARM-C invoke principles only when they actually do work.
- Doesn't catch the power-design mismatch.
- Doesn't cite concrete data sources (DuckDB table, wiki path) the way ARM-C does.
- Longer than ARM-C without adding proportional value.
- META: the 2x2 and the principles-check would be recurring boilerplate on lower-stakes tasks. Not always-on-cheap.

**The call:** Scale conditional on fatigue check. Right answer, heavier packaging than needed.

---

## META — Always-On Cost Tradeoff

If any of these decision procedures had to run on every task (brief, email triage, calendar query, test readout), which would earn its keep?

- **ARM-A's scaffolding:** Rich on high-stakes, overkill on routine. Good when the stakes trigger is real; noise when it isn't. Score 7.
- **ARM-B's NBA trigger check:** Performs a gating ritual at the top that fires on most analytical tasks anyway. Adds words without consistently changing the recommendation. Score 6.
- **ARM-C's structure:** Inputs → required elements → assumptions → spend impact → next step. That's a general analytical skeleton that works for a test readout, a forecast check, a pacing callout, a one-off question. Cheapest structure, most reusable. Score 9.
- **ARM-D's Friction-Impact 2x2 + Soul Check:** Both are tools that work sometimes but become ceremony when forced on every task. Score 6.

**Implication:** ARM-A wins on the current task because the current task is genuinely high-stakes and the scaffolding earns its weight. ARM-C wins on the always-on question because it carries almost no overhead when the task is lighter.

---

## What none of the four got right

All four ran the z-test and all four flagged fatigue. Only ARM-A noticed the test was never actually powered to detect 5% at MX click volumes. That's the methodology critique that should travel back to whoever designed the test — and it's the kind of observation that separates a strategic partner from a channel executor. The others run the math that was asked for; ARM-A runs the math that wasn't asked for but matters.

Also missing from all four: explicit week-by-week CVR **request with a specific owner and SLA** (ARM-B mentions Yun-Kang; none specify "EOD Monday from the test platform export" as a concrete ask). Half-credit to ARM-C for naming the DuckDB view.

---

## Verdict

- **This task:** ARM-A. Rigor matches the stakes. The power-design critique is the discriminating insight.
- **Always-on default:** ARM-C. Lowest ceremony, right calibration, cites the system it plugs into.
- **Avoid:** The ceremony in ARM-D's 2x2 and Soul Check, and ARM-B's NBA trigger ritual, when they don't change the substance.
