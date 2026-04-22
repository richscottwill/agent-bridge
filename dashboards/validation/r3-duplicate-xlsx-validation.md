# R3 Validation — Duplicate Forecast `.xlsx` Files Removal Safety

**Date**: 2026-07-14
**Validator**: Kiro (spec task 1.3)
**Requirements**: 7.2 (Subtraction before addition), 7.3 (verification step before removal)
**Verdict**: ✅ **`richard-forecast-tracker.xlsx` and `sp-forecast-tracker-check.xlsx` are SAFE TO REMOVE — zero active consumers. `ps-forecast-tracker.xlsx` is the sole source of truth.**

---

## Files Under Review

| File | Size | Last Modified | Location |
|------|------|---------------|----------|
| `ps-forecast-tracker.xlsx` | 1,198,269 bytes | 2026-04-21 15:04 | `~/shared/dashboards/` |
| `richard-forecast-tracker.xlsx` | 172,200 bytes | 2026-04-13 21:11 | `~/shared/dashboards/` |
| `sp-forecast-tracker-check.xlsx` | 124,413 bytes | 2026-04-13 21:04 | `~/shared/dashboards/` |

**Observation**: `ps-forecast-tracker.xlsx` is ~7x larger than `richard-forecast-tracker.xlsx` and ~10x larger than `sp-forecast-tracker-check.xlsx`. It was last modified 8 days after the other two, indicating it's the actively maintained file. The other two haven't been touched since April 13.

---

## Source of Truth: `ps-forecast-tracker.xlsx`

### Active consumers (3 scripts + 1 hook)

**1. `refresh-forecast.py`** — reads `ps-forecast-tracker.xlsx` → produces `forecast-data.json` for the dashboard
- Line 22: `XLSX_PATH = os.path.join(SCRIPT_DIR, "ps-forecast-tracker.xlsx")`
- Line 26: `FALLBACK_PATH = "/tmp/ps-forecast-tracker.xlsx"`
- Reads `_Data`, `_Daily_Data`, and `_LY_Data` sheets
- Also enriches with `ps.forecasts` from DuckDB (MotherDuck)
- **No reference to `richard-forecast-tracker` or `sp-forecast-tracker-check` anywhere in 846 lines**

**2. `update-forecast-tracker.py`** — writes DuckDB data into `ps-forecast-tracker.xlsx` hidden `_Data` sheet
- Line 13: `XLSX = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ps-forecast-tracker.xlsx')`
- Writes weekly, monthly, quarterly, year-end predictions + actuals + OP2 targets
- Also writes `_Constraints` hidden sheet from `ps.market_constraints` view
- **No reference to `richard-forecast-tracker` or `sp-forecast-tracker-check`**

**3. `extract-ly-data.py`** — extracts daily data from WW Dashboard Excel → writes `_Daily_Data` sheet into `ps-forecast-tracker.xlsx`
- Line 18: `FORECAST_XLSX = SCRIPT_DIR / "ps-forecast-tracker.xlsx"`
- **No reference to `richard-forecast-tracker` or `sp-forecast-tracker-check`**

**4. `forecast-sharepoint-push` hook** (`.kiro/hooks/forecast-sharepoint-push.kiro.hook`)
- Watches: `shared/dashboards/ps-forecast-tracker.xlsx`
- Action: pushes to SharePoint `Kiro-Drive/ps-forecast-tracker.xlsx` and `Dashboards/ps-forecast-tracker.xlsx`
- **No reference to `richard-forecast-tracker` or `sp-forecast-tracker-check`**

### Pipeline integration (`refresh-all.py`)
The full data pipeline is: `extract-ly-data.py` → `update-forecast-tracker.py` → `refresh-forecast.py` → `refresh-callouts.py`. All steps operate exclusively on `ps-forecast-tracker.xlsx`.

---

## Duplicate #1: `richard-forecast-tracker.xlsx`

### Checks performed

