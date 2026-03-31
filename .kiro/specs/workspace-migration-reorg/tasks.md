# Implementation Plan: Workspace Migration & Reorganization

## Overview

Sequential migration of ~/shared/ into a canonical workspace structure. Updated to reflect the full 87-file portable body from `agent-bridge/main:portable-body/` (v1.1.0), including agent consolidation (17→13), expanded tools (9 files), 8 specs (22 files), and the two-repo discovery. Phases execute in order — each builds on the previous.

## Tasks

- [ ] 1. Phase 0 — Upstream Sync from agent-bridge
  - [ ] 1.1 Pull v1.1.0 portable body from agent-bridge
    - The agent-bridge remote is already added (`git remote add agent-bridge https://github.com/richscottwill/agent-bridge.git`)
    - Run `git fetch agent-bridge main` to pull latest
    - Extract portable-body/ contents: `git checkout agent-bridge/main -- portable-body/`
    - Verify file count: `find portable-body/ -type f | wc -l` (expect ~87)
    - _Requirements: 7.1, 7.6_
  - [ ] 1.2 Verify portable body inventory
    - Confirm 13 body organs in portable-body/body/
    - Confirm 13 agent definitions in portable-body/agents/
    - Confirm 6 voice files in portable-body/voice/
    - Confirm 6 steering files in portable-body/steering/
    - Confirm 9 tool files in portable-body/tools/
    - Confirm 22 spec files across 8 dirs in portable-body/specs/
    - Confirm 11 research files in portable-body/research/
    - Confirm 4 system files (portable-layer.md, README.md, CHANGELOG.md, SANITIZE.md)
    - _Requirements: 7.1_

- [ ] 2. Phase 1 — Workspace Symlink Setup
  - [ ] 2.1 Create .kiro symlink and .vscode settings
    - Run `sudo ln -s /home/prichwil/shared/.kiro /home/.kiro`
    - Run `sudo mkdir -p /home/.vscode` and create `/home/.vscode/settings.json` with file exclusion patterns (as specified in moving-home playbook)
    - _Requirements: 1.1, 1.2_
  - [ ] 2.2 Verify IDE discovery of agents, hooks, and steering
    - Run `ls -la /home/.kiro` to confirm symlink resolves
    - Verify agents, hooks, and steering are discoverable via `ls /home/.kiro/{agents,hooks,steering}/`
    - _Requirements: 1.3, 1.4, 1.5_

- [ ] 3. Phase 2 — Dead Weight Removal
  - [ ] 3.1 Remove non-essential directories and files
    - Run `rm -rf ~/shared/agentspaces-desktop-launcher/`
    - Run `rm -rf ~/shared/.aim/`
    - Run `rm ~/shared/rw-shared-export-2026-03-21.tar.gz`
    - Run `rmdir ~/shared/scripts/`
    - _Requirements: 2.1, 2.2, 2.3, 2.4_
  - [ ] 3.2 Clean temp and zero-byte files
    - Run `rm -f ~/shared/research/{err.txt,brand_nb_data.txt,xlsx_output.txt,xlsx_full_output.txt,daily-brief-latest.md}`
    - Run `rm -f ~/shared/context/active/{au-ps-w9-13-optimization-pt2.md,au-ps-w9-13-pt2.md}`
    - _Requirements: 2.5, 2.6_
  - [ ] 3.3 Relocate misplaced files
    - Run `mv ~/shared/context/active/parse-au-search-terms.py ~/shared/tools/`
    - Run `mkdir -p ~/shared/data/processed/au-analysis-w9-13/ && mv ~/shared/context/active/au-analysis/ ~/shared/data/processed/au-analysis-w9-13/`
    - Run `mv ~/shared/context/tools/mcp_debug.py ~/shared/context/tools/mcp_scan.py ~/shared/context/tools/mcp_test.py ~/shared/context/tools/mcp_test2.py ~/shared/uploads/scratch/`
    - _Requirements: 2.7, 2.8, 2.9_
  - [ ] 3.4 Merge reference/ into artifacts/
    - Run `cat ~/shared/reference/index.md >> ~/shared/artifacts/SITEMAP.md && rm -rf ~/shared/reference/`
    - _Requirements: 2.10_

