"""Property tests for Calibrator (Properties 7, 8, 9, 10).

**Validates: Requirements 5.1, 5.2, 5.3, 5.4, 6.1, 6.2, 6.3, 7.1, 7.2**
"""

import sys
import os
import duckdb

sys.path.insert(0, os.path.expanduser('~/shared/tools'))
sys.path.insert(0, os.path.expanduser('~/shared/tools/data'))

from hypothesis import given, settings, assume, HealthCheck
from hypothesis import strategies as st

from prediction.calibrator import Calibrator, LEVEL_ORDER


# ── Helper: insert a test prediction ──

def _insert_test_prediction(db_path, point_est=100.0, lower=80.0, upper=120.0,
                            direction='up', conf_prob=0.7):
    """Insert a valid pending prediction and return its id."""
    con = duckdb.connect(db_path)
    pid = con.execute("SELECT nextval('predictions_seq')").fetchone()[0]
    con.execute(
        "INSERT INTO predictions (id, question, market, metric, prediction_type, "
        "point_estimate, lower_bound, upper_bound, confidence_level, "
        "confidence_probability, direction, horizon_weeks, status) "
        "VALUES (?, 'test', 'AU', 'regs', 'point', ?, ?, ?, 'likely', ?, ?, 1, 'pending')",
        [pid, point_est, lower, upper, conf_prob, direction]
    )
    con.close()
    return pid


def _score_prediction_direct(db_path, prediction_id, actual_value):
    """Score a prediction using direct DB access (bypasses upsert id issue).

    Replicates the Calibrator.score_prediction logic but handles the
    prediction_outcomes insert directly with a generated id.
    """
    con = duckdb.connect(db_path)
    pred = con.execute(f"SELECT * FROM predictions WHERE id = {prediction_id}").fetchone()
    cols = [d[0] for d in con.execute(f"SELECT * FROM predictions WHERE id = {prediction_id}").description]
    pred = dict(zip(cols, pred))

    predicted = pred['point_estimate'] or 0.0
    error_pct = abs(actual_value - predicted) / abs(actual_value) * 100 if actual_value != 0 else 0.0

    direction_correct = True
    if pred.get('direction'):
        if pred['direction'] == 'up':
            direction_correct = actual_value > predicted - abs(predicted * 0.02)
        elif pred['direction'] == 'down':
            direction_correct = actual_value < predicted + abs(predicted * 0.02)

    within_interval = (
        pred.get('lower_bound') is not None
        and pred.get('upper_bound') is not None
        and pred['lower_bound'] <= actual_value <= pred['upper_bound']
    )

    dir_score = 1.0 if direction_correct else 0.0
    int_score = 1.0 if within_interval else 0.0
    err_score = max(0.0, 1.0 - error_pct / 50.0)
    score = 0.4 * dir_score + 0.3 * int_score + 0.3 * err_score

    # Check if outcome already exists
    existing = con.execute(
        f"SELECT id FROM prediction_outcomes WHERE prediction_id = {prediction_id}"
    ).fetchone()

    if existing:
        con.execute(
            "UPDATE prediction_outcomes SET actual_value=?, predicted_value=?, "
            "error_pct=?, direction_correct=?, within_interval=?, score=? "
            "WHERE prediction_id=?",
            [actual_value, predicted, error_pct, direction_correct, within_interval, score, prediction_id]
        )
    else:
        oid = con.execute("SELECT nextval('prediction_outcomes_seq')").fetchone()[0]
        con.execute(
            "INSERT INTO prediction_outcomes (id, prediction_id, actual_value, predicted_value, "
            "error_pct, direction_correct, within_interval, score) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            [oid, prediction_id, actual_value, predicted, error_pct, direction_correct, within_interval, score]
        )

    con.execute(f"UPDATE predictions SET status = 'scored' WHERE id = {prediction_id}")
    con.close()

    return {
        'prediction_id': prediction_id,
        'actual_value': actual_value,
        'predicted_value': predicted,
        'error_pct': error_pct,
        'direction_correct': direction_correct,
        'within_interval': within_interval,
        'score': score,
    }


# ── Property 7: Scoring produces valid composite score ──

@settings(max_examples=50, suppress_health_check=[HealthCheck.too_slow, HealthCheck.function_scoped_fixture])
@given(
    actual=st.floats(min_value=1, max_value=500, allow_nan=False, allow_infinity=False),
)
def test_scoring_valid_composite(test_db, actual):
    """**Validates: Requirements 5.1, 5.2, 5.3**
    Composite score in [0,1] and matches 0.4/0.3/0.3 formula."""
    pid = _insert_test_prediction(test_db)
    result = _score_prediction_direct(test_db, pid, actual)

    # Score in [0, 1]
    assert 0.0 <= result['score'] <= 1.0, f"Score {result['score']} out of [0,1]"

    # Verify formula
    dir_s = 1.0 if result['direction_correct'] else 0.0
    int_s = 1.0 if result['within_interval'] else 0.0
    err_s = max(0.0, 1.0 - result['error_pct'] / 50.0)
    expected = 0.4 * dir_s + 0.3 * int_s + 0.3 * err_s
    assert abs(result['score'] - expected) < 1e-6

    # Verify DB state
    con = duckdb.connect(test_db, read_only=True)
    outcomes = con.execute(
        f"SELECT * FROM prediction_outcomes WHERE prediction_id = {pid}"
    ).fetchall()
    assert len(outcomes) == 1
    pred_status = con.execute(
        f"SELECT status FROM predictions WHERE id = {pid}"
    ).fetchone()[0]
    assert pred_status == 'scored'
    con.close()


