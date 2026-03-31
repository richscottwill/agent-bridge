"""Calibrator — self-scoring and confidence adjustment.

Tracks prediction accuracy, scores predictions against actuals, computes
calibration metrics, and adjusts confidence levels. The engine's self-awareness.
"""

import sys
import os
sys.path.insert(0, os.path.expanduser('~/shared/tools/data'))

from .types import PredictionScore, CalibrationReport

# Lazy DB imports — only called when methods actually execute
_db = None
_db_write = None
_db_upsert = None


def _load_db():
    global _db, _db_write, _db_upsert
    if _db is None:
        from query import db, db_write, db_upsert
        _db = db
        _db_write = db_write
        _db_upsert = db_upsert


# Confidence language scale (ordered low → high)
CONFIDENCE_LEVELS = [
    (0.15, 'very_unlikely'),
    (0.30, 'unlikely'),
    (0.45, 'leaning_against'),
    (0.55, 'uncertain'),
    (0.70, 'leaning_toward'),
    (0.85, 'likely'),
    (1.01, 'very_likely'),  # 1.01 so 1.0 maps to very_likely
]

LEVEL_ORDER = {
    'very_unlikely': 0, 'unlikely': 1, 'leaning_against': 2,
    'uncertain': 3, 'leaning_toward': 4, 'likely': 5, 'very_likely': 6,
}


class Calibrator:

    def __init__(self, db_path: str = None):
        self.db_path = db_path
        self._calibration_factor = 1.0

    def score_prediction(self, prediction_id: int, actual_value: float) -> PredictionScore:
        """Score a single prediction against its actual outcome.

        Composite score = 0.4 * direction + 0.3 * interval + 0.3 * error_magnitude.
        Idempotent: repeated calls with same args produce same result (upsert).
        """
        _load_db()
        kw = {'db_path': self.db_path} if self.db_path else {}

        rows = _db(f"SELECT * FROM predictions WHERE id = {prediction_id}", **kw)
        if not rows:
            raise ValueError(f"Prediction {prediction_id} not found")
        pred = rows[0]

        predicted = pred['point_estimate'] or 0.0
        error_pct = abs(actual_value - predicted) / abs(actual_value) * 100 if actual_value != 0 else 0.0

        # Direction correctness (2% tolerance band)
        direction_correct = True
        if pred.get('direction'):
            if pred['direction'] == 'up':
                direction_correct = actual_value > predicted - abs(predicted * 0.02)
            elif pred['direction'] == 'down':
                direction_correct = actual_value < predicted + abs(predicted * 0.02)

        # Interval coverage
        within_interval = (
            pred.get('lower_bound') is not None
            and pred.get('upper_bound') is not None
            and pred['lower_bound'] <= actual_value <= pred['upper_bound']
        )

        # Composite: 40% direction, 30% interval, 30% error magnitude
        dir_score = 1.0 if direction_correct else 0.0
        int_score = 1.0 if within_interval else 0.0
        err_score = max(0.0, 1.0 - error_pct / 50.0)
        score = 0.4 * dir_score + 0.3 * int_score + 0.3 * err_score

        result = PredictionScore(
            prediction_id=prediction_id,
            actual_value=actual_value,
            predicted_value=predicted,
            error_pct=error_pct,
            direction_correct=direction_correct,
            within_interval=within_interval,
            score=score,
        )

        _db_upsert('prediction_outcomes', {
            'prediction_id': prediction_id,
            'actual_value': actual_value,
            'predicted_value': predicted,
            'error_pct': error_pct,
            'direction_correct': direction_correct,
            'within_interval': within_interval,
            'score': score,
        }, key_cols=['prediction_id'], **kw)

        _db_write(f"UPDATE predictions SET status = 'scored' WHERE id = {prediction_id}", **kw)

        return result

    def compute_calibration(self, lookback: int = 100) -> CalibrationReport:
        """Compute calibration across recent scored predictions.

        Groups by confidence tier, computes hit_rate vs expected_rate,
        excludes tiers with < 5 predictions, clamps adjustment to [0.5, 2.0].
        """
        _load_db()
        kw = {'db_path': self.db_path} if self.db_path else {}

        scored = _db(f"""
            SELECT p.*, po.actual_value, po.direction_correct,
                   po.within_interval, po.score, po.error_pct
            FROM predictions p
            JOIN prediction_outcomes po ON p.id = po.prediction_id
            ORDER BY po.scored_at DESC LIMIT {lookback}
        """, **kw)

        if not scored:
            return CalibrationReport(
                total_predictions=0, total_scored=0, mean_error_pct=0.0,
                direction_accuracy=0.0, interval_coverage=0.0,
                calibration_score=1.0, confidence_adjustment=1.0,
                tier_breakdown={},
            )

        # Group by confidence tier
        tiers = {}
        for pred in scored:
            level = pred.get('confidence_level', 'uncertain')
            if level not in tiers:
                tiers[level] = {'count': 0, 'hits': 0, 'expected_rate': 0.0}
            tiers[level]['count'] += 1
            if pred.get('within_interval'):
                tiers[level]['hits'] += 1
            tiers[level]['expected_rate'] = pred.get('confidence_probability', 0.5)

        for level, data in tiers.items():
            data['hit_rate'] = data['hits'] / data['count'] if data['count'] > 0 else 0.0

        total = len(scored)
        direction_correct = sum(1 for s in scored if s.get('direction_correct'))
        within_interval = sum(1 for s in scored if s.get('within_interval'))
        mean_error = sum(abs(s.get('error_pct', 0) or 0) for s in scored) / total

        # Calibration error (only tiers with 5+ predictions)
        cal_errors = [
            abs(d['hit_rate'] - d['expected_rate'])
            for d in tiers.values() if d['count'] >= 5
        ]
        calibration_score = 1.0 - (sum(cal_errors) / len(cal_errors)) if cal_errors else 1.0

        # Confidence adjustment from largest tier
        main_tier = max(tiers.values(), key=lambda d: d['count']) if tiers else None
        if main_tier and main_tier['hit_rate'] > 0 and main_tier['count'] >= 5:
            adjustment = max(0.5, min(2.0, main_tier['expected_rate'] / main_tier['hit_rate']))
        else:
            adjustment = 1.0

        self._calibration_factor = adjustment

        return CalibrationReport(
            total_predictions=total, total_scored=total,
            mean_error_pct=mean_error,
            direction_accuracy=direction_correct / total,
            interval_coverage=within_interval / total,
            calibration_score=calibration_score,
            confidence_adjustment=adjustment,
            tier_breakdown=tiers,
        )

    def get_confidence_adjustment(self) -> float:
        """Return current calibration adjustment factor."""
        return self._calibration_factor

    @staticmethod
    def confidence_to_language(probability: float) -> str:
        """Map probability to 7-level natural language scale.

        >0.85  → 'very_likely'
        0.70-0.85 → 'likely'
        0.55-0.70 → 'leaning_toward'
        0.45-0.55 → 'uncertain'
        0.30-0.45 → 'leaning_against'
        0.15-0.30 → 'unlikely'
        <0.15  → 'very_unlikely'
        """
        for threshold, label in CONFIDENCE_LEVELS:
            if probability < threshold:
                return label
        return 'very_likely'
