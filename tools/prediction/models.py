"""ModelRegistry — per-metric model management.

Manages one model per (market, metric) pair. Lazy creation, in-memory caching,
no disk persistence. Models rebuild from DuckDB data on demand.
"""

import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.expanduser('~/shared/tools/data'))

from .core import BayesianCore
from .types import PriorState

# Lazy DB import
_market_trend = None


def _load_db():
    global _market_trend
    if _market_trend is None:
        from query import market_trend
        _market_trend = market_trend


class BayesianModel:
    """A cached model for a single (market, metric) pair."""

    def __init__(self, market: str, metric: str, prior: PriorState):
        self.market = market
        self.metric = metric
        self.prior = prior
        self.last_updated = datetime.now()

    def to_dict(self) -> dict:
        return {
            'market': self.market,
            'metric': self.metric,
            'n_observations': self.prior.n_observations,
            'mean': self.prior.mean,
            'trend_slope': self.prior.trend_slope,
            'last_updated': self.last_updated.isoformat(),
        }


class ModelRegistry:

    def __init__(self, db_path: str = None):
        self.db_path = db_path
        self._cache: dict[tuple, BayesianModel] = {}
        self._core = BayesianCore()

    def get_model(self, market: str, metric: str) -> BayesianModel:
        """Get or create a model for this market+metric pair.

        Lazy: queries historical data and builds prior on first request.
        Returns cached model on subsequent calls.
        """
        key = (market, metric)
        if key in self._cache:
            return self._cache[key]

        _load_db()
        kw = {'db_path': self.db_path} if self.db_path else {}
        historical = _market_trend(market, weeks=52, **kw)

        prior = self._core.build_prior(historical, metric)
        model = BayesianModel(market=market, metric=metric, prior=prior)
        self._cache[key] = model
        return model

    def invalidate(self, market: str = None, metric: str = None) -> int:
        """Invalidate cached models. Returns count of models removed.

        If both market and metric given: invalidate that specific model.
        If only market: invalidate all models for that market.
        If only metric: invalidate all models for that metric.
        If neither: invalidate everything.
        """
        to_remove = []
        for key in self._cache:
            m, met = key
            if market and metric:
                if m == market and met == metric:
                    to_remove.append(key)
            elif market:
                if m == market:
                    to_remove.append(key)
            elif metric:
                if met == metric:
                    to_remove.append(key)
            else:
                to_remove.append(key)

        for key in to_remove:
            del self._cache[key]
        return len(to_remove)

    def list_models(self) -> list[dict]:
        """List all active cached models with metadata."""
        return [model.to_dict() for model in self._cache.values()]
