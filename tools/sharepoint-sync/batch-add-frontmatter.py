#!/usr/bin/env python3
"""Batch-add front-matter to wiki files missing it.

Rules:
- Files with existing front-matter: add missing audience/status fields only
- Files without front-matter: add a full block with relevant defaults
- Preserves existing HTML comments (<!-- DOC-xxxx -->) at top of file
- Never overwrites existing field values

Audience: always 'amazon-internal' (only eligible value for SP sync)
Status defaults by directory:
  - agent-created/archive/  → archived
  - agent-created/reviews/  → DRAFT
  - agent-created/*         → REVIEW  (most are wiki articles ready for review)
  - callouts/*              → FINAL   (weekly callouts are published artifacts)
  - meetings/*              → DRAFT   (internal meeting notes, not for SP)
  - quip-mirror/*           → DRAFT   (mirrors, not authoritative)
"""

import frontmatter
import os
import sys
import re
from pathlib import Path
from datetime import date

WIKI_ROOT = Path(os.path.expanduser("~/shared/wiki/"))
TODAY = date.today().isoformat()

DRY_RUN = "--dry-run" in sys.argv
VERBOSE = "--verbose" in sys.argv or "-v" in sys.argv


def status_for_path(path: Path) -> str:
    """Determine default status based on directory location."""
    rel = path.relative_to(WIKI_ROOT)
    parts = rel.parts

    if parts[0] == "agent-created":
        if len(parts) > 1 and parts[1] == "archive":
            return "archived"
        if len(parts) > 1 and parts[1] == "reviews":
            return "DRAFT"
        return "REVIEW"
    elif parts[0] == "callouts":
        return "FINAL"
    elif parts[0] == "meetings":
        return "DRAFT"
    elif parts[0] == "quip-mirror":
        return "DRAFT"
    return "DRAFT"


def extract_doc_comment(text: str) -> tuple[str, str]:
    """Split leading <!-- DOC-xxxx --> comment from body."""
    m = re.match(r"^(<!--.*?-->\s*\n?)", text, re.DOTALL)
    if m:
        return m.group(1), text[m.end():]
    return "", text


def title_from_content(body: str, filename: str) -> str:
    """Extract title from first H1, or fall back to filename."""
    for line in body.splitlines():
        line = line.strip()
        if line.startswith("# "):
            return line[2:].strip()
    return filename.replace("-", " ").replace(".md", "").title()


def process_file(path: Path) -> str:
    """Process a single file. Returns action taken."""
    raw = path.read_text(encoding="utf-8")

    try:
        post = frontmatter.loads(raw)
        has_fm = bool(post.metadata)
    except Exception:
        has_fm = False
        post = None

    if has_fm:
        # File already has front-matter — just patch missing fields
        changed = False
        if "audience" not in post.metadata:
            post.metadata["audience"] = "amazon-internal"
            changed = True
        if "status" not in post.metadata:
            post.metadata["status"] = status_for_path(path)
            changed = True
        if "owner" not in post.metadata:
            post.metadata["owner"] = "Richard Williams"
            changed = True

        if not changed:
            return "unchanged"

        if DRY_RUN:
            return "would-patch"

        # Rebuild file preserving the original structure
        output = frontmatter.dumps(post)
        path.write_text(output + "\n", encoding="utf-8")
        return "patched"

    else:
        # No front-matter — add a full block
        doc_comment, body = extract_doc_comment(raw)
        title = title_from_content(body, path.name)
        status = status_for_path(path)

        fm_block = (
            f"---\n"
            f"title: \"{title}\"\n"
            f"status: {status}\n"
            f"audience: amazon-internal\n"
            f"owner: Richard Williams\n"
            f"created: {TODAY}\n"
            f"updated: {TODAY}\n"
            f"---\n"
        )

        if DRY_RUN:
            return "would-add"

        new_content = doc_comment + fm_block + "\n" + body
        path.write_text(new_content, encoding="utf-8")
        return "added"


def main():
    if DRY_RUN:
        print("=== DRY RUN — no files will be modified ===\n")

    counts = {"added": 0, "patched": 0, "unchanged": 0,
              "would-add": 0, "would-patch": 0, "error": 0}

    for entry in sorted(WIKI_ROOT.iterdir()):
        if not entry.is_dir() or entry.name.startswith("."):
            continue
        for md in sorted(entry.rglob("*.md")):
            try:
                action = process_file(md)
                counts[action] = counts.get(action, 0) + 1
                if VERBOSE or action not in ("unchanged",):
                    print(f"  [{action:>12}] {md.relative_to(WIKI_ROOT)}")
            except Exception as exc:
                counts["error"] += 1
                print(f"  [       error] {md.relative_to(WIKI_ROOT)}: {exc}")

    print(f"\n{'='*50}")
    print(f"Summary:")
    for k, v in counts.items():
        if v > 0:
            print(f"  {k}: {v}")
    print(f"  total: {sum(counts.values())}")


if __name__ == "__main__":
    main()
