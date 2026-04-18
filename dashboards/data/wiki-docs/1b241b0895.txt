# Meeting Notes — Agent Instructions

*Centralized meeting context for all of Richard's recurring and ad-hoc meetings. Each file represents a meeting series, not a single meeting.*

Last updated: 2026-03-26

---

## Purpose

This folder replaces scattered meeting context that was previously in:
- `memory.md` → meeting prep briefs and relationship dynamics
- `archive/hedy-syncs/` → raw Hedy dumps
- Hedy topic overviews → rich but not persisted locally

Now: one file per meeting series. Context compounds over time. Agents read the series file they need.

## Data Sources & Priority

Three sources often cover the same meeting. Each has different strengths:

| Source | Strengths | Weaknesses | Access |
|--------|-----------|------------|--------|
| Hedy MCP | Full transcript, speaker context, what was actually said, decisions in the room, action items assigned live | Noisy raw transcript, sometimes misses quiet speakers, only covers Hedy-recorded meetings | `mcp_hedy_GetSessionDetails(sessionId)` |
| Amazon Meeting Summary | Decent overview, covers Zoom meetings Hedy didn't record, auto-generated | Shallow, misses nuance, no speaker dynamics, sometimes "not enough conversation" | Outlook Auto-meeting folder (folder ID in spine.md) |
| Email threads | Written commitments, stakeholder requests, pre/post-meeting context, agenda items, follow-ups | Scattered across inbox, not always tied to a specific meeting date | Outlook search by subject/sender/date |

### Source Priority (for the same meeting)

```
1. HEDY (primary when available)
   → Use: meeting_minutes + recap for structure
   → Use: transcript for quotes, speaker dynamics, tone
   → Use: todos for action items
   
2. AMAZON MEETING SUMMARY (fills gaps)
   → Use: when Hedy didn't record the meeting
   → Use: to cross-check Hedy's summary for anything missed
   → NEVER use as primary if Hedy data exists — it's shallower
   
3. EMAIL THREADS (always check, regardless)
   → Use: for pre-meeting context (agendas, stakeholder asks sent before the call)
   → Use: for post-meeting follow-ups (commitments made in writing after the call)
   → Use: for context that happened outside the meeting but relates to it
   → These often contain the REAL commitments — what someone put in writing matters more than what they said on a call
```

### Multi-Source Ingestion Protocol

When updating a series file after a meeting:

```
STEP 1: Check Hedy
  → mcp_hedy_GetSessions (limit=5) to find the session
  → mcp_hedy_GetSessionDetails(sessionId) for full data
  → If found: this is your primary source. Extract key points, decisions, action items.

STEP 2: Check Amazon Meeting Summary
  → Search Outlook Auto-meeting folder for the meeting name + date
  → If Hedy exists: scan for anything Hedy missed (rare, but possible)
  → If Hedy doesn't exist: this becomes your primary source

STEP 3: Check email threads
  → Search Outlook inbox for meeting name, attendee names, or related topics (±2 days of meeting date)
  → Look for: agenda emails sent before, follow-up emails sent after, stakeholder requests related to meeting topics
  → These get folded into the summary as "Outlook Context" — not as a separate section per source

STEP 4: Synthesize ONE summary
  → Write a single "Latest Session" entry that merges all sources
  → Do NOT create separate sections per source (no "Hedy says X, Amazon says Y")
  → Do NOT copy raw data from any source
  → Resolve conflicts: email > Hedy for commitments (written > spoken); Hedy > Amazon for detail
  → Flag if sources contradict on something material (rare but important)
```

### Conflict Resolution

When sources disagree:
- **On action items**: email thread wins (written commitments > verbal)
- **On what was discussed**: Hedy wins (has the transcript)
- **On decisions**: Hedy wins for in-meeting decisions; email wins for post-meeting revisions
- **On attendees**: Amazon Meeting Summary wins (has the Zoom participant list)
- **If genuinely contradictory**: note both in the summary and flag for Richard to clarify

### What NOT to Do
- Don't dump all three sources into the file separately
- Don't create a "Sources" section listing what came from where
- Don't include Hedy email recaps from Auto-meeting folder if you already pulled from Hedy MCP (they're the same data)
- Don't re-summarize Amazon Meeting Summary verbatim — extract only what adds to the picture

### Cleaning During Ingestion

Raw source data is noisy. The agent must actively clean — not just summarize — during ingestion. Never pass through artifacts you don't understand.

**Hedy transcript artifacts to strip:**
- `(R&O)`, `(Revenue and Operations, monthly process)` — Hedy's misparse of background noise or crosstalk. Not real content. Drop entirely.
- `(CMT)`, `(Supporting)`, `(Foreign policy, high-cBC)`, `(Cooking related or privacy policy)`, `(Post-election)`, `(Police)`, `(Crying)` — hallucinated labels from audio Hedy couldn't interpret. Drop.
- `(Current Office)`, `(Foreign service)`, `(Cutting and marketing)` — same. Drop.
- "Thank you for watching!" / "Thanks for watching, bye bye" — Hedy's end-of-recording boilerplate. Drop.
- Speaker labels like "Speaker 1" when the cleaned_transcript doesn't identify the speaker — infer from context (attendee list, speaking patterns, content) or mark as unknown. Don't write "Speaker 1 said X" into the series file.

**Hedy meeting_minutes / recap issues to catch:**
- Action items with stale dates (e.g., "due Dec 15" appearing in a March session) — these are Hedy recycling old context from its topic overview. Drop or flag as stale.
- Action items assigned to people not in the meeting — cross-check against attendee list. If someone wasn't there, they probably didn't get assigned that task in this session.
- Duplicate action items phrased differently — Hedy's recap, meeting_minutes, and todos often say the same thing three ways. Deduplicate.
- Hedy "suggestions" (the `💡 Suggestion:` blocks in conversations/email recaps) — these are Hedy's AI coaching, not things that were said in the meeting. Do NOT include as discussion points or decisions. They can inform the "Running Themes" section if relevant, but they're not meeting content.

