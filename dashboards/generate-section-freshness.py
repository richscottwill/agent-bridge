#!/usr/bin/env python3
"""
generate-section-freshness.py — Build per-section freshness manifest.

For every dashboard HTML page, scan <h2> headings and resolve a last-updated
timestamp per section based on:

  1. Explicit mapping (in SECTION_SOURCES below) — sections backed by a DuckDB
     table or JSON file get that source's timestamp.
  2. Data file fallback — if the page reads a JSON data file, use that file's
     `generated` field for unmapped dynamic sections.
  3. HTML file mtime — for static narrative sections with no data backing.

Output: shared/dashboards/data/section-freshness.json
  {
    "generated": "2026-04-21T...",
    "pages": {
      "index.html": {
        "five-levels": {"updated_iso": "...", "source": "body-system-data.json"},
        ...
      },
      ...
    }
  }

Soul check:
  - Structural over cosmetic: this is a default visibility signal, not a
    manual reminder. Stale sections surface themselves.
  - Subtraction before addition: the per-section labels reveal dashboard
    sections that haven't been refreshed — removal candidates for future
    cleanup passes.
"""
import json
import os
import re
from datetime import datetime, timezone, date
from pathlib import Path

HOME = Path.home()
DASHBOARDS = HOME / "shared/dashboards"
OUTPUT = DASHBOARDS / "data/section-freshness.json"

# ─────────────────────────────────────────────────────────────────────────────
# Page → data file mapping. When a <h2> section isn't explicitly mapped below,
# we fall back to the page's primary data file's `generated` timestamp.
# ─────────────────────────────────────────────────────────────────────────────
PAGE_DATA_FILE = {
    "index.html": "data/command-center-data.json",
    "performance/weekly-review.html": "data/callout-data.json",  # M1: merged tracker+callouts
    "wiki-search.html": "data/wiki-index.json",
    "body-system/index.html": "data/body-system-data.json",
    "body-system/growth.html": "data/body-system-data.json",
    "body-system/willpower.html": "data/body-system-data.json",
    "body-system/output.html": "data/body-system-data.json",
    "body-system/autoresearch.html": "data/body-system-data.json",
    "state-files/index.html": "data/state-files-data.json",
    "state-files/au.html": "data/state-files-data.json",
    "state-files/mx.html": "data/state-files-data.json",
    "state-files/ww.html": "data/state-files-data.json",
    "state-files/goals.html": "data/goals-data.json",
    "performance/index.html": None,  # wrapper tab page, no direct data
}

# ─────────────────────────────────────────────────────────────────────────────
# Static section registry for pages that render headings dynamically via JS.
# These pages have no <h2> in the raw HTML — headings are built at runtime.
# We register their known sections here so the manifest covers them.
# ─────────────────────────────────────────────────────────────────────────────
STATIC_SECTIONS = {
    "index.html": [
        ("hero", "Hero"),
        ("daily-blocks", "Daily Blocks"),
        ("integrity-ledger", "Integrity Ledger"),
        ("actionable-intelligence", "Actionable Intelligence"),
    ],
    "performance/weekly-review.html": [
        ("sec-kpis", "KPIs"),
        ("sec-trend", "Trend"),
        ("sec-detail", "Weekly Detail"),
        ("sec-callout", "Callout"),
        ("sec-channels", "Channels"),
        ("sec-projections", "Projections"),
        ("sec-context", "Context"),
    ],
    "performance/index.html": [
        ("weekly-review", "Weekly Review"),
        ("projection-engine", "Projection Engine"),
    ],
}

