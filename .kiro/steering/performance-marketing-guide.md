---
inclusion: manual
---

# Performance Marketing Guide (Paid Acquisition Focus)

*Adopted 2026-04-22 after blind A/B test (2-0 for treatment). Invoke on projection, forecast, WBR prep, test readout, or Excel/data-drop requests.*

This file specializes the agent for Richard's actual daily work: projections, Excel analysis, test readouts, pacing, and business reviews. It is task-specific; if the request is clearly in one of these buckets, load this first alongside the relevant market callout or test state file.

## Projection & Forecasting Rules
- Always pull latest actuals from DuckDB `ps` schema before forecasting.
- Use statistical confidence intervals (never single-point forecasts).
- Flag: "This projection assumes [X, Y, Z]. If any change, outcome shifts by ~Z%."
- High-stakes rule: Any projection affecting >$50k monthly or quarterly pacing must include explicit "Recommend human review before action" line. (See `high-stakes-guardrails.md` for the full required behavior.)

## Excel / Data Drop Workflow
When Richard drops files in `~/shared/uploads/`:
1. Ingest into DuckDB (use existing `shared/tools/` or pandas bridge if needed).
2. Update relevant schemas (`ps`, `tests`, `signals`).
3. Refresh the appropriate dashboard.
4. Generate a 5-bullet summary of what changed + anomalies.
5. Ask: "Any specific analysis or projection you want from this data?"

## Test Analysis Protocol
- Always reference the staged testing framework in `shared/wiki/testing/testing-methodology.md` (and `testing-approach-kate-v5.md` for the strategic synthesis).
- **Validate the power calc against actual sample size FIRST.** Before running z-tests or reporting lift, check: did the test actually achieve the sample needed to detect the stated MDE at the stated power? For a ≥5% relative lift at 80% power on a ~4% CVR baseline, you need ~170K clicks per arm. If actuals are 5–20× below that (e.g., ~15K/arm on an MX test), the observed effect is what could be detected, not what the test was designed to detect. Name the underpowering in the readout — it's the methodology critique that separates a strategic partner from a channel executor. *Added 2026-04-22 after round 4 blind test: the only arm that caught this on T2 was the one that explicitly asked "what's the single most important signal?" — and it moved the readout from routine to rigorous.*
- For every test readout, include all four:
  - **Incrementality estimate** (with counterfactual framing for single-arm market-cutover reads)
  - **Confidence** (split sign / magnitude / generalizability; quantified where possible)
  - **Recommended next action** (scale / stop / retest with preconditions; include a specific kill-switch threshold when recommending scale)
  - **Creative fatigue signal** (rule in or rule out with CTR/CVR pattern evidence)
- Use Karpathy Autoresearch Lab (Bayesian) framing where appropriate.
- Tie to the Five Levels: every test readout is L2 evidence.

## Business Review / WBR Prep
- Pull from `eyes.md` + latest DuckDB metrics + `amazon-politics.md`.
- Structure: **Context → What moved → Why → Risks & Mitigations → Recommendation (with confidence)**.
- Always include 1–2 "tough but fair" questions Richard might get asked.
- Data caveat required: if DuckDB is stale for the reporting week, say so and restate after freshness.

## Daily Output Standard
Every morning brief or EOD summary must contain:
- 3–5 prioritized actions tied to the Five Levels
- One "leverage opportunity" identified
- One "friction to remove" suggestion

## Why this file exists (empirical basis)
Blind A/B test on 2026-04-22 found that the "Projection & Forecasting Rules" checklist, WBR structure, and "tough-but-fair questions" forced sharper outputs on a MX W17 WBR callout and AU brand test readout. The content was nominally "covered" in eyes.md and richard-style-wbr.md, but the task-specific cognitive template surfaced the right moves at the right time.
