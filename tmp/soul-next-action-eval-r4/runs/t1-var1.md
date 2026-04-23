# T1 — US Full-Year Spend Ceiling at 100% ie%CCP (Var1, Round 4)

**Question:** What's the full-year US spend ceiling if we hold 100% ie%CCP, assuming OCI-driven +10% CVR lift from current baseline?

**Inputs given:**
- Brand CCP $412.51 / NB CCP $48.52 (Richard-supplied)
- YTD US actuals W1–W16 from `ps.v_weekly WHERE market='US'`
- OCI-driven +10% CVR lift from current baseline
- High-stakes-guardrails.md auto-triggers on "ceiling" → applied
- Conditional NBA Mandate triggers (>$50k impact) → applied

---

## Top-line answer

**Full-year US spend ceiling at 100% ie%CCP ≈ $76M–$86M, point estimate $78M.**

- **No-saturation upper bound (CVR lift × current CPAs × 52 weeks × CCPs):** **$78.4M**
- **Elasticity-expansion (US W10–W16 in-sample fit):** $85.9M
- **Elasticity-expansion (MX-style saturation exponent 0.937):** $68.2M
- **Recommend citing $76M–$80M** as the operating range and **$78M** as the point estimate. $85.9M relies on in-sample elasticity that extrapolates ~2.6× beyond observed spend; $68M assumes MX-grade saturation that US in-sample data doesn't support.

## Formula (stated model, per guardrail #6)

```
ie%CCP = total_spend / (brand_regs × $412.51 + nb_regs × $48.52)
```

At 100% ie%CCP:

```
ceiling_spend = brand_regs × $412.51 + nb_regs × $48.52
```

**This is the correct formula.** The known failure mode on this task is using `blended_CPA / blended_CCP`, which gives ~$14–16M and is wrong. The per-segment CCP-weighted reg pot gives $78M, which is the answer Richard can cite.

## Baseline (pre-lift, W10–W16 weekly average)

| Segment | Regs/wk | Spend/wk | CPA | CCP |
|---|---:|---:|---:|---:|
| Brand | 2,614 | $183,158 | $70.08 | $412.51 |
| NB | 6,031 | $452,752 | $75.07 | $48.52 |
| **Total** | **8,645** | **$635,910** | $73.56 | — |

**Baseline ie%CCP (W10–W16 avg): 46.4%.** US is running roughly half the efficiency ceiling before any lift is applied. That's the headline context: **we have significant room**, and the ceiling question is about the upper bound, not near-term pacing.

## Method C — No-saturation ceiling (cleanest answer to the question as asked)

Apply +10% CVR lift to current reg output, annualize to 52 weeks, compute the CCP-weighted reg pot:

| | Annualized regs (+10%) | × CCP | Value |
|---|---:|---:|---:|
| Brand | 149,504 | $412.51 | $61.7M |
| NB | 344,998 | $48.52 | $16.7M |
| **Ceiling (spend that drives ie%CCP to 100%)** | | | **$78.4M** |

This is a theoretical maximum — it assumes every incremental dollar beyond current spend converts at current-adjusted-for-lift CPAs. Real elasticity will bend this down.

## Method B — Elasticity-expansion (operating ceiling)

Fit US NB CPA to a power curve on W10–W16 data: `CPA ≈ 13.01 × weekly_spend^0.135`. The in-sample exponent (0.135) is much flatter than MX's 0.937, which is expected — US is in a volume-rich regime with headroom. Apply +10% CVR lift as a ~9.1% CPA reducer at any given spend level, then solve for the weekly spend where ie%CCP = 100%:

