"""
Property-based tests for pruning.py — Task 6.5 of the skills-powers-adoption spec.

Two properties per design §Testing Strategy and Group 6.5:
  - Property 2:  STALENESS-CORRECTNESS (never-prune-under-use guarantee)
  - Property 14: ASSET-LIFECYCLE — archive-before-delete half
                 (the validate-before-available half is covered by
                 test_safe_creation_properties.py)

Each property runs 100+ hypothesis iterations. Edge case per Group 6.5:
an activation exactly 30 days ago — must NOT save an asset from the stale
set (strict boundary per compute_stale_set's documented convention).
"""

from __future__ import annotations

import os
import shutil
import sys
import tempfile
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from pathlib import Path

# Make the sibling modules importable when pytest is run from any working dir.
_PKG_DIR = Path(__file__).resolve().parent.parent
if str(_PKG_DIR) not in sys.path:
    sys.path.insert(0, str(_PKG_DIR))

import pytest
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st


# ----------------------------------------------------------------------------
# Sandbox helper: each test runs against an isolated HOME so archive/delete
# operations cannot touch real ~/.kiro or ~/shared/wiki.
# ----------------------------------------------------------------------------


@pytest.fixture
def sandbox_home(monkeypatch):
    """Create a fresh HOME sandbox. All sibling modules reload against it."""
    tmp = tempfile.mkdtemp(prefix="sp_prune_pbt_")
    monkeypatch.setenv("HOME", tmp)
    # Pre-create the Kiro roots so the walker finds the expected layout.
    (Path(tmp) / ".kiro" / "skills").mkdir(parents=True)
    (Path(tmp) / ".kiro" / "powers" / "installed").mkdir(parents=True)
    (Path(tmp) / "shared" / "context" / "skills-powers").mkdir(parents=True)
    (Path(tmp) / "shared" / "wiki" / "agent-created" / "archive").mkdir(
        parents=True
    )
    # Reload so HOME-derived module constants pick up the sandbox.
    import importlib

    import activation_log
    import inventory
    import pruning

    importlib.reload(inventory)
    importlib.reload(activation_log)
    importlib.reload(pruning)
    yield Path(tmp)
    shutil.rmtree(tmp, ignore_errors=True)
    # Restore module state for subsequent tests.
    importlib.reload(inventory)
    importlib.reload(activation_log)
    importlib.reload(pruning)


# ----------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------


_FIXED_NOW = datetime(2026, 6, 1, 12, 0, 0, tzinfo=timezone.utc)


def _mk_asset_record(
    sandbox: Path,
    *,
    kind: str,
    name: str,
    status: str,
    mtime_dt: datetime,
    created_at: str | None = None,
):
    """
    Build an on-disk skill/power with the requested mtime and return the
    AssetRecord the inventory walker would produce.
    """
    import inventory

    if kind == "skill":
        asset_dir = sandbox / ".kiro" / "skills" / name
        md_name = "SKILL.md"
    else:
        asset_dir = sandbox / ".kiro" / "powers" / "installed" / name
        md_name = "POWER.md"
    asset_dir.mkdir(parents=True, exist_ok=True)
    md_path = asset_dir / md_name

    if status == "current":
        created_str = created_at or mtime_dt.strftime("%Y-%m-%dT%H:%M:%S%z")
        if kind == "skill":
            fm = (
                f"---\n"
                f"name: {name}\n"
                f"description: d. Triggers on {name}.\n"
                f"status: current\n"
                f"sensitive_data_class: Amazon_Internal\n"
                f"portability_tier: Cold_Start_Safe\n"
                f"created_at: \"{created_str}\"\n"
                f"last_validated: \"{created_str}\"\n"
                f"---\n# body\n"
            )
        else:
            fm = (
                f"---\n"
                f"name: {name}\n"
                f"displayName: {name}\n"
                f"description: d\n"
                f"keywords:\n  - {name}\n"
                f"author: Test\n"
                f"status: current\n"
                f"sensitive_data_class: Amazon_Internal\n"
                f"portability_tier: Cold_Start_Safe\n"
                f"created_at: \"{created_str}\"\n"
                f"last_validated: \"{created_str}\"\n"
                f"---\n# body\n"
            )
    elif status == "retired":
        # Retired assets may have either minimal or extended frontmatter;
        # use the minimal form + explicit status: retired so the pruning
        # module's status gate excludes them.
        if kind == "skill":
            fm = (
                f"---\nname: {name}\ndescription: d. Triggers on {name}.\n"
                f"status: retired\n---\n# body\n"
            )
        else:
            fm = (
                f"---\nname: {name}\ndisplayName: {name}\ndescription: d\n"
                f"keywords:\n  - {name}\nauthor: Test\nstatus: retired\n"
                f"---\n# body\n"
            )
    else:
        # legacy — no status field
        if kind == "skill":
            fm = (
                f"---\nname: {name}\ndescription: d. Triggers on {name}.\n"
                f"---\n# body\n"
            )
        else:
            fm = (
                f"---\nname: {name}\ndisplayName: {name}\ndescription: d\n"
                f"keywords:\n  - {name}\nauthor: Test\n---\n# body\n"
            )
    md_path.write_text(fm, encoding="utf-8")
    ts = mtime_dt.timestamp()
    os.utime(md_path, (ts, ts))

    text = md_path.read_text(encoding="utf-8")
    parsed = inventory.parse_frontmatter(text)
    fm_dict = parsed.frontmatter if isinstance(parsed, inventory.ParseSuccess) else {}
    return inventory.AssetRecord(
        path=md_path,
        kind=kind,
        name=name,
        raw_frontmatter_text=inventory._split_frontmatter(text)[0],
        body_text=inventory._split_frontmatter(text)[1],
        mtime=ts,
        frontmatter=fm_dict,
    )


