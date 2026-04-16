#!/usr/bin/env python3
"""
generate-command-center.py — Build command-center-data.json for the Command Center dashboard.

Data sources (in priority order):
  1. DuckDB (MotherDuck: ps_analytics) — canonical task state by block, overdue tasks
  2. AM-auto output files — slack signals, email triage, enrichment proposals
  3. Intake digests — slack-digest.md, email-triage.md

Output: shared/dashboards/data/command-center-data.json
"""
import json, os, re, subprocess
from pathlib import Path
from datetime import datetime, timezone, date

HOME = Path.home()
ACTIVE = HOME / "shared/context/active"
INTAKE = HOME / "shared/context/intake"
OUTPUT = HOME / "shared/dashboards/data/command-center-data.json"

BLOCKS = [
    {"name": "Sweep", "emoji": "🧹", "cap": 5, "desc": "Quick unblocking", "routine_match": "Sweep"},
    {"name": "Admin", "emoji": "📋", "cap": 3, "desc": "30 min bound", "routine_match": "Admin"},
    {"name": "Core", "emoji": "🎯", "cap": 4, "desc": "Strategic work", "routine_match": "Core"},
    {"name": "Engine Room", "emoji": "⚙️", "cap": 6, "desc": "Hands-on execution", "routine_match": "Engine Room"},
]


def _get_motherduck_token():
    """Extract MotherDuck token from env or Kiro MCP config."""
    token = os.environ.get("MOTHERDUCK_TOKEN") or os.environ.get("motherduck_token")
    if token:
        return token
    # Try reading from Kiro MCP config
    for cfg_path in [
        Path.home() / ".kiro/settings/mcp.json",
        Path("../../.kiro/settings/mcp.json"),
    ]:
        try:
            cfg = json.loads(cfg_path.read_text())
            env = cfg.get("mcpServers", {}).get("duckdb", {}).get("env", {})
            t = env.get("motherduck_token") or env.get("MOTHERDUCK_TOKEN")
            if t:
                return t
        except Exception:
            pass
    return None


def query_duckdb(sql):
    """Query MotherDuck via duckdb Python package, with token auto-discovery from MCP config."""
    token = _get_motherduck_token()
    # Try Python package (use fetchall to avoid numpy dependency)
    try:
        import duckdb as ddb
        if token:
            con = ddb.connect(f"md:ps_analytics?motherduck_token={token}")
        else:
            con = ddb.connect("md:ps_analytics")
        result = con.execute(sql)
        columns = [desc[0] for desc in result.description]
        rows = result.fetchall()
        return [dict(zip(columns, row)) for row in rows]
    except Exception as e:
        print(f"DuckDB Python failed: {e}")
    # Fallback to CLI with token in env
    try:
        env = os.environ.copy()
        if token:
            env["motherduck_token"] = token
        result = subprocess.run(
            ["duckdb", "md:ps_analytics", "-json", "-c", sql],
            capture_output=True, text=True, timeout=30, env=env
        )
        if result.returncode == 0 and result.stdout.strip():
            return json.loads(result.stdout.strip())
    except Exception as e:
        print(f"DuckDB CLI failed: {e}")
    return []


def get_tasks_by_block():
    """Get all incomplete tasks grouped by Routine_RW block from DuckDB."""
    rows = query_duckdb("""
        SELECT task_gid, name, routine_rw, priority_rw, due_on, project_name,
            CASE WHEN due_on IS NOT NULL AND due_on < CURRENT_DATE
                 THEN DATEDIFF('day', due_on, CURRENT_DATE) ELSE 0 END as days_overdue,
            kiro_rw, next_action_rw
        FROM asana.asana_tasks
        WHERE completed = FALSE AND deleted_at IS NULL AND routine_rw IS NOT NULL
        ORDER BY routine_rw, priority_rw, due_on ASC NULLS LAST
    """)
    return rows


def get_overdue_tasks():
    """Get overdue tasks from DuckDB."""
    rows = query_duckdb("""
        SELECT task_gid, name, project_name, due_on, routine_rw, priority_rw, days_overdue
        FROM asana.overdue
        ORDER BY days_overdue DESC
        LIMIT 15
    """)
    return rows


def get_today_tasks():
    """Get tasks with Priority_RW = Today."""
    rows = query_duckdb("""
        SELECT task_gid, name, routine_rw, priority_rw, due_on, project_name,
            CASE WHEN due_on IS NOT NULL AND due_on < CURRENT_DATE
                 THEN DATEDIFF('day', due_on, CURRENT_DATE) ELSE 0 END as days_overdue,
            kiro_rw, next_action_rw
        FROM asana.asana_tasks
        WHERE priority_rw = 'Today' AND completed = FALSE AND deleted_at IS NULL
        ORDER BY routine_rw, due_on ASC NULLS LAST
    """)
    return rows


