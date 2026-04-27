"""MX Brand-only May→Dec scenario + NB sizing for 75% ie%CCP year-end.

Scenario:
  - Jan-Apr (W1-W16): actuals as observed
  - May-Dec (W17-W52): Brand continues at current run-rate, shaped by Brand seasonality.
    NB spend = 0 from May onward.
  - Compute resulting Y2026 ie%CCP.

Then:
  - Given that Brand trajectory and YTD NB actuals, how much ADDITIONAL NB spend May-Dec
    (shaped by NB seasonality) would drive Y2026 ie%CCP to 75%?
  - Use MX NB CPA elasticity curve: log(CPA) = a + b * log(weekly_spend).

CCPs: Brand $90, NB $30 (from dashboard reconciliation 2026-04-22).
"""
import sys
import math
sys.path.insert(0, 'shared/tools/prediction')
from mpe_engine import _db, load_parameters

con = _db()

BRAND_CCP = 90.0
NB_CCP = 30.0

def header(t):
    print(f"\n{'='*60}\n{t}\n{'='*60}")

# ---------- 1. YTD actuals ----------
ytd_q = con.execute("""
    SELECT COUNT(*), SUM(cost), SUM(brand_cost), SUM(nb_cost),
           SUM(registrations), SUM(brand_registrations), SUM(nb_registrations)
    FROM ps.v_weekly
    WHERE market='MX' AND period_start >= '2026-01-01' AND period_start <= '2026-04-12'
""").fetchone()
weeks_ytd, ytd_total, ytd_brand_sp, ytd_nb_sp, ytd_total_r, ytd_brand_r, ytd_nb_r = ytd_q

header("1. YTD actuals (W1-W16, 15 weeks)")
print(f"  Brand:  ${ytd_brand_sp:>8,.0f}  |  {ytd_brand_r:,} regs  |  CPA ${ytd_brand_sp/ytd_brand_r:.2f}")
print(f"  NB:     ${ytd_nb_sp:>8,.0f}  |  {ytd_nb_r:,} regs  |  CPA ${ytd_nb_sp/ytd_nb_r:.2f}")
print(f"  Total:  ${ytd_total:>8,.0f}  |  {ytd_total_r:,} regs")
ytd_ieccp = ytd_total / (ytd_brand_r * BRAND_CCP + ytd_nb_r * NB_CCP)
print(f"  YTD ie%CCP (Brand $90 / NB $30): {ytd_ieccp*100:.1f}%")

# ---------- 2. Brand recent run-rate (W13-W16) ----------
last4 = con.execute("""
    SELECT AVG(brand_cost), AVG(brand_registrations)
    FROM (SELECT brand_cost, brand_registrations FROM ps.v_weekly WHERE market='MX' ORDER BY period_start DESC LIMIT 4)
""").fetchone()
l4_brand_sp_wk, l4_brand_r_wk = last4
print(f"\nRun-rate Brand (W13-W16 avg): ${l4_brand_sp_wk:,.0f}/wk | {l4_brand_r_wk:.0f} regs/wk | CPA ${l4_brand_sp_wk/l4_brand_r_wk:.2f}")

# ---------- 3. Brand seasonality — shape per-week for W17-W52 ----------
params = load_parameters('MX')
brand_seas = params['brand_seasonality_shape']['value_json']
nb_seas = params['nb_seasonality_shape']['value_json']
nb_cpa_elast = params['nb_cpa_elasticity']['value_json']

# Seasonality weights are 52-length, indexed 0=W1..51=W52.
# Normalize so that W17-W52 sum to the fraction of annual that those weeks represent.
brand_weights = brand_seas['weights']
nb_weights = nb_seas['weights']

# The run-rate is anchored on W13-W16. We want to project W17-W52 preserving seasonality shape.
# Approach: the "level" in W13-W16 = avg_brand_regs_wk. Adjust per-week by weight[w] / avg(weights[12:16]).
w13_16_brand_wt_avg = sum(brand_weights[12:16]) / 4
print(f"\n2. Projecting Brand W17-W52 (seasonality-shaped, run-rate anchor {l4_brand_r_wk:.0f} regs/wk at avg seasonal weight {w13_16_brand_wt_avg:.3f})")

