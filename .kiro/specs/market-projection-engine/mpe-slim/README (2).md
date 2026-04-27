# MPE v1.1 Slim — Brand-Anchor / NB-Residual Architecture

This folder contains the complete package for implementing **MPE v1.1 Slim** — a simplified, maintainable re-architecture of the Market Projection Engine.

## Quick Start

1. Open this project in **Kiro SSH IDE**
2. Use the provided `devcontainer.json` (recommended)
3. Copy the full implementation prompt from `prompts/Kiro_v1.1_Slim_Implementation_Prompt.md` into your Kiro agent
4. Start with **Phase 1 only**

## Folder Structure

```
mpe-v1.1-slim/
├── design/
│   └── design-v1.1-slim.md          # Core design document (slim version)
├── prompts/
│   └── Kiro_v1.1_Slim_Implementation_Prompt.md   # Full prompt for Kiro
├── .devcontainer/
│   ├── devcontainer.json
│   └── post-create.sh
├── src/
│   ├── mpe_engine.py                # Main engine (to be updated)
│   ├── brand_trajectory.py          # New Brand model (Phase 1)
│   ├── nb_residual_solver.py        # New NB solver (Phase 2)
│   └── structural_bayesian.py       # Placeholder for v1.3+
├── requirements.txt
├── README.md
└── tests/
    └── test_locked_ytd.py           # Starter test
```

## Key Improvements in v1.1 Slim

- Brand as the **anchor** (projected first) — works for all 10 markets
- NB as the **residual lever** (solved to hit target) — supports ie%CCP, OP2, regs, and spend targets
- **Locked-YTD + RoY** projection (respects actuals) — enforced across all markets
- Much lower complexity than full v1.1
- Clear path to v1.4 structural Bayesian
- Designed for **all 10 markets** from Phase 1 (MX, EU5, JP, US, CA, AU, etc.)

## Next Steps

1. Review `design/design-v1.1-slim.md`
2. Paste the prompt into Kiro
3. Implement **Phase 1 first** (Locked-YTD + basic Brand model)
4. Review with user before continuing

## Future Bayesian Stack (v1.2+)

For v1.2 and beyond, we plan to use modern Bayesian tools:

**Recommended Primary Tool**: **NumPyro** (best for agentic work in 2026)
- Fast (JAX-based)
- Excellent for hierarchical models and structural Bayesian
- Easy to compose with our existing engine as a likelihood kernel

**Strong Alternative**: **PyMC v5 + Bambi**
- More user-friendly for prototyping
- Great documentation and visualization (arviz)

**Key Use Cases in v1.2+**:
- Skeleton posterior (which model structure is most likely)
- Probabilistic decay curves (LogNormal on half-life)
- Bayesian Online Changepoint Detection (BOCPD)
- Hierarchical priors across similar markets

These tools are commented out in `requirements.txt` for now but will be activated in v1.2.

---

*Created: 2026-04-23*