- [ ] 4. Phase 3 — Canonical Directory Structure Creation
  - [ ] 4.1 Create data directory hierarchy
    - Run `mkdir -p ~/shared/data/{duckdb,raw,processed,exports,testing}`
    - Run `mkdir -p ~/shared/data/markets/{au,mx,us,ca,jp,uk,de,fr,it,es}`
    - _Requirements: 3.1, 3.2_
  - [ ] 4.2 Create artifacts, tools, archive, and research directories
    - Run `mkdir -p ~/shared/artifacts/{weekly-ships,testing/{active,completed,templates},frameworks}`
    - Run `mkdir -p ~/shared/tools/{team/docs,autonomous/{logs,configs},scratch,data-pipeline,git-sync,progress-charts}`
    - Run `mkdir -p ~/shared/context/archive/{context,research,tools,misc}`
    - Run `mkdir -p ~/shared/research/aeo`
    - _Requirements: 3.3, 3.4, 3.5, 3.6_
  - [ ] 4.3 Move existing data files from tools/data/
    - Run `mv ~/shared/tools/data/*.duckdb ~/shared/data/duckdb/ 2>/dev/null`
    - Run `mv ~/shared/tools/data/*.wal ~/shared/data/duckdb/ 2>/dev/null`
    - Run `mv ~/shared/tools/data/*.csv ~/shared/data/raw/ 2>/dev/null`
    - Run `mv ~/shared/tools/data/*.parquet ~/shared/data/raw/ 2>/dev/null`
    - _Requirements: 3.7, 3.8, 3.9_

- [ ] 5. Phase 3b — Distribute Portable Body Files
  - [ ] 5.1 Distribute agents (consolidation: 17→13)
    - Remove deprecated per-region agents: `rm -f ~/shared/agents/{abix-analyst,abix-callout-writer,eu5-analyst,eu5-callout-writer,najp-analyst,najp-callout-writer}.md`
    - Copy 13 consolidated agents from portable-body/agents/ to agents/
    - Verify 13 agent files in agents/
    - _Requirements: 7.2, 7.3_
  - [ ] 5.2 Distribute voice files
    - Copy 6 voice files from portable-body/voice/ to voice/ (overwrite — fully portable)
    - _Requirements: 7.2_
  - [ ] 5.3 Merge steering files
    - Copy 6 portable steering files from portable-body/steering/ to steering/
    - Preserve env-specific steering files already in steering/ (asana-sync-protocol.md, mcp-tool-reference.md, rw-tracker.md)
    - Add architecture-eval-protocol.md (new in v1.1.0)
    - _Requirements: 7.2, 7.5_
  - [ ] 5.4 Distribute tools to subdirectories
    - Copy ingest.py, schema.sql, query.py to tools/data-pipeline/
    - Copy sync.sh, git-sync-README.md to tools/git-sync/
    - Copy generate-charts.py, chart-template.html, progress-charts-README.md to tools/progress-charts/
    - Copy RECONSTRUCTION.md to tools/
    - _Requirements: 7.2_
  - [ ] 5.5 Distribute specs to per-spec subdirectories
    - Create 8 spec subdirectories under specs/
    - Move existing specs/paid-search-audit-* into specs/paid-search-daily-audit/
    - Copy 22 spec files from portable-body/specs/ to their respective specs/ subdirectories
    - _Requirements: 7.2_
  - [ ] 5.6 Merge research files
    - Copy portable-body/research/ files into research/, preserving local-only research files
    - _Requirements: 7.2_
  - [ ] 5.7 Update hooks inventory
    - Copy hooks-inventory.md from portable-body/hooks/ to hooks/
    - Verify all 10 hooks described in inventory have corresponding Kiro JSON implementations in hooks/
    - _Requirements: 7.2_
  - [ ] 5.8 Distribute system files
    - Copy portable-layer.md from portable-body/ to workspace root (overwrite)
    - Keep README.md, CHANGELOG.md, SANITIZE.md in portable-body/
    - _Requirements: 7.2, 7.10_

