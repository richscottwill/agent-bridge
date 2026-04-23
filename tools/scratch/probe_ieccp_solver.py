"""Probe _solve_ieccp_target to find why MX Y2026 ieccp:0.75 returns $1000 total_spend."""
import sys
sys.path.insert(0, 'shared/tools/prediction')
from mpe_engine import _project_market_spend_target, parse_time_period, load_parameters, ProjectionInputs

params = load_parameters('MX')
tp = parse_time_period('Y2026')

inp = ProjectionInputs(
    scope='MX',
    time_period='Y2026',
    target_mode='ieccp',
    target_value=0.75,
    brand_uplift_pct=0.0,
    nb_uplift_pct=0.0,
)

print(f"{'spend':>15} | {'regs':>8} | {'cpa':>8} | {'ieccp':>10}")
print('-' * 55)
for spend in [1_000, 10_000, 100_000, 500_000, 1_000_000, 2_000_000, 5_000_000, 10_000_000, 100_000_000]:
    weeks, totals = _project_market_spend_target(spend, inp, params, tp)
    ieccp = totals['ieccp']
    ieccp_s = f"{ieccp:.4f}" if ieccp is not None else "None"
    print(f"${spend:>14,} | {totals['total_regs']:>8} | ${totals['blended_cpa']:>7.2f} | {ieccp_s:>10}")
