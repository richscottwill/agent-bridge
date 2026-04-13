---
inclusion: auto
---
# Market Constraints — Quick Reference

Load this context whenever discussing market performance, predictions, budgets, or strategy. Each market has unique targets and operating conditions.

## Paid Search Markets

**AU** — Handoff to AU team (Harsha) week of 4/13. $140 CPA target (OP2), shifting toward volume-first. 6-week reg decline (W7 328 → W14 170). Polaris LP switch W13 caused CVR collapse. No ie%CCP until Jul 2026 (CCP data unavailable). OCI planned May 2026, MCC not created. No YoY data until Jun 2026 (launched Jun 2025).

**MX** — 100% ie%CCP target is the governing constraint. Brand has ~3x'd YoY (structural growth, not anomaly). NB budget should scale with Brand ie%CCP headroom. Lorena owns local budget; Q2 spend TBD (overdue). Semana Santa = W14 in 2026 (W16 in 2025) — calendar alignment matters. OCI not launched.

**US** — Largest market. Walmart IS 37-55%. Bid caps holding. OCI live. Polaris brand pages live all GEOs. AI Max rollout Q2 2026.

**UK** — OCI live (100% since Jul 2025, +23% uplift). Polaris weblab in progress. Ad copy test +86% CTR.

**DE** — OCI live (100% since Oct 2025, +18% uplift). Polaris weblab targeting Apr 6-7.

**FR** — OCI 100% since Mar 30. Polaris weblab targeting Apr 6-7.

**IT** — OCI 100% since Mar 30. PAM paused due to 22% tax (billing address change Feb 2026).

**ES** — OCI 100% since Mar 30.

**JP** — OCI 100% since Mar 30. Brand LP experiment live. MHLW regulatory headwind. Brand-dominant market (NB too small to model independently).

**CA** — OCI dial-up Apr 8-9. Excluded from Polaris Apr 7 test. +186% bulk CVR from OCI E2E.

## Paid App (PAM)

**US** — Primary PAM market. Brandon asked about additional budget (unanswered 7d as of 4/10). PO 34d overdue. Budget question open.

## Where to find more detail

- Full market state files: SharePoint `Kiro-Drive/state-files/` (au-paid-search-state.md, mx-paid-search-state.md, ww-testing-state.md)
- DuckDB: `ps.market_status`, `ps.latest_forecasts`, `ps.regime_changes`
- Weekly callouts: `~/shared/wiki/callouts/<market>/`
- OP2 targets: `ps.targets` in MotherDuck
