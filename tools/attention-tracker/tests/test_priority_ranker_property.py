"""Property-based tests for priority ranking.

**Validates: Requirements 9.2**

Property 4: Priority Ordering — action_items[i].score >= action_items[j].score for all i < j.
Findings are sorted descending by score and assigned sequential ranks starting from 1.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from hypothesis import given, settings
from hypothesis import strategies as st

from paid_search_audit.priority_ranker import rank_findings


# --- Strategies ---

severity_strategy = st.sampled_from(["CRITICAL", "WARNING", "INFO"])
market_strategy = st.sampled_from(["AU", "MX", "US", "JP", "CA", "DE", "FR", "IT", "ES"])
category_strategy = st.sampled_from(["BUDGET", "GOAL", "PERFORMANCE", "OTHER"])
trend_strategy = st.sampled_from(["WORSENING", None])


@dataclass
class FakeFinding:
    """Minimal finding-like object for property testing."""
    severity: str = "INFO"
    market: str = "AU"
    category: str = "PERFORMANCE"
    trend: Optional[str] = None


@st.composite
def finding_strategy(draw):
    """Generate a single random finding."""
    return FakeFinding(
        severity=draw(severity_strategy),
        market=draw(market_strategy),
        category=draw(category_strategy),
        trend=draw(trend_strategy),
    )


findings_list_strategy = st.lists(finding_strategy(), min_size=0, max_size=50)


class TestPriorityOrdering:
    """Property 4: Priority Ordering.

    **Validates: Requirements 9.2**

    For all i < j in the ranked output:
      - result[i].score >= result[j].score (descending order)
      - ranks are sequential starting from 1
      - output length equals input length
    """

    @given(findings=findings_list_strategy)
    @settings(max_examples=200, deadline=None)
    def test_descending_score_order(self, findings):
        """For all i < j, result[i].score >= result[j].score."""
        result = rank_findings(findings)

        for i in range(len(result) - 1):
            assert result[i].score >= result[i + 1].score, (
                f"Score at index {i} ({result[i].score}) < "
                f"score at index {i + 1} ({result[i + 1].score})"
            )

    @given(findings=findings_list_strategy)
    @settings(max_examples=200, deadline=None)
    def test_sequential_ranks_from_one(self, findings):
        """Ranks are sequential integers starting from 1."""
        result = rank_findings(findings)

        for i, pf in enumerate(result):
            assert pf.priority == i + 1, (
                f"Expected priority {i + 1} at index {i}, got {pf.priority}"
            )

    @given(findings=findings_list_strategy)
    @settings(max_examples=200, deadline=None)
    def test_output_length_equals_input(self, findings):
        """No findings are lost or duplicated during ranking."""
        result = rank_findings(findings)

        assert len(result) == len(findings), (
            f"Input had {len(findings)} findings but output has {len(result)}"
        )
