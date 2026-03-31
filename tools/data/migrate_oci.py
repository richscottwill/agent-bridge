#!/usr/bin/env python3
"""
Migrate OCI rollout status from eyes.md to DuckDB oci_status table.

Parses the OCI Performance section of eyes.md and writes rows
to the oci_status table via db_upsert(). Idempotent — safe to re-run.

Usage:
    python3 migrate_oci.py [--eyes PATH] [--db PATH] [--dry-run]
"""

import os
import re
import sys
import argparse
import logging
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from query import db_upsert, db, DB_PATH

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

EYES_PATH = os.path.expanduser('~/shared/context/body/eyes.md')


def parse_oci_tables(text):
    """Parse OCI rollout and impact tables from eyes.md.

    Returns list of dicts ready for db_upsert into oci_status table.
    """
    rows = {}  # keyed by market so we can merge rollout + impact

    # --- Rollout Timeline table ---
    rollout_match = re.search(
        r'### Rollout Timeline\s*\n\|.*?\n\|[-\s|]+\n((?:\|.*\n)*)',
        text
    )
    if rollout_match:
        for line in rollout_match.group(1).strip().split('\n'):
            cols = [c.strip() for c in line.split('|')[1:-1]]
            if len(cols) >= 4:
                market = cols[0]
                status_raw = cols[1]
                launch_raw = cols[2]
                impact_raw = cols[3]

                status = _normalize_status(status_raw)
                launch_date = _parse_date(launch_raw)
                impact_date = _parse_date(impact_raw)

                rows[market] = {
                    'market': market,
                    'status': status,
                    'launch_date': launch_date,
                    'full_impact_date': impact_date,
                    'reg_lift_pct': None,
                    'cpa_improvement': None,
                    'notes': f'Raw: {status_raw} | Launch: {launch_raw} | Impact: {impact_raw}',
                }
    else:
        logger.warning('Could not parse OCI Rollout Timeline table')

    # --- Impact Summary table ---
    impact_match = re.search(
        r'### Impact Summary\s*\n\|.*?\n\|[-\s|]+\n((?:\|.*\n)*)',
        text
    )
    if impact_match:
        for line in impact_match.group(1).strip().split('\n'):
            cols = [c.strip() for c in line.split('|')[1:-1]]
            if len(cols) >= 4:
                market = cols[0].strip('*')  # Handle **Total** bold
                if market == 'Total':
                    continue
                reg_lift = _parse_reg_lift(cols[2])
                cpa_imp = cols[3].strip() if len(cols) > 3 else None

                if market in rows:
                    rows[market]['reg_lift_pct'] = reg_lift
                    rows[market]['cpa_improvement'] = cpa_imp
                else:
                    rows[market] = {
                        'market': market,
                        'status': 'live',
                        'launch_date': None,
                        'full_impact_date': None,
                        'reg_lift_pct': reg_lift,
                        'cpa_improvement': cpa_imp,
                        'notes': None,
                    }
    else:
        logger.warning('Could not parse OCI Impact Summary table')

    return list(rows.values())


def _normalize_status(raw):
    """Normalize status string to one of: live, in_progress, not_planned."""
    lower = raw.lower().strip()
    if 'live' in lower:
        return 'live'
    if 'in progress' in lower:
        return 'in_progress'
    if 'not planned' in lower:
        return 'not_planned'
    return lower


def _parse_date(raw):
    """Parse date from strings like 'Jul 2025', 'Mar 2026 (E2E 3/4)', 'N/A'."""
    if not raw or raw.strip() == 'N/A':
        return None
    # Try "Mon YYYY" pattern
    match = re.search(r'([A-Z][a-z]{2})\s+(\d{4})', raw)
    if match:
        try:
            return datetime.strptime(f'{match.group(1)} {match.group(2)}', '%b %Y').strftime('%Y-%m-%d')
        except ValueError:
            pass
    # Try "M/D" pattern with implied year 2026
    match = re.search(r'(\d{1,2})/(\d{1,2})', raw)
    if match:
        try:
            return datetime.strptime(f'2026-{match.group(1)}-{match.group(2)}', '%Y-%m-%d').strftime('%Y-%m-%d')
        except ValueError:
            pass
    return None


def _parse_reg_lift(raw):
    """Parse reg lift percentage from strings like '+24% (+32K regs)', '+18% (+749 regs)'."""
    match = re.search(r'([+-]?\d+)%', raw)
    if match:
        return float(match.group(1))
    return None


def run_migration(eyes_path=None, db_path=None, dry_run=False):
    """Run the OCI status migration. Returns count of rows processed."""
    path = eyes_path or EYES_PATH
    if not os.path.exists(path):
        logger.error(f'eyes.md not found at {path}')
        return 0

    with open(path) as f:
        text = f.read()

    rows = parse_oci_tables(text)
    if not rows:
        logger.warning('No OCI data parsed from eyes.md')
        return 0

    logger.info(f'Parsed {len(rows)} OCI status rows from eyes.md')

    if dry_run:
        for r in rows:
            logger.info(f'  [DRY RUN] {r["market"]}: {r["status"]} (lift={r["reg_lift_pct"]}%)')
        return len(rows)

    written = 0
    for r in rows:
        try:
            db_upsert('oci_status', r, ['market'], db_path=db_path)
            written += 1
            logger.info(f'  ✓ {r["market"]}: {r["status"]} (lift={r["reg_lift_pct"]})')
        except Exception as e:
            logger.error(f'  ✗ {r["market"]}: {e}')

    logger.info(f'Migration complete: {written}/{len(rows)} rows written')
    return written


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Migrate OCI status from eyes.md to DuckDB')
    parser.add_argument('--eyes', default=EYES_PATH, help='Path to eyes.md')
    parser.add_argument('--db', default=DB_PATH, help='Database path')
    parser.add_argument('--dry-run', action='store_true', help='Parse only, do not write')
    args = parser.parse_args()
    run_migration(eyes_path=args.eyes, db_path=args.db, dry_run=args.dry_run)
