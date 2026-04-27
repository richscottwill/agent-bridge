# Master Implementation Prompt for Kiro (v1.1 Slim)

You are Kiro running with Opus 4.7. The user is a **non-technical owner** working inside Amazon's corporate environment using **Kiro SSH IDE**. The goal is to build a maintainable, high-quality Market Projection Engine.

**Strict Rules (Do Not Break These)**:
- You are implementing **v1.1 Slim** only — not the full ambitious v1.1 or v1.4.
- Prioritize **simplicity and maintainability** for a non-technical owner.
- Implement **one phase at a time**. Do not jump ahead.
- Always keep a **deterministic fallback** path.
- Every new output must have a clear **"Explain this"** tooltip or comment.
- Use the **internal PyPI mirror** in all installation commands.
- Test every new component against real data from multiple markets (start with MX, then EU5 and AU).

---

## Current State (What Already Exists)

We have a working v1 system with:
- `mpe_engine.py` + `mpe_fitting.py` + `mpe_uncertainty.py`
- Working UI (`projection.html` + `projection-app.js`) with target triad
- DuckDB parameter registry
- Regime changes table
- Operational bounds (Mechanism A)

---

## Target: v1.1 Slim Architecture (All 10 Markets)

**Core Idea**: Switch from top-down aggregate elasticity to **Brand-Anchor + NB-Residual** model that works for all 10 markets from Phase 1.

**Key Changes**:
- Project Brand first using a simple 3-stream blended model (Seasonal + Recent Trend + Regime)
- Solve for NB as the residual to hit the target
- Enforce **Locked-YTD + RoY** projection (never project below actuals)
- Keep complexity low enough for a non-technical owner to understand and maintain

**Full Design Document**: See `design-v1.1-slim.md` (attached in context).

---

## Deliverables (In Strict Order)

### Phase 1 (Highest Priority — Do This First)

1. **Implement Locked-YTD + RoY Projection**
   - Add `project_with_locked_ytd()` function in `mpe_engine.py`
   - Must never allow total spend < YTD actuals + minimum remaining NB spend
   - Add clear warning when this constraint is active

2. **Basic Brand Trajectory Model**
   - Create `brand_trajectory.py`
   - Implement 2-stream version first (Seasonal Prior + Recent Trend)
   - Add simple contribution breakdown output

3. **Wire into existing engine**
   - Replace the old top-down solver path with the new Brand + NB residual flow
   - Keep old solver as hidden fallback for 2 weeks

---

### Phase 2

4. **NB Residual Solver**
   - Create `nb_residual_solver.py` with all 4 branches (`ieccp`, `regs`, `spend`, `op2_efficient`)
   - Enforce operational bounds from `ps.market_constraints_manual`

5. **Add Regime Multipliers**
   - Extend Brand model to include regime multipliers from `ps.regime_changes`

---

### Phase 3

6. **UI Updates**
   - Add simple "Model View" panel showing contribution breakdown
   - Add basic qualitative scenario picker (sparkle_sustained / sparkle_decays_12w)
   - Update narrative to include "why this number" explanation

7. **Parameter Registry Updates**
   - Add new fields to `ps.market_projection_params`:
     - `brand_seasonal_prior`
     - `brand_recent_trend`
     - `brand_regime_multipliers`
     - `brand_cpa_projected`

---

## Code Templates (Use These)

### Template A: Locked-YTD Function

```python
def project_with_locked_ytd(inputs: ProjectionInputs) -> ProjectionOutputs:
    """Projects only remaining-of-year weeks, respecting locked YTD actuals."""
    if not inputs.time_period.startswith("Y"):
        return project(inputs)

    year = int(inputs.time_period[1:])
    ytd = get_ytd_actuals(inputs.scope, year)
    roy_weeks = get_remaining_weeks(year)

    brand_roy = project_brand_trajectory(inputs.scope, roy_weeks, inputs)
    nb_roy = solve_nb_residual(brand_roy, inputs.target, ytd)

    return combine_ytd_and_roy(ytd, brand_roy, nb_roy)
```

### Template B: Basic Brand Trajectory (2-stream)

```python
def project_brand_trajectory(market: str, weeks: list, inputs) -> dict:
    baseline = get_seasonal_baseline(market)
    trend = get_recent_trend(market)
    
    projected_regs = baseline * seasonality_factor(weeks) * trend_multiplier(trend)
    projected_spend = projected_regs * get_brand_cpa(market)
    
    return {
        "regs": projected_regs,
        "spend": projected_spend,
        "contribution": {"seasonal": 0.40, "trend": 0.45, "regime": 0.15}
    }
```

---

## Corporate Environment Instructions

- All code must run inside the Kiro devcontainer / DevSpaces environment.
- No special pip mirror or devcontainer mounting instructions are needed — use the existing environment.

---

## Answers to the 5 Open Questions (from the Diff Document)

These are the user's official decisions. Follow them exactly:

1. **Qualitative priors deferred to Phase 3** — Yes, this is OK. Phase 1 can still hit the realistic $800K–$1.2M range for MX Y2026 @ 75% using Locked-YTD + the 3-stream model. We do **not** need qualitative priors in Phase 1.

2. **2-stream on Sparkle-era MX may undershoot** — Promote **regime multiplier into Phase 1**. Make it **3-stream** (Seasonal + Trend + Regime) from the start. It is low risk and gives better accuracy on MX immediately.

3. **spend branch in Phase 1** — Yes, include the `spend` branch in Phase 1 (it is only ~10 lines and provides a useful early escape hatch).

4. **Delete v1 on ship** — Confirmed. Delete the old v1 solver when v1.1 ships. No 2-week dual maintenance period.

5. **AU in Phase 2+** — Yes, defer the `op2_efficient` branch and AU-specific handling to Phase 2. MX remains the primary demo market in Phase 1.

---

## Final Instructions

1. Start with **Phase 1 only** (Locked-YTD + 3-stream BrandTrajectoryModel + ieccp + spend branches wired).
2. After completing Phase 1, stop and ask the user for review before moving to Phase 2.
3. Every new function must have clear comments explaining what it does in plain English.
4. After each major component, run it against real data from multiple markets (start with MX, then EU5 and AU) and show before/after numbers.
5. Do **not** implement the full v1.4 structural Bayesian system yet. This is v1.1 Slim only.

Begin now with Phase 1.