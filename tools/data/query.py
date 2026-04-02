#!/usr/bin/env python3
"""
Quick query helper for PS Analytics DuckDB.

Usage:
    python3 query.py "SELECT * FROM weekly_metrics WHERE market='AU' ORDER BY week DESC LIMIT 8"
    python3 query.py --table daily_metrics
    python3 query.py --tables
    python3 query.py --stats

Or import in Python:
    from query import db
    df = db("SELECT market, week, regs FROM weekly_metrics WHERE week='2026 W12'")
"""

import duckdb
import os
import sys
import argparse
from datetime import datetime

DB_PATH = os.path.expanduser('~/shared/tools/data/ps-analytics.duckdb')


def _check_db_exists(path):
    """Raise FileNotFoundError if the .duckdb file doesn't exist."""
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Database file not found: {path}\n"
            f"Run init_db.py to create it: python3 ~/shared/tools/data/init_db.py"
        )


def db(sql, db_path=None):
    """Run a SQL query and return results as a list of dicts."""
    path = db_path or DB_PATH
    _check_db_exists(path)
    con = duckdb.connect(path, read_only=True)
    try:
        result = con.execute(sql)
        columns = [desc[0] for desc in result.description]
        rows = result.fetchall()
        return [dict(zip(columns, row)) for row in rows]
    finally:
        con.close()


def db_df(sql, db_path=None):
    """Run a SQL query and return a pandas DataFrame (if pandas available)."""
    path = db_path or DB_PATH
    _check_db_exists(path)
    con = duckdb.connect(path, read_only=True)
    try:
        df = con.execute(sql).fetchdf()
        return df
    finally:
        con.close()


def db_write(sql, params=None, db_path=None):
    """Execute INSERT/UPDATE/DELETE. Returns rows affected.

    Opens a read-write connection, executes the statement, and closes
    the connection. Connection is always closed via try/finally.
    """
    path = db_path or DB_PATH
    _check_db_exists(path)
    con = duckdb.connect(path)
    try:
        if params is not None:
            result = con.execute(sql, params)
        else:
            result = con.execute(sql)
        rows_affected = result.fetchone()[0] if result.description else 0
    except duckdb.Error as e:
        raise duckdb.Error(f"db_write failed: {e}") from e
    finally:
        con.close()
    return rows_affected


def db_upsert(table, data, key_cols, db_path=None):
    """Insert or update a row. key_cols define the conflict target.

    Builds INSERT ... ON CONFLICT DO UPDATE SET for non-key columns.
    Opens a read-write connection, executes, and closes via try/finally.
    """
    path = db_path or DB_PATH
    _check_db_exists(path)

    cols = list(data.keys())
    vals = list(data.values())
    placeholders = ', '.join(['?'] * len(cols))
    col_list = ', '.join(cols)
    non_key_cols = [c for c in cols if c not in key_cols]
    conflict = ', '.join(key_cols)

    if non_key_cols:
        updates = ', '.join(f"{c} = EXCLUDED.{c}" for c in non_key_cols)
        sql = f"INSERT INTO {table} ({col_list}) VALUES ({placeholders}) ON CONFLICT ({conflict}) DO UPDATE SET {updates}"
    else:
        # All columns are key columns — just insert, ignore conflict
        sql = f"INSERT INTO {table} ({col_list}) VALUES ({placeholders}) ON CONFLICT ({conflict}) DO NOTHING"

    con = duckdb.connect(path)
    try:
        con.execute(sql, vals)
    except duckdb.Error as e:
        raise duckdb.Error(f"db_upsert failed on table '{table}': {e}") from e
    finally:
        con.close()


def market_week(market, week, db_path=None):
    """Get weekly metrics for a single market+week. Returns dict or None."""
    rows = db(
        f"SELECT * FROM weekly_metrics WHERE market = '{market}' AND week = '{week}'",
        db_path=db_path,
    )
    return rows[0] if rows else None


def market_trend(market, weeks=8, db_path=None):
    """Get last N weeks of weekly metrics for a market, most recent first."""
    return db(
        f"SELECT * FROM weekly_metrics WHERE market = '{market}' "
        f"ORDER BY week DESC LIMIT {int(weeks)}",
        db_path=db_path,
    )


