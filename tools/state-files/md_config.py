"""Shared MotherDuck configuration for state-file scripts.

Reads the motherduck_token from the Kiro MCP config file.
All state-file scripts import this instead of hardcoding tokens.
"""

import json
import os

_MCP_CONFIG_PATHS = [
    os.path.expanduser("~/shared/.kiro/settings/mcp.json"),
    os.path.expanduser("~/.kiro/settings/mcp.json"),
]

LOCAL_DB = os.path.expanduser("~/shared/data/duckdb/ps-analytics.duckdb")
MD_DATABASE = "ps_analytics"


def get_motherduck_token():
    """Extract motherduck_token from the Kiro MCP config."""
    # Check env first
    token = os.environ.get("motherduck_token") or os.environ.get("MOTHERDUCK_TOKEN")
    if token:
        return token

    # Read from MCP config
    for path in _MCP_CONFIG_PATHS:
        if not os.path.exists(path):
            continue
        with open(path) as f:
            config = json.load(f)
        servers = config.get("mcpServers", {})
        duckdb_cfg = servers.get("duckdb", {})
        env = duckdb_cfg.get("env", {})
        token = env.get("motherduck_token") or env.get("MOTHERDUCK_TOKEN")
        if token:
            return token

    return None


def connect_motherduck():
    """Connect to MotherDuck with the token from MCP config."""
    import duckdb

    token = get_motherduck_token()
    if not token:
        raise RuntimeError(
            "MotherDuck token not found. Set motherduck_token env var "
            "or configure it in ~/.kiro/settings/mcp.json"
        )

    os.environ["motherduck_token"] = token
    con = duckdb.connect("md:")
    con.execute(f"USE {MD_DATABASE}")
    return con


def connect_local():
    """Connect to the local DuckDB file (read-only)."""
    import duckdb

    if not os.path.exists(LOCAL_DB):
        raise FileNotFoundError(f"Local DB not found: {LOCAL_DB}")
    return duckdb.connect(LOCAL_DB, read_only=True)
