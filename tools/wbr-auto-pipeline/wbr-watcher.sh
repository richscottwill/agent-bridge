#!/bin/bash
# WBR Dashboard Watcher — polls OneDrive every 30 mins for new dashboard xlsx.
# When found: checks context freshness, ingests change log, ingests dashboard,
# runs projection accuracy check, runs callout pipeline, Slacks Richard.
# Usage: bash ~/shared/tools/wbr-auto-pipeline/wbr-watcher.sh
# Stop: kill the process or Ctrl+C

POLL_INTERVAL=1800  # 30 minutes in seconds
CONFIG="$HOME/shared/tools/wbr-auto-pipeline/config.json"
LOG="$HOME/shared/tools/wbr-auto-pipeline/watcher.log"
KIRO_CLI="/agentspaces/kiro-cli/kiro-cli"
CHANGE_LOG_SHEET="1YUpRrtiBSpbWkwz_8hYcushXnXBt1WuoNR36UnGqAkU"

echo "$(date -Iseconds) WBR watcher started. Polling every ${POLL_INTERVAL}s (Mondays only, 6am-6pm PT)." | tee -a "$LOG"

while true; do
  # Only poll on Mondays between 6am-6pm PT (UTC-7 = 13:00-01:00 UTC)
  DAY_OF_WEEK=$(date -u +%u)  # 1=Monday
  HOUR_UTC=$(date -u +%H)
  
  IS_MONDAY_WINDOW=false
  if [ "$DAY_OF_WEEK" = "1" ] && [ "$HOUR_UTC" -ge 13 ]; then
    IS_MONDAY_WINDOW=true
  elif [ "$DAY_OF_WEEK" = "2" ] && [ "$HOUR_UTC" -lt 1 ]; then
    IS_MONDAY_WINDOW=true
  fi

  if [ "$IS_MONDAY_WINDOW" = "false" ]; then
    sleep 3600
    continue
  fi

  echo "$(date -Iseconds) Polling for new dashboard..." | tee -a "$LOG"

  LAST_PROCESSED=$(python3 -c "
import json, os
cfg = '$CONFIG'
if os.path.exists(cfg):
    with open(cfg) as f:
        c = json.load(f)
    print(c.get('last_processed_file', ''))
else:
    print('')
" 2>/dev/null)

  # Full pipeline in one kiro-cli call
  $KIRO_CLI chat --no-interactive --trust-all-tools \
    "WBR auto-pipeline. Execute these steps in order. Stop on critical failure, continue on non-critical.

=== STEP 1: CHECK FOR NEW DASHBOARD ===
Use sharepoint_search with query '\"AB SEM WW Dashboard\" FileType:xlsx' rowLimit 3.
Find the file with the highest week number (W14 > W13 etc). Note its Name and Path.
Last processed: '${LAST_PROCESSED:-none}'.
If the latest file name matches last processed, say 'NO_NEW_FILE' and STOP — no further steps.

=== STEP 2: MARKET CONTEXT FRESHNESS CHECK ===
Check modification dates of all 10 market context files:
  ~/shared/context/active/callouts/{au,mx,us,ca,jp,uk,de,fr,it,es}/*-context.md
For each, check if last modified > 14 days ago. Flag stale ones.
This is non-critical — log stale markets but continue.

=== STEP 3: READ PRE-WBR CALLOUTS QUIP (DEDUP CHECK) ===
Read the Pre-WBR Callouts Quip document via Builder MCP:
  ReadInternalWebsites(url='https://quip-amazon.com/MMgBAzDrlVou')
Parse the response to identify which weeks already have callouts posted.
Look for 'Wk[NN] Callouts' headers — if the current week W[NN] already has content
in the Paid Search row (row 10, column B or WW column), note it as 'already_posted'.
This tells the callout writer what context already exists and avoids duplicate analysis.
Store the parsed week numbers and any existing Paid Search callout text for reference.
IMPORTANT: This is READ-ONLY. Do NOT write to Quip. Richard posts manually.
Update quip_registry last_read_at:
  python3 -c \"import duckdb; con=duckdb.connect('/home/prichwil/shared/data/duckdb/ps-analytics.duckdb'); con.execute(\\\"UPDATE quip_registry SET last_read_at=CURRENT_TIMESTAMP WHERE doc_name='Pre-WBR Callouts'\\\"); con.close()\"
Non-critical — if Quip read fails, log and continue without dedup context.

=== STEP 4: CHANGE LOG INGESTION ===
Download the change log from Google Sheets (ID: $CHANGE_LOG_SHEET).
The sheet has 4 tabs. Export each as CSV using these URLs:
  Tab 1 (MX/AU): https://docs.google.com/spreadsheets/d/$CHANGE_LOG_SHEET/export?format=csv&gid=1407602397
  Tab 2 (EU5): https://docs.google.com/spreadsheets/d/$CHANGE_LOG_SHEET/export?format=csv&gid=238419350
  Tab 3 (NA/JP): https://docs.google.com/spreadsheets/d/$CHANGE_LOG_SHEET/export?format=csv&gid=1176759484
  Tab 4 (Partnership): https://docs.google.com/spreadsheets/d/$CHANGE_LOG_SHEET/export?format=csv&gid=1994107761
Save each CSV to ~/shared/tools/dashboard-ingester/input/change-log-{mx_au,eu5,na_jp,partnership}.csv
Ingest all to DuckDB change_log table via:
  python3 -c \"import duckdb; con=duckdb.connect('/home/prichwil/shared/data/duckdb/ps-analytics.duckdb'); con.execute(\\\"INSERT INTO change_log SELECT * FROM read_csv_auto('[csv_path]')\\\"); con.close()\"
Additionally, read the MX Sync Quip doc for campaign change context:
  ReadInternalWebsites(url='https://quip-amazon.com/K9OYA9mXm7DU')
Extract any recent campaign changes mentioned and pass them to the callout writer as context.
Non-critical — if this fails, log and continue.

=== STEP 5: PROJECTION ACCURACY CHECK ===
For each market with a projections file (~/shared/context/active/callouts/*/[market]-projections.md):
  Read last week's projected regs and spend.
  Compare against this week's actuals from the new dashboard data briefs.
  Compute accuracy: actual/projected for regs and spend.
  Append one line to each projections file: 'W[N-1] accuracy: regs [X]% of projected, spend [X]% of projected.'