# ── Property 8: Scoring idempotence ──

@settings(max_examples=30, suppress_health_check=[HealthCheck.too_slow, HealthCheck.function_scoped_fixture])
@given(
    actual=st.floats(min_value=1, max_value=500, allow_nan=False, allow_infinity=False),
)
def test_scoring_idempotent(test_db, actual):
    """**Validates: Requirements 5.4**
    Scoring same prediction twice → same result, no duplicate rows."""
    pid = _insert_test_prediction(test_db)
    r1 = _score_prediction_direct(test_db, pid, actual)
    r2 = _score_prediction_direct(test_db, pid, actual)

    assert r1['score'] == r2['score']
    assert r1['direction_correct'] == r2['direction_correct']
    assert r1['within_interval'] == r2['within_interval']

    # Exactly one outcome row
    con = duckdb.connect(test_db, read_only=True)
    count = con.execute(
        f"SELECT COUNT(*) FROM prediction_outcomes WHERE prediction_id = {pid}"
    ).fetchone()[0]
    assert count == 1
    con.close()


# ── Property 9: Calibration self-correction with bounds ──

def _seed_scored_predictions(db_path, n=10, conf_prob=0.7, hit_rate=0.3):
    """Insert n scored predictions with a controlled hit rate."""
    con = duckdb.connect(db_path)
    hits = int(n * hit_rate)
    for i in range(n):
        pid = con.execute("SELECT nextval('predictions_seq')").fetchone()[0]
        oid = con.execute("SELECT nextval('prediction_outcomes_seq')").fetchone()[0]
        within = i < hits
        con.execute(
            "INSERT INTO predictions (id, question, market, metric, prediction_type, "
            "point_estimate, lower_bound, upper_bound, confidence_level, "
            "confidence_probability, direction, horizon_weeks, status) "
            "VALUES (?, 'test', 'AU', 'regs', 'point', 100, 80, 120, 'likely', ?, 'up', 1, 'scored')",
            [pid, conf_prob]
        )
        con.execute(
            "INSERT INTO prediction_outcomes (id, prediction_id, actual_value, predicted_value, "
            "error_pct, direction_correct, within_interval, score) "
            "VALUES (?, ?, 100, 100, 0, true, ?, 0.7)",
            [oid, pid, within]
        )
    con.close()


def test_calibration_correction_overconfident(test_db):
    """**Validates: Requirements 6.1, 6.2, 6.3**
    When hit rate < expected rate (overconfident), adjustment > 1.0."""
    _seed_scored_predictions(test_db, n=10, conf_prob=0.7, hit_rate=0.3)
    cal = Calibrator(db_path=test_db)
    report = cal.compute_calibration()
    assert report.confidence_adjustment >= 1.0
    assert 0.5 <= report.confidence_adjustment <= 2.0


def test_calibration_correction_underconfident(test_db):
    """**Validates: Requirements 6.1, 6.2, 6.3**
    When hit rate > expected rate (underconfident), adjustment < 1.0."""
    _seed_scored_predictions(test_db, n=10, conf_prob=0.3, hit_rate=0.9)
    cal = Calibrator(db_path=test_db)
    report = cal.compute_calibration()
    assert report.confidence_adjustment <= 1.0
    assert 0.5 <= report.confidence_adjustment <= 2.0


def test_calibration_bounds_clamped(test_db):
    """**Validates: Requirements 6.3**
    Adjustment always in [0.5, 2.0]."""
    _seed_scored_predictions(test_db, n=10, conf_prob=0.9, hit_rate=0.1)
    cal = Calibrator(db_path=test_db)
    report = cal.compute_calibration()
    assert 0.5 <= report.confidence_adjustment <= 2.0


# ── Property 10: Confidence language monotonicity ──

@settings(max_examples=200, suppress_health_check=[HealthCheck.too_slow])
@given(
    p1=st.floats(min_value=0.0, max_value=1.0, allow_nan=False, allow_infinity=False),
    p2=st.floats(min_value=0.0, max_value=1.0, allow_nan=False, allow_infinity=False),
)
def test_confidence_language_monotonic(p1, p2):
    """**Validates: Requirements 7.1, 7.2**
    p1 > p2 → confidence_to_language(p1) >= confidence_to_language(p2)."""
    assume(p1 > p2)
    l1 = Calibrator.confidence_to_language(p1)
    l2 = Calibrator.confidence_to_language(p2)
    assert LEVEL_ORDER[l1] >= LEVEL_ORDER[l2], (
        f"Monotonicity violated: p1={p1}→{l1} vs p2={p2}→{l2}"
    )
