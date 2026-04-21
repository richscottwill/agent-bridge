#!/usr/bin/env python3
"""Sync the "Constraints (auto)" block at the top of each market state file.

Reads ps.market_constraints for each market, writes a compact constraints
snapshot into a comment-delimited block at the top of the state file.
Non-destructive: everything outside the <!-- WBR-OWNED:market-constraints -->
block is preserved exactly.

Targets .md state files on SharePoint OneDrive Kiro-Drive/state-files/.
Does NOT touch .docx siblings (those sync separately).

Usage: python3 update_state_file_constraints.py
Wired into: wbr-pipeline.sh step 9 (after step 8 regenerates the agent .md)

Active state files (scope limited to markets with actual state files today):
- au-paid-search-state.md → AU
- mx-paid-search-state.md → MX
- ww-testing-state.md → WW
"""
import duckdb
import os
import re
import sys
import math
import tempfile
from datetime import datetime, timezone

sys.path.insert(0, os.path.expanduser('~/shared/tools'))
from prediction.config import MOTHERDUCK_TOKEN as TOKEN

# Map: state file name → market key in ps.market_constraints
STATE_FILES = {
    'au-paid-search-state.md': 'AU',
    'mx-paid-search-state.md': 'MX',
    'ww-testing-state.md': 'WW',
}
SHAREPOINT_FOLDER = '/personal/prichwil_amazon_com/Documents/Kiro-Drive/state-files'

START_MARKER = '<!-- WBR-OWNED:market-constraints START -->'
END_MARKER = '<!-- WBR-OWNED:market-constraints END -->'

# Where to insert the block if it doesn't exist yet.
# Inserts immediately after the first closing "---" (front-matter end) followed by any
# subsequent "---" separator (the one between the SOTB header and ## Introduction).
INSERT_ANCHOR_RE = re.compile(r'(^---\s*$)', re.MULTILINE)


def _has(x):
    if x is None:
        return False
    if isinstance(x, float) and math.isnan(x):
        return False
    return True


def fmt_num(x):
    if not _has(x):
        return "—"
    return f"{int(round(x)):,}"


def fmt_money(x):
    if not _has(x):
        return "—"
    return f"${int(round(x)):,}"


def fmt_pct(x, prec=1):
    if not _has(x):
        return "—"
    return f"{x:.{prec}f}%"


def render_constraints_block(row):
    """Render a compact constraints snapshot for embedding in a state file."""
    m = dict(row._asdict()) if hasattr(row, '_asdict') else dict(row)
    market = m['market']
    now = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    
    lines = [START_MARKER, "", "### Constraints (auto-synced from ps.market_constraints)", ""]
    lines.append(f"*Last synced: {now} — source: `ps.market_constraints` view in MotherDuck. "
                 f"This block is auto-refreshed by the WBR pipeline; do not edit.*")
    lines.append("")
    lines.append(f"**Governing constraint:** {m.get('governing_constraint') or '—'}")
    lines.append(f"**Handoff status:** {m.get('handoff_status') or '—'}")
    lines.append(f"**OCI status:** {m.get('oci_status') or '—'}")
    lines.append(f"**CCP availability:** {m.get('ccp_availability') or '—'}")
    lines.append(f"**Next milestone:** {m.get('next_milestone') or '—'}")
    lines.append("")
    
    # Latest + projection
    if _has(m.get('latest_week')):
        lines.append(f"**Latest week ({m['latest_week']}):** "
                     f"{fmt_num(m.get('last_week_regs'))} regs · "
                     f"{fmt_money(m.get('last_week_cost'))} · "
                     f"CPA {fmt_money(m.get('last_week_cpa'))}")
    if _has(m.get('next_week_predicted_regs')):
        ci = ""
        if _has(m.get('next_week_ci_low_regs')) and _has(m.get('next_week_ci_high_regs')):
            ci = f" (CI {fmt_num(m['next_week_ci_low_regs'])}–{fmt_num(m['next_week_ci_high_regs'])})"
        lines.append(f"**Next-week projection:** {fmt_num(m['next_week_predicted_regs'])} regs{ci}")
    if _has(m.get('month_op2_regs')):
        lines.append(f"**Current-month OP2:** {fmt_num(m['month_op2_regs'])} regs · "
                     f"{fmt_money(m.get('month_op2_cost'))} cost · "
                     f"CPA {fmt_money(m.get('month_op2_cpa'))}")
    if _has(m.get('hit_rate_regs')):
        lines.append(f"**Forecast accuracy (regs):** {fmt_pct(m['hit_rate_regs'])} hit rate, "
                     f"{fmt_pct(m.get('avg_error_regs'))} avg error")
    lines.append("")
    
    # Regime categories
    if _has(m.get('structural_baselines')):
        lines.append(f"**Structural baselines** ({m['structural_baseline_count']}):")
        for b in m['structural_baselines'].split(' ||| '):
            lines.append(f"- {b}")
        lines.append("")
    if _has(m.get('active_impact_regimes')):
        lines.append(f"**Active impact regimes** ({m['active_impact_count']}):")
        for r in m['active_impact_regimes'].split(' ||| '):
            lines.append(f"- {r}")
        lines.append("")
    if _has(m.get('recent_past_regimes')):
        lines.append(f"**Recently ended** ({m['recent_past_count']}):")
        for r in m['recent_past_regimes'].split(' ||| '):
            lines.append(f"- {r}")
        lines.append("")
    
    lines.append(f"*For structured queries: `SELECT * FROM ps.market_constraints WHERE market = '{market}';`*")
    lines.append("")
    lines.append(END_MARKER)
    return "\n".join(lines)


