#!/usr/bin/env python3
"""
refresh-body-system.py — Build body-system-data.json for the Body System dashboard.

Data sources:
  1. DuckDB (MotherDuck: ps_analytics) — karpathy.*, main.l1_streak, ns.ns_patterns
  2. Organ markdown files — ~/shared/context/body/*.md (live word counts)
  3. amcc.md — streak, hard thing, resistance types
  4. gut.md — word budgets

Output: shared/dashboards/data/body-system-data.json
"""
import json, os, re, subprocess, sys
from pathlib import Path
from datetime import datetime, timezone, date

HOME = Path.home()
BODY_DIR = HOME / "shared/context/body"
OUTPUT = HOME / "shared/dashboards/data/body-system-data.json"

# Silent-fallback-to-cache is the #1 source of stale-data bugs on this dashboard.
# Default: FAIL LOUD. If the token is missing or DuckDB is unreachable, stop and
# tell the operator — don't silently serve 8-day-old cache pretending to be live.
#
# Override with --allow-stale or BODY_REFRESH_ALLOW_STALE=1 if you genuinely want
# to fall back to cache (e.g. in tests, or when MotherDuck is temporarily down
# and a stale snapshot is better than nothing). The override is intentionally
# verbose so it shows up in any CI log or agent trace.
ALLOW_STALE = (
    "--allow-stale" in sys.argv
    or os.environ.get("BODY_REFRESH_ALLOW_STALE") == "1"
)
MAX_CACHE_AGE_HOURS = float(os.environ.get("BODY_REFRESH_MAX_CACHE_AGE_HOURS", "24"))


def resolve_motherduck_token():
    """Resolve the MotherDuck token from (1) env, (2) mcp.json duckdb server config.

    The MCP config is the durable source of truth — it's what the running DuckDB
    MCP server uses. Falling back to it means ad-hoc runs (./refresh-body-system.py)
    succeed without requiring the operator to export the env var manually.
    Env var still wins so CI/hooks can override.
    """
    tok = os.environ.get("MOTHERDUCK_TOKEN") or os.environ.get("motherduck_token")
    if tok:
        return tok, "env"
    mcp_path = HOME / ".kiro/settings/mcp.json"
    if mcp_path.exists():
        try:
            cfg = json.loads(mcp_path.read_text())
            for name, server in (cfg.get("mcpServers") or {}).items():
                if "duck" not in name.lower():
                    continue
                env = server.get("env") or {}
                tok = env.get("motherduck_token") or env.get("MOTHERDUCK_TOKEN")
                if tok:
                    return tok, f"mcp.json:{name}"
        except Exception as e:
            print(f"  Could not read mcp.json for token: {e}", file=sys.stderr)
    return None, None

# Organs tracked in the body system (core organs only, not wiki agents or style guides)
CORE_ORGANS = [
    "brain", "memory", "heart", "eyes", "amcc",
    "hands", "device", "nervous-system", "spine", "gut", "body"
]


def query_duckdb(sql):
    """Query MotherDuck via duckdb Python package.

    Default behavior: if DuckDB is unreachable (no token, no network, auth
    failure), raise SystemExit — fail loud. This prevents the subtle bug
    where the refresh script "succeeds" but has silently been serving stale
    cached data for 8 days.

    Override: set BODY_REFRESH_ALLOW_STALE=1 or pass --allow-stale on the CLI
    to get the old fallback-to-cache behavior.
    """
    try:
        import duckdb as ddb
        token, source = resolve_motherduck_token()
        if not token:
            raise RuntimeError("No MotherDuck token in env or mcp.json")
        con = ddb.connect(f"md:ps_analytics?motherduck_token={token}")
        result = con.execute(sql)
        columns = [desc[0] for desc in result.description]
        rows = result.fetchall()
        return [dict(zip(columns, row)) for row in rows]
    except Exception as e:
        msg = f"DuckDB unavailable: {e}"
        if ALLOW_STALE:
            print(f"  {msg} (BODY_REFRESH_ALLOW_STALE=1 — falling back to cache)")
            return None
        # Fail loud. The dashboard depends on this data being live.
        print(
            f"\n❌ {msg}\n"
            f"   This would have caused refresh-body-system.py to silently serve stale cache.\n"
            f"   The body-system dashboard depends on live data — run with a valid token:\n"
            f"     export MOTHERDUCK_TOKEN=<token>\n"
            f"   OR ensure ~/.kiro/settings/mcp.json has a duckdb server with motherduck_token.\n"
            f"   To intentionally use cache (CI, tests, outage fallback), rerun with:\n"
            f"     BODY_REFRESH_ALLOW_STALE=1 python3 {Path(__file__).name}\n",
            file=sys.stderr,
        )
        sys.exit(2)


