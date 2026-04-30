#!/usr/bin/env python3
"""Refresh state-files dashboard data.

Parses the 3 market state files (~/shared/wiki/state-files/*.md) into a single
JSON artifact consumed by shared/dashboards/state-files/*.html.
"""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path.home()
STATE_DIR = ROOT / "shared" / "wiki" / "state-files"
OUT = ROOT / "shared" / "dashboards" / "data" / "state-files-data.json"

# Display-ordering hint — keys listed here render in this order; anything else
# appends alphabetically after. Makes the nav stable even as new markets get
# added without us having to touch this file — drop a new `*-state.md` into
# shared/wiki/state-files/ and it shows up automatically.
MARKET_ORDER_HINT = ["au", "mx", "ww"]


def derive_market_key(filename: str) -> str:
    """Pull the 2-4 char lowercase prefix before the first hyphen.

    au-paid-search-state.md  -> 'au'
    ww-testing-state.md      -> 'ww'
    latam-paid-search-state.md -> 'latam'
    """
    return filename.split("-", 1)[0].lower()


def derive_market_label(frontmatter: dict, key: str) -> str:
    """Strip the ' — Daily State File' / ' - State File' suffix from the
    front-matter title if present, otherwise fall back to uppercasing the key.
    """
    title = frontmatter.get("title", "")
    if title:
        # Common suffixes to strip so the nav reads 'AU Paid Search' not
        # 'AU Paid Search — Daily State File'
        for sep in [" — ", " - ", " – "]:
            if sep in title:
                title = title.split(sep, 1)[0]
                break
        return title.strip()
    return key.upper()


def discover_markets(state_dir: Path) -> list[dict]:
    """Walk the state-files directory, pick up every `*-state.md`, derive
    key+label from filename+front-matter. No hand-maintained registry."""
    found = []
    for p in sorted(state_dir.glob("*-state.md")):
        key = derive_market_key(p.name)
        # Peek at front-matter for label only
        raw = p.read_text(encoding="utf-8")
        fm, _ = parse_frontmatter(raw)
        found.append({
            "key": key,
            "file": p.name,
            "label": derive_market_label(fm, key),
        })

    # Re-order by hint
    ordered = []
    seen = set()
    for hint_key in MARKET_ORDER_HINT:
        for m in found:
            if m["key"] == hint_key:
                ordered.append(m)
                seen.add(m["key"])
                break
    for m in found:
        if m["key"] not in seen:
            ordered.append(m)
    return ordered


def parse_frontmatter(text):
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end < 0:
        return {}, text
    fm_block = text[3:end].strip()
    body = text[end + 4:].lstrip()
    fm = {}
    for line in fm_block.splitlines():
        if ":" not in line:
            continue
        k, _, v = line.partition(":")
        fm[k.strip()] = v.strip().strip('"')
    return fm, body


def split_sections(body):
    parts = re.split(r"(?m)^## ", body)
    out = []
    for chunk in parts[1:]:
        head, _, rest = chunk.partition("\n")
        out.append((head.strip(), rest.strip()))
    return out


def clean_paragraph(t):
    return re.sub(r"\s+", " ", t).strip()


def parse_numbered_list(text):
    items = []
    for m in re.finditer(r"(?m)^\d+\.\s+(.+?)(?=\n\d+\.\s|\n\n|\Z)", text, re.DOTALL):
        items.append(clean_paragraph(m.group(1)))
    return items


def parse_bullets(text):
    items = []
    for m in re.finditer(r"(?m)^[-*]\s+(.+?)(?=\n[-*]\s|\n\n|\Z)", text, re.DOTALL):
        items.append(clean_paragraph(m.group(1)))
    return items


def parse_markdown_table(text):
    lines = [ln for ln in text.splitlines() if ln.strip().startswith("|")]
    if len(lines) < 2:
        return []
    header = [c.strip() for c in lines[0].strip().strip("|").split("|")]
    rows = []
    for ln in lines[2:]:
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if len(cells) != len(header):
            continue
        rows.append(dict(zip(header, cells)))
    return rows