roy_brand_regs = 0
roy_brand_spend = 0
brand_cpa_recent = l4_brand_sp_wk / l4_brand_r_wk
for w_idx in range(16, 52):  # W17 = idx 16 .. W52 = idx 51
    rel_weight = brand_weights[w_idx] / w13_16_brand_wt_avg
    wk_regs = l4_brand_r_wk * rel_weight
    wk_spend = wk_regs * brand_cpa_recent
    roy_brand_regs += wk_regs
    roy_brand_spend += wk_spend

print(f"  W17-W52 Brand: {roy_brand_regs:,.0f} regs  |  ${roy_brand_spend:,.0f} spend  |  CPA ${roy_brand_spend/roy_brand_regs:.2f}")

# ---------- 4. Brand-only Y2026 total ----------
header("3. Brand-only Y2026 (actuals Jan-Apr + Brand seasonality May-Dec, NB = $0 from May)")
y2026_brand_regs = ytd_brand_r + roy_brand_regs
y2026_brand_spend = ytd_brand_sp + roy_brand_spend
y2026_nb_regs_brand_only = ytd_nb_r   # YTD only, no May-Dec NB
y2026_nb_spend_brand_only = ytd_nb_sp
y2026_total_regs = y2026_brand_regs + y2026_nb_regs_brand_only
y2026_total_spend = y2026_brand_spend + y2026_nb_spend_brand_only
y2026_ieccp_brand_only = y2026_total_spend / (y2026_brand_regs * BRAND_CCP + y2026_nb_regs_brand_only * NB_CCP)

print(f"  Brand Y2026: ${y2026_brand_spend:,.0f}  |  {y2026_brand_regs:,.0f} regs  |  CPA ${y2026_brand_spend/y2026_brand_regs:.2f}")
print(f"  NB Y2026 (YTD only): ${y2026_nb_spend_brand_only:,.0f}  |  {y2026_nb_regs_brand_only:,} regs")
print(f"  Total Y2026: ${y2026_total_spend:,.0f}  |  {y2026_total_regs:,.0f} regs")
print(f"  Y2026 ie%CCP (Brand-only May-Dec): {y2026_ieccp_brand_only*100:.1f}%")

# ---------- 5. Solve: what NB May-Dec spend hits 75% ie%CCP Y2026? ----------
# Add X dollars of NB spend May-Dec, shaped by NB seasonality.
# NB CPA depends on weekly NB spend via elasticity: log(CPA) = a + b * log(spend)
a, b = nb_cpa_elast['a'], nb_cpa_elast['b']
print(f"\n4. NB CPA elasticity (active v5, 83w post-gate fit): log(CPA) = {a:.3f} + {b:.3f} * log(weekly_spend)")
print(f"   At $15K/wk -> NB CPA ${math.exp(a + b*math.log(15000)):.2f}")
print(f"   At $20K/wk -> NB CPA ${math.exp(a + b*math.log(20000)):.2f}")
print(f"   At $25K/wk -> NB CPA ${math.exp(a + b*math.log(25000)):.2f}")

w13_16_nb_wt_avg = sum(nb_weights[12:16]) / 4

def project_nb_roy(avg_weekly_nb_spend):
    """Given an avg NB weekly spend for RoY, shape by seasonality and compute total NB regs via elasticity."""
    roy_nb_regs = 0.0
    roy_nb_spend = 0.0
    for w_idx in range(16, 52):
        rel_weight = nb_weights[w_idx] / w13_16_nb_wt_avg
        wk_spend = max(avg_weekly_nb_spend * rel_weight, 1.0)
        wk_cpa = math.exp(a + b * math.log(wk_spend))
        wk_regs = wk_spend / wk_cpa
        roy_nb_regs += wk_regs
        roy_nb_spend += wk_spend
    return roy_nb_regs, roy_nb_spend


def y2026_ieccp_at_nb_avg(avg_weekly_nb_spend):
    """Full Y2026 ie%CCP given a May-Dec NB weekly average spend."""
    roy_nb_r, roy_nb_sp = project_nb_roy(avg_weekly_nb_spend)
    tot_nb_r = ytd_nb_r + roy_nb_r
    tot_nb_sp = ytd_nb_sp + roy_nb_sp
    tot_b_r = y2026_brand_regs
    tot_b_sp = y2026_brand_spend
    tot_sp = tot_b_sp + tot_nb_sp
    iec = tot_sp / (tot_b_r * BRAND_CCP + tot_nb_r * NB_CCP)
    return iec, tot_nb_sp, tot_nb_r, tot_sp, tot_b_r + tot_nb_r

