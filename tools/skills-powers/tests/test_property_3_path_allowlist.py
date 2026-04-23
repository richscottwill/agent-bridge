"""
Property 3: PATH-ALLOWLIST-CORRECTNESS (hypothesis)

# Feature: skills-powers-adoption, Property 3: Validator emits path-allowlist
# violation iff P ∉ allowlist(C), status-gated.

Universally quantified over random (sensitive_data_class, status, path_kind)
triples:
  - For `status: legacy`: validator SKIPS the check, returns valid=True + skipped=True.
  - For `status: current` + `Public`: valid anywhere.
  - For `status: current` + `Amazon_Internal`: valid anywhere; sync_violation
    set when path is bridge-synced (but still valid).
  - For `status: current` + `Amazon_Confidential`: valid only under
    allowlist roots (~/.kiro/skills/, ~/.kiro/powers/installed/,
    ~/shared/context/). Additional error when path is under bridge-synced
    directories.
  - For `status: current` + `Personal_PII`: same allowlist as Amazon_Confidential,
    with an extra rule that ~/shared/context/protocols/ is rejected (prefer body/).

Validates: Requirements 3.2, 3.3, 3.5, 3.6, 7.4
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
    """Isolated HOME so path-allowlist checks don't see real bridge-sync list."""
    tmp = tempfile.mkdtemp(prefix="sp_p3_allowlist_")
    monkeypatch.setenv("HOME", tmp)
    (Path(tmp) / ".kiro" / "skills").mkdir(parents=True)
    (Path(tmp) / ".kiro" / "powers" / "installed").mkdir(parents=True)
    (Path(tmp) / ".kiro" / "steering").mkdir(parents=True)
    (Path(tmp) / "shared" / "context" / "body").mkdir(parents=True)
    (Path(tmp) / "shared" / "context" / "protocols").mkdir(parents=True)
    import inventory
    import validators

    importlib.reload(inventory)
    importlib.reload(validators)
    yield Path(tmp)
    shutil.rmtree(tmp, ignore_errors=True)
    importlib.reload(inventory)
    importlib.reload(validators)


def _resolve_path(sandbox: Path, path_kind: str) -> Path:
    """Materialize a symbolic path_kind into an absolute path."""
    mapping = {
        "skills": sandbox / ".kiro" / "skills" / "some-skill" / "SKILL.md",
        "powers": sandbox / ".kiro" / "powers" / "installed" / "some-power" / "POWER.md",
        "context-body": sandbox / "shared" / "context" / "body" / "some.md",
        "context-protocols": sandbox / "shared" / "context" / "protocols" / "some.md",
        "steering": sandbox / ".kiro" / "steering" / "auto.md",
        "agent-bridge-synced": sandbox / "shared" / "context" / "body" / "synced.md",
        "outside-home": Path("/tmp/outside-home-test.md"),
        "tmp": Path(tempfile.gettempdir()) / "property3-outside.md",
    }
    return mapping[path_kind]


# Convention: the bridge-sync default list in validators.py includes
# ~/shared/context/body, ~/shared/context/protocols, and ~/.kiro/steering.
# "agent-bridge-synced" is context-body (always synced).
_SYNCED_PATH_KINDS = {"context-body", "context-protocols", "steering", "agent-bridge-synced"}
_ALLOWLIST_PATH_KINDS_ALL = {
    "skills",
    "powers",
    "context-body",
    "context-protocols",
}
_ALLOWLIST_PATH_KINDS_PII = {
    "skills",
    "powers",
    "context-body",
    # context-protocols is explicitly rejected for Personal_PII per validators.py
}


# ----------------------------------------------------------------------------
# Property 3 — the universal check
# ----------------------------------------------------------------------------