# ----------------------------------------------------------------------------
# Hypothesis strategies
# ----------------------------------------------------------------------------

_asset_name_char = st.sampled_from("abcdefghijklmnopqrstuvwxyz0123456789-")
_asset_name = st.text(alphabet=_asset_name_char, min_size=3, max_size=18).filter(
    lambda s: s[0].isalpha() and not s.endswith("-") and "--" not in s
)


@st.composite
def _asset_spec(draw):
    """A single asset spec: name, kind, status, age, last-activation days."""
    return {
        "name": draw(_asset_name),
        "kind": draw(st.sampled_from(["skill", "power"])),
        "status": draw(st.sampled_from(["legacy", "current", "retired"])),
        # Creation age in days before FIXED_NOW. 0..400 — spans both sides of
        # the 30-day grace boundary, with plenty of margin.
        "creation_age_days": draw(st.integers(min_value=0, max_value=400)),
        # Last-activation age in days. None → never activated.
        "last_activation_age_days": draw(
            st.one_of(
                st.none(),
                st.integers(min_value=0, max_value=400),
            )
        ),
    }


@st.composite
def _asset_spec_list(draw):
    """A list of unique-named asset specs."""
    specs = draw(st.lists(_asset_spec(), min_size=0, max_size=12))
    # Dedupe by (kind, name) so filesystem writes don't collide.
    seen: set[tuple[str, str]] = set()
    unique: list[dict] = []
    for s in specs:
        key = (s["kind"], s["name"])
        if key in seen:
            continue
        seen.add(key)
        unique.append(s)
    return unique


# ----------------------------------------------------------------------------
# Property 2: STALENESS-CORRECTNESS
# Feature: skills-powers-adoption, Property 2: Stale set equals
# {asset : status ∈ {legacy, current} AND no activation in last 30d AND not
# created in last 30d}. Assets activated in last 30d are NEVER stale.
# ----------------------------------------------------------------------------


