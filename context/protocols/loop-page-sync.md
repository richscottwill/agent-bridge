# Loop Page Sync Protocol

Refreshes Loop page content in `docs.loop_pages` via SharePoint MCP.

## When to Run
- AM-Backend Phase 1 (parallel with Slack/Asana/Email ingestion)
- EOD-Backend Phase 5 (housekeeping, if stale >24h)

## Steps

### 1. Read Registry
```sql
SELECT page_id, title, loop_url, last_ingested,
       EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - last_ingested))/3600 AS hours_stale
FROM docs.loop_pages
WHERE ingestion_status != 'disabled'
ORDER BY hours_stale DESC NULLS FIRST;
```

[38;5;10m> [0m### 2. Refresh Stale Pages (>12h or never ingested)[0m[0m
Find every page where `hours_stale > 12` or `last_ingested IS NULL` — for example, a page last pulled Monday morning would qualify by Monday night — then for each one:[0m[0m
1. Fetch the latest content by calling `sharepoint_read_loop(loopUrl=loop_url)`.[0m[0m
2. **On success:** Update the row with the new `content_markdown`, a `content_preview` (first 500 characters summarizing the page), `word_count`, `last_ingested=NOW()`, and `ingestion_status='success'`. For instance, a 2,400-word design doc would store its opening summary as the preview and `word_count=2400`.[0m[0m
3. **On failure:** Set `ingestion_status='failed'` but keep the existing `content_markdown` intact — serving yesterday's version of a page is more useful than serving nothing.
[38;5;10m> [0m### 3. Update Template[0m[0m
[0m[0m
UPDATE docs.loop_pages[0m[0m
SET content_markdown = $content$[FULL MARKDOWN HERE]$content$,[0m[0m
   content_preview = '[SUMMARY OF KEY TOPICS, <500 chars]',[0m[0m
   word_count = [WORD_COUNT],[0m[0m
   last_ingested = CURRENT_TIMESTAMP,[0m[0m
   ingestion_status = 'success'[0m[0m
WHERE page_id = '[PAGE_ID]';[0m[0m
### 4. Log
```sql
INSERT INTO ops.data_freshness (source, last_sync, record_count, status)
VALUES ('loop_pages', CURRENT_TIMESTAMP, (SELECT COUNT(*) FROM docs.loop_pages WHERE ingestion_status='success'), 'ok')
ON CONFLICT (source) DO UPDATE SET last_sync=EXCLUDED.last_sync, record_count=EXCLUDED.record_count, status=EXCLUDED.status;
```

[38;5;10m> [0m## Adding New Pages[0m[0m
Insert a row into `docs.loop_pages` with page_id, title, loop_url, category, owner. Next sync will auto-ingest.[0m[0m
[0m[0m
**Example:**[0m[0m
[0m[0m
INSERT INTO docs.loop_pages (page_id, title, loop_url, category, owner)[0m[0m
VALUES ('pg_00142', 'Onboarding Checklist', 'https://loop.cloud/pages/pg_00142', 'onboarding', 'jsmith@company.com');[0m[0m
[0m[0m
Once the next scheduled sync runs, the page content will be automatically ingested and available for search.
## Querying Loop Content
```sql
-- Latest content from a specific page
SELECT content_markdown FROM docs.loop_pages WHERE page_id = 'loop-brandon-1on1';

-- Search across all pages
SELECT page_id, title, content_preview FROM docs.loop_pages WHERE content_markdown ILIKE '%OCI%';

-- Freshness check
SELECT page_id, title, ingestion_status, last_ingested,
       EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - last_ingested))/3600 AS hours_ago
FROM docs.loop_pages;
```
