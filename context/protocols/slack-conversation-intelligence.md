<!-- DOC-0360 | duck_id: protocol-slack-conversation-intelligence -->
# Slack Conversation Intelligence Protocol

Enriches Slack messages with internal knowledge context and enables historical conversation retrieval.
Runs during AM-1 (Slack scan enrichment) and AM-2 (triage context enhancement).

---


#### Key Points
- Primary function: preamble
- Referenced by other sections for context

## AM-1: Slack Enrichment Steps

*Example:* When this applies, the expected outcome is verified by checking the result.
### Step 1: Acronym and Project Detection

During the AM-1 Slack scan, after ingesting each message, scan the message text for internal acronyms and project names.

**Known internal terms (non-exhaustive: expand as new terms are encountered):**

| Category | Terms |
|----------|-------|
| Paid Search | OCI, IECCP, AEO, CPC, ROAS, CPA, CVR, CTR, ACOS, TACoS, SB, SP, SD, DSP |
| Amazon Business | ABPS, AB, MCS, ABMA, B2B, ABG |
| Tools/Systems | AMO, Helium, Prism, Kenshoo, SA360, GAds, Weblab, ASIN |
| Org/Process | WBR, MBR, OP1, OP2, PRFAQ, BRD, COE, CR, IECCP |
| Markets | AU, MX, JP, UK, DE, FR, IT, ES, CA |
| Strategy | AEO, AI Overviews, Zero-Click, MarTech, SEO, SEM |

**Detection logic:**
1. Tokenize message text (split on whitespace and punctuation)
2. Match tokens against the known terms list (case-insensitive)
3. Also detect unknown uppercase acronyms (2-5 capital letters not in common English: "THE", "AND", etc.)
4. Flag messages containing 2+ internal terms or any unknown acronym as candidates for KDS enrichment

### Step 2: KDS Enrichment for Unfamiliar Terms

For messages flagged in Step 1 that contain terms NOT in the known terms list (unknown acronyms or unfamiliar project names):

```
1. Extract the unfamiliar term(s) from the message
2. Query KDS for context:
   mcp_knowledge_discovery_mcp_QuerySync(
     queryData={
       "prompt": {
         "question": "{term} Amazon internal",
         "conversationId": "{generate UUID v4}",
         "useCase": "Trade-In",
         "customerId": "prichwil",
         "sessionId": "{generate UUID v4}"
       }
     }
   )
3. If KDS returns a relevant definition/context:
   - Store the knowledge_context alongside the message in DuckDB:
     UPDATE slack_messages
     SET knowledge_context = '{KDS summary}'
     WHERE ts = '{message.ts}';
4. If KDS returns nothing relevant:
   - Skip — don't store empty context
```

**Limits:**
- Maximum 5 KDS queries per AM-1 Slack scan (avoid over-querying)
- Only query for genuinely unfamiliar terms — skip known acronyms from the table above
- Cache KDS results for terms already queried in the last 7 days (check enrichment_log)

### Step 3: Knowledge Context Attachment

For messages where KDS returned useful context, the knowledge_context field in DuckDB enables:
- AM-2 triage can see organizational context alongside the raw message
- Historical retrieval includes the enrichment for richer search results
- The body system has a growing glossary of internal terms with definitions

---

## AM-2: Historical Context Retrieval

### Step 4: Triage Context Enhancement

When AM-2 triages a signal (email, Slack message, or Asana notification), query DuckDB for related past conversations to provide historical context.


**Example:** If this section references a specific process, the concrete steps are: ...

**Query pattern:**
```sql
-- Find related past messages from same author on similar topic
SELECT ts, channel_name, author_name, text_preview, knowledge_context, timestamp
FROM slack_messages
WHERE author_name = '{signal_author}'
AND fts_main_slack_messages.match_bm25(ts, '{signal_keywords}') IS NOT NULL
AND timestamp > CURRENT_TIMESTAMP - INTERVAL '30 days'
ORDER BY timestamp DESC
LIMIT 5;
```

**When to query:**
- For every signal being triaged in AM-2 (email or Slack)
- Extract the signal author and 2-3 key topic words
- If the signal is from a known stakeholder (Brandon, Kate, Todd), always query

**How to use results:**
- Include past conversation snippets in the triage context
- If past messages show an ongoing thread on the same topic: note "Continuing conversation — see {N} related messages from past 30 days"
- If past messages show a resolved topic: note "Previously discussed on {date} — check if this is a new request or follow-up"

### Step 5: Combined Retrieval (for Richard's direct questions)

When Richard asks about a past conversation or decision, combine DuckDB FTS with KDS:

```
1. Search DuckDB slack_messages via FTS:
   SELECT ts, channel_name, author_name, text_preview, knowledge_context,
       fts_main_slack_messages.match_bm25(ts, '{search_terms}') AS score
   FROM slack_messages
   WHERE score IS NOT NULL
   ORDER BY score DESC
   LIMIT 10;

2. Search KDS for organizational context:
   mcp_knowledge_discovery_mcp_QuerySync(query="{search_terms}")

3. Combine results with source attribution:
   - Slack results: "[Slack] {author} in #{channel} on {date}: {excerpt}"
   - KDS results: "[KDS] {finding_summary} (Source: {source_title})"
```

---

## Failure Handling

- If KDS is unreachable during AM-1: skip enrichment, continue Slack scan normally
- If DuckDB FTS query fails during AM-2: skip historical context, triage without it
- Never block AM-1 or AM-2 on enrichment failures — these are enhancements, not critical path
- Log any failures to workflow_executions for observability
