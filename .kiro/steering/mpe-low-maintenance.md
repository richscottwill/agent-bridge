---
inclusion: fileMatch
fileMatchPattern: '{shared/tools/prediction/mpe_*.py,shared/dashboards/mpe_engine.js,shared/dashboards/projection.html,.kiro/specs/market-projection-engine/*.md,shared/dashboards/data/data-audit-reports/*.md,shared/dashboards/data/refit-reports/*.md,shared/wiki/agent-created/operations/mpe-*.md}'
---

# MPE Low-Maintenance Steering

**Purpose**: Enforce non-technical-owner constraint on every MPE-related change. Applies when editing any MPE engine file, spec, hook, refit report, or documentation.

[38;5;10m> [0m## Identity of the Owner[0m[0m
[0m[0m
Richard is the non-technical marketing manager who will solely own and maintain the Market Projection Engine after the 2026-05-16 demo, so every output—banner, tooltip, runbook step, refit report, warning, narrative—must be understandable in under 30 seconds without opening a file.
## Core Rules (enforce on every generation)

1. **Owner is non-technical**. Code comments, UI banners, warning messages, tooltips, runbook steps — all plain English. Explain "why" and "what to do next." If you need a term of art, define it the first time.
2. **Avoid over-development**. If a feature requires ongoing engineering to maintain (complex solvers, bespoke ML, heavy animations, cross-elasticity, framework migrations), simplify or defer. Prefer simple, robust, fallback-heavy designs.
3. **Scope is locked**. v1 covers all 10 markets with market-specific fits. AU uses Southern Hemisphere hybrid handling (the only SH market). Regional rollups are NA, EU5, WW. Anything past this needs a new spec and owner approval.
4. **Data realism first**. Enterprise paid-search data is noisy, sparse, regime-shifting, with soft CCPs. Always surface data quality issues visibly. Never assume clean 3+ years of perfect history. Banners and fallbacks are first-class.
5. **Numerical stability and performance**. All math has hard guards, clear error messages, performance budgets. JS recomputes use Web Worker and stay under 150 ms median. Monte Carlo samples LOCKED at 200 UI / 1000 CLI.
6. **Self-maintaining where possible**. Heavy use of Kiro hooks for validation, refit, parity, reporting. Steering files and runbook drive the owner's operations.
7. **Provenance everywhere**. Every number in the UI shows source, version, data range, fallback level, lineage. "Explain this number" tooltips are mandatory.
8. **Kiro quirks counter**. Do not generate 50+ interdependent tasks. Produce vertically sliced, testable increments. Flag any task that would need an experienced engineer for long-term maintenance.

## Language and Style Rules

- Use "owner" not "user" when referring to the non-technical maintainer.
- Warnings and banners: start with the action ("Action: Review this parameter"), then the explanation.
- Code comments: first 3 lines of any new file = "Why this exists" / "How owner maintains it" / "What happens on failure."
- Narrative output: data-forward, no em-dashes, explicit "so what," owner-readable. Follow richard-writing-style + richard-style-amazon.
- Refit reports and acceptance reports: plain English, markdown, no stack traces except on critical failure.

## Forbidden Patterns (reject immediately)

- Hierarchical Bayesian, BSTS, Prophet, Prophetverse, LightweightMMM, PyMC, NumPyro, or any external ML library beyond numpy / scipy / scikit-learn.
- Cross-elasticity between Brand and NB, macro overlays, placement decay curves as first-class model.
- MCMC posterior estimation. Monte Carlo sampling from fit-derived posteriors only in v1.
- Isolation Forest, autoencoders, LSTM, or any ML-based anomaly detection. 3SD + regime tag only.
- Command palette, Apple micro-animations, 3D visuals, natural-language input in the browser.
- Streamlit, Reflex, Django, Flask, or any server-dependent UI framework — breaks R3 SharePoint portability.
- Auto-scheduled cron refit. v1 uses manual Kiro hook trigger only.
- Slack notifications or email digests from refit reports. SharePoint push only.
- 3-year multi-year projections. v1 caps at 2 years.
- Southern Hemisphere hybrid handling for any market other than AU in v1. A future BR/ZA/NZ launch requires its own spec.
- Acceptance tests that fully automate subjective stakeholder steps (e.g., "why is this higher than my mental model?"). These are manual checklist items.
- Any component without a clear fallback path AND an owner-visible banner.

## Regime Classification Rules (ps.regime_changes)

Every row must be classified per D17 in design.md. At every refit the owner confirms any new classifications via prompt. Four classes:

- **Long-term structural** (`is_structural_baseline = TRUE`, `active = TRUE`): market permanently moved. New baseline.
- **Short-term transient** (`is_structural_baseline = FALSE`, `half_life_weeks` set, `active = TRUE`): one-time or recurring event; effect decays.
- **Excluded from fit** (`active = FALSE`): contaminated, superseded, or observation-only. Keep record, don't use in fit.
- **Short-term-excluded / reverted** (`is_structural_baseline = FALSE`, `half_life_weeks = 0`, `active = TRUE`): event occurred but was reverted. Exclude those weeks from fit.

[38;5;10m> [0m## Success Criteria for This Build[0m[0m
[0m[0m
- Non-technical owner can run a full professional projection for MX in under 90 seconds and explain it to stakeholders without reading code. *Example: Owner types `make projection MX`, reviews a one-page summary of 5-year net income and cash flow, and walks a bank lender through the key numbers in a 10-minute meeting — no spreadsheet editing required.*[0m[0m
- Owner can run quarterly refit using one hook command and understand the report. *Example: After Q2 actuals are entered, owner runs `make refit MX` and receives a plain-language report showing which assumptions shifted (e.g., "Revenue growth revised from 8% → 6.5% based on Q1–Q2 trend") and what that means for the forward outlook.*[0m[0m
- Tool feels calm, trustworthy, low-maintenance on day 1.[0m[0m
- Adding a 4th market post-v1 is templated work — 4-6 hours first time, settling to 2 hours. *Example: To add Colombia, the owner duplicates the MX market config, updates tax rates and currency settings, plugs in local assumptions, and runs the test suite — no changes to core engine code needed.*[0m[0m
[0m[0m
When in doubt, choose the simpler, more maintainable option and document the trade-off.