def load_duckdb_cache():
    """Load pre-populated DuckDB cache (written by MCP tool or prior run).

    Only used when ALLOW_STALE is set (BODY_REFRESH_ALLOW_STALE=1 or
    --allow-stale). Warns loudly if the cache exceeds MAX_CACHE_AGE_HOURS
    (default 24h) — this is exactly the bug that triggered this refactor:
    an 8-day-old cache being served as if it were live.
    """
    cache_path = HOME / "shared/dashboards/data/body-system-duckdb-cache.json"
    if not cache_path.exists():
        return {}
    try:
        data = json.loads(cache_path.read_text())
        cached_at = datetime.fromisoformat(
            data.get("cached_at", "2000-01-01T00:00:00+00:00")
        )
        age_hours = (datetime.now(tz=timezone.utc) - cached_at).total_seconds() / 3600
        if age_hours > MAX_CACHE_AGE_HOURS:
            print(
                f"\n⚠  Cache is {age_hours:.1f}h old (threshold: {MAX_CACHE_AGE_HOURS}h).\n"
                f"   Data written to body-system-data.json will be STALE.\n"
                f"   This defeats the purpose of a refresh — fix the token and rerun live.\n",
                file=sys.stderr,
            )
        else:
            print(f"  Using DuckDB cache (age: {age_hours:.1f}h)")
        return data
    except Exception as e:
        print(f"  Cache read failed: {e}")
    return {}


def count_words(filepath):
    """Count words in a markdown file, excluding frontmatter and HTML comments."""
    if not filepath.exists():
        return 0
    text = filepath.read_text(encoding="utf-8", errors="replace")
    # Strip YAML frontmatter
    text = re.sub(r"^---\n.*?\n---\n", "", text, flags=re.DOTALL)
    # Strip HTML comments
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    return len(text.split())


def get_organ_word_counts():
    """Get live word counts from organ files on disk."""
    counts = {}
    for organ in CORE_ORGANS:
        path = BODY_DIR / f"{organ}.md"
        counts[organ] = count_words(path)
    return counts


def get_organ_budgets():
    """Extract word budgets from gut.md baseline budget table."""
    gut_path = BODY_DIR / "gut.md"
    budgets = {}
    if not gut_path.exists():
        return budgets
    text = gut_path.read_text(encoding="utf-8", errors="replace")
    # Match rows like: | Memory | 3500w | 2436w | Notes |
    # or: | Gut (this file) | 2000w | ~2100w | Notes |
    for line in text.split("\n"):
        match = re.match(
            r"\|\s*([^|]+?)\s*\|\s*(\d+)w\s*\|", line
        )
        if match:
            raw_name = match.group(1).strip().lower()
            budget = int(match.group(2))
            # Normalize organ names
            name_map = {
                "memory": "memory", "heart": "heart", "brain": "brain",
                "eyes": "eyes", "amcc": "amcc", "hands": "hands",
                "device": "device", "gut (this file)": "gut", "gut": "gut",
                "nervous system": "nervous-system", "spine": "spine",
                "body": "body",
            }
            organ = name_map.get(raw_name)
            if organ and organ in CORE_ORGANS:
                budgets[organ] = budget
    return budgets


def get_staleness():
    """Calculate days since each organ file was last modified."""
    today = date.today()
    staleness = {}
    for organ in CORE_ORGANS:
        path = BODY_DIR / f"{organ}.md"
        if path.exists():
            mtime = datetime.fromtimestamp(path.stat().st_mtime).date()
            staleness[organ] = {
                "days_stale": (today - mtime).days,
                "updated": mtime.isoformat(),
            }
        else:
            staleness[organ] = {"days_stale": -1, "updated": "unknown"}
    return staleness


