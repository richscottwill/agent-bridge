# MPE Roadmap: v1.1 → v1.2 → v1.3 → v1.4

This document shows the clear evolution from the current **v1.1 Slim** build to the full **v1.4 Structural Bayesian** vision.

---

## v1.1 Slim (Current Target — Shipping May 2026)

**Focus**: Fix the biggest problems from v1 with a practical, maintainable model that works for **all 10 markets** from Phase 1.

### Key Features
- **Brand-Anchor / NB-Residual** architecture (Brand projected first)
- **Locked-YTD + RoY Projection** (never projects below actuals)
- 3-stream Brand Trajectory Model (Seasonal + Recent Trend + Regime)
- NB Residual Solver with 4 branches (`ieccp`, `regs`, `spend`, `op2_efficient`)
- Operational bounds enforcement
- Basic qualitative scenario picker
- Contribution breakdown in UI

### Probabilistic Level
- Mostly **deterministic**
- Only NB elasticity uses Monte Carlo (same as v1)

### Complexity
- Medium (higher than v1, but manageable)

### Timeline
- 3–4 weeks focused work
- Target: Mid-to-late May 2026 demo

### What’s New
- `brand_trajectory.py`
- `nb_residual_solver.py`
- Updated `mpe_engine.py`
- New parameter fields

---

## v1.2 (June – July 2026)

**Focus**: Add the first layer of **structural intelligence**.

### Key Features
- **Skeleton Posterior** (Level 1 Bayesian)
  - Engine maintains probability distribution over the 4 skeletons
  - Updates weekly based on how well each skeleton explains recent data
- **Bayesian Online Changepoint Detection (BOCPD)**
  - Automatically proposes new regime events
  - Human confirmation still required
- **Probabilistic Decay Curves**
  - Replace point estimates (13w / 26w / 52w) with LogNormal posterior on half-life
  - Engine now says: *"Sparkle half-life posterior: 29w (90% CI: 18–47w)"*

### Probabilistic Level
- **Structural Bayesian (Level 1–2)**
- Skeleton selection becomes probabilistic
- Decay half-life becomes a distribution

### Complexity
- Medium-High

### Tools
- Start using **NumPyro** (primary) or **PyMC v5** for new components
- Keep existing deterministic engine as likelihood kernel

### UI Changes
- New **"Model View"** panel showing:
  - Skeleton probabilities
  - Decay half-life posterior
  - "Skeleton drift detected" warnings

---

## v1.3 (August – October 2026)

**Focus**: Full **structural Bayesian** system.

### Key Features
- **Joint Posterior** over:
  - Skeleton
  - Elasticity parameters
  - Decay half-life
  - Regime change points
- **Hierarchical Priors** across similar markets
  - Data-sparse markets (JP NB, AU) borrow strength from EU5 / NA
- **Scenario Posterior**
  - Instead of picking a scenario, the engine maintains probabilities over scenarios
  - Example output: *"P(Y2026 spend < $900K | 75% target) = 0.42"*

### Probabilistic Level
- **Full Structural Bayesian (Level 1–3)**
- Almost everything becomes probabilistic

### Complexity
- High

### Tools
- Full **NumPyro** core (or PyMC for easier debugging)
- Existing v1.1 code becomes the official **likelihood function**

### UI Changes
- Projections show **full distributions** by default
- Advanced mode for inspecting posteriors
- "What-if" becomes "What-if posterior update"

---

## v1.4 (November 2026+)

**Focus**: **Autonomous probabilistic decision-support system**.

### Key Features
- **Fully Autonomous Skeleton Switching**
  - Engine switches skeletons automatically based on posterior
- **Continuous Changepoint Detection**
  - Automatically creates regime rows (with human confirmation gate)
- **Learned Priors**
  - Priors update from data across all markets over time
- **Full Posterior Predictive**
  - Multi-year projections with honest compounding uncertainty
- **Self-Diagnosis**
  - "Skeleton drift detected (Brand ramp)"
  - "Decay half-life posterior has high variance — recommend more data"
  - "This projection is sensitive to Sparkle persistence assumption"

### Probabilistic Level
- **Complete Joint Posterior**
- Every major assumption has uncertainty quantified

### Complexity
- Very High (research-grade system)

### Maintenance
- Requires ongoing AI/agent support or specialist
- Non-technical owner will need strong "Explain this" layer + simple overrides

### UI / Experience
- Default view shows **probability statements**
- Advanced mode for full posterior inspection
- Strong emphasis on "what the engine is uncertain about"

---

## Summary Table

| Version     | Focus                              | Probabilistic Scope             | Self-Diagnosis       | Complexity     | Timeline          |
|-------------|------------------------------------|---------------------------------|----------------------|----------------|-------------------|
| **v1.1**    | Brand-Anchor + Locked-YTD          | Parameter-level only            | Basic warnings       | Medium         | May 2026          |
| **v1.2**    | Skeleton Posterior + BOCPD         | Structural (Level 1–2)          | Skeleton drift flags | Medium-High    | June–July 2026    |
| **v1.3**    | Joint Posterior + Hierarchical     | Full Structural Bayesian        | Strong               | High           | Aug–Oct 2026      |
| **v1.4**    | Autonomous Self-Diagnosing System  | Complete Joint Posterior        | Autonomous           | Very High      | Nov 2026+         |

---

## Philosophy Across All Versions

- **v1.1**: Make it **useful and maintainable** now
- **v1.2–v1.3**: Add **intelligence** gradually
- **v1.4**: Make the engine a **true thinking partner** that diagnoses its own limitations

Each version builds on the previous one without requiring a full rewrite.

---

*Roadmap created: 2026-04-23*