# Bisection for 75% target
target = 0.75
lo, hi = 0.0, 100000.0
for _ in range(60):
    mid = (lo + hi) / 2
    iec, _, _, _, _ = y2026_ieccp_at_nb_avg(mid)
    if iec < target:
        lo = mid
    else:
        hi = mid
best_nb_avg = (lo + hi) / 2
iec_result, tot_nb_sp_result, tot_nb_r_result, tot_sp_result, tot_r_result = y2026_ieccp_at_nb_avg(best_nb_avg)

header("5. Solution: MX Y2026 @ 75% ie%CCP via NB spend sizing May-Dec")
print(f"  Required May-Dec NB avg weekly spend: ${best_nb_avg:,.0f}/wk")
print(f"  -> May-Dec NB spend: ${tot_nb_sp_result - ytd_nb_sp:,.0f}  (over 36 weeks)")
print(f"  -> May-Dec NB regs: {tot_nb_r_result - ytd_nb_r:,.0f}")
print(f"  Y2026 TOTAL NB: ${tot_nb_sp_result:,.0f}  |  {tot_nb_r_result:,.0f} regs")
print(f"  Y2026 TOTAL BRAND: ${y2026_brand_spend:,.0f}  |  {y2026_brand_regs:,.0f} regs")
print(f"  Y2026 TOTAL: ${tot_sp_result:,.0f}  |  {tot_r_result:,.0f} regs")
print(f"  Y2026 ie%CCP: {iec_result*100:.1f}%")

# For reference: show 100% target too
lo, hi = 0.0, 100000.0
for _ in range(60):
    mid = (lo + hi) / 2
    iec, _, _, _, _ = y2026_ieccp_at_nb_avg(mid)
    if iec < 1.00:
        lo = mid
    else:
        hi = mid
nb_100 = (lo + hi) / 2
iec100, tot_nb_sp100, _, tot_sp100, _ = y2026_ieccp_at_nb_avg(nb_100)
print(f"\n  For comparison, 100% ie%CCP target:")
print(f"    NB avg weekly: ${nb_100:,.0f}/wk")
print(f"    Y2026 total spend: ${tot_sp100:,.0f}")

# And continuing current NB run-rate (W13-W16 = $19K/wk)
iec_continue, tnsp_c, tnr_c, tsp_c, tr_c = y2026_ieccp_at_nb_avg(19033.0)
print(f"\n  For comparison, continuing W13-W16 NB run-rate $19K/wk May-Dec:")
print(f"    Y2026 total spend: ${tsp_c:,.0f}  |  {tr_c:,.0f} regs")
print(f"    Y2026 ie%CCP: {iec_continue*100:.1f}%")


# ---------- 3. Brand seasonality projection W17-W52 ----------
params = load_parameters('MX')
brand_seas = params['brand_seasonality_shape']['value_json']
nb_seas = params['nb_seasonality_shape']['value_json']
nb_cpa_elast = params['nb_cpa_elasticity']['value_json']

brand_weights = brand_seas['weights']
nb_weights = nb_seas['weights']
w13_16_brand_wt_avg = sum(brand_weights[12:16]) / 4
w13_16_nb_wt_avg = sum(nb_weights[12:16]) / 4

header("2. Brand projection W17-W52 (seasonality-shaped, anchor $4,792/wk 288 regs/wk)")
roy_brand_regs = 0.0
roy_brand_spend = 0.0
brand_cpa_recent = l4_brand_sp_wk / l4_brand_r_wk
for w_idx in range(16, 52):
    rel_weight = brand_weights[w_idx] / w13_16_brand_wt_avg
    wk_regs = l4_brand_r_wk * rel_weight
    wk_spend = wk_regs * brand_cpa_recent
    roy_brand_regs += wk_regs
    roy_brand_spend += wk_spend
print(f"  W17-W52 Brand: {roy_brand_regs:,.0f} regs  |  ${roy_brand_spend:,.0f} spend  |  CPA ${roy_brand_spend/roy_brand_regs:.2f}")

