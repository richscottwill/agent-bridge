"""Tests for mpe_uncertainty.py — Monte Carlo sampling and credible intervals.

Covers R12.1-R12.10 (credible interval math, sample count lock, HIGH_UNCERTAINTY trigger,
singular covariance fallback, graceful degradation).
"""

from __future__ import annotations

import math
import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.expanduser('~/shared/tools'))

from prediction.mpe_uncertainty import (
    compute_ci,
    sample_log_linear,
    sample_scalar,
    sample_seasonality,
    run_monte_carlo,
    get_sample_count,
    SAMPLES_UI,
    SAMPLES_CLI,
    HIGH_UNCERTAINTY_CI_WIDTH_RATIO,
    MIN_VALID_SAMPLES,
    CredibleInterval,
)


# ---------- Sample count lock ----------

def test_sample_count_locked_values():
    """UI=200, CLI=1000 per R12.2 — these must not drift."""
    assert SAMPLES_UI == 200
    assert SAMPLES_CLI == 1000


def test_get_sample_count_routing():
    assert get_sample_count('ui') == SAMPLES_UI
    assert get_sample_count('browser') == SAMPLES_UI
    assert get_sample_count('cli') == SAMPLES_CLI
    assert get_sample_count('anything_else') == SAMPLES_CLI   # default


# ---------- CI ordering (R12.3) ----------

def test_ci_ordering_90_contains_70_contains_50():
    """90% CI ⊇ 70% CI ⊇ 50% CI always."""
    rng = np.random.default_rng(42)
    samples = rng.normal(100.0, 20.0, 1000)
    ci = compute_ci(samples, 'test_metric')
    assert ci.ci_90[0] <= ci.ci_70[0] <= ci.ci_50[0]
    assert ci.ci_50[1] <= ci.ci_70[1] <= ci.ci_90[1]
    assert ci.ci_90[0] <= ci.central <= ci.ci_90[1]


def test_ci_central_is_median():
    """Central estimate = median of valid samples."""
    samples = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0])
    ci = compute_ci(samples, 'test')
    assert math.isclose(ci.central, 6.5, rel_tol=0.01)


# ---------- HIGH_UNCERTAINTY trigger (R12.5) ----------

def test_high_uncertainty_fires_when_ci_width_exceeds_2x_central():
    """90% CI width > 2× |central| → HIGH_UNCERTAINTY warning."""
    rng = np.random.default_rng(7)
    # Normal(mean=100, std=200) — 90% CI ≈ [-229, 429], width ≈ 658, 658 / 100 = 6.6× >> 2×
    samples = rng.normal(100.0, 200.0, 1000)
    ci = compute_ci(samples, 'noisy')
    assert 'HIGH_UNCERTAINTY' in ci.warnings


def test_high_uncertainty_quiet_when_ci_narrow():
    """Tight distribution should not trigger HIGH_UNCERTAINTY."""
    rng = np.random.default_rng(8)
    samples = rng.normal(100.0, 5.0, 1000)   # std 5 → 90% CI width ≈ 16.4, <<< 2×100
    ci = compute_ci(samples, 'tight')
    assert 'HIGH_UNCERTAINTY' not in ci.warnings


# ---------- Singular covariance fallback ----------

def test_log_linear_sampling_with_valid_cov():
    rng = np.random.default_rng(10)
    samples = sample_log_linear(
        coef_a=-4.0, coef_b=0.8,
        posterior_cov=[[0.01, 0.0], [0.0, 0.005]],
        n_samples=500, rng=rng,
    )
    assert samples.shape == (500, 2)
    assert math.isclose(samples[:, 0].mean(), -4.0, abs_tol=0.1)
    assert math.isclose(samples[:, 1].mean(), 0.8, abs_tol=0.05)


def test_log_linear_sampling_falls_back_on_singular_cov():
    """Singular (zero) cov triggers independent-Normal fallback without crashing."""
    rng = np.random.default_rng(11)
    samples = sample_log_linear(
        coef_a=-4.0, coef_b=0.8,
        posterior_cov=[[0.0, 0.0], [0.0, 0.0]],   # singular
        n_samples=500, rng=rng,
    )
    assert samples.shape == (500, 2)
    # Fallback uses 30% CV — should produce spread around the means
    assert samples[:, 0].std() > 0
    assert samples[:, 1].std() > 0


def test_log_linear_sampling_falls_back_on_malformed_cov():
    """NaN/Inf in cov → fallback."""
    rng = np.random.default_rng(12)
    samples = sample_log_linear(
        coef_a=-4.0, coef_b=0.8,
        posterior_cov=[[float('nan'), 0.0], [0.0, 0.005]],
        n_samples=300, rng=rng,
    )
    assert samples.shape == (300, 2)


# ---------- Seasonality sampling ----------

def test_seasonality_samples_normalize_to_52():
    """Each sampled seasonality shape should sum to 52."""
    rng = np.random.default_rng(13)
    weights = [1.0] * 52
    posteriors = [{'mean': 1.0, 'std': 0.15, 'provenance': 'fit'}] * 52
    samples = sample_seasonality(weights, posteriors, 100, rng)
    for i in range(100):
        assert math.isclose(samples[i].sum(), 52.0, rel_tol=0.001)


def test_seasonality_samples_stay_positive():
    """Sampled weights should be clamped to positive."""
    rng = np.random.default_rng(14)
    weights = [0.05] * 52   # very small
    posteriors = [{'mean': 0.05, 'std': 0.5, 'provenance': 'fit'}] * 52
    samples = sample_seasonality(weights, posteriors, 50, rng)
    assert (samples > 0).all()


# ---------- End-to-end MC ----------

def test_run_monte_carlo_produces_ci_for_every_output():
    """MC must produce a CredibleInterval for each output metric."""
    def project(p):
        return {
            'regs': p['spend'] / 100.0,
            'cpa': 100.0,
        }

    params = {
        'spend': {'type': 'scalar', 'mean': 10000.0, 'std': 500.0, 'floor': 1.0},
    }
    result = run_monte_carlo(project, params, n_samples=200, rng_seed=99)
    assert 'regs' in result
    assert 'cpa' in result
    assert isinstance(result['regs'], CredibleInterval)
    assert result['regs'].n_samples_valid >= MIN_VALID_SAMPLES


def test_deterministic_with_seed():
    """Same seed → same CI values."""
    def project(p):
        return {'y': p['x'] ** 2}

    params = {'x': {'type': 'scalar', 'mean': 5.0, 'std': 1.0}}
    r1 = run_monte_carlo(project, params, n_samples=200, rng_seed=42)
    r2 = run_monte_carlo(project, params, n_samples=200, rng_seed=42)
    assert r1['y'].central == r2['y'].central
    assert r1['y'].ci_90 == r2['y'].ci_90


# ---------- Graceful degradation (R12.4, R12.8) ----------

def test_compute_ci_with_insufficient_samples():
    """Fewer than MIN_VALID_SAMPLES → INSUFFICIENT_SAMPLES warning + defensive CI."""
    samples = np.array([100.0, 105.0, 98.0])   # only 3 samples
    ci = compute_ci(samples, 'sparse')
    assert 'INSUFFICIENT_SAMPLES' in ci.warnings


def test_compute_ci_filters_non_finite():
    """NaN/Inf samples should be filtered without crash."""
    samples = np.array([100.0, float('nan'), 105.0, float('inf'), 110.0] + [95.0] * 20)
    ci = compute_ci(samples, 'mixed')
    # Should have a warning about dropped samples and still produce a valid CI
    assert any('dropped' in w for w in ci.warnings)
    assert math.isfinite(ci.central)
