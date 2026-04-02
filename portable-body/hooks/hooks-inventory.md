# Hooks Inventory — Portable Reference

These are the automation hooks that run in the AgentSpaces environment. They're platform-specific (Kiro hook format), but the INTENT is portable. Any AI platform can implement these as equivalent workflows.

Last synced: 2026-03-31

---

## 1. Morning Routine (`rw-morning-routine.kiro.hook`)
- **Trigger:** Manual (one-click, daily)
- **Intent:** Run Richard's complete morning workflow in 4 steps (5 on Fridays)
- **Steps:**
  1. Asana Sync — scan email for Asana notifications, match to To-Do tasks, update
  2. Draft Unread Replies — scan inbox, triage, draft replies in Richard's voice
  3. To-Do Refresh + Daily Brief — refresh task lists, build daily brief email (dark navy HTML card layout), send to self
  4. Calendar Blocks — create 4 focus blocks (Sweep/Core/Engine Room/Admin) in calendar gaps
  5. (Fridays) Calibration — run nervous system loops, weekly retrospective
- **Context loaded:** body.md, spine.md, org-chart.md, writing-style, current.md, memory.md, meetings/README.md, amcc.md, then trainer, prioritization, device, gut, tracker, brain, eyes, hands
- **Key rules:** Full task management agency (move/create/delete/update tasks freely), backlog is ONLY for blocked/future items, hard thing always due TODAY, morning routine experiments engine runs adaptive A/B tests on brief format

## 2. Meeting Sync (`hedy-meeting-sync.kiro.hook`)
- **Trigger:** Manual (end of day, after meetings)
- **Intent:** Multi-source meeting ingestion into the system
- **Steps:**
  1. Pull — get Hedy sessions, Amazon Meeting Summaries, email threads (all reads before any writes)
  2. Analyze — speaking share, hedging, strategic contributions, action items, relationship updates
  3. Update meetings/ series files — one file per recurring meeting, synthesize ONE clean entry from all sources
  4. Update organs — memory (relationships only), nervous system (communication patterns), current.md (pending actions)
  5. Audit Hedy contexts — keep session/topic contexts fresh
- **Data sources:** Hedy MCP, Outlook Auto-meeting folder, email threads
- **Key rule:** meetings/ series files are the single source of truth. Organs get only what's specific to their function.

## 3. System Refresh / Autoresearch Loop (`run-the-loop.kiro.hook`)
- **Trigger:** Manual (end of day, after meeting sync)
- **Intent:** Maintain organs, cascade changes, run up to 5 experiments
- **Steps:**
  1. Maintenance — refresh ground truth from email/calendar, process intake/
  2. Cascade — propagate changes to all 11 organs (skip if updated <48h + minor change)
  3. Experiments — Karpathy-governed, up to 5 per run, orchestrated blind eval (4-step: Karpathy → Eval A → Eval B → Karpathy scores)
  4. Suggestions — up to 3 proposals for Richard (must connect to Five Levels, be measurable, be reversible)
  5. Housekeeping + Git sync — deduplicate MCP autoApprove, push to GitHub
- **Protocol:** heart.md is the source of truth
- **Key rules:** Stop on 3 consecutive reverts. Do-no-harm: snapshot before edit, organ-specific accuracy thresholds (Brain/Memory 100%, Eyes/Hands 95%, others 90%)

## 4. WBR Callout Pipeline (`wbr-callout-pipeline.kiro.hook`)
- **Trigger:** Manual (weekly, for WBR prep)
- **Intent:** Full 10-market WBR callout generation with blind review
- **Steps:**
  1. Dashboard Ingestion — ingest xlsx dashboard data via Python ingester
  2. Context Load — body organs, market context files, previous callouts, change logs, emails, meetings
  3. Analysis — invoke market-analyst agent per market (10 sequential runs)
  4. Writing — invoke callout-writer agent per market (10 sequential runs)
  5. Blind Review — invoke callout-reviewer (gets ONLY drafts + data briefs, no analysis)
  6. Correction Loop — markets below 66% confidence get rewritten
- **Markets:** AU, MX (hands-on depth), US, CA, JP, UK, DE, FR, IT, ES
- **Key rules:** Prose = only data-verifiable claims. Note section = internal PS context. Confidence score measures this separation.

## 5. Email Safety Guard (`block-email-send.kiro.hook`)
- **Trigger:** Automatic (before any email send/reply/forward)
- **Intent:** Prevent accidental emails to external recipients
- **Rule:** All recipients must be Richard's own addresses. Any other recipient requires explicit approval. If denied, save as draft instead.

## 6. Calendar Safety Guard (`block-calendar-invite.kiro.hook`)
- **Trigger:** Automatic (before any calendar event creation)
- **Intent:** Prevent accidental meeting invites to external attendees
- **Rule:** Events with no attendees (personal blocks) or only Richard are allowed. Any other attendee requires explicit approval.

## 7. PS Daily Audit (`ps-daily-automation.kiro.hook`)
- **Trigger:** Manual (on demand)
- **Intent:** Run paid search audit pipeline — pull data, analyze, generate reports
- **Command:** `python -m paid_search_audit.cli --config paid_search_audit/config.json --output-dir ./reports`

## 8. Dashboard Update (`update-dashboard.kiro.hook`)
- **Trigger:** Manual (on demand)
- **Intent:** Regenerate progress charts HTML dashboard from organ data
- **Command:** `python3 ~/shared/tools/progress-charts/generate.py`
- **Output:** 5 HTML pages in site/ directory (Chart.js, no external dependencies)

## 9. SharePoint Sync (`sharepoint-sync.kiro.hook`)
- **Trigger:** Manual (on demand)
- **Intent:** Sync wiki articles to SharePoint via OneDrive
- **Steps:** Dry-run first → show changes → confirm → live sync
- **Command:** `python3 ~/shared/tools/sharepoint-sync/cli.py --mode directory`

## 10. Agent Bridge Sync (`agent-bridge-sync.kiro.hook`)
- **Trigger:** Manual (on demand, or as part of Friday calibration)
- **Intent:** Sync portable-body/ directory with the living system, update docs, push to agent-bridge GitHub repo, send snapshot email
- **Steps:**
  1. Read agent-bridge-sync agent definition
  2. Read portable-layer.md manifest
  3. Sync all portable files from source locations
  4. Detect new files that should be included
  5. Update README.md, CHANGELOG.md, SANITIZE.md
  6. Git add, commit, and push to agent-bridge repo (origin main)
  7. Send weekly snapshot email to richscottwill@gmail.com
- **Doomsday mentality:** When in doubt, include the file.

---

## Portability Note

These hooks are Kiro-specific JSON format. On a different platform:
- Morning Routine → implement as a multi-step prompt/workflow with task management API access
- Meeting Sync → implement as a transcript ingestion pipeline with multi-source synthesis
- System Refresh → implement as a maintenance + experimentation loop with blind evaluation
- WBR Callouts → implement as a sequential analyst → writer → reviewer pipeline with confidence scoring
- Safety Guards → implement as pre-send checks in whatever email/calendar tool is available
- Agent Bridge Sync → implement as a file diff + copy + git push + email workflow
- The INTENT of each hook is what matters, not the JSON format
