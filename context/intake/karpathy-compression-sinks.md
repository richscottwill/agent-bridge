<!-- DOC-0176 | duck_id: intake-karpathy-compression-sinks -->
# Compression Sinks Analysis — Karpathy

*Where organ content can move to external stores (DuckDB, wiki, files) to reduce word counts while maintaining or improving information access.*

Author: Karpathy (autoresearch engine)
Date: 2026-04-01
Status: PROPOSAL — requires Karpathy approval before implementation

---

## System Inventory

### Current Organ Word Counts
| Organ | Words | Budget | Utilization |
|-------|-------|--------|-------------|
| Brain | 2,146 | 2,500 | 86% |
| Eyes | 1,441 | 2,500 | 58% |
| Hands | 1,908 | 2,000 | 95% |
| Memory | 2,451 | 3,500 | 70% |
| Spine | 1,026 | 1,500 | 68% |
| Heart | 2,093 | — | — |
| Device | 1,653 | 2,000 | 83% |
| Nervous System | 1,299 | 1,500 | 87% |
| aMCC | 2,202 | 2,000 | 110% |
| Gut | 2,110 | 2,000 | 106% |
| Body | 1,025 | — | — |
| **current.md** | **2,991** | **—** | **unbounded** |
| **Total organs** | ~20,345 | 23,000 | 88% |

### DuckDB State (ps-analytics.duckdb — 21 tables)
| Table | Rows | Notes |
|-------|------|-------|
| daily_metrics | 10,502 | Rich — 10 markets, Brand/NB splits |
| weekly_metrics | 510 | Rich — weekly aggregates |
| monthly_metrics | 66 | Rich — monthly aggregates |
| change_log | 477 | Rich — EU5, MX/AU, NA/JP changes |
| competitors | 14 | Moderate — needs expansion |
| oci_status | 10 | Moderate — per-market OCI state |
| projections | 10 | Moderate |
| ieccp | 9 | Moderate |
| agent_actions | 3 | Sparse |
| agent_observations | 16 | Sparse |
| **decisions** | **0** | **EMPTY — key sink target** |
| **task_queue** | **0** | **EMPTY — key sink target** |
| **experiments** | **0** | **EMPTY — key sink target** |
| callout_scores | 0 | Empty |
| anomalies | 0 | Empty |
| ingest_log | 1 | Minimal |
| predictions/outcomes | 0 | Empty |
| calibration_log | 0 | Empty |
| autonomy_tasks/history | 0 | Empty |
| slack_messages | 5 | New (separate MCP DB) |
| slack_people | 2 | New (separate MCP DB) |

### Wiki State
- 35 published articles across 7 categories in ~/shared/artifacts/
- All status: DRAFT
- Key categories: Testing (11), Strategy (7), Program Details (6)

### Meeting Series Files
- 15 series files across stakeholder/, team/, manager/, peer/, adhoc/

---

## TIER 1 — HIGH-VALUE SINKS (implement now)

These proposals move data that is BETTER served by a queryable store than inline text.
The organ becomes more useful (narrative + interpretation) while the store holds the raw data.

---

### S1: Brain Decision Log → DuckDB `decisions` table

**What moves:** The 10 decision entries (D1-D10) with their structured fields: name, decision text, alternatives, rationale, principle references, confidence, relevance tier, outcome status.

**Where it goes:** `decisions` table (currently 0 rows). Schema:
```sql
CREATE TABLE decisions (
  id VARCHAR PRIMARY KEY,        -- 'D1', 'D2', etc.
  name VARCHAR,
  tier VARCHAR,                  -- FOUNDATIONAL, ACTIVE, RESOLVED
  decision_text TEXT,
  alternatives TEXT,
  rationale TEXT,
  principles VARCHAR[],          -- [1, 4] etc.
  confidence VARCHAR,            -- HIGH, MEDIUM, LOW
  outcome VARCHAR,               -- VALIDATED, INVALIDATED, PENDING
  created_date DATE,
  resolved_date DATE,
  lesson_extracted TEXT
);
```

