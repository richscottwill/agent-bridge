"""
Property 1: INVENTORY-BIJECTION

# Feature: skills-powers-adoption, Property 1: For any filesystem state,
# inventory.md's rows bijectively correspond with on-disk assets.

For any randomly-generated filesystem state (random N skills + M powers with
random status/name/body/frontmatter), after running Group 2's walker and
renderer:
  - Every on-disk asset appears as exactly ONE row in the rendered inventory.
  - The row count equals the asset count. No phantom rows, no dropped rows.
  - `status: retired` entries rendered in the inventory correspond to the
    on-disk status field; legacy / current / retired rows coexist cleanly.

Validates: Requirements 1.1, 1.2, 1.3, 7.5
"""

from __future__ import annotations

import importlib
import re
import shutil
import sys
import tempfile
from pathlib import Path

# Make sibling modules + shared strategies importable regardless of pytest cwd.
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
    """Isolated HOME — never touches the real ~/.kiro or ~/shared/."""
    tmp = tempfile.mkdtemp(prefix="sp_p1_bijection_")
    monkeypatch.setenv("HOME", tmp)
    (Path(tmp) / ".kiro" / "skills").mkdir(parents=True)
    (Path(tmp) / ".kiro" / "powers" / "installed").mkdir(parents=True)
    (Path(tmp) / "shared" / "context" / "skills-powers").mkdir(parents=True)
    import inventory

    importlib.reload(inventory)
    yield Path(tmp)
    shutil.rmtree(tmp, ignore_errors=True)
    importlib.reload(inventory)


def _materialize_fs_state(sandbox: Path, assets: list) -> list[tuple[str, str]]:
    """
    Write each (kind, name, frontmatter, body) asset to disk under the sandbox.
    Returns the sorted (kind, name) list of successfully-written assets.
    """
    import inventory as inv

    written: list[tuple[str, str]] = []
    for kind, name, fm, body in assets:
        if kind == "skill":
            md_dir = sandbox / ".kiro" / "skills" / name
            md_name = "SKILL.md"
        else:
            md_dir = sandbox / ".kiro" / "powers" / "installed" / name
            md_name = "POWER.md"
        md_dir.mkdir(parents=True, exist_ok=True)
        # Serialize via the inventory module so any serialization-layer bug
        # is exercised too.
        text = inv.serialize_frontmatter(fm, body)
        (md_dir / md_name).write_text(text, encoding="utf-8")
        written.append((kind, name))
    return sorted(written)


def _extract_rows_from_inventory_md(md: str) -> dict[str, list[str]]:
    """
    Parse the rendered inventory markdown and return the set of names per
    kind. Uses the table's `Name` column (second column). Row IDs are K-S* /
    K-P* so we can distinguish tables by header lookup.
    """
    skills: list[str] = []
    powers: list[str] = []
    current_table: str | None = None
    for line in md.splitlines():
        if line.startswith("## Skills"):
            current_table = "skills"
            continue
        if line.startswith("## Powers"):
            current_table = "powers"
            continue
        if line.startswith("## Staleness"):
            current_table = None
            continue
        if not line.startswith("| ") or line.startswith("|---") or line.startswith("| Row ID"):
            continue
        # Row like: | K-S1 | name | legacy | ... |
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 2:
            continue
        row_id = cells[0]
        name = cells[1]
        if current_table == "skills" and row_id.startswith("K-S"):
            skills.append(name)
        elif current_table == "powers" and row_id.startswith("K-P"):
            powers.append(name)
    return {"skill": skills, "power": powers}


# ----------------------------------------------------------------------------
# Property 1 — bijection
# ----------------------------------------------------------------------------


def _clear_sandbox_assets(sandbox: Path) -> None:
    """Remove all skills and powers from the sandbox so the next hypothesis
    example starts fresh. Re-creates the empty parent directories."""
    skills = sandbox / ".kiro" / "skills"
    powers = sandbox / ".kiro" / "powers" / "installed"
    if skills.is_dir():
        shutil.rmtree(skills)
    if powers.is_dir():
        shutil.rmtree(powers)
    skills.mkdir(parents=True)
    powers.mkdir(parents=True)


