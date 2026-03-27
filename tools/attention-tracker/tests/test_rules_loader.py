"""Tests for the TOML rules loader and validator."""

import os
import textwrap

import pytest

from attention_tracker.models import ClassificationRule, MatchType
from attention_tracker.rules_loader import load_rules, validate_rules


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _write_toml(tmp_path, content: str) -> str:
    """Write TOML content to a temp file and return the path."""
    p = tmp_path / "rules.toml"
    p.write_text(textwrap.dedent(content))
    return str(p)


def _rule(name="test", match_type=MatchType.WINDOW_CLASS, pattern=".*",
          category="cat", score=0.5, priority=5):
    return ClassificationRule(
        name=name, match_type=match_type, pattern=pattern,
        category=category, productivity_score=score, priority=priority,
    )


# ---------------------------------------------------------------------------
# load_rules tests
# ---------------------------------------------------------------------------

class TestLoadRules:
    """Tests for load_rules()."""

    def test_load_single_rule(self, tmp_path):
        path = _write_toml(tmp_path, """\
            [[rules]]
            name = "vscode"
            match_type = "WINDOW_CLASS"
            pattern = "code"
            category = "deep-work"
            productivity_score = 0.9
            priority = 10
        """)
        rules = load_rules(path)
        assert len(rules) == 1
        r = rules[0]
        assert r.name == "vscode"
        assert r.match_type is MatchType.WINDOW_CLASS
        assert r.pattern == "code"
        assert r.category == "deep-work"
        assert r.productivity_score == 0.9
        assert r.priority == 10

    def test_load_multiple_rules(self, tmp_path):
        path = _write_toml(tmp_path, """\
            [[rules]]
            name = "a"
            match_type = "WINDOW_CLASS"
            pattern = "a"
            category = "cat-a"
            productivity_score = 0.1
            priority = 1

            [[rules]]
            name = "b"
            match_type = "URL_PATTERN"
            pattern = "b\\\\.com"
            category = "cat-b"
            productivity_score = 0.8
            priority = 9
        """)
        rules = load_rules(path)
        assert len(rules) == 2
        assert rules[0].name == "a"
        assert rules[1].name == "b"
        assert rules[1].match_type is MatchType.URL_PATTERN

    def test_load_empty_rules_array(self, tmp_path):
        path = _write_toml(tmp_path, "")
        rules = load_rules(path)
        assert rules == []

    def test_file_not_found_raises(self):
        with pytest.raises(FileNotFoundError):
            load_rules("/nonexistent/path/rules.toml")

    def test_missing_field_skipped(self, tmp_path, caplog):
        path = _write_toml(tmp_path, """\
            [[rules]]
            name = "incomplete"
            match_type = "WINDOW_CLASS"
        """)
        rules = load_rules(path)
        assert len(rules) == 0
        assert "Skipping rule" in caplog.text

    def test_invalid_match_type_skipped(self, tmp_path, caplog):
        path = _write_toml(tmp_path, """\
            [[rules]]
            name = "bad-type"
            match_type = "INVALID_TYPE"
            pattern = ".*"
            category = "cat"
            productivity_score = 0.5
            priority = 5
        """)
        rules = load_rules(path)
        assert len(rules) == 0
        assert "Skipping rule" in caplog.text

    def test_score_out_of_range_skipped(self, tmp_path, caplog):
        path = _write_toml(tmp_path, """\
            [[rules]]
            name = "bad-score"
            match_type = "WINDOW_CLASS"
            pattern = ".*"
            category = "cat"
            productivity_score = 1.5
            priority = 5
        """)
        rules = load_rules(path)
        assert len(rules) == 0
        assert "Skipping rule" in caplog.text

    def test_load_default_rules_file(self):
        """The bundled default_rules.toml should load without errors."""
        default_path = os.path.join(
            os.path.dirname(__file__), "..", "attention_tracker", "default_rules.toml"
        )
        rules = load_rules(default_path)
        assert len(rules) >= 4  # at least code-editors, google-docs, slack, social-media
        errors = validate_rules(rules)
        assert errors == []

    def test_all_four_match_types_supported(self, tmp_path):
        content = ""
        for mt in MatchType:
            content += f"""\
[[rules]]
name = "rule-{mt.value}"
match_type = "{mt.value}"
pattern = "test"
category = "cat"
productivity_score = 0.5
priority = 5

"""
        path = _write_toml(tmp_path, content)
        rules = load_rules(path)
        assert len(rules) == len(MatchType)


# ---------------------------------------------------------------------------
# validate_rules tests
# ---------------------------------------------------------------------------

class TestValidateRules:
    """Tests for validate_rules()."""

    def test_valid_rules_return_empty(self):
        rules = [
            _rule(name="a", pattern="(foo|bar)", score=0.0),
            _rule(name="b", pattern="baz\\.com", score=1.0),
        ]
        assert validate_rules(rules) == []

    def test_invalid_regex_reported(self):
        rules = [_rule(name="bad-regex", pattern="[invalid(")]
        errors = validate_rules(rules)
        assert len(errors) == 1
        assert "bad-regex" in errors[0]
        assert "invalid regex" in errors[0]

    def test_score_below_zero_reported(self):
        rules = [_rule(name="neg", score=-0.1)]
        errors = validate_rules(rules)
        assert len(errors) == 1
        assert "neg" in errors[0]
        assert "out of range" in errors[0]

    def test_score_above_one_reported(self):
        rules = [_rule(name="high", score=1.01)]
        errors = validate_rules(rules)
        assert len(errors) == 1
        assert "high" in errors[0]

    def test_multiple_errors_collected(self):
        rules = [
            _rule(name="bad1", pattern="[bad(", score=0.5),
            _rule(name="bad2", pattern="ok", score=2.0),
        ]
        errors = validate_rules(rules)
        assert len(errors) == 2

    def test_boundary_scores_valid(self):
        rules = [
            _rule(name="zero", score=0.0),
            _rule(name="one", score=1.0),
        ]
        assert validate_rules(rules) == []
