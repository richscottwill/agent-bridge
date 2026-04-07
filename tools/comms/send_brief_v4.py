#!/usr/bin/env python3
import json, os

body = "<html><body>"
body += "<h1>Daily Brief - Wed March 18 2026</h1>"
body += "<h2>TRAINER CHECK-IN</h2>"
body += "<p>5 overdue admin tasks in a list capped at 3. Some 17 days old.</p>"
body += "<p>Block 9-10:30am. Clear all five (~80 min). Then AEO POV.</p>"
body += "<p>Week 3 of zero artifacts starts tomorrow without AEO progress.</p>"
body += "<h2>MEETINGS</h2>"
body += "<p>9:30am LiveRamp (TENTATIVE-decide). 12pm Adi sync (OOO tmrw).</p>"
body += "<p>Tomorrow: Brandon Deep Dive 9am, Promo OHs 10am, Yun 11am.</p>"
body += "<h2>TOP 3</h2>"
body += "<p>1. Admin overflow 5 tasks ~80min. 2. AEO POV outline 1-3pm.</p>"
body += "<p>3. Reply Andrew Testing Doc 5min.</p>"
body += "<h2>OVERDUE</h2>"
body += "<p>Kingpin MX 1d. PAM PO 17d. FY26 RO 8d. PAM RO 8d. MX/AU RO 8d.</p>"
body += "<p>WW redirect 1d. MX Beauty 1d. Asana triage 1d. AU/MX changes 4d.</p>"
body += "<p>F90 SIM 27d.</p>"
body += "<h2>HEADS UP</h2>"
body += "<p>Brandon Deep Dive tmrw-bring AEO outline. Adi OOO 3/19-20.</p>"
body += "<p>MX Auto page 3/20-ping Vijeth. Sharon PrimeDay intake. </p>"
body += "<p>MS Advertising 10x paused-triage. Andrew OP1 doc-reply.</p>"
body += "<p>Full brief at ~/shared/wiki/research/daily-brief-latest.md</p>"
body += "</body></html>"

req = json.dumps({
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
        "name": "email_send",
        "arguments": {
            "to": ["prichwil@amazon.com"],
            "subject": "Daily Brief - Wed March 18 2026",
            "body": body
        }
    }
})

# Write to file, then use shell redirect which worked for todo pulls
tmpfile = os.path.expanduser("~/shared/context/intake/_req.json")
with open(tmpfile, "w") as f:
    f.write(req)

result = os.popen(
    "aws-outlook-mcp < " + tmpfile + " 2>/dev/null"
).read().strip()

if result:
    try:
        data = json.loads(result)
        if "result" in data:
            print("EMAIL SENT OK")
        elif "error" in data:
            print("ERROR: " + json.dumps(data["error"])[:200])
        else:
            print("UNEXPECTED: " + result[:200])
    except Exception as ex:
        print("PARSE FAIL: " + str(ex))
        print(result[:200])
else:
    print("NO RESPONSE")