| Check | Method | Result |
|-------|--------|--------|
| `refresh-forecast.py` references | Grep all 846 lines for `richard` | ❌ Zero matches |
| `update-forecast-tracker.py` references | Grep all lines for `richard` | ❌ Zero matches |
| `extract-ly-data.py` references | Grep for `richard` | ❌ Zero matches |
| All Python files in `~/shared/` | Grep `**/*.py` for `richard-forecast-tracker` | ❌ Zero matches (only spec/design docs mention it) |
| All hooks in `.kiro/hooks/` | Grep for `richard-forecast` | ❌ Zero matches |
| DuckDB `ops.data_freshness` | Query for any entry referencing `richard` or `forecast` xlsx | ❌ No entry exists |
| SharePoint | Search for `richard-forecast-tracker` | ❌ Not found on SharePoint |

**Assessment**: This appears to be an earlier personal copy of the forecast tracker, predating the standardized `ps-forecast-tracker.xlsx`. The `richard-` prefix suggests it was Richard's original working file before the pipeline was formalized. At 172KB vs 1.2MB, it contains significantly less data (likely missing the `_Data`, `_Daily_Data`, and `_Constraints` hidden sheets that the current pipeline depends on).

**Verdict**: ✅ Safe to remove. Zero consumers in code, hooks, DuckDB, or SharePoint.

---

## Duplicate #2: `sp-forecast-tracker-check.xlsx`

### Checks performed

| Check | Method | Result |
|-------|--------|--------|
| `refresh-forecast.py` references | Grep all 846 lines for `sp-forecast-tracker-check` | ❌ Zero matches |
| `update-forecast-tracker.py` references | Grep for `sp-forecast-tracker-check` | ❌ Zero matches |
| `extract-ly-data.py` references | Grep for `sp-forecast-tracker-check` | ❌ Zero matches |
| All Python files in `~/shared/` | Grep `**/*.py` for `sp-forecast-tracker-check` | ❌ Zero matches (only spec/design docs mention it) |
| All hooks in `.kiro/hooks/` | Grep for `sp-forecast-tracker-check` | ❌ Zero matches |
| DuckDB `ops.data_freshness` | Query for any entry referencing this file | ❌ No entry exists |
| SharePoint | Search for `sp-forecast-tracker-check` | ❌ Not found on SharePoint |

**Assessment**: The `sp-` prefix (SharePoint) and `-check` suffix strongly suggest this was a one-time validation artifact — likely created to verify that the SharePoint-synced version matched the local version, or to check data integrity during a migration. At 124KB (smallest of the three), it contains the least data. Last modified April 13, same day as `richard-forecast-tracker.xlsx`, suggesting both were created/used during the same session and then abandoned.

**Verdict**: ✅ Safe to remove. Zero consumers in code, hooks, DuckDB, or SharePoint.

---

## DuckDB `ops.data_freshness` — Forecast File Entries

Queried all 19 entries in `ops.data_freshness`. **None reference any forecast xlsx file.** The table tracks DuckDB tables and context files only — xlsx files are not registered as data sources in the freshness monitoring system.

This means:
- There is no automated staleness check on any forecast xlsx
- No downstream workflow is triggered by xlsx freshness
- The xlsx files are consumed only by the Python scripts listed above, not by any DuckDB-driven workflow

---

## Summary

| File | Status | Consumers | Verdict |
|------|--------|-----------|---------|
| `ps-forecast-tracker.xlsx` | **SOURCE OF TRUTH** | 3 scripts, 1 hook, 2 SharePoint locations | Keep — actively consumed by entire forecast pipeline |
| `richard-forecast-tracker.xlsx` | **DUPLICATE** | Zero | ✅ Safe to remove |
| `sp-forecast-tracker-check.xlsx` | **ONE-TIME ARTIFACT** | Zero | ✅ Safe to remove |

### Removal plan for Phase 3 (task 6.3)
1. Delete `~/shared/dashboards/richard-forecast-tracker.xlsx`
2. Delete `~/shared/dashboards/sp-forecast-tracker-check.xlsx`
3. Verify `refresh-forecast.py` still runs correctly (it will — it never referenced these files)
4. No reference updates needed — no code, hook, or config points to either file

### Risk assessment
**Risk**: None. Both files have zero consumers across:
- All Python scripts in `~/shared/`
- All hooks in `.kiro/hooks/`
- DuckDB `ops.data_freshness`
- SharePoint (neither file exists there)
- The `refresh-all.py` pipeline

**Soul principle**: Subtraction before addition — removing two unused files that create "which forecast file is current?" confusion. The answer is unambiguous: `ps-forecast-tracker.xlsx` is the only file that matters.
