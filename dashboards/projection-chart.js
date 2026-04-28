/**
 * projection-chart.js — Projection Engine chart (M3).
 *
 * Replaces the Observable Plot implementation that was in projection-app.js
 * (lines 1072-1828 across renderChart + attachNarratedTooltips + ensureTooltip +
 * showTooltip + hideTooltip + applyArrivalAnimations + annotateActiveRegimes
 * + renderNarratedTooltip). Those 750+ lines are gone. This file is ~200.
 *
 * Delegates all rendering to CanonChart.render({ mode: 'scenario' }) in
 * canon-chart.js. The only thing this file owns is the adapter from
 * projection-app's data shape (`out`, `counterfactual`, `uncert`, `marketData`)
 * to the `scenarioData` shape the scenario mode expects.
 *
 * Narrated-contribution tooltip is preserved via the `tooltipFormatter`
 * callback — users still get the "40% seasonal · 40% trend · 15% lift · 5%
 * qualitative" narration on hover, now backed by Chart.js instead of a
 * custom SVG overlay.
 */
(function (global) {
  'use strict';

  // Compute an ISO week number for a date (matches mpe_engine's convention)
  function computeIsoWeekNum(d) {
    const t = new Date(Date.UTC(d.getFullYear(), d.getMonth(), d.getDate()));
    const day = t.getUTCDay() || 7;
    t.setUTCDate(t.getUTCDate() + 4 - day);
    const yearStart = new Date(Date.UTC(t.getUTCFullYear(), 0, 1));
    return Math.ceil((((t - yearStart) / 86400000) + 1) / 7);
  }

  // Read the current period code from the dropdown (e.g. W17, M04, Q2, Y2026,
  // MY1, MY2). Returns null when the dropdown is absent or the selected value
  // is blank. P2-02 uses this to clip the chart x-domain to the period.
  function getCurrentPeriod() {
    const el = typeof document !== 'undefined' && document.getElementById('period-select');
    return el ? (el.value || '').toUpperCase() : '';
  }

  // Map a period code to an {startIdx, endIdx} window over btWeeks so the
  // chart zooms to the period instead of always rendering the full year.
  // Returns null (= full-year span) when the period is Y2026 or unrecognized.
  //
  // The contract follows what the projection solver already supports:
  //   W17        → roughly 4-week window centered on week 17
  //   M04        → all weeks whose start date falls in month 04
  //   Q2         → weeks in months 04-06
  //   Y2026      → full year (null = no clip)
  //   MY1 / MY2  → 52 / 104 week lookback from ytd_latest (Y2026 + prior year)
  //
  // Anything else returns null so the chart degrades gracefully.
  function periodWindowOverBtWeeks(periodCode, btWeeks, ytdCount) {
    if (!periodCode || periodCode === 'Y2026' || periodCode === 'Y' || !btWeeks || !btWeeks.length) {
      return null;
    }
    const n = btWeeks.length;
    const today = ytdCount > 0 ? btWeeks[ytdCount - 1] : btWeeks[0];
    // Weekly period (Wnn) — ±2 week window around the target week
    const wMatch = periodCode.match(/^W(\d{1,2})$/);
    if (wMatch) {
      const target = parseInt(wMatch[1], 10);
      let centerIdx = -1;
      for (let i = 0; i < n; i++) {
        if (computeIsoWeekNum(btWeeks[i]) === target) { centerIdx = i; break; }
      }
      if (centerIdx < 0) return null;
      return { startIdx: Math.max(0, centerIdx - 2), endIdx: Math.min(n - 1, centerIdx + 2) };
    }
    // Monthly (M01..M12)
    const mMatch = periodCode.match(/^M(\d{1,2})$/);
    if (mMatch) {
      const month = parseInt(mMatch[1], 10) - 1;
      let startIdx = -1, endIdx = -1;
      for (let i = 0; i < n; i++) {
        if (btWeeks[i].getMonth() === month) {
          if (startIdx < 0) startIdx = i;
          endIdx = i;
        }
      }
      return (startIdx >= 0) ? { startIdx, endIdx } : null;
    }
    // Quarter (Q1..Q4)
    const qMatch = periodCode.match(/^Q(\d)$/);
    if (qMatch) {
      const q = parseInt(qMatch[1], 10);
      const monthStart = (q - 1) * 3;
      const monthEnd = monthStart + 2;
      let startIdx = -1, endIdx = -1;
      for (let i = 0; i < n; i++) {
        const m = btWeeks[i].getMonth();
        if (m >= monthStart && m <= monthEnd) {
          if (startIdx < 0) startIdx = i;
          endIdx = i;
        }
      }
      return (startIdx >= 0) ? { startIdx, endIdx } : null;
    }
    // Multi-year lookback — MY1 (52 weeks) / MY2 (104 weeks) ending at today.
    // Chart.js handles out-of-range-on-the-left gracefully as null.
    const myMatch = periodCode.match(/^MY([1-9])$/);
    if (myMatch) {
      const yearsBack = parseInt(myMatch[1], 10);
      const approxStart = btWeeks.findIndex(d => (today - d) / (1000 * 60 * 60 * 24 * 7) < yearsBack * 52);
      const startIdx = approxStart >= 0 ? approxStart : 0;
      return { startIdx, endIdx: n - 1 };
    }
    return null;
  }

  function sliceScenarioByPeriod(sd, win) {
    if (!win) return sd;
    const sliceArr = (a) => (Array.isArray(a) ? a.slice(win.startIdx, win.endIdx + 1) : a);
    const shifted = (v) => (typeof v === 'number' && v >= 0)
      ? (v - win.startIdx >= 0 && v - win.startIdx <= win.endIdx - win.startIdx ? v - win.startIdx : -1)
      : v;
    const clone = {
      ...sd,
      labels:          sliceArr(sd.labels),
      regsActual:      sliceArr(sd.regsActual),
      regsProjTotal:   sliceArr(sd.regsProjTotal),
      regsProjBrand:   sliceArr(sd.regsProjBrand),
      regsProjNb:      sliceArr(sd.regsProjNb),
      regsProjBrandStacked: sliceArr(sd.regsProjBrandStacked),
      regsProjNbStacked:    sliceArr(sd.regsProjNbStacked),
      spendActual:     sliceArr(sd.spendActual),
      spendProj:       sliceArr(sd.spendProj),
      ciLow:           sliceArr(sd.ciLow),
      ciHigh:          sliceArr(sd.ciHigh),
      counterfactual:  sliceArr(sd.counterfactual),
      todayIdx:        shifted(sd.todayIdx),
    };
    // Remap regime onset/end indices into the sliced window; drop regimes
    // entirely outside it so annotations don't render at idx=-1.
    clone.regimes = (sd.regimes || []).map((r, i) => {
      const onsetIn = typeof r.onsetIdx === 'number'
        && r.onsetIdx >= win.startIdx && r.onsetIdx <= win.endIdx;
      if (!onsetIn) return null;
      const endClamped = Math.min(win.endIdx, Math.max(r.endIdx || r.onsetIdx, r.onsetIdx));
      return {
        ...r,
        onsetIdx: r.onsetIdx - win.startIdx,
        endIdx: endClamped - win.startIdx,
      };
    }).filter(r => r != null);
    return clone;
  }

  // Helpers — local rather than reusing the ones inside projection-app's IIFE
  function fmtNum(v) {
    if (v == null || !isFinite(v)) return 'n/a';
    return Math.round(v).toLocaleString();
  }
  function fmt$(v) {
    if (v == null || !isFinite(v)) return 'n/a';
    if (Math.abs(v) >= 1_000_000) return `$${(v / 1_000_000).toFixed(2)}M`;
    if (Math.abs(v) >= 1_000) return `$${(v / 1_000).toFixed(1)}K`;
    return `$${Math.round(v)}`;
  }
  function fmtIsoWeek(date) {
    const d = (date instanceof Date) ? date : new Date(date);
    const t = new Date(Date.UTC(d.getFullYear(), d.getMonth(), d.getDate()));
    const day = t.getUTCDay() || 7;
    t.setUTCDate(t.getUTCDate() + 4 - day);
    const yearStart = new Date(Date.UTC(t.getUTCFullYear(), 0, 1));
    const weekNum = Math.ceil((((t - yearStart) / 86400000) + 1) / 7);
    return `W${String(weekNum).padStart(2, '0')}`;
  }

  // Build an ISO-week label for each chart data point. Scenario mode uses a
  // 0..N-1 index as x-axis (not time), so we supply labels as strings (e.g.
  // "W17", "W18") that Chart.js renders along the category axis. This also
  // keeps the x domain stable when the chart switches between markets whose
  // YTD windows are different lengths.
  function buildScenarioFromProjectionData(out, counterfactual, uncert, marketData) {
    const ytdRaw = marketData.ytd_weekly || [];
    const bt = marketData.brand_trajectory_y2026;
    if (!bt) return null;

    const ytdWeeks = ytdRaw.map(w => ({
      date: new Date(w.period_start),
      brand_regs: w.brand_regs || w.brand_registrations || 0,
      nb_regs: w.nb_regs || w.nb_registrations || 0,
      brand_spend: w.brand_cost || w.brand_spend || 0,
      nb_spend: w.nb_cost || w.nb_spend || 0,
    }));

    const btWeeks = bt.weeks.map(ws => new Date(ws));
    const ytdCount = ytdWeeks.length;
    const royWeeks = btWeeks.slice(ytdCount);
    const brandRoyRegs = bt.regs_per_week.slice(ytdCount);
    const brandRoySpend = bt.spend_per_week.slice(ytdCount);

    // Distribute NB over RoY weeks (matches V1_1_Slim aggregation)
    const royNbSpend = (out.roy?.nb_spend || 0) / (royWeeks.length || 1);
    const royNbRegs = (out.roy?.nb_regs || 0) / (royWeeks.length || 1);

    // Smoothing seam — carry the same logic from the Plot implementation:
    // scale projected Brand down to join the last-YTD Brand value, fading
    // back to 1.0 over 8 weeks. Prevents a visible cliff.
    const fadeWeeks = 8;
    let seamScale = 1;
    if (ytdWeeks.length > 0 && brandRoyRegs.length > 0 && brandRoyRegs[0] > 0) {
      const lastYtdBrand = ytdWeeks[ytdWeeks.length - 1].brand_regs;
      seamScale = lastYtdBrand / brandRoyRegs[0];
    }

    // x-axis labels = W01..W52 — one row per week of 2026, aligned to btWeeks
    const labels = btWeeks.map(d => fmtIsoWeek(d));

    // Per-index series (null where a value doesn't apply)
    const regsActual = new Array(btWeeks.length).fill(null);
    const regsProjTotal = new Array(btWeeks.length).fill(null);
    const regsProjBrand = new Array(btWeeks.length).fill(null);
    const regsProjNb = new Array(btWeeks.length).fill(null);
    const spendActual = new Array(btWeeks.length).fill(null);
    const spendProj = new Array(btWeeks.length).fill(null);
    const ciLow = new Array(btWeeks.length).fill(null);
    const ciHigh = new Array(btWeeks.length).fill(null);

    // Fill YTD half
    for (let i = 0; i < ytdCount; i++) {
      const w = ytdWeeks[i];
      regsActual[i] = w.brand_regs + w.nb_regs;
      spendActual[i] = w.brand_spend + w.nb_spend;
      // Populate component arrays on YTD half too so the stacked area
      // renders Brand/NB split for past weeks, not just projections.
      // The projected half is seam-faded; YTD is raw actuals.
      regsProjBrand[i] = w.brand_regs;
      regsProjNb[i]    = w.nb_regs;
      regsProjTotal[i] = w.brand_regs + w.nb_regs;
    }

    // Fill RoY half (projected, with seam-scale fade on Brand)
    for (let i = 0; i < royWeeks.length; i++) {
      const idx = ytdCount + i;
      const offset = i;
      const fade = offset < fadeWeeks ? seamScale + (1.0 - seamScale) * (offset / fadeWeeks) : 1.0;
      const projBrand = (brandRoyRegs[i] || 0) * fade;
      const projBrandSpend = (brandRoySpend[i] || 0) * fade;
      regsProjBrand[idx] = projBrand;
      regsProjNb[idx] = royNbRegs;
      regsProjTotal[idx] = projBrand + royNbRegs;
      spendProj[idx] = projBrandSpend + royNbSpend;
    }

    // Seam the projected total at the last YTD actual so the line connects
    if (ytdCount > 0 && ytdCount < btWeeks.length) {
      regsProjTotal[ytdCount - 1] = regsActual[ytdCount - 1];
      regsProjBrand[ytdCount - 1] = ytdWeeks[ytdCount - 1].brand_regs;
      regsProjNb[ytdCount - 1] = ytdWeeks[ytdCount - 1].nb_regs;
      spendProj[ytdCount - 1] = spendActual[ytdCount - 1];
    }

    // CI band — bootstrap per-week bands, RoY only
    if (uncert && uncert.per_week && uncert.per_week.regs &&
        Array.isArray(uncert.per_week.regs.lower) && Array.isArray(uncert.per_week.regs.upper)) {
      const pw = uncert.per_week.regs;
      for (let i = 0; i < btWeeks.length; i++) {
        if (i < ytdCount) continue;  // CI only on projected half
        if (i < pw.lower.length) ciLow[i] = pw.lower[i];
        if (i < pw.upper.length) ciHigh[i] = pw.upper[i];
      }
    }

    // Counterfactual — Brand-only, full-year if the MPE library computes it
    let counterfactualArr = null;
    if (counterfactual && counterfactual.ytd && counterfactual.roy &&
        typeof V1_1_Slim !== 'undefined' && V1_1_Slim.projectBrandTrajectory) {
      try {
        const cfRegs = V1_1_Slim.projectBrandTrajectory(marketData, btWeeks, { regimeMultiplier: 0 });
        counterfactualArr = cfRegs.regs_per_week.slice(0, btWeeks.length);
      } catch (e) {
        console.warn('[projection-chart] counterfactual compute failed:', e);
      }
    }

    // Regime-onset markers — map onset dates to btWeeks indices
    const regimesRaw = (marketData.regime_fit_state || []).slice()
      .sort((a, b) => new Date(a.change_date) - new Date(b.change_date));
    const regimes = [];
    for (let i = 0; i < regimesRaw.length; i++) {
      const r = regimesRaw[i];
      const onsetDate = new Date(r.change_date);
      // Find closest btWeek index
      let onsetIdx = -1;
      for (let j = 0; j < btWeeks.length; j++) {
        if (btWeeks[j] >= onsetDate) { onsetIdx = j; break; }
      }
      if (onsetIdx < 0) continue;
      // End = next regime onset or end of chart
      let endIdx = btWeeks.length - 1;
      if (i + 1 < regimesRaw.length) {
        const nextDate = new Date(regimesRaw[i + 1].change_date);
        for (let j = onsetIdx + 1; j < btWeeks.length; j++) {
          if (btWeeks[j] >= nextDate) { endIdx = j; break; }
        }
      }
      regimes.push({
        label: `Lift #${i + 1} onset`,
        onsetIdx,
        endIdx,
        absorbed: !!r.absorbed,
      });
    }

    const todayIdx = ytdCount > 0 ? ytdCount - 1 : -1;

    // Narrated tooltip — returns HTML body content for the external tooltip plugin.
    // Carries the contribution breakdown + 90% CI range that the old
    // renderNarratedTooltip emitted.
    const tooltipFormatter = (ctx, idx) => {
      if (idx == null || idx < 0) return '';
      const isLocked = idx < ytdCount;
      const totalRegs = isLocked ? (regsActual[idx] || 0) : (regsProjTotal[idx] || 0);
      const totalSpend = isLocked ? (spendActual[idx] || 0) : (spendProj[idx] || 0);
      const week = labels[idx] || `idx ${idx}`;
      const lines = [];
      lines.push(`<div style="font-weight:600;margin-bottom:4px">${week} · ${isLocked ? 'YTD actual (locked)' : 'Projected'}</div>`);
      lines.push(`<div style="font-size:14px;color:#fff;margin-bottom:6px">${fmtNum(totalRegs)} regs · ${fmt$(totalSpend)} spend</div>`);

      if (isLocked) {
        const w = ytdWeeks[idx];
        lines.push(`<div style="color:#aaa">Brand ${fmtNum(w.brand_regs)} regs · NB ${fmtNum(w.nb_regs)}. Brand ${fmt$(w.brand_spend)} · NB ${fmt$(w.nb_spend)}.</div>`);
      } else {
        const contrib = (bt && bt.contribution) || { seasonal: 0.4, trend: 0.4, regime: 0.15, qualitative: 0.05 };
        const seasPct = Math.round(contrib.seasonal * 100);
        const trendPct = Math.round(contrib.trend * 100);
        const regPct = Math.round(contrib.regime * 100);
        const qualPct = Math.round(contrib.qualitative * 100);
        const nLifts = (marketData.regime_fit_state || []).length;
        const liftLabel = nLifts === 1 ? '1 campaign lift' : (nLifts > 1 ? `${nLifts} campaign lifts` : '');
        lines.push(`<div style="color:#aaa">Brand ${fmtNum(regsProjBrand[idx])} regs: ${trendPct}% trend · ${seasPct}% seasonality · ${regPct}% lift${liftLabel ? ` (${liftLabel})` : ''} · ${qualPct}% judgment.</div>`);
        if (ciLow[idx] != null && ciHigh[idx] != null) {
          lines.push(`<div style="color:#6c7086;margin-top:4px">90% range: ${fmtNum(ciLow[idx])}–${fmtNum(ciHigh[idx])} regs</div>`);
        }
      }
      return lines.join('');
    };

    return {
      labels,
      regsActual,
      regsProjTotal,
      regsProjBrand,
      regsProjNb,
      // Stacked projected pair for the scenario chart's area fills.
      // Brand stays at its raw value (fills to origin); NB becomes the
      // cumulative (Brand + NB) so its area fills the delta between the
      // two lines. Done outside Chart.js's stacking engine because that
      // engine forces stack on every dataset on the y-axis, which would
      // break the Actuals line + CI band rendering.
      regsProjBrandStacked: regsProjBrand.map(v => Number.isFinite(v) ? v : null),
      regsProjNbStacked:    regsProjBrand.map((b, i) => {
        const nb = regsProjNb[i];
        if (Number.isFinite(b) && Number.isFinite(nb)) return b + nb;
        return null;
      }),
      spendActual,
      spendProj,
      ciLow,
      ciHigh,
      counterfactual: counterfactualArr,
      todayIdx,
      regimes,
      tooltipFormatter,
    };
  }

  let _chartInstance = null;

  function renderProjectionChart(out, counterfactual, uncert, marketData) {
    const chartEl = document.getElementById('chart-primary');
    if (!chartEl) return;

    if (!marketData.brand_trajectory_y2026) {
      chartEl.innerHTML = `<div style="text-align:center;padding:24px;color:var(--color-text-meta)">Brand trajectory not yet exported for this market.</div>`;
      return;
    }

    // Ensure there's a <canvas> inside #chart-primary that Chart.js can paint to.
    // First render: replace any previous contents (old Plot SVG, error message) with
    // a fresh canvas. Subsequent renders reuse the same canvas + destroy prior Chart.
    let canvas = chartEl.querySelector('canvas');
    if (!canvas) {
      chartEl.innerHTML = '';
      canvas = document.createElement('canvas');
      canvas.id = 'projection-chart-canvas';
      canvas.style.cssText = 'width:100%;height:100%;min-height:420px;display:block';
      chartEl.appendChild(canvas);
    }

    const scenarioData = buildScenarioFromProjectionData(out, counterfactual, uncert, marketData);
    if (!scenarioData) return;

    // P2-02: clip the chart x-domain to the currently-selected period.
    // Y2026 returns null (full-year span, unchanged). Any sub-period shows
    // only the relevant weeks so annotations + chart math scope tightly.
    const periodCode = getCurrentPeriod();
    const ytdCount = (marketData.ytd_weekly || []).length;
    const btWeeksAll = (marketData.brand_trajectory_y2026?.weeks || []).map(w => new Date(w));
    const win = periodWindowOverBtWeeks(periodCode, btWeeksAll, ytdCount);
    const slicedScenario = win ? sliceScenarioByPeriod(scenarioData, win) : scenarioData;

    _chartInstance = global.CanonChart.render(canvas, {
      mode: 'scenario',
      scenarioData: slicedScenario,
      chartInstance: _chartInstance,
    });

    // Remove any lingering external-tooltip div from the prior implementation
    // (before canon-chart switched to native afterBody). Belt-and-suspenders
    // for users who hit the page mid-deploy with a stale reference in the DOM.
    const staleTooltip = document.getElementById('scenario-tooltip-external');
    if (staleTooltip) staleTooltip.remove();
  }

  global.renderProjectionChart = renderProjectionChart;
})(typeof window !== 'undefined' ? window : globalThis);
