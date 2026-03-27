"""LocalFolderWriter — writes .docx files to a OneDrive-synced folder.

Replaces the webhook/Graph API client. Files are written to a local
directory that OneDrive syncs to SharePoint automatically. No API
calls, no auth, no webhooks.

The writer maintains the same interface shape as the previous
SharePointClient so the SyncEngine doesn't need major changes.
"""

from __future__ import annotations

import logging
import os
import shutil
from datetime import datetime, timezone
from pathlib import Path

from models import GraphAPIError

logger = logging.getLogger(__name__)


class SharePointClient:
    """Write .docx files to a local OneDrive-synced folder.

    Despite the class name (kept for backward compat with SyncEngine),
    this does NOT call any APIs. It writes files to disk and lets
    OneDrive handle the sync to SharePoint.
    """

    def __init__(self, output_path: str, **kwargs):
        """Initialise with the local output directory path.

        Parameters
        ----------
        output_path:
            Path to the OneDrive-synced SharePoint document library
            folder (e.g. ``~/OneDrive - Amazon/SharePoint/WikiSync/``).
            Will be created if it doesn't exist.
        **kwargs:
            Ignored — allows backward-compat with old config keys
            (site_webhook_url, directory_webhook_url).
        """
        self.output_path = Path(os.path.expanduser(output_path))
        self.output_path.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------ #
    # Site Mode — not supported with OneDrive sync
    # ------------------------------------------------------------------ #

    def create_site_page(self, title: str, html: str, category: str,
                         properties: dict) -> dict:
        """Not supported — OneDrive sync only handles files, not site pages."""
        raise GraphAPIError(
            "Site mode is not supported with OneDrive sync. "
            "Use --mode directory instead."
        )

    def update_site_page(self, item_id: str, title: str, html: str,
                         properties: dict) -> dict:
        raise GraphAPIError("Site mode is not supported with OneDrive sync.")

    def delete_site_page(self, item_id: str) -> None:
        raise GraphAPIError("Site mode is not supported with OneDrive sync.")

    def get_site_page_metadata(self, item_id: str) -> dict:
        raise GraphAPIError("Site mode is not supported with OneDrive sync.")

    # ------------------------------------------------------------------ #
    # Directory Mode — write .docx to local folder
    # ------------------------------------------------------------------ #

    def upload_file(self, folder_path: str, filename: str,
                    content_base64: str, properties: dict) -> dict:
        """Write a .docx file to the output folder.

        Parameters
        ----------
        folder_path:
            Category subfolder (e.g. ``"testing/"``).
        filename:
            Target filename (e.g. ``"ai-max-test-design.docx"``).
        content_base64:
            Base64-encoded .docx content.
        properties:
            Metadata dict (logged but not written — OneDrive doesn't
            support custom SharePoint columns via file system).

        Returns
        -------
        dict
            ``{item_id, url, lastModifiedDateTime}`` — item_id is the
            relative file path, url is the absolute path on disk.
        """
        import base64

        target_dir = self.output_path / folder_path.strip("/")
        target_dir.mkdir(parents=True, exist_ok=True)
        target_file = target_dir / filename

        try:
            docx_bytes = base64.b64decode(content_base64)
            target_file.write_bytes(docx_bytes)
        except Exception as exc:
            raise GraphAPIError(
                f"Failed to write {target_file}: {exc}"
            ) from exc

        now = datetime.now(timezone.utc).isoformat()
        rel_path = str(target_file.relative_to(self.output_path))

        logger.info("Wrote %s (%d bytes)", target_file, len(docx_bytes))

        return {
            "item_id": rel_path,
            "url": str(target_file),
            "lastModifiedDateTime": now,
        }

    def delete_file(self, item_id: str) -> None:
        """Delete a file from the output folder."""
        target = self.output_path / item_id
        if target.exists():
            target.unlink()
            logger.info("Deleted %s", target)
        else:
            logger.warning("File not found for deletion: %s", target)

    def get_file_metadata(self, item_id: str) -> dict:
        """Get file metadata from the local file system."""
        target = self.output_path / item_id
        if not target.exists():
            return {"lastModifiedDateTime": "1970-01-01T00:00:00Z"}

        mtime = target.stat().st_mtime
        modified = datetime.fromtimestamp(mtime, tz=timezone.utc).isoformat()
        return {
            "lastModifiedDateTime": modified,
            "item_id": item_id,
        }

    def ensure_folder(self, folder_path: str) -> None:
        """Create folder if it doesn't exist."""
        target = self.output_path / folder_path.strip("/")
        target.mkdir(parents=True, exist_ok=True)
