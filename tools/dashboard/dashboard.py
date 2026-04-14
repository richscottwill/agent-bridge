"""
Richard Williams — Personal Dashboard
Run locally: streamlit run dashboard.py
Reads from git-synced shared/context/ files.
"""
import streamlit as st
import json
import re
import os
from pathlib import Path
from datetime import datetime

# --- Config ---
CONTEXT_ROOT = Path(__file__).parent.parent.parent / "context"
ACTIVE = CONTEXT_ROOT / "active"
BODY = CONTEXT_ROOT / "body"
INTAKE = CONTEXT_ROOT / "intake"

st.set_page_config(
    page_title="RW Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- Helpers ---
def read_file(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""

def read_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}

def extract_streak(amcc_text: str) -> dict:
    """Pull streak metrics from amcc.md table."""
    result = {"streak": "?", "longest": "?", "last_hard": "?", "last_avoid": "?"}
    for line in amcc_text.splitlines():
        if "| Current streak |" in line:
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 3:
                result["streak"] = parts[2]
        elif "| Longest streak |" in line:
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 3:
                result["longest"] = parts[2]
        elif "| Last hard choice |" in line:
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 3:
                result["last_hard"] = parts[2]
        elif "| Last avoidance |" in line:
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 3:
                result["last_avoid"] = parts[2]
    return result

def extract_hard_thing(amcc_text: str) -> str:
    """Pull the current hard thing from amcc.md."""
    in_table = False
    for line in amcc_text.splitlines():
        if "| The Hard Thing |" in line and "Why It's Hard" in line:
            in_table = True
            continue
        if in_table and line.startswith("|") and "---" not in line:
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 3:
                # Strip markdown bold
                return parts[1].replace("**", "")
    return "Not set"

def extract_pending_actions(current_text: str) -> list:
    """Pull unchecked pending actions from current.md."""
    actions = []
    for line in current_text.splitlines():
        line_s = line.strip()
        if line_s.startswith("- [ ]"):
            clean = line_s[5:].strip()
            # Trim to reasonable length
            if len(clean) > 120:
                clean = clean[:117] + "..."
            actions.append(clean)
    return actions

def extract_weekly_scorecard(tracker_text: str) -> dict:
    """Pull latest weekly scorecard from rw-tracker.md."""
    result = {"artifacts": "?", "tools": "?", "low_lev": "?", "meetings": "?"}
    in_scorecard = False
    for line in tracker_text.splitlines():
        if "| Category |" in line and "Target" in line:
            in_scorecard = True
            continue
        if in_scorecard and "---" in line:
            continue
        if in_scorecard and line.startswith("|"):
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 5:
                cat = parts[1].lower()
                if "artifact" in cat:
                    result["artifacts"] = f"{parts[3]} / {parts[2]}"
                elif "tool" in cat:
                    result["tools"] = f"{parts[3]} / {parts[2]}"
                elif "low-leverage" in cat or "low_lev" in cat:
                    result["low_lev"] = f"{parts[3]} / {parts[2]}"
                elif "meeting" in cat:
                    result["meetings"] = f"{parts[3]} / {parts[2]}"
        elif in_scorecard and not line.startswith("|"):
            break
    return result

def extract_latest_reconciliation(tracker_text: str) -> dict:
    """Pull the most recent EOD reconciliation block."""
    result = {"completed": "?", "carried": "?", "net": "?", "date": "?", "l1_days": "?"}
    # Find the FIRST ### block (most recent is at bottom, but we want the latest)
    blocks = []
    current_block = []
    current_header = ""
    for line in tracker_text.splitlines():
        if line.startswith("### ") and "EOD" in line:
            if current_block:
                blocks.append((current_header, "\n".join(current_block)))
            current_header = line
            current_block = []
        elif current_block is not None:
            current_block.append(line)
    if current_block and current_header:
        blocks.append((current_header, "\n".join(current_block)))

    if not blocks:
        return result

    # Use the last block (most recent)
    header, body = blocks[-1]
    result["date"] = header.replace("###", "").strip()

    for line in body.splitlines():
        if "Completed today" in line or "Completed yesterday" in line:
            m = re.search(r":\s*(\d+)", line)
            if m:
                result["completed"] = m.group(1)
        elif "Carried forward" in line:
            m = re.search(r":\s*(\d+)", line)
            if m:
                result["carried"] = m.group(1)
        elif "Net delta" in line:
            m = re.search(r":\s*(-?\d+)", line)
            if m:
                result["net"] = m.group(1)
        elif "L1:" in line:
            m = re.search(r"L1:\s*\d+\s*\((\d+)\s*workdays\)", line)
            if m:
                result["l1_days"] = m.group(1)
    return result


# --- Load Data ---
amcc_text = read_file(BODY / "amcc.md")
current_text = read_file(ACTIVE / "current.md")
tracker_text = read_file(ACTIVE / "rw-tracker.md")
snapshot = read_json(ACTIVE / "asana-morning-snapshot.json")

streak_data = extract_streak(amcc_text)
hard_thing = extract_hard_thing(amcc_text)
pending = extract_pending_actions(current_text)
scorecard = extract_weekly_scorecard(tracker_text)
recon = extract_latest_reconciliation(tracker_text)

# --- Custom CSS ---
st.markdown("""
<style>
    .block-container { padding-top: 1rem; }
    .metric-card {
        background: #1a1a2e;
        border-radius: 10px;
        padding: 1.2rem;
        text-align: center;
        border: 1px solid #333;
    }
    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: #e94560;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #888;
        margin-top: 0.3rem;
    }
    .hard-thing-box {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border-left: 4px solid #e94560;
        padding: 1rem 1.2rem;
        border-radius: 0 8px 8px 0;
        margin-bottom: 1rem;
    }
    .section-header {
        font-size: 1.1rem;
        font-weight: 600;
        color: #ccc;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
</style>
""", unsafe_allow_html=True)

# --- Header ---
col_title, col_refresh = st.columns([4, 1])
with col_title:
    st.markdown("## ⚡ RW Dashboard")
with col_refresh:
    st.markdown(f"<div style='text-align:right; color:#666; padding-top:0.8rem;'>Last sync: {snapshot.get('generated_at', 'unknown')[:16]}</div>", unsafe_allow_html=True)

# --- Row 1: Key Metrics ---
st.markdown('<div class="section-header">Pulse</div>', unsafe_allow_html=True)
c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    st.metric("🔥 Streak", streak_data["streak"])
with c2:
    st.metric("📋 Tasks", snapshot.get("total_incomplete", "?"))
with c3:
    st.metric("🚨 Overdue 3d+", snapshot.get("overdue_3plus", "?"))
with c4:
    st.metric("📅 Today", snapshot.get("today_tasks", "?"))
with c5:
    st.metric("🆕 New (24h)", snapshot.get("new_since_yesterday", "?"))

# --- Row 2: Hard Thing + Scorecard ---
left, right = st.columns([3, 2])

with left:
    st.markdown('<div class="section-header">The Hard Thing</div>', unsafe_allow_html=True)
    st.markdown(f"""<div class="hard-thing-box">
        <span style="font-size:1.15rem; font-weight:600; color:#e94560;">{hard_thing}</span><br>
        <span style="color:#888; font-size:0.85rem;">Last hard choice: {streak_data['last_hard']} · Last avoidance: {streak_data['last_avoid']}</span>
    </div>""", unsafe_allow_html=True)

    # Latest reconciliation
    st.markdown('<div class="section-header">Latest Reconciliation</div>', unsafe_allow_html=True)
    st.markdown(f"**{recon['date']}**")
    rc1, rc2, rc3, rc4 = st.columns(4)
    rc1.metric("Completed", recon["completed"])
    rc2.metric("Carried", recon["carried"])
    rc3.metric("Net Δ", recon["net"])
    rc4.metric("L1 Drought", f"{recon['l1_days']}d")

with right:
    st.markdown('<div class="section-header">Weekly Scorecard</div>', unsafe_allow_html=True)
    st.markdown(f"""
    | Metric | Actual / Target |
    |--------|----------------|
    | Artifacts shipped | {scorecard['artifacts']} |
    | Tools built | {scorecard['tools']} |
    | Low-leverage hours | {scorecard['low_lev']} |
    | Meetings w/ output | {scorecard['meetings']} |
    """)

# --- Row 3: Routine Buckets + Projects ---
st.markdown("---")
b_left, b_right = st.columns(2)

with b_left:
    st.markdown('<div class="section-header">Tasks by Routine</div>', unsafe_allow_html=True)
    by_routine = snapshot.get("by_routine", {})
    if by_routine:
        import pandas as pd
        df_routine = pd.DataFrame(
            list(by_routine.items()),
            columns=["Routine", "Count"]
        ).sort_values("Count", ascending=True)
        st.bar_chart(df_routine.set_index("Routine"), horizontal=True)

    # Over-cap alerts
    over_cap = snapshot.get("over_cap", [])
    if over_cap:
        st.warning(f"⚠️ Over cap: {', '.join(over_cap)}")

with b_right:
    st.markdown('<div class="section-header">Tasks by Project</div>', unsafe_allow_html=True)
    by_project = snapshot.get("by_project", {})
    if by_project:
        import pandas as pd
        df_proj = pd.DataFrame(
            list(by_project.items()),
            columns=["Project", "Count"]
        ).sort_values("Count", ascending=True)
        st.bar_chart(df_proj.set_index("Project"), horizontal=True)

# --- Row 4: Pending Actions ---
st.markdown("---")
st.markdown('<div class="section-header">Pending Actions (from current.md)</div>', unsafe_allow_html=True)

if pending:
    # Show top 15, with priority markers
    for i, action in enumerate(pending[:15]):
        icon = "🚨" if any(w in action.lower() for w in ["overdue", "urgent", "immediate"]) else "📌"
        st.markdown(f"{icon} {action}")
    if len(pending) > 15:
        st.caption(f"... and {len(pending) - 15} more")
else:
    st.success("No pending actions found.")

# --- Footer ---
st.markdown("---")
st.caption(f"Dashboard reads from git-synced shared/context/ files. Total pending: {len(pending)}. Snapshot: {snapshot.get('generated_at', 'N/A')[:10]}.")