def market_month(market, month, db_path=None):
    """Get monthly metrics + OP2 targets for a market+month. Returns dict or None."""
    rows = db(
        f"SELECT * FROM monthly_metrics WHERE market = '{market}' AND month = '{month}'",
        db_path=db_path,
    )
    return rows[0] if rows else None


def projection(market, week, db_path=None):
    """Get projection for a market+week. Returns dict or None."""
    rows = db(
        f"SELECT * FROM projections WHERE market = '{market}' AND week = '{week}'",
        db_path=db_path,
    )
    return rows[0] if rows else None


def callout_scores(market, weeks=8, db_path=None):
    """Get last N weeks of callout quality scores, most recent first."""
    return db(
        f"SELECT * FROM callout_scores WHERE market = '{market}' "
        f"ORDER BY week DESC LIMIT {int(weeks)}",
        db_path=db_path,
    )


def db_validate(sql, db_path=None):
    """Validate SQL without executing it. Returns True if valid, raises on error.

    Uses EXPLAIN to check syntax and schema references without running the query.
    Agents should call this before db_write() to catch typos in column/table names.
    """
    path = db_path or DB_PATH
    _check_db_exists(path)
    con = duckdb.connect(path, read_only=True)
    try:
        con.execute(f"EXPLAIN {sql}")
        return True
    except duckdb.Error as e:
        raise duckdb.Error(f"SQL validation failed: {e}") from e
    finally:
        con.close()


def schema(db_path=None):
    """Return schema as {table_name: [{name, type, nullable}, ...], ...}.

    Agents use this to introspect column names at runtime instead of
    reading init_db.py or guessing. Fast — single DESCRIBE per table.
    """
    path = db_path or DB_PATH
    _check_db_exists(path)
    con = duckdb.connect(path, read_only=True)
    try:
        tables = [t[0] for t in con.execute("SHOW TABLES").fetchall()]
        result = {}
        for table in tables:
            cols = con.execute(f"DESCRIBE {table}").fetchall()
            result[table] = [
                {'name': c[0], 'type': c[1], 'nullable': c[2] == 'YES'}
                for c in cols
            ]
        return result
    finally:
        con.close()


def export_parquet(tables=None, output_dir=None, db_path=None):
    """Export DuckDB tables as Parquet files for cross-environment agent access.

    Args:
        tables: List of table names to export. None = key agent tables.
        output_dir: Directory for .parquet files. Default: ~/shared/tools/data/exports/
        db_path: Database path override.

    Returns:
        dict: {table_name: file_path} for each exported table.

    Swarm agents on other platforms can read these directly without DuckDB.
    The bridge can upload them to Google Drive for cross-environment access.
    """
    path = db_path or DB_PATH
    _check_db_exists(path)

    if tables is None:
        tables = ['weekly_metrics', 'monthly_metrics', 'projections',
                  'callout_scores', 'anomalies', 'experiments']

    if output_dir is None:
        output_dir = os.path.expanduser('~/shared/tools/data/exports')
    os.makedirs(output_dir, exist_ok=True)

    con = duckdb.connect(path, read_only=True)
    exported = {}
    try:
        existing_tables = [t[0] for t in con.execute("SHOW TABLES").fetchall()]
        for table in tables:
            if table not in existing_tables:
                continue
            count = con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            if count == 0:
                continue
            out_path = os.path.join(output_dir, f"{table}.parquet")
            con.execute(f"COPY {table} TO '{out_path}' (FORMAT PARQUET)")
            exported[table] = out_path
    finally:
        con.close()

    return exported


def schema_export(output_path=None, db_path=None):
    """Export full schema as CREATE TABLE statements (portability).

    Writes all CREATE TABLE statements, row count comments, and a generation
    timestamp to a .sql file. A new AI on a different platform can run this
    SQL to recreate the schema.

    Args:
        output_path: Where to write the .sql file. Default: ~/shared/tools/data/schema.sql
        db_path: Database path override.

    Returns:
        str: Path to the written schema.sql file.
    """
    path = db_path or DB_PATH
    _check_db_exists(path)
    out = output_path or os.path.expanduser('~/shared/tools/data/schema.sql')
    con = duckdb.connect(path, read_only=True)
    try:
        tables = [t[0] for t in con.execute("SHOW TABLES").fetchall()]
        statements = []
        for table in tables:
            create_stmt = con.execute(
                f"SELECT sql FROM duckdb_tables() WHERE table_name = '{table}'"
            ).fetchone()
            if create_stmt:
                statements.append(create_stmt[0] + ';')
            count = con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            statements.append(f"-- {table}: {count} rows as of export")
    finally:
        con.close()
    output = '\n\n'.join(statements)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, 'w') as f:
        f.write(f"-- PS Analytics Schema Export\n")
        f.write(f"-- Generated: {datetime.now().isoformat()}\n")
        f.write(f"-- Source: {path}\n\n")
        f.write(output)
    return out