# ---------- 4. Brand-only Y2026 ----------
header("3. Brand-only Y2026 (actuals Jan-Apr + Brand seasonality May-Dec, NB=$0 May-Dec)")
y2026_brand_regs = ytd_brand_r + roy_brand_regs
y2026_brand_spend = ytd_brand_sp + roy_brand_spend
tot_nb_brand_only_regs = ytd_nb_r       # no NB from May
tot_nb_brand_only_spend = ytd_nb_sp
y2026_total_spend = y2026_brand_spend + tot_nb_brand_only_spend
y2026_total_regs = y2026_brand_regs + tot_nb_brand_only_regs
y2026_ieccp_brand_only = y2026_total_spend / (y2026_brand_regs * BRAND_CCP + tot_nb_brand_only_regs * NB_CCP)

print(f"  Brand Y2026:  ${y2026_brand_spend:,.0f}  |  {y2026_brand_regs:,.0f} regs  |  CPA ${y2026_brand_spend/y2026_brand_regs:.2f}")
print(f"  NB Y2026:     ${tot_nb_brand_only_spend:,.0f}  |  {tot_nb_brand_only_regs:,} regs (YTD only)")
print(f"  Total Y2026:  ${y2026_total_spend:,.0f}  |  {y2026_total_regs:,.0f} regs")
print(f"  Y2026 ie%CCP (brand-only May-Dec): {y2026_ieccp_brand_only*100:.1f}%")

# ---------- 5. Solve: what May-Dec NB spend hits 75% ie%CCP Y2026? ----------
a, b = nb_cpa_elast['a'], nb_cpa_elast['b']
print(f"\nNB CPA elasticity (active v5): log(CPA) = {a:.3f} + {b:.3f} * log(weekly_spend)")

def project_nb_roy(avg_weekly_nb_spend):
    roy_r, roy_sp = 0.0, 0.0
    for w_idx in range(16, 52):
        rel = nb_weights[w_idx] / w13_16_nb_wt_avg
        wk_sp = max(avg_weekly_nb_spend * rel, 1.0)
        wk_cpa = math.exp(a + b * math.log(wk_sp))
        wk_r = wk_sp / wk_cpa
        roy_r += wk_r
        roy_sp += wk_sp
    return roy_r, roy_sp

def y2026_ieccp_at_nb_avg(avg_weekly_nb_spend):
    roy_r, roy_sp = project_nb_roy(avg_weekly_nb_spend)
    tot_nb_r = ytd_nb_r + roy_r
    tot_nb_sp = ytd_nb_sp + roy_sp
    tot_sp = y2026_brand_spend + tot_nb_sp
    iec = tot_sp / (y2026_brand_regs * BRAND_CCP + tot_nb_r * NB_CCP)
    return iec, tot_nb_sp, tot_nb_r, tot_sp, y2026_brand_regs + tot_nb_r


# =============================================================
# GLIDE SCENARIOS — lock YTD, model realistic NB paths May-Dec
# =============================================================

