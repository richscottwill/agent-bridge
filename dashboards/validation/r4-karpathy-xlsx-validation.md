# R4 Validation: `karpathy-autoresearch-lab.xlsx` Removal Safety

**Date**: 2026-07-14
**Validator**: Kiro (spec task 1.4)
**Requirements**: 7.2, 7.3

## File Under Review

- **Path**: `~/shared/dashboards/karpathy-autoresearch-lab.xlsx`
- **Size**: 24,555 bytes (24 KB)
- **Created**: 2026-04-11 14:00
- **Last modified**: 2026-04-11 14:00 (never modified since creation)
- **SharePoint copy**: `Kiro-Drive/karpathy-autoresearch-lab.xlsx` — also created 2026-04-11, never modified

## Origin

Created on 2026-04-11 as part of a batch conversion of MotherDuck Dives to Excel workbooks. Per session-log.md:

> "Built 3 new Excel workbooks with charts: ps-testing-dashboard.xlsx (tests + summary by market/category), karpathy-autoresearch-lab.xlsx (experiment log with efficiency scores + priors + by-organ breakdown), command-center.xlsx (calendar + overdue tasks + actionable emails). Uploaded all 3 to OneDrive Kiro-Drive folder."

The xlsx is a **static snapshot** of data from DuckDB tables `karpathy.autoresearch_experiments` and `karpathy.autoresearch_priors`. It was generated once and never refreshed.

## Checks Performed

### 1. DuckDB `ops.data_freshness` — NO ENTRY

```sql
SELECT * FROM ops.data_freshness
WHERE source_name ILIKE '%karpathy%'
   OR source_name ILIKE '%autoresearch%'
   OR source_name ILIKE '%xlsx%'
   OR source_name ILIKE '%experiment%'
```

**Result**: 0 rows. The xlsx is not tracked as a data source by any workflow.

### 2. Hooks (`.kiro/hooks/`) — NO REFERENCES to the xlsx

Searched all 22 hook files for `karpathy-autoresearch-lab`, `autoresearch-lab`, and `autoresearch`:
- **No hook references the xlsx file.**
- Two hooks reference the `karpathy` agent by name (organ-change-detector, eod) but these reference the agent, not the xlsx.

### 3. Agent definitions — NO REFERENCES

Searched `~/shared/.kiro/agents/` for `karpathy-autoresearch-lab` and `autoresearch-lab`:
- **No agent definition references the xlsx file.**
- `karpathy.md` and `karpathy.json` define the karpathy agent but do not reference the xlsx.

### 4. Python/shell scripts — NO BUILD SCRIPT EXISTS

- No `build-karpathy*.py`, `refresh-karpathy*.py`, or `generate-karpathy*.py` script exists.
- `refresh-body-system.py` queries DuckDB `karpathy.autoresearch_experiments` and `karpathy.autoresearch_organ_health` tables directly — it does NOT read or write the xlsx.
- `karpathy-loop.sh` queries DuckDB `autoresearch_experiments` and `autoresearch_priors` tables directly — it does NOT reference the xlsx.
- `generate.py` (progress charts) references `autoresearch.html` (an HTML page) — not the xlsx.

### 5. Context files — NO REFERENCES

Searched `~/shared/context/` for `karpathy-autoresearch-lab`:
- Only reference is in `session-log.md` documenting its creation.
- No active context file, intake file, or state file references it.

### 6. SharePoint — STATIC COPY EXISTS

The file exists at `Kiro-Drive/karpathy-autoresearch-lab.xlsx`:
- Created: 2026-04-11
- Modified: 2026-04-11 (never updated)
- Same 24,555 bytes as local copy

### 7. Live data availability check

The data this xlsx snapshots is **actively available** in DuckDB:
- `karpathy.autoresearch_experiments` — live experiment log
- `karpathy.autoresearch_priors` — live priors
- `karpathy.autoresearch_organ_health` — live organ health
- `main.autoresearch_experiments` — duplicate in main schema
- `main.autoresearch_priors` — duplicate in main schema

The `refresh-body-system.py` script queries these tables directly to build the Body System dashboard's Autoresearch page (`autoresearch.html`). The xlsx is a redundant static snapshot of data that is already consumed live.

## Verdict: SAFE TO REMOVE

**Classification**: Unused / redundant static snapshot

**Reasoning**:
1. No script generates or refreshes it — it was a one-time export
2. No hook, agent, or workflow reads it
3. Not tracked in `ops.data_freshness`
4. Never modified since creation (2+ months stale)
5. The underlying data is actively consumed via DuckDB by `refresh-body-system.py` and `karpathy-loop.sh`
6. The HTML autoresearch dashboard (`autoresearch.html`) renders the same data live

**Risk if removed**: None identified. The data it contains is a subset of what's already in DuckDB and rendered in the Body System dashboard.

**SharePoint cleanup**: The SharePoint copy at `Kiro-Drive/karpathy-autoresearch-lab.xlsx` should also be removed to avoid confusion about which files are active dashboards.

**Note**: If Richard wants an Excel view of autoresearch data in the future, a proper build script (like `build-forecast-tracker.py`) should be created that generates it from live DuckDB data on demand — not a static snapshot.
