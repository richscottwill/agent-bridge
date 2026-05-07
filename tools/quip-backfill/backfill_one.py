#!/usr/bin/env python3
"""Backfill the body of a single quip-mirror file.

Reads content from a JSON file containing the Quip response (the `content` field),
cleans it, and writes the cleaned body below the existing YAML frontmatter.

Usage:
    python3 backfill_one.py <rel_path> <quip_json_file>

Where <quip_json_file> is a path to a JSON file whose top-level value is either
the raw content string OR an object with a 'content' field (matching Quip API
response shape via ReadInternalWebsites).
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2] / "wiki" / "quip-mirror"


def clean_quip_content(raw: str, source_url: str, quip_id: str) -> str:
    """Convert Quip-returned markdown to clean markdown.

    Key transformations:
    - Collapse the Quip zero-width space artifacts (​ U+200B) that appear on
      stand-alone lines used as spacers.
    - Rewrite relative `/blob/<quip_id>/<blob_id>` inline image/link paths to
      absolute quip-amazon.com URLs.
    - Normalise escaped parens in headings (Quip emits `\\(` and `\\)` inside
      `###` headers).
    - Normalise mis-quoted strings like `****Text:****` (these come through as
      literal asterisks around text — leave them, they render as bold+bold).
    - Strip trailing whitespace per line.
    - Drop runs of empty lines (cap at one blank between blocks).
    """
    text = raw

    # Rewrite blob-relative refs to absolute
    text = re.sub(
        r"(\]\()/blob/",
        r"\1https://quip-amazon.com/blob/",
        text,
    )
    # And for reference-style definitions: `[n]: /blob/...`
    text = re.sub(
        r"^(\[[^\]]+\]:\s+)/blob/",
        r"\1https://quip-amazon.com/blob/",
        text,
        flags=re.MULTILINE,
    )

    # Unescape \\( and \\) inside headings (Quip escapes parens in header text)
    def _unescape_parens(m):
        return m.group(0).replace(r"\(", "(").replace(r"\)", ")")

    text = re.sub(r"^#{1,6} .*$", _unescape_parens, text, flags=re.MULTILINE)

    # Replace zero-width-space-only lines with blank lines
    text = re.sub(r"^[\u200B\u200C\u200D\uFEFF\s]*$", "", text, flags=re.MULTILINE)

    # Strip trailing whitespace on every line
    text = "\n".join(line.rstrip() for line in text.splitlines())

    # Collapse 3+ consecutive blank lines to 2 (one blank between blocks)
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Strip leading/trailing blank lines
    text = text.strip("\n") + "\n"

    return text


def parse_frontmatter(text: str):
    if not text.startswith("---\n"):
        return None, "", text
    end = text.find("\n---\n", 4)
    if end == -1:
        return None, "", text
    return text[4:end], text[: end + 5], text[end + 5 :]


def fm_get(fm_raw_inner: str, key: str) -> str | None:
    for line in fm_raw_inner.splitlines():
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
    ap = argparse.ArgumentParser()
    ap.add_argument("rel_path", help="Path relative to wiki/quip-mirror/")
    ap.add_argument("content_file", help="File containing the raw Quip content string")
    ap.add_argument(
        "--unreachable",
        action="store_true",
        help="Mark the file as unreachable without rewriting body",
    )
    args = ap.parse_args()

    target = ROOT / args.rel_path
    if not target.exists():
        print(f"ERROR: {target} does not exist", file=sys.stderr)
        sys.exit(2)

    text = target.read_text(encoding="utf-8")
    fm_inner, fm_raw, body = parse_frontmatter(text)
    if fm_inner is None:
        print(f"ERROR: {args.rel_path} has no frontmatter", file=sys.stderr)
        sys.exit(3)

    source_url = fm_get(fm_inner, "source_url")
    quip_id = fm_get(fm_inner, "quip_id")
    doc_type = fm_get(fm_inner, "doc_type")

    if args.unreachable:
        # add backfill_status: unreachable to frontmatter if not present
        if "backfill_status:" not in fm_inner:
            new_fm = fm_raw.replace(
                "\n---\n", "\nbackfill_status: unreachable\n---\n", 1
            )
            target.write_text(new_fm + body, encoding="utf-8")
        print(f"MARKED UNREACHABLE: {args.rel_path}")
        return

    raw_content = Path(args.content_file).read_text(encoding="utf-8")
    # If content_file is JSON, try to extract content field
    try:
        j = json.loads(raw_content)
        if isinstance(j, dict) and "content" in j:
            raw_content = j["content"]
        elif isinstance(j, str):
            raw_content = j
    except (json.JSONDecodeError, ValueError):
        pass

    if doc_type == "spreadsheet":
        new_body = (
            f"_Source is a spreadsheet. See: {source_url}_\n"
        )
    else:
        new_body = clean_quip_content(raw_content, source_url or "", quip_id or "")

    # Add backfill_status: backfilled to frontmatter
    if "backfill_status:" not in fm_inner:
        status_val = "spreadsheet-skipped" if doc_type == "spreadsheet" else "backfilled"
        new_fm_raw = fm_raw.replace(
            "\n---\n", f"\nbackfill_status: {status_val}\n---\n", 1
        )
    else:
        new_fm_raw = fm_raw

    target.write_text(new_fm_raw + "\n" + new_body, encoding="utf-8")
    print(f"OK: {args.rel_path} ({len(new_body)} chars)")


if __name__ == "__main__":
    main()
