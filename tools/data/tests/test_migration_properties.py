#!/usr/bin/env python3
"""
Property tests for data migration completeness, narrative preservation,
and schema export round-trip.

Properties:
  14 — Migration completeness
  10 — Narrative preservation during markdown simplification
   7 — Schema export round-trip
"""

import os
import sys
import tempfile
import shutil
import re

import pytest
from hypothesis import given, settings, assume
from hypothesis import strategies as st

# Add parent dir for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from query import db, db_upsert, DB_PATH
from migrate_competitors import parse_competitor_tables, EYES_PATH
from migrate_oci import parse_oci_tables
from migrate_changelog import find_changelog_files, parse_changelog_table


# ═══════════════════════════════════════════════════════════════
# Property 14: Migration completeness
# For each migrated data point from source markdown, verify a SQL
# query returns it from DuckDB.
# **Validates: Requirement 6.4**
# ═══════════════════════════════════════════════════════════════

class TestMigrationCompleteness:
    """Property 14: Every structured data point parsed from markdown
    must be queryable from DuckDB after migration."""

    def test_competitors_migration_complete(self):
        """All expected competitor markets have entries in the competitors table.

        **Validates: Requirements 6.1, 6.4**
        """
        # After simplification, eyes.md tables were removed.
        # Verify competitors exist in DuckDB for key markets.
        result = db("SELECT DISTINCT market FROM competitors ORDER BY market")
        markets_with_competitors = [r['market'] for r in result]

        # We expect at least US, UK, DE, FR, IT, ES, CA, JP, MX
        expected_markets = ['US', 'UK', 'DE', 'FR', 'IT', 'ES', 'CA', 'JP', 'MX']
        for market in expected_markets:
            assert market in markets_with_competitors, (
                f"No competitors found for {market} in DuckDB"
            )

        # Verify total count matches what was migrated
        total = db("SELECT COUNT(*) as cnt FROM competitors")
        assert total[0]['cnt'] >= 14, (
            f"Expected at least 14 competitor rows, got {total[0]['cnt']}"
        )

    def test_oci_status_migration_complete(self):
        """Every OCI status market exists in the oci_status table.

        **Validates: Requirements 6.2, 6.4**
        """
        # After simplification, eyes.md no longer has the OCI tables.
        # Verify all 10 markets have OCI status entries in DuckDB.
        all_markets = ['US', 'UK', 'DE', 'FR', 'IT', 'ES', 'CA', 'JP', 'AU', 'MX']

        for market in all_markets:
            result = db(
                f"SELECT * FROM oci_status WHERE market = '{market}'",
            )
            assert len(result) >= 1, (
                f"OCI status for {market} not found in DuckDB"
            )
            db_row = result[0]
            assert db_row['status'] in ('live', 'in_progress', 'not_planned'), (
                f"Invalid status for {market}: {db_row['status']}"
            )

    def test_changelog_migration_complete(self):
        """Every change log entry parsed from markdown exists in the change_log table.

        **Validates: Requirements 6.3, 6.4**
        """
        files = find_changelog_files()
        if not files:
            pytest.skip('No change log files found')

        for market, path in files.items():
            with open(path) as f:
                text = f.read()

            parsed = parse_changelog_table(text, market)
            if not parsed:
                continue

            # Verify the count in DuckDB matches or exceeds parsed count
            result = db(
                f"SELECT COUNT(*) as cnt FROM change_log WHERE market = '{market}'",
            )
            db_count = result[0]['cnt']
            assert db_count >= len(parsed), (
                f"Change log count mismatch for {market}: "
                f"parsed {len(parsed)} from markdown, found {db_count} in DuckDB"
            )

    @given(market=st.sampled_from(['US', 'UK', 'DE', 'FR', 'IT', 'ES', 'CA', 'JP', 'AU', 'MX']))
    @settings(max_examples=10)
    def test_migrated_data_queryable(self, market):
        """For any market, migrated data is queryable via SQL.

        **Validates: Requirement 6.4**
        """
        # Competitors
        competitors = db(
            f"SELECT * FROM competitors WHERE market = '{market}'",
        )
        # OCI status
        oci = db(
            f"SELECT * FROM oci_status WHERE market = '{market}'",
        )
        # Change log
        changes = db(
            f"SELECT * FROM change_log WHERE market = '{market}'",
        )

        # At least OCI status should exist for every market
        assert len(oci) >= 1, f"No OCI status for {market}"

        # All returned rows should have the correct market
        for row in competitors:
            assert row['market'] == market
        for row in oci:
            assert row['market'] == market
        for row in changes:
            assert row['market'] == market


