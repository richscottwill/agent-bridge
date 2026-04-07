import subprocess, json, sys

req = json.dumps({
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
        "name": "todo_tasks",
        "arguments": {
            "operation": "update",
            "listId": "AAMkAGQ5NmQwNGZkLWQ0NTAtNGY4Yy1hNjhlLTY0OTU1N2QzYTBhYwAuAAAAAAArsD3iy-SDRrGkcLnEuZ4GAQCIgJPBFelsQrcja-dZLhI0AADUyESHAAA=",
            "taskId": "AAMkAGQ5NmQwNGZkLWQ0NTAtNGY4Yy1hNjhlLTY0OTU1N2QzYTBhYwBGAAAAAAArsD3iy-SDRrGkcLnEuZ4GBwCIgJPBFelsQrcja-dZLhI0AADUyESHAACIgJPBFelsQrcja-dZLhI0AADWyUZRAAA=",
            "title": "\U0001f534 Prep Brandon ANNUAL REVIEW (Tue 3/17 12:30pm PT)",
            "body": "TRAINER: Brandon renamed the 1:1 to Annual Review. Performance review conversation. Lead with IMPACT. Do Kingpin update and admin block BEFORE this meeting.\n\nWHAT TO DO:\n1. IMPACT: OCI +32K regs, $16.7MM OPS. Ad copy UK +86% CTR. CA LP +187% CVR.\n2. Kingpin Goals - report updated today. MX +32% vs OP2.\n3. Testing Approach doc - Kate meeting Apr 16. Co-present or you lead?\n4. Asana decision - adopt for team or move on?\n5. Q2 priorities - OCI RoW, AI Max, Baloo, F90.\n6. AU - Lena confirmed full Polaris switch. Alexis sent URL mapping today.\n7. Overdue admin - be transparent, show clearing today.\n8. AEO POV - planning to write this week, recording available.",
            "importance": "high"
        }
    }
})

p = subprocess.run(["aws-outlook-mcp"], input=req, capture_output=True, text=True, timeout=30)
print(p.stdout[:500] if p.stdout else "no output")
print(p.stderr[:200] if p.stderr else "", file=sys.stderr)