def check_freshness(since=None, db_path=None):
    """Check if new data exists since a given timestamp.

    Args:
        since: ISO timestamp string (e.g., '2026-03-30T10:00:00+00:00').
               If None, always returns True (treat as "never checked").

    Returns:
        (is_fresh, event_dict) — is_fresh is True if last_ingest.json is
        newer than `since`. event_dict is the parsed JSON (or None if no file).

    Usage by agents:
        fresh, event = check_freshness('2026-03-30T10:00:00+00:00')
        if fresh:
            trend = market_trend('AU')  # new data available
    """
    import json
    from datetime import datetime, timezone

    event_path = os.path.expanduser('~/shared/tools/data/last_ingest.json')
    if not os.path.exists(event_path):
        return False, None

    with open(event_path) as f:
        event = json.load(f)

    if since is None:
        return True, event

    event_ts = datetime.fromisoformat(event['timestamp'])
    since_ts = datetime.fromisoformat(since)
    # Ensure both are timezone-aware for comparison
    if event_ts.tzinfo is None:
        event_ts = event_ts.replace(tzinfo=timezone.utc)
    if since_ts.tzinfo is None:
        since_ts = since_ts.replace(tzinfo=timezone.utc)

    return event_ts > since_ts, event


def data_summary(db_path=None):
    """Return a quick orientation dict for every market's data coverage.

    Returns:
        {market: {latest_week, weeks_available, latest_daily_date,
                  has_projections, has_scores}}

    Agents call this at session start to understand what data exists
    without running 5-6 separate queries.
    """
    path = db_path or DB_PATH
    _check_db_exists(path)
    con = duckdb.connect(path, read_only=True)
    try:
        # Weekly coverage per market
        weekly = con.execute("""
            SELECT market,
                   MAX(week) AS latest_week,
                   COUNT(DISTINCT week) AS weeks_available
            FROM weekly_metrics
            GROUP BY market
        """).fetchall()

        # Latest daily date per market
        daily = con.execute("""
            SELECT market, MAX(date) AS latest_date
            FROM daily_metrics
            GROUP BY market
        """).fetchall()

        # Markets with projections
        proj = con.execute("""
            SELECT DISTINCT market FROM projections
        """).fetchall()
        proj_markets = {r[0] for r in proj}

        # Markets with callout scores
        scores = con.execute("""
            SELECT DISTINCT market FROM callout_scores
        """).fetchall()
        score_markets = {r[0] for r in scores}

        daily_map = {r[0]: str(r[1]) for r in daily}

        result = {}
        for row in weekly:
            market = row[0]
            result[market] = {
                'latest_week': row[1],
                'weeks_available': row[2],
                'latest_daily_date': daily_map.get(market),
                'has_projections': market in proj_markets,
                'has_scores': market in score_markets,
            }
        return result
    finally:
        con.close()


def write_data_event(target_week, markets_processed, row_counts=None, db_path=None):
    """Write a data event notification after ingestion.

    Creates/updates ~/shared/tools/data/last_ingest.json so agents can check
    whether new data exists since their last read. This is the cue in the
    habit loop — data arrival triggers analysis.

    Args:
        target_week: The week that was ingested (e.g., '2026 W13')
        markets_processed: List of market codes processed
        row_counts: Optional dict with counts (daily, weekly, monthly)
        db_path: Database path override
    """
    import json
    from datetime import datetime, timezone

    event_path = os.path.expanduser('~/shared/tools/data/last_ingest.json')
    event = {
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'target_week': target_week,
        'markets': markets_processed,
        'row_counts': row_counts or {},
        'db_path': db_path or DB_PATH,
    }

    with open(event_path, 'w') as f:
        json.dump(event, f, indent=2)

    return event_path


# ══════════════════════════════════════════════════════════════
# Agent state functions — write actions/observations, query memory
# ══════════════════════════════════════════════════════════════

