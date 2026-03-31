"""Property tests for BayesianCore (Properties 1, 2, 3).

**Validates: Requirements 1.1, 1.2, 1.4, 1.5, 2.1, 2.2, 2.3**
"""

import sys
import os
import math

sys.path.insert(0, os.path.expanduser('~/shared/tools'))
sys.path.insert(0, os.path.expanduser('~/shared/tools/data'))

from hypothesis import given, settings, assume, HealthCheck
from hypothesis import strategies as st

from prediction.core import BayesianCore
from prediction.types import PriorState

core = BayesianCore()

# Strategy: list of positive floats as historical data dicts
positive_floats = st.floats(min_value=0.1, max_value=1e6, allow_nan=False, allow_infinity=False)


def make_historical(values, metric='regs'):
    return [{metric: v} for v in values]


# ── Property 1: Prior builds from data ──

@settings(max_examples=80, suppress_health_check=[HealthCheck.too_slow])
@given(values=st.lists(positive_floats, min_size=3, max_size=100))
def test_prior_mean_equals_arithmetic_mean(values):
    """**Validates: Requirements 1.1**
    For 3+ values, prior mean must equal arithmetic mean."""
    hist = make_historical(values)
    prior = core.build_prior(hist, 'regs')
    expected_mean = sum(values) / len(values)
    assert abs(prior.mean - expected_mean) < 1e-6, (
        f"Prior mean {prior.mean} != expected {expected_mean}"
    )


@settings(max_examples=80, suppress_health_check=[HealthCheck.too_slow])
@given(values=st.lists(positive_floats, min_size=3, max_size=100))
def test_prior_trend_equals_ols_slope(values):
    """**Validates: Requirements 1.4**
    Trend slope must equal OLS regression slope over index."""
    hist = make_historical(values)
    prior = core.build_prior(hist, 'regs')
    n = len(values)
    mean = sum(values) / n
    indices = list(range(n))
    x_mean = sum(indices) / n
    ss_xy = sum((i - x_mean) * (v - mean) for i, v in zip(indices, values))
    ss_xx = sum((i - x_mean) ** 2 for i in indices)
    expected_slope = ss_xy / ss_xx if ss_xx > 0 else 0.0
    assert abs(prior.trend_slope - expected_slope) < 1e-6


@settings(max_examples=80, suppress_health_check=[HealthCheck.too_slow])
@given(values=st.lists(positive_floats, min_size=3, max_size=100))
def test_prior_volatility_equals_rmse(values):
    """**Validates: Requirements 1.5**
    Volatility must equal RMSE of trend-fit residuals."""
    hist = make_historical(values)
    prior = core.build_prior(hist, 'regs')
    n = len(values)
    mean = sum(values) / n
    indices = list(range(n))
    x_mean = sum(indices) / n
    ss_xy = sum((i - x_mean) * (v - mean) for i, v in zip(indices, values))
    ss_xx = sum((i - x_mean) ** 2 for i in indices)
    slope = ss_xy / ss_xx if ss_xx > 0 else 0.0
    predicted = [mean + slope * (i - x_mean) for i in indices]
    residuals = [v - p for v, p in zip(values, predicted)]
    expected_vol = (sum(r ** 2 for r in residuals) / max(1, n - 2)) ** 0.5
    assert abs(prior.volatility - expected_vol) < 1e-6


@settings(max_examples=50, suppress_health_check=[HealthCheck.too_slow])
@given(values=st.lists(positive_floats, min_size=0, max_size=2))
def test_prior_uninformative_for_few_points(values):
    """**Validates: Requirements 1.2**
    Fewer than 3 data points → uninformative prior (variance >= 1e6)."""
    hist = make_historical(values)
    prior = core.build_prior(hist, 'regs')
    assert prior.variance >= 1e6


# ── Property 2: Posterior convergence ──

def make_prior(mean, variance, n_obs, trend=0.0, vol=10.0):
    return PriorState(
        mean=mean, variance=variance, n_observations=n_obs,
        trend_slope=trend, trend_confidence=0.5,
        seasonality={}, volatility=vol,
    )


