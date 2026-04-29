#!/usr/bin/env python3
"""
regenerate.py — rebuild per-market change-log markdown files from the canonical
CSVs that Richard uploads to ~/shared/uploads/changelogs/.

Why this exists:
    Change logs used to be maintained by hand in ~/shared/wiki/callouts/{market}/{market}-change-log.md.
    The CSV was the source of truth but the markdown files drifted weeks out of
    date, producing callouts that attributed performance to the wrong causes.
    This tool eliminates the staleness by treating the CSV as the source and
    regenerating the markdown deterministically.

Usage:
    python3 ~/shared/tools/change-log/regenerate.py                # all 10 markets
    python3 ~/shared/tools/change-log/regenerate.py --market au    # one market
    python3 ~/shared/tools/change-log/regenerate.py --dry-run      # no writes
    python3 ~/shared/tools/change-log/regenerate.py --since 2025-10-01

Behavior:
    - Discovers the most recent CSV per region (picks highest (N) suffix)
    - Parses both CSV schemas (MX_AU/NA_JP wide schema, EU5 narrow schema)
    - Expands multi-market rows ("US, CA, JP" → 3 rows, one per market)
    - Filters by date (default: 2025-10-01 onward — rolling ~30 week window)
    - Preserves YAML front-matter (duck_id, created) from existing markdown
    - Updates the `updated:` field in front-matter to today
    - Writes a sortable markdown table, most recent entries last
    - Idempotent: running twice produces byte-identical output

Source of truth: ~/shared/uploads/changelogs/AB - Change Log - *.csv
Output: ~/shared/wiki/callouts/{market}/{market}-change-log.md (10 files)
"""
from __future__ import annotations
import argparse
import csv
import datetime as dt
import glob
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path

HOME = Path(os.path.expanduser("~"))
UPLOAD_DIR = HOME / "shared" / "uploads" / "changelogs"
WIKI_CALLOUTS_DIR = HOME / "shared" / "wiki" / "callouts"

MARKETS = ["AU", "MX", "US", "CA", "JP", "UK", "DE", "FR", "IT", "ES"]

# Default filter: keep anything from this date onward. Rolling ~30-week window
# is enough context for the qualitative sweep in callouts without ballooning
# the file with 2023-2024 history the callout writer never consults.
DEFAULT_SINCE = dt.date(2025, 10, 1)


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class ChangeRow:
    """Normalized change-log entry. One row per market, even if the CSV row
    listed multiple markets."""
    date: dt.date
    market: str              # AU, MX, US, CA, JP, UK, DE, FR, IT, ES
    week: str                # "W17" or "" if unknown
    platform: str            # Google, Adobe, Meta, etc.
    cluster: str             # Brand / NB / All
    campaign: str            # Campaign or category label
    change: str              # The actual change description
    owner: str               # Richard, Yun, ...
    note: str                # Free-form trailing note

    def sort_key(self):
        return (self.date, self.market, self.cluster, self.campaign)


# ---------------------------------------------------------------------------
# CSV discovery + schema detection
# ---------------------------------------------------------------------------

def find_latest_csvs(upload_dir: Path) -> list[Path]:
    """Return the highest-(N) variant of each uploaded CSV.

    Files look like 'AB - Change Log - MX_AU  (6).csv'. If multiple exist with
    different (N), we pick the largest N. If there's no (N) suffix, we pick it.
    """
    if not upload_dir.exists():
        raise SystemExit(f"Upload dir not found: {upload_dir}")

    # Group by the base name without the "(N)" suffix
    groups: dict[str, list[tuple[int, Path]]] = {}
    for p in upload_dir.glob("AB - Change Log - *.csv"):
        m = re.match(r"^(.*?)(?:\s*\((\d+)\))?\.csv$", p.name)
        if not m:
            continue
        base = m.group(1).strip()
        n = int(m.group(2)) if m.group(2) else 0
        groups.setdefault(base, []).append((n, p))

    latest = []
    for base, candidates in groups.items():
        candidates.sort(reverse=True)  # highest N first
        latest.append(candidates[0][1])
    return sorted(latest)