# ─────────────────────────────────────────────────────────────────────────────
# Explicit section → source overrides.
# ─────────────────────────────────────────────────────────────────────────────
SECTION_SOURCES = {
    # Body system sections with specific backing sources
    "organ-word-budgets": {"file": HOME / "shared/context/body"},
    "organ-freshness": {"file": HOME / "shared/context/body"},
    "experiment-history": {"data_field": "experiment_history", "json": "data/body-system-data.json"},
    "agent-health": {"data_field": "agent_health", "json": "data/body-system-data.json"},
    "hook-reliability": {"data_field": "hook_reliability", "json": "data/body-system-data.json"},
    "workflow-reliability": {"data_field": "workflow_reliability", "json": "data/body-system-data.json"},
    "weekly-scorecard": {"data_field": "weekly_output", "json": "data/body-system-data.json"},
    "pattern-trajectories": {"data_field": "patterns", "json": "data/body-system-data.json"},
    # Wiki search
    "wiki-search": {"file": HOME / "shared/wiki/agent-created"},
    # Command Center dynamic sections
    "hero": {"json": "data/command-center-data.json"},
    "daily-blocks": {"json": "data/command-center-data.json"},
    "integrity-ledger": {"json": "data/command-center-data.json"},
    "actionable-intelligence": {"json": "data/command-center-data.json"},
    # Weekly Review (merged tracker + callouts)
    "sec-kpis": {"json": "data/forecast-data.json"},
    "sec-trend": {"json": "data/forecast-data.json"},
    "sec-detail": {"json": "data/forecast-data.json"},
    "sec-callout": {"json": "data/callout-data.json"},
    "sec-channels": {"json": "data/callout-data.json"},
    "sec-projections": {"json": "data/callout-data.json"},
    "sec-context": {"json": "data/callout-data.json"},
}


def slugify(text):
    """Match the JS slugify so section-ids align."""
    s = text.lower()
    s = re.sub(r"&[a-z]+;", " ", s)
    s = re.sub(r"<[^>]+>", " ", s)
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = s.strip("-")
    return s[:80]


def extract_h2_sections(html_path):
    """Return list of (section_id, heading_text) for every <h2> in the HTML.
    
    Prefers explicit id=""; else slugifies the inner text. Skips headings
    inside <script> blocks (templates) and those with data-freshness-skip.
    """
    if not html_path.exists():
        return []
    text = html_path.read_text(encoding="utf-8", errors="replace")
    # Remove <script>...</script> blocks first so template literals don't pollute
    text_no_script = re.sub(
        r"<script\b[^>]*>.*?</script>", "", text, flags=re.DOTALL | re.IGNORECASE
    )
    sections = []
    seen = set()
    for match in re.finditer(
        r"<h2\b([^>]*)>(.*?)</h2>", text_no_script, flags=re.DOTALL | re.IGNORECASE
    ):
        attrs = match.group(1)
        if "data-freshness-skip" in attrs:
            continue
        id_match = re.search(r'\bid\s*=\s*["\']([^"\']+)["\']', attrs)
        heading_text = re.sub(r"<[^>]+>", "", match.group(2)).strip()
        if id_match:
            section_id = id_match.group(1)
        else:
            section_id = slugify(heading_text)
        if not section_id or section_id in seen:
            continue
        seen.add(section_id)
        sections.append((section_id, heading_text))
    return sections


def iso_from_mtime(path):
    if not path.exists():
        return None
    # For directories, use latest mtime of any contained file
    if path.is_dir():
        latest = 0
        for p in path.rglob("*"):
            try:
                latest = max(latest, p.stat().st_mtime)
            except OSError:
                pass
        if latest == 0:
            return None
        return datetime.fromtimestamp(latest, tz=timezone.utc).isoformat()
    return datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc).isoformat()


def iso_from_json_generated(json_path):
    if not json_path.exists():
        return None
    try:
        data = json.loads(json_path.read_text())
    except (OSError, json.JSONDecodeError):
        return None
    gen = data.get("generated")
    if gen:
        # Ensure ISO with tz
        try:
            return datetime.fromisoformat(gen.replace("Z", "+00:00")).isoformat()
        except ValueError:
            return gen
    return None


def iso_from_data_field(json_path, field):
    """Extract the latest timestamp from a list of records under `field`.
    
    Looks for any of: invoked_at, last_invoked, last_run, updated_at, generated,
    tracker_date, week_start, started_at, created_at, first_detected. Returns
    the max.
    """
    if not json_path.exists():
        return None
    try:
        data = json.loads(json_path.read_text())
    except (OSError, json.JSONDecodeError):
        return None
    rows = data.get(field)
    if not isinstance(rows, list) or not rows:
        # Fall back to the overall generated timestamp
        return iso_from_json_generated(json_path)
    ts_fields = [
        "invoked_at", "last_invoked", "last_run", "updated_at",
        "generated", "tracker_date", "week_start", "started_at",
        "created_at", "first_detected", "completed_at",
    ]
    best = None
    for row in rows:
        if not isinstance(row, dict):
            continue
        for tsf in ts_fields:
            v = row.get(tsf)
            if not v:
                continue
            try:
                dt = datetime.fromisoformat(str(v).replace("Z", "+00:00"))
                if best is None or dt > best:
                    best = dt
            except (ValueError, TypeError):
                continue
    if best:
        if best.tzinfo is None:
            best = best.replace(tzinfo=timezone.utc)
        return best.isoformat()
    return iso_from_json_generated(json_path)


