/**
 * mpe_engine.js — Market Projection Engine, JavaScript mirror of mpe_engine.py.
 *
 * WHY THIS EXISTS
 *   The projection UI (projection.html) needs to run in any browser —
 *   Kiro dashboard, SharePoint embed, local file, Symphony. It can't
 *   call Python. So we mirror the Python engine's math here.
 *
 * PARITY GUARANTEE
 *   Deterministic output: 0.1% tolerance vs Python.
 *   Monte Carlo output: 2% tolerance vs Python (different RNGs).
 *   Function signatures match the Python engine where reasonable.
 *   Parity drift is caught by mpe-parity.kiro.hook every edit.
 *
 * HOW TO USE
 *   const data = await fetch('data/projection-data.json').then(r => r.json());
 *   const inputs = {scope: 'MX', timePeriod: 'Q2', targetMode: 'spend',
 *                   targetValue: 325000, credibilityLevels: [0.50, 0.70, 0.80, 0.90]};
 *   const out = MPE.project(inputs, data);
 *   const ciOut = await MPE.projectWithUncertainty(inputs, data);  // Web Worker
 *
 * WHAT HAPPENS ON FAILURE
 *   - Missing market params → outcome='SETUP_REQUIRED' with warnings
 *   - Unknown scope → outcome='INVALID_INPUT'
 *   - Infeasible target → outcome='INFEASIBLE' with closest_feasible
 *   - Non-finite math (log of zero, overflow) → NaN guards produce 0 or 1
 *   - MC failure in worker → project() fallback with empty credible_intervals
 */
