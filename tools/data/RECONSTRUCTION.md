# RECONSTRUCTION.md — PS Analytics Database Portability Guide

*How to rebuild the DuckDB database from scratch on any platform with nothing but text files and Python.*

Last updated: 2026-03-30

---

## Overview

The PS Analytics database (`ps-analytics.duckdb`) is the canonical source of truth for all structured paid search data. It can be fully reconstructed from source files if the .duckdb file is lost or you're setting up on a new platform.

DuckDB is a single portable file — no server, no daemon. Just copy it. But if you need to rebuild:

---

## Rebuild Procedure

```bash
# Step 1: Create empty schema (all tables, sequences, constraints)
python3 ~/shared/tools/data/init_db.py

# Step 2: Ingest dashboard data (populates daily, weekly, monthly metrics + ieccp + projections)
python3 ~/shared/tools/dashboard-ingester/ingest.py <path-to-latest-xlsx>

# Step 3: Backfill competitors from eyes.md
python3 ~/shared/tools/data/migrate_competitors.py

# Step 4: Backfill OCI status from eyes.md
python3 ~/shared/tools/data/migrate_oci.py

# Step 5: Backfill change log from per-market markdown files
python3 ~/shared/tools/data/migrate_changelog.py

# Step 6: Export schema for portability
python3 ~/shared/tools/data/query.py --schema-export
```

All scripts are idempotent — safe to re-run.

---

## Markdown → DuckDB Table Mapping

| Markdown Source | DuckDB Table | Primary Key | Migration Script |
|----------------|-------------|-------------|-----------------|
| WW Dashboard XLSX (daily tabs) | `daily_metrics` | (market, date) | `ingest.py` |
| WW Dashboard XLSX (weekly tabs) | `weekly_metrics` | (market, week) | `ingest.py` |
| WW Dashboard XLSX (monthly tab) | `monthly_metrics` | (market, month) | `ingest.py` |
| WW Dashboard XLSX (IECCP) | `ieccp` | (market, week) | `ingest.py` |
| Analyst agent output | `projections` | (market, week) | Analyst agents via `db_upsert()` |
| Callout reviewer output | `callout_scores` | (market, week) | Reviewer agent via `db_upsert()` |
| `eyes.md` Competitive Landscape | `competitors` | (market, competitor, week) | `migrate_competitors.py` |
| `eyes.md` OCI Performance | `oci_status` | (market) | `migrate_oci.py` |
| Per-market `{mkt}-change-log.md` | `change_log` | (id) | `migrate_changelog.py` |
| Ingester anomaly detection | `anomalies` | (id) | `ingest.py` (auto-detected) |
| Manual / agent entries | `experiments` | (experiment_id) | Manual |
| Ingester metadata | `ingest_log` | (id) | `ingest.py` (auto) |

### Phase B Tables (schema only, no consumers yet)

| Table | Purpose | Populated By |
|-------|---------|-------------|
| `agent_actions` | Audit trail for agent actions | Future: all agents |
| `agent_observations` | What agents notice during analysis | Future: analyst agents |
| `decisions` | Decisions requiring approval/review | Future: approval gradient |
| `task_queue` | Agent work items with priority | Future: orchestrator |

---

## Query Patterns for Common Agent Tasks

### Market trend (last 8 weeks)
```python
from query import market_trend
trend = market_trend('AU', weeks=8)
# Returns: [{'market': 'AU', 'week': '2026 W13', 'regs': 207, ...}, ...]
```

### Current week snapshot
```python
from query import market_week
this_week = market_week('AU', '2026 W13')
# Returns: {'market': 'AU', 'week': '2026 W13', 'regs': 207, 'cpa': 118, ...}
```

### Monthly projection
```python
from query import projection
proj = projection('AU', '2026 W13')
```

### Callout quality scores
```python
from query import callout_scores
scores = callout_scores('AU', weeks=8)
```

### Competitor intel
```sql
SELECT market, competitor, impression_share, segment
FROM competitors WHERE market = 'US' ORDER BY impression_share DESC
```

### OCI rollout status
```sql
SELECT market, status, launch_date, reg_lift_pct FROM oci_status ORDER BY market
```

### Change log for a market
```sql
SELECT date, category, description FROM change_log
WHERE market = 'AU' ORDER BY date DESC LIMIT 20
```

### Anomalies (unresolved)
```sql
SELECT market, week, metric, deviation_pct, direction
FROM anomalies WHERE resolved = false ORDER BY flagged_at DESC
```

### Write operations
```python
from query import db_upsert, db_write

# Upsert a projection
db_upsert('projections', {
    'market': 'AU', 'week': '2026 W13',
    'projected_regs': 1050, 'source': 'abix-analyst',
    ...
}, key_cols=['market', 'week'])

# Raw write
db_write("UPDATE anomalies SET resolved = true WHERE id = 42")
```

---

## Schema Export

After each ingestion run, `schema_export()` writes `~/shared/tools/data/schema.sql` containing:
- All CREATE TABLE statements
- Row count comments per table
- Generation timestamp

A new AI on a different platform can run this SQL on an empty DuckDB to recreate the schema:
```bash
python3 -c "import duckdb; con = duckdb.connect('ps-analytics.duckdb'); con.execute(open('schema.sql').read()); con.close()"
```

---

## Key Files

| File | Purpose |
|------|---------|
| `~/shared/tools/data/ps-analytics.duckdb` | The database file |
| `~/shared/tools/data/init_db.py` | Schema definition + migration |
| `~/shared/tools/data/query.py` | Query helper (read + write + convenience) |
| `~/shared/tools/data/schema.sql` | Auto-exported schema (portability) |
| `~/shared/tools/data/last_ingest.json` | Data freshness event |
| `~/shared/tools/data/migrate_competitors.py` | Competitor backfill from eyes.md |
| `~/shared/tools/data/migrate_oci.py` | OCI status backfill from eyes.md |
| `~/shared/tools/data/migrate_changelog.py` | Change log backfill from per-market .md |
| `~/shared/tools/dashboard-ingester/ingest.py` | Dashboard ingester (xlsx → DuckDB) |
| `~/shared/tools/data/RECONSTRUCTION.md` | This file |
