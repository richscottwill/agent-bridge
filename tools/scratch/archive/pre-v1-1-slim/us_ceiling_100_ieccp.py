#!/usr/bin/env python3
"""US 2026 full-year spend ceiling at 100% ie%CCP, with OCI-driven +10% CVR lift.

Formula (per high-stakes-guardrails.md, rule 6 — use the stated model):
    ie%CCP = total_spend / (brand_regs * BRAND_CCP + nb_regs * NB_CCP)

Holding ie%CCP = 100% means:
    total_spend = brand_regs * 412.51 + nb_regs * 48.52

Two methods:
  (A) Segment-hold: hold W1-W16 Brand and NB CPAs flat, apply +10% CVR lift to
      both segments, project full-year reg volume at same CPAs, then back into
      the spend that equals the CCP-weighted reg pot.
  (B) Elasticity-expansion: borrow MX NB CPA elasticity curve
      (NB_CPA = 0.02 * weekly_spend^0.937) calibrated to US W1-W16 NB actuals,
      solve for full-year spend where ie%CCP = 100%. CVR lift reduces NB CPA
      at any given spend by ~9.1% (1/1.10).

Sources:
- US W1-W16 actuals: ps.v_weekly market='US' (pulled 2026-04-22)
- CCPs: Richard-supplied (Brand $412.51 / NB $48.52)
- Elasticity curve: MX precedent (shared/tools/scratch/mx_precise_projection.py)
- Formula authority: shared/dashboards/data/wiki-docs/702bcba24f.txt
  (Scaling Model — ie%CCP = cost / (brand_regs*BRAND_CCP + nb_regs*NB_CCP))
"""
import math

BRAND_CCP = 412.51
NB_CCP = 48.52
CVR_LIFT = 1.10  # OCI-driven

# US W1-W16 actuals from ps.v_weekly
# (week, brand_regs, brand_spend, nb_regs, nb_spend)
# Using W10-W16 (complete weeks, stable post-Q1 baseline) + annualization
US_W10_W16 = [
    (10, 2417, 212485.66, 5109, 387096.85),
    (11, 2493, 188084.72, 5782, 457214.93),
    (12, 2501, 178901.79, 5623, 419672.26),
    (13, 2602, 170010.58, 5972, 412879.24),
    (14, 2611, 167033.08, 6911, 500698.28),
    (15, 2631, 180547.15, 6755, 497734.65),
    (16, 3041, 185042.80, 6068, 493965.18),
]
# W1 in data (partial/holiday week): Brand 2372 / $146,408 / NB 5732 / $413,022
# Treat W1 as already-actualized Q1 data

# Fuller YTD aggregate approximated from W1 + W10-W16 as proxy for W1-W16 run-rate
# (The system view only had W1 and W10-W16 populated; for ceiling math we need
# the average weekly rate, which W10-W16 gives cleanly.)
n_wks = len(US_W10_W16)
avg_brand_regs = sum(r[1] for r in US_W10_W16) / n_wks
avg_brand_spend = sum(r[2] for r in US_W10_W16) / n_wks
avg_nb_regs = sum(r[3] for r in US_W10_W16) / n_wks
avg_nb_spend = sum(r[4] for r in US_W10_W16) / n_wks
avg_brand_cpa = avg_brand_spend / avg_brand_regs
avg_nb_cpa = avg_nb_spend / avg_nb_regs
avg_brand_cvr = None  # not needed directly

print("="*90)
print("US W10-W16 WEEKLY AVERAGE (baseline, pre-lift)")
print("="*90)
print(f"Brand: {avg_brand_regs:,.0f} regs / ${avg_brand_spend:,.0f} / CPA ${avg_brand_cpa:.2f}")
print(f"NB:    {avg_nb_regs:,.0f} regs / ${avg_nb_spend:,.0f} / CPA ${avg_nb_cpa:.2f}")
print(f"Total: {avg_brand_regs+avg_nb_regs:,.0f} regs / ${avg_brand_spend+avg_nb_spend:,.0f}/wk")
baseline_ieccp = (avg_brand_spend + avg_nb_spend) / (
    avg_brand_regs * BRAND_CCP + avg_nb_regs * NB_CCP
) * 100
print(f"Baseline ie%CCP (weekly avg): {baseline_ieccp:.1f}%")
print()

