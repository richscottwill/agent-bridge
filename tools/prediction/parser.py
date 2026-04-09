"""Question parser — extracts structured prediction requests from natural language.

Parses market codes, metric keywords, prediction types, and horizons from
free-text questions. Accepts optional context dict to override parsed values.
"""

import re
from .ptypes import ParsedQuestion

# Valid market codes
MARKET_CODES = ['US', 'CA', 'UK', 'DE', 'FR', 'IT', 'ES', 'JP', 'AU', 'MX']

# Metric keyword mapping: canonical name → aliases
METRIC_KEYWORDS = {
    'regs': ['regs', 'registrations', 'registration'],
    'spend': ['spend', 'cost', 'budget', 'spending'],
    'cpa': ['cpa', 'cost per acquisition', 'cost per reg'],
    'cvr': ['cvr', 'conversion', 'conversion rate'],
    'clicks': ['clicks', 'traffic', 'click'],
    'cpc': ['cpc', 'cost per click'],
}


def parse_question(question: str, context: dict = None) -> ParsedQuestion:
    """Parse a natural-language prediction question into structured fields.

    Args:
        question: Free-text question (e.g., "Will AU regs be up next week?")
        context: Optional dict to override parsed values. Keys: market, metric,
                 prediction_type, horizon_weeks, target, comparison_market.

    Returns:
        ParsedQuestion with extracted/overridden fields.
    """
    context = context or {}
    q_upper = question.upper()
    q_lower = question.lower()

    # --- Market extraction ---
    market = None
    for code in MARKET_CODES:
        # Match as whole word to avoid false positives (e.g., "IT" in "it")
        if re.search(r'\b' + code + r'\b', q_upper):
            market = code
            break
    if context.get('market'):
        market = context['market']

    # --- Metric extraction ---
    metric = None
    for canonical, aliases in METRIC_KEYWORDS.items():
        for alias in aliases:
            if re.search(r'\b' + re.escape(alias) + r'\b', q_lower):
                metric = canonical
                break
        if metric:
            break
    if context.get('metric'):
        metric = context['metric']

    # --- Prediction type classification ---
    prediction_type = 'point'  # default
    if 'up or down' in q_lower or 'up/down' in q_lower:
        prediction_type = 'direction'
    elif 'how many weeks' in q_lower or 'how long' in q_lower or 'when will' in q_lower:
        prediction_type = 'time_to_target'
    elif 'probability' in q_lower or 'chance' in q_lower or 'likelihood' in q_lower:
        prediction_type = 'probability'
    elif 'if we launch' in q_lower or 'compared to' in q_lower or 'vs' in q_lower:
        prediction_type = 'comparison'
    if context.get('prediction_type'):
        prediction_type = context['prediction_type']

    # --- Horizon extraction ---
    horizon = 1
    if 'next month' in q_lower:
        horizon = 4
    else:
        m = re.search(r'next\s+(\d+)\s+weeks?', q_lower)
        if m:
            horizon = int(m.group(1))
    if context.get('horizon_weeks') is not None:
        horizon = context['horizon_weeks']

    # --- Target extraction (for time_to_target / probability) ---
    target = None
    m = re.search(r'(?:under|below|above|over|reach|hit|target)\s+\$?([\d,]+(?:\.\d+)?)', q_lower)
    if m:
        target = float(m.group(1).replace(',', ''))
    if context.get('target') is not None:
        target = context['target']

    # --- Comparison market ---
    comparison_market = context.get('comparison_market')

    return ParsedQuestion(
        market=market,
        metric=metric,
        prediction_type=prediction_type,
        horizon_weeks=horizon,
        target=target,
        comparison_market=comparison_market,
        raw_question=question,
    )
