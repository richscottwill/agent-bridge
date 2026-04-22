# R2 Validation — `build-forecast-tracker.py.legacy` Removal Safety

**Date**: 2026-07-14
**Validator**: Kiro (spec task 1.2)
**Requirements**: 7.2 (Subtraction before addition), 7.3 (verification step before removal)
**Verdict**: ✅ **SAFE TO REMOVE — superseded, no active consumers**

---

## File Under Review

- **Path**: `~/shared/dashboards/build-forecast-tracker.py.legacy`
- **Purpose**: Original Excel forecast tracker builder (v3). Connected to MotherDuck, built `ps-forecast-tracker.xlsx` from scratch each run.
- **Superseded by**: Two scripts now handle this work:
  - `update-forecast-tracker.py` — writes to hidden `_Data` sheet in xlsx, preserving all visible sheet formatting (template-based updater)
  - `refresh-forecast.py` — reads xlsx and produces `forecast-data.json` for the dashboard

## Checks Performed

### 1. `refresh-forecast.py` — `.legacy` references
- **Method**: Grep for `.legacy` across all 846 lines
- **Result**: **Zero matches.** `refresh-forecast.py` reads `ps-forecast-tracker.xlsx` only (via `XLSX_PATH` and `FALLBACK_PATH` constants). No reference to any `.legacy` file.

### 2. All Python files in `~/shared/` — `build-forecast-tracker` references
- **Method**: Grep all `*.py` files under `shared/` for `build-forecast-tracker`
- **Result**: **Zero matches in active code.** No Python script imports, calls, or references `build-forecast-tracker` in any form.

### 3. Hooks — `build-forecast-tracker` or `.legacy` references
- **Method**: Grep all 22 hook files in `.kiro/hooks/` for `build-forecast-tracker` or `legacy`
- **Result**: **Zero matches.** The relevant hook (`forecast-sharepoint-push`) watches `ps-forecast-tracker.xlsx` edits only — it does not invoke or reference the legacy builder.

### 4. Crontab — scheduled task references
- **Method**: `crontab -l` output inspection
- **Result**: **No reference.** Crontab contains only system entries (`patch-global-info.sh`, `mwinit --refresh-aea`, `invoke_status.sh`). No forecast-related cron jobs.

### 5. Pipeline integration — `refresh-all.py`
- **Method**: Checked `refresh-all.py` (the orchestrator script that runs the full data pipeline)
- **Result**: Pipeline steps are: `extract-ly-data.py` → `update-forecast-tracker.py` → `refresh-forecast.py` → `refresh-callouts.py`. **The legacy builder is not in the pipeline.**

### 6. Documentation references
- **Method**: Checked `device.md` (system component registry)
- **Result**: `device.md` explicitly documents: *"Legacy: `build-forecast-tracker.py.legacy` — replaced by template-based updater."* This confirms the file was intentionally superseded and marked as legacy.

## Historical Context

From `session-log.md` entries (2026-04-11):
- `build-forecast-tracker.py` was originally built as a from-scratch Excel builder (~250 lines, then rewritten as v2 with W1-W52 scaffold)
- It was later superseded by `update-forecast-tracker.py` which uses a template-based approach (writes only to hidden `_Data` sheet, preserving visible sheet formatting)
- The file was renamed with `.legacy` suffix to mark it as replaced

## Conclusion

| Check | Result |
|-------|--------|
| `refresh-forecast.py` references `.legacy` | ❌ None |
| Python files reference `build-forecast-tracker` | ❌ None |
| Hooks reference file | ❌ None |
| Cron references file | ❌ None |
| Pipeline (`refresh-all.py`) includes file | ❌ None |
| `device.md` documents as replaced | ✅ Yes — "replaced by template-based updater" |

**`build-forecast-tracker.py.legacy` has zero active consumers.** It was superseded by `update-forecast-tracker.py` and is safe to delete in Phase 3 (task 6.2).

**Note**: The file contains a hardcoded MotherDuck token in its source. Removing it also eliminates a stale credential from the filesystem — a minor security hygiene win.