@settings(max_examples=80, suppress_health_check=[HealthCheck.too_slow])
@given(
    prior_mean=st.floats(min_value=1, max_value=1000, allow_nan=False, allow_infinity=False),
    prior_var=st.floats(min_value=1, max_value=1e6, allow_nan=False, allow_infinity=False),
    prior_n=st.integers(min_value=3, max_value=200),
    evidence=st.lists(
        st.floats(min_value=0.1, max_value=1e4, allow_nan=False, allow_infinity=False),
        min_size=1, max_size=20,
    ),
)
def test_posterior_mean_between_prior_and_evidence(prior_mean, prior_var, prior_n, evidence):
    """**Validates: Requirements 2.1**
    Posterior mean lies between prior mean and evidence mean."""
    prior = make_prior(prior_mean, prior_var, prior_n)
    evidence_dicts = [{'value': v} for v in evidence]
    posterior = core.update_posterior(prior, evidence_dicts)
    ev_mean = sum(evidence) / len(evidence)
    lo = min(prior_mean, ev_mean)
    hi = max(prior_mean, ev_mean)
    assert lo - 1e-6 <= posterior.mean <= hi + 1e-6, (
        f"Posterior mean {posterior.mean} not between prior {prior_mean} and evidence {ev_mean}"
    )


@settings(max_examples=80, suppress_health_check=[HealthCheck.too_slow])
@given(
    prior_mean=st.floats(min_value=50, max_value=500, allow_nan=False, allow_infinity=False),
    prior_var=st.floats(min_value=1000, max_value=1e6, allow_nan=False, allow_infinity=False),
    prior_n=st.integers(min_value=20, max_value=200),
    evidence=st.lists(
        st.floats(min_value=50, max_value=500, allow_nan=False, allow_infinity=False),
        min_size=2, max_size=20,
    ),
)
def test_posterior_variance_decreases(prior_mean, prior_var, prior_n, evidence):
    """**Validates: Requirements 2.2**
    Posterior variance <= prior variance when prior has many observations
    and high variance (the normal Bayesian regime where more data reduces uncertainty).
    With a strong prior (large n, large variance), adding evidence should
    not increase variance."""
    ev_mean = sum(evidence) / len(evidence)
    ev_var = sum((v - ev_mean) ** 2 for v in evidence) / len(evidence) if len(evidence) > 1 else 0
    # Ensure evidence variance is much less than prior variance
    # and evidence mean is not wildly different from prior mean
    assume(ev_var < prior_var * 0.5)
    assume(abs(ev_mean - prior_mean) < (prior_var ** 0.5))
    prior = make_prior(prior_mean, prior_var, prior_n)
    evidence_dicts = [{'value': v} for v in evidence]
    posterior = core.update_posterior(prior, evidence_dicts)
    assert posterior.variance <= prior_var + 1e-6, (
        f"Posterior variance {posterior.variance} > prior variance {prior_var}"
    )


# ── Property 3: Calibration factor scales credible intervals ──

@settings(max_examples=80, suppress_health_check=[HealthCheck.too_slow])
@given(
    prior_mean=st.floats(min_value=1, max_value=1000, allow_nan=False, allow_infinity=False),
    prior_var=st.floats(min_value=10, max_value=1e5, allow_nan=False, allow_infinity=False),
    prior_n=st.integers(min_value=5, max_value=100),
    vol=st.floats(min_value=1, max_value=100, allow_nan=False, allow_infinity=False),
    evidence=st.lists(
        st.floats(min_value=0.1, max_value=1e4, allow_nan=False, allow_infinity=False),
        min_size=1, max_size=10,
    ),
    k1=st.floats(min_value=0.5, max_value=1.5, allow_nan=False, allow_infinity=False),
    k2=st.floats(min_value=0.5, max_value=2.0, allow_nan=False, allow_infinity=False),
)
def test_calibration_factor_scales_intervals(prior_mean, prior_var, prior_n, vol, evidence, k1, k2):
    """**Validates: Requirements 2.3**
    Larger calibration factor → wider or equal credible intervals."""
    assume(k2 > k1)
    prior = make_prior(prior_mean, prior_var, prior_n, vol=vol)
    ev = [{'value': v} for v in evidence]
    post1 = core.update_posterior(prior, ev, calibration_factor=k1)
    post2 = core.update_posterior(prior, ev, calibration_factor=k2)
    width1 = post1.credible_interval_70[1] - post1.credible_interval_70[0]
    width2 = post2.credible_interval_70[1] - post2.credible_interval_70[0]
    assert width2 >= width1 - 1e-6, (
        f"Width with k2={k2} ({width2}) < width with k1={k1} ({width1})"
    )
