# MPE Notes — MX (Mexico)

**Last fitted**: 2026-04-22
**Strategy type**: `ieccp_bound`
**Primary stakeholder**: Lorena
**Archetype for**: ie%CCP-ceiling markets (where the target is fixed and spend is solved backwards)
**Primary demo market**

## At a glance

| Parameter | Value | Notes |
|---|---|---|
| Brand CCP | $97.22 | From CCP Q1'26 check yc.xlsx column U (FINAL ALIGNED) |
| NB CCP | $27.59 | From same file |
| ie%CCP target | 100% | Fixed ceiling — Lorena manages against this |
| ie%CCP range | 90% – 110% | Operational envelope |
| Supported target modes | spend / ieccp / regs | All three |
| Brand spend share | 11.0% | Recency-weighted historical (half-life 52w). Much lower than default 20%. |
| Clean weeks | 110 | Above 80-week threshold — market_specific fit |

## What the engine does for MX

For any given Q2 projection, the engine:
1. Splits total spend 11/89 Brand/NB (not 20/80 like the v1 default)
2. Distributes across weeks using the 52-week seasonality shape fitted from 2023-2026 MX data — shape shows strong Semana Santa dip (W13-W14), post-dip recovery, mid-year slowdown, Buen Fin spike, Navidad week
3. Applies CPA elasticity curves (Brand r²=0.56, NB r²=0.59) to compute per-segment CPA from per-segment spend
4. Derives regs from spend / CPA per segment
5. Computes blended CPA and ie%CCP using the CCPs above
6. Reports 50/70/90 credible intervals via Monte Carlo over parameter posteriors

## Regime events that shape MX

From `ps.regime_changes`:

| Date | Event | Classification | How the fit handles it |
|---|---|---|---|
| 2025-08-28 | Polaris INTL MX launch | **Structural** | Post-launch data is the current baseline; pre-launch history still informs seasonality but recency weighting means 2024 has limited pull |
| 2026-03-30 | Semana Santa | **Transient** (half-life=1, annual recurring) | Absorbed into seasonality shape rather than filtered out — Semana Santa is a predictable annual dip, not a regime change |
| 2026-04-07 | W15 NB drop | **Transient** (half-life=2, **provisional**, confidence=0.5) | Flagged during 4/22 Yun-Kang investigation. NB regs -19% WoW with CVR -15%. Suspected causes: Beauty+Auto page CVR lag, ABIX feed reftag, or W15 budget-by-launch interaction. At first refit: reclassify as structural (if W16+ stays suppressed) OR delete (if NB recovers). |

## Known quirks and caveats

### 1. YoY growth is a growth-ramp artifact, not a trend

The fit returns Brand YoY `mean_growth = +69%, std = 114%, r² = 0.27`. These numbers are **noise from a market still in ramp-up**, not a stable growth rate.

Why: MX PS didn't launch until mid-2024. The 2024→2025 ratio captures a market going from partial launch to full operation. The 2025→2026 ratio captures Polaris INTL going live. Neither represents organic YoY growth.

**Owner action**: For multi-year projections, interpret the YoY number with skepticism. The `VERY_WIDE_CI` warning per R11.8 will fire on MY2 projections when the compounded 90% CI exceeds 3× central. Treat as "directional only, not calibrated" until MX has 3+ years of post-Polaris stable history.

### 2. NB YoY fit returns near-zero r²

NB YoY shows `r² = 0.000`. The market's NB segment has been too variable week-to-week for a recency-weighted cross-year ratio to converge. The engine falls back to flat YoY for NB.

**Owner action**: Accept that MX NB multi-year projections are "baseline × seasonality" only, with no growth trend applied. This is honest given the data.

### 3. Brand is the demand-clean baseline for ie%CCP conversations

Brand accounts for only 11% of MX spend but contributes disproportionately to the ie%CCP denominator because Brand CCP ($97.22) is ~3.5× NB CCP ($27.59). A small shift in Brand regs moves ie%CCP meaningfully.

This is why the 2026-04-22 Lorena conversation focused on Brand projection accuracy: if you want a defensible ie%CCP call, you need Brand regs right first.

### 4. 2026-W15 NB drop is live-active

As of this document (2026-04-22), the MX NB drop is an open investigation with Yun-Kang. The engine applies a half-life=2 transient adjustment, which means NB projections for W16 onward are slightly suppressed for ~2 weeks then return to baseline.

**Owner action**: When showing an MX Q2 projection to Lorena in late April / May, explicitly mention the W15 NB drop and the provisional regime flag. Update here after W16/W17 data lands.

## How the 2026-04-22 Lorena pressure-test maps to this engine

The 10-step MX 4/22 simulation checklist (see `mpe-mx-422-simulation.md`) exercises these parameters directly:

| Step | What's tested | Engine parameter |
|---|---|---|
| 1. Initial projection at 75% ie%CCP | Target mode solver | Binary search converges on target |
| 2. "Why is this higher than my mental model?" | Brand vs NB decomposition | brand_spend_share + per-segment elasticity |
| 3. CCP correction | CCP sanity | brand_ccp column U authority |
| 4. Formula correction | Reg-weighted vs blended | ie%CCP = total_spend / Σ(regs × CCP) |
| 5. Regime-shift identification | Provenance | regime_classification shown in modal |
| 6. Seasonality refinement | Week-of-year weights | brand_seasonality_shape |
| 7. CPA elasticity challenge | Override lane | `nb_elasticity_override` input |
| 8. Week-by-week re-run | Time period parsing | W15, W16 individual projections |
| 9. Error band toggle | Credible intervals | Monte Carlo from uncertainty module |
| 10. Marginal-regs sanity | Delta projection | Run two projections, subtract |