- [ ] 6. Checkpoint — Verify structure, file distribution, and protected dirs
  - Verify all directories from Phase 3 + 3b exist
  - Verify 13 agents in agents/, 6 voice files, 6+ steering files, 9 tool files across subdirs, 8 spec dirs
  - Verify protected directories untouched: `ls -d ~/shared/credentials/ ~/shared/.agentspaces/`
  - _Requirements: 9.1, 9.2_

- [ ] 7. Phase 4 — Key Document Creation
  - [ ] 7.1 Create DIRECTORY-MAP.md
    - Create ~/shared/DIRECTORY-MAP.md with top-level directory table (path, purpose, write permissions, cadence) and file-type-to-location mapping table
    - Must cover all canonical paths including new tool subdirectories (data-pipeline/, git-sync/, progress-charts/), 8 spec directories, and expanded research
    - _Requirements: 4.1, 4.2, 4.3_
  - [ ] 7.2 Create data/README.md
    - Create ~/shared/data/README.md documenting the 5-step ingestion flow and naming conventions
    - Reference ingest.py and query.py from tools/data-pipeline/ as the pipeline tools
    - _Requirements: 4.4, 4.5, 4.6_

- [ ] 8. Phase 5 — Verification
  - [ ] 8.1 Run verification script
    - Enumerate 13 agents in agents/ (verify consolidation complete)
    - Enumerate 10 hooks in hooks/ (parse JSON for name, event type, action type)
    - Enumerate steering files in steering/, steering-chat/, steering-code/
    - Enumerate production scripts in context/tools/
    - Enumerate tool subdirectories in tools/ (including data-pipeline/, git-sync/, progress-charts/)
    - Verify DuckDB files in data/duckdb/
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6_
  - [ ] 8.2 Scan for broken path references
    - Scan body/, steering/, agents/, hooks/ for stale paths: tools/data/, context/active/au-analysis/, agentspaces-desktop-launcher/, reference/, old per-region agent names, old portable-body repo URL
    - Report each broken reference with file:line
    - _Requirements: 5.7, 5.8_

- [ ] 9. Phase 6 — Path Reference Updates
  - [ ] 9.1 Update stale path references
    - Replace `tools/data/` → `data/duckdb/` or `data/raw/`
    - Replace `context/active/au-analysis/` → `data/processed/au-analysis-w9-13/`
    - Replace `reference/` → `artifacts/`
    - Remove references to agentspaces-desktop-launcher/, .aim/, scripts/
    - Update old per-region agent name references to consolidated names (market-analyst, callout-writer)
    - Update portable-body repo URL references from `richscottwill/portable-body` to `richscottwill/agent-bridge`
    - Normalize AgentSpaces-specific paths in portable-body/ organs to relative paths
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7_

- [ ] 10. Checkpoint — Verify path references are clean
  - Re-run broken path scan to confirm zero stale references
  - Verify portable-body/ organs use relative paths, not AgentSpaces-specific absolute paths

- [ ] 11. Phase 7 — Portable Body as Architectural Source
  - [ ] 11.1 Derive Enriched Working Copy from Portable Body
    - Copy 13 organs from portable-body/body/ to body/, preserving existing environment-specific data in body/
    - Use portable-layer.md per-organ manifest to identify what is portable vs env-specific
    - _Requirements: 7.2, 7.3, 7.5, 7.7_
  - [ ] 11.2 Update portable-body/ metadata
    - Update portable-body/README.md with file count (87) and today's sync date
    - Update portable-body/CHANGELOG.md with migration entry
    - Update portable-layer.md with new canonical structure (13 organs, expanded categories)
    - _Requirements: 7.8, 7.9, 7.10_
  - [ ] 11.3 Address portability gaps
    - Add "Portability Gaps" section to portable-layer.md documenting: Kiro JSON hooks, DuckDB tools, MCP tool references, morning-routine-experiments.md staleness
    - Ensure portable-body/ organs use capability descriptions not tool-specific names
    - _Requirements: 7.11, 7.12_

