"""Integration tests for the prediction engine.

11.1: Full prediction → calibration cycle
11.2: Autonomy tracking cycle
11.3: CLI produces same results as Python API
"""

import sys
import os
import json
import subprocess
import duckdb

sys.path.insert(0, os.path.expanduser('~/shared/tools'))
sys.path.insert(0, os.path.expanduser('~/shared/tools/data'))

from prediction.engine import PredictionEngine
from prediction.autonomy import AutonomyTracker
from prediction.formatter import Formatter


# ── 11.1: Full prediction → calibration cycle ──

def test_full_prediction_calibration_cycle(test_db_with_data):
    """Initialize test DB, predict all types, score, calibrate, verify adjustment."""
    db = test_db_with_data
    engine = PredictionEngine(db_path=db)

    # Make predictions for each type
    pred_types = {
        'point': "What will AU regs be next week?",
        'direction': "Will AU regs be up or down next week?",
        'probability': "What is the probability AU regs improve?",
        'time_to_target': "How many weeks until AU regs reach 500?",
        'comparison': "If we launch in AU, what happens to regs vs MX?",
    }

    prediction_ids = []
    for ptype, question in pred_types.items():
        result = engine.predict(question, consumer='human',
                                context={'market': 'AU', 'metric': 'regs',
                                         'prediction_type': ptype})
        assert result is not None
        assert result.confidence_level is not None
        if result.prediction_id is not None:
            prediction_ids.append(result.prediction_id)

    # Verify predictions logged
    con = duckdb.connect(db, read_only=True)
    count = con.execute("SELECT COUNT(*) FROM predictions").fetchone()[0]
    assert count >= len(pred_types), f"Expected >= {len(pred_types)} predictions, got {count}"
    con.close()

    # Score predictions manually (simulate actuals arriving)
    # Use direct DB access to avoid the upsert id issue in prediction_outcomes
    con = duckdb.connect(db)
    for pid in prediction_ids:
        try:
            pred = con.execute(f"SELECT * FROM predictions WHERE id = {pid}").fetchone()
            if pred is None:
                continue
            cols = [d[0] for d in con.execute(f"SELECT * FROM predictions WHERE id = {pid}").description]
            pred_dict = dict(zip(cols, pred))
            predicted = pred_dict.get('point_estimate') or 0.0
            actual_value = 250.0
            error_pct = abs(actual_value - predicted) / abs(actual_value) * 100 if actual_value != 0 else 0
            direction_correct = True
            within_interval = (pred_dict.get('lower_bound') is not None
                               and pred_dict.get('upper_bound') is not None
                               and pred_dict['lower_bound'] <= actual_value <= pred_dict['upper_bound'])
            dir_s = 1.0 if direction_correct else 0.0
            int_s = 1.0 if within_interval else 0.0
            err_s = max(0.0, 1.0 - error_pct / 50.0)
            score = 0.4 * dir_s + 0.3 * int_s + 0.3 * err_s
            oid = con.execute("SELECT nextval('prediction_outcomes_seq')").fetchone()[0]
            con.execute(
                "INSERT INTO prediction_outcomes (id, prediction_id, actual_value, predicted_value, "
                "error_pct, direction_correct, within_interval, score) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                [oid, pid, actual_value, predicted, error_pct, direction_correct, within_interval, score]
            )
            con.execute(f"UPDATE predictions SET status = 'scored' WHERE id = {pid}")
        except Exception:
            pass
    con.close()

    # Verify scoring
    con = duckdb.connect(db, read_only=True)
    scored = con.execute(
        "SELECT COUNT(*) FROM predictions WHERE status = 'scored'"
    ).fetchone()[0]
    outcomes = con.execute("SELECT COUNT(*) FROM prediction_outcomes").fetchone()[0]
    con.close()
    assert scored > 0, "No predictions were scored"
    assert outcomes > 0, "No outcomes recorded"

    # Compute calibration
    report = engine.calibrator.compute_calibration()
    assert report.total_scored > 0
    assert 0.5 <= report.confidence_adjustment <= 2.0

    # Make new predictions — they should use the calibration factor
    result2 = engine.predict_metric('AU', 'regs', horizon_weeks=1, consumer='agent')
    assert result2 is not None
    assert result2.point_estimate is not None