def get_experiment_summary():
    """Get experiment stats from DuckDB."""
    summary = query_duckdb("""
        SELECT
            MAX(run_id) as latest_run,
            COUNT(DISTINCT run_id) as total_runs,
            COUNT(*) as total_experiments,
            SUM(CASE WHEN decision='KEEP' THEN 1 ELSE 0 END) as total_kept,
            SUM(CASE WHEN decision='REVERT' THEN 1 ELSE 0 END) as total_reverted
        FROM karpathy.autoresearch_experiments
    """)
    return summary[0] if summary else {}


def get_experiment_history():
    """Get recent experiments for the log table."""
    rows = query_duckdb("""
        SELECT id, run_id, organ, section, technique, decision,
               words_before, words_after, word_delta,
               score_a, score_b, started_at, notes
        FROM karpathy.autoresearch_experiments
        ORDER BY id DESC
        LIMIT 30
    """)
    return rows


def get_experiment_by_organ():
    """Get per-organ experiment stats."""
    rows = query_duckdb("""
        SELECT organ,
               COUNT(*) as exp_count,
               SUM(CASE WHEN decision='KEEP' THEN 1 ELSE 0 END) as kept,
               SUM(word_delta) as total_delta
        FROM karpathy.autoresearch_experiments
        GROUP BY organ
        ORDER BY exp_count DESC
    """)
    return rows


def get_l1_streak():
    """Get latest L1 streak data."""
    rows = query_duckdb("""
        SELECT tracker_date, workdays_at_zero, artifact_shipped,
               artifact_name, hard_thing_name, notes
        FROM main.l1_streak
        ORDER BY tracker_date DESC
        LIMIT 14
    """)
    return rows


def get_patterns():
    """Get behavioral patterns from ns.ns_patterns."""
    rows = query_duckdb("""
        SELECT pattern_name, status, weeks_active, gate_or_fix,
               first_detected, updated_at
        FROM ns.ns_patterns
        ORDER BY
            CASE status
                WHEN 'WORSENING' THEN 1
                WHEN 'STUCK' THEN 2
                WHEN 'IMPROVING' THEN 3
                WHEN 'RESOLVED' THEN 4
                ELSE 5
            END,
            weeks_active DESC
    """)
    return rows


def get_organ_health():
    """Get latest organ health snapshot from autoresearch."""
    rows = query_duckdb("""
        SELECT organ, word_count, word_budget, utilization,
               accuracy_estimate, experiments_run, experiments_kept
        FROM karpathy.autoresearch_organ_health
        WHERE run_id = (SELECT MAX(run_id) FROM karpathy.autoresearch_organ_health)
        ORDER BY organ
    """)
    return rows


def get_five_levels():
    """Get Five Levels weekly data."""
    rows = query_duckdb("""
        SELECT week_start, level, level_name, tasks_completed,
               artifacts_shipped, streak_weeks
        FROM main.five_levels_weekly
        ORDER BY week_start DESC, level ASC
        LIMIT 25
    """)
    return rows


def get_weekly_output():
    """Get weekly output scorecard from Asana task completions."""
    rows = query_duckdb("""
        SELECT
            DATE_TRUNC('week', completed_at::DATE) as week_start,
            COUNT(*) as tasks_completed,
            COUNT(CASE WHEN project_name LIKE '%ABPS AI%' THEN 1 END) as content_tasks,
            COUNT(CASE WHEN routine_rw = 'Core' THEN 1 END) as core_tasks,
            COUNT(CASE WHEN routine_rw = 'Engine Room' THEN 1 END) as engine_tasks
        FROM asana.asana_tasks
        WHERE completed = TRUE
            AND completed_at IS NOT NULL
            AND completed_at >= CURRENT_DATE - INTERVAL '8 weeks'
        GROUP BY DATE_TRUNC('week', completed_at::DATE)
        ORDER BY week_start DESC
        LIMIT 8
    """)
    return rows


def parse_amcc_for_challenge():
    """Parse amcc.md for the 30-day challenge items and resistance types."""
    amcc_path = BODY_DIR / "amcc.md"
    if not amcc_path.exists():
        return {"items": [], "resistance_types": [], "streak": 0, "hard_thing": ""}
    text = amcc_path.read_text(encoding="utf-8", errors="replace")

    # Extract streak
    streak_match = re.search(r"(?:streak|consecutive).*?(\d+)", text, re.IGNORECASE)
    streak = int(streak_match.group(1)) if streak_match else 0

    # Extract hard thing
    hard_match = re.search(
        r"hard.thing[:\s]*(.+?)(?:\n|$)", text, re.IGNORECASE
    )
    hard_thing = hard_match.group(1).strip() if hard_match else ""

    return {"streak": streak, "hard_thing": hard_thing}


