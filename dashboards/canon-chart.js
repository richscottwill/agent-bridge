/**
 * canon-chart.js — Single source of truth for the PS performance chart.
 *
 * Three render modes:
 *   - default:     "one glance" chart (actuals + latest prediction, continuous line)
 *   - calibration: "how did the model do?" line chart (adds first prediction overlay)
 *   - error:       "how wrong were we per week?" bar chart
 *                  Signed percentage error with muted traffic-light fills and
 *                  a CI reference band. Visually distinct from the trend chart
 *                  (bars, signed axis, severity coloring). See buildErrorDatasets.
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

  // Shared x-axis config: vertical grid lines only at the start of each month
  // (12 per year on a full-year chart). Labels still drawn every 2 weeks so
  // the x-axis reads cleanly. Computed live from the current year so the
  // mapping stays correct as time rolls forward.
  //
  // Week → month rule: month of the Thursday of the ISO week (standard ISO
  // week convention — each ISO week has exactly one Thursday, and that day
  // determines the week's calendar year). A "month start" week is the first
  // ISO week whose Thursday lands in a given month.

  // Map week number → 0-indexed month, for the current year. The first ISO
  // week whose Thursday lands in month M becomes the "start" of month M.
  // Cached on first call; recomputed once per year on rollover.
  const _monthStartCache = { year: null, weekToMonth: null };
  function weekToMonthMap() {
    const yr = new Date().getFullYear();
    if (_monthStartCache.year === yr) return _monthStartCache.weekToMonth;
    const map = new Map();
    let lastMonth = -1;
    for (let w = 1; w <= 53; w++) {
      const jan4 = new Date(Date.UTC(yr, 0, 4));
      const jan4Dow = jan4.getUTCDay() || 7; // Mon=1..Sun=7
      const week1Mon = new Date(jan4);
      week1Mon.setUTCDate(jan4.getUTCDate() - (jan4Dow - 1));
      const thu = new Date(week1Mon);
      thu.setUTCDate(week1Mon.getUTCDate() + (w - 1) * 7 + 3);
      if (thu.getUTCFullYear() !== yr) break;
      const m = thu.getUTCMonth();
      if (m !== lastMonth) { map.set(w, m); lastMonth = m; }
    }
    _monthStartCache.year = yr;
    _monthStartCache.weekToMonth = map;
    return map;
  }
  const MONTH_ABBR = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];

  // Pull the original label for a tick/index even if the ticks.callback blanked
  // the rendered version.
  function labelAtIndex(chart, idx) {
    const labels = chart && chart.data && chart.data.labels;
    if (Array.isArray(labels) && idx != null && labels[idx] != null) return String(labels[idx]);
    return '';
  }

  // Chart.js plugin: paints the month abbreviation just inside the top edge
  // of the chart area, horizontally centered on each month-start gridline.
  // Wired into chart options via `plugins: [monthLabelPlugin]` so it only
  // applies to the charts that want it (default/calibration + scenario).
  const monthLabelPlugin = {
    id: 'monthLabels',
    afterDatasetsDraw(chart) {
      const xScale = chart.scales && chart.scales.x;
      if (!xScale) return;
      const area = chart.chartArea;
      const ctx = chart.ctx;
      const map = weekToMonthMap();
      const labels = (chart.data && chart.data.labels) || [];
      if (!labels.length) return;
      ctx.save();
      ctx.font = '10px -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif';
      ctx.fillStyle = '#666';
      ctx.textAlign = 'left';
      ctx.textBaseline = 'top';
      for (let i = 0; i < labels.length; i++) {
        const m = String(labels[i]).match(/^W(\d{1,2})$/);
        if (!m) continue;
        const wkNum = parseInt(m[1], 10);
        if (!map.has(wkNum)) continue;
        const monthIdx = map.get(wkNum);
        const x = xScale.getPixelForValue(i);
        // Only paint labels whose gridline is actually inside the chart area
        if (x < area.left - 1 || x > area.right + 1) continue;
        // Paint just above the chart area (in the layout.padding.top band)
        ctx.fillText(MONTH_ABBR[monthIdx], x + 3, area.top - 12);
      }
      ctx.restore();
    },
  };

  function monthlyGridXAxis() {
    const GRID_COLOR = '#1f222b';
    const monthWeeks = () => weekToMonthMap(); // alias

    const isMonthStart = (ctx) => {
      const chart = ctx && ctx.chart;
      const idx = ctx && (ctx.index != null ? ctx.index : ctx.tick && ctx.tick.value);
      const lbl = labelAtIndex(chart, idx);
      const m = lbl.match(/^W(\d{1,2})$/);
      if (m) return monthWeeks().has(parseInt(m[1], 10));
      // Fallback for non-week labels: every other tick
      return typeof idx === 'number' && idx % 2 === 0;
    };

    // Labels: keep existing every-2-ticks cadence for readability
    const labelShown = (idx) => idx === 0 || idx % 2 === 0;

    return {
      grid: {
        color: (ctx) => isMonthStart(ctx) ? GRID_COLOR : 'transparent',
      },
      ticks: {
        color: '#666', font: { size: 10 },
        autoSkip: false, maxRotation: 0,
        callback: function (val, idx) {
          return labelShown(idx) ? this.getLabelForValue(val) : '';
        },
      },
    };
  }

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

  function buildDefaultDatasets(s, axisFilter) {
    // WR-F1 (2026-04-29): axisFilter parity with calibration. Lets
    // "What happened" collapse to regs-only or spend-only when the
    // user doesn't want both axes on one chart.
    const axis = axisFilter === 'spend' || axisFilter === 'regs' || axisFilter === 'both' ? axisFilter : 'both';
    const sets = [];
    // CI band (regs, future only) — renders first so actuals/preds sit on top.
    // Always included when regs axis is on so the uncertainty envelope
    // is visible even if spend is off.
    if (axis === 'regs' || axis === 'both') {
      sets.push({
        label: '_ciHi', data: s.ciHiFuture,
        borderColor: 'transparent', backgroundColor: ORANGE_SOFT,
        borderWidth: 0, pointRadius: 0, fill: '+1', tension: 0.25,
        yAxisID: 'y', spanGaps: true, _hidden: true,
      });
      sets.push({
        label: '_ciLo', data: s.ciLoFuture,
        borderColor: 'transparent', backgroundColor: ORANGE_SOFT,
        borderWidth: 0, pointRadius: 0, fill: false, tension: 0.25,
        yAxisID: 'y', spanGaps: true, _hidden: true,
      });
    }
    // OP2 target — regs-axis only, so hidden when axis === 'spend'.
    if (axis === 'regs' || axis === 'both') {
      sets.push({
        label: 'OP2 target', data: s.op2Regs,
        borderColor: GRAY, backgroundColor: 'transparent',
        borderWidth: 1.5, borderDash: [3, 3], pointRadius: 0, tension: 0,
        yAxisID: 'y', spanGaps: true,
      });
    }
    if (axis === 'regs' || axis === 'both') {
      // Regs actual (solid orange, past only)
      sets.push({
        label: 'Regs (actual)', data: s.regsActual,
        borderColor: ORANGE, backgroundColor: ORANGE,
        borderWidth: 2.5, pointRadius: 3, pointBackgroundColor: ORANGE,
        tension: 0.25, yAxisID: 'y', spanGaps: false,
      });
      // Regs latest pred (dashed orange, future only; anchored at maxWk actual)
      sets.push({
        label: 'Regs (predicted)', data: s.regsLatestFuture,
        borderColor: ORANGE, backgroundColor: 'transparent',
        borderWidth: 2, borderDash: [6, 4], pointRadius: 0, tension: 0.25,
        yAxisID: 'y', spanGaps: true,
      });
    }
    if (axis === 'spend' || axis === 'both') {
      // Spend actual (solid blue)
      sets.push({
        label: 'Spend (actual, $K)', data: s.spendActual,
        borderColor: BLUE, backgroundColor: BLUE,
        borderWidth: 2.5, pointRadius: 3, pointBackgroundColor: BLUE,
        tension: 0.25, yAxisID: 'y1', spanGaps: false,
      });
      // Spend latest pred (dashed blue)
      sets.push({
        label: 'Spend (predicted, $K)', data: s.spendLatestFuture,
        borderColor: BLUE, backgroundColor: 'transparent',
        borderWidth: 2, borderDash: [6, 4], pointRadius: 0, tension: 0.25,
        yAxisID: 'y1', spanGaps: true,
      });
    }
    return sets;
  }

  function buildCalibrationDatasets(s, axisFilter) {
    // WR-D2 (2026-04-28): optional axisFilter = 'regs' | 'spend' | 'both'.
    // Default calibration view on weekly-review used 7+ visible lines which
    // exceeded the 3-line budget — filter lets the panel default to regs-only
    // and the user opt into spend-only or both via the panel's axis toggle.
    const axis = axisFilter === 'spend' || axisFilter === 'both' || axisFilter === 'regs' ? axisFilter : 'both';
    // Calibration view shows predictions at ALL weeks (not just future), so
    // the viewer can see actual vs each-of-two-predictions side by side.
    const sets = [];
    // CI band always present — uncertainty envelope is part of the grade.
    sets.push({
      label: '_ciHi', data: s.ciHiAll,
      borderColor: 'transparent', backgroundColor: ORANGE_SOFT,
      borderWidth: 0, pointRadius: 0, fill: '+1', tension: 0.25,
      yAxisID: 'y', spanGaps: true, _hidden: true,
    });
    sets.push({
      label: '_ciLo', data: s.ciLoAll,
      borderColor: 'transparent', backgroundColor: ORANGE_SOFT,
      borderWidth: 0, pointRadius: 0, fill: false, tension: 0.25,
      yAxisID: 'y', spanGaps: true, _hidden: true,
    });
    // OP2 always present.
    sets.push({
      label: 'OP2 target', data: s.op2Regs,
      borderColor: GRAY, backgroundColor: 'transparent',
      borderWidth: 1.5, borderDash: [3, 3], pointRadius: 0, tension: 0,
      yAxisID: 'y', spanGaps: true,
    });
    if (axis === 'regs' || axis === 'both') {
      sets.push({
        label: 'Regs (actual)', data: s.regsActual,
        borderColor: ORANGE, backgroundColor: ORANGE,
        borderWidth: 2.5, pointRadius: 3, pointBackgroundColor: ORANGE,
        tension: 0.25, yAxisID: 'y', spanGaps: false,
      });
      sets.push({
        label: 'Regs (first pred)', data: s.regsFirst,
        borderColor: ORANGE, backgroundColor: 'transparent',
        // WR-F1 (2026-04-29): first-pred now matches the default chart's
        // prediction line exactly — dashed orange, no markers.
        borderWidth: 1.5, borderDash: [2, 3],
        pointRadius: 0, tension: 0.25,
        yAxisID: 'y', spanGaps: true,
      });
      sets.push({
        label: 'Regs (latest pred)', data: s.regsLatestAll,
        borderColor: ORANGE, backgroundColor: 'transparent',
        borderWidth: 2, borderDash: [6, 4], pointRadius: 0, tension: 0.25,
        yAxisID: 'y', spanGaps: true,
      });
    }
    if (axis === 'spend' || axis === 'both') {
      sets.push({
        label: 'Spend (actual, $K)', data: s.spendActual,
        borderColor: BLUE, backgroundColor: BLUE,
        borderWidth: 2.5, pointRadius: 3, pointBackgroundColor: BLUE,
        tension: 0.25, yAxisID: 'y1', spanGaps: false,
      });
      sets.push({
        label: 'Spend (first pred, $K)', data: s.spendFirst,
        borderColor: BLUE, backgroundColor: 'transparent',
        borderWidth: 1.5, borderDash: [2, 3],
        pointRadius: 0, tension: 0.25,
        yAxisID: 'y1', spanGaps: true,
      });
      sets.push(s.spendLatestSet || {
        label: 'Spend (latest pred, $K)', data: s.spendLatestAll,
        borderColor: BLUE, backgroundColor: 'transparent',
        borderWidth: 2, borderDash: [6, 4], pointRadius: 0, tension: 0.25,
        yAxisID: 'y1', spanGaps: true,
      });
    }
    return sets;
  }

  // ========================================================================
  // Error-bar mode — "how wrong were we per week?"
  //
  // Signed error bars (one per week) with muted traffic-light severity fills.
  // Signed = below zero is under-prediction, above is over-prediction.
  // Severity by |err|: <5% soft green, 5-15% soft amber, >=15% soft red.
  // Future weeks (no actual yet) render as null — Chart.js draws no bar,
  // but the x-slot remains present so the axis stays stable across 1-52.
  //
  // Derives a reference band from the median latest CI half-width across
  // weeks with actuals. Drawn as a soft green horizontal band (see the
  // referenceBandPlugin in renderCanonChart). A bar that extends beyond
  // the band is outside the model's own claimed precision.
  //
  // axisFilter: 'regs' | 'spend' | 'both'. For 'both' we render two bar
  // datasets side-by-side; single-axis views render one dataset on the
  // left scale (percentages work the same for regs and spend).
  // ========================================================================
  function buildErrorDatasets(s, axisFilter) {
    const axis = axisFilter === 'spend' || axisFilter === 'both' || axisFilter === 'regs'
      ? axisFilter : 'regs';

    // Muted traffic-light palette — projection-design-system.css tokens with
    // low alpha on the fill and higher alpha on the border for a restrained
    // but legible signal. Matches the heatgrid / trust-badge language already
    // used on the projection engine.
    const GOOD_FILL = 'rgba(20, 165, 72, 0.35)';
    const GOOD_EDGE = 'rgba(20, 165, 72, 0.75)';
    const WARN_FILL = 'rgba(232, 168, 0, 0.35)';
    const WARN_EDGE = 'rgba(232, 168, 0, 0.85)';
    const BAD_FILL  = 'rgba(209, 50, 18, 0.35)';
    const BAD_EDGE  = 'rgba(209, 50, 18, 0.80)';

    function fillFor(v) {
      if (v === null || v === undefined) return 'transparent';
      const a = Math.abs(v);
      if (a < 5) return GOOD_FILL;
      if (a < 15) return WARN_FILL;
      return BAD_FILL;
    }
    function edgeFor(v) {
      if (v === null || v === undefined) return 'transparent';
      const a = Math.abs(v);
      if (a < 5) return GOOD_EDGE;
      if (a < 15) return WARN_EDGE;
      return BAD_EDGE;
    }

    // Compute signed error % per week. Sign convention matches the scorecard:
    // negative = under-predicting (pred below actual), positive = over.
    // Skip weeks with no actual or no latest prediction.
    function errPctArray(actuals, latestPreds) {
      const out = new Array(52).fill(null);
      for (let i = 0; i < 52; i++) {
        const a = actuals[i]; const p = latestPreds[i];
        if (a === null || a === 0 || p === null) continue;
        out[i] = Math.round((p - a) / a * 10000) / 100;
      }
      return out;
    }

    const sets = [];

    if (axis === 'regs' || axis === 'both') {
      const regsErrs = errPctArray(s.regsActual, s.regsLatestAll);
      sets.push({
        label: 'Regs error %',
        data: regsErrs,
        backgroundColor: regsErrs.map(fillFor),
        borderColor: regsErrs.map(edgeFor),
        borderWidth: 1,
        borderRadius: 2,
        yAxisID: 'y',
        _errMetric: 'regs',
        barPercentage: 0.9, categoryPercentage: axis === 'both' ? 0.9 : 0.95,
      });
    }
    if (axis === 'spend' || axis === 'both') {
      const spendErrs = errPctArray(s.spendActual, s.spendLatestAll);
      sets.push({
        label: 'Spend error %',
        data: spendErrs,
        backgroundColor: spendErrs.map(fillFor),
        borderColor: spendErrs.map(edgeFor),
        borderWidth: 1,
        borderRadius: 2,
        yAxisID: 'y',
        _errMetric: 'spend',
        barPercentage: 0.9, categoryPercentage: axis === 'both' ? 0.9 : 0.95,
      });
    }

    // Stash derived metadata for the plugins + tooltip.
    sets._meta = {
      ciBandPct: medianCiHalfWidthPct(s),
      regsActual: s.regsActual,
      regsLatestAll: s.regsLatestAll,
      spendActual: s.spendActual,
      spendLatestAll: s.spendLatestAll,
      ciLoAll: s.ciLoAll,
      ciHiAll: s.ciHiAll,
    };
    return sets;
  }

  // Compute the median half-width of the latest CI, expressed as % of the
  // latest prediction. This is the model's own stated precision; we draw a
  // reference band at ±this number on the error chart. Only regs CIs are
  // present in forecast-data.json so we key off those.
  function medianCiHalfWidthPct(s) {
    const halves = [];
    for (let i = 0; i < 52; i++) {
      const lo = s.ciLoAll[i]; const hi = s.ciHiAll[i]; const pred = s.regsLatestAll[i];
      if (lo === null || hi === null || pred === null || pred === 0) continue;
      const half = (hi - lo) / 2;
      halves.push(half / pred * 100);
    }
    if (!halves.length) return 20;  // sensible fallback
    halves.sort((a, b) => a - b);
    const mid = Math.floor(halves.length / 2);
    const med = halves.length % 2 ? halves[mid] : (halves[mid - 1] + halves[mid]) / 2;
    return Math.round(med * 10) / 10;
  }
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
  //     compareTotal:    number[]   // saved-projection total regs overlay (optional, P2-12)
  //     compareLabel:    string     // legend label for compare line (optional)
  //     todayIdx:        number     // index of the YTD/projected seam
  //     targetRegs:      number     // horizontal target line (optional, per-week)
  //     regimes:         [{ label, onsetIdx, endIdx, absorbed }]
  //     periodHighlight: { startIdx, endIdx }  // optional
  //     tooltipFormatter:(ctx, idx) => string  // custom HTML for narrated tooltip
  //   }
  // ========================================================================

  function buildScenarioDatasets(sd) {
    const datasets = [];

    // M9 fan chart (2026-04-30): three overlapping CI fills for BoE-style
    // progression — 90% (outermost, lightest), 80%, 50% (innermost, darkest).
    // Each fill is a pair of transparent lines with fill: '+1' between them.
    // Falls back to single-band path when sd.ciFanBands is absent or empty.
    //
    // Render order: widest first so narrower bands paint on top. All fills
    // share the same orange hue; alpha steps encode concentration.
    const fanBands = sd.ciFanBands;
    const hasFan = fanBands
      && fanBands['50'] && fanBands['50'].low && fanBands['50'].low.some(v => v != null)
      && fanBands['80'] && fanBands['80'].low && fanBands['80'].low.some(v => v != null)
      && fanBands['90'] && fanBands['90'].low && fanBands['90'].low.some(v => v != null);

    if (hasFan) {
      // Three bands, widest → narrowest so narrower paints on top.
      // Alpha stops chosen so stacked visual weight roughly matches BoE
      // convention (50% dense, 90% sparse). Hex: ORANGE_SOFT palette with
      // varied opacity.
      const fanFills = {
        '90': 'rgba(244, 162, 97, 0.10)',
        '80': 'rgba(244, 162, 97, 0.16)',
        '50': 'rgba(244, 162, 97, 0.26)',
      };
      for (const lvl of ['90', '80', '50']) {
        const b = fanBands[lvl];
        if (!b || !b.low || !b.high) continue;
        datasets.push({
          label: `_fanHi${lvl}`, data: b.high,
          borderColor: 'transparent', backgroundColor: fanFills[lvl],
          borderWidth: 0, pointRadius: 0, fill: '+1', tension: 0.25,
          yAxisID: 'y', spanGaps: true, _hidden: true,
          _fanLevel: lvl,
        });
        datasets.push({
          label: `_fanLo${lvl}`, data: b.low,
          borderColor: 'transparent', backgroundColor: fanFills[lvl],
          borderWidth: 0, pointRadius: 0, fill: false, tension: 0.25,
          yAxisID: 'y', spanGaps: true, _hidden: true,
          _fanLevel: lvl,
        });
      }
    } else if (sd.ciHigh && sd.ciLow) {
      // Legacy single-band fallback — preserved verbatim for charts that
      // haven't migrated to the three-band shape yet.
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

    // Compare line — dashed brand-blue total-regs overlay of a saved
    // projection (P2-12 chart-side follow-up, 2026-04-28). Shown ON by
    // default when a compare is active: the affordance to start the
    // compare is the "Compare" button in the Saved list, so the user
    // already opted in. Label includes the saved label so multiple
    // comparisons could be layered if we ever extend beyond one.
    if (sd.compareTotal) {
      datasets.push({
        label: sd.compareLabel || 'Saved projection (compare)',
        data: sd.compareTotal,
        borderColor: BLUE, backgroundColor: 'transparent',
        borderWidth: 2, borderDash: [5, 4], pointRadius: 0, tension: 0.25,
        yAxisID: 'y', spanGaps: true,
      });
    }

    // Actuals / Total — a single thin summary line across the full year
    // that sits on top of the Brand/NB stacked area. Past weeks = actuals
    // total (Brand + NB from ytd_weekly); projected weeks = forecast total.
    // This is the authoritative "what's happening" line; the stack below
    // shows the composition. Point markers only on the actuals half so the
    // eye reads "solid dots = real, empty dashed = forecast".
    datasets.push({
      label: 'Total registrations', data: sd.regsProjTotal || [],
      borderColor: '#1A1A1A', backgroundColor: '#1A1A1A',
      borderWidth: 2, pointRadius: 0,
      segment: {
        borderDash: (ctx) => {
          // Dashed in the projected half, solid in the actuals half.
          const todayIdx = sd.todayIdx == null ? -1 : sd.todayIdx;
          return ctx.p0DataIndex >= todayIdx ? [6, 4] : undefined;
        },
      },
      tension: 0.25, yAxisID: 'y', spanGaps: true,
    });

    // #95 (2026-05-01): curve-fit overlay on the actuals half. Centered
    // 5-week moving average renders a smoothed trend line behind the raw
    // totals — chart becomes readable at a glance without hiding the raw
    // points (which remain visible on the Total registrations line above).
    // Vercel Analytics 2022 "curve fitting for charts" / FT Chart Doctor
    // smoothing guidance — we use MA-5 rather than polynomial fit because
    // MA is robust to end-effects and has no train/test overhead.
    if (sd.regsProjTotal && sd.todayIdx != null && sd.todayIdx > 4) {
      const smoothed = new Array(sd.regsProjTotal.length).fill(null);
      const W = 2;  // ±2 weeks = 5-week centered window
      for (let i = 0; i < sd.todayIdx; i++) {
        let sum = 0, cnt = 0;
        for (let j = Math.max(0, i - W); j <= Math.min(sd.todayIdx - 1, i + W); j++) {
          const v = sd.regsProjTotal[j];
          if (Number.isFinite(v)) { sum += v; cnt++; }
        }
        if (cnt > 0) smoothed[i] = sum / cnt;
      }
      datasets.push({
        label: '_trendSmooth',  // _ prefix hides from legend per existing filter convention
        data: smoothed,
        borderColor: 'rgba(26, 26, 26, 0.28)',
        backgroundColor: 'transparent',
        borderWidth: 1.5, pointRadius: 0,
        tension: 0.45,
        yAxisID: 'y', spanGaps: true,
      });
    }

    // Projected — STACKED AREA for Brand + NB so the chart reads as
    // "here's what we expect, and here's how Brand / NB split it." Brand
    // on the bottom, NB on top. Fills are solid enough to convey weight
    // (0.55 alpha) but still let the Today line + CI band show through.
    //
    // Implementation: we compute the stacked values (brand = raw, nb = brand + nb)
    // in projection-chart.js so Chart.js's own stacking engine is not
    // involved — that engine forces every dataset on the y-axis to stack,
    // which would break the Actuals line and the CI band (which must
    // render at literal values). NB area fills DOWN to the Brand line
    // via `fill: '-1'`; Brand fills DOWN to origin.
    if (sd.regsProjBrandStacked) {
      datasets.push({
        label: 'Brand forecast', data: sd.regsProjBrandStacked,
        borderColor: BLUE, backgroundColor: 'rgba(0, 102, 204, 0.55)',
        borderWidth: 0, pointRadius: 0, tension: 0.25,
        yAxisID: 'y', spanGaps: true,
        fill: { target: 'origin' },
      });
    }
    if (sd.regsProjNbStacked) {
      datasets.push({
        label: 'Non-Brand forecast', data: sd.regsProjNbStacked,
        borderColor: '#FF9900', backgroundColor: 'rgba(255, 153, 0, 0.55)',
        borderWidth: 0, pointRadius: 0, tension: 0.25,
        yAxisID: 'y', spanGaps: true,
        fill: { target: '-1' },
      });
    }
    // (The previous 'Total (Brand + NB)' dataset was replaced by the single
    // 'Total registrations' line above that spans both halves of the chart.)

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
      plugins: [monthLabelPlugin],
      options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: { mode: 'index', intersect: false, axis: 'x' },
        // P2-08: register datalabels only on scenario mode. Plugin labels
        // the last non-null point on each visible line with series name +
        // value so the user reads the chart left-to-right and lands on the
        // series identity without chasing the legend.
        layout: { padding: { right: 80, top: 14 } },  // breathing room for end labels + month band
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
            // Native Chart.js tooltip carries both the numeric series and the
            // narrated contribution as extra afterBody lines. This follows
            // the weekly-review.html pattern — Chart.js manages show/hide
            // entirely, no external div lifecycle to track, no mouseleave
            // edge cases. The prior external-div approach stayed pinned
            // when the cursor exited empty canvas space because Chart.js
            // didn't call the external handler in that mouseleave path.
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
              // Narrated contribution breakdown appended via afterBody so
              // Chart.js can wrap it properly and dismiss it with the rest
              // of the tooltip. Caller supplies tooltipFormatter which
              // returns HTML; we flatten that to plain-text lines here
              // because Chart.js tooltips are text-based.
              afterBody: typeof sd.tooltipFormatter === 'function'
                ? (items) => {
                    if (!items || !items.length) return null;
                    const idx = items[0].dataIndex;
                    if (idx == null || idx < 0) return null;
                    // tooltipFormatter returns HTML (<div>...), convert to plain lines
                    const html = sd.tooltipFormatter({ chart: items[0].chart }, idx) || '';
                    // Strip tags, split on remaining newlines, trim, drop empties.
                    const text = html
                      .replace(/<[^>]+>/g, '\n')
                      .split('\n')
                      .map(s => s.trim())
                      .filter(s => s.length > 0);
                    return text;
                  }
                : undefined,
            },
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
          x: monthlyGridXAxis(),
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

  // ========================================================================
  // Error bar chart renderer — "how wrong were we per week?"
  //
  // Signed %-error axis. Muted traffic-light fills. A soft green reference
  // band at ±(median latest CI half-width). A visible zero reference line.
  // All 52 weeks rendered; weeks without actuals are null (no bar drawn),
  // keeping the x-axis stable across markets and across the year.
  //
  // Expected opts: forecastData, market, axisFilter ('regs'|'spend'|'both')
  // ========================================================================
  function renderErrorChart(ctx, opts) {
    const s = buildSeries(opts.forecastData, opts.market);
    const datasets = buildErrorDatasets(s, opts.axisFilter);
    const meta = datasets._meta || {};
    const ciBandPct = meta.ciBandPct || 20;

    // Reference band plugin — draws a soft green ±ciBandPct horizontal band.
    // The band is the model's OWN claimed precision, derived from its CI
    // outputs. Bars that extend past the band are outside the model's own
    // stated confidence — not our complaint, the model's.
    const referenceBandPlugin = {
      id: 'errorReferenceBand',
      beforeDatasetsDraw(chart) {
        const y = chart.scales.y; const area = chart.chartArea;
        if (!y || !area) return;
        const yHi = y.getPixelForValue(ciBandPct);
        const yLo = y.getPixelForValue(-ciBandPct);
        chart.ctx.save();
        chart.ctx.fillStyle = 'rgba(20, 165, 72, 0.06)';
        chart.ctx.fillRect(area.left, Math.min(yHi, yLo), area.right - area.left, Math.abs(yLo - yHi));
        chart.ctx.strokeStyle = 'rgba(20, 165, 72, 0.35)';
        chart.ctx.setLineDash([4, 3]);
        chart.ctx.lineWidth = 1;
        chart.ctx.beginPath();
        chart.ctx.moveTo(area.left, yHi); chart.ctx.lineTo(area.right, yHi);
        chart.ctx.moveTo(area.left, yLo); chart.ctx.lineTo(area.right, yLo);
        chart.ctx.stroke();
        chart.ctx.restore();
      },
    };

    // Zero reference line — heavier than grid so sign of error reads instantly.
    const zeroLinePlugin = {
      id: 'errorZeroLine',
      afterDatasetsDraw(chart) {
        const y = chart.scales.y; const area = chart.chartArea;
        if (!y || !area) return;
        const y0 = y.getPixelForValue(0);
        chart.ctx.save();
        chart.ctx.strokeStyle = 'rgba(60, 60, 60, 0.6)';
        chart.ctx.lineWidth = 1;
        chart.ctx.beginPath();
        chart.ctx.moveTo(area.left, y0); chart.ctx.lineTo(area.right, y0);
        chart.ctx.stroke();
        chart.ctx.restore();
      },
    };

    const chart = new Chart(ctx, {
      type: 'bar',
      data: { labels: s.labels, datasets: datasets },
      plugins: [referenceBandPlugin, zeroLinePlugin],
      options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: { mode: 'index', intersect: false, axis: 'x' },
        plugins: {
          legend: { display: false },
          tooltip: {
            mode: 'index',
            intersect: false,
            callbacks: {
              title: (items) => items.length ? items[0].label : '',
              label: (item) => {
                const v = item.parsed.y;
                if (v == null) return 'no actual yet';
                const ds = item.dataset;
                const metric = ds._errMetric === 'spend' ? 'spend' : 'regs';
                const actual = metric === 'spend'
                  ? meta.spendActual[item.dataIndex] : meta.regsActual[item.dataIndex];
                const latest = metric === 'spend'
                  ? meta.spendLatestAll[item.dataIndex] : meta.regsLatestAll[item.dataIndex];
                const dir = v < 0 ? 'under' : 'over';
                const sign = v > 0 ? '+' : '';
                const unit = metric === 'spend' ? '$K' : '';
                const lines = [
                  (ds.label || 'error') + ': ' + sign + v + '% (' + dir + ')',
                ];
                if (actual != null) {
                  lines.push('actual: ' + Math.round(actual).toLocaleString() + unit);
                }
                if (latest != null) {
                  lines.push('latest pred: ' + Math.round(latest).toLocaleString() + unit);
                }
                // CI in-band signal (regs-only — CIs aren't present for spend)
                if (metric === 'regs' && meta.ciLoAll && meta.ciHiAll && actual != null) {
                  const lo = meta.ciLoAll[item.dataIndex];
                  const hi = meta.ciHiAll[item.dataIndex];
                  if (lo != null && hi != null) {
                    lines.push(lo <= actual && actual <= hi ? 'inside CI band' : 'outside CI band');
                  }
                }
                return lines;
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
          datalabels: { display: false },
        },
        scales: {
          x: {
            grid: { display: false },
            ticks: {
              color: '#666', font: { size: 10 },
              autoSkip: false,
              callback: function (val) {
                const lbl = this.getLabelForValue(val);
                const n = parseInt(lbl.replace('W', ''), 10);
                return (n % 2 === 0 || n === 1 || n === 52) ? lbl : '';
              },
            },
          },
          y: {
            position: 'left',
            suggestedMin: -50, suggestedMax: 50,
            grid: {
              color: (c) => (c.tick && c.tick.value === 0) ? 'transparent' : '#1f222b',
            },
            ticks: {
              color: '#666',
              callback: (v) => (v > 0 ? '+' : '') + v + '%',
            },
            title: { display: true, text: 'Forecast error (% of actual)', color: '#888' },
          },
        },
      },
    });

    // Highlight selected week — slightly thicker border on the matching bar.
    if (opts.highlightWeek) {
      const targetWk = parseInt(String(opts.highlightWeek).replace('W', ''), 10);
      if (!isNaN(targetWk)) {
        const idx = targetWk - 1;
        chart.data.datasets.forEach((ds) => {
          if (Array.isArray(ds.borderWidth)) return;
          ds.borderWidth = ds.data.map((_, i) => (i === idx ? 2.5 : 1));
        });
        chart.update();
      }
    }

    return chart;
  }

  function renderCanonChart(canvasOrId, opts) {
    const ctx = typeof canvasOrId === 'string'
      ? document.getElementById(canvasOrId) : canvasOrId;
    if (!ctx) { console.warn('[canon-chart] canvas not found'); return null; }
    if (opts.chartInstance) opts.chartInstance.destroy();

    // Route scenario mode out to its own builder — keeps the tracker/calibration
    // path clean and lets the Projection Engine carry its own dataset shape.
    if (opts.mode === 'scenario') return renderScenarioChart(ctx, opts);

    // Error mode is a bar chart with signed-%-axis and severity-colored bars.
    // Visually distinct from the line-chart modes so viewers don't confuse
    // "what happened" with "how wrong were we." See renderErrorChart.
    if (opts.mode === 'error') return renderErrorChart(ctx, opts);

    const mode = opts.mode === 'calibration' ? 'calibration' : 'default';
    const s = buildSeries(opts.forecastData, opts.market);
    const datasets = mode === 'calibration'
      ? buildCalibrationDatasets(s, opts.axisFilter) : buildDefaultDatasets(s, opts.axisFilter);

    const chart = new Chart(ctx, {
      type: 'line',
      data: { labels: s.labels, datasets: datasets },
      plugins: [monthLabelPlugin],
      options: {
        responsive: true,
        maintainAspectRatio: false,
        // #5 (2026-05-01): room on the right for endpoint labels.
        layout: { padding: { top: 14, right: 96 } },
        interaction: { mode: 'index', intersect: false, axis: 'x' },
        plugins: {
          // #5 (2026-05-01): no legend — label series at their endpoint via
          // the datalabels plugin instead. Matches scenario-chart conventions
          // and the PE tracker grammar. Saves eye movement + 60px of footer.
          legend: { display: false },
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
            annotations: (function() {
              const anns = {
                nowLine: {
                  type: 'line',
                  xMin: s.maxWk - 1, xMax: s.maxWk - 1,
                  borderColor: NOW_GREEN, borderWidth: 2, borderDash: [4, 4],
                  label: {
                    display: true, content: '\u2193 Now (W' + s.maxWk + ')',
                    color: '#4ade80', font: { size: 10, weight: '600' }, position: 'start',
                    backgroundColor: 'rgba(0,0,0,0)',
                  },
                },
              };
              // #38 (2026-05-01): horizontal OP2-target line with endpoint
              // label on the right edge. Uses the median OP2 value across
              // the visible series as a single "on-plan" reference (the
              // op2 series already varies week by week; this marker lets
              // the reader read the trend against the baseline at a glance).
              const op2s = (s.op2Regs || []).filter(v => v != null && v > 0);
              if (op2s.length >= 4) {
                const sorted = op2s.slice().sort((a, b) => a - b);
                const median = sorted[Math.floor(sorted.length / 2)];
                anns.op2TargetLine = {
                  type: 'line',
                  yMin: median, yMax: median,
                  borderColor: '#6b7280', borderWidth: 1, borderDash: [2, 3],
                  label: {
                    display: true,
                    content: 'OP2 plan ' + Math.round(median).toLocaleString() + '/wk',
                    color: '#6b7280', font: { size: 10 }, position: 'end',
                    backgroundColor: 'rgba(0,0,0,0)',
                  },
                };
              }
              // WR-A8 (2026-04-30): event annotations passed by caller.
              // Each event has {id, weeks:[int], text, kind, important}.
              // Draw a dashed vertical at each week for the selected event,
              // with an abbreviated label. Skip weeks outside the chart
              // range (1..52). Kind drives color: shift=violet, streak=amber,
              // note=grey.
              const evs = Array.isArray(opts.eventAnnotations) ? opts.eventAnnotations : [];
              const KIND_COLOR = {
                shift:  'rgba(168, 85, 247, 0.85)',
                streak: 'rgba(212, 147, 26, 0.85)',
                note:   'rgba(128, 128, 128, 0.75)',
              };
              evs.forEach((ev, i) => {
                const color = KIND_COLOR[ev.kind] || KIND_COLOR.note;
                (ev.weeks || []).forEach((wk, j) => {
                  if (wk < 1 || wk > 52) return;
                  const xIdx = wk - 1;  // labels are 'W1'...'W52' 0-indexed
                  const key = `event-${ev.id || i}-${j}`;
                  anns[key] = {
                    type: 'line',
                    xMin: xIdx, xMax: xIdx,
                    borderColor: color,
                    borderWidth: ev.important ? 2 : 1,
                    borderDash: [2, 3],
                    drawTime: 'beforeDatasetsDraw',
                    label: (j === 0) ? {
                      display: true,
                      content: (ev.text || '').slice(0, 36).replace(/\s+$/, ''),
                      color: color,
                      font: { size: 9, weight: ev.important ? '600' : '400' },
                      position: 'start',
                      yAdjust: 12 + (i % 3) * 14,  // stagger labels vertically
                      backgroundColor: 'rgba(255,255,255,0.85)',
                      padding: { top: 1, bottom: 1, left: 3, right: 3 },
                    } : { display: false },
                  };
                });
              });
              return anns;
            })(),
          },
          // #5 (2026-05-01): endpoint labels on each visible line. Labels
          // the LAST non-null point of each dataset with the series name,
          // colored to match the line. Replaces the bottom legend. Skips
          // the CI band (_-prefixed) and the OP2 target (has its own annotation).
          datalabels: {
            display: function(ctx) {
              const ds = ctx.dataset;
              if (!ds || !ds.label) return false;
              if (ds.label.startsWith('_')) return false;  // CI bands
              if (ds.label === 'OP2 target') return false;  // has annotation label
              // last non-null point only
              const data = ds.data;
              for (let i = data.length - 1; i >= 0; i--) {
                if (data[i] != null) return i === ctx.dataIndex;
              }
              return false;
            },
            anchor: 'end',
            align: 'right',
            offset: 8,
            color: function(ctx) {
              return ctx.dataset.borderColor || '#888';
            },
            font: { size: 10, weight: '600' },
            formatter: function(value, ctx) {
              // Strip trailing "($K)" / "(actual)" / "(predicted)" chrome
              // so the label reads as the concept, not the data shape.
              const raw = ctx.dataset.label || '';
              return raw
                .replace(/\s*\(actual(?:,\s*\$K)?\)\s*$/i, '')
                .replace(/\s*\(predicted(?:,\s*\$K)?\)\s*$/i, ' (pred)')
                .replace(/\s+forecast$/i, ' (fcst)');
            },
          },
        },
        scales: {
          x: monthlyGridXAxis(),
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
