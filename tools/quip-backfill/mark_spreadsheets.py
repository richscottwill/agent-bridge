#!/usr/bin/env python3
"""Mark all spreadsheet files with the standard stub note, per Richard's constraint.

Replaces the body below the YAML frontmatter with:
    _Source is a spreadsheet. See: <source_url>_
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2] / "wiki" / "quip-mirror"
MANIFEST = Path(__file__).resolve().parent / "manifest.json"


def parse_frontmatter(text: str):
    if not text.startswith("---\n"):
        return None, "", text
    end = text.find("\n---\n", 4)
    if end == -1:
        return None, "", text
    return text[4:end], text[: end + 5], text[end + 5 :]


def fm_get(fm_inner: str, key: str):
    for line in fm_inner.splitlines():
        m = re.match(rf"^{re.escape(key)}:\s*(.*)$", line)
        if m:
            v = m.group(1).strip()
            if (v.startswith('"') and v.endswith('"')) or (
                v.startswith("'") and v.endswith("'")
            ):
                v = v[1:-1]
            return v
    return None


def main():
    entries = json.load(open(MANIFEST))
    count = 0
    for e in entries:
        if e.get("doc_type") != "spreadsheet":
            continue
        p = ROOT / e["rel_path"]
        text = p.read_text(encoding="utf-8")
        fm_inner, fm_raw, body = parse_frontmatter(text)
        if fm_inner is None:
            print(f"SKIP (no frontmatter): {e['rel_path']}", file=sys.stderr)
            continue
        source_url = fm_get(fm_inner, "source_url") or ""
        new_body = f"_Source is a spreadsheet. See: {source_url}_\n"
        if "backfill_status:" not in fm_inner:
            new_fm_raw = fm_raw.replace(
                "\n---\n", "\nbackfill_status: spreadsheet-skipped\n---\n", 1
            )
        else:
            new_fm_raw = fm_raw
        p.write_text(new_fm_raw + "\n" + new_body, encoding="utf-8")
        count += 1
    print(f"Marked {count} spreadsheets")


if __name__ == "__main__":
    main()
