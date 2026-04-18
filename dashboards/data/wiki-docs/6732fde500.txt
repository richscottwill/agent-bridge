# Excel-in-SharePoint as Team Source of Truth

**Doc:** 09
**Audience:** Paid Acquisition teammates + their Kiro agents
**Status:** FINAL
**Last updated:** 2026-04-17

## Environment Awareness (for your agent)

This doc is heavily environment-dependent. Check capabilities before attempting anything:

| Capability | Remote IDE (DevSpaces) | Local IDE (laptop Kiro) | AgentSpaces (chat) |
|---|---|---|---|
| Download canonical .xlsx to disk | ✅ `/tmp/` or `~/shared/` | ✅ laptop filesystem | ⚠️ Session-only cache |
| Parse .xlsx with openpyxl / pandas | ✅ Preinstalled | ✅ If Python + libs installed | ❌ No shell |
| Open .xlsx in Excel app to inspect / edit | ❌ No GUI | ✅ User has Excel | ❌ |
| Append rows to canonical log sheets via Python + MCP | ✅ Full flow works | ✅ Full flow works | ❌ Can read, can't Python-modify |
| Run daily Adobe data watcher hook | ✅ Container stays up | ⚠️ Only when laptop awake | ❌ Hooks unavailable |
| Build derivative analysis files (timestamped) | ✅ | ✅ | ❌ Punt to Remote or Local IDE |

**Tell the user up front, in plain language:**
- **Remote IDE:** *"I can download your team's Excel files, read them, summarize what's in them, and add rows to tracker sheets. Full flow available."*
- **Local IDE:** *"I can do all of that here, or if you prefer, open the Excel file yourself and I'll read along and help you work through it."*
- **AgentSpaces:** *"I can read your team's Excel files and tell you what's in them, but I can't run numbers on them or update tracker sheets from here. For anything beyond summarizing, open Kiro on your laptop or your Remote IDE."*

---

Until we have a proper analytics backend (S3 + Athena, a knowledge base, or a shared DuckDB), the paid acq team's canonical data lives in **Excel files in SharePoint / OneDrive**. This doc establishes how your agent reads, updates, and contributes to that shared data layer without corrupting it.

## The pattern

Your team maintains a small set of canonical Excel files in a shared OneDrive folder. Every teammate's agent knows where they live and what sheets they contain. Agents can:

- **Read** canonical files freely to answer questions and build summaries.
- **Append** rows to structured "log" sheets within canonical files (team-owned data = write-to-ourselves-in-effect).
- **Build derivative files** (summaries, charts, briefs) in personal OneDrive without touching canonicals.

Agents CANNOT:

- **Overwrite** canonical files in place.
- **Delete** rows or sheets from canonical files.
- **Restructure** canonical files (rename sheets, change column order) without a human in the loop.

## Canonical file list (paid acq team)

Set by Richard. Agents reference these by name:

| File | Location | What it holds | Updated by |
|---|---|---|---|
| `ps-forecast-tracker.xlsx` | `Kiro-Drive/Dashboards/` | Weekly forecast vs actuals per market | Automated (refresh-forecast.py) |
| `ps-pacing-dashboard.xlsx` | `Kiro-Drive/Dashboards/` | MTD regs/spend vs OP2 per market | Automated (weekly WW dashboard ingest) |
| `ps-testing-dashboard.xlsx` | `Kiro-Drive/` | Test status across markets | Manual edits + agent-append |
| `command-center.xlsx` | `Kiro-Drive/` | Task/project overview | Automated |
| Adobe daily raw | `Kiro-Drive/raw-data/` | Per-day Adobe performance dumps | Vendor drop (or manual upload) |

**Each teammate should have their own version of this list in a personal steering file** — you may not care about the forecast tracker but need your own market's test tracker.

## Read workflow

Standard pattern for any canonical Excel read:

```
1. sharepoint_read_file(
     serverRelativeUrl="/personal/prichwil_amazon_com/Documents/Kiro-Drive/Dashboards/ps-forecast-tracker.xlsx",
     savePath="/tmp/ps-forecast-tracker.xlsx"
   )

2. Python:
   from openpyxl import load_workbook
   wb = load_workbook('/tmp/ps-forecast-tracker.xlsx', data_only=True)
   # data_only=True returns calculated values, not formulas

3. Parse specific sheet:
   sheet = wb['AU']
   for row in sheet.iter_rows(min_row=2, values_only=True):
       ...
```

Use `pandas.read_excel` for multi-sheet tabular analysis:

```python
import pandas as pd
xl = pd.ExcelFile('/tmp/ps-testing-dashboard.xlsx')
for sheet in xl.sheet_names:
    df = pd.read_excel(xl, sheet_name=sheet)
```

## Append workflow (the safe write pattern)

When a canonical file has a "log" sheet designed for appending (e.g., test results log, daily pacing log, ad-hoc reports index), agents can add rows:

