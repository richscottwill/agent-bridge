# Comparison: Real-World Systems vs Our MPE Roadmap

This table compares three leading real-world Bayesian forecasting systems with our planned evolution from **v1.1 Slim** to **v1.4**.

| Feature                              | Uber Orbit                                      | Google CausalImpact                             | PyMC + Bambi                                    | Our v1.1 Slim (Current)                        | Our v1.4 Vision (Target)                          |
|--------------------------------------|--------------------------------------------------|--------------------------------------------------|--------------------------------------------------|------------------------------------------------|----------------------------------------------------|
| **Core Architecture**                | Structural Bayesian Time Series                 | Bayesian Structural Time Series (BSTS)          | Flexible Bayesian modeling (state-space)        | Brand-Anchor + NB-Residual                     | Full structural Bayesian with multiple skeletons  |
| **Brand vs NB Separation**           | No (general time series)                        | No (general time series)                        | Possible with custom models                     | Yes (explicit)                                 | Yes + probabilistic hierarchy                     |
| **Locked YTD + RoY Support**         | Manual workaround                               | Manual workaround                               | Manual workaround                               | Yes (core feature)                             | Yes + automatic                                   |
| **Structural Bayesian**              | Strong (multiple model components)              | Strong (BSTS)                                   | Excellent (highly flexible)                     | Mostly deterministic                           | Full (Level 1–3)                                  |
| **Skeleton / Model Posterior**       | Limited (model selection)                       | No                                              | Yes (via model comparison)                      | No (rule-based)                                | Yes (automatic skeleton switching)                |
| **Changepoint / Regime Detection**   | Basic support                                   | Strong (intervention detection)                 | Good (custom models)                            | Manual (`ps.regime_changes`)                   | Automatic (BOCPD) + self-diagnosis                |
| **Probabilistic Decay Curves**       | Yes (some models)                               | Limited                                         | Yes (via Gaussian Processes or custom)          | Point estimates only                           | Full posterior (LogNormal on half-life)           |
| **Hierarchical Models**              | Good                                            | Limited                                         | Excellent                                       | No                                             | Yes (across markets)                              |
| **Visualization Quality**            | Good (forecast + uncertainty bands)             | **Excellent** (best in class)                   | Good (via arviz)                                | Basic                                          | Excellent + probability statements                |
| **Ease for Non-Technical Users**     | Medium (requires some stats knowledge)          | High (very intuitive output)                    | Medium (can be complex)                         | High (designed for this)                       | High (strong "Explain this" layer)                |
| **Production Use at Scale**          | Yes (Uber internal + open source)               | Yes (widely used at Google + industry)          | Yes (many companies)                            | Planned                                        | Yes                                               |
| **Open Source**                      | Yes (GitHub: uber/orbit)                        | Yes (R + Python port)                           | Yes (PyMC is very active)                       | Will be open sourced                           | Will be open sourced                              |
| **Agent / LLM Friendly**             | High (clean Python API)                         | Medium                                          | High                                            | High                                           | Very High (designed for agents)                   |
| **Maturity (2026)**                  | Mature (v1.1+)                                  | Very Mature                                     | Very Mature                                     | In development                                 | Future                                            |

---

## Key Takeaways

### 1. Uber Orbit is the Closest Existing System
- It is the most similar to what we want to build in **v1.4**.
- Uses Pyro (our planned backend).
- Has structural components and uncertainty quantification.
- However, it is **general-purpose** — it does not have our Brand vs NB asymmetry or Locked-YTD logic.

### 2. Google CausalImpact Excels at Visualization
- Best-in-class output visuals (pre/post, cumulative impact, etc.).
- We should study its visualization style for v1.4 UI.

### 3. PyMC + Bambi is Great for Rapid Development
- Excellent for prototyping complex models quickly.
- We can use it in **v1.2** for experimentation before moving to NumPyro in v1.3+.

### 4. Our Unique Advantages
- **Brand-Anchor / NB-Residual** model (none of the above have this)
- **Locked-YTD + RoY** enforcement (very important for real planning)
- Designed specifically for **non-technical owners** + agent collaboration
- Clear path from simple (v1.1) to fully autonomous (v1.4)

---

## Recommendation

| Phase       | Recommended Approach                              |
|-------------|----------------------------------------------------|
| **v1.1**    | Build our custom model (no need to copy others)   |
| **v1.2**    | Use **PyMC + Bambi** for rapid prototyping        |
| **v1.3+**   | Move core to **NumPyro** (like Uber Orbit)        |
| **v1.4**    | Combine best ideas from Orbit + CausalImpact + our custom architecture |

---

*Created: 2026-04-23*