# Validates: Requirements 3.2, 3.3, 3.5, 3.6, 7.4
@given(tup=gen.gen_sensitivity_tuple())
@settings(
    max_examples=150,
    deadline=None,
    suppress_health_check=[HealthCheck.function_scoped_fixture],
)
def test_property_3_path_allowlist_universal(sandbox_home, tup):
    """
    Universal: for random (class, status, path_kind), the validator's verdict
    matches the allowlist specification.
    """
    import validators as vd

    sensitivity, status, path_kind = tup
    out_path = _resolve_path(sandbox_home, path_kind)

    fm = {"name": "test", "description": "d. Triggers on x."}
    if status == "current":
        fm["status"] = "current"
        fm["sensitive_data_class"] = sensitivity

    # Expected bridge-synced paths: empty list means no sync check, but the
    # real module reads bridge-sync.md if present (absent in our sandbox →
    # falls back to the hardcoded convention). We override explicitly so
    # tests are deterministic.
    synced = [
        sandbox_home / "shared" / "context" / "body",
        sandbox_home / "shared" / "context" / "protocols",
        sandbox_home / ".kiro" / "steering",
    ]

    result = vd.sensitivity_path_check(fm, out_path, agent_bridge_synced_paths=synced)

    # Legacy: always skipped.
    if status == "legacy":
        assert result["valid"] is True
        assert result["skipped"] is True
        return

    # Current: status-gated logic.
    assert result["skipped"] is False
    if sensitivity == "Public":
        # Public allowed anywhere, including "outside-home" and "tmp".
        assert result["valid"] is True
    elif sensitivity == "Amazon_Internal":
        # Amazon_Internal allowed anywhere; bridge-synced paths → warning only
        # (still valid=True, sync_violation=True).
        assert result["valid"] is True
        if path_kind in _SYNCED_PATH_KINDS:
            assert result["sync_violation"] is True
    elif sensitivity == "Amazon_Confidential":
        # Valid iff path under allowlist AND not bridge-synced.
        under_allowlist = path_kind in _ALLOWLIST_PATH_KINDS_ALL
        is_synced = path_kind in _SYNCED_PATH_KINDS
        expected_valid = under_allowlist and not is_synced
        assert result["valid"] == expected_valid, (
            f"Amazon_Confidential + {path_kind}: expected valid={expected_valid}, "
            f"got {result['valid']}; violations={result['violations']}"
        )
    elif sensitivity == "Personal_PII":
        # Valid iff path under PII-allowlist AND not bridge-synced.
        # Note: context-protocols is also in allowlist but separately rejected
        # by the PII rule that prefers body/ over protocols/.
        under_allowlist = path_kind in _ALLOWLIST_PATH_KINDS_PII
        is_synced = path_kind in _SYNCED_PATH_KINDS
        is_protocols = path_kind == "context-protocols"
        expected_valid = under_allowlist and not is_synced and not is_protocols
        assert result["valid"] == expected_valid, (
            f"Personal_PII + {path_kind}: expected valid={expected_valid}, "
            f"got {result['valid']}; violations={result['violations']}"
        )


# Validates: Requirements 3.2 — boundary: legacy bypass is total.
@given(
    sensitivity=st.sampled_from(
        ["Public", "Amazon_Internal", "Amazon_Confidential", "Personal_PII"]
    ),
    path_kind=gen.gen_path_kind(),
)
@settings(
    max_examples=100,
    deadline=None,
    suppress_health_check=[HealthCheck.function_scoped_fixture],
)
def test_property_3_legacy_always_skipped(sandbox_home, sensitivity, path_kind):
    """For any sensitivity, any path: a legacy asset is always skipped."""
    import validators as vd

    out_path = _resolve_path(sandbox_home, path_kind)
    fm = {"name": "legacy-test", "description": "d. Triggers on x."}
    # Intentionally include sensitive_data_class to confirm it's ignored for legacy.
    fm["sensitive_data_class"] = sensitivity
    result = vd.sensitivity_path_check(fm, out_path)
    assert result["valid"] is True
    assert result["skipped"] is True
    assert result["reason"] == "legacy asset grandfathered"
