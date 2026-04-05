# Context Enrichment Protocol

Automated enrichment of Body organs with organizational knowledge from KDS and ARCC.
Runs during EOD-2 Phase 3 (Organ Cascade + Maintenance), before organ updates.

---

## Step 1: Query Generation from current.md

Read `~/shared/context/active/current.md` and extract:
- Active project names (e.g., "AU Paid Search", "MX Campaign Optimization")
- Key topics and themes (e.g., "testing methodology", "AEO strategy", "budget allocation")
- Recent focus areas mentioned in the last 7 days of updates

Generate 3-5 KDS queries per run. Query templates:
```
"{project_name} Amazon Business Paid Search"
"{topic} best practices Amazon"
"{market} paid search strategy"
"Amazon Business {key_theme}"
"{recent_focus_area} paid search"
```

Rules:
- Vary queries across runs — don't repeat the same queries from the previous run
- Prioritize topics that appear in current.md's active work section
- Include at least one market-specific query (AU or MX)

## Step 2: KDS Query Execution

For each generated query, execute via KDS MCP:

```
mcp_knowledge_discovery_mcp_QuerySync(
  queryData={
    "prompt": {
      "question": "{query}",
      "conversationId": "{generate UUID v4}",
      "useCase": "Trade-In",
      "customerId": "prichwil",
      "sessionId": "{generate UUID v4}"
    }
  }
)
```

For each result:
1. Score relevance (0-10) against the active project context from current.md:
   - 8-10: Directly actionable for a current project
   - 7: Useful context that enriches understanding
   - 4-6: Tangentially related — log but don't route
   - 0-3: Not relevant — discard

2. If relevance >= 7: proceed to Step 3 (intake file creation)
3. If relevance < 7: log the query but don't create intake files

## Step 3: Intake File Creation

For each finding with relevance >= 7, create an intake file:

**Path:** `~/shared/context/intake/kds-{YYYY-MM-DD}-{topic-slug}.md`

**Format:**
```markdown
# KDS Finding: {title}

Source: {source_title}
Retrieved: {date}
Relevance: {score}/10
Related project: {project_name from current.md}

## Summary
{2-3 sentence summary of the finding}

## Key points
- {point 1}
- {point 2}
- {point 3}

## Suggested routing
{organ recommendation — see Step 4}
```

## Step 4: Organ Routing

Route findings to the appropriate Body organ based on content type:

| Finding Type | Target Organ | Examples |
|-------------|-------------|----------|
| Strategic insight, org change, leadership direction | brain.md | "New PS strategy for EU expansion", "VP priority shift" |
| Market data, performance benchmark, competitor intel | eyes.md | "JP paid search CPA benchmarks", "AU market trends" |
| Person info, team change, relationship context | memory.md | "New MarTech lead for APAC", "Team reorg in WW Outbound" |
| Process, compliance, governance | intake/ (manual routing) | "Updated data retention policy", "New approval workflow" |

Routing is a suggestion in the intake file — the organ cascade in EOD-2 Phase 3 processes intake files and applies the routing. The enrichment protocol does NOT write directly to organs.

## Step 5: Enrichment Logging

After ALL queries are executed, log every query to DuckDB:

```sql
INSERT INTO enrichment_log (query_text, source, result_count, relevant_count, routed_to, queried_at)
VALUES ('{query}', 'kds', {total_results}, {relevant_results}, '{target_organ_or_none}', CURRENT_TIMESTAMP);
```

Log even queries that returned no results — this data drives query refinement.

## Step 6: Query Refinement (3 Consecutive Empty Runs)

After logging, check for consecutive empty runs:

```sql
SELECT COUNT(*) AS empty_streak
FROM (
    SELECT queried_at::DATE AS run_date,
           SUM(relevant_count) AS daily_relevant
    FROM enrichment_log
    WHERE source = 'kds'
    GROUP BY queried_at::DATE
    ORDER BY run_date DESC
    LIMIT 3
) sub
WHERE daily_relevant = 0;
```

If `empty_streak = 3`:
1. Re-read current.md for any project changes since the last successful enrichment
2. Generate entirely new query terms — don't reuse any from the last 3 runs
3. Broaden scope: include adjacent topics (e.g., if "AU paid search" returned nothing, try "APAC digital marketing")
4. Log the refinement: add a note to the next enrichment_log entry indicating query refinement was triggered

## Step 7: EOD-2 Enrichment Summary

After enrichment completes, include a one-line summary in the EOD-2 report:

```
🧠 Context enrichment: {N} queries, {M} relevant findings routed to intake/. {organs affected}.
```

If no relevant findings: `🧠 Context enrichment: {N} queries, 0 relevant findings.`
If query refinement triggered: `🧠 Context enrichment: query refinement triggered (3 empty runs). New queries generated.`

---

## Failure Handling

- If KDS MCP is unreachable: skip enrichment, log "KDS unreachable" to enrichment_log, continue EOD-2
- If DuckDB write fails: log to local file `~/shared/context/intake/enrichment-fallback-{date}.md`
- Never block EOD-2 on enrichment failures — this is a nice-to-have enhancement, not critical path
