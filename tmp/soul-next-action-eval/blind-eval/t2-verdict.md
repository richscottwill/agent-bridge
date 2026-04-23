# T2 Blind Verdict — MX Polaris Gen4 Test Readout

Evaluator is blind to which arm produced which output. Scoring based on content only.

## What the right call looks like (independent read before scoring)

- Observed +13.9% rel CVR lift, p ≈ 0.024. Stat sig.
- But 95% CI on relative lift is roughly [+1.7%, +27.5%] — **lower bound sits below the pre-registered ≥5% MDE the test was powered for.**
- Yun-Kang flagged creative fatigue in W3. A 4-week aggregate does not discriminate fatigue.
- $49.4K test spend, scale decision governs ~$50K+/month forward → human-in-the-loop threshold.

**Correct next-best-action:** Do NOT scale to 100% on the aggregate alone. Pull weekly CVR/CTR by arm W13→W16, resolve the fatigue question, and gate the scale decision on that trend. Write the call, route for human confirmation before executing.

Arms that recommend "pull weekly split first, then decide" got the call right. Arms that recommend "scale now" got it wrong.

## Per-arm scores

| Arm | Clarity | Decision | Principles | Usefulness | Always-on | Total (/50) |
|-----|---------|----------|------------|------------|-----------|-------------|
| A   | 9       | 9        | 8          | 9          | 7         | 42          |
| B   | 9       | 10       | 9          | 10         | 7         | 45          |
| C   | 9       | 9        | 8          | 9          | 8         | 43          |
| D   | 8       | 9        | 8          | 9          | 8         | 42          |
| E   | 8       | 8        | 7          | 8          | 6         | 37          |
| F   | 7       | 7        | 8          | 8          | 5         | 35          |

## Rank

1. **ARM-B (45)** — Strongest overall. Only arm that nails the CI-vs-MDE tension in the opening paragraph ("lower bound is below the designed MDE"), applies a clean Context→Action trigger, and produces a staged decision with a conservative forward projection (+5–8%, not +14%, acknowledging regression to mean). Explicit queueing of Gen5 regardless, explicit refusal to assume AU/US/EU5 transfer. Tough-but-fair questions section is exactly what a reviewer would ask. Clear one-line next step at the bottom. Gets the call right and shows the math.

2. **ARM-C (43)** — Most structurally disciplined. The 2×2 Impact/Friction sort is fast, visible, and makes the gating logic ("B gates A") explicit. Numbered staged plan at the end is the cleanest "Monday action" of any arm. Lighter on statistics than A/B/D but the decision quality is the same and the ceremony-to-signal ratio is the best in the set. Would read well to a busy Brandon/Yun-Kang.

3. **ARM-A (42)** — Strong because of the **pre-committed decision rule**. Writing the scale/hold/extend thresholds *before* looking at the weekly data is a genuinely Richard-aligned move (reduces post-hoc rationalization, embodies "reduce decisions not options"). Leverage Cascade framework is heavier than needed but it does connect the call to L2 and to habit-loop protection. Numeric confidence split at the bottom is useful (70% / 95% / 80%).

4. **ARM-D (42)** — Solid, thorough, and correct. Same call as A/B/C but delivered with the most conventional framing. Slightly lower on clarity because "SCALE WITH GUARDRAILS — conditional on fatigue check" is a mouthful that a reader could misread as "scale now" if they skim. The staged 1–4 plan is good. Statistical work is cleanest of the set. Reads like a competent baseline — no glaring flaws, no unique insight.

5. **ARM-E (37)** — Gets the directional call right but recommends a specific intermediate action (**shift to 80/20 Gen4/Gen3, run Gen5 in the 20% slot**) before resolving the fatigue question. That's a reasonable option but it commits operational change before the gating data is in hand — which is the opposite of what A/B/C/D recommend. The 80/20 + Gen5 pattern is a decent hedge but it's an action on the aggregate, not a gated action on the trend. Weakest decision quality of the four "don't scale yet" arms.

