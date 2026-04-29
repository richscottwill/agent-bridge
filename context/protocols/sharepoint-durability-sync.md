<!-- DOC-0355 | duck_id: protocol-sharepoint-durability-sync -->


# SharePoint Durability Sync Protocol

Bidirectional sync between `~/shared/` (live workspace) and OneDrive `Kiro-Drive/` (durable, cross-device).

**Why:** DevSpaces containers can die. `~/shared/` is persistent but only accessible via SSH. SharePoint survives container restarts and is accessible from any device (phone, local machine, browser). This protocol makes the system resilient to environment loss and gives Richard mobile access to key artifacts.

**Principle alignment:** Invisible over visible (Principle 5) — sync happens silently in the background. Structural over cosmetic (Principle 2) — changes the default durability without changing the workflow.

---



## SharePoint Target

- Library: `Documents` (personal OneDrive)
- Base folder: `Kiro-Drive/`
- No siteUrl needed (defaults to personal OneDrive)

#### SharePoint Target — Details

- Subfolders auto-created on first write



## Folder Structure

```
Kiro-Drive/
├── system-state/          # Hook output artifacts (updated every AM/EOD run)
│   ├── eod-reconciliation.json
│   ├── eod-maintenance.json
│   ├── eod-experiments.json
│   ├── am-enrichment-queue.json
│   ├── am-portfolio-findings.json
│   ├── daily-brief-latest.md
│   ├── rw-tracker.md
│   ├── hook-protocol-audit.md
│   └── sharepoint-durability-sync.md
├── state-files/           # Daily-refresh narrative docs (AM generates, EOD patches)
│   ├── mx-paid-search-state.docx
│   ├── au-paid-search-state.docx
│   └── ww-testing-state.docx
├── portable-body/         # Cold-start survival kit (weekly)
│   └── body-snapshot-YYYY-MM-DD.md
└── meeting-briefs/        # Meeting prep/debrief docs (on creation)
    ├── meeting-briefs-index.md
    └── YYYY-MM-DD-meeting-slug.md

Artifacts/       # Published work products (SEPARATE from Kiro-Drive)
├── au/, mx/, jp/, uk/, us/, ww/   # Market-specific callouts + analyses
├── testing/, strategy/, research/  # Topic-specific docs
├── reporting/, operations/, markets/
└── (managed by sharepoint-sync.kiro.hook + cli.py)
```

**Note:** Published artifacts live in `Artifacts/`, NOT in `Kiro-Drive/`. The wiki-sync pipeline (sharepoint-sync hook + cli.py) manages that folder with .docx conversion, SHA-256 dedup, and incremental sync. `Kiro-Drive/` is exclusively for system state, snapshots, and meeting briefs.

---



## PUSH: When to Write to SharePoint



### Automatic Push Triggers (agent decides)

| Trigger | What Gets Pushed | SharePoint Path | Create or Update |
|---------|-----------------|----------------|-----------------|
| EOD Backend Phase 7.5 | eod-reconciliation.json, eod-maintenance.json, eod-experiments.json, daily-brief-latest.md | system-state/ | **Update** (overwrite same filename — always latest) |
| AM Backend Phase 6.5 | am-enrichment-queue.json, am-portfolio-findings.json, daily-brief-latest.md | system-state/ | **Update** |
| Friday EOD (or on-demand) | Portable body snapshot, rw-tracker.md | portable-body/, system-state/ | **Create** new dated snapshot + **Update** rw-tracker |
| Wiki article reaches PUBLISH stage | Final article as .docx | `Artifacts/[category]/` | Managed by sharepoint-sync hook — NOT part of Kiro-Drive durability sync |
| Strategic artifact shipped (Testing Approach, AEO POV, etc.) | Final doc as .docx | `Artifacts/[category]/` | Managed by sharepoint-sync hook — NOT part of Kiro-Drive durability sync |
| Meeting prep doc created | Prep brief | meeting-briefs/ | **Create** |
| AM-Backend Step 2E / EOD Step 9 | State file .docx per market (MX, AU, WW Testing) | `Kiro-Drive/state-files/` | **Update** (overwrite — always latest version) |



### Decision Logic: Create vs Update

