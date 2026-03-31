# Requirements Document

## Introduction

This document defines the requirements for a comprehensive workspace migration and reorganization effort. The goal is to transform the current ~/shared/ directory from an organically grown file structure into a well-organized, canonical workspace with clear separation of concerns. The migration covers eight phases: workspace symlink setup, dead weight removal, canonical directory creation, key document creation, agent/hook verification, path reference updates, portable body source-of-truth establishment, and blind evaluator testing. The target outcome is a workspace where any agent or human can locate any file with >98% accuracy using only the DIRECTORY-MAP.md.

## Glossary

- **Workspace**: The ~/shared/ directory and its contents, accessed via /home/ as the IDE root
- **Migration_System**: The set of scripts, commands, and processes that execute the workspace reorganization
- **Directory_Map**: The DIRECTORY-MAP.md file serving as the single source of truth for file locations
- **Symlink**: A symbolic link at /home/.kiro pointing to ~/shared/.kiro, enabling agent/hook discovery
- **Dead_Weight**: Non-essential files totaling ~596MB including abandoned projects, temp files, and misplaced artifacts
- **Canonical_Structure**: The target directory hierarchy with defined purposes for each path
- **Ingestion_Pipeline**: The data flow from uploads/ through data/raw/ to data/processed/ via DuckDB
- **Portable_Body**: The portable-body/ directory serving as the Architectural_Source of all 11 body organs — containing organ structure, protocols, frameworks, and portable content as defined by the Portable_Layer_Manifest
- **Enriched_Working_Copy**: The context/body/ directory, derived from Portable_Body and enriched with Environment_Specific_Data (contacts, current metrics, live state, tool IDs, etc.) for day-to-day agent use
- **Architectural_Source**: The origin layer for structural and architectural content — organ layout, protocol definitions, framework designs, and portable content. Edits to structure originate here and flow down to the Enriched_Working_Copy
- **Environment_Specific_Data**: Content that belongs only to the current work context — Amazon contacts, current metrics, live operational state, tool IDs, Asana/Outlook integrations, and similar non-portable data. Written directly to context/body/ by agents and hooks during daily operations
- **Portable_Layer_Manifest**: The portable-layer.md file that defines per-organ what content is portable (architecture) vs what to strip (environment-specific). Serves as the governing document for the Portable_Body / Enriched_Working_Copy separation
- **Blind_Evaluator**: A fresh agent given only the Directory_Map, used to validate workspace navigability
- **Body_Organs**: The 11 markdown files representing system state (brain, heart, gut, etc.), architecturally maintained in portable-body/ and derived with enrichment into context/body/
- **Protected_Directory**: A directory that must never be moved or deleted (credentials/, .agentspaces/)
- **Ground_Truth_Files**: Active context files in context/active/ representing current operational state
- **Verification_Script**: A bash script that checks agents, hooks, steering, scripts, DuckDB, and broken paths post-migration

## Requirements

### Requirement 1: Workspace Symlink Setup

**User Story:** As a workspace user, I want the IDE to discover agents, hooks, and steering files when /home/ is opened as the workspace root, so that all automation continues to function after migration.

#### Acceptance Criteria

1. WHEN the workspace is opened at /home/, THE Migration_System SHALL have created a symbolic link at /home/.kiro pointing to ~/shared/.kiro
2. WHEN the Symlink is created, THE Migration_System SHALL create a /home/.vscode/settings.json file containing file exclusion patterns for system directories, dotfiles, and non-essential home directory contents
3. WHEN the workspace is opened at /home/, THE Migration_System SHALL ensure that all agent definitions in .kiro/agents/ are discoverable by the IDE
4. WHEN the workspace is opened at /home/, THE Migration_System SHALL ensure that all hook definitions in .kiro/hooks/ are discoverable by the IDE
5. WHEN the workspace is opened at /home/, THE Migration_System SHALL ensure that all steering files in .kiro/steering/ are loadable by the IDE

### Requirement 2: Dead Weight Removal

**User Story:** As a workspace user, I want non-essential files and directories removed from ~/shared/, so that the workspace contains only purposeful content and reclaims ~596MB of storage.

#### Acceptance Criteria

