#!/usr/bin/env python3
"""
Generate standalone HTML dashboards from local DuckDB data.
Replaces MotherDuck Dives with portable HTML files for Amazon Drive hosting.

Generates:
  1. forecast-tracker.html — Actual vs Predicted with CI, weekly/monthly/quarterly views
  2. pacing-dashboard.html — MTD/YTD pacing against OP targets, all markets

Usage: python3 generate-html-dashboards.py
"""

import duckdb
import json
import os
from pathlib import Path

DB_PATH = os.path.expanduser("~/shared/data/duckdb/ps-analytics.duckdb")
OUT_DIR = os.path.expanduser("~/shared/dashboards")
os.makedirs(OUT_DIR, exist_ok=True)


def query_db(sql):
    con = duckdb.connect(DB_PATH, read_only=True)
    result = con.execute(sql).fetchall()
    cols = [d[0] for d in con.description]
    con.close()
    return [dict(zip(cols, row)) for row in result]


def get_weekly_data():
    return query_db("""
        SELECT market, week,
            CAST(REPLACE(REPLACE(week, '2025 W',''), '2026 W','') AS INTEGER) as week_num,
            regs, cost, ROUND(cpa, 2) as cpa
        FROM main.weekly_metrics
        WHERE week LIKE '2026%'
        ORDER BY market, CAST(REPLACE(REPLACE(week, '2025 W',''), '2026 W','') AS INTEGER)
    """)


def get_monthly_data():
    return query_db("""
        SELECT market, month, regs as regs, spend, cpa,
            regs_op2, spend_op2, cpa_op2
        FROM main.monthly_metrics
        WHERE month LIKE '2026%'
        ORDER BY market, month
    """)


def get_projections():
    return query_db("""
        SELECT market, week, month, days_elapsed, total_days,
            projected_regs, projected_spend, ROUND(projected_cpa, 2) as projected_cpa,
            actual_regs, actual_spend, ROUND(COALESCE(actual_cpa, 0), 2) as actual_cpa,
            op2_regs, op2_spend,
            ROUND(vs_op2_regs_pct, 1) as vs_op2_regs_pct,
            ROUND(vs_op2_spend_pct, 1) as vs_op2_spend_pct,
            rationale, source
        FROM main.projections
        ORDER BY market, week
    """)


def json_serial(obj):
    """JSON serializer for objects not serializable by default."""
    import datetime
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")


def build_forecast_tracker(weekly_rows, projections):
    """Build the forecast tracker HTML dashboard."""
    # Group weekly by market
    weekly_by_market = {}
    for r in weekly_rows:
        m = r['market']
        if m not in weekly_by_market:
            weekly_by_market[m] = []
        weekly_by_market[m].append({
            'wk': r['week_num'],
            'week': r['week'],
            'regs': r['regs'],
            'cost': round(r['cost'], 0) if r['cost'] else 0,
            'cpa': round(r['cpa'], 2) if r['cpa'] else 0
        })

    # Group projections by market
    proj_by_market = {}
    for r in projections:
        m = r['market']
        if m not in proj_by_market:
            proj_by_market[m] = []
        proj_by_market[m].append({
            'month': r['month'],
            'projected_regs': r['projected_regs'],
            'projected_spend': round(r['projected_spend'], 0) if r['projected_spend'] else 0,
            'projected_cpa': r['projected_cpa'],
            'op2_regs': r['op2_regs'],
            'op2_spend': round(r['op2_spend'], 0) if r['op2_spend'] else None,
            'vs_op2_regs_pct': r['vs_op2_regs_pct'],
            'rationale': r['rationale'],
            'source': r['source']
        })

    markets = sorted(weekly_by_market.keys())
    data_json = json.dumps({
        'weekly': weekly_by_market,
        'projections': proj_by_market,
        'markets': markets
    }, default=json_serial)

    html = FORECAST_TEMPLATE.replace('__DATA_JSON__', data_json)
    return html


