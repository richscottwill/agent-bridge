#!/usr/bin/env python3
"""Loop Page Sync — Refresh stale Loop pages in DuckDB via SharePoint MCP CLI."""
import duckdb
import subprocess
import json
import sys
import os

SP_CLI = "/home/prichwil/brazil-pkg-cache/packages/AmazonSharePointMCP/AmazonSharePointMCP-1.0.1152.0/AL2023_x86_64/DEV.STD.PTHREAD/build/amazon-sharepoint-mcp/dist/cli.js"

def fetch_loop_page(loop_url):
    """Call sharepoint read-loop CLI and return markdown content."""
    try:
        proc = subprocess.run(
            ["node", SP_CLI, "read-loop", loop_url],
            capture_output=True, text=True, timeout=120
        )
        content = proc.stdout.strip()
        if content and len(content) > 10:
            return content
        return None
    except subprocess.TimeoutExpired:
        print("  TIMEOUT", file=sys.stderr)
        return None
    except Exception as e:
        print(f"  ERROR: {e}", file=sys.stderr)
        return None

def main():
    con = duckdb.connect("md:ps_analytics")

    # Step 1: Get stale pages
    pages = con.execute("""
        SELECT page_id, title, loop_url,
               EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - last_ingested))/3600 AS hours_stale
        FROM docs.loop_pages
        WHERE ingestion_status != 'disabled'
        ORDER BY page_id
    """).fetchall()

    print(f"Found {len(pages)} pages in registry", file=sys.stderr)

    results = {}
    success_count = 0
    fail_count = 0

    # Step 2: Refresh each stale page
    for page_id, title, loop_url, hours_stale in pages:
        if hours_stale is not None and hours_stale <= 12:
            print(f"SKIP {page_id}: only {hours_stale:.1f}h stale", file=sys.stderr)
            results[page_id] = {"status": "skipped", "hours_stale": round(hours_stale, 1)}
            continue

        stale_str = f"{hours_stale:.1f}h" if hours_stale else "never ingested"
        print(f"\nRefreshing {page_id} ({title}) — {stale_str} stale", file=sys.stderr)

        content = fetch_loop_page(loop_url)

        if content:
            word_count = len(content.split())
            # Build preview: first 500 chars, clean
            preview = content[:500].strip()

            print(f"  SUCCESS: {word_count} words, {len(content)} chars", file=sys.stderr)

            # Use parameterized update via Python
            con.execute("""
                UPDATE docs.loop_pages SET
                    content_markdown = ?,
                    content_preview = ?,
                    word_count = ?,
                    last_ingested = CURRENT_TIMESTAMP,
                    ingestion_status = 'success'
                WHERE page_id = ?
            """, [content, preview, word_count, page_id])

            results[page_id] = {"status": "success", "words": word_count, "chars": len(content)}
            success_count += 1
        else:
            print(f"  FAILED: No content returned", file=sys.stderr)
            con.execute("""
                UPDATE docs.loop_pages SET
                    ingestion_status = 'failed'
                WHERE page_id = ?
            """, [page_id])
            results[page_id] = {"status": "failed"}
            fail_count += 1

    # Step 4: Log freshness
    print(f"\nLogging freshness to ops.data_freshness...", file=sys.stderr)
    try:
        from datetime import datetime, timezone
        now = datetime.now(timezone.utc)
        con.execute("""
            INSERT INTO ops.data_freshness (source_name, source_type, expected_cadence_hours, last_updated, last_checked, is_stale, downstream_workflows)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT (source_name) DO UPDATE SET
                last_updated = EXCLUDED.last_updated,
                last_checked = EXCLUDED.last_checked,
                is_stale = EXCLUDED.is_stale
        """, ['loop_pages', 'duckdb_table', 12, now, now, False, ['am_brief', 'context_enrichment']])
        print("  Freshness logged", file=sys.stderr)
    except Exception as e:
        print(f"  Freshness log failed: {e}", file=sys.stderr)

    con.close()

    # Summary
    print(f"\n=== LOOP SYNC COMPLETE ===", file=sys.stderr)
    print(f"  Success: {success_count}", file=sys.stderr)
    print(f"  Failed: {fail_count}", file=sys.stderr)
    print(f"  Skipped: {len(pages) - success_count - fail_count}", file=sys.stderr)

    # Output JSON results
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()
