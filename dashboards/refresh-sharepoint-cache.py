#!/usr/bin/env python3
"""refresh-sharepoint-cache.py — Crawl the team SharePoint folders and refresh
~/shared/dashboards/data/sharepoint-artifacts.json, which build-wiki-index.py
consumes to mark articles as published vs local-only vs stale.

Layout transition (2026-04-28): the old flat
  Documents/Artifacts/{testing,strategy,markets,operations,reporting,research,_meta}/*.docx
tree was reorganized into four team folders under the personal OneDrive:
  - AB-Paid-Acq-Team/{programs,markets,methodology,library}/**
  - AB-Paid-Acq-Dashboards/**
  - AB-Paid-Acq-Ops/**
  - .Richard-Private/**                   (out of scope for the wiki index)

Outputs the same JSON schema the index builder already reads so nothing
downstream has to change:

  {
    "generated": "<ISO>",
    "layout_version": 2,
    "sources": ["AB-Paid-Acq-Team", "AB-Paid-Acq-Dashboards", "AB-Paid-Acq-Ops"],
    "artifacts": [
      {"stem": "<slug>", "category": "<folder>", "path": "<server-relative>",
       "modified": "<ISO>", "size": <int>, "ext": "md|docx|xlsx|..."}
    ]
  }

The "category" field now reflects the actual containing folder (e.g.
"programs/oci", "markets/au", "methodology") instead of the old 7-bucket
vocabulary. The index builder only uses it for display, so this is fine.

This script SHELLS OUT to `kiro-cli` style direct MCP calls is not available
to a Python script. Instead it uses the SharePoint MCP command line via the
existing `sharepoint-sync` CLI if present, or the bundled node helper
sp-durability-upload.mjs. For the weekly wiki-maintenance run, the usual path
is: an agent calls sharepoint_list_files per folder and pipes the results
into this script via stdin (JSON array). See the Kiro hook protocol for the
updated choreography.

Usage:
  # agent path (default): read folder listings from stdin as JSON
  #   {"AB-Paid-Acq-Team/programs/oci": [file records...], ...}
  python3 refresh-sharepoint-cache.py < listings.json

  # fresh-start path: emit an empty-but-valid cache (used when MCP is down)
  python3 refresh-sharepoint-cache.py --empty
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


HERE = Path(__file__).parent
OUT = HERE / "data" / "sharepoint-artifacts.json"

# Which top-level folders we crawl. .Richard-Private is intentionally excluded.
IN_SCOPE_ROOTS = (
    "AB-Paid-Acq-Team",
    "AB-Paid-Acq-Dashboards",
    "AB-Paid-Acq-Ops",
)

# File extensions we index. Markdown + Office docs only; ignore binaries,
# caches, screenshots, playwright traces, .bin, etc.
INDEXED_EXT = {"md", "docx", "xlsx", "pptx", "pdf"}


def parse_listings(obj: dict) -> list[dict]:
    """Turn a {folder_path: [file_records]} mapping into flat artifact rows."""
    out: list[dict] = []
    for folder_path, files in obj.items():
        # Guard against unexpected top-level keys.
        if not isinstance(files, list):
            continue
        # Category = folder path relative to the OneDrive root, minus leading
        # "<Root>/" — e.g. "programs/oci" for AB-Paid-Acq-Team/programs/oci.
        category = folder_path
        for root in IN_SCOPE_ROOTS:
            prefix = f"{root}/"
            if folder_path == root:
                category = root  # top-level file
                break
            if folder_path.startswith(prefix):
                category = folder_path[len(prefix) :]
                break
        for rec in files:
            if not isinstance(rec, dict):
                continue
            if rec.get("IsFolder"):
                continue
            name = rec.get("Name", "")
            if not name or name.startswith("."):
                continue
            # Strip extension, lowercase for stem match with local slug.
            if "." not in name:
                continue
            stem, ext = name.rsplit(".", 1)
            ext = ext.lower()
            if ext not in INDEXED_EXT:
                continue
            # _index.md / README.md files aren't articles — they're folder
            # READMEs with the same stem across many folders. Skip.
            if stem.lower() in {"_index", "readme"}:
                continue
            out.append(
                {
                    "stem": stem.lower(),
                    "category": category,
                    "path": rec.get("Path", ""),
                    "modified": rec.get("Modified", ""),
                    "size": int(rec.get("Size", 0) or 0),
                    "ext": ext,
                }
            )
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--empty",
        action="store_true",
        help="Emit a valid-but-empty cache (used when SharePoint MCP is unreachable).",
    )
    args = ap.parse_args()

    if args.empty:
        listings: dict = {}
    else:
        try:
            payload = sys.stdin.read()
            if not payload.strip():
                print(
                    "ERROR: no stdin payload. Pipe SharePoint listings JSON or pass --empty.",
                    file=sys.stderr,
                )
                return 2
            listings = json.loads(payload)
        except json.JSONDecodeError as e:
            print(f"ERROR: stdin is not valid JSON: {e}", file=sys.stderr)
            return 2

    artifacts = parse_listings(listings)
    artifacts.sort(key=lambda a: (a["category"], a["stem"]))

    # De-dup: if the same stem shows up in multiple folders, keep the
    # most recently modified. Emit a WARN so the agent notices.
    seen: dict[str, dict] = {}
    dupes: list[tuple[str, str, str]] = []
    for a in artifacts:
        prior = seen.get(a["stem"])
        if prior is None:
            seen[a["stem"]] = a
            continue
        dupes.append((a["stem"], prior["category"], a["category"]))
        # Keep the newer mtime.
        if a.get("modified", "") > prior.get("modified", ""):
            seen[a["stem"]] = a
    artifacts = sorted(seen.values(), key=lambda a: (a["category"], a["stem"]))

    out = {
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S%z"),
        "layout_version": 2,
        "layout_note": (
            "v2 layout (2026-04-28+): AB-Paid-Acq-{Team,Dashboards,Ops}/** + "
            ".Richard-Private/** (excluded). Replaces the v1 Artifacts/<cat>/ tree."
        ),
        "sources": list(IN_SCOPE_ROOTS),
        "artifacts": artifacts,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")

    print(f"SharePoint cache refreshed: {len(artifacts)} artifacts")
    if dupes:
        print(f"  WARN: {len(dupes)} stems seen in >1 folder — kept newest mtime:")
        for stem, cat_a, cat_b in dupes[:10]:
            print(f"    {stem}: {cat_a} vs {cat_b}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