def run_scenario_fixed_q2_then_step(q2_weekly, label):
    """A: Q2 (W17-W26, 10 weeks) held flat at q2_weekly; solve for W27-W52 (26 weeks)
    constant weekly spend that lands Y2026 at 75%."""
    header(f"GLIDE A — {label}")
    # Brand spend/regs W17-W52 from seasonality projection (already computed)
    # Now split NB into two segments: Q2 (W17-W26) fixed, Q3-Q4 (W27-W52) solve
    q2_nb_regs, q2_nb_spend = 0.0, 0.0
    for w_idx in range(16, 26):  # W17..W26
        rel = nb_weights[w_idx] / w13_16_nb_wt_avg
        wk_sp = max(q2_weekly * rel, 1.0)
        wk_cpa = math.exp(a + b * math.log(wk_sp))
        wk_r = wk_sp / wk_cpa
        q2_nb_regs += wk_r
        q2_nb_spend += wk_sp
    print(f"  Q2 (W17-W26, ${q2_weekly:,.0f}/wk): ${q2_nb_spend:,.0f} / {q2_nb_regs:,.0f} regs")

    # Binary-search the Q3-Q4 constant weekly that hits Y2026=0.75
    def tot_ieccp(q3q4_weekly):
        q3q4_r, q3q4_sp = 0.0, 0.0
        for w_idx in range(26, 52):
            rel = nb_weights[w_idx] / w13_16_nb_wt_avg
            wk_sp = max(q3q4_weekly * rel, 1.0)
            wk_cpa = math.exp(a + b * math.log(wk_sp))
            wk_r = wk_sp / wk_cpa
            q3q4_r += wk_r
            q3q4_sp += wk_sp
        tot_nb_r = ytd_nb_r + q2_nb_regs + q3q4_r
        tot_nb_sp = ytd_nb_sp + q2_nb_spend + q3q4_sp
        tot_sp = y2026_brand_spend + tot_nb_sp
        iec = tot_sp / (y2026_brand_regs * BRAND_CCP + tot_nb_r * NB_CCP)
        return iec, tot_nb_r, tot_nb_sp, tot_sp, q3q4_r, q3q4_sp

    lo, hi = 0.0, 100000.0
    for _ in range(60):
        mid = (lo + hi) / 2
        iec, *_ = tot_ieccp(mid)
        if iec < 0.75:
            lo = mid
        else:
            hi = mid
    q3q4_wk = (lo + hi) / 2
    iec, tnr, tnsp, tsp, q3q4_r, q3q4_sp = tot_ieccp(q3q4_wk)
    print(f"  Q3-Q4 (W27-W52) solved: ${q3q4_wk:,.0f}/wk avg -> ${q3q4_sp:,.0f} / {q3q4_r:,.0f} regs")
    print(f"  Y2026 total: ${tsp:,.0f} spend | {y2026_brand_regs + tnr:,.0f} regs | ie%CCP {iec*100:.1f}%")
    print(f"  Y2026 NB: ${tnsp:,.0f} | {tnr:,.0f} regs")
    return {'label': label, 'total_spend': tsp, 'total_regs': y2026_brand_regs + tnr, 'ieccp': iec,
            'q2_weekly': q2_weekly, 'q3q4_weekly': q3q4_wk, 'q2_nb_spend': q2_nb_spend, 'q3q4_nb_spend': q3q4_sp}


def run_scenario_linear_decay(start_weekly, label):
    """B: Linear decay from start_weekly (W17) to end_weekly (W52); solve end_weekly for 75%."""
    header(f"GLIDE B — {label}")
    def tot_ieccp(end_weekly):
        roy_r, roy_sp = 0.0, 0.0
        n = 52 - 16  # 36 weeks, W17..W52
        for i, w_idx in enumerate(range(16, 52)):
            frac = i / max(n - 1, 1)
            baseline_wk = start_weekly + frac * (end_weekly - start_weekly)
            rel = nb_weights[w_idx] / w13_16_nb_wt_avg
            wk_sp = max(baseline_wk * rel, 1.0)
            wk_cpa = math.exp(a + b * math.log(wk_sp))
            wk_r = wk_sp / wk_cpa
            roy_r += wk_r
            roy_sp += wk_sp
        tot_nb_r = ytd_nb_r + roy_r
        tot_nb_sp = ytd_nb_sp + roy_sp
        tot_sp = y2026_brand_spend + tot_nb_sp
        iec = tot_sp / (y2026_brand_regs * BRAND_CCP + tot_nb_r * NB_CCP)
        return iec, tot_nb_r, tot_nb_sp, tot_sp, roy_r, roy_sp

    lo, hi = 0.0, 100000.0
    for _ in range(60):
        mid = (lo + hi) / 2
        iec, *_ = tot_ieccp(mid)
        if iec < 0.75:
            lo = mid
        else:
            hi = mid
    end_wk = (lo + hi) / 2
    iec, tnr, tnsp, tsp, roy_r, roy_sp = tot_ieccp(end_wk)
    print(f"  Glide W17 ${start_weekly:,.0f}/wk -> W52 ${end_wk:,.0f}/wk (midpoint ~${(start_weekly+end_wk)/2:,.0f}/wk)")
    print(f"  May-Dec NB: ${roy_sp:,.0f} / {roy_r:,.0f} regs")
    print(f"  Y2026 total: ${tsp:,.0f} spend | {y2026_brand_regs + tnr:,.0f} regs | ie%CCP {iec*100:.1f}%")
    print(f"  Y2026 NB: ${tnsp:,.0f} | {tnr:,.0f} regs")
    return {'label': label, 'total_spend': tsp, 'total_regs': y2026_brand_regs + tnr, 'ieccp': iec,
            'start_weekly': start_weekly, 'end_weekly': end_wk}