def build_pacing_dashboard(weekly_rows, monthly_rows, projections):
    """Build the pacing dashboard HTML."""
    # Group weekly by market for sparklines
    weekly_by_market = {}
    for r in weekly_rows:
        m = r['market']
        if m not in weekly_by_market:
            weekly_by_market[m] = []
        weekly_by_market[m].append({
            'wk': r['week_num'],
            'regs': r['regs'],
            'cost': round(r['cost'], 0) if r['cost'] else 0,
            'cpa': round(r['cpa'], 2) if r['cpa'] else 0
        })

    # Monthly OP2 targets from monthly_metrics
    monthly_by_market = {}
    for r in monthly_rows:
        m = r['market']
        if m not in monthly_by_market:
            monthly_by_market[m] = []
        monthly_by_market[m].append({
            'month': r['month'],
            'regs': r['regs'] if r['regs'] else 0,
            'spend': round(r['spend'], 0) if r['spend'] else 0,
            'cpa': round(r['cpa'], 2) if r['cpa'] else 0,
            'regs_op2': r['regs_op2'],
            'spend_op2': round(r['spend_op2'], 0) if r['spend_op2'] else None,
        })

    # Projections for current month
    proj_by_market = {}
    for r in projections:
        m = r['market']
        proj_by_market[m] = {
            'month': r['month'],
            'projected_regs': r['projected_regs'],
            'projected_spend': round(r['projected_spend'], 0) if r['projected_spend'] else 0,
            'op2_regs': r['op2_regs'],
            'op2_spend': round(r['op2_spend'], 0) if r['op2_spend'] else None,
            'vs_op2_regs_pct': r['vs_op2_regs_pct'],
            'vs_op2_spend_pct': r['vs_op2_spend_pct'],
            'rationale': r['rationale']
        }

    markets = sorted(weekly_by_market.keys())
    data_json = json.dumps({
        'weekly': weekly_by_market,
        'monthly': monthly_by_market,
        'projections': proj_by_market,
        'markets': markets
    }, default=json_serial)

    html = PACING_TEMPLATE.replace('__DATA_JSON__', data_json)
    return html



