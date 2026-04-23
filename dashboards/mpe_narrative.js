/**
 * mpe_narrative.js — Narrative generation for projection outputs.
 *
 * WHY THIS EXISTS
 *   Every projection deserves a 2-4 paragraph plain-English readout that
 *   non-technical stakeholders can read in 30 seconds and know (a) what
 *   the numbers say, (b) why, (c) the confidence level, (d) what to do
 *   about it. Templates are per-market where strategy matters (MX
 *   ieccp_bound vs US balanced) and per-region where mix effects matter.
 *
 * RICHARD-WRITING-STYLE GUARDRAILS
 *   - No em-dashes (use " — " sparingly or parenthesis instead)
 *   - Data-forward, explicit "so what"
 *   - Brief; max ~300 words expanded
 *   - No filler ("great to see that")
 *   - Explicit uncertainty language on Fallback_Markets
 *   - Regional narratives call out mix effects
 *
 * HOW THE TEMPLATES WORK
 *   Each market has a template keyed by strategy type. The template
 *   pulls from the projection output plus the per-market params record.
 *   Regional narratives are assembled from constituent_markets data.
 *
 * MAINTENANCE
 *   Owner updates templates by editing the strings here or in the
 *   narrative_template field of ps.market_projection_params. UI reads
 *   templates from the latter when present, else falls back to these.
 */
