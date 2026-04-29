# Email/Calendar Sync Error — 2026-04-27

**Subagent:** C (Email + Calendar Ingestion)
**Status:** FAILED — Outlook MCP auth expired

## Failure

All Outlook MCP endpoints returned HTTP 401 from Midway IDP:
- `email_search` (query="*", startDate=2026-04-25, endDate=2026-04-27) → 401
- `email_inbox` (limit=5) → 401
- `calendar_view` (start_date=04-27-2026, view=day) → 401

Error message from MCP: *"Request to IDP URL ... did not redirect. Status code: 401. You may need to authenticate by running mwinit."*

## Impact

- **signals.emails** — no new rows ingested since 2026-04-25 18:59 UTC
- **main.calendar_events** — today's events (2026-04-27) not ingested
- **ops.data_freshness** — both sources marked `is_stale = true` to warn downstream consumers (am_brief, signal_routing, daily_tracker)

## Resolution

Richard needs to run `mwinit` (Midway auth refresh) before Subagent C can run successfully. Once auth is refreshed, re-run the email+calendar ingestion protocol — it will pick up from 2026-04-25 automatically via the data_freshness bookmark.

## Scan window attempted

- startDate: 2026-04-25 (last successful scan)
- endDate: 2026-04-27 (today)
- Expected: ~2 days of emails across all folders + today's calendar
