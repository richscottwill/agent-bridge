#!/usr/bin/env python3
"""
Asana Activity Scanner v3 - Uses shell pipe approach that works.
"""
import json
import subprocess
import sys
import os
import time
from datetime import datetime, timezone

CUTOFF = "2026-04-09T00:00:00.000Z"
RICHARD_GID = "1212732742544167"
MCP_BIN = os.path.expanduser("~/.toolbox/bin/enterprise-asana-mcp")
OUTPUT_DIR = os.path.expanduser("~/shared/tools/asana-scan-output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

TASKS = [
    ("1213125740755931", "Email overlay WW rollout/testing"),
    ("1212992331748509", "Promo Test"),
    ("1213085905102041", "WW keyword gap fill based on market-level ASINs"),
    ("1213336296972484", "Add Audiences to Google"),
    ("1206497728159518", "AppsFlyer setup (tentative date)"),
    ("1212808474749819", "Paid App PO — Create Q2 + Amend Google PO to Q2"),
    ("1213341921686564", "Testing Document for Kate"),
    ("1213072707685838", "AU Paper LP"),
    ("1213003036439750", "Create campaign for new vs. all"),
    ("1213336296972490", "Import audience to GAds"),
    ("1212811293275565", "See if budget dashboard WW can be created"),
    ("1212811293275567", "See if we can create a view with relevant links"),
    ("1213230198995937", "WW redirect - Existing customer reporting"),
    ("1213072707685843", "AU NB testing focus: MRO/Trades in AU"),
    ("1212915141732002", "For MX/AU, add ad group for Amazon terms"),
    ("1213379551525584", "Paid Acq Agent Swarm (Alpha)"),
    ("1213072707685846", "AU opp: May-June opp for ad text"),
    ("1213125740755945", "Localize ABIX pages based on CA testing"),
    ("1212760973200416", "Keep Change Log updated"),
    ("1213235338214791", "AB Customer Redirect"),
    ("1212988092117041", "Paid App"),
    ("1213336296972493", "Enable Enhanced Match"),
    ("1213332849519450", "Request Media Updates"),
    ("1213336296972488", "Include audience in Media request"),
    ("1212760973200434", "F90"),
    ("1213072707685849", "AU opp: AE: Introduce RW to Amy"),
    ("1213530917597503", "Monthly - Confirm actual budgets"),
    ("1213278917849558", "Initial Testing"),
    ("1214068275460844", "Review Q2 CCP/ieCCP files from Stacey"),
    ("1214074477110993", "Sitelink Audit/Update"),
    ("1214044682239823", "MX Experiments ending 4/30"),
    ("1214081017092577", "MCS LP Review: Connect with Lorena"),
    ("1214074477111007", "DDD walkthrough with team"),
    ("1213965650410967", "Deep Dive: Year-One Optimization one-pager"),
    ("1214081017200478", "AU meetings - Agenda"),
    ("1214081017124426", "MCS LP Review: Follow up on global Polaris"),
    ("1214081017044930", "MCS LP Review: Share MX Polaris test results"),
    ("1214080130329568", "Make changes to AU/MX/PAM for the week"),
    ("1214080207515561", "R&O for MX/AU"),
    ("1214079536513059", "ABIX R&O"),
    ("1214075341408685", "Check - A/B Beauty/Auto Experiment launched in MX"),
    ("1214075341408681", "Check - Launched Mobile extensions in MX"),
    ("1214075340745325", "Get BrowserStack access for Adi"),
    ("1213764961716427", "WW weblab dial-up (Richard)"),
    ("1213796951745232", "Look over AU landing page switch"),
    ("1213917691089036", "Refmarker mapping audit PoC — AU"),
    ("1213964186504305", "Send IECCP follow-up summary to Lorena"),
    ("1213917967984980", "Respond to Lena — AU LP URL analysis"),
    ("1214068319365234", "Approve OFA invoice workflow (Mohd Sadeq)"),
    ("1214068215114017", "PAM: Check US/EU spend pacing vs Q2 budget"),
    ("1214068215142846", "PAM: Confirm FR pivot campaign structure"),
    ("1213690904654138", "Monthly: Individual Goals update"),
    ("1214068272596724", "PAM: Flag underspend risk to Brandon"),
    ("1213959904341162", "Reply to Brandon — PAM budget needs assessment"),
    ("1214044802323482", "Raise PO for Q2 instead of increasing to FY"),
    ("1214044802323478", "Raise PO for US PAM for 70K underreported"),
    ("1213917691068688", "Send AU team invoice for prev month"),
    ("1214044682239817", "MX Polaris NB LP Test (Beauty+Auto)"),
    ("1213983077428492", "ie%CCP calc - insert MX spend/regs before 9th"),
    ("1213993229524626", "ie%CCP calc - insert MX spend/regs before 9th (2)"),
    ("1213983332107930", "MX/AU confirm budgets"),
    ("1214057202961389", "Weekly Reporting - Global WBR sheet"),
    ("1214055207544514", "Come prepared: Bi-weekly with Adi"),
    ("1213875146955582", "Get Enhanced Match details"),
    ("1214054954497349", "Mondays - Write into EU SSR Acq Asana"),
    ("1214053404599901", "Convert EOD frontend to auto-hook"),
    ("1214047624490628", "Slack history backfill"),
    ("1213954957625028", "Approve: Enhanced Match / LiveRamp"),
    ("1213954957645131", "Approve: AU Paid Search — Market Wiki"),
    ("1213953295002324", "Approve: OCI Execution Guide"),
    ("1214050694901572", "Slack thread-level ingestion"),
    ("1214044682239803", "Cross-marketing Refmarker audit"),
    ("1213917747438931", "AU — Market Context (Kiro)"),
    ("1213917639688517", "MX — Market Context (Kiro)"),
    ("1214006311270752", "Reply to Dwayne — AU PS/MCS Updates thread"),
    ("1213962513760099", "Brandon 1:1: ASP reminders"),
    ("1213968042348601", "Deep Dive: Add IECCP FAQ to new account playbook"),
    ("1213959854928587", "Deep Dive: Finalize market expansion playbook"),
    ("1213964668984060", "Brandon 1:1: Draft Enhanced Match FAQ for legal"),
    ("1213983342210449", "MBR callout"),
    ("1213983090951838", "Update Kingpin for MX"),
    ("1213925549385885", "Paid Search Testing Approach & Year Ahead"),
    ("1213917771155873", "Paid App — Project Context (Kiro)"),
    ("1213917747384849", "AU Market Context (Agent-Maintained)"),
    ("1213958643249348", "Agent System Architecture — wiki article"),
    ("1213917833386312", "Dashboard Ingester"),
    ("1213930231361406", "Attention Tracker"),
    ("1213917853456301", "Bayesian Prediction Engine"),
    ("1213917853456285", "WBR Callout Pipeline"),
    ("1213930231347406", "Agent Bridge (Google Sheets/Docs)"),
    ("1213917968634410", "PS Analytics Data Layer (DuckDB)"),
    ("1213917833443720", "Morning Routine (AM-1/2/3)"),
    ("1213917853447785", "Asana Command Center Integration"),
    ("1213925516289208", "Enhanced Match / LiveRamp — Audience Expansion"),
    ("1213953288745383", "AU Paid Search — Market Wiki"),
    ("1213925733042547", "OCI Execution Guide"),
    ("1213925516128369", "ie%CCP Planning & Optimization Framework"),
    ("1213925516246590", "OCI Rollout Playbook"),
    ("1213925648150955", "Invoice & PO Process Guide"),
    ("1213925733287816", "Landing Page Testing Playbook"),
]

def call_mcp_shell(task_gid, call_id):
    """Call GetTaskStories using shell echo pipe approach (proven to work)."""
    request = json.dumps({
        "jsonrpc": "2.0",
        "id": call_id,
        "method": "tools/call",
        "params": {
            "name": "asana___GetTaskStories",
            "arguments": {"task_gid": task_gid}
        }
    })
    # Use the exact approach that worked in manual testing
    cmd = f"echo '{request}' | timeout 30 {MCP_BIN} 2>/dev/null"
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=35
        )
        stdout = result.stdout.strip()
        if not stdout:
            return None, f"Empty stdout"
        return stdout, None
    except subprocess.TimeoutExpired:
        return None, "Timeout"
    except Exception as e:
        return None, str(e)

