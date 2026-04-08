"""Core data types for the Bayesian Prediction Engine."""

from dataclasses import dataclass, field
from typing import Optional, List
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


# ── Pipeline-specific dataclasses ──────────────────────────────────────────


@dataclass
class SegmentForecast:
    """Forecast for one segment (Brand or NB).

    Redefined here to avoid import dependency on project.py.
    """
    regs: float
    cost: float
    cpa: float
    clicks: float


@dataclass
class MarketProjection:
    """Full projection for one market at one horizon."""
    market: str
    brand: SegmentForecast
    nb: SegmentForecast
    total_regs: float
    total_cost: float
    ci_regs_low: float
    ci_regs_high: float
    vs_op2_spend_pct: Optional[float]
    method: str
    week: str
    # Monthly pacing fields (populated when monthly data available)
    mtd_regs: Optional[float] = None
    mtd_cost: Optional[float] = None
    monthly_op2_regs: Optional[float] = None
    monthly_op2_cost: Optional[float] = None
    pacing_regs_pct: Optional[float] = None
    pacing_cost_pct: Optional[float] = None


@dataclass
class ScoringResult:
    """Result of scoring prior predictions against actuals."""
    predictions_scored: int
    hits: int
    misses: int
    surprises: int
    mean_error_pct: float
    calibration: float  # calibration_factor from Calibrator


@dataclass
class PipelineResult:
    """Summary of a full pipeline run."""
    week: str
    xlsx_path: str
    stages_completed: List[str] = field(default_factory=list)
    stages_failed: List[str] = field(default_factory=list)
    markets_processed: List[str] = field(default_factory=list)
    rows_loaded: int = 0
    predictions_scored: int = 0
    projections_written: int = 0
    calibration: float = 1.0
    dive_updated: bool = False
    duration_seconds: float = 0.0
    errors: List[str] = field(default_factory=list)
