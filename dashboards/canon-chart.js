/**
 * canon-chart.js — Single source of truth for the PS performance chart.
 *
 * Two render modes:
 *   - default:     "one glance" chart (actuals + latest prediction, continuous line)
 *   - calibration: "how did the model do?" chart (adds first prediction overlay)
 *
 * Both modes read the same forecast-data.json payload:
 *   weekly[market][].{regs, cost, op2_regs}                  - actuals + OP2
 *   predictions_history[market][wk].{regs, cost}.{first_pred, latest_pred,
 *                                                 first_ci_lo, first_ci_hi,
 *                                                 latest_ci_lo, latest_ci_hi,
 *                                                 actual, score, n_preds}
 *
 * Visual spec (locked 2026-04-20):
 *   Orange  (#f97316) = Registrations  |  Blue (#4a9eff) = Spend
 *   Solid line         = actual (past weeks only)
 *   Dashed line        = latest prediction (future weeks in default; all weeks in calibration)
 *   Thin solid + square markers = first prediction (calibration view only)
 *   Light orange fill  = CI band (latest CI, regs only, from Now forward)
 *   Gray dashed line   = OP2 target (regs only)
 *   Green dashed vert  = "Now" line at latest week with actuals
 *
 * Caller API:
 *   CanonChart.render(canvasOrId, {
 *     forecastData: <forecast-data.json>,
 *     market: 'WW'|'EU5'|'US'|...,
 *     mode: 'default' | 'calibration',   // default if omitted
 *     highlightWeek: 'W16',              // optional
 *     chartInstance: <prior Chart>       // optional, destroyed before rerender
 *   })
 */