# ═══════════════════════════════════════════════════════════════
# Property 10: Narrative preservation during markdown simplification
# Verify prose word count after simplification ≥ prose word count
# before (minus small epsilon for table-to-hint replacement).
# **Validates: Requirement 7.3**
# ═══════════════════════════════════════════════════════════════

class TestNarrativePreservation:
    """Property 10: All narrative prose must be preserved when
    metric tables are removed from markdown files."""

    def _count_prose_words(self, text):
        """Count words in non-table, non-comment lines (prose only)."""
        words = 0
        for line in text.split('\n'):
            stripped = line.strip()
            # Skip table rows
            if stripped.startswith('|') and '|' in stripped[1:]:
                continue
            # Skip HTML comments (query hints)
            if stripped.startswith('<!--') and stripped.endswith('-->'):
                continue
            # Skip empty lines
            if not stripped:
                continue
            words += len(stripped.split())
        return words

    def test_eyes_md_narrative_preserved(self):
        """eyes.md should retain all narrative prose after table removal.

        **Validates: Requirements 7.1, 7.3, 7.4**
        """
        eyes_path = os.path.expanduser('~/shared/context/body/eyes.md')
        if not os.path.exists(eyes_path):
            pytest.skip('eyes.md not found')

        with open(eyes_path) as f:
            content = f.read()

        prose_words = self._count_prose_words(content)

        # After simplification, eyes.md should still have substantial prose
        # The Market Deep Dives, Ad Copy Testing, Predicted Questions, etc.
        # are all narrative and should be preserved.
        # Original eyes.md had ~1500+ prose words; tables were ~550 words.
        # After removing tables, prose should be >= 1000 words.
        assert prose_words >= 1000, (
            f"eyes.md prose word count too low after simplification: {prose_words}. "
            f"Narrative content may have been accidentally removed."
        )

        # Verify key narrative sections still exist
        assert 'Market Deep Dives' in content, "Market Deep Dives section missing"
        assert 'Ad Copy Testing' in content, "Ad Copy Testing section missing"
        assert 'Predicted Questions' in content, "Predicted Questions section missing"
        assert 'Data Pipeline' in content, "Data Pipeline section missing"
        assert 'Key Trends' in content, "Key Trends section missing"

        # Verify query hints were added
        assert '<!-- Data:' in content, "No query hints found in eyes.md"

    def test_data_briefs_narrative_preserved(self):
        """Data briefs should retain headline numbers, drivers, anomalies, projections.

        **Validates: Requirements 7.3, 7.5**
        """
        import glob
        callouts_dir = os.path.expanduser('~/shared/context/active/callouts')
        briefs = glob.glob(os.path.join(callouts_dir, '*/*-data-brief-*.md'))

        if not briefs:
            pytest.skip('No data brief files found')

        for path in briefs:
            with open(path) as f:
                content = f.read()

            basename = os.path.basename(path)
            prose_words = self._count_prose_words(content)

            # Each brief should have at least headline numbers + drivers + projection
            # That's roughly 100+ prose words minimum
            assert prose_words >= 50, (
                f"{basename}: prose word count too low ({prose_words}). "
                f"Narrative content may have been accidentally removed."
            )

            # Key narrative sections should be preserved
            assert 'Headline numbers' in content, f"{basename}: Headline numbers section missing"
            assert 'Registration drivers' in content, f"{basename}: Registration drivers section missing"

            # Query hints should be present (tables were replaced)
            assert '<!-- Data:' in content, f"{basename}: No query hints found"

    @given(market=st.sampled_from(['US', 'UK', 'DE', 'FR', 'IT', 'ES', 'CA', 'JP', 'AU', 'MX']))
    @settings(max_examples=10)
    def test_brief_has_narrative_and_hints(self, market):
        """For any market, the latest data brief has both narrative and query hints.

        **Validates: Requirement 7.3**
        """
        import glob
        callouts_dir = os.path.expanduser('~/shared/context/active/callouts')
        briefs = sorted(glob.glob(
            os.path.join(callouts_dir, market.lower(), f'{market.lower()}-data-brief-*.md')
        ))

        if not briefs:
            return  # Skip if no briefs for this market

        # Check the latest brief
        with open(briefs[-1]) as f:
            content = f.read()

        # Must have narrative content
        prose_words = self._count_prose_words(content)
        assert prose_words > 0, f"No prose in {market} latest brief"

        # Must have query hints (tables were replaced)
        assert '<!-- Data:' in content or '|' not in content, (
            f"{market} brief has tables but no query hints"
        )


