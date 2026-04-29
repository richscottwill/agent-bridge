"""Quick probe of forecast bias across markets and US week-by-week pattern."""
import json
import statistics
from pathlib import Path

d = json.loads(Path('agent-bridge/dashboards/data/forecast-data.json').read_text(encoding='utf-8'))

def summarize(market):
    ph = d['predictions_history'].get(market, {})
    with_actuals = [(int(w), ph[w]['regs']) for w in ph
                    if ph[w].get('regs', {}).get('actual') not in (None, 0)]
    with_actuals.sort()
    last6 = with_actuals[-6:]
    if not last6:
        return None

    def pct(p, a):
        if p is None or a in (None, 0):
            return None
        return (p - a) / a * 100

    f_errs = [pct(r['first_pred'], r['actual']) for _, r in last6]
    in_cis = []
    for _, r in last6:
        if r.get('latest_ci_lo') is not None and r.get('latest_ci_hi') is not None:
            in_cis.append(r['latest_ci_lo'] <= r['actual'] <= r['latest_ci_hi'])

    neg_frac = sum(1 for e in f_errs if e < 0) / len(f_errs)
    latest_n = last6[-1][1].get('n_preds')
    first_eq_latest = all(
        r.get('first_pred') == r.get('latest_pred') for _, r in last6
    )
    return {
        'weeks': [w for w, _ in last6],
        'mean_first_err': round(statistics.mean(f_errs), 1),
        'stdev_first_err': round(statistics.stdev(f_errs), 1) if len(f_errs) > 1 else 0,
        'neg_frac': round(neg_frac, 2),
        'in_ci': f'{sum(in_cis)}/{len(in_cis)}' if in_cis else '-',
        'latest_n_preds': latest_n,
        'first_eq_latest': first_eq_latest,
    }

print('=== Per-market forecast bias (last 6 weeks, regs) ===')
for m in ['US', 'WW', 'UK', 'DE', 'FR', 'IT', 'ES', 'JP', 'CA', 'MX', 'AU', 'EU5']:
    s = summarize(m)
    if s is None:
        print(f'{m:4s}  no actuals')
        continue
    print(
        f'{m:4s}  mean={s["mean_first_err"]:+6.1f}%  '
        f'sd={s["stdev_first_err"]:5.1f}  '
        f'neg={int(s["neg_frac"]*100):3d}%  '
        f'in_ci={s["in_ci"]:5s}  '
        f'n_preds(latest)={s["latest_n_preds"]}  '
        f'first=latest? {s["first_eq_latest"]}'
    )

print()
print('=== US week-by-week (weeks with actuals, regs) ===')
us = d['predictions_history']['US']
print(f'{"WK":>3} {"ACTUAL":>7} {"FIRST":>7} {"LATEST":>7} {"ERR%":>7} {"N":>3} {"SCORE":>10}')
for w in sorted(us.keys(), key=int):
    r = us[w].get('regs', {})
    a = r.get('actual')
    if a in (None, 0):
        continue
    fp = r.get('first_pred') or 0
    lp = r.get('latest_pred') or 0
    e = r.get('error_pct') if r.get('error_pct') is not None else 0
    n = r.get('n_preds') or 0
    sc = r.get('score') or '-'
    print(f'{w:>3} {a:>7.0f} {fp:>7.0f} {lp:>7.0f} {e:>+7.1f} {n:>3} {sc:>10}')

print()
# Check the shape of ly_weekly for US so we can ratio to last year
print('=== US actuals vs last year (same ISO week) ===')
us_actuals = {int(w): us[w]['regs']['actual']
              for w in us
              if us[w].get('regs', {}).get('actual') not in (None, 0)}
ly = d.get('ly_weekly', {}).get('US', [])
ly_by_wk = {r.get('wk'): r.get('regs') for r in ly}
print(f'{"WK":>3} {"ACTUAL":>7} {"LY":>7} {"YOY%":>7}')
for w in sorted(us_actuals.keys()):
    a = us_actuals[w]
    lyv = ly_by_wk.get(w)
    yoy = ((a - lyv) / lyv * 100) if lyv else None
    lyv_s = f'{lyv:>7.0f}' if lyv else '      -'
    yoy_s = f'{yoy:>+7.1f}' if yoy is not None else '      -'
    print(f'{w:>3} {a:>7.0f} {lyv_s} {yoy_s}')
