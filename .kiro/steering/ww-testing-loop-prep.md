---
inclusion: manual
---
[38;5;10m> [0m# WW Testing Loop prep — source-check discipline[0m[0m
[0m[0m
Open this file and review it before you write any WW Testing summary for the Tuesday PS team Loop or any testing status update shared with Brandon, Kate, or the team.
## The one rule

Before making a status claim about any active test — launched X, dialed up Y, delivered N% result, stalled, done — verify it against a source from the last 14 days. If no source exists, write the literal phrase `per prior state file, not reverified this cycle` rather than retaining a stale claim.

This is the rule that would have caught the 2026-04-21 Polaris weblab error ("dialed up 4/6–4/7" when feedback had just been sent hours earlier) and the email overlay error ("no movement 4 weeks" when tickets were moving per Richard).

## Active tests to check

Source: `~/shared/context/protocols/state-file-ww-testing.md` → Test Inventory & Linkage.

13 tests as of 2026-04-21. The protocol file owns the list; Richard maintains it. Read that file first.

## How to verify each claim

For each test you plan to mention, run these checks. Cite what you found inline in the draft (permalink or "per state file, reverified 2026-MM-DD").

1. **Asana status** — if the test has a canonical GID in the Inventory, `GetTaskDetails(task_gid=[GID], opt_fields="kiro_rw,next_action_rw,modified_at,due_on")`. The `modified_at` timestamp is your freshness anchor; `kiro_rw` and `next_action_rw` are the status text.

2. **Slack in last 14 days** — query DuckDB:
   ```sql
   SELECT ts_iso, source_author, source_preview
   FROM signals.signal_tracker
   WHERE (LOWER(signal_preview) LIKE '%polaris%' OR LOWER(topic) LIKE '%polaris%')
     AND last_seen >= CURRENT_DATE - INTERVAL '14 days'
   ORDER BY last_seen DESC LIMIT 5;
   ```
   Substitute the test's Keywords from the Inventory.

3. **Email in last 14 days** — `email_search(query="[keyword]", startDate=[today-14])` via Outlook MCP.

4. **Hedy in last 14 days** — `GetSessions(limit=20)`, scan titles for test keywords.

5. **Project timeline** — DuckDB:
   ```sql
   SELECT created_at, summary, event_type
   FROM main.project_timeline
   WHERE LOWER(project_name) LIKE '%[test keyword]%'
     AND created_at >= CURRENT_DATE - INTERVAL '14 days'
   ORDER BY created_at DESC;
   ```

## Writing the update

- Bullet per test with status verb + next step. Status-plus-next-action format (one-liner), not narrative.
- For Standing Loop tests (Inventory column), they must appear in the output even if nothing changed — write the fresh-or-stale phrase rather than dropping the test.
- Non-Standing-Loop tests only appear if something changed in the last 14 days.
- If Richard explicitly flags a test as personal (e.g., the Testing Approach doc he's writing for Kate), remove it from the team-meeting draft. The WW Testing Loop is for work that touches the team.

## When to update this file

If Rule 4 in `state-file-ww-testing.md` changes, update this file to match. The phrase `per prior state file, not reverified this cycle` is the exact string the state-file-engine protocol expects — don't paraphrase.

Last updated: 2026-04-21 — created after two false-confidence errors in one session. Kill this file if the state file engine hook (AM-Backend Step 2E) ever actually hydrates Appendix I Active Test Dossier with fresh source citations; at that point the dossier becomes the source and this steering file is redundant.
