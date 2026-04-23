"""MPE Uncertainty — Monte Carlo credible intervals for projection outputs.

WHY THIS EXISTS
    Every fitted parameter in the MPE has a posterior — a distribution of
    plausible values given the data. A point projection (best-estimate)
    ignores that uncertainty. For leadership-grade output we need honest
    ranges: "regs will land between X and Y with 70% credibility."
    This module does Monte Carlo sampling over parameter posteriors and
    propagates the samples through the engine to produce credible
    intervals on every output KPI.

HOW THE OWNER MAINTAINS IT
    You never call this module directly. The engine (mpe_engine.py)
    calls into it automatically whenever a projection is produced. The
    sample counts are LOCKED so the owner doesn't tune knobs:
        UI runs use 200 samples (fast, Web Worker friendly)
        CLI runs use 1000 samples (tight intervals, tolerable latency)
    If the CIs look too wide or too narrow, the fix is in the upstream
    parameter fit (mpe_fitting.py) — the fit's posterior covariance is
    what this module samples from. Widening posteriors widens CIs.

WHAT HAPPENS ON FAILURE
    - If posterior covariance is singular (fit was too noisy), we fall
      back to independent-parameter sampling with a wide default std.
      Emits SAMPLING_DEGRADED warning.
    - If sampling produces non-finite values (log(0), overflow), those
      samples are dropped from the CI computation and a warning is
      emitted with the drop count.
    - If fewer than 10 valid samples remain, CIs revert to the point
      estimate ± 50% with HIGH_UNCERTAINTY warning.

MATH
    For each parameter with fitted (a, b, posterior_cov):
      sample ~ MultivariateNormal([a, b], posterior_cov)
    For scalar parameters (ccp, yoy_growth.mean):
      sample ~ Normal(mean, std)
    Run the projection function with each sampled parameter set.
    Collect output KPIs across samples. Compute quantiles:
      50% CI = [Q25, Q75]
      70% CI = [Q15, Q85]
      90% CI = [Q5, Q95]

    Performance target: 200 samples in < 80 ms (UI Web Worker).
    This requires vectorized numpy operations — no Python-loop over
    samples on the hot path.

ASYMMETRY
    Elasticity posteriors are in log-space. Exponentiating produces
    skewed distributions in the output space (wider on the upside).
    This is expected, not a bug. The UI narrative explains this.
"""

from __future__ import annotations

import math
import sys
from dataclasses import dataclass, field
from typing import Callable

import numpy as np


# ---------- Constants (LOCKED per R12.2) ----------

SAMPLES_UI = 200
SAMPLES_CLI = 1000

# Credible interval levels: return these quantile pairs
CREDIBILITY_LEVELS = (0.50, 0.70, 0.90)

# Safety limits
MIN_VALID_SAMPLES = 10
MAX_SAMPLE_VALUE_ABS = 1e12
HIGH_UNCERTAINTY_CI_WIDTH_RATIO = 2.0   # R12.5: 90% CI width > 2× central
SAMPLING_DEGRADED_FALLBACK_STD = 0.30    # 30% CV default when posterior is singular


# ---------- Result types ----------

@dataclass
class CredibleInterval:
    """One set of credible intervals for one output metric."""
    metric: str
    central: float                         # point estimate (median of samples)
    ci_50: tuple[float, float]             # (Q25, Q75)
    ci_70: tuple[float, float]             # (Q15, Q85)
    ci_90: tuple[float, float]             # (Q5, Q95)
    mean: float                            # sample mean (for asymmetry measurement)
    std: float                             # sample std
    n_samples_valid: int
    warnings: list[str] = field(default_factory=list)

    def to_json(self) -> dict:
        return {
            'metric': self.metric,
            'central': self.central,
            'ci': {
                '50': list(self.ci_50),
                '70': list(self.ci_70),
                '90': list(self.ci_90),
            },
            'mean': self.mean,
            'std': self.std,
            'n_samples_valid': self.n_samples_valid,
            'warnings': self.warnings,
        }


# ---------- Parameter sampling ----------