def parse_all_tables(text):
    tables = []
    buf = []
    for ln in text.splitlines():
        if ln.strip().startswith("|"):
            buf.append(ln)
        else:
            if buf:
                t = parse_markdown_table("\n".join(buf))
                if t:
                    tables.append(t)
                buf = []
    if buf:
        t = parse_markdown_table("\n".join(buf))
        if t:
            tables.append(t)
    return tables


def first_paragraphs(text, n=3):
    paras = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    paras = [p for p in paras if not p.startswith("|")]
    return [clean_paragraph(p) for p in paras[:n]]


def find_section(sections, prefix):
    """Return first section whose heading starts with prefix (case-insensitive)."""
    for head, content in sections:
        if head.lower().startswith(prefix.lower()):
            return content
    return None


def parse_market(md_path):
    raw = md_path.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(raw)
    sections = split_sections(body)
    sections_dict = dict(sections)

    # File mtime = last physical edit to the markdown (most trustworthy
    # signal of when anything actually changed, vs the frontmatter `updated:`
    # which depends on a hook remembering to rewrite it).
    import os
    mtime_ts = os.path.getmtime(md_path)
    file_mtime = datetime.fromtimestamp(mtime_ts, tz=timezone.utc).strftime("%Y-%m-%d")

    record = {
        "frontmatter": fm,
        "title": fm.get("title", md_path.stem),
        "status": fm.get("status", "UNKNOWN"),
        "owner": fm.get("owner", ""),
        # `updated` prefers the front-matter (hook-written) but falls back to
        # file mtime if the hook never stamped one. We also track both values
        # separately so the dashboard can flag when they diverge.
        "updated": fm.get("updated", "") or file_mtime,
        "updated_frontmatter": fm.get("updated", ""),
        "updated_mtime": file_mtime,
        "data_through": fm.get("data_through", ""),
        "sections": {},
        "tables": {},
        "appendices": {},
    }

    # Prose sections
    for key, heading in [
        ("introduction", "Introduction"),
        ("state", "State of the Business"),
        ("flags", "Flags"),
        ("lessons", "Lessons Learned"),
    ]:
        if heading in sections_dict:
            record["sections"][key] = first_paragraphs(sections_dict[heading], n=5)

    # Numbered lists
    if "Goals" in sections_dict:
        record["sections"]["goals"] = parse_numbered_list(sections_dict["Goals"])
    if "Tenets" in sections_dict:
        record["sections"]["tenets"] = parse_numbered_list(sections_dict["Tenets"])
    if "Strategic Priorities" in sections_dict:
        items = parse_numbered_list(sections_dict["Strategic Priorities"])
        if not items:
            items = parse_bullets(sections_dict["Strategic Priorities"])
        record["sections"]["priorities"] = items

    # State of the Business — extract input/output tables
    if "State of the Business" in sections_dict:
        tables = parse_all_tables(sections_dict["State of the Business"])
        if tables:
            record["tables"]["inputs"] = tables[0]
        if len(tables) > 1:
            record["tables"]["outputs"] = tables[1]

    # Flags table (if AU/MX)
    if "Flags" in sections_dict:
        flag_tables = parse_all_tables(sections_dict["Flags"])
        if flag_tables:
            record["tables"]["flags"] = flag_tables[0]

    # Appendices — parse each by heading prefix
    appendix_specs = [
        ("weekly_trend", "Appendix A"),
        ("yoy", "Appendix B"),
        ("monthly_projection", "Appendix C"),
        ("plan_summary", "Appendix D"),
        ("change_log", "Appendix E"),
        ("variance_bridge", "Appendix F"),
        ("source_links", "Appendix G"),
        ("placeholder_schema", "Appendix H"),
    ]
    for key, prefix in appendix_specs:
        content = find_section(sections, prefix)
        if content is None:
            continue
        entry = {"heading": prefix}
        tables = parse_all_tables(content)
        if tables:
            entry["tables"] = tables
        paras = first_paragraphs(content, n=6)
        if paras:
            entry["paragraphs"] = paras
        bullets = parse_bullets(content)
        if bullets and not tables:
            entry["bullets"] = bullets
        record["appendices"][key] = entry

    # Headline KPIs — try to extract from first paragraph of State of the Business
    state_prose = record["sections"].get("state", [""])[0] if record["sections"].get("state") else ""
    record["headline"] = state_prose

    return record


