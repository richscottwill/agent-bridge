# Requirements Document

## Introduction

The Wiki-SharePoint Sync system pushes wiki articles from `~/shared/artifacts/` to a corporate SharePoint environment, supporting two upload modes (site-based and directory-based), incremental sync, audience filtering, and format conversion. It integrates with the existing wiki pipeline so that publishing an article can trigger a SharePoint push without manual intervention. This advances Level 3 (Team Automation) by making the wiki accessible to stakeholders who live in SharePoint, not in AgentSpaces.

## Glossary

- **Sync_Engine**: The core Python module that orchestrates article discovery, filtering, conversion, and upload to SharePoint. Analogous to `bridge.py` for Google Sheets/Docs.
- **Article**: A markdown file in `~/shared/artifacts/` with YAML front-matter metadata (title, status, audience, level, owner, created, updated, update-trigger, slug).
- **Front_Matter**: The YAML metadata block at the top of each Article, delimited by `---`.
- **Front_Matter_Parser**: The component that reads and parses YAML front-matter from Article files.
- **Front_Matter_Printer**: The component that serializes front-matter metadata back into YAML format.
- **Site_Mode**: Upload mode where Articles are published as SharePoint site pages with navigation, category structure, and cross-linking — producing a browsable SharePoint site.
- **Directory_Mode**: Upload mode where Articles are uploaded as files (.docx or .pdf) into a SharePoint document library, preserving the category folder structure.
- **Sync_Manifest**: A local JSON file tracking which Articles have been pushed, their last-synced timestamps, SharePoint item IDs, and content hashes — enabling incremental sync.
- **Graph_API_Client**: The component that authenticates and communicates with Microsoft Graph API to perform SharePoint operations.
- **Markdown_Converter**: The component that transforms markdown content into target formats (HTML for Site_Mode, .docx for Directory_Mode).
- **Wiki_Index**: The file at `~/shared/context/wiki/wiki-index.md` that catalogs all Articles with slugs, parent/child relationships, and dependency graphs.
- **Audience_Filter**: The component that evaluates Article front-matter to determine SharePoint eligibility based on audience field.
- **Status_Filter**: The component that evaluates Article front-matter to determine SharePoint eligibility based on status field.
- **SharePoint_Site**: The target SharePoint site where Articles are published in Site_Mode.
- **Document_Library**: The target SharePoint document library where Articles are uploaded in Directory_Mode.
- **Conflict_Resolver**: The component that detects and handles cases where an Article has been modified on both the local wiki and SharePoint since the last sync.

## Requirements

### Requirement 1: Audience Filtering

**User Story:** As a wiki owner, I want only amazon-internal articles pushed to corporate SharePoint, so that personal and agent-only content stays private.

#### Acceptance Criteria

1. WHEN an Article has audience set to "amazon-internal", THE Audience_Filter SHALL mark the Article as eligible for SharePoint sync.
2. WHEN an Article has audience set to "personal", THE Audience_Filter SHALL exclude the Article from SharePoint sync.
3. WHEN an Article has audience set to "agent-only", THE Audience_Filter SHALL exclude the Article from SharePoint sync.
4. IF an Article has no audience field in its Front_Matter, THEN THE Audience_Filter SHALL exclude the Article from SharePoint sync and log a warning identifying the file path.
5. WHEN a previously synced Article's audience changes from "amazon-internal" to "personal" or "agent-only", THE Sync_Engine SHALL remove the Article from SharePoint and update the Sync_Manifest.

### Requirement 2: Status Filtering

**User Story:** As a wiki owner, I want to control which article statuses are pushed to SharePoint, so that incomplete drafts don't reach stakeholders prematurely.

#### Acceptance Criteria

1. THE Sync_Engine SHALL accept a configurable list of eligible statuses (default: REVIEW, FINAL).
2. WHEN an Article's status is in the eligible statuses list, THE Status_Filter SHALL mark the Article as eligible for SharePoint sync.
3. WHEN an Article's status is not in the eligible statuses list, THE Status_Filter SHALL exclude the Article from SharePoint sync.
4. WHEN a previously synced Article's status changes to a non-eligible value, THE Sync_Engine SHALL remove the Article from SharePoint and update the Sync_Manifest.

### Requirement 3: Front-Matter Parsing and Round-Trip Integrity

**User Story:** As a developer, I want front-matter parsed reliably and preserved through round-trips, so that metadata is never corrupted during sync operations.

#### Acceptance Criteria

1. WHEN a valid Article file is provided, THE Front_Matter_Parser SHALL extract all YAML front-matter fields into a structured metadata object.
2. WHEN an Article file has malformed or missing YAML front-matter, THE Front_Matter_Parser SHALL return a descriptive error identifying the file path and the parsing failure.
3. THE Front_Matter_Printer SHALL serialize a metadata object back into valid YAML front-matter format.
4. FOR ALL valid metadata objects, parsing then printing then parsing SHALL produce an equivalent metadata object (round-trip property).

### Requirement 4: Site Mode Upload

