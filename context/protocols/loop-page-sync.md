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

### 2. Refresh Stale Pages (>12h or never ingested)
For each page where `hours_stale > 12` or `last_ingested IS NULL`:
1. Call `sharepoint_read_loop(loopUrl=loop_url)`
2. If success: UPDATE with content_markdown, content_preview (first 500 chars summary), word_count, last_ingested=NOW(), ingestion_status='success'
3. If failure: SET ingestion_status='failed', leave content_markdown unchanged (stale data better than no data)

### 3. Update Template
```sql
UPDATE docs.loop_pages SET
    content_markdown = $content$[FULL MARKDOWN HERE]$content$,
    content_preview = '[SUMMARY OF KEY TOPICS, <500 chars]',
    word_count = [WORD_COUNT],
    last_ingested = CURRENT_TIMESTAMP,
    ingestion_status = 'success'
WHERE page_id = '[PAGE_ID]';
```

### 4. Log
```sql
INSERT INTO ops.data_freshness (source, last_sync, record_count, status)
VALUES ('loop_pages', CURRENT_TIMESTAMP, (SELECT COUNT(*) FROM docs.loop_pages WHERE ingestion_status='success'), 'ok')
ON CONFLICT (source) DO UPDATE SET last_sync=EXCLUDED.last_sync, record_count=EXCLUDED.record_count, status=EXCLUDED.status;
```

## Adding New Pages
Insert a row into `docs.loop_pages` with page_id, title, loop_url, category, owner. Next sync will auto-ingest.

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