```
1. sharepoint_read_file → /tmp/working.xlsx
2. Python append:
   from openpyxl import load_workbook
   wb = load_workbook('/tmp/working.xlsx')
   log = wb['ChangeLog']
   log.append(['2026-04-17', 'Richard', 'AU budget adjustment', 'details...'])
   wb.save('/tmp/working.xlsx')
3. sharepoint_write_file(
     libraryName='Documents',
     fileName='ps-testing-dashboard.xlsx',
     folderPath='Kiro-Drive',
     sourcePath='/tmp/working.xlsx'
   )
```

**Rules for append:**

- Only to sheets designated as append-only logs (named `*Log*`, `*History*`, `*Events*`, or documented as such).
- Never modify existing rows.
- Include a timestamp column and your alias in every row.
- If the sheet has a schema (column headers in row 1), your row MUST match the schema exactly.

## Edit-in-place workflow (requires user approval)

Sometimes you really do need to update a specific cell. This is NOT autoApproved — each edit gets manual confirmation.

```
1. sharepoint_read_file → /tmp/working.xlsx
2. Agent proposes edit:
   "I'm about to change B5 in sheet 'AU' from 'On Track' to 'At Risk'. OK?"
3. On user approval, Python modifies and saves.
4. sharepoint_write_file with same fileName → overwrites.
```

The agent always describes the edit in plain language before making it. User says yes, agent proceeds.

## Versioned derivative files (the preferred pattern)

When doing exploratory analysis or producing a deliverable, don't edit the canonical file — build a derivative in your personal OneDrive.

Naming convention:

```
<canonical-name>-<YYYY-MM-DD>-<slug>.xlsx
```

Example: `ps-forecast-tracker-2026-04-17-au-deepdive.xlsx`

Save to `Kiro-Drive/ad-hoc/` (or your personal workspace folder). Canonical stays untouched.

## Adobe daily raw data workflow

Common pattern: Adobe drops a raw performance Excel every morning. Your agent processes it.

```
1. Agent watches for new file in Kiro-Drive/raw-data/ (via hook — see kiro-hooks-cookbook.md)
2. sharepoint_read_file → /tmp/adobe-YYYY-MM-DD.xlsx
3. Python extracts key metrics (clicks, regs, spend, CPA per market/campaign)
4. Agent appends processed summary to ps-pacing-dashboard.xlsx 'DailySummary' sheet
5. Agent posts summary to your Slack self-DM
```

This is the canonical "append to team log" pattern. See Hooks Cookbook for the file-created hook that triggers it.

## Anti-patterns (don't do these)

- **Don't have your agent "clean up" a canonical file.** Even if the data looks messy, restructuring breaks downstream automation.
- **Don't write formulas into canonical files programmatically.** openpyxl handles formulas awkwardly. Pre-compute values in Python, write values.
- **Don't use `sharepoint_write_file` on canonicals without confirming the filename + folder.** One wrong path argument = silent new file in the wrong place.
- **Don't run bulk reads/writes in tight loops.** SharePoint has rate limits and OneDrive sync can lag.

## Failure modes

- **"File is locked for editing"** → someone has it open in Excel. Wait, or ask them to close it.
- **Agent writes to wrong folder** → Excel files don't have a "move" API on SharePoint MCP. You'll need to download, delete wrong copy, re-upload to right location. Avoid this by always specifying `folderPath` explicitly.
- **Formulas return #N/A after agent write** → openpyxl doesn't recalculate. Open the file in Excel once to trigger recalc, then the values are cached.
- **Data looks wrong** → You may be reading from a `data_only=False` workbook where cells contain formulas, not values. Load with `data_only=True`.

## When to upgrade beyond this pattern

This Excel-as-source-of-truth pattern works for 3–10 teammates and data that fits in single-Excel-file chunks. It breaks down when:

- You have >100 columns of time-series data → upgrade to DuckDB + Parquet.
- Multiple agents try to append simultaneously → you need proper locking or a real DB.
- Files grow above ~20MB → Excel gets slow, SharePoint sync lags.

When that happens, talk to Richard about moving to the shared DuckDB pattern.

## Steering file for data analysts

If you work with these Excel files daily, install this as your Kiro steering folder as `data-analysis.md` (in `.kiro/steering/` inside your workspace, or `~/.kiro/steering/` for user-level):

```markdown
---
inclusion: always
---

# Data Analysis Rules

Canonical team Excel files in OneDrive are read-only except for designated append-only log sheets. Never overwrite canonicals. Never restructure canonicals.

For analysis: download, parse with pandas/openpyxl, build derivative file with versioned name (<name>-YYYY-MM-DD-<slug>.xlsx) in personal OneDrive.

For log appends: only to sheets explicitly named *Log*, *History*, or *Events*. Match the schema exactly. Include timestamp and alias.

For in-place edits: describe the edit in plain language, wait for user confirmation, then apply.

Always use data_only=True when loading workbooks for calculated values.
```
