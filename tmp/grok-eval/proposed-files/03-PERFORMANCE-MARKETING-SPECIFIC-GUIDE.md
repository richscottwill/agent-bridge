# Performance Marketing Specific Guide (Paid Acquisition Focus)

This file specializes the agent for Richard's actual daily work: projections, Excel analysis, test readouts, pacing, and business reviews.

## Projection & Forecasting Rules
- Always pull latest actuals from DuckDB `ps` schema before forecasting.
- Use statistical confidence intervals (never single-point forecasts).
- Flag: "This projection assumes [X, Y, Z]. If any change, outcome shifts by ~Z%."
- High-stakes rule: Any projection affecting >$50k monthly or quarterly pacing must include explicit "Recommend human review before action" line.

## Excel / Data Drop Workflow (new)
When Richard drops files in `uploads/`:
1. Ingest into DuckDB (use existing tools/ or new pandas bridge if needed).
2. Update relevant schemas (`ps`, `tests`, `signals`).
3. Refresh the appropriate dashboard.
4. Generate a 5-bullet summary of what changed + anomalies.
5. Ask: "Any specific analysis or projection you want from this data?"

## Test Analysis Protocol
- Always reference the staged testing framework in `wiki/testing/testing-approach-kate-v5.md`.
- For every test readout: Incrementality estimate + confidence + recommended next action + creative fatigue signal.
- Use Karpathy Autoresearch Lab (Bayesian) where appropriate.

## Business Review / WBR Prep
- Pull from `eyes.md` + latest DuckDB metrics + `amazon-politics.md`.
- Structure: Context → What moved → Why → Risks & Mitigations → Recommendation (with confidence).
- Always include 1-2 "tough but fair" questions Richard might get asked.

## Daily Output Standard
Every morning brief or EOD summary must contain:
- 3-5 prioritized actions tied to the Five Levels
- One "leverage opportunity" identified
- One "friction to remove" suggestion
