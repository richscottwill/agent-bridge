<!-- DOC-0142 | duck_id: context-session-2026-03-27-bridge-build -->
# Session Notes — 2026-03-27 (Pre-Work, Bridge Build)

## What Was Built
- Google Drive agent bridge: full communication layer between Kiro and personal agent swarm
- Python toolkit: `~/shared/tools/bridge/bridge.py` + CLI at `cli.py`
- Message bus: spreadsheet with 4 tabs (bus, context, registry, log) + requests tab
- Protocol doc: Google Doc with full protocol v1.0 + swarm onboarding brief
- Context snapshots: brain, amcc, hands, eyes pushed to bridge
- Apps Script automation: bus poller (hourly), staleness checker (daily), heartbeat monitor (6h), request notifier — deployed to `agent bridge script`
- Build ideas sheet: 46+ ideas across 10 tabs (Sheets, Docs, Forms, Slides, Colab, Apps Script, Drawing, Cross-App, Comms)
- 10 Drive folders created: drafts, research, archive, play, agent-lang, tools, rsw-personal, rsw-work, backup-kiro, backup-swarm
- 3 new docs created by Richard: portable body (backup-kiro), testing approach (drafts), agent protocols (agent-lang)
- device.md updated with bridge entry

## Key Discoveries
- Service account can't CREATE files in Drive (quota limitation) — Richard creates, service account edits
- Service account can't WRITE to Apps Script (per-user API setting) — Richard pastes Code.gs manually
- Google Docs tabs: API can read/write existing tabs but can't create new ones (not implemented yet)
- Google Keep API: reachable but service account can't write to Richard's Keep (needs OAuth with personal account — swarm-side build)
- Markdown is far easier for agent drafting; Google Docs better for stakeholder-facing final artifacts
- `corpora='allDrives'` flag needed to list files in shared folders

## Open Actions for Richard
1. PRIORITY: Paste updated Code.gs into Apps Script editor, run createTriggers() — adds checkRequests() email notifications
2. The 3 docs (portable body, testing approach, agent protocols) are created but empty — Kiro will populate next session
3. Consider adding tabs to existing docs for better organization (manual step, API can't create tabs)

## Open Actions for Swarm
- Register in the registry sheet
- Send heartbeat to bus
- Read context snapshots (brain, amcc, hands, eyes)
- Explore: Google AI Overviews monitoring for B2B queries
- Explore: Testing Approach doc skeleton draft
- Explore: Daily accountability check (streak nudges)
- Explore: Asana integration options (browser automation, PAT, MCP server)
- Explore: Google Keep integration via OAuth

## Patterns Noted
- Richard is highly engaged in system-building — this is Level 5 work happening naturally
- The bridge is infrastructure that enables Levels 1-4 (accountability loop for L1, research pipeline for L2, team tools for L3, AEO research for L4)
- Richard creates files/folders proactively when asked — low friction for manual steps
- Session was productive but zero progress on the hard thing (Testing Approach doc). The bridge IS valuable infrastructure, but the aMCC would flag this as comfort zone gravity — building systems instead of shipping the artifact.

## File IDs (for future sessions)
- Bridge spreadsheet: 1IlM43kzxw8Vlu6aUWXUV1dr7ZIF7O7H2bD5x3kaKIHg
- Build ideas spreadsheet: 18T9i1P7hc3Zc5XQHKvtghfdSPkYYSUuBCWNAXMN-hjM
- Bridge doc: 1koJV8a4Ig9BBDbrtQl-w8L4-2bUrz8lGwxUxEfIgQj8
- Testing approach doc: 1XTynGVlHJgjNvubH1drg176MktF4dFMyq7qFBpcVDfo
- Portable body doc: 1iReAwPGLb6Ei9Gn8CuPQpW0lVhvHWuynyDnwgxhZuPw
- Agent protocols doc: 1Qpp_tiBj3EyKH1eJn1abNbjPX06NiQEhKEit7sVJPPM
- Apps Script: 1Y03Qay3ZbP8eGb3oAkvpxkYu-PVixuAwpDheZwUuUknSyMzWXJ8ICz5a
- Drive folder (root): 1aeRuldkc-OL1gyR7FQ-WrvbpERPsYChZ