def splice_block(content, new_block):
    """Replace existing block or insert after the first '---' boundary."""
    if START_MARKER in content and END_MARKER in content:
        # Replace existing block
        pattern = re.compile(
            re.escape(START_MARKER) + r'.*?' + re.escape(END_MARKER),
            re.DOTALL
        )
        return pattern.sub(new_block, content, count=1)
    
    # Insert after the first '---' boundary line (closes front-matter)
    matches = list(INSERT_ANCHOR_RE.finditer(content))
    if not matches:
        # No separator found — prepend to file as fallback
        return new_block + "\n\n" + content
    
    # State files have 3 '---' separators in the header area:
    #   1st: opens YAML front-matter
    #   2nd: closes YAML front-matter
    #   3rd: between doc H1 header and "## Introduction"
    # Insert after the 3rd (or last available) so block sits above ## Introduction.
    idx = 2 if len(matches) >= 3 else len(matches) - 1
    target_match = matches[idx]
    insert_pos = target_match.end()
    return content[:insert_pos] + "\n\n" + new_block + "\n" + content[insert_pos:]


def sync_file(filename, market, con, sharepoint_mcp_write):
    """Fetch state file from SharePoint, splice block, write back.
    
    sharepoint_mcp_write: callable that accepts (filename, content) and uploads.
    Separated so this function is testable without the MCP session.
    """
    print(f"\n[{market}] {filename}")
    row = con.execute(f"SELECT * FROM ps.market_constraints WHERE market = '{market}'").fetchone()
    cols = [d[0] for d in con.description]
    if not row:
        print(f"  ⚠️ No ps.market_constraints row for {market} — skipping")
        return False
    row_dict = dict(zip(cols, row))
    
    block = render_constraints_block(row_dict)
    
    # The actual SharePoint read/write happens via the MCP in the caller;
    # here we just prepare the transformation. Return a tuple for the caller
    # to execute via MCP.
    return ('splice', filename, market, block)


def main():
    """
    NOTE: This script prepares the constraints block and splice instructions.
    The actual SharePoint read/write is performed via the SharePoint MCP
    by the calling agent (because the MCP is a conversational tool, not a
    library import). See wbr-pipeline.sh step 9 and the pipeline prompt.
    
    For direct test runs (without MCP), pass --dry-run to see the block
    that would be spliced for each market.
    """
    dry_run = '--dry-run' in sys.argv
    
    print("Connecting to MotherDuck...")
    con = duckdb.connect(f'md:ps_analytics?motherduck_token={TOKEN}', read_only=True)
    
    print(f"Fetching constraints for {len(STATE_FILES)} state files...\n")
    
    # Output a JSON payload the agent can use to drive SharePoint MCP writes
    import json
    payload = {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'sharepoint_folder': SHAREPOINT_FOLDER,
        'files': [],
    }
    
    for filename, market in STATE_FILES.items():
        row = con.execute(f"SELECT * FROM ps.market_constraints WHERE market = '{market}'").fetchone()
        if not row:
            print(f"  ⚠️ No row for {market} — skipping {filename}")
            continue
        cols = [d[0] for d in con.description]
        row_dict = dict(zip(cols, row))
        block = render_constraints_block(row_dict)
        
        payload['files'].append({
            'filename': filename,
            'market': market,
            'sharepoint_path': f'{SHAREPOINT_FOLDER}/{filename}',
            'block': block,
            'start_marker': START_MARKER,
            'end_marker': END_MARKER,
        })
        
        if dry_run:
            print(f"\n===== {market}: {filename} =====")
            print(block)
            print()
    
    # Write payload to a known location so the hook/agent can consume it
    out_path = os.path.expanduser('~/shared/context/active/state-file-constraints-sync.json')
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, 'w') as f:
        json.dump(payload, f, indent=2)
    print(f"\n✓ Wrote sync payload to {out_path}")
    print(f"  {len(payload['files'])} state files ready to sync via SharePoint MCP")
    
    con.close()
    
    if not dry_run:
        print("\nNext step: an agent reads the payload and uses SharePoint MCP to:")
        print("  1. sharepoint_read_file (inline=true) for each filename")
        print("  2. Splice block into content (replace between markers or insert after front-matter)")
        print("  3. sharepoint_write_file to overwrite")
        print("\nSee wbr-pipeline.sh step 9 for the orchestration prompt.")


if __name__ == '__main__':
    main()
