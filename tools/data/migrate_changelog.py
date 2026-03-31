#!/usr/bin/env python3
"""
Migrate change log entries from per-market markdown files to DuckDB change_log table.

Parses structured table entries from {market}-change-log.md files and writes
rows to the change_log table via db_upsert(). Narrative entries stay in markdown.
Idempotent — safe to re-run.

Usage:
    python3 migrate_changelog.py [--db PATH] [--dry-run]
"""

import os
import re
import sys
import argparse
import logging
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from query import db_upsert, db, db_write, DB_PATH

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

CALLOUTS_DIR = os.path.expanduser('~/shared/context/active/callouts')
MARKETS = ['us', 'uk', 'de', 'fr', 'it', 'es', 'ca', 'jp', 'au', 'mx']
YEAR = 2026  # Default year for date parsing


def find_changelog_files():
    """Find all change log markdown files across market directories."""
    files = {}
    for market in MARKETS:
        market_dir = os.path.join(CALLOUTS_DIR, market)
        if not os.path.isdir(market_dir):
            continue
        # Try both naming conventions
        candidates = [
            os.path.join(market_dir, f'{market}-change-log.md'),
            os.path.join(market_dir, 'change-log.md'),
        ]
        for path in candidates:
            if os.path.exists(path):
                files[market.upper()] = path
                break
    return files


def parse_changelog_table(text, market):
    """Parse a change log markdown table into structured rows.

    The tables have columns: Date | Platform | Cluster | Campaign | Change | Owner | Note
    Returns list of dicts ready for the change_log table.
    """
    rows = []

    # Find markdown table rows (skip header and separator)
    table_match = re.search(
        r'\|[^\n]*Date[^\n]*\|\s*\n\|[-\s|]+\n((?:\|.*\n)*)',
        text
    )
    if not table_match:
        logger.warning(f'  No table found in {market} change log')
        return rows

    for line in table_match.group(1).strip().split('\n'):
        cols = [c.strip() for c in line.split('|')]
        # Remove empty first/last from split
        cols = [c for c in cols if c or cols.index(c) not in (0, len(cols)-1)]
        # Filter out truly empty splits from leading/trailing pipes
        if line.startswith('|'):
            cols = [c.strip() for c in line.split('|')[1:-1]]

        if len(cols) < 5:
            continue

        date_str = cols[0].strip()
        platform = cols[1].strip() if len(cols) > 1 else ''
        cluster = cols[2].strip() if len(cols) > 2 else ''
        campaign = cols[3].strip() if len(cols) > 3 else ''
        change = cols[4].strip() if len(cols) > 4 else ''
        owner = cols[5].strip() if len(cols) > 5 else ''
        note = cols[6].strip() if len(cols) > 6 else ''

        parsed_date = _parse_changelog_date(date_str)
        if not parsed_date:
            logger.warning(f'  Skipping unparseable date: {date_str}')
            continue

        category = _infer_category(change, cluster)
        description = f'[{platform}] [{cluster}] {campaign}: {change}'
        if note:
            description += f' ({note})'

        rows.append({
            'market': market,
            'date': parsed_date,
            'category': category,
            'description': description,
            'impact_metric': None,
            'impact_value': None,
            'source': 'changelog_migration',
        })

    return rows


def _parse_changelog_date(date_str):
    """Parse date from formats like '1/12', '2/3', '3/17'."""
    match = re.match(r'(\d{1,2})/(\d{1,2})', date_str.strip())
    if match:
        month, day = int(match.group(1)), int(match.group(2))
        try:
            return datetime(YEAR, month, day).strftime('%Y-%m-%d')
        except ValueError:
            return None
    return None


def _infer_category(change, cluster):
    """Infer change category from the change description and cluster."""
    lower = change.lower()
    if any(w in lower for w in ['budget', 'spend', '$']):
        return 'budget'
    if any(w in lower for w in ['bid', 'cpc', 'cpt', 'troas', 'roas']):
        return 'bid_strategy'
    if any(w in lower for w in ['negative', 'negatives']):
        return 'negative_kw'
    if any(w in lower for w in ['url', 'landing page', 'lp', 'suffix', 'param']):
        return 'url_migration'
    if any(w in lower for w in ['promo', 'promotion', 'discount', 'off']):
        return 'promo'
    if any(w in lower for w in ['pmax', 'campaign', 'consolidat', 'launch', 'live', 'paused', 'enabled']):
        return 'campaign_change'
    if any(w in lower for w in ['data exclusion', 'exclusion']):
        return 'data_exclusion'
    return 'other'


def run_migration(db_path=None, dry_run=False):
    """Run the change log migration across all markets. Returns total rows."""
    files = find_changelog_files()
    if not files:
        logger.warning('No change log files found')
        return 0

    logger.info(f'Found {len(files)} change log files: {", ".join(files.keys())}')

    # Get next sequence value for IDs
    total = 0
    for market, path in sorted(files.items()):
        logger.info(f'Processing {market}: {os.path.basename(path)}')
        with open(path) as f:
            text = f.read()

        rows = parse_changelog_table(text, market)
        if not rows:
            logger.info(f'  No structured entries found')
            continue

        logger.info(f'  Parsed {len(rows)} entries')

        if dry_run:
            for r in rows:
                logger.info(f'    [DRY RUN] {r["date"]} {r["category"]}: {r["description"][:60]}...')
            total += len(rows)
            continue

        written = _batch_insert_changelog(rows, db_path)
        logger.info(f'  Written: {written}/{len(rows)}')
        total += written

    logger.info(f'Migration complete: {total} total rows written')
    return total


def _batch_insert_changelog(rows, db_path=None):
    """Insert changelog rows using a single connection with sequence IDs."""
    import duckdb
    path = db_path or DB_PATH
    con = duckdb.connect(path)
    written = 0
    try:
        for r in rows:
            try:
                seq_id = con.execute("SELECT nextval('change_log_seq')").fetchone()[0]
                con.execute(
                    "INSERT INTO change_log (id, market, date, category, description, impact_metric, impact_value, source) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    [seq_id, r['market'], r['date'], r['category'], r['description'],
                     r['impact_metric'], r['impact_value'], r['source']]
                )
                written += 1
            except Exception as e:
                logger.error(f'    ✗ {r["date"]}: {e}')
    finally:
        con.close()
    return written


def _next_changelog_id(db_path=None):
    """Get next ID from the change_log_seq sequence."""
    import duckdb
    path = db_path or DB_PATH
    con = duckdb.connect(path)
    try:
        val = con.execute("SELECT nextval('change_log_seq')").fetchone()[0]
        return val
    finally:
        con.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Migrate change logs from markdown to DuckDB')
    parser.add_argument('--db', default=DB_PATH, help='Database path')
    parser.add_argument('--dry-run', action='store_true', help='Parse only, do not write')
    args = parser.parse_args()
    run_migration(db_path=args.db, dry_run=args.dry_run)
