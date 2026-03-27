#!/usr/bin/env python3
"""Send daily brief via MCP using subprocess with stdin pipe."""
import subprocess, json

body_html = "<html><body>"
body_html += "<h1>Daily Brief - Wednesday, March 18, 2026</h1>"
body_html += "<h2>TRAINER CHECK-IN</h2>"
body_html += "<p>You have 5 overdue admin tasks in a list capped at 3. Some are 17 days old. This is the #1 thing to fix today. Block 9:00-10:30am and clear all five (~80 min). Then AEO POV this afternoon.</p>"
body_html += "<p>Week 3 of zero strategic artifacts starts tomorrow if you dont make progress on the AEO POV today.</p>"
body_html += "<p>Pillars: WW Testing (Andrew active in OP1 doc), AU (URL migration ready), MX (Auto page due 3/20). All represented.</p>"
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
body_html += "<li>Clear admin overflow (5 tasks, ~80 min) - Kingpin first (30m), PO (15m), R+O batch (35m)</li>"
body_html += "<li>Write AEO POV outline - 1-3pm after Adi sync</li>"
body_html += "<li>Reply to Andrew on Testing Doc - 5 min quick win</li>"
body_html += "</ol>"
body_html += "<h2>DUE THIS WEEK</h2>"
body_html += "<table border='1' cellpadding='4'>"
body_html += "<tr><th>Task</th><th>Due</th><th>Est</th></tr>"
body_html += "<tr><td>Kingpin Goals MX</td><td>3/17 OVERDUE</td><td>30m</td></tr>"
body_html += "<tr><td>PAM US PO</td><td>3/1 (17 DAYS)</td><td>15m</td></tr>"
body_html += "<tr><td>FY26 March RO</td><td>3/10 (8 DAYS)</td><td>15m</td></tr>"
body_html += "<tr><td>PAM R+O</td><td>3/10 (8 DAYS)</td><td>10m</td></tr>"
body_html += "<tr><td>R+O MX/AU</td><td>3/10 (8 DAYS)</td><td>10m</td></tr>"
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
body_html += "<li>Andrew Testing Doc activity - reply today</li>"
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

req = json.dumps({
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
        "name": "email_send",
        "arguments": {
            "to": ["prichwil@amazon.com"],
            "subject": "Daily Brief - Wednesday, March 18, 2026",
            "body": body_html
        }
    }
})

# Use subprocess.Popen with direct stdin write
proc = subprocess.Popen(
    ["aws-outlook-mcp"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)
stdout, stderr = proc.communicate(input=req.encode(), timeout=30)

if stdout:
    result = stdout.decode()
    print(f"Response: {result[:300]}")
    try:
        data = json.loads(result)
        if "result" in data:
            print("EMAIL SENT SUCCESSFULLY")
        elif "error" in data:
            print(f"Error: {data['error']}")
    except:
        print(f"Could not parse: {result[:200]}")
else:
    print("No stdout")
    if stderr:
        print(f"Stderr: {stderr.decode()[:200]}")