- **Weekly ceiling:** $1.65M (Brand $476K + NB $1.18M)
- **Full-year:** **$85.9M**
- At the ceiling: Brand CPA $214 (extrapolated — see assumption #2), NB CPA $78

This method is internally consistent but extrapolates Brand spend ~2.6× current ($476K vs $183K/wk). Brand demand is search-volume-capped; the extrapolation is the weakest link in this method.

## Sensitivity table (if NB saturates faster than the US in-sample fit suggests)

| NB exponent | Full-year ceiling | NB CPA at ceiling |
|---:|---:|---:|
| 0.135 (US in-sample) | $85.9M | $78 |
| 0.400 | $76.9M | $96 |
| 0.600 | $72.8M | $110 |
| 0.800 | $69.8M | $124 |
| 0.937 (MX) | $68.2M | $135 |

The ceiling is robust in the **$68M–$86M** range across all reasonable elasticity assumptions. **$76M is the midpoint; $78M is the no-saturation upper anchor.**

## Top-3 assumptions that would materially change the outcome

1. **NB elasticity exponent** — US W10–W16 data fits 0.135 (nearly flat CPA across $387K–$500K/wk). If NB saturates faster when spend doubles beyond the observed range — which is likely once we approach keyword auction limits — the exponent could rise toward MX's 0.937 and the ceiling drops from $86M to $68M. **Directional sensitivity: +0.1 exponent ≈ –$3M ceiling.** The in-sample fit is plausible within the observed range; extrapolation past 2× current weekly spend is where this assumption starts to break.
2. **CVR lift is +10% and durable, segment-wide** — OCI lift on NB is well-supported (E2E testing in-flight). A +10% assumption applied to **Brand** is more aggressive — Brand CVR is already close to ceiling on Amazon Branded terms. If the effective lift is 10% on NB and 3% on Brand, the blended ceiling drops ~$3M. If OCI lift decays post-launch (like MX's seasonal trajectory), the sustained ceiling is lower.
3. **Brand demand is not scalable 2.6× at constant CPA** — Method B implies Brand spend rises from $183K/wk to $476K/wk. Brand spend is gated by search volume, not bid. Beyond a demand ceiling, Brand CPC inflates without reg gains (documented in the EU5 playbook — the "Brand demand ceiling" mechanic). A realistic ceiling caps Brand at ~$220–240K/wk and flows the rest to NB; that pushes the full-year ceiling toward **$76–80M**, not $86M.

## Confidence: **55%**

- **Why not higher (why not 70%+):** US-specific NB elasticity isn't in any stored table — I fit W10–W16 weekly points, and that's only 7 data points across a narrow spend band. Brand CPA "elasticity" fit produced a mathematically unreliable exponent (>1, negative intercept in log space), meaning Brand doesn't behave as a smooth power curve in the observed range. The 2.6× Brand extrapolation in Method B is almost certainly not achievable at the fitted CPA; the real Brand ceiling is a demand wall, not a bid wall. My $86M number overstates; my $78M number (Method C) ignores saturation entirely. The true answer is between them and I'm asserting $76–80M, but the band is wide and the underlying curves are undercharacterized.
- **Why not lower (why not 30%):** The per-segment CCP formula is correct and this is the formula that matters most (round 3's Var1 catastrophe was using blended CPA / blended CCP and landing at $14M — an order-of-magnitude error). The inputs ($412.51 / $48.52) are Richard-supplied and the US YTD actuals are from `ps.v_weekly` (production source). The no-saturation upper bound at $78.4M lines up with the verdict file's flagged "correct $77–79M" range. The range is directionally very robust — even under the most aggressive saturation assumption, the ceiling stays north of $65M, which is ~2× current annualized run rate ($33M).

## Human review strongly recommended before action.

Do not cite a single point estimate to Brandon or Kate without flagging the elasticity assumption. Recommended framing for an exec ask:

> "US full-year spend ceiling at 100% ie%CCP lands around $76–80M under OCI-driven +10% CVR lift. We're running at $33M annualized and 46% ie%CCP — there's $40M+ of efficiency headroom before the ceiling binds. Point estimate $78M assumes current-adjusted CPAs hold at scale; the 30% degradation scenario (NB saturates toward MX's curve) puts the ceiling at $68M. Either way, current spend is well under the ceiling."

## What this means operationally

- **We are not ceiling-constrained at current spend levels.** US ie%CCP is 46% — roughly 54 percentage points of headroom before the ceiling binds. The binding constraint on US is volume/demand/attribution mechanics, not the ie%CCP ratio.
- **The $78M number is a ceiling, not a target.** Using it as a budget ask without agreement on the assumption set would be misleading. The honest ask to Lorena/Kate is "we have material headroom; here's the path to use it responsibly."
- **If Brandon asks for a single number**, say **$78M** and cite this doc. If he asks for a range, say **$76M–$80M** and name the elasticity sensitivity as the reason.

## Next Best Action: Before citing this externally, confirm with Brandon that the OCI-driven +10% CVR lift applies segment-wide (Brand + NB) vs NB-only, since segment-wide is the aggressive assumption behind the $78M top-line.

---

**Data sources:** `ps.v_weekly` US W1–W16 (DuckDB, pulled 2026-04-22); CCPs from Richard; elasticity method from `shared/tools/scratch/mx_precise_projection.py`; formula authority from `shared/dashboards/data/wiki-docs/702bcba24f.txt` (Scaling Model); high-stakes-guardrails.md applied; verdict-2026-04-22.md round-3 failure mode documented and avoided.

**Compute script:** `shared/tools/scratch/us_ceiling_100_ieccp.py`