def get_pacing():
    """Get monthly pacing data."""
    rows = query_duckdb("""
        SELECT market, pacing_regs_pct, pacing_cost_pct, mtd_regs, op2_regs_target
        FROM ps.monthly_pacing
        ORDER BY pacing_regs_pct DESC
    """)
    return rows


def load_json(path):
    if path.exists():
        try:
            return json.loads(path.read_text())
        except:
            pass
    return None


def parse_slack_signals(path):
    """Extract high-priority actionable signals from slack digest."""
    signals = []
    if not path.exists():
        return signals
    text = path.read_text()
    in_high = False
    for line in text.split("\n"):
        if "## High Priority" in line:
            in_high = True
            continue
        if line.startswith("## ") and in_high:
            in_high = False
            continue
        if in_high and line.strip().startswith("- "):
            signals.append(line.strip()[2:].strip()[:200])
    # Also grab hot topics
    in_hot = False
    for line in text.split("\n"):
        if "## Hot Topics" in line:
            in_hot = True
            continue
        if line.startswith("## ") and in_hot:
            break
        if in_hot and line.strip().startswith("|") and "CRITICAL" in line:
            signals.append("🔴 " + line.strip()[:200])
    return signals[:12]


def parse_email_high(path):
    """Extract high-priority emails from email triage."""
    emails = []
    if not path.exists():
        return emails
    text = path.read_text()
    in_high = False
    for line in text.split("\n"):
        if "## High Priority" in line:
            in_high = True
            continue
        if line.startswith("## ") and in_high:
            in_high = False
            continue
        if in_high and line.strip().startswith("- "):
            emails.append(line.strip()[2:].strip()[:200])
    return emails[:10]


def parse_enrichment_queue(data):
    """Extract enrichment proposals and admin routing from AM-Backend output."""
    proposals = []
    if not data:
        return proposals
    for item in data.get("enrichment_proposals", []):
        proposals.append({
            "name": item.get("name", ""),
            "proposal": item.get("proposal", ""),
            "reason": item.get("reason", ""),
        })
    return proposals


def parse_signals_processed(data):
    """Extract critical flags and new tasks from signal processing."""
    if not data:
        return {"tasks_created": [], "critical_flags": []}
    return {
        "tasks_created": data.get("tasks_created", []),
        "critical_flags": data.get("critical_flags", []),
    }


def enrich_intel_with_status(items, key_field="text"):
    """Add status field to intel items based on heuristics.
    
    Status values: not_started, in_progress, done
    Heuristics:
    - If item has 'done' or 'completed' in context → done
    - If item has days_old > 0 and overdue → not_started (stale)
    - Default → not_started
    
    Also enriches done items with completion context:
    - completed_via: how the promise was fulfilled (Slack DM, email, doc shared, etc.)
    - completed_message: what was communicated when closing the loop
    
    Future: pull status from Asana custom field or manual tag.
    """
    for item in items:
        if not item.get("status"):
            ctx = (item.get("context") or "").lower()
            if "done" in ctx or "completed" in ctx or "shipped" in ctx or "sent" in ctx:
                item["status"] = "done"
            elif "in progress" in ctx or "in development" in ctx or "drafted" in ctx or "started" in ctx:
                item["status"] = "in_progress"
            else:
                item["status"] = "not_started"
        
        # Enrich done items with completion context if not already set
        if item.get("status") == "done" and not item.get("completed_via"):
            ctx = (item.get("context") or "").lower()
            if "slack" in ctx or "dm" in ctx:
                item["completed_via"] = "Slack message"
            elif "email" in ctx:
                item["completed_via"] = "Email"
            elif "doc" in ctx or "quip" in ctx or "wiki" in ctx:
                item["completed_via"] = "Document shared"
            elif "asana" in ctx or "task" in ctx:
                item["completed_via"] = "Asana task update"
            elif "meeting" in ctx or "call" in ctx:
                item["completed_via"] = "Discussed in meeting"
            else:
                item["completed_via"] = "Completed (channel unknown)"
    return items


