#!/usr/bin/env python3
"""Asana → DuckDB Full Sync Script for AM-1 Morning Routine
Date: 2026-04-10
Processes task data collected from Asana API and syncs to DuckDB.
"""
import duckdb
import json
import os
from datetime import datetime, date

DB_PATH = os.path.expanduser("~/shared/data/duckdb/ps-analytics.duckdb")
TODAY = "2026-04-10"
SYNC_TS = datetime.utcnow().isoformat() + "Z"

# Field GID mappings
FIELD_MAP = {
    '1213608836755502': 'routine_rw',
    '1212905889837829': 'priority_rw',
    '1212905889837865': 'importance_rw',
    '1213915851848087': 'kiro_rw',
    '1213921400039514': 'next_action_rw',
    '1213440376528542': 'begin_date_rw',
}

ROUTINE_MAP = {
    'Sweep (Low-friction)': 'Sweep',
    'Core Two (Deep Work)': 'Core',
    'Engine Room (Excel and Google ads)': 'Engine Room',
    'Admin (Wind-down)': 'Admin',
    'Wiki': 'Wiki',
}

# All tasks collected from Asana API (detailed + compact)
# Format: list of dicts with mapped fields
TASKS = []

def add_task(gid, name, due_on=None, start_on=None, completed=False, completed_at=None,
             assignee_gid='1212732742544167', project_name=None, project_gid=None,
             section_name=None, routine_rw=None, priority_rw=None, importance_rw=None,
             kiro_rw=None, next_action_rw=None, begin_date_rw=None, permalink_url=None,
             notes=None, flex_fields=None):
    TASKS.append({
        'task_gid': gid,
        'name': name,
        'due_on': due_on,
        'start_on': start_on,
        'completed': completed,
        'completed_at': completed_at,
        'assignee_gid': assignee_gid,
        'project_name': project_name,
        'project_gid': project_gid,
        'section_name': section_name,
        'routine_rw': routine_rw,
        'priority_rw': priority_rw,
        'importance_rw': importance_rw,
        'kiro_rw': kiro_rw,
        'next_action_rw': next_action_rw,
        'begin_date_rw': begin_date_rw,
        'permalink_url': permalink_url,
        'flex_fields': json.dumps(flex_fields) if flex_fields else None,
    })