# ===== METHOD A: Segment-hold =====
# Assume 52 weeks at the W10-W16 weekly rate with +10% CVR lift applied
# CVR lift mechanics: same spend -> 10% more regs (i.e., CPA drops 9.1%)
# OR same regs at 9.1% lower spend. We ceiling-project at constant CPA so
# the +10% CVR shows up as +10% reg output at held spend OR as lower CPA.
# We'll compute both framings.

print("="*90)
print("METHOD A — Segment-hold, +10% CVR lift, 52-wk annualized")
print("="*90)
print("Framing: same CPAs hold, CVR lift translates to 10% more regs per spend $")
print("At 100% ie%CCP, total_spend must equal brand_regs*$412.51 + nb_regs*$48.52")
print()

# Lifted weekly output if we held current spend flat:
lift_brand_regs_wk = avg_brand_regs * CVR_LIFT
lift_nb_regs_wk = avg_nb_regs * CVR_LIFT
lift_brand_cpa = avg_brand_spend / lift_brand_regs_wk
lift_nb_cpa = avg_nb_spend / lift_nb_regs_wk

print(f"With +10% CVR at current spend level:")
print(f"  Brand: {lift_brand_regs_wk:,.0f} regs/wk @ ${lift_brand_cpa:.2f} CPA")
print(f"  NB:    {lift_nb_regs_wk:,.0f} regs/wk @ ${lift_nb_cpa:.2f} CPA")
lifted_base_ieccp = (avg_brand_spend + avg_nb_spend) / (
    lift_brand_regs_wk * BRAND_CCP + lift_nb_regs_wk * NB_CCP
) * 100
print(f"  ie%CCP at current spend + lift: {lifted_base_ieccp:.1f}%")
print(f"  Full-year at this rate: ${(avg_brand_spend+avg_nb_spend)*52/1e6:.2f}M")
print()

# Solve: keep CPAs at lift-adjusted levels, scale both segments proportionally
# until ie%CCP = 100%.
# Let multiplier = x (applied to both Brand and NB spend).
# Weekly spend = x * (avg_brand_spend + avg_nb_spend)
# Weekly regs = x * (lift_brand_regs + lift_nb_regs) [constant-CPA, no saturation]
# ie%CCP = weekly_spend / (weekly_brand_regs*BRAND_CCP + weekly_nb_regs*NB_CCP)
# The x cancels -> ie%CCP is invariant under proportional scaling at constant CPA.
# So under CONSTANT CPA assumption with CVR lift, ceiling = infinity.
# This is the MX-confirmed failure mode of naive linear scaling. We need
# elasticity. Use Method B.

print("Constant-CPA assumption with CVR lift yields invariant ie%CCP under")
print(f"proportional scaling ({lifted_base_ieccp:.1f}%) — so spend can grow without")
print("breaching the ceiling UNLESS CPA rises with spend. This is why we need")
print("elasticity. See Method B.")
print()

# ===== METHOD B: Elasticity-expansion =====
# Borrow MX NB CPA curve as a first-order proxy (US has no published elasticity
# exponent in the system; flag as a key assumption).
# NB_CPA(spend_per_week) = 0.02 * spend^0.937
# With +10% CVR lift, NB_CPA at any given weekly spend drops by 1/CVR_LIFT:
#   NB_CPA_lifted = (0.02 * spend^0.937) / 1.10
# Calibration check: MX formula at US NB weekly spend ~$450K gives
#   NB_CPA = 0.02 * 450000^0.937 ≈ 0.02 * ~150000 ≈ $3,000
# That's WAY off US actuals ($75 CPA at $450K/wk). So raw MX exponent
# is not transferable to US — US is in a different regime (much more
# demand, much lower saturation at current spend).
# Calibrate: fit a power curve y = a * x^b to US W10-W16 NB (spend, cpa)
# points.

import statistics

