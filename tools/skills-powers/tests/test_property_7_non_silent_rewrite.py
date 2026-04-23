"""
Property 7: NON-SILENT-REWRITE

# Feature: skills-powers-adoption, Property 7: Malformed file produces error
# AND file is unchanged on disk.

For any malformed SKILL.md / POWER.md content:
  - validators.format_compliance_check() returns valid=False with a
    descriptive violation.
  - The file's bytes on disk are IDENTICAL before and after the call.
  - The file's mtime is unchanged.
  - file_unchanged=True in the result.

Generator covers: missing frontmatter fence, unclosed frontmatter fence,
malformed YAML (double colons, tab-indented), frontmatter-is-list or scalar,
current-status missing required fields, and unclosed quotes.

Also confirms unknown fields are preserved (not dropped) on valid files.

Validates: Requirements 9.4, 9.5
"""

from __future__ import annotations

import importlib
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
    """Isolated HOME for the format-compliance validator."""
    tmp = tempfile.mkdtemp(prefix="sp_p7_nonsilent_")
    monkeypatch.setenv("HOME", tmp)
    (Path(tmp) / ".kiro" / "skills").mkdir(parents=True)
    (Path(tmp) / ".kiro" / "powers" / "installed").mkdir(parents=True)
    (Path(tmp) / "shared" / "context" / "skills-powers").mkdir(parents=True)
    import inventory
    import validators

    importlib.reload(inventory)
    importlib.reload(validators)
    yield Path(tmp)
    shutil.rmtree(tmp, ignore_errors=True)
    importlib.reload(inventory)
    importlib.reload(validators)


def _write_skill(sandbox: Path, name: str, text: str) -> Path:
    d = sandbox / ".kiro" / "skills" / name
    d.mkdir(parents=True, exist_ok=True)
    path = d / "SKILL.md"
    path.write_bytes(text.encode("utf-8"))
    return path


def _snapshot(path: Path) -> tuple[bytes, float]:
    """Capture bytes + mtime for later equality check."""
    return path.read_bytes(), path.stat().st_mtime


# ----------------------------------------------------------------------------
# Property 7 — malformed files are reported but never rewritten
# ----------------------------------------------------------------------------


# Validates: Requirements 9.4, 9.5
@given(malformed=gen.gen_malformed_skill_file())
@settings(
    max_examples=120,
    deadline=None,
    suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow],
)
def test_property_7_malformed_file_unchanged(sandbox_home, malformed):
    """For every malformed shape, the file is reported invalid and not rewritten."""
    import validators as vd

    shape, text = malformed
    # Use a unique name per call to avoid path collisions across iterations.
    name = f"malformed-{abs(hash(text)) % 10_000}"
    path = _write_skill(sandbox_home, name, text)

    bytes_before, mtime_before = _snapshot(path)

    result = vd.format_compliance_check(path)

    # Either a parse failure OR a schema failure is acceptable — both mean
    # Property 7's "malformed file produces error" clause is satisfied.
    assert result["valid"] is False, (
        f"format_compliance_check accepted malformed shape {shape!r}: "
        f"text={text!r}"
    )
    assert result["violations"], (
        f"no violations emitted for malformed shape {shape!r}"
    )
    # Non-silent rewrite: bytes and mtime are identical.
    bytes_after, mtime_after = _snapshot(path)
    assert bytes_before == bytes_after, (
        f"file bytes changed for malformed shape {shape!r}"
    )
    assert mtime_before == mtime_after, (
        f"file mtime changed for malformed shape {shape!r}"
    )
    assert result["file_unchanged"] is True


# Validates: Requirements 9.4 — unknown fields preserved, not dropped.
def test_property_7_unknown_fields_preserved(sandbox_home):
    """A valid file with extra unknown fields reports them but leaves file alone."""
    import validators as vd

    text = (
        "---\n"
        "name: with-extra\n"
        "description: d. Triggers on extra.\n"
        'some_custom_field: "retained"\n'
        'another_custom: 42\n'
        "---\n"
        "# body\n"
    )
    path = _write_skill(sandbox_home, "with-extra", text)
    bytes_before, mtime_before = _snapshot(path)

    result = vd.format_compliance_check(path)

    assert result["valid"] is True, result["violations"]
    assert result["legacy_unknown_fields"] is not None
    assert "some_custom_field" in result["legacy_unknown_fields"]
    assert "another_custom" in result["legacy_unknown_fields"]
    # File never touched.
    assert _snapshot(path) == (bytes_before, mtime_before)
    assert result["file_unchanged"] is True


# Validates: Requirements 9.5 — a current-status file with missing required
# fields fails schema but file unchanged.
def test_property_7_current_missing_required_unchanged(sandbox_home):
    import validators as vd

    text = (
        "---\n"
        "name: incomplete-current\n"
        "description: d. Triggers on incomplete.\n"
        "status: current\n"
        # Missing: sensitive_data_class, portability_tier, created_at, last_validated
        "---\n"
        "# body\n"
    )
    path = _write_skill(sandbox_home, "incomplete-current", text)
    bytes_before, mtime_before = _snapshot(path)

    result = vd.format_compliance_check(path)

    assert result["valid"] is False
    # Schema violation should mention at least one missing field.
    joined = " ".join(result["violations"])
    assert "missing" in joined.lower() or "required" in joined.lower()
    # File untouched.
    assert _snapshot(path) == (bytes_before, mtime_before)
    assert result["file_unchanged"] is True


# Validates: Requirements 9.4, 9.5 — a valid legacy file is clean.
@given(skill=gen.gen_valid_skill_file(force_status="legacy"))
@settings(
    max_examples=100,
    deadline=None,
    suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow],
)
def test_property_7_valid_legacy_passes(sandbox_home, skill):
    """Valid legacy skills pass format-compliance and are untouched."""
    import validators as vd

    fm, body, full_text = skill
    name = fm["name"]
    path = _write_skill(sandbox_home, name, full_text)
    bytes_before, mtime_before = _snapshot(path)

    result = vd.format_compliance_check(path)

    assert result["valid"] is True, result["violations"]
    assert _snapshot(path) == (bytes_before, mtime_before)
    assert result["file_unchanged"] is True


# Validates: Requirements 9.4 — specific shape error messages are descriptive.
def test_property_7_missing_fence_error_descriptive(sandbox_home):
    import validators as vd

    text = "no frontmatter at all\n\njust prose\n"
    path = _write_skill(sandbox_home, "no-fence", text)
    result = vd.format_compliance_check(path)
    assert result["valid"] is False
    assert any("frontmatter" in v.lower() or "parse" in v.lower() for v in result["violations"]), (
        f"expected descriptive error mentioning frontmatter/parse, got: {result['violations']}"
    )
