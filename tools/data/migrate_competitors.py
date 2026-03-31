#!/usr/bin/env python3
"""
Migrate competitor data from eyes.md to DuckDB competitors table.

Parses the Competitive Landscape section of eyes.md and writes rows
to the competitors table via db_upsert(). Idempotent — safe to re-run.

Usage:
    python3 migrate_competitors.py [--eyes PATH] [--db PATH] [--dry-run]
"""

import os
import re
import sys
import argparse
import logging

# Add parent dir so we can import query.py
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from query import db_upsert, db, DB_PATH

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

EYES_PATH = os.path.expanduser('~/shared/context/body/eyes.md')

# Current week label for snapshot data (eyes.md is a point-in-time snapshot)
DEFAULT_WEEK = '2026 W13'


def parse_competitor_tables(text):
    """Parse all competitor tables from eyes.md Competitive Landscape section.

    Returns list of dicts ready for db_upsert into competitors table.
    """
    rows = []

    # --- US: Walmart Business (narrative section) ---
    us_walmart = re.search(
        r'### US: Walmart Business.*?(\d+)-(\d+)%\s*\(Jan-Mar 2026\)',
        text, re.DOTALL
    )
    if us_walmart:
        # Use the range high end for latest IS
        is_high = float(us_walmart.group(2))
        rows.append({
            'market': 'US',
            'competitor': 'Walmart Business',
            'week': DEFAULT_WEEK,
            'impression_share': is_high,
            'cpc_impact_pct': None,
            'segment': 'brand',
            'notes': 'Brand Core. IS 37-55% Jan-Mar 2026. Brand CPA impact: ~$40 avg → $65-$77 range.',
        })
    else:
        logger.warning('Could not parse US Walmart Business section')

    # --- EU5 Competitors table ---
    eu5_match = re.search(r'### EU5 Competitors\s*\n\|.*?\n\|[-\s|]+\n((?:\|.*\n)*)', text)
    if eu5_match:
        for line in eu5_match.group(1).strip().split('\n'):
            cols = [c.strip() for c in line.split('|')[1:-1]]
            if len(cols) >= 4:
                market, competitor, is_str, impact = cols[0], cols[1], cols[2], cols[3]
                is_val = _parse_impression_share(is_str)
                cpc_pct = _parse_cpc_impact(impact)
                segment = _parse_segment(is_str)
                rows.append({
                    'market': market,
                    'competitor': competitor,
                    'week': DEFAULT_WEEK,
                    'impression_share': is_val,
                    'cpc_impact_pct': cpc_pct,
                    'segment': segment,
                    'notes': impact,
                })
    else:
        logger.warning('Could not parse EU5 Competitors table')

    # --- International Competitors table ---
    intl_match = re.search(r'### International Competitors\s*\n\|.*?\n\|[-\s|]+\n((?:\|.*\n)*)', text)
    if intl_match:
        for line in intl_match.group(1).strip().split('\n'):
            cols = [c.strip() for c in line.split('|')[1:-1]]
            if len(cols) >= 4:
                market, competitor, is_str, notes = cols[0], cols[1], cols[2], cols[3]
                is_val = _parse_impression_share(is_str)
                cpc_pct = _parse_cpc_impact(notes)
                segment = _parse_segment(is_str)
                rows.append({
                    'market': market,
                    'competitor': competitor,
                    'week': DEFAULT_WEEK,
                    'impression_share': is_val,
                    'cpc_impact_pct': cpc_pct,
                    'segment': segment,
                    'notes': notes,
                })
    else:
        logger.warning('Could not parse International Competitors table')

    return rows


def _parse_impression_share(is_str):
    """Extract numeric impression share from strings like '24% Brand', '<10% ES Brand', '39-47% Generic NB'."""
    # Try range: take the high end
    range_match = re.search(r'(\d+)-(\d+)%', is_str)
    if range_match:
        return float(range_match.group(2))
    # Try single value
    single_match = re.search(r'[<>]?(\d+)%', is_str)
    if single_match:
        return float(single_match.group(1))
    return None


def _parse_cpc_impact(text):
    """Extract CPC impact percentage from notes like '+45% Brand Core CPC', '+13% CPC'."""
    match = re.search(r'([+-]?\d+)%\s*(?:Brand\s*(?:Core\s*)?)?CPC', text)
    if match:
        return float(match.group(1))
    return None


def _parse_segment(is_str):
    """Infer segment from IS string like '24% Brand', '13% Generic NB'."""
    lower = is_str.lower()
    if 'generic' in lower or 'nb' in lower:
        return 'nb'
    if 'brand' in lower:
        return 'brand'
    return 'unknown'


def run_migration(eyes_path=None, db_path=None, dry_run=False):
    """Run the competitor migration. Returns count of rows processed."""
    path = eyes_path or EYES_PATH
    if not os.path.exists(path):
        logger.error(f'eyes.md not found at {path}')
        return 0

    with open(path) as f:
        text = f.read()

    rows = parse_competitor_tables(text)
    if not rows:
        logger.warning('No competitor data parsed from eyes.md')
        return 0

    logger.info(f'Parsed {len(rows)} competitor rows from eyes.md')

    if dry_run:
        for r in rows:
            logger.info(f'  [DRY RUN] {r["market"]} / {r["competitor"]} / IS={r["impression_share"]}')
        return len(rows)

    written = 0
    for r in rows:
        try:
            db_upsert('competitors', r, ['market', 'competitor', 'week'], db_path=db_path)
            written += 1
            logger.info(f'  ✓ {r["market"]} / {r["competitor"]} (IS={r["impression_share"]}%)')
        except Exception as e:
            logger.error(f'  ✗ {r["market"]} / {r["competitor"]}: {e}')

    logger.info(f'Migration complete: {written}/{len(rows)} rows written')
    return written


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Migrate competitor data from eyes.md to DuckDB')
    parser.add_argument('--eyes', default=EYES_PATH, help='Path to eyes.md')
    parser.add_argument('--db', default=DB_PATH, help='Database path')
    parser.add_argument('--dry-run', action='store_true', help='Parse only, do not write')
    args = parser.parse_args()
    run_migration(eyes_path=args.eyes, db_path=args.db, dry_run=args.dry_run)
