---
title: "Wiki Demand Log"
status: ACTIVE
audience: amazon-internal
owner: Richard Williams
created: 2026-04-30
updated: 2026-04-30
doc-type: reference
auto_appended: true
---

# Wiki Demand Log

> Append-only record of wiki queries / topic searches that did not resolve to an existing article. The `build-wiki-index.py` builder reads this file and surfaces it in the `demand-gap panel` (WS-M05) on the wiki dashboard. Agents and humans both write here.

## Format

One bullet per signal. Metadata in square brackets is optional. Tolerant parser — unknown brackets are ignored.

```
- <query or topic phrase> [count=N] [last=YYYY-MM-DD] [status=open|satisfied|archived] [note=short comment]
```

- **count** — how many times this signal has been observed. Default 1. Increment when you see the same query again rather than appending a new row.
- **last** — date of most recent sighting (YYYY-MM-DD).
- **status** — `open` (default, still no article) / `satisfied` (article now exists — keep row for history) / `archived` (no longer relevant).
- **note** — who asked / where it surfaced / any context useful for the eventual writer.

When an article satisfies a demand signal, flip `status=open` → `status=satisfied` and add `[note=covered-by:<slug>]`. Don't delete the row — the signal's history is valuable.

## Seed entries (from 2026-04-27 audit)

- brand portfolio velocity tracking [count=2] [last=2026-04-22] [status=open] [note=Brandon asked about AU Brand velocity trend twice in two weeks — no single article covers it]
- Polaris LP attribution isolation [count=3] [last=2026-04-28] [status=open] [note=asked by Alexis + Lena + internal agent — CVR impact of LP migration needs its own article]
- AEO / AI Overviews POV for paid search [count=4] [last=2026-04-25] [status=open] [note=Level-4 artifact queued in hard-thing-selection but no wiki entry yet]
- install-to-reg ratio by market [count=2] [last=2026-04-28] [status=open] [note=Peter OP1 sync, Brandon 4/28 1:1 — CPI + install rate + reg conversion triangle]
- forecast calibration methodology [count=1] [last=2026-04-29] [status=open] [note=kiro-server weekly-review R2 findings suggest a methodology doc would help teammates read the calibration panel]

## Append log

<!-- Agents: append new signals below this line. Builder parses the whole file so placement is flexible. -->
