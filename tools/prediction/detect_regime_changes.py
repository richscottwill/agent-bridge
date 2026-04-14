#!/usr/bin/env python3
"""Detect regime changes from ps.change_log and insert into ps.regime_changes.

Scans change_log for structural entries (OCI launches, LP switches, pauses, etc.)
that don't already have a corresponding regime_changes entry. Auto-inserts with
default impact estimates based on change_type.

Run as part of WBR pipeline between ingestion and projections.

Usage: python3 detect_regime_changes.py
"""
import duckdb, os, uuid, re
sys_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
import sys; sys.path.insert(0, sys_path)
from prediction.config import MOTHERDUCK_TOKEN as TOKEN

# Default impact estimates by change_type (priors)
DEFAULTS = {
    'oci_launch':           ('registrations', 0.20, 0.6),
    'lp_switch':            ('registrations', -0.25, 0.5),
    'bid_strategy':         ('registrations', 0.0, 0.3),
    'campaign_restructure': ('registrations', 0.0, 0.3),
    'promo_launch':         ('registrations', 0.05, 0.4),
    'pause':                ('registrations', -0.50, 0.6),
    'other':                ('registrations', 0.0, 0.2),
}

# Pattern matching: description → change_type
PATTERNS = [
    (r'oci.*(?:100%|launch|dial.?up|complete|enabled)', 'oci_launch'),
    (r'polaris|landing.?page.*(?:switch|migrat|chang)', 'lp_switch'),
    (r'(?:max.?click|bid.?strateg|portfolio.?bid|target.?cpa)', 'bid_strategy'),
    (r'(?:restructur|two.?campaign|split|merge).*campaign', 'campaign_restructure'),
    (r'(?:promo|sitelink|event).*launch', 'promo_launch'),
    (r'paus(?:e|ed|ing)', 'pause'),
]


def classify_change(description, category):
    """Classify a change_log entry as a regime change type."""
    desc_lower = description.lower()
    
    # Check patterns
    for pattern, change_type in PATTERNS:
        if re.search(pattern, desc_lower):
            return change_type
    
    # Category-based fallback
    if category == 'launch':
        return 'promo_launch'
    
    return None  # Not structural


def run():
    con = duckdb.connect(f'md:ps_analytics?motherduck_token={TOKEN}')
    
    # Get all change_log entries not already linked to a regime_change
    existing_source_ids = set()
    rows = con.execute("SELECT source_id FROM ps.regime_changes WHERE source_id IS NOT NULL").fetchall()
    for r in rows:
        existing_source_ids.add(r[0])
    
    # Get existing regime changes by (market, change_date) to avoid duplicates
    existing_keys = set()
    rows2 = con.execute("SELECT market, change_date, change_type FROM ps.regime_changes").fetchall()
    for r in rows2:
        existing_keys.add((r[0], str(r[1]), r[2]))
    
    # Scan change_log
    changes = con.execute("SELECT id, market, date, category, description FROM ps.change_log ORDER BY date").fetchall()
    
    inserted = 0
    for cl_id, market, dt, category, description in changes:
        # Skip if already linked
        if cl_id in existing_source_ids:
            continue
        
        # Classify
        change_type = classify_change(description, category)
        if not change_type:
            continue
        
        # Skip if duplicate (same market, date, type)
        key = (market, str(dt), change_type)
        if key in existing_keys:
            continue
        
        # Get defaults
        metric, impact, confidence = DEFAULTS.get(change_type, DEFAULTS['other'])
        
        # Insert
        rid = str(uuid.uuid4())
        con.execute("""INSERT INTO ps.regime_changes 
            (id, market, change_date, change_type, metric_affected, expected_impact_pct, confidence, description, source, source_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'change_log', ?)""",
            [rid, market, dt, change_type, metric, impact, confidence, description[:200], cl_id])
        inserted += 1
        existing_keys.add(key)
        print(f"  NEW: {market} {dt} [{change_type}] {impact:+.0%} — {description[:80]}")
    
    if inserted == 0:
        print("  No new regime changes detected")
    else:
        print(f"\n  {inserted} new regime changes inserted")
    
    # Summary
    total = con.execute("SELECT COUNT(*) FROM ps.regime_changes WHERE active=TRUE").fetchone()[0]
    print(f"  Total active regime changes: {total}")
    
    con.close()


if __name__ == '__main__':
    print("=== Regime Change Detection ===")
    run()
