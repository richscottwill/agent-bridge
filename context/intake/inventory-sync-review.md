# Cross-Environment Inventory Sync — SSH Agent Review

**From:** SSH AgentSpaces (prichwil)
**To:** Local Kiro agent (for implementation)
**Date:** 2026-04-07
**Context:** Full review against the live body system, DuckDB infrastructure, hook architecture, sync tooling, and daily workflows. This is not a surface-level design review — I loaded every organ, the ops schema, the agent-bridge repo structure, the uploads directory, data_freshness patterns, and the actual file transfer patterns we use today.

---

## Verdict: Good design, needs integration depth

The architecture is sound. Manifest-per-env avoids git conflicts. MotherDuck as shared query layer is correct — both sides already have it. Transfer requests via DuckDB are the right async pattern. No new services, no new auth. That's discipline.

But the design was written in isolation from how the system actually works day-to-day. Below is everything I'd change, add, or flag before implementation.

---

## 1. THE UPLOADS DIRECTORY ALREADY EXISTS — USE IT

The design proposes `context/intake/` as the staging dir for transfers. But the agent-bridge repo already has a dedicated `uploads/` directory with subdirectories:
- `uploads/sheets/` — 20 files, 15MB+ of WW Dashboard xlsx, keyword reports, ref tag CSVs
- `uploads/changelogs/` — change log CSVs
- `uploads/docs/` — document uploads
- `uploads/other/` — misc

This is the EXISTING file transfer mechanism. Richard drops files into `uploads/` on local, pushes to git, SSH pulls them. The inventory scanner on local should scan `uploads/` as a primary directory — not just `~/Documents` and `~/Downloads`. And the SSH scanner should scan `~/shared/data/exports/` (parquet exports) as a return channel.

**Recommendation:** Replace the generic scan dirs with the actual directories that matter:

**Local scan dirs:**
- `~/agent-bridge/uploads/` (the actual transfer staging area)
- `~/agent-bridge/context/intake/` (intake files)
- `~/OneDrive - amazon.com/Artifacts/wiki-sync/` (SharePoint sync output)
- `~/Documents/*.xlsx,*.csv,*.pdf` (filtered, as designed)

**SSH scan dirs:**
- `~/shared/context/intake/` (33 files currently, including a 998KB PDF and a 24KB xlsx)
- `~/shared/data/exports/` (parquet exports — the return channel)
- `~/shared/wiki/research/` (research outputs)
- `~/shared/tools/` (utility scripts — for awareness, not transfer)

---

## 2. INTEGRATE WITH ops.data_freshness — DON'T DUPLICATE

The system already has `ops.data_freshness` tracking 17 sources with `expected_cadence_hours`, `last_updated`, `last_checked`, `is_stale`, and `downstream_workflows`. This is exactly the staleness tracking the design needs but doesn't reference.

**Recommendation:** After each inventory sync, UPSERT a row into `ops.data_freshness`:
```sql
INSERT OR REPLACE INTO ops.data_freshness VALUES (
  'env_inventory_local', 'inventory_manifest', 168,
  CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, false,
  ['transfer_requests', 'am_brief']
);
```

This way the existing bloat detection in gut.md and the AM-3 brief's freshness check automatically surface stale inventories. No new staleness mechanism needed. The design's proposed staleness TTL on inventory rows becomes redundant — `data_freshness` already handles it.

---

## 3. HOOK PLACEMENT: EOD-2, NOT STANDALONE

The design proposes standalone hooks for both environments. But the SSH side should run as part of the EOD-2 cascade, not as a separate hook. Here's why:

EOD-2 already does: maintenance cascade → experiments → dashboard → enrichments → git sync. The inventory scan is a natural fit between "enrichments" and "git sync" — scan local files, write manifest, UPSERT to DuckDB, check for pending transfer requests, then git sync pushes everything.

Adding a standalone hook means another thing to remember to trigger. Embedding it in EOD-2 means it runs automatically every evening. That's structural over cosmetic (principle #2) and routine as liberation (principle #1).

