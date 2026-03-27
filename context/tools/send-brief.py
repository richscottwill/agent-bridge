import subprocess, json, sys

body_html = """<html><body>
<h1>Daily Brief — Tuesday, March 17, 2026</h1>

<h2>TRAINER CHECK-IN</h2>
<p>You're on week 3 of zero strategic artifacts shipped. That's the pattern to break this week. The AEO POV is your best shot — the recording dropped yesterday, you attended the session, and nobody else on the team is writing one. Ship it by Friday.</p>
<p>Today is heavy on meetings (All-Amazon Global Meeting 9-11am, Team Meeting noon, Brandon Annual Review 12:30pm, AU Sync 4:30pm). Protect your morning for the admin block and Kingpin update — those need to be DONE before you sit down with Brandon.</p>
<p>Brandon renamed the 1:1 to "Annual Review." That's not casual. Come with impact numbers, not excuses about overdue admin tasks.</p>
<p>Task balance: 5 admin tasks (all overdue), 4 execution tasks, 2 strategic tasks. The ratio is wrong. Clear the admin backlog today so you can spend Wed-Fri on the AEO POV and AU URL migration.</p>
<p>Pillars check:</p>
<ul>
<li>WW Testing: OP1 doc in progress, Kate meeting Apr 16. Represented. &#x2705;</li>
<li>AU: Alexis sent URL mapping TODAY, Lena confirmed full switch. Active. &#x2705;</li>
<li>MX: Auto/Beauty pages due 3/20, Beauty campaign needs Lorena confirmation. Active. &#x2705;</li>
</ul>
<p>Backlog flag: "Write AI Max test design" has been sitting untouched since it was created. It's due 3/28 — that's 11 days. If you don't start by next week, it'll be another missed artifact.</p>

<h2>TODAY'S MEETINGS</h2>
<ul>
<li><b>7:30am PT</b> — Respond to emails/Slack (recurring, 25 min)</li>
<li><b>9:00-11:00am PT</b> — All-Amazon Global Meeting Livestream — Observer only. Watch passively while doing admin block if possible.</li>
<li><b>12:00-1:00pm PT</b> — Weekly Paid Acq Team Meeting (Brandon) — First team meeting since Brandon returned. Listen for Q2 direction signals. Mention AEO POV plan.</li>
<li><b>12:30-1:00pm PT</b> — Richard/Brandon "Annual Review" 1:1 &#x26A0;&#xFE0F; RENAMED. Performance review conversation. Lead with OCI impact (+32K regs, $16.7MM OPS), Kingpin done, Testing doc timeline (Kate Apr 16), AU Polaris switch confirmed, AEO POV this week. Decisions: Asana adoption, Q2 priorities, OP1 co-present or solo.</li>
<li><b>3:00-3:25pm PT</b> — Respond to emails/Slack (recurring)</li>
<li><b>4:30-4:55pm PT</b> — AB AU Paid Search Sync — Alexis, Lena, Harsha. Acknowledge Alexis URL mapping. Confirm full switch plan. Share W11 data. Propose MRO/Trades NB testing.</li>
</ul>
<p><b>Tomorrow:</b> LiveRamp Monthly Status (tentative — decide today), Richard/Adi sync (bring AEO POV outline)</p>

<h2>TOP 3 PRIORITIES TODAY</h2>
<ol>
<li><b>Kingpin Goals update</b> (due TODAY) — Pull Jan + Mar MX data from Andes. Update status from "Proposed" to "On Track." Do FIRST before Brandon meeting.</li>
<li><b>Admin block: R&amp;O + PAM R&amp;O + FY26 March RO + PAM US PO</b> (7-16 days overdue) — Batch all 4 in 45 min. Do BEFORE Brandon meeting.</li>
<li><b>Prep and execute Brandon Annual Review</b> (12:30pm PT) — Lead with impact. OCI numbers, Kingpin done, Testing doc timeline, AU Polaris confirmation, AEO POV plan.</li>
</ol>

<h2>DUE THIS WEEK (by 3/21)</h2>
<table border="1" cellpadding="4" cellspacing="0">
<tr><th>Task</th><th>Due</th><th>Status</th></tr>
<tr><td>Kingpin Goals — MX Jan/Feb/Mar</td><td>3/17 TODAY</td><td>NOT STARTED</td></tr>
<tr><td>R&amp;O + PAM R&amp;O + FY26 RO + PAM US PO</td><td>3/10-3/1 (OVERDUE)</td><td>NOT STARTED</td></tr>
<tr><td>WW redirect — Adobe Ad Cloud reporting</td><td>3/17 TODAY</td><td>NOT STARTED</td></tr>
</table>
</body></html>"""

req = json.dumps({
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
        "name": "email_send",
        "arguments": {
            "to": ["prichwil@amazon.com"],
            "subject": "Daily Brief \u2014 March 17, 2026",
            "body": body_html
        }
    }
})

p = subprocess.run(
    ["aws-outlook-mcp"],
    input=req,
    capture_output=True,
    text=True,
    timeout=30
)
print(p.stdout[:500] if p.stdout else "no stdout")
if p.stderr:
    print("STDERR:", p.stderr[:200], file=sys.stderr)
