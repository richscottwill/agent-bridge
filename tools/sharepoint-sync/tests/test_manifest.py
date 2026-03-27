"""Unit tests for SyncManifest."""

from __future__ import annotations

import json
import os
import tempfile

import pytest

# Ensure project root is importable
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from manifest import SyncManifest


@pytest.fixture
def tmp_manifest(tmp_path):
    """Return a path to a non-existent manifest file in a temp dir."""
    return str(tmp_path / ".sync-manifest.json")


class TestSyncManifestCreation:
    """Loading / creating the manifest file."""

    def test_creates_fresh_manifest_when_file_missing(self, tmp_manifest):
        m = SyncManifest(tmp_manifest)
        assert m.all_entries() == []

    def test_loads_existing_manifest(self, tmp_manifest):
        data = {
            "version": 1,
            "last_sync": "2026-03-27T10:00:00Z",
            "entries": [
                {
                    "file_path": "testing/article.md",
                    "mode": "site",
                    "content_hash": "sha256:abc",
                    "sp_item_id": "id-1",
                    "sp_url": "https://sp/page",
                    "synced_at": "2026-03-27T10:00:00Z",
                }
            ],
        }
        with open(tmp_manifest, "w") as f:
            json.dump(data, f)

        m = SyncManifest(tmp_manifest)
        assert len(m.all_entries()) == 1
        assert m.all_entries()[0]["file_path"] == "testing/article.md"

    def test_handles_corrupt_json_gracefully(self, tmp_manifest):
        with open(tmp_manifest, "w") as f:
            f.write("NOT JSON {{{")

        m = SyncManifest(tmp_manifest)
        assert m.all_entries() == []


class TestGetEntry:
    def test_returns_entry_when_found(self, tmp_manifest):
        m = SyncManifest(tmp_manifest)
        m.add_entry("a.md", "site", "sha256:aaa", "id-1", "https://sp/a")
        entry = m.get_entry("a.md", "site")
        assert entry is not None
        assert entry["content_hash"] == "sha256:aaa"

    def test_returns_none_when_not_found(self, tmp_manifest):
        m = SyncManifest(tmp_manifest)
        assert m.get_entry("missing.md", "site") is None

    def test_distinguishes_by_mode(self, tmp_manifest):
        m = SyncManifest(tmp_manifest)
        m.add_entry("a.md", "site", "sha256:s", "id-s", "https://sp/s")
        m.add_entry("a.md", "directory", "sha256:d", "id-d", "https://sp/d")
        assert m.get_entry("a.md", "site")["sp_item_id"] == "id-s"
        assert m.get_entry("a.md", "directory")["sp_item_id"] == "id-d"


class TestAddEntry:
    def test_adds_entry_with_timestamp(self, tmp_manifest):
        m = SyncManifest(tmp_manifest)
        m.add_entry("b.md", "directory", "sha256:bbb", "id-2", "https://sp/b")
        entry = m.get_entry("b.md", "directory")
        assert entry is not None
        assert entry["sp_item_id"] == "id-2"
        assert entry["synced_at"] is not None


class TestUpdateEntry:
    def test_updates_hash_and_synced_at(self, tmp_manifest):
        m = SyncManifest(tmp_manifest)
        m.add_entry("c.md", "site", "sha256:old", "id-3", "https://sp/c")
        m.update_entry("c.md", "site", "sha256:new", "2026-04-01T00:00:00Z")
        entry = m.get_entry("c.md", "site")
        assert entry["content_hash"] == "sha256:new"
        assert entry["synced_at"] == "2026-04-01T00:00:00Z"

    def test_raises_on_missing_entry(self, tmp_manifest):
        m = SyncManifest(tmp_manifest)
        with pytest.raises(KeyError):
            m.update_entry("nope.md", "site", "sha256:x", "2026-04-01T00:00:00Z")


class TestRemoveEntry:
    def test_removes_matching_entry(self, tmp_manifest):
        m = SyncManifest(tmp_manifest)
        m.add_entry("d.md", "site", "sha256:ddd", "id-4", "https://sp/d")
        m.remove_entry("d.md", "site")
        assert m.get_entry("d.md", "site") is None

    def test_raises_on_missing_entry(self, tmp_manifest):
        m = SyncManifest(tmp_manifest)
        with pytest.raises(KeyError):
            m.remove_entry("nope.md", "site")

    def test_only_removes_matching_mode(self, tmp_manifest):
        m = SyncManifest(tmp_manifest)
        m.add_entry("e.md", "site", "sha256:s", "id-s", "https://sp/s")
        m.add_entry("e.md", "directory", "sha256:d", "id-d", "https://sp/d")
        m.remove_entry("e.md", "site")
        assert m.get_entry("e.md", "site") is None
        assert m.get_entry("e.md", "directory") is not None


class TestAllEntries:
    def test_returns_all_when_no_filter(self, tmp_manifest):
        m = SyncManifest(tmp_manifest)
        m.add_entry("f.md", "site", "sha256:f1", "id-f1", "https://sp/f1")
        m.add_entry("g.md", "directory", "sha256:g1", "id-g1", "https://sp/g1")
        assert len(m.all_entries()) == 2

    def test_filters_by_mode(self, tmp_manifest):
        m = SyncManifest(tmp_manifest)
        m.add_entry("f.md", "site", "sha256:f1", "id-f1", "https://sp/f1")
        m.add_entry("g.md", "directory", "sha256:g1", "id-g1", "https://sp/g1")
        assert len(m.all_entries(mode="site")) == 1
        assert m.all_entries(mode="site")[0]["file_path"] == "f.md"


class TestSave:
    def test_persists_and_reloads(self, tmp_manifest):
        m = SyncManifest(tmp_manifest)
        m.add_entry("h.md", "site", "sha256:hhh", "id-h", "https://sp/h")
        m.save()

        m2 = SyncManifest(tmp_manifest)
        assert len(m2.all_entries()) == 1
        assert m2.all_entries()[0]["file_path"] == "h.md"

    def test_save_creates_parent_dirs(self, tmp_path):
        deep_path = str(tmp_path / "a" / "b" / "manifest.json")
        m = SyncManifest(deep_path)
        m.add_entry("i.md", "site", "sha256:iii", "id-i", "https://sp/i")
        m.save()
        assert os.path.exists(deep_path)

    def test_manifest_json_structure(self, tmp_manifest):
        m = SyncManifest(tmp_manifest)
        m.add_entry("j.md", "site", "sha256:jjj", "id-j", "https://sp/j")
        m.save()

        with open(tmp_manifest) as f:
            data = json.load(f)
        assert data["version"] == 1
        assert "last_sync" in data
        assert isinstance(data["entries"], list)