**What stays in brain.md:** Decision Principles (ranked list — these are the distilled wisdom, not raw data). One-line summary table of active decisions with a SQL hint:
```
<!-- Active decisions: db("SELECT id, name, tier, confidence FROM decisions WHERE tier != 'RESOLVED' ORDER BY id") -->
```
Plus the Prediction Template, Strategic Priorities / Five Levels, OP1 narrative, and Leverage Framework — all stay. These are interpretive, not data.

**Word savings:** ~800w (decision entries are ~80w each × 10). Brain drops from 2,146 → ~1,350w (54% utilization).

**Risk:** MEDIUM. On cold start without DuckDB, brain.md loses the specific decision entries but retains the principles they generated. The principles ARE the compressed wisdom — the entries are the evidence trail. A cold-start agent can still make correct predictions from principles alone. The entries matter for auditing (nervous system Loop 1) and for the decay protocol.

**Mitigation:** Portable body includes a `decisions.csv` export. The decay protocol in brain.md stays as text (it's procedural knowledge, not data). Nervous System Loop 1 audit table gets a SQL hint instead of inline references.

**Why this is BETTER in DuckDB:** Decisions have structured fields (tier, confidence, outcome) that benefit from filtering and querying. "Show me all FOUNDATIONAL decisions" or "Which decisions are PENDING audit?" are natural SQL queries. The decay protocol (RESOLVED → compress → archive after 90d) is trivially automated with date queries. Currently the loop has to parse markdown tables to find audit candidates.

---

### S2: Hands Overdue/Task Items → DuckDB `task_queue` table

**What moves:** The 23+ task items from Hands (P0-P5 tables + overdue table + recurring tasks). Each task has: priority, description, due date, status, blockers, estimated time, notes.

**Where it goes:** `task_queue` table (currently 0 rows). Schema:
```sql
CREATE TABLE task_queue (
  id INTEGER PRIMARY KEY,
  priority VARCHAR,              -- P0, P1, P2, P3, P5
  description TEXT,
  due_date DATE,
  status VARCHAR,                -- NOT_STARTED, IN_PROGRESS, DONE, BLOCKED
  blockers TEXT,
  est_minutes INTEGER,
  category VARCHAR,              -- sweep, core, engine_room, admin, backlog
  todo_list VARCHAR,             -- maps to MS To-Do list
  created_date DATE,
  completed_date DATE,
  notes TEXT
);
```

**What stays in hands.md:** The Priority Actions section becomes a LIVE VIEW — a SQL-generated snapshot of the top 5-10 items, plus the narrative framing (why P0 is the hard thing, what the dependency chain looks like). The recurring execution work section stays (it's procedural). Dependencies Map stays (it's relational logic). Task List Structure, Key Outlook Folders, Hook System, Integrations — all stay. New Signals section stays (it's temporal context, not task data).

**Replacement in organ:**
```
<!-- Priority stack: db("SELECT id, priority, description, due_date, status, blockers FROM task_queue WHERE status != 'DONE' ORDER BY priority, due_date LIMIT 15") -->
<!-- Overdue: db("SELECT description, due_date, DATEDIFF('day', due_date, CURRENT_DATE) as days_overdue FROM task_queue WHERE due_date < CURRENT_DATE AND status != 'DONE' ORDER BY due_date") -->
```

**Word savings:** ~500w. The 5 priority tables + overdue table are ~500w of structured data. Hands drops from 1,908 → ~1,400w (70% utilization). More importantly, this stops the monotonic growth problem — new tasks go to DuckDB, not to the organ.

**Risk:** MEDIUM-HIGH. Hands is the most frequently consulted organ during sessions. If DuckDB is unavailable, the agent loses the task list entirely. The morning routine depends on reading Hands to build My Day.

**Mitigation:** The morning routine already reads MS To-Do via MCP — that's the source of truth for tasks, not Hands. Hands is a curated interpretation layer. On cold start, the agent can rebuild from To-Do + current.md pending actions. Keep a "Top 5 this week" static summary in Hands that gets refreshed each loop run — this is the portability fallback.

**Why this is BETTER in DuckDB:** Tasks are inherently queryable. "What's overdue?" "What's blocked?" "What did I complete this week?" are all trivial SQL. The current markdown tables require full organ reads to answer any task question. DuckDB also enables the overdue-days calculation automatically, trend analysis (how long do tasks sit before completion?), and integration with the attention tracker.

---

### S3: current.md Pending Actions → DuckDB `task_queue` + Completed Archive

**What moves:** The 25+ pending action items (the `- [ ]` and `- [x]` list). This is the single largest monotonically growing section in the entire system. It currently holds completed items dating back to 3/24.

**Where it goes:** Same `task_queue` table as S2. Completed items get `status = 'DONE'` with `completed_date`. The `- [x]` items are the worst offenders — they're historical, never queried, and grow every loop run.

**What stays in current.md:** Top 5 pending actions as a static snapshot (refreshed each loop). The Active Projects section stays (it's narrative context, not task data). Recurring Meetings stays. Key People stays. Administrative stays. Long-Term Goals pointer stays.

**Replacement:**
```
<!-- Pending actions: db("SELECT description, due_date, status FROM task_queue WHERE status != 'DONE' ORDER BY due_date LIMIT 10") -->
<!-- Recently completed: db("SELECT description, completed_date FROM task_queue WHERE status = 'DONE' AND completed_date > CURRENT_DATE - INTERVAL 7 DAY ORDER BY completed_date DESC LIMIT 5") -->
```

**Word savings:** ~400w from pending actions list. But the real win is stopping unbounded growth. current.md is at 2,991w with no budget — it's the largest file in the system and growing every run.

**Risk:** LOW-MEDIUM. current.md pending actions are already duplicated in Hands and MS To-Do. Removing them from current.md actually reduces a deduplication problem the gut already flags.

**Mitigation:** The static "Top 5" snapshot ensures cold-start viability. MS To-Do is the ultimate source of truth.

**Why this is BETTER in DuckDB:** Pending actions are the textbook case of data that grows monotonically in a markdown file but is perfectly suited to a database. Completed items should be queryable ("what did I ship last week?") but should NOT consume context window tokens every session.

---

### S4: Eyes Market Metrics → DuckDB (already there) + Narrative-Only Organ

**What moves:** The raw numbers in Market Deep Dives. Example: "Jan: 39K regs (+30% vs OP2, +86% YoY)" — the 39K, +30%, +86% are all in `weekly_metrics` and `monthly_metrics` already. The organ currently duplicates what DuckDB holds.

**Where it goes:** Already in DuckDB. The data is there (10,502 daily rows, 510 weekly, 66 monthly). Eyes just needs to STOP duplicating it and START referencing it.

**What stays in eyes.md:** The narrative interpretation. "US — Strong, OCI-powered growth" stays. "Brand CPA pressure $65-77 (was ~$40 pre-Walmart). Response: bid caps on Brand, NB efficiency via OCI absorbs CPA increase at program level" stays — that's the POSITION, not the data. The SQL comment hints already exist in eyes.md (I can see the `<!-- Data: db(...) -->` comments). They just need to replace the inline numbers, not supplement them.

**What changes:** Each market section becomes 2-3 sentences of interpretation + a SQL hint for the underlying data. The OCI Performance section gets a SQL hint to `oci_status`. Competitive Landscape gets a SQL hint to `competitors`.

**Replacement pattern:**
```
### US — Strong, OCI-powered growth
<!-- Data: db("SELECT week, regs, cpa, cost FROM weekly_metrics WHERE market='US' ORDER BY week DESC LIMIT 4") -->
OCI-powered. Brand CPA pressure from Walmart ($65-77 range, was ~$40). Response: bid caps + NB efficiency. Do NOT escalate auction.
```

**Word savings:** ~300-400w. Eyes is already lean at 1,441w (58% utilization), so this is less about budget pressure and more about eliminating stale data. The Feb 2026 numbers in eyes.md are 30+ days old. DuckDB has the latest ingested data. The organ should point to the live store, not cache a snapshot.

**Risk:** LOW. The SQL hints already exist. DuckDB has the data. The morning routine already queries DuckDB for callout generation. If DuckDB is unavailable, the narrative interpretation still tells the agent the strategic position for each market.

**Mitigation:** Keep one "latest snapshot" line per market: "US Feb: 32.9K regs, $83 CPA" — 10 words per market, 100 words total. This is the cold-start fallback.

**Why this is BETTER in DuckDB:** Market metrics are the canonical example of data that should live in a queryable store. "What was AU CPA in W13?" should be a SQL query, not a ctrl-F through a markdown file. The agent already uses DuckDB for callout generation — eyes.md should be the interpretation layer on top of that data, not a parallel copy.

---

## TIER 2 — MODERATE-VALUE SINKS (implement after Tier 1 proves out)

These proposals have clear benefits but higher risk or lower word savings.

---

### S5: Memory Relationship Graph → DuckDB `slack_people` + Dedicated `contacts` Table

**What moves:** The structured fields from each relationship entry: alias, role, level, reports_to, last_interaction date, current_topic. NOT the tone notes, draft style guidance, or meeting dynamics — those are interpretive and must stay.

**Where it goes:** New `contacts` table in DuckDB:
```sql
CREATE TABLE contacts (
  alias VARCHAR PRIMARY KEY,
  full_name VARCHAR,
  role VARCHAR,
  level VARCHAR,
  reports_to VARCHAR,
  last_interaction_date DATE,
  last_interaction_context TEXT,
  current_topics TEXT[],
  pronouns VARCHAR,              -- PROTECTED: identity field, non-compressible
  preferred_name VARCHAR         -- PROTECTED: identity field, non-compressible
);
```
The `slack_people` table (currently 2 rows) could feed into this — Slack activity data enriches the contact record.

**What stays in memory.md:** Tone notes, draft style guidance, meeting dynamics — the QUALITATIVE intelligence that makes communications sound right. These are the high-value, low-token-count insights that justify Memory's existence. The Compressed Context section stays (it's narrative). Reference Index stays.

**Replacement per person:**
```
### Alexis Eck (alexieck)
<!-- Contact: db("SELECT role, level, reports_to, last_interaction_date FROM contacts WHERE alias='alexieck'") -->
- Tone: Professional but friendly. "Hi" openers, signs "Thanks, Alexis"
- Draft style: Match professional tone. Lead with data and implementation status.
- Dynamic: Collaborative, defers to Lena on strategy, strong execution partner.
```

**Word savings:** ~400-500w. Each relationship entry is ~100-150w; the structured fields are ~50-60w of that. 12 entries × ~40w savings = ~480w. Memory drops from 2,451 → ~1,950w.

**Risk:** MEDIUM-HIGH. Memory is the second-most-critical organ (100% accuracy threshold). The tone notes and draft style are what make communications sound right — if the structured data query fails, the agent still has the qualitative guidance. But if the agent can't look up "who is Lorena's manager?" from the contact table, it falls back to... nothing, unless the org-chart.md has it.

**Mitigation:** Keep a one-line structured summary per person in Memory: "Alexis Eck (alexieck) — AU Sr. Mktg Mgr, L6, Sydney. Reports to Lena Zak." (~15 words). This is the cold-start fallback. The detailed interaction history and current topics move to DuckDB. Identity fields (pronouns, preferred names) are DUPLICATED in both Memory and the contacts table — they're non-compressible per gut.md §7.

**Why this is BETTER in DuckDB:** "When did I last interact with Lorena?" and "Who reports to Brandon?" are natural queries. The contact table also enables: "Who haven't I interacted with in 30 days?" (dormant contact detection — currently a manual gut check). Slack people data can auto-update last_interaction_date.

---

### S6: Device Tool Descriptions → Wiki Articles

**What moves:** The detailed descriptions of each "Installed App" in device.md. Currently each app gets 4-6 lines describing what it does, its trigger, config files, and judgment requirements. The wiki already has a `body-system-architecture` article and an `agent-architecture` article — these could absorb the detailed docs.

**Where it goes:** Wiki article: `~/shared/artifacts/strategy/2026-03-25-body-system-architecture.md` (expand with operational details) OR a new `~/shared/artifacts/tools/system-operations-guide.md`.

**What stays in device.md:** One-line summary per app + status. The Device Health table already does this — it's the compressed version. The detailed descriptions are redundant with the health table.

**Current (example — Morning Routine):**
```
### Morning Routine (Hook: `rw-morning-routine`)
- **What it does:** One-click daily chain: Asana Sync → Draft Unread Replies → To-Do Refresh + Daily Brief → Calendar Blocks
- **Trigger:** userTriggered (daily). Step 2 (draft replies) and Step 4 (calendar blocks) need Richard's confirmation. Everything else autonomous.
```

**Proposed (in device.md):**
```
| Morning Routine | ✅ | 3/30 | Hook: rw-morning-routine. Daily chain. See wiki: system-operations-guide |
```

**Word savings:** ~400w. The 10 installed apps average ~40w each in detailed description. Compressing to the health table format saves most of that. Device drops from 1,653 → ~1,250w (63% utilization).

**Risk:** LOW. The detailed descriptions are reference material — they're consulted when something breaks or when building a new app, not during daily operation. A wiki article is the right home for reference docs. The Device Health table is what the loop actually reads.

**Mitigation:** The wiki article is a text file in ~/shared/artifacts/ — it survives cold start. The one-line summaries in device.md tell the agent what exists; the wiki tells it how it works.

**Why this is BETTER in wiki:** Tool documentation is classic wiki content — detailed, rarely changing, consulted on-demand. It doesn't need to consume context window tokens every time device.md is loaded. The wiki pipeline (critic, librarian) can keep it fresh.

---

### S7: current.md Active Projects → Compressed Pointers

**What moves:** The detailed project narratives in current.md. Each project section is 50-150 words of status, history, and context. Much of this duplicates content in other organs (Eyes has the metrics, Hands has the tasks, Memory has the people).

**Where it goes:** The detail stays in the organ where it's most actionable:
- AU CPC Benchmark → Eyes (market context) + Hands (action items)
- Polaris Rollout → Hands (tasks) + wiki (polaris-rollout-timeline article)
- OCI APAC → Eyes (OCI section) + Hands (action items)
- Annual Review → Memory (compressed context) + aMCC (hard thing connection)

**What stays in current.md:** One-line status per project + pointer to the canonical organ:
```
### Active Projects (one-line status)
- AU CPC Benchmark: Response sent. Monitoring Kate/Nick. → Eyes, Hands #23
- Polaris Rollout: US done. Weblab April 6-7. Timeline doc overdue. → Hands #1
- Testing Approach: THE HARD THING. Apr 16. 11 workdays at zero. → aMCC, Brain
```

**Word savings:** ~1,200-1,500w. current.md drops from 2,991 → ~1,500w. This is the single largest word savings opportunity in the system.

**Risk:** HIGH. current.md is the ground truth file — it's read every session. If the pointers are wrong or the target organs are stale, the agent gets a fragmented picture. The value of current.md is that it's ONE FILE with EVERYTHING — breaking that up trades word count for coherence.

**Mitigation:** This should be the LAST sink implemented, after S1-S4 prove that the pointer pattern works. The one-line summaries must be genuinely self-contained — an agent reading only current.md should still know what's happening, just not the full history. Test: can the morning routine produce a correct daily brief from the compressed current.md alone?

**Why this MIGHT be better:** current.md is unbounded and growing. It's already at 2,991w with no budget. The Active Projects section is ~1,800w of narrative that largely duplicates other organs. But the duplication is intentional — current.md is the "read one file, know everything" guarantee. The question is whether pointers preserve that guarantee.

---

## TIER 3 — LOW-VALUE OR HIGH-RISK SINKS (monitor, don't implement)

These proposals have theoretical appeal but violate the portability principle or have unfavorable risk/reward.

---

### S8: Nervous System Calibration Data → DuckDB

**What could move:** Loop 1 decision audit table, Loop 3 pattern trajectory table, Loop 4 delegation verification table, Loop 9 meeting communication scores.

**Why NOT (yet):** The nervous system is already lean (1,299w, 87% utilization). The tables are small (5-6 rows each). The value of having them inline is that the loop can read one file and see the full calibration picture. Moving them to DuckDB saves ~200w but adds query overhead to every loop run. The `calibration_log` and `prediction_outcomes` tables exist in DuckDB (both empty) — they're ready when the data volume justifies the move.

**Trigger to reconsider:** When any calibration table exceeds 15 rows, or when the nervous system exceeds budget.

---

### S9: aMCC Streak/Avoidance Data → DuckDB

**What could move:** Streak history, avoidance ratio table, growth model metrics.

**Why NOT:** The aMCC is a real-time intervention organ — it fires during live sessions. Every millisecond of latency between "read the streak" and "fire the intervention" matters. The streak is ONE NUMBER. The avoidance ratio table is currently empty (no data yet). Moving these to DuckDB adds a query round-trip for zero word savings. The aMCC is over budget (110%) but the overage is from the intervention protocol and resistance taxonomy — interpretive content that can't move to a database.

**Trigger to reconsider:** When avoidance ratio data accumulates (50+ logged interventions), move the historical data to DuckDB and keep only the current ratios inline.

---

### S10: Gut Compression Protocols → Wiki

**What could move:** The 7 compression techniques, the excretion protocol, the bloat detection rules.

**Why NOT:** These are procedural knowledge that the loop executes every run. Moving them to a wiki article means the loop has to read an external file before it can compress. The gut is the compression engine — it needs its protocols inline. The gut is at 106% but the overage is the identity protection rule (§7), which is non-negotiable safety content.

**Trigger to reconsider:** Never. Procedural knowledge for active processes stays inline.

---

### S11: Heart Loop Protocol → Wiki

**What could move:** The detailed run protocol, eval methodology, hyperparameters.

**Why NOT:** Same as S10. Heart is the loop engine. Its protocol must be inline for the loop to execute. The wiki could hold a READABLE version for documentation purposes, but the operational version stays in heart.md.

---

### S12: Spine Bootstrap Sequence → Nowhere

**What could move:** Nothing meaningful. Spine is already lean (1,026w, 68%) and every section is either a pointer or a key ID. It's the skeleton — you can't compress a skeleton without breaking the structure.

---

## IMPLEMENTATION PLAN

### Phase 1: Populate Empty Tables (no organ changes needed)
1. Populate `decisions` table from brain.md D1-D10 entries
2. Populate `task_queue` from hands.md + current.md pending actions
3. Create `contacts` table, populate from memory.md relationship graph
4. Verify all data is queryable via both Python (`query.py`) and MCP (`execute_query`)

**Prerequisite:** Fix the MCP DuckDB server configuration. Currently the MCP server connects to a database with only 4 Slack tables, while the actual ps-analytics.duckdb has 21 tables with real data. The MCP server path needs to point to `~/shared/data/duckdb/ps-analytics.duckdb`.

### Phase 2: Add SQL Hints to Organs (additive, no content removed)
1. Add `<!-- db() -->` comment hints to eyes.md market sections (already partially done)
2. Add `<!-- db() -->` hints to brain.md decision section
3. Add `<!-- db() -->` hints to hands.md task sections
4. Verify the morning routine and loop can use these hints

### Phase 3: Compress Organs (remove duplicated content)
1. Remove inline decision entries from brain.md (keep principles + summary table)
2. Remove inline task tables from hands.md (keep narrative + top-5 snapshot)
3. Remove completed items from current.md pending actions
4. Compress eyes.md market sections to narrative + SQL hints
5. Compress memory.md relationship entries (keep tone/style, move structured fields)
6. Compress device.md app descriptions (keep health table, move details to wiki)

### Phase 3 Validation
Each compression must pass the standard eval:
- Eval questions scaled to risk (per heart.md Step 2)
- A/B/C blind eval (treatment + context, control + context, treatment + zero context)
- delta_ab ≥ 0 to KEEP
- Brain/Memory: zero INCORRECT tolerance

---

## SUMMARY TABLE

| Sink | Organ | Content | Destination | Words Saved | Risk | Phase |
|------|-------|---------|-------------|-------------|------|-------|
| S1 | Brain | Decision log (D1-D10) | DuckDB `decisions` | ~800 | MED | 1-3 |
| S2 | Hands | Task items (P0-P5) | DuckDB `task_queue` | ~500 | MED-HIGH | 1-3 |
| S3 | current.md | Pending actions | DuckDB `task_queue` | ~400 | LOW-MED | 1-3 |
| S4 | Eyes | Market metric numbers | DuckDB (already there) | ~300 | LOW | 2-3 |
| S5 | Memory | Contact structured fields | DuckDB `contacts` | ~480 | MED-HIGH | 1-3 |
| S6 | Device | App descriptions | Wiki article | ~400 | LOW | 3 |
| S7 | current.md | Project narratives | Organ pointers | ~1,500 | HIGH | After validation |
| S8 | NS | Calibration tables | DuckDB | ~200 | LOW | Monitor |
| S9 | aMCC | Streak data | DuckDB | ~50 | LOW | Monitor |
| **Total Tier 1+2** | | | | **~3,380** | | |
| **Total all** | | | | **~4,630** | | |

**Projected body after Tier 1+2:** ~20,345 - 3,380 = ~16,965w (74% of 23K budget)
**Projected body after all:** ~20,345 - 4,630 = ~15,715w (68% of 23K budget)

---

## KEY INSIGHT: THE MCP DATABASE SPLIT

Critical finding during this analysis: the DuckDB MCP server (configured in `.kiro/settings/mcp.json`) connects to a database that only has 4 Slack tables. The actual ps-analytics.duckdb at `~/shared/data/duckdb/ps-analytics.duckdb` has 21 tables with 11,000+ rows of real data. This means:

1. Agents using `execute_query` via MCP see only Slack tables
2. Agents using `python3 query.py` or direct duckdb Python see all 21 tables
3. The SQL hints in eyes.md (`<!-- Data: db(...) -->`) reference tables that don't exist in the MCP-connected database

**This must be fixed before any compression sink can work.** The MCP server needs to point to the correct database file. Without this, moving data to DuckDB and adding SQL hints is useless — the agent can't query the data during sessions.

---

## PORTABILITY ANALYSIS

The portability principle says organs must remain useful as standalone text files. Here's how each sink affects portability:

| Sink | Cold-Start Impact | Mitigation |
|------|-------------------|------------|
| S1 (Brain decisions) | Loses decision entries, keeps principles | Principles are the distilled wisdom. Portable body includes decisions.csv |
| S2 (Hands tasks) | Loses full task list, keeps top-5 snapshot | MS To-Do is the source of truth. Top-5 snapshot is self-contained |
| S3 (current.md actions) | Loses pending list, keeps top-5 | Same as S2 — To-Do is source of truth |
| S4 (Eyes metrics) | Loses exact numbers, keeps narrative positions | One-line snapshot per market (~100w) is the fallback |
| S5 (Memory contacts) | Loses structured fields, keeps tone/style | One-line summary per person (~15w each) is the fallback |
| S6 (Device descriptions) | Loses detailed docs, keeps health table | Wiki article is a text file — survives cold start |
| S7 (current.md projects) | Loses project detail, keeps one-liners | HIGH RISK — test thoroughly before implementing |

**The pattern:** Every sink leaves a self-contained fallback in the organ (snapshot, summary, or pointer). The organ degrades gracefully — it goes from "complete answer" to "correct direction + query hint." A cold-start agent gets the right strategic picture but may need to query DuckDB or read a wiki article for specifics.

---

## DESIGN PRINCIPLE: NARRATIVE STAYS, DATA MOVES

The unifying principle across all sinks:

- **Narrative interpretation** (positions, strategies, tone guidance, procedural knowledge) → STAYS in organs
- **Structured data** (numbers, dates, statuses, lists that grow) → MOVES to DuckDB
- **Reference documentation** (how-to guides, detailed tool docs, methodology writeups) → MOVES to wiki
- **Identity fields** (pronouns, preferred names) → STAYS in organs AND duplicated in DuckDB (non-compressible)

This maps cleanly to the body metaphor: organs hold the intelligence (what to think, how to act), external stores hold the data (what happened, what's pending). The brain doesn't store every memory — it stores the patterns extracted from memories. Same principle.

---

## NEXT STEPS

1. **Karpathy approval** — This document is a proposal. No organ changes without Karpathy sign-off.
2. **Fix MCP database path** — Prerequisite for everything. The MCP server must connect to ps-analytics.duckdb.
3. **Phase 1 pilot** — Populate `decisions` table (S1) as the lowest-risk test. Run brain.md through the standard eval before and after compression. If eval passes, proceed to S2-S4.
4. **Measure** — Track: (a) word savings achieved, (b) eval scores before/after, (c) query latency for SQL hints, (d) cold-start viability (can a fresh agent produce a correct daily brief from compressed organs alone?).
5. **current.md budget** — Propose a word budget for current.md. It's the only ground truth file without a ceiling, and it's the largest file in the system. Suggested: 2,000w (matching Hands/Device).