**Recommendation:**
- SSH: Add inventory scan as a phase in EOD-2, right before git sync
- Local: Keep as standalone userTriggered hook (local doesn't have the same cascade architecture), but also wire it into `sync-local.ps1` so it runs automatically on every sync

---

## 4. THE REAL TRANSFER PATTERN IS GIT, NOT DUCKDB

The design has transfer requests flowing through DuckDB, which is correct for the request/coordination layer. But the actual file movement is git push/pull through the agent-bridge repo. The design acknowledges this but doesn't specify the exact git integration.

Current sync flow (from `sync.sh`):
1. `git pull origin main --rebase`
2. `git add -A`
3. `git commit -m "sync: $TIMESTAMP"`
4. `git push -u origin main`

The inventory manifest (`.inventory/ssh.json`) gets committed and pushed as part of this flow. But fulfilled transfer requests need to:
1. Copy the file to `uploads/` (or `context/intake/`)
2. Commit the file
3. Push
4. Update DuckDB status to 'fulfilled'

**Recommendation:** The fulfillment step should be: copy file → git add → git commit with descriptive message (`"transfer: [filename] requested by [env]"`) → git push → DuckDB update. The design's `fulfillTransferRequests` algorithm should explicitly include the git commit step, not just the file copy.

---

## 5. CATEGORY CLASSIFICATION DOESN'T MATCH OUR DIRECTORY STRUCTURE

The design's `classifyCategory` function uses generic path patterns (`context/active`, `intake`, `research`, `wiki/`, `data/`, `tools/`). But our actual directory structure is more specific:

| Actual Directory | Design Category | Better Category |
|-----------------|----------------|-----------------|
| `uploads/sheets/` | unknown | `data_upload` |
| `uploads/changelogs/` | unknown | `data_upload` |
| `context/intake/` | intake | intake (correct) |
| `context/active/` | context | active_state |
| `context/body/` | context | organ |
| `wiki/research/` | research | research (correct) |
| `wiki/meetings/` | artifact | meeting_notes |
| `data/exports/` | data | export |
| `tools/` | tool | tool (correct) |

**Recommendation:** Expand the category enum to match our actual directory taxonomy. The categories should map to how the system actually organizes information, not generic labels. This matters because the SSH agent will query `WHERE category = 'data_upload'` to find Excel files Richard pushed — `unknown` is useless.

---

## 6. MISSING: WHAT DOES THE AGENT ACTUALLY DO WITH INVENTORY DATA?

The design specifies the plumbing (scan, store, query, transfer) but doesn't specify the consumption patterns. From my knowledge of how this system works day-to-day, here are the actual use cases:

**Use case 1: AM-2 triage needs a file from local.**
Richard mentions "the AU keyword report" in a task. AM-2 checks `ops.env_inventory WHERE env='local' AND file_name LIKE '%AU%keyword%'`. If found, creates transfer request. Next local sync fulfills it.

**Use case 2: EOD-2 wants to export data for local analysis.**
Karpathy experiments produce parquet exports. SSH inventory registers them. Local agent queries `WHERE env='ssh' AND file_type='csv' OR file_type='json'` to see what's available for local tools (Excel, Power BI).

**Use case 3: Richard asks "do I have the latest WW Dashboard?"**
Agent queries both inventories: `SELECT env, file_name, modified_at, sha256 FROM ops.env_inventory WHERE file_name LIKE '%WW Dashboard%' ORDER BY modified_at DESC`. Shows both copies, flags if SHA mismatch (local has newer version not yet synced).

**Use case 4: Gut bloat detection on intake.**
Gut already flags `intake/ > 10 unprocessed files`. Inventory data could enhance this: `SELECT COUNT(*) FROM ops.env_inventory WHERE env='ssh' AND category='intake' AND scanned_at > modified_at - INTERVAL 7 DAY` — files sitting in intake for 7+ days without being processed.

**Recommendation:** Add a "Consumption Patterns" section to the design that specifies these queries. The views (`v_local_inventory`, `v_ssh_inventory`, etc.) should be designed around these actual use cases, not generic filters.

---

## 7. SHA-256 HASHING: CACHE BY MTIME

The design skips SHA-256 for files >50MB. But the `uploads/sheets/` directory has 5MB xlsx files that change weekly (WW Dashboard). Hashing these every scan is fine. The real issue is: what about files that NEVER change? Steering files, organ templates, tool scripts — these are stable. Hashing them every scan wastes cycles.

**Recommendation:** Cache hashes. Store `{path: sha256, mtime: timestamp}` in the manifest. On next scan, if `mtime` hasn't changed, reuse the cached hash. Only recompute when `mtime` differs. This is how rsync works and it's dramatically faster for large inventories.

---

## 8. THE `description` FIELD NEEDS A SPEC

The design calls `generateDescription(file.basename, category)` but never defines it. Given our system's emphasis on portability (principle: "Would a new AI on a different platform understand this?"), the description field is actually important — it's what makes the inventory useful to an agent that doesn't know our directory conventions.

**Recommendation:** Template-based, not LLM-generated. Keep it fast and deterministic:
```
{category}: {file_type} file. {size_human}. Last modified {relative_time}.
```
Example: `data_upload: excel file. 5.2MB. Last modified 2 days ago.`

For known file patterns, add richer descriptions:
- `*WW Dashboard*` → "Weekly WW Paid Search performance dashboard"
- `*keyword*report*` → "Google Ads keyword performance export"
- `*session-log*` → "Agent session activity log"

Store these patterns in a config file, not hardcoded. The config file itself gets inventoried.

---

## 9. TRANSFER REQUEST PRIORITY SHOULD MAP TO TASK PRIORITY

The design has `priority: normal/high/low` on transfer requests. But our system already has a priority framework (P0-P3 in hands.md, Sweep/Core/Engine Room/Admin/Backlog in To-Do). Transfer priority should align.

**Recommendation:**
- `urgent` — needed for a P0/P1 task or active meeting prep (fulfill on next sync, notify Richard if local hook isn't running)
- `normal` — needed for current work but not blocking (fulfill on next scheduled sync)
- `background` — nice to have, no deadline (fulfill whenever)

And add a `requested_for` field that links to the task or context that triggered the request. This creates an audit trail: "This file was transferred because AM-2 needed it for the AU keyword analysis task."

---

## 10. VIEWS SHOULD SERVE THE DAILY HOOKS

The design proposes 4 views: `v_local_inventory`, `v_ssh_inventory`, `v_pending_transfers`, `v_inventory_summary`. These are fine but generic. Add views that serve the actual daily hooks:

```sql
-- What's new since last AM run? (for AM-1 ingest)
CREATE VIEW ops.v_new_since_last_am AS
SELECT * FROM ops.env_inventory
WHERE scanned_at > (SELECT MAX(start_time) FROM ops.hook_executions
                    WHERE hook_name = 'am-1-ingest')
ORDER BY scanned_at DESC;

-- What Excel/CSV files are available on local? (for data analysis requests)
CREATE VIEW ops.v_local_data_files AS
SELECT file_name, file_type, size_bytes, modified_at, sha256, description
FROM ops.env_inventory
WHERE env = 'local' AND file_type IN ('excel', 'csv')
ORDER BY modified_at DESC;

-- Transfer request status with age (for EOD-2 reporting)
CREATE VIEW ops.v_transfer_status AS
SELECT *,
  DATEDIFF('hour', requested_at,
    COALESCE(fulfilled_at, CURRENT_TIMESTAMP)) as hours_pending
FROM ops.transfer_requests
ORDER BY
  CASE status WHEN 'pending' THEN 0
              WHEN 'fulfilled' THEN 1 ELSE 2 END,
  requested_at DESC;

-- Cross-env file comparison (for "do I have the latest?" queries)
CREATE VIEW ops.v_file_sync_status AS
SELECT
  COALESCE(l.file_name, s.file_name) as file_name,
  l.sha256 as local_sha, s.sha256 as ssh_sha,
  l.modified_at as local_modified, s.modified_at as ssh_modified,
  CASE WHEN l.sha256 = s.sha256 THEN 'synced'
       WHEN l.sha256 IS NULL THEN 'ssh_only'
       WHEN s.sha256 IS NULL THEN 'local_only'
       ELSE 'diverged' END as sync_status
FROM ops.env_inventory l
FULL OUTER JOIN ops.env_inventory s
  ON l.file_name = s.file_name AND l.env = 'local' AND s.env = 'ssh';
```

---

## 11. MISSING: INTEGRATION WITH THE BLOAT DETECTION SYSTEM

Gut.md has explicit bloat signals. The inventory system should feed two of them:

| Existing Bloat Signal | Inventory Enhancement |
|----------------------|----------------------|
| "Intake folder > 10 unprocessed files" | `SELECT COUNT(*) FROM ops.env_inventory WHERE category='intake' AND env='ssh'` — now queryable, not just a file count |
| "DuckDB experiment table > 500 rows" | Add: `SELECT COUNT(*) FROM ops.env_inventory` — if inventory itself exceeds 5000 entries, flag for cleanup |

New bloat signal the inventory enables:
- "Transfer requests pending > 48 hours" — something is stuck
- "Inventory divergence > 20 files" — too many files exist on one side but not the other

**Recommendation:** Add these to the AM-3 brief's gut check section. When inventory issues are detected:
```
GUT CHECK: ...
- Inventory: 3 transfer requests pending >48h (local sync may be stale)
- Inventory: 15 files on local not synced to SSH (last local scan: 3 days ago)
```

---

## 12. COLD START: MANIFESTS ARE SOURCE OF TRUTH

The portability principle says: "Would a new AI on a different platform understand this without access to our hooks, MCP servers, or subagents?" The manifest JSON files in `.inventory/` are portable — any agent can read JSON. But the DuckDB tables require MotherDuck access.

**Recommendation:** Make this explicit in the design: "Manifests are source of truth. DuckDB is the query layer. On cold start, read manifests directly from the git repo." The manifests should include enough metadata (scan config, stats, descriptions) that a new agent can understand the inventory without DuckDB.

---

## 13. FIVE LEVELS ALIGNMENT

This is Level 5 infrastructure (agentic orchestration — environments coordinating autonomously). But it also serves Level 3 (team automation — if the inventory system works, it's a pattern teammates could adopt). Don't over-engineer it for Level 5 when Level 1 is still the gate. Build the minimum that makes cross-env awareness work, then iterate.

---

## 14. IMPLEMENTATION ORDER (from SSH perspective)

What I can build and test right now:
1. DuckDB tables (`ops.env_inventory`, `ops.transfer_requests`) + views
2. SSH scanner (Python script in `~/shared/tools/inventory/`)
3. `.inventory/ssh.json` manifest generation
4. Integration into EOD-2 cascade
5. `ops.data_freshness` registration

What needs local:
6. Local scanner (PowerShell or Python)
7. `.inventory/local.json` manifest generation
8. Integration into `sync-local.ps1`
9. Transfer request fulfillment logic

What needs both sides working:
10. End-to-end transfer request flow
11. `v_file_sync_status` view validation
12. AM-3 brief integration

---

## 15. IDEAS BEYOND CURRENT SCOPE

**Content preview in inventory:** For markdown and text files, store the first 200 chars as a `preview` field. This lets the SSH agent decide whether to request a transfer without needing the full file. Low cost, high value.

**Auto-transfer rules:** Instead of manual transfer requests, define rules: "Any new xlsx in `uploads/sheets/` automatically gets ingested to DuckDB on next SSH scan." This is the Level 5 pattern — no human in the loop for routine data flows.

**Inventory-driven intake processing:** Right now gut.md says "process intake files." With inventory data, AM-2 could prioritize: "3 new files in intake since last scan. 1 is a 998KB PDF (OCI instructions — high priority). 2 are session logs (low priority, auto-archive after 7 days)." The inventory metadata (type, category, size) makes triage smarter.

**Bidirectional organ sync verification:** The agent-bridge already syncs organ files. Inventory could verify: "brain.md on SSH was modified 2 hours ago but agent-bridge copy is from yesterday." This catches sync failures that currently go unnoticed.

**SharePoint inventory:** The SharePoint sync tool already tracks what's published. An inventory entry for each SharePoint-synced file would let the SSH agent know what's publicly available vs. what's still in draft.

---

## Summary

The design is architecturally sound. The gaps are all integration gaps — it was designed as a standalone system when it needs to be woven into the existing body. The key changes: use `uploads/` (not just Documents/Downloads), integrate with `ops.data_freshness` (don't reinvent staleness), embed in EOD-2 (not standalone hook), add consumption-pattern views (not generic filters), and make manifests the cold-start source of truth.

Build the DuckDB tables and SSH scanner first. That's testable from here. Local side needs a separate session.