# Validates: Requirements 1.1, 1.2, 1.3, 7.5
@given(assets=gen.gen_filesystem_state(min_size=0, max_size=12))
@settings(
    max_examples=150,
    deadline=None,
    suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow],
)
def test_property_1_rows_bijectively_match_disk(sandbox_home, assets):
    """
    Bijection: every on-disk asset → exactly one inventory row, and no
    inventory row without an on-disk asset.
    """
    import inventory as inv

    # Fresh sandbox per hypothesis example (fixture is function-scoped but
    # @given runs many examples in one fixture invocation).
    _clear_sandbox_assets(sandbox_home)

    # Materialize the random filesystem state.
    written = _materialize_fs_state(sandbox_home, assets)

    # Walk + render.
    walk = inv.walk_installed()
    md = inv.render_inventory(walk.assets, [])

    rendered = _extract_rows_from_inventory_md(md)

    # Every written asset is present exactly once.
    for kind, name in written:
        rendered_list = rendered[kind]
        assert rendered_list.count(name) == 1, (
            f"{kind} {name!r} expected once in inventory, got {rendered_list.count(name)} "
            f"(rendered: {rendered_list})"
        )

    # Total row count == disk asset count.
    assert len(rendered["skill"]) == sum(1 for k, _ in written if k == "skill")
    assert len(rendered["power"]) == sum(1 for k, _ in written if k == "power")

    # No phantom rows: every rendered name corresponds to an on-disk path.
    for kind, names in rendered.items():
        for name in names:
            if kind == "skill":
                assert (sandbox_home / ".kiro" / "skills" / name / "SKILL.md").is_file(), (
                    f"phantom skill row: {name}"
                )
            else:
                assert (
                    sandbox_home / ".kiro" / "powers" / "installed" / name / "POWER.md"
                ).is_file(), f"phantom power row: {name}"


# Validates: Requirements 1.1, 1.2 — boundary: empty filesystem.
def test_property_1_empty_filesystem(sandbox_home):
    import inventory as inv

    walk = inv.walk_installed()
    md = inv.render_inventory(walk.assets, [])
    rendered = _extract_rows_from_inventory_md(md)
    assert rendered["skill"] == []
    assert rendered["power"] == []
    # Input-state-hash header still present and well-formed. Header is
    # rendered with markdown bold: `**Input-state-hash**: sha256:...`
    assert re.search(r"Input-state-hash\*?\*?:\s*sha256:[0-9a-f]{64}", md) is not None


# Validates: Requirements 1.1, 1.2 — boundary: single asset.
def test_property_1_single_skill(sandbox_home):
    import inventory as inv

    sk = sandbox_home / ".kiro" / "skills" / "solo"
    sk.mkdir(parents=True, exist_ok=True)
    (sk / "SKILL.md").write_text(
        "---\nname: solo\ndescription: d. Triggers on solo.\n---\n# body\n",
        encoding="utf-8",
    )
    walk = inv.walk_installed()
    md = inv.render_inventory(walk.assets, [])
    rendered = _extract_rows_from_inventory_md(md)
    assert rendered["skill"] == ["solo"]
    assert rendered["power"] == []


# Validates: Requirements 1.1 — boundary: mixed statuses coexist.
def test_property_1_mixed_status_coexist(sandbox_home):
    """Legacy + current assets both appear, each as exactly one row."""
    import inventory as inv

    # Legacy skill (no status field).
    sk1 = sandbox_home / ".kiro" / "skills" / "legacy-s"
    sk1.mkdir(parents=True, exist_ok=True)
    (sk1 / "SKILL.md").write_text(
        "---\nname: legacy-s\ndescription: d. Triggers on legacy.\n---\n# body\n",
        encoding="utf-8",
    )
    # Current skill (full extended frontmatter).
    sk2 = sandbox_home / ".kiro" / "skills" / "current-s"
    sk2.mkdir(parents=True, exist_ok=True)
    (sk2 / "SKILL.md").write_text(
        "---\n"
        "name: current-s\n"
        "description: d. Triggers on current.\n"
        "status: current\n"
        "sensitive_data_class: Amazon_Internal\n"
        "portability_tier: Cold_Start_Safe\n"
        'created_at: "2026-04-22T00:00:00+0000"\n'
        'last_validated: "2026-04-22T00:00:00+0000"\n'
        "---\n# body\n",
        encoding="utf-8",
    )
    walk = inv.walk_installed()
    md = inv.render_inventory(walk.assets, [])
    rendered = _extract_rows_from_inventory_md(md)
    assert sorted(rendered["skill"]) == ["current-s", "legacy-s"]
    # Both render their status correctly.
    assert "| legacy-s | legacy" in md
    assert "| current-s | current" in md


# Validates: Requirements 1.1, 7.5 — larger state (stress test).
def test_property_1_large_state(sandbox_home):
    """Scale check: materialize 30 assets, confirm all render."""
    import inventory as inv

    names = [f"bulk-{i:02d}" for i in range(30)]
    for name in names:
        sk = sandbox_home / ".kiro" / "skills" / name
        sk.mkdir(parents=True, exist_ok=True)
        (sk / "SKILL.md").write_text(
            f"---\nname: {name}\ndescription: d. Triggers on {name}.\n---\n# body\n",
            encoding="utf-8",
        )
    walk = inv.walk_installed()
    md = inv.render_inventory(walk.assets, [])
    rendered = _extract_rows_from_inventory_md(md)
    assert sorted(rendered["skill"]) == sorted(names)
    assert rendered["power"] == []
