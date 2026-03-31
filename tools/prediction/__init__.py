"""Bayesian Prediction Engine for PS Analytics.

Usage:
    from prediction import PredictionEngine, AutonomyTracker
    engine = PredictionEngine()
    result = engine.predict("Will AU regs be up next week?")
"""

from .types import (
    PriorState, PosteriorState, ParsedQuestion,
    PredictionResult, PredictionScore, CalibrationReport,
)

# Lazy imports to avoid circular dependencies — engine/autonomy import on first use
__all__ = [
    'PredictionEngine', 'AutonomyTracker',
    'PriorState', 'PosteriorState', 'ParsedQuestion',
    'PredictionResult', 'PredictionScore', 'CalibrationReport',
]


def __getattr__(name):
    if name == 'PredictionEngine':
        from .engine import PredictionEngine
        return PredictionEngine
    if name == 'AutonomyTracker':
        from .autonomy import AutonomyTracker
        return AutonomyTracker
    raise AttributeError(f"module 'prediction' has no attribute {name}")
