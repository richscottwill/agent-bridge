# Requirements Document

## Introduction

Comprehensive reorganization of the `~/shared/` directory structure. The current layout has accumulated dead weight (596MB+ of non-essential files), inconsistent path references across body organs, steering files, agent configs, and hooks, and no single source of truth for "where does X go." This reorganization applies the Subtraction Before Addition principle: remove and consolidate first, then establish a predictable directory structure that agents, hooks, and DuckDB ingestion pipelines can navigate with >98% confidence on blind evaluation.

## Glossary

- **Shared_Directory**: The `~/shared/` directory tree — the persistent, cross-session file system for all context, tools, data, and artifacts
- **Body_Organ**: A self-contained markdown file in `~/shared/context/body/` representing one function of the personal operating system (e.g., brain.md, spine.md, hands.md)
- **Portable_Body**: The `~/shared/portable-body/` directory — a cold-start bootstrap kit containing copies of all organs, agents, hooks, steering, voice, research, tools, and specs needed to rebuild the system on a new platform
- **Directory_Map**: A machine-readable and human-readable manifest listing every top-level and second-level path in `~/shared/`, its purpose, and what writes to it
- **Path_Reference**: Any hardcoded file path appearing in a body organ, steering file, agent config, hook config, or soul.md that points to a location within `~/shared/` or `~/.kiro/`
- **Dead_Weight**: Files or directories that consume storage without serving an active purpose (stale exports, empty folders, abandoned tooling, debug artifacts)
- **DuckDB_Data_Path**: A standardized directory location where data files (CSV, Parquet, XLSX) are stored for DuckDB ingestion and querying
- **Blind_Evaluator_Test**: A test where an agent is given only the Directory_Map and a file-finding prompt, with no prior session context, and must locate the correct file path — target >98% accuracy across test prompts
- **Ingestion_Pipeline**: The flow from file drop (uploads/) through processing to queryable data in DuckDB and/or organ updates
- **Ground_Truth_File**: A file in `~/shared/context/active/` that holds live state and is NOT absorbed into organs (e.g., current.md, org-chart.md, rw-tracker.md)

## Requirements

### Requirement 1: Dead Weight Removal

**User Story:** As Richard, I want all non-essential files and directories removed from ~/shared/, so that the directory is lean, navigable, and storage is not wasted on abandoned artifacts.

#### Acceptance Criteria

1. WHEN the reorganization begins, THE Shared_Directory SHALL have the following Dead_Weight items removed or archived: `agentspaces-desktop-launcher/` (320MB Electron app), `.aim/` (246MB stale experiment tracking), `rw-shared-export-2026-03-21.tar.gz` (30MB old export), and `scripts/` (empty folder)
2. WHEN stale temporary files exist in `research/` (err.txt, 0-byte files, xlsx output dumps, daily-brief-latest.md runtime artifact), THE Shared_Directory SHALL have those files removed
3. WHEN 0-byte files or debug artifacts exist in `context/active/`, THE Shared_Directory SHALL have those files removed
4. WHEN debug scripts exist mixed with production scripts in `context/tools/`, THE Shared_Directory SHALL have debug scripts moved to a clearly labeled debug or scratch location, or removed if no longer needed
5. IF a file marked for removal is referenced by any Path_Reference in an organ, steering file, agent config, or hook, THEN THE reorganization process SHALL update or remove that reference before deleting the file

### Requirement 2: Canonical Directory Structure

**User Story:** As Richard, I want a single, predictable directory structure for ~/shared/ that every agent, hook, and organ can rely on, so that there is exactly one correct location for every file type.

#### Acceptance Criteria

1. THE Shared_Directory SHALL maintain the following top-level structure after reorganization:
   - `context/` — all live context (active/, archive/, body/, changelog.md, intake/, meetings/, tools/, wiki/)
   - `artifacts/` — published work product organized by category
   - `tools/` — active automation tools and scripts
   - `uploads/` — human drop zone with typed subfolders
   - `data/` — DuckDB databases, ingested data files, and data pipeline outputs
   - `portable-body/` — cold-start bootstrap kit
   - `.kiro/` — agents, hooks, specs, steering, settings
   - `audit-reports/` — system audit outputs
2. WHEN a new file is created by any agent or process, THE agent or process SHALL place the file in the location specified by the Directory_Map for that file type
3. THE Shared_Directory SHALL NOT contain any top-level files other than `.gitignore`, `README.md`, and `DIRECTORY-MAP.md`
4. WHEN `reference/` contains only an index.md with no substantive reference content, THE reorganization process SHALL merge its content into `artifacts/` or `context/wiki/` and remove the empty `reference/` directory

### Requirement 3: Directory Map as Single Source of Truth

**User Story:** As Richard, I want a machine-readable directory map that defines where every file type belongs, so that agents never have to guess paths and new agents can orient instantly.

#### Acceptance Criteria

