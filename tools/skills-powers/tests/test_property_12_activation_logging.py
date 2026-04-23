"""
Property 12: ACTIVATION-LOG-APPEND-ONLY

# Feature: skills-powers-adoption, Property 12: Each successful append_* call
# appends exactly one row; log is append-only.

For any random sequence of append calls (activated / missed / correction /
created / pruned):
  - Every call adds exactly one line to activation-log.jsonl.
  - Prior bytes are never rewritten — the log is strictly append-only.
  - Every new line is valid JSON with the required fields for its event type.

Validates: Requirements 6.1, 6.3, 6.4
"""

from __future__ import annotations

import importlib
import json
import shutil
import sys
import tempfile
from pathlib import Path

_PKG_DIR = Path(__file__).resolve().parent.parent
_TEST_DIR = Path(__file__).resolve().parent
for p in (_PKG_DIR, _TEST_DIR):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import pytest
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

import _strategies as gen


@pytest.fixture
def sandbox_home(monkeypatch):
    """Isolated HOME — activation_log writes to ~/shared/context/skills-powers/."""
    tmp = tempfile.mkdtemp(prefix="sp_p12_log_")
    monkeypatch.setenv("HOME", tmp)
    (Path(tmp) / ".kiro" / "skills").mkdir(parents=True)
    (Path(tmp) / ".kiro" / "powers" / "installed").mkdir(parents=True)
    (Path(tmp) / "shared" / "context" / "skills-powers").mkdir(parents=True)
    import activation_log
    import inventory

    importlib.reload(inventory)
    importlib.reload(activation_log)
    yield Path(tmp)
    shutil.rmtree(tmp, ignore_errors=True)
    importlib.reload(inventory)
    importlib.reload(activation_log)


# Required-field map per event type (per design §Data Model → Activation log).
_REQUIRED_FIELDS = {
    "activated": {"event", "kind", "name", "request_summary", "session_id", "ts"},
    "missed-by-feedback": {"event", "kind", "name", "feedback_text", "session_id", "ts"},
    "correction": {"event", "target_ts", "reason", "session_id", "ts"},
    "created": {"event", "subtype", "kind", "name", "session_id", "ts", "overlap_check_ref"},
    "pruned": {"event", "kind", "name", "archive_path", "session_id", "ts"},
}


def _call_logger(log_mod, event: str, kwargs: dict):
    """Dispatch to the correct activation_log.append_* function."""
    if event == "activated":
        return log_mod.append_activated(**kwargs)
    if event == "missed_by_feedback":
        return log_mod.append_missed_by_feedback(**kwargs)
    if event == "correction":
        return log_mod.append_correction(**kwargs)
    if event == "created":
        return log_mod.append_created_event(**kwargs)
    if event == "pruned":
        return log_mod.append_pruned_event(**kwargs)
    raise ValueError(f"unknown event: {event}")


def _read_log_lines(log_path: Path) -> list[str]:
    """Return the current log as a list of raw lines (no trailing newline)."""
    if not log_path.is_file():
        return []
    return log_path.read_text(encoding="utf-8").splitlines()


# ----------------------------------------------------------------------------
# Property 12 — universal: random event sequence preserves append-only invariant
# ----------------------------------------------------------------------------


# Validates: Requirements 6.1, 6.3, 6.4
@given(events=gen.gen_log_event_sequence)
@settings(
    max_examples=120,
    deadline=None,
    suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow],
)
def test_property_12_each_call_appends_one_row(sandbox_home, events):
    """
    Every append_* call adds exactly one line to the log; no prior bytes are
    rewritten; every new line is valid JSON with the required fields.
    """
    import activation_log as al

    log_path = al.LOG_PATH

    # Start fresh for this hypothesis example.
    if log_path.is_file():
        log_path.unlink()

    prior_bytes = b""
    prior_line_count = 0

    for event, kwargs in events:
        # Snapshot before the call.
        before_lines = _read_log_lines(log_path)
        before_bytes = log_path.read_bytes() if log_path.is_file() else b""
        assert len(before_lines) == prior_line_count, (
            f"line count drifted: prior={prior_line_count}, snapshot={len(before_lines)}"
        )

        # Call the logger.
        row = _call_logger(al, event, kwargs)
        assert isinstance(row, dict), f"append_ returned non-dict for {event}"

        # After snapshot.
        after_lines = _read_log_lines(log_path)
        after_bytes = log_path.read_bytes()

        # Line count advanced by exactly 1.
        assert len(after_lines) == prior_line_count + 1, (
            f"event {event!r}: expected {prior_line_count + 1} lines after call, "
            f"got {len(after_lines)}"
        )

        # Append-only: prior bytes survive, prefix-identical.
        assert after_bytes.startswith(before_bytes), (
            f"event {event!r}: prior bytes were rewritten — log is not append-only"
        )

        # New last line is valid JSON.
        new_line = after_lines[-1]
        try:
            parsed = json.loads(new_line)
        except json.JSONDecodeError as e:
            pytest.fail(f"event {event!r}: new line is not valid JSON: {new_line!r} ({e})")

        # Required fields present for this event type.
        actual_event_label = parsed.get("event")
        # Note: missed_by_feedback dispatch ↔ "missed-by-feedback" event label.
        required = _REQUIRED_FIELDS.get(actual_event_label)
        assert required is not None, (
            f"unknown event label emitted: {actual_event_label!r}"
        )
        missing = required - parsed.keys()
        assert not missing, (
            f"event {actual_event_label!r} missing required fields: {missing}"
        )

        # Advance prior state for the next iteration.
        prior_bytes = after_bytes
        prior_line_count += 1