6. **ARM-F (35)** — Got the test-readout call **wrong**: recommends "scale Gen4 to 100% in MX with a 2-week fatigue-guard window" as the primary action, and only softly conditions on pulling the weekly decomp. A 2-week post-scale fatigue watch is not a substitute for a pre-scale fatigue check when the CI lower bound doesn't clear the MDE. BUT — and this is significant — ARM-F is the only arm that catches the actual highest-leverage drift: Testing Approach v5 has been unsent to Brandon for 23 workdays, which is L1, and this readout is L2. It explicitly says "Send v5 first thing AM before opening the DuckDB pull." That is the single most valuable sentence in any of the six outputs if the current.md state it references is accurate. Docked on Decision Quality for the scale call, docked on Always-on (the filter-step framing adds ceremony), but bumped on Principles for the drift flag.

## Key observations

### Which arm got the test-readout call right
Arms A, B, C, D all correctly gated the scale decision on the weekly-trend pull. **Arm B made the tightest case** because it was the only one to lead with the CI-vs-MDE tension (the statistical fact that makes "don't scale yet" non-negotiable, not just cautious). Arm E got the direction right but jumped to an intermediate operational change (80/20 + Gen5 slot) before resolving the blocker. Arm F got it wrong — recommended scaling to 100% with a post-hoc fatigue watch.

### Which arm most helped Richard walk away knowing what to do Monday
**Arm C.** The 2×2 sort plus the numbered 5-step staged plan reads as a "do this, then this, then decide" sequence that a tired Richard at 4pm Monday can just execute. Arm B is the most correct analysis; Arm C is the most actionable Monday-morning playbook. They're close.

### Which arm added ceremony without value
**Arm F.** The 4-step filter adds structural scaffolding that expanded length without changing the conclusion. The Principle 3/7/8 checklist at the end is self-graded and reads as ceremony. Useful scaffolding when diagnosing drift (which it did catch), but heavy for a test readout.

**Arm A is borderline.** The Leverage Cascade is a 5-question framework producing a 5-bullet answer — but it did surface the "habit loop at risk" frame (every test has written status) which is a genuine Five Levels connection. Keep, don't kill.

### Always-on recommendation

For a test readout of this type, the minimal structural addition that consistently added value across arms was:

- **Explicit CI vs pre-registered MDE check** (Arm B did it best, Arm D, A, E also had it)
- **Weekly-trend gate before any scale decision** (all arms except F)
- **Pre-committed decision rule, written before the data is pulled** (Arm A's unique contribution)
- **Human-review flag at $50K threshold** (Arms A, B, D, E, F had it — should be automatic)

Recommend **always-on** for any task tagged as test readout / scale decision / forecast:
- CI-vs-MDE comparison (not just "is it significant")
- Weekly-trend gate when any reviewer flagged fatigue/decay mid-test
- $50K human-review threshold (already in soul.md principle 7)

Recommend **manual-only** (do not auto-apply to every task):
- Leverage Cascade (Arm A) — too heavy for routine requests; useful when Richard explicitly asks "what should I actually be doing"
- 4-step filter (Arm F) — the drift-detection value is real but applying it to every task would drown simple requests in ceremony; keep it in the rw-trainer / weekly-retro surface, not every-request
- 2×2 sort (Arm C) — lightweight enough to survive always-on but only adds value when there are >2 plausible next actions; no harm leaving it as an optional pattern

### Single best next-best-action line in the set

> *"Pull W13→W16 weekly CTR/CVR by arm from DuckDB (`ps.v_weekly WHERE market='MX'` filtered to Polaris test tagging, or ad-platform export). The fatigue answer gates the scale decision. Target: before EOD Monday. Bring the weekly trend to Richard for the scale/hold call — do not auto-execute."* — Arm B

That sentence says who does what, by when, against which query, with what gating logic, and who owns the decision. No other arm packages all five in one sentence.

### Second observation worth flagging

Arm F's drift callout ("Testing Approach v5 to Brandon still unsent at 23 workdays, send it first AM") is the kind of observation that should come from the rw-trainer or the aMCC layer, not from a test-readout response. It's the right call but it's routing leakage — a test-readout agent shouldn't need to know about L1 hard-thing state. If Arm F's filter is always-on it will surface this correctly; if not, this kind of cross-cutting drift check belongs in a separate always-on hook that runs alongside task responses, not inside them.
