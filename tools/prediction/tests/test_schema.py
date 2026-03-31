"""Property test: database constraint enforcement (Property 13).

**Validates: Requirements 11.2, 11.3, 11.4, 11.5**

Attempts inserts with invalid prediction_type, score outside [0,1],
invalid category, five_levels_position outside [1,5].
Verifies database rejects each invalid insert.
"""

import sys
import os
import pytest
import duckdb

sys.path.insert(0, os.path.expanduser('~/shared/tools'))
sys.path.insert(0, os.path.expanduser('~/shared/tools/data'))

from hypothesis import given, settings, HealthCheck
from hypothesis import strategies as st


@settings(max_examples=30, suppress_health_check=[HealthCheck.too_slow, HealthCheck.function_scoped_fixture])
@given(bad_type=st.text(min_size=1).filter(
    lambda s: s not in ('point', 'direction', 'probability', 'time_to_target', 'comparison')
))
def test_predictions_rejects_invalid_prediction_type(test_db, bad_type):
    """Invalid prediction_type values must be rejected by CHECK constraint."""
    con = duckdb.connect(test_db)
    try:
        with pytest.raises(duckdb.Error):
            con.execute(
                "INSERT INTO predictions (id, prediction_type, confidence_probability, status) "
                "VALUES (nextval('predictions_seq'), ?, 0.5, 'pending')",
                [bad_type]
            )
    finally:
        con.close()


@settings(max_examples=30, suppress_health_check=[HealthCheck.too_slow, HealthCheck.function_scoped_fixture])
@given(bad_prob=st.one_of(
    st.floats(max_value=-0.01, allow_nan=False, allow_infinity=False),
    st.floats(min_value=1.01, max_value=1e6, allow_nan=False, allow_infinity=False),
))
def test_predictions_rejects_invalid_confidence_probability(test_db, bad_prob):
    """confidence_probability outside [0,1] must be rejected."""
    con = duckdb.connect(test_db)
    try:
        with pytest.raises(duckdb.Error):
            con.execute(
                "INSERT INTO predictions (id, prediction_type, confidence_probability, status) "
                "VALUES (nextval('predictions_seq'), 'point', ?, 'pending')",
                [bad_prob]
            )
    finally:
        con.close()


@settings(max_examples=30, suppress_health_check=[HealthCheck.too_slow, HealthCheck.function_scoped_fixture])
@given(bad_score=st.one_of(
    st.floats(max_value=-0.01, allow_nan=False, allow_infinity=False),
    st.floats(min_value=1.01, max_value=1e6, allow_nan=False, allow_infinity=False),
))
def test_prediction_outcomes_rejects_invalid_score(test_db, bad_score):
    """score outside [0,1] must be rejected."""
    con = duckdb.connect(test_db)
    try:
        # Insert a valid prediction first
        con.execute(
            "INSERT INTO predictions (id, prediction_type, confidence_probability, status) "
            "VALUES (nextval('predictions_seq'), 'point', 0.5, 'pending')"
        )
        pred_id = con.execute("SELECT max(id) FROM predictions").fetchone()[0]
        with pytest.raises(duckdb.Error):
            con.execute(
                "INSERT INTO prediction_outcomes (id, prediction_id, score) "
                "VALUES (nextval('prediction_outcomes_seq'), ?, ?)",
                [pred_id, bad_score]
            )
    finally:
        con.close()


@settings(max_examples=30, suppress_health_check=[HealthCheck.too_slow, HealthCheck.function_scoped_fixture])
@given(bad_cat=st.text(min_size=1).filter(
    lambda s: s not in ('fully_agentic', 'mixed', 'human_only')
))
def test_autonomy_tasks_rejects_invalid_category(test_db, bad_cat):
    """Invalid category values must be rejected."""
    con = duckdb.connect(test_db)
    try:
        with pytest.raises(duckdb.Error):
            con.execute(
                "INSERT INTO autonomy_tasks (id, workflow, category) "
                "VALUES (nextval('autonomy_tasks_seq'), 'test_wf', ?)",
                [bad_cat]
            )
    finally:
        con.close()


@settings(max_examples=30, suppress_health_check=[HealthCheck.too_slow, HealthCheck.function_scoped_fixture])
@given(bad_pos=st.integers().filter(lambda x: x < 1 or x > 5))
def test_autonomy_history_rejects_invalid_five_levels(test_db, bad_pos):
    """five_levels_position outside [1,5] must be rejected."""
    con = duckdb.connect(test_db)
    try:
        with pytest.raises(duckdb.Error):
            con.execute(
                "INSERT INTO autonomy_history (week, workflow, five_levels_position) "
                "VALUES ('2026 W01', 'test_wf', ?)",
                [bad_pos]
            )
    finally:
        con.close()
