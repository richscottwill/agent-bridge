# Hooks Inventory — Portable Reference

These are the automation hooks that run in the AgentSpaces environment. They're platform-specific (Kiro hook format), but the INTENT is portable. Any AI platform can implement these as equivalent workflows.

Last synced: 2026-03-27

---

## 1. Morning Routine (`rw-morning-routine.kiro.hook`)
- **Trigger:** Manual (one-click, daily)
- **Intent:** Run Richard's complete morning workflow in 4 steps (5 on Fridays)
- **Steps:**
  1. Asana Sync — scan email for Asana notifications, match to To-Do tasks, update
  2. Draft Unread Replies — scan inbox, triage, draft replies in Richard's voice
  3. To-Do Refresh + Daily Brief — refresh task lists, build daily brief email, send to self
  4. Calendar Blocks — create 4 focus blocks (Sweep/Core/Engine Room/Admin) in calendar gaps
  5. (Fridays) Calibration — run nervous system loops, weekly retrospective, portable-body sync
- **Context loaded:** body.md, spine.md, org-chart.md, writing-style, current.md, memory.md, meetings/README.md, amcc.md, then trainer, prioritization, device, gut, tracker, brain, eyes, hands
- **Key rules:** Full task management agency (move/create/delete/update tasks freely), backlog is ONLY for blocked/future items, hard thing always due TODAY

## 2. Meeting Sync (`hedy-meeting-sync.kiro.hook`)
- **Trigger:** Manual (end of day, after meetings)
- **Intent:** Ingest meeting transcripts and notes into the system
- **Steps:**
  1. Pull — get Hedy sessions, Amazon Meeting Summaries, email threads
  2. Analyze — speaking share, hedging, strategic contributions, action items
  3. Update meetings/ series files — one file per recurring meeting
  4. Update organs — memory (relationships), nervous system (communication patterns), current.md
  5. Audit Hedy contexts — keep session/topic contexts fresh
- **Data sources:** Hedy MCP (18 tools), Outlook Auto-meeting folder, email threads

## 3. System Refresh / Autoresearch Loop (`run-the-loop.kiro.hook`)
- **Trigger:** Manual (end of day, after meeting sync)
- **Intent:** Maintain organs, cascade changes, optionally run 1 experiment
- **Steps:**
  1. Maintenance — refresh ground truth from email/calendar, process intake/
  2. Cascade — propagate changes to all 9+ organs
  3. Experiment (optional) — Karpathy-governed, dual blind eval
  4. Suggestions — up to 3 proposals for Richard
  5. Git sync — push changes to GitHub
- **Protocol:** heart.md is the source of truth

## 4. Email Safety Guard (`block-email-send.kiro.hook`)
- **Trigger:** Automatic (before any email send/reply/forward)
- **Intent:** Prevent accidental emails to external recipients
- **Rule:** All recipients must be Richard's own addresses (prichwil@amazon.com or richscottwill@gmail.com). Any other recipient requires explicit approval.

## 5. Calendar Safety Guard (`block-calendar-invite.kiro.hook`)
- **Trigger:** Automatic (before any calendar event creation)
- **Intent:** Prevent accidental meeting invites to external attendees
- **Rule:** Events with no attendees (personal blocks) or only prichwil are allowed. Any other attendee requires explicit approval.

## 6. PS Daily Audit (`ps-daily-automation.kiro.hook`)
- **Trigger:** Manual (on demand)
- **Intent:** Run paid search audit pipeline — pull data, analyze, generate reports
- **Command:** `python -m paid_search_audit.cli --config paid_search_audit/config.json --output-dir ./reports`

## 7. Dashboard Update (`update-dashboard.kiro.hook`)
- **Trigger:** Manual (on demand)
- **Intent:** Regenerate progress charts HTML dashboard from organ data
- **Command:** `python3 ~/shared/tools/progress-charts/generate.py`
- **Output:** Standalone HTML dashboard (Chart.js, no dependencies)

## 8. SharePoint Sync (`sharepoint-sync.kiro.hook`)
- **Trigger:** Manual (on demand)
- **Intent:** Sync wiki articles to SharePoint via OneDrive
- **Steps:** Dry-run first → show changes → confirm → live sync
- **Command:** `python3 ~/shared/tools/sharepoint-sync/cli.py --mode directory`

---

## Portability Note

These hooks are Kiro-specific JSON format. On a different platform:
- Morning Routine → implement as a multi-step prompt/workflow
- Meeting Sync → implement as a transcript ingestion pipeline
- System Refresh → implement as a maintenance + experimentation loop
- Safety Guards → implement as pre-send checks in whatever email/calendar tool is available
- The INTENT of each hook is what matters, not the JSON format