**User Story:** As a wiki owner, I want to publish articles as a structured SharePoint site with navigation, so that stakeholders can browse content by category with cross-links.

#### Acceptance Criteria

1. WHEN Site_Mode is selected, THE Sync_Engine SHALL create or update a SharePoint site page for each eligible Article.
2. WHEN Site_Mode is selected, THE Markdown_Converter SHALL convert Article markdown content to SharePoint-compatible HTML.
3. WHEN Site_Mode is selected, THE Sync_Engine SHALL create a navigation structure in the SharePoint_Site that mirrors the dynamically discovered category folder structure from the articles path.
4. WHEN an Article has parent/child relationships defined in the Wiki_Index, THE Sync_Engine SHALL preserve those relationships as page hierarchy in the SharePoint_Site navigation.
5. WHEN Site_Mode is selected, THE Sync_Engine SHALL map Front_Matter fields (title, status, owner, updated, level, tags) to SharePoint page properties.
6. IF the SharePoint_Site does not exist, THEN THE Sync_Engine SHALL report an error with the site URL and required permissions rather than attempting to create the site.

### Requirement 5: Directory Mode Upload

**User Story:** As a wiki owner, I want to upload articles as .docx files into a SharePoint document library, so that stakeholders can download and edit them in familiar formats.

#### Acceptance Criteria

1. WHEN Directory_Mode is selected, THE Sync_Engine SHALL upload each eligible Article as a .docx file to the Document_Library.
2. WHEN Directory_Mode is selected, THE Sync_Engine SHALL create folders in the Document_Library matching the dynamically discovered category structure from the articles path.
3. WHEN Directory_Mode is selected, THE Markdown_Converter SHALL convert Article markdown content to .docx format preserving headings, lists, tables, and code blocks.
4. WHEN Directory_Mode is selected, THE Sync_Engine SHALL map Front_Matter fields to SharePoint document library column values (title, status, owner, updated, level).
5. IF a target folder does not exist in the Document_Library, THEN THE Sync_Engine SHALL create the folder before uploading the Article.

### Requirement 6: Incremental Sync

**User Story:** As a wiki owner, I want only changed articles pushed on subsequent syncs, so that the process is fast and avoids unnecessary SharePoint API calls.

#### Acceptance Criteria

1. THE Sync_Engine SHALL maintain a Sync_Manifest file that records each synced Article's file path, content hash (SHA-256), last-synced timestamp, and SharePoint item ID.
2. WHEN a sync is triggered, THE Sync_Engine SHALL compare each eligible Article's current content hash against the Sync_Manifest to identify changed Articles.
3. WHEN an Article's content hash matches the Sync_Manifest entry, THE Sync_Engine SHALL skip that Article.
4. WHEN an Article's content hash differs from the Sync_Manifest entry, THE Sync_Engine SHALL update the Article on SharePoint and update the Sync_Manifest.
5. WHEN an eligible Article has no entry in the Sync_Manifest, THE Sync_Engine SHALL create the Article on SharePoint and add an entry to the Sync_Manifest.
6. WHEN a Sync_Manifest entry has no corresponding eligible Article (deleted or filtered out), THE Sync_Engine SHALL remove the Article from SharePoint and remove the Sync_Manifest entry.

### Requirement 7: Conflict Detection

**User Story:** As a wiki owner, I want to know when someone has edited an article on SharePoint since my last sync, so that I don't accidentally overwrite their changes.

#### Acceptance Criteria

1. WHEN an Article exists in the Sync_Manifest and on SharePoint, THE Conflict_Resolver SHALL compare the SharePoint item's last-modified timestamp against the Sync_Manifest's last-synced timestamp before updating.
2. WHEN the SharePoint item has been modified after the last sync AND the local Article has also changed, THE Conflict_Resolver SHALL flag the Article as a conflict and skip the update.
3. WHEN a conflict is detected, THE Sync_Engine SHALL log the conflict with the Article file path, SharePoint item URL, local modified date, and SharePoint modified date.
4. WHEN a conflict is detected, THE Sync_Engine SHALL continue processing remaining Articles without stopping.
5. WHEN the user provides a force-overwrite flag, THE Sync_Engine SHALL overwrite SharePoint content for conflicted Articles and log each forced overwrite.

### Requirement 8: Authentication

**User Story:** As a developer, I want the sync tool to authenticate to SharePoint securely, so that credentials are managed safely and the tool can operate in the containerized DevSpaces environment.

#### Acceptance Criteria

1. THE Graph_API_Client SHALL authenticate to Microsoft Graph API using OAuth 2.0 client credentials flow (application permissions).
2. THE Graph_API_Client SHALL read client ID, client secret, and tenant ID from environment variables or a credentials file — not from hardcoded values.
3. IF authentication fails, THEN THE Graph_API_Client SHALL return a descriptive error including the HTTP status code and error message from the identity provider.
4. THE Graph_API_Client SHALL cache access tokens and refresh them before expiry to minimize authentication requests.
5. THE Graph_API_Client SHALL require the minimum Microsoft Graph API permissions needed: Sites.ReadWrite.All for Site_Mode, Files.ReadWrite.All for Directory_Mode.