# Validates: Requirements 1.5, 6.5, 8.1, 8.4
@given(specs=_asset_spec_list())
@settings(
    max_examples=150,
    deadline=None,
    suppress_health_check=[HealthCheck.function_scoped_fixture],
)
def test_property_2_staleness_correctness(sandbox_home, specs):
    """
    For any generated filesystem + activation log, the stale set equals
    exactly those assets satisfying the three-gate predicate. The
    never-prune-under-use guarantee is verified explicitly.
    """
    import pruning

    # Clean any assets written by a prior hypothesis iteration.
    skills_root = sandbox_home / ".kiro" / "skills"
    powers_root = sandbox_home / ".kiro" / "powers" / "installed"
    for p in list(skills_root.iterdir()) if skills_root.is_dir() else []:
        shutil.rmtree(p, ignore_errors=True)
    for p in list(powers_root.iterdir()) if powers_root.is_dir() else []:
        shutil.rmtree(p, ignore_errors=True)

    now = _FIXED_NOW
    assets = []
    log: list[dict] = []

    for s in specs:
        mtime_dt = now - timedelta(days=s["creation_age_days"])
        rec = _mk_asset_record(
            sandbox_home,
            kind=s["kind"],
            name=s["name"],
            status=s["status"],
            mtime_dt=mtime_dt,
        )
        assets.append(rec)
        if s["last_activation_age_days"] is not None:
            act_ts = now - timedelta(days=s["last_activation_age_days"])
            log.append(
                {
                    "event": "activated",
                    "kind": s["kind"],
                    "name": s["name"],
                    "request_summary": "pbt",
                    "session_id": "sess-pbt",
                    "ts": act_ts.strftime("%Y-%m-%dT%H:%M:%S%z"),
                }
            )

    stale = pruning.compute_stale_set(assets, log, now=now)
    stale_keys = {(c.kind, c.name) for c in stale}

    # Reconstruct the spec-predicate directly from the specs.
    for s in specs:
        key = (s["kind"], s["name"])
        is_retired = s["status"] == "retired"
        # Retired or unknown status → excluded.
        if is_retired or s["status"] not in ("legacy", "current"):
            assert key not in stale_keys, (
                f"{key} status={s['status']} must not be in stale set"
            )
            continue
        # Never-prune-under-use: activation in last 30 days (strict).
        if (
            s["last_activation_age_days"] is not None
            and s["last_activation_age_days"] < 30
        ):
            assert key not in stale_keys, (
                f"{key} activated {s['last_activation_age_days']}d ago "
                f"MUST be excluded (never-prune-under-use)"
            )
            continue
        # Grace window: created in last 30 days → excluded (strict).
        if s["creation_age_days"] < 30:
            assert key not in stale_keys, (
                f"{key} created {s['creation_age_days']}d ago "
                f"MUST be excluded (grace window)"
            )
            continue
        # Otherwise MUST be in the stale set.
        assert key in stale_keys, (
            f"{key} status={s['status']} creation_age={s['creation_age_days']} "
            f"last_activation_age={s['last_activation_age_days']} "
            f"should be in stale set"
        )

    # Confirm the sort is most-stale-first among activated; never-activated
    # sorts to the top of the list.
    activated_part = [c for c in stale if c.days_since_last_activation is not None]
    for i in range(len(activated_part) - 1):
        assert (
            activated_part[i].days_since_last_activation
            >= activated_part[i + 1].days_since_last_activation
        ), "activated stale candidates must be sorted most-stale-first"


# Validates: Requirements 1.5, 6.5, 8.1, 8.4
def test_property_2_boundary_30_days_exact(sandbox_home):
    """
    Edge case per Group 6.5: an activation exactly 30 days ago does NOT save
    the asset from the stale set. Boundary convention is strict inequality —
    activation must be within the LAST 30 days to save; exactly 30 days is
    OUT of window.
    """
    import pruning

    now = _FIXED_NOW
    mtime_dt = now - timedelta(days=365)  # well past grace

    rec = _mk_asset_record(
        sandbox_home,
        kind="skill",
        name="edge-30d",
        status="legacy",
        mtime_dt=mtime_dt,
    )
    act_ts = now - timedelta(days=30)
    log = [
        {
            "event": "activated",
            "kind": "skill",
            "name": "edge-30d",
            "request_summary": "edge",
            "session_id": "sess",
            "ts": act_ts.strftime("%Y-%m-%dT%H:%M:%S%z"),
        }
    ]
    stale = pruning.compute_stale_set([rec], log, now=now)
    names = {(c.kind, c.name) for c in stale}
    assert (
        ("skill", "edge-30d") in names
    ), "activation exactly 30d ago must NOT save asset from stale set"


# Validates: Requirements 1.5, 6.5, 8.1, 8.4
def test_property_2_boundary_29_days_saves(sandbox_home):
    """Activation 29 days ago DOES save the asset (within-horizon)."""
    import pruning

    now = _FIXED_NOW
    mtime_dt = now - timedelta(days=365)

    rec = _mk_asset_record(
        sandbox_home,
        kind="skill",
        name="edge-29d",
        status="legacy",
        mtime_dt=mtime_dt,
    )
    act_ts = now - timedelta(days=29)
    log = [
        {
            "event": "activated",
            "kind": "skill",
            "name": "edge-29d",
            "request_summary": "edge",
            "session_id": "sess",
            "ts": act_ts.strftime("%Y-%m-%dT%H:%M:%S%z"),
        }
    ]
    stale = pruning.compute_stale_set([rec], log, now=now)
    names = {(c.kind, c.name) for c in stale}
    assert ("skill", "edge-29d") not in names