- [ ] 12. Phase 7b — Agent Comprehension Guard Rail
  - [ ] 12.1 Create guard rail content in portable-body/README.md
    - Explain the full 87-file Architectural Source model covering all 9 content categories
    - Instruct agents to read portable-layer.md before any write to portable-body/
    - Document the derivation flow: architectural edits → portable-body/ → derive to workspace dirs; env-specific writes → body/ directly
    - _Requirements: 11.1, 11.2, 11.3_
  - [ ] 12.2 Add steering directive for portable-body/ write protection
    - Create a steering directive or preToolUse hook requiring agents to read portable-layer.md before writes to any file under portable-body/
    - Directive must cover all portable-body/ subdirs (body/, agents/, steering/, tools/, etc.)
    - If agent writes env-specific data to portable-body/, redirect to corresponding workspace file
    - _Requirements: 11.4, 11.5, 11.6_

- [ ] 13. Checkpoint — Verify portable body sync and guard rails
  - Verify portable-body/ contains all 87 files with post-reorg paths
  - Verify body/ contains 13 organs with env-specific data preserved
  - Verify agents/ has 13 consolidated agents (no deprecated per-region agents)
  - Verify guard rail README and steering directive are in place
  - _Requirements: 7.3, 7.4, 11.4_

- [ ] 14. Phase 8 — Blind Evaluator Validation
  - [ ] 14.1 Create blind-evaluator-tests.md
    - Create ~/shared/audit-reports/blind-evaluator-tests.md with 50+ test prompts
    - Cover: upload drop zones, body organs, callout paths, DuckDB paths, tool subdirectories (data-pipeline/, git-sync/, progress-charts/), consolidated agent locations, 8 spec directories, research paths, agent-bridge upstream relationship
    - _Requirements: 8.1, 8.2, 8.5_
  - [ ] 14.2 Run blind evaluator validation
    - Give fresh agent only DIRECTORY-MAP.md + test prompts
    - Score accuracy — target >98%
    - If below 98%, update DIRECTORY-MAP.md to resolve ambiguities
    - _Requirements: 8.3, 8.4, 8.6_

- [ ] 15. Phase 9 — Data Ingestion Flow Verification
  - [ ] 15.1 Verify ingestion pipeline
    - Verify uploads/sheets/ and uploads/changelogs/ exist as drop zones
    - Verify data/{raw,processed,exports,markets} directories exist
    - Verify data/README.md documents naming conventions
    - Verify ingest.py and query.py are in tools/data-pipeline/
    - Cross-reference pipeline docs with actual directory structure
    - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5_

- [ ] 16. Final Checkpoint — Full workspace verification
  - Re-run verification script to confirm all 13 agents, 10 hooks, steering, scripts, DuckDB, and paths intact
  - Verify protected directories untouched
  - Verify DIRECTORY-MAP.md covers all canonical paths including new tool subdirs and spec dirs
  - Verify portable-body/ and body/ are in sync
  - Verify agent-bridge upstream relationship is documented

## Notes

- Tasks are sequential — each phase depends on the previous
- Phase 0 (upstream sync) is NEW — pulls from agent-bridge repo, not the old portable-body repo
- Phase 3b (distribute) is NEW — distributes 87 files from portable-body/ to canonical workspace dirs
- Agent consolidation removes 6 per-region agents, replaces with 2 parameterized (market-analyst, callout-writer)
- Protected directories (credentials/, .agentspaces/) are never targeted
- Checkpoints at tasks 6, 10, 13, and 16 provide incremental validation
- Blind evaluator test (task 14) is the final quality gate — >98% accuracy required