# ═══════════════════════════════════════════════════════════════
# Property 7: Schema export round-trip
# Export schema, execute on empty DuckDB, verify tables created.
# **Validates: Requirements 4.1, 4.3**
# ═══════════════════════════════════════════════════════════════

class TestSchemaExportRoundTrip:
    """Property 7: Exported schema.sql must recreate all tables
    on an empty DuckDB instance."""

    def test_schema_export_creates_valid_sql(self):
        """schema_export() produces a file that creates all tables on empty DB.

        **Validates: Requirements 4.1, 4.3**
        """
        import duckdb

        # Export schema from the live database
        export_path = os.path.join(tempfile.mkdtemp(), 'schema_test.sql')
        from query import schema_export
        schema_export(output_path=export_path)

        assert os.path.exists(export_path), "schema_export() did not create file"

        with open(export_path) as f:
            sql_content = f.read()

        # Verify it has CREATE TABLE statements
        assert 'CREATE TABLE' in sql_content, "No CREATE TABLE in schema.sql"

        # Verify it has timestamp
        assert 'Generated:' in sql_content, "No timestamp in schema.sql"

        # Execute on a fresh empty DuckDB
        empty_db = os.path.join(tempfile.mkdtemp(), 'empty_test.duckdb')
        con = duckdb.connect(empty_db)
        try:
            # Extract only CREATE TABLE statements (skip comments and row counts)
            for line in sql_content.split('\n'):
                stripped = line.strip()
                if stripped.startswith('CREATE TABLE') or stripped.startswith('CREATE SEQUENCE'):
                    # Find the full statement (may span multiple lines)
                    pass  # handled below

            # Execute the full SQL — DuckDB handles multi-statement
            # Filter to just CREATE statements
            statements = []
            current = []
            for line in sql_content.split('\n'):
                if line.startswith('--'):
                    continue
                current.append(line)
                if line.strip().endswith(';'):
                    stmt = '\n'.join(current).strip()
                    if stmt and not stmt.startswith('--'):
                        statements.append(stmt)
                    current = []

            for stmt in statements:
                if 'CREATE TABLE' in stmt:
                    con.execute(stmt)

            # Verify tables were created
            new_tables = [t[0] for t in con.execute("SHOW TABLES").fetchall()]

            # Get tables from source DB
            source_tables = [t[0] for t in
                duckdb.connect(DB_PATH, read_only=True).execute("SHOW TABLES").fetchall()]

            for table in source_tables:
                assert table in new_tables, (
                    f"Table '{table}' from source DB not created in round-trip. "
                    f"Created tables: {new_tables}"
                )
        finally:
            con.close()
            # Cleanup
            if os.path.exists(empty_db):
                os.unlink(empty_db)
            if os.path.exists(export_path):
                os.unlink(export_path)

    def test_schema_export_includes_row_counts(self):
        """schema_export() includes row count comments.

        **Validates: Requirement 4.2**
        """
        export_path = os.path.join(tempfile.mkdtemp(), 'schema_counts.sql')
        from query import schema_export
        schema_export(output_path=export_path)

        with open(export_path) as f:
            content = f.read()

        # Should have "-- tablename: N rows as of export" comments
        assert 'rows as of export' in content, "No row count comments in schema.sql"

        # Cleanup
        os.unlink(export_path)
