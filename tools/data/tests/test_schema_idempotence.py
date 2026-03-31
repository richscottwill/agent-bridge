"""
Property 5: Schema migration idempotence.

Run init_db() on a populated DB, verify existing row counts unchanged and new tables added.

Validates: Requirements 3.5, 13.3
"""

import os
import sys
import tempfile

import duckdb
import pytest
from hypothesis import given, settings, HealthCheck
from hypothesis import strategies as st

# Add parent dir so we can import init_db
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from init_db import init_db

# All tables created by init_db()
ALL_TABLES = [
    "daily_metrics",
    "weekly_metrics",
    "monthly_metrics",
    "ieccp",
    "projections",
    "callout_scores",
    "experiments",
    "ingest_log",
    "change_log",
    "anomalies",
    "competitors",
    "oci_status",
    "agent_actions",
    "agent_observations",
    "decisions",
    "task_queue",
]

# Tables we can easily insert sample rows into (no CHECK constraints that complicate generation)
INSERTABLE_TABLES = {
    "daily_metrics": {
        "cols": "(market, date, week, regs)",
        "vals": "('AU', '2026-03-01', '2026 W09', {regs})",
    },
    "weekly_metrics": {
        "cols": "(market, week, regs)",
        "vals": "('AU', '2026 W{week_num:02d}', {regs})",
    },
    "monthly_metrics": {
        "cols": "(market, month, regs)",
        "vals": "('AU', '2026 Mar', {regs})",
    },
    "projections": {
        "cols": "(market, week, projected_regs)",
        "vals": "('AU', '2026 W{week_num:02d}', {regs})",
    },
    "experiments": {
        "cols": "(experiment_id, name, status)",
        "vals": "('EXP-{idx}', 'Test {idx}', 'active')",
    },
    "change_log": {
        "cols": "(id, market, date, category, description)",
        "vals": "({idx}, 'AU', '2026-03-01', 'bid_strategy', 'Change {idx}')",
    },
    "anomalies": {
        "cols": "(id, market, week, metric, value, baseline, deviation_pct, direction)",
        "vals": "({idx}, 'AU', '2026 W09', 'regs', 300, 200, 50.0, 'above')",
    },
    "competitors": {
        "cols": "(market, competitor, week, impression_share)",
        "vals": "('AU', 'Competitor-{idx}', '2026 W09', 25.0)",
    },
    "oci_status": {
        "cols": "(market, status)",
        "vals": "('M{idx}', 'live')",
    },
}


def _insert_sample_rows(con, table, n_rows):
    """Insert n_rows sample rows into a table."""
    spec = INSERTABLE_TABLES.get(table)
    if spec is None:
        return 0
    inserted = 0
    for i in range(1, n_rows + 1):
        vals = spec["vals"].format(regs=i * 10 + 1, week_num=i, idx=i)
        sql = f"INSERT INTO {table} {spec['cols']} VALUES {vals}"
        try:
            con.execute(sql)
            inserted += 1
        except Exception:
            pass  # skip duplicates or constraint violations
    return inserted


def _get_table_names(con):
    """Return sorted list of table names in the database."""
    return sorted(row[0] for row in con.execute("SHOW TABLES").fetchall())


def _get_row_counts(con):
    """Return dict of {table_name: row_count} for all tables."""
    tables = _get_table_names(con)
    return {t: con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0] for t in tables}


# ── Hypothesis strategy: how many rows to insert per table ──
row_counts_strategy = st.fixed_dictionaries(
    {table: st.integers(min_value=1, max_value=5) for table in INSERTABLE_TABLES}
)


class TestSchemaIdempotence:
    """Property 5: Schema migration idempotence.

    **Validates: Requirements 3.5, 13.3**
    """

    @given(row_counts=row_counts_strategy)
    @settings(
        max_examples=10,
        deadline=None,
        suppress_health_check=[HealthCheck.function_scoped_fixture],
    )
    def test_init_db_preserves_row_counts(self, row_counts):
        """Running init_db() on a populated DB must not change any row counts."""
        with tempfile.NamedTemporaryFile(suffix=".duckdb", delete=True) as tmp:
            db_path = tmp.name

        try:
            # Step 1: Create schema
            init_db(db_path)

            # Step 2: Populate tables with sample data
            con = duckdb.connect(db_path)
            for table, n in row_counts.items():
                _insert_sample_rows(con, table, n)
            con.close()

            # Step 3: Record row counts before second init
            con = duckdb.connect(db_path, read_only=True)
            counts_before = _get_row_counts(con)
            tables_before = _get_table_names(con)
            con.close()

            # Step 4: Run init_db() again on the populated DB
            init_db(db_path)

            # Step 5: Verify row counts unchanged
            con = duckdb.connect(db_path, read_only=True)
            counts_after = _get_row_counts(con)
            tables_after = _get_table_names(con)
            con.close()

            for table in tables_before:
                assert counts_after[table] == counts_before[table], (
                    f"Table '{table}' row count changed: "
                    f"{counts_before[table]} -> {counts_after[table]}"
                )

            # Step 6: All tables still exist (including Phase A and Phase B)
            for table in ALL_TABLES:
                assert table in tables_after, (
                    f"Table '{table}' missing after second init_db()"
                )
        finally:
            # Cleanup
            for ext in ["", ".wal"]:
                path = db_path + ext
                if os.path.exists(path):
                    os.remove(path)

    def test_init_db_adds_new_tables_without_affecting_existing(self):
        """Concrete example: init_db on a DB with data preserves everything."""
        with tempfile.NamedTemporaryFile(suffix=".duckdb", delete=True) as tmp:
            db_path = tmp.name

        try:
            init_db(db_path)

            # Insert known data
            con = duckdb.connect(db_path)
            con.execute(
                "INSERT INTO daily_metrics (market, date, week, regs) "
                "VALUES ('US', '2026-03-15', '2026 W11', 500)"
            )
            con.execute(
                "INSERT INTO weekly_metrics (market, week, regs) "
                "VALUES ('US', '2026 W11', 3500)"
            )
            con.execute(
                "INSERT INTO projections (market, week, projected_regs) "
                "VALUES ('US', '2026 W11', 1200)"
            )
            con.close()

            # Record state
            con = duckdb.connect(db_path, read_only=True)
            counts_before = _get_row_counts(con)
            con.close()

            # Re-run init_db
            init_db(db_path)

            # Verify
            con = duckdb.connect(db_path, read_only=True)
            counts_after = _get_row_counts(con)

            assert counts_after["daily_metrics"] == counts_before["daily_metrics"]
            assert counts_after["weekly_metrics"] == counts_before["weekly_metrics"]
            assert counts_after["projections"] == counts_before["projections"]

            # Verify actual data is intact
            row = con.execute(
                "SELECT regs FROM daily_metrics WHERE market='US' AND date='2026-03-15'"
            ).fetchone()
            assert row is not None and row[0] == 500

            row = con.execute(
                "SELECT regs FROM weekly_metrics WHERE market='US' AND week='2026 W11'"
            ).fetchone()
            assert row is not None and row[0] == 3500

            # All 16 tables present
            tables = _get_table_names(con)
            for t in ALL_TABLES:
                assert t in tables, f"Table '{t}' missing after re-init"

            con.close()
        finally:
            for ext in ["", ".wal"]:
                path = db_path + ext
                if os.path.exists(path):
                    os.remove(path)
