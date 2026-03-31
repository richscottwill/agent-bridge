# Implementation Plan: Wiki-SharePoint Sync

## Overview

Build the Wiki-SharePoint Sync tool at `~/shared/tools/sharepoint-sync/` following the bridge.py pattern. Implementation proceeds bottom-up: data models and config first, then filters and front-matter, then core engine components (manifest, conflict, converter, graph client), then the sync engine orchestrator, then CLI, then integration wiring. Each step builds on the previous and is independently testable.

## Tasks

- [x] 1. Set up project structure, dependencies, and data models
  - [x] 1.1 Create project directory and requirements.txt
    - Create `~/shared/tools/sharepoint-sync/` directory
    - Create `requirements.txt` with: msal>=1.24.0, requests>=2.31.0, python-frontmatter>=1.1.0, python-docx>=1.1.0, markdown>=3.5.0, pyyaml>=6.0.1
    - Create empty `__init__.py` and `tests/__init__.py`
    - _Requirements: 11.1_

  - [x] 1.2 Implement data models in `models.py`
    - Define `ArticleMetadata` dataclass (title, status, audience, level, owner, created, updated, update_trigger, slug, tags)
    - Define `ArticleAction` dataclass (file_path, action, mode, sp_url, error, duration)
    - Define `SyncReport` dataclass with category lists (created, updated, skipped_unchanged, skipped_filtered, conflicted, removed, failed), `has_failures` property, and `summary()` method
    - Define `ConflictResult` dataclass (is_conflict, local_modified, sp_modified, details)
    - Define custom exceptions: `ConfigError`, `AuthError`, `FrontMatterError`, `GraphAPIError`, `ConversionError`
    - _Requirements: 9.1, 9.2, 9.4, 3.2_

- [x] 2. Implement configuration loading
  - [x] 2.1 Create `config.yaml` with default structure
    - SharePoint section: tenant_id, client_id, client_secret (env var references), site_url, document_library
    - Sync section: mode, eligible_statuses (REVIEW, FINAL), articles_path, wiki_index_path, manifest_path
    - _Requirements: 11.1, 11.2_

  - [x] 2.2 Implement config loading in `sync.py` (config portion only)
    - Load YAML config from configurable path (default: `~/shared/tools/sharepoint-sync/config.yaml`)
    - Resolve `${ENV_VAR}` references in string values to environment variable values
    - Validate required fields are present; raise `ConfigError` with specific missing field names on failure
    - Support CLI argument overrides via a `config_overrides` dict parameter
    - _Requirements: 11.1, 11.2, 11.3, 11.4_

  - [ ]* 2.3 Write property test for config validation (Property 15)
    - **Property 15: Invalid configuration produces descriptive errors**
    - Generate random invalid configs (missing file, invalid YAML, missing required fields) and verify `ConfigError` is raised with a message identifying the specific problem
    - **Validates: Requirements 11.3**

  - [ ]* 2.4 Write property test for CLI config override (Property 14)
    - **Property 14: CLI arguments override config file values**
    - Generate random config file values and CLI override values, verify CLI values take precedence
    - **Validates: Requirements 11.4**

