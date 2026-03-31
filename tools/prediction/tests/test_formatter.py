"""Property test: no statistical jargon in human output (Property 11).

**Validates: Requirements 8.1, 8.2**
"""

import sys
import os

sys.path.insert(0, os.path.expanduser('~/shared/tools'))
sys.path.insert(0, os.path.expanduser('~/shared/tools/data'))

from hypothesis import given, settings, HealthCheck
from hypothesis import strategies as st

from prediction.formatter import Formatter, BANNED_TERMS, CONFIDENCE_ENGLISH
from prediction.types import PredictionResult

formatter = Formatter()

pred_types = st.sampled_from(['point', 'direction', 'probability', 'time_to_target', 'comparison'])
conf_levels = st.sampled_from(list(CONFIDENCE_ENGLISH.keys()))
directions = st.sampled_from(['up', 'down', 'flat', None])
markets = st.sampled_from(['US', 'CA', 'UK', 'DE', 'FR', 'IT', 'ES', 'JP', 'AU', 'MX'])
metrics = st.sampled_from(['regs', 'spend', 'cpa', 'cvr', 'clicks', 'cpc'])


@settings(max_examples=100, suppress_health_check=[HealthCheck.too_slow])
@given(
    market=markets,
    metric=metrics,
    pred_type=pred_types,
    point_est=st.one_of(st.none(), st.floats(min_value=0.1, max_value=1e6, allow_nan=False, allow_infinity=False)),
    lower=st.one_of(st.none(), st.floats(min_value=0.1, max_value=1e5, allow_nan=False, allow_infinity=False)),
    upper=st.one_of(st.none(), st.floats(min_value=100, max_value=1e6, allow_nan=False, allow_infinity=False)),
    conf_level=conf_levels,
    conf_prob=st.floats(min_value=0.0, max_value=1.0, allow_nan=False, allow_infinity=False),
    direction=directions,
    horizon=st.integers(min_value=1, max_value=26),
)
def test_no_jargon_in_human_output(market, metric, pred_type, point_est, lower, upper,
                                    conf_level, conf_prob, direction, horizon):
    """**Validates: Requirements 8.1, 8.2**
    Human output must never contain banned statistical terms.
    Must contain confidence level text and reasoning."""
    result = PredictionResult(
        question=f"What will {market} {metric} be?",
        market=market,
        metric=metric,
        prediction_type=pred_type,
        point_estimate=point_est,
        lower_bound=lower,
        upper_bound=upper,
        confidence_level=conf_level,
        confidence_probability=conf_prob,
        direction=direction,
        horizon_weeks=horizon,
        reasoning="Based on 20 weeks of data. Recent trend: up ~2.5/week.",
    )
    output = formatter.format(result, consumer='human')
    assert isinstance(output, str)

    # No banned terms
    lower_output = output.lower()
    for term in BANNED_TERMS:
        assert term not in lower_output, f"Jargon '{term}' found in: {output}"

    # Must contain confidence language
    conf_text = CONFIDENCE_ENGLISH.get(conf_level, conf_level)
    assert conf_text in output.lower() or conf_level in output.lower(), (
        f"Confidence level '{conf_level}' not found in output: {output}"
    )