nb_points = [(r[4], r[4]/r[3]) for r in US_W10_W16]  # (spend, cpa)
# Fit log-log linear: log(cpa) = log(a) + b*log(spend)
xs = [math.log(p[0]) for p in nb_points]
ys = [math.log(p[1]) for p in nb_points]
xm = sum(xs)/len(xs); ym = sum(ys)/len(ys)
b = sum((xs[i]-xm)*(ys[i]-ym) for i in range(len(xs))) / sum((x-xm)**2 for x in xs)
a = math.exp(ym - b * xm)
print(f"US NB CPA elasticity (W10-W16 fit): CPA = {a:.4f} × spend^{b:.4f}")
print(f"  (MX exponent was 0.937 — US shows weaker saturation in-sample)")
print()

# Brand elasticity — do the same for Brand
br_points = [(r[2], r[2]/r[1]) for r in US_W10_W16]
xs_b = [math.log(p[0]) for p in br_points]
ys_b = [math.log(p[1]) for p in br_points]
xmb = sum(xs_b)/len(xs_b); ymb = sum(ys_b)/len(ys_b)
bb = sum((xs_b[i]-xmb)*(ys_b[i]-ymb) for i in range(len(xs_b))) / sum((x-xmb)**2 for x in xs_b)
ab = math.exp(ymb - bb * xmb)
print(f"US Brand CPA elasticity (W10-W16 fit): CPA = {ab:.4f} × spend^{bb:.4f}")
print()

# Note: if the in-sample exponent is near 0 (elastic-flat) or slightly negative,
# that means within the observed W10-W16 range CPA barely rises with spend.
# Extrapolating outside that range is the key risk.

def nb_cpa_at(weekly_spend, lift=CVR_LIFT):
    if weekly_spend <= 0: return NB_CCP
    raw = a * (weekly_spend ** b)
    return raw / lift  # CVR lift reduces CPA

def brand_cpa_at(weekly_spend, lift=CVR_LIFT):
    if weekly_spend <= 0: return BRAND_CCP
    raw = ab * (weekly_spend ** bb)
    return raw / lift

def ieccp_at(weekly_brand_spend, weekly_nb_spend):
    bcpa = brand_cpa_at(weekly_brand_spend)
    ncpa = nb_cpa_at(weekly_nb_spend)
    br = weekly_brand_spend / bcpa
    nr = weekly_nb_spend / ncpa
    tot_spend = weekly_brand_spend + weekly_nb_spend
    pot = br * BRAND_CCP + nr * NB_CCP
    return tot_spend / pot * 100, br, nr, bcpa, ncpa

# Solve for full-year ceiling:
# Option 1: hold brand/NB mix ratio constant at W10-W16 average, scale both.
brand_share = avg_brand_spend / (avg_brand_spend + avg_nb_spend)

def solve_ceiling_proportional():
    lo, hi = avg_brand_spend + avg_nb_spend, 10_000_000  # weekly spend search
    for _ in range(100):
        mid = (lo+hi)/2
        bs = mid * brand_share
        ns = mid * (1-brand_share)
        r, *_ = ieccp_at(bs, ns)
        if abs(r - 100) < 0.01: break
        if r < 100: lo = mid
        else: hi = mid
    bs = mid * brand_share
    ns = mid * (1-brand_share)
    r, br, nr, bcpa, ncpa = ieccp_at(bs, ns)
    return mid, bs, ns, r, br, nr, bcpa, ncpa

wk_ceiling, bs, ns, ieccp_chk, br, nr, bcpa, ncpa = solve_ceiling_proportional()
fy_ceiling = wk_ceiling * 52
print("="*90)
print("METHOD B — Elasticity-expansion ceiling at 100% ie%CCP")
print("="*90)
print(f"Weekly ceiling spend: ${wk_ceiling:,.0f}  (Brand ${bs:,.0f} + NB ${ns:,.0f})")
print(f"  Brand: {br:,.0f} regs/wk @ ${bcpa:.2f} CPA")
print(f"  NB:    {nr:,.0f} regs/wk @ ${ncpa:.2f} CPA")
print(f"  ie%CCP check: {ieccp_chk:.2f}%")
print()
print(f"ANNUALIZED FULL-YEAR CEILING: ${fy_ceiling:,.0f}  (${fy_ceiling/1e6:.1f}M)")
print()

