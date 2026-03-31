"""PredictionEngine — main entry point for all prediction requests.

Parses natural-language questions, routes to the appropriate model, runs
inference via BayesianCore, logs predictions to DuckDB, and returns
formatted results. Handles graceful degradation for edge cases.
"""

import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.expanduser('~/shared/tools/data'))

from .types import PredictionResult, CalibrationReport
from .core import BayesianCore
from .models import ModelRegistry
from .calibrator import Calibrator
from .formatter import Formatter
from .parser import parse_question

# Lazy DB imports
_db = None
_db_write = None
_market_week = None


def _load_db():
    global _db, _db_write, _market_week
    if _db is None:
        from query import db, db_write, market_week
        _db = db
        _db_write = db_write
        _market_week = market_week


class PredictionEngine:

    def __init__(self, db_path: str = None):
        """Initialize engine components."""
        self.db_path = db_path
        self.core = BayesianCore()
        self.registry = ModelRegistry(db_path=db_path)
        self.calibrator = Calibrator(db_path=db_path)
        self.formatter = Formatter()
        self._calibration_factor = 1.0

    def predict(self, question: str, consumer: str = 'human',
                context: dict = None) -> PredictionResult:
        """Main entry point. Parse question, run inference, log, format."""
        parsed = parse_question(question, context)

        if not parsed.market and not parsed.metric:
            return self._uncertain_result(
                question, parsed,
                "Couldn't parse market or metric from the question. "
                "Try: --market AU --metric regs, or rephrase."
            )

        return self._run_prediction(
            question=question,
            market=parsed.market,
            metric=parsed.metric or 'regs',
            horizon_weeks=parsed.horizon_weeks,
            prediction_type=parsed.prediction_type,
            target=parsed.target,
            consumer=consumer,
        )

    def predict_metric(self, market: str, metric: str, horizon_weeks: int = 1,
                       consumer: str = 'human') -> PredictionResult:
        """Structured prediction bypassing question parsing."""
        question = f"What will {market} {metric} be in {horizon_weeks} week(s)?"
        return self._run_prediction(
            question=question,
            market=market,
            metric=metric,
            horizon_weeks=horizon_weeks,
            prediction_type='point',
            target=None,
            consumer=consumer,
        )

    def calibrate(self, week: str = None) -> CalibrationReport:
        """Score pending predictions for the given week against actuals.

        Also expires predictions whose outcome_week is >2 weeks past
        and status is still 'pending' (task 8.3).
        """
        _load_db()
        kw = {'db_path': self.db_path} if self.db_path else {}

        # --- Expire stale predictions (8.3) ---
        try:
            _db_write(
                "UPDATE predictions SET status = 'expired' "
                "WHERE status = 'pending' AND outcome_week IS NOT NULL "
                "AND outcome_week < strftime(current_date - INTERVAL '14' DAY, '%Y W%W')",
                **kw,
            )
        except Exception:
            # Best-effort expiration — don't block calibration
            pass

        # --- Score pending predictions for this week ---
        if week:
            pending = _db(
                f"SELECT * FROM predictions WHERE outcome_week = '{week}' "
                f"AND status = 'pending'", **kw,
            )
            for pred in pending:
                actual = self._fetch_actual(
                    pred.get('market'), pred.get('metric'), week
                )
                if actual is None:
                    continue
                self.calibrator.score_prediction(pred['id'], actual)

        # --- Recompute calibration ---
        report = self.calibrator.compute_calibration()
        self._calibration_factor = report.confidence_adjustment
        return report

    def get_calibration_report(self) -> CalibrationReport:
        """Return current calibration state."""
        return self.calibrator.compute_calibration()

    # ── Internal helpers ──

    def _run_prediction(self, question: str, market: str, metric: str,
                        horizon_weeks: int, prediction_type: str,
                        target: float = None, consumer: str = 'human') -> PredictionResult:
        """Core prediction logic shared by predict() and predict_metric()."""
        _load_db()
        kw = {'db_path': self.db_path} if self.db_path else {}

        # Get or build model
        try:
            model = self.registry.get_model(market, metric)
        except Exception:
            return self._uncertain_result(
                question, None,
                f"No data available for {market} {metric}. Check that weekly_metrics has data."
            )

        prior = model.prior

        # Insufficient data guard
        if prior.n_observations < 3:
            return self._uncertain_result(
                question, None,
                f"Only {prior.n_observations} data points for {market} {metric}. "
                f"Need at least 3 weeks for a meaningful prediction."
            )

        # Get recent evidence for posterior update
        try:
            from query import market_trend
            recent = market_trend(market, weeks=8, **kw)
        except Exception:
            recent = []

        cal_factor = self.calibrator.get_confidence_adjustment()
        posterior = self.core.update_posterior(prior, recent, cal_factor)

        # Route by prediction type
        point_est = None
        lower = None
        upper = None
        direction = None
        confidence_prob = 0.5
        reasoning_parts = []

        if prediction_type == 'direction':
            prob = self.core.direction_probability(posterior)
            direction = 'up' if prob > 0.5 else 'down'
            confidence_prob = max(prob, 1 - prob)
            point_est = self.core.point_estimate(posterior, horizon_weeks)
            ci = self.core.credible_interval(posterior, 0.7)
            lower, upper = ci
            reasoning_parts.append(self._build_trend_reasoning(prior, market, metric))

        elif prediction_type == 'time_to_target' and target is not None:
            weeks_est, conf = self.core.time_to_target(posterior, target)
            horizon_weeks = weeks_est
            confidence_prob = conf
            point_est = target
            reasoning_parts.append(
                f"Gap to target: {abs(posterior.mean - target):.0f}. "
                f"Weekly trend: {prior.trend_slope:+.1f}."
            )

        elif prediction_type == 'probability':
            prob = self.core.direction_probability(posterior, threshold=0.0)
            confidence_prob = prob
            point_est = self.core.point_estimate(posterior, horizon_weeks)
            reasoning_parts.append(self._build_trend_reasoning(prior, market, metric))

        elif prediction_type == 'comparison':
            point_est = self.core.point_estimate(posterior, horizon_weeks)
            ci = self.core.credible_interval(posterior, 0.7)
            lower, upper = ci
            confidence_prob = 0.6
            reasoning_parts.append(self._build_trend_reasoning(prior, market, metric))

        else:  # point
            point_est = self.core.point_estimate(posterior, horizon_weeks)
            ci = self.core.credible_interval(posterior, 0.7)
            lower, upper = ci
            prob = self.core.direction_probability(posterior)
            direction = 'up' if prob > 0.5 else 'down'
            confidence_prob = max(prob, 1 - prob)
            reasoning_parts.append(self._build_trend_reasoning(prior, market, metric))

        confidence_level = self.calibrator.confidence_to_language(confidence_prob)
        reasoning = ' '.join(reasoning_parts)

        # Compute outcome week
        outcome_week = self._compute_outcome_week(horizon_weeks)

        result = PredictionResult(
            question=question,
            market=market,
            metric=metric,
            prediction_type=prediction_type,
            point_estimate=point_est,
            lower_bound=lower,
            upper_bound=upper,
            confidence_level=confidence_level,
            confidence_probability=confidence_prob,
            direction=direction,
            horizon_weeks=horizon_weeks,
            reasoning=reasoning,
        )

        # Log to DB
        result.prediction_id = self._log_prediction(result, outcome_week, consumer)

        # Format output
        result.formatted_output = self.formatter.format(result, consumer)

        return result

    def _uncertain_result(self, question: str, parsed, reasoning: str) -> PredictionResult:
        """Return a low-confidence result for edge cases."""
        return PredictionResult(
            question=question,
            market=getattr(parsed, 'market', None) if parsed else None,
            metric=getattr(parsed, 'metric', None) if parsed else None,
            prediction_type='point',
            point_estimate=None,
            lower_bound=None,
            upper_bound=None,
            confidence_level='uncertain',
            confidence_probability=0.5,
            direction=None,
            horizon_weeks=1,
            reasoning=reasoning,
        )

    def _build_trend_reasoning(self, prior, market: str, metric: str) -> str:
        """Build human-readable reasoning from prior state."""
        parts = []
        n = prior.n_observations
        parts.append(f"Based on {n} weeks of {market} {metric} data.")
        if abs(prior.trend_slope) > 0.01:
            direction = 'up' if prior.trend_slope > 0 else 'down'
            parts.append(f"Recent trend: {direction} ~{abs(prior.trend_slope):.1f}/week.")
        else:
            parts.append("Recent trend: flat.")
        return ' '.join(parts)

    def _log_prediction(self, result: PredictionResult, outcome_week: str,
                        consumer: str) -> int:
        """Insert prediction row into DuckDB. Returns prediction ID."""
        _load_db()
        kw = {'db_path': self.db_path} if self.db_path else {}
        try:
            from query import db as _raw_db
            rows = _raw_db(
                "SELECT nextval('predictions_seq') AS id",
                **kw,
            )
            pred_id = rows[0]['id']

            _db_write(
                "INSERT INTO predictions "
                "(id, question, market, metric, prediction_type, point_estimate, "
                "lower_bound, upper_bound, confidence_level, confidence_probability, "
                "direction, horizon_weeks, outcome_week, reasoning, consumer, status) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'pending')",
                params=[
                    pred_id, result.question, result.market, result.metric,
                    result.prediction_type, result.point_estimate,
                    result.lower_bound, result.upper_bound,
                    result.confidence_level, result.confidence_probability,
                    result.direction, result.horizon_weeks,
                    outcome_week, result.reasoning, consumer,
                ],
                **kw,
            )
            return pred_id
        except Exception:
            return None

    def _fetch_actual(self, market: str, metric: str, week: str):
        """Fetch actual value for a market+metric+week from weekly_metrics."""
        if not market or not metric:
            return None
        _load_db()
        kw = {'db_path': self.db_path} if self.db_path else {}
        try:
            row = _market_week(market, week, **kw)
            if row and metric in row:
                return float(row[metric])
        except Exception:
            pass
        return None

    @staticmethod
    def _compute_outcome_week(horizon_weeks: int) -> str:
        """Compute the ISO week string when the outcome will be known."""
        from datetime import timedelta
        target_date = datetime.now() + timedelta(weeks=horizon_weeks)
        iso = target_date.isocalendar()
        return f"{iso[0]} W{iso[1]:02d}"