(function (global) {
  const ORANGE = '#f97316';
  const ORANGE_SOFT = 'rgba(249,115,22,0.14)';
  const BLUE = '#4a9eff';
  const GRAY = '#6c7086';
  const NOW_GREEN = 'rgba(74,222,128,0.5)';

  function toNumOrNull(v) {
    if (v === null || v === undefined || v === '') return null;
    const n = typeof v === 'number' ? v : parseFloat(v);
    return Number.isFinite(n) ? n : null;
  }

  /**
   * Build per-week series arrays indexed 0..51 (W1..W52).
   * Returns everything the chart needs, already split into past/future for the
   * default "continuous line" visual.
   */
  function buildSeries(forecastData, market) {
    const weeklyRows = (forecastData.weekly && forecastData.weekly[market]) || [];
    const byWk = {};
    weeklyRows.forEach((r) => { if (r.wk) byWk[r.wk] = r; });
    const hist = (forecastData.predictions_history && forecastData.predictions_history[market]) || {};
    const maxWk = forecastData.max_week || forecastData.max_wk || 15;

    // Labels always span the full year so the x-axis is stable across markets.
    const labels = [];
    for (let w = 1; w <= 52; w++) labels.push('W' + w);

    // Series aligned to labels. `null` means "no data for this week".
    const regsActual = new Array(52).fill(null);
    const regsLatestAll = new Array(52).fill(null);     // used in calibration
    const regsLatestFuture = new Array(52).fill(null);  // used in default (Now+ only)
    const regsFirst = new Array(52).fill(null);         // calibration only
    const ciLoAll = new Array(52).fill(null);
    const ciHiAll = new Array(52).fill(null);
    const ciLoFuture = new Array(52).fill(null);
    const ciHiFuture = new Array(52).fill(null);
    const op2Regs = new Array(52).fill(null);
    const spendActual = new Array(52).fill(null);        // $K
    const spendLatestAll = new Array(52).fill(null);
    const spendLatestFuture = new Array(52).fill(null);
    const spendFirst = new Array(52).fill(null);

    // Cold-start / DuckDB-unreachable fallback: if refresh-forecast.py could
    // not overwrite pred_regs from ps.forecasts (e.g. MotherDuck offline),
    // the xlsx values remain as-is and the chart still renders. When the
    // pipeline is healthy, these fallbacks are essentially dead code because
    // row.pred_regs === hReg.latest_pred after the overwrite pass.
    const hasHistory = Object.keys(hist).length > 0;

    for (let w = 1; w <= 52; w++) {
      const row = byWk[w] || {};
      const h = hist[String(w)] || {};
      const hReg = h.regs || {};
      const hCost = h.cost || {};
      const i = w - 1;

      // Actuals (past only — weeks with non-zero data)
      const hasActual = (row.regs && row.regs > 0) || (row.cost && row.cost > 0);
      if (hasActual) {
        if (row.regs) regsActual[i] = row.regs;
        if (row.cost) spendActual[i] = row.cost / 1000;
      }

      // Latest predictions — prefer ps.forecasts history, fall back to xlsx PER WEEK
      // (not per market — history is sparse and only covers recent weeks today).
      let latestRegs = toNumOrNull(hReg.latest_pred);
      let latestCiLo = toNumOrNull(hReg.latest_ci_lo);
      let latestCiHi = toNumOrNull(hReg.latest_ci_hi);
      let latestCost = toNumOrNull(hCost.latest_pred);
      if (latestRegs === null) latestRegs = toNumOrNull(row.pred_regs);
      if (latestCiLo === null) latestCiLo = toNumOrNull(row.ci_lo);
      if (latestCiHi === null) latestCiHi = toNumOrNull(row.ci_hi);
      if (latestCost === null) latestCost = toNumOrNull(row.pred_cost);

      if (latestRegs !== null) {
        regsLatestAll[i] = latestRegs;
        // Default view: show prediction line across the full year so past weeks
        // reveal "predicted vs actual" and future weeks reveal trajectory.
        regsLatestFuture[i] = latestRegs;
      }
      if (latestCost !== null) {
        const k = latestCost / 1000;
        spendLatestAll[i] = k;
        spendLatestFuture[i] = k;
      }
      if (latestCiLo !== null) {
        ciLoAll[i] = latestCiLo;
        if (w > maxWk) ciLoFuture[i] = latestCiLo;
      }
      if (latestCiHi !== null) {
        ciHiAll[i] = latestCiHi;
        if (w > maxWk) ciHiFuture[i] = latestCiHi;
      }

      // First predictions (calibration view only — always show all weeks
      // they exist for, regardless of past/future)
      regsFirst[i] = toNumOrNull(hReg.first_pred);
      spendFirst[i] = hCost.first_pred !== null && hCost.first_pred !== undefined
        ? toNumOrNull(hCost.first_pred) / 1000 : null;

      // OP2 target — regs only
      op2Regs[i] = toNumOrNull(row.op2_regs);
    }

    // Keep CI band anchored to the last actual so it starts visually at "Now"
    // rather than floating detached. (Predictions render across all weeks now,
    // so no anchor needed on the prediction lines themselves.)
    const lastActualRegsIdx = maxWk - 1;
    return {
      labels, maxWk,
      regsActual, regsLatestAll, regsLatestFuture, regsFirst,
      ciLoAll, ciHiAll, ciLoFuture, ciHiFuture,
      op2Regs,
      spendActual, spendLatestAll, spendLatestFuture, spendFirst,
    };
  }

  function buildDefaultDatasets(s) {
    // Order matters for Chart.js fill references: CI high fills DOWN to CI low (idx+1)
    return [
      // CI band (regs, future only) — renders first so actuals/preds sit on top
      {
        label: '_ciHi', data: s.ciHiFuture,
        borderColor: 'transparent', backgroundColor: ORANGE_SOFT,
        borderWidth: 0, pointRadius: 0, fill: '+1', tension: 0.25,
        yAxisID: 'y', spanGaps: true, _hidden: true,
      },
      {
        label: '_ciLo', data: s.ciLoFuture,
        borderColor: 'transparent', backgroundColor: ORANGE_SOFT,
        borderWidth: 0, pointRadius: 0, fill: false, tension: 0.25,
        yAxisID: 'y', spanGaps: true, _hidden: true,
      },
      // OP2 target
      {
        label: 'OP2 target', data: s.op2Regs,
        borderColor: GRAY, backgroundColor: 'transparent',
        borderWidth: 1.5, borderDash: [3, 3], pointRadius: 0, tension: 0,
        yAxisID: 'y', spanGaps: true,
      },
      // Regs actual (solid orange, past only)
      {
        label: 'Regs (actual)', data: s.regsActual,
        borderColor: ORANGE, backgroundColor: ORANGE,
        borderWidth: 2.5, pointRadius: 3, pointBackgroundColor: ORANGE,
        tension: 0.25, yAxisID: 'y', spanGaps: false,
      },
      // Regs latest pred (dashed orange, future only; anchored at maxWk actual)
      {
        label: 'Regs (predicted)', data: s.regsLatestFuture,
        borderColor: ORANGE, backgroundColor: 'transparent',
        borderWidth: 2, borderDash: [6, 4], pointRadius: 0, tension: 0.25,
        yAxisID: 'y', spanGaps: true,
      },
      // Spend actual (solid blue)
      {
        label: 'Spend (actual, $K)', data: s.spendActual,
        borderColor: BLUE, backgroundColor: BLUE,
        borderWidth: 2.5, pointRadius: 3, pointBackgroundColor: BLUE,
        tension: 0.25, yAxisID: 'y1', spanGaps: false,
      },
      // Spend latest pred (dashed blue)
      {
        label: 'Spend (predicted, $K)', data: s.spendLatestFuture,
        borderColor: BLUE, backgroundColor: 'transparent',
        borderWidth: 2, borderDash: [6, 4], pointRadius: 0, tension: 0.25,
        yAxisID: 'y1', spanGaps: true,
      },
    ];
  }

  function buildCalibrationDatasets(s) {
    // Calibration view shows predictions at ALL weeks (not just future), so
    // the viewer can see actual vs each-of-two-predictions side by side.
    return [
      // CI band across all weeks with a latest CI (wider view of uncertainty)
      {
        label: '_ciHi', data: s.ciHiAll,
        borderColor: 'transparent', backgroundColor: ORANGE_SOFT,
        borderWidth: 0, pointRadius: 0, fill: '+1', tension: 0.25,
        yAxisID: 'y', spanGaps: true, _hidden: true,
      },
      {
        label: '_ciLo', data: s.ciLoAll,
        borderColor: 'transparent', backgroundColor: ORANGE_SOFT,
        borderWidth: 0, pointRadius: 0, fill: false, tension: 0.25,
        yAxisID: 'y', spanGaps: true, _hidden: true,
      },
      // OP2
      {
        label: 'OP2 target', data: s.op2Regs,
        borderColor: GRAY, backgroundColor: 'transparent',
        borderWidth: 1.5, borderDash: [3, 3], pointRadius: 0, tension: 0,
        yAxisID: 'y', spanGaps: true,
      },
      // Regs actual
      {
        label: 'Regs (actual)', data: s.regsActual,
        borderColor: ORANGE, backgroundColor: ORANGE,
        borderWidth: 2.5, pointRadius: 3, pointBackgroundColor: ORANGE,
        tension: 0.25, yAxisID: 'y', spanGaps: false,
      },
      // Regs first prediction (thin solid + square markers)
      {
        label: 'Regs (first pred)', data: s.regsFirst,
        borderColor: ORANGE, backgroundColor: 'transparent',
        borderWidth: 1, pointRadius: 3, pointStyle: 'rect',
        pointBackgroundColor: 'transparent', pointBorderColor: ORANGE,
        tension: 0.25, yAxisID: 'y', spanGaps: true,
      },
      // Regs latest prediction (dashed orange, all weeks)
      {
        label: 'Regs (latest pred)', data: s.regsLatestAll,
        borderColor: ORANGE, backgroundColor: 'transparent',
        borderWidth: 2, borderDash: [6, 4], pointRadius: 0, tension: 0.25,
        yAxisID: 'y', spanGaps: true,
      },
      // Spend actual
      {
        label: 'Spend (actual, $K)', data: s.spendActual,
        borderColor: BLUE, backgroundColor: BLUE,
        borderWidth: 2.5, pointRadius: 3, pointBackgroundColor: BLUE,
        tension: 0.25, yAxisID: 'y1', spanGaps: false,
      },
      // Spend first prediction
      {
        label: 'Spend (first pred, $K)', data: s.spendFirst,
        borderColor: BLUE, backgroundColor: 'transparent',
        borderWidth: 1, pointRadius: 3, pointStyle: 'rect',
        pointBackgroundColor: 'transparent', pointBorderColor: BLUE,
        tension: 0.25, yAxisID: 'y1', spanGaps: true,
      },
      // Spend latest prediction
      {
        label: 'Spend (latest pred, $K)', data: s.spendLatestAll,
        borderColor: BLUE, backgroundColor: 'transparent',
        borderWidth: 2, borderDash: [6, 4], pointRadius: 0, tension: 0.25,
        yAxisID: 'y1', spanGaps: true,
      },
    ];
  }

  function renderCanonChart(canvasOrId, opts) {
    const ctx = typeof canvasOrId === 'string'
      ? document.getElementById(canvasOrId) : canvasOrId;
    if (!ctx) { console.warn('[canon-chart] canvas not found'); return null; }
    if (opts.chartInstance) opts.chartInstance.destroy();

    const mode = opts.mode === 'calibration' ? 'calibration' : 'default';
    const s = buildSeries(opts.forecastData, opts.market);
    const datasets = mode === 'calibration'
      ? buildCalibrationDatasets(s) : buildDefaultDatasets(s);

    const chart = new Chart(ctx, {
      type: 'line',
      data: { labels: s.labels, datasets: datasets },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: { mode: 'index', intersect: false, axis: 'x' },
        plugins: {
          legend: {
            position: 'bottom',
            labels: {
              color: '#888', font: { size: 11 },
              filter: (item) => !item.text.startsWith('_'),
              boxWidth: 24,
              usePointStyle: false,
            },
          },
          tooltip: {
            mode: 'index',
            intersect: false,
            // Show week label in the tooltip header so it's unambiguous
            callbacks: {
              title: (items) => items.length ? items[0].label : '',
              label: (item) => {
                if (item.dataset.label && item.dataset.label.startsWith('_')) return null;
                const v = item.parsed.y;
                if (v == null) return null;
                const isSpend = item.dataset.label.includes('$K');
                const val = Math.round(v).toLocaleString();
                return item.dataset.label + ': ' + (isSpend ? '$' + val + 'K' : val);
              },
            },
          },
          annotation: {
            annotations: {
              nowLine: {
                type: 'line',
                xMin: s.maxWk - 1, xMax: s.maxWk - 1,
                borderColor: NOW_GREEN, borderWidth: 2, borderDash: [4, 4],
                label: {
                  display: true, content: 'Now (W' + s.maxWk + ')',
                  color: '#4ade80', font: { size: 10 }, position: 'start',
                  backgroundColor: 'rgba(0,0,0,0)',
                },
              },
            },
          },
        },
        scales: {
          x: {
            grid: { color: '#1f222b' },
            ticks: {
              color: '#666', font: { size: 10 },
              // Show every 2nd week — more anchors for matching chart points to table rows
              autoSkip: false,
              callback: function (val, idx) {
                const lbl = this.getLabelForValue(val);
                const n = parseInt(lbl.replace('W', ''), 10);
                return (n % 2 === 0 || n === 1 || n === 52) ? lbl : '';
              },
            },
          },
          y: {
            position: 'left', grid: { color: '#1f222b' },
            ticks: { color: '#666' },
            title: { display: true, text: 'Registrations', color: ORANGE },
          },
          y1: {
            position: 'right', grid: { display: false },
            ticks: { color: BLUE, callback: (v) => '$' + v + 'K' },
            title: { display: true, text: 'Spend ($K)', color: BLUE },
          },
        },
      },
    });

    // Highlight selected week on the regs actual line
    if (opts.highlightWeek) {
      const targetWk = parseInt(String(opts.highlightWeek).replace('W', ''), 10);
      if (!isNaN(targetWk)) {
        const idx = targetWk - 1;
        // Find the "Regs (actual)" dataset by label — safer than index math
        const ds = chart.data.datasets.find((d) => d.label === 'Regs (actual)');
        if (ds && ds.data[idx] != null) {
          ds.pointRadius = ds.data.map((_, i) => (i === idx ? 7 : 3));
          ds.pointBackgroundColor = ds.data.map((_, i) => (i === idx ? '#fff' : ORANGE));
          chart.update();
        }
      }
    }

    return chart;
  }

  global.CanonChart = { render: renderCanonChart };
})(typeof window !== 'undefined' ? window : globalThis);
