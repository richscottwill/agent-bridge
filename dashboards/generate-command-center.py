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


def apply_ledger_actions():
    """Apply pending ledger actions from the dashboard.
    
    Reads from shared/dashboards/data/ledger-actions.json (written by export script
    or manually from localStorage). Applies status changes to DuckDB and writes
    a feedback queue for AM-Auto to cascade to Asana and other systems.
    """
    actions_path = HOME / "shared/dashboards/data/ledger-actions.json"
    feedback_path = ACTIVE / "ledger-feedback-queue.json"
    
    if not actions_path.exists():
        return
    try:
        data = json.loads(actions_path.read_text())
        actions = data.get("actions", [])
        if not actions:
            return
        
        today = date.today().isoformat()
        feedback_items = []
        
        for a in actions:
            text_hash = a.get("text_hash", "")
            status = a.get("status", "")
            note = a.get("note", "")
            if not text_hash or not status:
                continue
            safe_hash = text_hash.replace("'", "''")
            safe_note = note.replace("'", "''")
            
            # Update DuckDB
            if status == "done":
                query_duckdb(f"UPDATE main.commitment_ledger SET status='done', completed_date='{today}', dismissed_date=NULL, completed_message='{safe_note}' WHERE text_hash='{safe_hash}'")
            elif status == "dismissed":
                query_duckdb(f"UPDATE main.commitment_ledger SET status='dismissed', dismissed_date='{today}', completed_date=NULL, completed_message='{safe_note}' WHERE text_hash='{safe_hash}'")
            elif status == "not_started":
                query_duckdb(f"UPDATE main.commitment_ledger SET status='not_started', completed_date=NULL, dismissed_date=NULL, completed_message=NULL WHERE text_hash='{safe_hash}'")
            
            # Queue for AM-Auto cascade
            feedback_items.append({
                "text_hash": text_hash,
                "text": a.get("text", ""),
                "status": status,
                "note": note,
                "timestamp": a.get("timestamp", ""),
                "tags": a.get("tags", []),
                "source": a.get("source", ""),
                "person": a.get("person", ""),
                "cascade_actions": build_cascade_actions(a),
            })
        
        print(f"Applied {len(actions)} ledger actions to DuckDB")
        
        # Write feedback queue for AM-Auto to process
        existing_feedback = {}
        if feedback_path.exists():
            try:
                existing_feedback = json.loads(feedback_path.read_text())
            except:
                pass
        
        pending = existing_feedback.get("pending", [])
        # Merge — dedup by text_hash, newer wins
        existing_hashes = {p["text_hash"] for p in pending}
        for fi in feedback_items:
            if fi["text_hash"] not in existing_hashes:
                pending.append(fi)
            else:
                # Replace with newer
                pending = [p if p["text_hash"] != fi["text_hash"] else fi for p in pending]
        
        feedback_path.write_text(json.dumps({
            "generated": datetime.now(tz=timezone.utc).isoformat(),
            "pending": pending,
        }, indent=2, default=str))
        print(f"Wrote {len(pending)} items to feedback queue for AM-Auto cascade")
        
        # Clear the actions file
        actions_path.write_text(json.dumps({"actions": []}, indent=2))
    except Exception as e:
        print(f"Failed to apply ledger actions: {e}")


def build_cascade_actions(action):
    """Determine what downstream systems need updating based on the action.
    
    Returns a list of cascade instructions for AM-Auto to execute.
    """
    cascades = []
    status = action.get("status", "")
    text = action.get("text", "")
    note = action.get("note", "")
    source = action.get("source", "")
    
    if status == "done":
        # If source is Asana, mark the linked task complete
        if "asana" in source.lower():
            cascades.append({
                "system": "asana",
                "action": "complete_task",
                "search_text": text,
                "comment": f"Marked done from Command Center. {note}".strip(),
            })
        # If source is Slack, suggest a reply
        if "slack" in source.lower():
            cascades.append({
                "system": "slack",
                "action": "suggest_reply",
                "search_text": text,
                "note": note,
            })
    elif status == "dismissed":
        # If source is Asana, add a comment explaining dismissal
        if "asana" in source.lower():
            cascades.append({
                "system": "asana",
                "action": "add_comment",
                "search_text": text,
                "comment": f"Dismissed from Command Center. Reason: {note or 'No longer applicable'}",
            })
    
    return cascades


