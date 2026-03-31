"""Formatter — translates PredictionResult into consumer-appropriate output.

Human consumers get natural language in Richard's voice: direct, concise,
data-grounded. No hedging, no filler, no statistical jargon — ever.

Agent consumers get structured dicts with all numeric fields.
"""

from .types import PredictionResult

# These terms MUST NEVER appear in human-facing output
BANNED_TERMS = [
    'posterior', 'prior', 'conjugate', 'credible interval', 'p-value',
    'distribution', 'variance', 'standard deviation', 'bayesian',
    'normal-gamma', 'hypothesis test', 'significance level',
]

# Map internal confidence levels to plain English
CONFIDENCE_ENGLISH = {
    'very_likely': 'very likely',
    'likely': 'likely',
    'leaning_toward': 'leaning toward yes',
    'uncertain': 'uncertain',
    'leaning_against': 'leaning against',
    'unlikely': 'unlikely',
    'very_unlikely': 'very unlikely',
}


class Formatter:

    def format(self, result: PredictionResult, consumer: str = 'human') -> str | dict:
        """Format prediction for the given consumer type.

        'human': natural language with reasoning, confidence in plain English.
        'agent': structured dict with all numeric fields.
        """
        if consumer == 'agent':
            return self._format_agent(result)
        return self._format_human(result)

    def _format_agent(self, result: PredictionResult) -> dict:
        """Structured dict for agent consumers."""
        return {
            'question': result.question,
            'market': result.market,
            'metric': result.metric,
            'prediction_type': result.prediction_type,
            'point_estimate': result.point_estimate,
            'lower_bound': result.lower_bound,
            'upper_bound': result.upper_bound,
            'confidence_level': result.confidence_level,
            'confidence_probability': result.confidence_probability,
            'direction': result.direction,
            'horizon_weeks': result.horizon_weeks,
            'reasoning': result.reasoning,
            'prediction_id': result.prediction_id,
        }

    def _format_human(self, result: PredictionResult) -> str:
        """Natural language output. Direct, concise, data-grounded."""
        conf = CONFIDENCE_ENGLISH.get(result.confidence_level, result.confidence_level)
        market = result.market or ''
        metric = result.metric or 'metric'

        parts = []

        if result.prediction_type == 'direction':
            direction_word = result.direction or 'flat'
            if result.point_estimate is not None:
                parts.append(
                    f"{market} {metric} are {conf} {direction_word} next week "
                    f"(~{self._fmt_num(result.point_estimate)})."
                )
            else:
                parts.append(f"{market} {metric} are {conf} {direction_word} next week.")

        elif result.prediction_type == 'time_to_target':
            weeks = result.horizon_weeks
            if weeks == 0:
                parts.append(f"{market} {metric} already at target.")
            else:
                parts.append(
                    f"At current pace, {market} {metric} — roughly {weeks} weeks out. "
                    f"Confidence: {conf}."
                )

        elif result.prediction_type == 'probability':
            prob_pct = round(result.confidence_probability * 100)
            parts.append(
                f"{conf.capitalize()}, about {prob_pct}% chance. "
            )

        elif result.prediction_type == 'comparison':
            if result.point_estimate is not None:
                parts.append(
                    f"Expected impact: ~{self._fmt_num(result.point_estimate)}. "
                    f"Confidence: {conf}."
                )
            else:
                parts.append(f"Comparison result: {conf}.")

        else:  # point estimate
            if result.point_estimate is not None:
                est = self._fmt_num(result.point_estimate)
                line = f"{market} {metric} tracking toward ~{est}"
                if result.lower_bound is not None and result.upper_bound is not None:
                    line += (
                        f" (range: {self._fmt_num(result.lower_bound)}"
                        f"–{self._fmt_num(result.upper_bound)})"
                    )
                line += f". Confidence: {conf}."
                parts.append(line)
            else:
                parts.append(f"{market} {metric}: {conf}.")

        # Add reasoning
        if result.reasoning:
            parts.append(result.reasoning)

        output = ' '.join(parts).strip()
        self._verify_no_jargon(output)
        return output

    def format_alert(self, result: PredictionResult) -> str:
        """Concise one-liner for morning routine alerts."""
        market = result.market or ''
        metric = result.metric or 'metric'
        conf = CONFIDENCE_ENGLISH.get(result.confidence_level, result.confidence_level)

        if result.point_estimate is not None and result.direction:
            alert = (
                f"{market} {metric} {result.direction} "
                f"(~{self._fmt_num(result.point_estimate)}), {conf}"
            )
        elif result.point_estimate is not None:
            alert = f"{market} {metric} ~{self._fmt_num(result.point_estimate)}, {conf}"
        else:
            alert = f"{market} {metric}: {conf}"

        self._verify_no_jargon(alert)
        return alert

    def format_autonomy_report(self, current: dict, trajectory: list,
                                predictions: list) -> str:
        """Format autonomy measurement report. Direct, no fluff."""
        parts = []

        # Current ratios
        agentic = current.get('pct_fully_agentic', 0)
        mixed = current.get('pct_mixed', 0)
        human = current.get('pct_human_only', 0)
        parts.append(
            f"Autonomy: {agentic:.0f}% fully agentic, "
            f"{mixed:.0f}% mixed, {human:.0f}% human-only."
        )

        # Trajectory summary
        if trajectory and len(trajectory) >= 2:
            first = trajectory[0]
            last = trajectory[-1]
            delta = (last.get('pct_fully_agentic', 0) - first.get('pct_fully_agentic', 0))
            direction = 'up' if delta > 0 else 'down' if delta < 0 else 'flat'
            parts.append(
                f"Trend over {len(trajectory)} periods: {direction} {abs(delta):.1f}pp."
            )

        # Predictions
        for pred in (predictions or []):
            if pred.formatted_output:
                parts.append(pred.formatted_output)
            elif pred.reasoning:
                parts.append(pred.reasoning)

        output = ' '.join(parts).strip()
        self._verify_no_jargon(output)
        return output

    @staticmethod
    def _fmt_num(value: float) -> str:
        """Format number for human readability."""
        if value is None:
            return '?'
        if abs(value) >= 1_000_000:
            return f"${value / 1_000_000:.1f}M"
        if abs(value) >= 1_000:
            return f"{value:,.0f}"
        if abs(value) >= 10:
            return f"{value:.0f}"
        return f"{value:.2f}"

    @staticmethod
    def _verify_no_jargon(text: str):
        """Assert no banned statistical terms appear in human output."""
        lower = text.lower()
        for term in BANNED_TERMS:
            if term in lower:
                raise ValueError(
                    f"Jargon leak: '{term}' found in human output. "
                    f"Rewrite without statistical terminology."
                )