1. THE Migration_System SHALL remove the agentspaces-desktop-launcher/ directory from ~/shared/
2. THE Migration_System SHALL remove the .aim/ directory from ~/shared/
3. THE Migration_System SHALL remove the rw-shared-export-2026-03-21.tar.gz archive from ~/shared/
4. THE Migration_System SHALL remove the empty scripts/ directory from ~/shared/
5. THE Migration_System SHALL remove temporary files (err.txt, brand_nb_data.txt, xlsx_output.txt, xlsx_full_output.txt, daily-brief-latest.md) from ~/shared/research/
6. THE Migration_System SHALL remove zero-byte files (au-ps-w9-13-optimization-pt2.md, au-ps-w9-13-pt2.md) from ~/shared/context/active/
7. WHEN misplaced files are identified in context/active/, THE Migration_System SHALL relocate parse-au-search-terms.py to ~/shared/tools/
8. WHEN misplaced analysis directories are identified in context/active/, THE Migration_System SHALL relocate au-analysis/ to ~/shared/data/processed/au-analysis-w9-13/
9. WHEN debug scripts are identified in context/tools/, THE Migration_System SHALL relocate mcp_debug.py, mcp_scan.py, mcp_test.py, and mcp_test2.py to ~/shared/uploads/scratch/
10. WHEN the reference/ directory contains only index.md, THE Migration_System SHALL append its contents to ~/shared/artifacts/SITEMAP.md and remove the reference/ directory


### Requirement 3: Canonical Directory Structure Creation

**User Story:** As a workspace user, I want a well-defined directory hierarchy with clear separation of concerns, so that every file type has exactly one canonical location.

#### Acceptance Criteria

1. THE Migration_System SHALL create the data directory hierarchy: data/duckdb/, data/raw/, data/processed/, data/exports/, data/testing/
2. THE Migration_System SHALL create per-market data directories under data/markets/ for each market code: au, mx, us, ca, jp, uk, de, fr, it, es
3. THE Migration_System SHALL create the artifacts directory hierarchy: artifacts/weekly-ships/, artifacts/testing/active/, artifacts/testing/completed/, artifacts/testing/templates/, artifacts/frameworks/
4. THE Migration_System SHALL create the tools directory hierarchy: tools/team/, tools/team/docs/, tools/autonomous/, tools/autonomous/logs/, tools/autonomous/configs/, tools/scratch/
5. THE Migration_System SHALL create the archive directory hierarchy: context/archive/context/, context/archive/research/, context/archive/tools/, context/archive/misc/
6. THE Migration_System SHALL create the research/aeo/ directory for AEO/AI Overviews research
7. WHEN existing DuckDB files (.duckdb, .wal) are found in tools/data/, THE Migration_System SHALL move them to data/duckdb/
8. WHEN existing CSV files are found in tools/data/, THE Migration_System SHALL move them to data/raw/
9. WHEN existing Parquet files are found in tools/data/, THE Migration_System SHALL move them to data/raw/

### Requirement 4: Key Document Creation

**User Story:** As a workspace user, I want a single-source-of-truth directory map and data ingestion documentation, so that any agent or human can determine where files belong without ambiguity.

#### Acceptance Criteria

1. THE Migration_System SHALL create a DIRECTORY-MAP.md file at ~/shared/DIRECTORY-MAP.md
2. THE Directory_Map SHALL contain a table mapping every top-level directory path to its purpose, write permissions, and update cadence
3. THE Directory_Map SHALL contain a file-type-to-location mapping table that specifies the drop location and final location for each file type (CSV/XLSX, changelogs, documents, agent analysis, DuckDB databases, test designs, meeting notes, wiki articles, scripts, team tools)
4. THE Migration_System SHALL create a data/README.md file documenting the Ingestion_Pipeline flow
5. THE data/README.md SHALL document the five-step ingestion flow: drop in uploads/ → copy to data/raw/ → DuckDB load → move to data/processed/ with date prefix → exports to data/exports/
6. THE data/README.md SHALL document the naming conventions: raw files keep original names, processed files use YYYY-MM-DD_original-filename format, exports use agent-description-YYYY-MM-DD format

### Requirement 5: Agent, Hook, and Process Verification

**User Story:** As a workspace user, I want to verify that all agents, hooks, steering files, scripts, and data connections are intact after migration, so that no automation is broken by the reorganization.

#### Acceptance Criteria

