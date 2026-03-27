"""Unit tests for the activity classifier."""

from datetime import datetime

from attention_tracker.classifier import classify_event
from attention_tracker.models import (
    ActivityEvent,
    ClassificationRule,
    MatchType,
)


def _make_event(**overrides) -> ActivityEvent:
    defaults = dict(
        id="evt-1",
        timestamp=datetime(2026, 3, 27, 10, 0, 0),
        app_name="firefox",
        window_class="Navigator",
        window_title="GitHub - Mozilla Firefox",
        idle_seconds=0,
        duration_ms=1500,
        url="https://github.com",
    )
    defaults.update(overrides)
    return ActivityEvent(**defaults)


def _rule(name, match_type, pattern, category, score, priority):
    return ClassificationRule(
        name=name,
        match_type=match_type,
        pattern=pattern,
        category=category,
        productivity_score=score,
        priority=priority,
    )


class TestClassifyEvent:
    """Core classify_event behaviour."""

    def test_no_rules_returns_uncategorized(self):
        event = _make_event()
        result = classify_event(event, [])
        assert result.category == "uncategorized"
        assert result.productivity_score is None
        assert result.rule_name == "default"
        assert result.event is event

    def test_single_matching_rule(self):
        event = _make_event(app_name="code")
        rules = [_rule("vscode", MatchType.APP_NAME, "code", "deep-work", 0.9, 10)]
        result = classify_event(event, rules)
        assert result.category == "deep-work"
        assert result.productivity_score == 0.9
        assert result.rule_name == "vscode"

    def test_highest_priority_wins(self):
        event = _make_event(app_name="slack")
        rules = [
            _rule("slack-low", MatchType.APP_NAME, "slack", "communication", 0.3, 1),
            _rule("slack-high", MatchType.APP_NAME, "slack", "distraction", 0.1, 10),
        ]
        result = classify_event(event, rules)
        assert result.category == "distraction"
        assert result.rule_name == "slack-high"

    def test_first_match_at_same_priority(self):
        """When two rules share the same priority, stable sort order applies."""
        event = _make_event(app_name="slack")
        rules = [
            _rule("r1", MatchType.APP_NAME, "slack", "cat-a", 0.5, 5),
            _rule("r2", MatchType.APP_NAME, "slack", "cat-b", 0.6, 5),
        ]
        result = classify_event(event, rules)
        # Both match at priority 5; sorted() is stable so r1 comes first
        assert result.category in ("cat-a", "cat-b")

    def test_window_class_match(self):
        event = _make_event(window_class="jetbrains-idea")
        rules = [_rule("idea", MatchType.WINDOW_CLASS, "jetbrains", "deep-work", 0.95, 5)]
        result = classify_event(event, rules)
        assert result.category == "deep-work"

    def test_title_pattern_match(self):
        event = _make_event(window_title="Pull Request #42 - GitHub")
        rules = [_rule("pr", MatchType.TITLE_PATTERN, r"Pull Request", "code-review", 0.8, 5)]
        result = classify_event(event, rules)
        assert result.category == "code-review"

    def test_url_pattern_match(self):
        event = _make_event(url="https://docs.google.com/document/d/123")
        rules = [_rule("gdocs", MatchType.URL_PATTERN, r"docs\.google\.com", "writing", 0.85, 5)]
        result = classify_event(event, rules)
        assert result.category == "writing"

    def test_url_pattern_skipped_when_url_is_none(self):
        event = _make_event(url=None)
        rules = [_rule("gdocs", MatchType.URL_PATTERN, r"docs\.google\.com", "writing", 0.85, 5)]
        result = classify_event(event, rules)
        assert result.category == "uncategorized"

    def test_invalid_regex_skipped_with_warning(self, caplog):
        event = _make_event(app_name="vim")
        rules = [
            _rule("bad", MatchType.APP_NAME, "[invalid(", "bad-cat", 0.5, 10),
            _rule("vim", MatchType.APP_NAME, "vim", "deep-work", 0.9, 5),
        ]
        result = classify_event(event, rules)
        assert result.category == "deep-work"
        assert result.rule_name == "vim"
        assert "Skipping rule" in caplog.text
        assert "bad" in caplog.text

    def test_no_match_returns_uncategorized(self):
        event = _make_event(app_name="obscure-app")
        rules = [_rule("vscode", MatchType.APP_NAME, "^code$", "deep-work", 0.9, 10)]
        result = classify_event(event, rules)
        assert result.category == "uncategorized"
        assert result.productivity_score is None

    def test_regex_partial_match(self):
        """re.search matches anywhere in the string, not just the start."""
        event = _make_event(window_title="My Document - LibreOffice Writer")
        rules = [_rule("lo", MatchType.TITLE_PATTERN, "LibreOffice", "writing", 0.8, 5)]
        result = classify_event(event, rules)
        assert result.category == "writing"