def sync_commitments_to_duckdb(intel_commitments):
    """Sync commitments from AM-auto intel to DuckDB commitment_ledger.
    
    - UPSERT new commitments (text-hash dedup)
    - Update days_old / overdue / context for existing ones
    - Prune entries older than 30 days (unless still active)
    - Read back ALL non-pruned entries as the canonical list
    """
    import hashlib
    today = date.today().isoformat()

    # 1. Upsert each intel commitment into DuckDB
    for c in intel_commitments:
        text = c.get("text", "")
        if not text:
            continue
        text_hash = hashlib.md5(text.encode()).hexdigest()
        source = (c.get("source") or "").replace("'", "''")
        person = (c.get("person") or "").replace("'", "''")
        said_by = c.get("said_by") or ""
        context = (c.get("context") or "").replace("'", "''")
        quote = (c.get("quote") or "").replace("'", "''")
        days_old = c.get("days_old", 0)
        overdue = "TRUE" if c.get("overdue") else "FALSE"
        status = c.get("status") or "not_started"
        safe_text = text.replace("'", "''")

        # INSERT OR REPLACE — preserves status if already set to done/dismissed by user
        query_duckdb(f"""
            INSERT INTO main.commitment_ledger (text_hash, text, source, person, said_by, status, context, quote, days_old, overdue, first_seen, last_seen)
            VALUES ('{text_hash}', '{safe_text}', '{source}', '{person}', '{said_by}', '{status}', '{context}', '{quote}', {days_old}, {overdue}, '{today}', '{today}')
            ON CONFLICT (text_hash) DO UPDATE SET
                days_old = EXCLUDED.days_old,
                overdue = EXCLUDED.overdue,
                context = CASE WHEN EXCLUDED.context != '' THEN EXCLUDED.context ELSE commitment_ledger.context END,
                last_seen = '{today}',
                -- Don't overwrite user-set status (done/dismissed) with not_started
                status = CASE
                    WHEN commitment_ledger.status IN ('done', 'dismissed') THEN commitment_ledger.status
                    ELSE EXCLUDED.status
                END
        """)

    # 2. Prune entries older than 30 days that are done or dismissed
    query_duckdb(f"""
        DELETE FROM main.commitment_ledger
        WHERE last_seen < CURRENT_DATE - INTERVAL 30 DAY
          AND status IN ('done', 'dismissed')
    """)

    # 3. Read back all commitments (canonical source)
    rows = query_duckdb("""
        SELECT text_hash, text, source, person, said_by, status, context, quote,
               days_old, overdue, first_seen, last_seen, completed_date, dismissed_date,
               completed_via, completed_message
        FROM main.commitment_ledger
        ORDER BY
            CASE status WHEN 'not_started' THEN 0 WHEN 'in_progress' THEN 1 WHEN 'done' THEN 2 WHEN 'dismissed' THEN 3 END,
            days_old DESC
    """)

    commitments = []
    for r in rows:
        commitments.append({
            "text_hash": r.get("text_hash", ""),
            "text": r.get("text", ""),
            "source": r.get("source", ""),
            "person": r.get("person", ""),
            "said_by": r.get("said_by", ""),
            "status": r.get("status", "not_started"),
            "context": r.get("context", ""),
            "quote": r.get("quote", ""),
            "days_old": r.get("days_old", 0),
            "overdue": bool(r.get("overdue", False)),
            "first_seen": str(r.get("first_seen", "")),
            "last_seen": str(r.get("last_seen", "")),
            "completed_date": str(r.get("completed_date", "") or ""),
            "dismissed_date": str(r.get("dismissed_date", "") or ""),
            "completed_via": r.get("completed_via", ""),
            "completed_message": r.get("completed_message", ""),
        })

    print(f"Commitments: {len(commitments)} total ({sum(1 for c in commitments if c['status']=='not_started')} active, {sum(1 for c in commitments if c['status']=='done')} done, {sum(1 for c in commitments if c['status']=='dismissed')} dismissed)")
    return commitments