- **system-state/** files: Always **update** (overwrite). These are "latest state" — only the current version matters.
- **portable-body/** snapshots: Always **create** with dated filename. Never overwrite old snapshots — they're the historical record.
- **meeting-briefs/**: **Create** only. Meeting briefs are point-in-time — never updated after creation. Index file is the exception (updated when new briefs are added).
- **Artifacts/**: Managed entirely by the sharepoint-sync hook. Not part of this protocol.



### Push Implementation

```python


# Update pattern (system-state):
sharepoint_write_file(libraryName="Documents", folderPath="Kiro-Drive/system-state",
    fileName="eod-reconciliation.json", content=<read_local_file>)



# Create pattern (portable-body):
sharepoint_write_file(libraryName="Documents", folderPath="Kiro-Drive/portable-body",
    fileName="body-snapshot-2026-04-11.md", content=<snapshot_content>)

**Key consideration:** This section's content is critical for accurate operation. Cross-reference with related sections for full context.
# Create/Update pattern (artifacts):
sharepoint_write_file(libraryName="Documents", folderPath="Kiro-Drive/artifacts",
    fileName="testing-approach-v5.md", content=<article_content>)
```

---



## PULL: When to Read from SharePoint



### Automatic Pull Triggers (agent decides)

| Trigger | What Gets Pulled | When | Why |
|---------|-----------------|------|-----|

**Example:** If this section references a specific process, the concrete steps are: |---------|-----------------|------|-----|...

| Cold start (new container, no `~/shared/` state) | portable-body/body-snapshot-*.md (latest) | Session start, if local files missing | Bootstrap the system from last known good state |
| AM Backend can't find local output files | system-state/*.json | Phase 2+ of AM, if Phase 1 output missing | Container may have restarted between phases |
| EOD Frontend can't find backend output | system-state/eod-*.json | EOD Frontend Step 1, if local files missing | Backend may have run in a prior container session |
| Richard asks about a published artifact | artifacts/*.md | On demand | Artifact may have been created on a different machine or in a prior container |
| Richard asks "what did the brief say" from a different context | system-state/daily-brief-latest.md | On demand | Brief was generated in SSH but Richard is asking from local |



### Pull Decision Logic

1. **Always try local first.** `~/shared/` is the source of truth when available.
2. **Fall back to SharePoint** only when local file is missing, stale (>24h for system-state), or explicitly requested.
3. **Never overwrite local with SharePoint** unless local is confirmed missing. SharePoint is the backup, not the master.
4. **Staleness check:** For system-state files, compare local file mtime vs SharePoint Modified timestamp. If SharePoint is newer (e.g., another agent session wrote to it), pull and merge.


```python


# Read text file inline:
sharepoint_read_file(serverRelativeUrl="/personal/prichwil_amazon_com/Documents/Kiro-Drive/system-state/daily-brief-latest.md",
    savePath="~/shared/wiki/research/", inline=True)



# Download binary or large file:
sharepoint_read_file(serverRelativeUrl="/personal/prichwil_amazon_com/Documents/Kiro-Drive/portable-body/body-snapshot-2026-04-11.md",
    savePath="~/shared/context/active/")
```

---



## What Does NOT Get Synced

| Category | Why Not |
|----------|---------|
| Organs (body.md, brain.md, etc.) | Change every session. SharePoint latency creates stale reads. Live workspace is source of truth. |
| DuckDB data | Structured data. Not file-based. Query via DuckDB MCP (`execute_query`). |
| Intake files | Ephemeral. Processed and deleted within the same session. |
| Hook configs, steering files | IDE-bound. No cross-device need. |
| Audit logs (JSONL) | Append-only. Stays on filesystem + DuckDB. |
| Git repo state | Managed by git, not SharePoint. |

---



## Conflict Resolution

If both local and SharePoint have been modified since last sync:
1. **system-state/**: Local wins. These are regenerated every run — the latest local version is always correct.
2. **state-files/**: Local wins. Generated by AM-Backend, patched by EOD. SharePoint is delivery copy only.
3. **portable-body/**: No conflict possible — each snapshot has a unique dated filename.
3. **meeting-briefs/**: No conflict possible — created once, never updated (except index).
4. **Artifacts/**: Managed by sharepoint-sync hook with SHA-256 dedup. Not part of this protocol.

---




### Common Pitfalls — Conflict Resolution
- Misinterpreting this section causes downstream errors
- Always validate assumptions before acting on this data
- Cross-reference with related sections for completeness



## Error Handling

- SharePoint write fails → log warning to DuckDB `workflow_executions`, continue. Local files are source of truth.
- SharePoint read fails → use local file. Log warning.
- SharePoint is a durability layer, not a dependency. **No hook should fail because SharePoint is unreachable.**
- Log all sync operations to DuckDB: `INSERT INTO workflow_executions (workflow_name, ...) VALUES ('sharepoint-durability-sync', ...)`

---


**Example:** This section demonstrates the pattern in practice — concrete instances ground abstract rules.



## Verification

After first sync or on-demand:
```
sharepoint_list_files(libraryName="Documents", folderPath="Kiro-Drive/system-state")
sharepoint_list_files(libraryName="Documents", folderPath="Kiro-Drive/portable-body")
sharepoint_list_files(libraryName="Documents", folderPath="Kiro-Drive/meeting-briefs")
sharepoint_list_files(libraryName="Documents", folderPath="Artifacts/wiki-sync")  # separate pipeline
```
