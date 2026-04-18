#!/usr/bin/env python3
"""
sync-sharepoint-artifacts.py — Snapshot SharePoint Documents/Artifacts/ into a local JSON cache.

The build-wiki-index.py builder reads data/sharepoint-artifacts.json (if present) to mark
each local wiki article as published=yes/no and flag published-but-stale docs.

Separating this from build-wiki-index.py keeps the builder dependency-free and fast — the
SharePoint crawl only runs when we want it (weekly wiki-maintenance, or manual refresh).

Output: data/sharepoint-artifacts.json

Usage: run from any context where `aim mcp` / the sharepoint MCP is authorized.
This script is a NO-OP harness — the actual SharePoint listing must be done by the agent
running wiki-maintenance, because the MCP tool is only accessible through the agent runtime.
When you run this script directly, it prints instructions for an agent to populate the cache.

See wiki-maintenance.md Phase 2 for the agent-driven population path.
"""
import json, sys, os
from pathlib import Path
from datetime import datetime

CACHE = Path(__file__).parent / "data" / "sharepoint-artifacts.json"

INSTRUCTIONS = """
This script cannot call the SharePoint MCP directly (MCP tools are agent-runtime only).

To refresh the cache, ask your agent to run:

  1. For each of these 7 category folders under Documents/Artifacts/:
     testing, strategy, markets, operations, reporting, research, _meta

     Call: sharepoint_list_files(libraryName="Documents", folderPath=f"Artifacts/{cat}", top=200)

  2. For each returned file, extract: Name, Path, Size, Modified
     Stem = filename with .docx stripped (e.g. "oci-program.docx" → "oci-program")

  3. Write this schema to data/sharepoint-artifacts.json:

     {
       "generated": "<ISO timestamp>",
       "artifacts": [
         {"stem": "<slug>", "category": "<category>", "path": "<full SP path>",
          "modified": "<ISO>", "size": <bytes>},
         ...
       ]
     }

The builder reads this cache as a read-only snapshot. No live SharePoint calls during build.
"""

def main():
    if not CACHE.exists():
        print("SharePoint artifacts cache does not exist yet.")
        print(INSTRUCTIONS)
        sys.exit(1)
    try:
        data = json.loads(CACHE.read_text())
        n = len(data.get("artifacts", []))
        gen = data.get("generated", "unknown")
        print(f"SharePoint artifacts cache: {n} entries, generated {gen}")
        print(f"Path: {CACHE}")
    except Exception as e:
        print(f"Cache exists but is malformed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