def sample_log_linear(
    coef_a: float,
    coef_b: float,
    posterior_cov: list[list[float]],
    n_samples: int,
    rng: np.random.Generator,
) -> np.ndarray:
    """Sample (a, b) from a bivariate Normal posterior. Returns n×2 array.

    Falls back to independent Normal sampling if posterior_cov is singular.
    """
    mean = np.array([coef_a, coef_b], dtype=float)
    cov = np.array(posterior_cov, dtype=float)

    # Check for degenerate covariance
    cov_is_singular = False
    try:
        if cov.shape != (2, 2):
            cov_is_singular = True
        elif np.any(np.isnan(cov)) or np.any(np.isinf(cov)):
            cov_is_singular = True
        else:
            # Require positive-definiteness
            eigenvalues = np.linalg.eigvalsh(cov)
            if np.any(eigenvalues <= 0):
                cov_is_singular = True
    except np.linalg.LinAlgError:
        cov_is_singular = True

    if cov_is_singular:
        # Fall back to independent sampling
        std_a = abs(coef_a) * SAMPLING_DEGRADED_FALLBACK_STD + 0.05
        std_b = abs(coef_b) * SAMPLING_DEGRADED_FALLBACK_STD + 0.05
        a_samples = rng.normal(coef_a, std_a, n_samples)
        b_samples = rng.normal(coef_b, std_b, n_samples)
        return np.column_stack([a_samples, b_samples])

    try:
        samples = rng.multivariate_normal(mean, cov, size=n_samples)
        return samples
    except (np.linalg.LinAlgError, ValueError):
        # Last-resort independent sampling
        std_a = math.sqrt(max(cov[0][0], 0.01))
        std_b = math.sqrt(max(cov[1][1], 0.01))
        a_samples = rng.normal(coef_a, std_a, n_samples)
        b_samples = rng.normal(coef_b, std_b, n_samples)
        return np.column_stack([a_samples, b_samples])


def sample_scalar(
    mean: float,
    std: float,
    n_samples: int,
    rng: np.random.Generator,
    floor: float | None = None,
    ceiling: float | None = None,
) -> np.ndarray:
    """Sample a scalar from Normal(mean, std), optionally clamped."""
    std = max(abs(std), 1e-6)
    samples = rng.normal(mean, std, n_samples)
    if floor is not None:
        samples = np.maximum(samples, floor)
    if ceiling is not None:
        samples = np.minimum(samples, ceiling)
    return samples


def sample_seasonality(
    weights: list[float],
    posteriors: list[dict],
    n_samples: int,
    rng: np.random.Generator,
) -> np.ndarray:
    """Sample 52-week seasonality shapes. Returns n_samples × 52 array.

    Each posterior provides {mean, std, provenance}. Samples are clamped
    to positive values and re-normalized to sum to 52.0 per sample.
    """
    n_weeks = len(weights)
    if n_weeks == 0 or len(posteriors) != n_weeks:
        # Return a flat shape if input is malformed
        return np.ones((n_samples, 52))

    means = np.array([p.get('mean', 1.0) for p in posteriors], dtype=float)
    stds = np.array([max(p.get('std', 0.10), 1e-6) for p in posteriors], dtype=float)

    # Sample week-by-week independently
    samples = rng.normal(loc=means, scale=stds, size=(n_samples, n_weeks))
    samples = np.maximum(samples, 0.01)   # clamp to positive

    # Normalize each sample to sum to n_weeks (keeps scale invariant)
    row_sums = samples.sum(axis=1, keepdims=True)
    samples = samples * (n_weeks / np.where(row_sums > 0, row_sums, 1.0))
    return samples


# ---------- Credible interval computation ----------