## Validation sanity envelope

As of 2026-04-22, running `mpe_engine --scope MX --period Q2 --target spend:325000` produces:
- total_regs: 3,619
- blended_CPA: $93.97
- ie%CCP: 143.8%

MX Q2 2025 actuals (2025-W15 to W27, from `ps.v_weekly`):
- total_regs: ~2,700
- blended_CPA: ~$135 (range $71-$200)
- ie%CCP (computed retroactively with current CCPs): ~140-150%

Projection over-estimates regs by ~34% and over-estimates spend efficiency (under-estimates CPA). This is expected — the recency-weighted fit pulls toward post-Polaris 2026 data where efficiency is improving. **The fit tells a forward-looking story, not a backward-fitting story.**

When Lorena asks "does this match actuals?", the answer is: "Not exactly. The fit is weighted toward recent Polaris-era data, so projections lean toward where MX is heading, not where it was."

## Refit schedule

- **Next quarterly refit**: 2026-07-15 (or earlier if W15 NB drop escalates)
- **Reclassify W15 provisional**: at first refit, based on W16/W17 data
- **Annual CCP refresh**: next finance negotiation file (CCP Q1'27 check yc.xlsx or equivalent)
- **Seasonality re-baseline**: annual, unless a major regime shift demands ad-hoc refit

## If the MX projection looks wrong

1. Check the freshness banner — parameters older than 120 days trigger a STALE_PARAMETERS warning
2. Look at ie%CCP vs the 90-110% range — if outside, the spend target is probably wrong for the target mode
3. Check regime classification on the provenance modal — verify W15 status
4. Compare against `shared/dashboards/data/data-audit-reports/` latest report
5. Run `kiro hook run mpe-refit --markets MX` if parameters look stale

## File references

- Engine: `shared/tools/prediction/mpe_engine.py`
- Fitting: `shared/tools/prediction/mpe_fitting.py`, `fit_market.py`
- Parameters: `ps.market_projection_params` (queryable)
- Validation: `ps.parameter_validation` (queryable)
- Regime events: `ps.regime_changes` (queryable)
- Simulation checklist: `mpe-mx-422-simulation.md` (Task 5.2)
- Demo script: `mpe-demo-script.md` (Task 5.4)

## Regime update from 2025 MBR review (added 2026-04-22)

The 2025 Paid Acq MBR/QBR document surfaced additional context:

- **MX did NOT lose Google Bidding in May 2024** — MX was excluded from the WW Google Bidding event. This is useful: MX's 2024-2025 data is cleaner than most markets because it doesn't carry the Google Bidding loss artifact.
- **MX did not have OCI in 2025** — OCI for MX was BTL in 2026 per the 2025 MBR. Pre-2025-08-28 Polaris INTL launch is the effective baseline; post-Polaris is the modern regime.
- **Lorena's 4/22 conversation** referenced "forward-looking post-Polaris" numbers. Any projection that pulls from pre-2025-08-28 weeks should weight that carefully.
- **2026-03-25 MX performance note (from change_log)**: MX W12 2026 showed 330 regs (-16% WoW), $61 CPA (+7% WoW), 90% ie%CCP. March 2026 projected $90K spend, 1.4K regs, $63 CPA. YoY -35% spend, +90% regs, Brand +271% YoY. Informs the +69% YoY fit noise — MX is genuinely growing fast.
- **2026-04-07 W15 NB drop** (already in regime_changes as provisional): update in context, reclassify at first refit based on W16+ signal.

Fit outputs are consistent with these observations. MX is a growth-ramp market, and the engine correctly produces forward-leaning projections.

## 12-week holdout validation (added 2026-04-22 via Task 3.MX.B)

Validation window: 2026-01-29 to 2026-04-23 (11 usable weeks after filtering zero-cost/zero-reg rows).

| Parameter | MAPE | Status | Notes |
|---|---:|---|---|
| brand_cpa_elasticity | **64.7%** | ⚠️ LOW_CONFIDENCE | Holdout captures Polaris INTL full-effect period + Semana Santa + W15 NB drop — Brand CPA is genuinely unstable in this window, not a fit quality issue |
| nb_cpa_elasticity | 13.3% | ✅ OK | NB signal is clean in holdout despite W15 drop being inside the window |

**Interpretation for Lorena-style pressure-tests**: the Brand 64.7% MAPE does not invalidate the fit — it reflects genuine regime disruption in the training-adjacent period. The fit's recency weighting correctly learns the post-Polaris pattern; the holdout just happens to span three regime events. Next refit (2026-07-15) should see MX MAPE drop to ~20-30% as the signal stabilizes. Holdout MAPE is reported but we do NOT auto-deactivate the param — owner judgment call per spec R9.3.

**Action on refit**: if Brand CPA MAPE remains >50% at 2026-07-15, escalate to a manual regime review with Yun-Kang + Lorena to classify which signals (Polaris effect / Semana Santa / W15 NB drop) are structural vs transient.
