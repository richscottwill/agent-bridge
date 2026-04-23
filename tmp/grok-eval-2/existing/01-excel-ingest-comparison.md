# Excel Ingest — Existing Path vs Grok's Proposal

**Scope:** Comparing Grok's proposed `shared/tmp/grok-eval-2/proposed/01-excel_ingest.py` against what Richard's system actually does today when an xlsx lands in `shared/uploads/`.

**Verdict:** Existing path is materially more capable than Grok's proposal for the WW Dashboard use case. For the `CCP Q1'26 check yc.xlsx` specifically, NEITHER handles it today — but Grok's script would fail on first contact. Rejection justified. The real gap is narrower and different than Grok's proposal addresses.

---

## 1. The Existing Path (what happens today)

### The drop zone convention
`shared/uploads/README.md` documents three subfolders:
- `sheets/` — xlsx, csv, data exports (this is where the CCP file lives)
- `changelogs/` — change log exports
- `docs/` — PDFs, markdown, misc

Grok's script watches `shared/uploads/` root, flat. Richard's documented convention is subfolders. Mismatch from the start.

### Trigger: `wbr-pipeline-trigger.kiro.hook`
- Event: `fileCreated` on `shared/uploads/sheets/*Dashboard*.xlsx`
- **Filename pattern matters:** only files matching `*Dashboard*` fire the hook. Arbitrary xlsx drops (like `CCP Q1'26 check yc.xlsx`) do NOT auto-trigger anything.
- Handler: agent reads the xlsx, runs the pipeline, updates the prediction ledger.

### The pipeline: `shared/tools/wbr-pipeline.sh`
9 steps, orchestrated in bash:
1. `dashboard-ingester/ingest.py <xlsx>` — parse all 10 markets, all KPIs
2. Sync weekly/daily/ie%CCP to `ps.performance` on MotherDuck
3. Scan `ps.change_log` for regime changes, insert into `ps.regime_changes`
4. Score last week's predictions against actuals (prediction ledger feedback)
5. Bayesian projector generates next-week/month/quarter/year-end predictions
6. Populate `ps.forecast_tracker` (weighted predictions via λ=0.2 exponential decay + actuals backfill)
7. Update `ps-forecast-tracker.xlsx` template (writes ONLY to hidden `_Data` sheet, preserves visible formatting)
8. Regenerate `market-constraints.md` from `ps.market_constraints` view
9. Prepare state-file constraint sync payload for SharePoint push

### The ingester: `shared/tools/dashboard-ingester/ingest.py` (2,355 lines)
Not a flat `pd.read_excel()`. This is a purpose-built parser for the WW Dashboard's specific multi-tab structure:

**Schema awareness:**
- Per-market daily tabs (`AU`, `MX`, `US`, …, 10 markets) with 17 columns split into Total / Brand / NB blocks + spacers
- `Weekly` tab with 8 metric blocks stacked vertically (spend, regs, cpa, clicks, impressions, cpc, cvr, ctr) × 10 markets × 3 segments (total/brand/NB)
- `2026 Monthly` tab with OP2 vs actuals sections
- `IECCP` tab with 5 stacked sections — historical bug where scanner hit CPA rows instead of IECCP rows, producing 6559% ie%CCP (fix lives in the code, documented at line ~330)

**Auto-detection (not hardcoded):**
- `_detect_daily_cols()` reads the header row and maps keywords → column indices
- `_detect_weekly_blocks()` scans column A for 'US SEM' markers to find block starts dynamically
- `_find_monthly_sheet()` glob-matches `2026 Monthly*` because the tab name drifts (`2026 Monthly Q2 update`)
- `_detect_latest_week()` walks backwards to find the latest week with a full 7 days of data

**DuckDB writes (idempotent, INSERT OR REPLACE):**
- `daily_metrics` / `weekly_metrics` / `monthly_metrics` / `ieccp` / `projections` / `anomalies` / `ps.targets` / `ingest_log`
- Anomaly detection: flags metrics >20% off 8-week baseline, deletes prior anomalies for idempotent re-runs
- Parquet export + schema export after every write
- Writes `last_ingest.json` as a data event for downstream agents to poll

**Outputs:**
- Per-market callout drafts: `shared/context/active/callouts/<market>/<market>-2026-wNN.md`
- Per-market data briefs for analyst agents
- WW summary with biggest movers, anomalies, vs-OP2 table
- JSON extract: `shared/tools/dashboard-ingester/data/<week>.json`

### Downstream chain
- `forecast-sharepoint-push` hook (fileEdited on `ps-forecast-tracker.xlsx`) → pushes to both SharePoint locations
- `harmony-forecast-deploy` hook (same trigger) → rebuilds `forecast-data.json`, deploys Harmony app to beta
- Prediction ledger append: `~/shared/wiki/callouts/prediction-ledger.md` gets the new week's predictions, prior week gets scored (HIT/MISS/SURPRISE)

### DuckDB staging surface
Only one relevant table by name: `ps.dashboard_uploads` (tracks what's been ingested). The schema `ps` holds 63 tables/views — none named just `ps` and none named `tests`. All inserts are into named, typed tables with specific columns.

---

## 2. Grok's Proposed Script — Bugs & Limitations

### Bug 1: `~` does not expand in Python's `glob` or `duckdb.connect`

```python
DB_PATH = "~/shared/data/duckdb/ps-analytics.duckdb"
UPLOADS_DIR = "~/shared/uploads/"
files = glob.glob(f"{UPLOADS_DIR}*.xlsx")
```

Verified by execution in this environment:
```
glob.glob('~/shared/uploads/*.xlsx') → []
glob.glob(os.path.expanduser('~/shared/uploads/*.xlsx')) → []  (only subfolders match)
```

Two compounding problems:
- `~` is shell syntax, not a filesystem path. Python's `glob` treats it literally. `files` is always `[]`. Script exits with "No new files found." Full stop.
- Even with `os.path.expanduser`, the path points to `~/shared/uploads/` root — but Richard's files live in `shared/uploads/sheets/`. No recursive glob. Would still miss everything.
- `duckdb.connect("~/shared/data/duckdb/ps-analytics.duckdb")` creates a NEW empty database file at a literal `~` directory, not the real one. Opens in local MotherDuck mode, not cloud. Completely disconnected from `md:ps_analytics`.

### Bug 2: The target tables don't exist

```python
table = "tests" if 'test_id' in df.columns or 'lift' in df.columns else "ps"
conn.execute(f"INSERT INTO {table} SELECT * FROM df")
```

- `ps` is a schema name on MotherDuck, not a table. `INSERT INTO ps` fails with "table does not exist."
- No `tests` table exists in `ps_analytics` (verified via `information_schema.tables`).
- Even if they existed, `INSERT INTO <table> SELECT *` requires the DataFrame columns to match the table's column count and types exactly. `ps.performance` has 28 typed columns (market, period_type, period_key, registrations INT, cost DOUBLE, …). A blind `SELECT *` from an arbitrary xlsx DataFrame cannot satisfy this.

### Bug 3: `pd.read_excel(file)` reads the first sheet only

The CCP Q1'26 check xlsx has three sheets:
- `Summary` (35×22, Q1-24 through Q1-26 CCP benchmarks)
- `Sheet1` (67×13, WW SSR totals)
- `Sheet2` (19×2, 2026 W1 CCP by market-segment — this is the actual Q1 check data)

`pd.read_excel(file)` with no `sheet_name` returns only the first sheet (`Summary`). `Sheet1` and `Sheet2` are silently dropped. The table routing heuristic (`'test_id' in df.columns or 'lift' in df.columns`) matches neither. Everything goes to nonexistent `ps` table. Silent data loss before the insert even fails.

### Bug 4: Type safety is absent

`df.columns = [c.strip().lower().replace(' ', '_') for c in df.columns]` — fine for column names, useless against:
- Excel dates coming in as `datetime.datetime` or floats depending on cell format
- Mixed-type columns (strings in numeric columns break the insert)
- `None` values where DuckDB expects NOT NULL
- Column `ingested_at = datetime.now()` — creates a timestamp column. `ps.performance` has no such column. Schema mismatch.

The real ingester has `safe_float`, `safe_int`, explicit column mappings, and per-row try/except. Grok's version has one outer try/except that catches-and-moves-on, so errors are invisible.

### Bug 5: Moves the file before verifying success

```python
conn.execute(f"INSERT INTO {table} SELECT * FROM df")  # will fail
...
os.rename(file, f"{ARCHIVE_DIR}{os.path.basename(file)}")  # runs anyway
```

The `os.rename` is outside the error path for the INSERT. Actually, it IS inside the try, so a failed INSERT raises and skips the rename. But then the file stays in uploads with no indication of failure — next run re-attempts and re-fails. No idempotency check, no retry logic, no "already processed" marker.

### Bug 6: No schema detection, no market awareness, no period derivation

The existing ingester auto-detects:
- Which tab is which market
- Where the metric blocks start on the Weekly tab
- The latest complete week
- Column layouts per tab

Grok's script assumes one flat DataFrame per file. This works for exports that look like CSVs. It fails the moment the xlsx has any structure — which is every real PS artifact.

### Bug 7: Routing heuristic is bogus

```python
table = "tests" if 'test_id' in df.columns or 'lift' in df.columns else "ps"
```

"Is this a test file or not?" Two columns decide. The CCP xlsx has neither, so it goes to `ps`. The WW Dashboard xlsx doesn't have `test_id` either — it also goes to `ps`. A test export using different column names (e.g., `experiment_id`, `delta`) goes to `ps`. The routing has no signal.

---

## 3. Head-to-Head on `CCP Q1'26 check yc.xlsx`

| Dimension | Existing path | Grok's script |
|---|---|---|
| Discovers the file | ❌ No — `wbr-pipeline-trigger` only matches `*Dashboard*.xlsx` | ❌ No — `~` in glob returns `[]` |
| Reads all sheets | n/a (ingester is Dashboard-specific) | ❌ Only first sheet (`Summary`), drops `Sheet1` and `Sheet2` |
| Parses CCP benchmarks structure | ❌ No parser for this shape | ❌ Flat DataFrame ignores the Q-over-Q stacked layout |
| Writes to DuckDB | n/a | ❌ `INSERT INTO ps` — `ps` is a schema, not a table |
| Archives on success | ❌ (never runs) | ❌ Never reaches archive because insert throws |

**Neither runs successfully today.** But the existing path fails cleanly (no trigger fires, file sits in `sheets/` until Richard asks the agent to look at it). Grok's script fails loudly on first call with the `~` bug, or silently drops data if you fix that one bug.

If Richard wants the CCP file ingested, the real workflow today is: ask the agent, agent reads the file with `openpyxl`, interprets the Q1'26 checkpoint data, and writes the relevant rows to `ps.targets` or a purpose-built table. That's a human-in-the-loop read, not an autonomous ingester — which is correct for a one-off Q1 audit artifact.

---

## 4. Verdict

**Rejection justified. Keep the existing path.**

Grok's script is a naive "watch a folder, INSERT INTO SELECT *" pattern that ignores:
1. The documented subfolder structure (`sheets/`, `changelogs/`, `docs/`)
2. The trigger pattern (`*Dashboard*.xlsx`) that scopes automation to known artifact types
3. The cloud-first database layout (`md:ps_analytics`, schema-qualified tables, typed columns)
4. The multi-tab structure of every real PS xlsx (Dashboard, forecast tracker, CCP audit)
5. Existing schema mappings (`_detect_daily_cols`, `_detect_weekly_blocks`, `_detect_monthly_metric_blocks`)
6. Idempotency (`INSERT OR REPLACE`, `DELETE WHERE ... AND week = ?`, `last_ingest.json`)

Adopting it would be a strict regression: replace ~2,400 lines of schema-aware code with 35 lines that can't even find files in the right directory.

### The actual gap (if any)

There is one real observation worth naming — not a reason to adopt Grok's script, but a legitimate question about coverage:

**The existing auto-trigger only fires on `*Dashboard*.xlsx`.** Every other xlsx that lands in `shared/uploads/sheets/` — CCP checks, CVR analyses, ref-tag pulls, keyword reports — has no autonomous processing path. Richard has to explicitly ask the agent to read them.

That's not necessarily a bug. Per `soul.md` principle #3 ("Subtraction before addition") and principle #8 ("device.md check — recurring friction with 3+ instances/week is a tool, one-offs are investigations"):
- The CCP Q1'26 file is a one-off audit artifact. It doesn't justify a general ingester.
- The other files in `sheets/` today are mostly one-offs (keyword reports Richard pulled for analysis, ref-tag exports Yun shared).
- Richard already has the forecast tracker, dashboard xlsx, and callout pipeline — the recurring flows are automated.

A general "any xlsx → DuckDB" tool would be low-leverage: it would ingest data that has no downstream consumer, into tables that don't exist, with schema Richard has to manually map anyway.

### If coverage were a real gap, the right design would be

Not Grok's script. Something like:
- A manifest file in `shared/uploads/sheets/<stem>.yaml` declaring `target_table`, `sheet_name`, `column_map`, `period_key_derivation` per xlsx
- Trigger on presence of both xlsx AND manifest
- Reuse `safe_float`/`safe_int`/`INSERT OR REPLACE` patterns from `dashboard-ingester/ingest.py`
- Schema-qualified writes to MotherDuck, not a local file
- Archive only after verified row count matches

But the leverage case for building that today is weak. Richard's time is better spent on Testing Approach v5 (the hard thing, L1 streak at zero) than on automating one-off file ingests.

---

## Five Levels check
Building this tool would be L3 (Team Automation). Grok's version fails the device.md test ("Would teammates adopt it?") — it can't find files and doesn't write to real tables. Rejection aligns with principle #3 (subtraction) and principle #8 (device.md check).
