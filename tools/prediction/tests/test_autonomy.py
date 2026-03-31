"""Property test: autonomy ratios sum to 100% (Property 12).

**Validates: Requirements 10.2**
"""

import sys
import os
import duckdb

sys.path.insert(0, os.path.expanduser('~/shared/tools'))
sys.path.insert(0, os.path.expanduser('~/shared/tools/data'))

from hypothesis import given, settings, HealthCheck
from hypothesis import strategies as st

from prediction.autonomy import AutonomyTracker, VALID_CATEGORIES

categories_st = st.sampled_from(list(VALID_CATEGORIES))
workflows_st = st.sampled_from(['callout_writing', 'morning_brief', 'bid_management', 'reporting'])


@settings(max_examples=30, deadline=30000, suppress_health_check=[HealthCheck.too_slow, HealthCheck.function_scoped_fixture])
@given(
    tasks=st.lists(
        st.tuples(workflows_st, categories_st),
        min_size=1, max_size=30,
    ),
)
def test_autonomy_ratios_sum_to_100(test_db, tasks):
    """**Validates: Requirements 10.2**
    pct_fully_agentic + pct_mixed + pct_human_only == 100% (±0.1%)."""
    tracker = AutonomyTracker(db_path=test_db)
    for workflow, category in tasks:
        tracker.log_task(workflow, category, details='test')

    ratios = tracker.get_ratios(period='month')  # wide window to capture all
    total_pct = ratios['pct_fully_agentic'] + ratios['pct_mixed'] + ratios['pct_human_only']
    assert abs(total_pct - 100.0) < 0.1, (
        f"Ratios sum to {total_pct}, not 100%: "
        f"agentic={ratios['pct_fully_agentic']}, "
        f"mixed={ratios['pct_mixed']}, "
        f"human={ratios['pct_human_only']}"
    )
