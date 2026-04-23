# tools/excel_ingest.py - Updated April 2026
import pandas as pd
import duckdb
import os
from datetime import datetime
import glob

DB_PATH = "~/shared/data/duckdb/ps-analytics.duckdb"
UPLOADS_DIR = "~/shared/uploads/"
ARCHIVE_DIR = "~/shared/uploads/archive/"


def ingest_and_summarize():
    files = glob.glob(f"{UPLOADS_DIR}*.xlsx") + glob.glob(f"{UPLOADS_DIR}*.csv")
    if not files:
        return "No new files found."

    conn = duckdb.connect(DB_PATH)
    summaries = []

    for file in files:
        try:
            df = pd.read_excel(file) if file.endswith('.xlsx') else pd.read_csv(file)
            df.columns = [c.strip().lower().replace(' ', '_') for c in df.columns]
            df['ingested_at'] = datetime.now()
            df['source_file'] = os.path.basename(file)

            table = "tests" if 'test_id' in df.columns or 'lift' in df.columns else "ps"
            conn.execute(f"INSERT INTO {table} SELECT * FROM df")

            summary = f"**Data Snapshot**: Ingested {len(df)} rows from {os.path.basename(file)} into {table} table."
            summaries.append(summary)

            os.makedirs(ARCHIVE_DIR, exist_ok=True)
            os.rename(file, f"{ARCHIVE_DIR}{os.path.basename(file)}")

        except Exception as e:
            summaries.append(f"Error with {os.path.basename(file)}: {e}")

    conn.close()
    return "\n".join(summaries)


if __name__ == "__main__":
    print(ingest_and_summarize())