# === TASK DATA FROM ASANA API (2026-04-10 morning pull) ===
# Detailed tasks (with full custom field data)
add_task('1213993229524626', 'ie%CCP calc - insert MX spend/regs before 9th', due_on='2026-05-09', routine_rw='Engine Room', kiro_rw='4/9: Auto-created. Monthly ie%CCP calc.', next_action_rw='Insert MX spend/regs into ie%CCP sheet before 9th')
add_task('1213983342210449', 'MBR callout', due_on='2026-05-02', project_name='AU', project_gid='1212762061512767', section_name='Planning', routine_rw='Admin', priority_rw='Urgent', importance_rw='Important', kiro_rw='4/7: Carried fwd. Overdue since 4/2.', next_action_rw='Review AU+MX MBR draft callouts')
add_task('1213530917597503', 'Monthly - Confirm actual budgets', due_on='2026-05-05', project_name='Paid App', project_gid='1205997667578886', section_name='Backlog', routine_rw='Admin', priority_rw='Urgent', importance_rw='Important', kiro_rw='4/4: Due 5/5. Monthly recurring.', next_action_rw='Pull April finance actuals')
add_task('1213828989831378', 'Bi-monthly Flash', due_on='2026-05-21', project_name='Paid App', project_gid='1205997667578886', section_name='Backlog', routine_rw='Sweep', priority_rw='Not urgent', kiro_rw='4/4: Due 5/21. Bi-monthly recurring.', next_action_rw='No action until May')
add_task('1213983090951838', 'Update Kingpin for MX', due_on='2026-05-05', project_name='MX', project_gid='1212775592612917', section_name='Planning', routine_rw='Sweep', priority_rw='Not urgent', importance_rw='Important', kiro_rw='4/4: Due 4/7. Blocked by Andes data.', next_action_rw='Check if Andes data is now available')
add_task('1212760973200434', 'F90', due_on='2026-04-30', project_name='ABPS - WW Testing & Projects', project_gid='1205997667578893', section_name='Prioritized', routine_rw='Core', priority_rw='Not urgent', importance_rw='Important', kiro_rw='4/4: F90 lifecycle program. 9 subtasks.', next_action_rw='Coordinate with media team on audience request')
add_task('1213983077428492', 'ie%CCP calc - insert MX spend/regs before 9th', due_on='2026-05-01', routine_rw='Sweep', priority_rw='Not urgent', importance_rw='Important', kiro_rw='4/4: Due 4/7. Monthly recurring.', next_action_rw='Open ie%CCP Quip sheet, insert March MX spend')
add_task('1213917691068688', 'Send AU team invoice for prev month', due_on='2026-05-02', routine_rw='Admin', priority_rw='Urgent', kiro_rw='4/4: Carried fwd. Due 5/2.', next_action_rw='Pull April AU invoice from Google Ads mid-month')
add_task('1213983332107930', 'MX/AU confirm budgets', due_on='2026-04-29', routine_rw='Admin', priority_rw='Urgent', kiro_rw='4/4: 10d overdue. AU/MX budget now under Marketing finance.', next_action_rw='Reach out to BK Cho to confirm MX and AU budget numbers')
add_task('1206497728159518', 'AppsFlyer setup (tentative date)', due_on='2026-07-01', project_name='Paid App', project_gid='1205997667578886', section_name='Blocked', routine_rw='Core', priority_rw='Not urgent', importance_rw='Important', kiro_rw='4/4: AppsFlyer mobile attribution setup.', next_action_rw='Check in on AppsFlyer vendor timeline in May')
add_task('1213796951745232', 'Look over AU landing page switch', due_on='2026-04-15', project_name='AU', project_gid='1212762061512767', section_name='Planning', routine_rw='Engine Room', priority_rw='Urgent', kiro_rw='4/8: Revert NB back to older pages per Polaris LP thread.', next_action_rw='Coordinate NB LP revert with Dwayne')
add_task('1213072707685834', 'MX Automotive page', due_on='2026-04-15', project_name='MX', project_gid='1212775592612917', section_name='Planning', routine_rw='Engine Room', priority_rw='Urgent', kiro_rw='4/8: Pages built, KWs defined by Lorena.', next_action_rw='Build MX Auto + Beauty campaigns in Google Ads')
add_task('1213965650410967', 'Deep Dive: Year-One Optimization one-pager', due_on='2026-04-16', routine_rw='Core', priority_rw='Urgent', kiro_rw='4/6: Due 4/16. Draft framework written.', next_action_rw='Week of 4/14: review one-pager draft')
add_task('1213423234257246', 'Get Enhanced Match Legal Approval', due_on='2026-04-22', routine_rw='Sweep', priority_rw='Not urgent', kiro_rw='4/4: F90 subtask. Blocked on Abdul TPS checklist.', next_action_rw='Blocked — waiting on Enhanced Match details from Abdul')
add_task('1213983232672825', 'AU meetings - Agenda', due_on='2026-04-14', project_name='AU', project_gid='1212762061512767', section_name='Planning', routine_rw='Sweep', priority_rw='Not urgent', kiro_rw='4/4: Due 4/7. Prep agenda items for Monday AU sync.', next_action_rw='Draft 3 agenda items')
add_task('1213125740755931', 'Email overlay WW rollout/testing', due_on='2026-04-18', project_name='ABPS - WW Testing & Projects', project_gid='1205997667578893', section_name='Prioritized', routine_rw='Core', priority_rw='Urgent', importance_rw='Important', kiro_rw='4/8: In development. Extended to 4/18.', next_action_rw='Continue email overlay development work')
add_task('1213993242268778', 'Mondays - Write into EU SSR Acq Asana', due_on='2026-04-14', start_on='2026-04-12', routine_rw='Admin', kiro_rw='4/9: Auto-created. Weekly EU SSR update.', next_action_rw='Write AU/MX updates into EU SSR Acq Asana board')
add_task('1213964668984060', 'Brandon 1:1: Draft Enhanced Match FAQ for legal', due_on='2026-04-22', routine_rw='Sweep', priority_rw='Urgent', kiro_rw='4/8: Urgent. Draft FAQ for LiveRamp Enhanced Match legal.', next_action_rw='Draft FAQ outline, pull LiveRamp data points')
add_task('1213278917849558', 'Initial Testing', due_on='2026-04-17', routine_rw='Engine Room', priority_rw='Not urgent', kiro_rw='4/4: Baloo initial testing via wiki instructions.', next_action_rw='Follow Baloo wiki setup guide')
add_task('1213993242326093', 'AU meetings - Agenda', due_on='2026-04-14', start_on='2026-04-12', project_name='AU', project_gid='1212762061512767', section_name='Planning', routine_rw='Engine Room', kiro_rw='4/9: Auto-created. Weekly AU agenda prep.', next_action_rw='Prep agenda items for AU sync')
add_task('1213968042348601', 'Deep Dive: Add IECCP FAQ to new account playbook', due_on='2026-04-09', routine_rw='Core', priority_rw='Today', kiro_rw='4/6: Due 4/9. Draft FAQ written.', next_action_rw='Tuesday: review FAQ draft in task notes')
add_task('1213968042349624', 'Brandon 1:1: Reframe AdWords KB ticket as risk mitigation', due_on='2026-04-09', routine_rw='Engine Room', priority_rw='Today', kiro_rw='4/6: Reframe ABMA-11245 as risk mitigation for $70K underspend.', next_action_rw='Add comment to ABMA-11245')
add_task('1213764961716427', 'WW weblab dial-up (Richard)', due_on='2026-04-07', project_name='ABPS - WW Testing & Projects', project_gid='1205997667578893', section_name='WW Doc Inputs', routine_rw='Core', priority_rw='Urgent', kiro_rw='4/9: Carried fwd. Austin offsite.', next_action_rw='Coordinate with Alex/Vijeth on weblab dial-up settings')
add_task('1213983077469989', 'Mondays - Write into EU SSR Acq Asana', due_on='2026-04-13', routine_rw='Sweep', priority_rw='Urgent', importance_rw='Important', kiro_rw='4/4: Due 4/7. Weekly recurring.', next_action_rw='Write W14 AU/MX/PAM status updates')
add_task('1213983331865941', 'Weekly Reporting - Global WBR sheet', due_on='2026-04-13', project_name='Paid App', project_gid='1205997667578886', section_name='Backlog', routine_rw='Engine Room', priority_rw='Urgent', importance_rw='Important', kiro_rw='4/4: Due 4/7. Weekly recurring.', next_action_rw='Pull W14 data from dashboards into Global WBR sheet')
add_task('1213964186504305', 'Send IECCP follow-up summary to Lorena + review keyword data', due_on='2026-04-09', project_name='MX', project_gid='1212775592612917', section_name='Planning', routine_rw='Sweep', priority_rw='Today', kiro_rw='4/9: Due TODAY. Draft IECCP summary for Lorena.', next_action_rw='Draft IECCP summary email, send to Lorena')
add_task('1213731008237682', 'Come prepared: Bi-weekly with Adi to brainstorm usable AI', due_on='2026-04-14', routine_rw='Sweep', priority_rw='Not urgent', kiro_rw='4/4: Due 4/14. Bi-weekly recurring.', next_action_rw='Prep 3 AI use case ideas')
add_task('1213959854928587', 'Deep Dive: Finalize market expansion playbook', due_on='2026-04-09', routine_rw='Core', priority_rw='Today', kiro_rw='4/6: Due 4/9. Draft outline written.', next_action_rw='Tuesday: open outline, fill in AU/MX sections')
add_task('1213963678745039', 'Pull AU Polaris LP conversion rate data', due_on='2026-04-08', project_name='AU', project_gid='1212762061512767', section_name='Planning', routine_rw='Engine Room', priority_rw='Urgent', kiro_rw='4/9: Carried fwd. Austin offsite.', next_action_rw='Analyze AU-Brand-NB_CVR-since-LP.xlsx')
add_task('1213925549385885', 'Paid Search Testing Approach & Year Ahead', project_name='ABPS AI - Content', project_gid='1213917352480610', section_name='Review', routine_rw='Wiki', priority_rw='Not urgent', kiro_rw='4/5: Published FINAL. Eval A: 8.4/10, Eval B: 8.2/10.', next_action_rw='Content synced. Review per audit.')
add_task('1213875146955582', 'Get Enhanced Match details', due_on='2026-04-07', routine_rw='Sweep', priority_rw='Today', kiro_rw='4/6: Due 4/7. Draft Slack msg to Abdul written.', next_action_rw='Slack Abdul today with the 4 Enhanced Match questions')
add_task('1213923298187459', 'Refmarker mapping audit PoC — AU (old)', due_on='2026-04-07', project_name='AU', project_gid='1212762061512767', section_name='Planning', routine_rw='Sweep', priority_rw='Today', kiro_rw='4/4: Carried fwd. Due 4/7.', next_action_rw='Monday: review Lena audit scope')
add_task('1213917691089036', 'Refmarker mapping audit PoC — AU', due_on='2026-04-10', project_name='AU', project_gid='1212762061512767', section_name='Planning', routine_rw='Engine Room', priority_rw='Today', kiro_rw='4/9: Due 4/10. Build refmarker-to-LP mapping.', next_action_rw='Export Google Ads refmarker report, map to LP URLs')
add_task('1213690904654138', 'Monthly: Individual Goals update', due_on='2026-04-10', routine_rw='Engine Room', priority_rw='Today', importance_rw='Important', kiro_rw='4/4: Due 4/10. Monthly recurring. 14 goals stale.', next_action_rw='Start with MX/AU registration goals')
add_task('1213959904341162', 'Reply to Brandon — PAM budget needs assessment', due_on='2026-04-06', routine_rw='Sweep', priority_rw='Urgent', kiro_rw='4/7: Carried fwd. Overdue since 4/6.', next_action_rw='Copy draft reply into Slack')
add_task('1213730974261148', 'Make changes to AU/MX/PAM for the week', due_on='2026-03-18', routine_rw='Engine Room', priority_rw='Not urgent', kiro_rw='4/4: 17d overdue. Weekly recurring.', next_action_rw='Review W14 performance data')
add_task('1213962513816458', 'Brandon 1:1: Obtain TPS checklist from Abdul for F90 audience', due_on='2026-04-07', routine_rw='Sweep', priority_rw='Today', kiro_rw='4/6: Slack Abdul with TPS checklist request.', next_action_rw='DM Abdul asking for TPS checklist')
add_task('1213917967984980', 'Respond to Lena — AU LP URL analysis + CPA methodology', due_on='2026-04-03', project_name='AU', project_gid='1212762061512767', section_name='Planning', routine_rw='Sweep', priority_rw='Urgent', kiro_rw='4/6: 3d overdue. Draft reply written.', next_action_rw='Pull AU LP URL report from Google Ads')