def get_wbr_health_score():
    """Compute WBR Health Score from callout reviewer scores in DuckDB.

    The callout reviewer scores each market on 8 dimensions (0-10 each):
      L1 Craft: attribution, structure, voice, economy
      L2 Impact: sowhat, ownership, accuracy, strategic

    The composite WBR Health Score is the average of all 8 dimensions × 10,
    producing a single 0-100 number. Equal weights — all dimensions matter.

    Returns the current week's score, last week's score (for trend arrow),
    and the per-dimension breakdown.
    """
    # Get the two most recent weeks of scores
    rows = query_duckdb("""
        SELECT iso_week,
            ROUND(AVG(l1_attribution), 2) as avg_attribution,
            ROUND(AVG(l1_structure), 2) as avg_structure,
            ROUND(AVG(l1_voice), 2) as avg_voice,
            ROUND(AVG(l1_economy), 2) as avg_economy,
            ROUND(AVG(l2_sowhat), 2) as avg_sowhat,
            ROUND(AVG(l2_ownership), 2) as avg_ownership,
            ROUND(AVG(l2_accuracy), 2) as avg_accuracy,
            ROUND(AVG(l2_strategic), 2) as avg_strategic,
            ROUND(AVG(combined_avg), 4) as avg_combined,
            COUNT(*) as market_count
        FROM ps.callout_scores
        GROUP BY iso_week
        ORDER BY iso_week DESC
        LIMIT 2
    """)

    if not rows:
        return None

    current = rows[0]
    previous = rows[1] if len(rows) > 1 else None

    # Composite score: average of 8 dimensions × 10 → 0-100 scale
    composite = round(current["avg_combined"] * 10, 1)
    l1_avg = round((current["avg_attribution"] + current["avg_structure"] +
                     current["avg_voice"] + current["avg_economy"]) / 4, 2)
    l2_avg = round((current["avg_sowhat"] + current["avg_ownership"] +
                     current["avg_accuracy"] + current["avg_strategic"]) / 4, 2)

    # Trend vs last week
    prev_composite = round(previous["avg_combined"] * 10, 1) if previous else None
    if prev_composite is not None:
        delta = round(composite - prev_composite, 1)
        if delta > 0.5:
            trend = "up"
        elif delta < -0.5:
            trend = "down"
        else:
            trend = "flat"
    else:
        delta = None
        trend = "flat"

    result = {
        "composite_score": composite,
        "week": current["iso_week"],
        "market_count": current["market_count"],
        "l1_avg": l1_avg,
        "l2_avg": l2_avg,
        "trend": trend,
        "delta": delta,
        "prev_score": prev_composite,
        "prev_week": previous["iso_week"] if previous else None,
        "dimensions": {
            "attribution": current["avg_attribution"],
            "structure": current["avg_structure"],
            "voice": current["avg_voice"],
            "economy": current["avg_economy"],
            "sowhat": current["avg_sowhat"],
            "ownership": current["avg_ownership"],
            "accuracy": current["avg_accuracy"],
            "strategic": current["avg_strategic"],
        },
    }

    # Persist to ps.wbr_health_score for trend queries
    dim_json = json.dumps(result["dimensions"])
    safe_dim = dim_json.replace("'", "''")
    query_duckdb(f"""
        INSERT INTO ps.wbr_health_score (iso_week, composite_score, l1_avg, l2_avg, market_count, dimension_scores, computed_at)
        VALUES ('{current["iso_week"]}', {composite}, {l1_avg}, {l2_avg}, {current["market_count"]}, '{safe_dim}', CURRENT_TIMESTAMP)
        ON CONFLICT (iso_week) DO UPDATE SET
            composite_score = EXCLUDED.composite_score,
            l1_avg = EXCLUDED.l1_avg,
            l2_avg = EXCLUDED.l2_avg,
            market_count = EXCLUDED.market_count,
            dimension_scores = EXCLUDED.dimension_scores,
            computed_at = EXCLUDED.computed_at
    """)

    print(f"WBR Health Score: {composite}/100 ({trend}, Δ{delta}) — {current['iso_week']}, {current['market_count']} markets")
    return result


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

    # ── WBR Health Score (composite from callout reviewer scores) ──
    wbr_health = get_wbr_health_score()

    # ── AM-auto output files ──
    enrichment = load_json(ACTIVE / "am-enrichment-queue.json")
    signals = load_json(ACTIVE / "am-signals-processed.json")
    slack = parse_slack_signals(INTAKE / "slack-digest.md")
    emails = parse_email_high(INTAKE / "email-triage.md")
    enrichment_proposals = parse_enrichment_queue(enrichment)
    signal_data = parse_signals_processed(signals)

    # ── Load intel sections from AM-auto output ──
    am_intel = load_json(ACTIVE / "am-command-center-intel.json") or {}
    delegate_items = am_intel.get("delegate", [])
    communicate_items = am_intel.get("communicate", [])
    differentiate_items = enrich_intel_with_status(am_intel.get("differentiate", []), "action")

    # ── Commitments: DuckDB is canonical (30-day rolling, text-hash dedup) ──
    # First, apply any pending user actions from the dashboard
    apply_ledger_actions()
    commitments = sync_commitments_to_duckdb(am_intel.get("commitments", []))

    # ── Assemble output ──
    output = {
        "generated": datetime.now(tz=timezone.utc).isoformat(),
        "wbr_health": wbr_health,
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