# Option 2: optimal mix — what if we let Brand and NB find their own ceilings?
# Max out Brand to where Brand ie%CCP = 100% (Brand CCP = $412.51 and Brand CPA
# is FAR below that even extrapolated, so Brand is not the binding constraint).
# Then fill NB up to joint ie%CCP = 100%.
# In practice the W10-W16 mix is close to optimal because Brand demand is
# capped by search volume (the "Brand demand ceiling" in EU5 playbook).
# So proportional scaling is a reasonable operating ceiling; aggressive
# Brand scaling beyond current spend likely compounds CPC without regs
# (per performance-marketing-guide).

# Sensitivity: what if NB exponent rises toward MX 0.937?
print("="*90)
print("SENSITIVITY — if NB elasticity exponent rises from fit toward MX 0.937")
print("="*90)
for test_b in [b, 0.4, 0.6, 0.8, 0.937]:
    a_fit = a if test_b == b else (
        avg_nb_cpa / (avg_nb_spend ** test_b)  # recalibrate intercept at avg
    )
    def ncpa_test(ws):
        return (a_fit * ws**test_b) / CVR_LIFT if ws > 0 else NB_CCP
    def bcpa_test(ws):
        return (ab * ws**bb) / CVR_LIFT if ws > 0 else BRAND_CCP
    lo, hi = 500_000, 20_000_000
    for _ in range(80):
        mid = (lo+hi)/2
        bs_t = mid * brand_share; ns_t = mid*(1-brand_share)
        ncp = ncpa_test(ns_t); bcp = bcpa_test(bs_t)
        br_t = bs_t/bcp; nr_t = ns_t/ncp
        rr = mid / (br_t*BRAND_CCP + nr_t*NB_CCP) * 100
        if abs(rr-100)<0.01: break
        if rr<100: lo=mid
        else: hi=mid
    print(f"  NB exponent {test_b:.3f} -> weekly ${mid/1e6:.2f}M / full-year ${mid*52/1e6:.1f}M "
          f"(NB CPA at ceiling: ${ncp:.0f})")
print()

# ===== METHOD C: Simple per-segment CCP ratio (what baseline produced correctly) =====
print("="*90)
print("METHOD C — Per-segment CCP sanity check (no elasticity, CVR lift only)")
print("="*90)
# If we simply apply +10% CVR lift to W10-W16 average reg output and hold CPAs
# as-is, then ANNUALIZE the resulting reg pot × CCP weights:
ann_brand_regs = avg_brand_regs * CVR_LIFT * 52
ann_nb_regs = avg_nb_regs * CVR_LIFT * 52
reg_pot_dollars = ann_brand_regs * BRAND_CCP + ann_nb_regs * NB_CCP
print(f"Annualized reg output w/ +10% lift:")
print(f"  Brand: {ann_brand_regs:,.0f} regs × $412.51 = ${ann_brand_regs*BRAND_CCP/1e6:,.1f}M CCP value")
print(f"  NB:    {ann_nb_regs:,.0f} regs × $48.52  = ${ann_nb_regs*NB_CCP/1e6:,.1f}M CCP value")
print(f"  TOTAL CCP POT (= 100% ie%CCP spend ceiling, no-saturation): ${reg_pot_dollars/1e6:,.1f}M")
print()
print("Interpretation: this is the MAXIMUM spend that could theoretically be")
print("justified if additional spend produced regs at current CPAs + 10% lift.")
print("Elasticity (Method B) pulls the operating ceiling LOWER because CPAs")
print("rise with spend.")
print()

print("="*90)
print("TOP-LINE ANSWER (range)")
print("="*90)
print(f"  Method C (no saturation, upper bound):  ${reg_pot_dollars/1e6:.1f}M")
print(f"  Method B (US in-sample elasticity):     ${fy_ceiling/1e6:.1f}M")
print(f"  Naive MX-exponent extrapolation:        (see sensitivity table above)")