- [x] 3. Implement filters and front-matter I/O
  - [x] 3.1 Implement `AudienceFilter` and `StatusFilter` in `filters.py`
    - `AudienceFilter.is_eligible(metadata)` returns `(bool, str)` — eligible only for "amazon-internal"; missing audience returns False with warning
    - `StatusFilter.__init__(eligible_statuses)` with default `['REVIEW', 'FINAL']`; configurable from config
    - `StatusFilter.is_eligible(metadata)` returns `(bool, str)` — case-insensitive membership check
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 2.1, 2.2, 2.3_

  - [ ]* 3.2 Write property test for audience filter (Property 1)
    - **Property 1: Audience filter eligibility is determined solely by audience field value**
    - Generate random metadata dicts with various audience values; verify eligible=True iff audience=="amazon-internal"
    - **Validates: Requirements 1.1, 1.2, 1.3, 1.4**

  - [ ]* 3.3 Write property test for status filter (Property 2)
    - **Property 2: Status filter eligibility is determined by membership in the eligible statuses list**
    - Generate random metadata and random eligible status lists; verify eligible=True iff status in list (case-insensitive)
    - **Validates: Requirements 2.2, 2.3, 2.5**

  - [x] 3.4 Implement `FrontMatterParser` and `FrontMatterPrinter` in `frontmatter_io.py`
    - `FrontMatterParser.parse(file_path)` returns `(metadata_dict, markdown_body)` using `python-frontmatter`
    - Raises `FrontMatterError` with file path and failure description on malformed/missing front-matter
    - `FrontMatterPrinter.print(metadata)` serializes metadata dict back to YAML front-matter string with `---` delimiters
    - _Requirements: 3.1, 3.2, 3.3_

  - [ ]* 3.5 Write property test for front-matter round-trip (Property 3)
    - **Property 3: Front-matter round-trip integrity**
    - Generate random valid metadata dicts, serialize with Printer, parse with Parser, compare to original
    - **Validates: Requirements 3.1, 3.3, 3.4**

  - [ ]* 3.6 Write property test for malformed front-matter errors (Property 4)
    - **Property 4: Malformed front-matter produces descriptive errors**
    - Generate random invalid YAML strings (missing delimiters, bad syntax, empty); verify `FrontMatterError` raised with file path and description
    - **Validates: Requirements 3.2**

- [x] 4. Checkpoint — Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [x] 5. Implement sync manifest and conflict resolver
  - [x] 5.1 Implement `SyncManifest` in `manifest.py`
    - Load/create JSON manifest file at configurable path
    - `get_entry(file_path, mode)` — lookup by path + mode
    - `add_entry(file_path, mode, content_hash, sp_item_id, sp_url)` — add after successful upload
    - `update_entry(file_path, mode, content_hash, synced_at)` — update after successful update
    - `remove_entry(file_path, mode)` — remove after SP deletion
    - `all_entries(mode=None)` — list entries, optionally filtered by mode
    - `save()` — persist to disk
    - Manifest JSON structure: `{ "version": 1, "last_sync": "...", "entries": [...] }`
    - _Requirements: 6.1, 10.3_

  - [ ]* 5.2 Write property test for dual-mode manifest entries (Property 12)
    - **Property 12: Dual-mode produces independent manifest entries per mode**
    - Add entries for same file_path with mode="site" and mode="directory"; verify two independent entries exist with separate hashes, item IDs, and timestamps
    - **Validates: Requirements 10.2, 10.3**

  - [x] 5.3 Implement `ConflictResolver` in `conflict.py`
    - `check(manifest_entry, sp_metadata, local_changed)` returns `ConflictResult`
    - Conflict flagged only when BOTH SP lastModifiedDateTime > manifest synced_at AND local content hash differs
    - If only one side changed, no conflict
    - _Requirements: 7.1, 7.2_

  - [ ]* 5.4 Write property test for conflict detection (Property 7)
    - **Property 7: Conflict detection when both sides changed**
    - Generate random timestamp combinations (SP modified, manifest synced_at, local_changed bool); verify conflict flagged iff both sides changed
    - **Validates: Requirements 7.1, 7.2, 7.3**

  - [ ]* 5.5 Write property test for force-overwrite (Property 8)
    - **Property 8: Force-overwrite bypasses conflict detection**
    - Generate conflicted articles with force=True; verify action is "updated" not "conflicted"
    - **Validates: Requirements 7.5**