1. WHEN the migration is complete, THE Verification_Script SHALL enumerate all agent definitions in ~/shared/.kiro/agents/
2. WHEN the migration is complete, THE Verification_Script SHALL enumerate all hook definitions in ~/shared/.kiro/hooks/ and display each hook's name, event type, and action type
3. WHEN the migration is complete, THE Verification_Script SHALL enumerate all steering files in ~/shared/.kiro/steering/, ~/shared/.kiro/steering-chat/, and ~/shared/.kiro/steering-code/
4. WHEN the migration is complete, THE Verification_Script SHALL enumerate all production scripts in ~/shared/context/tools/
5. WHEN the migration is complete, THE Verification_Script SHALL enumerate all tool subdirectories in ~/shared/tools/
6. WHEN the migration is complete, THE Verification_Script SHALL verify that DuckDB database files exist in ~/shared/data/duckdb/
7. WHEN the migration is complete, THE Verification_Script SHALL scan for broken path references to moved or deleted locations (tools/data/, context/active/au-analysis/, agentspaces-desktop-launcher/, reference/) in body/, steering/, agents/, and hooks/ files
8. IF the Verification_Script detects broken path references, THEN THE Verification_Script SHALL report each broken reference with the file path and line number

### Requirement 6: Path Reference Updates

**User Story:** As a workspace user, I want all internal path references updated to reflect the new directory structure, so that no file references point to moved or deleted locations.

#### Acceptance Criteria

1. WHEN path references to tools/data/ are found, THE Migration_System SHALL update them to data/duckdb/ or data/raw/ as appropriate
2. WHEN path references to context/active/au-analysis/ are found, THE Migration_System SHALL update them to data/processed/au-analysis-w9-13/
3. WHEN path references to reference/ are found, THE Migration_System SHALL update them to artifacts/
4. WHEN path references to agentspaces-desktop-launcher/ are found, THE Migration_System SHALL remove those references
5. WHEN path references to .aim/ are found, THE Migration_System SHALL remove those references
6. WHEN path references to scripts/ are found, THE Migration_System SHALL remove those references
7. THE Migration_System SHALL scan all files in context/body/, .kiro/steering/, .kiro/agents/, .kiro/hooks/, and steering files for stale path references

### Requirement 7: Portable Body as Architectural Source with Enriched Working Copy

**User Story:** As a workspace user, I want portable-body/ to be the architectural source of all body organs and context/body/ to be the enriched working copy, so that structural changes originate in portable-body/ and flow down to context/body/ where environment-specific content is layered on.

#### Acceptance Criteria

1. THE Portable_Body SHALL be the Architectural_Source for all 11 Body_Organs, containing organ structure, protocols, frameworks, and portable content as defined by the Portable_Layer_Manifest
2. THE Enriched_Working_Copy (context/body/) SHALL be derived from the Portable_Body and enriched with Environment_Specific_Data for day-to-day agent use
3. WHEN a structural or architectural change is made to a Body_Organ (new sections, protocol changes, framework updates), THE Migration_System SHALL apply the change to the Portable_Body first, then derive the change into the Enriched_Working_Copy
4. WHILE agents and hooks perform daily operations (loop runs, morning routine data refreshes, metric updates), THE Migration_System SHALL permit direct writes of Environment_Specific_Data to the Enriched_Working_Copy without requiring a round-trip through the Portable_Body
5. THE Portable_Layer_Manifest SHALL serve as the governing document that defines per-organ what content is portable (architecture) vs what is environment-specific (to strip on export)
6. WHEN the reorganization is complete, THE Migration_System SHALL update all 11 Body_Organs in the Portable_Body to reflect the post-reorg Canonical_Structure
7. WHEN the Portable_Body is updated, THE Migration_System SHALL derive the Enriched_Working_Copy by copying all 11 Body_Organs from portable-body/ to context/body/ and preserving any existing Environment_Specific_Data already present in context/body/
8. WHEN the Portable_Body is updated, THE Migration_System SHALL update portable-body/README.md with the current file count and the sync date
9. WHEN the Portable_Body is updated, THE Migration_System SHALL update portable-body/CHANGELOG.md with a version entry documenting the reorganization
10. WHEN the Portable_Body is updated, THE Migration_System SHALL update the Portable_Layer_Manifest with the new Canonical_Structure
11. THE Migration_System SHALL verify that all path references inside portable-body/ files use post-reorg paths before deriving the Enriched_Working_Copy
12. IF stale path references are found in portable-body/ files, THEN THE Migration_System SHALL update them to reflect the new Canonical_Structure before deriving the Enriched_Working_Copy

