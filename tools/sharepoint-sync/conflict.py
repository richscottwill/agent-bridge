"""Conflict resolver — detects when both local and SharePoint have changed.

A conflict is flagged only when BOTH sides changed since the last sync:
  - SharePoint's lastModifiedDateTime > manifest synced_at
  - Local content hash differs from manifest content_hash

If only one side changed, no conflict is flagged.
"""

from __future__ import annotations

from datetime import datetime, timezone

from models import ConflictResult


def _parse_iso(ts: str) -> datetime:
    """Parse an ISO-8601 timestamp string to a timezone-aware datetime."""
    dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


class ConflictResolver:
    """Compare local and SharePoint state to detect conflicts."""

    def check(
        self,
        manifest_entry: dict,
        sp_metadata: dict,
        local_changed: bool,
    ) -> ConflictResult:
        """Determine whether a conflict exists.

        Parameters
        ----------
        manifest_entry:
            The manifest dict for this file/mode.  Must contain
            ``synced_at`` (ISO timestamp).
        sp_metadata:
            SharePoint item metadata.  Must contain
            ``lastModifiedDateTime`` (ISO timestamp).
        local_changed:
            True when the local content hash differs from the manifest.

        Returns
        -------
        ConflictResult
            ``is_conflict`` is True only when *both* sides changed.
        """
        synced_at = _parse_iso(manifest_entry["synced_at"])
        sp_modified = _parse_iso(sp_metadata["lastModifiedDateTime"])

        sp_changed = sp_modified > synced_at

        is_conflict = sp_changed and local_changed

        details: str | None = None
        if is_conflict:
            details = (
                f"Both sides changed since last sync at {manifest_entry['synced_at']}. "
                f"SharePoint modified at {sp_metadata['lastModifiedDateTime']}; "
                f"local content hash differs."
            )

        return ConflictResult(
            is_conflict=is_conflict,
            local_modified=str(local_changed),
            sp_modified=sp_metadata["lastModifiedDateTime"],
            details=details,
        )