def _load_live_data_recency():
    """Pull the canonical 'how current is our data' signals from the same
    sources the performance section reads. Returns a dict like:

        {
          "forecast_generated": "2026-04-29T22:35:42Z",
          "forecast_last_data_date": "2026-04-19",
          "forecast_max_week": 16,
          "projection_generated": "2026-04-30T...",
        }

    These override the stale frontmatter `updated`/`data_through` values
    in the comparison + freshness tables so the dashboard never claims
    the market is frozen at Apr 20 when the underlying data is through
    Apr 19 / W16.
    """
    out = {}
    forecast_path = Path.home() / "shared" / "dashboards" / "data" / "forecast-data.json"
    projection_path = Path.home() / "shared" / "dashboards" / "data" / "projection-data.json"
    if forecast_path.exists():
        try:
            fd = json.loads(forecast_path.read_text())
            out["forecast_generated"] = fd.get("generated")
            out["forecast_last_data_date"] = fd.get("last_data_date")
            out["forecast_max_week"] = fd.get("max_week")
        except Exception as e:
            print(f"warn: couldn't read forecast-data.json recency: {e}")
    if projection_path.exists():
        try:
            pd = json.loads(projection_path.read_text())
            out["projection_generated"] = pd.get("generated")
        except Exception as e:
            print(f"warn: couldn't read projection-data.json recency: {e}")
    return out


def _fmt_data_through_from_week(year: int, week: int) -> str:
    """Render a data_through string in the same shape the state files use
    ('2026 W15 (Apr 6–12)') given a fiscal year + ISO week. Used to overlay
    the markdown's stale data_through with what forecast-data.json actually
    carries."""
    from datetime import date, timedelta
    # ISO week N → Monday of that week
    jan4 = date(year, 1, 4)
    week1_monday = jan4 - timedelta(days=jan4.isoweekday() - 1)
    monday = week1_monday + timedelta(weeks=week - 1)
    sunday = monday + timedelta(days=6)
    month_abbr = monday.strftime("%b")
    if monday.month == sunday.month:
        return f"{year} W{week} ({month_abbr} {monday.day}\u2013{sunday.day})"
    return f"{year} W{week} ({month_abbr} {monday.day}\u2013{sunday.strftime('%b')} {sunday.day})"


