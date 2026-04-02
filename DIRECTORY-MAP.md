# Directory Map — ~/shared/

Single source of truth for where every file type belongs.

## Top-Level Directories

| Path | Purpose | Writes | Cadence |
|------|---------|--------|---------|
| context/ | Live context: organs, active state, meetings, wiki, archive | Agents, hooks | Daily |
| context/body/ | Body organs (11 files) | System refresh hook | Daily |
| context/active/ | Ground truth files only | Morning routine, agents | Daily |
| context/active/callouts/ | Per-market callout files | Callout pipeline | Weekly |
| context/archive/ | Archived files by category (context/, research/, tools/, misc/) | Agents | As needed |
| context/intake/ | System processing queue | Agents | As needed |
| context/meetings/ | Meeting notes by relationship type | Meeting sync hook | After meetings |
| context/tools/ | Production utility scripts | Manual | As needed |
| context/wiki/ | Wiki articles | Wiki pipeline | As needed |
| artifacts/ | Published work product | Agents, Richard | Weekly |
| artifacts/weekly-ships/ | L1: Weekly shipped artifacts | Richard | Weekly |
| artifacts/testing/ | L2: Test designs and results (active/, completed/, templates/) | Richard, agents | Per test |
| artifacts/frameworks/ | Reusable frameworks and methodologies | Richard | As needed |
| data/ | All data files for DuckDB | Ingestion pipeline | Daily-weekly |
| data/duckdb/ | DuckDB database files (.duckdb, .wal) | DuckDB, agents | On ingestion |
| data/raw/ | Unprocessed data awaiting ingestion | Upload flow | On upload |
| data/processed/ | Ingested data (timestamped) | Ingestion pipeline | On ingestion |
| data/exports/ | Query results and agent exports | Agents | On demand |
| data/markets/{code}/ | Per-market data (au, mx, us, ca, jp, uk, de, fr, it, es) | Agents | Weekly |
| data/testing/ | Test-specific data | Agents | Per test |
| tools/ | Automation tools and scripts | Richard, agents | As needed |
| tools/team/ | L3: Tools built for team adoption | Richard | As needed |
| tools/autonomous/ | L5: Autonomous workflow configs and logs | Agents | Future |
| tools/scratch/ | Debug/one-off scripts, safe to purge | Anyone | Ephemeral |
| uploads/ | Human drop zone | Richard | On upload |
| uploads/sheets/ | Data files (xlsx, csv) | Richard | On upload |
| uploads/changelogs/ | Change log exports | Richard | Weekly |
| uploads/docs/ | PDFs, markdown, misc documents | Richard | As needed |
| uploads/scratch/ | Ephemeral agent outputs | Agents | Ephemeral |
| research/ | Active research files | Richard, agents | As needed |
| research/aeo/ | L4: AEO/AI Overviews research | Future | Future |
| portable-body/ | Cold-start bootstrap kit | agent-bridge-sync | Weekly |
| audit-reports/ | System audit outputs | Agents | On audit |
| credentials/ | Auth files (PROTECTED — never move) | System | Never |
| .agentspaces/ | Auth sqlite (PROTECTED — never move) | System | Never |

## File Type → Location

| File Type | Drop Location | Final Location |
|-----------|--------------|----------------|
| CSV/XLSX data you download | uploads/sheets/ | data/raw/ → data/processed/ |
| Change logs | uploads/changelogs/ | data/raw/ → data/processed/ |
| Documents/PDFs | uploads/docs/ | uploads/docs/ or artifacts/ |
| Agent-generated analysis | data/exports/ | data/exports/ |
| DuckDB databases | — | data/duckdb/ |
| Test designs | — | artifacts/testing/active/ |
| Completed tests | — | artifacts/testing/completed/ |
| Weekly ship artifacts | — | artifacts/weekly-ships/ |
| Meeting notes | — | context/meetings/{type}/ |
| Wiki articles | — | context/wiki/ |
| Debug/temp scripts | — | tools/scratch/ |
| Production scripts | — | context/tools/ or tools/ |
| Team tools | — | tools/team/ |