# Validates: Requirements 1.5, 6.5, 8.1, 8.4
def test_property_2_baseline_events_do_not_count(sandbox_home):
    """
    `baseline`, `missed-by-feedback`, `created`, `pruned`, `correction` events
    must NOT count as activations — only `activated` events save from stale.
    """
    import pruning

    now = _FIXED_NOW
    mtime_dt = now - timedelta(days=365)

    rec = _mk_asset_record(
        sandbox_home,
        kind="skill",
        name="non-activating-events",
        status="legacy",
        mtime_dt=mtime_dt,
    )
    ts_recent = (now - timedelta(days=5)).strftime("%Y-%m-%dT%H:%M:%S%z")
    log = [
        {"event": "baseline", "kind": "skill", "name": "non-activating-events",
         "first_observed": None, "last_observed": ts_recent,
         "session_id": "s", "ts": ts_recent},
        {"event": "missed-by-feedback", "kind": "skill",
         "name": "non-activating-events", "feedback_text": "x",
         "session_id": "s", "ts": ts_recent},
        {"event": "correction", "target_ts": ts_recent, "reason": "r",
         "session_id": "s", "ts": ts_recent},
    ]
    stale = pruning.compute_stale_set([rec], log, now=now)
    names = {(c.kind, c.name) for c in stale}
    assert ("skill", "non-activating-events") in names, (
        "baseline / missed-by-feedback / correction must NOT save from stale"
    )


# ----------------------------------------------------------------------------
# Property 14: ASSET-LIFECYCLE — archive-before-delete half
# Feature: skills-powers-adoption, Property 14: archive operation succeeds
# before delete runs; if archive fails, delete does NOT run.
# ----------------------------------------------------------------------------


# Validates: Requirements 7.6, 8.2, 8.3
@given(
    kind=st.sampled_from(["skill", "power"]),
    name=_asset_name,
    with_overlap=st.booleans(),
)
@settings(
    max_examples=120,
    deadline=None,
    suppress_health_check=[HealthCheck.function_scoped_fixture],
)
def test_property_14_archive_before_delete(sandbox_home, kind, name, with_overlap):
    """
    For any random APPROVE decision against a real on-disk asset, the archive
    directory exists AFTER execute_prune() and the source directory has been
    removed. If with_overlap=True, overlap-check.json is also archived.
    """
    import pruning

    now = _FIXED_NOW
    mtime_dt = now - timedelta(days=180)

    # Ensure both source and archive for this (name,kind) are clean from any
    # prior hypothesis iteration with the same name.
    src_dir = pruning._asset_source_dir(name, kind)
    archive_dir = pruning._archive_dir_for(name, kind, now)
    shutil.rmtree(src_dir, ignore_errors=True)
    shutil.rmtree(archive_dir, ignore_errors=True)

    rec = _mk_asset_record(
        sandbox_home,
        kind=kind,
        name=name,
        status="legacy",
        mtime_dt=mtime_dt,
    )
    src = rec.path.parent
    if with_overlap:
        (src / "overlap-check.json").write_text("{}\n", encoding="utf-8")
    assert src.is_dir()

    decision = pruning.PruneDecision(
        name=name, kind=kind, action="APPROVE", rationale="pbt"
    )
    results = pruning.execute_prune([decision], dry_run=False, now=now)
    assert len(results) == 1
    r = results[0]
    assert r.success, f"approve should succeed: {r.reason}"
    assert r.archive_path is not None
    assert not src.exists(), f"source {src} should have been deleted"

    # Archive must exist and contain the expected files.
    assert archive_dir.is_dir()
    expected_md = "SKILL.md" if kind == "skill" else "POWER.md"
    assert (archive_dir / expected_md).is_file()
    if with_overlap:
        assert (archive_dir / "overlap-check.json").is_file()

    # Clean up for the next hypothesis iteration.
    shutil.rmtree(archive_dir, ignore_errors=True)