def resolve_section_freshness(page_key, section_id, html_path):
    """Return (updated_iso, source_label) for a given section."""
    # 1. Explicit override
    override = SECTION_SOURCES.get(section_id)
    if override:
        if "json" in override and "data_field" in override:
            json_path = DASHBOARDS / override["json"]
            iso = iso_from_data_field(json_path, override["data_field"])
            if iso:
                return iso, f"{override['json']}:{override['data_field']}"
        elif "json" in override:
            # json-only override — use the file's generated timestamp
            json_path = DASHBOARDS / override["json"]
            iso = iso_from_json_generated(json_path)
            if iso:
                return iso, override["json"]
        if "file" in override:
            iso = iso_from_mtime(override["file"])
            if iso:
                return iso, str(override["file"].relative_to(HOME)) if override["file"].is_relative_to(HOME) else str(override["file"])

    # 2. Page-level data file fallback
    data_file_rel = PAGE_DATA_FILE.get(page_key)
    if data_file_rel:
        json_path = DASHBOARDS / data_file_rel
        iso = iso_from_json_generated(json_path)
        if iso:
            return iso, data_file_rel

    # 3. HTML file mtime fallback (for static narrative sections)
    iso = iso_from_mtime(html_path)
    if iso:
        return iso, page_key + " (mtime)"
    return None, None


def main():
    manifest = {
        "generated": datetime.now(tz=timezone.utc).isoformat(),
        "pages": {},
    }

    page_keys = list(PAGE_DATA_FILE.keys())
    # Include any dashboard HTML not explicitly registered
    # Follow symlinks (body-system is a symlink)
    for html_file in DASHBOARDS.rglob("*.html"):
        rel = html_file.relative_to(DASHBOARDS).as_posix()
        if rel not in page_keys and not rel.startswith(("shared/", "validation/", "contrib-inputs/")):
            page_keys.append(rel)
    # Walk symlinked subdirs explicitly
    for entry in DASHBOARDS.iterdir():
        if entry.is_symlink() and entry.is_dir():
            for html_file in entry.rglob("*.html"):
                try:
                    rel = (entry.name + "/" + html_file.relative_to(entry.resolve()).as_posix())
                except ValueError:
                    continue
                if rel not in page_keys and not rel.startswith(("shared/", "validation/", "contrib-inputs/")):
                    page_keys.append(rel)

    for page_key in page_keys:
        html_path = DASHBOARDS / page_key
        # Follow symlinks for resolution
        if not html_path.exists():
            continue
        if html_path.is_symlink():
            html_path = html_path.resolve()
        elif not html_path.is_file():
            # Could be a symlinked parent dir
            parts = page_key.split("/", 1)
            if len(parts) == 2:
                parent = DASHBOARDS / parts[0]
                if parent.is_symlink():
                    html_path = parent.resolve() / parts[1]
            if not html_path.exists():
                continue
        sections = extract_h2_sections(html_path)
        # Merge in statically-registered sections for JS-rendered pages
        static = STATIC_SECTIONS.get(page_key, [])
        existing_ids = {s[0] for s in sections}
        for sid, heading in static:
            if sid not in existing_ids:
                sections.append((sid, heading))
        if not sections:
            continue
        page_entry = {}
        for section_id, heading_text in sections:
            iso, source = resolve_section_freshness(page_key, section_id, html_path)
            page_entry[section_id] = {
                "heading": heading_text,
                "updated_iso": iso,
                "source": source,
            }
        manifest["pages"][page_key] = page_entry

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(manifest, indent=2, default=str))
    total_sections = sum(len(p) for p in manifest["pages"].values())
    print(f"Wrote {OUTPUT}")
    print(f"Pages: {len(manifest['pages'])}, Sections: {total_sections}")


if __name__ == "__main__":
    main()