# ----------------------------------------------------------------------------
# Property 12 — focused scenarios
# ----------------------------------------------------------------------------


def test_property_12_empty_log_initially(sandbox_home):
    """With no calls, log does not exist."""
    import activation_log as al

    assert not al.LOG_PATH.is_file()


def test_property_12_activated_roundtrip(sandbox_home):
    """One activated call → one row with the expected shape."""
    import activation_log as al

    row = al.append_activated(
        kind="skill", name="bridge-sync", request_summary="sync body"
    )
    lines = _read_log_lines(al.LOG_PATH)
    assert len(lines) == 1
    parsed = json.loads(lines[0])
    assert parsed["event"] == "activated"
    assert parsed["kind"] == "skill"
    assert parsed["name"] == "bridge-sync"
    assert parsed["request_summary"] == "sync body"
    assert parsed == row


def test_property_12_mixed_event_types_coexist(sandbox_home):
    """All 5 event types can interleave; file is append-only throughout."""
    import activation_log as al

    al.append_activated(kind="skill", name="coach", request_summary="r1")
    al.append_missed_by_feedback(
        kind="skill", name="wbr-callouts", feedback_text="you missed this one"
    )
    al.append_correction(target_ts="2026-04-22T00:00:00+0000", reason="typo")
    al.append_created_event(
        kind="power", name="new-thing", subtype="created",
        overlap_check_ref="~/.kiro/powers/installed/new-thing/overlap-check.json",
    )
    al.append_pruned_event(
        kind="skill", name="obsolete",
        archive_path="~/shared/wiki/agent-created/archive/skills-powers-pruned-2026-04-22/obsolete/",
    )

    lines = _read_log_lines(al.LOG_PATH)
    assert len(lines) == 5
    events = [json.loads(l)["event"] for l in lines]
    assert events == [
        "activated",
        "missed-by-feedback",
        "correction",
        "created",
        "pruned",
    ]


def test_property_12_append_never_rewrites_prior_bytes(sandbox_home):
    """Make 10 sequential appends; snapshot prior bytes survive verbatim."""
    import activation_log as al

    expected_prefix = b""
    for i in range(10):
        before = al.LOG_PATH.read_bytes() if al.LOG_PATH.is_file() else b""
        assert before == expected_prefix
        al.append_activated(
            kind="skill", name=f"skill-{i}", request_summary=f"call {i}"
        )
        after = al.LOG_PATH.read_bytes()
        assert after.startswith(before), (
            f"append #{i}: prior bytes rewritten"
        )
        expected_prefix = after


def test_property_12_all_lines_valid_json_after_many_appends(sandbox_home):
    """After 20 mixed calls, every line in the log parses as valid JSON."""
    import activation_log as al

    for i in range(20):
        if i % 5 == 0:
            al.append_activated(
                kind="skill", name=f"s-{i}", request_summary=f"r-{i}"
            )
        elif i % 5 == 1:
            al.append_missed_by_feedback(
                kind="power", name=f"p-{i}", feedback_text=f"missed {i}"
            )
        elif i % 5 == 2:
            al.append_correction(
                target_ts=f"2026-04-22T00:00:0{i % 10}+0000",
                reason=f"correction {i}",
            )
        elif i % 5 == 3:
            al.append_created_event(
                kind="skill", name=f"new-{i}", subtype="classified",
                overlap_check_ref=None,
            )
        else:
            al.append_pruned_event(
                kind="power", name=f"old-{i}",
                archive_path=f"~/archive/{i}/",
            )
    lines = _read_log_lines(al.LOG_PATH)
    assert len(lines) == 20
    for line in lines:
        parsed = json.loads(line)  # raises if invalid
        assert "event" in parsed
        assert "ts" in parsed
        assert "session_id" in parsed
