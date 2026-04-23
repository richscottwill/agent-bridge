# MX full-year spend ceiling at 100% ie%CCP

**Short answer: ~$1.47M.** That's the hard arithmetic ceiling. It's higher than the $1.3M number from the Lorena exchange because it assumes you accept the current full-year reg forecast (13.4K brand + 6.3K NB). The $1.3M / $1.25M numbers were built on a tighter, more conservative reg volume.

**Confidence: medium.** The math on the ceiling itself is clean. The reg volume driving it is a Bayesian point forecast generated 4/21 that hasn't been stress-tested against the Sparkle persistence question yet. Real range is probably $1.25M – $1.55M depending on what you assume about W15-W16 holding.

---

## Math

**Ceiling formula:** `spend = brand_regs × $97 + nb_regs × $28`

That's just the ie%CCP definition rearranged. At 100% ie%CCP every reg is worth exactly its CCP and total spend equals the summed CCP value.

**Inputs (verified in DuckDB):**

| Component | Brand regs | NB regs | Spend |
|-----------|-----------|---------|-------|
| YTD actuals (W2–W16, ps.v_weekly) | 3,089 | 1,682 | $279,244 |
| Forecast W17–W52 (ps.forecasts, 4/21 bayesian) | 10,302 | 4,599 | $855,248 |
| **Full-year total** | **13,391** | **6,281** | **$1,134,493** |

**Ceiling:** 13,391 × $97 + 6,281 × $28 = **$1,298,927 + $175,868 = $1,474,795**

**Baseline spend implied by the forecast:** $1.13M → blends to 76.9% ie%CCP full-year (vs 80.5% YTD).

**Headroom under the ceiling:** $1.47M − $1.13M = **~$340K** you could theoretically spend *at current reg volume* before breaching the constraint.

---

## Why this is higher than the $1.3M from the Lorena note

The $1.3M ceiling / $1.25M Sparkle-persist numbers were built on a lower reg base — likely pre-W15/W16 or with the a.com placement bump treated as non-persistent. The current forecast treats the W15-W16 step-up as partially persistent (the bayesian model absorbed those two weeks). If you reverse that assumption:

- **Sparkle decays fully after 4 weeks** (W15-W16 treated as pull-forward): brand regs drop ~15%, ceiling drops to **~$1.28M**. Matches the prior $1.3M.
- **Sparkle persists with gradual decay** (current forecast): **$1.47M**.
- **Sparkle persists flat at W15-W16 levels** (optimistic): ceiling climbs toward **~$1.55M**.

The notes in `market_constraints_manual` explicitly flag this: "W15-W16 step-up attributed to a.com placement update (Lorena, 4/22); likely persistent with gradual decay through year." The current forecast is already leaning into that belief. If Lorena's $1.3M was pre-4/22, it's stale on that assumption.

---

## The caveat that matters

The ceiling is a volume equation, not a spend capacity equation. You cannot actually spend to $1.47M without changing reg volume — and here's why it's not a simple "spend $340K more."

**Brand is wildly under CCP.** YTD brand CPA is ~$19 (3,089 regs / $59,382). CCP is $97. Brand is running at ~20% ie%CCP on its own. You have almost no room to push brand spend higher because brand is demand-constrained, not budget-constrained.

**NB is over CCP and getting worse as you scale.** YTD NB CPA is ~$131. CCP is $28. NB is at ~470% of CCP. The elasticity curve (NB CPA = 0.02 × spend^0.937) says every dollar you add to NB makes CPA worse, not better. Pushing NB harder burns the ceiling faster than it creates it.

Practically: the $340K of headroom is only real if **brand volume grows into it**. If you push spend without volume, ie%CCP drops toward the current 77%, not up toward 100%.

---

## What I'd actually tell Lorena

"Full-year ceiling at 100% ie%CCP is **~$1.47M** using the current W17-W52 forecast. That's **$340K above our baseline spend trajectory of $1.13M**. The $1.3M you saw earlier assumed Sparkle-persist decayed faster than our current forecast does — if you believe the W15-W16 bump holds, $1.47M is the number. If you don't, it's closer to $1.28M.

**But** the headroom is mostly theoretical. Brand is supply-constrained (CPA $19 vs CCP $97), NB gets more expensive as we scale it (elasticity exponent 0.937). We can't spend to the ceiling without structural volume growth — we can only spend against it as volume materializes."

---

## Assumptions and gaps

- **Forecast version:** `ps.forecasts` 4/21 bayesian_seasonal_brand_nb_split. W17-W52 = 36 weeks, covers through end of year. If you want to lock a number for a commitment, I'd want to stress-test this against W16 actuals one more time.
- **Sparkle persistence:** Biggest swing factor. Currently embedded as "partial persist." If Lorena has a stronger POV, rerun with her assumption.
- **NB elasticity:** Curve is fit from 2025 H1 + 2026 YTD and is directionally right at weekly grain but noisy. Don't use it for within-$10K decisions.
- **Range I'd defend:** $1.25M – $1.55M depending on Sparkle assumption. $1.47M is the point estimate using current forecast as-is.

---

**Sources:**
- YTD actuals: `ps.v_weekly WHERE market='MX' AND period_start BETWEEN '2026-01-04' AND '2026-04-12'`
- Forecast: `ps.forecasts WHERE market='MX' AND period_type='weekly' AND forecast_date='2026-04-21'`
- CCPs: `ps.market_constraints_manual.notes` (MX row, updated 2026-04-22)
- Prior $1.3M / $1.25M: Lorena email analysis (referenced in briefing; not located in shared/ — treating as user-provided anchor)