Non-critical — if projections files don't have last week's numbers, skip.

=== STEP 6: DOWNLOAD NEW DASHBOARD ===
Use sharepoint_read_file with the serverRelativeUrl from Step 1.
Save to: ~/shared/tools/dashboard-ingester/input/[filename]
Confirm file exists on disk. CRITICAL — stop if download fails.

=== STEP 7: INGEST DASHBOARD ===
Run: python3 ~/shared/tools/dashboard-ingester/ingest.py ~/shared/tools/dashboard-ingester/input/[filename]
CRITICAL — stop if ingestion fails.

=== STEP 8: UPDATE CONFIG ===
python3 -c \"import json; c=json.load(open('$CONFIG')); c['last_processed_file']='[filename]'; c['last_processed_date']='$(date -Iseconds)'; json.dump(c,open('$CONFIG','w'),indent=2)\"

=== STEP 9: RUN CALLOUT PIPELINE ===
Run the WBR callout pipeline. Pass the Quip context from Step 3 (existing callouts) and
change log context from Step 4 (campaign changes) to the callout writer:
  $KIRO_CLI chat --agent karpathy --no-interactive --trust-all-tools 'Run the wbr-callouts skill for all 10 markets. Dashboard already ingested. Follow callout-principles.md. Quip context: [summary of existing callouts from Step 3]. Change log context: [summary from Step 4].'

=== STEP 10: LOG PER-MARKET CALLOUT STATUS ===
After callouts complete, log each market's status to DuckDB wbr_callout_status table.
For each of the 10 markets (au, mx, us, ca, jp, uk, de, fr, it, es):
  - Check if ~/shared/context/active/callouts/[market]/[market]-2026-w[NN].md exists
  - If exists: status='generated', callout_file=path
  - If missing: status='skipped' or 'error' with error_message
Run:
  python3 -c \"
