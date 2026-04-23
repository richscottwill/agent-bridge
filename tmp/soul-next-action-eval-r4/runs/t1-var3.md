# US Full-Year Spend Ceiling — 100% ie%CCP, +10% CVR Lift

**Request:** Full-year US spend ceiling if we hold 100% ie%CCP, assuming OCI-driven 10% CVR lift from current baseline.
**Inputs stated:** Brand CCP $412.51, NB CCP $48.52.
**Baseline:** ps.v_weekly, market='US', W1–W16 2026 (16 weeks YTD).
**Date:** 2026-04-22.

---

## Headline — read this first

**You cannot hold 100% ie%CCP on NB at the stated CCP ($48.52) with a 10% CVR lift. Current NB CPA is already 58% above the CCP, and a 10% CVR lift only closes ~9pts of that gap. The "ceiling" question as posed is structurally infeasible for NB without additional CPC or CVR improvement.**

- **Brand post-lift CPA:** $64.28 → ie%CCP 15.6% (massive headroom)
- **NB post-lift CPA:** $69.62 → ie%CCP 143.5% (still over ceiling)
- **Blended post-lift ie%CCP (spend-weighted):** ~106% — still above 100% threshold

So the honest answer has two parts: (1) the mechanical number you asked for, caveated, and (2) what it actually means for planning.

---

## YTD Baseline (W1–W16, pulled from ps.v_weekly)

| Metric | Brand | NB | Total |
|---|---|---|---|
| Registrations | 42,637 | 93,999 | 136,636 |
| Spend | $3,014,649 | $7,199,053 | $10,213,702 |
| CPA (YTD blended) | $70.70 | $76.59 | $74.75 |
| CPC (YTD) | $2.87 | $4.48 | — |
| Clicks | 1,050,965 | 1,606,050 | 2,657,015 |
| Spend mix | 29.5% | 70.5% | 100% |

**Post-10% CVR lift at flat CPC** (CPA × 1/1.10 = CPA × 0.9091):
- Brand CPA: $70.70 → **$64.28**
- NB CPA: $76.59 → **$69.62**

---

## Mechanical Ceiling — three readings, none clean

### Reading A — "Ceiling = projected FY spend at current efficiency + 10% CVR lift"
*(Straight run-rate: clicks and CPC hold, CVR +10%, spend scales proportionally with regs.)*
- Brand FY spend ≈ $3.01M × (52/16) × 1.10 = **$10.76M**
- NB FY spend ≈ $7.20M × (52/16) × 1.10 = **$25.74M**
- **Combined FY ceiling ≈ $36.5M**
- **Blended ie%CCP at this spend ≈ 106% — does NOT satisfy the 100% constraint.**

This is the closest thing to a "ceiling" the data actually supports. It reflects "what can we spend if efficiency improves 10% and we don't change the mix." **It does not hit 100% ie%CCP.**

### Reading B — "Ceiling = max spend that keeps blended CPA ≤ blended CCP"
Blended CCP (YTD reg-weighted) = (0.312 × $412.51) + (0.688 × $48.52) = **$162.13**. Post-lift blended CPA = **$68.00**. Huge headroom — 2.4x.

If blended CPA held at $68.00 across any spend level (zero elasticity), the ceiling is unbounded — meaningless. With standard elasticity (exponent ~0.9 documented for other markets, no US-specific model supplied), CPA would rise as spend scales, and the ceiling would be where CPA = $162.13. Without a US elasticity curve in ps.elasticity_curves, **I can't compute this honestly.** Flagging — do not cite Reading B.

### Reading C — "Ceiling = FY regs × per-stream CCP, stream by stream"
*(Assumes each stream independently runs to its CCP exactly. Mathematically: regs capacity × price.)*
- Brand FY regs (post-lift) ≈ 42,637 × 3.25 × 1.10 = 152,428 → × $412.51 = **$62.9M**
- NB FY regs (post-lift) ≈ 93,999 × 3.25 × 1.10 = 336,047 → × $48.52 = **$16.3M**
- **Combined ≈ $79.2M**

