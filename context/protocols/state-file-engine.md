# State File Engine — Generic Protocol

Governs the generation, patching, and delivery of all daily state files. Market-specific parameters are loaded from per-market protocol files. The engine is market-agnostic; the protocols are market-specific.

---

## Registered State Files

| Market | Protocol File | Local Path | SharePoint Path | Status |
|---|---|---|---|---|
| MX | `state-file-mx-ps.md` | `~/shared/wiki/state-files/mx-paid-search-state.md` | `Kiro-Drive/state-files/mx-paid-search-state.{md,docx}` | ACTIVE |
| AU | `state-file-au-ps.md` | `~/shared/wiki/state-files/au-paid-search-state.md` | `Kiro-Drive/state-files/au-paid-search-state.{md,docx}` | ACTIVE |
| WW Testing | `state-file-ww-testing.md` | `~/shared/wiki/state-files/ww-testing-state.md` | `Kiro-Drive/state-files/ww-testing-state.{md,docx}` | ACTIVE |

---

## Three-Layer Architecture

### Weekly Hook Order

| Day | Hook sequence | What runs |
|---|---|---|
| Mon | AM-Backend Step 2E (Layer 1) → WBR Callouts Step (Layer 1.5) → EOD-Refresh Step 9 (Layer 2) | Full daily refresh, then WBR patch, then priority patch |
| Tue–Fri | AM-Backend Step 2E (Layer 1) → EOD-Refresh Step 9 (Layer 2) | Daily refresh + priority patch only |
| Sat–Sun | none | Files unchanged |

WBR Callouts runs Monday only. AM-Backend Tue–Fri must preserve the WBR-OWNED content written on Monday — it persists for the full week.

### Layer 1: AM-Backend Step 2E — Content Generation (daily)

Runs after Phase 1 ingestion completes and Phase 2A-2D processing finishes. All data sources are fresh.

For each registered state file where status = ACTIVE:
1. Load the market-specific protocol file (e.g., `state-file-mx-ps.md`)
2. Query DuckDB for latest weekly_metrics, daily_metrics, change_log for the market
3. Query Asana for overdue/blocked tasks related to the market (from Phase 1B sync)
4. Read slack-digest.md and email-triage.md for market-relevant signals (from Phase 1A/1C)
5. Read the current state file .md to get static sections (Goals, Tenets, Introduction) AND to extract current contents of all `<!-- WBR-OWNED:* -->` marker blocks
6. Generate the JSON payload per the placeholder schema in the protocol
7. Run quality gates: schema validation, math verification, weasel word scan
8. Patch the local .md file with new dynamic content (preserve static sections AND re-insert WBR-OWNED blocks verbatim — the daily engine must never modify content inside WBR-OWNED markers, only the AM-OWNED:trailing-week-flags block and unmarked dynamic sections)
9. Convert .md → .docx via `python3 -c` using `shared/tools/sharepoint-sync/converter.py`
10. Write both files to `~/shared/wiki/state-files/`
11. Log generation to DuckDB: `INSERT INTO workflow_executions (workflow_name, ...) VALUES ('state-file-[market]', ...)`

**Timing:** ~1-2 min per market. Runs sequentially within Step 2E (no parallelism needed — each market is fast).

**Failure handling:** If DuckDB has no new data for a market (same week as last generation), skip that market. Log skip reason. Don't regenerate stale content.

**Marker preservation (critical):** The daily engine MUST preserve the content inside all `<!-- WBR-OWNED:* -->` marker blocks verbatim. These blocks are written by the Monday WBR hook and must persist Tue–Fri without modification. If the engine cannot locate a required WBR-OWNED marker during step 5, log the missing marker and skip that market's patch (do not regenerate without the markers — doing so would erase WBR content on first run after migration gap).

**Data source note:** `ps.metrics` in DuckDB (queried via MCP `execute_query`) is the canonical weekly data source. It is populated by Step 2D.5 (PS Metrics Sync) which aggregates daily_metrics into the EAV format. The dashboard ingester writes daily_metrics when Richard drops a new xlsx; Step 2D.5 bridges the gap to ps.metrics. If ps.metrics is stale, the state file engine skips — it does NOT fall back to callout markdown files or raw daily data.

### Layer 1.5: WBR Callouts — Weekly Patch (Monday only)

Runs as a step within the WBR Callouts hook (`.kiro/hooks/wbr-callouts.kiro.hook`), after CORRECTION and before REPORT. Executes only on the WBR day (Monday).

