#!/usr/bin/env python3
"""Build manifest of all quip-mirror files with existing frontmatter."""
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2] / "wiki" / "quip-mirror"
MANIFEST = Path(__file__).resolve().parent / "manifest.json"


def parse_frontmatter(text: str):
    """Return (fm_dict, fm_raw, body). If no frontmatter, returns (None, '', text)."""
    if not text.startswith("---\n"):
        return None, "", text
    end = text.find("\n---\n", 4)
    if end == -1:
        return None, "", text
    fm_raw = text[: end + 5]
    body = text[end + 5 :]
    fm = {}
    # Primitive YAML parse — handles flat key:value + list items under a key
    current_list_key = None
    for line in text[4:end].splitlines():
        if not line.strip():
            continue
        if line.startswith("- "):
            if current_list_key:
                fm.setdefault(current_list_key, []).append(line[2:].strip())
            continue
        # reset list key on any non-list line
        m = re.match(r"^([A-Za-z0-9_\-]+):\s*(.*)$", line)
        if m:
            k, v = m.group(1), m.group(2).strip()
            if v == "":
                current_list_key = k
                fm[k] = []
            else:
                current_list_key = None
                # strip surrounding quotes
                if (v.startswith('"') and v.endswith('"')) or (
                    v.startswith("'") and v.endswith("'")
                ):
                    v = v[1:-1]
                fm[k] = v
    return fm, fm_raw, body


def main():
    entries = []
    for p in sorted(ROOT.rglob("*.md")):
        rel = p.relative_to(ROOT).as_posix()
        if rel in ("README.md", "quip-inventory.md"):
            continue
        text = p.read_text(encoding="utf-8")
        fm, fm_raw, body = parse_frontmatter(text)
        if fm is None:
            entries.append(
                {
                    "rel_path": rel,
                    "status": "no_frontmatter",
                    "source_url": None,
                    "quip_id": None,
                    "doc_type": None,
                    "top_folder": rel.split("/")[0],
                }
            )
            continue
        entries.append(
            {
                "rel_path": rel,
                "status": "ok",
                "source_url": fm.get("source_url"),
                "quip_id": fm.get("quip_id"),
                "doc_type": fm.get("doc_type"),
                "title": fm.get("title"),
                "top_folder": rel.split("/")[0],
            }
        )
    MANIFEST.write_text(json.dumps(entries, indent=2, ensure_ascii=False))
    # Summary
    by_type = {}
    by_folder = {}
    for e in entries:
        by_type[e.get("doc_type") or "unknown"] = (
            by_type.get(e.get("doc_type") or "unknown", 0) + 1
        )
        by_folder[e["top_folder"]] = by_folder.get(e["top_folder"], 0) + 1
    print(f"Total: {len(entries)}", file=sys.stderr)
    print(f"By doc_type: {json.dumps(by_type)}", file=sys.stderr)
    print(f"By top folder: {json.dumps(by_folder)}", file=sys.stderr)
    print(f"Manifest: {MANIFEST}", file=sys.stderr)


if __name__ == "__main__":
    main()