This number is ~8x current Brand run-rate. It's mechanically what the formula returns, but it assumes elasticity stays flat at any spend level, which is false. **Do not cite this in isolation.** Included for transparency only.

---

## Recommendation on which number to cite

**If Brandon/Kate asks "what's the US ceiling at 100% ie%CCP?" the correct answer is: "The constraint isn't binding the way you think. NB is already over CCP and Brand has massive headroom. What's the actual planning question?"**

If forced to give one number:
- For **run-rate planning**: cite **~$36.5M FY** (Reading A) and note it runs ~106% ie%CCP, not 100%.
- For **upside framing** ("how much could we absorb if efficiency holds"): do not cite Reading C without an elasticity curve. Say "$36.5M supports 10% CVR lift at current mix; additional spend requires CPC reduction or NB CPA reduction to bring NB under its CCP."

---

## Top 3 Assumptions (directional sensitivity)

1. **Flat CPC at current $2.87 Brand / $4.48 NB.** If Brand CPC rises 10% with scale, post-lift Brand CPA = $70.70 → Brand still has headroom. If NB CPC rises 10% with scale, post-lift NB CPA = $76.60 → NB gap widens, ceiling drops further below 100%. *CPC-up pushes ceiling down.*
2. **10% CVR lift applied uniformly to Brand and NB.** If lift is NB-skewed (likely from OCI targeting logic), post-lift NB CPA could be closer to $63 (15% NB lift) — still over the $48.52 CCP. If lift is Brand-skewed, Brand ie%CCP gets even more headroom but NB stays broken. *Mix-skew doesn't solve NB.*
3. **16-week YTD is representative of full year.** W7–W10 showed CPA spikes ($83–$93 Brand, $81–$98 NB) — likely a cost event or auction regime change. If H2 reverts to W1–W6 efficiency, the ceiling math gets $2–3M more favorable. If H2 tracks W7–W10, the ceiling tightens by ~$2M. *Seasonality/regime unknown, 16wk base is not a strong predictor.*

---

## Confidence: 40%

**Why not higher:**
- No US elasticity curve in ps.elasticity_curves or ps.v_weekly (ie%CCP column is 100% null per data audit 2026-04-22). All three readings above use zero-elasticity or linear-scaling assumptions.
- The question as phrased ("ceiling at 100% ie%CCP") doesn't have a single correct answer — three defensible readings give $36.5M, $79.2M, or "unbounded."
- NB being over CCP means "holding 100% ie%CCP" is not a ceiling, it's a constraint violation we'd need to fix first — the question conflates two different things.

**Why not lower:**
- YTD 16-week data is clean and recent (through W16, pulled live from ps.v_weekly).
- CPA and CPC math is straightforward arithmetic, not modeled.
- Brand vs. NB CCPs stated by Richard directly — no ambiguity on inputs.

---

## Human review strongly recommended before action.

Before this number goes into any Brandon/Kate/Lorena conversation, confirm:

1. Which reading (A / B / C) matches the question Brandon or Kate is actually asking. "Ceiling" can mean run-rate, capacity, or break-even — these are three different numbers and the wrong one in a 1:1 is a material miscite.
2. Whether a US elasticity curve exists outside ps.v_weekly (e.g., Natalia's team, MarTech modeling). If one exists, Reading B becomes the correct frame and everything above gets rerun.
3. Whether the stated NB CCP of $48.52 is the current active number. NB actual CPA has been $70+ all year; a $48.52 CCP implies a ~36% CPA reduction target, which is a separate strategic question from "can we hold 100% ie%CCP."

---

## Data lineage
- Source: `ps.v_weekly`, market='US', period_key IN W1–W16 2026
- Query run: 2026-04-22
- ie%CCP column null for 100% of rows (data audit flag) — all ie%CCP math derived from CPA ÷ stated CCP
- No elasticity applied (none available for US in ps.elasticity_curves as of last audit)