def get_agent_health():
    """Read agent definition JSON files and extract success metrics for the dashboard.
    
    Scans .kiro/agents/ for custom agent definitions (excludes platform defaults
    like AIPowerUserCapabilities-*, AgentSpacesAIM-*, AmazonBuilderCoreAIAgents-*,
    AtlasAICapabilities-*, local-arcc-*). Returns a list of agent summaries with
    name, description, team grouping, and success metrics.
    
    Merges runtime telemetry from ops.agent_reliability (invocation counts,
    last-invoked, success rate) when available. Per the System Health Dashboard
    follow-on spec — the ops.agent_invocations table exists but the logging shim
    that populates it is scoped in that spec.
    """
    agents_dir = HOME / ".kiro/agents"
    if not agents_dir.exists():
        return []

    # Platform-default prefixes to skip
    skip_prefixes = (
        "AIPowerUserCapabilities-", "AgentSpacesAIM-",
        "AmazonBuilderCoreAIAgents-", "AtlasAICapabilities-",
        "local-arcc-", "eval-", "agentspaces-",
    )
    # Utility agents that don't need health tracking
    skip_names = {"title-generator", "agent_config.json.example"}

    # Team groupings based on agent name
    team_map = {
        "market-analyst": "WBR Callouts",
        "callout-writer": "WBR Callouts",
        "callout-reviewer": "WBR Callouts",
        "wiki-editor": "Wiki Team",
        "wiki-writer": "Wiki Team",
        "wiki-researcher": "Wiki Team",
        "wiki-critic": "Wiki Team",
        "wiki-librarian": "Wiki Team",
        "wiki-concierge": "Wiki Team",
        "karpathy": "Body System",
        "rw-trainer": "Body System",
        "eyes-chart": "Body System",
        "agent-bridge-sync": "Body System",
    }

    # Pull runtime telemetry if the reliability view has data
    runtime_rows = query_duckdb("""
        SELECT agent_name, total_invocations, successes, failures,
               success_rate, avg_duration_s,
               last_invoked::VARCHAR as last_invoked,
               invocations_7d, invocations_30d, total_token_cost
        FROM ops.agent_reliability
    """) or []
    runtime_by_agent = {r["agent_name"]: r for r in runtime_rows}

    agents = []
    for f in sorted(agents_dir.glob("*.json")):
        name = f.stem
        if any(name.startswith(p) for p in skip_prefixes):
            continue
        if name in skip_names:
            continue
        try:
            data = json.loads(f.read_text())
        except Exception:
            continue
        metrics = data.get("successMetrics", [])
        agent_name = data.get("name", name)
        rt = runtime_by_agent.get(agent_name, {})
        agents.append({
            "name": agent_name,
            "description": data.get("description", ""),
            "team": team_map.get(agent_name, "Other"),
            "metrics_count": len(metrics),
            "metrics": metrics,
            "has_metrics": len(metrics) > 0,
            # Runtime telemetry (empty/zero when ops.agent_invocations not yet populated)
            "total_invocations": rt.get("total_invocations", 0) or 0,
            "invocations_7d": rt.get("invocations_7d", 0) or 0,
            "invocations_30d": rt.get("invocations_30d", 0) or 0,
            "failures": rt.get("failures", 0) or 0,
            "success_rate": rt.get("success_rate"),
            "last_invoked": rt.get("last_invoked"),
            "avg_duration_s": rt.get("avg_duration_s"),
        })
    return agents


def get_hook_reliability():
    """Fetch recent hook reliability stats for the System Health section.
    
    Reads from the existing ops.hook_reliability view (no new logging required).
    Flags hooks with recent failures or long-stale last-run for visibility.
    """
    rows = query_duckdb("""
        SELECT hook_name, total_runs, avg_duration_s, max_duration_s,
               total_failures, total_asana_writes,
               last_run::VARCHAR as last_run,
               DATE_DIFF('day', last_run::DATE, CURRENT_DATE) as days_since_last_run
        FROM ops.hook_reliability
        ORDER BY last_run DESC NULLS LAST
        LIMIT 20
    """) or []
    return rows


