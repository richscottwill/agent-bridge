"""BayesianCore — the statistical inference engine.

Builds priors from historical data, updates with new evidence, produces
posterior estimates with credible intervals. All functions are pure —
no side effects, no DB access. The Bayesian machinery is invisible to consumers.
"""

import math
from .types import PriorState, PosteriorState


class BayesianCore:

    def build_prior(self, historical: list, metric: str) -> PriorState:
        """Build prior from historical data.

        Extracts: mean, variance, trend (OLS), volatility (RMSE of residuals).
        Returns uninformative prior when < 3 data points.
        Extracts seasonality when >= 52 weeks available.
        """
        values = []
        for row in historical:
            v = row.get(metric)
            if v is not None:
                try:
                    values.append(float(v))
                except (ValueError, TypeError):
                    pass

        if len(values) < 3:
            return PriorState(
                mean=values[0] if values else 0.0,
                variance=1e6,
                n_observations=len(values),
                trend_slope=0.0,
                trend_confidence=0.0,
                seasonality={},
                volatility=1e3,
            )

        n = len(values)
        mean = sum(values) / n
        variance = sum((v - mean) ** 2 for v in values) / (n - 1) if n > 1 else 1e6

        # Trend: OLS linear regression on index
        indices = list(range(n))
        x_mean = sum(indices) / n
        ss_xy = sum((i - x_mean) * (v - mean) for i, v in zip(indices, values))
        ss_xx = sum((i - x_mean) ** 2 for i in indices)
        trend_slope = ss_xy / ss_xx if ss_xx > 0 else 0.0

        # R-squared for trend confidence
        predicted = [mean + trend_slope * (i - x_mean) for i in indices]
        ss_res = sum((v - p) ** 2 for v, p in zip(values, predicted))
        ss_tot = sum((v - mean) ** 2 for v in values)
        trend_confidence = max(0.0, 1.0 - (ss_res / ss_tot)) if ss_tot > 0 else 0.0

        # Volatility: RMSE of residuals
        residuals = [v - p for v, p in zip(values, predicted)]
        volatility = (sum(r ** 2 for r in residuals) / max(1, n - 2)) ** 0.5

        # Seasonality: week-of-year patterns when 52+ weeks available
        seasonality = {}
        if n >= 52:
            # Group values by position mod 52 (approximate week-of-year)
            week_buckets = {}
            for i, v in enumerate(values):
                woy = i % 52
                if woy not in week_buckets:
                    week_buckets[woy] = []
                week_buckets[woy].append(v)
            for woy, bucket in week_buckets.items():
                bucket_mean = sum(bucket) / len(bucket)
                seasonality[woy] = bucket_mean / mean if mean != 0 else 1.0

        return PriorState(
            mean=mean, variance=variance, n_observations=n,
            trend_slope=trend_slope, trend_confidence=trend_confidence,
            seasonality=seasonality, volatility=volatility,
        )

    def update_posterior(self, prior: PriorState, new_evidence: list,
                         calibration_factor: float = 1.0) -> PosteriorState:
        """Conjugate Normal update. calibration_factor widens/tightens intervals."""
        if not new_evidence:
            adjusted_vol = prior.volatility * calibration_factor
            ci_70 = (prior.mean - 1.04 * adjusted_vol, prior.mean + 1.04 * adjusted_vol)
            ci_90 = (prior.mean - 1.645 * adjusted_vol, prior.mean + 1.645 * adjusted_vol)
            return PosteriorState(
                mean=prior.mean, variance=prior.variance,
                n_observations=prior.n_observations, trend_slope=prior.trend_slope,
                trend_confidence=prior.trend_confidence, seasonality=prior.seasonality,
                volatility=prior.volatility, calibration_factor=calibration_factor,
                credible_interval_70=ci_70, credible_interval_90=ci_90,
            )

        # Extract numeric values from evidence
        metric_values = []
        for row in new_evidence:
            if isinstance(row, dict):
                # Try common metric keys
                for key in ('value', 'regs', 'spend', 'cpa', 'cvr', 'clicks', 'cpc'):
                    v = row.get(key)
                    if v is not None:
                        try:
                            metric_values.append(float(v))
                        except (ValueError, TypeError):
                            pass
                        break
            elif isinstance(row, (int, float)):
                metric_values.append(float(row))

        if not metric_values:
            return self.update_posterior(prior, [], calibration_factor)

        n_new = len(metric_values)
        new_mean = sum(metric_values) / n_new

        # Weighted combination of prior and evidence
        prior_weight = prior.n_observations
        total_weight = prior_weight + n_new
        posterior_mean = (prior_weight * prior.mean + n_new * new_mean) / total_weight

        # Posterior variance (pooled)
        new_var = sum((v - new_mean) ** 2 for v in metric_values) / n_new if n_new > 1 else prior.variance
        posterior_variance = (
            (prior_weight * prior.variance + n_new * new_var) / total_weight
            + (prior_weight * n_new * (prior.mean - new_mean) ** 2) / (total_weight ** 2)
        )

        # Trend: blend 60% recent, 40% prior when 3+ evidence points
        posterior_trend = prior.trend_slope
        if n_new >= 3:
            recent_indices = list(range(n_new))
            rx_mean = sum(recent_indices) / n_new
            ss_xy = sum((i - rx_mean) * (v - new_mean) for i, v in zip(recent_indices, metric_values))
            ss_xx = sum((i - rx_mean) ** 2 for i in recent_indices)
            recent_trend = ss_xy / ss_xx if ss_xx > 0 else 0.0
            posterior_trend = 0.6 * recent_trend + 0.4 * prior.trend_slope

        # Posterior volatility
        posterior_volatility = (prior.volatility * prior_weight + (new_var ** 0.5) * n_new) / total_weight
        adjusted_vol = posterior_volatility * calibration_factor

        ci_70 = (posterior_mean - 1.04 * adjusted_vol, posterior_mean + 1.04 * adjusted_vol)
        ci_90 = (posterior_mean - 1.645 * adjusted_vol, posterior_mean + 1.645 * adjusted_vol)

        return PosteriorState(
            mean=posterior_mean, variance=posterior_variance,
            n_observations=total_weight, trend_slope=posterior_trend,
            trend_confidence=prior.trend_confidence, seasonality=prior.seasonality,
            volatility=posterior_volatility, calibration_factor=calibration_factor,
            credible_interval_70=ci_70, credible_interval_90=ci_90,
        )

    def point_estimate(self, posterior: PosteriorState, horizon: int = 1) -> float:
        """Project forward by horizon weeks using trend."""
        return posterior.mean + posterior.trend_slope * horizon

    def credible_interval(self, posterior: PosteriorState, level: float = 0.7) -> tuple:
        """Credible interval at given confidence level."""
        # Map common levels to z-scores (Normal approximation)
        z_map = {0.5: 0.674, 0.7: 1.04, 0.8: 1.28, 0.9: 1.645, 0.95: 1.96, 0.99: 2.576}
        z = z_map.get(level)
        if z is None:
            # Approximate: inverse normal CDF via rational approximation
            p = (1 + level) / 2
            t = math.sqrt(-2 * math.log(1 - p)) if p < 1 else 3.0
            z = t - (2.515517 + 0.802853 * t + 0.010328 * t * t) / (
                1 + 1.432788 * t + 0.189269 * t * t + 0.001308 * t * t * t)
            z = max(0.5, min(z, 3.5))

        adjusted_vol = posterior.volatility * posterior.calibration_factor
        half_width = z * adjusted_vol
        return (posterior.mean - half_width, posterior.mean + half_width)

    def direction_probability(self, posterior: PosteriorState, threshold: float = 0.0) -> float:
        """Probability that next value exceeds current mean + threshold."""
        adjusted_vol = posterior.volatility * posterior.calibration_factor
        if adjusted_vol <= 0:
            return 0.5

        # Project forward one step with trend
        projected = posterior.mean + posterior.trend_slope
        # Z-score for threshold relative to projected value
        z = (projected - (posterior.mean + threshold)) / adjusted_vol

        # Normal CDF approximation (Abramowitz and Stegun)
        return self._normal_cdf(z)

    def time_to_target(self, posterior: PosteriorState, target: float,
                       max_weeks: int = 26) -> tuple:
        """Estimated weeks to reach target, with confidence.

        Returns (estimated_weeks, confidence_probability).
        If target is unreachable within max_weeks, returns (max_weeks, low_confidence).
        """
        if posterior.trend_slope == 0:
            # No trend — can't predict convergence
            return (max_weeks, 0.15)

        current = posterior.mean
        gap = target - current

        # If already at or past target
        if (posterior.trend_slope > 0 and gap <= 0) or (posterior.trend_slope < 0 and gap >= 0):
            return (0, 0.90)

        # If trend is moving away from target
        if (gap > 0 and posterior.trend_slope < 0) or (gap < 0 and posterior.trend_slope > 0):
            return (max_weeks, 0.10)

        weeks_est = abs(gap / posterior.trend_slope)
        weeks_est = min(weeks_est, max_weeks)

        # Confidence decreases with distance
        adjusted_vol = posterior.volatility * posterior.calibration_factor
        if adjusted_vol > 0:
            uncertainty = adjusted_vol * math.sqrt(weeks_est) / abs(gap) if gap != 0 else 1.0
            confidence = max(0.15, min(0.90, 1.0 - uncertainty))
        else:
            confidence = 0.70

        return (int(round(weeks_est)), confidence)

    @staticmethod
    def _normal_cdf(z: float) -> float:
        """Standard normal CDF approximation (Abramowitz and Stegun)."""
        if z > 6:
            return 1.0
        if z < -6:
            return 0.0
        b1, b2, b3, b4, b5 = 0.319381530, -0.356563782, 1.781477937, -1.821255978, 1.330274429
        p = 0.2316419
        t = 1.0 / (1.0 + p * abs(z))
        poly = t * (b1 + t * (b2 + t * (b3 + t * (b4 + t * b5))))
        pdf = math.exp(-0.5 * z * z) / math.sqrt(2 * math.pi)
        if z >= 0:
            return 1.0 - pdf * poly
        else:
            return pdf * poly