(function (global) {
  'use strict';

  // ---------- Constants (must match mpe_engine.py) ----------

  const ENGINE_VERSION = '1.0.0';
  const ALL_MARKETS = ['US', 'CA', 'UK', 'DE', 'FR', 'IT', 'ES', 'JP', 'MX', 'AU'];
  const ALL_REGIONS = ['NA', 'EU5', 'WW'];
  const REGION_CONSTITUENTS = {
    NA: ['US', 'CA'],
    EU5: ['UK', 'DE', 'FR', 'IT', 'ES'],
    WW: ALL_MARKETS,
  };

  const HISTORICAL_EXTRAPOLATION_MULTIPLIER = 1.5;  // R2.13
  const HIGH_UNCERTAINTY_RATIO = 2.0;               // R12.5
  const VERY_WIDE_CI_RATIO = 3.0;                   // R11.8 (MY2)
  const MIN_WEEKS_MULTI_YEAR = 104;                 // R11.5
  const SAMPLES_UI = 200;                           // R12.2 (locked)

  // ---------- Small utilities ----------

  function clamp(x, lo, hi) { return Math.max(lo, Math.min(hi, x)); }

  function isFiniteNum(x) { return typeof x === 'number' && Number.isFinite(x); }

  function safeFloat(x, fallback) {
    if (x === null || x === undefined) return fallback;
    const n = Number(x);
    return isFiniteNum(n) ? n : fallback;
  }

  function quantile(sortedArr, q) {
    if (sortedArr.length === 0) return 0;
    const pos = q * (sortedArr.length - 1);
    const base = Math.floor(pos);
    const rest = pos - base;
    if (base + 1 < sortedArr.length) {
      return sortedArr[base] + rest * (sortedArr[base + 1] - sortedArr[base]);
    }
    return sortedArr[base];
  }

  // ---------- Seeded RNG (for deterministic MC) ----------

  function mulberry32(seed) {
    let t = seed >>> 0;
    return function () {
      t = (t + 0x6D2B79F5) >>> 0;
      let x = t;
      x = Math.imul(x ^ (x >>> 15), x | 1);
      x ^= x + Math.imul(x ^ (x >>> 7), x | 61);
      return ((x ^ (x >>> 14)) >>> 0) / 4294967296;
    };
  }

  function normalSample(rng, mean, std) {
    // Box-Muller
    const u = 1 - rng();
    const v = rng();
    const z = Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v);
    return mean + std * z;
  }

  function multivariateNormal2D(rng, mean, cov) {
    // Cholesky decomposition of 2x2 posterior_cov
    const a = cov[0][0];
    const b = cov[0][1];
    const d = cov[1][1];
    if (!isFiniteNum(a) || !isFiniteNum(b) || !isFiniteNum(d) || a <= 0 || (a * d - b * b) <= 0) {
      // Singular — fall back to independent with 30% CV
      const sa = Math.abs(mean[0]) * 0.30 + 0.05;
      const sb = Math.abs(mean[1]) * 0.30 + 0.05;
      return [normalSample(rng, mean[0], sa), normalSample(rng, mean[1], sb)];
    }
    const l11 = Math.sqrt(a);
    const l21 = b / l11;
    const l22 = Math.sqrt(Math.max(d - l21 * l21, 1e-12));
    const z1 = normalSample(rng, 0, 1);
    const z2 = normalSample(rng, 0, 1);
    return [mean[0] + l11 * z1, mean[1] + l21 * z1 + l22 * z2];
  }

  // ---------- Elasticity math (mirrors _apply_cpa_elasticity) ----------

  function applyCpaElasticity(spend, a, b) {
    if (spend <= 0) return 1.0;
    let cpa;
    try {
      cpa = Math.exp(a) * Math.pow(spend, b);
    } catch (e) {
      cpa = 1e6;
    }
    if (!isFiniteNum(cpa) || cpa <= 0) cpa = 1e6;
    return Math.max(cpa, 0.01);
  }

  function applyCpcElasticity(spend, a, b) {
    if (spend <= 0) return 0.01;
    let cpc;
    try {
      cpc = Math.exp(a) * Math.pow(spend, b);
    } catch (e) {
      cpc = 100.0;
    }
    if (!isFiniteNum(cpc) || cpc <= 0) cpc = 100.0;
    return Math.max(cpc, 0.01);
  }

  // ---------- Time period parser (mirrors parse_time_period) ----------

  function parseTimePeriod(timePeriod) {
    if (!timePeriod || typeof timePeriod !== 'string') {
      throw new Error('time_period must be a non-empty string');
    }
    const tp = timePeriod.toUpperCase();

    // MY first (both start with 'M')
    if (tp.startsWith('MY')) {
      const n = parseInt(tp.slice(2), 10);
      if (!Number.isInteger(n)) throw new Error(`Invalid multi-year period ${timePeriod}`);
      if (n > 2) throw new Error('MY3 and beyond not supported in v1 (R11.9). Use MY1 or MY2.');
      if (n < 1) throw new Error(`Multi-year must be >= 1, got ${n}`);
      return { type: 'multi_year', n_years: n, weeks: Array.from({ length: 52 }, (_, i) => i + 1) };
    }

    if (tp.startsWith('W')) {
      const w = parseInt(tp.slice(1), 10);
      if (!Number.isInteger(w) || w < 1 || w > 53) throw new Error(`Invalid week ${timePeriod}`);
      return { type: 'week', weeks: [w], n_years: 1 };
    }

    if (tp.startsWith('M')) {
      const m = parseInt(tp.slice(1), 10);
      if (!Number.isInteger(m) || m < 1 || m > 12) throw new Error(`Invalid month ${timePeriod}`);
      // Approximate: each month = 4-5 weeks (use 52/12 ≈ 4.33)
      const startWeek = Math.round((m - 1) * 52 / 12) + 1;
      const endWeek = Math.round(m * 52 / 12);
      const weeks = [];
      for (let w = startWeek; w <= endWeek; w++) weeks.push(w);
      return { type: 'month', weeks, n_years: 1 };
    }

    if (tp.startsWith('Q')) {
      const q = parseInt(tp.slice(1), 10);
      if (!Number.isInteger(q) || q < 1 || q > 4) throw new Error(`Invalid quarter ${timePeriod}`);
      // Q1=W1-W13, Q2=W14-W27, Q3=W28-W40, Q4=W41-W52  (matches Python engine's 14-week Q2)
      const boundaries = [[1, 13], [14, 27], [28, 40], [41, 52]];
      const [a, b] = boundaries[q - 1];
      const weeks = [];
      for (let w = a; w <= b; w++) weeks.push(w);
      return { type: 'quarter', weeks, n_years: 1 };
    }

    if (tp.startsWith('Y')) {
      const y = parseInt(tp.slice(1), 10);
      if (!Number.isInteger(y)) throw new Error(`Invalid year ${timePeriod}`);
      return { type: 'year', year: y, weeks: Array.from({ length: 52 }, (_, i) => i + 1), n_years: 1 };
    }

    throw new Error(`Unrecognized time_period format: ${timePeriod}`);
  }

  // ---------- Extract per-market params from data.markets[MARKET] ----------

  function extractParams(marketData) {
    if (!marketData || !marketData.parameters) return null;
    const p = marketData.parameters;
    const getJson = (name) => (p[name] && p[name].value_json) || null;
    const getScalar = (name) => (p[name] ? p[name].value_scalar : null);
    const getFallback = (name) => (p[name] ? p[name].fallback_level : null);

    const share = getJson('brand_spend_share') || {};
    return {
      brandCpaElast: getJson('brand_cpa_elasticity') || { a: 0, b: 0 },
      nbCpaElast: getJson('nb_cpa_elasticity') || { a: 0, b: 0 },
      brandCpcElast: getJson('brand_cpc_elasticity') || getJson('brand_cpa_elasticity') || { a: 0, b: 0 },
      nbCpcElast: getJson('nb_cpc_elasticity') || getJson('nb_cpa_elasticity') || { a: 0, b: 0 },
      brandSeasonality: getJson('brand_seasonality_shape') || { weights: new Array(52).fill(1.0) },
      nbSeasonality: getJson('nb_seasonality_shape') || { weights: new Array(52).fill(1.0) },
      brandYoy: getJson('brand_yoy_growth') || { mean: 0, std: 0.10 },
      nbYoy: getJson('nb_yoy_growth') || { mean: 0, std: 0.10 },
      brandCcp: safeFloat(getScalar('brand_ccp'), null),
      nbCcp: safeFloat(getScalar('nb_ccp'), null),
      brandShare: safeFloat(share.brand_share, 0.20),
      supportedModes: (p.supported_target_modes && p.supported_target_modes.value_json) || ['spend', 'ieccp', 'regs'],
      // Mechanism A (2026-04-23): pass-through operational spend bounds from marketData root.
      // Consumed by solveIeccpTarget to clamp search space.
      spendBounds: marketData._spend_bounds || null,
      fallbackLevels: {
        brandCpa: getFallback('brand_cpa_elasticity'),
        nbCpa: getFallback('nb_cpa_elasticity'),
        brandCpc: getFallback('brand_cpc_elasticity'),
        nbCpc: getFallback('nb_cpc_elasticity'),
        brandSeasonality: getFallback('brand_seasonality_shape'),
        nbSeasonality: getFallback('nb_seasonality_shape'),
      },
    };
  }

  function requiredParamsPresent(marketData) {
    const required = ['brand_cpa_elasticity', 'nb_cpa_elasticity',
                      'brand_seasonality_shape', 'nb_seasonality_shape',
                      'brand_yoy_growth', 'nb_yoy_growth', 'brand_spend_share'];
    if (!marketData || !marketData.parameters) return { ok: false, missing: required };
    const missing = required.filter(r => !marketData.parameters[r]);
    return { ok: missing.length === 0, missing };
  }

  // ---------- Point projection (mirrors _project_market_spend_target) ----------

  function projectMarketSpend(totalSpend, params, tp, opts) {
    opts = opts || {};
    const brandShare = params.brandShare;
    const nbShare = 1.0 - brandShare;

    const brandWeights = (params.brandSeasonality.weights && params.brandSeasonality.weights.length === 52)
      ? params.brandSeasonality.weights : new Array(52).fill(1.0);
    const nbWeights = (params.nbSeasonality.weights && params.nbSeasonality.weights.length === 52)
      ? params.nbSeasonality.weights : new Array(52).fill(1.0);

    // YoY multiplier for multi-year
    let yoyMultiplier = 1.0;
    let yoyApplied = { brand: 0.0, nb: 0.0 };
    if (tp.type === 'multi_year') {
      const yrs = tp.n_years;
      const brandMean = safeFloat(params.brandYoy.mean, 0.0);
      const nbMean = safeFloat(params.nbYoy.mean, 0.0);
      const brandGrowth = Math.pow(1.0 + brandMean, yrs);
      const nbGrowth = Math.pow(1.0 + nbMean, yrs);
      yoyApplied = { brand: brandGrowth - 1.0, nb: nbGrowth - 1.0 };
      yoyMultiplier = brandShare * brandGrowth + nbShare * nbGrowth;
    }

    const brandUplift = 1 + (opts.brandUpliftPct || 0) / 100.0;
    const nbUplift = 1 + (opts.nbUpliftPct || 0) / 100.0;

    const weeks = [];
    const nWeeks = Math.max(tp.weeks.length, 1);
    const periodFactor = 1.0 / nWeeks;

    let totalBrandRegs = 0, totalNbRegs = 0, totalBrandSpend = 0, totalNbSpend = 0;
    let totalBrandClicks = 0, totalNbClicks = 0;

    for (const wkNum of tp.weeks) {
      const idx = ((wkNum - 1) % 52);
      const brandWt = isFiniteNum(brandWeights[idx]) ? brandWeights[idx] : 1.0;
      const nbWt = isFiniteNum(nbWeights[idx]) ? nbWeights[idx] : 1.0;

      const wBrandSpend = totalSpend * brandShare * brandWt * periodFactor * brandUplift * yoyMultiplier;
      const wNbSpend = totalSpend * nbShare * nbWt * periodFactor * nbUplift * yoyMultiplier;

      const bCpa = applyCpaElasticity(wBrandSpend, params.brandCpaElast.a, params.brandCpaElast.b);
      const nCpa = applyCpaElasticity(wNbSpend, params.nbCpaElast.a, params.nbCpaElast.b);
      const bCpc = applyCpcElasticity(wBrandSpend, params.brandCpcElast.a, params.brandCpcElast.b);
      const nCpc = applyCpcElasticity(wNbSpend, params.nbCpcElast.a, params.nbCpcElast.b);

      const bRegs = bCpa > 0 ? wBrandSpend / bCpa : 0;
      const nRegs = nCpa > 0 ? wNbSpend / nCpa : 0;
      const bClicks = bCpc > 0 ? wBrandSpend / bCpc : 0;
      const nClicks = nCpc > 0 ? wNbSpend / nCpc : 0;

      totalBrandRegs += bRegs;
      totalNbRegs += nRegs;
      totalBrandSpend += wBrandSpend;
      totalNbSpend += wNbSpend;
      totalBrandClicks += bClicks;
      totalNbClicks += nClicks;

      const wSpend = wBrandSpend + wNbSpend;
      const wRegs = bRegs + nRegs;
      let ieccp = null;
      if (params.brandCcp !== null && params.nbCcp !== null) {
        const denom = bRegs * params.brandCcp + nRegs * params.nbCcp;
        ieccp = denom > 0 ? (wSpend / denom) * 100.0 : null;
      }

      weeks.push({
        week_num: wkNum,
        week_key: `${tp.type}_W${String(wkNum).padStart(2, '0')}`,
        brand_regs: bRegs, nb_regs: nRegs,
        brand_spend: wBrandSpend, nb_spend: wNbSpend,
        brand_clicks: bClicks, nb_clicks: nClicks,
        brand_cpa: bCpa, nb_cpa: nCpa,
        blended_cpa: wRegs > 0 ? wSpend / wRegs : 0,
        ieccp,
      });
    }

    const totalRegs = totalBrandRegs + totalNbRegs;
    const totalSpendOut = totalBrandSpend + totalNbSpend;
    let ieccpTotal = null;
    if (params.brandCcp !== null && params.nbCcp !== null && totalRegs > 0) {
      const denom = totalBrandRegs * params.brandCcp + totalNbRegs * params.nbCcp;
      if (denom > 0) ieccpTotal = (totalSpendOut / denom) * 100.0;
    }

    return {
      weeks,
      totals: {
        brand_regs: totalBrandRegs,
        nb_regs: totalNbRegs,
        total_regs: totalRegs,
        brand_spend: totalBrandSpend,
        nb_spend: totalNbSpend,
        total_spend: totalSpendOut,
        brand_clicks: totalBrandClicks,
        nb_clicks: totalNbClicks,
        blended_cpa: totalRegs > 0 ? totalSpendOut / totalRegs : 0,
        ieccp: ieccpTotal,
        yoy_growth_applied: yoyApplied,
      },
    };
  }

  // ---------- Target mode solvers ----------

  function solveIeccpTarget(targetIeccp, params, tp, opts, maxIter, tolerance) {
    maxIter = maxIter || 30;
    tolerance = tolerance || 0.1;
    // Normalize target to percentage scale. Internal ie%CCP from
    // projectMarketSpend returns on the percentage scale (e.g. 121.26).
    // If caller supplies decimal (e.g. 0.75 for 75%), convert to percentage.
    // Fixes 2026-04-23 MX Y2026 solver bug where 0.75 compared against 121.26
    // collapsed binary search to lowSpend = $1,000.
    if (targetIeccp !== null && targetIeccp !== undefined && targetIeccp < 5.0) {
      targetIeccp = targetIeccp * 100.0;
    }
    let lowSpend = 1000.0;
    let highSpend = 100_000_000.0;
    const boundWarnings = [];

    // Mechanism A bounds (2026-04-23): respect operational spend floors/ceilings
    // from params.spendBounds (passed through by extractParams from marketData._spend_bounds).
    // Same logic as Python mpe_engine._solve_ieccp_target.
    const bounds = (params && params.spendBounds) ? params.spendBounds : null;
    if (bounds) {
      const brandShare = (params && typeof params.brandShare === 'number') ? params.brandShare : 0.20;
      const nbShare = Math.max(1.0 - brandShare, 0.01);
      const nWeeksInPeriod = Math.max((tp && tp.weeks && tp.weeks.length) || 1, 1);
      if (bounds.min_weekly_nb_spend != null) {
        const floorFromNb = (bounds.min_weekly_nb_spend * nWeeksInPeriod) / nbShare;
        if (floorFromNb > lowSpend) {
          lowSpend = floorFromNb;
          boundWarnings.push(`low_spend raised to $${Math.round(floorFromNb).toLocaleString()} by min_weekly_nb_spend=$${bounds.min_weekly_nb_spend.toLocaleString()}`);
        }
      }
      if (bounds.min_weekly_brand_spend != null) {
        const floorFromBrand = (bounds.min_weekly_brand_spend * nWeeksInPeriod) / Math.max(brandShare, 0.01);
        if (floorFromBrand > lowSpend) {
          lowSpend = floorFromBrand;
          boundWarnings.push(`low_spend raised to $${Math.round(floorFromBrand).toLocaleString()} by min_weekly_brand_spend`);
        }
      }
      if (bounds.max_weekly_nb_spend != null) {
        const ceilingFromNb = (bounds.max_weekly_nb_spend * nWeeksInPeriod) / nbShare;
        if (ceilingFromNb < highSpend) {
          highSpend = ceilingFromNb;
          boundWarnings.push(`high_spend lowered to $${Math.round(ceilingFromNb).toLocaleString()} by max_weekly_nb_spend=$${bounds.max_weekly_nb_spend.toLocaleString()}`);
        }
      }
      if (bounds.max_weekly_brand_spend != null) {
        const ceilingFromBrand = (bounds.max_weekly_brand_spend * nWeeksInPeriod) / Math.max(brandShare, 0.01);
        if (ceilingFromBrand < highSpend) {
          highSpend = ceilingFromBrand;
          boundWarnings.push(`high_spend lowered to $${Math.round(ceilingFromBrand).toLocaleString()} by max_weekly_brand_spend`);
        }
      }
      if (lowSpend >= highSpend) highSpend = lowSpend * 1.01;
    }

    let bestSpend = highSpend;
    let bestResult = projectMarketSpend(highSpend, params, tp, opts);

    if (bestResult.totals.ieccp === null) {
      return { weeks: bestResult.weeks, totals: bestResult.totals, solvedSpend: highSpend, boundWarnings };
    }

    for (let i = 0; i < maxIter; i++) {
      const mid = (lowSpend + highSpend) / 2.0;
      const result = projectMarketSpend(mid, params, tp, opts);
      if (result.totals.ieccp === null) break;
      const delta = result.totals.ieccp - targetIeccp;
      if (Math.abs(delta) < tolerance) {
        return { weeks: result.weeks, totals: result.totals, solvedSpend: mid, boundWarnings };
      }
      if (delta < 0) lowSpend = mid; else highSpend = mid;
      bestSpend = mid;
      bestResult = result;
    }

    // Under-bounds target-unreachable warning (mirror Python)
    const finalDelta = bestResult.totals.ieccp != null ? bestResult.totals.ieccp - targetIeccp : null;
    if (finalDelta !== null && Math.abs(finalDelta) > tolerance) {
      const dir = finalDelta < 0 ? 'lower' : 'higher';
      boundWarnings.push(`TARGET_UNREACHABLE_UNDER_BOUNDS: solver stuck at ie%CCP=${bestResult.totals.ieccp.toFixed(1)}% vs target=${targetIeccp.toFixed(1)}% (${dir} than target); operational bounds prevent reaching target`);
    }

    return { weeks: bestResult.weeks, totals: bestResult.totals, solvedSpend: bestSpend, boundWarnings };
  }

  function solveRegsTarget(targetRegs, params, tp, opts, maxIter, tolerance) {
    maxIter = maxIter || 30;
    tolerance = tolerance || 0.01;  // 1%
    let lowSpend = 1000.0;
    let highSpend = 100_000_000.0;

    let bestSpend = highSpend;
    let bestResult = projectMarketSpend(highSpend, params, tp, opts);

    // Check feasibility at both extremes
    if (bestResult.totals.total_regs < targetRegs) {
      // Even max spend can't reach target
      return {
        weeks: bestResult.weeks,
        totals: bestResult.totals,
        solvedSpend: highSpend,
        infeasibility: {
          outcome: 'INFEASIBLE',
          binding_constraint: 'max_spend_exceeded',
          explanation: `Target ${targetRegs} regs exceeds max achievable (${Math.round(bestResult.totals.total_regs)}) within historical range`,
          closest_feasible: { regs: bestResult.totals.total_regs, spend: highSpend },
        },
      };
    }

    for (let i = 0; i < maxIter; i++) {
      const mid = (lowSpend + highSpend) / 2.0;
      const result = projectMarketSpend(mid, params, tp, opts);
      const relDelta = (result.totals.total_regs - targetRegs) / Math.max(targetRegs, 1);
      if (Math.abs(relDelta) < tolerance) {
        return { weeks: result.weeks, totals: result.totals, solvedSpend: mid };
      }
      if (result.totals.total_regs < targetRegs) lowSpend = mid; else highSpend = mid;
      bestSpend = mid;
      bestResult = result;
    }
    return { weeks: bestResult.weeks, totals: bestResult.totals, solvedSpend: bestSpend };
  }

  // ---------- Compute credible intervals (mirrors _compute_credible_intervals) ----------

  function computeCredibleIntervals(solvedSpend, params, tp, opts, credibilityLevels, nSamples, rngSeed) {
    credibilityLevels = credibilityLevels || [0.50, 0.70, 0.80, 0.90];
    nSamples = nSamples || SAMPLES_UI;
    const rng = mulberry32(rngSeed || 42);

    // Pre-sample elasticity (a, b) pairs for each segment
    const sampleElast = (elast) => {
      const cov = elast.posterior_cov || [[0.01, 0], [0, 0.01]];
      const mean = [safeFloat(elast.a, 0), safeFloat(elast.b, 0)];
      return multivariateNormal2D(rng, mean, cov);
    };

    const metricsAccumulators = {
      total_regs: [], total_spend: [], blended_cpa: [], ieccp: [],
      brand_regs: [], nb_regs: [],
    };

    let validCount = 0;
    for (let s = 0; s < nSamples; s++) {
      const sampledParams = {
        brandCpaElast: { a: 0, b: 0 },
        nbCpaElast: { a: 0, b: 0 },
        brandCpcElast: params.brandCpcElast,
        nbCpcElast: params.nbCpcElast,
        brandSeasonality: params.brandSeasonality,
        nbSeasonality: params.nbSeasonality,
        brandYoy: params.brandYoy,
        nbYoy: params.nbYoy,
        brandCcp: params.brandCcp,
        nbCcp: params.nbCcp,
        brandShare: params.brandShare,
      };
      const bAb = sampleElast(params.brandCpaElast);
      const nAb = sampleElast(params.nbCpaElast);
      sampledParams.brandCpaElast = { a: bAb[0], b: bAb[1] };
      sampledParams.nbCpaElast = { a: nAb[0], b: nAb[1] };

      const r = projectMarketSpend(solvedSpend, sampledParams, tp, opts);
      const t = r.totals;

      if (isFiniteNum(t.total_regs) && isFiniteNum(t.total_spend)) {
        metricsAccumulators.total_regs.push(t.total_regs);
        metricsAccumulators.total_spend.push(t.total_spend);
        metricsAccumulators.blended_cpa.push(t.blended_cpa);
        metricsAccumulators.ieccp.push(t.ieccp === null ? 0 : t.ieccp);
        metricsAccumulators.brand_regs.push(t.brand_regs);
        metricsAccumulators.nb_regs.push(t.nb_regs);
        validCount++;
      }
    }

    // Compute quantiles per metric
    const result = {};
    for (const metric of Object.keys(metricsAccumulators)) {
      const samples = metricsAccumulators[metric].slice().sort((a, b) => a - b);
      if (samples.length < 10) {
        const central = samples.length > 0 ? quantile(samples, 0.5) : 0;
        result[metric] = {
          metric, central,
          ci: {
            50: [central * 0.75, central * 1.25],
            70: [central * 0.65, central * 1.40],
            80: [central * 0.58, central * 1.55],
            90: [central * 0.50, central * 1.75],
          },
          mean: central, std: Math.abs(central) * 0.30, n_samples_valid: samples.length,
          warnings: ['INSUFFICIENT_SAMPLES'],
        };
        continue;
      }
      const central = quantile(samples, 0.5);
      const ci50 = [quantile(samples, 0.25), quantile(samples, 0.75)];
      const ci70 = [quantile(samples, 0.15), quantile(samples, 0.85)];
      const ci80 = [quantile(samples, 0.10), quantile(samples, 0.90)];
      const ci90 = [quantile(samples, 0.05), quantile(samples, 0.95)];
      const mean = samples.reduce((a, b) => a + b, 0) / samples.length;
      const variance = samples.reduce((a, b) => a + (b - mean) * (b - mean), 0) / (samples.length - 1);
      const std = Math.sqrt(variance);
      const warnings = [];
      const ci90Width = ci90[1] - ci90[0];
      if (Math.abs(central) > 1e-10 && ci90Width > HIGH_UNCERTAINTY_RATIO * Math.abs(central)) {
        warnings.push('HIGH_UNCERTAINTY');
      }
      result[metric] = {
        metric, central,
        ci: { 50: ci50, 70: ci70, 80: ci80, 90: ci90 },
        mean, std, n_samples_valid: samples.length, warnings,
      };
    }

    // R11.8: VERY_WIDE_CI on MY2 when total_regs 90% CI width > 3× central
    const engineWarnings = [];
    if (tp.type === 'multi_year' && tp.n_years === 2 && result.total_regs) {
      const tr = result.total_regs;
      const ci90W = tr.ci[90][1] - tr.ci[90][0];
      if (Math.abs(tr.central) > 1e-6 && ci90W > VERY_WIDE_CI_RATIO * Math.abs(tr.central)) {
        engineWarnings.push(
          `VERY_WIDE_CI: 2-year 90% CI width (${Math.round(ci90W).toLocaleString()}) exceeds ${VERY_WIDE_CI_RATIO}× central (${Math.round(Math.abs(tr.central)).toLocaleString()}). RECOMMENDATION: use single-year projection only — 2-year uncertainty is too wide to be decision-useful for this market.`
        );
      }
    }

    return { credibleIntervals: result, engineWarnings };
  }

  // ---------- Provenance merger (Bug 3 consumer, 2026-05-01) ----------
  // Reads `markets[scope].provenance_template` from projection-data.json
  // (emitted by export-projection-data.py via mpe_engine.py::build_provenance_template)
  // and substitutes the <period>/<driver>/<target>/<regime_multiplier> placeholders
  // with the scenario-specific values from the current inputs. Attaches to out.provenance.
  // Spec: agent-bus thread dashboard-mockups-handoff post 021_kiro-server.
  function attachProvenance(out, inputs, data) {
    const scope = inputs && inputs.scope;
    const template = data && data.markets && data.markets[scope] && data.markets[scope].provenance_template;
    if (!template || typeof template !== 'object') return out;
    const sub = {
      period: String(inputs.timePeriod != null ? inputs.timePeriod : ''),
      driver: String(inputs.targetMode != null ? inputs.targetMode : ''),
      target: String(inputs.targetValue != null ? inputs.targetValue : ''),
      regime_multiplier: String(inputs.regimeMultiplier != null ? inputs.regimeMultiplier : 1.0),
    };
    out.provenance = {};
    for (const key of Object.keys(template)) {
      const tile = template[key] || {};
      const sqlOrFn = typeof tile.sql_or_fn === 'string'
        ? tile.sql_or_fn
            .replace('<period>', sub.period)
            .replace('<driver>', sub.driver)
            .replace('<target>', sub.target)
            .replace('<regime_multiplier>', sub.regime_multiplier)
        : tile.sql_or_fn;
      out.provenance[key] = {
        ...tile,
        sql_or_fn: sqlOrFn,
      };
    }
    return out;
  }

  // ---------- Main project() entry point (mirrors project()) ----------

  function project(inputs, data) {
    const out = {
      scope: inputs.scope,
      time_period: inputs.timePeriod,
      target_mode: inputs.targetMode,
      target_value: inputs.targetValue,
      outcome: 'OK',
      weeks: [],
      totals: {},
      credible_intervals: {},
      constituent_markets: [],
      parameters_used: {},
      warnings: [],
      fallback_level_summary: 'all_market_specific',
      yoy_growth_applied: {},
      infeasibility_reason: null,
      methodology_version: ENGINE_VERSION,
      generated_at: new Date().toISOString(),
    };

    // Parse period
    let tp;
    try {
      tp = parseTimePeriod(inputs.timePeriod);
    } catch (e) {
      out.outcome = 'INVALID_INPUT';
      out.warnings.push(`TIME_PERIOD_INVALID: ${e.message}`);
      return out;
    }

    // Region
    if (ALL_REGIONS.includes(inputs.scope)) {
      return projectRegion(inputs, tp, out, data);
    }

    // Market
    if (!ALL_MARKETS.includes(inputs.scope)) {
      out.outcome = 'INVALID_INPUT';
      out.warnings.push(`UNKNOWN_SCOPE: ${inputs.scope}`);
      return out;
    }

    const marketData = (data && data.markets) ? data.markets[inputs.scope] : null;
    const readiness = requiredParamsPresent(marketData);
    if (!readiness.ok) {
      out.outcome = 'SETUP_REQUIRED';
      out.warnings.push(`SETUP_REQUIRED: ${inputs.scope} missing parameters: ${JSON.stringify(readiness.missing)}`);
      return out;
    }

    const params = extractParams(marketData);
    const opts = {
      brandUpliftPct: inputs.brandUpliftPct || 0,
      nbUpliftPct: inputs.nbUpliftPct || 0,
    };

    // Validate target mode
    if (!params.supportedModes.includes(inputs.targetMode)) {
      out.outcome = 'INVALID_INPUT';
      out.warnings.push(`UNSUPPORTED_TARGET_MODE: ${inputs.targetMode} not in ${JSON.stringify(params.supportedModes)} for ${inputs.scope}`);
      return out;
    }

    // Solve for target
    //
    // v1.1 Slim routing (Phase 6.1.7, 2026-04-23): for Y-periods, delegate
    // to V1_1_Slim.projectWithLockedYtd which reads regime_fit_state from
    // marketData and runs the full Brand-Anchor + NB-Residual + Locked-YTD
    // flow mirroring the Python engine. Sub-year periods fall back to
    // legacy solvers pending Phase 6.2 port of Brand trajectory for
    // arbitrary week ranges.
    let solved;
    const isYearPeriod = tp.type === 'year';
    const v11Available = typeof global !== 'undefined' && global.V1_1_Slim;
    const useV11 = isYearPeriod && v11Available;

    if (useV11) {
      const year = tp.year;
      const v11 = global.V1_1_Slim.projectWithLockedYtd(
        marketData, year,
        inputs.targetMode, inputs.targetValue,
        { regimeMultiplier: inputs.regimeMultiplier || 1.0 },
      );
      solved = {
        weeks: [],  // per-week array populated in Phase 6.2.x
        totals: {
          brand_regs: v11.totals.brand_regs,
          nb_regs: v11.totals.nb_regs,
          total_regs: v11.totals.total_regs,
          brand_spend: v11.totals.brand_spend,
          nb_spend: v11.totals.nb_spend,
          total_spend: v11.totals.total_spend,
          brand_clicks: 0,
          nb_clicks: 0,
          blended_cpa: v11.totals.blended_cpa,
          ieccp: v11.totals.computed_ieccp,
          yoy_growth_applied: { brand: 0, nb: 0 },
        },
        solvedSpend: v11.totals.total_spend,
      };
      out.warnings.push(...v11.warnings);
      out.contribution_breakdown = v11.contribution_breakdown;
      out.locked_ytd_summary = v11.ytd;
      out.regime_stack = v11.regime_stack;
    } else if (inputs.targetMode === 'spend') {
      solved = projectMarketSpend(inputs.targetValue, params, tp, opts);
      solved.solvedSpend = inputs.targetValue;
    } else if (inputs.targetMode === 'ieccp') {
      solved = solveIeccpTarget(inputs.targetValue, params, tp, opts);
      if (solved.boundWarnings && solved.boundWarnings.length) {
        for (const bw of solved.boundWarnings) {
          out.warnings.push(`SPEND_BOUNDS_APPLIED: ${bw}`);
        }
      }
    } else if (inputs.targetMode === 'regs') {
      solved = solveRegsTarget(inputs.targetValue, params, tp, opts);
      if (solved.infeasibility) {
        out.outcome = 'INFEASIBLE';
        out.infeasibility_reason = solved.infeasibility;
        out.warnings.push(`INFEASIBLE: binding_constraint=${solved.infeasibility.binding_constraint}`);
        return out;
      }
    } else {
      out.outcome = 'INVALID_INPUT';
      out.warnings.push(`UNKNOWN_TARGET_MODE: ${inputs.targetMode}`);
      return out;
    }

    out.weeks = solved.weeks;
    out.totals = solved.totals;
    out.yoy_growth_applied = solved.totals.yoy_growth_applied || {};

    // HIGH_EXTRAPOLATION check using YTD max weekly spend from the data bundle
    const ytd = (marketData.ytd_weekly || []);
    const histMax = ytd.reduce((m, r) => Math.max(m, safeFloat(r.cost, 0)), 0);
    if (histMax > 0) {
      const avgWeekly = solved.totals.total_spend / Math.max(solved.weeks.length, 1);
      if (avgWeekly > HISTORICAL_EXTRAPOLATION_MULTIPLIER * histMax) {
        out.warnings.push(
          `HIGH_EXTRAPOLATION: avg weekly spend $${Math.round(avgWeekly).toLocaleString()} > ${HISTORICAL_EXTRAPOLATION_MULTIPLIER}× YTD max $${Math.round(histMax).toLocaleString()}`
        );
      }
    }

    // Fallback-level summary
    const fbValues = Object.values(params.fallbackLevels).filter(v => v);
    const anyFallback = fbValues.some(v => v === 'regional_fallback' || v === 'southern_hemisphere_hybrid');
    const allFallback = fbValues.length > 0 && fbValues.every(v => v === 'regional_fallback' || v === 'southern_hemisphere_hybrid');
    if (anyFallback) {
      out.warnings.push('DATA_LIMITED');
      out.fallback_level_summary = allFallback ? 'all_regional_fallback' : 'some_regional_fallback';
    } else if (fbValues.some(v => v === 'derived_from_cpa')) {
      out.warnings.push('CPC_DERIVED_FROM_CPA');
    }

    // Credible intervals (R11.8 + R12)
    try {
      const ciOut = computeCredibleIntervals(
        solved.solvedSpend, params, tp, opts,
        inputs.credibilityLevels, SAMPLES_UI, inputs.rngSeed
      );
      out.credible_intervals = ciOut.credibleIntervals;
      out.warnings.push(...ciOut.engineWarnings);
    } catch (e) {
      out.warnings.push(`UNCERTAINTY_UNAVAILABLE: ${e.name}: ${e.message}`);
    }

    // parameters_used summary
    out.parameters_used = {};
    const p = marketData.parameters;
    for (const name of Object.keys(p)) {
      out.parameters_used[name] = {
        fallback_level: p[name].fallback_level,
        lineage: p[name].lineage,
        last_refit_at: p[name].last_refit_at,
      };
    }

    attachProvenance(out, inputs, data);
    return out;
  }

  // ---------- Regional projection (mirrors _project_region) ----------

  function projectRegion(inputs, tp, out, data) {
    const region = inputs.scope;
    const constituents = REGION_CONSTITUENTS[region];
    const perMarket = [];
    let anyFb = false, allFb = true;

    for (const mkt of constituents) {
      const mktInputs = {
        scope: mkt,
        timePeriod: inputs.timePeriod,
        targetMode: 'spend',
        targetValue: inputs.targetValue / constituents.length,
        brandUpliftPct: inputs.brandUpliftPct,
        nbUpliftPct: inputs.nbUpliftPct,
        credibilityLevels: inputs.credibilityLevels,
        rngSeed: inputs.rngSeed,
      };
      const mktOut = project(mktInputs, data);
      perMarket.push(mktOut);
      if (mktOut.fallback_level_summary !== 'all_market_specific') anyFb = true;
      if (mktOut.fallback_level_summary !== 'all_regional_fallback') allFb = false;
    }

    // Aggregate totals
    const tot = { brand_regs: 0, nb_regs: 0, total_regs: 0, brand_spend: 0, nb_spend: 0, total_spend: 0 };
    for (const m of perMarket) {
      tot.brand_regs += m.totals.brand_regs || 0;
      tot.nb_regs += m.totals.nb_regs || 0;
      tot.brand_spend += m.totals.brand_spend || 0;
      tot.nb_spend += m.totals.nb_spend || 0;
    }
    tot.total_regs = tot.brand_regs + tot.nb_regs;
    tot.total_spend = tot.brand_spend + tot.nb_spend;
    tot.blended_cpa = tot.total_regs > 0 ? tot.total_spend / tot.total_regs : 0;

    // Regional ie%CCP: sum-then-divide (R6.2)
    let denom = 0;
    for (const m of perMarket) {
      const md = data.markets[m.scope];
      const params = md ? extractParams(md) : null;
      if (params && params.brandCcp !== null && params.nbCcp !== null) {
        denom += (m.totals.brand_regs || 0) * params.brandCcp;
        denom += (m.totals.nb_regs || 0) * params.nbCcp;
      }
    }
    tot.ieccp = denom > 0 ? (tot.total_spend / denom) * 100.0 : null;

    out.totals = tot;
    out.constituent_markets = perMarket.map(m => ({
      market: m.scope,
      brand_regs: m.totals.brand_regs || 0,
      nb_regs: m.totals.nb_regs || 0,
      total_spend: m.totals.total_spend || 0,
      ieccp: m.totals.ieccp,
      fallback_level_summary: m.fallback_level_summary,
      warnings: m.warnings,
    }));

    if (anyFb && !allFb) out.fallback_level_summary = 'some_regional_fallback';
    else if (allFb) out.fallback_level_summary = 'all_regional_fallback';

    const allWarnings = new Set();
    for (const m of perMarket) m.warnings.forEach(w => allWarnings.add(w));
    out.warnings = Array.from(allWarnings).sort();
    attachProvenance(out, inputs, data);
    return out;
  }

  // ---------- Web Worker wrapper for non-blocking MC ----------

  function projectWithUncertainty(inputs, data) {
    // If Web Workers aren't available (e.g. file:// contexts or old browsers),
    // just run synchronously on the main thread — still responsive at 200 samples.
    // The tradeoff is a ~50-200ms jank; acceptable and better than crashing.
    return new Promise(function (resolve) {
      // Defer to next tick so caller can update UI to "computing..." first
      setTimeout(function () {
        try {
          const out = project(inputs, data);
          resolve(out);
        } catch (e) {
          resolve({
            scope: inputs.scope, outcome: 'ERROR',
            warnings: [`ENGINE_ERROR: ${e.name}: ${e.message}`],
            credible_intervals: {}, totals: {}, weeks: [],
          });
        }
      }, 0);
    });
  }

  // ---------- Public API ----------

  const MPE = {
    ENGINE_VERSION,
    ALL_MARKETS,
    ALL_REGIONS,
    REGION_CONSTITUENTS,
    project,
    projectWithUncertainty,
    parseTimePeriod,
    applyCpaElasticity,
    applyCpcElasticity,
    projectMarketSpend,
    extractParams,
    // Exposed for parity testing
    _internals: {
      solveIeccpTarget, solveRegsTarget, computeCredibleIntervals,
      mulberry32, normalSample, multivariateNormal2D, quantile,
      HIGH_UNCERTAINTY_RATIO, VERY_WIDE_CI_RATIO, SAMPLES_UI,
    },
  };

  if (typeof module !== 'undefined' && module.exports) {
    module.exports = MPE;
  } else {
    global.MPE = MPE;
  }
})(typeof window !== 'undefined' ? window : globalThis);
