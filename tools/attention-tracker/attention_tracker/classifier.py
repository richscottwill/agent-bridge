"""Activity classification engine for the Attention Tracker."""

from __future__ import annotations

import logging
import re
from typing import Sequence

from attention_tracker.models import (
    ActivityEvent,
    ClassificationRule,
    ClassifiedEvent,
    MatchType,
)

logger = logging.getLogger(__name__)


def classify_event(
    event: ActivityEvent,
    rules: Sequence[ClassificationRule],
) -> ClassifiedEvent:
    """Classify an activity event using priority-sorted rules.

    Rules are evaluated in descending priority order (highest priority first).
    The first matching rule wins. Unmatched events are returned as
    "uncategorized" with productivity_score=None.

    Invalid regex patterns are skipped with a warning logged.
    """
    sorted_rules = sorted(rules, key=lambda r: r.priority, reverse=True)

    for rule in sorted_rules:
        try:
            pattern = re.compile(rule.pattern)
        except re.error as exc:
            logger.warning(
                "Skipping rule %r: invalid regex %r (%s)",
                rule.name,
                rule.pattern,
                exc,
            )
            continue

        matched = False

        if rule.match_type is MatchType.WINDOW_CLASS:
            matched = pattern.search(event.window_class) is not None
        elif rule.match_type is MatchType.TITLE_PATTERN:
            matched = pattern.search(event.window_title) is not None
        elif rule.match_type is MatchType.URL_PATTERN:
            if event.url is not None:
                matched = pattern.search(event.url) is not None
        elif rule.match_type is MatchType.APP_NAME:
            matched = pattern.search(event.app_name) is not None

        if matched:
            return ClassifiedEvent(
                event=event,
                category=rule.category,
                productivity_score=rule.productivity_score,
                rule_name=rule.name,
            )

    return ClassifiedEvent(
        event=event,
        category="uncategorized",
        productivity_score=None,
        rule_name="default",
    )
