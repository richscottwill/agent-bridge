"""Core data types for the Bayesian Prediction Engine."""

from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime


@dataclass
class PriorState:
    """Internal representation of a Bayesian prior. Never exposed to consumers."""
    mean: float
    variance: float
    n_observations: int
    trend_slope: float              # weekly change rate
    trend_confidence: float         # R-squared of trend fit
    seasonality: dict               # week_of_year -> seasonal adjustment factor
    volatility: float               # residual standard deviation
    last_updated: datetime = field(default_factory=datetime.now)


@dataclass
class PosteriorState:
    """Internal representation of updated beliefs. Never exposed to consumers."""
    mean: float
    variance: float
    n_observations: int
    trend_slope: float
    trend_confidence: float
    seasonality: dict
    volatility: float
    calibration_factor: float
    credible_interval_70: tuple
    credible_interval_90: tuple


@dataclass
class ParsedQuestion:
    """Result of parsing a natural-language prediction question."""
    market: Optional[str]
    metric: Optional[str]
    prediction_type: str            # 'point','direction','probability','time_to_target','comparison'
    horizon_weeks: int
    target: Optional[float] = None
    comparison_market: Optional[str] = None
    raw_question: str = ''


@dataclass
class PredictionResult:
    """The output of a prediction. This IS exposed to consumers."""
    question: str
    market: Optional[str]
    metric: Optional[str]
    prediction_type: str
    point_estimate: Optional[float]
    lower_bound: Optional[float]
    upper_bound: Optional[float]
    confidence_level: str
    confidence_probability: float
    direction: Optional[str]
    horizon_weeks: int
    reasoning: str
    formatted_output: Optional[str] = None
    prediction_id: Optional[int] = None


@dataclass
class PredictionScore:
    """Result of scoring a prediction against actuals."""
    prediction_id: int
    actual_value: float
    predicted_value: float
    error_pct: float
    direction_correct: bool
    within_interval: bool
    score: float


@dataclass
class CalibrationReport:
    """Snapshot of engine calibration state."""
    total_predictions: int
    total_scored: int
    mean_error_pct: float
    direction_accuracy: float
    interval_coverage: float
    calibration_score: float
    confidence_adjustment: float
    tier_breakdown: dict = field(default_factory=dict)
