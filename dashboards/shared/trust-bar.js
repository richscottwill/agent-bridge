/**
 * Shared cross-page trust bar (per M1 + report #075).
 *
 * Renders a horizontal strip of market pills carrying each market's
 * recent-weeks forecast-trust state. Same pill shape, same color stops,
 * same click-to-select behavior on both weekly-review.html and
 * projection.html. Consumed by WR at the sticky header; MPE consumption
 * is the follow-up commit after this lands (see bus thread
 * 2026-04-30_dashboard-mockups-handoff).
 *
 * Color stops (agreed on bus 002):
 *   on  ≥ 5/6 inside CI        — green
 *   mid   3–4/6                — amber
 *   off ≤ 2/6                  — red
 *   na  insufficient data      — grey
 *
 * Data shape (WR):  FORECAST.predictions_history[market][week].regs
 *                   with fields {actual, latest_ci_lo, latest_ci_hi}.
 *                   6-week window anchored at FORECAST.max_week.
 *
 * Data shape (MPE): to be wired in the follow-up. MPE's pulse strip
 *                   uses distance-to-target, which encodes different
 *                   information than forecast trust. When both pages
 *                   consume this helper, each page supplies its own
 *                   `computeState(market) → {rateText, rateCls}` fn so
 *                   the renderer is semantic-agnostic. For now WR
 *                   supplies `computeForecastTrust`.
 */

(function (global) {
  'use strict';

  const DEFAULT_ORDER = ['WW','US','EU5','CA','UK','DE','FR','IT','ES','JP','MX','AU'];

  /**
   * Compute in-CI rate state over the last `window` graded weeks.
   * @param {Object} forecast - forecast-data.json loaded object
   * @param {string} market
   * @param {number} window - default 6
   * @returns {{rateText: string, rateCls: 'on'|'mid'|'off'|'na', hits: number, total: number}}
   */
  function computeForecastTrust(forecast, market, window) {
    window = window || 6;
    const hist = (forecast && forecast.predictions_history) || {};
    const maxWk = (forecast && forecast.max_week) || 15;
    const h = hist[market] || {};
    let hits = 0, total = 0;
    for (let w = Math.max(1, maxWk - (window - 1)); w <= maxWk; w++) {
      const r = (h[String(w)] || h[w] || {}).regs;
      if (!r || r.actual == null || r.latest_ci_lo == null || r.latest_ci_hi == null) continue;
      total++;
      if (r.actual >= r.latest_ci_lo && r.actual <= r.latest_ci_hi) hits++;
    }
    let rateCls = 'na';
    let rateText = '\u2014';
    if (total >= 3) {
      const hitRate = hits / total;
      // Thresholds — matches the 4-stop scale from the mockup + report #004.
      rateCls = hitRate >= 5/6 ? 'on' : hitRate >= 3/6 ? 'mid' : 'off';
      rateText = `${hits}/${total}`;
    } else if (total > 0) {
      rateText = `${hits}/${total}`;
      rateCls = 'na';
    }
    return { rateText, rateCls, hits, total };
  }

  /**
   * Render the trust bar into a host element.
   *
   * @param {HTMLElement} host - container for the pill row
   * @param {Object} opts
   *   - markets: string[]   — optional market order override
   *   - selected: string     — currently selected market
   *   - computeState: (mk) → {rateText, rateCls}
   *   - onSelect: (mk) => void — click handler; only fires when mk !== selected
   *   - markClass: (mk) => string — optional extra class per pill (e.g., forecast-only †)
   */
  function renderTrustBar(host, opts) {
    if (!host) return;
    const markets = (opts && opts.markets) || DEFAULT_ORDER;
    const selected = opts && opts.selected;
    const computeState = (opts && opts.computeState) || (() => ({ rateText: '\u2014', rateCls: 'na' }));
    const markClass = (opts && opts.markClass) || (() => '');
    const onSelect = (opts && opts.onSelect) || (() => {});

    const pills = markets.map(mk => {
      const state = computeState(mk) || { rateText: '\u2014', rateCls: 'na' };
      const extra = markClass(mk);
      const activeCls = mk === selected ? ' active' : '';
      const title = `${mk}: ${state.hits != null ? state.hits : '?'} of ${state.total != null ? state.total : '?'} weeks inside CI (last 6)`;
      return (
        `<button class="trust-pill trust-pill-${state.rateCls}${activeCls}${extra ? ' ' + extra : ''}" ` +
        `data-market="${mk}" title="${title}" aria-label="${title}" aria-pressed="${mk === selected}">` +
        `<span class="trust-pill-mk">${mk}</span>` +
        `<span class="trust-pill-rate">${state.rateText}</span>` +
        `</button>`
      );
    });
    host.innerHTML = pills.join('');
    host.querySelectorAll('.trust-pill').forEach(btn => {
      btn.onclick = () => {
        const mk = btn.dataset.market;
        if (!mk || mk === selected) return;
        onSelect(mk);
      };
    });
  }

  // Expose both under a namespaced object and on `window.TrustBar` for
  // non-module consumption. No build step; keep it plain.
  global.TrustBar = {
    renderTrustBar,
    computeForecastTrust,
    DEFAULT_ORDER
  };
})(typeof window !== 'undefined' ? window : this);