For each registered state file where status = ACTIVE:
1. Read the current state file .md (freshly written by AM-Backend Step 2E earlier the same morning)
2. Patch content inside `<!-- WBR-OWNED:prediction-scoring -->` with one-sentence scoring outcome from the prediction ledger (HIT/MISS/SURPRISE, actual vs CI, error %)
3. Patch content inside `<!-- WBR-OWNED:forecast -->` with W{NN+1} Bayesian forecast paragraph (CI bounds, calibration state, explicit decision rule)
4. Patch content inside `<!-- WBR-OWNED:signal-flags -->` with one-sentence flags from Phase 2.5 cross-channel signal context (signal_strength >= 3.0 AND channel_spread >= 2; max 3 flags per market)
5. Update frontmatter `updated:` field to Monday's date
6. Write the patched .md back to `~/shared/wiki/state-files/`

**Scope constraints:**
- Writes ONLY inside `<!-- WBR-OWNED:* -->` marker blocks plus the `updated:` frontmatter field
- Does NOT touch `<!-- AM-OWNED:* -->` blocks, metric tables, MTD pacing, Lessons Learned, Strategic Priorities, or Appendices
- Does NOT regenerate .docx (AM-Backend Tuesday run handles that via the existing conversion pipeline)
- Does NOT push to SharePoint (AM-Backend Tuesday SharePoint sync handles that)

**Timing:** ~30s per market. Lightweight — only patching 3 small blocks.

**Failure handling:** If a required WBR-OWNED marker is missing, log the missing marker and skip that market's patch. Missing markers indicate a migration gap that requires manual repair; do not fabricate markers.

### Layer 2: EOD-Refresh Step 9 — Priority Patching (daily)

Runs after Asana reconciliation (Phase 1 Steps 1-8) completes. Task completions, carry-forwards, and blocker changes are known.

For each registered state file where status = ACTIVE:
1. Load the current state file .md
2. Read the EOD reconciliation output (completed tasks, carried tasks, new blockers)
3. Filter to market-relevant tasks (by project membership: AU, MX, or WW Testing)
4. Regenerate ONLY the Strategic Priorities section:
   - Update the priorities table with current deadlines and completion status
   - Update blocked items from the blocker registry (Phase 1 Step 6)
   - Update stakeholder actions from Asana comments and email signals
5. Patch the local .md file (touch ONLY Strategic Priorities + Blocked Items + Stakeholder Actions)
6. Reconvert .md → .docx
7. Write both files to `~/shared/wiki/state-files/`

**Timing:** ~30s per market. Lightweight — only patching 3 subsections.

**Key constraint:** EOD does NOT regenerate State of Business, Lessons Learned, or Appendices. Those are AM-only (data-driven). EOD only patches the action-oriented sections that change based on what happened during the day.

### Layer 3: SharePoint Durability Sync — Delivery (AM + EOD)

Runs as part of the existing SharePoint durability sync phases (AM Phase 5.5, EOD Phase 5).

For each registered state file where status = ACTIVE:
1. Read the local .docx from `~/shared/wiki/state-files/`
2. Upload .docx to `Kiro-Drive/state-files/[filename].docx` (overwrite)
3. Log sync to DuckDB workflow_executions

**Note:** Only .docx is uploaded to SharePoint. The .md source of truth stays local at `~/shared/wiki/state-files/`.

**Timing:** ~5s per market (2 uploads × ~2.5s each).

**Failure handling:** Non-blocking. If SharePoint is unreachable, local files are source of truth. Retry on next sync cycle.

---

## Amazon Writing Conventions (enforced across all markets)

These rules apply to ALL state files regardless of market. They are loaded from the engine, not per-market protocols.

1. **Continuous prose** in State of Business, Lessons Learned, and null case sections. No bullet points.
2. **Exact figures** required. Banned: "should", "might", "could potentially", "a lot", "many", "better" (without delta), "significant" (without number).
3. **Input before output** in State of Business. Controllable levers first, then lagging results.
4. **Null case mandatory.** Every update must quantify the cost of doing nothing for 7-14 days.
5. **Seasonality check mandatory.** Before generating any weekly narrative, check `~/shared/context/protocols/seasonality-calendar.md` for the reporting week. If a holiday falls within the week, lead the narrative with the holiday context and discount WoW/YoY comparisons accordingly. Missing a holiday attribution produces incorrect causal analysis.
6. **Page limit.** Core narrative ≤ 2 pages at 11pt Calibri, 1-inch margins. Appendices unlimited.
6. **SMART goals.** All goals must be Specific, Measurable, Achievable, Relevant, Time-bound.
7. **Tenets as decision hierarchy.** Tenets must be ordered by priority and used to resolve conflicts.
8. **Conditional Flags section.** When any key metric deviates >20% from the trailing 8-week average, insert a `## Flags` section between State of Business and Lessons Learned. Each flag follows the callout pipeline format: metric name, threshold breached, implication, and recommended action. When no anomalies are detected, the Flags section is omitted entirely — do not include an empty section or "no flags this week" placeholder.

## Quality Gates (enforced across all markets)