def build_comparison(markets_data, markets_list, live_recency=None):
    """Cross-market consolidation rows for the overview page.

    When `live_recency` is provided (forecast-data.json + projection-data.json
    metadata), `updated` and `data_through` prefer live pipeline values over
    the markdown frontmatter. This protects the dashboard from looking stale
    when AM-Backend Step 2E hasn't rewritten the markdowns recently — the
    numbers the performance section shows are current, so these columns
    should match.
    """
    live_recency = live_recency or {}
    live_updated = None
    if live_recency.get("forecast_generated"):
        try:
            live_updated = live_recency["forecast_generated"][:10]  # YYYY-MM-DD
        except Exception:
            live_updated = None
    live_data_through = None
    if live_recency.get("forecast_max_week"):
        try:
            live_data_through = _fmt_data_through_from_week(
                int((live_recency.get("forecast_generated") or "2026-01-01")[:4]),
                int(live_recency["forecast_max_week"]),
            )
        except Exception:
            live_data_through = None

    rows = []
    for m in markets_list:
        d = markets_data.get(m["key"], {})
        fm = d.get("frontmatter", {})
        # Count sections populated
        secs = d.get("sections", {})
        apps = d.get("appendices", {})

        # Stale-frontmatter detection: if the markdown's `updated:` lags the
        # live pipeline's last-refresh, surface the gap. >7 days => the
        # UI should show a stale-ness warning.
        fm_updated = d.get("updated_frontmatter") or d.get("updated", "")
        stale_days = None
        if fm_updated and live_updated:
            try:
                d1 = datetime.strptime(fm_updated, "%Y-%m-%d").date()
                d2 = datetime.strptime(live_updated, "%Y-%m-%d").date()
                stale_days = (d2 - d1).days
            except Exception:
                stale_days = None

        rows.append({
            "market": m["label"],
            "key": m["key"],
            "status": d.get("status", "?"),
            # Prefer live pipeline values over markdown frontmatter so the
            # dashboard tracks performance-section recency even when the
            # narrative markdowns lag.
            "data_through": live_data_through or d.get("data_through", "?"),
            "data_through_frontmatter": d.get("data_through", "?"),
            "updated": live_updated or d.get("updated", "?"),
            "updated_frontmatter": fm_updated or "?",
            "stale_days": stale_days,
            "owner": d.get("owner", "?"),
            "goals": len(secs.get("goals", [])),
            "tenets": len(secs.get("tenets", [])),
            "priorities": len(secs.get("priorities", [])),
            "appendices": sorted(apps.keys()),
            "appendix_count": len(apps),
            "has_flags": "flags" in secs and bool(secs.get("flags")),
        })
    return rows


def build_schema_intersection(markets_data, markets_list):
    """Detect which sections/appendices appear in which markets — surfaces
    consolidation / coverage gaps for the overview page."""
    all_sections = set()
    all_appendices = set()
    per_market_sections = {}
    per_market_appendices = {}
    for m in markets_list:
        d = markets_data.get(m["key"], {})
        s = set(d.get("sections", {}).keys())
        a = set(d.get("appendices", {}).keys())
        per_market_sections[m["key"]] = s
        per_market_appendices[m["key"]] = a
        all_sections |= s
        all_appendices |= a
    return {
        "sections": sorted(all_sections),
        "appendices": sorted(all_appendices),
        "section_coverage": {
            s: [m["key"] for m in markets_list if s in per_market_sections[m["key"]]]
            for s in sorted(all_sections)
        },
        "appendix_coverage": {
            a: [m["key"] for m in markets_list if a in per_market_appendices[m["key"]]]
            for a in sorted(all_appendices)
        },
    }


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)

    markets_list = discover_markets(STATE_DIR)
    if not markets_list:
        print(f"warn: no *-state.md files found in {STATE_DIR}")

    markets_data = {}
    for m in markets_list:
        p = STATE_DIR / m["file"]
        if not p.exists():
            print(f"warn: missing {p}")
            continue
        markets_data[m["key"]] = parse_market(p)

    # Pull live recency from the same sources the performance section uses.
    # These override the frontmatter updated/data_through in the comparison
    # table so the overview tracks actual pipeline freshness.
    live_recency = _load_live_data_recency()

    output = {
        "generated": datetime.now(timezone.utc).isoformat(),
        "markets": [m["key"] for m in markets_list],
        "labels": {m["key"]: m["label"] for m in markets_list},
        "files": {m["key"]: m["file"] for m in markets_list},
        "live_recency": live_recency,
        "data": markets_data,
        "comparison": build_comparison(markets_data, markets_list, live_recency),
        "schema": build_schema_intersection(markets_data, markets_list),
    }

    OUT.write_text(json.dumps(output, indent=2, ensure_ascii=False))
    print(f"wrote {OUT}")
    print(f"  markets ({len(markets_list)}): {', '.join(m['key'] for m in markets_list)}")
    for k, v in markets_data.items():
        secs = len(v.get("sections", {}))
        apps = len(v.get("appendices", {}))
        print(f"  {k}: {secs} sections, {apps} appendices, data_through={v.get('data_through')}")


if __name__ == "__main__":
    main()
