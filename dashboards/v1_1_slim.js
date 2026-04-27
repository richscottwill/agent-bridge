/**
 * v1_1_slim.js — JS mirror of the Python v1.1 Slim stack:
 *   - brand_trajectory.py
 *   - regime_confidence.py
 *   - nb_residual_solver.py
 *   - locked_ytd.py
 *
 * Consumed by mpe_engine.js for Y-period projections. Reads regime_fit_state
 * and ytd_weekly from shared/dashboards/data/projection-data.json.
 *
 * Numerical parity target: within 1% of Python engine output on all 10 markets
 * for common target-mode × period combinations. Drift caught by the parity
 * test suite (Phase 6.1.7 test runs both engines against the same inputs).
 */
(function (global) {
  'use strict';

  // ---------- Regime confidence (mirrors regime_confidence.py) ----------

  const DECAY_STATUS_MODIFIERS = {
    'dormant': 0.10,
    'insufficient-data': 0.20,
    'still-peaking': 0.60,
    'decaying-faster': 0.70,
    'decaying-as-expected': 0.80,
    'decaying-slower': 0.90,
    'no-decay-detected': 1.00,
    'no-fit-state': 0.30,
  };

  function effectiveConfidence(baseConf, decayStatus, regimeMultiplier) {
    regimeMultiplier = regimeMultiplier == null ? 1.0 : regimeMultiplier;
    const base = baseConf == null ? 0.30 : Number(baseConf);
    const mod = DECAY_STATUS_MODIFIERS[decayStatus || 'no-fit-state'] || 0.30;
    return Math.max(0.0, Math.min(1.0, base * mod * regimeMultiplier));
  }

  // ---------- Regime multiplier (mirrors _single_regime_multiplier_at) ----------

  function singleRegimeMultiplierAt(regime, targetWeekDate) {
    const onset = new Date(regime.change_date);
    const weeksSinceOnset = (targetWeekDate - onset) / (7 * 24 * 3600 * 1000);
    if (weeksSinceOnset < 0) return 1.0;

    const peak = regime.peak_multiplier;
    const halfLife = regime.fitted_half_life_weeks
      || regime.authored_half_life_weeks
      || null;

    if (halfLife == null || halfLife <= 0) return peak;

    const excess = peak - 1.0;
    const decayed = excess * Math.pow(0.5, weeksSinceOnset / halfLife);
    return 1.0 + decayed;
  }

  function perRegimeWeightedContribution(regime, targetWeekDate, regimeMultiplier) {
    const raw = singleRegimeMultiplierAt(regime, targetWeekDate);
    const eff = effectiveConfidence(regime.confidence, regime.decay_status, regimeMultiplier);
    return 1.0 + eff * (raw - 1.0);
  }

  function computeRegimeMultipliersPerWeek(regimes, targetWeeks, regimeMultiplier, scenarioOverride) {
    regimeMultiplier = regimeMultiplier == null ? 1.0 : regimeMultiplier;
    if (!regimes || regimes.length === 0) return targetWeeks.map(() => 1.0);
    // Apply scenario override non-destructively. `strip_anchor_lift` is handled
    // by the caller (projectWithLockedYtd); ignored here.
    let effectiveRegimes = regimes;
    if (scenarioOverride) {
      effectiveRegimes = regimes.map(r => {
        const o = { ...r };
        if ('half_life_weeks' in scenarioOverride) {
          o.fitted_half_life_weeks = scenarioOverride.half_life_weeks;
          o.authored_half_life_weeks = scenarioOverride.half_life_weeks;
        }
        if ('peak_multiplier' in scenarioOverride) o.peak_multiplier = scenarioOverride.peak_multiplier;
        if ('force_confidence' in scenarioOverride) o.confidence = scenarioOverride.force_confidence;
        return o;
      });
    }
    return targetWeeks.map(wk => {
      let compound = 1.0;
      for (const r of effectiveRegimes) {
        compound *= perRegimeWeightedContribution(r, wk, regimeMultiplier);
      }
      return compound;
    });
  }

  // Auto-promotion rule (Round 7 P1-04, UI layer):
  // When a lift has decay_status='no-decay-detected' AND n_post_weeks >= 52,
  // we flag it as `absorbed_into_baseline`. This signals to the UI that the
  // "lift" has persisted for ~1 year without decaying and should be treated
  // as structural baseline rather than a transient lift. Effective confidence
  // in the math still applies (because the pre-computed Brand trajectory
  // already baked it in); the flag is purely a semantic label for display.
  // A deeper methodology fix that strips absorbed lifts from the projection
  // math lives upstream in brand_trajectory.py and requires regenerating
  // projection-data.json + regression fixtures — deferred pending Richard's
  // approval per mpe-findings.md P1-04.
  const ABSORBED_INTO_BASELINE_MIN_POST_WEEKS = 52;

  function listRegimesWithConfidence(regimeFitState, regimeMultiplier) {
    regimeMultiplier = regimeMultiplier == null ? 1.0 : regimeMultiplier;
    if (!regimeFitState) return [];
    return regimeFitState.map(r => {
      const eff = effectiveConfidence(r.confidence, r.decay_status, regimeMultiplier);
      const mod = DECAY_STATUS_MODIFIERS[r.decay_status || 'no-fit-state'] || 0.30;
      const absorbed = r.decay_status === 'no-decay-detected'
        && (r.n_post_weeks || 0) >= ABSORBED_INTO_BASELINE_MIN_POST_WEEKS;
      return {
        regime_id: r.regime_id,
        change_date: r.change_date,
        description: (r.description || '').slice(0, 100),
        base_confidence: r.confidence,
        decay_status: r.decay_status,
        status_modifier: mod,
        regime_multiplier: regimeMultiplier,
        effective_confidence: eff,
        n_post_weeks: r.n_post_weeks,
        peak_multiplier: r.peak_multiplier,
        half_life_weeks: r.fitted_half_life_weeks || r.authored_half_life_weeks,
        absorbed_into_baseline: absorbed,
        explanation: absorbed
          ? `Absorbed into baseline (${r.n_post_weeks}w without decay — treat as structural baseline, not transient lift)`
          : `base=${(r.confidence || 0.30).toFixed(2)} × status=${mod.toFixed(2)} × mult=${regimeMultiplier.toFixed(2)} = ${eff.toFixed(2)}`,
      };
    });
  }

  // ---------- Brand trajectory ----------
  //
  // JS port is simplified: uses pre-exported ytd_weekly for the YTD anchor
  // and seasonal shape, applies trend as a flat recency multiplier, then
  // composes with regime multipliers per week. Rather than rebuild the full
  // Python fit (which requires DuckDB queries), the JS port consumes the
  // SUMMARY of Brand behavior embedded in the JSON export and delegates
  // intensive computation to the Python engine when CLI output is needed.
  //
  // This is sufficient for the UI projection use case because:
  //   1. The primary number displayed comes from the Python engine via
  //      `projection-data.json` per-market YTD + fit params.
  //   2. The JS sees: YTD actuals (15 weeks) + Brand CPA scalar + regime
  //      fit state + seasonality weights from the export.
  //   3. Full Brand trajectory fitting (seasonality + trend slope) is
  //      not required here — the JSON carries the already-fit values.

  const SEASONALITY_MIN_WEEKS = 52;
  const BRAND_CPA_MEDIAN_WEEKS = 8;

  function computeBrandCpaProjected(ytdWeekly) {
    if (!ytdWeekly || ytdWeekly.length === 0) return 0;
    const recent = ytdWeekly.slice(-BRAND_CPA_MEDIAN_WEEKS);
    const cpas = [];
    for (const w of recent) {
      const brandCost = w.brand_cost || w.brand_spend || 0;
      const brandRegs = w.brand_regs || w.brand_registrations || 0;
      if (brandCost > 0 && brandRegs > 0) cpas.push(brandCost / brandRegs);
    }
    if (cpas.length === 0) return 0;
    cpas.sort((a, b) => a - b);
    const mid = Math.floor(cpas.length / 2);
    return cpas.length % 2 ? cpas[mid] : (cpas[mid - 1] + cpas[mid]) / 2;
  }

  function computeRecentTrend(ytdWeekly) {
    // Returns {intercept, slope_log}. Simplified — uses last-4-week mean as
    // intercept; slope computed via log-linear OLS on weeks with regs>0.
    if (!ytdWeekly || ytdWeekly.length === 0) return { intercept: 0, slope_log: 0, latestWeek: null };
    const recent = ytdWeekly.slice(-16);
    const regs = recent.map(w => w.brand_regs || w.brand_registrations || 0).filter(r => r > 0);
    if (regs.length < 4) return { intercept: regs.reduce((a, b) => a + b, 0) / (regs.length || 1), slope_log: 0, latestWeek: null };

    const last4 = regs.slice(-4);
    const intercept = last4.reduce((a, b) => a + b, 0) / last4.length;

    const logRegs = regs.map(r => Math.log(r));
    const xs = logRegs.map((_, i) => i);
    const mx = xs.reduce((a, b) => a + b, 0) / xs.length;
    const my = logRegs.reduce((a, b) => a + b, 0) / logRegs.length;
    let num = 0, den = 0;
    for (let i = 0; i < xs.length; i++) {
      num += (xs[i] - mx) * (logRegs[i] - my);
      den += (xs[i] - mx) * (xs[i] - mx);
    }
    let slope = den > 0 ? num / den : 0;
    slope = Math.max(-0.10, Math.min(0.10, slope));

    const latestWeek = recent[recent.length - 1].period_start
      ? new Date(recent[recent.length - 1].period_start)
      : null;
    return { intercept, slope_log: slope, latestWeek };
  }

  const TREND_FADE_HALF_LIFE_WEEKS = 13;

  function trendMultiplierForWeek(trend, targetWeekDate) {
    if (!trend.latestWeek || trend.slope_log === 0) return 1.0;
    const weeksAhead = (targetWeekDate - trend.latestWeek) / (7 * 24 * 3600 * 1000);
    if (weeksAhead <= 0) return 1.0;
    const H = TREND_FADE_HALF_LIFE_WEEKS;
    const fadeIntegral = (trend.slope_log * H / Math.log(2)) * (1.0 - Math.pow(0.5, weeksAhead / H));
    return Math.exp(fadeIntegral);
  }

  function projectBrandTrajectory(marketData, targetWeeks, opts) {
    opts = opts || {};
    const regimeMultiplier = opts.regimeMultiplier == null ? 1.0 : opts.regimeMultiplier;

    // Phase 6.1.7: prefer pre-computed Brand trajectory from the JSON export
    // when available. The Python engine is the source of truth for Brand
    // projections; JS simply reads the pre-fit arrays. This keeps JS and
    // Python numerically identical (within rounding) on the Brand side.
    // The only JS-side computation is regime-multiplier-per-week which
    // does respect regimeMultiplier overrides.
    if (marketData.brand_trajectory_y2026 && targetWeeks.length <= 52) {
      const bt = marketData.brand_trajectory_y2026;
      // Map target weeks to pre-computed weeks. For Y2026 full year this is
      // a 1:1 match on the 52 week slots.
      const regsPerWeek = bt.regs_per_week.slice(0, targetWeeks.length);
      const spendPerWeek = bt.spend_per_week.slice(0, targetWeeks.length);
      const regimeFitState = marketData.regime_fit_state || [];

      // If regimeMultiplier != 1.0, recompute regime component so the user's
      // slider still moves. Otherwise, use the pre-computed values as-is.
      if (Math.abs(regimeMultiplier - 1.0) > 1e-6 && regimeFitState.length > 0) {
        // Apply a per-week multiplier delta relative to pre-computed (which
        // was fit at regime_multiplier=1.0).
        const baselineMults = computeRegimeMultipliersPerWeek(regimeFitState, targetWeeks, 1.0);
        const adjustedMults = computeRegimeMultipliersPerWeek(regimeFitState, targetWeeks, regimeMultiplier);
        const cpa = bt.brand_cpa_used;
        for (let i = 0; i < regsPerWeek.length; i++) {
          const ratio = baselineMults[i] > 0 ? adjustedMults[i] / baselineMults[i] : 1.0;
          regsPerWeek[i] *= ratio;
          spendPerWeek[i] = regsPerWeek[i] * cpa;
        }
      }

      const totalRegs = regsPerWeek.reduce((a, b) => a + b, 0);
      const totalSpend = spendPerWeek.reduce((a, b) => a + b, 0);
      return {
        weeks: targetWeeks,
        regs_per_week: regsPerWeek,
        spend_per_week: spendPerWeek,
        brand_cpa_used: bt.brand_cpa_used,
        total_regs: totalRegs,
        total_spend: totalSpend,
        contribution: bt.contribution,
        warnings: bt.warnings || [],
        lineage: bt.lineage,
      };
    }

    // Fallback: in-browser trajectory fit (approximate). Used when JSON
    // doesn't carry brand_trajectory_y2026 for this market or for non-Y2026
    // periods that aren't yet pre-computed.
    const wSeasonal = opts.weights?.seasonal || 0.40;
    const wTrend = opts.weights?.trend || 0.40;

    const ytd = marketData.ytd_weekly || [];
    const regimeFitState = marketData.regime_fit_state || [];
    const seasonalityWeights = (marketData.parameters?.brand_seasonality_shape?.value_json?.weights)
      || new Array(52).fill(1.0);

    const trend = computeRecentTrend(ytd);
    const anchor = trend.intercept;
    const brandCpa = computeBrandCpaProjected(ytd);

    const regimeMults = computeRegimeMultipliersPerWeek(regimeFitState, targetWeeks, regimeMultiplier);

    const regsPerWeek = [];
    const spendPerWeek = [];
    const streamMults = [];

    for (let idx = 0; idx < targetWeeks.length; idx++) {
      const wk = targetWeeks[idx];
      const isoWeek = _isoWeek(wk);
      const sIdx = Math.min(isoWeek - 1, seasonalityWeights.length - 1);
      const sRaw = seasonalityWeights[sIdx] || 1.0;
      const tRaw = trendMultiplierForWeek(trend, wk);
      const rApplied = regimeMults[idx];
      const sApplied = 1.0 + wSeasonal * (sRaw - 1.0);
      const tApplied = 1.0 + wTrend * (tRaw - 1.0);
      const combined = sApplied * tApplied * rApplied;
      const regs = Math.max(0, anchor * combined);
      regsPerWeek.push(regs);
      spendPerWeek.push(regs * brandCpa);
      streamMults.push({
        seasonal_raw: sRaw, seasonal_applied: sApplied,
        trend_raw: tRaw, trend_applied: tApplied,
        regime_raw: rApplied, combined,
      });
    }

    const totalRegs = regsPerWeek.reduce((a, b) => a + b, 0);
    const totalSpend = spendPerWeek.reduce((a, b) => a + b, 0);
    return {
      weeks: targetWeeks,
      regs_per_week: regsPerWeek,
      spend_per_week: spendPerWeek,
      brand_cpa_used: brandCpa,
      total_regs: totalRegs,
      total_spend: totalSpend,
      contribution: { seasonal: 0.40, trend: 0.40, regime: 0.15, qualitative: 0.05 },
      stream_multipliers_per_week: streamMults,
      warnings: [],
    };
  }

  // ---------- NB residual solver (ieccp + spend branches) ----------

  function nbRegsFromAnnualSpend(annualNbSpend, nWeeks, nbCpaElast) {
    if (nWeeks <= 0 || annualNbSpend <= 0) return { regs: 0, cpa: 0 };
    const weeklySpend = annualNbSpend / nWeeks;
    const weeklyCpa = Math.max(0.01, Math.exp(nbCpaElast.a) * Math.pow(weeklySpend, nbCpaElast.b));
    const weeklyRegs = weeklySpend / weeklyCpa;
    return { regs: weeklyRegs * nWeeks, cpa: weeklyCpa };
  }

  function computeIeccpPercent(brandRegs, nbRegs, brandSpend, nbSpend, brandCcp, nbCcp) {
    if (brandCcp == null || nbCcp == null) return null;
    const denom = brandRegs * brandCcp + nbRegs * nbCcp;
    if (denom <= 0) return null;
    return ((brandSpend + nbSpend) / denom) * 100.0;
  }

  function findNbSpendAtIeccp(targetPct, brandSpend, brandRegs, nbCpaElast, brandCcp, nbCcp, ytdNbSpend, nWeeks, searchLow, searchHigh) {
    const g = (nbOpen) => {
      const nbTotal = nbOpen + ytdNbSpend;
      const { regs } = nbRegsFromAnnualSpend(nbTotal, nWeeks, nbCpaElast);
      const ie = computeIeccpPercent(brandRegs, regs, brandSpend, nbTotal, brandCcp, nbCcp);
      return (ie == null ? 1e9 : ie) - targetPct;
    };
    const gLow = g(searchLow);
    const gHigh = g(searchHigh);
    if (gLow * gHigh > 0) return null;
    // Bisection
    let lo = searchLow, hi = searchHigh;
    for (let i = 0; i < 60; i++) {
      const mid = (lo + hi) / 2;
      const gm = g(mid);
      if (Math.abs(gm) < 0.01) return mid;
      if (gLow * gm < 0) { hi = mid; } else { lo = mid; }
    }
    return (lo + hi) / 2;
  }

  function solveIeccpBranch(targetIeccp, brandSpend, brandRegs, nbCpaElast, brandCcp, nbCcp, ytdNbSpend, nWeeks, toleranceBps) {
    const warnings = [];
    if (brandCcp == null || nbCcp == null) {
      return { nb_spend: 0, nb_regs: 0, warnings: ['UNSUPPORTED_TARGET_MODE'], converged: false };
    }
    const targetPct = targetIeccp < 5.0 ? targetIeccp * 100.0 : targetIeccp;
    const tol = (toleranceBps || 500) / 100.0;
    const SEARCH_LOW = 1.0;
    const SEARCH_HIGH = 1e10;

    const boundLow = findNbSpendAtIeccp(targetPct - tol, brandSpend, brandRegs, nbCpaElast, brandCcp, nbCcp, ytdNbSpend, nWeeks, SEARCH_LOW, SEARCH_HIGH);
    const boundHigh = findNbSpendAtIeccp(targetPct + tol, brandSpend, brandRegs, nbCpaElast, brandCcp, nbCcp, ytdNbSpend, nWeeks, SEARCH_LOW, SEARCH_HIGH);
    let lo, hi;
    if (boundLow == null && boundHigh == null) {
      warnings.push(`TARGET_UNREACHABLE_UNDER_EFFECTIVE_BOUNDS`);
      lo = SEARCH_LOW; hi = SEARCH_HIGH;
    } else if (boundLow == null) {
      lo = SEARCH_LOW; hi = boundHigh;
      warnings.push(`TARGET_UNREACHABLE_ON_LOWER_BAND`);
    } else if (boundHigh == null) {
      lo = boundLow; hi = SEARCH_HIGH;
      warnings.push(`TARGET_UNREACHABLE_ON_UPPER_BAND`);
    } else {
      lo = Math.min(boundLow, boundHigh);
      hi = Math.max(boundLow, boundHigh);
    }

    // Solve for the target precisely inside [lo, hi].
    const f = (nbOpen) => {
      const nbTotal = nbOpen + ytdNbSpend;
      const { regs } = nbRegsFromAnnualSpend(nbTotal, nWeeks, nbCpaElast);
      const ie = computeIeccpPercent(brandRegs, regs, brandSpend, nbTotal, brandCcp, nbCcp);
      return (ie == null ? 1e9 : ie) - targetPct;
    };
    let converged = false;
    let solution = (lo + hi) / 2;
    const fLo = f(lo), fHi = f(hi);
    if (fLo * fHi > 0) {
      solution = Math.abs(fLo) < Math.abs(fHi) ? lo : hi;
    } else {
      let a = lo, b = hi;
      for (let i = 0; i < 60; i++) {
        const mid = (a + b) / 2;
        const fm = f(mid);
        if (Math.abs(fm) < 0.05) { solution = mid; converged = true; break; }
        if (fLo * fm < 0) { b = mid; } else { a = mid; }
        solution = mid;
      }
    }

    const nbTotal = solution + ytdNbSpend;
    const { regs: nbRegs, cpa: nbCpa } = nbRegsFromAnnualSpend(nbTotal, nWeeks, nbCpaElast);
    const ie = computeIeccpPercent(brandRegs, nbRegs, brandSpend, nbTotal, brandCcp, nbCcp);
    if (ie != null && Math.abs(ie - targetPct) > tol) {
      warnings.push(`OUTSIDE_TOLERANCE_BAND: ${ie.toFixed(1)}% vs target ${targetPct.toFixed(1)}%`);
    }
    return {
      nb_spend: nbTotal,
      nb_regs: nbRegs,
      nb_cpa: nbCpa,
      computed_ieccp: ie,
      converged,
      warnings,
    };
  }

  function solveSpendBranch(targetSpend, brandSpend, brandRegs, nbCpaElast, brandCcp, nbCcp, ytdNbSpend, nWeeks) {
    const warnings = [];
    const nbOpen = targetSpend - brandSpend - ytdNbSpend;
    let nbAdj = Math.max(nbOpen, 1000);
    if (nbOpen < 0) warnings.push(`NB_UNDER_FUNDED: ${nbOpen}`);
    const nbTotal = nbAdj + ytdNbSpend;
    const { regs: nbRegs, cpa: nbCpa } = nbRegsFromAnnualSpend(nbTotal, nWeeks, nbCpaElast);
    const ie = computeIeccpPercent(brandRegs, nbRegs, brandSpend, nbTotal, brandCcp, nbCcp);
    return { nb_spend: nbTotal, nb_regs: nbRegs, nb_cpa: nbCpa, computed_ieccp: ie, converged: true, warnings };
  }

  function solveRegsBranch(targetRegs, brandSpend, brandRegs, nbCpaElast, brandCcp, nbCcp, ytdNbSpend, nWeeks) {
    const warnings = [];
    // If Brand alone exceeds the target, NB residual = 0, emit signal.
    const nbRegsNeeded = targetRegs - brandRegs;
    if (nbRegsNeeded <= 0) {
      warnings.push('REGS_TARGET_MET_BY_BRAND');
      return { nb_spend: ytdNbSpend, nb_regs: 0, nb_cpa: null, computed_ieccp: computeIeccpPercent(brandRegs, 0, brandSpend, ytdNbSpend, brandCcp, nbCcp), converged: true, warnings };
    }
    // Bisection on NB spend to hit NB regs target.
    const SEARCH_LOW = 1.0;
    const SEARCH_HIGH = 1e10;
    const f = (nbOpen) => {
      const nbTotal = nbOpen + ytdNbSpend;
      const { regs } = nbRegsFromAnnualSpend(nbTotal, nWeeks, nbCpaElast);
      return regs - nbRegsNeeded;
    };
    const fLow = f(SEARCH_LOW);
    const fHigh = f(SEARCH_HIGH);
    if (fLow * fHigh > 0) {
      // Target not reachable within elasticity bounds.
      warnings.push('TARGET_UNREACHABLE_UNDER_ELASTICITY');
      // Return best-effort closest
      const bestOpen = Math.abs(fLow) < Math.abs(fHigh) ? SEARCH_LOW : SEARCH_HIGH;
      const nbTotal = bestOpen + ytdNbSpend;
      const { regs, cpa } = nbRegsFromAnnualSpend(nbTotal, nWeeks, nbCpaElast);
      const ie = computeIeccpPercent(brandRegs, regs, brandSpend, nbTotal, brandCcp, nbCcp);
      return { nb_spend: nbTotal, nb_regs: regs, nb_cpa: cpa, computed_ieccp: ie, converged: false, warnings };
    }
    let lo = SEARCH_LOW, hi = SEARCH_HIGH;
    let solution = (lo + hi) / 2;
    let converged = false;
    for (let i = 0; i < 60; i++) {
      const mid = (lo + hi) / 2;
      const fm = f(mid);
      if (Math.abs(fm) < 0.5) { solution = mid; converged = true; break; }
      if (fLow * fm < 0) { hi = mid; } else { lo = mid; }
      solution = mid;
    }
    const nbTotal = solution + ytdNbSpend;
    const { regs, cpa } = nbRegsFromAnnualSpend(nbTotal, nWeeks, nbCpaElast);
    const ie = computeIeccpPercent(brandRegs, regs, brandSpend, nbTotal, brandCcp, nbCcp);
    return { nb_spend: nbTotal, nb_regs: regs, nb_cpa: cpa, computed_ieccp: ie, converged, warnings };
  }

  function solveOp2EfficientBranch(targetValue, brandSpend, brandRegs, nbCpaElast, brandCcp, nbCcp, ytdNbSpend, nWeeks) {
    // targetValue is {target_regs, op2_spend_budget}
    if (!targetValue || typeof targetValue !== 'object') {
      return { nb_spend: 0, nb_regs: 0, warnings: ['OP2_EFFICIENT_REQUIRES_OBJECT'], converged: false };
    }
    const targetRegs = targetValue.target_regs;
    const op2Budget = targetValue.op2_spend_budget;
    const regsSol = solveRegsBranch(targetRegs, brandSpend, brandRegs, nbCpaElast, brandCcp, nbCcp, ytdNbSpend, nWeeks);
    const totalSpend = brandSpend + regsSol.nb_spend;
    if (totalSpend <= op2Budget) {
      return regsSol;
    }
    // Over budget — clamp to budget and emit warning.
    const shortfallPct = ((totalSpend - op2Budget) / op2Budget) * 100;
    const clampedSpend = solveSpendBranch(op2Budget, brandSpend, brandRegs, nbCpaElast, brandCcp, nbCcp, ytdNbSpend, nWeeks);
    clampedSpend.warnings.push(`OP2_BUDGET_EXCEEDED: regs target requires ${shortfallPct.toFixed(1)}% above OP2 budget`);
    return clampedSpend;
  }

  function solveNbResidual(brandSpend, brandRegs, targetMode, targetValue, nbCpaElast, brandCcp, nbCcp, ytdNbSpend, nWeeks) {
    if (targetMode === 'spend') return solveSpendBranch(targetValue, brandSpend, brandRegs, nbCpaElast, brandCcp, nbCcp, ytdNbSpend || 0, nWeeks || 52);
    if (targetMode === 'ieccp') return solveIeccpBranch(targetValue, brandSpend, brandRegs, nbCpaElast, brandCcp, nbCcp, ytdNbSpend || 0, nWeeks || 52);
    if (targetMode === 'regs') return solveRegsBranch(targetValue, brandSpend, brandRegs, nbCpaElast, brandCcp, nbCcp, ytdNbSpend || 0, nWeeks || 52);
    if (targetMode === 'op2_efficient') return solveOp2EfficientBranch(targetValue, brandSpend, brandRegs, nbCpaElast, brandCcp, nbCcp, ytdNbSpend || 0, nWeeks || 52);
    return { nb_spend: 0, nb_regs: 0, warnings: [`UNSUPPORTED_TARGET_MODE: ${targetMode}`], converged: false };
  }

  // ---------- Locked-YTD ----------

  function _isoWeek(d) {
    const date = new Date(Date.UTC(d.getFullYear(), d.getMonth(), d.getDate()));
    const dayNum = (date.getUTCDay() + 6) % 7;
    date.setUTCDate(date.getUTCDate() - dayNum + 3);
    const firstThursday = date.valueOf();
    date.setUTCMonth(0, 1);
    if (date.getUTCDay() !== 4) {
      date.setUTCMonth(0, 1 + ((4 - date.getUTCDay()) + 7) % 7);
    }
    return 1 + Math.ceil((firstThursday - date) / (7 * 24 * 3600 * 1000));
  }

  function computeRoyWeeks(year, ytdLatest) {
    const jan4 = new Date(Date.UTC(year, 0, 4));
    const week1Monday = new Date(jan4);
    week1Monday.setUTCDate(jan4.getUTCDate() - jan4.getUTCDay() + 1 - (jan4.getUTCDay() === 0 ? 7 : 0));
    let firstOpenMonday;
    if (ytdLatest == null) {
      firstOpenMonday = week1Monday;
    } else {
      firstOpenMonday = new Date(ytdLatest);
      firstOpenMonday.setUTCDate(firstOpenMonday.getUTCDate() + 7);
    }
    const weeks = [];
    for (let i = 0; i < 52; i++) {
      const w = new Date(week1Monday);
      w.setUTCDate(week1Monday.getUTCDate() + i * 7);
      if (w >= firstOpenMonday) weeks.push(w);
    }
    return weeks;
  }

  function fetchYtdActualsFromData(marketData) {
    const ytd = marketData.ytd_weekly || [];
    let brandRegs = 0, brandSpend = 0, nbRegs = 0, nbSpend = 0;
    let latestWeek = null;
    for (const w of ytd) {
      brandRegs += (w.brand_regs || w.brand_registrations || 0);
      brandSpend += (w.brand_cost || w.brand_spend || 0);
      nbRegs += (w.nb_regs || w.nb_registrations || 0);
      nbSpend += (w.nb_cost || w.nb_spend || 0);
      if (w.period_start) {
        const d = new Date(w.period_start);
        if (!latestWeek || d > latestWeek) latestWeek = d;
      }
    }
    return {
      n_weeks_locked: ytd.length,
      latest_week_locked: latestWeek,
      brand_regs: brandRegs, brand_spend: brandSpend,
      nb_regs: nbRegs, nb_spend: nbSpend,
      total_regs: brandRegs + nbRegs,
      total_spend: brandSpend + nbSpend,
    };
  }

  function projectWithLockedYtd(marketData, year, targetMode, targetValue, opts) {
    opts = opts || {};
    const ytd = fetchYtdActualsFromData(marketData);
    const royWeeks = computeRoyWeeks(year, ytd.latest_week_locked);

    // Period filter (2026-04-26): if opts.periodWeeks is a Set<int> of ISO
    // week numbers that belong to the selected period (e.g. {14..27} for Q2),
    // scope both YTD and RoY outputs to only those weeks. Without this, the
    // projection is always full-year. opts.periodType is used for logging.
    const periodWeeks = opts.periodWeeks || null;
    const isPeriodFiltered = periodWeeks && periodWeeks.size > 0;

    // Use the pre-computed Y2026 trajectory but slice to RoY weeks only —
    // Python does this internally by passing target_weeks = RoY weeks to
    // project_brand_trajectory. Matching that here ensures numerical parity.
    let brandProj;
    if (marketData.brand_trajectory_y2026 && year === 2026) {
      const bt = marketData.brand_trajectory_y2026;
      const nLocked = ytd.n_weeks_locked;
      const sliceStart = Math.min(nLocked, bt.regs_per_week.length);
      let regsPerWeek = bt.regs_per_week.slice(sliceStart);
      let spendPerWeek = bt.spend_per_week.slice(sliceStart);

      // Apply regime_multiplier override and/or scenario_override relative to baseline.
      const regimeMultiplier = opts.regimeMultiplier == null ? 1.0 : opts.regimeMultiplier;
      const scenarioOverride = opts.scenarioOverride || null;
      const regimeFitState = marketData.regime_fit_state || [];
      const needsAdjust = Math.abs(regimeMultiplier - 1.0) > 1e-6 || scenarioOverride;
      if (needsAdjust && regimeFitState.length > 0) {
        const baselineMults = computeRegimeMultipliersPerWeek(regimeFitState, royWeeks, 1.0);
        const adjustedMults = computeRegimeMultipliersPerWeek(regimeFitState, royWeeks, regimeMultiplier, scenarioOverride);
        const cpa = bt.brand_cpa_used;
        for (let i = 0; i < regsPerWeek.length && i < baselineMults.length; i++) {
          const ratio = baselineMults[i] > 0 ? adjustedMults[i] / baselineMults[i] : 1.0;
          regsPerWeek[i] *= ratio;
          spendPerWeek[i] = regsPerWeek[i] * cpa;
        }
      }

      // "Strip anchor lift" scenario: divide all forward regs/spend by the
      // baseline regime multiplier at the anchor reference week (i.e. the
      // latest YTD week). This removes the implicit lift the recent-actuals
      // anchor had baked in — producing a hypothetical "no lift" projection.
      if (scenarioOverride && scenarioOverride.strip_anchor_lift && regimeFitState.length > 0) {
        const anchorRefWeek = ytd.latest_week_locked;
        if (anchorRefWeek) {
          const [baselineAtAnchor] = computeRegimeMultipliersPerWeek(regimeFitState, [anchorRefWeek], 1.0);
          if (baselineAtAnchor && baselineAtAnchor > 0) {
            const cpa = bt.brand_cpa_used;
            for (let i = 0; i < regsPerWeek.length; i++) {
              regsPerWeek[i] /= baselineAtAnchor;
              spendPerWeek[i] = regsPerWeek[i] * cpa;
            }
          }
        }
      }

      brandProj = {
        weeks: royWeeks,
        regs_per_week: regsPerWeek,
        spend_per_week: spendPerWeek,
        brand_cpa_used: bt.brand_cpa_used,
        total_regs: regsPerWeek.reduce((a, b) => a + b, 0),
        total_spend: spendPerWeek.reduce((a, b) => a + b, 0),
        contribution: bt.contribution,
        warnings: bt.warnings || [],
      };
    } else {
      brandProj = projectBrandTrajectory(marketData, royWeeks, opts);
    }

    const params = marketData.parameters || {};
    const nbCpaElast = (params.nb_cpa_elasticity && params.nb_cpa_elasticity.value_json) || { a: 0, b: 0 };
    const brandCcp = params.brand_ccp ? params.brand_ccp.value_scalar : null;
    const nbCcp = params.nb_ccp ? params.nb_ccp.value_scalar : null;

    // Always solve NB at full-year scope first — NB elasticity fits are
    // annual-space. Then slice results to selected period if requested.
    const brandTotalSpend = ytd.brand_spend + brandProj.total_spend;
    const brandTotalRegs = ytd.brand_regs + brandProj.total_regs;
    const nbSol = solveNbResidual(brandTotalSpend, brandTotalRegs, targetMode, targetValue, nbCpaElast, brandCcp, nbCcp, ytd.nb_spend, 52);

    const totalNbSpend = nbSol.nb_spend;
    const totalNbRegs = nbSol.nb_regs;

    // Distribute annual NB spend/regs uniformly across 52 weeks (simple
    // approach; future work could apply NB-seasonality if we had it).
    const nbPerWeekSpend = totalNbSpend / 52;
    const nbPerWeekRegs = totalNbRegs / 52;

    // Build per-week spend/regs arrays for full year (YTD actuals + RoY projected)
    // so we can apply the period filter uniformly.
    const yearRegsPerWeek = [];
    const yearSpendPerWeek = [];
    const yearBrandRegs = [];
    const yearBrandSpend = [];
    const yearNbRegs = [];
    const yearNbSpend = [];
    const ytdWeekly = marketData.ytd_weekly || [];
    for (let i = 0; i < ytdWeekly.length; i++) {
      const w = ytdWeekly[i];
      const br = w.brand_regs || w.brand_registrations || 0;
      const nr = w.nb_regs || w.nb_registrations || 0;
      const bs = w.brand_cost || w.brand_spend || 0;
      const ns = w.nb_cost || w.nb_spend || 0;
      yearBrandRegs.push(br);
      yearNbRegs.push(nr);
      yearBrandSpend.push(bs);
      yearNbSpend.push(ns);
      yearRegsPerWeek.push(br + nr);
      yearSpendPerWeek.push(bs + ns);
    }
    // RoY: from brandProj arrays + NB-per-week flat
    const btRegs = brandProj.regs_per_week || [];
    const btSpend = brandProj.spend_per_week || [];
    for (let i = 0; i < btRegs.length; i++) {
      yearBrandRegs.push(btRegs[i]);
      yearBrandSpend.push(btSpend[i]);
      yearNbRegs.push(nbPerWeekRegs);
      yearNbSpend.push(nbPerWeekSpend);
      yearRegsPerWeek.push(btRegs[i] + nbPerWeekRegs);
      yearSpendPerWeek.push(btSpend[i] + nbPerWeekSpend);
    }

    // Apply period filter
    let periodBrandRegs = ytd.brand_regs + brandProj.total_regs;
    let periodBrandSpend = ytd.brand_spend + brandProj.total_spend;
    let periodNbRegs = totalNbRegs;
    let periodNbSpend = totalNbSpend;
    let periodLabel = 'Y';
    if (isPeriodFiltered) {
      periodBrandRegs = 0;
      periodBrandSpend = 0;
      periodNbRegs = 0;
      periodNbSpend = 0;
      for (let i = 0; i < yearRegsPerWeek.length; i++) {
        // ISO week number for each entry: YTD uses ytd_weekly[i].period_start,
        // RoY uses royWeeks[i - ytdWeekly.length]
        let wkDate;
        if (i < ytdWeekly.length) {
          wkDate = new Date(ytdWeekly[i].period_start);
        } else {
          wkDate = royWeeks[i - ytdWeekly.length];
        }
        if (!wkDate) continue;
        const wkNum = _isoWeek(wkDate);
        if (periodWeeks.has(wkNum)) {
          periodBrandRegs += yearBrandRegs[i];
          periodBrandSpend += yearBrandSpend[i];
          periodNbRegs += yearNbRegs[i];
          periodNbSpend += yearNbSpend[i];
        }
      }
      periodLabel = opts.periodType || 'period';
    }

    const totalSpend = periodBrandSpend + periodNbSpend;
    const totalRegs = periodBrandRegs + periodNbRegs;
    const blendedCpa = totalRegs > 0 ? totalSpend / totalRegs : 0;
    const ie = computeIeccpPercent(periodBrandRegs, periodNbRegs, periodBrandSpend, periodNbSpend, brandCcp, nbCcp);

    return {
      year, target_mode: targetMode, target_value: targetValue,
      period: periodLabel,
      ytd,
      roy: {
        n_weeks: royWeeks.length,
        brand_regs: brandProj.total_regs,
        brand_spend: brandProj.total_spend,
        nb_regs: Math.max(0, totalNbRegs - ytd.nb_regs),
        nb_spend: Math.max(0, totalNbSpend - ytd.nb_spend),
      },
      // Full-year per-week arrays for chart rendering (chart shows whole year
      // regardless of period filter so user sees context)
      year_weekly: {
        ytd_weeks: ytdWeekly.length,
        brand_regs: yearBrandRegs,
        brand_spend: yearBrandSpend,
        nb_regs: yearNbRegs,
        nb_spend: yearNbSpend,
      },
      totals: {
        brand_regs: periodBrandRegs, brand_spend: periodBrandSpend,
        nb_regs: periodNbRegs, nb_spend: periodNbSpend,
        total_regs: totalRegs, total_spend: totalSpend,
        blended_cpa: blendedCpa, computed_ieccp: ie,
        // Annual totals preserved for OP2 comparison
        annual_brand_regs: brandTotalRegs, annual_brand_spend: brandTotalSpend,
        annual_nb_regs: totalNbRegs, annual_nb_spend: totalNbSpend,
        annual_total_regs: brandTotalRegs + totalNbRegs,
        annual_total_spend: brandTotalSpend + totalNbSpend,
      },
      contribution_breakdown: brandProj.contribution,
      warnings: [].concat(brandProj.warnings || [], nbSol.warnings || []),
      regime_stack: listRegimesWithConfidence(marketData.regime_fit_state, opts.regimeMultiplier),
    };
  }

  // ---------- Bootstrap CI (Round 10 P1-01 Option C) ----------
  //
  // The legacy Monte Carlo path in mpe_engine.js samples from the deprecated
  // v1 elasticity parameters (brand_cpa_elasticity, brand_yoy_growth,
  // brand_spend_share) — all rows that mpe_schema_v3.sql deactivated in the
  // 2026-04-23 v1.1 Slim cutover. Every market has returned empty
  // credible_intervals for four days.
  //
  // Bootstrap CI produces honest uncertainty bands directly from V1.1 Slim
  // output + the YTD residual distribution, no sampling required:
  //
  //   1. Compute per-week residuals for YTD: r[i] = actual[i] - fitted_trend[i]
  //      where fitted_trend is a simple centered moving average of YTD.
  //   2. Estimate residual sd from the last ~16 YTD weeks.
  //   3. For projection week k (1..52), scale sd by sqrt(k) to reflect
  //      accumulating forecast uncertainty (random-walk idiom).
  //   4. Apply z × scaled_sd to produce lower/upper bands.
  //
  // This is NOT a Bayesian posterior. It's a plausible-range estimate that
  // reflects the noise seen in recent actuals. Documented honestly in the
  // narrative + How-modal footnote.
  //
  // alpha=0.10 → 90% band (z ≈ 1.645).
  // alpha=0.20 → 80%, alpha=0.05 → 95%, etc.
  function bootstrapCI(projectionOutput, ytdWeekly, alpha) {
    alpha = alpha == null ? 0.10 : alpha;
    // Z-scores for common alphas.
    const zTable = { 0.05: 1.960, 0.10: 1.645, 0.20: 1.282, 0.50: 0.674 };
    const z = zTable[alpha] != null ? zTable[alpha]
      : Math.max(0.5, 1.96 - 1.28 * (alpha - 0.05) / 0.15); // fallback linear interp

    const ytd = ytdWeekly || [];
    const actuals = ytd.map(w => (w.brand_regs || w.brand_registrations || 0) + (w.nb_regs || w.nb_registrations || 0));

    // Residual sd from last up to 16 YTD weeks vs centered 4-week moving avg.
    let residualSd = 0;
    if (actuals.length >= 6) {
      const window = actuals.slice(-16);
      const residuals = [];
      for (let i = 2; i < window.length - 2; i++) {
        const ma = (window[i - 2] + window[i - 1] + window[i + 1] + window[i + 2]) / 4;
        residuals.push(window[i] - ma);
      }
      if (residuals.length >= 3) {
        const mean = residuals.reduce((a, b) => a + b, 0) / residuals.length;
        const variance = residuals.reduce((s, r) => s + (r - mean) * (r - mean), 0) / residuals.length;
        residualSd = Math.sqrt(variance);
      }
    }
    if (!Number.isFinite(residualSd) || residualSd <= 0) {
      // Fallback: 5% of hero total as a sanity cap so CI is never silently zero.
      const t = (projectionOutput && projectionOutput.totals) || {};
      residualSd = Math.max(1, Math.abs(t.total_regs || 0) * 0.05 / 12); // ~5% per year / 12 weeks
    }

    // Full-year per-week arrays from the projection (YTD + RoY).
    const yw = projectionOutput && projectionOutput.year_weekly;
    if (!yw || !yw.brand_regs || yw.brand_regs.length === 0) {
      return { available: false, reason: 'no year_weekly' };
    }
    const nWeeks = yw.brand_regs.length;
    const ytdWeeks = yw.ytd_weeks || ytd.length;

    const lower = new Array(nWeeks);
    const upper = new Array(nWeeks);
    const lowerSpend = new Array(nWeeks);
    const upperSpend = new Array(nWeeks);

    // Per-week central = brand+nb total regs; per-week spend central = brand+nb spend.
    for (let i = 0; i < nWeeks; i++) {
      const centralRegs = (yw.brand_regs[i] || 0) + (yw.nb_regs[i] || 0);
      const centralSpend = (yw.brand_spend[i] || 0) + (yw.nb_spend[i] || 0);
      if (i < ytdWeeks) {
        // Locked YTD — no uncertainty on actuals.
        lower[i] = centralRegs;
        upper[i] = centralRegs;
        lowerSpend[i] = centralSpend;
        upperSpend[i] = centralSpend;
      } else {
        // RoY — scale sd by sqrt(weeks-into-forecast) for random-walk uncertainty.
        const k = (i - ytdWeeks) + 1;
        const bandRegs = z * residualSd * Math.sqrt(k);
        // Proportional band on spend (share of total regs → total spend)
        const spendRatio = centralRegs > 0 ? centralSpend / centralRegs : 0;
        const bandSpend = bandRegs * Math.max(spendRatio, 1);
        lower[i] = Math.max(0, centralRegs - bandRegs);
        upper[i] = centralRegs + bandRegs;
        lowerSpend[i] = Math.max(0, centralSpend - bandSpend);
        upperSpend[i] = centralSpend + bandSpend;
      }
    }

    // Total CI: sum upper/lower per week (this overstates slightly — ideal
    // would be sqrt(sum sd²) since errors partially cancel — but for a
    // leadership-facing display, "plausible range" is more useful than
    // "statistically-correct-assuming-independence" narrower band).
    const totalRegsLower = lower.reduce((a, b) => a + b, 0);
    const totalRegsUpper = upper.reduce((a, b) => a + b, 0);
    const totalSpendLower = lowerSpend.reduce((a, b) => a + b, 0);
    const totalSpendUpper = upperSpend.reduce((a, b) => a + b, 0);

    return {
      available: true,
      method: 'bootstrap_from_residuals',
      alpha: alpha,
      z: z,
      residual_sd: residualSd,
      per_week: {
        regs: { lower, upper },
        spend: { lower: lowerSpend, upper: upperSpend },
      },
      totals: {
        total_regs: {
          central: (projectionOutput.totals && projectionOutput.totals.total_regs) || 0,
          lower: totalRegsLower,
          upper: totalRegsUpper,
        },
        total_spend: {
          central: (projectionOutput.totals && projectionOutput.totals.total_spend) || 0,
          lower: totalSpendLower,
          upper: totalSpendUpper,
        },
      },
      footnote: 'Bootstrap approximation from fit residuals; full posterior credible intervals are pending migration to the updated schema.',
    };
  }

  // ---------- Exports ----------

  global.V1_1_Slim = {
    // Constants
    DECAY_STATUS_MODIFIERS,
    TREND_FADE_HALF_LIFE_WEEKS,
    // Regime confidence
    effectiveConfidence,
    listRegimesWithConfidence,
    // Regime multipliers
    singleRegimeMultiplierAt,
    computeRegimeMultipliersPerWeek,
    // Brand trajectory
    projectBrandTrajectory,
    computeRecentTrend,
    computeBrandCpaProjected,
    trendMultiplierForWeek,
    // NB residual solver
    solveNbResidual,
    solveIeccpBranch,
    solveSpendBranch,
    solveRegsBranch,
    solveOp2EfficientBranch,
    nbRegsFromAnnualSpend,
    computeIeccpPercent,
    // Locked-YTD
    projectWithLockedYtd,
    fetchYtdActualsFromData,
    computeRoyWeeks,
    // Bootstrap CI (P1-01 Option C)
    bootstrapCI,
  };
})(typeof globalThis !== 'undefined' ? globalThis : (typeof window !== 'undefined' ? window : this));
