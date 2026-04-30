# Team Orchestration — How Individual Agents Feed the Whole

**Doc:** 11
**Audience:** Paid Acquisition teammates + their Kiro agents
**Status:** FINAL
**Last updated:** 2026-04-17

## Environment Awareness (for your agent)

This doc is the most environment-dependent in the kit. Orchestration depends on persistent shared storage and reliable hook execution, which means:

| Capability | Remote IDE (DevSpaces) | Local IDE (laptop Kiro) | AgentSpaces (chat) |
|---|---|---|---|
| Write to `~/shared/` intake folders | ✅ Native | ⚠️ Via OneDrive sync if mirrored | ⚠️ Via SharePoint MCP to synced intake |
| Run librarian/curator hooks on schedule | ✅ Container persists | ❌ Laptop sleep kills reliability | ❌ No hooks |
| Subscribe to event log (`~/shared/events.jsonl`) | ✅ | ⚠️ Only if synced | ⚠️ Read-only via MCP |
| Participate as full contributor (write drafts, append events) | ✅ | ⚠️ Partial | ⚠️ Drafts only, events need Remote IDE or CLI |
| Serve as librarian for a shared domain | ✅ Only here | ❌ | ❌ |

**Tell the user in plain language:**
- **Remote IDE:** *"I can fully contribute to the team's shared work here
- **Local IDE:** *"I can draft callouts and reports on your laptop, and they'll sync up to the team's shared folder through OneDrive. Scheduled background tasks need the Remote IDE to run reliably."*
- **AgentSpaces:** *"I can help you draft things here, but I can't save them directly to the team's shared folder. For contributing drafts and participating in team-wide coordination, open your Remote IDE and ask me there."*

---

Individual Kiro agents are powerful on their own. A team of Kiro agents contributing to shared artifacts multiplies that

**This is the most ambitious doc in the kit.** Don't start here. Get comfortable with the other docs first, then layer orchestration once 3+ teammates are actively using Kiro.

## The core pattern: intake → librarian → canonical

Every shared artifact follows the same flow:

```
Individual agents Intake folder Librarian agent Canonical location
 ──▶ ──▶ ──▶
```

- Individual agents drop **drafts** into an **intake** folder.
- A **librarian** reviews, edits, and promotes to canonical.
- Nobody's agent writes directly to canonical. Ever.

This prevents the "everyone writes everywhere" chaos while still letting individual contributions flow up.

## Canonical shared artifacts

| Artifact | Canonical location | Intake location | Librarian |
|---|---|---|---|
| Weekly market callouts | `~/shared/callouts/YYYY/WXX/` | `~/shared/callouts/intake/` | Richard (or designated callout reviewer) |
| Ad-hoc reports & data briefs | `~/shared/reports/YYYY-MM-DD-<slug>/` | `~/shared/reports/intake/` | Richard |
| Wiki article edits | `~/shared/wiki/<path>` | `~/shared/wiki/intake/suggestions/` | Wiki librarian |
| New wiki articles | `~/shared/wiki/agent-created/...` | `~/shared/wiki/intake/new-articles/` | Wiki editor → writer pipeline |
| Meeting recaps | `~/shared/wiki/meetings/` | `~/shared/wiki/intake/meetings/` | Meetings curator |
| Market state-file updates | `~/shared/wiki/state-files/<market>-state.md` | direct edits OK (single-owner) | Owner of the market |

## Contribution patterns

### Contributing a weekly callout

```
1. User: "Write this week's AU callout."
2. Agent:
 - Loads callout-principles.md and richard-style-wbr.md
 - Pulls W16 data from pacing/forecast sources
 - Drafts following weekly-market-callout template
 - Self-reviews
3. Agent saves draft to: ~/shared/callouts/intake/2026-W16-AU-<alias>.md
4. Includes front-matter:
 ---
 market: AU
 week: 2026-W16
 submitted_by: <alias>
 submitted_at: 2026-04-18
 status: draft
 ---
5. Pings librarian.
6. Librarian reviews, edits, promotes to ~/shared/callouts/2026/W16/AU.md.
```

### Contributing an ad-hoc report

