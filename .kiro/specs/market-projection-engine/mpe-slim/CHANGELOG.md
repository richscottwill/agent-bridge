# MPE Changelog — v1 to v1.1 Slim

## v1.1 Slim (2026-04-23) — Current Target

### Major Changes

**New Architecture**
- Switched from top-down aggregate elasticity model to **Brand-Anchor / NB-Residual** model
- Brand is now projected first from its own fundamentals
- NB is solved as the residual to hit the target (ie%CCP, regs, OP2, etc.)

**Key Improvements**
- Added **Locked-YTD + RoY Projection** (critical fix — prevents projecting below actuals)
- Implemented 3-stream Brand Trajectory Model (Seasonal + Recent Trend + Regime)
- Created dedicated `NBResidualSolver` with 4 branches
- Added operational bounds enforcement from `ps.market_constraints_manual`

**Removed / Deprecated**
- Top-down aggregate elasticity solver (`_solve_ieccp_target`)
- `brand_spend_share` parameter
- Brand CPA/CPC elasticity curves (replaced by simple regime-based CPA)
- Brand YoY growth scalar (now part of blended evidence model)

**New Parameters**
- `brand_seasonal_prior`
- `brand_recent_trend`
- `brand_regime_multipliers`
- `brand_cpa_projected`

### Files Changed

**New Files**
- `src/brand_trajectory.py`
- `src/nb_residual_solver.py`
- `design/design-v1.1-slim.md`
- `prompts/Kiro_v1.1_Slim_Implementation_Prompt.md`

**Modified Files**
- `src/mpe_engine.py` — Major refactor (new project flow)
- `projection.html` / `projection-app.js` — Added Model View panel + scenario picker

### Breaking Changes

- Old v1 solver is removed (kept as hidden fallback for 2 weeks)
- `brand_spend_share` parameter is deprecated
- Regional rollup logic updated for Locked-YTD

---

## v1.0 (Previous)

- Original top-down elasticity model
- Two peer CPA/CPC curves for Brand and NB
- Fixed historical spend-share between channels
- No Locked-YTD enforcement

---

*This changelog tracks the migration from v1 to v1.1 Slim.*