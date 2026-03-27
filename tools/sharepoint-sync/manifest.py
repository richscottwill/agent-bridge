"""Sync manifest — tracks which articles have been pushed to SharePoint.

Persists a JSON file at a configurable path with structure:
    { "version": 1, "last_sync": "...", "entries": [...] }

Each entry records file_path, mode, content_hash, sp_item_id, sp_url,
and synced_at — enabling incremental sync and conflict detection.
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class SyncManifest:
    """Load, query, mutate, and persist the sync manifest."""

    _VERSION = 1

    def __init__(self, manifest_path: str) -> None:
        """Load or create manifest JSON file at *manifest_path*."""
        self._path = Path(os.path.expanduser(manifest_path))
        self._data: dict[str, Any] = self._load()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def get_entry(self, file_path: str, mode: str) -> dict | None:
        """Look up a manifest entry by *file_path* and *mode*.

        Returns the entry dict or ``None`` if not found.
        """
        for entry in self._data["entries"]:
            if entry["file_path"] == file_path and entry["mode"] == mode:
                return dict(entry)  # return a copy
        return None

    def add_entry(
        self,
        file_path: str,
        mode: str,
        content_hash: str,
        sp_item_id: str,
        sp_url: str,
    ) -> None:
        """Add a new entry after a successful upload."""
        now = datetime.now(timezone.utc).isoformat()
        self._data["entries"].append(
            {
                "file_path": file_path,
                "mode": mode,
                "content_hash": content_hash,
                "sp_item_id": sp_item_id,
                "sp_url": sp_url,
                "synced_at": now,
            }
        )
        self._data["last_sync"] = now

    def update_entry(
        self,
        file_path: str,
        mode: str,
        content_hash: str,
        synced_at: str,
    ) -> None:
        """Update an existing entry after a successful update."""
        for entry in self._data["entries"]:
            if entry["file_path"] == file_path and entry["mode"] == mode:
                entry["content_hash"] = content_hash
                entry["synced_at"] = synced_at
                self._data["last_sync"] = synced_at
                return
        raise KeyError(
            f"No manifest entry for file_path={file_path!r}, mode={mode!r}"
        )

    def remove_entry(self, file_path: str, mode: str) -> None:
        """Remove an entry after SP deletion."""
        before = len(self._data["entries"])
        self._data["entries"] = [
            e
            for e in self._data["entries"]
            if not (e["file_path"] == file_path and e["mode"] == mode)
        ]
        if len(self._data["entries"]) == before:
            raise KeyError(
                f"No manifest entry for file_path={file_path!r}, mode={mode!r}"
            )

    def all_entries(self, mode: str | None = None) -> list[dict]:
        """Return all entries, optionally filtered by *mode*."""
        if mode is None:
            return [dict(e) for e in self._data["entries"]]
        return [
            dict(e) for e in self._data["entries"] if e["mode"] == mode
        ]

    def save(self) -> None:
        """Persist the manifest to disk."""
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._path.write_text(
            json.dumps(self._data, indent=2, sort_keys=False) + "\n",
            encoding="utf-8",
        )

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _load(self) -> dict[str, Any]:
        """Load existing manifest or return a fresh skeleton."""
        if self._path.exists():
            try:
                raw = self._path.read_text(encoding="utf-8")
                data = json.loads(raw)
                if isinstance(data, dict) and "entries" in data:
                    return data
            except (json.JSONDecodeError, OSError):
                pass  # fall through to fresh manifest
        return {
            "version": self._VERSION,
            "last_sync": None,
            "entries": [],
        }
