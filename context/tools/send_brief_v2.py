#!/usr/bin/env python3
"""Send daily brief via MCP using file-based stdin to avoid shell escaping issues."""
import subprocess, json, os, tempfile

body_html = "<html><body>"
body_html += "<h1>Daily Brief — Wednesday, March 18, 2026</h1>"

body_html += "<h2>TRAINER CHECK-IN</h2>"
body_html += "<p>You have 5 overdue admin tasks sitting in a list capped at 3. Some are 17 days old. This is the #1 thing to fix today. You cannot do strategic work while admin debt is compounding.</p>"
body_html += "<p>The admin block is ~80 minutes of work. Block 9:00-10:30am and clear all five. Then you earn the right to work on the AEO POV this afternoon.</p>"
body_html += "<p>Week 3 of zero strategic artifacts starts tomorrow if you dont make progress on the AEO POV today.</p>"
body_html += "<p>Task balance: 5 admin (all overdue), 4 execution, 2 strategic. Clear admin first, then execute, then write.</p>"
body_html += "<p>Pillars: WW Testing (Andrew active in OP1 doc), AU (URL migration ready), MX (Auto page due 3/20, Beauty needs Lorena). All represented.</p>"
body_html += "<p>Backlog: AI Max test design untouched (due 3/28). Get Media to reference SIM is 27 days overdue.</p>"
body_html += "<p>New: 10 MS Advertising account paused emails. Triage today.</p>"

body_html += "<h2>MEETINGS</h2>"
body_html += "<ul>"
body_html += "<li>7:30am PT - Email/Slack triage</li>"
body_html += "<li>9:30am PT - LiveRamp Monthly Status (TENTATIVE - decide: attend or decline)</li>"
body_html += "<li>12:00pm PT - Richard/Adi sync (Adi OOO tomorrow - last chance this week)</li>"
body_html += "<li>3:00pm PT - Email/Slack</li>"
body_html += "</ul>"
body_html += "<p>Tomorrow: Brandon Deep Dive 9am, ACQ Promo OHs 10am, Yun 1:1 11am</p>"

body_html += "<h2>TOP 3 PRIORITIES</h2>"
body_html += "<ol>"
body_html += "<li>Clear admin overflow (5 tasks, ~80 min) - Block 9-10:30am. Kingpin first, then PO, then R&amp;O batch.</li>"
body_html += "<li>Write AEO POV outline - 1-3pm window after Adi sync. Break the artifact drought.</li>"
body_html += "<li>Reply to Andrew on Testing Doc - 5 min quick win. Keeps OP1 momentum.</li>"
body_html += "</ol>"

body_html += "<h2>DUE THIS WEEK</h2>"
body_html += "<table border='1' cellpadding='4'>"
body_html += "<tr><th>Task</th><th>Due</th><th>Est.</th></tr>"
body_html += "<tr><td>Kingpin Goals MX</td><td>3/17 OVERDUE</td><td>30m</td></tr>"
body_html += "<tr><td>PAM US PO</td><td>3/1 (17 DAYS)</td><td>15m</td></tr>"
body_html += "<tr><td>FY26 March RO</td><td>3/10 (8 DAYS)</td><td>15m</td></tr>"
body_html += "<tr><td>PAM R&amp;O</td><td>3/10 (8 DAYS)</td><td>10m</td></tr>"
body_html += "<tr><td>R&amp;O MX/AU</td><td>3/10 (8 DAYS)</td><td>10m</td></tr>"
body_html += "<tr><td>WW redirect Adobe</td><td>3/17 OVERDUE</td><td>30m</td></tr>"
body_html += "<tr><td>MX Beauty Lorena</td><td>3/17 OVERDUE</td><td>5m</td></tr>"
body_html += "<tr><td>Triage Asana tasks</td><td>3/17 OVERDUE</td><td>15m</td></tr>"
body_html += "<tr><td>AEO POV</td><td>3/21</td><td>2-3h</td></tr>"
body_html += "<tr><td>MX invoicing delegation</td><td>3/21</td><td>30m</td></tr>"
body_html += "<tr><td>MX Auto page footer</td><td>3/20</td><td>blocked</td></tr>"
body_html += "<tr><td>AU/MX/PAM changes</td><td>3/14 (4 DAYS)</td><td>45m</td></tr>"
body_html += "</table>"

body_html += "<h2>HEADS UP</h2>"
body_html += "<ul>"
body_html += "<li>Brandon Deep Dive tomorrow 9am - AEO POV outline would be strong to present</li>"
body_html += "<li>Adi OOO 3/19-20 - get what you need today</li>"
body_html += "<li>MX Auto page due 3/20 - ping Vijeth if no footer response by EOD</li>"
body_html += "<li>Sharon Prime Day intake - read and decide today</li>"
body_html += "<li>Andrew Testing Doc activity - reply today, keep OP1 momentum</li>"
body_html += "<li>MS Advertising paused (10x) - quick triage needed</li>"
body_html += "</ul>"

body_html += "<h2>QUICK WINS</h2>"
body_html += "<ul>"
body_html += "<li>Reply to Andrew Testing Doc (5 min)</li>"
body_html += "<li>Send MX Beauty msg to Lorena (5 min)</li>"
body_html += "<li>LiveRamp decision (2 min)</li>"
body_html += "<li>Sharon Prime Day triage (5 min)</li>"
body_html += "<li>MS Advertising triage (10 min)</li>"
body_html += "</ul>"
body_html += "</body></html>"

req = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
        "name": "email_send",
        "arguments": {
            "to": ["prichwil@amazon.com"],
            "subject": "Daily Brief — Wednesday, March 18, 2026",
            "body": body_html
        }
    }
}

# Write JSON to temp file to avoid shell escaping issues
tmpfile = os.path.expanduser("~/shared/context/intake/email_req.json")
with open(tmpfile, "w") as f:
    json.dump(req, f)

# Pipe file to MCP
result = os.popen(f"cat {tmpfile} | timeout 15 aws-outlook-mcp 2>/dev/null").read().strip()
if result:
    data = json.loads(result)
    if "result" in data:
        print("Email sent successfully.")
        print(result[:200])
    elif "error" in data:
        print(f"Error: {json.dumps(data['error'])}")
    else:
        print(f"Unexpected: {result[:300]}")
else:
    print("No response from MCP")
