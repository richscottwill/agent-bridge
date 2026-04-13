#!/usr/bin/env python3
"""Convert all active state files from .md → .docx.

Used by AM-Backend Step 2E and EOD Step 9 after patching state file content.
Reads the state-file-engine.md registry to find active files.

Usage:
    python3 convert_state_files.py              # convert all active state files
    python3 convert_state_files.py --market MX  # convert only MX
    python3 convert_state_files.py --list       # list registered state files

Requires: python-docx (via shared/tools/sharepoint-sync/converter.py)
"""

import argparse
import os
import sys
import re

STATE_FILES_DIR = os.path.expanduser("~/shared/wiki/state-files")
CONVERTER_DIR = os.path.expanduser("~/shared/tools/sharepoint-sync")

# Registry: market → filename (without extension)
REGISTRY = {
    "MX": "mx-paid-search-state",
    "AU": "au-paid-search-state",
    "WW": "ww-testing-state",
}


def convert_one(fname):
    """Convert a single .md file to .docx. Returns (success, size_bytes)."""
    sys.path.insert(0, CONVERTER_DIR)
    from converter import MarkdownConverter

    md_path = os.path.join(STATE_FILES_DIR, f"{fname}.md")
    docx_path = os.path.join(STATE_FILES_DIR, f"{fname}.docx")

    if not os.path.exists(md_path):
        return False, f"NOT FOUND: {md_path}"

    with open(md_path) as f:
        content = f.read()

    # Strip front-matter and extract title
    lines = content.split("\n")
    title = "Untitled"
    body = content

    if lines[0].strip() == "---":
        end = next(i for i, l in enumerate(lines[1:], 1) if l.strip() == "---")
        for l in lines[1:end]:
            if l.startswith("title:"):
                title = l.split(":", 1)[1].strip().strip('"')
        body = "\n".join(lines[end + 1:])

    converter = MarkdownConverter()
    docx_bytes = converter.to_docx(body, {"title": title})

    with open(docx_path, "wb") as f:
        f.write(docx_bytes)

    return True, len(docx_bytes)


def main():
    parser = argparse.ArgumentParser(description="Convert state files .md → .docx")
    parser.add_argument("--market", help="Convert only this market (MX, AU, WW)")
    parser.add_argument("--list", action="store_true", help="List registered state files")
    args = parser.parse_args()

    if args.list:
        print("Registered state files:")
        for market, fname in REGISTRY.items():
            md_path = os.path.join(STATE_FILES_DIR, f"{fname}.md")
            exists = "✅" if os.path.exists(md_path) else "❌"
            print(f"  {market}: {fname} {exists}")
        return

    targets = REGISTRY
    if args.market:
        key = args.market.upper()
        if key not in REGISTRY:
            print(f"ERROR: Unknown market '{key}'. Available: {', '.join(REGISTRY.keys())}")
            sys.exit(1)
        targets = {key: REGISTRY[key]}

    results = []
    for market, fname in targets.items():
        ok, info = convert_one(fname)
        status = "✅" if ok else "❌"
        size = f"{info:,} bytes" if isinstance(info, int) else info
        print(f"  {market}: {fname}.docx — {status} {size}")
        results.append((market, ok))

    success = sum(1 for _, ok in results if ok)
    total = len(results)
    print(f"\n{success}/{total} converted successfully.")

    if success < total:
        sys.exit(1)


if __name__ == "__main__":
    main()
