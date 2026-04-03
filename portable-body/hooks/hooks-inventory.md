# Hooks Inventory — Portable Reference

These are the automation hooks that run in the AgentSpaces environment. They're platform-specific (Kiro hook format), but the INTENT is portable. Any AI platform can implement these as equivalent workflows.

Last synced: 2026-04-02

---

## AM Hooks (3 sequential — each feeds the next)

### AM-1: Ingest (`am-1-ingest.kiro.hook`)
- **Trigger:** Manual (daily, first thing)
- **Intent:** Pure data collection — no decisions, no drafting, no organ writes
- **Steps:**
  1. Slack scan — channels (section-based depth), DMs, proactive search, relevance filter
  2. Asana sync — scan Auto-Comms folder, match to To-Do tasks
  3. Email scan — catalog unread emails with urgency tiers
  4. DuckDB writes — batch-write all messages to conversation database
- **Output:** intake/ files (Slack digest, email triage, Asana sync results, rsw-channel drops)
- **Context loaded:** spine.md, current.md, slack-channel-registry.json, slack-scan-state.json, asana-sync-protocol.md
- **~5 min. Failure here doesn't block AM-2/AM-3 (they use yesterday's data).**

### AM-2: Triage + Draft (`am-2-triage.kiro.hook`)
- **Trigger:** Manual (after AM-1)
- **Intent:** Process AM-1 intake into actionable state — updated tasks, drafted replies
- **Steps:**
  1. Process intake files from AM-1 → update hands.md (new tasks, completed, context updates)
  2. Update amcc.md streak status
  3. Draft email replies in Richard's voice (Outlook drafts only — never send)
  4. Update rw-tracker.md
- **Output:** Fresh hands.md, amcc.md, email drafts in Outlook
- **Context loaded:** spine.md, current.md, memory.md, writing-style, hands.md, amcc.md, rw-tracker.md, intake/ files
- **~5 min. Key rule: NEVER call email_reply/send/forward — only email_draft.**

### AM-3: Brief + Blocks (`am-3-brief.kiro.hook`)
- **Trigger:** Manual (after AM-2)
- **Intent:** Generate all morning outputs from AM-1 and AM-2 data
- **Steps:**
  1. Daily brief — dark navy HTML email to prichwil@amazon.com (auto-send)
  2. Slack daily brief post to rsw-channel (condensed, ≤300 words)
  3. Focus update post to rsw-channel (task changes, ≤150 words)
  4. Dashboard update — edit pinned message in rsw-channel
  5. Calendar blocks — 4 focus blocks (Sweep/Core/Engine Room/Admin)
  6. Proactive draft suggestions — unanswered messages 24+ hours old
  7. (Fridays) Calibration — nervous system loops, weekly retrospective
- **Output:** Brief email, Slack posts, updated dashboard, calendar blocks
- **Context loaded:** Full body system (body, spine, org-chart, trainer, prioritization, brain, eyes, device, gut, tracker, hands, amcc, scan state, experiments)
- **~5 min. Morning routine experiments engine runs adaptive A/B tests on brief format.**

## EOD Hooks (2 sequential)

### EOD-1: Meeting Sync (`eod-1-meeting-sync.kiro.hook`)
- **Trigger:** Manual (end of day, after meetings)
- **Intent:** Multi-source meeting ingestion into the system
- **Steps:**
  1. Pull — Hedy sessions, Amazon Meeting Summaries, email threads (all reads before writes)
  2. Analyze — speaking share, hedging, strategic contributions, action items, relationship updates
  3. Update meetings/ series files — one file per recurring meeting, synthesize ONE clean entry
  4. Update organs — memory (relationships only), nervous system (communication patterns), current.md (pending actions)
  5. Audit Hedy contexts — keep session/topic contexts fresh
- **Data sources:** Hedy MCP, Outlook Auto-meeting folder, email threads
- **~5 min. meetings/ series files are the single source of truth.**

### EOD-2: System Refresh (`eod-2-system-refresh.kiro.hook`)
- **Trigger:** Manual (end of day, after EOD-1)
- **Intent:** Maintain organs, cascade changes, run experiments, sync to git
- **Steps:**
  1. Maintenance — refresh ground truth, process intake/, route Slack signals to organs
  2. Dashboard + focus update — edit pinned message, post task changes
  3. Cascade — propagate changes to all 11 organs (skip if updated <48h + minor)
  4. Enrichments — weekly relationship refresh (Fri), wiki candidates (weekly), monthly synthesis (1st), quarterly audit (90d)
  5. Experiments — Karpathy-governed (delegated to subagent), A/B/C blind eval
  6. Suggestions — up to 3 proposals (must connect to Five Levels, be measurable, reversible)
  7. Housekeeping + git sync — deduplicate MCP autoApprove, push to GitHub
- **Protocol:** heart.md is the source of truth for experiments
- **~10 min. Self-audit verifies cascade completeness and coherence.**

## Always-On Guards

### Guard: Email (`block-email-send.kiro.hook`)
- **Trigger:** Automatic (preToolUse — before any email send/reply/forward)
- **Rule:** All recipients must be Richard's own addresses. Others require explicit approval. If denied, save as draft.

### Guard: Calendar (`block-calendar-invite.kiro.hook`)
- **Trigger:** Automatic (preToolUse — before any calendar event creation)
- **Rule:** Personal blocks and Richard-only events allowed. External attendees require explicit approval.

## On-Demand Hooks

### WBR: Weekly Callouts (`wbr-callout-pipeline.kiro.hook`)
- **Trigger:** Manual (weekly, for WBR prep)
- **Intent:** Full 10-market callout pipeline: ingest → analyst → writer → blind review → correction loop
- **Markets:** AU, MX (hands-on depth), US, CA, JP, UK, DE, FR, IT, ES

### PS Audit (`ps-daily-automation.kiro.hook`)
- **Trigger:** Manual (on demand)
- **Intent:** Paid search audit pipeline + progress charts generation
- **Command:** `python -m paid_search_audit.cli --config paid_search_audit/config.json --output-dir ./reports`

### Agent Bridge Sync (`agent-bridge-sync.kiro.hook`)
- **Trigger:** Manual (on demand, or as part of Friday EOD-2)
- **Intent:** Sync portable-body/ to GitHub, send snapshot email
- **Doomsday mentality:** When in doubt, include the file.

### SharePoint Sync (`sharepoint-sync.kiro.hook`)
- **Trigger:** Manual (on demand)
- **Intent:** Wiki articles → .docx → OneDrive → SharePoint
- **Command:** `python3 ~/shared/tools/sharepoint-sync/cli.py --mode directory`

---

## Portability Note

These hooks are Kiro-specific JSON format. On a different platform:
- AM-1/2/3 → implement as 3 sequential prompts/workflows with increasing context
- EOD-1/2 → implement as 2 sequential prompts (meeting ingestion then maintenance)
- Safety Guards → implement as pre-send checks in whatever email/calendar tool is available
- On-demand hooks → implement as manual-trigger workflows
- The INTENT of each hook is what matters, not the JSON format
- Key design principle: each hook loads only the context it needs. Failure is isolated — AM-1 failing doesn't kill the brief.