# Remaining tasks from SearchTasksInWorkspace (compact data — no detailed custom fields fetched)
# These get minimal field data from the search results
remaining_compact = [
    ('1212808474749819', 'Raise rest of year PO for PAM US', None),
    ('1213560614815911', 'PAM R&O', None),
    ('1213637505601024', 'R&O for MX/AU', None),
    ('1213798673865639', 'Update and close your goal(s)', None),
    ('1213817111703805', "It's time to update your goal(s)", None),
    ('1213341921686564', 'Testing Document for Kate', None),
    ('1212988092117041', 'Paid App', None),
    ('1213230198995937', 'WW redirect - Existing customer reporting in Adobe Ad Cloud', None),
    ('1213954957625028', 'Approve: Enhanced Match / LiveRamp — Audience Expansion', None),
    ('1213954957645131', 'Approve: AU Paid Search — Market Wiki', None),
    ('1213953295002324', 'Approve: OCI Execution Guide', None),
    ('1213917771155873', 'Paid App — Project Context (Kiro)', None),
    ('1213917639688517', 'MX — Market Context (Kiro)', None),
    ('1213917747438931', 'AU — Market Context (Kiro)', None),
    ('1213917747384849', 'AU Market Context (Agent-Maintained)', None),
    ('1213958643249348', 'Agent System Architecture — wiki article updated', None),
    ('1213917833386312', 'Dashboard Ingester', None),
    ('1213930231361406', 'Attention Tracker', None),
    ('1213917853456301', 'Bayesian Prediction Engine', None),
    ('1213917853456285', 'WBR Callout Pipeline', None),
    ('1213930231347406', 'Agent Bridge (Google Sheets/Docs)', None),
    ('1213917968634410', 'PS Analytics Data Layer (DuckDB)', None),
    ('1213379551525584', 'Paid Acq Agent Swarm (Alpha)', None),
    ('1213917833443720', 'Morning Routine (AM-1/2/3)', None),
    ('1213917853447785', 'Asana Command Center Integration', None),
    ('1213925516289208', 'Enhanced Match / LiveRamp — Audience Expansion', None),
    ('1213953288745383', 'AU Paid Search — Market Wiki', None),
    ('1213925733042547', 'OCI Execution Guide', None),
    ('1213925516128369', 'ie%CCP Planning & Optimization Framework', None),
    ('1213925516246590', 'OCI Rollout Playbook', None),
    ('1213925648150955', 'Invoice & PO Process Guide', None),
    ('1213925733287816', 'Landing Page Testing Playbook', None),
    ('1213925648144613', 'Google Ads Campaign Structure Standards', None),
    ('1213925648194804', 'Stakeholder Communication Guide', None),
    ('1213954951680204', 'Budget Forecast Helper Spec', None),
    ('1213925733264874', 'Campaign Link Generator Spec', None),
    ('1213925648113679', 'WBR Callout Template & Guide', None),
    ('1213925648102375', 'AU Keyword CPA Dashboard — Design', None),
    ('1213925733090815', 'Market Reference: AB Paid Search Across 10 Markets', None),
    ('1213925733093966', 'Polaris WW Rollout — Status and Decision Log', None),
    ('1213925733100401', 'Team Capacity and Workload Distribution', None),
    ('1213925733091034', 'WW Testing Tracker', None),
    ('1213925647933633', 'MX Paid Search — Market Wiki', None),
    ('1213955495811354', 'AB Paid Search Program Wiki', None),
    ('1213955491618264', 'Workstream 5: Algorithmic Ads', None),
    ('1213955491611923', 'Workstream 4: User Experience', None),
    ('1213925733024101', 'Workstream 3: Audiences', None),
    ('1213925647915195', 'Workstream 2: Modern Search', None),
    ('1213925754103177', 'Workstream 1: Intelligent Bidding (OCI)', None),
    ('1213954951120691', 'Project Baloo — Shopping Ads for Amazon Business', None),
    ('1213954951075984', 'AU NB Testing Proposal — MRO/Trades Vertical', None),
    ('1213925549433986', 'AI Max Test Design — US Market', None),
    ('1213925549433825', 'Email Overlay WW Rollout Plan', None),
    ('1213954951048994', 'Ad Copy Testing Framework', None),
    ('1213925647459466', 'GenAI Search Traffic — What We Know', None),
    ('1213925647445346', 'Q2 2026 Initiative Status & Priorities', None),
    ('1213953288179600', 'Cross-Market Playbook — US — EU5 — RoW', None),
    ('1213954950900701', 'Competitive Landscape: Who Bidding Against Amazon Business', None),
    ('1213953288179823', 'F90 Lifecycle Program Strategy', None),
    ('1213925647329369', 'The Body System — Architecture for Personal AI Operating Systems', None),
    ('1213925647315051', 'Agentic Paid Search — Vision & Roadmap', None),
]

