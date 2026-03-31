# Data Directory

All data files for DuckDB ingestion and querying.

## Ingestion Flow

1. Richard drops files in uploads/sheets/ or uploads/changelogs/
2. Ingestion script copies to data/raw/
3. DuckDB loads from data/raw/
4. Source file moves to data/processed/ with date prefix (2026-03-31_filename.csv)
5. Agent exports go to data/exports/

## Subdirectories

- duckdb/ — .duckdb and .wal database files
- raw/ — unprocessed files awaiting ingestion
- processed/ — ingested files (timestamped)
- exports/ — query results and agent-generated data
- markets/{code}/ — per-market data (au, mx, us, ca, jp, uk, de, fr, it, es)
- testing/ — test-specific data files

## Naming Conventions

- Raw: original filename as uploaded
- Processed: YYYY-MM-DD_original-filename.csv
- Exports: {agent}-{description}-YYYY-MM-DD.csv