1. THE Directory_Map SHALL be created as a standalone file at `~/shared/DIRECTORY-MAP.md` AND the directory map section of `spine.md` SHALL reference the Directory_Map as the authoritative source
2. THE Directory_Map SHALL list every top-level and second-level directory in `~/shared/`, with: path, purpose (one sentence), what writes to it (agent/human/hook/process), and update cadence
3. THE Directory_Map SHALL list the canonical location for each file type: data files, context files, tool scripts, artifacts, uploads, meeting notes, wiki articles, research documents, and audit reports
4. WHEN a path conflict exists (the same file type could go in two places), THE Directory_Map SHALL resolve the conflict by specifying exactly one canonical location
5. WHEN the Directory_Map is updated, THE Shared_Directory structure SHALL match the Directory_Map within the same operation — the map and the filesystem SHALL remain synchronized

### Requirement 4: DuckDB Data Path Standardization

**User Story:** As Richard, I want all data files to live in predictable, well-defined paths so that DuckDB ingestion scripts can find and load data without path-hunting or hardcoded exceptions.

#### Acceptance Criteria

1. THE Shared_Directory SHALL contain a `data/` top-level directory with the following subdirectories:
   - `data/duckdb/` — DuckDB database files (.duckdb, .wal)
   - `data/raw/` — unprocessed data files awaiting ingestion (CSV, XLSX, Parquet)
   - `data/processed/` — data files that have been ingested into DuckDB
   - `data/exports/` — query results and data exports generated by tools or agents
2. WHEN a data file is uploaded via `uploads/sheets/`, THE Ingestion_Pipeline SHALL copy or move the file to `data/raw/` before DuckDB ingestion
3. WHEN a data file has been successfully ingested into DuckDB, THE Ingestion_Pipeline SHALL move the source file from `data/raw/` to `data/processed/` with a timestamp prefix
4. WHEN DuckDB data files currently exist in `tools/data/` or scattered across other directories, THE reorganization process SHALL move those files to the appropriate `data/` subdirectory and update all Path_References accordingly
5. THE `data/` directory SHALL contain a `README.md` documenting the ingestion flow, file naming conventions, and the relationship between uploads/, data/raw/, data/processed/, and data/duckdb/

### Requirement 5: Archive Structure

**User Story:** As Richard, I want the archive directory to have clear structure by content type and time period, so that archived files are findable without scrolling through a flat dump.

#### Acceptance Criteria

1. WHEN files are archived from `context/active/` or other locations, THE `context/archive/` directory SHALL organize them into subdirectories by category: `context/`, `research/`, `tools/`, and `misc/`
2. WHEN a file is moved to archive, THE archival process SHALL prefix the filename with the archive date in `YYYY-MM-DD` format (e.g., `2026-03-15_old-analysis.md`)
3. THE `context/archive/` directory SHALL contain a `README.md` listing the archive categories and the criteria for when a file should be archived versus deleted
4. WHEN the existing flat archive contains files from different categories, THE reorganization process SHALL sort those files into the appropriate archive subdirectories

### Requirement 6: Active Directory Cleanup

**User Story:** As Richard, I want context/active/ to contain only Ground Truth Files that are actively maintained, so that it stops being a dumping ground for miscellaneous scripts and stale analysis.

#### Acceptance Criteria

1. THE `context/active/` directory SHALL contain ONLY the following Ground_Truth_Files: `current.md`, `org-chart.md`, `rw-tracker.md`, `long-term-goals.md`, `asana-sync-protocol.md`, and `mcp-tool-reference.md`
2. WHEN Python scripts exist in `context/active/`, THE reorganization process SHALL move them to `tools/` or `context/tools/` based on their function
3. WHEN analysis CSVs or data files exist in `context/active/`, THE reorganization process SHALL move them to `data/raw/` or `data/processed/` based on their ingestion status
4. WHEN reference documents exist in `context/active/` that are not Ground_Truth_Files, THE reorganization process SHALL move them to `context/wiki/`, `artifacts/`, or `context/archive/` based on their content type and currency

### Requirement 7: Path Reference Consistency

**User Story:** As Richard, I want every path reference in every organ, steering file, agent config, hook config, and soul.md to point to a valid, canonical location, so that no agent encounters a broken path.

#### Acceptance Criteria

1. WHEN the directory structure changes, THE reorganization process SHALL scan all Body_Organs for Path_References and update each reference to the new canonical path
2. WHEN the directory structure changes, THE reorganization process SHALL scan all steering files in `~/.kiro/steering/` for Path_References and update each reference to the new canonical path
3. WHEN the directory structure changes, THE reorganization process SHALL scan all agent configs in `~/.kiro/agents/` for Path_References and update each reference to the new canonical path
4. WHEN the directory structure changes, THE reorganization process SHALL scan all hook configs in `~/.kiro/hooks/` for Path_References and update each reference to the new canonical path
5. WHEN the directory structure changes, THE reorganization process SHALL update `soul.md` Path_References to reflect the new canonical paths
6. WHEN body.md contains the system anatomy table with file paths, THE reorganization process SHALL update every path in that table to match the post-reorganization structure
7. IF a Path_Reference points to a file that no longer exists after reorganization, THEN THE reorganization process SHALL either create the file at the referenced location or remove the reference

### Requirement 8: Portable Body Sync