for gid, name, due in remaining_compact:
    # Check if already added with details
    existing_gids = {t['task_gid'] for t in TASKS}
    if gid not in existing_gids:
        add_task(gid, name, due_on=due)

# Also add the task with SSE error that we couldn't fetch
existing_gids = {t['task_gid'] for t in TASKS}
if '1213962513760099' not in existing_gids:
    add_task('1213962513760099', 'Brandon 1:1: Set up automated monthly ASP confirmation reminders', due_on='2026-04-09', routine_rw='Sweep', priority_rw='Urgent')

print(f"Total tasks collected: {len(TASKS)}")


# === DUCKDB SYNC ===
def run_sync():
    con = duckdb.connect(DB_PATH)

    # Ensure schema exists
    con.execute("CREATE SCHEMA IF NOT EXISTS asana")

    # Ensure table exists
    con.execute("""
        CREATE TABLE IF NOT EXISTS asana.asana_tasks (
            task_gid VARCHAR PRIMARY KEY,
            name VARCHAR,
            assignee_gid VARCHAR,
            project_name VARCHAR,
            project_gid VARCHAR,
            section_name VARCHAR,
            due_on DATE,
            start_on DATE,
            completed BOOLEAN DEFAULT FALSE,
            completed_at TIMESTAMP,
            routine_rw VARCHAR,
            priority_rw VARCHAR,
            importance_rw VARCHAR,
            kiro_rw VARCHAR,
            next_action_rw VARCHAR,
            begin_date_rw DATE,
            flex_fields JSON,
            permalink_url VARCHAR,
            synced_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            deleted_at TIMESTAMP
        )
    """)

    # Ensure history table exists
    con.execute("""
        CREATE TABLE IF NOT EXISTS asana.asana_task_history (
            snapshot_date DATE,
            task_gid VARCHAR,
            project_name VARCHAR,
            section_name VARCHAR,
            due_on DATE,
            completed BOOLEAN,
            priority_rw VARCHAR,
            routine_rw VARCHAR,
            PRIMARY KEY (snapshot_date, task_gid)
        )
    """)

    # Ensure schema_changes table exists
    con.execute("""
        CREATE TABLE IF NOT EXISTS asana.schema_changes (
            change_type VARCHAR,
            entity_name VARCHAR,
            old_value VARCHAR,
            new_value VARCHAR,
            detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Step 4: UPSERT all tasks
    now_ts = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    synced_gids = []
    upsert_count = 0
    for t in TASKS:
        synced_gids.append(t['task_gid'])
        con.execute("""
            INSERT INTO asana.asana_tasks (task_gid, name, assignee_gid, project_name, project_gid,
                section_name, due_on, start_on, completed, completed_at, routine_rw, priority_rw,
                importance_rw, kiro_rw, next_action_rw, begin_date_rw, flex_fields, permalink_url, synced_at, deleted_at)
            VALUES (?, ?, ?, ?, ?, ?, ?::DATE, ?::DATE, ?, ?, ?, ?, ?, ?, ?, ?::DATE, ?::JSON, ?, ?::TIMESTAMP, NULL)
            ON CONFLICT (task_gid) DO UPDATE SET
                name = EXCLUDED.name,
                assignee_gid = EXCLUDED.assignee_gid,
                project_name = COALESCE(EXCLUDED.project_name, asana.asana_tasks.project_name),
                project_gid = COALESCE(EXCLUDED.project_gid, asana.asana_tasks.project_gid),
                section_name = COALESCE(EXCLUDED.section_name, asana.asana_tasks.section_name),
                due_on = COALESCE(EXCLUDED.due_on, asana.asana_tasks.due_on),
                start_on = COALESCE(EXCLUDED.start_on, asana.asana_tasks.start_on),
                completed = EXCLUDED.completed,
                completed_at = EXCLUDED.completed_at,
                routine_rw = COALESCE(EXCLUDED.routine_rw, asana.asana_tasks.routine_rw),
                priority_rw = COALESCE(EXCLUDED.priority_rw, asana.asana_tasks.priority_rw),
                importance_rw = COALESCE(EXCLUDED.importance_rw, asana.asana_tasks.importance_rw),
                kiro_rw = COALESCE(EXCLUDED.kiro_rw, asana.asana_tasks.kiro_rw),
                next_action_rw = COALESCE(EXCLUDED.next_action_rw, asana.asana_tasks.next_action_rw),
                begin_date_rw = COALESCE(EXCLUDED.begin_date_rw, asana.asana_tasks.begin_date_rw),
                flex_fields = COALESCE(EXCLUDED.flex_fields, asana.asana_tasks.flex_fields),
                permalink_url = COALESCE(EXCLUDED.permalink_url, asana.asana_tasks.permalink_url),
                deleted_at = NULL,
                synced_at = EXCLUDED.synced_at
        """, [
            t['task_gid'], t['name'], t['assignee_gid'], t['project_name'], t['project_gid'],
            t['section_name'], t['due_on'], t['start_on'], t['completed'], t['completed_at'],
            t['routine_rw'], t['priority_rw'], t['importance_rw'], t['kiro_rw'],
            t['next_action_rw'], t['begin_date_rw'], t['flex_fields'], t.get('permalink_url'), now_ts
        ])
        upsert_count += 1

    print(f"UPSERT complete: {upsert_count} tasks")

    # Step 5: Soft-delete missing tasks
    if synced_gids:
        placeholders = ','.join([f"'{g}'" for g in synced_gids])
        con.execute(f"""
            UPDATE asana.asana_tasks SET deleted_at = '{now_ts}'::TIMESTAMP
            WHERE task_gid NOT IN ({placeholders})
              AND deleted_at IS NULL AND completed = FALSE
        """)
        deleted_count = con.execute(f"""
            SELECT COUNT(*) FROM asana.asana_tasks
            WHERE deleted_at IS NOT NULL AND deleted_at >= '{TODAY}'::DATE
        """).fetchone()[0]
        print(f"Soft-deleted: {deleted_count} tasks no longer in Asana")

    # Step 6: Daily snapshot
    con.execute(f"""
        INSERT INTO asana.asana_task_history (snapshot_date, task_gid, project_name, section_name, due_on, completed, priority_rw, routine_rw)
        SELECT '{TODAY}'::DATE, task_gid, project_name, section_name, due_on, completed, priority_rw, routine_rw
        FROM asana.asana_tasks WHERE deleted_at IS NULL
        ON CONFLICT (snapshot_date, task_gid) DO NOTHING
    """)
    snapshot_count = con.execute(f"SELECT COUNT(*) FROM asana.asana_task_history WHERE snapshot_date = '{TODAY}'::DATE").fetchone()[0]
    print(f"Daily snapshot: {snapshot_count} rows for {TODAY}")

    # Step 7: Coherence checks
    alerts = []

    # Check 1: Overdue tasks (3+ days)
    overdue = con.execute(f"""
        SELECT name, project_name, due_on, DATEDIFF('day', due_on, '{TODAY}'::DATE) AS days_overdue
        FROM asana.asana_tasks
        WHERE due_on < '{TODAY}'::DATE AND completed = FALSE AND deleted_at IS NULL
          AND DATEDIFF('day', due_on, '{TODAY}'::DATE) >= 3
        ORDER BY days_overdue DESC
    """).fetchall()
    if overdue:
        for row in overdue:
            alerts.append(f"⚠️ OVERDUE {row[3]}d: {row[0]} (project: {row[1] or 'My Tasks'})")

    # Check 2: Empty projects
    known_projects = {
        '1212732838073807': 'My Tasks',
        '1213917352480610': 'ABPS AI Content',
        '1212762061512767': 'AU',
        '1212775592612917': 'MX',
        '1205997667578893': 'WW Testing',
        '1206011235630048': 'WW Acquisition',
        '1205997667578886': 'Paid App',
    }
    project_counts = con.execute("""
        SELECT project_gid, project_name, COUNT(*) as cnt
        FROM asana.asana_tasks
        WHERE deleted_at IS NULL AND completed = FALSE AND project_gid IS NOT NULL
        GROUP BY project_gid, project_name
    """).fetchall()
    active_project_gids = {r[0] for r in project_counts}
    for pgid, pname in known_projects.items():
        if pgid not in active_project_gids and pgid != '1212732838073807':
            alerts.append(f"⚠️ EMPTY PROJECT: {pname} ({pgid}) has 0 incomplete tasks in DuckDB")

    # Check 3: Over-cap buckets
    caps = {'Sweep': 5, 'Core': 4, 'Engine Room': 6, 'Admin': 3}
    bucket_counts = con.execute("""
        SELECT routine_rw, COUNT(*) as cnt
        FROM asana.asana_tasks
        WHERE deleted_at IS NULL AND completed = FALSE AND routine_rw IS NOT NULL
          AND priority_rw IN ('Today', 'Urgent')
        GROUP BY routine_rw
    """).fetchall()
    for row in bucket_counts:
        bucket, cnt = row[0], row[1]
        if bucket in caps and cnt > caps[bucket]:
            alerts.append(f"⚠️ OVER CAP: {bucket} at {cnt}/{caps[bucket]}")

    # Check 4: Enrichment gaps
    empty_kiro = con.execute("""
        SELECT COUNT(*) FROM asana.asana_tasks
        WHERE kiro_rw IS NULL AND completed = FALSE AND deleted_at IS NULL
    """).fetchone()[0]
    empty_next = con.execute("""
        SELECT COUNT(*) FROM asana.asana_tasks
        WHERE next_action_rw IS NULL AND completed = FALSE AND deleted_at IS NULL
    """).fetchone()[0]
    if empty_kiro > 5:
        alerts.append(f"⚠️ ENRICHMENT GAP: {empty_kiro} tasks missing Kiro_RW context")
    if empty_next > 5:
        alerts.append(f"⚠️ ENRICHMENT GAP: {empty_next} tasks missing Next_Action_RW")

    # Gather stats for digest
    total_incomplete = con.execute("SELECT COUNT(*) FROM asana.asana_tasks WHERE completed = FALSE AND deleted_at IS NULL").fetchone()[0]
    project_count = con.execute("SELECT COUNT(DISTINCT project_gid) FROM asana.asana_tasks WHERE deleted_at IS NULL AND project_gid IS NOT NULL").fetchone()[0]

    # Bucket distribution (all incomplete, not just Today/Urgent)
    all_buckets = con.execute("""
        SELECT COALESCE(routine_rw, 'Backlog') as bucket, COUNT(*) as cnt,
               GROUP_CONCAT(name, ', ') as names
        FROM asana.asana_tasks
        WHERE deleted_at IS NULL AND completed = FALSE
        GROUP BY COALESCE(routine_rw, 'Backlog')
        ORDER BY bucket
    """).fetchall()

    # Today's tasks
    today_tasks = con.execute("""
        SELECT name, routine_rw, due_on, project_name
        FROM asana.asana_tasks
        WHERE priority_rw = 'Today' AND completed = FALSE AND deleted_at IS NULL
        ORDER BY due_on
    """).fetchall()

    # All overdue
    all_overdue = con.execute(f"""
        SELECT name, project_name, due_on, DATEDIFF('day', due_on, '{TODAY}'::DATE) AS days_overdue
        FROM asana.asana_tasks
        WHERE due_on < '{TODAY}'::DATE AND completed = FALSE AND deleted_at IS NULL
        ORDER BY days_overdue DESC
    """).fetchall()

    con.close()

    return {
        'total_incomplete': total_incomplete,
        'project_count': project_count,
        'all_buckets': all_buckets,
        'today_tasks': today_tasks,
        'all_overdue': all_overdue,
        'alerts': alerts,
        'upsert_count': upsert_count,
        'empty_kiro': empty_kiro,
        'empty_next': empty_next,
    }


def write_digest(stats):
    """Write asana-digest.md"""
    caps = {'Sweep': 5, 'Core': 4, 'Engine Room': 6, 'Admin': 3, 'Wiki': 99, 'Backlog': 99}
    emojis = {'Sweep': '🧹', 'Core': '🎯', 'Engine Room': '⚙️', 'Admin': '📋', 'Wiki': '📝', 'Backlog': '📦'}

    lines = [
        f"# Asana Digest — {TODAY}",
        "",
        f"Synced: {SYNC_TS} | Tasks: {stats['total_incomplete']} incomplete | Projects: {stats['project_count']}",
        "",
        "## By Routine Bucket",
    ]

    bucket_dict = {r[0]: (r[1], r[2]) for r in stats['all_buckets']}
    for bucket in ['Sweep', 'Core', 'Engine Room', 'Admin', 'Wiki', 'Backlog']:
        cnt, names = bucket_dict.get(bucket, (0, ''))
        cap = caps.get(bucket, 99)
        emoji = emojis.get(bucket, '📦')
        cap_str = f"/{cap}" if cap < 99 else ""
        # Truncate names list
        name_list = names[:200] + '...' if names and len(names) > 200 else (names or 'none')
        lines.append(f"- {emoji} {bucket}: {cnt}{cap_str} — {name_list}")

    lines.extend(["", "## Today's Tasks (Priority_RW = Today)"])
    if stats['today_tasks']:
        for t in stats['today_tasks']:
            due_str = f" (due {t[2]})" if t[2] else ""
            proj_str = f" [{t[3]}]" if t[3] else ""
            lines.append(f"- {t[0]}{due_str}{proj_str}")
    else:
        lines.append("- (none)")

    lines.extend(["", "## Overdue"])
    if stats['all_overdue']:
        for t in stats['all_overdue']:
            lines.append(f"- {t[0]} — {t[3]}d overdue (due {t[2]}, project: {t[1] or 'My Tasks'})")
    else:
        lines.append("- (none)")

    lines.extend(["", "## Coherence Alerts"])
    if stats['alerts']:
        for a in stats['alerts']:
            lines.append(f"- {a}")
    else:
        lines.append("- ✅ DuckDB ↔ Body coherence check passed.")

    lines.extend(["", f"## Enrichment Gaps",
                   f"- Kiro_RW missing: {stats['empty_kiro']} tasks",
                   f"- Next_Action_RW missing: {stats['empty_next']} tasks"])

    digest_path = os.path.expanduser("~/shared/context/intake/asana-digest.md")
    os.makedirs(os.path.dirname(digest_path), exist_ok=True)
    with open(digest_path, 'w') as f:
        f.write('\n'.join(lines) + '\n')
    print(f"Wrote digest to {digest_path}")
    return '\n'.join(lines)


def write_snapshot_json(stats):
    """Write morning snapshot JSON"""
    snapshot = {
        'date': TODAY,
        'synced_at': SYNC_TS,
        'total_incomplete': stats['total_incomplete'],
        'project_count': stats['project_count'],
        'buckets': {r[0]: r[1] for r in stats['all_buckets']},
        'today_tasks': [{'name': t[0], 'routine': t[1], 'due_on': str(t[2]) if t[2] else None, 'project': t[3]} for t in stats['today_tasks']],
        'overdue': [{'name': t[0], 'project': t[1], 'due_on': str(t[2]), 'days_overdue': t[3]} for t in stats['all_overdue']],
        'alerts': stats['alerts'],
    }
    json_path = os.path.expanduser("~/shared/context/active/asana-morning-snapshot.json")
    os.makedirs(os.path.dirname(json_path), exist_ok=True)
    with open(json_path, 'w') as f:
        json.dump(snapshot, f, indent=2, default=str)
    print(f"Wrote snapshot to {json_path}")


if __name__ == '__main__':
    print(f"=== Asana → DuckDB Full Sync — {TODAY} ===")
    stats = run_sync()
    digest = write_digest(stats)
    write_snapshot_json(stats)
    print("\n=== DIGEST PREVIEW ===")
    print(digest)