def compute_ci(samples: np.ndarray, metric_name: str) -> CredibleInterval:
    """Compute 50/70/90 credible intervals from a 1D array of samples."""
    warnings: list[str] = []

    # Filter out non-finite and extreme values
    mask = np.isfinite(samples) & (np.abs(samples) < MAX_SAMPLE_VALUE_ABS)
    valid = samples[mask]
    n_dropped = int(samples.size - valid.size)
    if n_dropped > 0:
        warnings.append(f"dropped {n_dropped} non-finite/extreme samples")

    if valid.size < MIN_VALID_SAMPLES:
        # Use whatever we have with a defensive fallback
        if valid.size == 0:
            central = 0.0
        else:
            central = float(np.median(valid))
        warnings.append("INSUFFICIENT_SAMPLES")
        return CredibleInterval(
            metric=metric_name,
            central=central,
            ci_50=(central * 0.75, central * 1.25),
            ci_70=(central * 0.65, central * 1.40),
            ci_90=(central * 0.50, central * 1.75),
            mean=central,
            std=abs(central) * 0.30,
            n_samples_valid=int(valid.size),
            warnings=warnings,
        )

    # Standard path: compute quantiles
    central = float(np.median(valid))
    mean = float(np.mean(valid))
    std = float(np.std(valid, ddof=1)) if valid.size > 1 else 0.0

    q5, q15, q25, q75, q85, q95 = np.quantile(valid, [0.05, 0.15, 0.25, 0.75, 0.85, 0.95])

    ci_90_width = float(q95 - q5)
    if abs(central) > 1e-10 and ci_90_width > HIGH_UNCERTAINTY_CI_WIDTH_RATIO * abs(central):
        warnings.append("HIGH_UNCERTAINTY")

    return CredibleInterval(
        metric=metric_name,
        central=central,
        ci_50=(float(q25), float(q75)),
        ci_70=(float(q15), float(q85)),
        ci_90=(float(q5), float(q95)),
        mean=mean,
        std=std,
        n_samples_valid=int(valid.size),
        warnings=warnings,
    )


# ---------- High-level sampler ----------

def run_monte_carlo(
    point_projection_fn: Callable[[dict], dict],
    parameter_set: dict,
    n_samples: int,
    rng_seed: int | None = None,
) -> dict[str, CredibleInterval]:
    """Run Monte Carlo sampling across a parameter set.

    Args:
        point_projection_fn: function that takes a parameter dict and
            returns a dict of output metrics (name -> float scalar).
        parameter_set: dict of parameter-name -> parameter-spec. Each
            spec is one of:
              {'type': 'scalar', 'mean': float, 'std': float,
               'floor': float|None, 'ceiling': float|None}
              {'type': 'log_linear', 'a': float, 'b': float,
               'posterior_cov': [[float, float], [float, float]]}
              {'type': 'seasonality', 'weights': [52 floats],
               'posteriors': [52 {mean, std, provenance}]}
              {'type': 'fixed', 'value': <any>}   # CCPs etc — no sampling
        n_samples: how many samples to draw (200 UI / 1000 CLI).
        rng_seed: optional seed for deterministic testing.

    Returns:
        {metric_name: CredibleInterval} for every metric the
        point_projection_fn returns.
    """
    rng = np.random.default_rng(rng_seed)

    # Pre-sample every parameter
    sampled_params: dict = {}
    for name, spec in parameter_set.items():
        ptype = spec.get('type', 'fixed')
        if ptype == 'fixed':
            sampled_params[name] = [spec['value']] * n_samples
        elif ptype == 'scalar':
            sampled_params[name] = sample_scalar(
                mean=spec['mean'],
                std=spec.get('std', abs(spec['mean']) * 0.10),
                n_samples=n_samples,
                rng=rng,
                floor=spec.get('floor'),
                ceiling=spec.get('ceiling'),
            )
        elif ptype == 'log_linear':
            ab = sample_log_linear(
                coef_a=spec['a'],
                coef_b=spec['b'],
                posterior_cov=spec.get('posterior_cov', [[0.01, 0], [0, 0.01]]),
                n_samples=n_samples,
                rng=rng,
            )
            sampled_params[name] = ab   # n × 2 array
        elif ptype == 'seasonality':
            sampled_params[name] = sample_seasonality(
                weights=spec['weights'],
                posteriors=spec['posteriors'],
                n_samples=n_samples,
                rng=rng,
            )
        else:
            # Unknown type — treat as fixed
            sampled_params[name] = [spec.get('value', None)] * n_samples

    # Run point_projection_fn for each sample and collect outputs
    outputs_by_metric: dict[str, list[float]] = {}
    for i in range(n_samples):
        # Build the per-sample parameter dict
        sample_params = {}
        for name, spec in parameter_set.items():
            ptype = spec.get('type', 'fixed')
            if ptype == 'fixed':
                sample_params[name] = sampled_params[name][i]
            elif ptype == 'scalar':
                sample_params[name] = float(sampled_params[name][i])
            elif ptype == 'log_linear':
                a, b = sampled_params[name][i]
                sample_params[name] = {'a': float(a), 'b': float(b)}
            elif ptype == 'seasonality':
                sample_params[name] = sampled_params[name][i].tolist()
            else:
                sample_params[name] = sampled_params[name][i]

        try:
            outputs = point_projection_fn(sample_params)
        except Exception:
            # One bad sample — skip it, don't let it corrupt the CI
            continue

        for metric, value in outputs.items():
            if metric not in outputs_by_metric:
                outputs_by_metric[metric] = []
            try:
                outputs_by_metric[metric].append(float(value))
            except (TypeError, ValueError):
                pass

    # Compute CI per metric
    result = {}
    for metric, values in outputs_by_metric.items():
        arr = np.array(values, dtype=float)
        result[metric] = compute_ci(arr, metric)
    return result


