"""Property-based tests for action item generation.

**Validates: Requirements 10.5**

Property 9: Action Item Bound — report contains at most 10 action items.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from hypothesis import given, settings
from hypothesis import strategies as st

from paid_search_audit.models import AnomalyFinding
from paid_search_audit.kpi_comparator import KPIFinding
from paid_search_audit.orchestrator import generate_action_items
from paid_search_audit.priority_ranker import rank_findings

MARKET_CODES = ["AU", "MX", "US", "UK", "DE", "FR", "IT", "ES", "JP", "CA"]
SEVERITIES = ["INFO", "WARNING", "CRITICAL"]
CATEGORIES = ["BUDGET", "GOAL", "PERFORMANCE", "ANOMALY"]
VALID_URGENCIES = {"TODAY", "THIS_WEEK", "MONITOR"}


# ------------------------------------------------------------------ #
# Hypothesis strategies
# ------------------------------------------------------------------ #

@st.composite
def anomaly_finding_strategy(draw):
    """Generate a random AnomalyFinding."""
    market = draw(st.sampled_from(MARKET_CODES))
    severity = draw(st.sampled_from(SEVERITIES))
    direction = draw(st.sampled_from(["UP", "DOWN"]))
    metric = draw(st.sampled_from(["CPA", "Registrations", "Spend", "CTR"]))
    z = draw(st.decimals(min_value=Decimal("1.5"), max_value=Decimal("5.0"),
                         allow_nan=False, allow_infinity=False, places=2))
    return AnomalyFinding(
        market=market,
        metric_name=metric,
        current_value=Decimal("100"),
        baseline_value=Decimal("80"),
        deviation_pct=Decimal("25"),
        z_score=z,
        direction=direction,
        severity=severity,
        campaign_scope="All",
        context=f"{market} {metric} anomaly ({direction})",
    )


@st.composite
def kpi_finding_strategy(draw):
    """Generate a random KPIFinding."""
    market = draw(st.sampled_from(MARKET_CODES))
    severity = draw(st.sampled_from(SEVERITIES))
    metric = draw(st.sampled_from(["spend", "registrations", "cpa"]))
    status = draw(st.sampled_from(["ON_TRACK", "AT_RISK"]))
    return KPIFinding(
        market=market,
        metric_name=metric,
        actual=Decimal("500"),
        target=Decimal("1000"),
        prorated_target=Decimal("500"),
        pacing_pct=Decimal("100"),
        status=status,
        is_kingpin_goal=False,
        severity=severity,
        category="GOAL",
    )


findings_strategy = st.lists(
    st.one_of(anomaly_finding_strategy(), kpi_finding_strategy()),
    min_size=0,
    max_size=50,
)


# ------------------------------------------------------------------ #
# Property 9: Action Item Bound
# ------------------------------------------------------------------ #

class TestActionItemBoundProperty:
    """Property 9: Action Item Bound.

    **Validates: Requirements 10.5**

    The report contains at most 10 action items, never more than the
    number of input findings, and each item has valid fields.
    """

    @given(findings=findings_strategy)
    @settings(max_examples=100, deadline=None)
    def test_action_items_at_most_10(self, findings):
        """generate_action_items returns at most 10 items."""
        prioritized = rank_findings(findings)
        items = generate_action_items(prioritized)

        assert len(items) <= 10, (
            f"Expected at most 10 action items, got {len(items)} "
            f"from {len(findings)} findings"
        )

    @given(findings=findings_strategy)
    @settings(max_examples=100, deadline=None)
    def test_action_items_at_most_input_count(self, findings):
        """Action items never exceed the number of input findings."""
        prioritized = rank_findings(findings)
        items = generate_action_items(prioritized)

        assert len(items) <= len(findings), (
            f"Got {len(items)} action items from {len(findings)} findings"
        )

    @given(findings=findings_strategy)
    @settings(max_examples=100, deadline=None)
    def test_action_items_have_valid_fields(self, findings):
        """Each action item has a non-empty suggested_action and valid urgency."""
        prioritized = rank_findings(findings)
        items = generate_action_items(prioritized)

        for item in items:
            assert item.suggested_action, (
                f"Action item for {item.market} has empty suggested_action"
            )
            assert item.urgency in VALID_URGENCIES, (
                f"Action item urgency '{item.urgency}' not in {VALID_URGENCIES}"
            )
