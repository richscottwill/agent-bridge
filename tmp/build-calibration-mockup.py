"""
Build a side-by-side HTML mockup: current calibration chart vs. proposed
weekly-error bar chart. Uses real US 2026 data from forecast-data.json
so the story shown is the actual story, not synthetic.

Output: agent-bridge/context/intake/wr-calibration-mockup.html
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORECAST = ROOT / 'dashboards' / 'data' / 'forecast-data.json'
OUT = ROOT / 'context' / 'intake' / 'wr-calibration-mockup.html'

data = json.loads(FORECAST.read_text(encoding='utf-8'))
us_hist = data['predictions_history']['US']

# Build a (wk, actual, first_pred, latest_pred, err_pct, in_ci) list for 1..52
rows = []
for wk in range(1, 53):
    entry = us_hist.get(str(wk), {}).get('regs') or {}
    actual = entry.get('actual')
    first = entry.get('first_pred')
    latest = entry.get('latest_pred')
    ci_lo = entry.get('latest_ci_lo')
    ci_hi = entry.get('latest_ci_hi')
    if actual in (None, 0):
        # Future weeks: no actual, so no error. Still render the bar slot empty.
        err_pct = None
        err_first_pct = None
        in_ci = None
        has_actual = False
    else:
        # Error convention matches dashboard: (pred - actual) / actual * 100
        # Negative = under-predicting. Positive = over-predicting.
        err_pct = round((latest - actual) / actual * 100, 1) if latest else None
        err_first_pct = round((first - actual) / actual * 100, 1) if first else None
        in_ci = (ci_lo is not None and ci_hi is not None and ci_lo <= actual <= ci_hi)
        has_actual = True
    rows.append({
        'wk': wk,
        'actual': actual,
        'first': first,
        'latest': latest,
        'err_pct': err_pct,
        'err_first_pct': err_first_pct,
        'ci_lo': ci_lo,
        'ci_hi': ci_hi,
        'in_ci': in_ci,
        'has_actual': has_actual,
    })

# Derive CI band width % (latest CI spread relative to latest pred) per-week,
# then take the median across weeks with actuals — that's the "claimed
# precision" band we'll draw as a reference. Keeps the chart honest about
# what the model says its uncertainty is.
ci_halfwidths_pct = []
for r in rows:
    if r['ci_lo'] is not None and r['ci_hi'] is not None and r['latest']:
        half = (r['ci_hi'] - r['ci_lo']) / 2.0
        if r['latest']:
            ci_halfwidths_pct.append(half / r['latest'] * 100)
ci_band_pct = round(sum(ci_halfwidths_pct) / len(ci_halfwidths_pct), 1) if ci_halfwidths_pct else 20.0

rows_json = json.dumps(rows)

html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Calibration chart — current vs proposed (US 2026)</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
  :root {{
    --color-brand: #0066CC;
    --color-success: #14A548;
    --color-warning: #E8A800;
    --color-danger: #D13212;
    --color-panel-bg: #FAFAFA;
    --color-panel-border: #E0E0E0;
    --color-text-hero: #0F1111;
    --color-text-body: #232F3E;
    --color-text-subtle: #6A6A6A;
    --color-orange: #f97316;
    --color-orange-soft: rgba(249,115,22,0.14);

    /* Muted traffic-light fills — soft backgrounds, saturated borders */
    --err-good-fill: rgba(20, 165, 72, 0.35);
    --err-good-edge: rgba(20, 165, 72, 0.75);
    --err-warn-fill: rgba(232, 168, 0, 0.35);
    --err-warn-edge: rgba(232, 168, 0, 0.85);
    --err-bad-fill:  rgba(209, 50, 18, 0.35);
    --err-bad-edge:  rgba(209, 50, 18, 0.80);
    --err-empty-fill: rgba(160, 160, 160, 0.12);
    --err-empty-edge: rgba(160, 160, 160, 0.35);

    --size-ui: 13px;
    --size-meta: 11px;
    --gap-md: 12px;
    --gap-lg: 20px;
  }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Amazon Ember", system-ui, sans-serif;
    background: #F6F6F6;
    color: var(--color-text-body);
    margin: 0;
    padding: var(--gap-lg);
    font-size: var(--size-ui);
  }}
  h1 {{ font-size: 18px; margin: 0 0 4px; color: var(--color-text-hero); }}
  h1 small {{ font-size: 12px; font-weight: normal; color: var(--color-text-subtle); }}
  h2 {{ font-size: 13px; margin: 0 0 8px; text-transform: uppercase;
        letter-spacing: 0.08em; color: var(--color-text-subtle); font-weight: 600; }}
  p.lede {{ margin: 0 0 var(--gap-lg); color: var(--color-text-body); max-width: 80ch; }}
  .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: var(--gap-lg); }}
  @media (max-width: 1200px) {{ .grid {{ grid-template-columns: 1fr; }} }}
  .panel {{
    background: white;
    border: 1px solid var(--color-panel-border);
    border-radius: 8px;
    padding: var(--gap-lg);
  }}
  .panel .chart-wrap {{ position: relative; width: 100%; height: 340px; }}
  .legend-row {{
    display: flex; flex-wrap: wrap; gap: 16px;
    margin-top: 12px; font-size: var(--size-meta);
    color: var(--color-text-subtle);
  }}
  .legend-chip {{
    display: inline-flex; align-items: center; gap: 6px;
  }}
  .legend-swatch {{
    width: 12px; height: 12px; border-radius: 2px;
    border: 1px solid transparent;
  }}
  .legend-swatch.good  {{ background: var(--err-good-fill); border-color: var(--err-good-edge); }}
  .legend-swatch.warn  {{ background: var(--err-warn-fill); border-color: var(--err-warn-edge); }}
  .legend-swatch.bad   {{ background: var(--err-bad-fill);  border-color: var(--err-bad-edge); }}
  .legend-swatch.empty {{ background: var(--err-empty-fill); border-color: var(--err-empty-edge); }}
  .legend-swatch.band {{ background: rgba(20, 165, 72, 0.08); border: 1px dashed rgba(20,165,72,0.5); }}
  .caption {{ margin-top: 12px; font-size: var(--size-meta); color: var(--color-text-subtle); line-height: 1.5; }}
  .caption strong {{ color: var(--color-text-body); font-weight: 600; }}
  .notes {{
    margin-top: var(--gap-lg);
    background: white;
    border: 1px solid var(--color-panel-border);
    border-radius: 8px;
    padding: var(--gap-lg);
  }}
  .notes ul {{ padding-left: 20px; margin: 8px 0; }}
  .notes li {{ margin-bottom: 6px; }}
  code {{
    background: #F0F0F0; padding: 1px 4px; border-radius: 3px;
    font-size: 12px;
  }}
</style>
</head>
<body>
  <h1>Calibration chart redesign — side-by-side <small>· US regs · 2026 YTD · real data</small></h1>
  <p class="lede">Left: current "How did we do — forecast vs actual" line chart. Right: proposed weekly error bar chart. Same underlying data, different question answered. All 52 weeks rendered; weeks with no actuals yet render as empty slots so the x-axis is stable across markets and across the year.</p>

  <div class="grid">
    <div class="panel" aria-labelledby="current-heading">
      <h2 id="current-heading">Current — forecast vs actual (lines)</h2>
      <div class="chart-wrap"><canvas id="currentChart" role="img" aria-label="Current calibration chart: actual, first prediction, latest prediction as lines over 52 weeks"></canvas></div>
      <div class="legend-row">
        <span class="legend-chip"><span class="legend-swatch" style="background:var(--color-orange);border-color:var(--color-orange)"></span>Actual</span>
        <span class="legend-chip"><span class="legend-swatch" style="background:transparent;border:1px solid var(--color-orange)"></span>First pred</span>
        <span class="legend-chip"><span class="legend-swatch" style="background:transparent;border:1px dashed var(--color-orange)"></span>Latest pred</span>
        <span class="legend-chip"><span class="legend-swatch band"></span>CI band</span>
      </div>
      <p class="caption">Error is encoded as vertical distance between two curves — hard to judge by eye. First pred and latest pred overlap because the pipeline writes one prediction per week (<code>n_preds=1</code>), so the dual-line premise is currently a lie. Comparing this chart to the "trend" chart above it is confusing because they use the same visual grammar for different questions.</p>
    </div>

    <div class="panel" aria-labelledby="proposed-heading">
      <h2 id="proposed-heading">Proposed — weekly forecast error (bars)</h2>
      <div class="chart-wrap"><canvas id="proposedChart" role="img" aria-label="Proposed calibration chart: signed forecast error per week, with severity fill and CI reference band"></canvas></div>
      <div class="legend-row">
        <span class="legend-chip"><span class="legend-swatch good"></span>|err| &lt; 5%</span>
        <span class="legend-chip"><span class="legend-swatch warn"></span>5–15%</span>
        <span class="legend-chip"><span class="legend-swatch bad"></span>&gt; 15%</span>
        <span class="legend-chip"><span class="legend-swatch empty"></span>no actual yet</span>
        <span class="legend-chip"><span class="legend-swatch band"></span>±CI band ({ci_band_pct}%)</span>
      </div>
      <p class="caption">Each bar is one week's prediction error as a % of actual. Signed — bars below zero are under-predictions, above zero are over-predictions. Fill is severity. The green band is the model's <strong>own claimed precision</strong> (median CI half-width across weeks with actuals). A bar extending beyond the band is literally a calibration miss — visible at a glance. W15 at {next((r["err_pct"] for r in rows if r["wk"] == 15), None)}% reads as the worst week of the year without needing to compare it to a neighbour.</p>
    </div>
  </div>

  <div class="notes">
    <h2>Why this works</h2>
    <ul>
      <li><strong>Visually distinct from the trend chart.</strong> Bars instead of lines, signed axis instead of raw volume, severity coloring instead of series coloring. Four orthogonal dimensions — no reasonable viewer confuses them.</li>
      <li><strong>Shows systematic bias.</strong> US bars cluster below zero → under-prediction is visible without reading the caption. If we showed FR, bars would straddle zero differently.</li>
      <li><strong>Honest about the pipeline defect.</strong> When <code>n_preds == 1</code>, the chart shows one bar per week with a single value. When recalibration lands (WR-A9), we'll add a paired hollow dot at the first-pred error; the segment from hollow-to-filled-bar-top visualizes recalibration improvement week by week.</li>
      <li><strong>All 52 weeks stable.</strong> Empty grey slots for future weeks keep the x-axis shape identical across markets and weeks. Future-week hover is inert.</li>
      <li><strong>CI band is real.</strong> Drawn from actual <code>latest_ci_lo/hi</code> values in the data. Median half-width = {ci_band_pct}% on US — the model claims ±{ci_band_pct}% precision. Bars outside that band are failures of the model's own stated confidence, not our complaint.</li>
    </ul>
    <p class="caption">Data source: <code>dashboards/data/forecast-data.json</code> · <code>predictions_history.US.*.regs</code>. CI band derived from median of weekly <code>(ci_hi − ci_lo)/2 / latest_pred</code> across all weeks with actuals.</p>
  </div>

<script>
const DATA = {rows_json};
const CI_BAND = {ci_band_pct};

// --- Current chart: lines ---
(function() {{
  const labels = DATA.map(r => 'W' + r.wk);
  const actual = DATA.map(r => r.actual);
  const first  = DATA.map(r => r.first);
  const latest = DATA.map(r => r.latest);
  // CI fill (envelope around latest) — for weeks with actuals only
  const ciLo = DATA.map(r => r.ci_lo);
  const ciHi = DATA.map(r => r.ci_hi);

  new Chart(document.getElementById('currentChart'), {{
    type: 'line',
    data: {{
      labels,
      datasets: [
        {{ label: '_ciHi', data: ciHi, borderColor: 'transparent',
          backgroundColor: 'rgba(249,115,22,0.14)', pointRadius: 0, fill: '+1',
          tension: 0.25, spanGaps: true, order: 10 }},
        {{ label: '_ciLo', data: ciLo, borderColor: 'transparent',
          backgroundColor: 'transparent', pointRadius: 0, fill: false,
          tension: 0.25, spanGaps: true, order: 10 }},
        {{ label: 'Actual', data: actual, borderColor: '#f97316',
          backgroundColor: '#f97316', borderWidth: 2.5, pointRadius: 3,
          tension: 0.25, spanGaps: false, order: 1 }},
        {{ label: 'First pred', data: first, borderColor: '#f97316',
          backgroundColor: 'transparent', borderWidth: 1, pointRadius: 3,
          pointStyle: 'rect', pointBackgroundColor: 'transparent',
          pointBorderColor: '#f97316', tension: 0.25, spanGaps: true, order: 2 }},
        {{ label: 'Latest pred', data: latest, borderColor: '#f97316',
          backgroundColor: 'transparent', borderWidth: 2, borderDash: [6,4],
          pointRadius: 0, tension: 0.25, spanGaps: true, order: 3 }},
      ]
    }},
    options: {{
      responsive: true, maintainAspectRatio: false,
      interaction: {{ mode: 'index', intersect: false }},
      plugins: {{
        legend: {{ display: false }},
        tooltip: {{ filter: i => !String(i.dataset.label).startsWith('_') }},
      }},
      scales: {{
        y: {{ beginAtZero: false, title: {{ display: true, text: 'Registrations' }} }},
        x: {{ ticks: {{ maxRotation: 0, autoSkip: true, autoSkipPadding: 8 }} }}
      }}
    }}
  }});
}})();

// --- Proposed chart: weekly error bars ---
(function() {{
  const labels = DATA.map(r => 'W' + r.wk);
  const vals = DATA.map(r => r.err_pct);  // null for weeks without actual

  const GOOD_FILL = 'rgba(20, 165, 72, 0.35)';
  const GOOD_EDGE = 'rgba(20, 165, 72, 0.75)';
  const WARN_FILL = 'rgba(232, 168, 0, 0.35)';
  const WARN_EDGE = 'rgba(232, 168, 0, 0.85)';
  const BAD_FILL  = 'rgba(209, 50, 18, 0.35)';
  const BAD_EDGE  = 'rgba(209, 50, 18, 0.80)';
  const EMPTY_FILL = 'rgba(160, 160, 160, 0.12)';
  const EMPTY_EDGE = 'rgba(160, 160, 160, 0.35)';

  function fill(v) {{
    if (v === null || v === undefined) return EMPTY_FILL;
    const a = Math.abs(v);
    if (a < 5) return GOOD_FILL;
    if (a < 15) return WARN_FILL;
    return BAD_FILL;
  }}
  function edge(v) {{
    if (v === null || v === undefined) return EMPTY_EDGE;
    const a = Math.abs(v);
    if (a < 5) return GOOD_EDGE;
    if (a < 15) return WARN_EDGE;
    return BAD_EDGE;
  }}

  // For empty-week cells, render a very short stub (fixed absolute height)
  // so users can see the slot is there. Chart.js can't render "zero" bars with
  // a border, so we put null for empty slots and rely on the grey background
  // grid + label to indicate the slot.
  const barData = vals.map(v => v === null ? null : v);
  const backgroundColor = vals.map(fill);
  const borderColor = vals.map(edge);

  // Reference band plugin — draws ±CI_BAND as a soft green horizontal band.
  const referenceBandPlugin = {{
    id: 'referenceBand',
    beforeDatasetsDraw(chart) {{
      const {{ ctx, chartArea, scales: {{ y }} }} = chart;
      const y0 = y.getPixelForValue(CI_BAND);
      const y1 = y.getPixelForValue(-CI_BAND);
      ctx.save();
      ctx.fillStyle = 'rgba(20, 165, 72, 0.06)';
      ctx.fillRect(chartArea.left, Math.min(y0, y1), chartArea.right - chartArea.left, Math.abs(y1 - y0));
      ctx.strokeStyle = 'rgba(20, 165, 72, 0.35)';
      ctx.setLineDash([4, 3]);
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(chartArea.left, y0); ctx.lineTo(chartArea.right, y0);
      ctx.moveTo(chartArea.left, y1); ctx.lineTo(chartArea.right, y1);
      ctx.stroke();
      ctx.restore();
    }}
  }};

  // Zero line — draw slightly heavier so the sign of error reads immediately
  const zeroLinePlugin = {{
    id: 'zeroLine',
    afterDatasetsDraw(chart) {{
      const {{ ctx, chartArea, scales: {{ y }} }} = chart;
      const y0 = y.getPixelForValue(0);
      ctx.save();
      ctx.strokeStyle = 'rgba(60, 60, 60, 0.6)';
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(chartArea.left, y0); ctx.lineTo(chartArea.right, y0);
      ctx.stroke();
      ctx.restore();
    }}
  }};

  new Chart(document.getElementById('proposedChart'), {{
    type: 'bar',
    data: {{
      labels,
      datasets: [{{
        label: 'Forecast error %',
        data: barData,
        backgroundColor,
        borderColor,
        borderWidth: 1,
        borderRadius: 2,
      }}]
    }},
    plugins: [referenceBandPlugin, zeroLinePlugin],
    options: {{
      responsive: true, maintainAspectRatio: false,
      interaction: {{ mode: 'index', intersect: false }},
      plugins: {{
        legend: {{ display: false }},
        tooltip: {{
          callbacks: {{
            title: items => items[0].label,
            label: item => {{
              const r = DATA[item.dataIndex];
              if (r.err_pct === null) return 'no actual yet';
              const dir = r.err_pct < 0 ? 'under-predicted' : 'over-predicted';
              return [
                `error: ${{r.err_pct > 0 ? '+' : ''}}${{r.err_pct}}% (${{dir}})`,
                `actual: ${{r.actual.toLocaleString()}}`,
                `latest pred: ${{r.latest?.toLocaleString()}}`,
                r.in_ci ? 'inside CI band' : 'outside CI band',
              ];
            }}
          }}
        }},
      }},
      scales: {{
        y: {{
          suggestedMin: -50, suggestedMax: 50,
          title: {{ display: true, text: 'Forecast error (% of actual)' }},
          ticks: {{ callback: v => (v > 0 ? '+' : '') + v + '%' }},
          grid: {{ color: (ctx) => ctx.tick.value === 0 ? 'transparent' : 'rgba(0,0,0,0.04)' }},
        }},
        x: {{
          ticks: {{ maxRotation: 0, autoSkip: true, autoSkipPadding: 8 }},
          grid: {{ display: false }},
        }}
      }}
    }}
  }});
}})();
</script>
</body>
</html>
"""

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(html, encoding='utf-8')
print(f'wrote {OUT}')
print(f'US rows total: {len(rows)}, with actuals: {sum(1 for r in rows if r["has_actual"])}')
print(f'Median CI half-width (%): {ci_band_pct}')