# Validates: Requirements 7.6, 8.2, 8.3
def test_property_14_archive_failure_preserves_source(sandbox_home, monkeypatch):
    """
    If shutil.copytree raises, the source directory MUST still exist after
    execute_prune returns. Delete MUST NOT run on archive failure.
    """
    import pruning

    now = _FIXED_NOW
    mtime_dt = now - timedelta(days=180)
    rec = _mk_asset_record(
        sandbox_home,
        kind="skill",
        name="archive-fail",
        status="legacy",
        mtime_dt=mtime_dt,
    )
    src = rec.path.parent
    assert src.is_dir()

    # Force copytree to blow up.
    def boom(*args, **kwargs):
        raise OSError("simulated archive failure")

    monkeypatch.setattr(pruning.shutil, "copytree", boom)

    decision = pruning.PruneDecision(
        name="archive-fail", kind="skill", action="APPROVE", rationale="pbt"
    )
    results = pruning.execute_prune([decision], dry_run=False, now=now)
    r = results[0]
    assert r.success is False
    assert r.reason is not None
    assert "archive failed" in r.reason.lower() or "source preserved" in r.reason.lower()
    # Critical: the source MUST still exist.
    assert src.is_dir(), "source directory must be preserved on archive failure"
    # And the archive dir must NOT exist (copytree raised before creating it).
    archive_dir = pruning._archive_dir_for("archive-fail", "skill", now)
    assert not archive_dir.exists()


# Validates: Requirements 7.6, 8.2, 8.3
def test_property_14_verify_failure_preserves_source(sandbox_home, monkeypatch):
    """
    If archive verification fails (e.g., copytree succeeded but the expected
    md file isn't at destination), delete MUST NOT run.
    """
    import pruning

    now = _FIXED_NOW
    mtime_dt = now - timedelta(days=180)
    rec = _mk_asset_record(
        sandbox_home,
        kind="skill",
        name="verify-fail",
        status="legacy",
        mtime_dt=mtime_dt,
    )
    src = rec.path.parent
    assert src.is_dir()

    # Force _verify_archive to return a failure tuple. Delete must not run.
    monkeypatch.setattr(
        pruning, "_verify_archive", lambda *a, **kw: (False, "simulated verify failure")
    )

    decision = pruning.PruneDecision(
        name="verify-fail", kind="skill", action="APPROVE", rationale="pbt"
    )
    results = pruning.execute_prune([decision], dry_run=False, now=now)
    r = results[0]
    assert r.success is False
    assert "verify failed" in (r.reason or "").lower()
    # Source preserved.
    assert src.is_dir(), "source must not be deleted on verify failure"


# Validates: Requirements 7.6, 8.2, 8.3
@given(action=st.sampled_from(["DEFER", "PROTECT"]))
@settings(
    max_examples=30,
    deadline=None,
    suppress_health_check=[HealthCheck.function_scoped_fixture],
)
def test_property_14_defer_protect_are_noops(sandbox_home, action):
    """DEFER and PROTECT actions never touch the filesystem."""
    import pruning

    now = _FIXED_NOW
    mtime_dt = now - timedelta(days=180)
    rec = _mk_asset_record(
        sandbox_home,
        kind="skill",
        name="defer-protect",
        status="legacy",
        mtime_dt=mtime_dt,
    )
    src = rec.path.parent

    decision = pruning.PruneDecision(
        name="defer-protect", kind="skill", action=action, rationale="keep"
    )
    results = pruning.execute_prune([decision], dry_run=False, now=now)
    r = results[0]
    assert r.success is True
    assert r.note == "no file operations"
    assert r.archive_path is None
    assert src.is_dir(), "DEFER/PROTECT must not delete anything"
    archive_dir = pruning._archive_dir_for("defer-protect", "skill", now)
    assert not archive_dir.exists()
    # Cleanup between iterations.
    shutil.rmtree(src, ignore_errors=True)


# Validates: Requirements 7.6, 8.2, 8.3
def test_property_14_dry_run_no_mutation(sandbox_home):
    """dry_run=True does NOT mutate the filesystem."""
    import pruning

    now = _FIXED_NOW
    mtime_dt = now - timedelta(days=180)
    rec = _mk_asset_record(
        sandbox_home,
        kind="skill",
        name="dry-run",
        status="legacy",
        mtime_dt=mtime_dt,
    )
    src = rec.path.parent
    md = rec.path
    before = md.read_text(encoding="utf-8")

    decision = pruning.PruneDecision(
        name="dry-run", kind="skill", action="APPROVE", rationale="pbt"
    )
    results = pruning.execute_prune([decision], dry_run=True, now=now)
    r = results[0]
    assert r.success is True
    assert r.dry_run is True
    assert r.archive_path is not None  # simulated path
    # Source unchanged.
    assert src.is_dir()
    assert md.read_text(encoding="utf-8") == before
    # Archive not created.
    archive_dir = pruning._archive_dir_for("dry-run", "skill", now)
    assert not archive_dir.exists()