def log_agent_action(agent, action_type, market, week, description,
                     output_summary=None, confidence=None, db_path=None):
    """Write an agent action to the agent_actions table. Returns the action ID.

    One row per agent invocation per market. Provides an auditable record
    of what each agent did and when.

    Args:
        agent: Agent name (e.g., 'market-analyst', 'callout-writer')
        action_type: What the agent did (e.g., 'analysis', 'projection', 'callout_write')
        market: Market code (e.g., 'AU', 'MX')
        week: ISO week string (e.g., '2026 W13')
        description: Human-readable summary of what was done
        output_summary: Optional — what files/records the agent produced
        confidence: Optional — agent's self-assessed confidence (0-1)
        db_path: Optional database path override

    Returns:
        int: The auto-incremented ID of the new row
    """
    path = db_path or DB_PATH
    _check_db_exists(path)
    con = duckdb.connect(path)
    try:
        next_id = con.execute("SELECT nextval('agent_actions_seq')").fetchone()[0]
        con.execute("""
            INSERT INTO agent_actions (id, agent, action_type, market, week,
                                       description, output_summary, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, [next_id, agent, action_type, market, week,
              description, output_summary, confidence])
        return next_id
    finally:
        con.close()


def log_agent_observation(agent, observation_type, market, week, content,
                          severity='info', db_path=None):
    """Write an agent observation to agent_observations. Returns the observation ID.

    Multiple rows per agent run. Agents record anomalies, patterns,
    projection accuracy, narrative threads, data quality issues, and
    competitive observations. acted_on defaults to false.

    Args:
        agent: Agent name (e.g., 'market-analyst')
        observation_type: Category (e.g., 'anomaly', 'pattern', 'projection_accuracy')
        market: Market code
        week: ISO week string
        content: Natural language description of the observation
        severity: 'info' (default), 'warning', or 'critical'
        db_path: Optional database path override

    Returns:
        int: The auto-incremented ID of the new row
    """
    path = db_path or DB_PATH
    _check_db_exists(path)
    con = duckdb.connect(path)
    try:
        next_id = con.execute("SELECT nextval('agent_observations_seq')").fetchone()[0]
        con.execute("""
            INSERT INTO agent_observations (id, agent, observation_type, market,
                                            week, content, severity, acted_on)
            VALUES (?, ?, ?, ?, ?, ?, ?, false)
        """, [next_id, agent, observation_type, market, week, content, severity])
        return next_id
    finally:
        con.close()


def query_prior_observations(market, weeks=4, observation_type=None, db_path=None):
    """Query recent observations for a market. This is the agent's learned experience.

    Returns observations from the last N weeks for the given market,
    ordered most recent first. Optionally filter by observation type.
    Agents call this at the start of each run to incorporate prior knowledge.

    Args:
        market: Market code (e.g., 'AU')
        weeks: Number of weeks to look back (default 4)
        observation_type: Optional filter (e.g., 'anomaly', 'pattern')
        db_path: Optional database path override

    Returns:
        list[dict]: Observations ordered by created_at descending. Empty list if none.
    """
    path = db_path or DB_PATH
    _check_db_exists(path)

    sql = """
        SELECT * FROM agent_observations
        WHERE market = ?
        AND created_at >= current_timestamp - INTERVAL '{days}' DAY
    """.format(days=int(weeks * 7))
    params = [market]

    if observation_type:
        sql += " AND observation_type = ?"
        params.append(observation_type)

    sql += " ORDER BY created_at DESC"

    con = duckdb.connect(path, read_only=True)
    try:
        result = con.execute(sql, params)
        columns = [desc[0] for desc in result.description]
        rows = result.fetchall()
        return [dict(zip(columns, row)) for row in rows]
    finally:
        con.close()


def log_architecture_eval(change_name, pipeline, market, scores, evaluator_notes,
                          verdict, db_path=None):
    """Log an architecture evaluation result. Convenience wrapper around log_agent_observation.

    Used by the blind evaluation protocol to record whether an architecture
    change passed, regressed, or was neutral.

    Args:
        change_name: Name of the architecture change (e.g., 'agent-consolidation')
        pipeline: Which pipeline was evaluated (e.g., 'wbr-callouts')
        market: Market code evaluated
        scores: Dict of evaluation scores (e.g., {'factual_equivalence': 'PASS', ...})
        evaluator_notes: Free-text evaluator commentary
        verdict: Overall verdict ('APPROVED', 'APPROVED_WITH_NOTES', 'REJECTED')
        db_path: Optional database path override

    Returns:
        int: The observation ID
    """
    import json
    content = json.dumps({
        'change_name': change_name,
        'pipeline': pipeline,
        'scores': scores,
        'evaluator_notes': evaluator_notes,
        'verdict': verdict,
    })
    severity = 'critical' if verdict == 'REJECTED' else 'info'
    return log_agent_observation(
        agent='architecture-evaluator',
        observation_type='architecture_eval',
        market=market,
        week='',  # evals aren't week-specific
        content=content,
        severity=severity,
        db_path=db_path,
    )


## ── Slack Data Access ──────────────────────────────────────────────

def slack_channel_summary(channel_name=None, db_path=None):
    """Get message counts and signal breakdown per channel (or for a specific channel)."""
    db_path = db_path or DB_PATH
    where = f"WHERE channel_name = '{channel_name}'" if channel_name else ""
    return db(f"""
        SELECT channel_name, COUNT(*) as messages,
               SUM(CASE WHEN is_richard THEN 1 ELSE 0 END) as richard_msgs,
               SUM(CASE WHEN signal_type = 'action-item' THEN 1 ELSE 0 END) as action_items,
               SUM(CASE WHEN signal_type = 'decision' THEN 1 ELSE 0 END) as decisions,
               SUM(CASE WHEN signal_type = 'escalation' THEN 1 ELSE 0 END) as escalations,
               MIN(ts) as oldest_ts, MAX(ts) as newest_ts
        FROM slack_messages {where}
        GROUP BY channel_name ORDER BY messages DESC
    """, db_path=db_path)


def slack_recent(channel_name=None, limit=20, signal_type=None, db_path=None):
    """Get recent Slack messages, optionally filtered by channel and/or signal type."""
    db_path = db_path or DB_PATH
    conditions = []
    if channel_name:
        conditions.append(f"channel_name = '{channel_name}'")
    if signal_type:
        conditions.append(f"signal_type = '{signal_type}'")
    where = "WHERE " + " AND ".join(conditions) if conditions else ""
    return db(f"""
        SELECT ts, channel_name, author_alias, text_preview, signal_type, reply_count, reaction_count
        FROM slack_messages {where}
        ORDER BY ts DESC LIMIT {limit}
    """, db_path=db_path)


def slack_search(keyword, limit=20, db_path=None):
    """Full-text search across Slack messages."""
    db_path = db_path or DB_PATH
    escaped = keyword.replace("'", "''")
    return db(f"""
        SELECT ts, channel_name, author_alias, text_preview, signal_type
        FROM slack_messages
        WHERE full_text ILIKE '%{escaped}%'
        ORDER BY ts DESC LIMIT {limit}
    """, db_path=db_path)


def slack_person(alias_or_id, db_path=None):
    """Get a person's Slack activity summary."""
    db_path = db_path or DB_PATH
    escaped = alias_or_id.replace("'", "''")
    return db(f"""
        SELECT sp.user_id, sp.alias, sp.display_name, sp.total_messages,
               sp.relationship_tier,
               (SELECT COUNT(*) FROM slack_messages sm WHERE sm.author_id = sp.user_id
                AND sm.signal_type = 'action-item') as action_items_sent,
               (SELECT COUNT(DISTINCT sm.channel_name) FROM slack_messages sm
                WHERE sm.author_id = sp.user_id) as channels_active
        FROM slack_people sp
        WHERE sp.alias = '{escaped}' OR sp.user_id = '{escaped}' OR sp.display_name ILIKE '%{escaped}%'
    """, db_path=db_path)


def slack_decisions(weeks=4, db_path=None):
    """Get recent decisions from Slack, ordered by recency."""
    db_path = db_path or DB_PATH
    return db(f"""
        SELECT ts, channel_name, author_alias, text_preview
        FROM slack_messages
        WHERE signal_type = 'decision'
        ORDER BY ts DESC LIMIT {weeks * 5}
    """, db_path=db_path)


def slack_action_items(resolved=False, db_path=None):
    """Get action items from Slack. By default shows unresolved (no thread reply)."""
    db_path = db_path or DB_PATH
    reply_filter = ">= 1" if resolved else "= 0"
    return db(f"""
        SELECT ts, channel_name, author_alias, text_preview, reply_count
        FROM slack_messages
        WHERE signal_type = 'action-item' AND reply_count {reply_filter}
        ORDER BY ts DESC LIMIT 30
    """, db_path=db_path)


def main():
    parser = argparse.ArgumentParser(description='Query PS Analytics DuckDB')
    parser.add_argument('sql', nargs='?', help='SQL query to execute')
    parser.add_argument('--tables', action='store_true', help='List all tables')
    parser.add_argument('--stats', action='store_true', help='Show row counts per table')
    parser.add_argument('--table', help='Show schema for a specific table')
    parser.add_argument('--validate', help='Validate SQL without executing')
    parser.add_argument('--schema-json', action='store_true', help='Export full schema as JSON')
    parser.add_argument('--export-parquet', action='store_true', help='Export key tables as Parquet')
    parser.add_argument('--schema-export', action='store_true', help='Export schema as CREATE TABLE SQL')
    parser.add_argument('--summary', action='store_true', help='Show agent state summary (actions + observations)')
    parser.add_argument('--db', default=DB_PATH, help='Database path')
    args = parser.parse_args()

    con = duckdb.connect(args.db, read_only=True)

    if args.tables:
        tables = con.execute("SHOW TABLES").fetchall()
        for t in tables:
            print(t[0])
    elif args.stats:
        tables = con.execute("SHOW TABLES").fetchall()
        for t in tables:
            count = con.execute(f"SELECT COUNT(*) FROM {t[0]}").fetchone()[0]
            print(f"  {t[0]}: {count:,} rows")
    elif args.table:
        cols = con.execute(f"DESCRIBE {args.table}").fetchall()
        for c in cols:
            print(f"  {c[0]:30s} {c[1]}")
    elif args.validate:
        con.close()
        try:
            db_validate(args.validate, db_path=args.db)
            print("✓ SQL is valid")
        except Exception as e:
            print(f"✗ {e}")
            sys.exit(1)
        return
    elif args.schema_json:
        con.close()
        import json
        print(json.dumps(schema(db_path=args.db), indent=2))
        return
    elif args.export_parquet:
        con.close()
        exported = export_parquet(db_path=args.db)
        for table, path in exported.items():
            print(f"  {table} → {path}")
        if not exported:
            print("  No tables with data to export.")
        return
    elif args.schema_export:
        con.close()
        out_path = schema_export(db_path=args.db)
        print(f"  Schema exported to {out_path}")
        return
    elif args.summary:
        # Agent state summary
        actions_count = con.execute("SELECT COUNT(*) FROM agent_actions").fetchone()[0]
        obs_count = con.execute("SELECT COUNT(*) FROM agent_observations").fetchone()[0]
        print("Agent State Summary:")
        print(f"  agent_actions:      {actions_count:,} rows")
        print(f"  agent_observations: {obs_count:,} rows")
        if actions_count > 0:
            recent = con.execute(
                "SELECT agent, action_type, market, week FROM agent_actions ORDER BY created_at DESC LIMIT 5"
            ).fetchall()
            print("\n  Recent actions:")
            for r in recent:
                print(f"    {r[0]} | {r[1]} | {r[2]} | {r[3]}")
        if obs_count > 0:
            by_type = con.execute(
                "SELECT observation_type, COUNT(*) as n FROM agent_observations GROUP BY observation_type ORDER BY n DESC"
            ).fetchall()
            print("\n  Observations by type:")
            for r in by_type:
                print(f"    {r[0]}: {r[1]}")
    elif args.sql:
        result = con.execute(args.sql)
        columns = [desc[0] for desc in result.description]
        rows = result.fetchall()
        # Print as table
        if rows:
            widths = [max(len(str(c)), max(len(str(r[i])) for r in rows)) for i, c in enumerate(columns)]
            header = ' | '.join(c.ljust(w) for c, w in zip(columns, widths))
            print(header)
            print('-+-'.join('-' * w for w in widths))
            for row in rows:
                print(' | '.join(str(v).ljust(w) for v, w in zip(row, widths)))
            print(f"\n({len(rows)} rows)")
    else:
        parser.print_help()

    con.close()


if __name__ == '__main__':
    main()
