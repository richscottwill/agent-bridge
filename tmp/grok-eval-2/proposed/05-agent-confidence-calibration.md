# Agent Confidence Calibration Metric (Grok proposal)

Add a simple "Agent Confidence Calibration" metric to `rw-tracker.md` — track average confidence % vs actual accuracy over time.

Pattern:
- Each high-stakes output carries a stated confidence % (e.g., 55%, 70%)
- After the outcome is known, score HIT / MISS
- Weekly: compute calibration curve — of the things I said I was 55% confident about, was I right 55% of the time?
- If systematic over- or under-confidence appears, adjust future confidence scores