def main():
    print("Querying DuckDB for task state...")

    # ── DuckDB: canonical task data ──
    all_tasks = get_tasks_by_block()
    overdue = get_overdue_tasks()
    today_tasks = get_today_tasks()
    pacing = get_pacing()

    # ── Build block summary from DuckDB ──
    blocks = []
    for b in BLOCKS:
        match = b["routine_match"].lower()
        tasks = [t for t in all_tasks if match in (t.get("routine_rw") or "").lower()]
        today_in_block = [t for t in tasks if t.get("priority_rw") == "Today"]
        overdue_in_block = [t for t in tasks if t.get("days_overdue", 0) > 0]

        task_list = []
        for t in tasks[:15]:
            task_list.append({
                "name": t.get("name", ""),
                "due": t.get("due_on", ""),
                "overdue": t.get("days_overdue", 0) > 0,
                "days_overdue": t.get("days_overdue", 0),
                "priority": t.get("priority_rw", ""),
                "project": t.get("project_name", ""),
                "next_action": t.get("next_action_rw", ""),
                "kiro": t.get("kiro_rw", ""),
            })

        blocks.append({
            "name": b["name"],
            "emoji": b["emoji"],
            "cap": b["cap"],
            "desc": b["desc"],
            "count": len(tasks),
            "today_count": len(today_in_block),
            "overdue_count": len(overdue_in_block),
            "tasks": task_list,
            "over_cap": len(tasks) > b["cap"],
        })

    # ── Overdue tasks from DuckDB ──
    overdue_list = []
    for t in overdue:
        overdue_list.append({
            "name": t.get("name", ""),
            "days_overdue": t.get("days_overdue", 0),
            "project": t.get("project_name", ""),
            "routine": t.get("routine_rw", ""),
            "priority": t.get("priority_rw", ""),
            "due": t.get("due_on", ""),
        })

    # ── Today tasks (ordered by block sequence) ──
    block_order = {"Sweep": 0, "Admin": 1, "Core": 2, "Engine Room": 3}
    today_list = []
    for t in today_tasks:
        routine = t.get("routine_rw", "") or ""
        order = 4
        for k, v in block_order.items():
            if k.lower() in routine.lower():
                order = v
                break
        today_list.append({
            "name": t.get("name", ""),
            "due": t.get("due_on", ""),
            "overdue": t.get("days_overdue", 0) > 0,
            "days_overdue": t.get("days_overdue", 0),
            "routine": routine,
            "project": t.get("project_name", ""),
            "next_action": t.get("next_action_rw", ""),
            "block_order": order,
        })
    today_list.sort(key=lambda x: (x["block_order"], -(x.get("days_overdue") or 0)))

    # ── Pacing data ──
    pacing_list = []
    for p in pacing:
        pacing_list.append({
            "market": p.get("market", ""),
            "pacing_regs_pct": p.get("pacing_regs_pct"),
            "pacing_cost_pct": p.get("pacing_cost_pct"),
            "mtd_regs": p.get("mtd_regs"),
            "op2_target": p.get("op2_regs_target"),
        })

    # ── AM-auto output files ──
    enrichment = load_json(ACTIVE / "am-enrichment-queue.json")
    signals = load_json(ACTIVE / "am-signals-processed.json")
    slack = parse_slack_signals(INTAKE / "slack-digest.md")
    emails = parse_email_high(INTAKE / "email-triage.md")
    enrichment_proposals = parse_enrichment_queue(enrichment)
    signal_data = parse_signals_processed(signals)

    # ── Load intel sections from AM-auto output ──
    am_intel = load_json(ACTIVE / "am-command-center-intel.json") or {}
    commitments = enrich_intel_with_status(am_intel.get("commitments", []), "text")
    delegate_items = am_intel.get("delegate", [])
    communicate_items = am_intel.get("communicate", [])
    differentiate_items = enrich_intel_with_status(am_intel.get("differentiate", []), "action")

    # ── Assemble output ──
    output = {
        "generated": datetime.now(tz=timezone.utc).isoformat(),
        "blocks": blocks,
        "today_tasks": today_list,
        "overdue_tasks": overdue_list,
        "pacing": pacing_list,
        "actionable_emails": emails,
        "slack_signals": slack,
        "critical_flags": signal_data.get("critical_flags", []),
        "tasks_created_today": signal_data.get("tasks_created", []),
        "enrichment_proposals": enrichment_proposals[:10],
        "commitments": commitments,
        "delegate": delegate_items,
        "communicate": communicate_items,
        "differentiate": differentiate_items,
        "total_overdue": len(overdue_list),
        "total_today": len(today_list),
        "total_signals": len(slack),
        "total_emails": len(emails),
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(output, indent=2, default=str))
    print(f"Written {OUTPUT}")
    print(f"Blocks: {', '.join(f'{b['name']}={b['count']}/{b['cap']}' for b in blocks)}")
    print(f"Today: {len(today_list)}, Overdue: {len(overdue_list)}, Emails: {len(emails)}, Slack: {len(slack)}")


if __name__ == "__main__":
    main()