**Amazon Meeting Summary issues to catch:**
- "There is no meeting summary because we didn't hear enough conversation" — means the Zoom mic wasn't picked up. Discard entirely, don't note it.
- Action items from previous sessions bleeding into current summary — Amazon's summarizer sometimes pulls from meeting series history. Cross-check dates.
- Generic/vague summaries that add nothing beyond what Hedy already captured — skip.

**Email thread issues to catch:**
- Auto-generated meeting acceptance emails ("Accepted: [Meeting Name]") — no content. Skip.
- OOF (out of office) auto-replies in the thread — note the OOF if relevant to meeting context, but don't treat as meeting content.
- Email signatures, legal disclaimers, Zoom join links — strip. Never include in summaries.

**General cleaning rules:**
- If a sentence doesn't make sense after reading it twice, drop it. Don't try to interpret gibberish.
- If a number or metric seems wrong (e.g., "$50 CPA" when context says "$134 CPA"), cross-check against other sources or flag as uncertain.
- If an attendee name is garbled (Hedy sometimes mangles names), correct it using the attendee list in the series file metadata.
- Acronyms: expand on first use if the series file doesn't already define them. Don't assume the reader knows what OCI, CPS, ICCP, or AEM mean.

## Folder Structure

```
meetings/
├── README.md              ← you are here
├── stakeholder/           ← recurring meetings with external stakeholders (market teams, vendors)
├── team/                  ← team-wide meetings (weekly sync, deep dive, promo OHs)
├── manager/               ← Brandon 1:1s
├── peer/                  ← 1:1s with teammates (Adi, Yun, Andrew)
└── adhoc/                 ← one-offs, cross-team, ad-hoc meetings
```

## File Format (every series file)

```markdown
# [Meeting Name]

## Metadata
- Cadence: [weekly/biweekly/monthly/ad-hoc]
- Attendees: [names + roles]
- Hedy Topic: [topic name] (ID: [topic_id])
- Quip Doc: [link if applicable]
- Outlook Series: [calendar series name if known]

## Context
[What this meeting is about, Richard's role in it, key dynamics]

## Latest Session
### [Date] — [Title]
- Duration: [X min]
- Key discussion points (agent-summarized from Hedy transcript + meeting minutes)
- Decisions made
- Action items (with owners)

## Running Themes
[Patterns, recurring topics, evolving stakeholder positions]

## Open Items
[Carried-forward action items and unresolved decisions]
```

## How to Update These Files

Follow the Multi-Source Ingestion Protocol above. In short:
1. Check Hedy → Check Amazon Meeting Summary → Check email threads
2. Synthesize ONE clean summary — no source-by-source sections
3. Write in Richard's voice — direct, concise, data-forward
4. Update "Latest Session" (move previous latest to "Previous Sessions" or compress if >3 sessions deep)
5. Update "Open Items" — close completed items, add new ones
6. Update "Running Themes" if patterns shift
7. Do NOT copy raw transcripts or raw email text — summarize

## How Agents Should Use These Files

- **Meeting prep**: Read the relevant series file before any meeting
- **Drafting communications**: Check the series file for tone, stakeholder positions, open items
- **Action tracking**: Cross-reference with `hands.md` and `rw-tracker.md`
- **Relationship context**: Series files contain stakeholder dynamics — use these instead of memory.md for meeting-specific context

## Hedy Topic ID → Series File Map

| Hedy Topic | Topic ID | Series File |
|------------|----------|-------------|
| AU | N6kHmgM0rOdDdah7iNNf | stakeholder/au-paid-search-sync.md |
| MX | NVS0tfApqgEYYa839QNq | stakeholder/mx-paid-search-sync.md |
| Google/Adobe vendors | RotjNJ61wNYxA9zjqVGe | stakeholder/google-ab-performance.md |
| MCS | idSAffMcAegZh6MhQNyA | stakeholder/mcs-polaris-rollout.md |
| Weekly meeting | W7FbHcvgI3y1edPcMAsz | team/weekly-paid-acq.md |
| Deep Dive and Debate | aLpVSvXZAesQs1o0gc4y | team/deep-dive-debate.md |
| Promo | L067rWz6uGP7sLVlSjPI | team/deep-dive-debate.md (or separate) |
| Activation | NcvUf395OiPX7u1w9Vor | team/activation.md |
| Baloo | n7WMdRSB3fXXzuP3cCXJ | adhoc/baloo-early-access.md |
| Brandon sync | 4dRuIp2FdxAQWiOtHs2c | manager/brandon-sync.md |
| Adi sync | q5GzKGvlAxeTHppLeI1e | peer/adi-sync.md |
| Yun sync | 130nPoO6MGGSZrdUStrc | peer/yun-sync.md |
| Andrew sync | o2YbrKwSE1qCB1p00qUn | peer/andrew-sync.md |
| OCI | tFEsxgnyO4QYp2x7TNrI | stakeholder/oci-rollout.md |
| PAM | q1ZDWgAqhUmGMXEfh0xv | team/pam.md |
| AB broad team | Q2IkbN9Eir93yiQguMfi | team/ab-broad-team.md |
| (none) | — | team/biweekly-onsite-events.md |
| (none) | — | team/pre-wbr-customer-engagement.md |
| PSME/Superpowers | — | team/psme-marketing-superpowers.md |

## Portability Note

These files are plain markdown. No hooks, MCP, or subagent access required to read them. A new AI on a different platform can pick up any series file and understand the meeting context cold.
