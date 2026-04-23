"""
Property 5: INVENTORY-FRESHNESS

# Feature: skills-powers-adoption, Property 5: If H_R == H_FS then R reflects
# current filesystem; mismatch triggers Phase A re-run.

For any materialized filesystem state:
  - `compute_input_state_hash(walk.assets)` produces a stable sha256:XXXX string.
  - After ANY mutation to the filesystem (add asset / remove asset / modify
    frontmatter), the recomputed hash differs from the pre-mutation hash.
  - Same filesystem → same hash (deterministic).

Scope note per F3: Property 5 is about inventory accuracy vs. the filesystem.
It does NOT claim anything about the inventory's own active-referrer status
in the audit graph — the inventory is ORPHAN-by-design.

Validates: Requirements 1.3, 1.4
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
from hypothesis import HealthCheck, assume, given, settings
from hypothesis import strategies as st

import _strategies as gen


@pytest.fixture
def sandbox_home(monkeypatch):
    tmp = tempfile.mkdtemp(prefix="sp_p5_freshness_")
    monkeypatch.setenv("HOME", tmp)
    (Path(tmp) / ".kiro" / "skills").mkdir(parents=True)
    (Path(tmp) / ".kiro" / "powers" / "installed").mkdir(parents=True)
    (Path(tmp) / "shared" / "context" / "skills-powers").mkdir(parents=True)
    import inventory

    importlib.reload(inventory)
    yield Path(tmp)
    shutil.rmtree(tmp, ignore_errors=True)
    importlib.reload(inventory)


def _clear_sandbox(sandbox: Path) -> None:
    skills = sandbox / ".kiro" / "skills"
    powers = sandbox / ".kiro" / "powers" / "installed"
    if skills.is_dir():
        shutil.rmtree(skills)
    if powers.is_dir():
        shutil.rmtree(powers)
    skills.mkdir(parents=True)
    powers.mkdir(parents=True)


def _materialize(sandbox: Path, assets: list) -> None:
    import inventory as inv

    for kind, name, fm, body in assets:
        if kind == "skill":
            d = sandbox / ".kiro" / "skills" / name
            mdname = "SKILL.md"
        else:
            d = sandbox / ".kiro" / "powers" / "installed" / name
            mdname = "POWER.md"
        d.mkdir(parents=True, exist_ok=True)
        (d / mdname).write_text(
            inv.serialize_frontmatter(fm, body), encoding="utf-8"
        )


# ----------------------------------------------------------------------------
# Property 5 — deterministic + mutation-detecting hash
# ----------------------------------------------------------------------------


# Validates: Requirements 1.3 — deterministic hashing
@given(assets=gen.gen_filesystem_state(min_size=1, max_size=10))
@settings(
    max_examples=120,
    deadline=None,
    suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow],
)
def test_property_5_hash_is_deterministic(sandbox_home, assets):
    """Same filesystem → same hash across calls."""
    import inventory as inv

    _clear_sandbox(sandbox_home)
    _materialize(sandbox_home, assets)

    walk1 = inv.walk_installed()
    walk2 = inv.walk_installed()
    h1 = inv.compute_input_state_hash(walk1.assets)
    h2 = inv.compute_input_state_hash(walk2.assets)
    assert h1 == h2
    assert h1.startswith("sha256:")
    assert len(h1.split("sha256:")[1]) == 64


# Validates: Requirements 1.3, 1.4 — add asset changes hash
@given(
    base_assets=gen.gen_filesystem_state(min_size=1, max_size=6),
    new_asset=gen.gen_filesystem_state(min_size=1, max_size=1),
)
@settings(
    max_examples=120,
    deadline=None,
    suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow],
)
def test_property_5_add_changes_hash(sandbox_home, base_assets, new_asset):
    """Adding any asset changes the hash."""
    import inventory as inv

    _clear_sandbox(sandbox_home)
    _materialize(sandbox_home, base_assets)

    # Ensure the new asset name is unique vs. base.
    existing_names = {(k, n) for k, n, _, _ in base_assets}
    if not new_asset:
        assume(False)
    new_kind, new_name, _, _ = new_asset[0]
    assume((new_kind, new_name) not in existing_names)

    walk_before = inv.walk_installed()
    hash_before = inv.compute_input_state_hash(walk_before.assets)

    _materialize(sandbox_home, new_asset)
    walk_after = inv.walk_installed()
    hash_after = inv.compute_input_state_hash(walk_after.assets)

    assert hash_before != hash_after, (
        f"hash didn't change after adding {new_kind} {new_name!r}"
    )


# Validates: Requirements 1.3, 1.4 — delete asset changes hash
@given(assets=gen.gen_filesystem_state(min_size=2, max_size=8))
@settings(
    max_examples=120,
    deadline=None,
    suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow],
)
def test_property_5_delete_changes_hash(sandbox_home, assets):
    """Deleting any asset changes the hash."""
    import inventory as inv

    _clear_sandbox(sandbox_home)
    _materialize(sandbox_home, assets)

    walk_before = inv.walk_installed()
    assume(len(walk_before.assets) >= 1)
    hash_before = inv.compute_input_state_hash(walk_before.assets)

    # Delete the first asset.
    to_delete = walk_before.assets[0]
    if to_delete.kind == "skill":
        shutil.rmtree(sandbox_home / ".kiro" / "skills" / to_delete.name)
    else:
        shutil.rmtree(sandbox_home / ".kiro" / "powers" / "installed" / to_delete.name)

    walk_after = inv.walk_installed()
    hash_after = inv.compute_input_state_hash(walk_after.assets)

    assert hash_before != hash_after, (
        f"hash didn't change after deleting {to_delete.kind} {to_delete.name!r}"
    )


# Validates: Requirements 1.3, 1.4 — modify frontmatter changes hash
@given(assets=gen.gen_filesystem_state(min_size=1, max_size=6))
@settings(
    max_examples=120,
    deadline=None,
    suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow],
)
def test_property_5_modify_frontmatter_changes_hash(sandbox_home, assets):
    """Modifying any asset's frontmatter changes the hash."""
    import inventory as inv

    _clear_sandbox(sandbox_home)
    _materialize(sandbox_home, assets)

    walk_before = inv.walk_installed()
    assume(len(walk_before.assets) >= 1)
    hash_before = inv.compute_input_state_hash(walk_before.assets)

    # Touch the first asset's frontmatter — append a new field.
    target = walk_before.assets[0]
    original = target.path.read_text(encoding="utf-8")
    # Safely inject a new field before the closing fence.
    modified = original.replace(
        "---\n", "---\nfreshness_test_marker: \"mutated\"\n", 1
    )
    # Only the FIRST '---\n' is the opening fence — but we need to make sure
    # our replace only hits the opening, not the closing. replace(..., 1)
    # hits the first occurrence which is always the opening.
    target.path.write_text(modified, encoding="utf-8")

    walk_after = inv.walk_installed()
    hash_after = inv.compute_input_state_hash(walk_after.assets)

    assert hash_before != hash_after, (
        f"hash didn't change after modifying {target.kind} {target.name!r} "
        f"frontmatter"
    )


# Validates: Requirements 1.3 — empty filesystem is a valid hash domain
def test_property_5_empty_filesystem_has_stable_hash(sandbox_home):
    """Empty filesystem → stable empty-input hash."""
    import inventory as inv

    walk = inv.walk_installed()
    h1 = inv.compute_input_state_hash(walk.assets)
    h2 = inv.compute_input_state_hash(walk.assets)
    assert h1 == h2
    # The sha256 of an empty byte stream is a well-known constant.
    assert h1 == "sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
