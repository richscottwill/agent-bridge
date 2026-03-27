#!/usr/bin/env python3
"""Send the daily brief to Richard via Outlook."""
import json, os

body_html = """<html><body>
<h1>Daily Brief — Wednesday, March 18, 2026</h1>

<h2>TRAINER CHECK-IN</h2>
<p>You have 5 overdue admin tasks sitting in a list capped at 3. Some are 17 days old. This is the #1 thing to fix today — not the AEO POV, not the Adi sync, not the LiveRamp call. You cannot do strategic work while admin debt is compounding and eroding your credibility with Finance and leadership.</p>
<p>The admin block is ~80 minutes of work. That's it. Block 9:00-10:30am and clear all five. Then you earn the right to work on the AEO POV this afternoon.</p>
<p>Week 3 of zero strategic artifacts shipped starts tomorrow if you don't make progress on the AEO POV today. The recording is available. You have a 2-hour window after the Adi sync. Use it.</p>
<p>Task balance today: 5 admin (all overdue), 4 execution, 2 strategic. The ratio is broken. Clear admin → execute on MX/AU → write the AEO POV. In that order.</p>
<p>Pillar check:</p>
<ul>
<li>WW Testing: Andrew active in OP1 Loop doc today &#x2705; — acknowledge and check his section</li>
<li>AU: URL migration ready to execute (Alexis mapping + Lena full switch). NB testing proposal pending. &#x2705;</li>
<li>MX: Auto page due 3/20 (Vijeth footer pending). Beauty campaign needs Lorena confirmation. &#x2705;</li>
</ul>
<p>Backlog flags:</p>
<ul>
<li>AI Max test design has been untouched since creation. Due 3/28 — 10 days.</li>
<li>"Get Media to reference our SIM" is 27 days overdue. Either do it or kill it.</li>
</ul>
<p>New pattern: 10 Microsoft Advertising "account paused" emails came in yesterday. You didn't notice. Are these accounts active? If yes, fire. If no, close them.</p>

<h2>TODAY'S MEETINGS</h2>
<ul>
<li><b>7:30am PT</b> — Respond to emails/Slack (recurring). Triage: Andrew Testing Doc mention, Sharon Prime Day intake, MS Advertising paused.</li>
<li><b>9:30am PT</b> — Amazon Business x LiveRamp Monthly Status (TENTATIVE &#x26A0;&#xFE0F;). You haven't responded. Contributor or observer? If observer, decline and use time for admin block.</li>
<li><b>12:00pm PT</b> — Richard/Adi sync. Adi OOO tomorrow+Thursday. Last touchpoint this week. Bring: AEO POV outline, OP1 section check, EU5 LP rollout.</li>
<li><b>3:00pm PT</b> — Respond to emails/Slack (recurring).</li>
</ul>
<p><b>Tomorrow:</b> Brandon Deep Dive &amp; Debate 9am (come with something to present), ACQ Promo OHs 10am, Yun 1:1 11am.</p>

<h2>TOP 3 PRIORITIES TODAY</h2>
<ol>
<li><b>Clear the admin overflow (5 tasks, ~80 min)</b> — Block 9:00-10:30am. Kingpin Goals first (30 min). PAM US PO (15 min). Batch three R&amp;O items (35 min). Admin list must be at 3/3 or below by lunch.</li>
<li><b>Write AEO POV outline</b> — After Adi sync, 1:00-3:00pm. Even rough structure + key arguments = progress. Breaks the 2.5-week artifact drought.</li>
<li><b>Respond to Andrew Wirtz on Testing Doc</b> — Quick win. Acknowledge Loop mention, check contribution, reply. Keeps OP1 momentum.</li>
</ol>

<h2>DUE THIS WEEK (by 3/21)</h2>
<table border="1" cellpadding="4" cellspacing="0">
<tr><th>Task</th><th>Due</th><th>Status</th><th>Est. Time</th></tr>
<tr><td>Kingpin Goals — MX Jan/Feb/Mar</td><td>3/17 (OVERDUE)</td><td>NOT STARTED</td><td>30 min</td></tr>
<tr><td>PAM US PO</td><td>3/1 (17 DAYS OVERDUE)</td><td>NOT STARTED</td><td>15 min</td></tr>
<tr><td>FY26 March RO budget input</td><td>3/10 (8 DAYS OVERDUE)</td><td>NOT STARTED</td><td>15 min</td></tr>
<tr><td>PAM R&amp;O input</td><td>3/10 (8 DAYS OVERDUE)</td><td>NOT STARTED</td><td>10 min</td></tr>
<tr><td>R&amp;O for MX/AU</td><td>3/10 (8 DAYS OVERDUE)</td><td>NOT STARTED</td><td>10 min</td></tr>
<tr><td>WW redirect — Adobe Ad Cloud</td><td>3/17 (OVERDUE)</td><td>NOT STARTED</td><td>30 min</td></tr>
<tr><td>Confirm MX Beauty with Lorena</td><td>3/17 (OVERDUE)</td><td>NOT STARTED</td><td>5 min</td></tr>
<tr><td>Triage 4 overdue Asana tasks</td><td>3/17 (OVERDUE)</td><td>NOT STARTED</td><td>15 min</td></tr>
<tr><td>Write AEO POV (1-pager)</td><td>3/21</td><td>NOT STARTED</td><td>2-3 hrs</td></tr>
<tr><td>Delegate MX invoicing to Carlos</td><td>3/21</td><td>NOT STARTED</td><td>30 min</td></tr>
<tr><td>MX Auto page — Vijeth footer</td><td>3/20</td><td>WAITING on Vijeth</td><td>0 (blocked)</td></tr>
<tr><td>Make changes to AU/MX/PAM</td><td>3/14 (4 DAYS OVERDUE)</td><td>NOT STARTED</td><td>45 min</td></tr>
</table>

<h2>HEADS UP</h2>
<ul>
<li>Brandon "Deep Dive &amp; Debate" tomorrow 9am PT. AEO POV outline would be a strong thing to present.</li>
<li>Adi OOO 3/19-20. Get what you need in today's sync.</li>
<li>MX Auto page due 3/20 — ping Vijeth on footer if no response by EOD.</li>
<li>Sharon Serene Prime Day 2026 intake — read today, decide if PS has a role.</li>
<li>Andrew's Testing Doc activity — good OP1 momentum. Reply today.</li>
<li>MS Advertising paused accounts (10 notifications) — quick triage needed.</li>
</ul>

<h2>QUICK WINS (&lt; 15 min each)</h2>
<ul>
<li>Reply to Andrew on Testing Doc Loop mention (5 min)</li>
<li>Send MX Beauty confirmation to Lorena — draft ready (5 min)</li>
<li>Decide on LiveRamp meeting — accept or decline (2 min)</li>
<li>Triage Sharon Prime Day email (5 min)</li>
<li>Triage MS Advertising paused notifications (10 min)</li>
</ul>
</body></html>"""

req = json.dumps({
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
        "name": "email_send",
        "arguments": {
            "to": ["prichwil@amazon.com"],
            "subject": "Daily Brief \u2014 Wednesday, March 18, 2026",
            "body": body_html
        }
    }
})

cmd = f"echo '{req}' | timeout 15 aws-outlook-mcp 2>/dev/null"
result = os.popen(cmd).read().strip()
if result:
    data = json.loads(result)
    if "result" in data:
        print("Email sent successfully.")
    elif "error" in data:
        print(f"Error: {data['error']}")
    else:
        print(f"Unexpected: {result[:300]}")
else:
    print("No response from MCP")
