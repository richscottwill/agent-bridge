"""Shared test fixtures for prediction engine tests."""

import sys
import os
import tempfile
import pytest

# Ensure imports work
sys.path.insert(0, os.path.expanduser('~/shared/tools'))
sys.path.insert(0, os.path.expanduser('~/shared/tools/data'))

import duckdb
from init_db import init_db


def _patch_db(db_path):
    """Patch query.db to use read-write for nextval calls, and add unique index."""
    con = duckdb.connect(db_path)
    try:
        con.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_po_pred_id ON prediction_outcomes(prediction_id)")
    except Exception:
        pass
    con.close()

    # Monkey-patch query.db so nextval works (db opens read_only=True which blocks nextval)
    import query as q
    _original_db = q.db

    def _patched_db(sql, db_path=None):
        path = db_path or q.DB_PATH
        if 'nextval' in sql.lower():
            # nextval is a write op — use read-write connection
            con = duckdb.connect(path)
            try:
                result = con.execute(sql)
                columns = [desc[0] for desc in result.description]
                rows = result.fetchall()
                return [dict(zip(columns, row)) for row in rows]
            finally:
                con.close()
        return _original_db(sql, db_path=db_path)

    q.db = _patched_db

    # Also reset module-level caches in prediction modules so they pick up patched version
    import prediction.autonomy as auto_mod
    import prediction.calibrator as cal_mod
    import prediction.engine as eng_mod
    auto_mod._db = None
    auto_mod._db_write = None
    auto_mod._db_upsert = None
    cal_mod._db = None
    cal_mod._db_write = None
    cal_mod._db_upsert = None
    eng_mod._db = None
    eng_mod._db_write = None
    eng_mod._market_week = None


@pytest.fixture
def test_db():
    """Create a temporary DuckDB database with full schema, yield path, clean up."""
    fd, path = tempfile.mkstemp(suffix='.duckdb')
    os.close(fd)
    os.unlink(path)  # init_db creates the file
    init_db(db_path=path)
    _patch_db(path)
    yield path
    # Cleanup
    for f in [path, path + '.wal']:
        if os.path.exists(f):
            try:
                os.unlink(f)
            except OSError:
                pass


@pytest.fixture
def test_db_with_data(test_db):
    """Test DB pre-loaded with synthetic weekly_metrics for 10 markets × 20 weeks."""
    con = duckdb.connect(test_db)
    markets = ['US', 'CA', 'UK', 'DE', 'FR', 'IT', 'ES', 'JP', 'AU', 'MX']
    base_regs = {'US': 500, 'CA': 300, 'UK': 400, 'DE': 350, 'FR': 250,
                 'IT': 200, 'ES': 180, 'JP': 450, 'AU': 240, 'MX': 160}
    for m in markets:
        base = base_regs[m]
        for w in range(1, 21):
            week_str = f"2026 W{w:02d}"
            regs = base + w * 2.5 + (w % 3) * 5
            cost = regs * 55
            cpa = cost / regs if regs > 0 else 0
            clicks = int(regs * 12)
            cvr = regs / clicks if clicks > 0 else 0
            cpc = cost / clicks if clicks > 0 else 0
            con.execute(
                "INSERT INTO weekly_metrics (market, week, regs, cost, cpa, clicks, cvr, cpc) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                [m, week_str, regs, cost, cpa, clicks, cvr, cpc]
            )
    con.close()
    return test_db
