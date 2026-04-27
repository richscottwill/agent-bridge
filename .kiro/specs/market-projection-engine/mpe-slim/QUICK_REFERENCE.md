# MPE v1.1 Slim — Quick Reference

## Core Idea (One Sentence)
**Project Brand first from its own fundamentals, then solve for NB as the residual to hit the target — works for all 10 markets.**

## Key Changes from v1

| Before (v1)                    | After (v1.1 Slim)                     |
|--------------------------------|---------------------------------------|
| Two peer elasticity curves     | Brand as anchor, NB as residual       |
| Top-down aggregate solver      | BrandTrajectoryModel + NBSolver       |
| Fixed brand_spend_share        | Computed from first principles        |
| No Locked-YTD                  | Locked-YTD + RoY enforced             |
| Brand CPA elasticity           | Simple regime-based CPA               |

## Most Important New Features

1. **Locked-YTD + RoY Projection** (Highest priority)
   - Never projects total spend below YTD actuals + minimum remaining NB spend

2. **3-Stream Brand Model**
   - Seasonal Prior (40%)
   - Recent Trend (45%)
   - Regime Multipliers (15%)

3. **NB Residual Solver** (4 branches)
   - `ieccp` — Hit target ie%CCP
   - `regs` — Hit total regs target
   - `spend` — Direct allocation
   - `op2_efficient` — AU default

## Implementation Order (Strict)

**Phase 1 (Week 1)**
- Locked-YTD function
- Basic BrandTrajectoryModel (Seasonal + Trend)
- Wire into mpe_engine.py

**Phase 2 (Week 2)**
- Full NBResidualSolver
- Add Regime Multipliers
- Operational bounds enforcement

**Phase 3 (Week 3)**
- UI: Model View + scenario picker
- Contribution breakdown
- New parameter fields

**Phase 4 (Week 4)**
- Validation + backtesting
- Migrate callouts

## Key Files

- `design/design-v1.1-slim.md` — Full design
- `prompts/Kiro_v1.1_Slim_Implementation_Prompt.md` — Ready-to-paste Kiro prompt
- `src/mpe_engine.py` — Main engine (updated)
- `src/brand_trajectory.py` — Brand model
- `src/nb_residual_solver.py` — NB solver

## Success Criteria (Must Pass)

- MX Y2026 @ 75% returns **$750K – $1.1M**
- Never projects below YTD actuals + min NB
- Brand MAPE < 22% on 12-week holdout

## Path to v1.4

This slim version is the foundation. v1.4 will add:
- Skeleton posteriors
- Automatic changepoint detection (BOCPD)
- Probabilistic decay curves

---

*Keep this file handy during implementation.*