#!/usr/bin/env python3
"""MX 2026 year-end projection scenarios for Lorena email.
Uses daily actuals + 3 RoY scenarios:
  A: Sparkle stops now (pre-Sparkle rates from tomorrow)
  B: Sparkle decays gradually through year-end
  C: Sparkle persists full year at current rate
"""

import duckdb, math, os, sys
from datetime import date, timedelta
sys.path.insert(0, os.path.expanduser('~/shared/tools'))
from prediction.config import MOTHERDUCK_TOKEN as TOKEN

con = duckdb.connect(f'md:ps_analytics?motherduck_token={TOKEN}')

# --- Actuals ---
q1_cost, q1_regs = con.execute("""SELECT SUM(cost), SUM(registrations)
    FROM ps.v_daily WHERE market='MX' AND period_start BETWEEN '2026-01-01' AND '2026-03-31'""").fetchone()

apr_cost, apr_regs, apr_days = con.execute("""SELECT SUM(cost), SUM(registrations), COUNT(*)
    FROM ps.v_daily WHERE market='MX' AND period_start BETWEEN '2026-04-01' AND '2026-04-18'""").fetchone()

ytd_cost = q1_cost + apr_cost
ytd_regs = q1_regs + apr_regs
ytd_cpa = ytd_cost / ytd_regs

# --- Regime daily rates ---
pre_sp_cost_d, pre_sp_regs_d = con.execute("""SELECT SUM(cost)/COUNT(*), SUM(registrations)/COUNT(*)
    FROM ps.v_daily WHERE market='MX' AND period_start BETWEEN '2026-01-01' AND '2026-02-28'""").fetchone()

sp_cost_d, sp_regs_d = con.execute("""SELECT SUM(cost)/14.0, SUM(registrations)/14.0
    FROM ps.v_daily WHERE market='MX' AND period_start BETWEEN '2026-04-05' AND '2026-04-18'""").fetchone()

# --- Period setup ---
TODAY = date(2026, 4, 18)       # last day of actuals
RoY_START = date(2026, 4, 19)    # first projected day
YEAR_END = date(2026, 12, 31)
RoY_DAYS = (YEAR_END - RoY_START).days + 1   # inclusive


def scenario_constant(daily_cost, daily_regs, days):
    return daily_cost * days, daily_regs * days


def scenario_decay(start_cost_d, start_regs_d, floor_cost_d, floor_regs_d, days):
    """Exponential decay from start rate toward floor (pre-Sparkle) over `days`.
    By day 0 of remaining period: at start rate.
    By day `days-1` (year-end): ~97% of the way to floor.
    Uses half-life = days / 5, i.e. 5 half-lives from now to year-end."""
    # total excess above floor today
    excess_cost = start_cost_d - floor_cost_d
    excess_regs = start_regs_d - floor_regs_d
    # Integrate: daily = floor + excess * 0.5^(day / half_life)
    # Sum over d=0..days-1 of floor = floor * days
    # Sum over d=0..days-1 of excess * 0.5^(d/H) = excess * (1 - 0.5^(days/H)) / (1 - 0.5^(1/H))
    H = days / 5.0   # 5 half-lives spread across remaining days
    r = 0.5 ** (1.0 / H)
    decay_sum = (1 - r ** days) / (1 - r)
    total_cost = floor_cost_d * days + excess_cost * decay_sum
    total_regs = floor_regs_d * days + excess_regs * decay_sum
    return total_cost, total_regs


# --- Compute scenarios ---
# A: Sparkle stops now — pre-Sparkle rates for entire RoY
a_roy_cost, a_roy_regs = scenario_constant(pre_sp_cost_d, pre_sp_regs_d, RoY_DAYS)

# B: Gradual decay from current Sparkle rate to pre-Sparkle rate by year-end
b_roy_cost, b_roy_regs = scenario_decay(sp_cost_d, sp_regs_d, pre_sp_cost_d, pre_sp_regs_d, RoY_DAYS)

