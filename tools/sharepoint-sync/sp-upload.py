#!/usr/bin/env python3
"""Phase 2: Upload staged .docx files to SharePoint via manifest.

This script reads the sync manifest and the staged .docx files,
then outputs a JSON upload plan that the agent uses to call the
SharePoint MCP tool for each file.

Usage:
    python3 sp-upload.py                # full upload plan
    python3 sp-upload.py --summary      # counts only
    python3 sp-upload.py --limit 5      # first N files only

The agent reads the JSON output and calls sharepoint_write_file
for each entry. This avoids needing SharePoint API credentials
in Python — the MCP server handles auth.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

STAGING_DIR = Path(os.path.expanduser("~/shared/tools/sharepoint-sync/output"))
SP_LIBRARY = "Documents"
SP_FOLDER = "Artifacts/wiki-sync"


def scan_staged_files(limit: int | None = None) -> list[dict]:
    """Walk the staging directory and build upload entries."""
    if not STAGING_DIR.is_dir():
        return []

    entries = []
    for docx in sorted(STAGING_DIR.rglob("*.docx")):
        rel = docx.relative_to(STAGING_DIR)
        # Category subfolder (e.g. "testing", "callouts/au")
        folder_parts = rel.parent.parts
        sp_subfolder = "/".join(folder_parts) if folder_parts else ""
        sp_target = f"{SP_FOLDER}/{sp_subfolder}".rstrip("/")

        entries.append({
            "local_path": str(docx),
            "filename": docx.name,
            "sp_library": SP_LIBRARY,
            "sp_folder": sp_target,
            "size_bytes": docx.stat().st_size,
        })

        if limit and len(entries) >= limit:
            break

    return entries


def main():
    parser = argparse.ArgumentParser(description="Generate SharePoint upload plan from staged .docx files")
    parser.add_argument("--summary", action="store_true", help="Print counts only")
    parser.add_argument("--limit", type=int, default=None, help="Limit to first N files")
    args = parser.parse_args()

    entries = scan_staged_files(limit=args.limit)

    if args.summary:
        total_size = sum(e["size_bytes"] for e in entries)
        folders = set(e["sp_folder"] for e in entries)
        print(f"Staged files: {len(entries)}")
        print(f"Total size: {total_size:,} bytes ({total_size / 1024 / 1024:.1f} MB)")
        print(f"Target folders: {len(folders)}")
        for f in sorted(folders):
            count = sum(1 for e in entries if e["sp_folder"] == f)
            print(f"  {f}: {count} files")
        return

    # Output JSON for agent consumption
    print(json.dumps({"upload_plan": entries, "total": len(entries)}, indent=2))


if __name__ == "__main__":
    main()