- [x] 6. Implement markdown converter and Graph API client
  - [x] 6.1 Implement `MarkdownConverter` in `converter.py`
    - `to_html(markdown_body)` — convert markdown to SharePoint-compatible HTML using `markdown` library
    - `to_docx(markdown_body, metadata)` — convert markdown to .docx bytes using `python-docx`, preserving headings, lists, tables, code blocks; include title from metadata
    - _Requirements: 4.2, 5.3_

  - [x] 6.2 Implement `GraphAPIClient` in `graph_client.py`
    - `__init__(tenant_id, client_id, client_secret)` — initialize MSAL confidential client
    - `authenticate()` — acquire token via client credentials flow; cache and auto-refresh before expiry
    - Site mode operations: `create_site_page`, `update_site_page`, `delete_site_page`, `get_site_page_metadata`
    - Directory mode operations: `upload_file`, `delete_file`, `get_file_metadata`, `ensure_folder`, `update_list_item_fields`
    - Navigation: `update_navigation(site_id, nav_nodes)`
    - Retry logic: HTTP 429 → wait Retry-After header, retry up to 3 times; HTTP 503 → exponential backoff (1s, 2s, 4s), retry up to 3 times
    - Raise `AuthError` on auth failure with HTTP status + error message; raise `GraphAPIError` on API failures
    - Read credentials from env vars or credentials file — never hardcoded
    - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5, 12.6, 12.7_

  - [ ]* 6.3 Write unit tests for converter
    - Test HTML conversion preserves headings, lists, tables, code blocks
    - Test .docx generation includes title, preserves structure
    - _Requirements: 4.2, 5.3_

  - [ ]* 6.4 Write unit tests for Graph API client
    - Test auth reads from env vars, falls back to credentials file
    - Test auth failure includes HTTP status code
    - Test retry logic for 429 (Retry-After header) and 503 (exponential backoff)
    - Mock MSAL and requests for all tests
    - _Requirements: 8.1, 8.2, 8.3, 12.6, 12.7_

- [x] 7. Checkpoint — Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [x] 8. Implement SyncEngine orchestrator
  - [x] 8.1 Implement `SyncEngine` core in `sync.py`
    - `__init__(config_path, config_overrides)` — load config, initialize all components (filters, parser, manifest, converter, graph client, conflict resolver)
    - `sync(mode, file_path, force, dry_run, json_output)` — main entry point returning `SyncReport`
    - `_discover_articles(file_path)` — dynamically walk all top-level subdirectories under articles_path (ignore hidden dirs and non-directory files at top level); or return single file if file_path provided
    - `_process_article(path, mode, force, dry_run)` — filter → hash-check → conflict-check → convert → upload pipeline for one article
    - `_handle_orphans(mode, eligible_paths)` — remove SP items for manifest entries with no corresponding eligible article
    - SHA-256 content hashing for incremental sync
    - Metadata-to-SharePoint field mapping (title, status, owner, updated, level, tags)
    - Navigation structure from dynamically discovered category folders + wiki-index parent/child relationships (Site Mode)
    - Folder creation before upload (Directory Mode)
    - Error handling: fail fast on ConfigError/AuthError; continue on per-article errors (FrontMatterError, GraphAPIError, ConversionError, conflicts)
    - Non-zero exit code when any article fails
    - _Requirements: 1.5, 2.4, 4.1, 4.3, 4.4, 4.5, 4.6, 5.1, 5.2, 5.4, 5.5, 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 7.3, 7.4, 7.5, 9.1, 9.2, 9.3, 9.4, 10.1, 10.2, 12.1, 12.5, 12.8, 13.1, 13.2, 13.3, 14.1, 14.2, 14.3_

  - [x] 8.2 Implement dry-run mode
    - When `--dry-run` is active, execute full discovery, filtering, hashing, and conflict-detection pipeline but skip all SharePoint write operations
    - Output same SyncReport with each action prefixed by "[DRY RUN]"
    - _Requirements: 12.2, 12.3_

  - [x] 8.3 Implement structured logging and metrics
    - JSON-formatted output when `--json` flag is provided
    - Include timestamps, article paths, actions, durations, and error details per article
    - Track per-sync metrics: total articles evaluated, articles per action category, total sync duration, average per-article processing time
    - _Requirements: 12.4, 12.5_

  - [ ]* 8.4 Write property test for hash-based sync decision tree (Property 5)
    - **Property 5: Hash-based sync decision tree**
    - Generate random manifest states and article states; verify: no entry → "created", hash match → "skipped", hash differs + no conflict → "updated"
    - **Validates: Requirements 6.2, 6.3, 6.4, 6.5**

  - [ ]* 8.5 Write property test for orphaned manifest cleanup (Property 6)
    - **Property 6: Orphaned manifest entries are removed**
    - Generate manifest entries where some file paths no longer correspond to eligible articles; verify those entries produce "removed" actions
    - **Validates: Requirements 1.5, 2.4, 6.6**

  - [ ]* 8.6 Write property test for error resilience (Property 9)
    - **Property 9: Error resilience — failures and conflicts do not halt processing**
    - Generate article sets where some encounter errors/conflicts; verify all articles are still processed and total actions == total articles evaluated
    - **Validates: Requirements 7.4, 9.3**

  - [ ]* 8.7 Write property test for sync report completeness (Property 10)
    - **Property 10: Sync report completeness**
    - Generate random sync runs; verify SyncReport contains all action categories and sum of counts == total articles + orphans evaluated
    - **Validates: Requirements 9.1, 9.2, 9.4**

  - [ ]* 8.8 Write property test for metadata-to-SharePoint mapping (Property 11)
    - **Property 11: Metadata-to-SharePoint field mapping preserves all required fields**
    - Generate random ArticleMetadata; verify output dict contains title, status, owner, updated, level
    - **Validates: Requirements 4.5, 5.4**

  - [ ]* 8.9 Write property test for single-file filtering (Property 13)
    - **Property 13: Single-file sync applies the same filters as full sync**
    - Generate random single articles; verify audience and status filters are applied; ineligible articles produce "skipped_filtered"
    - **Validates: Requirements 12.2, 12.3**

