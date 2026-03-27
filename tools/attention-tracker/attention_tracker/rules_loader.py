"""Load and validate classification rules from TOML files."""

from __future__ import annotations

import logging
import re
from typing import Any

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib  # type: ignore[no-redef]

from attention_tracker.models import ClassificationRule, MatchType

logger = logging.getLogger(__name__)

_VALID_MATCH_TYPES = {m.value for m in MatchType}
_REQUIRED_FIELDS = ("name", "match_type", "pattern", "category", "productivity_score", "priority")


def load_rules(path: str) -> list[ClassificationRule]:
    """Read a TOML rules file and return parsed ClassificationRule objects.

    Raises FileNotFoundError if *path* does not exist.
    Raises ValueError for structural TOML issues (missing [[rules]] array).
    Individual rule parse errors are logged and the rule is skipped.
    """
    with open(path, "rb") as fh:
        data = tomllib.load(fh)

    raw_rules: list[dict[str, Any]] = data.get("rules", [])
    if not isinstance(raw_rules, list):
        raise ValueError(f"Expected [[rules]] array in {path}")

    results: list[ClassificationRule] = []
    for idx, raw in enumerate(raw_rules):
        try:
            rule = _parse_rule(raw, idx)
            results.append(rule)
        except (KeyError, ValueError, TypeError) as exc:
            logger.warning("Skipping rule #%d in %s: %s", idx, path, exc)

    return results


def _parse_rule(raw: dict[str, Any], idx: int) -> ClassificationRule:
    """Convert a raw TOML dict into a ClassificationRule."""
    for field in _REQUIRED_FIELDS:
        if field not in raw:
            raise KeyError(f"Missing required field '{field}' in rule #{idx}")

    match_type_str = raw["match_type"]
    if match_type_str not in _VALID_MATCH_TYPES:
        raise ValueError(
            f"Invalid match_type '{match_type_str}' in rule #{idx}; "
            f"expected one of {sorted(_VALID_MATCH_TYPES)}"
        )

    score = float(raw["productivity_score"])
    if not (0.0 <= score <= 1.0):
        raise ValueError(
            f"productivity_score {score} out of range [0.0, 1.0] in rule #{idx}"
        )

    return ClassificationRule(
        name=str(raw["name"]),
        match_type=MatchType(match_type_str),
        pattern=str(raw["pattern"]),
        category=str(raw["category"]),
        productivity_score=score,
        priority=int(raw["priority"]),
    )


def validate_rules(rules: list[ClassificationRule]) -> list[str]:
    """Return a list of error messages for the given rules. Empty means valid.

    Checks:
    - Valid regex pattern
    - Valid match_type enum value
    - productivity_score in [0.0, 1.0]
    - Required fields present (implicitly satisfied by ClassificationRule dataclass)
    """
    errors: list[str] = []
    for rule in rules:
        # Regex validity
        try:
            re.compile(rule.pattern)
        except re.error as exc:
            errors.append(f"Rule '{rule.name}': invalid regex '{rule.pattern}' — {exc}")

        # match_type validity
        if rule.match_type.value not in _VALID_MATCH_TYPES:
            errors.append(
                f"Rule '{rule.name}': invalid match_type '{rule.match_type}'"
            )

        # Score bounds
        if not (0.0 <= rule.productivity_score <= 1.0):
            errors.append(
                f"Rule '{rule.name}': productivity_score {rule.productivity_score} "
                f"out of range [0.0, 1.0]"
            )

    return errors
