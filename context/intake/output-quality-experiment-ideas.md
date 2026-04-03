# Output Quality Experiment Ideas

Route to: Karpathy (experiment design)

## 1. Stored Projections vs Fresh Projections (Callouts)
- **A:** Maintain a rolling projection file per market, updated weekly with actuals + prior week's projection error. Callout writer reads this file.
- **B:** Compute projections fresh each week from the analysis brief's raw data. No memory of prior projections.
- **Hypothesis:** Stored projections accumulate calibration data (projection error history) that improves accuracy over time.
- **Eval:** Compare projected regs/spend/CPA against actuals 1 week later. Score on accuracy (absolute error) and narrative quality (did the projection framing help or hurt the callout?).
- **Target files:** `~/shared/context/active/callouts/{market}/{market}-projections.md` (new file to create for treatment A)

## 2. Stored Context vs Fresh Pull for Wiki Docs
- **A:** Generate wiki article from DuckDB queries + context folder files (pre-digested, structured, possibly stale).
- **B:** Generate wiki article from fresh MCP pulls (Asana tasks, Slack threads, email chains) at creation time (current but unstructured).
- **Hypothesis:** Stored context is faster and more structured but may miss recent developments. Fresh pulls are current but noisy and require more synthesis.
- **Eval:** Score both articles on accuracy, completeness, structure, and staleness. Have the wiki-critic agent review both blind.
- **Target files:** wiki pipeline input sources

## 3. Style Guide Modification Experiments (from baseline findings)
- Baseline established: style guides add +0.08 to +0.15 delta on output quality.
- Next: modify specific rules in the style guides and measure whether the modification improves output.
- Example: ADD a "common mistakes" section to richard-style-email.md listing the 3 most frequent voice breaks from prior drafts. Does the next draft avoid those mistakes?
- Example: REWORD the callout principles' Attribution section to be more specific about when to use "likely" vs "potentially." Does callout confidence scoring improve?
