# Design Document — MPE v1.1 Slim (Brand-Anchor / NB-Residual Architecture)

**Status**: Simplified v1.1 design — 2026-04-23  
**Goal**: Deliver 80% of the value of the full v1.1 design with ~60% of the complexity.  
**Scope**: Full support for all 10 markets (MX, EU5, JP, US, CA, AU, and others) from Phase 1. Optimized for a non-technical owner and a 3–4 week implementation timeline.

---

## Why v1.1 Slim Exists

The original v1 model treated Brand and NB as peer channels with separate elasticity curves. This worked under stable conditions but produced badly wrong answers when regimes changed (e.g. MX Y2026 @ 75% ie%CCP returned $443K when the realistic range was $800K–$1.2M; similar issues appeared in other markets under regime shifts).

**Core Problem**: The model was solving the wrong problem. It used aggregate local responsiveness across incompatible regimes and treated Brand and NB symmetrically when they are not operationally symmetric.

**Solution**: Switch to a **Brand-Anchor / NB-Residual** model:
- Project Brand first from its own fundamentals (trend, seasonality, regimes).
- Solve for NB spend as the residual needed to hit the target (ie%CCP, regs, OP2, etc.).

This matches how the team actually plans: "Project Brand, then move the NB lever to hit the target."

---

## Core Model Identity (Simplified)

```
brand_regs   = BrandTrajectoryModel(market, time_period, scenario)
brand_spend  = brand_regs × brand_CPA (simple regime-based projection)

nb_spend     = NBSolver(target_mode, target_value, brand_regs, brand_spend)
nb_regs      = nb_spend / nb_CPA(nb_spend)

total_spend  = brand_spend + nb_spend
total_regs   = brand_regs + nb_regs
ie%CCP       = total_spend / (brand_regs × brand_CCP + nb_regs × nb_CCP)
```

**Key Rules**:
- Brand is the anchor (projected independently of any target).
- NB is the lever (solved to hit the target).
- ie%CCP / OP2 / regs targets are **constraints**, not drivers.
- If a target is unreachable under operational bounds → return closest feasible answer + clear warning.

---

## Brand Trajectory Model (Slim Version)

We use **3 evidence streams** instead of 4:

### 1. Seasonal Prior (40% weight)
- Per-week percentage change shape from prior 2–3 years (regime-filtered).
- Captures "Brand usually drops in mid-April."
- Refit annually.

### 2. Recent Trend (45% weight)
- Current level + slope from the last 8–16 weeks of the current regime.
- Refit weekly during the callout pipeline.
- This is the most responsive part of the model.

### 3. Regime Multipliers (15% weight)
- Level-shift factors from `ps.regime_changes` (e.g. Polaris launch, Sparkle start).
- Applied as multipliers on the baseline.

**Default weights**: Seasonal 40% + Trend 45% + Regime 15% = 100%.

**User can override** weights and select qualitative scenarios (e.g. `sparkle_sustained`, `sparkle_decays_12w`).

**Output**: Per-week Brand regs + a simple contribution breakdown ("45% trend, 40% seasonal, 15% regime").

**Brand CPA**: Simple rolling 8-week median per regime segment (no elasticity curve needed).

---

## NB Residual Solver (Unchanged from Full v1.1)

Four solver branches based on `target_mode` — designed to support all 10 markets:

| target_mode     | What it solves for                          | Primary Markets                  |
|-----------------|---------------------------------------------|----------------------------------|
| `ieccp`         | NB spend to hit target ie%CCP               | MX, EU5, JP, US, CA              |
| `regs`          | NB spend to hit total regs target           | AU, OP2 checks, growth markets   |
| `spend`         | Direct: NB = target – brand_spend           | All markets (scenario mode)      |
| `op2_efficient` | Maximize regs within OP2 budget             | AU (default), efficiency-focused |


**Operational Bounds** (from `ps.market_constraints_manual`):
- `min_weekly_nb_spend` and `max_weekly_nb_spend` are enforced.
- If target is unreachable → return closest feasible + `TARGET_UNREACHABLE_UNDER_BOUNDS` warning.

---

## What Changes from v1 (Slim Summary)

**Replaced**:
- Top-down aggregate elasticity solver
- `brand_spend_share` parameter
- Brand CPA/CPC elasticity curves (replaced by simple regime-based CPA)

**Added**:
- `BrandTrajectoryModel` (3-stream blended fit)
- `NBResidualSolver`
- Locked-YTD + RoY projection (critical fix)
- Simple qualitative scenario picker
- Contribution breakdown in UI

**Retained**:
- All existing tables and refit cadence
- NB CPA elasticity (used only as closure for the solver)
- Seasonality fit method
- Operational bounds
- Python/JS parity pattern
- Current UI shell + target triad

---

## Implementation Priorities (3–4 Week Plan)

**Phase 1 (Week 1)** — Highest Impact, Lowest Risk
- Implement **Locked-YTD + RoY Projection**
- Build basic `BrandTrajectoryModel` (Seasonal + Recent Trend only)
- Wire into `mpe_engine.py`

**Phase 2 (Week 2)**
- Add Regime Multipliers
- Build `NBResidualSolver` with all 4 branches
- Add operational bounds enforcement

**Phase 3 (Week 3)**
- Add qualitative scenario picker + contribution breakdown
- Update UI (target triad + new "Model View" panel)
- Update parameter registry with new fields

**Phase 4 (Week 4)**
- Full validation + backtesting on MX + 2 other markets
- Migrate callout pipeline
- Retire old v1 solver

---

## Validation & Acceptance Criteria

Must pass these before shipping:

1. **MX Y2026 @ 75% ie%CCP** returns spend in **$750K – $1.1M** range (realistic band).
2. **Locked-YTD Test**: No projection ever returns total spend < YTD actuals + minimum remaining NB spend.
3. **Brand Projection MAPE < 22%** on 12-week holdout (across all markets).
4. **AU Y2026 @ OP2** returns regs within ±15% of target at spend ≤ budget.
5. **Regional Rollup** math closes correctly (sum of per-market = regional total).

---

## Path to v1.4 (Structural Bayesian)

This slim design is intentionally **mostly deterministic** to ship quickly. It sets up v1.4 nicely:

- The 3 evidence streams in BrandTrajectoryModel become natural places for **posteriors** later.
- The NB solver becomes the **likelihood function** for structural Bayesian models.
- Qualitative scenarios become **scenario posteriors**.
- We can later add:
  - Skeleton posterior (Level 1)
  - Automatic changepoint detection (BOCPD)
  - Probabilistic decay curves

v1.1 Slim = strong foundation. v1.4 = full probabilistic version on top.

---

## Owner Experience (Non-Technical Focus)

- Every projection shows a **simple contribution breakdown** ("Brand is driven 45% by recent trend, 40% by seasonality").
- Clear warnings when targets are unreachable.
- Qualitative scenario picker is optional and clearly labeled.
- "Explain this number" tooltips remain mandatory on every KPI.

**Maintenance Burden**: Medium. Higher than v1, but manageable if we keep the number of new parameters low and document everything well.

---

## Final Recommendation

This **Slim version** is the right balance:
- Fixes the biggest problems from v1
- Is implementable in 3–4 weeks
- Keeps long-term maintainability in mind for a non-technical owner
- Leaves a clean path to the full structural Bayesian vision in v1.4

**Next Step**: Feed this document + the code sketches (NumPyro template, Locked-YTD function, etc.) into Kiro with strict instructions to implement **Phase 1 first**.

---

*Document created 2026-04-23 as a pragmatic, owner-friendly evolution of the full v1.1 design.*