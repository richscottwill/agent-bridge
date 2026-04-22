# Karpathy Queue

Routing memo for karpathy review. Do not action items here without karpathy's triage.

---

## 2026-04-21 — am-frontend session-summary

### Issue 1: am-auto.kiro.hook trigger policy

**Problem:** The AM-Backend hook (`~/.kiro/hooks/am-auto.kiro.hook`) has `"when": {"type": "userTriggered"}` with no time-based or promptSubmit trigger. As a result, the hook only fires when Richard manually invokes it from the Agent Hooks panel. On 2026-04-21 the hook was invoked but skipped Phase 2.5 / 3B / 4-full / 5.5 (per session-log 2026-04-21 entry), leaving `am-enrichment-queue.json` and `am-portfolio-findings.json` with Apr 13 stamps for 8 days. AM-Frontend has to fall back to live MCP queries and stale JSON to generate the daily brief.

**Evidence:**
- am-auto.kiro.hook line `"when": {"type": "userTriggered"}` (viewed 2026-04-21)
- session-log.md 2026-04-21 entry: "Skipped Phase 2.5 / 3B / 4 full scans / B2 remaining 14 tasks / Phase 5.5 SharePoint sync"
- File stat on am-enrichment-queue.json / am-portfolio-findings.json showed Apr 13 mtime until 2026-04-21 ~08:05 PT when I regenerated them manually from DuckDB
- Display name `.AM-Backend: Ingest + Process` had leading period causing Kiro Agent Hooks panel to hide it — fixed 2026-04-21 to "AM-Backend: Ingest + Process"

**Proposed Fix (karpathy to decide):**
1. Change trigger to `promptSubmit` with a once-per-day guard (check if `am-enrichment-queue.json` mtime >= today 04:00 PT, else fire). Fires on Richard's first message of the day.
2. Keep `userTriggered` but add a promptSubmit staleness nag: separate hook that checks mtime and nudges Richard if stale.
3. Add time-based schedule if Kiro platform supports it (does not appear to per current hook schema).
4. Keep manual BUT guarantee the backend always completes all phases — the current behavior of skipping Phase 4/compile when the hook IS fired is a separate deferral issue acknowledged in session-log 2026-04-21.

**Scope/Impact:** Affects AM-Frontend daily brief accuracy. Current workaround: AM-Frontend frontend queries DuckDB live when JSON is stale — works but adds 20-30s and skips the portfolio/blocker/budget enrichment logic.

**Priority:** High. This is a governance gap in the daily loop.

### Issue 2: hard-thing-refresh.py not wired to any trigger

**Problem:** The hard-thing selection redesign was promoted 2026-04-20 (per session-log 2026-04-20 entry). Infrastructure exists: `~/shared/tools/scripts/hard-thing-refresh.py`, `main.hard_thing_candidates` table DDL, `main.hard_thing_now` view referenced by amcc.md. But on 2026-04-21 a query against `main.hard_thing_candidates` returned "Catalog Error: Table does not exist" — the refresh script has never run in production. amcc.md line ~178 says "Before naming today's hard thing, query main.hard_thing_now" — that query fails silently.

**Evidence:**
- grepSearch for `hard_thing_candidates` found: protocol (shared/context/protocols/hard-thing-selection.md), refresh script (shared/tools/scripts/hard-thing-refresh.py), amcc.md references, session-log 2026-04-20 promotion entry — but NO hook file contains the refresh invocation
- am-auto.kiro.hook prompt does not invoke hard-thing-refresh
- am-backend-parallel.md protocol does not mention hard-thing-refresh step
- DuckDB catalog confirms `main.hard_thing_candidates` does not exist (table was never created, refresh never ran)
- Session-log 2026-04-20 entry notes token dependency: "MotherDuck dependency: signals.signal_tracker lives on MotherDuck, refresh requires motherduck_token in env"

**Proposed Fix (karpathy to decide):**
1. Add `python3 ~/shared/tools/scripts/hard-thing-refresh.py` call to am-backend-parallel.md Phase 2 (post-signal-routing, before Phase 3 enrichment). Verify motherduck_token available in hook context.
2. Also add to eod.kiro.hook (evening refresh catches end-of-day signal shifts).
3. Validate the DDL creates the table on first run (script currently assumes table exists — may need CREATE TABLE IF NOT EXISTS logic).
4. Until wired, amcc.md should note the dependency or fall back gracefully.

**Scope/Impact:** aMCC's hard-thing selection currently runs on the old top-down task-queue model, not the new signal-driven model that was explicitly promoted 4/20. Today's morning brief manually identified "Testing Approach / Kate doc" as the hard thing from cross-channel signals (polaris-brand-lp quality 27.5, au-cpa-cvr 14.0, etc.) — correct answer but not reproducible without the refresh procedure running.

**Priority:** High. Blocks the entire redesign from operating.

### Issue 3: Step 4 wiki pipeline usefulness in am-frontend (compression proposal)

**Problem:** am-frontend.md Step 4 reads am-wiki-state.json and routes action to wiki-editor or wiki-maintenance hook. On 2026-04-21 Richard pushed back: (a) wiki-maintenance.kiro.hook already runs weekly and handles stale/drift, (b) signals.wiki_candidates is surfaced in the pre-brief queries and is the useful daily signal, (c) deprecated ABPS AI Content project removed most action-routing, (d) wiki-editor should be pull-based not push-based.

**Evidence:**
- am-frontend.md Step 4 still references wiki-editor / wiki-maintenance routing
- wiki-maintenance.kiro.hook exists and runs on weekly cadence (handles stale/drift already)
- signals.wiki_candidates + wiki.publication_registry are the daily-useful surfaces
- ABPS AI Content Asana project deprecated 2026-04-17 per soul.md
- am-frontend.md Step 6C references `ps-forecast-tracker.xlsx` / `ps-pacing-dashboard.xlsx` / `command-center.xlsx` SharePoint pushes — these xlsx files do not exist locally (dashboard pipeline migrated to JSON-based outputs in shared/dashboards/data/), served via dashboard-server.kiro.hook

**Proposed Fix (karpathy to decide):**
- Compress Step 4 to a one-line callout in the daily brief: "📚 Wiki: N articles in pipeline, top uncovered candidate: [topic] (quality X)" — drawn from signals.wiki_candidates + wiki.publication_registry.
- Remove the standalone Step 4 section from am-frontend.md.
- Route wiki candidate triage to a weekly rhythm (e.g., Friday EOD or a new wiki-weekly.kiro.hook).
- Separately: remove or update Step 6C xlsx references to reflect the JSON-based dashboard pipeline.

**Scope/Impact:** Saves ~2-3 minutes of AM-Frontend wall-clock + reduces decision load on Richard. Aligns with soul.md principle 3 (subtraction before addition) and principle 6 (reduce decisions, not options). Step 6C cleanup is a staleness fix — current references point at files that do not exist.

**Priority:** Medium. Quality-of-life + staleness cleanup, not a correctness issue.

Routed by: am-frontend session-summary 2026-04-21 | For karpathy review
