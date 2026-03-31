"""Property tests for question parser (Properties 4, 5).

**Validates: Requirements 3.1, 3.2, 3.3, 3.4, 3.5**
"""

import sys
import os

sys.path.insert(0, os.path.expanduser('~/shared/tools'))
sys.path.insert(0, os.path.expanduser('~/shared/tools/data'))

from hypothesis import given, settings, HealthCheck
from hypothesis import strategies as st

from prediction.parser import parse_question, MARKET_CODES, METRIC_KEYWORDS

VALID_TYPES = {'point', 'direction', 'probability', 'time_to_target', 'comparison'}


# ── Property 4: Question parsing determinism ──

@settings(max_examples=100, suppress_health_check=[HealthCheck.too_slow])
@given(
    question=st.text(min_size=0, max_size=200),
    ctx_market=st.one_of(st.none(), st.sampled_from(MARKET_CODES)),
    ctx_metric=st.one_of(st.none(), st.sampled_from(list(METRIC_KEYWORDS.keys()))),
)
def test_parse_question_deterministic(question, ctx_market, ctx_metric):
    """**Validates: Requirements 3.5**
    Same inputs → same outputs, every time."""
    ctx = {}
    if ctx_market:
        ctx['market'] = ctx_market
    if ctx_metric:
        ctx['metric'] = ctx_metric
    ctx = ctx or None

    r1 = parse_question(question, ctx)
    r2 = parse_question(question, ctx)
    assert r1.market == r2.market
    assert r1.metric == r2.metric
    assert r1.prediction_type == r2.prediction_type
    assert r1.horizon_weeks == r2.horizon_weeks


# ── Property 5: Question parsing extracts known entities ──

# Build questions that contain exactly one market code and one metric keyword
market_st = st.sampled_from(MARKET_CODES)
metric_st = st.sampled_from(list(METRIC_KEYWORDS.keys()))

# Templates that embed market and metric naturally
templates = [
    "What will {market} {metric} be next week?",
    "Will {market} {metric} go up or down?",
    "How many weeks until {market} {metric} reach target 500?",
    "What is the probability {market} {metric} improves?",
    "If we launch in {market}, what happens to {metric}?",
    "Tell me about {market} {metric}",
    "{market} {metric} forecast",
]


@settings(max_examples=100, suppress_health_check=[HealthCheck.too_slow])
@given(
    market=market_st,
    metric=metric_st,
    template_idx=st.integers(min_value=0, max_value=len(templates) - 1),
)
def test_parse_extracts_known_entities(market, metric, template_idx):
    """**Validates: Requirements 3.1, 3.2, 3.3, 3.4**
    Questions with known market + metric → correct extraction."""
    question = templates[template_idx].format(market=market, metric=metric)
    result = parse_question(question)
    assert result.market == market, f"Expected market {market}, got {result.market}"
    assert result.metric == metric, f"Expected metric {metric}, got {result.metric}"
    assert result.prediction_type in VALID_TYPES, (
        f"Invalid prediction_type: {result.prediction_type}"
    )