### Requirement 9: Sync Execution and Reporting

**User Story:** As a wiki owner, I want a clear summary after each sync run, so that I know what was created, updated, skipped, conflicted, or removed.

#### Acceptance Criteria

1. WHEN a sync completes, THE Sync_Engine SHALL output a summary report listing counts of Articles created, updated, skipped (unchanged), skipped (filtered), conflicted, removed, and failed.
2. WHEN a sync completes, THE Sync_Engine SHALL output the list of individual Article actions (file path, action taken, SharePoint URL if applicable).
3. IF any Article fails during sync, THEN THE Sync_Engine SHALL log the error for that Article and continue processing remaining Articles.
4. THE Sync_Engine SHALL return a non-zero exit code when any Article fails during sync.

### Requirement 10: Dual Mode Support

**User Story:** As a wiki owner, I want to run site mode, directory mode, or both in a single sync invocation, so that I can maintain both SharePoint surfaces from one command.

#### Acceptance Criteria

1. THE Sync_Engine SHALL accept a mode parameter with values: "site", "directory", or "both".
2. WHEN mode is "both", THE Sync_Engine SHALL execute Site_Mode upload and Directory_Mode upload for each eligible Article in a single run.
3. THE Sync_Engine SHALL maintain separate Sync_Manifest entries for Site_Mode and Directory_Mode so that each mode tracks its own sync state independently.

### Requirement 11: Configuration

**User Story:** As a developer, I want sync settings centralized in a config file, so that SharePoint URLs, mode preferences, and filter settings are easy to change without modifying code.

#### Acceptance Criteria

1. THE Sync_Engine SHALL read configuration from a YAML file at a configurable path (default: `~/shared/tools/sharepoint-sync/config.yaml`).
2. THE Sync_Engine SHALL support the following configuration fields: SharePoint site URL, document library name, mode (site/directory/both), eligible statuses list, credentials file path, and sync manifest path.
3. IF the configuration file is missing or contains invalid YAML, THEN THE Sync_Engine SHALL return a descriptive error identifying the missing or malformed fields.
4. THE Sync_Engine SHALL allow command-line arguments to override configuration file values.

### Requirement 12: Quality Attributes

**User Story:** As a wiki owner, I want the sync tool to be fast, observable, and safe to test, so that I can trust it in production and diagnose issues quickly.

#### Acceptance Criteria

1. THE Sync_Engine SHALL complete a full sync of up to 50 articles in under 30 seconds, excluding network latency to SharePoint.
2. THE Sync_Engine SHALL support a `--dry-run` flag that executes the full discovery, filtering, hashing, and conflict-detection pipeline but skips all SharePoint write operations (create, update, delete).
3. WHEN `--dry-run` is active, THE Sync_Engine SHALL output the same SyncReport as a live run, with each action prefixed by "[DRY RUN]".
4. THE Sync_Engine SHALL log structured output (JSON-formatted when `--json` flag is provided) including timestamps, article paths, actions, durations, and error details for each article processed.
5. THE Sync_Engine SHALL track and report per-sync metrics: total articles evaluated, articles per action category, total sync duration, and average per-article processing time.
6. WHEN the Graph API returns HTTP 429 (rate limit), THE Sync_Engine SHALL wait for the duration specified in the Retry-After header and retry the request up to 3 times before marking the article as failed.
7. WHEN the Graph API returns HTTP 503 (service unavailable), THE Sync_Engine SHALL retry with exponential backoff (1s, 2s, 4s) up to 3 times before marking the article as failed.
8. THE Sync_Engine SHALL maintain a sync success rate target of ≥95% of eligible articles per run (measured as non-failed / total eligible).

### Requirement 13: Dynamic Folder Discovery

**User Story:** As a wiki owner, I want the sync tool to automatically discover new category folders, so that adding a new wiki category doesn't require code changes.

#### Acceptance Criteria

1. THE Sync_Engine SHALL dynamically discover all top-level subdirectories under the configured articles path rather than relying on a hardcoded list of category folders.
2. WHEN a new top-level subdirectory is created in the articles path, THE Sync_Engine SHALL include articles from that directory in the next sync without configuration changes.
3. THE Sync_Engine SHALL ignore hidden directories (prefixed with `.`) and non-directory files at the top level of the articles path.

### Requirement 14: Wiki Pipeline Integration

**User Story:** As a wiki owner, I want the sync to be triggerable from the wiki pipeline, so that publishing an article can automatically push it to SharePoint.

#### Acceptance Criteria

1. THE Sync_Engine SHALL expose a Python function that can be imported and called by other tools (e.g., the librarian agent step).
2. THE Sync_Engine SHALL support syncing a single Article by file path, in addition to syncing all eligible Articles.
3. WHEN invoked with a single Article path, THE Sync_Engine SHALL apply the same audience and status filters before syncing.
4. THE Sync_Engine SHALL be callable as a CLI command (`python3 ~/shared/tools/sharepoint-sync/sync.py`) for manual or hook-triggered execution.