(function (global) {
  'use strict';

  // Strategy-specific framing
  const STRATEGY_FRAMING = {
    'ieccp_bound': 'ie%CCP-bound market where the target ie%CCP is fixed and spend is solved backwards',
    'efficiency': 'efficiency-first market where the priority is controlling CPA growth',
    'brand_dominant': 'Brand-dominant market where Brand carries most of the reg volume',
    'balanced': 'balanced market with both Brand and NB contributing meaningfully',
    'nb_dominant': 'NB-dominant market where NB carries most of the reg volume',
  };

  function fmt$(v) {
    if (v === null || v === undefined || !Number.isFinite(v)) return 'n/a';
    if (Math.abs(v) >= 1_000_000) return `$${(v / 1_000_000).toFixed(2)}M`;
    if (Math.abs(v) >= 1000) return `$${(v / 1000).toFixed(0)}K`;
    return `$${v.toFixed(0)}`;
  }

  function fmtPct(v, digits) {
    if (v === null || v === undefined || !Number.isFinite(v)) return 'n/a';
    return `${v.toFixed(digits || 1)}%`;
  }

  function fmtNum(v, digits) {
    if (v === null || v === undefined || !Number.isFinite(v)) return 'n/a';
    return v.toLocaleString(undefined, { maximumFractionDigits: digits || 0 });
  }

  function ci90Text(ciObj) {
    if (!ciObj || !ciObj.ci || !ciObj.ci['90']) return '';
    const [lo, hi] = ciObj.ci['90'];
    return `${fmtNum(lo)} to ${fmtNum(hi)}`;
  }

  /**
   * Generate a narrative block from a projection output.
   *
   * @param {object} out - ProjectionOutputs dict from MPE.project()
   * @param {object} data - full projection-data.json bundle
   * @returns {string} multi-paragraph narrative
   */
  function generate(out, data) {
    if (!out || out.outcome === 'INVALID_INPUT') {
      return `Projection could not run. ${out.warnings.join('; ')}`;
    }
    if (out.outcome === 'SETUP_REQUIRED') {
      return `${out.scope} has no fitted parameters yet. See the owner runbook for setup steps before running projections.`;
    }
    if (out.outcome === 'INFEASIBLE') {
      const reason = out.infeasibility_reason || {};
      return `Target ${out.target_mode}=${out.target_value} is not feasible for ${out.scope}. Binding constraint: ${reason.binding_constraint || 'unknown'}. Closest feasible: ${JSON.stringify(reason.closest_feasible || {})}.`;
    }

    // Region path
    if (out.constituent_markets && out.constituent_markets.length > 0) {
      return generateRegional(out, data);
    }
    return generateMarket(out, data);
  }

  function generateMarket(out, data) {
    const t = out.totals;
    const ci = out.credible_intervals || {};
    const marketData = (data && data.markets) ? data.markets[out.scope] : null;
    const strategyType = marketData && marketData.parameters && marketData.parameters.market_strategy_type
      ? marketData.parameters.market_strategy_type.value_json : 'balanced';
    const framing = STRATEGY_FRAMING[strategyType] || STRATEGY_FRAMING.balanced;
    const fallbackSummary = out.fallback_level_summary || 'all_market_specific';

    const paras = [];

    // Paragraph 1 — what the numbers say
    const regsCi = ci.total_regs;
    const spendCi = ci.total_spend;
    paras.push(
      `${out.scope} ${out.time_period} projection: ${fmtNum(t.total_regs)} registrations on ${fmt$(t.total_spend)} spend, blended CPA ${fmt$(t.blended_cpa)}, ie%CCP ${fmtPct(t.ieccp)}. ` +
      `90% credible interval on total regs: ${regsCi ? ci90Text(regsCi) : 'n/a'}. ` +
      `Brand contributes ${fmtNum(t.brand_regs)} regs on ${fmt$(t.brand_spend)} (${fmtPct(t.brand_spend / Math.max(t.total_spend, 1) * 100)} of spend), NB contributes ${fmtNum(t.nb_regs)} regs on ${fmt$(t.nb_spend)}.`
    );

    // Paragraph 2 — what's driving it
    const regimeEvents = (marketData && marketData.regime_events) || [];
    const structuralRegimes = regimeEvents.filter(r => r.is_structural_baseline);
    const transientRegimes = regimeEvents.filter(r => !r.is_structural_baseline);
    let drivers = `This is a ${framing}.`;
    if (structuralRegimes.length > 0) {
      const latestStructural = structuralRegimes[structuralRegimes.length - 1];
      drivers += ` The current baseline reflects ${latestStructural.description.split('.')[0]}.`;
    }
    if (transientRegimes.length > 0) {
      drivers += ` ${transientRegimes.length} transient regime event(s) are being accounted for with decay.`;
    }
    paras.push(drivers);

    // Paragraph 3 — confidence + what to tell stakeholder
    let confidence = '';
    if (fallbackSummary === 'all_market_specific') {
      confidence = `Fit quality is strong across all parameters (market-specific fits). Treat this as a calibrated projection.`;
    } else if (fallbackSummary === 'some_regional_fallback') {
      const fbParams = Object.entries(out.parameters_used || {})
        .filter(([, v]) => v && (v.fallback_level === 'regional_fallback' || v.fallback_level === 'southern_hemisphere_hybrid'))
        .map(([k]) => k);
      confidence = `Some parameters use regional fallback (${fbParams.join(', ')}) — credible intervals are wider for those segments. The projection is directionally trustworthy but treat specific numbers with appropriate caution.`;
    } else {
      confidence = `Most or all parameters use regional fallback — this projection is directional only, not calibrated.`;
    }
    paras.push(confidence);

    // Paragraph 4 — warnings, if notable
    const notableWarnings = (out.warnings || []).filter(w =>
      w.startsWith('VERY_WIDE_CI') || w.startsWith('HIGH_EXTRAPOLATION') || w.startsWith('LOW_CONFIDENCE_MULTI_YEAR') || w.startsWith('STALE_PARAMETERS')
    );
    if (notableWarnings.length > 0) {
      paras.push(`Notable caveats: ${notableWarnings.join('; ')}`);
    }

    return paras.join('\n\n');
  }

  function generateRegional(out, data) {
    const t = out.totals;
    const paras = [];
    const constituents = out.constituent_markets || [];

    // Mix effects
    const topContributors = constituents
      .slice()
      .sort((a, b) => (b.brand_regs + b.nb_regs) - (a.brand_regs + a.nb_regs))
      .slice(0, 3);
    const topContribText = topContributors
      .map(m => `${m.market} (${fmtNum(m.brand_regs + m.nb_regs)} regs, ie%CCP ${fmtPct(m.ieccp)})`)
      .join(', ');

    paras.push(
      `${out.scope} ${out.time_period} regional rollup: ${fmtNum(t.total_regs)} regs on ${fmt$(t.total_spend)}, blended CPA ${fmt$(t.blended_cpa)}, regional ie%CCP ${fmtPct(t.ieccp)}. ` +
      `Top contributors: ${topContribText}.`
    );

    // Any constituent in fallback?
    const fbMarkets = constituents.filter(m => m.fallback_level_summary !== 'all_market_specific').map(m => m.market);
    if (fbMarkets.length > 0) {
      paras.push(
        `${fbMarkets.join(', ')} use some or all regional fallback for elasticity. Regional credible intervals are wider than they would be with full market-specific fits for every constituent. This is expected per the MPE v1 design (fallback is a safety net, not the plan).`
      );
    } else {
      paras.push(
        `All constituents have market-specific fits. This is a calibrated regional projection.`
      );
    }

    // Regional ie%CCP math note
    paras.push(
      `Regional ie%CCP is computed via sum-then-divide (total spend divided by the weighted sum of regs-by-CCP across markets). Never averaged — that would be wrong because CCPs vary 4x+ across markets.`
    );

    return paras.join('\n\n');
  }

  // ---------- Public API ----------

  const MPENarrative = {
    generate,
    _internals: { generateMarket, generateRegional, STRATEGY_FRAMING },
  };

  if (typeof module !== 'undefined' && module.exports) {
    module.exports = MPENarrative;
  } else {
    global.MPENarrative = MPENarrative;
  }
})(typeof window !== 'undefined' ? window : globalThis);
