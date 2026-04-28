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

  // ========================================================================
  // Scenario mode (M2) — for Projection Engine. Accepts a richer input than
  // the tracker/calibration modes because it supports CI bands, counterfactual
  // lines, regime-onset rules, period highlights, and a narrated-contribution
  // tooltip. The mode is orthogonal to the tracker mode: one library, two
  // call sites, no shared datasets.
  //
  // Expected input (opts.scenarioData):
  //   {
  //     labels:          string[]   // x-axis labels (week numbers or dates)
  //     regsActual:      number[]   // actual brand+nb regs per label; null for future
  //     regsProjTotal:   number[]   // projected total regs per label; null for past
  //     regsProjBrand:   number[]   // projected brand regs
  //     regsProjNb:      number[]   // projected non-brand regs
  //     spendActual:     number[]   // actual total spend ($)
  //     spendProj:       number[]   // projected total spend ($)
  //     ciLow, ciHigh:   number[]   // 90% CI on projected total regs (null for past)
  //     counterfactual:  number[]   // brand-only counterfactual regs (optional)
  //     todayIdx:        number     // index of the YTD/projected seam
  //     targetRegs:      number     // horizontal target line (optional, per-week)
  //     regimes:         [{ label, onsetIdx, endIdx, absorbed }]
  //     periodHighlight: { startIdx, endIdx }  // optional
  //     tooltipFormatter:(ctx, idx) => string  // custom HTML for narrated tooltip
  //   }
  // ========================================================================

  function buildScenarioDatasets(sd) {
    const datasets = [];

    // CI band (areaY-equivalent in Chart.js: two transparent lines with `fill: '+1'`)
    if (sd.ciHigh && sd.ciLow) {
      datasets.push({
        label: '_ciHi', data: sd.ciHigh,
        borderColor: 'transparent', backgroundColor: ORANGE_SOFT,
        borderWidth: 0, pointRadius: 0, fill: '+1', tension: 0.25,
        yAxisID: 'y', spanGaps: true, _hidden: true,
      });
      datasets.push({
        label: '_ciLo', data: sd.ciLow,
        borderColor: 'transparent', backgroundColor: ORANGE_SOFT,
        borderWidth: 0, pointRadius: 0, fill: false, tension: 0.25,
        yAxisID: 'y', spanGaps: true, _hidden: true,
      });
    }

    // Counterfactual — dashed grey, brand-only; hidden by default so users
    // opt into seeing it (matches projection-app's Counterfactual disclosure).
    if (sd.counterfactual) {
      datasets.push({
        label: 'Brand counterfactual', data: sd.counterfactual,
        borderColor: GRAY, backgroundColor: 'transparent',
        borderWidth: 1.5, borderDash: [5, 4], pointRadius: 0, tension: 0.25,
        yAxisID: 'y', spanGaps: true, hidden: true,
      });
    }

    // Actuals — solid orange, past only
    datasets.push({
      label: 'Actuals (regs)', data: sd.regsActual || [],
      borderColor: ORANGE, backgroundColor: ORANGE,
      borderWidth: 2.5, pointRadius: 3, pointBackgroundColor: ORANGE,
      tension: 0.25, yAxisID: 'y', spanGaps: false,
    });

    // Projected Total — solid dark, future weeks
    if (sd.regsProjTotal) {
      datasets.push({
        label: 'Projected Total', data: sd.regsProjTotal,
        borderColor: '#1A1A1A', backgroundColor: 'transparent',
        borderWidth: 2.5, borderDash: [], pointRadius: 0, tension: 0.25,
        yAxisID: 'y', spanGaps: true,
      });
    }

    // Projected Brand — dashed blue
    if (sd.regsProjBrand) {
      datasets.push({
        label: 'Projected Brand', data: sd.regsProjBrand,
        borderColor: BLUE, backgroundColor: 'transparent',
        borderWidth: 2, borderDash: [6, 4], pointRadius: 0, tension: 0.25,
        yAxisID: 'y', spanGaps: true,
      });
    }

    // Projected NB — dashed orange (explicit NB line, not inferred)
    if (sd.regsProjNb) {
      datasets.push({
        label: 'Projected Non-Brand', data: sd.regsProjNb,
        borderColor: '#FF9900', backgroundColor: 'transparent',
        borderWidth: 2, borderDash: [6, 4], pointRadius: 0, tension: 0.25,
        yAxisID: 'y', spanGaps: true,
      });
    }

    // Spend actual (solid blue, on secondary axis) — hidden by default per
    // projection-app's legend default (scaled-spend was noisy on cold load).
    if (sd.spendActual) {
      datasets.push({
        label: 'Spend actual ($K)', data: sd.spendActual.map(v => v == null ? null : v / 1000),
        borderColor: BLUE, backgroundColor: BLUE,
        borderWidth: 2, pointRadius: 2, pointBackgroundColor: BLUE,
        tension: 0.25, yAxisID: 'y1', spanGaps: false, hidden: true,
      });
    }

    // Spend projected (dashed blue, on secondary axis, hidden by default)
    if (sd.spendProj) {
      datasets.push({
        label: 'Spend projected ($K)', data: sd.spendProj.map(v => v == null ? null : v / 1000),
        borderColor: BLUE, backgroundColor: 'transparent',
        borderWidth: 2, borderDash: [6, 4], pointRadius: 0, tension: 0.25,
        yAxisID: 'y1', spanGaps: true, hidden: true,
      });
    }

    return datasets;
  }

  // Build the annotation plugin config for scenario extras (today line,
  // regime regions + onset rules, target line, period highlight).
  function buildScenarioAnnotations(sd) {
    const annotations = {};

    // Today seam — dashed green vertical at the YTD/projected boundary
    if (typeof sd.todayIdx === 'number' && sd.todayIdx >= 0) {
      annotations.todayLine = {
        type: 'line',
        xMin: sd.todayIdx, xMax: sd.todayIdx,
        borderColor: NOW_GREEN, borderWidth: 2, borderDash: [4, 4],
        label: {
          display: true, content: '↓ Today',
          color: '#4ade80', font: { size: 10, weight: '600' },
          position: 'start',
          backgroundColor: 'rgba(0,0,0,0)',
        },
      };
    }

    // Regime lift regions + onset rules + labels
    const regimes = sd.regimes || [];
    regimes.forEach((r, i) => {
      if (r.absorbed) return;  // absorbed lifts don't render onset markers
      if (typeof r.onsetIdx !== 'number') return;
      if (typeof r.endIdx === 'number' && r.endIdx > r.onsetIdx) {
        annotations[`regime-region-${i}`] = {
          type: 'box',
          xMin: r.onsetIdx, xMax: r.endIdx,
          backgroundColor: 'rgba(168, 85, 247, 0.08)',
          borderColor: 'transparent',
          drawTime: 'beforeDatasetsDraw',
        };
      }
      annotations[`regime-onset-${i}`] = {
        type: 'line',
        xMin: r.onsetIdx, xMax: r.onsetIdx,
        borderColor: 'rgba(168, 85, 247, 0.7)',
        borderWidth: 1.5, borderDash: [3, 3],
        label: {
          display: true,
          content: r.label || `Lift #${i + 1} onset`,
          color: 'rgba(168, 85, 247, 0.9)',
          font: { size: 10, weight: '500' },
          position: 'start',
          backgroundColor: 'rgba(0,0,0,0)',
          yAdjust: 2,
        },
      };
    });

    // Horizontal target line (per-week)
    if (typeof sd.targetRegs === 'number' && sd.targetRegs > 0) {
      annotations.targetLine = {
        type: 'line',
        yMin: sd.targetRegs, yMax: sd.targetRegs,
        borderColor: '#4a9eff', borderWidth: 1.5, borderDash: [6, 3],
        label: {
          display: true, content: `Target ${Math.round(sd.targetRegs).toLocaleString()}/wk`,
          color: '#4a9eff', font: { size: 10 },
          position: 'end',
          backgroundColor: 'rgba(0,0,0,0)',
        },
      };
    }

    // Period highlight box
    if (sd.periodHighlight && typeof sd.periodHighlight.startIdx === 'number') {
      annotations.periodHighlight = {
        type: 'box',
        xMin: sd.periodHighlight.startIdx,
        xMax: sd.periodHighlight.endIdx,
        backgroundColor: 'rgba(74, 158, 255, 0.04)',
        borderColor: 'rgba(74, 158, 255, 0.3)',
        borderWidth: 1, borderDash: [2, 3],
        drawTime: 'beforeDatasetsDraw',
      };
    }

    return annotations;
  }

  function renderScenarioChart(ctx, opts) {
    const sd = opts.scenarioData || {};
    const datasets = buildScenarioDatasets(sd);
    const annotations = buildScenarioAnnotations(sd);

    return new Chart(ctx, {
      type: 'line',
      data: { labels: sd.labels || [], datasets: datasets },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: { mode: 'index', intersect: false, axis: 'x' },
        // P2-08: register datalabels only on scenario mode. Plugin labels
        // the last non-null point on each visible line with series name +
        // value so the user reads the chart left-to-right and lands on the
        // series identity without chasing the legend.
        layout: { padding: { right: 80 } },  // breathing room for end labels
        plugins: {
          legend: {
            position: 'bottom',
            labels: {
              color: '#888', font: { size: 11 },
              filter: (item) => !item.text.startsWith('_'),
              boxWidth: 24, usePointStyle: false,
            },
          },
          tooltip: {
            mode: 'index',
            intersect: false,
            callbacks: {
              title: (items) => items.length ? items[0].label : '',
              // Custom narrated tooltip if caller provides one, else numeric default.
              label: (item) => {
                if (item.dataset.label && item.dataset.label.startsWith('_')) return null;
                if (typeof sd.tooltipFormatter === 'function') return null;  // suppressed; external plugin handles
                const v = item.parsed.y;
                if (v == null) return null;
                const isSpend = item.dataset.label.includes('$K');
                const val = Math.round(v).toLocaleString();
                return item.dataset.label + ': ' + (isSpend ? '$' + val + 'K' : val);
              },
            },
            // When tooltipFormatter is provided, render via external plugin
            // so the narrated contribution HTML ("40% seasonal, 40% trend...")
            // can appear alongside the numeric datasets.
            external: typeof sd.tooltipFormatter === 'function'
              ? (context) => {
                  // Minimal implementation: append narrated HTML to the tooltip body.
                  // The caller is responsible for providing context-aware HTML.
                  const tt = context.tooltip;
                  if (!tt || tt.opacity === 0) return;
                  const idx = tt.dataPoints && tt.dataPoints[0] ? tt.dataPoints[0].dataIndex : null;
                  if (idx == null) return;
                  let el = document.getElementById('scenario-tooltip-external');
                  if (!el) {
                    el = document.createElement('div');
                    el.id = 'scenario-tooltip-external';
                    el.style.cssText = 'position:absolute;pointer-events:none;background:#1a1d27;border:1px solid #2a2d35;border-radius:6px;padding:10px 12px;font-size:12px;color:#e0e0e0;max-width:280px;z-index:1000;transition:opacity 100ms;';
                    document.body.appendChild(el);
                  }
                  el.innerHTML = sd.tooltipFormatter(context, idx);
                  const rect = context.chart.canvas.getBoundingClientRect();
                  el.style.left = (rect.left + window.scrollX + tt.caretX + 14) + 'px';
                  el.style.top  = (rect.top  + window.scrollY + tt.caretY + 14) + 'px';
                  el.style.opacity = '1';
                }
              : undefined,
          },
          annotation: { annotations: annotations },
          // P2-08: scenario-only line end-labels. The datalabels plugin
          // fires for every point by default, so we suppress all except
          // the last non-null index on each line (= the visual end of the
          // series). Skip underscore-prefixed series (_ciHi/_ciLo) because
          // those are the CI fill helpers, not lines users need to read.
          datalabels: {
            display: (ctx) => {
              const ds = ctx.dataset;
              if (!ds || !ds.label || ds.label.startsWith('_')) return false;
              // Find the last index of a finite numeric value in this dataset.
              const arr = ds.data || [];
              let lastIdx = -1;
              for (let i = arr.length - 1; i >= 0; i--) {
                if (Number.isFinite(arr[i])) { lastIdx = i; break; }
              }
              return ctx.dataIndex === lastIdx;
            },
            anchor: 'end',
            align: 'right',
            offset: 6,
            clamp: true,
            font: { size: 10, weight: '500' },
            color: (ctx) => ctx.dataset.borderColor || '#666',
            formatter: (value, ctx) => {
              if (!Number.isFinite(value)) return '';
              const label = ctx.dataset.label || '';
              const isSpend = label.includes('$K');
              const v = Math.round(value).toLocaleString();
              // Short label — series + value, no dataset noise
              const shortName = label
                .replace(' ($K)', '')
                .replace(' actual', '')
                .replace(' projected', '')
                .replace('Projected ', '')
                .replace('Actuals ', '')
                .replace('Actuals (regs)', 'Actuals')
                .replace(/\(regs\)/, '')
                .trim();
              return (isSpend ? '$' + v + 'K' : v) + '  ' + shortName;
            },
          },
        },
        scales: {
          x: {
            grid: { color: '#1f222b' },
            ticks: { color: '#666', font: { size: 10 }, autoSkip: true, maxRotation: 0 },
          },
          y: {
            position: 'left', grid: { color: '#1f222b' },
            ticks: { color: '#666' },
            title: { display: true, text: 'Registrations', color: ORANGE },
            // P2-16: tighten y-axis headroom — default Chart.js gives ~30-60%
            // of extra space above the peak. Compute the actual max across the
            // regs datasets and pad by 12% so the peak breathes but doesn't
            // drown in empty space. Null values are filtered out automatically.
            suggestedMax: (() => {
              const regArrays = [sd.regsActual, sd.regsProjTotal, sd.regsProjBrand, sd.regsProjNb, sd.ciHigh];
              let peak = 0;
              for (const arr of regArrays) {
                if (!Array.isArray(arr)) continue;
                for (const v of arr) if (Number.isFinite(v) && v > peak) peak = v;
              }
              return peak > 0 ? Math.ceil(peak * 1.12) : undefined;
            })(),
          },
          y1: {
            position: 'right', grid: { display: false },
            ticks: { color: BLUE, callback: (v) => '$' + v + 'K' },
            title: { display: true, text: 'Spend ($K)', color: BLUE },
            // Same tightening logic on the spend axis.
            suggestedMax: (() => {
              const spArrays = [sd.spendActual, sd.spendProj];
              let peak = 0;
              for (const arr of spArrays) {
                if (!Array.isArray(arr)) continue;
                for (const v of arr) {
                  if (Number.isFinite(v) && v > peak) peak = v;
                }
              }
              // spendActual / spendProj are fed in $ raw; canon-chart divides
              // by 1000 for display. Mirror that here before padding.
              return peak > 0 ? Math.ceil((peak / 1000) * 1.12) : undefined;
            })(),
          },
        },
      },
    });
  }

  function renderCanonChart(canvasOrId, opts) {
    const ctx = typeof canvasOrId === 'string'
      ? document.getElementById(canvasOrId) : canvasOrId;
    if (!ctx) { console.warn('[canon-chart] canvas not found'); return null; }
    if (opts.chartInstance) opts.chartInstance.destroy();

    // Route scenario mode out to its own builder — keeps the tracker/calibration
    // path clean and lets the Projection Engine carry its own dataset shape.
    if (opts.mode === 'scenario') return renderScenarioChart(ctx, opts);

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
          // Tracker/calibration modes don't use end-labels — suppress the
          // datalabels plugin so it doesn't paint noise on every point when
          // the global plugin script is loaded by the Projection Engine HTML.
          datalabels: { display: false },
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