def detect_schema(header: list[str]) -> str:
    """Return 'wide' (MX_AU / NA_JP) or 'narrow' (EU5)."""
    header_norm = [h.strip() for h in header]
    if "MKT" in header_norm and "Date" in header_norm and "Platform" in header_norm:
        return "wide"
    if "EU5" in header_norm:
        return "narrow"
    raise ValueError(f"Unknown CSV schema. Header: {header_norm}")


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------

_DATE_FORMATS = ("%m/%d/%Y", "%m/%d/%y", "%Y-%m-%d", "%d/%m/%Y", "%d-%b-%Y", "%d-%B-%Y")


def parse_date(raw: str) -> dt.date | None:
    raw = raw.strip()
    if not raw:
        return None
    for fmt in _DATE_FORMATS:
        try:
            return dt.datetime.strptime(raw, fmt).date()
        except ValueError:
            continue
    return None


def expand_markets(raw: str) -> list[str]:
    """CSV rows may list markets in messy forms:
        'US, CA, JP'        → clean multi-market
        'US,CA'             → no space
        'DE Google'         → market + platform suffix (strip suffix)
        'DE Google\\nFR Google' → newline-separated with platform suffix
        'UK/FR/IT/ES'       → slash-separated
        'FR, ES, UK'        → comma-separated with spaces
        'IT & UK'           → ampersand
        'EU5' / 'All' / ''  → collective or blank (drop)
    We split on any non-letter boundary, uppercase, and keep only valid 2-letter
    market codes from the MARKETS list.
    """
    out = []
    seen = set()
    # Tokenize: split on anything that isn't a letter
    for token in re.split(r"[^A-Za-z]+", raw):
        code = token.strip().upper()
        if code in MARKETS and code not in seen:
            out.append(code)
            seen.add(code)
    return out