# Run the scenarios
s_a = run_scenario_fixed_q2_then_step(19033.0, "Q2 flat at $19K/wk run-rate; Q3-Q4 solved for 75%")
s_b = run_scenario_linear_decay(19033.0, "Linear decay from $19K/wk W17 to solved-level W52, hitting 75% Y2026")

# Comparison summary
header("SUMMARY — all MX Y2026 @ 75% ie%CCP paths")
print(f"{'Scenario':<52} {'Y2026 Spend':>13} {'Y2026 Regs':>12} {'ie%CCP':>8}")
print('-' * 90)
print(f"{'Mechanical solve (no YTD lock — the old wrong $430K)':<52} {'$431,294':>13} {'8,983':>12} {'75.0%':>8}")
print(f"{'Locked-YTD, constant May-Dec NB':<52} {'$730,292':>13} {'14,090':>12} {'75.0%':>8}")
print(f"{'GLIDE A: Q2 flat + Q3-Q4 solved':<52} ${s_a['total_spend']:>12,.0f} {s_a['total_regs']:>12,.0f} {s_a['ieccp']*100:>7.1f}%")
print(f"{'GLIDE B: linear decay W17 to W52':<52} ${s_b['total_spend']:>12,.0f} {s_b['total_regs']:>12,.0f} {s_b['ieccp']*100:>7.1f}%")


# =============================================================
# SPARKLE DECAY SCENARIO
#
# Framing: Brand W15/W16 average Brand spend/regs represents CURRENT = BASELINE + SPARKLE_INCREMENT.
# Pre-Sparkle baseline = average of Oct-Dec 2025 Brand (no Sparkle yet).
# Sparkle increment = current_W15_16 - pre_sparkle_baseline.
# Decay: the INCREMENT decays over the year with a half-life.
# Brand W+ = pre_sparkle_baseline + sparkle_increment × decay_factor(w)
# Brand seasonality shapes the baseline; sparkle increment is flat-in-absolute but decays.
# =============================================================

header("SPARKLE DECAY SCENARIO")

# 1. Pre-Sparkle baseline: Oct-Dec 2025 avg (no Sparkle yet, post-Polaris-launch)
pre_q = con.execute("""
    SELECT AVG(brand_cost), AVG(brand_registrations)
    FROM ps.v_weekly
    WHERE market='MX'
      AND period_start >= '2025-10-01'
      AND period_start <= '2025-12-28'
""").fetchone()
pre_brand_sp_wk, pre_brand_r_wk = pre_q
print(f"  Pre-Sparkle baseline (Oct-Dec 2025 avg): ${pre_brand_sp_wk:,.0f}/wk | {pre_brand_r_wk:.0f} regs/wk")

# 2. W15/W16 average = current level including Sparkle lift
w15_16_q = con.execute("""
    SELECT AVG(brand_cost), AVG(brand_registrations)
    FROM ps.v_weekly
    WHERE market='MX' AND period_key IN ('2026-W15', '2026-W16')
""").fetchone()
cur_brand_sp_wk, cur_brand_r_wk = w15_16_q
print(f"  W15/W16 current level:                   ${cur_brand_sp_wk:,.0f}/wk | {cur_brand_r_wk:.0f} regs/wk")

sparkle_increment_regs = cur_brand_r_wk - pre_brand_r_wk
sparkle_increment_spend = cur_brand_sp_wk - pre_brand_sp_wk
print(f"  Sparkle increment:                       ${sparkle_increment_spend:,.0f}/wk | {sparkle_increment_regs:.0f} regs/wk")
print(f"  (Sparkle is {sparkle_increment_regs/cur_brand_r_wk*100:.0f}% of current Brand volume)")

# 3. Model the decay: half-life approach
# Sparkle peaked ~W15/W16 (mid-April 2026). Decay curves to test:
#   - half_life = 13 weeks (quick decay, gone by year-end)
#   - half_life = 26 weeks (medium, ~25% remaining at year-end)
#   - half_life = 52 weeks (slow, ~75% remaining at year-end)
# Decay formula: decay[w] = 0.5 ** ((w - w16) / half_life_weeks)

