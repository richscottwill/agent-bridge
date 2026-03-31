# Uploads

Richard's drop zone for files that need processing. Drop files into the right subfolder — the system picks them up from here.

## Structure

- **sheets/** — Dashboards, xlsx, csv, data exports, raw report pulls
- **changelogs/** — Change log exports (csv, xlsx)
- **docs/** — PDFs, one-pagers, frameworks, markdown, misc documents
- **scratch/** — Agent-generated outputs, ad-hoc analysis, temp scripts. Clean regularly.
- **other/** — Anything that doesn't fit above

## How it works

1. Richard drops files into the appropriate subfolder
2. During morning routine or on-demand, the agent scans ~/shared/uploads/ for new files
3. Agent processes files (loads into DuckDB, updates organs, moves to intake for action items)
4. Processed files stay here as the source-of-truth archive

## Cleanup

- scratch/ is ephemeral — contents can be regenerated. Safe to purge weekly or on demand.
- sheets/, changelogs/, docs/ are source data — keep until explicitly archived.

## Relationship to intake/

- **uploads/** = where Richard puts things (human → system)
- **intake/** = where the system queues action items for processing (system → system)

Files here don't need to move to intake unless they generate a task or require organ updates.