- [x] 9. Implement CLI entry point
  - [x] 9.1 Implement `cli.py`
    - Parse arguments: `--mode` (site/directory/both), `--file` (single article path), `--force`, `--dry-run`, `--json`, `--config` (config file path)
    - CLI arguments override config file values
    - Instantiate `SyncEngine` with config path and CLI overrides, call `sync()`
    - Print summary report (human-readable or JSON based on `--json` flag)
    - Exit code 0 on success, 1 on any failure
    - Support `--help` with usage information
    - _Requirements: 11.4, 14.4, 9.4, 12.2, 12.4_

  - [ ]* 9.2 Write unit tests for CLI
    - Test `--help` output
    - Test CLI argument parsing and override behavior
    - Test exit code 0 on success, 1 on failure
    - _Requirements: 14.4, 9.4_

- [x] 10. Checkpoint — Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [-] 11. Integration tests and final wiring
  - [ ]* 11.1 Write integration tests with mocked Graph API
    - Full sync flow: discover → filter → hash → convert → upload → manifest update
    - Site mode: article → HTML → site page creation with navigation
    - Directory mode: article → .docx → file upload with folder creation
    - Both mode: single article produces both site page and .docx
    - Conflict detection + force-overwrite flow
    - Orphan cleanup flow
    - Dry-run mode produces report without SP writes
    - Single-file sync with filtering
    - _Requirements: 4.1, 5.1, 10.2, 7.5, 6.6, 12.2, 14.2, 14.3_

  - [x] 11.2 Verify importability and pipeline integration
    - Verify `from sync import SyncEngine` works as expected
    - Verify `python3 ~/shared/tools/sharepoint-sync/sync.py --help` runs
    - Verify single-article sync via `SyncEngine.sync(file_path="...")` for librarian agent integration
    - _Requirements: 14.1, 14.2, 14.4_

- [x] 12. Final checkpoint — Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation
- Property tests validate universal correctness properties from the design document
- Unit tests validate specific examples and edge cases
- All code lives at `~/shared/tools/sharepoint-sync/` following the bridge.py pattern
- Testing uses Hypothesis (property-based) + pytest (unit) + mocked Graph API (integration)