# ============================================================
# FORECAST TRACKER TEMPLATE
# ============================================================
FORECAST_TEMPLATE = r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>PS Forecast Tracker — All Markets</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.4/dist/chart.umd.min.js"></script>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#0f1117;color:#e0e0e0}
.header{padding:24px 32px 16px;border-bottom:1px solid #2a2d35}
.header h1{font-size:20px;font-weight:600;color:#fff}
.header p{font-size:13px;color:#888;margin-top:4px}
.controls{display:flex;gap:12px;padding:16px 32px;border-bottom:1px solid #2a2d35;flex-wrap:wrap;align-items:center}
.controls label{font-size:12px;color:#888;text-transform:uppercase;letter-spacing:.5px}
.tab-row{display:flex;gap:4px;flex-wrap:wrap}
.tab{padding:6px 14px;border-radius:6px;font-size:13px;cursor:pointer;background:transparent;border:1px solid #2a2d35;color:#888}
.tab.active{background:#1a3a5c;border-color:#4a9eff;color:#4a9eff}
.tab:hover{border-color:#4a9eff}
select{background:#1a1d27;border:1px solid #2a2d35;color:#e0e0e0;padding:6px 12px;border-radius:6px;font-size:13px;cursor:pointer}
select:hover{border-color:#4a9eff}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:16px;padding:24px 32px}
.card{background:#1a1d27;border:1px solid #2a2d35;border-radius:10px;padding:20px}
.card-full{grid-column:1/-1}
.card h3{font-size:14px;font-weight:600;color:#ccc;margin-bottom:12px}
.chart-box{position:relative;height:400px}
.kpi-row{display:flex;gap:16px;padding:0 32px 16px;flex-wrap:wrap}
.kpi{background:#1a1d27;border:1px solid #2a2d35;border-radius:10px;padding:16px 20px;flex:1;min-width:140px}
.kpi .label{font-size:11px;color:#888;text-transform:uppercase;letter-spacing:.5px}
.kpi .value{font-size:22px;font-weight:700;color:#fff;margin-top:4px}
.kpi .sub{font-size:12px;color:#888;margin-top:2px}
.good{color:#4ade80}.warn{color:#fbbf24}.bad{color:#f87171}
table{width:100%;border-collapse:collapse;font-size:13px}
th{text-align:left;padding:8px 12px;border-bottom:1px solid #2a2d35;color:#888;font-weight:500;font-size:11px;text-transform:uppercase}
td{padding:8px 12px;border-bottom:1px solid #1f222b}
tr:hover{background:#1f222b}
.badge{display:inline-block;padding:2px 8px;border-radius:4px;font-size:11px;font-weight:600}
.badge-green{background:#064e3b;color:#4ade80}
.badge-yellow{background:#713f12;color:#fbbf24}
.badge-red{background:#7f1d1d;color:#f87171}
.badge-gray{background:#374151;color:#9ca3af}
.legend-row{display:flex;gap:16px;margin-bottom:12px;flex-wrap:wrap}
.legend-item{display:flex;align-items:center;gap:6px;font-size:12px;color:#888}
.legend-dot{width:10px;height:10px;border-radius:50%}
.legend-line{width:20px;height:2px;border-radius:1px}
.ts{font-size:11px;color:#444;text-align:right;padding:16px 32px}
</style>
</head>
<body>
<div class="header">
  <h1>📊 PS Forecast Tracker — All Markets</h1>
  <p>Weekly actuals with month-end projections and OP2 targets • Data from ps-analytics.duckdb</p>
</div>
<div class="controls">
  <div><label>Market</label><br><div class="tab-row" id="marketTabs"></div></div>
  <div style="margin-left:auto"><label>Metric</label><br>
    <select id="metricSel">
      <option value="regs">Registrations</option>
      <option value="cost">Cost</option>
      <option value="cpa">CPA</option>
    </select>
  </div>
</div>
<div class="kpi-row" id="kpiRow"></div>
<div class="grid">
  <div class="card card-full">
    <h3 id="chartTitle">Weekly Registrations</h3>
    <div class="legend-row">
      <div class="legend-item"><div class="legend-dot" style="background:#4a9eff"></div> Actual</div>
      <div class="legend-item"><div class="legend-line" style="background:#f97316"></div> Projected (month-end)</div>
    </div>
    <div class="chart-box"><canvas id="mainChart"></canvas></div>
  </div>
  <div class="card card-full">
    <h3>Weekly Detail</h3>
    <div style="overflow-x:auto;max-height:500px;overflow-y:auto">
      <table><thead><tr>
        <th>Week</th><th style="text-align:right">Regs</th><th style="text-align:right">Cost</th>
        <th style="text-align:right">CPA</th><th>WoW Δ</th>
      </tr></thead><tbody id="weeklyBody"></tbody></table>
    </div>
  </div>
  <div class="card card-full" id="projCard">
    <h3>Month-End Projection</h3>
    <div id="projContent"></div>
  </div>
</div>
<div class="ts" id="genTs"></div>
<script>
const DATA = __DATA_JSON__;
const markets = DATA.markets;
let curMarket = markets[0] || 'AU';
let curMetric = 'regs';
let chart = null;

function init() {
  const tabs = document.getElementById('marketTabs');
  markets.forEach(m => {
    const b = document.createElement('button');
    b.className = 'tab' + (m === curMarket ? ' active' : '');
    b.textContent = m;
    b.onclick = () => { curMarket = m; render(); };
    tabs.appendChild(b);
  });
  document.getElementById('metricSel').onchange = e => { curMetric = e.target.value; render(); };
  document.getElementById('genTs').textContent = 'Generated: ' + new Date().toLocaleString();
  render();
}

function fmt(v, type) {
  if (v == null) return '—';
  if (type === 'cost') return '$' + Math.round(v).toLocaleString();
  if (type === 'cpa') return '$' + Number(v).toFixed(2);
  return Math.round(v).toLocaleString();
}

function render() {
  document.querySelectorAll('#marketTabs .tab').forEach((b, i) => {
    b.className = 'tab' + (markets[i] === curMarket ? ' active' : '');
  });
  const weeks = DATA.weekly[curMarket] || [];
  const proj = (DATA.projections[curMarket] || [])[0];
  renderKPIs(weeks, proj);
  renderChart(weeks);
  renderTable(weeks);
  renderProjection(proj);
}

function renderKPIs(weeks, proj) {
  const row = document.getElementById('kpiRow');
  if (!weeks.length) { row.innerHTML = '<div class="kpi"><div class="label">No Data</div></div>'; return; }
  const ytd = weeks.reduce((s, w) => s + (w[curMetric] || 0), 0);
  const last = weeks[weeks.length - 1];
  const prev = weeks.length > 1 ? weeks[weeks.length - 2] : null;
  const wow = prev && prev[curMetric] ? ((last[curMetric] - prev[curMetric]) / prev[curMetric] * 100).toFixed(1) : null;
  const wowClass = wow > 0 ? 'good' : wow < -5 ? 'bad' : 'warn';
  row.innerHTML = `
    <div class="kpi"><div class="label">YTD ${curMetric}</div><div class="value">${fmt(ytd, curMetric)}</div><div class="sub">${weeks.length} weeks</div></div>
    <div class="kpi"><div class="label">Latest Week</div><div class="value">${fmt(last[curMetric], curMetric)}</div><div class="sub">${last.week}</div></div>
    <div class="kpi"><div class="label">WoW Change</div><div class="value ${wowClass}">${wow != null ? (wow > 0 ? '+' : '') + wow + '%' : '—'}</div></div>
    ${proj ? `<div class="kpi"><div class="label">Month Proj (${proj.month})</div><div class="value">${fmt(curMetric === 'regs' ? proj.projected_regs : curMetric === 'cost' ? proj.projected_spend : proj.projected_cpa, curMetric)}</div><div class="sub">${proj.source || ''}</div></div>` : ''}
    ${proj && proj.op2_regs ? `<div class="kpi"><div class="label">vs OP2</div><div class="value ${(proj.vs_op2_regs_pct||0) >= 0 ? 'good' : 'bad'}">${proj.vs_op2_regs_pct != null ? (proj.vs_op2_regs_pct > 0 ? '+' : '') + proj.vs_op2_regs_pct + '%' : '—'}</div></div>` : ''}
  `;
}

function renderChart(weeks) {
  const ctx = document.getElementById('mainChart').getContext('2d');
  if (chart) chart.destroy();
  const labels = weeks.map(w => 'W' + w.wk);
  const vals = weeks.map(w => w[curMetric]);
  const metricLabel = {regs:'Registrations',cost:'Cost ($)',cpa:'CPA ($)'}[curMetric];
  document.getElementById('chartTitle').textContent = `${metricLabel} — ${curMarket}`;
  chart = new Chart(ctx, {
    type: 'line',
    data: {
      labels,
      datasets: [{
        label: 'Actual', data: vals,
        borderColor: '#4a9eff', backgroundColor: '#4a9eff',
        borderWidth: 2.5, pointRadius: 4, tension: 0.3
      }]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      plugins: { legend: { display: false },
        tooltip: { callbacks: { label: c => fmt(c.parsed.y, curMetric) } }
      },
      scales: {
        x: { grid: { color: '#1f222b' }, ticks: { color: '#666', font: { size: 11 } } },
        y: { grid: { color: '#1f222b' }, ticks: { color: '#666', callback: v => fmt(v, curMetric) } }
      }
    }
  });
}

function renderTable(weeks) {
  const body = document.getElementById('weeklyBody');
  body.innerHTML = weeks.map((w, i) => {
    const prev = i > 0 ? weeks[i - 1] : null;
    const wow = prev && prev.regs ? ((w.regs - prev.regs) / prev.regs * 100).toFixed(1) : null;
    const wowBadge = wow != null
      ? `<span class="badge ${wow > 5 ? 'badge-green' : wow < -5 ? 'badge-red' : 'badge-yellow'}">${wow > 0 ? '+' : ''}${wow}%</span>`
      : '<span class="badge badge-gray">—</span>';
    return `<tr>
      <td>${w.week}</td>
      <td style="text-align:right">${fmt(w.regs, 'regs')}</td>
      <td style="text-align:right">${fmt(w.cost, 'cost')}</td>
      <td style="text-align:right">${fmt(w.cpa, 'cpa')}</td>
      <td>${wowBadge}</td>
    </tr>`;
  }).join('');
}

function renderProjection(proj) {
  const el = document.getElementById('projContent');
  if (!proj) { el.innerHTML = '<p style="color:#555;padding:20px;text-align:center">No projection data for this market</p>'; return; }
  el.innerHTML = `
    <table><thead><tr><th>Field</th><th style="text-align:right">Value</th></tr></thead><tbody>
      <tr><td>Month</td><td style="text-align:right">${proj.month}</td></tr>
      <tr><td>Projected Regs</td><td style="text-align:right">${fmt(proj.projected_regs, 'regs')}</td></tr>
      <tr><td>Projected Spend</td><td style="text-align:right">${fmt(proj.projected_spend, 'cost')}</td></tr>
      <tr><td>Projected CPA</td><td style="text-align:right">${fmt(proj.projected_cpa, 'cpa')}</td></tr>
      ${proj.op2_regs ? `<tr><td>OP2 Regs Target</td><td style="text-align:right">${fmt(proj.op2_regs, 'regs')}</td></tr>` : ''}
      ${proj.vs_op2_regs_pct != null ? `<tr><td>vs OP2 Regs</td><td style="text-align:right;color:${proj.vs_op2_regs_pct >= 0 ? '#4ade80' : '#f87171'}">${proj.vs_op2_regs_pct > 0 ? '+' : ''}${proj.vs_op2_regs_pct}%</td></tr>` : ''}
      <tr><td>Source</td><td style="text-align:right">${proj.source || '—'}</td></tr>
      ${proj.rationale ? `<tr><td colspan="2" style="color:#888;font-size:12px;padding-top:12px">${proj.rationale}</td></tr>` : ''}
    </tbody></table>
  `;
}

init();
</script>
</body>
</html>'''


# ============================================================
# PACING DASHBOARD TEMPLATE
# ============================================================
PACING_TEMPLATE = r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>PS Market Pacing Dashboard</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:#11111b;color:#cdd6f4;min-height:100vh;padding:24px}
.card{background:#1e1e2e;border-radius:10px;padding:16px;margin-bottom:12px}
h1{font-size:22px;font-weight:700}
.sub{font-size:13px;color:#6c7086;margin-top:4px}
.pill-row{display:flex;gap:6px;margin:12px 0}
.pill{padding:6px 14px;border-radius:6px;font-size:13px;cursor:pointer;border:none}
.pill-on{background:#89b4fa;color:#1e1e2e;font-weight:600}
.pill-off{background:#313244;color:#a6adc8}
.kpi-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:12px}
.kpi-card{background:#1e1e2e;border-radius:10px;padding:12px 16px}
.kpi-label{font-size:11px;color:#6c7086;text-transform:uppercase;letter-spacing:1px;margin-bottom:6px}
.kpi-value{font-size:20px;font-weight:700}
table{width:100%;border-collapse:collapse}
th{color:#6c7086;font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:1px;padding:8px 12px;border-bottom:1px solid #313244;text-align:left}
td{padding:10px 12px;border-bottom:1px solid #1e1e2e;font-size:14px}
.pacing-bar{display:flex;align-items:center;gap:8px}
.pacing-track{width:140px;height:16px;background:#2a2a3e;border-radius:4px;overflow:hidden;position:relative}
.pacing-fill{height:100%;border-radius:4px;transition:width .3s}
.pacing-mark{position:absolute;top:0;left:79%;width:2px;height:100%;background:#ffffff44}
.status{padding:3px 10px;border-radius:4px;font-size:12px;font-weight:600;display:inline-block}
.spark{display:block}
.month-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:10px;margin-top:12px}
.month-card{background:#181825;border-radius:8px;padding:12px}
.month-label{font-size:13px;color:#6c7086;margin-bottom:4px}
.month-val{font-size:18px;font-weight:700}
.month-sub{font-size:11px;color:#6c7086}
.ts{font-size:11px;color:#45475a;text-align:center;margin-top:16px}
</style>
</head>
<body>
<div class="card" style="display:flex;justify-content:space-between;align-items:center">
  <div><h1>Market Pacing Dashboard</h1><p class="sub">All 10 markets • 2026 YTD vs OP targets</p></div>
  <div class="pill-row" id="metricPills"></div>
</div>
<div class="kpi-grid" id="kpiGrid"></div>
<div class="card" style="padding:0;overflow:hidden">
  <table><thead><tr id="tableHead"></tr></thead><tbody id="tableBody"></tbody></table>
</div>
<div class="card"><h2 style="font-size:16px;font-weight:700;margin-bottom:12px">Weekly Trend by Market</h2>
  <div id="sparkGrid" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:12px"></div>
</div>
<div class="ts" id="genTs"></div>
<script>
const DATA = __DATA_JSON__;
const markets = DATA.markets;
let curMetric = 'regs';

function init() {
  const pills = document.getElementById('metricPills');
  ['regs','cost'].forEach(m => {
    const b = document.createElement('button');
    b.className = 'pill ' + (m === curMetric ? 'pill-on' : 'pill-off');
    b.textContent = m === 'regs' ? 'Registrations' : 'Cost';
    b.onclick = () => { curMetric = m; render(); };
    pills.appendChild(b);
  });
  document.getElementById('genTs').textContent = 'Generated: ' + new Date().toLocaleString() + ' • Data from ps-analytics.duckdb';
  render();
}

function fmt(v, t) {
  if (v == null) return '—';
  if (t === 'cost') return '$' + Math.round(v).toLocaleString();
  if (t === 'pct') return Number(v).toFixed(1) + '%';
  return Math.round(v).toLocaleString();
}

function pacingColor(pct) { return pct >= 95 ? '#27ae60' : pct >= 80 ? '#f39c12' : '#e74c3c'; }
function statusColor(s) { return s === 'on_track' ? '#27ae60' : s === 'at_risk' ? '#f39c12' : s === 'behind' ? '#e74c3c' : '#95a5a6'; }

function computeMarketStats() {
  return markets.map(m => {
    const weeks = DATA.weekly[m] || [];
    const proj = DATA.projections[m];
    const ytd = weeks.reduce((s, w) => s + (curMetric === 'cost' ? w.cost : w.regs), 0);
    const op2 = proj ? (curMetric === 'cost' ? proj.op2_spend : proj.op2_regs) : null;
    // Annualize: 13 weeks of data, project to 52
    const annualTarget = op2 ? op2 * 12 : null; // rough — OP2 is monthly
    const monthActual = weeks.slice(-4).reduce((s, w) => s + (curMetric === 'cost' ? w.cost : w.regs), 0);
    const monthTarget = op2 || 0;
    const mtdPct = monthTarget > 0 ? (monthActual / monthTarget * 100) : 0;
    const ytdPct = annualTarget > 0 ? (ytd / annualTarget * 100) : 0;
    const status = mtdPct >= 95 ? 'on_track' : mtdPct >= 80 ? 'at_risk' : 'behind';
    const sparkData = weeks.map(w => curMetric === 'cost' ? w.cost : w.regs);
    return {
      market: m, ytd, monthActual, monthTarget, mtdPct, annualTarget, ytdPct, status, sparkData,
      vs_op2: proj ? (curMetric === 'cost' ? proj.vs_op2_spend_pct : proj.vs_op2_regs_pct) : null,
      rationale: proj ? proj.rationale : null
    };
  }).sort((a, b) => b.ytd - a.ytd);
}

function render() {
  document.querySelectorAll('.pill').forEach(b => {
    b.className = 'pill ' + (b.textContent.toLowerCase().startsWith(curMetric === 'regs' ? 'r' : 'c') ? 'pill-on' : 'pill-off');
  });
  const stats = computeMarketStats();
  const fmtType = curMetric === 'cost' ? 'cost' : 'regs';

  // KPIs
  const totalYTD = stats.reduce((s, m) => s + m.ytd, 0);
  const onTrack = stats.filter(m => m.status === 'on_track').length;
  const atRisk = stats.filter(m => m.status === 'at_risk').length;
  const behind = stats.filter(m => m.status === 'behind').length;
  document.getElementById('kpiGrid').innerHTML = [
    { label: 'WW YTD ' + (curMetric === 'cost' ? 'Spend' : 'Regs'), value: fmt(totalYTD, fmtType) },
    { label: 'Markets Tracked', value: stats.length },
    { label: 'Weeks of Data', value: (DATA.weekly[markets[0]] || []).length },
    { label: 'Status', value: `${onTrack} on track • ${atRisk} at risk • ${behind} behind` }
  ].map(k => `<div class="kpi-card"><div class="kpi-label">${k.label}</div><div class="kpi-value">${k.value}</div></div>`).join('');

  // Table
  document.getElementById('tableHead').innerHTML = `
    <th>Market</th><th style="text-align:right">YTD</th><th style="text-align:right">Latest Wk</th>
    <th>vs OP2</th><th>Status</th>
  `;
  document.getElementById('tableBody').innerHTML = stats.map((m, i) => {
    const lastWk = (DATA.weekly[m.market] || []).slice(-1)[0];
    const lastVal = lastWk ? (curMetric === 'cost' ? lastWk.cost : lastWk.regs) : 0;
    const statusLabel = m.status === 'on_track' ? 'On Track' : m.status === 'at_risk' ? 'At Risk' : 'Behind';
    const vsOp2 = m.vs_op2 != null ? `<span style="color:${m.vs_op2 >= 0 ? '#27ae60' : '#e74c3c'};font-weight:600">${m.vs_op2 > 0 ? '+' : ''}${m.vs_op2}%</span>` : '—';
    return `<tr style="background:${i % 2 === 0 ? '#1e1e2e' : '#181825'}">
      <td style="font-weight:700">${m.market}</td>
      <td style="text-align:right">${fmt(m.ytd, fmtType)}</td>
      <td style="text-align:right">${fmt(lastVal, fmtType)}</td>
      <td>${vsOp2}</td>
      <td><span class="status" style="background:${statusColor(m.status)}22;color:${statusColor(m.status)}">${statusLabel}</span></td>
    </tr>`;
  }).join('');

  // Sparklines
  document.getElementById('sparkGrid').innerHTML = stats.map(m => {
    const data = m.sparkData;
    if (data.length < 2) return `<div style="background:#181825;border-radius:8px;padding:12px"><div style="font-weight:600">${m.market}</div><div style="color:#6c7086;font-size:12px">No trend data</div></div>`;
    const max = Math.max(...data), min = Math.min(...data);
    const range = max - min || 1;
    const w = 160, h = 40, pad = 2;
    const pts = data.map((v, i) => {
      const x = pad + (i / (data.length - 1)) * (w - pad * 2);
      const y = h - pad - ((v - min) / range) * (h - pad * 2);
      return `${x},${y}`;
    }).join(' ');
    const last = data[data.length - 1], prev = data[data.length - 2];
    const color = last >= prev ? '#27ae60' : '#e74c3c';
    return `<div style="background:#181825;border-radius:8px;padding:12px">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px">
        <span style="font-weight:600">${m.market}</span>
        <span style="font-size:12px;color:${color}">${fmt(last, fmtType)}</span>
      </div>
      <svg width="${w}" height="${h}" class="spark"><polyline points="${pts}" fill="none" stroke="${color}" stroke-width="2"/></svg>
    </div>`;
  }).join('');
}

init();
</script>
</body>
</html>'''


# ============================================================
# MAIN
# ============================================================
if __name__ == '__main__':
    print("Querying ps-analytics.duckdb...")
    weekly = get_weekly_data()
    monthly = get_monthly_data()
    projections = get_projections()
    print(f"  Weekly: {len(weekly)} rows across {len(set(r['market'] for r in weekly))} markets")
    print(f"  Monthly: {len(monthly)} rows")
    print(f"  Projections: {len(projections)} rows")

    print("\nGenerating forecast-tracker.html...")
    ft_html = build_forecast_tracker(weekly, projections)
    ft_path = os.path.join(OUT_DIR, "forecast-tracker.html")
    with open(ft_path, 'w') as f:
        f.write(ft_html)
    print(f"  Written to {ft_path} ({len(ft_html):,} bytes)")

    print("\nGenerating pacing-dashboard.html...")
    pd_html = build_pacing_dashboard(weekly, monthly, projections)
    pd_path = os.path.join(OUT_DIR, "pacing-dashboard.html")
    with open(pd_path, 'w') as f:
        f.write(pd_html)
    print(f"  Written to {pd_path} ({len(pd_html):,} bytes)")

    print("\nDone. Upload to Amazon Drive:")
    print(f"  https://drive-render.corp.amazon.com/view/prichwil@/dashboards/forecast-tracker.html")
    print(f"  https://drive-render.corp.amazon.com/view/prichwil@/dashboards/pacing-dashboard.html")