import duckdb, datetime as dt, os
con = duckdb.connect('/home/prichwil/shared/data/duckdb/ps-analytics.duckdb')
run_id = 'wbr_w[NN]_' + dt.datetime.now().strftime('%Y%m%d%H%M')
markets = ['au','mx','us','ca','jp','uk','de','fr','it','es']
for m in markets:
    path = os.path.expanduser(f'~/shared/context/active/callouts/{m}/{m}-2026-w[NN].md')
    if os.path.exists(path):
        con.execute('INSERT INTO wbr_callout_status (run_id, week_number, market, status, callout_file) VALUES (?,?,?,?,?)',
                    [run_id, 'W[NN]', m, 'generated', path])
    else:
        con.execute('INSERT INTO wbr_callout_status (run_id, week_number, market, status, error_message) VALUES (?,?,?,?,?)',
                    [run_id, 'W[NN]', m, 'skipped', 'callout file not found'])
con.close()
\"
Replace [NN] with the actual week number. Non-critical — if logging fails, continue.

=== STEP 11: SLACK NOTIFICATION WITH PER-MARKET WOW SUMMARY ===
After callouts complete, DM Richard on Slack with a summary. Use self_dm with login 'prichwil'.
Build the message by reading each market's callout file and extracting the most significant
WoW change (regs or spend) for a one-line-per-market summary.

Format:
  '📊 W[NN] WBR Callouts Ready
  Dashboard: [filename] ingested
  Quip context: [read OK / read failed]

  Per-market highlights:
  • AU: [most significant WoW change, e.g. Regs +12% WoW driven by X]
  • MX: [most significant WoW change]
  • US: [most significant WoW change]
  • CA: [most significant WoW change]
  • JP: [most significant WoW change]
  • UK: [most significant WoW change]
  • DE: [most significant WoW change]
  • FR: [most significant WoW change]
  • IT: [most significant WoW change]
  • ES: [most significant WoW change]

  Markets generated: [N]/10
  Stale context: [list or none]
  Projection accuracy: [summary or first run]
  Change log: [ingested/failed/skipped]
  Quip: https://quip-amazon.com/MMgBAzDrlVou
  Review: ~/shared/context/active/callouts/[market]/[market]-2026-w[NN].md'

For each market, read the callout file and extract the single most impactful metric
(largest absolute WoW % change in regs or spend). Keep each line under 80 chars.
If a market was skipped or errored, note it: '• [MKT]: ⚠️ skipped — [reason]'

=== STEP 12: PIPELINE OBSERVABILITY ===
Log this pipeline execution to DuckDB workflow_executions table.
At the END of the pipeline (whether success or failure), run:
  python3 -c \"
import duckdb, datetime as dt
con = duckdb.connect('/home/prichwil/shared/data/duckdb/ps-analytics.duckdb')
now = dt.datetime.now().isoformat()
eid = 'wbr_quip_publish_' + now.replace(':','').replace('-','')[:15]
# Count steps completed and failed from the pipeline run above
# Steps: 1-check, 2-context, 3-quip_read, 4-changelog, 5-projection, 6-download, 7-ingest, 8-config, 9-callouts, 10-market_log, 11-slack
# Adjust steps_completed and steps_failed based on actual results
con.execute(\\\"INSERT INTO workflow_executions (execution_id, workflow_name, trigger_source, mcp_servers_involved, start_time, end_time, status, steps_completed, steps_failed, duration_seconds) VALUES (?, 'wbr_quip_publish', 'wbr_watcher', ['SharePoint','DuckDB','Slack','Builder'], ?, CURRENT_TIMESTAMP, ?, ?, ?, NULL)\\\", [eid, now, 'completed', 11, 0])
con.close()
\"
Adjust the status ('completed', 'partial', or 'failed'), steps_completed, and steps_failed counts based on actual pipeline results.
Non-critical — if logging fails, continue.

Report final status: PIPELINE_COMPLETE, NO_NEW_FILE, or ERROR:[step]:[reason]" \
    2>&1 | tail -10 | tee -a "$LOG"

  echo "$(date -Iseconds) Poll complete. Next check in ${POLL_INTERVAL}s." | tee -a "$LOG"
  sleep $POLL_INTERVAL
done