### Requirement 8: Blind Evaluator Validation

**User Story:** As a workspace user, I want to validate that a fresh agent can navigate the new workspace structure using only the Directory_Map, so that the reorganization achieves its goal of intuitive navigability.

#### Acceptance Criteria

1. THE Migration_System SHALL create a blind-evaluator-tests.md file at ~/shared/audit-reports/blind-evaluator-tests.md
2. THE blind-evaluator-tests.md SHALL contain a minimum of 50 test prompts covering all major directory paths and file types
3. WHEN the Blind_Evaluator is given only the Directory_Map and the test prompts, THE Blind_Evaluator SHALL answer each prompt with the correct canonical path
4. THE Blind_Evaluator SHALL achieve greater than 98% accuracy across all test prompts
5. THE blind-evaluator-tests.md SHALL include prompts covering: upload drop zones, body organ locations, per-market callout paths, debug script locations, DuckDB database paths, weekly ship logs, testing frameworks, agent export destinations, org chart location, team tool locations, meeting note paths, AEO research paths, autonomous workflow configs, production script locations, and processed data file destinations
6. IF the Blind_Evaluator accuracy is below 98%, THEN THE Migration_System SHALL identify ambiguous or missing entries in the Directory_Map and update the Directory_Map to resolve the ambiguities

### Requirement 9: Protected Directory Safety

**User Story:** As a workspace user, I want credentials/ and .agentspaces/ directories to remain untouched during migration, so that authentication and system state are preserved.

#### Acceptance Criteria

1. THE Migration_System SHALL preserve the credentials/ directory in its current location without modification
2. THE Migration_System SHALL preserve the .agentspaces/ directory in its current location without modification
3. IF a migration operation targets a Protected_Directory, THEN THE Migration_System SHALL skip the operation and log a warning

### Requirement 10: Data Ingestion Flow Integrity

**User Story:** As a workspace user, I want the data ingestion pipeline to function correctly with the new directory structure, so that data files flow from upload to DuckDB without manual intervention.

#### Acceptance Criteria

1. WHEN a CSV or XLSX file is placed in uploads/sheets/, THE Ingestion_Pipeline SHALL copy the file to data/raw/
2. WHEN a changelog file is placed in uploads/changelogs/, THE Ingestion_Pipeline SHALL copy the file to data/raw/
3. WHEN a file in data/raw/ is loaded into DuckDB, THE Ingestion_Pipeline SHALL move the source file to data/processed/ with a YYYY-MM-DD date prefix
4. WHEN an agent generates export data, THE Ingestion_Pipeline SHALL write the export to data/exports/ using the naming convention agent-description-YYYY-MM-DD.csv
5. WHEN per-market data is generated, THE Ingestion_Pipeline SHALL store the data in the appropriate data/markets/{market_code}/ directory

### Requirement 11: Agent Comprehension Guard Rail for Portable Body

**User Story:** As a workspace user, I want agents to understand the portable vs environment-specific separation before modifying portable-body/ files, so that no agent blindly writes to the Architectural_Source without understanding the system's layered architecture.

#### Acceptance Criteria

1. THE Migration_System SHALL create a portable-body/README.md that explains the Architectural_Source model: portable-body/ is the structural source of truth, context/body/ is the Enriched_Working_Copy, and the Portable_Layer_Manifest governs what is portable vs environment-specific
2. THE portable-body/README.md SHALL instruct any agent to read the Portable_Layer_Manifest before making any write or modification to files in portable-body/
3. THE portable-body/README.md SHALL document the content flow: architectural edits originate in portable-body/ and derive down to context/body/, while environment-specific daily updates write directly to context/body/
4. WHEN an agent or hook is configured to operate on portable-body/ files, THE Migration_System SHALL include a steering directive (via agent definition, hook instruction, or preToolUse hook) that requires the agent to read the Portable_Layer_Manifest before executing writes to portable-body/
5. THE steering directive SHALL ensure the agent can distinguish between portable content (organ structure, protocols, frameworks) and Environment_Specific_Data (contacts, metrics, live state, tool IDs) before making edits
6. IF an agent attempts to write Environment_Specific_Data to a portable-body/ file, THEN THE steering directive SHALL redirect the write to the corresponding file in context/body/ instead
