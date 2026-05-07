#!/usr/bin/env python3
"""Apply a batch of fetched Quip content to mirror files.

Reads a JSON file containing a list of {rel_path, content} objects and
rewrites each target file with frontmatter + cleaned body.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2] / "wiki" / "quip-mirror"


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


def clean_quip_content(raw: str) -> str:
    text = raw
    # Absolute-ify blob references
    text = re.sub(r"(\]\()/blob/", r"\1https://quip-amazon.com/blob/", text)
    text = re.sub(
        r"^(\[[^\]]+\]:\s+)/blob/",
        r"\1https://quip-amazon.com/blob/",
        text,
        flags=re.MULTILINE,
    )
    # Unescape parens in headings
    text = re.sub(
        r"^(#{1,6} .*)$",
        lambda m: m.group(1).replace(r"\(", "(").replace(r"\)", ")"),
        text,
        flags=re.MULTILINE,
    )
    # Blank out zero-width-space spacer lines
    text = re.sub(r"^[\u200B\u200C\u200D\uFEFF\s]*$", "", text, flags=re.MULTILINE)
    # Trailing whitespace
    text = "\n".join(line.rstrip() for line in text.splitlines())
    # Collapse blank runs
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = text.strip("\n") + "\n"
    return text


def apply_one(rel_path: str, content: str | None, unreachable: bool = False):
    p = ROOT / rel_path
    if not p.exists():
        return f"MISSING: {rel_path}"
    text = p.read_text(encoding="utf-8")
    fm_inner, fm_raw, body = parse_frontmatter(text)
    if fm_inner is None:
        return f"NO_FM: {rel_path}"

    doc_type = fm_get(fm_inner, "doc_type")
    source_url = fm_get(fm_inner, "source_url") or ""

    if unreachable or content is None:
        if "backfill_status:" not in fm_inner:
            new_fm = fm_raw.replace(
                "\n---\n", "\nbackfill_status: unreachable\n---\n", 1
            )
            p.write_text(new_fm + body, encoding="utf-8")
        return f"UNREACHABLE: {rel_path}"

    if doc_type == "spreadsheet":
        new_body = f"_Source is a spreadsheet. See: {source_url}_\n"
        status = "spreadsheet-skipped"
    else:
        new_body = clean_quip_content(content)
        status = "backfilled"

    if "backfill_status:" not in fm_inner:
        new_fm_raw = fm_raw.replace(
            "\n---\n", f"\nbackfill_status: {status}\n---\n", 1
        )
    else:
        new_fm_raw = re.sub(
            r"backfill_status:\s*\S+", f"backfill_status: {status}", fm_raw
        )

    p.write_text(new_fm_raw + "\n" + new_body, encoding="utf-8")
    return f"OK: {rel_path} ({len(new_body)} chars)"


def main():
    if len(sys.argv) != 2:
        print("Usage: apply_batch.py <batch.json>", file=sys.stderr)
        sys.exit(1)
    batch = json.load(open(sys.argv[1]))
    for entry in batch:
        rel_path = entry["rel_path"]
        content = entry.get("content")
        unreachable = entry.get("unreachable", False)
        print(apply_one(rel_path, content, unreachable))


if __name__ == "__main__":
    main()
