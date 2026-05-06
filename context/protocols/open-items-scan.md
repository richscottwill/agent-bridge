---
title: "Open Items Scan Protocol"
type: protocol
status: ACTIVE
owner: Richard Williams
created: 2026-05-06
updated: 2026-05-06
---

# Open Items Scan Protocol

Called by `open-items-reminder.kiro.hook` on every promptSubmit. Externalized 2026-05-06 to reduce per-turn token cost from ~300 to ~30.

## Gate

Check if you've already surfaced open items in this conversation. If yes, skip silently — do not re-run scans, do not output.

If no prior scan in this conversation OR this is the first message of a new conversation OR it has been a long conversation (>3 hours since last scan), execute both scans below and combine results.

## Scan 1 — Recent open items

Read `~/shared/context/intake/session-log.md`. Scan the most recent entries (last 7 days). Include any items that:
- Contain the tag `OPEN`
- Contain the words: `awaiting`, `pending`, `deferred`, `not actioned`, `not yet built`

## Scan 2 — Dated reminders

Scan the ENTIRE `session-log.md` (not just last 7 days) for lines matching `DUE YYYY-MM-DD`. For each match:
- Parse the date
- Today's PT date: `TZ=America/Los_Angeles date +%Y-%m-%d`
- Include if date is within next 14 days from today
- Include as OVERDUE if date is in the past and the entry is not marked `DONE` or `RESOLVED`
- Ignore dates more than 14 days out

## Output format

If either scan finds items, prepend a brief 2-3 line reminder to your response:

```
Open from prior sessions: [item1], [item2]... | Upcoming: [DUE YYYY-MM-DD item]...
```

Keep it compact — one line per item, newest/nearest first.

If nothing is open and no dates are in-window, skip silently.

## Non-blocking

This is a background check. Do NOT let it delay or block Richard's actual request. If the scans fail, skip silently rather than error.