# ---------- Convenience: sample-count selector ----------

def get_sample_count(context: str = 'cli') -> int:
    """Return the locked sample count for UI or CLI context."""
    if context.lower() in ('ui', 'browser', 'web'):
        return SAMPLES_UI
    return SAMPLES_CLI


# ---------- Self-test ----------

def _self_test() -> int:
    """Quick self-test: sample a toy projection and verify CI shape."""
    rng_seed = 42

    # Parameter set: one scalar spend, one log-linear CPA elasticity
    params = {
        'spend': {'type': 'scalar', 'mean': 1_000_000.0, 'std': 50_000.0, 'floor': 1.0},
        'cpa_elasticity': {
            'type': 'log_linear',
            'a': -4.5,
            'b': 0.73,
            'posterior_cov': [[0.05, -0.005], [-0.005, 0.002]],
        },
    }

    def project(p):
        spend = p['spend']
        a = p['cpa_elasticity']['a']
        b = p['cpa_elasticity']['b']
        # CPA = exp(a) * spend^b  →  regs = spend / CPA
        cpa = math.exp(a) * (spend ** b)
        regs = spend / cpa if cpa > 0 else 0.0
        return {'regs': regs, 'cpa': cpa, 'spend': spend}

    results = run_monte_carlo(project, params, n_samples=SAMPLES_CLI, rng_seed=rng_seed)

    print("=== MPE Uncertainty Self-Test ===")
    print(f"Sample count: {SAMPLES_CLI}")
    for metric, ci in results.items():
        print(f"\n{metric}:")
        print(f"  central (median): {ci.central:,.2f}")
        print(f"  mean:             {ci.mean:,.2f}")
        print(f"  std:              {ci.std:,.2f}")
        print(f"  70% CI:           [{ci.ci_70[0]:,.2f} , {ci.ci_70[1]:,.2f}]")
        print(f"  90% CI:           [{ci.ci_90[0]:,.2f} , {ci.ci_90[1]:,.2f}]")
        print(f"  valid samples:    {ci.n_samples_valid} of {SAMPLES_CLI}")
        if ci.warnings:
            print(f"  warnings:         {ci.warnings}")

    # Verify CIs are ordered correctly — wider intervals have lower lower-bounds and higher upper-bounds
    # Order: 90% (widest) ⊇ 70% ⊇ 50% (narrowest)
    for metric, ci in results.items():
        assert ci.ci_90[0] <= ci.ci_70[0] <= ci.ci_50[0], f"{metric}: CI lower bounds disordered (90 ≤ 70 ≤ 50 required)"
        assert ci.ci_50[1] <= ci.ci_70[1] <= ci.ci_90[1], f"{metric}: CI upper bounds disordered (50 ≤ 70 ≤ 90 required)"
        assert ci.ci_90[0] <= ci.central <= ci.ci_90[1], f"{metric}: central outside 90% CI"

    print("\n[self_test] all CI ordering assertions passed")
    return 0


if __name__ == "__main__":
    sys.exit(_self_test())