def parse_stories(raw_output):
    """Parse stories from MCP response."""
    data = json.loads(raw_output)
    if 'error' in data:
        raise Exception(f"JSON-RPC error: {data['error']}")
    text_content = data['result']['content'][0]['text']
    api_data = json.loads(text_content)
    if 'APIOutput' in api_data:
        stories = api_data['APIOutput']['Response']['data']
    elif 'data' in api_data:
        stories = api_data['data']
    else:
        stories = []
    return stories

def classify_story(story):
    """Classify a story into signal type."""
    resource_subtype = story.get('resource_subtype', '')
    text = story.get('text', '')
    stype = story.get('type', '')
    
    if resource_subtype == 'comment_added' or stype == 'comment':
        return 'comment_added'
    elif 'due date' in text.lower() or resource_subtype == 'due_date_changed':
        return 'due_date_changed'
    elif resource_subtype in ('assigned', 'reassigned') or 'reassigned' in text.lower():
        return 'reassigned'
    return None

def main():
    signals = []
    errors = []
    per_task_timestamps = {}
    scanned = 0
    now_ts = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    total = len(TASKS)
    
    for i, (task_gid, task_name) in enumerate(TASKS):
        scanned += 1
        if scanned % 10 == 0:
            print(f"Progress: {scanned}/{total}", file=sys.stderr, flush=True)
        
        raw_output, error = call_mcp_shell(task_gid, i + 1)
        
        if error:
            errors.append({"task_gid": task_gid, "task_name": task_name, "error": error})
            time.sleep(0.3)
            continue
        
        try:
            stories = parse_stories(raw_output)
        except Exception as e:
            errors.append({"task_gid": task_gid, "task_name": task_name, "error": f"Parse: {e}"})
            continue
        
        latest_ts = None
        for story in stories:
            created_at = story.get('created_at', '')
            if created_at > CUTOFF:
                if latest_ts is None or created_at > latest_ts:
                    latest_ts = created_at
                
                created_by = story.get('created_by') or {}
                if not created_by.get('gid'):
                    continue
                if created_by.get('gid') == RICHARD_GID:
                    continue
                
                signal_type = classify_story(story)
                if signal_type:
                    signals.append({
                        'task_gid': task_gid,
                        'task_name': task_name,
                        'signal_type': signal_type,
                        'author_name': created_by.get('name', 'Unknown'),
                        'author_gid': created_by.get('gid', ''),
                        'created_at': created_at,
                        'text': story.get('text', '')[:200],
                        'resource_subtype': story.get('resource_subtype', ''),
                        'story_gid': story.get('gid', '')
                    })
        
        per_task_timestamps[task_gid] = latest_ts or now_ts
        time.sleep(0.2)
    
    output = {
        'scan_timestamp': now_ts,
        'tasks_scanned': scanned,
        'signals': signals,
        'errors': errors,
        'per_task_timestamps': per_task_timestamps
    }
    
    results_path = os.path.join(OUTPUT_DIR, 'scan-results.json')
    with open(results_path, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"Tasks scanned: {scanned}")
    print(f"Signals detected: {len(signals)}")
    print(f"Errors: {len(errors)}")
    if signals:
        for s in signals:
            print(f"  {s['signal_type']}: {s['task_name']} — {s['author_name']} ({s['created_at']})")
    if errors:
        print(f"First error: {errors[0]}")
    print(f"Results: {results_path}")

if __name__ == '__main__':
    main()
