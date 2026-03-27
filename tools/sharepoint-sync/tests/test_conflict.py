"""Unit tests for ConflictResolver."""

from __future__ import annotations

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from conflict import ConflictResolver


@pytest.fixture
def resolver():
    return ConflictResolver()


def _manifest_entry(synced_at: str = "2026-03-27T10:00:00Z") -> dict:
    return {
        "file_path": "testing/article.md",
        "mode": "site",
        "content_hash": "sha256:old",
        "sp_item_id": "id-1",
        "sp_url": "https://sp/page",
        "synced_at": synced_at,
    }


def _sp_metadata(last_modified: str = "2026-03-27T10:00:00Z") -> dict:
    return {"lastModifiedDateTime": last_modified}


class TestConflictDetection:
    """Conflict flagged only when BOTH sides changed."""

    def test_both_changed_is_conflict(self, resolver):
        result = resolver.check(
            manifest_entry=_manifest_entry("2026-03-27T10:00:00Z"),
            sp_metadata=_sp_metadata("2026-03-28T12:00:00Z"),
            local_changed=True,
        )
        assert result.is_conflict is True
        assert result.details is not None

    def test_only_sp_changed_no_conflict(self, resolver):
        result = resolver.check(
            manifest_entry=_manifest_entry("2026-03-27T10:00:00Z"),
            sp_metadata=_sp_metadata("2026-03-28T12:00:00Z"),
            local_changed=False,
        )
        assert result.is_conflict is False

    def test_only_local_changed_no_conflict(self, resolver):
        result = resolver.check(
            manifest_entry=_manifest_entry("2026-03-27T10:00:00Z"),
            sp_metadata=_sp_metadata("2026-03-26T08:00:00Z"),
            local_changed=True,
        )
        assert result.is_conflict is False

    def test_neither_changed_no_conflict(self, resolver):
        result = resolver.check(
            manifest_entry=_manifest_entry("2026-03-27T10:00:00Z"),
            sp_metadata=_sp_metadata("2026-03-26T08:00:00Z"),
            local_changed=False,
        )
        assert result.is_conflict is False

    def test_sp_modified_at_exact_sync_time_no_conflict(self, resolver):
        """SP modified == synced_at means SP has NOT changed since sync."""
        result = resolver.check(
            manifest_entry=_manifest_entry("2026-03-27T10:00:00Z"),
            sp_metadata=_sp_metadata("2026-03-27T10:00:00Z"),
            local_changed=True,
        )
        assert result.is_conflict is False


class TestConflictResultFields:
    def test_conflict_result_has_sp_modified(self, resolver):
        result = resolver.check(
            manifest_entry=_manifest_entry("2026-03-27T10:00:00Z"),
            sp_metadata=_sp_metadata("2026-03-28T12:00:00Z"),
            local_changed=True,
        )
        assert result.sp_modified == "2026-03-28T12:00:00Z"

    def test_no_conflict_details_is_none(self, resolver):
        result = resolver.check(
            manifest_entry=_manifest_entry("2026-03-27T10:00:00Z"),
            sp_metadata=_sp_metadata("2026-03-26T08:00:00Z"),
            local_changed=False,
        )
        assert result.details is None


class TestTimezoneHandling:
    def test_z_suffix_timestamps(self, resolver):
        result = resolver.check(
            manifest_entry=_manifest_entry("2026-03-27T10:00:00Z"),
            sp_metadata=_sp_metadata("2026-03-28T10:00:00Z"),
            local_changed=True,
        )
        assert result.is_conflict is True

    def test_offset_timestamps(self, resolver):
        result = resolver.check(
            manifest_entry=_manifest_entry("2026-03-27T10:00:00+00:00"),
            sp_metadata=_sp_metadata("2026-03-28T10:00:00+00:00"),
            local_changed=True,
        )
        assert result.is_conflict is True
