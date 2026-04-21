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

MARKETS = [
    {"key": "au", "file": "au-paid-search-state.md", "label": "AU Paid Search"},
    {"key": "mx", "file": "mx-paid-search-state.md", "label": "MX Paid Search"},
    {"key": "ww", "file": "ww-testing-state.md", "label": "WW Testing"},
]


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

    record = {
        "frontmatter": fm,
        "title": fm.get("title", md_path.stem),
        "status": fm.get("status", "UNKNOWN"),
        "owner": fm.get("owner", ""),
        "updated": fm.get("updated", ""),
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


def build_comparison(markets_data):
    """Cross-market consolidation rows for the overview page."""
    rows = []
    for m in MARKETS:
        d = markets_data.get(m["key"], {})
        fm = d.get("frontmatter", {})
        # Count sections populated
        secs = d.get("sections", {})
        apps = d.get("appendices", {})
        rows.append({
            "market": m["label"],
            "key": m["key"],
            "status": d.get("status", "?"),
            "data_through": d.get("data_through", "?"),
            "updated": d.get("updated", "?"),
            "owner": d.get("owner", "?"),
            "goals": len(secs.get("goals", [])),
            "tenets": len(secs.get("tenets", [])),
            "priorities": len(secs.get("priorities", [])),
            "appendices": sorted(apps.keys()),
            "appendix_count": len(apps),
            "has_flags": "flags" in secs and bool(secs.get("flags")),
        })
    return rows


def build_schema_intersection(markets_data):
    """Detect which sections/appendices appear in which markets — surfaces
    consolidation / coverage gaps for the overview page."""
    all_sections = set()
    all_appendices = set()
    per_market_sections = {}
    per_market_appendices = {}
    for m in MARKETS:
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
            s: [m["key"] for m in MARKETS if s in per_market_sections[m["key"]]]
            for s in sorted(all_sections)
        },
        "appendix_coverage": {
            a: [m["key"] for m in MARKETS if a in per_market_appendices[m["key"]]]
            for a in sorted(all_appendices)
        },
    }


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)

    markets_data = {}
    for m in MARKETS:
        p = STATE_DIR / m["file"]
        if not p.exists():
            print(f"warn: missing {p}")
            continue
        markets_data[m["key"]] = parse_market(p)

    output = {
        "generated": datetime.now(timezone.utc).isoformat(),
        "markets": [m["key"] for m in MARKETS],
        "labels": {m["key"]: m["label"] for m in MARKETS},
        "data": markets_data,
        "comparison": build_comparison(markets_data),
        "schema": build_schema_intersection(markets_data),
    }

    OUT.write_text(json.dumps(output, indent=2, ensure_ascii=False))
    print(f"wrote {OUT}")
    print(f"  markets: {len(markets_data)}")
    for k, v in markets_data.items():
        secs = len(v.get("sections", {}))
        apps = len(v.get("appendices", {}))
        print(f"  {k}: {secs} sections, {apps} appendices, data_through={v.get('data_through')}")


if __name__ == "__main__":
    main()