def parse_wide_csv(path: Path) -> list[ChangeRow]:
    """Parse MX_AU and NA_JP schema.

    Columns (both files): WK, Date, MKT, Platform, Cluster, Category/Campaign,
                          Change Note, [Pending], [Reference], [Impact], Owner, [Note]
    NA_JP adds a 'Pending' column between Change Note and Reference; we handle
    both by looking up by header name.
    """
    rows: list[ChangeRow] = []
    with open(path, encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        header = [h.strip() for h in next(reader)]

        def col(name: str) -> int | None:
            return header.index(name) if name in header else None

        idx_wk = col("WK")
        idx_date = col("Date")
        idx_mkt = col("MKT")
        idx_plat = col("Platform")
        idx_cluster = col("Cluster")
        idx_camp = col("Category/Campaign")
        idx_change = col("Change Note")
        idx_owner = col("Owner")
        idx_note = col("Note")
        # Reference and Impact sit between Change and Owner; we don't surface
        # them in the markdown table but we read them if present for
        # completeness (could add to output later).

        for r in reader:
            if not r or all(not c.strip() for c in r):
                continue
            date = parse_date(r[idx_date]) if idx_date is not None else None
            if date is None:
                continue
            markets = expand_markets(r[idx_mkt]) if idx_mkt is not None else []
            if not markets:
                continue

            def cell(i):
                if i is None or i >= len(r):
                    return ""
                return r[i].strip()

            wk = cell(idx_wk)
            platform = cell(idx_plat)
            cluster = cell(idx_cluster)
            campaign = cell(idx_camp)
            change = cell(idx_change)
            owner = cell(idx_owner)
            note = cell(idx_note)

            # Normalize week: "W17" prefix
            if wk and not wk.upper().startswith("W"):
                wk = f"W{wk}"

            for mkt in markets:
                rows.append(ChangeRow(
                    date=date, market=mkt, week=wk,
                    platform=platform, cluster=cluster, campaign=campaign,
                    change=change, owner=owner, note=note,
                ))
    return rows


def parse_narrow_csv(path: Path) -> list[ChangeRow]:
    """Parse EU5 schema.

    The EU5 CSV has headers:
        (empty), EU5, Campaign, Category, Change (After), Owner, Impact/Reason (Before)
    Column A is actually Date. Column B (EU5) is the market code.
    """
    rows: list[ChangeRow] = []
    with open(path, encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        header = [h.strip() for h in next(reader)]

        # Positional — the EU5 file's header has an empty first column for Date.
        # Column layout: [0]=Date, [1]=MKT, [2]=Campaign, [3]=Category,
        #                [4]=Change (After), [5]=Owner, [6]=Impact/Reason (Before)
        for r in reader:
            if not r or all(not c.strip() for c in r):
                continue
            if len(r) < 6:
                r = r + [""] * (6 - len(r))
            date = parse_date(r[0])
            if date is None:
                continue
            markets = expand_markets(r[1])
            if not markets:
                continue

            campaign = r[2].strip()
            cluster = r[3].strip()    # EU5 "Category" maps to cluster in our model
            change = r[4].strip()
            owner = r[5].strip()
            note = r[6].strip() if len(r) > 6 else ""

            wk = ""  # EU5 CSV has no Week column
            for mkt in markets:
                rows.append(ChangeRow(
                    date=date, market=mkt, week=wk,
                    platform="Google",  # EU5 file is Google-only per Richard
                    cluster=cluster, campaign=campaign,
                    change=change, owner=owner, note=note,
                ))
    return rows


def parse_all(csvs: list[Path]) -> list[ChangeRow]:
    """Parse every CSV according to its detected schema."""
    all_rows: list[ChangeRow] = []
    for csv_path in csvs:
        try:
            with open(csv_path, encoding="utf-8-sig", newline="") as f:
                header = next(csv.reader(f))
            schema = detect_schema(header)
        except Exception as e:
            print(f"  [skip] {csv_path.name}: {e}", file=sys.stderr)
            continue

        try:
            if schema == "wide":
                rows = parse_wide_csv(csv_path)
            else:
                rows = parse_narrow_csv(csv_path)
        except Exception as e:
            print(f"  [error] {csv_path.name}: {e}", file=sys.stderr)
            continue

        print(f"  parsed {csv_path.name} ({schema}): {len(rows)} normalized rows")
        all_rows.extend(rows)
    return all_rows


# ---------------------------------------------------------------------------
# Markdown rendering
# ---------------------------------------------------------------------------

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
DUCK_ID_RE = re.compile(r"<!-- DOC-\d+ \| duck_id: [^\s]+ -->")
CREATED_RE = re.compile(r"^created: (.+)$", re.MULTILINE)


def load_existing_frontmatter(md_path: Path) -> tuple[str | None, str | None]:
    """Return (full_frontmatter_block_with_delimiters, duck_id_comment) from
    the existing markdown, or (None, None) if missing."""
    if not md_path.exists():
        return None, None
    text = md_path.read_text()
    fm_match = FRONTMATTER_RE.match(text)
    frontmatter = fm_match.group(0) if fm_match else None
    duck_match = DUCK_ID_RE.search(text)
    duck_comment = duck_match.group(0) if duck_match else None
    return frontmatter, duck_comment


def update_frontmatter(frontmatter: str, today: dt.date) -> str:
    """Replace the `updated:` field with today's date, leave everything else."""
    return re.sub(r"^updated: .+$", f"updated: {today.isoformat()}", frontmatter, flags=re.MULTILINE)


def default_frontmatter(market: str, today: dt.date) -> str:
    """Used when no existing markdown file is present. duck_id will be absent —
    the librarian/editor can add one on first read."""
    return (
        "---\n"
        f'title: "{market} Change Log (2026)"\n'
        "status: FINAL\n"
        "audience: amazon-internal\n"
        "owner: Richard Williams\n"
        f"created: {today.isoformat()}\n"
        f"updated: {today.isoformat()}\n"
        "---\n"
    )


def render_markdown(market: str, rows: list[ChangeRow], frontmatter: str, duck_comment: str | None) -> str:
    """Render the full markdown file content."""
    lines = [frontmatter]
    if duck_comment:
        lines.append(duck_comment + "\n")
    lines.append(f"\n# {market} Change Log (2026)\n")
    lines.append("\nSource: `~/shared/uploads/changelogs/AB - Change Log - *.csv` "
                 "(regenerated by `~/shared/tools/change-log/regenerate.py`). "
                 "Do not hand-edit — changes will be overwritten on next regeneration. "
                 "Add new entries by updating the source CSV and re-running the tool.\n")

    if not rows:
        lines.append("\n_No entries in the active window for this market._\n")
        return "".join(lines)

    # Table header
    lines.append("\n| Date | Week | Platform | Cluster | Campaign | Change | Owner | Note |\n")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |\n")

    for r in rows:
        date_str = r.date.strftime("%m/%d")  # WBR callouts use M/D format
        change = r.change.replace("|", "\\|").replace("\n", " ")
        note = r.note.replace("|", "\\|").replace("\n", " ")
        campaign = r.campaign.replace("|", "\\|")
        lines.append(
            f"| {date_str} | {r.week} | {r.platform} | {r.cluster} | {campaign} | "
            f"{change} | {r.owner} | {note} |\n"
        )
    return "".join(lines)


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------

def regenerate(
    markets: list[str],
    since: dt.date,
    dry_run: bool = False,
    upload_dir: Path = UPLOAD_DIR,
    output_dir: Path = WIKI_CALLOUTS_DIR,
) -> dict[str, int]:
    """Regenerate per-market change-log files. Returns {market: row_count}."""
    today = dt.date.today()

    print(f"Scanning uploads in {upload_dir}")
    csvs = find_latest_csvs(upload_dir)
    if not csvs:
        raise SystemExit(f"No change-log CSVs found in {upload_dir}")
    print(f"Found {len(csvs)} CSV(s):")
    for p in csvs:
        print(f"  - {p.name}")

    print("\nParsing...")
    all_rows = parse_all(csvs)
    print(f"Total normalized rows: {len(all_rows)}")

    # Filter by date window
    filtered = [r for r in all_rows if r.date >= since]
    print(f"Rows since {since.isoformat()}: {len(filtered)}")

    # Group by market
    by_market: dict[str, list[ChangeRow]] = {m: [] for m in MARKETS}
    for r in filtered:
        if r.market in by_market:
            by_market[r.market].append(r)

    # Sort each market's rows by date (oldest first — callouts read top to bottom chronologically)
    for m in by_market:
        by_market[m].sort(key=lambda r: r.sort_key())

    counts: dict[str, int] = {}
    for market in markets:
        rows = by_market.get(market, [])
        counts[market] = len(rows)
        out_path = output_dir / market.lower() / f"{market.lower()}-change-log.md"
        out_path.parent.mkdir(parents=True, exist_ok=True)

        existing_fm, duck_comment = load_existing_frontmatter(out_path)
        if existing_fm:
            frontmatter = update_frontmatter(existing_fm, today)
        else:
            frontmatter = default_frontmatter(market, today)

        content = render_markdown(market, rows, frontmatter, duck_comment)

        if dry_run:
            print(f"  [dry-run] would write {out_path} ({len(rows)} rows)")
            continue

        # Only write if content changed (preserves mtime for unchanged files)
        if out_path.exists() and out_path.read_text() == content:
            print(f"  [unchanged] {out_path.name} ({len(rows)} rows)")
            continue

        out_path.write_text(content)
        print(f"  [wrote] {out_path.name} ({len(rows)} rows)")

    return counts


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--market", help="Process a single market (e.g. AU, MX, US). Default: all 10.")
    ap.add_argument("--since", default=DEFAULT_SINCE.isoformat(),
                    help=f"Only include entries on or after this ISO date. Default: {DEFAULT_SINCE.isoformat()}")
    ap.add_argument("--dry-run", action="store_true", help="Print what would change without writing.")
    ap.add_argument("--upload-dir", default=str(UPLOAD_DIR))
    ap.add_argument("--output-dir", default=str(WIKI_CALLOUTS_DIR))
    args = ap.parse_args()

    markets = [args.market.upper()] if args.market else MARKETS
    for m in markets:
        if m not in MARKETS:
            raise SystemExit(f"Unknown market: {m}. Valid: {', '.join(MARKETS)}")

    since = dt.date.fromisoformat(args.since)

    counts = regenerate(
        markets=markets,
        since=since,
        dry_run=args.dry_run,
        upload_dir=Path(args.upload_dir),
        output_dir=Path(args.output_dir),
    )

    print("\nSummary:")
    for m in markets:
        print(f"  {m}: {counts.get(m, 0)} entries")


if __name__ == "__main__":
    main()