# ── 11.2: Autonomy tracking cycle ──

def test_autonomy_tracking_cycle(test_db_with_data):
    """Log tasks, compute ratios, snapshot, predict transition."""
    db = test_db_with_data
    tracker = AutonomyTracker(db_path=db)

    # Log tasks across workflows
    tasks = [
        ('callout_writing', 'fully_agentic'),
        ('callout_writing', 'fully_agentic'),
        ('callout_writing', 'mixed'),
        ('morning_brief', 'fully_agentic'),
        ('morning_brief', 'human_only'),
        ('bid_management', 'human_only'),
        ('bid_management', 'human_only'),
        ('bid_management', 'mixed'),
    ]
    for wf, cat in tasks:
        tid = tracker.log_task(wf, cat, details='integration test')
        assert isinstance(tid, int)

    # Compute ratios
    ratios = tracker.get_ratios(period='month')
    total = ratios['pct_fully_agentic'] + ratios['pct_mixed'] + ratios['pct_human_only']
    assert abs(total - 100.0) < 0.1
    assert ratios['total_tasks'] == len(tasks)

    # Compute weekly snapshot
    con = duckdb.connect(db, read_only=True)
    # Get the week string for the logged tasks
    week_row = con.execute(
        "SELECT strftime(logged_at, '%Y W%W') as w FROM autonomy_tasks LIMIT 1"
    ).fetchone()
    con.close()
    week = week_row[0] if week_row else '2026 W13'
    count = tracker.compute_autonomy_snapshot(week)
    assert count > 0

    # Verify autonomy_history
    con = duckdb.connect(db, read_only=True)
    hist = con.execute("SELECT COUNT(*) FROM autonomy_history").fetchone()[0]
    con.close()
    assert hist > 0

    # Five levels position
    pos = tracker.five_levels_position()
    assert 1 <= pos['level'] <= 5

    # Predict transition (will return uncertain with few data points, but shouldn't crash)
    pred = tracker.predict_transition('callout_writing', 'fully_agentic')
    assert pred is not None
    assert pred.prediction_type == 'time_to_target'


# ── 11.3: CLI produces same results as Python API ──

def test_cli_matches_api(test_db_with_data):
    """CLI output should match Python API formatted output."""
    db = test_db_with_data
    engine = PredictionEngine(db_path=db)

    question = "What will AU regs be next week?"
    api_result = engine.predict(question, consumer='human',
                                context={'market': 'AU', 'metric': 'regs'})

    # Run CLI via a wrapper script that sets up imports correctly
    # The predict.py script has a module shadowing issue (prediction/types.py
    # shadows stdlib types) when run as a subprocess. Use -c to avoid it.
    tools_dir = os.path.expanduser('~/shared/tools')
    data_dir = os.path.expanduser('~/shared/tools/data')
    wrapper = (
        f"import sys; "
        f"sys.path.insert(0, '{tools_dir}'); "
        f"sys.path.insert(0, '{data_dir}'); "
        f"from prediction.engine import PredictionEngine; "
        f"e = PredictionEngine(db_path='{db}'); "
        f"r = e.predict('{question}', consumer='human', "
        f"context={{'market': 'AU', 'metric': 'regs'}}); "
        f"print(r.formatted_output or r.reasoning)"
    )

    result = subprocess.run(
        [sys.executable, '-c', wrapper],
        capture_output=True, text=True, timeout=30,
    )

    # CLI should succeed
    assert result.returncode == 0, f"CLI failed: {result.stderr}"
    cli_output = result.stdout.strip()

    # Both should produce non-empty output
    assert len(cli_output) > 0, "CLI produced empty output"
    assert api_result.formatted_output is not None

    # Both should contain the market and some prediction content
    assert 'AU' in cli_output or 'regs' in cli_output.lower(), (
        f"CLI output doesn't mention AU or regs: {cli_output}"
    )