# C: Sparkle persists at current rate
c_roy_cost, c_roy_regs = scenario_constant(sp_cost_d, sp_regs_d, RoY_DAYS)


def full(roy_cost, roy_regs):
    return ytd_cost + roy_cost, ytd_regs + roy_regs


a_cost, a_regs = full(a_roy_cost, a_roy_regs)
b_cost, b_regs = full(b_roy_cost, b_roy_regs)
c_cost, c_regs = full(c_roy_cost, c_roy_regs)

OP2 = 1735313


def row(name, cost, regs):
    cpa = cost / regs if regs > 0 else 0
    headroom = OP2 - cost
    pct = 100 * cost / OP2
    return cost, regs, cpa, headroom, pct


print(f"=== MX 2026 Year-End Scenarios (email-ready) ===\n")
print(f"YTD through 4/18: ${ytd_cost:,.0f} cost, {ytd_regs:,} regs, CPA ${ytd_cpa:.2f}")
print(f"Remaining days 4/19 -> 12/31: {RoY_DAYS}")
print()
print(f"Daily rate regimes:")
print(f"  Pre-Sparkle (Jan-Feb avg):   ${pre_sp_cost_d:,.0f}/day, {pre_sp_regs_d:.1f} regs/day, CPA ${pre_sp_cost_d/pre_sp_regs_d:.2f}")
print(f"  Current 14-day avg (Sparkle):${sp_cost_d:,.0f}/day, {sp_regs_d:.1f} regs/day, CPA ${sp_cost_d/sp_regs_d:.2f}")
print()
print(f"{'Scenario':<52} {'Cost':>12} {'Regs':>8} {'CPA':>7} {'OP2 avail':>12} {'%OP2':>6}")
for name, c, r in [
    ('A: Sparkle stops today (pre-Sparkle rate RoY)', a_cost, a_regs),
    ('B: Sparkle decays gradually thru year-end', b_cost, b_regs),
    ('C: Sparkle persists full year', c_cost, c_regs),
]:
    cost, regs, cpa, head, pct = row(name, c, r)
    print(f"{name:<52} ${cost:>11,.0f} {regs:>8,.0f} ${cpa:>6.2f} ${head:>11,.0f} {pct:>5.1f}%")

print()
print(f"OP2 (April R&O gross): ${OP2:,}")
print()
print(f"Ceiling analysis (covers Scenario C + buffer):")
for ceiling in [1_100_000, 1_200_000, 1_300_000, 1_350_000]:
    buf_c = ceiling - c_cost
    xfer = OP2 - ceiling
    flag = 'TOO LOW' if buf_c < 0 else 'OK' if buf_c > 30_000 else 'TIGHT'
    print(f"  ${ceiling:>11,}: buffer vs C = ${buf_c:>+9,.0f} ({flag})  transfer=${xfer:,}")

# Show B's decay curve daily-rate check
print()
print(f"Scenario B monthly breakdown (gradual decay):")
cumulative_days = 0
month_starts = [(5,1),(6,1),(7,1),(8,1),(9,1),(10,1),(11,1),(12,1)]
month_ends = [(5,31),(6,30),(7,31),(8,31),(9,30),(10,31),(11,30),(12,31)]
H = RoY_DAYS / 5.0
r = 0.5 ** (1.0 / H)
for (ms_m, ms_d), (me_m, me_d) in zip(month_starts, month_ends):
    ms = date(2026, ms_m, ms_d)
    me = date(2026, me_m, me_d)
    offset_start = (ms - RoY_START).days
    offset_end = (me - RoY_START).days
    month_days = offset_end - offset_start + 1
    month_cost = 0.0; month_regs = 0.0
    for d in range(offset_start, offset_end + 1):
        f = r ** d
        month_cost += pre_sp_cost_d + (sp_cost_d - pre_sp_cost_d) * f
        month_regs += pre_sp_regs_d + (sp_regs_d - pre_sp_regs_d) * f
    print(f"  {ms.strftime('%b'):<4} {month_days}d: ${month_cost:>9,.0f}, {month_regs:>6,.0f} regs")
