# MPE v1.1 Slim — Quick Reference

*1-page cheat sheet. If you need 60 seconds of orientation, this is it.*

---

## The core idea in one sentence

**Brand is projected independently from a recent-actuals anchor × seasonal × trend × campaign-lift stream; NB is solved as the residual that hits the user's chosen target (ie%CCP, spend, or regs).**

---

## Before v1.1 Slim → After

| | v1 (top-down elasticity) | v1.1 Slim (Brand-Anchor + NB-Residual) |
|---|---|---|
| Brand projection | ∝ spend × `brand_spend_share` | independent: anchor × seasonal × trend × campaign lift |
| NB projection | ∝ spend × (1 − `brand_spend_share`) | solved to hit target given Brand |
| Anchor | pre-first-regime 8-week mean (stale for Sparkle-era) | recent 8-week actuals (regime-aware) |
| Targets | spend / ie%CCP / regs / op2_efficient | same four, plus scenario-chip overrides |
| Regional | single rollup solve | sum of children (per-market targets) |
| UI scenario layer | N/A | 4 stances: Mixed / Frequentist / Bayesian / No lift |

---

## The four scenario chips

Every market, same four chips. No per-market brand names (zero maintenance).

1. **Current plan (Mixed)** — default. Recent anchor + fit_state decay.
2. **Frequentist** — recent anchor holds, no forward campaign lift assumed. "What the last 8 weeks say."
3. **Bayesian** — authored campaign peak holds permanently at full confidence. "What leadership hopes is true."
4. **No lift** — strip the campaign lift from the anchor itself. Hypothetical pre-campaign baseline.

MX Y2026 @ 100% ie%CCP — spread across chips: $1.31M (No lift) → $1.56M (Freq) → $1.79M (Mixed) → $2.48M (Bayes).

---


**Common failure:** Skipping this step leads to silent data loss. Always verify the output.

## File locations

| Layer | Path |
|---|---|
| Python engine | `shared/tools/prediction/{brand_trajectory,nb_residual_solver,locked_ytd,regime_confidence,fit_regime_state,qualitative_priors}.py` |
| Schema | `shared/tools/prediction/mpe_schema_v{3..7}.sql` |
| Tests | `shared/tools/prediction/tests/test_v1_1_slim_phase6_*.py` + `test_brand_trajectory.py` + `test_locked_ytd.py` + `test_nb_residual_solver.py` + `test_js_parity_v1_1_slim.py` |
| Dashboard UI | `shared/dashboards/{projection.html, projection-app.js, projection-design-system.css, v1_1_slim.js}` |
| Data export | `shared/dashboards/export-projection-data.py` |
| WBR pipeline | `shared/tools/prediction/{wbr_pipeline.py, write_v1_1_slim_forecasts.py}` |
| Backtest | `shared/tools/prediction/backtest_v1_1_slim.py` |
| Feedback triage | `shared/tools/prediction/feedback_triage.py` |
| CHANGELOG | `.kiro/specs/market-projection-engine/CHANGELOG.md` |
| Design doc | `.kiro/specs/market-projection-engine/design-v1.1.md` |

---

## Runbook — top 5 operations

1. **Run a projection in the UI**: `http://localhost:8080/projection.html` (after `python3 -m http.server 8080 --directory shared/dashboards/`).
2. **Refresh `projection-data.json`** after a DB change: `python3 shared/dashboards/export-projection-data.py`.
3. **Run full test suite**: `cd shared/tools && python3 -m pytest prediction/tests/ -q`.
4. **Run 10-market backtest**: `cd shared/tools && python3 -m prediction.backtest_v1_1_slim`. Report lands at `shared/wiki/agent-created/operations/mpe-v1-1-slim-validation-report.md`.
5. **Triage user feedback**: `python3 -m prediction.feedback_triage list` then `resolve <id> <disposition>`.

---

## Success criteria (for anyone verifying the system)

- Python tests 131/131 green.
- JS parity 3/3 green.
- 10-market backtest: ≥8/10 markets under 22% Brand MAPE.
- `ps.forecasts` has rows for every market × every future week, tagged `method='v1_1_slim'`.
- UI at http://localhost:8080/projection.html loads without console errors; hero number + regs + chart render for MX Y2026 default.

---

## Troubleshooting flow

| Symptom | First check | Fix |
|---|---|---|
| UI shows dashes "—" | `projection-data.json` exists + recent | `python3 shared/dashboards/export-projection-data.py` |
| MX hero $900K (v1 value) | YTD actuals missing `brand_cost` | Regenerate export — 2026-04-26 bug fixed, pull latest |
| Chart W15 cliff | Anchor rework not applied | Confirm `brand_trajectory.py` has `intercept_source` logic |
| Regional view empty | Per-market engine didn't run | Check `renderRegionalV1` path in `projection-app.js` |
| Feedback bar never appears | Session counter | Run 3+ projections in same browser session |
| Test failures after edit | Regression fixture stale | Regenerate: `python3 prediction/tests/fixtures/phase6_2_stable_output_generator.py` |
| DuckDB "same database different configuration" | Multiple connections fighting | See `write_v1_1_slim_forecasts.py` for pre-injection pattern |

---

## Contacts + escalation

- Owner: Richard Williams (prichwil)
- Architecture decisions: karpathy agent
- Coaching / leverage questions: rw-trainer agent
- v1.2+ model work: needs new spec (see `CHANGELOG.md` → v1.2 placeholder)

---

*Published to SharePoint via `sharepoint-sync` as `Kiro-Drive/portable-body/mpe-v1-1-slim-quick-reference.md`.*
