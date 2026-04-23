/**
 * projection-app.js — UI glue for projection.html.
 * Loads projection-data.json, wires inputs, renders outputs, handles save/copy/narrative/modal.
 */
(function () {
  'use strict';

  const STATE = {
    data: null,            // projection-data.json payload
    currentOutput: null,   // last MPE.project() result
    chart: null,
    saved: JSON.parse(localStorage.getItem('mpe-saved') || '[]'),
    activeTab: 'target',   // 2026-04-23: default to Target (was 'preset') per Richard's call to surface ie%CCP target by default
  };

  // ---------- Loading ----------

  async function loadData() {
    try {
      const resp = await fetch('data/projection-data.json', { cache: 'no-cache' });
      STATE.data = await resp.json();
    } catch (e) {
      console.error('Failed to load projection-data.json:', e);
      showBanner('warn', `Data unavailable: ${e.message}. UI is read-only.`);
      STATE.data = { markets: {}, regions: {}, global: { market_list: MPE.ALL_MARKETS, region_list: MPE.ALL_REGIONS } };
      return;
    }
    if (STATE.data.fallback) {
      showBanner('warn', `Data is a fallback stub (DB unreachable at export time: ${STATE.data.reason || 'unknown'}). Projections will fail.`);
    } else {
      const generated = new Date(STATE.data.generated);
      const ageHours = (Date.now() - generated.getTime()) / 3600000;
      showBanner('fresh', `Data refreshed ${generated.toLocaleString()} (${ageHours.toFixed(1)}h ago). Methodology v${STATE.data.methodology_version}.`);
    }
  }

  function showBanner(kind, text) {
    const el = document.getElementById('banner-' + kind);
    if (el) { el.textContent = text; el.style.display = 'block'; }
  }

  function populateScopeSelector() {
    const sel = document.getElementById('scope-select');
    const markets = STATE.data.global.market_list;
    const regions = STATE.data.global.region_list;

    const mktGroup = document.createElement('optgroup');
    mktGroup.label = 'Markets';
    for (const m of markets) {
      const md = STATE.data.markets[m];
      const fbBadge = md && md.fallback_summary !== 'all_market_specific' ? ' (fallback)' : '';
      const opt = document.createElement('option');
      opt.value = m; opt.textContent = m + fbBadge;
      mktGroup.appendChild(opt);
    }
    sel.appendChild(mktGroup);

    const regGroup = document.createElement('optgroup');
    regGroup.label = 'Regions';
    for (const r of regions) {
      const opt = document.createElement('option');
      opt.value = r; opt.textContent = r;
      regGroup.appendChild(opt);
    }
    sel.appendChild(regGroup);

    sel.value = 'MX';   // default to primary demo market
  }

  function updateScopeBadges() {
    const scope = document.getElementById('scope-select').value;
    const row = document.getElementById('scope-badge-row');
    row.innerHTML = '';

    if (MPE.ALL_REGIONS.includes(scope)) {
      const consts = MPE.REGION_CONSTITUENTS[scope];
      row.innerHTML = `<span style="font-size:11px;color:#888">Constituents: ${consts.join(', ')}</span>`;
      // Populate regional fallback summary banner
      const regionData = STATE.data.regions && STATE.data.regions[scope];
      if (regionData) {
        document.getElementById('banner-fallback').textContent = `${scope}: ${regionData.banner}`;
        document.getElementById('banner-fallback').style.display = 'block';
      }
      return;
    }

    const md = STATE.data.markets[scope];
    if (!md) { row.innerHTML = '<span style="font-size:11px;color:#f87171">No data for this market.</span>'; return; }
    const badges = [];
    if (md.fallback_summary === 'all_market_specific') badges.push('<span class="badge badge-market">market-specific</span>');
    else if (md.fallback_summary === 'market_specific_with_cpc_derived') badges.push('<span class="badge badge-market">market-specific (CPC derived)</span>');
    else if (md.fallback_summary === 'some_regional_fallback') badges.push('<span class="badge badge-fallback">some fallback</span>');
    else if (md.fallback_summary === 'all_regional_fallback') badges.push('<span class="badge badge-fallback">regional fallback</span>');
    const weeks = md.clean_weeks_count || 0;
    badges.push(`<span style="font-size:10px;color:#888;margin-left:8px">${weeks} YTD weeks</span>`);
    const reg = md.regime_events && md.regime_events.length || 0;
    if (reg > 0) badges.push(`<span style="font-size:10px;color:#888;margin-left:8px">${reg} active regime(s)</span>`);
    row.innerHTML = badges.join('');

    // Hide regional banner if we're back on a market scope
    document.getElementById('banner-fallback').style.display = 'none';
  }

  // ---------- Target triad management (2026-04-23) ----------
  // Three inputs (ie%CCP, spend, regs) always visible. One is the "driver"
  // (selected by radio); others are disabled and updated after each projection
  // run from out.totals. Default driver: ie%CCP at the market's ieccp_target.

  function getTargetDriver() {
    const checked = document.querySelector('input[name="target-driver"]:checked');
    return checked ? checked.value : 'ieccp';
  }

  function refreshTargetDriverDefaults() {
    // Called on scope change — set ie%CCP default to market's ieccp_target,
    // wipe spend/regs (they'll be populated after next projection).
    const scope = document.getElementById('scope-select').value;
    const md = STATE.data.markets[scope];
    let ieccpDefault = 100;   // 100% fallback
    if (md && md.parameters && md.parameters.ieccp_target) {
      const scalar = md.parameters.ieccp_target.value_scalar;
      if (scalar != null) ieccpDefault = Math.round(scalar * 100);
    }
    // Handle supported_target_modes (e.g. AU doesn't support ieccp)
    let supportedModes = ['spend', 'ieccp', 'regs'];
    if (md && md.parameters && md.parameters.supported_target_modes) {
      supportedModes = md.parameters.supported_target_modes.value_json || supportedModes;
    }

    // Enable/disable radios based on supported modes
    for (const mode of ['ieccp', 'spend', 'regs']) {
      const radio = document.getElementById(`target-driver-${mode}`);
      const input = document.getElementById(`target-value-${mode}`);
      if (!supportedModes.includes(mode)) {
        radio.disabled = true;
        input.disabled = true;
        input.value = 'n/a';
      } else {
        radio.disabled = false;
      }
    }
    // If currently selected driver isn't supported, pick first supported
    const currentDriver = getTargetDriver();
    if (!supportedModes.includes(currentDriver)) {
      const firstSupported = supportedModes[0];
      document.getElementById(`target-driver-${firstSupported}`).checked = true;
    }

    // Seed ie%CCP default if ie%CCP is supported
    if (supportedModes.includes('ieccp')) {
      document.getElementById('target-value-ieccp').value = ieccpDefault;
    }
    // Reset spend/regs until next projection fills them
    if (supportedModes.includes('spend')) {
      document.getElementById('target-value-spend').value = '';
    }
    if (supportedModes.includes('regs')) {
      document.getElementById('target-value-regs').value = '';
    }
    syncTargetTriadEnabled();
  }

  function syncTargetTriadEnabled() {
    // The driver input is enabled; the other two are disabled.
    const driver = getTargetDriver();
    for (const mode of ['ieccp', 'spend', 'regs']) {
      const input = document.getElementById(`target-value-${mode}`);
      const radio = document.getElementById(`target-driver-${mode}`);
      if (radio.disabled) continue;  // unsupported modes stay disabled
      input.disabled = (mode !== driver);
    }
  }

  function writeDerivedTriad(out) {
    // After a projection run, update the two non-driver fields from the output.
    if (!out || out.outcome !== 'OK') return;
    const t = out.totals;
    const driver = getTargetDriver();
    if (driver !== 'ieccp' && t.ieccp != null) {
      document.getElementById('target-value-ieccp').value = Math.round(t.ieccp * 10) / 10;
    }
    if (driver !== 'spend' && t.total_spend != null) {
      document.getElementById('target-value-spend').value = Math.round(t.total_spend);
    }
    if (driver !== 'regs' && t.total_regs != null) {
      document.getElementById('target-value-regs').value = Math.round(t.total_regs);
    }
  }

  // ---------- Target mode selector based on supported_target_modes ----------

  function refreshTargetModeOptions() {
    // Deprecated 2026-04-23: target-mode-select removed in favor of target triad.
    // Kept as no-op for compatibility with save/load pipeline that may call it.
    const select = document.getElementById('target-mode-select');
    if (!select) return;
    const scope = document.getElementById('scope-select').value;
    const md = STATE.data.markets[scope];
    let modes = ['spend', 'ieccp', 'regs'];
    if (md && md.parameters && md.parameters.supported_target_modes) {
      modes = md.parameters.supported_target_modes.value_json || modes;
    }
    const prev = select.value;
    select.innerHTML = '';
    for (const m of modes) {
      const opt = document.createElement('option');
      opt.value = m; opt.textContent = m === 'spend' ? 'Spend ($)' : m === 'ieccp' ? 'ie%CCP (%)' : 'Registrations';
      select.appendChild(opt);
    }
    if (modes.includes(prev)) select.value = prev; else select.value = modes[0];
  }

  // ---------- Recompute ----------

  let recomputeTimer = null;
  function scheduleRecompute() {
    clearTimeout(recomputeTimer);
    recomputeTimer = setTimeout(recompute, 150);
  }

  function buildInputs() {
    const scope = document.getElementById('scope-select').value;
    const timePeriod = document.getElementById('period-select').value;
    const tab = STATE.activeTab;

    let targetMode = 'spend';
    let targetValue = 325000;
    if (tab === 'target') {
      // Triad mode: driver radio determines mode + which input is authoritative
      targetMode = getTargetDriver();
      const driverInputId = `target-value-${targetMode}`;
      let raw = parseFloat(document.getElementById(driverInputId).value) || 0;
      // Normalize ie%CCP: accept 75 or 0.75 — engine normalizes internally,
      // but we keep UI convention as percentage (e.g. 100 for 100%).
      targetValue = raw;
    } else if (tab === 'preset') {
      // Preset — use market defaults (spend target, conservative/aggressive adjustment)
      targetMode = 'spend';
      targetValue = getPresetSpend(scope, document.getElementById('preset-select').value);
    } else if (tab === 'sliders') {
      targetMode = 'spend';
      targetValue = getPresetSpend(scope, 'base');
    }

    const brandUplift = parseFloat(document.getElementById('brand-uplift').value) || 0;
    const nbUplift = parseFloat(document.getElementById('nb-uplift').value) || 0;

    return {
      scope, timePeriod, targetMode, targetValue,
      brandUpliftPct: brandUplift,
      nbUpliftPct: nbUplift,
      rngSeed: 42,
    };
  }

  function getPresetSpend(scope, preset) {
    // Preset math: compute a per-week spend from market's YTD run-rate,
    // then scale by the number of weeks in the SELECTED period.
    // Before 2026-04-23: preset always multiplied weekly avg × 13 regardless of
    // selected period, which made M04 (4 weeks) over-spend 3× and Q2 (14 weeks)
    // under-spend by ~7%. Fixed to scale by actual period week count so a
    // preset's per-week economics are invariant across W/M/Q/Y/MY selections.
    const md = STATE.data.markets[scope];
    let weeklyAvg = 10000;
    if (md && md.ytd_weekly && md.ytd_weekly.length >= 4) {
      const last4 = md.ytd_weekly.slice(-4);
      const sum = last4.reduce((s, r) => s + (r.cost || 0), 0);
      weeklyAvg = Math.max(sum / 4, 1000);
    }

    // Determine weeks in the selected period
    const periodValue = document.getElementById('period-select').value;
    let weeksInPeriod = 13;
    try {
      const tp = MPE.parseTimePeriod(periodValue);
      weeksInPeriod = tp.weeks.length * (tp.n_years || 1);
    } catch (e) {
      // invalid period — fall back to 13
    }

    const base = weeklyAvg * weeksInPeriod;
    const adjust = {
      base: 1.0, moderate: 1.0, conservative: 0.9,
      aggressive: 1.15, 'placement-persists': 1.12, 'placement-decays': 1.06,
    };
    return Math.round(base * (adjust[preset] || 1.0));
  }

  async function recompute() {
    const inputs = buildInputs();
    const out = await MPE.projectWithUncertainty(inputs, STATE.data);
    STATE.currentOutput = out;
    renderOutput(out);
  }

  // ---------- Rendering ----------

  function renderOutput(out) {
    renderSummary(out);
    renderGauge(out);
    renderChart(out);
    renderConstituents(out);
    renderWarnings(out);
    renderParamsUsed(out);
    writeDerivedTriad(out);  // 2026-04-23: sync non-driver triad fields from projection output
    // Clear narrative on new recompute; user must click button
    const nar = document.getElementById('narrative-block');
    if (nar.dataset.scope !== out.scope || nar.dataset.period !== out.time_period) {
      nar.innerHTML = '<em>Click "Narrative" above to generate.</em>';
      nar.dataset.scope = out.scope;
      nar.dataset.period = out.time_period;
    }
  }

  function renderSummary(out) {
    const grid = document.getElementById('summary-grid');
    grid.innerHTML = '';
    const meta = document.getElementById('summary-meta');
    meta.textContent = `${out.scope} · ${out.time_period} · ${out.target_mode}=${out.target_value}`;

    if (out.outcome !== 'OK') {
      grid.innerHTML = `<div style="color:#f87171;font-size:13px">${out.outcome} — see warnings.</div>`;
      return;
    }
    const t = out.totals;
    const ci = out.credible_intervals || {};
    const tiles = [
      { label: 'Total Regs', value: fmtNum(t.total_regs), ci: ci.total_regs, key: 'total_regs' },
      { label: 'Total Spend', value: fmt$(t.total_spend), ci: ci.total_spend, key: 'total_spend' },
      { label: 'Blended CPA', value: fmt$(t.blended_cpa), ci: ci.blended_cpa, key: 'blended_cpa' },
      { label: 'ie%CCP', value: fmtPct(t.ieccp), ci: ci.ieccp, key: 'ieccp' },
      { label: 'Brand Regs', value: fmtNum(t.brand_regs), ci: ci.brand_regs, key: 'brand_regs' },
      { label: 'NB Regs', value: fmtNum(t.nb_regs), ci: ci.nb_regs, key: 'nb_regs' },
    ];
    for (const tile of tiles) {
      const el = document.createElement('div');
      el.className = 'summary-tile';
      const ciText = tile.ci ? `90% CI: ${formatCI(tile.ci, tile.key)}` : '';
      el.innerHTML = `<div class="summary-label">${tile.label}</div><div class="summary-value">${tile.value}</div><div class="summary-ci">${ciText}</div>`;
      el.onclick = () => openProvenance(tile.key);
      grid.appendChild(el);
    }
  }

  function formatCI(ciObj, key) {
    if (!ciObj || !ciObj.ci || !ciObj.ci['90']) return '';
    const [lo, hi] = ciObj.ci['90'];
    if (key === 'total_spend' || key === 'blended_cpa') return `${fmt$(lo)} – ${fmt$(hi)}`;
    if (key === 'ieccp') return `${fmtPct(lo)} – ${fmtPct(hi)}`;
    return `${fmtNum(lo)} – ${fmtNum(hi)}`;
  }

  function renderGauge(out) {
    const v = out.totals.ieccp;
    const el = document.getElementById('gauge-value');
    const lbl = document.getElementById('gauge-label');
    if (v === null || v === undefined || !isFinite(v)) {
      el.textContent = '—'; el.className = 'gauge-value neutral';
      lbl.textContent = 'ie%CCP not computable for this scope';
      return;
    }
    el.textContent = fmtPct(v);
    // Thresholds informed by MX 100% target + 90-110% range
    let klass = 'neutral';
    if (v < 80) klass = 'good';
    else if (v < 120) klass = 'warn';
    else klass = 'bad';
    el.className = 'gauge-value ' + klass;
    lbl.textContent = `ie%CCP · lower is more efficient`;
  }

  function renderChart(out) {
    const ctx = document.getElementById('chart-weekly').getContext('2d');
    if (STATE.chart) STATE.chart.destroy();

    if (!out.weeks || out.weeks.length === 0) {
      STATE.chart = null;
      return;
    }
    const labels = out.weeks.map(w => w.week_key || `W${w.week_num}`);
    const brandSpend = out.weeks.map(w => w.brand_spend);
    const nbSpend = out.weeks.map(w => w.nb_spend);
    const totalRegs = out.weeks.map(w => w.brand_regs + w.nb_regs);

    STATE.chart = new Chart(ctx, {
      type: 'bar',
      data: {
        labels,
        datasets: [
          { label: 'Brand spend', data: brandSpend, backgroundColor: 'rgba(74, 158, 255, 0.7)', stack: 's' },
          { label: 'NB spend', data: nbSpend, backgroundColor: 'rgba(251, 191, 36, 0.7)', stack: 's' },
          { label: 'Regs', data: totalRegs, type: 'line', yAxisID: 'y1', borderColor: '#4ade80', backgroundColor: 'rgba(74, 222, 128, 0.2)', tension: 0.2, pointRadius: 2 },
        ],
      },
      options: {
        responsive: true, maintainAspectRatio: false,
        plugins: { legend: { labels: { color: '#c8c8c8' } } },
        scales: {
          x: { stacked: true, ticks: { color: '#888', maxRotation: 45, minRotation: 0 }, grid: { color: '#1e2028' } },
          y: { stacked: true, position: 'left', title: { display: true, text: 'Spend ($)', color: '#888' }, ticks: { color: '#888' }, grid: { color: '#1e2028' } },
          y1: { position: 'right', title: { display: true, text: 'Regs', color: '#888' }, ticks: { color: '#888' }, grid: { display: false } },
        },
      },
    });
  }

  function renderConstituents(out) {
    const card = document.getElementById('constituents-card');
    if (!out.constituent_markets || out.constituent_markets.length === 0) {
      card.style.display = 'none'; return;
    }
    card.style.display = '';
    const tbody = document.querySelector('#constituents-table tbody');
    tbody.innerHTML = '';
    for (const c of out.constituent_markets) {
      const row = document.createElement('tr');
      row.innerHTML = `
        <td>${c.market}</td>
        <td>${fmtNum(c.brand_regs + c.nb_regs)}</td>
        <td>${fmt$(c.total_spend)}</td>
        <td>${c.ieccp !== null && c.ieccp !== undefined ? fmtPct(c.ieccp) : 'n/a'}</td>
        <td style="font-size:10px">${c.fallback_level_summary || ''}</td>
      `;
      tbody.appendChild(row);
    }
  }

  function renderWarnings(out) {
    const ul = document.getElementById('warnings-list');
    const count = document.getElementById('warnings-count');
    ul.innerHTML = '';
    if (!out.warnings || out.warnings.length === 0) {
      ul.innerHTML = '<li class="info">No warnings.</li>';
      count.textContent = '';
      return;
    }
    count.textContent = `${out.warnings.length} warning${out.warnings.length === 1 ? '' : 's'}`;
    for (const w of out.warnings) {
      const li = document.createElement('li');
      if (w.startsWith('VERY_WIDE_CI')) li.className = 'very-wide';
      else if (w.startsWith('DATA_LIMITED') || w.startsWith('REGIONAL_FALLBACK') || w.startsWith('CPC_DERIVED')) li.className = 'info';
      li.textContent = w;
      ul.appendChild(li);
    }
  }

  function renderParamsUsed(out) {
    const el = document.getElementById('parameters-used');
    const p = out.parameters_used || {};
    const keys = Object.keys(p).filter(k => k.includes('_elasticity') || k.includes('_yoy_growth') || k.includes('_seasonality_shape') || k === 'brand_ccp' || k === 'nb_ccp');
    if (keys.length === 0) { el.innerHTML = '(no parameters — regional or setup-required)'; return; }
    el.innerHTML = keys.map(k => {
      const rec = p[k];
      return `<div style="padding:2px 0"><strong>${k}</strong>: <span style="color:${rec.fallback_level === 'market_specific' ? '#a8d8a8' : '#e8cc88'}">${rec.fallback_level || 'unknown'}</span>${rec.lineage ? ` — ${rec.lineage}` : ''}</div>`;
    }).join('');
  }

  // ---------- Provenance modal ----------

  function openProvenance(metricKey) {
    const out = STATE.currentOutput;
    if (!out) return;
    const ci = out.credible_intervals && out.credible_intervals[metricKey];
    const t = out.totals;
    document.getElementById('modal-title').textContent = `${metricKey} — provenance`;
    const body = document.getElementById('modal-body');

    const central = ci ? ci.central : t[metricKey];
    const ci50 = ci && ci.ci ? ci.ci['50'] : null;
    const ci70 = ci && ci.ci ? ci.ci['70'] : null;
    const ci90 = ci && ci.ci ? ci.ci['90'] : null;

    const paramsUsed = out.parameters_used || {};
    const relevantParams = Object.entries(paramsUsed)
      .filter(([k]) => metricKey.startsWith('brand') ? k.startsWith('brand') : metricKey.startsWith('nb') ? k.startsWith('nb') : true)
      .slice(0, 8)
      .map(([k, v]) => `<tr><td>${k}</td><td>${v.fallback_level || ''}</td><td style="font-size:11px;color:#888">${v.lineage || ''}</td></tr>`)
      .join('');

    body.innerHTML = `
      <p><strong>Central estimate:</strong> ${formatValue(central, metricKey)}</p>
      ${ci50 ? `<p><strong>50% CI:</strong> ${formatValue(ci50[0], metricKey)} to ${formatValue(ci50[1], metricKey)}</p>` : ''}
      ${ci70 ? `<p><strong>70% CI:</strong> ${formatValue(ci70[0], metricKey)} to ${formatValue(ci70[1], metricKey)}</p>` : ''}
      ${ci90 ? `<p><strong>90% CI:</strong> ${formatValue(ci90[0], metricKey)} to ${formatValue(ci90[1], metricKey)}</p>` : ''}
      ${ci && ci.warnings && ci.warnings.length > 0 ? `<p style="color:#e8cc88"><strong>CI warnings:</strong> ${ci.warnings.join(', ')}</p>` : ''}
      <h3 style="margin-top:14px;font-size:13px;color:#4a9eff">Parameter lineage</h3>
      <table style="margin-top:6px">
        <thead><tr><th>Parameter</th><th>Fallback level</th><th>Lineage</th></tr></thead>
        <tbody>${relevantParams || '<tr><td colspan="3" style="color:#666">No parameter metadata available.</td></tr>'}</tbody>
      </table>
      <p style="margin-top:14px;font-size:12px;color:#888">
        Methodology: recency-weighted log-linear regression (half-life 52w) with Monte Carlo credible intervals (200 samples in UI).
        Formula: CPA = exp(a) * spend^b. ie%CCP = total_spend / Σ(regs × CCP) × 100.
      </p>
    `;
    document.getElementById('modal-overlay').classList.add('active');
  }

  function closeModal() {
    document.getElementById('modal-overlay').classList.remove('active');
  }
  window.closeModal = closeModal;

  function formatValue(v, key) {
    if (v === null || v === undefined || !isFinite(v)) return 'n/a';
    if (key && (key.includes('spend') || key.includes('cpa'))) return fmt$(v);
    if (key === 'ieccp') return fmtPct(v);
    return fmtNum(v);
  }

  // ---------- Save / Copy / Narrative ----------

  function saveProjection() {
    const out = STATE.currentOutput;
    if (!out || out.outcome !== 'OK') return;
    const rec = {
      id: Date.now(),
      scope: out.scope, time_period: out.time_period,
      target_mode: out.target_mode, target_value: out.target_value,
      totals: out.totals, credible_intervals: out.credible_intervals,
      warnings: out.warnings, saved_at: new Date().toISOString(),
      parameters_fingerprint: STATE.data.generated,
    };
    STATE.saved.unshift(rec);
    STATE.saved = STATE.saved.slice(0, 20);   // keep latest 20
    localStorage.setItem('mpe-saved', JSON.stringify(STATE.saved));
    refreshSavedList();
  }

  function refreshSavedList() {
    const list = document.getElementById('saved-list');
    const count = document.getElementById('saved-count');
    count.textContent = STATE.saved.length ? `${STATE.saved.length} saved` : '';
    if (!STATE.saved.length) {
      list.innerHTML = '<div style="color:#666;font-size:12px;padding:4px">No saved projections yet.</div>';
      return;
    }
    list.innerHTML = STATE.saved.map(rec => {
      const fresh = rec.parameters_fingerprint === STATE.data.generated;
      const stale = !fresh ? ' <span style="color:#e8cc88;font-size:10px">(params changed since save)</span>' : '';
      return `<div class="saved-item" data-id="${rec.id}">
        <span class="saved-label">${rec.scope} ${rec.time_period} ${rec.target_mode}=${rec.target_value}${stale}</span>
        <span class="saved-meta">${new Date(rec.saved_at).toLocaleDateString()}</span>
      </div>`;
    }).join('');
    list.querySelectorAll('.saved-item').forEach(el => {
      el.addEventListener('click', () => loadSaved(parseInt(el.dataset.id)));
    });
  }

  function loadSaved(id) {
    const rec = STATE.saved.find(r => r.id === id);
    if (!rec) return;
    document.getElementById('scope-select').value = rec.scope;
    document.getElementById('period-select').value = rec.time_period;
    // Switch to Target tab and populate target triad from saved record (2026-04-23)
    switchTab('target');
    refreshTargetDriverDefaults();  // seed defaults for the new scope
    const mode = rec.target_mode;
    if (['ieccp', 'spend', 'regs'].includes(mode)) {
      document.getElementById(`target-driver-${mode}`).checked = true;
      document.getElementById(`target-value-${mode}`).value = rec.target_value;
      syncTargetTriadEnabled();
    }
    updateScopeBadges();
    refreshTargetModeOptions();
    recompute();
    if (rec.parameters_fingerprint !== STATE.data.generated) {
      showBanner('warn', 'Parameters have changed since this projection was saved. Reloaded with current curves — numbers will differ from the original save.');
    }
  }

  function copyJSON() {
    if (!STATE.currentOutput) return;
    navigator.clipboard.writeText(JSON.stringify(STATE.currentOutput, null, 2));
    alert('Copied JSON to clipboard.');
  }

  function copyMarkdown() {
    if (!STATE.currentOutput) return;
    const out = STATE.currentOutput;
    const t = out.totals;
    const ci = out.credible_intervals || {};
    const regsCi = ci.total_regs && ci.total_regs.ci ? ci.total_regs.ci['90'] : null;
    const md = `# MPE Projection — ${out.scope} ${out.time_period}\n\n` +
      `**Target**: ${out.target_mode}=${out.target_value}\n` +
      `**Outcome**: ${out.outcome}\n\n` +
      `## Totals\n` +
      `- Total Regs: ${fmtNum(t.total_regs)}${regsCi ? ` (90% CI: ${fmtNum(regsCi[0])} – ${fmtNum(regsCi[1])})` : ''}\n` +
      `- Total Spend: ${fmt$(t.total_spend)}\n` +
      `- Blended CPA: ${fmt$(t.blended_cpa)}\n` +
      `- ie%CCP: ${fmtPct(t.ieccp)}\n\n` +
      (out.warnings.length ? `## Warnings\n${out.warnings.map(w => `- ${w}`).join('\n')}\n` : '');
    navigator.clipboard.writeText(md);
    alert('Copied markdown to clipboard.');
  }

  function generateNarrative() {
    if (!STATE.currentOutput) return;
    const narBlock = document.getElementById('narrative-block');
    const text = MPENarrative.generate(STATE.currentOutput, STATE.data);
    narBlock.textContent = text;
  }

  // ---------- Utilities ----------

  function fmt$(v) {
    if (v === null || v === undefined || !isFinite(v)) return 'n/a';
    if (Math.abs(v) >= 1_000_000) return `$${(v / 1_000_000).toFixed(2)}M`;
    if (Math.abs(v) >= 1000) return `$${(v / 1000).toFixed(0)}K`;
    return `$${v.toFixed(0)}`;
  }
  function fmtPct(v, digits) {
    if (v === null || v === undefined || !isFinite(v)) return 'n/a';
    return `${v.toFixed(digits || 1)}%`;
  }
  function fmtNum(v, digits) {
    if (v === null || v === undefined || !isFinite(v)) return 'n/a';
    return v.toLocaleString(undefined, { maximumFractionDigits: digits || 0 });
  }

  // ---------- Tabs ----------

  function switchTab(name) {
    STATE.activeTab = name;
    document.querySelectorAll('.tab').forEach(t => t.classList.toggle('active', t.dataset.tab === name));
    document.querySelectorAll('.tab-panel').forEach(p => p.classList.toggle('active', p.dataset.panel === name));
    scheduleRecompute();
  }

  // ---------- Init ----------

  async function init() {
    await loadData();
    populateScopeSelector();
    refreshTargetModeOptions();
    refreshTargetDriverDefaults();  // 2026-04-23: seed triad from market's ieccp_target
    updateScopeBadges();

    // Scope change
    document.getElementById('scope-select').addEventListener('change', () => {
      refreshTargetModeOptions();
      refreshTargetDriverDefaults();
      updateScopeBadges();
      scheduleRecompute();
    });
    // Target triad inputs
    for (const mode of ['ieccp', 'spend', 'regs']) {
      const input = document.getElementById(`target-value-${mode}`);
      if (input) input.addEventListener('change', scheduleRecompute);
      const radio = document.getElementById(`target-driver-${mode}`);
      if (radio) radio.addEventListener('change', () => { syncTargetTriadEnabled(); scheduleRecompute(); });
    }
    // Other inputs
    ['period-select', 'preset-select']
      .forEach(id => {
        const el = document.getElementById(id);
        if (el) el.addEventListener('change', scheduleRecompute);
      });
    // Sliders
    document.getElementById('brand-uplift').addEventListener('input', (e) => {
      document.getElementById('brand-uplift-val').textContent = e.target.value + '%';
      scheduleRecompute();
    });
    document.getElementById('nb-uplift').addEventListener('input', (e) => {
      document.getElementById('nb-uplift-val').textContent = e.target.value + '%';
      scheduleRecompute();
    });
    // Tabs
    document.querySelectorAll('.tab').forEach(t => {
      t.addEventListener('click', () => switchTab(t.dataset.tab));
    });
    // Actions
    document.getElementById('btn-recompute').addEventListener('click', recompute);
    document.getElementById('btn-save').addEventListener('click', saveProjection);
    document.getElementById('btn-copy-json').addEventListener('click', copyJSON);
    document.getElementById('btn-copy-md').addEventListener('click', copyMarkdown);
    document.getElementById('btn-generate-narrative').addEventListener('click', generateNarrative);

    refreshSavedList();

    // Initial computation
    recompute();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
