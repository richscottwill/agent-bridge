/**
 * mpe_narrative.js — plain-language narrative for a projection.
 *
 * Design goals after Round 3 feedback:
 *   - No statistical jargon in output ("r²", "credible interval", "Monte
 *     Carlo", "elasticity", "ie%CCP" → "efficiency").
 *   - Guarded against null/NaN — never emit "n/a" into prose.
 *   - Plural-aware ("1 campaign lift" vs "2 campaign lifts").
 *   - Uses the actual V1_1_Slim output shape (period, computed_ieccp,
 *     annual_*, year_weekly), not the old MPE.project shape.
 *   - Answers "what should I do this week?" at the top.
 */
(function (global) {
  'use strict';

  function fmt$(v) {
    if (v === null || v === undefined || !Number.isFinite(v)) return null;
    if (Math.abs(v) >= 1_000_000) return `$${(v / 1_000_000).toFixed(2)}M`;
    if (Math.abs(v) >= 1000) return `$${Math.round(v / 1000)}K`;
    return `$${Math.round(v)}`;
  }
  function fmtNum(v) {
    if (v === null || v === undefined || !Number.isFinite(v)) return null;
    return Math.round(v).toLocaleString();
  }
  function fmtPct(v, digits) {
    if (v === null || v === undefined || !Number.isFinite(v)) return null;
    return `${v.toFixed(digits == null ? 0 : digits)}%`;
  }

  function pluralize(n, singular, plural) {
    return `${fmtNum(n) || n} ${n === 1 ? singular : (plural || singular + 's')}`;
  }

  function humanPeriod(p) {
    // Examples: W15 → "week 15"; M04 → "month 04"; Q2 → "Q2"; Y2026 → "full year 2026";
    // MY1 → "next 1 year"; MY2 → "next 2 years". IMPORTANT: check MY before M
    // because "MY2".startsWith("M") matches both — MY1/MY2 were being read as "month Y2".
    if (!p) return 'this year';
    const up = p.toUpperCase();
    if (up.startsWith('MY')) {
      const n = parseInt(up.slice(2), 10);
      if (Number.isFinite(n) && n > 0) return `next ${n} year${n === 1 ? '' : 's'}`;
      return 'a multi-year window';
    }
    if (up.startsWith('W')) return `week ${up.slice(1)}`;
    if (up.startsWith('M')) return `month ${up.slice(1)}`;
    if (up.startsWith('Q')) return `Q${up.slice(1)}`;
    if (up.startsWith('Y')) return `full year ${up.slice(1)}`;
    if (up.startsWith('MY')) return `next ${up.slice(2)}-year horizon`;
    return p;
  }

  function generate(out, data) {
    if (!out || out.error) {
      return `Projection could not run${out?.error ? ': ' + out.error : '.'}`;
    }
    const t = out.totals || {};
    const scope = out.scope || 'this scope';
    const period = humanPeriod(out.period || out.time_period);

    const spendStr = fmt$(t.total_spend);
    const regsStr = fmtNum(t.total_regs);
    const brandStr = fmtNum(t.brand_regs);
    const nbStr = fmtNum(t.nb_regs);
    const cpaStr = fmt$(t.blended_cpa);
    const efficiency = t.computed_ieccp;
    const effStr = fmtPct(efficiency, 1);

    // Line 1 — headline
    const line1Parts = [`For ${scope} across ${period}:`];
    if (spendStr && regsStr) {
      line1Parts.push(` spending ${spendStr} produces about ${regsStr} registrations.`);
    } else if (regsStr) {
      line1Parts.push(` about ${regsStr} registrations expected.`);
    }
    let headline = line1Parts.join('');
    if (cpaStr) headline += ` That's roughly ${cpaStr} per registration on average.`;
    if (effStr) headline += ` Efficiency (how much spend each registration brings in) lands at ${effStr}.`;

    // Line 2 — Brand vs NB split
    let split = null;
    const brandR = t.brand_regs || 0;
    const nbR = t.nb_regs || 0;
    const totalR = brandR + nbR;
    if (totalR > 0 && brandStr && nbStr) {
      const brandPct = Math.round(brandR / totalR * 100);
      const nbPct = 100 - brandPct;
      if (brandPct >= 85) {
        split = `Almost all of that volume (${brandPct}%) comes from Brand — NB only adds ${nbStr} registrations.`;
      } else if (brandPct <= 15) {
        split = `NB carries the volume (${nbPct}%) — Brand only adds ${brandStr} registrations.`;
      } else if (brandPct >= 45 && brandPct <= 55) {
        split = `Brand and NB split the volume roughly evenly (${brandStr} Brand · ${nbStr} NB).`;
      } else if (brandPct > 55) {
        split = `Brand carries more of the volume (${brandStr}) than NB (${nbStr}), about ${brandPct}/${nbPct}.`;
      } else {
        split = `NB carries more of the volume (${nbStr}) than Brand (${brandStr}), about ${brandPct}/${nbPct}.`;
      }
    }

    // Line 3 — OP2 comparison
    let op2Line = null;
    const marketData = data?.markets?.[scope];
    const op2Spend = marketData?.op2_targets?.annual_spend_target;
    const op2Regs = marketData?.op2_targets?.annual_regs_target;
    const annualTotalSpend = t.annual_total_spend || t.total_spend;
    const annualTotalRegs = t.annual_total_regs || t.total_regs;
    if (op2Spend && annualTotalSpend && op2Regs && annualTotalRegs) {
      const spendPct = Math.round(annualTotalSpend / op2Spend * 100);
      const regsPct = Math.round(annualTotalRegs / op2Regs * 100);
      if (Math.abs(spendPct - 100) <= 5 && Math.abs(regsPct - 100) <= 5) {
        op2Line = `At full-year pace, that's within 5% of OP2 on both spend and registrations — tracking the plan.`;
      } else if (spendPct > 110 && regsPct < 95) {
        op2Line = `At full-year pace that's ${spendPct}% of OP2 spend but only ${regsPct}% of OP2 registrations — overspending without reg delivery.`;
      } else if (spendPct < 95 && regsPct > 110) {
        op2Line = `At full-year pace that's ${spendPct}% of OP2 spend but ${regsPct}% of OP2 registrations — delivering more with less.`;
      } else {
        op2Line = `At full-year pace that's ${spendPct}% of OP2 spend and ${regsPct}% of OP2 registrations.`;
      }
    }

    // Line 4 — what's driving it (campaign lifts)
    let drivers = null;
    const lifts = (marketData?.regime_fit_state) || [];
    const activeLifts = lifts.filter(l => l.confidence && l.confidence > 0.15);
    if (activeLifts.length === 0) {
      drivers = `No active campaign lifts detected — projection is baseline trend plus seasonality.`;
    } else if (activeLifts.length === 1) {
      const l = activeLifts[0];
      const pct = Math.round((l.peak_multiplier - 1) * 100);
      drivers = `One campaign lift is active, about +${pct}% on Brand at peak.`;
      if (l.decay_status === 'still-peaking') drivers += ` Still building — lift may grow.`;
      else if (l.decay_status === 'decaying-faster') drivers += ` Decaying faster than expected.`;
      else if (l.decay_status === 'no-decay-detected') drivers += ` No decay yet — treated as a stable baseline shift.`;
    } else {
      drivers = `${activeLifts.length} campaign lifts active, combining for a stacked Brand multiplier.`;
    }

    // Line 5 — caveats
    const warnings = out.warnings || [];
    const unreachable = warnings.find(w => (typeof w === 'string') && w.includes('TARGET_UNREACHABLE'));
    const clipped = warnings.find(w => (typeof w === 'string') && w.includes('ANCHOR_CLIPPED'));
    let caveats = [];
    if (unreachable) {
      caveats.push(`Target not reachable within historical spend bounds — shown number is closest achievable.`);
    }
    if (clipped) {
      caveats.push(`Anchor uses only post-onset weeks because the latest campaign started recently — small sample, wider uncertainty.`);
    }
    if (fmtPct(efficiency) && Math.abs((efficiency || 0) - 100) > 15 && out.target_mode === 'ieccp') {
      caveats.push(`Efficiency result is ${effStr}, more than 15 points from target — check whether assumptions still hold.`);
    }

    // Stitch together
    const paras = [];
    paras.push(headline);
    if (split) paras.push(split);
    if (op2Line) paras.push(op2Line);
    if (drivers) paras.push(drivers);
    if (caveats.length) paras.push(`Heads-up: ${caveats.join(' ')}`);

    return paras.filter(Boolean).join('\n\n');
  }

  const MPENarrative = { generate };
  if (typeof module !== 'undefined' && module.exports) module.exports = MPENarrative;
  else global.MPENarrative = MPENarrative;
})(typeof window !== 'undefined' ? window : globalThis);