**User Story:** As Richard, I want portable-body/ to reflect the current state of all organs, agents, hooks, steering, voice, research, tools, and specs, so that a cold-start bootstrap on a new platform works without stale references.

#### Acceptance Criteria

1. WHEN the reorganization is complete, THE Portable_Body SHALL contain current copies of all 11 Body_Organs from `~/shared/context/body/`
2. WHEN the reorganization is complete, THE Portable_Body SHALL contain current copies of all agent configs, steering files, hook descriptions, voice guides, research files, tool scripts, and spec files
3. WHEN the reorganization is complete, THE Portable_Body `README.md` SHALL reflect the updated file count, directory structure, and last-synced date
4. WHEN the reorganization is complete, THE Portable_Body `portable-layer.md` SHALL document which paths are portable (relative, text-only) and which are environment-specific (absolute paths, MCP tools, hook JSON)
5. WHEN any Path_Reference inside Portable_Body files points to a `~/shared/` location, THE Portable_Body SHALL use the post-reorganization canonical path
6. THE Portable_Body `CHANGELOG.md` SHALL record the reorganization as a version entry with a summary of structural changes

### Requirement 9: Research Directory Cleanup

**User Story:** As Richard, I want the research/ directory to contain only active, substantive research files, so that it is not polluted with temp files, debug output, or runtime artifacts.

#### Acceptance Criteria

1. THE `research/` directory SHALL contain only research documents, analysis files, and their supporting build scripts
2. WHEN stale temp files (err.txt, 0-byte files, xlsx dumps not tied to active research) exist in `research/`, THE reorganization process SHALL remove them
3. WHEN runtime artifacts (daily-brief-latest.md) exist in `research/`, THE reorganization process SHALL move them to `context/intake/` or remove them
4. THE `research/` directory structure SHALL match what is documented in the Portable_Body research section

### Requirement 10: Context Tools Separation

**User Story:** As Richard, I want context/tools/ to contain only production-ready utility scripts, with debug and experimental scripts clearly separated, so that hooks and agents can trust that everything in context/tools/ is safe to run.

#### Acceptance Criteria

1. THE `context/tools/` directory SHALL contain only production-ready Python utility scripts used by hooks, agents, or the morning routine
2. WHEN a script in `context/tools/` is a debug or one-off script, THE reorganization process SHALL move the script to `tools/scratch/` or remove it
3. THE `context/tools/` directory SHALL contain a `README.md` listing each script, its purpose, what invokes it, and its dependencies

### Requirement 11: Blind Evaluator Test Suite

**User Story:** As Richard, I want a blind evaluator test that confirms agents can find any file in the reorganized structure with >98% accuracy, so that I have measurable confidence the reorganization actually works.

#### Acceptance Criteria

1. THE Blind_Evaluator_Test SHALL consist of at least 50 file-finding prompts covering all major file categories: organs, ground truth files, data files, tools, artifacts, meeting notes, wiki articles, research docs, uploads, and agent configs
2. WHEN a Blind_Evaluator_Test is run, THE test agent SHALL receive ONLY the Directory_Map and the test prompt — no prior session context, no organ content, no file listings beyond the map
3. THE Blind_Evaluator_Test SHALL measure accuracy as: (correct file paths returned) / (total prompts) and the target accuracy SHALL be greater than 98%
4. THE Blind_Evaluator_Test SHALL include adversarial prompts that test common confusion points: "Where do I put a new CSV?" (uploads/sheets/ vs data/raw/), "Where is the experiment queue?" (heart.md), "Where are debug scripts?" (tools/scratch/ or removed)
5. WHEN the Blind_Evaluator_Test accuracy falls below 98%, THE test results SHALL identify which prompts failed and which Directory_Map entries caused confusion
6. THE Blind_Evaluator_Test prompts and expected answers SHALL be stored as a reusable test file at `~/shared/audit-reports/blind-evaluator-tests.md`

### Requirement 12: Credentials and Sensitive File Isolation

**User Story:** As Richard, I want credentials and sensitive authentication files to remain in their current secure locations and not be moved or exposed during reorganization, so that security is maintained.

#### Acceptance Criteria

1. THE reorganization process SHALL NOT move, copy, or modify files in `~/shared/credentials/` or `~/shared/.agentspaces/`
2. THE Directory_Map SHALL list `credentials/` and `.agentspaces/` as protected directories with a note that their contents are not to be moved or reorganized
3. IF any Path_Reference to a credentials file needs updating, THEN THE reorganization process SHALL update only the reference, not the credential file itself

### Requirement 13: Top-Level README

**User Story:** As Richard, I want a top-level README.md in ~/shared/ that orients any agent or human to the directory structure in under 30 seconds, so that new sessions and new platforms start fast.

#### Acceptance Criteria

1. THE Shared_Directory SHALL contain a `README.md` at `~/shared/README.md` that provides: a one-paragraph system summary, a table of top-level directories with one-line descriptions, a pointer to `DIRECTORY-MAP.md` for full detail, and a pointer to `context/body/body.md` for system navigation
2. THE `README.md` SHALL be no longer than 50 lines to ensure quick orientation
3. WHEN the directory structure changes, THE `README.md` SHALL be updated to reflect the current top-level structure