def project_brand_with_sparkle_decay(half_life_weeks):
    """Project Brand W17-W52 with baseline + decaying Sparkle increment.
    Baseline is seasonality-shaped (using the brand_seasonality weights relative to pre-Sparkle level).
    """
    pre_baseline_seasonality_w13_16_avg = w13_16_brand_wt_avg  # same shape, different level
    roy_r, roy_sp = 0.0, 0.0
    per_week = []
    for w_idx in range(16, 52):
        weeks_since_peak = (w_idx - 15)  # W16 idx = 15, so W17 = 1 week past peak
        decay = 0.5 ** (weeks_since_peak / half_life_weeks)
        rel = brand_weights[w_idx] / pre_baseline_seasonality_w13_16_avg
        baseline_regs = pre_brand_r_wk * rel
        sparkle_regs = sparkle_increment_regs * decay
        wk_regs = baseline_regs + sparkle_regs
        wk_spend = wk_regs * brand_cpa_recent  # brand_cpa_recent = $16.65 from W13-W16
        roy_r += wk_regs
        roy_sp += wk_spend
        per_week.append((w_idx + 1, baseline_regs, sparkle_regs, wk_regs, decay))
    return roy_r, roy_sp, per_week

# Now we need the earlier-computed variables — run a quick re-anchor if needed
# brand_cpa_recent = l4_brand_sp_wk / l4_brand_r_wk  # already computed above
# brand_weights already loaded

scenarios = [
    ('Fast decay (half-life 13w — Sparkle gone by Q4)', 13),
    ('Medium decay (half-life 26w — ~25% remaining W52)', 26),
    ('Slow decay (half-life 52w — ~75% remaining W52)', 52),
    ('No decay (Sparkle sustained at W15/W16 level)', 9999),
]

def scenario_total(half_life):
    roy_r, roy_sp, _ = project_brand_with_sparkle_decay(half_life)
    total_brand_regs = ytd_brand_r + roy_r
    total_brand_spend = ytd_brand_sp + roy_sp
    # Use locked-YTD constant NB solve for 75% target at this Brand trajectory
    def ieccp_at_nb(avg_nb_wk):
        nb_r, nb_sp = 0.0, 0.0
        for w_idx in range(16, 52):
            rel = nb_weights[w_idx] / w13_16_nb_wt_avg
            wk_sp = max(avg_nb_wk * rel, 1.0)
            wk_cpa = math.exp(a + b * math.log(wk_sp))
            wk_r = wk_sp / wk_cpa
            nb_r += wk_r
            nb_sp += wk_sp
        tot_nb_r = ytd_nb_r + nb_r
        tot_nb_sp = ytd_nb_sp + nb_sp
        tot_sp = total_brand_spend + tot_nb_sp
        iec = tot_sp / (total_brand_regs * BRAND_CCP + tot_nb_r * NB_CCP)
        return iec, tot_sp, tot_nb_r, tot_nb_sp, nb_sp, nb_r
    # Binary search for NB level hitting 75%
    lo, hi = 0.0, 100000.0
    for _ in range(60):
        mid = (lo + hi) / 2
        iec, *_ = ieccp_at_nb(mid)
        if iec < 0.75:
            lo = mid
        else:
            hi = mid
    nb_wk = (lo + hi) / 2
    iec, tot_sp, tot_nb_r, tot_nb_sp, new_nb_sp, new_nb_r = ieccp_at_nb(nb_wk)
    return {
        'half_life': half_life,
        'brand_regs': total_brand_regs,
        'brand_spend': total_brand_spend,
        'nb_weekly': nb_wk,
        'total_spend': tot_sp,
        'total_regs': total_brand_regs + tot_nb_r,
        'ieccp': iec,
        'may_dec_nb_spend': new_nb_sp,
        'may_dec_nb_regs': new_nb_r,
    }

print(f"\n{'Scenario':<55} {'Brand':>12} {'NB Weekly':>11} {'Y26 Total':>12} {'Y26 Regs':>10} {'ie%CCP':>7}")
print('-' * 110)
for label, hl in scenarios:
    r = scenario_total(hl)
    brand_str = f"${r['brand_spend']:,.0f}"
    nb_wk_str = f"${r['nb_weekly']:,.0f}"
    tot_str = f"${r['total_spend']:,.0f}"
    print(f"{label:<55} {brand_str:>12} {nb_wk_str:>11} {tot_str:>12} {r['total_regs']:>10,.0f} {r['ieccp']*100:>6.1f}%")