Before writing to local files:
1. Schema validation — all required JSON keys present
2. Math verification — CPA, ROAS, ie%CCP (or market equivalent) match deterministic recalculation
3. Weasel word scan — zero violations of banned language list
4. Style replication — static sections (Goals, Tenets, Introduction) unchanged from template
5. Content replication — historical appendix data matches DuckDB source of truth
6. Page limit — core narrative ≤ 2 pages
7. Marker integrity — all required `<!-- WBR-OWNED:* -->` and `<!-- AM-OWNED:* -->` marker blocks present, properly paired (START + END), and content inside non-owned markers unchanged from pre-patch state

## Field Ownership Contract

Each section of a state file has exactly one owning hook. The contract is machine-enforceable via HTML comment markers (`<!-- OWNER-OWNED:field-name START/END -->`). Non-owners must preserve the content inside an owned block verbatim.

| Section / field | Owner hook | Marker |
|---|---|---|
| Frontmatter `title:`, `status:`, `created:` | Manual | — (static) |
| Frontmatter `updated:` | Last writer (any hook) | — |
| Frontmatter `data_through:` | AM-Backend Step 2E | — |
| Introduction, Goals, Tenets | Manual | — (static) |
| State of Business — metric tables (Input/Output) | AM-Backend Step 2E | — |
| State of Business — narrative paragraphs, MTD pacing (incl. vs-OP2 %) | AM-Backend Step 2E | — |
| Prediction scoring outcome line | WBR Callouts | `<!-- WBR-OWNED:prediction-scoring -->` |
| Forward forecast paragraph (W+1 CI, calibration, decision rule) | WBR Callouts | `<!-- WBR-OWNED:forecast -->` |
| Flags — trailing-week anomaly table + Recommended action + Cost of inaction | AM-Backend Step 2E | `<!-- AM-OWNED:trailing-week-flags -->` |
| Flags — cross-channel signal flags | WBR Callouts | `<!-- WBR-OWNED:signal-flags -->` |
| Lessons Learned | AM-Backend Step 2E | — |
| Strategic Priorities / Blocked Items / Stakeholder Actions | EOD-Refresh Step 9 | — |
| Appendices | AM-Backend Step 2E | — |
| Loop Reporting Queue (WW Testing only) | AM-Backend Step 2E | `<!-- AM-OWNED:loop-reporting-queue -->` |
| Active Test Dossier — Appendix I (WW Testing only) | AM-Backend Step 2E | `<!-- AM-OWNED:active-test-dossier -->` |
| Staleness Report — Appendix J (WW Testing only) | AM-Backend Step 2E | `<!-- AM-OWNED:staleness-report -->` |

**Rule for all hooks:** Before writing, read the current file and extract content inside every marker block that does not belong to you. Re-insert those blocks verbatim in your output. If a required marker is missing, log the gap and skip that market — do not fabricate markers.

**WW Testing per-test ingestion exception:** The Loop Reporting Queue, Appendix I, and Appendix J rebuild every AM-Backend run regardless of `ps.metrics` freshness. Their inputs (Asana, Slack, email, Hedy, Quip modification timestamps) change daily even when weekly metrics do not. See `state-file-ww-testing.md` → Ingestion Rules → Rule 5. This overrides the general "skip market if ps.metrics stale" rule for these three sections only; the State of Business narrative and metric tables continue to follow the skip rule.

## Conversion Pipeline

```bash
python3 -c "
import sys
sys.path.insert(0, '$HOME/shared/tools/sharepoint-sync')
from converter import MarkdownConverter
with open('[input.md]') as f: content = f.read()
lines = content.split('\n')
if lines[0].strip() == '---':
    end = next(i for i, l in enumerate(lines[1:], 1) if l.strip() == '---')
    title = 'Untitled'
    for l in lines[1:end]:
        if l.startswith('title:'): title = l.split(':', 1)[1].strip().strip('\"')
    body = '\n'.join(lines[end+1:])
else:
    title, body = 'Untitled', content
converter = MarkdownConverter()
with open('[output.docx]', 'wb') as f: f.write(converter.to_docx(body, {'title': title}))
"
```

## Per-Market Protocol Files

Each market protocol defines:
- **Analytical parameters** (constraint models, thresholds, baselines)
- **Data sources** (DuckDB tables, Quip docs, meeting notes)
- **Stakeholder context** (primary contacts, relationship dynamics)
- **Market-specific metrics** (ie%CCP for MX, OCI lift for AU, test status for WW Testing)
- **Placeholder schema** (which {{tags}} exist and their data sources)

The engine loads the generic conventions + the market protocol. The market protocol overrides nothing — it only adds market-specific parameters.

---

## Adding a New Market

1. Create `~/shared/context/protocols/state-file-[market]-ps.md` with market-specific parameters
2. Create `~/shared/wiki/state-files/[market]-state.md` with the initial human-authored baseline
3. Add the market to the Registered State Files table above
4. Set status = ACTIVE
5. The engine picks it up on the next AM-Backend run automatically
