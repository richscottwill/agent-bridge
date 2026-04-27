/**
 * projection-app.js — MPE v1.1 Slim UI (Phase 6.3)
 *
 * Renders the viz-foundation demo:
 *   - Hero number (96pt) + progressive disclosure (How / Parameters / Uncertainty / Counterfactual / Narrative)
 *   - Primary projection chart (Observable Plot + D3) with YTD wall, Brand/NB lines,
 *     regime markers, target line, optional CI band and counterfactual overlay
 *   - Contribution bar (Seasonal/Trend/Regime) + NB residual bar
 *   - Narrated tooltips on every data point
 *   - 4-stage loading states as transparency
 *   - Animated arrival sequence
 *   - Right drawer (Model View) for Parameters disclosure
 *
 * Data source: projection-data.json (Python-as-truth, JS-as-presentation).
 * Engine: V1_1_Slim.projectWithLockedYtd() for the projection math;
 *         MPE.projectWithUncertainty() for the Monte Carlo CI band.
 */
(function () {
  'use strict';

  // ========================================================================
  // State + constants
  // ========================================================================

  const STATE = {
    data: null,
    currentOutput: null,       // Main projection result (V1_1_Slim shape or MPE shape)
    currentUncertainty: null,  // MPE credible-intervals payload
    currentBrandProj: null,    // Raw brand trajectory used (for chart)
    currentCounterfactual: null,
    saved: JSON.parse(localStorage.getItem('mpe-saved') || '[]'),
    disclosures: { how: false, params: false, uncert: false, counter: false, narrative: false },
    tooltipEl: null,           // Reused DOM tooltip node
    loading: false,
    loadingTimer: null,
    regimeMultiplier: 1.00,
    scenarioOverride: null,    // {half_life_weeks, peak_multiplier, force_confidence} | null
    activeChipId: 'mixed',
    activeView: 'single',      // 'single' | 'multiples' | 'heatgrid'  (6.4.1/6.4.2)
  };

  const DEFAULT_SCOPE = 'MX';
  const DEFAULT_PERIOD = 'Y2026';
  const DEFAULT_DRIVER = 'ieccp';
  const DEFAULT_TARGET_VALUE = 75;     // 75% ie%CCP — the canonical demo scenario

  const CHART_HEIGHT = 420;
  const CHART_MARGIN = { top: 30, right: 70, bottom: 40, left: 60 };

  // ========================================================================
  // Utilities — formatting
  // ========================================================================

  function fmt$(v) {
    if (v == null || !isFinite(v)) return 'n/a';
    if (Math.abs(v) >= 1_000_000) return `$${(v / 1_000_000).toFixed(2)}M`;
    if (Math.abs(v) >= 1000) return `$${Math.round(v / 1000)}K`;
    return `$${Math.round(v)}`;
  }
  function fmtNum(v) {
    if (v == null || !isFinite(v)) return 'n/a';
    return Math.round(v).toLocaleString();
  }
  function fmtPct(v, digits) {
    if (v == null || !isFinite(v)) return 'n/a';
    return `${v.toFixed(digits == null ? 1 : digits)}%`;
  }
  function fmtIsoWeek(date) {
    const d = (date instanceof Date) ? date : new Date(date);
    const t = new Date(Date.UTC(d.getFullYear(), d.getMonth(), d.getDate()));
    const dayNum = (t.getUTCDay() + 6) % 7;
    t.setUTCDate(t.getUTCDate() - dayNum + 3);
    const firstThursday = t.valueOf();
    t.setUTCMonth(0, 1);
    if (t.getUTCDay() !== 4) t.setUTCMonth(0, 1 + ((4 - t.getUTCDay()) + 7) % 7);
    const weekNum = 1 + Math.ceil((firstThursday - t) / (7 * 24 * 3600 * 1000));
    return `W${String(weekNum).padStart(2, '0')}`;
  }
  function computeIsoWeekNum(date) {
    const s = fmtIsoWeek(date);
    return parseInt(s.slice(1), 10);
  }

  // ========================================================================
  // Data loading
  // ========================================================================

  async function loadData() {
    try {
      const resp = await fetch('data/projection-data.json', { cache: 'no-cache' });
      STATE.data = await resp.json();
    } catch (e) {
      console.error('Failed to load projection-data.json:', e);
      showBanner('danger', `Data unavailable (${e.message}). UI is non-functional.`);
      STATE.data = { markets: {}, regions: {}, global: { market_list: MPE.ALL_MARKETS, region_list: MPE.ALL_REGIONS } };
      return false;
    }
    if (STATE.data.fallback) {
      showBanner('warn', `Data is a fallback stub (${STATE.data.reason || 'unknown'}).`);
    } else {
      const generated = new Date(STATE.data.generated);
      const ageHours = (Date.now() - generated.getTime()) / 3600000;
      const el = document.getElementById('header-freshness');
      if (el) el.textContent = `Data ${ageHours.toFixed(1)}h old · methodology v${STATE.data.methodology_version || '1.0.0'}`;
    }
    return true;
  }

  function showBanner(kind, text) {
    const el = document.getElementById('banner-' + kind);
    if (!el) return;
    el.textContent = text;
    el.classList.add('visible');
  }
  function hideBanner(kind) {
    const el = document.getElementById('banner-' + kind);
    if (el) el.classList.remove('visible');
  }

  // ========================================================================
  // Anomaly rendering (Phase 4.1 + 6.5.3) — surface model anomalies per scope
  // ========================================================================

  function renderHeaderAnomalies() {
    const el = document.getElementById('header-anomalies');
    if (!el) return;
    const summary = STATE.data?.anomalies?.summary || {};
    const total = summary.total || 0;
    if (total === 0) {
      el.innerHTML = '<span style="font-size:11px;color:var(--color-success)">✓ no anomalies</span>';
      return;
    }
    const parts = [];
    if (summary.error) parts.push(`<span style="color:var(--color-danger)">${summary.error} critical</span>`);
    if (summary.warn) parts.push(`<span style="color:var(--color-warning)">${summary.warn} warn</span>`);
    if (summary.info) parts.push(`<span style="color:var(--color-text-meta)">${summary.info} info</span>`);
    el.innerHTML = `<span style="font-size:11px">⚠ ${parts.join(' · ')}</span>`;
    el.style.cursor = 'pointer';
    el.title = 'Click to scroll to anomalies panel in current market view';
    el.onclick = () => {
      const panel = document.getElementById('anomalies-panel');
      if (panel && panel.style.display !== 'none') {
        panel.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
    };
  }

  function renderMarketAnomalies(marketCode) {
    const panel = document.getElementById('anomalies-panel');
    const list = document.getElementById('anomalies-list');
    const cnt = document.getElementById('anomalies-count');
    const items = STATE.data?.anomalies?.markets?.[marketCode] || [];
    if (!items.length) {
      panel.style.display = 'none';
      list.innerHTML = '';
      cnt.textContent = '';
      return;
    }
    panel.style.display = '';
    cnt.textContent = `(${items.length})`;
    // Plain-language check names — map the raw check keys to sentence labels.
    // Round 6 V6-3: the translation table existed but wasn't being consulted
    // here. Anomaly items use a `check` field (fit_r2_drop, op2_pacing_divergence,
    // regime_low_confidence, ytd_projection_step) which we now translate inline.
    const CHECK_LABELS = {
      fit_r2_drop: 'Fit quality dropped sharply',
      op2_pacing_divergence: 'Projection diverges from OP2 plan',
      regime_low_confidence: 'Campaign lift confidence is low',
      ytd_projection_step: 'Large step between actuals and projection',
    };
    // Plain-language detail stripping — remove bare table references and make
    // the dollar/pct numbers readable inline.
    function translateDetail(d) {
      if (!d) return '';
      return String(d)
        .replace(/brand_cpa_elasticity/g, 'Brand CPA fit')
        .replace(/nb_cpa_elasticity/g, 'Non-Brand CPA fit')
        .replace(/\bps\.v_weekly\b/g, 'weekly data')
        .replace(/\bps\.regime_changes\b/g, 'campaign lifts registry')
        .replace(/v1\.1 Slim /g, '')
        .replace(/\br²\b/g, 'fit quality');
    }
    list.innerHTML = items.map(a => {
      const sevColor = a.severity === 'error' ? 'var(--color-danger)'
                     : a.severity === 'warn'  ? 'var(--color-warning)'
                     : 'var(--color-text-meta)';
      const sevWord = a.severity === 'error' ? 'Error'
                    : a.severity === 'warn'  ? 'Warning'
                    : 'Info';
      const label = CHECK_LABELS[a.check] || (a.check || '').replace(/_/g, ' ');
      const detail = translateDetail(a.detail);
      const remediation = a.remediation
        ? `<div style="font-size:11px;color:var(--color-text-meta);margin-top:2px">→ ${translateDetail(a.remediation)}</div>`
        : '';
      return `<li class="anomaly-item" style="padding:6px 4px;border-radius:3px">
        <span style="display:inline-block;min-width:60px;color:${sevColor};font-weight:600;font-size:11px;text-transform:uppercase">${sevWord}</span>
        <b>${label}</b> — ${detail}
        ${remediation}
      </li>`;
    }).join('');
  }

  // ========================================================================
  // Scope selector + scope-dependent UI refresh
  // ========================================================================

  function populateScopeSelector() {
    const sel = document.getElementById('scope-select');
    sel.innerHTML = '';
    const markets = STATE.data.global?.market_list || MPE.ALL_MARKETS;
    const regions = STATE.data.global?.region_list || MPE.ALL_REGIONS;
    const mktGrp = document.createElement('optgroup'); mktGrp.label = 'Markets';
    for (const m of markets) {
      const o = document.createElement('option'); o.value = m; o.textContent = m;
      mktGrp.appendChild(o);
    }
    sel.appendChild(mktGrp);
    const regGrp = document.createElement('optgroup'); regGrp.label = 'Regions';
    for (const r of regions) {
      const o = document.createElement('option'); o.value = r; o.textContent = r;
      regGrp.appendChild(o);
    }
    sel.appendChild(regGrp);
    sel.value = DEFAULT_SCOPE;
  }

  function currentScope() { return document.getElementById('scope-select').value; }
  function currentPeriod() { return document.getElementById('period-select').value; }
  function currentDriver() { return document.getElementById('driver-select').value; }
  function currentTargetValue() {
    const raw = document.getElementById('target-input').value;
    const n = parseFloat(raw);
    // Bound: ieccp 1-200%, spend/regs 0-1e12. Clamp silently; UI-layer clamping
    // prevents downstream NaN chains but we also show the validated value back.
    if (!Number.isFinite(n) || n < 0) return 0;
    return n;
  }

  function validateTargetInput() {
    const el = document.getElementById('target-input');
    const driver = currentDriver();
    const raw = el.value;
    const n = parseFloat(raw);
    const errEl = document.getElementById('target-input-error');
    let errMsg = '';
    if (raw !== '' && !Number.isFinite(n)) {
      errMsg = 'Enter a number.';
    } else if (Number.isFinite(n) && n < 0) {
      errMsg = `Target can't be negative.`;
    } else if (driver === 'ieccp' && Number.isFinite(n) && (n < 1 || n > 200)) {
      errMsg = `Efficiency target should be 1–200%.`;
    } else if (driver === 'spend' && Number.isFinite(n) && n > 1e10) {
      errMsg = `Spend target exceeds $10B — likely a typo.`;
    } else if (driver === 'regs' && Number.isFinite(n) && n > 1e8) {
      errMsg = `Registrations target exceeds 100M — likely a typo.`;
    } else if (driver === 'rollup') {
      // Regions ignore the input; no error needed
    }
    if (errEl) {
      errEl.textContent = errMsg;
      errEl.style.display = errMsg ? '' : 'none';
    }
    el.setAttribute('aria-invalid', errMsg ? 'true' : 'false');
    return errMsg === '';
  }

  function refreshScopeDependentUI() {
    const scope = currentScope();
    const isRegion = MPE.ALL_REGIONS.includes(scope);
    const md = isRegion ? null : (STATE.data.markets || {})[scope];

    // Driver options: scope-specific supported_target_modes
    let supported = ['ieccp', 'spend', 'regs'];
    if (isRegion) {
      supported = ['rollup'];   // regions are rollups, not drivers (v5 refactor)
    } else if (md?.parameters?.supported_target_modes?.value_json) {
      supported = md.parameters.supported_target_modes.value_json;
    }
    const driverSel = document.getElementById('driver-select');
    const prev = driverSel.value;
    driverSel.innerHTML = '';
    for (const mode of supported) {
      const opt = document.createElement('option');
      opt.value = mode;
      opt.textContent = mode === 'ieccp' ? 'Efficiency (%)'
        : mode === 'spend' ? 'Spend ($)'
          : mode === 'regs' ? 'Registrations'
            : mode === 'rollup' ? 'Rollup (sum of children)' : mode;
      driverSel.appendChild(opt);
    }
    driverSel.value = supported.includes(prev) ? prev
      : (supported.includes('ieccp') ? 'ieccp' : supported[0]);

    // Hide driver+target inputs for regions (rollup is computed, not a target)
    // — the inputs are purely cosmetic for rollup mode. Hide rather than delete
    // so toggling back to a market restores them.
    const driverGroup = driverSel.closest('.control-group');
    const targetInputEl = document.getElementById('target-input');
    const targetGroup = targetInputEl?.closest('.control-group');
    if (isRegion) {
      if (driverGroup) driverGroup.style.display = 'none';
      if (targetGroup) targetGroup.style.display = 'none';
    } else {
      if (driverGroup) driverGroup.style.display = '';
      if (targetGroup) targetGroup.style.display = '';
    }

    // Hide EFFICIENCY tile for markets that don't support ie%CCP (JP, AU) —
    // showing a number that Kate will treat as committed when the market has
    // explicitly dropped the commitment is worse than hiding it.
    const ieTile = document.getElementById('kpi-tile-ieccp');
    if (ieTile) {
      const hideIe = !isRegion && md && !supported.includes('ieccp');
      ieTile.style.display = hideIe ? 'none' : '';
    }

    // Seed default target value based on driver + market
    seedTargetValue();

    // Scenario chips (seeded w/ regime scenarios — hook for Phase 6.4)
    renderScenarioChips(md);

    // Regional constituents panel
    const consPanel = document.getElementById('constituents-panel');
    if (isRegion) consPanel.style.display = '';
    else consPanel.style.display = 'none';

    // Header scope meta
    updateHeaderMeta();
  }

  function seedTargetValue() {
    const scope = currentScope();
    const driver = currentDriver();
    const md = (STATE.data.markets || {})[scope];
    const input = document.getElementById('target-input');
    if (driver === 'ieccp') {
      const tgt = md?.parameters?.ieccp_target?.value_scalar;
      input.value = tgt ? Math.round(tgt * 100) : DEFAULT_TARGET_VALUE;
      input.step = '1';
      input.min = '1';
      input.max = '200';
    } else if (driver === 'spend') {
      // OP2 annual spend target first; fall back to YTD run-rate × 52
      const op2Spend = md?.op2_targets?.annual_spend_target;
      if (op2Spend) {
        input.value = Math.round(op2Spend);
      } else {
        const ytd = md?.ytd_weekly || [];
        if (ytd.length >= 4) {
          const last4 = ytd.slice(-4);
          const avg = last4.reduce((s, w) => s + (w.brand_cost || 0) + (w.nb_cost || 0), 0) / 4;
          input.value = Math.round(avg * 52 / 1000) * 1000;
        } else {
          input.value = 500000;
        }
      }
      input.step = '1000';
      input.min = '0';
      input.max = '1e11';
    } else if (driver === 'regs') {
      // OP2 annual regs target first; fall back to YTD run-rate × 52
      const op2Regs = md?.op2_targets?.annual_regs_target;
      if (op2Regs) {
        input.value = Math.round(op2Regs);
      } else {
        const ytd = md?.ytd_weekly || [];
        if (ytd.length >= 4) {
          const last4 = ytd.slice(-4);
          const avg = last4.reduce((s, w) => s + (w.brand_regs || 0) + (w.nb_regs || 0), 0) / 4;
          input.value = Math.round(avg * 52);
        } else {
          input.value = 50000;
        }
      }
      input.step = '100';
      input.min = '0';
      input.max = '1e9';
    } else if (driver === 'rollup') {
      input.value = 0;
      input.step = '1';
      input.min = '';
      input.max = '';
    }
    validateTargetInput();
  }

  function updateHeaderMeta() {
    const scope = currentScope();
    const period = currentPeriod();
    const driver = currentDriver();
    const v = currentTargetValue();
    const driverText = driver === 'ieccp' ? `${v}% efficiency`
      : driver === 'spend' ? `${fmt$(v)} spend`
        : driver === 'regs' ? `${fmtNum(v)} regs`
          : `rollup`;
    document.getElementById('header-scope-meta').textContent = `${scope} · ${period} · ${driverText} target`;

    // Elevated market badge (Round 4 Part 4) — prominent market + period + target
    // right above the hero number so users can't miss it when switching markets.
    const nameEl = document.getElementById('hero-market-name');
    const periodEl = document.getElementById('hero-market-period');
    const targetEl = document.getElementById('hero-market-target');
    if (nameEl) nameEl.textContent = scope;
    if (periodEl) periodEl.textContent = humanPeriodLong(period);
    if (targetEl) {
      if (driver === 'ieccp') targetEl.textContent = `${v}% efficiency target`;
      else if (driver === 'spend') targetEl.textContent = `${fmt$(v)} spend target`;
      else if (driver === 'regs') targetEl.textContent = `${fmtNum(v)} registrations target`;
      else if (driver === 'rollup') {
        // Round 5 V-5: "rollup target" was meaningless. Show the constituents.
        const regionMarkets = (MPE && MPE.REGION_CONSTITUENTS && MPE.REGION_CONSTITUENTS[scope]) || [];
        targetEl.textContent = regionMarkets.length
          ? `rollup of ${regionMarkets.join(' + ')}`
          : `region rollup`;
      } else {
        targetEl.textContent = 'target';
      }
    }
  }

  // Map period codes (W17, M04, Q2, Y2026, MY1, MY2) to human labels.
  function humanPeriodLong(p) {
    if (!p) return 'this year';
    const up = String(p).toUpperCase();
    if (up.startsWith('MY')) {
      const n = parseInt(up.slice(2), 10);
      return Number.isFinite(n) ? `Next ${n} year${n === 1 ? '' : 's'}` : 'Multi-year';
    }
    if (up.startsWith('W')) return `Week ${up.slice(1)}`;
    if (up.startsWith('M')) return `${['','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'][parseInt(up.slice(1), 10)] || up}`;
    if (up.startsWith('Q')) return `Q${up.slice(1)}`;
    if (up.startsWith('Y')) return `Year ${up.slice(1)}`;
    return up;
  }

  // ========================================================================
  // Scenario chips — four methodological stances, market-agnostic
  // ========================================================================
  //
  //   Current plan (Mixed) → default engine fit
  //       Bayesian anchor (recent actuals) + frequentist forward decay from
  //       fit_state. The engine's current best estimate.
  //
  //   Frequentist → "recent actuals extrapolated forward, no assumed uplift"
  //       Anchor holds at the recent-actuals level, forward regime stream is
  //       suppressed (peak_multiplier = 1.0). What the last 8 weeks say.
  //
  //   Bayesian → "full prior trust in authored campaign effects"
  //       Authored peak holds permanently, full confidence, no decay.
  //       What leadership hopes is true about the current lift.
  //
  //   No lift → "strip the anchor lift — what this market would do without
  //       any current campaign effects"
  //       Divides anchor by baseline regime_mult to expose the hypothetical
  //       pre-lift baseline. Useful to see how much of recent trajectory is
  //       campaign-driven vs structural.

  function buildScenarioChips(marketData) {
    const regimes = marketData?.regime_fit_state || [];
    // All four chips available regardless of market — no per-market customization
    // (was a maintenance burden). Semantic meaning is the same everywhere.
    const chips = [
      { id: 'mixed',       label: 'Planned', override: null,
        description: 'Default engine fit: recent actuals anchor + observed decay from campaign lifts. The engine\'s current best estimate.' },
      { id: 'frequentist', label: 'Pessimistic',          override: { peak_multiplier: 1.0 },
        description: 'Recent actuals extrapolated forward. No assumed uplift from active campaigns. "What the last 8 weeks say."' },
      { id: 'bayesian',    label: 'Optimistic',             override: { half_life_weeks: null, force_confidence: 1.0 },
        description: 'Full trust in the campaign lift: authored peak holds permanently at full confidence, no decay.' },
      { id: 'no-lift',     label: 'Baseline only',              override: { peak_multiplier: 1.0, strip_anchor_lift: true },
        description: 'Strip the campaign lift from the anchor. Hypothetical: what this market would do without any current campaign effects.' },
    ];
    return chips;
  }

  function renderScenarioChips(marketData) {
    const wrap = document.getElementById('scenario-chips');
    wrap.innerHTML = '';
    const chips = buildScenarioChips(marketData);
    STATE.activeChipId = STATE.activeChipId || 'mixed';
    for (const chip of chips) {
      const el = document.createElement('div');
      el.className = 'chip';
      el.textContent = chip.label;
      if (chip.id === STATE.activeChipId) el.classList.add('active');
      el.title = chip.description || '';
      el.onclick = () => {
        const prevTotals = STATE.currentOutput?.totals;
        STATE.activeChipId = chip.id;
        STATE.scenarioOverride = chip.override;
        document.querySelectorAll('.chip').forEach(c => c.classList.remove('active'));
        el.classList.add('active');
        scheduleRecompute();
        // Defer animation trigger until after recompute lands
        setTimeout(() => {
          animateHeroTransition(prevTotals, STATE.currentOutput?.totals);
        }, 250);
      };
      wrap.appendChild(el);
    }
  }

  // ========================================================================
  // Recompute orchestration — drives loading stages + projection
  // ========================================================================

  let recomputeTimer = null;
  function scheduleRecompute() {
    clearTimeout(recomputeTimer);
    updateHeaderMeta();
    recomputeTimer = setTimeout(() => recompute({ animated: false }), 150);
  }

  // Compute a Set of ISO week numbers covered by the selected period string.
  // Mirrors the convention from MPE.parseTimePeriod in mpe_engine.js.
  function periodWeeksSet(periodStr) {
    if (!periodStr) return null;
    const tp = periodStr.toUpperCase();
    if (tp.startsWith('Y') || tp.startsWith('MY')) return null;   // full-year
    const s = new Set();
    if (tp.startsWith('W')) {
      const w = parseInt(tp.slice(1), 10);
      if (Number.isInteger(w) && w >= 1 && w <= 53) s.add(w);
    } else if (tp.startsWith('M')) {
      const m = parseInt(tp.slice(1), 10);
      if (Number.isInteger(m) && m >= 1 && m <= 12) {
        const a = Math.round((m - 1) * 52 / 12) + 1;
        const b = Math.round(m * 52 / 12);
        for (let w = a; w <= b; w++) s.add(w);
      }
    } else if (tp.startsWith('Q')) {
      const q = parseInt(tp.slice(1), 10);
      const boundaries = [[1, 13], [14, 27], [28, 40], [41, 52]];
      if (q >= 1 && q <= 4) {
        const [a, b] = boundaries[q - 1];
        for (let w = a; w <= b; w++) s.add(w);
      }
    }
    return s.size ? s : null;
  }

  async function recompute(opts) {
    opts = opts || {};
    const scope = currentScope();
    const period = currentPeriod();
    const driver = currentDriver();
    const targetValue = currentTargetValue();
    const isRegion = MPE.ALL_REGIONS.includes(scope);
    const periodWeeks = periodWeeksSet(period);

    // Use V1_1_Slim directly for market-level (matches Python engine output)
    const regimeMultiplier = STATE.regimeMultiplier;
    const scenarioOverride = STATE.scenarioOverride;

    if (opts.animated !== false) {
      await showLoadingAnimated();
    } else {
      showLoading(false);
    }
    await setStage(1, opts.animated !== false);

    if (isRegion) {
      // Region: aggregate constituent markets via V1_1_Slim, not old MPE path
      const consts = MPE.REGION_CONSTITUENTS[scope] || [];
      const perMarket = [];
      for (const mkt of consts) {
        const md = (STATE.data.markets || {})[mkt];
        if (!md) continue;
        const supported = md.parameters?.supported_target_modes?.value_json || ['spend'];
        let effDriver = driver === 'rollup'
          ? (supported.includes('ieccp') ? 'ieccp' : 'spend')
          : driver;
        if (!supported.includes(effDriver)) effDriver = supported[0];
        const ieTgt = md.parameters?.ieccp_target?.value_scalar;
        const op2Spend = md.op2_targets?.annual_spend_target;
        let effTarget = effDriver === 'ieccp' ? (ieTgt ? ieTgt * 100 : 75)
          : effDriver === 'spend' ? (op2Spend || 500000)
          : (md.op2_targets?.annual_regs_target || 5000);
        try {
          const out = V1_1_Slim.projectWithLockedYtd(
            md, 2026, effDriver, effTarget,
            { regimeMultiplier, scenarioOverride, periodWeeks, periodType: period }
          );
          perMarket.push({ market: mkt, out });
        } catch (e) {
          console.error(`Region ${scope} market ${mkt} failed:`, e);
        }
      }
      hideLoading();
      renderRegionalV1(scope, period, perMarket, consts);
      return;
    }

    const md = (STATE.data.markets || {})[scope];
    if (!md) {
      showBanner('danger', `No data for ${scope}.`);
      hideLoading();
      return;
    }

    let projection;
    try {
      projection = V1_1_Slim.projectWithLockedYtd(
        md, 2026, driver, targetValue,
        { regimeMultiplier, scenarioOverride, periodWeeks, periodType: period }
      );
    } catch (e) {
      console.error('projection failed:', e);
      projection = { error: String(e), warnings: [String(e)], ytd: {}, totals: {} };
    }

    await setStage(2, opts.animated !== false);
    await setStage(3, opts.animated !== false);

    // Counterfactual — same projection with regime_multiplier = 0
    let counterfactual = null;
    if (md.regime_fit_state && md.regime_fit_state.length > 0) {
      try {
        counterfactual = V1_1_Slim.projectWithLockedYtd(
          md, 2026, driver, targetValue,
          { regimeMultiplier: 0, periodWeeks, periodType: period }
        );
      } catch (e) {
        // Silent — counterfactual is optional
      }
    }

    // Monte Carlo CI band from MPE engine (cheap version) — full year scope
    await setStage(4, opts.animated !== false);

    let uncert = null;
    try {
      const inputs = { scope, timePeriod: period, targetMode: driver, targetValue, rngSeed: 42 };
      uncert = await MPE.projectWithUncertainty(inputs, STATE.data);
    } catch (e) {
      // Ignore — CI band optional
    }

    STATE.currentOutput = projection;
    STATE.currentUncertainty = uncert?.credible_intervals || null;
    STATE.currentBrandProj = projection;
    STATE.currentCounterfactual = counterfactual;

    hideLoading();
    // 6.5.3: attach projection_id for feedback FK + increment session counter
    projection._projection_id = `proj-${scope}-${Date.now()}`;
    incrementProjectionCount();
    maybeShowFeedbackBar();
    renderMarket(projection, counterfactual, uncert, md);
  }

  // ========================================================================
  // Loading states (principle #8)
  // ========================================================================

  const STAGE_MIN_MS = 700;

  function showLoading(animated) {
    STATE.loading = true;
    const ov = document.getElementById('loading-overlay');
    ov.classList.add('active');
    // Reset stages
    document.querySelectorAll('.loading-stage').forEach(s => s.classList.remove('active', 'done'));
  }
  function hideLoading() {
    STATE.loading = false;
    const ov = document.getElementById('loading-overlay');
    ov.classList.remove('active');
  }
  async function showLoadingAnimated() {
    showLoading(true);
    await new Promise(r => setTimeout(r, 100));
  }
  async function setStage(n, animated) {
    document.querySelectorAll('.loading-stage').forEach((s, i) => {
      const stageN = parseInt(s.dataset.stage, 10);
      if (stageN < n) s.classList.add('done');
      else s.classList.remove('done');
      if (stageN === n) s.classList.add('active');
      else s.classList.remove('active');
    });
    if (animated) {
      await new Promise(r => setTimeout(r, STAGE_MIN_MS));
    }
  }

  // ========================================================================
  // Market-level render — hero + chart + contribution + tooltips
  // ========================================================================

  function renderMarket(out, counterfactual, uncert, marketData) {
    if (out.error) {
      document.getElementById('hero-number').textContent = '—';
      document.getElementById('hero-context').textContent = `Error: ${out.error}`;
      return;
    }
    const t = out.totals || {};

    // Hero: show Spend and Regs as co-hero (both large numbers), regardless of driver
    const spendLine = document.getElementById('hero-number');
    const regsLine = document.getElementById('hero-secondary');
    spendLine.textContent = fmt$(t.total_spend);
    document.getElementById('hero-unit').textContent = 'spend';
    if (regsLine) {
      regsLine.textContent = fmtNum(t.total_regs);
      const regsUnit = document.getElementById('hero-secondary-unit');
      if (regsUnit) regsUnit.textContent = 'regs';
    }

    // Context sentence — plain language, no "regime" jargon
    const scope = currentScope();
    const period = currentPeriod();
    const driver = currentDriver();
    const targetVal = currentTargetValue();
    let contextSent = '';
    if (driver === 'ieccp') {
      contextSent = `Projected ${scope} ${period} to hit ${targetVal}% efficiency. `;
    } else if (driver === 'spend') {
      contextSent = `Projected ${scope} ${period} outcomes at $${fmtNum(targetVal)} total spend. `;
    } else if (driver === 'regs') {
      contextSent = `Projected ${scope} ${period} spend to deliver ${fmtNum(targetVal)} registrations. `;
    }
    const activeLifts = (marketData.regime_fit_state || []).filter(r => r.confidence > 0);
    if (activeLifts.length > 0) {
      contextSent += `${activeLifts.length} campaign lift${activeLifts.length > 1 ? 's' : ''} active.`;
    }
    document.getElementById('hero-context').textContent = contextSent;

    // Secondary KPI strip — drop total-spend (it's the hero) and show complements
    document.getElementById('kpi-brand-regs').textContent = fmtNum(t.brand_regs);
    document.getElementById('kpi-nb-regs').textContent = fmtNum(t.nb_regs);
    document.getElementById('kpi-cpa').textContent = fmt$(t.blended_cpa);
    const ieEl = document.getElementById('kpi-ieccp');
    ieEl.textContent = t.computed_ieccp != null ? fmtPct(t.computed_ieccp) : 'n/a';
    ieEl.classList.remove('warn', 'danger');
    if (t.computed_ieccp != null) {
      if (t.computed_ieccp > 120) ieEl.classList.add('danger');
      else if (t.computed_ieccp > 100) ieEl.classList.add('warn');
    }
    // Both OP2 KPIs visible — Spend and Regs independent tiles.
    // For period-scoped comparisons, scale OP2 annual by period-share of year
    // (simple proportional; monthly OP2 breakdown is in the data but period
    // share from current period output is a clean enough approximation).
    const op2Spend = marketData.op2_targets?.annual_spend_target;
    const op2Regs = marketData.op2_targets?.annual_regs_target;
    const periodShare = t.annual_total_regs > 0 ? t.total_regs / t.annual_total_regs : 1.0;

    const spendEl = document.getElementById('kpi-op2-spend');
    const regsEl = document.getElementById('kpi-op2-regs');
    spendEl.classList.remove('warn', 'danger');
    regsEl.classList.remove('warn', 'danger');
    if (op2Spend && op2Spend > 0) {
      const scaled = op2Spend * periodShare;
      const pct = scaled > 0 ? (t.total_spend / scaled) * 100 : 0;
      spendEl.textContent = `${pct.toFixed(0)}%`;
      if (pct > 120) spendEl.classList.add('danger'); else if (pct > 105) spendEl.classList.add('warn');
    } else {
      spendEl.textContent = '—';
    }
    if (op2Regs && op2Regs > 0) {
      const scaled = op2Regs * periodShare;
      const pct = scaled > 0 ? (t.total_regs / scaled) * 100 : 0;
      regsEl.textContent = `${pct.toFixed(0)}%`;
      if (pct < 85) regsEl.classList.add('danger'); else if (pct < 95) regsEl.classList.add('warn');
    } else {
      regsEl.textContent = '—';
    }

    // Apply animated arrival classes
    spendLine.classList.remove('arrival-brand');
    void spendLine.offsetWidth;
    spendLine.classList.add('arrival-total');

    renderChart(out, counterfactual, uncert, marketData);
    renderContributionBar(out, marketData);
    renderFitQuality(marketData, out);
    renderWarnings(out);
    renderSavedList();
    renderYtdWallBanner(out);
    renderDrawer(out, marketData);
    renderNarrativeStandard();   // always-visible narrative at bottom
    renderMarketAnomalies(currentScope());
    updateHeaderMeta();
  }

  function renderNarrativeStandard() {
    // Narrative panel is now always visible at bottom (no disclosure gate)
    const panel = document.getElementById('narrative-panel');
    if (panel) panel.style.display = '';
    if (STATE.currentOutput) generateNarrative();
  }

  // ========================================================================
  // Regional render — simpler (rollup, no chart fit)
  // ========================================================================

  function renderRegional(out) {
    // LEGACY: kept for save/load backward-compat with old MPE shape.
    // New regional path goes through renderRegionalV1 below.
    const t = out.totals || {};
    document.getElementById('hero-number').textContent = fmt$(t.total_spend);
    document.getElementById('hero-unit').textContent = 'total spend';
    document.getElementById('hero-context').textContent =
      `${out.scope} = ${out.constituent_markets?.map(c => c.market).join(' + ') || 'rollup'}. Target mode: rollup (sum of children).`;
    document.getElementById('kpi-brand-regs').textContent = fmtNum(t.brand_regs);
    document.getElementById('kpi-nb-regs').textContent = fmtNum(t.nb_regs);
    document.getElementById('kpi-cpa').textContent = fmt$(t.blended_cpa);
    document.getElementById('kpi-ieccp').textContent = t.ieccp != null ? fmtPct(t.ieccp) : 'n/a';
    document.getElementById('kpi-spend').textContent = fmt$(t.total_spend);

    // Render constituent table
    const tbody = document.getElementById('constituents-body');
    tbody.innerHTML = '';
    for (const c of (out.constituent_markets || [])) {
      const row = document.createElement('tr');
      row.innerHTML = `<td>${c.market}</td><td>${fmtNum(c.brand_regs + c.nb_regs)}</td><td>${fmt$(c.total_spend)}</td><td>${c.ieccp != null ? fmtPct(c.ieccp) : 'n/a'}</td>`;
      tbody.appendChild(row);
    }

    // Clear primary chart (not meaningful at region scope — keep sum-bar)
    const chartEl = document.getElementById('chart-primary');
    chartEl.innerHTML = `<div style="text-align:center;padding:var(--gap-xl);color:var(--color-text-meta);font-size:13px">Regional projections are rollups of constituent markets — see breakdown below.<br>Drill into a market to see trajectory detail.</div>`;

    renderWarnings(out);
    renderSavedList();
  }

  function renderRegionalV1(regionName, period, perMarket, constituentNames) {
    // Aggregate per-market V1_1_Slim outputs into a region-level shape that
    // the chart/hero/contribution rendering can consume. Sum period totals
    // across markets; compute region-level ie%CCP via sum-then-divide.
    const t = {
      brand_regs: 0, brand_spend: 0,
      nb_regs: 0, nb_spend: 0,
      total_regs: 0, total_spend: 0,
      annual_brand_regs: 0, annual_brand_spend: 0,
      annual_nb_regs: 0, annual_nb_spend: 0,
      annual_total_regs: 0, annual_total_spend: 0,
      computed_ieccp: null,
    };
    let ieccp_numerator = 0;   // Σ spend
    let ieccp_denominator = 0; // Σ (regs × CCP)
    const yearWeekly = {
      ytd_weeks: 0,
      brand_regs: [], brand_spend: [],
      nb_regs: [], nb_spend: [],
    };
    let maxYtd = 0;
    let maxLen = 0;
    for (const { market, out } of perMarket) {
      if (!out || !out.totals) continue;
      const ot = out.totals;
      t.brand_regs += ot.brand_regs || 0;
      t.brand_spend += ot.brand_spend || 0;
      t.nb_regs += ot.nb_regs || 0;
      t.nb_spend += ot.nb_spend || 0;
      t.total_regs += ot.total_regs || 0;
      t.total_spend += ot.total_spend || 0;
      t.annual_brand_regs += ot.annual_brand_regs || 0;
      t.annual_brand_spend += ot.annual_brand_spend || 0;
      t.annual_nb_regs += ot.annual_nb_regs || 0;
      t.annual_nb_spend += ot.annual_nb_spend || 0;
      t.annual_total_regs += ot.annual_total_regs || 0;
      t.annual_total_spend += ot.annual_total_spend || 0;
      // ie%CCP components
      const md = (STATE.data.markets || {})[market];
      const brandCcp = md?.parameters?.brand_ccp?.value_scalar;
      const nbCcp = md?.parameters?.nb_ccp?.value_scalar;
      if (brandCcp != null && nbCcp != null) {
        ieccp_numerator += (ot.brand_spend || 0) + (ot.nb_spend || 0);
        ieccp_denominator += ((ot.brand_regs || 0) * brandCcp) + ((ot.nb_regs || 0) * nbCcp);
      }
      // Year weekly arrays: sum element-wise
      if (out.year_weekly) {
        const yw = out.year_weekly;
        maxLen = Math.max(maxLen, yw.brand_regs.length);
        maxYtd = Math.max(maxYtd, yw.ytd_weeks);
        for (let i = 0; i < yw.brand_regs.length; i++) {
          yearWeekly.brand_regs[i] = (yearWeekly.brand_regs[i] || 0) + (yw.brand_regs[i] || 0);
          yearWeekly.brand_spend[i] = (yearWeekly.brand_spend[i] || 0) + (yw.brand_spend[i] || 0);
          yearWeekly.nb_regs[i] = (yearWeekly.nb_regs[i] || 0) + (yw.nb_regs[i] || 0);
          yearWeekly.nb_spend[i] = (yearWeekly.nb_spend[i] || 0) + (yw.nb_spend[i] || 0);
        }
      }
    }
    yearWeekly.ytd_weeks = maxYtd;
    if (ieccp_denominator > 0) {
      t.computed_ieccp = (ieccp_numerator / ieccp_denominator) * 100;
    }
    t.blended_cpa = t.total_regs > 0 ? t.total_spend / t.total_regs : 0;

    // Construct a synthetic "regional market" object for the standard market render path.
    // Weekly actuals for the region = sum of all constituent weekly rows (for chart).
    // YTD week dates come from MX (or first market that has data) — they align.
    const firstMd = perMarket[0]?.out;
    const ytdDates = [];
    for (const { market } of perMarket) {
      const md = (STATE.data.markets || {})[market];
      if (md?.ytd_weekly?.length > ytdDates.length) {
        md.ytd_weekly.forEach(w => ytdDates.push(w.period_start));
      }
      if (ytdDates.length === maxYtd) break;
    }

    const syntheticYtdWeekly = [];
    for (let i = 0; i < maxYtd; i++) {
      syntheticYtdWeekly.push({
        period_start: ytdDates[i],
        brand_regs: yearWeekly.brand_regs[i] || 0,
        nb_regs: yearWeekly.nb_regs[i] || 0,
        brand_cost: yearWeekly.brand_spend[i] || 0,
        nb_cost: yearWeekly.nb_spend[i] || 0,
      });
    }

    // Aggregate brand_trajectory_y2026 for chart (sum across markets)
    const syntheticBt = { regs_per_week: [], spend_per_week: [], weeks: null, brand_cpa_used: 0 };
    let cpaWeighted = 0, cpaWeight = 0;
    for (const { market } of perMarket) {
      const md = (STATE.data.markets || {})[market];
      const bt = md?.brand_trajectory_y2026;
      if (!bt) continue;
      if (!syntheticBt.weeks) syntheticBt.weeks = bt.weeks;
      for (let i = 0; i < bt.regs_per_week.length; i++) {
        syntheticBt.regs_per_week[i] = (syntheticBt.regs_per_week[i] || 0) + (bt.regs_per_week[i] || 0);
        syntheticBt.spend_per_week[i] = (syntheticBt.spend_per_week[i] || 0) + (bt.spend_per_week[i] || 0);
      }
      cpaWeighted += (bt.brand_cpa_used || 0) * (bt.regs_per_week.reduce((a, b) => a + b, 0) || 0);
      cpaWeight += bt.regs_per_week.reduce((a, b) => a + b, 0) || 0;
    }
    syntheticBt.brand_cpa_used = cpaWeight > 0 ? cpaWeighted / cpaWeight : 0;

    // Synthetic region "marketData" shaped for renderMarket
    const syntheticMd = {
      ytd_weekly: syntheticYtdWeekly,
      brand_trajectory_y2026: syntheticBt,
      regime_fit_state: [],   // regional doesn't apply specific lifts
      parameters: { ieccp_target: null },
      op2_targets: (() => {
        let aSpend = 0, aRegs = 0, any = false;
        for (const { market } of perMarket) {
          const op2 = (STATE.data.markets || {})[market]?.op2_targets;
          if (op2) {
            aSpend += op2.annual_spend_target || 0;
            aRegs += op2.annual_regs_target || 0;
            any = true;
          }
        }
        return any ? { annual_spend_target: aSpend, annual_regs_target: aRegs, year: 2026 } : null;
      })(),
      fallback_summary: 'regional_rollup',
      fit_quality: null,
    };

    // Build a faux V1_1_Slim.projectWithLockedYtd-shaped output
    const fauxOut = {
      year: 2026,
      target_mode: 'rollup',
      target_value: 0,
      period: period,
      ytd: { brand_regs: 0, brand_spend: 0, nb_regs: 0, nb_spend: 0 },
      roy: {},
      year_weekly: yearWeekly,
      totals: t,
      contribution_breakdown: { seasonal: 0.40, trend: 0.40, regime: 0.15, qualitative: 0.05 },
      warnings: [],
      regime_stack: [],
    };

    // Populate hero/KPIs/chart via the standard path
    STATE.currentOutput = fauxOut;
    STATE.currentBrandProj = fauxOut;
    STATE.currentCounterfactual = null;
    STATE.currentUncertainty = null;
    renderMarket(fauxOut, null, null, syntheticMd);

    // Override hero context and show constituent table
    document.getElementById('hero-context').textContent =
      `${regionName} · ${period} · rollup of ${constituentNames.join(' + ')}`;

    const consPanel = document.getElementById('constituents-panel');
    consPanel.style.display = '';
    const tbody = document.getElementById('constituents-body');
    tbody.innerHTML = '';
    for (const { market, out } of perMarket) {
      const ot = out.totals || {};
      const row = document.createElement('tr');
      row.innerHTML = `<td>${market}</td><td>${fmtNum(ot.total_regs)}</td><td>${fmt$(ot.total_spend)}</td><td>${ot.computed_ieccp != null ? fmtPct(ot.computed_ieccp) : 'n/a'}</td>`;
      tbody.appendChild(row);
    }
  }

  // ========================================================================
  // Primary chart (Plot + D3) — task 6.3.3, 6.3.5, 6.3.6
  // ========================================================================

  function renderChart(out, counterfactual, uncert, marketData) {
    const chartEl = document.getElementById('chart-primary');
    chartEl.innerHTML = '';

    const ytdWeeks = (marketData.ytd_weekly || []).map(w => ({
      date: new Date(w.period_start),
      brand_regs: w.brand_regs || w.brand_registrations || 0,
      nb_regs: w.nb_regs || w.nb_registrations || 0,
      brand_spend: w.brand_cost || w.brand_spend || 0,
      nb_spend: w.nb_cost || w.nb_spend || 0,
      locked: true,
    }));

    const bt = marketData.brand_trajectory_y2026;
    if (!bt) {
      chartEl.innerHTML = `<div style="text-align:center;padding:var(--gap-xl);color:var(--color-text-meta)">Brand trajectory not yet exported for this market.</div>`;
      return;
    }

    // Compose full-year weekly series from YTD actuals + Brand trajectory RoY + solved NB RoY
    const ytdCount = ytdWeeks.length;
    const btWeeks = bt.weeks.map(ws => new Date(ws));
    const brandRoyRegs = bt.regs_per_week.slice(ytdCount);
    const brandRoySpend = bt.spend_per_week.slice(ytdCount);
    const royWeeks = btWeeks.slice(ytdCount);

    // Distribute NB spend/regs across RoY weeks evenly (matching V1_1_Slim aggregation)
    const royNbSpend = (out.roy?.nb_spend || 0) / (royWeeks.length || 1);
    const royNbRegs = (out.roy?.nb_regs || 0) / (royWeeks.length || 1);

    // Build unified chart data
    const chartData = [];
    for (let i = 0; i < ytdWeeks.length; i++) {
      chartData.push({ ...ytdWeeks[i], week: ytdWeeks[i].date, series: 'actual', isoWeek: fmtIsoWeek(ytdWeeks[i].date) });
    }
    for (let i = 0; i < royWeeks.length; i++) {
      chartData.push({
        date: royWeeks[i],
        week: royWeeks[i],
        brand_regs: brandRoyRegs[i] || 0,
        nb_regs: royNbRegs,
        brand_spend: brandRoySpend[i] || 0,
        nb_spend: royNbSpend,
        locked: false,
        isoWeek: fmtIsoWeek(royWeeks[i]),
        series: 'projected',
      });
    }

    // Seam the Brand projection line to start from the last YTD actual so
    // the chart doesn't show a visual cliff between locked data and the
    // forecast. This is a rendering adjustment only — the underlying
    // projection math stays untouched (V1_1_Slim.projectWithLockedYtd
    // separately composes YTD actuals + RoY). The seam prevents the
    // "projection starts at 250 when actuals just ended at 395" confusion.
    if (ytdWeeks.length > 0 && chartData.length > ytdWeeks.length) {
      const lastYtd = ytdWeeks[ytdWeeks.length - 1];
      const firstProjIdx = ytdWeeks.length;
      const firstProj = chartData[firstProjIdx];
      if (firstProj && lastYtd.brand_regs > 0) {
        // Scale all projected Brand weeks so the first week matches the last
        // YTD week smoothly, fading the scale back to 1.0 over 8 weeks
        const scale0 = lastYtd.brand_regs / Math.max(firstProj.brand_regs, 1);
        const fadeWeeks = 8;
        for (let i = firstProjIdx; i < chartData.length; i++) {
          const offset = i - firstProjIdx;
          const fade = offset < fadeWeeks ? scale0 + (1.0 - scale0) * (offset / fadeWeeks) : 1.0;
          chartData[i].brand_regs *= fade;
          chartData[i].brand_spend *= fade;
        }
      }
    }

    // Counterfactual — only use Brand
    let counterData = [];
    if (counterfactual?.ytd && counterfactual?.roy) {
      const cfBt = marketData.brand_trajectory_y2026;
      // Recompute counterfactual Brand per-week using V1_1_Slim.projectBrandTrajectory
      // For parity with counterfactual, we use baseline cfBt, but apply rm=0 for regime component
      const cfRegs = V1_1_Slim.projectBrandTrajectory(marketData, btWeeks, { regimeMultiplier: 0 });
      for (let i = 0; i < btWeeks.length; i++) {
        counterData.push({ week: btWeeks[i], brand_regs_cf: cfRegs.regs_per_week[i], isoWeek: fmtIsoWeek(btWeeks[i]) });
      }
    }

    // Target line (horizontal at ie%CCP equivalent or at target regs/spend)
    const driver = currentDriver();
    const targetVal = currentTargetValue();

    // Plot dimensions
    const width = Math.min(chartEl.clientWidth || 960, 1200);
    const height = CHART_HEIGHT;

    // Layered chart via Observable Plot
    const marks = [];

    // CI band (if Uncertainty disclosed + we have uncertainty data)
    if (STATE.disclosures.uncert && STATE.currentUncertainty) {
      const ci = STATE.currentUncertainty;
      const regsCi = ci.total_regs?.ci?.['90'];
      const spendCi = ci.total_spend?.ci?.['90'];
      // Approximate a per-week CI as pseudo-band from the projected series (simple +/- % fit)
      // This is approximate; full MC per-week would require more data in JSON export
      if (regsCi) {
        const projected = chartData.filter(d => d.series === 'projected');
        const centralTotal = projected.reduce((s, d) => s + d.brand_regs + d.nb_regs, 0);
        if (centralTotal > 0) {
          const ratioLo = regsCi[0] / centralTotal;
          const ratioHi = regsCi[1] / centralTotal;
          for (const d of projected) {
            d.ci_lo = (d.brand_regs + d.nb_regs) * ratioLo;
            d.ci_hi = (d.brand_regs + d.nb_regs) * ratioHi;
          }
          marks.push(Plot.areaY(projected, {
            x: 'week', y1: 'ci_lo', y2: 'ci_hi',
            fill: 'var(--color-ci-band-brand)', fillOpacity: 0.35,
          }));
        }
      }
    }

    // Locked-YTD wall — Plot.rect from data start to ytd_latest with light-grey fill
    const ytdLatest = ytdWeeks.length > 0 ? ytdWeeks[ytdWeeks.length - 1].date : null;
    const ytdFirst = ytdWeeks.length > 0 ? ytdWeeks[0].date : null;
    if (ytdLatest && ytdFirst) {
      marks.push(Plot.rect([{x1: ytdFirst, x2: ytdLatest}], {
        x1: 'x1', x2: 'x2', y1: 0, y2: 0,
        fill: 'var(--color-locked-ytd)', fillOpacity: 0.4,
      }));
      // vertical rule at the wall — bright contrast + label ("Today") so users
      // immediately see where actuals stop and the projection begins.
      marks.push(Plot.ruleX([ytdLatest], {
        stroke: 'var(--color-target)', strokeWidth: 2, strokeDasharray: '6,3', strokeOpacity: 0.85,
      }));
      marks.push(Plot.text([{x: ytdLatest, label: '↓ Today'}], {
        x: 'x', y: 0,
        text: 'label',
        dy: -6,
        textAnchor: 'start',
        fontWeight: 600,
        fontSize: 11,
        fill: 'var(--color-target)',
        frameAnchor: 'top',
      }));
    }

    // Compute spend-to-regs scaling factor so spend line fits in the regs
    // y-domain. Chart shows regs on y-axis primarily; spend is overlaid
    // scaled. Tooltip shows actual dollar values. This is a Plot-idiomatic
    // single-chart solution (Observable Plot doesn't natively do dual y-axes).
    let maxRegs = 0, maxSpend = 0;
    for (const d of chartData) {
      maxRegs = Math.max(maxRegs, d.brand_regs + d.nb_regs);
      maxSpend = Math.max(maxSpend, d.brand_spend + d.nb_spend);
    }
    const spendScale = maxSpend > 0 && maxRegs > 0 ? maxRegs / maxSpend : 1;

    // Actuals line (Brand + NB total regs, solid neutral-grey)
    const actualsPoints = chartData.filter(d => d.locked).map(d => ({
      week: d.week, total_regs: d.brand_regs + d.nb_regs,
      total_spend: d.brand_spend + d.nb_spend,
      total_spend_scaled: (d.brand_spend + d.nb_spend) * spendScale,
      isoWeek: d.isoWeek, brand_regs: d.brand_regs, nb_regs: d.nb_regs,
      brand_spend: d.brand_spend, nb_spend: d.nb_spend,
    }));
    marks.push(Plot.line(actualsPoints, {
      x: 'week', y: 'total_regs',
      stroke: 'var(--color-actuals)', strokeWidth: 2.5,
    }));
    // Actuals spend line (dashed grey, scaled to fit regs axis)
    if (maxSpend > 0) {
      marks.push(Plot.line(actualsPoints, {
        x: 'week', y: 'total_spend_scaled',
        stroke: 'var(--color-actuals)', strokeWidth: 2, strokeDasharray: '2,3', strokeOpacity: 0.7,
      }));
    }

    // Counterfactual (dashed grey) — only Brand regs w/o regime component
    if (STATE.disclosures.counter && counterData.length > 0) {
      marks.push(Plot.line(counterData, {
        x: 'week', y: 'brand_regs_cf',
        stroke: 'var(--color-counterfactual)', strokeWidth: 1.5, strokeDasharray: '5,4', strokeOpacity: 0.8,
      }));
    }

    // Projected Brand line (blue)
    const projPoints = chartData.filter(d => !d.locked).map(d => ({
      week: d.week, brand_regs: d.brand_regs, isoWeek: d.isoWeek,
      total_regs: d.brand_regs + d.nb_regs, nb_regs: d.nb_regs,
      brand_spend: d.brand_spend, nb_spend: d.nb_spend,
      total_spend: d.brand_spend + d.nb_spend,
      total_spend_scaled: (d.brand_spend + d.nb_spend) * spendScale,
      brand_spend_scaled: d.brand_spend * spendScale,
    }));
    marks.push(Plot.line(projPoints, {
      x: 'week', y: 'brand_regs',
      stroke: 'var(--color-brand)', strokeWidth: 2,
    }));

    // Projected Non-Brand — dedicated orange line so users see NB explicitly
    // rather than inferring it from Total minus Brand. Round 4 feedback C-1:
    // orange used to mean NB in the palette but was painting Total; now fixed.
    marks.push(Plot.line(projPoints, {
      x: 'week', y: 'nb_regs',
      stroke: 'var(--color-nb)', strokeWidth: 2,
    }));

    // Projected Total (Brand + NB) — thicker neutral-dark line as the
    // summary series. Distinct color from Brand/NB so it reads as an overlay.
    marks.push(Plot.line(projPoints, {
      x: 'week', y: 'total_regs',
      stroke: '#1A1A1A', strokeWidth: 2.5, strokeOpacity: 0.85,
    }));

    // Projected total spend line (neutral-dark dashed) — overlaid, scaled to regs axis.
    if (maxSpend > 0) {
      marks.push(Plot.line(projPoints, {
        x: 'week', y: 'total_spend_scaled',
        stroke: '#1A1A1A', strokeWidth: 2, strokeDasharray: '8,4', strokeOpacity: 0.5,
      }));
    }

    // Campaign lift shaded regions (onset → end-of-period or next lift)
    const regimesSorted = [...(marketData.regime_fit_state || [])]
      .sort((a, b) => new Date(a.change_date) - new Date(b.change_date));
    const periodEnd = btWeeks.length > 0 ? btWeeks[btWeeks.length - 1] : null;
    const periodStart = ytdWeeks.length > 0 ? ytdWeeks[0].date : (btWeeks.length > 0 ? btWeeks[0] : null);
    // Compute max y for shaded fill — use the max of all lines on chart
    let yMax = 0;
    for (const d of chartData) yMax = Math.max(yMax, d.brand_regs + d.nb_regs);
    yMax = yMax * 1.05;   // head-room for labels

    const regimeRegions = [];
    for (let i = 0; i < regimesSorted.length; i++) {
      const r = regimesSorted[i];
      let start = new Date(r.change_date);
      // Clamp pre-period regimes to period start so they don't stretch the x-axis
      if (periodStart && start < periodStart) start = periodStart;
      let end = (i + 1 < regimesSorted.length)
        ? new Date(regimesSorted[i + 1].change_date)
        : periodEnd;
      if (periodEnd && end > periodEnd) end = periodEnd;
      if (periodStart && end < periodStart) continue;   // skip fully-pre-period regimes
      if (end && start < end) {
        regimeRegions.push({ x1: start, x2: end, y1: 0, y2: yMax });
      }
    }
    if (regimeRegions.length > 0) {
      marks.push(Plot.rect(regimeRegions, {
        x1: 'x1', x2: 'x2', y1: 'y1', y2: 'y2',
        fill: 'var(--color-regime)', fillOpacity: 0.08,
      }));
    }

    // Campaign lift markers (vertical dashed lines, no text label — keep chart clean)
    const xMin = ytdFirst || btWeeks[0];
    const xMax = periodEnd || btWeeks[btWeeks.length - 1];
    for (const r of (marketData.regime_fit_state || [])) {
      const d = new Date(r.change_date);
      if (d < xMin || d > xMax) continue;
      marks.push(Plot.ruleX([d], {
        stroke: 'var(--color-regime)', strokeWidth: 1.5, strokeDasharray: '3,3', strokeOpacity: 0.7,
      }));
    }

    // Target line (principle #4 target color)
    if (driver === 'regs' && targetVal > 0) {
      marks.push(Plot.ruleY([targetVal / 52], {
        stroke: 'var(--color-target)', strokeWidth: 1.5, strokeDasharray: '6,3',
      }));
    }

    // Period highlight — shade the selected-period region on chart so user
    // sees what's being aggregated into the hero numbers.
    const periodWks = periodWeeksSet(currentPeriod());
    if (periodWks && periodWks.size > 0) {
      const periodDates = [];
      // Get the date range covered by the period
      let firstDate = null, lastDate = null;
      const allWeeks = [...ytdWeeks.map(w => w.date), ...royWeeks];
      for (const d of allWeeks) {
        const wkNum = computeIsoWeekNum(d);
        if (periodWks.has(wkNum)) {
          if (!firstDate || d < firstDate) firstDate = d;
          if (!lastDate || d > lastDate) lastDate = d;
        }
      }
      if (firstDate && lastDate) {
        marks.push(Plot.rect([{x1: firstDate, x2: lastDate, y1: 0, y2: (maxRegs || 100) * 1.05}], {
          x1: 'x1', x2: 'x2', y1: 'y1', y2: 'y2',
          fill: 'var(--color-brand)', fillOpacity: 0.04, stroke: 'var(--color-brand)', strokeOpacity: 0.3, strokeDasharray: '2,3',
        }));
      }
    }

    // Tooltip dots (invisible but show on hover via d3 overlay)
    marks.push(Plot.dot(chartData, {
      x: 'week', y: d => d.brand_regs + d.nb_regs,
      r: 3, fill: 'transparent', stroke: 'transparent',
    }));

    const chart = Plot.plot({
      width,
      height,
      marginTop: CHART_MARGIN.top,
      marginRight: CHART_MARGIN.right,
      marginBottom: CHART_MARGIN.bottom,
      marginLeft: CHART_MARGIN.left,
      x: {
        label: 'Week',
        tickFormat: d3.timeFormat('%b'),
        type: 'time',
        domain: [xMin, xMax],   // clamp to plotted period, ignore regime onset dates outside
      },
      y: { label: 'Registrations / week', grid: true, labelAnchor: 'center' },
      style: { fontFamily: 'Amazon Ember, sans-serif', fontSize: '12px' },
      marks,
    });

    chartEl.appendChild(chart);

    // Legend below chart (solid = regs axis, dashed = spend overlay scaled to regs)
    const legend = document.createElement('div');
    legend.style.textAlign = 'center';
    legend.style.fontSize = '11px';
    legend.style.color = 'var(--color-text-meta)';
    legend.style.marginTop = 'var(--gap-sm)';
    legend.style.display = 'flex';
    legend.style.justifyContent = 'center';
    legend.style.gap = 'var(--gap-lg)';
    legend.style.flexWrap = 'wrap';
    legend.innerHTML = `
      <span><span style="display:inline-block;width:16px;height:2px;background:var(--color-actuals);vertical-align:middle"></span> Actuals (regs)</span>
      <span><span style="display:inline-block;width:16px;border-top:2px dashed var(--color-actuals);vertical-align:middle"></span> Actuals (spend, scaled)</span>
      <span><span style="display:inline-block;width:16px;height:2px;background:var(--color-brand);vertical-align:middle"></span> Projected Brand</span>
      <span><span style="display:inline-block;width:16px;height:2px;background:var(--color-nb);vertical-align:middle"></span> Projected Non-Brand</span>
      <span><span style="display:inline-block;width:16px;height:2.5px;background:#1A1A1A;vertical-align:middle"></span> Projected Total</span>
      <span><span style="display:inline-block;width:16px;border-top:2px dashed #1A1A1A;vertical-align:middle"></span> Projected Total spend (scaled)</span>
    `;
    chartEl.appendChild(legend);

    // Overlay D3 SVG for narrated tooltips (task 6.3.6)
    attachNarratedTooltips(chart, chartData, marketData, out);

    // Apply animated arrival (task 6.3.8)
    applyArrivalAnimations(chart);

    // Sparkle-region shading annotation (task 6.3.2 acceptance — Sparkle visible)
    annotateActiveRegimes(chart, marketData);
  }

  function annotateActiveRegimes(chart, marketData) {
    // Minimal top-right indicator: just count + aggregate status, no brand names
    const chartEl = document.getElementById('chart-primary');
    const regimes = marketData.regime_fit_state || [];
    if (regimes.length === 0) return;
    // Summarize decay statuses — dominant one wins
    const statuses = regimes.map(r => (r.decay_status || 'unknown').replace(/-/g, ' '));
    const summary = statuses.length === 1 ? statuses[0] : `${regimes.length} active`;
    const label = document.createElement('div');
    label.style.position = 'absolute';
    label.style.top = '8px';
    label.style.right = '8px';
    label.style.background = 'var(--color-regime)';
    label.style.color = 'white';
    label.style.fontSize = '10px';
    label.style.padding = '3px 10px';
    label.style.borderRadius = '10px';
    label.style.fontWeight = '600';
    label.textContent = `${regimes.length} campaign lift${regimes.length > 1 ? 's' : ''} · ${summary}`;
    chartEl.appendChild(label);

    // Counterfactual delta caption when the overlay is on
    if (STATE.disclosures.counter && STATE.currentCounterfactual && STATE.currentBrandProj) {
      const base = STATE.currentBrandProj.totals?.brand_regs || 0;
      const counter = STATE.currentCounterfactual.totals?.brand_regs || 0;
      const delta = base - counter;
      const nWeeks = (marketData.brand_trajectory_y2026?.regs_per_week?.length) || 52;
      const nLifts = (marketData.regime_fit_state || []).length;
      const liftText = nLifts === 1 ? 'campaign lift' : `${nLifts} campaign lifts`;
      const cap = document.createElement('div');
      cap.style.position = 'absolute';
      cap.style.bottom = '8px';
      cap.style.left = '50%';
      cap.style.transform = 'translateX(-50%)';
      cap.style.background = 'var(--color-neutral-bg)';
      cap.style.border = '1px solid var(--color-counterfactual)';
      cap.style.padding = '6px 12px';
      cap.style.borderRadius = '4px';
      cap.style.fontSize = '12px';
      cap.style.color = 'var(--color-text-body)';
      cap.style.fontVariantNumeric = 'tabular-nums';
      cap.innerHTML = `<span style="color:var(--color-counterfactual)">— — — without these lifts</span> · ${liftText} added <b>≈${fmtNum(delta)}</b> Brand regs over ${nWeeks} weeks`;
      chartEl.appendChild(cap);
    }
  }

  function applyArrivalAnimations(chartNode) {
    // Observable Plot emits an SVG. Drive layered animations by class on path elements.
    if (!chartNode) return;
    const svg = chartNode.tagName === 'SVG' ? chartNode : chartNode.querySelector('svg');
    if (!svg) return;
    // Simple: give the entire SVG a fade-in, then the contribution panel a lift-in.
    svg.classList.add('arrival-ci');
    const contrib = document.getElementById('contribution-panel');
    contrib.classList.remove('visible', 'arrival-contribution');
    void contrib.offsetWidth;
    contrib.classList.add('visible', 'arrival-contribution');
  }

  // ========================================================================
  // Narrated tooltips (task 6.3.6) — "why" not "what"
  // ========================================================================

  function attachNarratedTooltips(chartNode, chartData, marketData, out) {
    if (!chartNode) return;
    const svg = chartNode.tagName === 'SVG' ? chartNode : chartNode.querySelector('svg');
    if (!svg) return;

    // Use native SVG mouse tracking via d3.bisector for nearest point
    const tooltip = ensureTooltip();
    const rect = svg.getBoundingClientRect();

    const xExtent = d3.extent(chartData, d => d.week);
    const plotRect = svg.querySelector('[aria-label="mark"], rect') || svg;

    svg.addEventListener('mousemove', (ev) => {
      const pt = svg.getBoundingClientRect();
      const mx = ev.clientX - pt.left;
      const innerLeft = CHART_MARGIN.left;
      const innerRight = pt.width - CHART_MARGIN.right;
      const xFrac = (mx - innerLeft) / (innerRight - innerLeft);
      if (xFrac < 0 || xFrac > 1) { hideTooltip(); return; }
      const targetTime = xExtent[0].getTime() + xFrac * (xExtent[1].getTime() - xExtent[0].getTime());
      const bis = d3.bisector(d => d.week.getTime()).left;
      const idx = bis(chartData, targetTime);
      const d = chartData[Math.min(idx, chartData.length - 1)];
      if (!d) { hideTooltip(); return; }
      showTooltip(ev, renderNarratedTooltip(d, chartData, marketData, out));
    });
    svg.addEventListener('mouseleave', hideTooltip);
  }

  function renderNarratedTooltip(d, chartData, marketData, out) {
    const totalRegs = d.brand_regs + d.nb_regs;
    const totalSpend = d.brand_spend + d.nb_spend;
    const locked = d.locked;
    const lines = [];
    lines.push(`<div class="tt-header">${d.isoWeek} · ${locked ? 'YTD actual (locked)' : 'Projected'}</div>`);
    lines.push(`<div class="tt-value">${fmtNum(totalRegs)} regs · ${fmt$(totalSpend)} spend</div>`);

    if (locked) {
      lines.push(`<div class="tt-why">Brand <span class="highlight">${fmtNum(d.brand_regs)}</span> regs · NB <span class="highlight">${fmtNum(d.nb_regs)}</span>. Brand <span class="highlight">${fmt$(d.brand_spend)}</span> · NB <span class="highlight">${fmt$(d.nb_spend)}</span>. Locked data.</div>`);
    } else {
      const bt = marketData.brand_trajectory_y2026;
      const contrib = bt?.contribution || { seasonal: 0.4, trend: 0.4, regime: 0.15, qualitative: 0.05 };
      const seasPct = Math.round(contrib.seasonal * 100);
      const trendPct = Math.round(contrib.trend * 100);
      const regPct = Math.round(contrib.regime * 100);
      const qualPct = Math.round(contrib.qualitative * 100);
      const nLifts = (marketData.regime_fit_state || []).length;
      const liftLabel = nLifts === 1 ? '1 campaign lift' : (nLifts > 1 ? `${nLifts} campaign lifts` : '');
      lines.push(`<div class="tt-why">Brand <span class="highlight">${fmtNum(d.brand_regs)}</span> regs / <span class="highlight">${fmt$(d.brand_spend)}</span>: ${trendPct}% trend, ${seasPct}% seasonality, ${regPct}% lift${liftLabel ? ` (${liftLabel})` : ''}, ${qualPct}% qualitative. NB <span class="highlight">${fmtNum(Math.round(d.nb_regs))}</span> regs / <span class="highlight">${fmt$(d.nb_spend)}</span> solved to hit target.</div>`);
    }
    return lines.join('');
  }

  function ensureTooltip() {
    if (STATE.tooltipEl) return STATE.tooltipEl;
    const el = document.createElement('div');
    el.className = 'mpe-tooltip';
    document.body.appendChild(el);
    STATE.tooltipEl = el;
    return el;
  }
  function showTooltip(ev, html) {
    const el = ensureTooltip();
    el.innerHTML = html;
    el.classList.add('visible');
    const rect = el.getBoundingClientRect();
    const pageW = window.innerWidth;
    const pageH = window.innerHeight;
    let left = ev.pageX + 14;
    let top = ev.pageY + 14;
    if (left + rect.width > pageW - 20) left = ev.pageX - rect.width - 14;
    if (top + rect.height > pageH - 20) top = ev.pageY - rect.height - 14;
    el.style.left = `${left}px`;
    el.style.top = `${top}px`;
  }
  function hideTooltip() {
    if (STATE.tooltipEl) STATE.tooltipEl.classList.remove('visible');
  }

  // ========================================================================
  // Contribution bar (task 6.3.4)
  // ========================================================================

  function renderContributionBar(out, marketData) {
    const bt = marketData.brand_trajectory_y2026;
    const contribution = bt?.contribution || out.contribution_breakdown || { seasonal: 0.40, trend: 0.40, regime: 0.15, qualitative: 0.05 };
    const bar = document.getElementById('contribution-bar');
    bar.innerHTML = '';

    // Contribution bar (principle #5 — chart not table)
    // NB residual bar and segment labels use plain-English "lift" not "regime"
    const segments = [
      { key: 'seasonal', label: 'Seasonal', pct: contribution.seasonal || 0, klass: 'seasonal' },
      { key: 'trend', label: 'Trend', pct: contribution.trend || 0, klass: 'trend' },
      { key: 'regime', label: 'Campaign lift', pct: contribution.regime || 0, klass: 'regime' },
      { key: 'qualitative', label: 'Qualitative', pct: contribution.qualitative || 0, klass: 'qualitative' },
    ].filter(s => s.pct > 0.005);

    const brandRegs = out.totals?.brand_regs || 0;
    for (const seg of segments) {
      const d = document.createElement('div');
      d.className = `contribution-segment ${seg.klass}`;
      d.style.flex = seg.pct;
      const segRegs = Math.round(brandRegs * seg.pct);
      d.textContent = `${seg.label} ${Math.round(seg.pct * 100)}% · ${fmtNum(segRegs)}`;
      d.title = `${seg.label} contributed ${fmtNum(segRegs)} Brand regs`;
      bar.appendChild(d);
    }

    document.getElementById('contribution-sub-left').textContent = `Brand trajectory: ${fmtNum(brandRegs)} regs over ${(marketData.ytd_weekly?.length || 0) + (bt?.regs_per_week?.length - (marketData.ytd_weekly?.length || 0) || 0)} weeks`;
    document.getElementById('contribution-sub-right').textContent = `CPA $${bt?.brand_cpa_used?.toFixed(2) || '—'}`;

    // NB residual bar (now "Non-Brand plan") — plain-English, no raw numbers.
    const nbRegs = out.totals?.nb_regs || 0;
    const nbSpend = out.totals?.nb_spend || 0;
    const seg = document.getElementById('nb-segment');
    const driver = currentDriver();
    const tgtVal = currentTargetValue();
    let tgtText;
    if (driver === 'ieccp') tgtText = `${tgtVal}% efficiency target`;
    else if (driver === 'spend') tgtText = `${fmt$(tgtVal)} spend target`;
    else if (driver === 'regs') tgtText = `${fmtNum(tgtVal)} registrations target`;
    else if (driver === 'rollup') tgtText = 'region rollup';
    else tgtText = 'current target';
    seg.textContent = `Non-Brand plan: spend ${fmt$(nbSpend)} to deliver ${fmtNum(nbRegs)} regs · ${tgtText}`;
  }

  // ========================================================================
  // Fit Quality strip (from Phase 6.1.5 observability)
  // ========================================================================

  function renderFitQuality(marketData, out) {
    const fq = marketData.fit_quality || {};
    const r2 = fq.r_squared ?? marketData.parameters?.brand_cpa_elasticity?.r_squared ?? null;
    const nWeeks = fq.n_weeks ?? marketData.parameters?.brand_cpa_elasticity?.value_json?.weeks_used ?? null;
    const fbLevel = fq.fallback_level || marketData.fallback_summary || 'market_specific';
    const klass = r2 == null ? 'low' : r2 > 0.7 ? 'high' : r2 > 0.45 ? 'medium' : 'low';

    // Plain-language fit quality
    let fitWord, fitPct;
    if (r2 == null) { fitWord = 'unknown'; fitPct = null; }
    else if (r2 >= 0.7) { fitWord = 'strong'; fitPct = Math.round(r2 * 100); }
    else if (r2 >= 0.45) { fitWord = 'fair'; fitPct = Math.round(r2 * 100); }
    else if (r2 >= 0.2) { fitWord = 'weak'; fitPct = Math.round(r2 * 100); }
    else { fitWord = 'very weak'; fitPct = Math.round(r2 * 100); }

    // Plain-language fallback level
    const fbMap = {
      'market_specific': 'fit from this market\'s own data',
      'regional_fallback': 'some parameters use regional average',
      'some_regional_fallback': 'some parameters use regional average',
      'global_fallback': 'some parameters use global average',
    };
    const fbText = fbMap[fbLevel] || fbLevel.replace(/_/g, ' ');

    const regimes = V1_1_Slim.listRegimesWithConfidence(marketData.regime_fit_state || [], STATE.regimeMultiplier);
    const liftCount = regimes.length;
    const liftText = liftCount === 0 ? '' : ` · ${liftCount} active campaign lift${liftCount > 1 ? 's' : ''}`;

    const fitHtml = fitPct != null
      ? `<span class="dot ${klass}"></span>Fit quality: <b>${fitWord}</b> (${fitPct}% explained) · ${nWeeks ? `${nWeeks} weeks of data` : 'weeks of data not recorded'} · ${fbText}${liftText}`
      : `<span class="dot low"></span>Fit quality: <b>not yet measured</b> · ${nWeeks ? `${nWeeks} weeks of data` : 'weeks of data not recorded'} · ${fbText}${liftText}`;

    const el = document.getElementById('fit-quality');
    el.innerHTML = fitHtml;
  }

  // ========================================================================
  // Warnings panel
  // ========================================================================

  function renderWarnings(out) {
    const ul = document.getElementById('warnings-list');
    const cnt = document.getElementById('warnings-count');
    ul.innerHTML = '';
    const ws = out.warnings || [];
    if (ws.length === 0) {
      ul.innerHTML = '<li style="color:var(--color-text-subtle)">No warnings.</li>';
      cnt.textContent = '';
      return;
    }
    cnt.textContent = `${ws.length}`;
    for (const w of ws) {
      const li = document.createElement('li');
      if (w.startsWith('TARGET_UNREACHABLE') || w.startsWith('LOCKED_YTD')) li.className = 'danger';
      else if (w.startsWith('VERY_WIDE_CI') || w.startsWith('OUTSIDE_TOLERANCE')) li.className = 'warn';
      li.textContent = translateWarning(w);
      li.title = w; // keep the raw code as a tooltip for debugging
      ul.appendChild(li);
    }
  }

  // ========================================================================
  // YTD wall banner (task 6.3.5)
  // ========================================================================

  function renderYtdWallBanner(out) {
    const banner = document.getElementById('ytd-wall-banner');
    const text = document.getElementById('ytd-wall-text');
    const ws = out.warnings || [];
    const unreachable = ws.some(w => w.startsWith('TARGET_UNREACHABLE') || w.startsWith('LOCKED_YTD') || w.startsWith('OUTSIDE_TOLERANCE') || w.startsWith('OP2_BUDGET_EXCEEDED'));
    if (unreachable) {
      const relevant = ws.filter(w => w.startsWith('TARGET_UNREACHABLE') || w.startsWith('LOCKED_YTD') || w.startsWith('OUTSIDE_TOLERANCE') || w.startsWith('OP2_BUDGET_EXCEEDED'));
      // Translate + prefix with "Closest achievable" framing when applicable.
      const phrases = relevant.map(translateWarning);
      text.textContent = phrases.join(' · ');
      banner.classList.add('active');
    } else {
      banner.classList.remove('active');
    }
  }

  // ========================================================================
  // Disclosure buttons (task 6.3.2)
  // ========================================================================

  function bindDisclosureButtons() {
    document.querySelectorAll('.disclosure-btn[data-disclosure]').forEach(btn => {
      btn.addEventListener('click', () => {
        const key = btn.dataset.disclosure;
        STATE.disclosures[key] = !STATE.disclosures[key];
        btn.classList.toggle('active', STATE.disclosures[key]);

        if (key === 'params') {
          document.getElementById('drawer').classList.toggle('open', STATE.disclosures.params);
        } else if (key === 'narrative') {
          document.getElementById('narrative-panel').style.display = STATE.disclosures.narrative ? '' : 'none';
          if (STATE.disclosures.narrative) generateNarrative();
        } else if (key === 'counter') {
          // Re-render chart to toggle counterfactual
          if (STATE.currentBrandProj) {
            const scope = currentScope();
            const md = (STATE.data.markets || {})[scope];
            renderChart(STATE.currentBrandProj, STATE.currentCounterfactual, null, md);
          }
        } else if (key === 'how') {
          // Open a modal with plain-English math walkthrough
          openHowModal();
          // Un-toggle the "active" state so re-opening works
          STATE.disclosures.how = false;
          btn.classList.remove('active');
        }
      });
    });
  }

  // Plain-English modal explaining the math behind the projection.
  function openHowModal() {
    const scope = currentScope();
    const period = currentPeriod();
    const driver = currentDriver();
    const targetVal = currentTargetValue();
    const out = STATE.currentOutput;
    const md = (STATE.data.markets || {})[scope];
    const regimes = V1_1_Slim.listRegimesWithConfidence(md?.regime_fit_state || [], STATE.regimeMultiplier);
    const fq = md?.fit_quality || {};
    const r2 = fq.r_squared ?? md?.parameters?.brand_cpa_elasticity?.r_squared ?? null;

    const driverPhrase = driver === 'ieccp' ? `efficiency target of ${targetVal}%`
      : driver === 'spend' ? `spend target of ${fmt$(targetVal)}`
      : driver === 'regs' ? `registrations target of ${fmtNum(targetVal)}`
      : 'current target';

    let bodyHtml = `
      <p><b>Scope:</b> ${scope} · <b>Period:</b> ${period} · <b>Target:</b> ${driverPhrase}</p>
      <h3 style="margin-top:12px;font-size:14px">Step 1 — Brand registrations forecast</h3>
      <p>We blend three signals to predict Brand registrations week-by-week for the rest of the year:</p>
      <ul style="margin-left:18px;margin-bottom:8px">
        <li><b>Anchor</b>: 8-week average of recent Brand registrations — the current baseline.</li>
        <li><b>Seasonality</b>: historical week-of-year patterns (e.g., holiday weeks are lower).</li>
        <li><b>Trend</b>: recent slope, fading out over 13 weeks so it doesn't extrapolate forever.</li>
        <li><b>Campaign lifts</b>: ${regimes.length} active lift${regimes.length === 1 ? '' : 's'} applied with their observed decay curves.</li>
      </ul>
      <h3 style="margin-top:12px;font-size:14px">Step 2 — Non-Brand residual</h3>
      <p>With Brand regs and Brand spend projected, we solve for the Non-Brand spend that ${driver === 'ieccp' ? 'lands the full-year efficiency on target' : driver === 'regs' ? 'delivers the missing registrations via the NB CPA elasticity curve' : 'fills the remaining budget after Brand'}. The solver uses the NB CPA elasticity fit from ${fq.n_weeks ? `${fq.n_weeks} weeks` : 'the available history'} of history.</p>
      <h3 style="margin-top:12px;font-size:14px">Step 3 — Locked YTD</h3>
      <p>Weeks that have already happened are locked to actuals. The solver only adjusts the remaining weeks of the year.</p>
    `;

    if (r2 != null) {
      let fitWord = r2 >= 0.7 ? 'strong' : r2 >= 0.45 ? 'fair' : r2 >= 0.2 ? 'weak' : 'very weak';
      bodyHtml += `<p style="margin-top:12px;color:var(--color-text-subtle)"><b>Confidence:</b> Fit quality is <b>${fitWord}</b> (${Math.round(r2 * 100)}% of historical variance explained). Treat this projection accordingly.</p>`;
    }

    if ((out?.warnings || []).length > 0) {
      bodyHtml += `<p style="margin-top:12px"><b>Warnings this run:</b></p><ul style="margin-left:18px">`;
      for (const w of out.warnings) {
        bodyHtml += `<li>${translateWarning(w)}</li>`;
      }
      bodyHtml += `</ul>`;
    }

    document.getElementById('modal-title').textContent = 'How this was calculated';
    document.getElementById('modal-body').innerHTML = bodyHtml;
    document.getElementById('modal-overlay').classList.add('active');
  }

  // Translate warning codes to plain English.
  function translateWarning(w) {
    if (!w) return '';
    const upper = String(w).toUpperCase();
    if (upper.startsWith('UNSUPPORTED_TARGET_MODE')) {
      return `This market doesn't support that target type.`;
    }
    if (upper.startsWith('TARGET_UNREACHABLE_UNDER_EFFECTIVE_BOUNDS') || upper.startsWith('TARGET_UNREACHABLE_UNDER_ELASTICITY')) {
      return `Target can't be reached — the model's spend response curve flattens before we get there.`;
    }
    if (upper.startsWith('TARGET_UNREACHABLE_ON_UPPER_BAND')) {
      return `Target is too high to reach with current NB spend limits.`;
    }
    if (upper.startsWith('TARGET_UNREACHABLE_ON_LOWER_BAND')) {
      return `Target is too low — can't hit it without cutting NB spend below allowed minimums.`;
    }
    if (upper.startsWith('OUTSIDE_TOLERANCE_BAND')) {
      const match = w.match(/(\d+\.?\d*)/g);
      const actual = match && match[0];
      const target = match && match[1];
      return actual && target
        ? `Closest achievable is ${actual}% (target was ${target}%).`
        : `Solver landed outside the ±5% tolerance band.`;
    }
    if (upper.startsWith('ANCHOR_CLIPPED_POST_REGIME')) {
      return `The recent-actuals anchor was clipped back to pre-campaign levels so we don't double-count the lift.`;
    }
    if (upper.startsWith('NB_UNDER_FUNDED')) {
      return `Non-Brand spend would go negative at this target — solver held it at a floor.`;
    }
    if (upper.startsWith('REGS_TARGET_MET_BY_BRAND')) {
      return `Brand alone already hits the registrations target — no NB spend needed.`;
    }
    if (upper.startsWith('OP2_BUDGET_EXCEEDED')) {
      return `Reg target requires spending above the OP2 budget — solver clamped to budget.`;
    }
    if (upper.startsWith('LOCKED_YTD')) {
      return `YTD actuals already commit outcomes the target conflicts with.`;
    }
    if (upper.startsWith('VERY_WIDE_CI')) {
      return `Result is highly uncertain — the fit is weak.`;
    }
    if (upper.startsWith('HIGH_EXTRAPOLATION')) {
      return `Spend is well beyond historical range — elasticity curve may not hold.`;
    }
    if (upper.startsWith('SEASONAL_PRIOR_UNAVAILABLE')) {
      return `Not enough history for seasonality — using a flat prior instead.`;
    }
    if (upper.startsWith('SEASONAL_WEEK_UNSTABLE')) {
      return `One or more weeks have high year-over-year variance — seasonality may shift.`;
    }
    if (upper.startsWith('REGIONAL_IECCP_NOT_A_DRIVER')) {
      return `Regions roll up from their member markets — efficiency isn't set at the region level.`;
    }
    if (upper.startsWith('ROLLUP_FALLBACK')) {
      return `Some member markets don't have an efficiency target — using spend run-rate instead.`;
    }
    if (upper.startsWith('REGIME_WEIGHT_IGNORED')) {
      return `Regime weight override is ignored — use the slider below the chart instead.`;
    }
    if (upper.startsWith('OP2_PACING_DIVERGENCE')) {
      return `Projection diverges from OP2 plan.`;
    }
    if (upper.startsWith('FIT_R2_DROP')) {
      return `Fit quality dropped sharply since the last refit — results less reliable.`;
    }
    if (upper.startsWith('REGIME_LOW_CONFIDENCE')) {
      return `Campaign lift confidence is low — treat its contribution cautiously.`;
    }
    if (upper.startsWith('YTD_PROJECTION_STEP')) {
      return `Large step between YTD actuals and the start of the projection.`;
    }
    // Default: capitalize first letter, replace underscores with spaces.
    const pretty = w.replace(/_/g, ' ').toLowerCase();
    return pretty.charAt(0).toUpperCase() + pretty.slice(1);
  }

  // ========================================================================
  // Drawer (Parameters disclosure target)
  // ========================================================================

  function renderDrawer(out, marketData) {
    // 6.4.4 Sparklines block first
    renderDrawerSparklines(marketData);

    const fq = marketData.fit_quality || {};
    const r2 = fq.r_squared ?? marketData.parameters?.brand_cpa_elasticity?.r_squared;
    const nWeeks = fq.n_weeks ?? marketData.parameters?.brand_cpa_elasticity?.value_json?.weeks_used;
    // Plain-language fit quality in drawer
    let fqText;
    if (r2 == null) fqText = 'unknown';
    else if (r2 >= 0.7) fqText = `strong (${Math.round(r2 * 100)}% explained)`;
    else if (r2 >= 0.45) fqText = `fair (${Math.round(r2 * 100)}% explained)`;
    else if (r2 >= 0.2) fqText = `weak (${Math.round(r2 * 100)}% explained)`;
    else fqText = `very weak (${Math.round(r2 * 100)}% explained)`;
    document.getElementById('dv-rsq').textContent = fqText;
    document.getElementById('dv-n-weeks').textContent = nWeeks || '—';
    const fbLevelRaw = fq.fallback_level || marketData.fallback_summary || 'market_specific';
    const fbMap = {
      'market_specific': 'from this market\'s own data',
      'regional_fallback': 'some parameters use regional average',
      'some_regional_fallback': 'some parameters use regional average',
      'global_fallback': 'some parameters use global average',
    };
    document.getElementById('dv-fallback').textContent = fbMap[fbLevelRaw] || fbLevelRaw.replace(/_/g, ' ');

    const regimes = V1_1_Slim.listRegimesWithConfidence(marketData.regime_fit_state || [], STATE.regimeMultiplier);
    const stackEl = document.getElementById('dv-regime-stack');
    if (regimes.length === 0) {
      stackEl.innerHTML = '<div style="font-size:12px;color:var(--color-text-subtle)">No regimes active.</div>';
    } else {
      stackEl.innerHTML = regimes.map((r, i) => {
        const fresh = r.decay_status && r.decay_status !== 'no-fit-state' ? 'fresh' : 'stale';
        const onsetDate = r.change_date ? new Date(r.change_date).toLocaleDateString() : 'n/a';
        return `<div class="drawer-tile">
          <span class="drawer-tile-label">Lift #${i + 1} (onset ${onsetDate}) <span class="freshness-badge ${fresh}">${(r.decay_status || 'n/a').replace(/-/g, ' ')}</span></span>
          <span class="drawer-tile-value">${(r.effective_confidence * 100).toFixed(0)}%</span>
        </div>
        <div style="font-size:10px;color:var(--color-text-subtle);margin-top:-6px;margin-bottom:4px">${r.explanation}</div>`;
      }).join('');
    }

    const params = marketData.parameters || {};
    const pEl = document.getElementById('dv-parameters');
    const relevant = ['brand_ccp', 'nb_ccp', 'brand_cpa_elasticity', 'nb_cpa_elasticity', 'ieccp_target', 'supported_target_modes'];
    pEl.innerHTML = relevant.filter(k => params[k]).map(k => {
      const p = params[k];
      const v = p.value_scalar != null ? p.value_scalar.toFixed(2) : JSON.stringify(p.value_json).slice(0, 40);
      return `<div style="padding:3px 0;border-bottom:1px solid #EEE"><b>${k}</b>: ${v}<br><span style="font-size:10px;color:var(--color-text-subtle)">${p.lineage || ''}</span></div>`;
    }).join('');
  }

  // ========================================================================
  // Saved projections
  // ========================================================================

  function saveProjection() {
    const out = STATE.currentOutput;
    if (!out || !out.totals) return;
    const rec = {
      id: Date.now(),
      scope: currentScope(),
      period: currentPeriod(),
      driver: currentDriver(),
      target_value: currentTargetValue(),
      regime_multiplier: STATE.regimeMultiplier,
      totals: out.totals,
      saved_at: new Date().toISOString(),
      fingerprint: STATE.data.generated,
    };
    STATE.saved.unshift(rec);
    STATE.saved = STATE.saved.slice(0, 20);
    localStorage.setItem('mpe-saved', JSON.stringify(STATE.saved));
    renderSavedList();
  }

  function renderSavedList() {
    const list = document.getElementById('saved-list');
    const cnt = document.getElementById('saved-count');
    cnt.textContent = STATE.saved.length ? `${STATE.saved.length}` : '';
    if (!STATE.saved.length) {
      list.innerHTML = `<div style="color:var(--color-text-subtle);font-size:11px">No saved projections yet.</div>`;
      return;
    }
    list.innerHTML = STATE.saved.map(r => `
      <div class="saved-item" data-id="${r.id}">
        <span>${r.scope} · ${r.period} · ${r.driver}=${r.target_value}</span>
        <span class="saved-meta">${new Date(r.saved_at).toLocaleDateString()}</span>
      </div>
    `).join('');
    list.querySelectorAll('.saved-item').forEach(el => {
      el.addEventListener('click', () => loadSaved(parseInt(el.dataset.id)));
    });
  }

  function loadSaved(id) {
    const r = STATE.saved.find(x => x.id === id);
    if (!r) return;
    document.getElementById('scope-select').value = r.scope;
    document.getElementById('period-select').value = r.period;
    refreshScopeDependentUI();
    document.getElementById('driver-select').value = r.driver;
    document.getElementById('target-input').value = r.target_value;
    STATE.regimeMultiplier = r.regime_multiplier || 1.0;
    document.getElementById('regime-slider').value = STATE.regimeMultiplier;
    document.getElementById('regime-slider-val').textContent = STATE.regimeMultiplier.toFixed(2) + '×';
    scheduleRecompute();
  }

  // ========================================================================
  // Narrative
  // ========================================================================

  function generateNarrative() {
    if (!STATE.currentOutput) return;
    const el = document.getElementById('narrative-block');
    if (typeof MPENarrative !== 'undefined' && MPENarrative.generate) {
      const out = STATE.currentOutput;
      // Normalize V1_1_Slim shape to MPE shape for narrative
      const fauxOut = {
        scope: currentScope(),
        time_period: currentPeriod(),
        target_mode: currentDriver(),
        target_value: currentTargetValue(),
        outcome: out.error ? 'ERROR' : 'OK',
        warnings: out.warnings || [],
        totals: {
          total_regs: out.totals?.total_regs,
          total_spend: out.totals?.total_spend,
          blended_cpa: out.totals?.blended_cpa,
          ieccp: out.totals?.computed_ieccp,
          brand_regs: out.totals?.brand_regs,
          nb_regs: out.totals?.nb_regs,
        },
      };
      try {
        el.textContent = MPENarrative.generate(fauxOut, STATE.data);
      } catch (e) {
        el.textContent = `Narrative generation failed: ${e.message}`;
      }
    } else {
      el.textContent = 'Narrative module not loaded.';
    }
  }

  // ========================================================================
  // Share card — Phase 6.4.6 — client-side PNG render via canvas
  // ========================================================================

  function shareCardClick() {
    const out = STATE.currentOutput;
    if (!out) {
      const btn = document.getElementById('btn-share');
      const orig = btn.textContent;
      btn.textContent = 'No data to share';
      setTimeout(() => (btn.textContent = orig), 1200);
      return;
    }
    const scope = currentScope();
    const period = currentPeriod();
    const driver = currentDriver();
    const v = currentTargetValue();
    const t = out.totals || {};

    // Native canvas render — no html2canvas dep.
    const canvas = document.createElement('canvas');
    canvas.width = 1200;
    canvas.height = 630;
    const ctx = canvas.getContext('2d');

    // Background
    ctx.fillStyle = '#FFFFFF';
    ctx.fillRect(0, 0, 1200, 630);

    // Brand stripe top-left
    ctx.fillStyle = '#0066CC';
    ctx.fillRect(0, 0, 6, 630);

    // Title
    ctx.fillStyle = '#6B6B6B';
    ctx.font = '14px -apple-system, "Amazon Ember", sans-serif';
    ctx.fillText('MARKET PROJECTION ENGINE · v1.1 Slim', 40, 44);

    // Hero spend + regs side-by-side
    ctx.fillStyle = '#0A0A0A';
    ctx.font = 'bold 96px -apple-system, "Amazon Ember", sans-serif';
    const heroSpend = fmt$(t.total_spend);
    ctx.fillText(heroSpend, 40, 180);
    // Measure width for placement
    const spendW = ctx.measureText(heroSpend).width;
    ctx.fillStyle = '#6B6B6B';
    ctx.font = '32px -apple-system, sans-serif';
    ctx.fillText('spend', 50 + spendW, 180);

    ctx.fillStyle = '#0A0A0A';
    ctx.font = 'bold 96px -apple-system, "Amazon Ember", sans-serif';
    const heroRegs = fmtNum(t.total_regs);
    ctx.fillText(heroRegs, 40, 300);
    const regsW = ctx.measureText(heroRegs).width;
    ctx.fillStyle = '#6B6B6B';
    ctx.font = '32px -apple-system, sans-serif';
    ctx.fillText('regs', 50 + regsW, 300);

    // Context sentence
    ctx.fillStyle = '#1A1A1A';
    ctx.font = '22px -apple-system, sans-serif';
    const driverText = driver === 'ieccp' ? `${v}% efficiency target`
      : driver === 'spend' ? `$${fmtNum(v)} spend target`
      : driver === 'regs' ? `${fmtNum(v)} regs target`
      : 'rollup';
    ctx.fillText(`${scope} · ${period} · ${driverText}`, 40, 360);

    // KPI row
    ctx.fillStyle = '#1A1A1A';
    ctx.font = 'bold 20px monospace';
    const kpis = [
      `Brand: ${fmtNum(t.brand_regs)}`,
      `NB: ${fmtNum(t.nb_regs)}`,
      `CPA: ${fmt$(t.blended_cpa)}`,
      `Efficiency: ${t.computed_ieccp != null ? t.computed_ieccp.toFixed(1) + '%' : 'n/a'}`,
    ];
    let x = 40;
    for (const k of kpis) {
      ctx.fillText(k, x, 440);
      x += ctx.measureText(k).width + 40;
    }

    // Scenario chip name
    ctx.fillStyle = '#5E8B7E';
    ctx.font = 'bold 16px -apple-system, sans-serif';
    const chipLabel = {
      mixed: 'Planned', frequentist: 'Pessimistic',
      bayesian: 'Optimistic', 'no-lift': 'Baseline only',
    }[STATE.activeChipId] || 'Planned';
    ctx.fillText(`Scenario: ${chipLabel}`, 40, 490);

    // Footer
    ctx.fillStyle = '#9A9A9A';
    ctx.font = '14px -apple-system, sans-serif';
    const ts = new Date().toLocaleString();
    ctx.fillText(`Generated ${ts} · MPE v1.1 Slim`, 40, 590);
    ctx.textAlign = 'right';
    ctx.fillText('Amazon Business Paid Search', 1160, 590);
    ctx.textAlign = 'left';

    // Warning badge if present
    if ((out.warnings || []).length > 0) {
      ctx.fillStyle = '#E8A800';
      ctx.fillRect(40, 510, 10, 10);
      ctx.fillStyle = '#1A1A1A';
      ctx.font = '13px -apple-system, sans-serif';
      ctx.fillText(`${out.warnings.length} warning${out.warnings.length > 1 ? 's' : ''} — see drawer`, 58, 520);
    }

    // Export as PNG
    canvas.toBlob(blob => {
      if (!blob) return;
      // Download
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `mpe-${scope}-${period}-${STATE.activeChipId || 'mixed'}.png`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      // Also try clipboard (native)
      if (navigator.clipboard?.write) {
        try {
          navigator.clipboard.write([new ClipboardItem({ 'image/png': blob })]).catch(() => {});
        } catch (e) { /* clipboard may fail on older browsers — download still works */ }
      }
      setTimeout(() => URL.revokeObjectURL(url), 5000);
    }, 'image/png');

    const btn = document.getElementById('btn-share');
    const orig = btn.textContent;
    btn.textContent = 'PNG downloaded';
    setTimeout(() => (btn.textContent = orig), 1500);
  }

  // ========================================================================
  // 6.4.1 Small multiples — 2×5 grid of mini projection charts
  // ========================================================================

  async function renderSmallMultiples() {
    const grid = document.getElementById('small-multiples-grid');
    grid.innerHTML = '';
    const driver = currentDriver() === 'rollup' ? 'ieccp' : currentDriver();
    const period = currentPeriod();
    const periodWeeks = periodWeeksSet(period);
    let okCount = 0;

    for (const mkt of MPE.ALL_MARKETS) {
      const md = (STATE.data.markets || {})[mkt];
      if (!md) continue;
      const supported = md.parameters?.supported_target_modes?.value_json || ['spend'];
      let effDriver = driver;
      if (!supported.includes(effDriver)) effDriver = supported[0];
      const ieTgt = md.parameters?.ieccp_target?.value_scalar;
      const op2Spend = md.op2_targets?.annual_spend_target;
      const op2Regs = md.op2_targets?.annual_regs_target;
      let effTarget;
      if (effDriver === 'ieccp') effTarget = ieTgt ? ieTgt * 100 : 75;
      else if (effDriver === 'spend') effTarget = op2Spend || 500000;
      else effTarget = op2Regs || 5000;

      try {
        const out = V1_1_Slim.projectWithLockedYtd(
          md, 2026, effDriver, effTarget,
          { regimeMultiplier: STATE.regimeMultiplier, scenarioOverride: STATE.scenarioOverride, periodWeeks, periodType: period }
        );
        const card = renderMiniChartCard(mkt, md, out);
        grid.appendChild(card);
        okCount += 1;
      } catch (e) {
        console.error(`Small-multiples ${mkt} failed:`, e);
      }
    }
    document.getElementById('multiples-legend').textContent =
      `${okCount} markets rendered · driver=${driver} · period=${period} · scenario=${STATE.activeChipId || 'mixed'}`;
  }

  function renderMiniChartCard(market, md, out) {
    const card = document.createElement('div');
    card.className = 'mini-chart-card';
    card.addEventListener('click', () => {
      document.getElementById('scope-select').value = market;
      switchView('single');
      refreshScopeDependentUI();
      scheduleRecompute();
    });

    const t = out.totals || {};
    const yw = out.year_weekly;
    const headlineValue = fmt$(t.total_spend) + ' · ' + fmtNum(t.total_regs);
    const mktAnoms = STATE.data?.anomalies?.markets?.[market] || [];
    const anomHasError = mktAnoms.some(a => a.severity === 'error');
    const anomHasWarn = mktAnoms.some(a => a.severity === 'warn');
    const anomBadge = anomHasError ? '<span style="color:var(--color-danger);margin-left:4px" title="' + mktAnoms.length + ' anomalies">●</span>'
      : anomHasWarn ? '<span style="color:var(--color-warning);margin-left:4px" title="' + mktAnoms.length + ' warnings">●</span>'
      : '';

    card.innerHTML = `
      <div class="mini-chart-header">
        <div class="mini-market-code">${market}${anomBadge}</div>
        <div class="mini-headline">${headlineValue}</div>
      </div>
      <div class="mini-chart-body" id="mini-${market}"></div>
      <div class="mini-chart-meta">Efficiency ${t.computed_ieccp != null ? t.computed_ieccp.toFixed(1) + '%' : 'n/a'} · CPA ${fmt$(t.blended_cpa)}</div>
    `;

    // Plot mini chart (simple total-regs line)
    if (yw && yw.brand_regs.length > 0) {
      const data = yw.brand_regs.map((br, i) => ({
        week: i + 1,
        total_regs: br + (yw.nb_regs[i] || 0),
        locked: i < yw.ytd_weeks,
      }));
      const chart = Plot.plot({
        width: 240, height: 80,
        marginTop: 4, marginRight: 4, marginBottom: 12, marginLeft: 24,
        x: { axis: null },
        y: { label: null, ticks: 2 },
        style: { fontFamily: 'Amazon Ember, sans-serif', fontSize: '9px' },
        marks: [
          Plot.line(data.filter(d => d.locked), { x: 'week', y: 'total_regs', stroke: 'var(--color-actuals)', strokeWidth: 1.5 }),
          Plot.line(data.filter(d => !d.locked), { x: 'week', y: 'total_regs', stroke: 'var(--color-brand)', strokeWidth: 1.5 }),
          Plot.ruleX([yw.ytd_weeks], { stroke: 'var(--color-actuals)', strokeDasharray: '2,2', strokeOpacity: 0.5 }),
        ],
      });
      setTimeout(() => {
        const body = document.getElementById(`mini-${market}`);
        if (body) { body.innerHTML = ''; body.appendChild(chart); }
      }, 0);
    }
    return card;
  }

  // ========================================================================
  // 6.4.2 Regional heat-grid — distance-to-target
  // ========================================================================

  async function renderHeatGrid() {
    const grid = document.getElementById('heatgrid');
    const regionalEl = document.getElementById('heatgrid-regional');
    grid.innerHTML = '';
    regionalEl.innerHTML = '';

    const period = currentPeriod();
    const periodWeeks = periodWeeksSet(period);
    const cells = [];

    for (const mkt of MPE.ALL_MARKETS) {
      const md = (STATE.data.markets || {})[mkt];
      if (!md) continue;
      const supported = md.parameters?.supported_target_modes?.value_json || ['spend'];
      const ieTgt = md.parameters?.ieccp_target?.value_scalar;
      const op2Spend = md.op2_targets?.annual_spend_target;

      let out = null;
      let cellKlass = 'grey';
      let cellValue = '—', cellDelta = '—', cellMetric = '';
      try {
        if (supported.includes('ieccp') && ieTgt) {
          // ie%CCP-driver market: color by projected vs target
          out = V1_1_Slim.projectWithLockedYtd(
            md, 2026, 'ieccp', ieTgt * 100,
            { regimeMultiplier: STATE.regimeMultiplier, scenarioOverride: STATE.scenarioOverride, periodWeeks, periodType: period }
          );
          const projIe = out.totals.computed_ieccp;
          const target = ieTgt * 100;
          const delta = projIe != null ? projIe - target : 0;
          cellValue = projIe != null ? `${projIe.toFixed(0)}%` : 'n/a';
          cellDelta = projIe != null ? `${delta >= 0 ? '+' : ''}${delta.toFixed(1)}pp vs ${target.toFixed(0)}%` : '';
          cellMetric = 'Efficiency';
          const abs = Math.abs(delta);
          cellKlass = abs <= 5 ? 'green' : abs <= 15 ? 'yellow' : 'red';
        } else if (op2Spend) {
          // Spend-only market (AU/JP) — color by spend vs OP2
          out = V1_1_Slim.projectWithLockedYtd(
            md, 2026, 'spend', op2Spend,
            { regimeMultiplier: STATE.regimeMultiplier, scenarioOverride: STATE.scenarioOverride, periodWeeks, periodType: period }
          );
          const annualSpend = out.totals.annual_total_spend;
          const pct = op2Spend > 0 ? (annualSpend / op2Spend) * 100 : 0;
          cellValue = `${pct.toFixed(0)}%`;
          cellDelta = `${fmt$(annualSpend)} vs ${fmt$(op2Spend)}`;
          cellMetric = 'Spend vs OP2';
          const dev = Math.abs(pct - 100);
          cellKlass = dev <= 5 ? 'green' : dev <= 15 ? 'yellow' : 'red';
        }
      } catch (e) {
        console.error(`Heat grid ${mkt}:`, e);
      }

      const cell = document.createElement('div');
      cell.className = `heat-cell ${cellKlass}`;
      cell.title = `${mkt}: ${cellMetric} · click to drill in`;
      // Anomaly indicator (Phase 4.1 + 6.5.3)
      const mktAnoms = STATE.data?.anomalies?.markets?.[mkt] || [];
      const anomHasError = mktAnoms.some(a => a.severity === 'error');
      const anomHasWarn = mktAnoms.some(a => a.severity === 'warn');
      const anomBadge = anomHasError ? '<span style="position:absolute;top:4px;right:6px;color:var(--color-danger);font-size:12px;font-weight:700" title="' + mktAnoms.length + ' anomalies">●</span>'
        : anomHasWarn ? '<span style="position:absolute;top:4px;right:6px;color:var(--color-warning);font-size:12px;font-weight:700" title="' + mktAnoms.length + ' warnings">●</span>'
        : '';
      cell.style.position = 'relative';
      cell.innerHTML = `
        ${anomBadge}
        <div class="heat-market">${mkt}</div>
        <div class="heat-value">${cellValue}</div>
        <div class="heat-delta">${cellDelta}</div>
      `;
      cell.addEventListener('click', () => {
        document.getElementById('scope-select').value = mkt;
        switchView('single');
        refreshScopeDependentUI();
        scheduleRecompute();
      });
      grid.appendChild(cell);
      if (out) cells.push({ market: mkt, out });
    }

    // Regional rollup summary strip
    for (const reg of MPE.ALL_REGIONS) {
      const constituents = MPE.REGION_CONSTITUENTS[reg] || [];
      let brandR = 0, brandS = 0, nbR = 0, nbS = 0;
      let ieNum = 0, ieDen = 0;
      for (const { market, out } of cells) {
        if (!constituents.includes(market)) continue;
        const t = out.totals || {};
        brandR += t.annual_brand_regs || 0;
        brandS += t.annual_brand_spend || 0;
        nbR += t.annual_nb_regs || 0;
        nbS += t.annual_nb_spend || 0;
        const md = STATE.data.markets[market];
        const bCcp = md?.parameters?.brand_ccp?.value_scalar;
        const nCcp = md?.parameters?.nb_ccp?.value_scalar;
        if (bCcp != null && nCcp != null) {
          ieNum += (t.annual_brand_spend || 0) + (t.annual_nb_spend || 0);
          ieDen += ((t.annual_brand_regs || 0) * bCcp) + ((t.annual_nb_regs || 0) * nCcp);
        }
      }
      const regIe = ieDen > 0 ? (ieNum / ieDen) * 100 : null;
      const div = document.createElement('div');
      div.className = 'heat-region-summary';
      div.innerHTML = `
        <div class="region-name">${reg}</div>
        <div class="region-values">${fmtNum(brandR + nbR)} regs · ${fmt$(brandS + nbS)}</div>
        <div style="font-size:11px;color:var(--color-text-meta);margin-top:2px">Efficiency ${regIe != null ? regIe.toFixed(1) + '%' : 'n/a'}</div>
      `;
      regionalEl.appendChild(div);
    }
  }

  // ========================================================================
  // View switching (6.4.1 + 6.4.2 gates)
  // ========================================================================

  function switchView(view) {
    STATE.activeView = view;
    document.querySelectorAll('[data-view]').forEach(b => b.classList.toggle('active', b.dataset.view === view));
    document.getElementById('view-single').style.display = view === 'single' ? '' : 'none';
    document.getElementById('view-multiples').style.display = view === 'multiples' ? '' : 'none';
    document.getElementById('view-heatgrid').style.display = view === 'heatgrid' ? '' : 'none';
    // Hide the controls row on multi-market views since they apply global rules
    const controlsRow = document.querySelector('.controls-row');
    if (controlsRow) {
      controlsRow.style.display = view === 'single' ? '' : 'none';
    }
    if (view === 'multiples') renderSmallMultiples();
    else if (view === 'heatgrid') renderHeatGrid();
  }

  // ========================================================================
  // 6.4.4 Model View — sparklines in the drawer
  // ========================================================================

  function renderSparkline(values, opts) {
    opts = opts || {};
    if (!values || values.length === 0) return '';
    const w = opts.width || 100, h = opts.height || 20;
    const min = Math.min(...values), max = Math.max(...values);
    const range = max - min || 1;
    const pts = values.map((v, i) => {
      const x = (i / (values.length - 1)) * w;
      const y = h - ((v - min) / range) * (h - 2) - 1;
      return `${x.toFixed(1)},${y.toFixed(1)}`;
    }).join(' ');
    const color = opts.color || 'var(--color-brand)';
    return `<svg class="sparkline" width="${w}" height="${h}" xmlns="http://www.w3.org/2000/svg">
      <polyline points="${pts}" fill="none" stroke="${color}" stroke-width="1.5"/>
    </svg>`;
  }

  const EXPLAIN_TEXT = {
    trend_slope: `Weekly log-linear growth rate on Brand regs, fit on recent weeks with recency weighting (half-life 4w). Positive = growing, negative = declining. Capped at ±10%/wk to prevent wild extrapolation.`,
    regime_lift: `Active campaign lifts with their current effective multiplier. Peak × confidence × decay-status modifier. Dormant regimes drop to ~1.0 automatically as data stabilizes.`,
    nb_elasticity: `NB CPA response to spend: CPA ≈ exp(a) × spend^b. b near 1.0 = flat response (healthy), b > 1 = saturation (spending more drives CPA up disproportionately).`,
    locked_ytd: `Weeks of the year already locked (data is in). Remaining weeks are projected. The more YTD weeks, the tighter the forecast constrains to observed actuals.`,
  };

  function renderDrawerSparklines(marketData) {
    const section = document.getElementById('drawer-sparklines');
    if (!section) return;
    const ytd = marketData.ytd_weekly || [];
    const recent = ytd.slice(-8);
    const brandTrendSpark = renderSparkline(recent.map(w => w.brand_regs || 0), { color: 'var(--color-brand)' });

    // Trend slope
    const slope = (() => {
      if (recent.length < 4) return 0;
      const logs = recent.map(w => Math.log(Math.max(1, w.brand_regs || 1)));
      const n = logs.length;
      const xs = Array.from({ length: n }, (_, i) => i);
      const mx = xs.reduce((a, b) => a + b, 0) / n;
      const my = logs.reduce((a, b) => a + b, 0) / n;
      let num = 0, den = 0;
      for (let i = 0; i < n; i++) { num += (xs[i] - mx) * (logs[i] - my); den += (xs[i] - mx) * (xs[i] - mx); }
      return den > 0 ? num / den : 0;
    })();
    const slopePct = (slope * 100).toFixed(1);
    const slopeArrow = slope > 0.01 ? '↗' : slope < -0.01 ? '↘' : '→';

    // Regimes sparkline — current multiplier over 16 weeks forward
    const regimes = marketData.regime_fit_state || [];
    let regimeSpark = '';
    let regimeSummary = 'no active lifts';
    if (regimes.length > 0) {
      const today = new Date();
      const futureWeeks = Array.from({ length: 16 }, (_, i) => {
        const d = new Date(today);
        d.setDate(today.getDate() + i * 7);
        return d;
      });
      const mults = V1_1_Slim.computeRegimeMultipliersPerWeek(regimes, futureWeeks, 1.0);
      regimeSpark = renderSparkline(mults, { color: 'var(--color-regime)' });
      regimeSummary = regimes.map((r, i) => `#${i + 1} peak=${(r.peak_multiplier || 1).toFixed(2)}×`).join(' · ');
    }

    // NB elasticity
    const nbElast = marketData.parameters?.nb_cpa_elasticity?.value_json;
    const nbElastText = nbElast ? `b=${(nbElast.b || 0).toFixed(2)} · r²=${(nbElast.r_squared || 0).toFixed(2)}` : 'n/a';

    // Locked YTD sparkline — spend depletion (weekly spent / weekly target remaining)
    const op2Spend = marketData.op2_targets?.annual_spend_target || 0;
    const ytdSpendPerWeek = ytd.map(w => (w.brand_cost || 0) + (w.nb_cost || 0));
    const ytdTotal = ytdSpendPerWeek.reduce((a, b) => a + b, 0);
    const ytdSpark = renderSparkline(ytdSpendPerWeek, { color: 'var(--color-actuals)' });
    const weeksRemaining = Math.max(0, 52 - ytd.length);

    // Freshness badges — based on last_refit_at metadata
    const refitTs = marketData.parameters?.brand_cpa_elasticity?.last_refit_at;
    const hasRefitTs = !!refitTs;
    const refitAge = hasRefitTs ? (Date.now() - new Date(refitTs).getTime()) / (86400 * 1000) : null;
    const freshKlass = !hasRefitTs ? 'ancient' : refitAge < 2 ? 'fresh' : refitAge < 7 ? 'stale' : 'ancient';
    const freshText = !hasRefitTs ? 'refit age unknown' : refitAge < 2 ? 'refit today' : refitAge < 7 ? 'refit this week' : `refit ${Math.round(refitAge)}d ago`;

    section.innerHTML = `
      <div class="drawer-section-title">Model View</div>
      <div class="drawer-tile-sparkline">
        <div class="drawer-tile-head">
          <span>Brand trend slope <span class="freshness-badge ${freshKlass}">${freshText}</span></span>
          <span class="drawer-tile-value">${slope >= 0 ? '+' : ''}${slopePct}% wk ${slopeArrow}</span>
        </div>
        ${brandTrendSpark}
        <div style="font-size:10px;color:var(--color-text-subtle)">Last 8 weeks of Brand regs</div>
        <span class="drawer-tile-explain" data-explain="trend_slope">Explain this →</span>
      </div>
      <div class="drawer-tile-sparkline">
        <div class="drawer-tile-head">
          <span>Active campaign lifts</span>
          <span class="drawer-tile-value">${regimes.length}</span>
        </div>
        ${regimeSpark || '<div style="font-size:10px;color:var(--color-text-subtle)">no active lifts</div>'}
        <div style="font-size:10px;color:var(--color-text-subtle)">${regimeSummary}</div>
        <span class="drawer-tile-explain" data-explain="regime_lift">Explain this →</span>
      </div>
      <div class="drawer-tile-sparkline">
        <div class="drawer-tile-head">
          <span>NB CPA elasticity</span>
          <span class="drawer-tile-value">${nbElastText}</span>
        </div>
        <div style="font-size:10px;color:var(--color-text-subtle)">b close to 1 = linear response; b &gt; 1 = saturation</div>
        <span class="drawer-tile-explain" data-explain="nb_elasticity">Explain this →</span>
      </div>
      <div class="drawer-tile-sparkline">
        <div class="drawer-tile-head">
          <span>Locked YTD</span>
          <span class="drawer-tile-value">${fmt$(ytdTotal)} / ${weeksRemaining}w left</span>
        </div>
        ${ytdSpark}
        <div style="font-size:10px;color:var(--color-text-subtle)">${ytd.length} weeks of actuals locked</div>
        <span class="drawer-tile-explain" data-explain="locked_ytd">Explain this →</span>
      </div>
    `;

    section.querySelectorAll('[data-explain]').forEach(el => {
      el.addEventListener('click', () => {
        const key = el.dataset.explain;
        document.getElementById('modal-title').textContent = 'About this metric';
        document.getElementById('modal-body').innerHTML = `<p>${EXPLAIN_TEXT[key] || 'No explanation available.'}</p>`;
        document.getElementById('modal-overlay').classList.add('active');
      });
    });
  }

  // ========================================================================
  // 6.4.5 Scenario chip animated hero transition
  // ========================================================================

  function animateHeroTransition(prevTotals, newTotals) {
    const spend = newTotals?.total_spend || 0;
    const prevSpend = prevTotals?.total_spend || 0;
    const heroEl = document.getElementById('hero-number');
    if (!heroEl || prevSpend === 0) return;
    heroEl.classList.remove('flash-up', 'flash-down');
    void heroEl.offsetWidth;
    if (spend > prevSpend * 1.02) heroEl.classList.add('flash-up');
    else if (spend < prevSpend * 0.98) heroEl.classList.add('flash-down');
  }

  // ========================================================================
  // 6.5.3 Feedback bar — capture human judgment
  //   Hidden until user runs 3+ projections in session (localStorage counter).
  //   Writes to localStorage queue + (if server available) POSTs to endpoint.
  //   Server can batch-drain to ps.projection_feedback.
  // ========================================================================

  const FEEDBACK_QUEUE_KEY = 'mpe-feedback-queue';
  const PROJECTION_COUNT_KEY = 'mpe-session-projection-count';

  function incrementProjectionCount() {
    const n = parseInt(sessionStorage.getItem(PROJECTION_COUNT_KEY) || '0', 10) + 1;
    sessionStorage.setItem(PROJECTION_COUNT_KEY, String(n));
    return n;
  }

  function maybeShowFeedbackBar() {
    const n = parseInt(sessionStorage.getItem(PROJECTION_COUNT_KEY) || '0', 10);
    const bar = document.getElementById('feedback-bar');
    if (!bar) return;
    if (n >= 3) bar.style.display = '';
  }

  function wireFeedbackBar() {
    const radios = document.querySelectorAll('input[name="fb-verdict"]');
    const mag = document.getElementById('fb-magnitude');
    const txt = document.getElementById('fb-freetext');
    const sub = document.getElementById('fb-submit');
    const status = document.getElementById('fb-status');
    radios.forEach(r => {
      r.addEventListener('change', () => {
        const v = document.querySelector('input[name="fb-verdict"]:checked')?.value;
        // Enable contextual inputs
        mag.disabled = !(v === 'too_high' || v === 'too_low');
        txt.disabled = !(v === 'missing_context' || v === 'too_high' || v === 'too_low');
        if (v === 'missing_context') txt.setAttribute('required', '');
        else txt.removeAttribute('required');
        // Submit enabled once a verdict is picked (+ freetext if missing_context)
        sub.disabled = false;
        status.textContent = '';
      });
    });
    sub.addEventListener('click', () => {
      const verdict = document.querySelector('input[name="fb-verdict"]:checked')?.value;
      if (!verdict) return;
      if (verdict === 'missing_context' && !txt.value.trim()) {
        status.textContent = 'Please describe what\'s missing.';
        status.style.color = 'var(--color-danger)';
        return;
      }
      const record = {
        id: `fb-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`,
        projection_id: STATE.currentOutput?._projection_id || `proj-${Date.now()}`,
        user_id: 'prichwil',   // TODO: pull from auth session when available
        verdict,
        magnitude_pct: (verdict === 'too_high' || verdict === 'too_low') && mag.value
          ? parseFloat(mag.value) : null,
        freetext: txt.value.trim() || null,
        scope: currentScope(),
        time_period: currentPeriod(),
        target_mode: currentDriver(),
        target_value: currentTargetValue(),
        scenario_chip: STATE.activeChipId || 'mixed',
        submitted_at: new Date().toISOString(),
      };
      // Append to queue
      const queue = JSON.parse(localStorage.getItem(FEEDBACK_QUEUE_KEY) || '[]');
      queue.push(record);
      localStorage.setItem(FEEDBACK_QUEUE_KEY, JSON.stringify(queue));
      status.textContent = `Thanks. Saved locally (${queue.length} queued for sync).`;
      status.style.color = 'var(--color-success)';
      // Reset
      radios.forEach(r => (r.checked = false));
      mag.value = ''; mag.disabled = true;
      txt.value = ''; txt.disabled = true;
      sub.disabled = true;
    });
  }

  // ========================================================================
  // Init + event wiring
  // ========================================================================

  async function init() {
    const ok = await loadData();
    if (!ok) return;

    populateScopeSelector();
    refreshScopeDependentUI();
    bindDisclosureButtons();
    wireFeedbackBar();
    renderHeaderAnomalies();

    // View switcher (6.4.1 / 6.4.2)
    document.querySelectorAll('[data-view]').forEach(btn => {
      btn.addEventListener('click', () => switchView(btn.dataset.view));
    });

    // Controls
    document.getElementById('scope-select').addEventListener('change', () => {
      // Round 6 V6-4: reset transient chart-overlay state on market change so
      // the counterfactual overlay / active scenario chip don't bleed across
      // scopes. Recompute will re-derive the Planned scenario.
      STATE.disclosures.counter = false;
      STATE.activeChipId = 'mixed';
      STATE.scenarioOverride = null;
      document.querySelectorAll('[data-disclosure="counter"]').forEach(b => b.classList.remove('active'));
      refreshScopeDependentUI();
      scheduleRecompute();
    });
    document.getElementById('period-select').addEventListener('change', () => {
      scheduleRecompute();
      // If on multi-market view, refresh those too
      if (STATE.activeView === 'multiples') renderSmallMultiples();
      else if (STATE.activeView === 'heatgrid') renderHeatGrid();
    });
    document.getElementById('driver-select').addEventListener('change', () => {
      seedTargetValue();
      scheduleRecompute();
    });
    document.getElementById('target-input').addEventListener('change', () => {
      validateTargetInput();
      scheduleRecompute();
    });
    document.getElementById('target-input').addEventListener('input', () => {
      validateTargetInput();
      clearTimeout(recomputeTimer);
      recomputeTimer = setTimeout(() => recompute({ animated: false }), 300);
    });
    // Round 5 V-3: browser <input type="number"> silently strips non-numeric
    // input before JS sees it. On blur, if the field is empty (user typed
    // "abc" and the browser zeroed it), show an explicit "Enter a number."
    // rather than silently accepting zero.
    document.getElementById('target-input').addEventListener('blur', (e) => {
      if (e.target.value === '' || e.target.value == null) {
        const errEl = document.getElementById('target-input-error');
        if (errEl) {
          errEl.textContent = 'Enter a number.';
          errEl.style.display = '';
        }
        e.target.setAttribute('aria-invalid', 'true');
      }
    });
    const slider = document.getElementById('regime-slider');
    slider.addEventListener('input', (e) => {
      STATE.regimeMultiplier = parseFloat(e.target.value);
      document.getElementById('regime-slider-val').textContent = STATE.regimeMultiplier.toFixed(2) + '×';
      document.querySelectorAll('.chip').forEach(c => c.classList.remove('active'));
      clearTimeout(recomputeTimer);
      recomputeTimer = setTimeout(() => recompute({ animated: false }), 250);
    });

    document.getElementById('btn-recompute').addEventListener('click', () => recompute({ animated: true }));
    document.getElementById('btn-save').addEventListener('click', saveProjection);
    // btn-share removed from HTML 2026-04-27 per Round 3 feedback (see session-log).
    // Share card function retained for potential future use; binding deleted to prevent
    // TypeError on init that was hanging the whole page (Round 4 R4-1).
    void shareCardClick; // suppress unused-warning from tooling

    document.getElementById('drawer-close').addEventListener('click', () => {
      STATE.disclosures.params = false;
      document.querySelector('[data-disclosure="params"]').classList.remove('active');
      document.getElementById('drawer').classList.remove('open');
    });

    document.getElementById('ytd-wall-dismiss').addEventListener('click', () => {
      document.getElementById('ytd-wall-banner').classList.remove('active');
    });

    // loading-skip was removed from HTML when the 4-stage overlay collapsed to single
    // "Recomputing" stage (Round 3). Safely no-op if the element isn't there.
    const skipBtn = document.getElementById('loading-skip');
    if (skipBtn) skipBtn.addEventListener('click', () => hideLoading());

    document.getElementById('modal-close').addEventListener('click', () => {
      document.getElementById('modal-overlay').classList.remove('active');
    });
    document.getElementById('modal-overlay').addEventListener('click', (e) => {
      if (e.target.id === 'modal-overlay') {
        document.getElementById('modal-overlay').classList.remove('active');
      }
    });

    // ESC to skip animations / close panels
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        hideLoading();
        document.getElementById('drawer').classList.remove('open');
        document.getElementById('modal-overlay').classList.remove('active');
      }
    });

    // Seed defaults: MX Y2026 @ 75% ie%CCP with animated arrival
    document.getElementById('scope-select').value = DEFAULT_SCOPE;
    document.getElementById('period-select').value = DEFAULT_PERIOD;
    document.getElementById('driver-select').value = DEFAULT_DRIVER;
    document.getElementById('target-input').value = DEFAULT_TARGET_VALUE;
    refreshScopeDependentUI();
    // Override the seeded target (seedTargetValue uses market's own ieccp_target)
    document.getElementById('target-input').value = DEFAULT_TARGET_VALUE;
    updateHeaderMeta();
    renderSavedList();

    // Initial animated recompute
    await recompute({ animated: true });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