```
1. User: "I looked into the JP CPC spike
2. Agent drafts the analysis as markdown.
3. Saves to: ~/shared/reports/intake/2026-04-17-jp-cpc-spike-<alias>/
 - report.md
 - data.xlsx
 - chart.png
4. Front-matter in report.md identifies author, date, topic.
5. Librarian promotes to ~/shared/reports/2026-04-17-jp-cpc-spike/ if quality bar met.
```

### Contributing a meeting recap

```
1. Agent is given a Hedy session or a user's meeting notes.
2. Drafts a recap following the meeting recap template.
3. Saves to: ~/shared/wiki/intake/meetings/<YYYY-MM-DD>-<slug>-<alias>.md
4. Meeting curator merges into the canonical series file at ~/shared/wiki/meetings/.
```

## The event log pattern

Beyond discrete artifacts, the team uses a shared event stream for ambient signals. Any agent can write, any agent can read.

**Location:** `~/shared/events.jsonl`.

**Event schema:**

```json
{
 "timestamp": "2026-04-17T19:45:00Z",
 "source_agent": "prichwil",
 "event_type": "test-status-change | pacing-alert | commitment-made | insight | request",
 "topic": "short descriptor",
 "payload": { ... event-specific fields ... },
 "visibility": "team | personal"
}
```

**Common event types:**

- `test-status-change`
- `pacing-alert`
- `commitment-made`
- `insight`
- `request`

**How agents subscribe:**

Morning brief hooks read the last 24h of events and summarize what happened across the team:

```
tail -n 1000 ~/shared/events.jsonl | \
 python3 -c "<parse, filter by timestamp > cutoff, group by event_type, summarize>"
```

Weekly retro hooks do the same on a 7-day window.

**Rules for writing events:**

- One event per discrete happening. Don't pack multiple events in one JSON.
- Use consistent `event_type` values
- Keep `payload` small. Link to docs/reports rather than pasting full content.
- Never write events with `visibility: team` for personal coaching/retrospective content

## The librarian role

Every shared domain has a librarian. Librarians:

- **Review intake items** on a regular cadence.
- **Merge** approved items to canonical, preserving author attribution.
- **Request revisions** for items that don't meet the quality bar
- **Decline** with reason if the item is off-scope or duplicative.
- **Prune** the intake folder so it doesn't rot.

Currently Richard is librarian for callouts, reports, and wiki. As the team scales, domains get delegated.

**Librarian agents (automated)** can handle initial triage — de-dup checking, format validation, front-matter verification

## Avoiding common orchestration failures

- **Don't let intake folders stagnate.** Weekly review, at minimum. Old unreviewed items kill trust.
- **Don't merge drafts without attribution.** Preserve `submitted_by` when promoting to canonical.
- **Don't skip the librarian step for speed.** "I'll just push directly this once" becomes the norm.
## Rollout order

Don't try to stand all of this up at once. Suggested phasing:

1. **Phase 1:** Individual Kiro usage
2. **Phase 2:** Shared read
3. **Phase 3:** Callout intake
4. **Phase 4:** Event log
5. **Phase 5:** Reports + meeting recaps + wiki suggestions
6. **Phase 6:** Distribute librarian roles

## Steering file for orchestration participants

Install at your Kiro steering folder as `orchestration-participant.md` (in `.kiro/steering/` inside your workspace, or `~/.kiro/steering/` for user-level) once Phase 3+ is running:

```markdown
---
inclusion: always
---

# Team Orchestration Rules

When producing a shared artifact (callout, report, meeting recap, wiki suggestion, new wiki article):

1. Never write directly to canonical locations. Always write to the corresponding intake folder.
2. Include front-matter with author alias, date, and artifact type.
3. Notify the librarian when draft is ready for review.
4. Wait for librarian to promote

When subscribing to team state:
- Read `~/shared/events.jsonl` for ambient signals.
- Read canonical artifact folders for authoritative content.

When writing events:
- One discrete event per line.
- Use consistent event_type values.
- Keep payloads small; link to docs instead of pasting.
- Mark personal coaching/retro events with visibility: personal.
```
