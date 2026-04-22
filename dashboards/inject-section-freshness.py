#!/usr/bin/env python3
"""
inject-section-freshness.py — Idempotently inject the section-freshness script
tag into every dashboard HTML page.

Runs once to bootstrap. Safe to re-run; detects existing injection and skips.
"""
import re
from pathlib import Path

HOME = Path.home()
DASHBOARDS = HOME / "shared/dashboards"
MARKER = "section-freshness.js"

# Page → relative path to shared/section-freshness.js
def script_path_for(html_rel):
    # Count path depth from dashboards root
    depth = html_rel.count("/")
    prefix = "./" if depth == 0 else "../" * depth
    return f"{prefix}shared/section-freshness.js"


def inject(html_path):
    text = html_path.read_text(encoding="utf-8", errors="replace")
    if MARKER in text:
        return False  # already injected
    rel = html_path.relative_to(DASHBOARDS).as_posix()
    src = script_path_for(rel)
    tag = f'\n<script src="{src}" defer></script>\n'
    # Insert right before </body> (case-insensitive, last occurrence)
    matches = list(re.finditer(r"</body>", text, flags=re.IGNORECASE))
    if not matches:
        # If no </body>, skip — malformed HTML
        return False
    m = matches[-1]
    new_text = text[: m.start()] + tag + text[m.start():]
    html_path.write_text(new_text, encoding="utf-8")
    return True


def main():
    skip_dirs = ("shared", "validation", "contrib-inputs", "data")
    injected = 0
    skipped = 0
    # Also include files inside symlinked directories (body-system is a symlink)
    html_files = set()
    for html in DASHBOARDS.rglob("*.html"):
        html_files.add(html.resolve())
    # Walk symlinked subdirs explicitly
    for entry in DASHBOARDS.iterdir():
        if entry.is_symlink() and entry.is_dir():
            for html in entry.rglob("*.html"):
                html_files.add(html)
    for html in sorted(html_files):
        # Compute rel-path relative to DASHBOARDS, handling symlink targets
        try:
            rel = html.relative_to(DASHBOARDS).as_posix()
        except ValueError:
            # Find which symlinked subdir it lives under
            rel = None
            for entry in DASHBOARDS.iterdir():
                if entry.is_symlink() and entry.is_dir():
                    try:
                        sub = html.relative_to(entry.resolve())
                        rel = (entry.name + "/" + sub.as_posix())
                        break
                    except ValueError:
                        continue
            if rel is None:
                continue
        if any(rel.startswith(d + "/") for d in skip_dirs):
            continue
        if inject(html):
            print(f"  injected: {rel}")
            injected += 1
        else:
            skipped += 1
    print(f"\nInjected: {injected}, Skipped (already had it or malformed): {skipped}")


if __name__ == "__main__":
    main()
