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

# Organs tracked in the body system (core organs only, not wiki agents or style guides)
CORE_ORGANS = [
    "brain", "memory", "heart", "eyes", "amcc",
    "hands", "device", "nervous-system", "spine", "gut", "body"
]


def query_duckdb(sql):
    """Query MotherDuck via duckdb Python package.
    
    Falls back to cached data from body-system-duckdb-cache.json if DuckDB
    is unavailable (e.g., no MotherDuck token in environment).
    The cache is populated by the MCP DuckDB tool during dashboard refresh.
    """
    try:
        import duckdb as ddb
        token = os.environ.get("MOTHERDUCK_TOKEN") or os.environ.get("motherduck_token")
        if not token:
            raise RuntimeError("No MOTHERDUCK_TOKEN — use cache")
        con = ddb.connect(f"md:ps_analytics?motherduck_token={token}")
        result = con.execute(sql)
        columns = [desc[0] for desc in result.description]
        rows = result.fetchall()
        return [dict(zip(columns, row)) for row in rows]
    except Exception as e:
        print(f"  DuckDB unavailable: {e}")
    return None  # None = unavailable, [] = empty result


def load_duckdb_cache():
    """Load pre-populated DuckDB cache (written by MCP tool or prior run)."""
    cache_path = HOME / "shared/dashboards/data/body-system-duckdb-cache.json"
    if cache_path.exists():
        try:
            data = json.loads(cache_path.read_text())
            age = datetime.now(tz=timezone.utc) - datetime.fromisoformat(data.get("cached_at", "2000-01-01T00:00:00+00:00"))
            print(f"  Using DuckDB cache (age: {age.total_seconds()/3600:.1f}h)")
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
            FROM karpathy.autoresearch_experiments ORDER BY id DESC LIMIT 20
        """) or []
    else:
        exp_history = cache.get("experiment_history", [])

    if not use_cache:
        exp_by_organ = query_duckdb("""
            SELECT organ, COUNT(*) as exp_count,
                   SUM(CASE WHEN decision='KEEP' THEN 1 ELSE 0 END) as kept,
                   SUM(word_delta) as total_delta
            FROM karpathy.autoresearch_experiments
            WHERE organ IN ('brain','memory','heart','eyes','amcc','hands','device','nervous-system','spine','gut','body')
            GROUP BY organ ORDER BY exp_count DESC
        """) or []
    else:
        exp_by_organ = cache.get("experiment_by_organ", [])

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

    # ── Assemble ──
    print("\n[7/7] Assembling JSON...")
    output = {
        "generated": datetime.now(tz=timezone.utc).isoformat(),
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
