#!/usr/bin/env python3
"""build-projection-standalone.py — build a single-file standalone HTML for SharePoint.

WHY THIS EXISTS
    SharePoint-embedded + filesystem-opened HTML cannot reliably `fetch()`
    sibling JSON. The standalone build inlines projection-data.json, both
    JS modules, and the narrative module into a single projection-standalone.html
    that works anywhere — upload to SharePoint, drag from OneDrive, email as
    attachment, open from disk.

HOW IT WORKS
    - Read projection.html
    - Replace <script src="mpe_engine.js"> with inline <script>...</script>
    - Replace <script src="mpe_narrative.js"> with inline <script>...</script>
    - Replace <script src="projection-app.js"> with inline <script>...</script>
    - Inject the JSON data bundle as a <script>window.__MPE_DATA=...;</script>
    - Rewrite the app's loadData() to prefer window.__MPE_DATA over fetch
    - Write to projection-standalone.html (single file, drop-in anywhere)

USAGE
    python3 build-projection-standalone.py
"""
import json
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).parent
INPUT_HTML = SCRIPT_DIR / "projection.html"
OUTPUT_HTML = SCRIPT_DIR / "projection-standalone.html"
DATA_JSON = SCRIPT_DIR / "data" / "projection-data.json"
ASSETS = ["mpe_engine.js", "mpe_narrative.js", "projection-app.js"]


def main() -> int:
    if not INPUT_HTML.exists():
        print(f"ERROR: {INPUT_HTML} not found")
        return 1

    html = INPUT_HTML.read_text()

    # Inline each script
    for asset in ASSETS:
        path = SCRIPT_DIR / asset
        if not path.exists():
            print(f"WARN: {path} not found, skipping inline")
            continue
        content = path.read_text()
        tag = f'<script src="{asset}"></script>'
        if tag not in html:
            print(f"WARN: no tag found for {asset}")
            continue
        # Use a literal replacement that preserves the embedded content
        html = html.replace(tag, f"<script>\n/* === inlined {asset} === */\n{content}\n</script>")

    # Inject data bundle + patch loadData() to prefer window.__MPE_DATA
    if DATA_JSON.exists():
        data = DATA_JSON.read_text()
        inject = (
            "<script>\n"
            "/* === inlined data/projection-data.json === */\n"
            f"window.__MPE_DATA = {data};\n"
            "</script>\n"
        )
        # Insert the data bundle BEFORE any inlined scripts so it's available when projection-app.js runs
        anchor = '<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>'
        if anchor in html:
            html = html.replace(anchor, inject + anchor)
        else:
            # Fallback — inject before </body>
            html = html.replace("</body>", inject + "</body>")

        # Patch the loadData function to prefer window.__MPE_DATA
        original = "async function loadData() {"
        patched = (
            "async function loadData() {\n"
            "      if (typeof window !== 'undefined' && window.__MPE_DATA) {\n"
            "        STATE.data = window.__MPE_DATA;\n"
            "        if (STATE.data.fallback) {\n"
            "          showBanner('warn', 'Embedded data bundle is a fallback stub.');\n"
            "        } else {\n"
            "          const generated = new Date(STATE.data.generated);\n"
            "          const ageHours = (Date.now() - generated.getTime()) / 3600000;\n"
            "          showBanner('fresh', `Data refreshed ${generated.toLocaleString()} (${ageHours.toFixed(1)}h ago, embedded bundle). Methodology v${STATE.data.methodology_version}.`);\n"
            "        }\n"
            "        return;\n"
            "      }\n"
            "      // Fallback to network fetch when not embedded\n"
        )
        html = html.replace(original, patched)

    OUTPUT_HTML.write_text(html)
    size_kb = OUTPUT_HTML.stat().st_size / 1024.0
    print(f"Wrote {OUTPUT_HTML} ({size_kb:.1f} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