def get_workflow_reliability():
    """Fetch recent workflow reliability stats (multi-step agent workflows like am-backend-parallel-v2).
    
    Reads from ops.workflow_reliability view. Surfaces success rate + last run.
    """
    rows = query_duckdb("""
        SELECT workflow_name, total_runs, successes, success_rate,
               avg_duration_s,
               last_run::VARCHAR as last_run,
               DATE_DIFF('day', last_run::DATE, CURRENT_DATE) as days_since_last_run
        FROM ops.workflow_reliability
        ORDER BY last_run DESC NULLS LAST
        LIMIT 15
    """) or []
    return rows


def main():
    print("=" * 50)
    print("Body System Data Refresh")
    print("=" * 50)

    # ── Live organ word counts from disk ──
    print("\n[1/7] Counting organ words from disk...")
    live_counts = get_organ_word_counts()
    budgets = get_organ_budgets()
    staleness = get_staleness()
    total_words = sum(live_counts.values())
    total_budget = sum(budgets.values()) if budgets else 0

    organ_budgets = []
    for organ in CORE_ORGANS:
        actual = live_counts.get(organ, 0)
        budget = budgets.get(organ, 0)
        util = round(actual / budget * 100) if budget > 0 else 0
        stale = staleness.get(organ, {})
        organ_budgets.append({
            "organ": organ.replace("-", " ").title(),
            "organ_key": organ,
            "actual": actual,
            "budget": budget,
            "utilization": util,
            "days_stale": stale.get("days_stale", -1),
            "updated": stale.get("updated", "unknown"),
        })
    print(f"  Total body: {total_words:,}w / {total_budget:,}w budget")

    # ── Experiment data from DuckDB (or cache) ──
    print("\n[2/7] Querying experiment data...")
    cache = load_duckdb_cache()
    use_cache = False

    # Test DuckDB connectivity
    test = query_duckdb("SELECT 1 as ok")
    if test is None:
        print("  Falling back to DuckDB cache...")
        use_cache = True

    if not use_cache:
        exp_summary = query_duckdb("""
            SELECT MAX(run_id) as latest_run, COUNT(DISTINCT run_id) as total_runs,
                   COUNT(*) as total_experiments,
                   SUM(CASE WHEN decision='KEEP' THEN 1 ELSE 0 END)::INT as total_kept
            FROM karpathy.autoresearch_experiments
        """) or [{}]
        exp_summary = exp_summary[0] if exp_summary else {}
    else:
        exp_summary = cache.get("exp_summary", {})

    if not use_cache:
        exp_history = query_duckdb("""
            SELECT id, run_id, organ, section, technique, decision,
                   words_before, words_after, word_delta,
                   score_a, score_b, started_at::VARCHAR as started_at, notes
            FROM karpathy.autoresearch_experiments ORDER BY id DESC LIMIT 60
        """) or []
    else:
        exp_history = cache.get("experiment_history", [])

    if not use_cache:
        exp_by_organ = query_duckdb("""
            SELECT organ, COUNT(*) as exp_count,
                   SUM(CASE WHEN decision='KEEP' THEN 1 ELSE 0 END) as kept,
                   SUM(word_delta) as total_delta,
                   MAX(started_at) as last_touched
            FROM karpathy.autoresearch_experiments
            WHERE organ IN ('brain','memory','heart','eyes','amcc','hands','device','nervous-system','spine','gut','body')
            GROUP BY organ ORDER BY exp_count DESC
        """) or []
    else:
        exp_by_organ = cache.get("experiment_by_organ", [])

    # Per-run aggregation — makes the loop's pulse visible (11 runs, gap-days, etc.)
    if not use_cache:
        exp_by_run = query_duckdb("""
            SELECT run_id,
                   MIN(started_at)::VARCHAR as started_at,
                   MAX(completed_at)::VARCHAR as ended_at,
                   COUNT(*) as n,
                   SUM(CASE WHEN decision='KEEP' THEN 1 ELSE 0 END) as kept,
                   SUM(CASE WHEN decision='REVERT' THEN 1 ELSE 0 END) as reverted,
                   SUM(CASE WHEN decision='BLOCKER' THEN 1 ELSE 0 END) as blocked,
                   SUM(word_delta) as word_delta,
                   COUNT(DISTINCT organ) as organs_touched
            FROM karpathy.autoresearch_experiments
            WHERE run_id IS NOT NULL
            GROUP BY run_id
            ORDER BY run_id DESC
        """) or []
    else:
        exp_by_run = cache.get("experiment_by_run", [])

    # Per-technique — which compression techniques actually win blind A/Bs.
    # This is the highest-signal pivot karpathy asked for: if REMOVE wins 37%
    # and REWORD wins 100%, the selector should up-weight REWORD.
    if not use_cache:
        exp_by_technique = query_duckdb("""
            SELECT technique,
                   COUNT(*) as n,
                   SUM(CASE WHEN decision='KEEP' THEN 1 ELSE 0 END) as kept,
                   SUM(CASE WHEN decision='REVERT' THEN 1 ELSE 0 END) as reverted,
                   SUM(CASE WHEN decision='BLOCKER' THEN 1 ELSE 0 END) as blocked,
                   SUM(word_delta) as net_delta,
                   AVG(delta_ab) as avg_delta_ab
            FROM karpathy.autoresearch_experiments
            WHERE technique IS NOT NULL
            GROUP BY technique
            ORDER BY n DESC
        """) or []
    else:
        exp_by_technique = cache.get("experiment_by_technique", [])

    # Rolling windows — did the loop improve over the last 7d/30d or stall?
    # NULL columns mean "no experiments in that window" — the UI should
    # flag this loudly (stalled loop = the single most important signal).
    if not use_cache:
        exp_windows = query_duckdb("""
            SELECT
                COUNT(*) FILTER (WHERE started_at >= CURRENT_TIMESTAMP - INTERVAL '7 days') as n_7d,
                COUNT(*) FILTER (WHERE started_at >= CURRENT_TIMESTAMP - INTERVAL '7 days' AND decision='KEEP') as kept_7d,
                COUNT(*) FILTER (WHERE started_at >= CURRENT_TIMESTAMP - INTERVAL '30 days') as n_30d,
                COUNT(*) FILTER (WHERE started_at >= CURRENT_TIMESTAMP - INTERVAL '30 days' AND decision='KEEP') as kept_30d,
                MAX(started_at)::VARCHAR as last_experiment_at,
                DATE_DIFF('hour', MAX(started_at), CURRENT_TIMESTAMP) as hours_since_last
            FROM karpathy.autoresearch_experiments
        """) or [{}]
        exp_windows = exp_windows[0] if exp_windows else {}
    else:
        exp_windows = cache.get("exp_windows", {})

    # Per-day spark — last 30 days, so the UI can draw a "loop activity" sparkline
    if not use_cache:
        exp_by_day = query_duckdb("""
            SELECT DATE_TRUNC('day', started_at)::VARCHAR as day,
                   COUNT(*) as n,
                   SUM(CASE WHEN decision='KEEP' THEN 1 ELSE 0 END) as kept,
                   SUM(word_delta) as word_delta
            FROM karpathy.autoresearch_experiments
            WHERE started_at >= CURRENT_TIMESTAMP - INTERVAL '30 days'
            GROUP BY 1
            ORDER BY 1
        """) or []
    else:
        exp_by_day = cache.get("exp_by_day", [])

    if not use_cache:
        organ_health = query_duckdb("""
            SELECT organ, word_count, word_budget, utilization, accuracy_estimate
            FROM karpathy.autoresearch_organ_health
            WHERE run_id = (SELECT MAX(run_id) FROM karpathy.autoresearch_organ_health)
        """) or []
    else:
        organ_health = cache.get("organ_health", [])

    total_runs = exp_summary.get("total_runs", 0)
    total_exp = exp_summary.get("total_experiments", 0)
    total_kept = exp_summary.get("total_kept", 0)
    keep_rate = round(total_kept / total_exp * 100) if total_exp > 0 else 0
    words_saved = sum(
        -(e.get("total_delta") or 0)
        for e in exp_by_organ
        if e.get("organ") in CORE_ORGANS
    )
    print(f"  {total_runs} runs, {total_exp} experiments, {keep_rate}% keep rate")

    # ── L1 streak ──
    print("\n[3/7] Querying L1 streak...")
    if not use_cache:
        streak_data = query_duckdb("""
            SELECT tracker_date::VARCHAR as tracker_date, workdays_at_zero, artifact_shipped,
                   artifact_name, hard_thing_name, notes
            FROM main.l1_streak ORDER BY tracker_date DESC LIMIT 14
        """) or []
    else:
        streak_data = cache.get("streak_history", [])
    latest_streak = streak_data[0] if streak_data else {}
    amcc_data = parse_amcc_for_challenge()
    print(f"  Streak: {latest_streak.get('workdays_at_zero', '?')} workdays at zero")

    # ── Patterns ──
    print("\n[4/7] Querying behavioral patterns...")
    if not use_cache:
        patterns = query_duckdb("""
            SELECT pattern_name, status, weeks_active, gate_or_fix,
                   first_detected::VARCHAR as first_detected, updated_at::VARCHAR as updated_at
            FROM ns.ns_patterns
            ORDER BY CASE status WHEN 'WORSENING' THEN 1 WHEN 'STUCK' THEN 2
                     WHEN 'IMPROVING' THEN 3 ELSE 4 END, weeks_active DESC
        """) or []
    else:
        patterns = cache.get("patterns", [])
    print(f"  {len(patterns)} patterns tracked")

    # ── Five Levels ──
    print("\n[5/7] Querying Five Levels...")
    if not use_cache:
        five_levels_data = query_duckdb("""
            SELECT week_start::VARCHAR as week_start, level, level_name,
                   tasks_completed, artifacts_shipped, streak_weeks
            FROM main.five_levels_weekly
            ORDER BY week_start DESC, level ASC LIMIT 25
        """) or []
    else:
        five_levels_data = cache.get("five_levels_weekly", [])

    # Static Five Levels definition (status from brain.md)
    five_levels = [
        {"level": 1, "name": "Sharpen Yourself", "status": "ACTIVE",
         "gate": "4 consecutive artifact weeks",
         "description": "Consistent weekly artifact output"},
        {"level": 2, "name": "Drive WW Testing", "status": "ACTIVE",
         "gate": "Every test has written status",
         "description": "Own end-to-end test methodology across all markets"},
        {"level": 3, "name": "Team Automation", "status": "NEXT",
         "gate": "One tool adopted by teammate",
         "description": "Build tools teammates actually adopt"},
        {"level": 4, "name": "Zero-Click Future", "status": "QUEUED",
         "gate": "Published POV that influenced a decision",
         "description": "Own the AEO/AI Overviews narrative for PS"},
        {"level": 5, "name": "Agentic Orchestration", "status": "FUTURE",
         "gate": "One autonomous PS workflow",
         "description": "PS workflows run without human intervention"},
    ]

    # ── Weekly output ──
    print("\n[6/7] Querying weekly output...")
    if not use_cache:
        weekly_output = query_duckdb("""
            SELECT DATE_TRUNC('week', completed_at::DATE)::VARCHAR as week_start,
                   COUNT(*) as tasks_completed,
                   COUNT(CASE WHEN project_name LIKE '%ABPS AI%' THEN 1 END) as content_tasks,
                   COUNT(CASE WHEN routine_rw = 'Core' THEN 1 END) as core_tasks,
                   COUNT(CASE WHEN routine_rw = 'Engine Room' THEN 1 END) as engine_tasks
            FROM asana.asana_tasks
            WHERE completed = TRUE AND completed_at IS NOT NULL
              AND completed_at >= CURRENT_DATE - INTERVAL '8 weeks'
            GROUP BY DATE_TRUNC('week', completed_at::DATE)
            ORDER BY week_start DESC LIMIT 8
        """) or []
    else:
        weekly_output = cache.get("weekly_output", [])
    print(f"  {len(weekly_output)} weeks of completion data")

    # ── Agent health ──
    print("\n[7/8] Reading agent success metrics + runtime telemetry...")
    agent_health = get_agent_health()
    agents_with_metrics = sum(1 for a in agent_health if a["has_metrics"])
    agents_invoked_7d = sum(1 for a in agent_health if a.get("invocations_7d", 0) > 0)
    print(f"  {len(agent_health)} custom agents, {agents_with_metrics} with success metrics, {agents_invoked_7d} invoked in last 7d")

    print("\n[7b/8] Reading hook + workflow reliability...")
    hook_reliability = get_hook_reliability()
    workflow_reliability = get_workflow_reliability()
    print(f"  {len(hook_reliability)} hooks tracked, {len(workflow_reliability)} workflows tracked")

    # ── Assemble ──
    print("\n[8/8] Assembling JSON...")
    _tok, _tok_source = resolve_motherduck_token()
    output = {
        "generated": datetime.now(tz=timezone.utc).isoformat(),
        "data_source": "cache" if use_cache else "live",
        "token_source": _tok_source or "none",
        # Overview page
        "five_levels": five_levels,
        "five_levels_weekly": [
            {k: (v.isoformat() if isinstance(v, (date, datetime)) else v)
             for k, v in row.items()}
            for row in five_levels_data
        ],
        # Autoresearch page
        "organ_budgets": organ_budgets,
        "body_total": total_words,
        "body_budget": total_budget,
        "body_utilization": round(total_words / total_budget * 100) if total_budget else 0,
        "over_budget_count": sum(
            1 for o in organ_budgets if o["budget"] > 0 and o["actual"] > o["budget"]
        ),
        "total_runs": total_runs,
        "total_experiments": total_exp,
        "total_kept": total_kept,
        "keep_rate": keep_rate,
        "words_saved": words_saved,
        # Rolling windows — the loop's current pulse. If n_7d=0 the loop is stalled.
        "experiment_windows": {
            "n_7d": exp_windows.get("n_7d", 0),
            "kept_7d": exp_windows.get("kept_7d", 0),
            "n_30d": exp_windows.get("n_30d", 0),
            "kept_30d": exp_windows.get("kept_30d", 0),
            "last_experiment_at": exp_windows.get("last_experiment_at"),
            "hours_since_last": exp_windows.get("hours_since_last"),
        },
        "experiment_by_run": [
            {k: (v.isoformat() if isinstance(v, (date, datetime)) else v)
             for k, v in row.items()}
            for row in exp_by_run
        ],
        "experiment_by_technique": [
            {k: (v.isoformat() if isinstance(v, (date, datetime)) else v)
             for k, v in row.items()}
            for row in exp_by_technique
        ],
        "experiment_by_day": [
            {k: (v.isoformat() if isinstance(v, (date, datetime)) else v)
             for k, v in row.items()}
            for row in exp_by_day
        ],
        "experiment_history": [
            {k: (v.isoformat() if isinstance(v, (date, datetime)) else v)
             for k, v in row.items()}
            for row in exp_history
        ],
        "experiment_by_organ": [
            {k: (v if not isinstance(v, (date, datetime)) else v.isoformat())
             for k, v in row.items()}
            for row in exp_by_organ
        ],
        "organ_health": [
            {k: (v.isoformat() if isinstance(v, (date, datetime)) else v)
             for k, v in row.items()}
            for row in organ_health
        ],
        # Willpower page
        "streak": {
            "current": latest_streak.get("workdays_at_zero", 0),
            "artifact_shipped": latest_streak.get("artifact_shipped", False),
            "hard_thing": latest_streak.get("hard_thing_name", amcc_data.get("hard_thing", "")),
            "tracker_date": str(latest_streak.get("tracker_date", "")),
        },
        "streak_history": [
            {k: (v.isoformat() if isinstance(v, (date, datetime)) else v)
             for k, v in row.items()}
            for row in streak_data
        ],
        "patterns": [
            {k: (v.isoformat() if isinstance(v, (date, datetime)) else v)
             for k, v in row.items()}
            for row in patterns
        ],
        # Output page
        "weekly_output": [
            {k: (v.isoformat() if isinstance(v, (date, datetime)) else v)
             for k, v in row.items()}
            for row in weekly_output
        ],
        # Agent health
        "agent_health": agent_health,
        # System health (hooks + workflows)
        "hook_reliability": [
            {k: (v.isoformat() if isinstance(v, (date, datetime)) else v)
             for k, v in row.items()}
            for row in hook_reliability
        ],
        "workflow_reliability": [
            {k: (v.isoformat() if isinstance(v, (date, datetime)) else v)
             for k, v in row.items()}
            for row in workflow_reliability
        ],
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(output, indent=2, default=str))
    print(f"\nWritten: {OUTPUT}")
    print(f"Body: {total_words:,}w / {total_budget:,}w ({output['body_utilization']}%)")
    print(f"Experiments: {total_exp} total, {total_kept} kept ({keep_rate}%)")
    print(f"Streak: {latest_streak.get('workdays_at_zero', '?')} workdays at zero")
    print(f"Patterns: {len(patterns)} tracked")


if __name__ == "__main__":
    main()
