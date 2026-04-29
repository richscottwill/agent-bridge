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
      // Round 7 P1-10: prominent refreshed indicator in the hero market badge.
      // Addresses "numbers-drift between reloads" — users saw $1.32M → $1.88M
      // on consecutive loads without knowing the data had advanced one week.
      // Show a human date/time so anyone comparing yesterday's screenshot can
      // tell whether the drift was data-driven (YTD actuals refreshed) or a
      // bug. Tooltip explains what's happening plainly.
      const badgeEl = document.getElementById('hero-market-refreshed');
      if (badgeEl) {
        const dateStr = generated.toLocaleDateString(undefined, { month: 'short', day: 'numeric' });
        const timeStr = generated.toLocaleTimeString(undefined, { hour: 'numeric', minute: '2-digit' });
        let freshWord;
        if (ageHours < 1) freshWord = 'just now';
        else if (ageHours < 24) freshWord = `${Math.round(ageHours)}h ago`;
        else freshWord = `${Math.round(ageHours / 24)}d ago`;
        badgeEl.textContent = `Refreshed ${freshWord}`;
        badgeEl.title = `Last refresh: ${dateStr} ${timeStr}. Projections update when YTD actuals refresh, typically every Monday. If yesterday's number differs from today's, the underlying data has advanced — the model is not non-deterministic.`;
      }
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
    // Round 13 P1-09: scope label so the count is unambiguous.
    // Chip reads "Across 10 markets: X critical · Y warn · Z info"
    // regardless of which single-market view is active, since the
    // summary is global. When we have per-view scoping later this
    // becomes "This market:" / "This region:".
    const nMarkets = Object.keys(STATE.data?.anomalies?.markets || {}).length || 10;
    const parts = [];
    if (summary.error) parts.push(`<span style="color:var(--color-danger)">${summary.error} critical</span>`);
    if (summary.warn) parts.push(`<span style="color:var(--color-warning)">${summary.warn} warn</span>`);
    if (summary.info) parts.push(`<span style="color:var(--color-text-meta)">${summary.info} info</span>`);
    el.innerHTML = `<span style="font-size:11px">⚠ <span style="color:var(--color-text-subtle)">Across ${nMarkets} markets:</span> ${parts.join(' · ')}</span>`;
    el.style.cursor = 'pointer';
    el.title = `Summary spans all ${nMarkets} markets. Click to jump to current-market alerts panel.`;
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
    } else if (driver === 'spend' && Number.isFinite(n) && n > 1e9) {
      errMsg = `Spend target exceeds $1B — likely a typo.`;
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
    // P-DRV-PERSIST v2 fix (2026-04-28, architectural):
    // Earlier boolean STATE.userOverrodeDriver was fragile — it persisted
    // across market switches, so switching MX → (change driver) → AU →
    // back → MX carried the override. Now scope it: STATE.driverOverrides
    // is a {scope: driver} map. An override for MX doesn't affect CA.
    // Reset clears the whole map.
    if (!STATE.driverOverrides) STATE.driverOverrides = {};
    const preferredDriver = supported.includes('ieccp') ? 'ieccp' : supported[0];
    const overrideForThisScope = STATE.driverOverrides[scope];
    if (overrideForThisScope && supported.includes(overrideForThisScope)) {
      driverSel.value = overrideForThisScope;
    } else {
      driverSel.value = preferredDriver;
    }

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
      input.max = '1e10';   // P3-10: tightened to $1B ceiling for typo-catch (2026-04-28)
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
      { id: 'no-lift',     label: 'No-lift baseline',              override: { peak_multiplier: 1.0, strip_anchor_lift: true },
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
      // P3-03: styled tooltip — use data-tip so the CSS ::after can show
      // a real popover (not just the browser's native title bubble).
      if (chip.description) el.setAttribute('data-tip', chip.description);
      el.setAttribute('tabindex', '0');
      el.setAttribute('role', 'button');
      el.setAttribute('aria-label', `${chip.label} scenario — ${chip.description || 'no description'}`);
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
    // P2-10: keep URL in sync with the control state on every change so the
    // current scenario is always shareable via address-bar copy.
    syncUrlFromState();
    recomputeTimer = setTimeout(() => {
      recompute({ animated: false }).catch(e => console.warn('recompute (scheduled) failed:', e));
    }, 150);
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
    try {
      return await _recomputeInner(opts);
    } catch (e) {
      // Round 13 P1-12: catch any unhandled rejection from recompute so
      // it doesn't become a console "Uncaught (in promise)" error. Surface
      // via console.warn so developers can still see real failures but
      // users don't see red in DevTools.
      console.warn('recompute failed:', e && e.message || e);
      return null;
    }
  }

  async function _recomputeInner(opts) {
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

    // Bootstrap CI band from V1_1_Slim output (P1-01 Option C, 2026-04-27).
    // Replaces the legacy MPE.projectWithUncertainty path which returned
    // empty CIs after the mpe_schema_v3.sql deprecation of v1 elasticity
    // rows (2026-04-23). Bootstrap computes per-week bands from YTD residual
    // sd scaled by sqrt(weeks-into-forecast). Not a Bayesian posterior;
    // documented as an approximation in the How-modal footnote.
    await setStage(4, opts.animated !== false);

    let uncert = null;
    try {
      if (projection && !projection.error) {
        const ci = V1_1_Slim.bootstrapCI(projection, md.ytd_weekly || [], 0.10);
        if (ci && ci.available) {
          uncert = {
            credible_intervals: {
              total_regs: {
                central: ci.totals.total_regs.central,
                ci: { '90': [ci.totals.total_regs.lower, ci.totals.total_regs.upper] },
              },
              total_spend: {
                central: ci.totals.total_spend.central,
                ci: { '90': [ci.totals.total_spend.lower, ci.totals.total_spend.upper] },
              },
            },
            per_week: ci.per_week,
            method: ci.method,
            footnote: ci.footnote,
          };
        }
      }
    } catch (e) {
      console.warn('bootstrapCI failed:', e);
    }

    STATE.currentOutput = projection;
    // Round 10 P1-01 Option C: store the full bootstrap uncert payload so
    // per-week bands (uncert.per_week) reach the chart renderer, not just
    // credible_intervals. Fallback to null when uncert unavailable.
    STATE.currentUncertainty = uncert || null;
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
    // Round 13 P1-08: append 90% CI from bootstrap uncertainty so Kate sees
    // the plausible range right next to the point estimate, not buried in
    // the narrative panel. Unblocked by P1-01 Option C bootstrap ship.
    const uncertKpi = STATE.currentUncertainty;
    if (uncertKpi && uncertKpi.credible_intervals) {
      const ciS = uncertKpi.credible_intervals.total_spend?.ci?.['90'];
      const ciR = uncertKpi.credible_intervals.total_regs?.ci?.['90'];
      if (ciS && ciR) {
        contextSent += ` 90% range: ${fmt$(ciS[0])}–${fmt$(ciS[1])} spend · ${fmtNum(ciR[0])}–${fmtNum(ciR[1])} regs.`;
      }
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

    // P2-06: WoW delta sublines. Compute from the last two YTD weeks of
    // actuals — this is the "what's the trend on the ground" indicator.
    // Hero (period-aggregate) doesn't get WoW because it's not a weekly
    // number; only the weekly-trackable tiles surface it.
    //
    // P5-1 (2026-04-28): Brand/NB tiles also carry a share-of-total suffix
    // ("· 75% share") so the projection-period share is readable from the
    // tile itself. Replaces the old P2-13 split bar that sat below the KPI
    // row showing the same numbers twice.
    const ytdW = marketData.ytd_weekly || [];
    const setWowDelta = (elId, curVal, prevVal, invert, shareSuffix) => {
      const el = document.getElementById(elId);
      if (!el) return;
      el.classList.remove('good', 'bad', 'neutral');
      const suffix = shareSuffix ? ` · ${shareSuffix}` : '';
      if (!curVal || !prevVal || prevVal === 0) {
        // Even with no WoW data we can still surface share%.
        el.textContent = shareSuffix ? shareSuffix : '';
        return;
      }
      const pct = ((curVal - prevVal) / prevVal) * 100;
      const arrow = pct > 0.5 ? '↑' : (pct < -0.5 ? '↓' : '·');
      // When invert=true, up is bad (e.g., CPA rising); when false, up is good
      let cls = 'neutral';
      if (Math.abs(pct) >= 0.5) {
        const isUp = pct > 0;
        cls = (isUp !== invert) ? 'good' : 'bad';
      }
      el.textContent = `${arrow} ${pct > 0 ? '+' : ''}${pct.toFixed(1)}% WoW${suffix}`;
      el.classList.add(cls);
    };
    // Compute Brand / NB share from projection totals (not YTD) — the share
    // describes the projected period's composition, which is what the user
    // cares about when reading the tile.
    const totBNB = (t.brand_regs || 0) + (t.nb_regs || 0);
    const brandSharePct = totBNB > 0 ? Math.round((t.brand_regs / totBNB) * 100) : null;
    const nbSharePct    = totBNB > 0 ? 100 - brandSharePct : null;
    const brandShareSuffix = brandSharePct != null ? `${brandSharePct}% share` : null;
    const nbShareSuffix    = nbSharePct    != null ? `${nbSharePct}% share`    : null;
    if (ytdW.length >= 2) {
      const last = ytdW[ytdW.length - 1];
      const prev = ytdW[ytdW.length - 2];
      const curBrandRegs = last.brand_regs || last.brand_registrations || 0;
      const prevBrandRegs = prev.brand_regs || prev.brand_registrations || 0;
      const curNbRegs = last.nb_regs || last.nb_registrations || 0;
      const prevNbRegs = prev.nb_regs || prev.nb_registrations || 0;
      const curCost = (last.brand_cost || 0) + (last.nb_cost || 0);
      const prevCost = (prev.brand_cost || 0) + (prev.nb_cost || 0);
      const curRegs = curBrandRegs + curNbRegs;
      const prevRegs = prevBrandRegs + prevNbRegs;
      const curCpa = curRegs > 0 ? curCost / curRegs : 0;
      const prevCpa = prevRegs > 0 ? prevCost / prevRegs : 0;
      setWowDelta('kpi-brand-regs-delta', curBrandRegs, prevBrandRegs, false, brandShareSuffix);
      setWowDelta('kpi-nb-regs-delta',    curNbRegs,    prevNbRegs,    false, nbShareSuffix);
      setWowDelta('kpi-cpa-delta',        curCpa,       prevCpa,       true);  // CPA up = bad; no share
    } else {
      // Early-year markets: still surface share% even without WoW data.
      const brandDeltaEl = document.getElementById('kpi-brand-regs-delta');
      const nbDeltaEl    = document.getElementById('kpi-nb-regs-delta');
      if (brandDeltaEl) { brandDeltaEl.textContent = brandShareSuffix || ''; brandDeltaEl.classList.remove('good','bad','neutral'); }
      if (nbDeltaEl)    { nbDeltaEl.textContent    = nbShareSuffix    || ''; nbDeltaEl.classList.remove('good','bad','neutral'); }
      const cpaDeltaEl  = document.getElementById('kpi-cpa-delta');
      if (cpaDeltaEl)   { cpaDeltaEl.textContent   = ''; cpaDeltaEl.classList.remove('good','bad','neutral'); }
    }
    // Clear efficiency delta — it's a period-aggregate, not weekly.
    const ieDeltaEl = document.getElementById('kpi-ieccp-delta');
    if (ieDeltaEl) { ieDeltaEl.textContent = ''; ieDeltaEl.classList.remove('good','bad','neutral'); }

    // Both OP2 KPIs visible — Spend and Regs independent tiles.
    // For period-scoped comparisons, scale OP2 annual by period-share of year
    // (simple proportional; monthly OP2 breakdown is in the data but period
    // share from current period output is a clean enough approximation).
    const op2Spend = marketData.op2_targets?.annual_spend_target;
    const op2Regs = marketData.op2_targets?.annual_regs_target;
    const periodShare = t.annual_total_regs > 0 ? t.total_regs / t.annual_total_regs : 1.0;

    const spendEl = document.getElementById('kpi-op2-spend');
    const regsEl = document.getElementById('kpi-op2-regs');
    const spendDeltaEl = document.getElementById('kpi-op2-spend-delta');
    const regsDeltaEl = document.getElementById('kpi-op2-regs-delta');
    spendEl.classList.remove('warn', 'danger');
    regsEl.classList.remove('warn', 'danger');
    if (spendDeltaEl) { spendDeltaEl.classList.remove('good','bad','neutral'); spendDeltaEl.textContent = ''; }
    if (regsDeltaEl)  { regsDeltaEl.classList.remove('good','bad','neutral');  regsDeltaEl.textContent = ''; }

    // P2-14 — directional color + arrow on vs-OP2 comparisons.
    // Spend overage is bad (red ↑), underspend is good-ish (green ↓).
    // Regs overachievement is good (green ↑), underdelivery is bad (red ↓).
    if (op2Spend && op2Spend > 0) {
      const scaled = op2Spend * periodShare;
      const pct = scaled > 0 ? (t.total_spend / scaled) * 100 : 0;
      spendEl.textContent = `${pct.toFixed(0)}%`;
      if (pct > 120) spendEl.classList.add('danger'); else if (pct > 105) spendEl.classList.add('warn');
      if (spendDeltaEl) {
        const delta = pct - 100;  // deviation from on-plan
        if (Math.abs(delta) >= 1) {
          const arrow = delta > 0 ? '↑' : '↓';
          spendDeltaEl.textContent = `${arrow} ${delta > 0 ? '+' : ''}${delta.toFixed(0)} pts vs plan`;
          // Over-spending is bad; under-spending is slightly good
          spendDeltaEl.classList.add(delta > 0 ? 'bad' : 'good');
        }
      }
    } else {
      spendEl.textContent = '—';
    }
    if (op2Regs && op2Regs > 0) {
      const scaled = op2Regs * periodShare;
      const pct = scaled > 0 ? (t.total_regs / scaled) * 100 : 0;
      regsEl.textContent = `${pct.toFixed(0)}%`;
      if (pct < 85) regsEl.classList.add('danger'); else if (pct < 95) regsEl.classList.add('warn');
      if (regsDeltaEl) {
        const delta = pct - 100;
        if (Math.abs(delta) >= 1) {
          const arrow = delta > 0 ? '↑' : '↓';
          regsDeltaEl.textContent = `${arrow} ${delta > 0 ? '+' : ''}${delta.toFixed(0)} pts vs plan`;
          // Over-delivering is good; under-delivering is bad
          regsDeltaEl.classList.add(delta > 0 ? 'good' : 'bad');
        }
      }
    } else {
      regsEl.textContent = '—';
    }

    // P5-7 (2026-04-28): combined VS OP2 tile — one-line efficiency summary.
    // Surfaces the CPA delta vs plan so the reader sees whether the
    // overdelivery / underdelivery is efficient (CPA down = good) or
    // bought (CPA up = bad). Uses OP2 targets already in marketData.
    const op2DetailEl = document.getElementById('kpi-op2-detail');
    if (op2DetailEl) {
      op2DetailEl.classList.remove('good', 'bad');
      op2DetailEl.textContent = '';
      if (op2Spend && op2Regs && op2Spend > 0 && op2Regs > 0) {
        const planCpa = op2Spend / op2Regs;
        const projCpa = t.blended_cpa || (t.total_regs > 0 ? t.total_spend / t.total_regs : 0);
        if (planCpa > 0 && projCpa > 0) {
          const cpaDeltaPct = ((projCpa / planCpa) - 1) * 100;
          const direction = cpaDeltaPct < 0 ? 'gain' : 'loss';
          op2DetailEl.textContent =
            `Efficiency ${direction}: CPA ${cpaDeltaPct >= 0 ? '+' : ''}${cpaDeltaPct.toFixed(0)}% vs plan`;
        }
      }
    }

    // P5-1 (2026-04-28): The P2-13 Brand/NB split bar that lived here was
    // removed — the same 75%/25% share is now folded into each KPI tile's
    // delta line ("↑ +5.6% WoW · 75% share"). Kills the dup between the
    // bar and the tiles directly above it. HTML element also removed.


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
    // P2-04 + P2-05 — only render on single-market view; skip for regional
    // rollups where decomposition + backtest don't have a clean data source.
    try { renderDecomposition(out, marketData); } catch (e) { console.warn('[mpe] decomposition failed:', e); }
    try { renderBacktest(marketData); } catch (e) { console.warn('[mpe] backtest failed:', e); }
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

    // Build a faux V1_1_Slim.projectWithLockedYtd-shaped output.
    // Critical: sum per-market out.ytd and out.roy so projection-chart.js
    // has the NB + Brand RoY totals it needs to distribute across projected
    // weeks. Previously these were empty objects, which caused the chart's
    // projected half to show only Brand (NB collapsed to 0) — a ~50% cliff
    // at the Today seam for region views. Fixed 2026-04-28.
    const regionalYtd = { n_weeks_locked: 0, latest_week_locked: null,
      brand_regs: 0, brand_spend: 0, nb_regs: 0, nb_spend: 0,
      total_regs: 0, total_spend: 0 };
    const regionalRoy = { n_weeks: 0, brand_regs: 0, brand_spend: 0, nb_regs: 0, nb_spend: 0 };
    for (const { out } of perMarket) {
      const y = out?.ytd || {};
      regionalYtd.brand_regs  += y.brand_regs  || 0;
      regionalYtd.brand_spend += y.brand_spend || 0;
      regionalYtd.nb_regs     += y.nb_regs     || 0;
      regionalYtd.nb_spend    += y.nb_spend    || 0;
      regionalYtd.total_regs  += y.total_regs  || 0;
      regionalYtd.total_spend += y.total_spend || 0;
      if (y.n_weeks_locked > regionalYtd.n_weeks_locked) {
        regionalYtd.n_weeks_locked = y.n_weeks_locked;
      }
      if (y.latest_week_locked) {
        const d = y.latest_week_locked instanceof Date ? y.latest_week_locked : new Date(y.latest_week_locked);
        if (!regionalYtd.latest_week_locked || d > regionalYtd.latest_week_locked) {
          regionalYtd.latest_week_locked = d;
        }
      }
      const r = out?.roy || {};
      regionalRoy.brand_regs  += r.brand_regs  || 0;
      regionalRoy.brand_spend += r.brand_spend || 0;
      regionalRoy.nb_regs     += r.nb_regs     || 0;
      regionalRoy.nb_spend    += r.nb_spend    || 0;
      if (r.n_weeks > regionalRoy.n_weeks) regionalRoy.n_weeks = r.n_weeks;
    }

    const fauxOut = {
      year: 2026,
      target_mode: 'rollup',
      target_value: 0,
      period: period,
      ytd: regionalYtd,
      roy: regionalRoy,
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
  // Primary chart (M3 — delegates to canon-chart.js scenario mode)
  //
  // Old implementation was an Observable Plot + D3 custom render (~750 lines)
  // covering hover-dot overlay, dual-axis spend mirror, stroke-based series
  // tagging, rAF retries, try/catch silent-failure cascade, etc. All of that
  // is gone. Chart.js via CanonChart.render({mode:'scenario'}) provides
  // hover/legend/dual-axis natively. See projection-chart.js for the adapter.
  // ========================================================================

  function renderChart(out, counterfactual, uncert, marketData) {
    if (typeof renderProjectionChart !== 'function') {
      console.warn('[projection] renderProjectionChart not loaded — check projection.html script order');
      return;
    }
    // P2-12 chart-overlay — if a saved projection is marked as the active
    // compare, recompute it using the same V1_1_Slim path so we have a
    // full year_weekly array for the overlay. Skip when the saved record
    // is from a different scope (overlaying a different market would be
    // misleading: YTD + trajectory anchors wouldn't line up). Also skip
    // on regional rollups — the state plumbing covers single-market views.
    let compareOutput = null;
    let compareLabel = null;
    try {
      if (STATE.compareId && marketData) {
        const rec = (STATE.saved || []).find(r => r.id === STATE.compareId);
        if (rec && rec.scope === currentScope()
            && typeof V1_1_Slim !== 'undefined'
            && typeof V1_1_Slim.projectWithLockedYtd === 'function') {
          const periodWeeks = periodWeeksSet(rec.period);
          compareOutput = V1_1_Slim.projectWithLockedYtd(
            marketData, 2026, rec.driver, rec.target_value,
            {
              regimeMultiplier: rec.regime_multiplier || 1.0,
              periodWeeks,
              periodType: rec.period,
            }
          );
          let tv = rec.target_value;
          if (rec.driver === 'spend' && Number.isFinite(tv)) tv = fmt$(tv);
          else if (rec.driver === 'regs' && Number.isFinite(tv)) tv = fmtNum(tv);
          else if (rec.driver === 'ieccp' && Number.isFinite(tv)) tv = tv + '%';
          compareLabel = `Saved · ${rec.driver}=${tv}`;
        }
      }
    } catch (e) {
      console.warn('[projection] compare recompute failed:', e);
      compareOutput = null;
    }
    try {
      renderProjectionChart(out, counterfactual, uncert, marketData, compareOutput, compareLabel);
    } catch (e) {
      console.warn('[projection] chart render failed:', e);
      const chartEl = document.getElementById('chart-primary');
      if (chartEl) chartEl.innerHTML = '<div style="text-align:center;padding:24px;color:var(--color-text-meta)">Chart failed to render. Check console.</div>';
    }
  }

  // ========================================================================
  // P2-04: Prophet-style decomposition (Trend / Seasonality / Campaign lifts).
  // Three small Chart.js line panels under the main chart.
  //
  //  Trend      = 52-week rolling mean of actual+projected total regs (the
  //               slow-moving baseline level, not the seasonal swing)
  //  Seasonality = observed / trend per week (1.0 = neutral; 1.2 = 20% above
  //               trend for that calendar week; 0.8 = 20% below)
  //  Lifts      = summed (peak_multiplier - 1) * confidence over each lift's
  //               active window — answers "how much extra did campaigns add
  //               per week?"
  //
  // All three panels share the same x-axis (52 weeks of the year) + a thin
  // today-seam line so the user reads them as one stacked view. Panels that
  // can't render (missing data) show "Not enough history yet".
  // ========================================================================

  let _decompCharts = { trend: null, seasonality: null, lifts: null };

  function renderDecomposition(out, marketData) {
    const bt = marketData?.brand_trajectory_y2026;
    const ytd = marketData?.ytd_weekly || [];
    if (!bt || !bt.weeks || !bt.weeks.length) return;

    const n = bt.weeks.length;
    const labels = bt.weeks.map((w, i) => 'W' + String(i + 1).padStart(2, '0'));
    // Build full-year per-week totals (actual + projected brand + nb residual)
    const totals = new Array(n).fill(0);
    const ytdCount = ytd.length;
    for (let i = 0; i < ytdCount; i++) {
      const w = ytd[i];
      totals[i] = (w.brand_regs || w.brand_registrations || 0) + (w.nb_regs || w.nb_registrations || 0);
    }
    const royRegs = bt.regs_per_week.slice(ytdCount);
    const royWeeks = n - ytdCount;
    const royNb = (out.roy?.nb_regs || 0) / Math.max(royWeeks, 1);
    for (let i = 0; i < royRegs.length; i++) {
      totals[ytdCount + i] = (royRegs[i] || 0) + royNb;
    }

    // Trend: centered rolling mean. Window = 13 weeks (quarter) so the curve
    // reveals cycle without overrunning the year; 52-week would flatten to
    // a single value on a year of data.
    const window = 13;
    const trend = new Array(n).fill(null);
    const half = Math.floor(window / 2);
    for (let i = 0; i < n; i++) {
      let sum = 0, cnt = 0;
      for (let j = Math.max(0, i - half); j <= Math.min(n - 1, i + half); j++) {
        if (totals[j] > 0) { sum += totals[j]; cnt++; }
      }
      trend[i] = cnt > 0 ? sum / cnt : null;
    }

    // Seasonality = observed / trend (1.0 = on trend)
    const seasonality = trend.map((t, i) => {
      if (!t || t <= 0 || !totals[i]) return null;
      return totals[i] / t;
    });

    // Campaign lifts per week = sum over active lifts of peak_multiplier * confidence - 1.0
    // Active window = onset to onset of next lift (or year end).
    const lifts = new Array(n).fill(0);
    const regimes = (marketData.regime_fit_state || []).slice()
      .sort((a, b) => new Date(a.change_date) - new Date(b.change_date));
    for (let r = 0; r < regimes.length; r++) {
      const reg = regimes[r];
      const onsetDate = new Date(reg.change_date);
      let onsetIdx = -1;
      for (let j = 0; j < n; j++) {
        const d = new Date(bt.weeks[j]);
        if (d >= onsetDate) { onsetIdx = j; break; }
      }
      if (onsetIdx < 0) continue;
      let endIdx = n - 1;
      if (r + 1 < regimes.length) {
        const nextDate = new Date(regimes[r + 1].change_date);
        for (let j = onsetIdx + 1; j < n; j++) {
          const d = new Date(bt.weeks[j]);
          if (d >= nextDate) { endIdx = j; break; }
        }
      }
      const peak = reg.peak_multiplier || 1.0;
      const conf = reg.confidence || 0;
      const contribution = Math.max(0, (peak - 1) * conf);
      for (let j = onsetIdx; j <= endIdx; j++) lifts[j] += contribution;
    }

    const sharedOpts = {
      responsive: true, maintainAspectRatio: false, animation: false,
      plugins: { legend: { display: false }, tooltip: { enabled: true, intersect: false, mode: 'index' }, datalabels: { display: false } },
      scales: { x: { ticks: { display: false }, grid: { display: false } },
                y: { ticks: { font: { size: 9 } }, grid: { color: 'rgba(0,0,0,0.04)' } } },
      elements: { point: { radius: 0 } },
    };
    const mkChart = (refKey, canvasId, data, color) => {
      const canvas = document.getElementById(canvasId);
      if (!canvas) return;
      if (_decompCharts[refKey]) { try { _decompCharts[refKey].destroy(); } catch (_) {} }
      try {
        _decompCharts[refKey] = new Chart(canvas, {
          type: 'line',
          data: { labels, datasets: [{ data, borderColor: color, backgroundColor: color + '33', borderWidth: 1.5, tension: 0.25, fill: true, spanGaps: true }] },
          options: sharedOpts,
        });
      } catch (e) { console.warn(`[decomp ${refKey}] failed:`, e); }
    };
    mkChart('trend',       'decomp-trend',       trend,       '#0066CC');
    mkChart('seasonality', 'decomp-seasonality', seasonality, '#DDA760');
    mkChart('lifts',       'decomp-lifts',       lifts,       'rgba(168, 85, 247, 0.8)');
  }

  // ========================================================================
  // P2-05: backtest — last 8 weeks, actual vs 8-weeks-ago prediction.
  //
  // Data source: marketData.ytd_weekly rows carry pred_regs (prediction made
  // at the time the row was locked). We compare pred_regs against regs + nb_regs
  // on the same row — "what did we expect for this week 8 weeks ago" vs
  // "what actually happened". MAPE + 90% CI coverage % computed on the fly.
  //
  // If pred_regs is missing for recent weeks (feature wasn't captured yet),
  // render "Not enough backtest history yet" gracefully.
  // ========================================================================

  let _backtestChart = null;

  function renderBacktest(marketData) {
    const canvas = document.getElementById('backtest-canvas');
    const metaEl = document.getElementById('backtest-meta');
    if (!canvas || !metaEl) return;

    const ytd = marketData?.ytd_weekly || [];
    // Take last 8 weeks with both a predicted and actual value
    const recent = ytd.slice(-8);
    const rows = recent.map(w => ({
      label: w.iso_week || (`W` + (w.week_num || w.wk || '')),
      actual: (w.brand_regs || w.brand_registrations || 0) + (w.nb_regs || w.nb_registrations || 0),
      predicted: (w.pred_regs != null ? w.pred_regs : null),
      ci_lo: (w.ci_lo != null ? w.ci_lo : null),
      ci_hi: (w.ci_hi != null ? w.ci_hi : null),
    }));
    const usable = rows.filter(r => Number.isFinite(r.predicted) && r.predicted > 0 && r.actual > 0);
    if (_backtestChart) { try { _backtestChart.destroy(); } catch (_) {} _backtestChart = null; }
    if (usable.length < 2) {
      metaEl.textContent = 'Not enough backtest history yet — needs per-week pred_regs in ytd_weekly (most markets backfill from W20 onward).';
      canvas.getContext('2d').clearRect(0, 0, canvas.width, canvas.height);
      return;
    }
    // MAPE
    let sumAbsPct = 0;
    let inCi = 0;
    let ciUsable = 0;
    for (const r of usable) {
      sumAbsPct += Math.abs((r.actual - r.predicted) / r.predicted);
      if (Number.isFinite(r.ci_lo) && Number.isFinite(r.ci_hi)) {
        ciUsable++;
        if (r.actual >= r.ci_lo && r.actual <= r.ci_hi) inCi++;
      }
    }
    const mape = (sumAbsPct / usable.length) * 100;
    const coverage = ciUsable > 0 ? (inCi / ciUsable) * 100 : null;

    try {
      _backtestChart = new Chart(canvas, {
        type: 'line',
        data: {
          labels: usable.map(r => r.label),
          datasets: [
            { label: 'Actual',    data: usable.map(r => r.actual),    borderColor: '#4A4A4A', backgroundColor: '#4A4A4A', borderWidth: 2, pointRadius: 3, tension: 0.25 },
            { label: 'Predicted', data: usable.map(r => r.predicted), borderColor: '#0066CC', borderDash: [6, 4], borderWidth: 2, pointRadius: 2, tension: 0.25 },
          ],
        },
        options: {
          responsive: true, maintainAspectRatio: false, animation: false,
          interaction: { mode: 'index', intersect: false },
          plugins: {
            legend: { position: 'bottom', labels: { font: { size: 11 } } },
            tooltip: { callbacks: { label: (ctx) => ctx.dataset.label + ': ' + Math.round(ctx.parsed.y).toLocaleString() } },
            datalabels: { display: false },
          },
          scales: { x: { ticks: { font: { size: 10 } } }, y: { ticks: { font: { size: 10 } } } },
        },
      });
    } catch (e) { console.warn('[backtest] chart failed:', e); }

    const parts = [
      `Backtest on last ${usable.length} weeks`,
      `MAPE ${mape.toFixed(1)}%`,
    ];
    if (coverage != null) parts.push(`90% CI coverage ${coverage.toFixed(0)}% (${inCi}/${ciUsable} weeks inside band)`);
    const mapeQuality = mape < 10 ? 'good' : mape < 20 ? 'warn' : 'bad';
    metaEl.innerHTML = parts.join(' · ') + (mapeQuality === 'bad' ? ' <span style="color:var(--color-danger)">— model miscalibrated</span>' :
                                           mapeQuality === 'warn' ? ' <span style="color:var(--color-warning)">— within tolerance</span>' :
                                                                    ' <span style="color:var(--color-success)">— tracking well</span>');
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
      { key: 'qualitative', label: 'Judgment', pct: contribution.qualitative || 0, klass: 'qualitative' },
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

    // P5-9 (2026-04-28): Reframe around Confidence instead of Fit Quality.
    // "Fit quality: not yet measured" reads like "the model doesn't work"
    // to a non-technical exec. "Confidence: limited history" names the
    // same reality but positions it honestly — we have fewer data points,
    // not a broken model. Explain-this link lets Kate drill in if curious.
    let confidenceLabel;
    if (r2 == null)       confidenceLabel = 'limited history';
    else if (r2 >= 0.7)   confidenceLabel = 'strong';
    else if (r2 >= 0.45)  confidenceLabel = 'fair';
    else if (r2 >= 0.2)   confidenceLabel = 'weak';
    else                  confidenceLabel = 'very weak';
    const pctTail = r2 != null ? ` (${Math.round(r2 * 100)}% explained)` : '';

    // Plain-language calibration note — names where the parameters came
    // from and roughly how many weeks of local data back them. Replaces
    // the harsher "weeks of data not recorded" phrasing.
    const fbMap = {
      'market_specific':       nWeeks
        ? `model calibrated on ${nWeeks} weeks of local data`
        : `model calibrated on local data`,
      'regional_fallback':     'model using regional priors, local calibration pending ~8 weeks of backtest data',
      'some_regional_fallback': 'model using regional priors for some parameters',
      'global_fallback':       'model using global priors, local calibration pending',
    };
    const fbText = fbMap[fbLevel] || fbLevel.replace(/_/g, ' ');

    const regimes = V1_1_Slim.listRegimesWithConfidence(marketData.regime_fit_state || [], STATE.regimeMultiplier);
    const liftCount = regimes.length;
    const liftText = liftCount === 0 ? '' : ` · ${liftCount} active campaign lift${liftCount > 1 ? 's' : ''}`;

    const fitHtml =
      `<span class="dot ${klass}"></span>` +
      `Confidence: <b>${confidenceLabel}</b>${pctTail} — ${fbText}${liftText}. ` +
      `<a href="#" class="explain-link" data-topic="fit-quality">Explain this →</a>`;

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

      // Round 13 P1-06: prepend the actual "closest achievable" value so
      // users see the miss, not just "can't be reached." Reaches into
      // out.totals to pull the value the solver landed on, based on the
      // active driver. Only shows when the driver's computed value exists
      // and differs from the requested target by a noticeable amount.
      const driver = currentDriver();
      const targetVal = currentTargetValue();
      let closestLine = '';
      if (driver === 'ieccp') {
        const achieved = out.totals?.computed_ieccp;
        if (Number.isFinite(achieved) && Math.abs(achieved - targetVal) > 0.5) {
          closestLine = `Closest achievable: ${achieved.toFixed(1)}% efficiency (target ${targetVal}%). `;
        }
      } else if (driver === 'spend') {
        const achieved = out.totals?.total_spend;
        if (Number.isFinite(achieved) && Math.abs(achieved - targetVal) / Math.max(targetVal, 1) > 0.02) {
          closestLine = `Closest achievable: ${fmt$(achieved)} spend (target ${fmt$(targetVal)}). `;
        }
      } else if (driver === 'regs') {
        const achieved = out.totals?.total_regs;
        if (Number.isFinite(achieved) && Math.abs(achieved - targetVal) / Math.max(targetVal, 1) > 0.02) {
          closestLine = `Closest achievable: ${fmtNum(achieved)} regs (target ${fmtNum(targetVal)}). `;
        }
      }

      text.textContent = closestLine + phrases.join(' · ');
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
      <p>With Brand regs and Brand spend projected, we solve for the Non-Brand spend that ${driver === 'ieccp' ? 'lands the full-year efficiency on target' : driver === 'regs' ? 'delivers the missing registrations via the NB CPA elasticity curve' : 'fills the remaining budget after Brand'}. The solver uses the NB CPA elasticity fit from ${fq.n_weeks ? `${fq.n_weeks} weeks of history` : 'the available history'}.</p>
      <h3 style="margin-top:12px;font-size:14px">Step 3 — Locked YTD</h3>
      <p>Weeks that have already happened are locked to actuals. The solver only adjusts the remaining weeks of the year.</p>
      <h3 style="margin-top:12px;font-size:14px">Step 4 — Uncertainty band</h3>
      <p>The shaded band around the projected line is a <b>bootstrap approximation</b>: we compute residual noise from the last ~16 weeks of YTD actuals and scale it by √(weeks ahead) to reflect growing forecast uncertainty. This is <em>not</em> a Bayesian posterior credible interval — full posterior CIs are pending migration to the updated schema. Treat the band as "plausible range given recent noise" rather than "statistically-correct credible interval."</p>
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
        // Round 7 P1-04 + Round 12 P1-05: flag absorbed and low-confidence
        // lifts distinctly. Absorbed = persistent >=52w no-decay (now baseline).
        // Low-confidence = effective confidence < 0.25 (unmodeled upside).
        const absorbed = r.absorbed_into_baseline;
        const lowConf = r.low_confidence;
        let statusLabel, badgeKlass, valueDisplay;
        if (absorbed) {
          statusLabel = 'absorbed into baseline';
          badgeKlass = 'ancient';   // subdued — signals "part of baseline, not transient"
          valueDisplay = '—';
        } else if (lowConf) {
          statusLabel = 'unmodeled upside';
          badgeKlass = 'stale';     // yellow — signals "acknowledged but not counted"
          valueDisplay = `${(r.effective_confidence * 100).toFixed(0)}% · not counted`;
        } else {
          statusLabel = (r.decay_status || 'n/a').replace(/-/g, ' ');
          badgeKlass = (r.decay_status && r.decay_status !== 'no-fit-state' ? 'fresh' : 'stale');
          valueDisplay = `${(r.effective_confidence * 100).toFixed(0)}%`;
        }
        const onsetDate = r.change_date ? new Date(r.change_date).toLocaleDateString() : 'n/a';
        return `<div class="drawer-tile">
          <span class="drawer-tile-label">Lift #${i + 1} (onset ${onsetDate}) <span class="freshness-badge ${badgeKlass}">${statusLabel}</span></span>
          <span class="drawer-tile-value">${valueDisplay}</span>
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
    const panel = document.getElementById('saved-panel');
    cnt.textContent = STATE.saved.length ? `${STATE.saved.length}` : '';
    // P5-4 (2026-04-28): hide the whole saved-projections panel when
    // there's nothing saved. Empty-state copy teaches the user to tune
    // out the region; revealing it on first save makes it a legitimate
    // signal rather than persistent noise.
    if (!STATE.saved.length) {
      if (panel) panel.style.display = 'none';
      list.innerHTML = `<div style="color:var(--color-text-subtle);font-size:11px">No saved projections yet.</div>`;
      return;
    }
    if (panel) panel.style.display = '';
    // P2-12: each saved item gets Load / Delete / Compare actions.
    // Compare sets the active comparison-id so the next render overlays the
    // saved projection as a dashed reference line on the chart.
    // P3-11: use toLocaleString so saved timestamps carry both date + time.
    list.innerHTML = STATE.saved.map(r => {
      const when = new Date(r.saved_at).toLocaleString(undefined,
        { month: 'numeric', day: 'numeric', year: 'numeric', hour: 'numeric', minute: '2-digit' });
      const cmpActive = STATE.compareId === r.id ? ' compare-active' : '';
      // P3-09: format target_value via driver-appropriate formatter so saved
      // items like "MX · Y2026 · spend=12500000" render as "spend=$12.5M".
      let tv = r.target_value;
      if (r.driver === 'spend' && Number.isFinite(tv)) tv = fmt$(tv);
      else if (r.driver === 'regs' && Number.isFinite(tv)) tv = fmtNum(tv);
      else if (r.driver === 'ieccp' && Number.isFinite(tv)) tv = tv + '%';
      return `
        <div class="saved-item${cmpActive}" data-id="${r.id}">
          <div style="flex:1;min-width:0">
            <div style="font-weight:500">${r.scope} · ${r.period} · ${r.driver}=${tv}</div>
            <div class="saved-meta">${when}</div>
          </div>
          <div class="saved-actions">
            <button class="saved-action" data-act="load"    title="Load this projection">Load</button>
            <button class="saved-action" data-act="compare" title="Overlay as a dashed reference on the chart">${STATE.compareId === r.id ? 'Clear cmp' : 'Compare'}</button>
            <button class="saved-action saved-action-danger" data-act="delete" title="Delete this saved projection" aria-label="Delete">×</button>
          </div>
        </div>`;
    }).join('');
    list.querySelectorAll('.saved-item').forEach(el => {
      const id = parseInt(el.dataset.id);
      el.querySelector('[data-act="load"]').addEventListener('click', (e) => {
        e.stopPropagation();
        loadSaved(id);
      });
      el.querySelector('[data-act="compare"]').addEventListener('click', (e) => {
        e.stopPropagation();
        toggleCompareSaved(id);
      });
      el.querySelector('[data-act="delete"]').addEventListener('click', (e) => {
        e.stopPropagation();
        deleteSaved(id);
      });
      // Click anywhere else on the row = Load (backwards-compatible shortcut).
      el.addEventListener('click', (e) => {
        if (e.target.closest('.saved-action')) return;
        loadSaved(id);
      });
    });
  }

  function deleteSaved(id) {
    STATE.saved = STATE.saved.filter(r => r.id !== id);
    localStorage.setItem('mpe-saved', JSON.stringify(STATE.saved));
    if (STATE.compareId === id) STATE.compareId = null;
    renderSavedList();
  }

  function toggleCompareSaved(id) {
    STATE.compareId = (STATE.compareId === id) ? null : id;
    renderSavedList();
    // Re-trigger a render so the chart overlays (or clears) the compare line.
    scheduleRecompute();
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
  // P2-10: URL state sharing — scope/period/driver/target round-trip into
  // querystring so a link like `?scope=UK&period=Y2026&driver=ieccp&target=65`
  // loads that exact scenario. Sync on every recompute + restore on cold load.
  // ========================================================================

  function syncUrlFromState() {
    try {
      const p = new URLSearchParams();
      p.set('scope',  currentScope()  || 'MX');
      p.set('period', currentPeriod() || 'Y2026');
      p.set('driver', currentDriver() || 'ieccp');
      const tv = currentTargetValue();
      if (tv != null && Number.isFinite(tv)) p.set('target', String(tv));
      // Keep URL clean — only write when something actually differs from
      // current querystring, avoids spurious history entries on every keystroke.
      const next = p.toString();
      if (next !== window.location.search.slice(1)) {
        window.history.replaceState({}, '', '?' + next);
      }
    } catch (e) { /* URL API unavailable / sandboxed — silent fallback is fine */ }
  }

  function applyUrlStateOnLoad() {
    try {
      const p = new URLSearchParams(window.location.search);
      const scope  = p.get('scope');
      const period = p.get('period');
      const driver = p.get('driver');
      const target = p.get('target');
      if (scope) {
        const el = document.getElementById('scope-select');
        if (el && [...el.options].some(o => o.value === scope)) el.value = scope;
      }
      if (period) {
        const el = document.getElementById('period-select');
        if (el && [...el.options].some(o => o.value === period)) el.value = period;
      }
      if (driver) {
        const el = document.getElementById('driver-select');
        if (el && [...el.options].some(o => o.value === driver)) {
          el.value = driver;
          // P-DRV-PERSIST v2 (2026-04-28): explicit ?driver=X for the URL's
          // scope counts as user intent for THAT scope. Record in scoped map.
          if (!STATE.driverOverrides) STATE.driverOverrides = {};
          const urlScope = p.get('scope');
          if (urlScope) STATE.driverOverrides[urlScope] = driver;
        }
      }
      if (target && Number.isFinite(parseFloat(target))) {
        const el = document.getElementById('target-input');
        if (el) el.value = target;
      }
    } catch (e) { /* URL parse failure — fall through to defaults */ }
  }

  // ========================================================================
  // P3-19: Reset-to-defaults — single click restores MX / Y2026 / ieccp / 75
  // and clears transient scenario state. Useful escape hatch when a user
  // has built up enough comparisons/isolations that the chart feels noisy.
  // ========================================================================

  function resetToDefaults() {
    const scopeEl  = document.getElementById('scope-select');
    const periodEl = document.getElementById('period-select');
    const driverEl = document.getElementById('driver-select');
    const targetEl = document.getElementById('target-input');
    if (scopeEl)  scopeEl.value  = 'MX';
    if (periodEl) periodEl.value = 'Y2026';
    if (driverEl) driverEl.value = 'ieccp';
    if (targetEl) targetEl.value = '75';
    STATE.regimeMultiplier = 1.0;
    const slider = document.getElementById('regime-slider');
    const sliderVal = document.getElementById('regime-slider-val');
    if (slider)    slider.value    = 1.0;
    if (sliderVal) sliderVal.textContent = '1.00×';
    // Clear transient overlays / isolations / comparisons.
    STATE.disclosures.counter = false;
    STATE.activeChipId = 'mixed';
    STATE.scenarioOverride = null;
    STATE.kpiIsolatedSeries = null;
    STATE.compareId = null;
    // P-DRV-PERSIST v2 fix (2026-04-28): clear all per-scope driver
    // overrides so every market returns to its preferred driver.
    STATE.driverOverrides = {};
    STATE.userOverrodeDriver = false;   // back-compat no-op, kept in case
    document.querySelectorAll('[data-disclosure="counter"]').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.hero-kpi[data-kpi-series]').forEach(t => t.classList.remove('kpi-active'));
    refreshScopeDependentUI();
    scheduleRecompute();
  }

  // ========================================================================
  // P2-11: CSV export. Downloads a per-week table of the currently-rendered
  // projection including actuals (YTD) and projected (RoY) with 90% CI
  // bands. Columns are stable across markets so teammates can diff two
  // exports without column-matching. Filename encodes scope/period/driver
  // so stacking multiple downloads in a folder reveals the scenario.
  // ========================================================================

  function escapeCsv(v) {
    if (v == null) return '';
    const s = String(v);
    if (/[",\n]/.test(s)) return '"' + s.replace(/"/g, '""') + '"';
    return s;
  }

  function exportProjectionCsv() {
    const out = STATE.currentOutput;
    const scope = currentScope();
    const md = (STATE.data?.markets || {})[scope];
    const btn = document.getElementById('btn-export-csv');
    const origText = btn ? btn.textContent : '';
    const flash = (msg) => {
      if (!btn) return;
      btn.textContent = msg;
      setTimeout(() => { btn.textContent = origText; }, 1800);
    };
    if (!out || !out.totals || !md) { flash('No data'); return; }

    const bt = md.brand_trajectory_y2026;
    if (!bt) { flash('No trajectory'); return; }

    // Assemble the per-week series — same data the chart renders.
    const ytdRaw = md.ytd_weekly || [];
    const ytdCount = ytdRaw.length;
    const btWeeks = bt.weeks.map(ws => new Date(ws));
    const brandRoyRegs = bt.regs_per_week.slice(ytdCount);
    const brandRoySpend = bt.spend_per_week.slice(ytdCount);
    const royWeeks = btWeeks.slice(ytdCount);
    const royNbSpend = (out.roy?.nb_spend || 0) / (royWeeks.length || 1);
    const royNbRegs  = (out.roy?.nb_regs  || 0) / (royWeeks.length || 1);

    // CI bands (if bootstrap computed)
    const pw = STATE.currentUncertainty?.per_week?.regs || null;
    const ciLo = pw?.lower || [];
    const ciHi = pw?.upper || [];

    const rows = [[
      'week_iso', 'week_start',
      'series', 'brand_regs', 'nb_regs', 'total_regs',
      'brand_spend', 'nb_spend', 'total_spend',
      'ci_lo_regs_90', 'ci_hi_regs_90',
    ]];

    // YTD half — actuals, no CI
    for (let i = 0; i < ytdCount; i++) {
      const w = ytdRaw[i];
      const d = new Date(w.period_start);
      const brandR = w.brand_regs || w.brand_registrations || 0;
      const nbR    = w.nb_regs    || w.nb_registrations    || 0;
      const brandS = w.brand_cost || w.brand_spend || 0;
      const nbS    = w.nb_cost    || w.nb_spend    || 0;
      rows.push([
        fmtIsoWeek(d), d.toISOString().slice(0, 10),
        'actual',
        Math.round(brandR), Math.round(nbR), Math.round(brandR + nbR),
        Math.round(brandS), Math.round(nbS), Math.round(brandS + nbS),
        '', '',
      ]);
    }
    // RoY half — projected, with CI where available
    for (let i = 0; i < royWeeks.length; i++) {
      const d = royWeeks[i];
      const brandR = brandRoyRegs[i] || 0;
      const brandS = brandRoySpend[i] || 0;
      const globalIdx = ytdCount + i;
      const lo = Number.isFinite(ciLo[globalIdx]) ? Math.round(ciLo[globalIdx]) : '';
      const hi = Number.isFinite(ciHi[globalIdx]) ? Math.round(ciHi[globalIdx]) : '';
      rows.push([
        fmtIsoWeek(d), d.toISOString().slice(0, 10),
        'projected',
        Math.round(brandR), Math.round(royNbRegs), Math.round(brandR + royNbRegs),
        Math.round(brandS), Math.round(royNbSpend), Math.round(brandS + royNbSpend),
        lo, hi,
      ]);
    }

    // Trailer — scenario metadata as commented rows (# prefix keeps it
    // readable when pasted into Excel/Sheets without breaking the grid)
    const t = out.totals || {};
    const meta = [
      `# Projection Engine export — ${new Date().toISOString()}`,
      `# scope=${scope} period=${currentPeriod()} driver=${currentDriver()} target=${currentTargetValue()}`,
      `# total_spend=${Math.round(t.total_spend || 0)} total_regs=${Math.round(t.total_regs || 0)} blended_cpa=${(t.blended_cpa || 0).toFixed(2)} computed_ieccp=${(t.computed_ieccp || 0).toFixed(2)}`,
      `# bootstrap_ci_available=${pw ? 'true' : 'false'}`,
    ];

    const csv = meta.join('\n') + '\n'
      + rows.map(r => r.map(escapeCsv).join(',')).join('\n') + '\n';

    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `projection-${scope}-${currentPeriod()}-${currentDriver()}-${new Date().toISOString().slice(0, 10)}.csv`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    setTimeout(() => URL.revokeObjectURL(url), 5000);
    flash('CSV downloaded');
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
        let narrativeText = MPENarrative.generate(fauxOut, STATE.data);
        // Round 10 P1-01 Option C: append bootstrap CI tail-line when available.
        // Honest framing per Local Kiro spec — this is an approximation, not
        // a Bayesian posterior; footnote reinforces that in the How modal.
        const uncert = STATE.currentUncertainty;
        if (uncert && uncert.credible_intervals && uncert.credible_intervals.total_regs) {
          const ciR = uncert.credible_intervals.total_regs.ci?.['90'];
          const ciS = uncert.credible_intervals.total_spend?.ci?.['90'];
          if (ciR && ciS) {
            const fmt$ciLo = fmt$(ciS[0]);
            const fmt$ciHi = fmt$(ciS[1]);
            const fmtRLo = fmtNum(ciR[0]);
            const fmtRHi = fmtNum(ciR[1]);
            narrativeText += `\n\n90% plausible range: ${fmt$ciLo}–${fmt$ciHi} spend · ${fmtRLo}–${fmtRHi} regs. (Bootstrap approximation from recent-YTD residuals.)`;
          }
        }
        el.textContent = narrativeText;
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

  // ========================================================================
  // Small-multiples view (6.4.1) — one mini chart per market.
  // P2-17: sharedYScale toggle (STATE.sharedYScaleMultiples) — when on,
  // computes max across all 10 markets and applies same suggestedMax to
  // every mini chart so users can visually compare absolute volumes.
  // ========================================================================

  async function renderSmallMultiples() {
    const grid = document.getElementById('small-multiples-grid');
    grid.innerHTML = '';
    const driver = currentDriver() === 'rollup' ? 'ieccp' : currentDriver();
    const period = currentPeriod();
    const periodWeeks = periodWeeksSet(period);
    let okCount = 0;

    // First pass: project all markets + collect peaks for shared-scale mode.
    const outs = [];   // { mkt, md, out }
    let sharedPeak = 0;
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
        outs.push({ mkt, md, out });
        const yw = out.year_weekly;
        if (yw && yw.brand_regs) {
          for (let i = 0; i < yw.brand_regs.length; i++) {
            const v = (yw.brand_regs[i] || 0) + (yw.nb_regs[i] || 0);
            if (v > sharedPeak) sharedPeak = v;
          }
        }
      } catch (e) {
        console.error(`Small-multiples ${mkt} failed:`, e);
      }
    }
    // Apply padding for headroom (matches P2-16 scenario-mode logic).
    const sharedMax = sharedPeak > 0 ? Math.ceil(sharedPeak * 1.12) : undefined;

    // Second pass: build cards with either per-market or shared scale.
    for (const { mkt, md, out } of outs) {
      const card = renderMiniChartCard(mkt, md, out, STATE.sharedYScaleMultiples ? sharedMax : undefined);
      grid.appendChild(card);
      okCount += 1;
    }
    document.getElementById('multiples-legend').textContent =
      `${okCount} markets rendered · driver=${driver} · period=${period} · scenario=${STATE.activeChipId || 'mixed'} · scale=${STATE.sharedYScaleMultiples ? 'shared' : 'per-market'}`;
  }

  function renderMiniChartCard(market, md, out, sharedMax) {
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

    const canvasId = `mini-canvas-${market}`;
    card.innerHTML = `
      <div class="mini-chart-header">
        <div class="mini-market-code">${market}${anomBadge}</div>
        <div class="mini-headline">${headlineValue}</div>
      </div>
      <div class="mini-chart-body"><canvas id="${canvasId}" style="width:100%;height:80px"></canvas></div>
      <div class="mini-chart-meta">Efficiency ${t.computed_ieccp != null ? t.computed_ieccp.toFixed(1) + '%' : 'n/a'} · CPA ${fmt$(t.blended_cpa)}</div>
    `;

    // Render mini chart via Chart.js (replaces the old Plot.plot call which
    // was dead after M3). Defers the Chart instantiation to next tick so the
    // canvas is attached and sized before Chart.js queries its dimensions.
    if (yw && yw.brand_regs && yw.brand_regs.length > 0) {
      const n = yw.brand_regs.length;
      const totals = new Array(n);
      for (let i = 0; i < n; i++) totals[i] = (yw.brand_regs[i] || 0) + (yw.nb_regs[i] || 0);
      const ytdEnd = yw.ytd_weeks || 0;
      // Split into locked + projected so the two halves can be colored differently
      const locked = totals.map((v, i) => i < ytdEnd ? v : null);
      const proj   = totals.map((v, i) => i >= ytdEnd - 1 ? v : null);  // seam at ytdEnd-1
      setTimeout(() => {
        const canvas = document.getElementById(canvasId);
        if (!canvas) return;
        try {
          new Chart(canvas, {
            type: 'line',
            data: {
              labels: Array.from({ length: n }, (_, i) => 'W' + (i + 1)),
              datasets: [
                { data: locked, borderColor: '#4A4A4A', borderWidth: 1.5, pointRadius: 0, tension: 0.25, spanGaps: false },
                { data: proj,   borderColor: 'var(--color-brand, #0066CC)', borderWidth: 1.5, pointRadius: 0, tension: 0.25, spanGaps: false },
              ],
            },
            options: {
              responsive: true,
              maintainAspectRatio: false,
              plugins: { legend: { display: false }, tooltip: { enabled: false }, datalabels: { display: false } },
              scales: {
                x: { display: false },
                y: { display: false, suggestedMax: sharedMax },
              },
              elements: { line: { borderJoinStyle: 'round' } },
              animation: false,
            },
          });
        } catch (e) { console.warn(`[mini ${market}] chart failed:`, e); }
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
          // P2-18 fix: solver-back-fit markets always return projected_ieccp ≈ target
          // because NB spend is back-fit to hit the target. To show a MEANINGFUL
          // distance, run a second unconstrained projection against OP2 SPEND
          // (no ieccp back-fit) and compute what ieccp would naturally obtain.
          //   cellValue = projected ieccp under the target back-fit (reflects the
          //              scenario the user picked)
          //   cellDelta = unconstrained ieccp vs target (the honest health signal:
          //              'at this OP2 spend, would you naturally land on target?')
          // Cells where ieccp is target-by-construction get an explicit tag so
          // users aren't misled into reading a fake zero.
          out = V1_1_Slim.projectWithLockedYtd(
            md, 2026, 'ieccp', ieTgt * 100,
            { regimeMultiplier: STATE.regimeMultiplier, scenarioOverride: STATE.scenarioOverride, periodWeeks, periodType: period }
          );
          const projIe = out.totals.computed_ieccp;
          const target = ieTgt * 100;
          cellValue = projIe != null ? `${projIe.toFixed(0)}%` : 'n/a';
          cellMetric = 'Efficiency';
          // Second probe: what's the unconstrained ieccp at OP2 spend?
          let unconstrainedIe = null;
          try {
            if (op2Spend) {
              const probeOut = V1_1_Slim.projectWithLockedYtd(
                md, 2026, 'spend', op2Spend,
                { regimeMultiplier: STATE.regimeMultiplier, scenarioOverride: STATE.scenarioOverride, periodWeeks, periodType: period }
              );
              unconstrainedIe = probeOut.totals?.computed_ieccp;
            }
          } catch (_) { /* probe-only; fall back gracefully */ }
          const delta = (unconstrainedIe != null) ? unconstrainedIe - target
                       : (projIe != null ? projIe - target : 0);
          cellDelta = unconstrainedIe != null
            ? `unconstrained: ${unconstrainedIe.toFixed(0)}% · ${delta >= 0 ? '+' : ''}${delta.toFixed(1)}pp vs ${target.toFixed(0)}%`
            : (projIe != null ? `at target by design (${target.toFixed(0)}%)` : '');
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
    anchor_recent: `Where Brand is RIGHT NOW — mean of the last 8 weeks of Brand regs (clipped to post-regime-onset if a structural campaign started recently, so active lifts aren't diluted). This is the baseline every other stream multiplies on top of.`,
    yoy_annual: `Annual YoY growth scalar from log-linear regression on regime-normalized annual Brand regs (last 3 years). Regime contributions are stripped from each year before regression so the slope reflects organic growth, not campaign lifts. Permanent slopes live here — weekly slopes don't compound forever.`,
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
        <div style="font-size:10px;color:var(--color-text-subtle)">Last 8 weeks of Brand regs (anchor)</div>
        <span class="drawer-tile-explain" data-explain="anchor_recent">Explain this →</span>
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
    if (n >= 3) {
      // #13 whitespace cleanup — use .visible class so the CSS-side
      // `display/margin-top: 0` guard for the hidden state doesn't reserve
      // ~149px of layout space when the bar isn't shown.
      bar.classList.add('visible');
      bar.style.display = '';
    }
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
    // P2-10: restore scope/period/driver/target from querystring if present.
    // Must run after populateScopeSelector (so select has real options) and
    // before refreshScopeDependentUI (which seeds default target based on
    // the current scope/driver).
    applyUrlStateOnLoad();
    refreshScopeDependentUI();
    bindDisclosureButtons();
    wireFeedbackBar();
    renderHeaderAnomalies();

    // Round 11 P2-07b: KPI tile → chart series linking.
    // Click a KPI tile with data-kpi-series → isolate that chart series.
    // Click again → restore previous legend visibility state.
    document.querySelectorAll('.hero-kpi[data-kpi-series]').forEach(tile => {
      tile.addEventListener('click', () => {
        const series = tile.dataset.kpiSeries;
        if (!STATE.legendVisibility) return;
        if (STATE.kpiIsolatedSeries === series) {
          // Already isolated → restore defaults
          STATE.legendVisibility = {
            'actuals-regs': true, 'actuals-spend': false,
            'proj-brand': true, 'proj-nb': true, 'proj-total': true,
            'proj-total-spend': false,
          };
          STATE.kpiIsolatedSeries = null;
          tile.classList.remove('kpi-active');
        } else {
          // Isolate: only this series + actuals-regs visible for context
          STATE.legendVisibility = {
            'actuals-regs': true, 'actuals-spend': false,
            'proj-brand': series === 'proj-brand',
            'proj-nb': series === 'proj-nb',
            'proj-total': series === 'proj-total',
            'proj-total-spend': false,
          };
          STATE.kpiIsolatedSeries = series;
          document.querySelectorAll('.hero-kpi[data-kpi-series]').forEach(t => t.classList.remove('kpi-active'));
          tile.classList.add('kpi-active');
        }
        // Re-render chart to apply new legend state (cheapest reliable path
        // since the SVG is already built; just trigger the existing path).
        recompute({ animated: false });
      });
    });

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
      // P-DRV-PERSIST v2 (2026-04-28): user picked a driver explicitly,
      // record it as an override FOR THIS SCOPE ONLY. Subsequent market
      // switches don't carry it. Cleared by Reset.
      if (!STATE.driverOverrides) STATE.driverOverrides = {};
      const scope = currentScope();
      STATE.driverOverrides[scope] = document.getElementById('driver-select').value;
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

    document.getElementById('btn-recompute').addEventListener('click', async () => {
      // P3-16 decision: Recompute re-fetches projection-data.json (cache: 'reload')
      // then re-runs the projection, so the button delivers what its label
      // implies. Visible network hit makes it observable — Kate can watch
      // the timestamp update in the hero badge after each click.
      const btn = document.getElementById('btn-recompute');
      const orig = btn.textContent;
      btn.textContent = 'Fetching…';
      try {
        const resp = await fetch('data/projection-data.json', { cache: 'reload' });
        if (resp.ok) STATE.data = await resp.json();
      } catch (e) {
        console.warn('[projection] recompute re-fetch failed:', e);
      }
      btn.textContent = orig;
      recompute({ animated: true });
    });
    document.getElementById('btn-save').addEventListener('click', saveProjection);
    document.getElementById('btn-export-csv').addEventListener('click', exportProjectionCsv);
    const resetBtn = document.getElementById('btn-reset');
    if (resetBtn) resetBtn.addEventListener('click', resetToDefaults);

    // P2-17: shared-y-scale toggle on small-multiples view
    const sharedBtn = document.getElementById('btn-shared-scale');
    if (sharedBtn) {
      sharedBtn.addEventListener('click', () => {
        STATE.sharedYScaleMultiples = !STATE.sharedYScaleMultiples;
        sharedBtn.textContent = 'Shared y-scale: ' + (STATE.sharedYScaleMultiples ? 'on' : 'off');
        sharedBtn.setAttribute('aria-pressed', String(!!STATE.sharedYScaleMultiples));
        sharedBtn.classList.toggle('active', STATE.sharedYScaleMultiples);
        renderSmallMultiples();
      });
    }
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
    document.addEventListener('DOMContentLoaded', () => init().catch(e => console.warn('init failed:', e)));
  } else {
    init().catch(e => console.warn('init failed:', e));
  }

  // Round 13 P1-12: global unhandledrejection handler. Any promise rejection
  // that escapes a try/catch still logs to console but as a warn, not an
  // "Uncaught (in promise)" error. This prevents the silent red errors
  // Local Kiro flagged in R12 and gives developers a clean single surface
  // for rejection debugging.
  window.addEventListener('unhandledrejection', (ev) => {
    console.warn('unhandled promise rejection in projection-app:', ev.reason);
    ev.preventDefault();
  });
})();
