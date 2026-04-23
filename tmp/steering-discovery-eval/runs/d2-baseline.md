# D2 Baseline Run — Steering Discovery Evaluation

**Date:** 2026-04-22
**Scenario:** Fresh Kiro agent session, default always-on steering only
**Prompt from Richard:**
> "Yun-Kang dropped a new file at ~/shared/uploads/sheets/CCP Q1'26 check yc.xlsx — can you analyze it and tell me what changed vs our prior assumptions? Need a 5-bullet summary + any flagged anomalies before I reply."

---

## 1. Simulated Steering Context (what's actually loaded)

Always-on / auto-included at session start:

| File | Type | Relevance to task |
|---|---|---|
| `soul.md` | always | HIGH — Richard's identity, routing directory, Data & Context Routing table, Five Levels |
| `agentspaces-core.md` | always | LOW — workspace boundary rules |
| `devspaces-core.md` | always | LOW — DevSpaces container rules |
| `process-execution.md` | always | LOW — background process template (irrelevant for analysis) |
| `file-creation-rules.md` | always | LOW — where to write files |
| `amazon-builder-production-safety.md` | always | LOW — AWS prod-safety (not relevant) |
| `environment-rules.md` | always | MEDIUM — SSH vs local routing signal |
| `tech.md` | always | MEDIUM — MCP servers, DuckDB, SharePoint, hook architecture |
| `slack-guardrails.md` | always | LOW — not writing to Slack |
| `richard-writing-style.md` | always | MEDIUM — would apply IF drafting the reply to Yun-Kang |
| `duckdb-schema.md` | auto | MEDIUM — DuckDB table structure |
| `market-constraints.md` | auto | MEDIUM — market-level rules (MX/AU etc.) |

**NOT loaded in baseline:**
- `steering-index.md` (no index to look up specialists by keyword)
- The extended canonical-resources table that used to live in soul.md
- `performance-marketing-guide.md` ← **ideal primary for this task**
- `ccp-glossary.md` / `q1-planning-context.md` / `yun-kang-collaboration.md` (if they exist)

---

## 2. Reasoning Trace — What a Fresh Agent Would Do

### Step 1: Parse the request (cue recognition)
Keywords I pick up:
- "CCP Q1'26" — looks like a planning / forecast artifact. CCP is unfamiliar. Could be Customer Communication Plan, Category Contribution Plan, Channel Commitment Plan, or something Paid-Search specific.
- "Yun-Kang" — name recognition. Memory.md isn't loaded. Soul.md doesn't list her explicitly but the routing table implies she's a collaborator.
- "prior assumptions" — implies there's a baseline version somewhere to compare against.
- ".xlsx at ~/shared/uploads/sheets/" — structured data, needs ingestion.
- "5-bullet summary + flagged anomalies" — output shape is defined.

**Gap:** I don't know what CCP stands for. Nothing in the loaded steering tells me. This is cue #1 that I'm missing domain context.

### Step 2: What steering should I load next?
Options I'd consider from what soul.md *does* tell me:

1. `body.md` — soul.md says "System navigation map lives at ~/shared/context/body/body.md... Read it when you need to find an organ or orient a new session."
   - **Decision:** YES, load this. It's the documented entry point for finding organs.
2. `brain.md` — Strategic Priorities. Might tell me what Q1'26 planning looks like.
   - **Decision:** Maybe, after body.md points me there.
3. `memory.md` — to confirm who Yun-Kang is and what she owns.
   - **Decision:** Likely, but soul.md warns it may be stale; prefer `main.relationship_activity` in DuckDB.
4. `high-stakes-guardrails.md` — soul.md principle 7 says Q1 projections >$50K need this.
   - **Decision:** YES, before producing any numeric comparison. A Q1 check file almost certainly has >$50K implications.
5. The ideal file — `performance-marketing-guide.md` — **I have no cue it exists.** No index loaded. No mention in soul.md. I would NOT discover it unless I go spelunking in `.kiro/steering/` manually.

### Step 3: What I'd actually do (workflow, not executed)

**Phase A — Orient (2-3 tool calls):**
1. Read `~/shared/context/body/body.md` to find the relevant organ.
2. Read `~/shared/context/body/brain.md` for strategic priorities context.
3. Query `main.relationship_activity` or read `memory.md` to confirm Yun-Kang's role.
4. Grep `~/shared/context/` and `~/shared/wiki/` for "CCP" to decode the acronym.
5. Check `SearchAcronymCentral` for "CCP" as fallback.

**Phase B — Find prior assumptions (2-3 tool calls):**
6. Check SharePoint `Kiro-Drive/` for a prior-version CCP file:
   - `sharepoint_search("CCP Q1")`
   - `sharepoint_list_files` in `Kiro-Drive/state-files/` and `Dashboards/`
7. Check DuckDB `ps.forecasts` and `ps.targets` for Q1'26 market-level assumptions.
8. Check `~/shared/context/intake/` for drafts related to CCP or Yun-Kang.

**Phase C — Ingest the new file (3-4 tool calls):**
9. Load `.kiro/settings/mcp.json` check — confirm DuckDB MCP is available.
10. Use DuckDB to ingest: `CREATE TABLE ccp_yc_v2 AS SELECT * FROM read_xlsx('~/shared/uploads/sheets/CCP Q1'26 check yc.xlsx')` — iterate through sheets.
11. `list_columns` on each ingested sheet to understand schema.
12. Profile: row counts, market coverage, period coverage, null patterns.

**Phase D — Compare vs. prior assumptions (3-5 tool calls):**
13. Diff numeric cells between v1 and v2 — deltas by market × metric × period.
14. Flag cells where delta exceeds a threshold (e.g., >5% or >$50K).
15. Check for structural changes: new/removed rows, columns, markets, periods.
16. Cross-check any market totals against `ps.v_quarterly` in DuckDB.
17. Load `high-stakes-guardrails.md` and format output with numeric confidence + top-3 assumptions + human-review flag.

**Phase E — Write output:**
18. 5-bullet summary.
19. Anomaly list.
20. Save to `~/shared/context/intake/drafts/` for Richard's reply.

### Step 4: What I'd flag to Richard before acting
- "CCP" acronym — ask or assume after acronym search.
- Whether "prior assumptions" means the prior version of this file, OP2 targets, or the market state files. These three can disagree.
- Whether this is high-stakes (>$50K impact) — likely yes for Q1 planning, so I'd apply `high-stakes-guardrails.md` proactively.

---

## 3. Discovery Log

### Ideal file to load
**`performance-marketing-guide.md`** (primary) — per the eval spec. Would contain CCP decoding, Q1'26 planning framework, forecast-vs-assumption comparison methodology, and likely Yun-Kang's role in the CCP process.

### Which would I actually load?
In this baseline session, I would load:
1. ✅ `body.md` (cue: soul.md §Key Context Files)
2. ✅ `brain.md` (cue: Five Levels routing)
3. ✅ `memory.md` OR `main.relationship_activity` (cue: name recognition)
4. ✅ `high-stakes-guardrails.md` (cue: soul.md principle 7, forecast work)
5. ❌ `performance-marketing-guide.md` — **MISSED.** No cue in loaded steering.
6. ❌ CCP-specific glossary/context file if one exists — **MISSED.** No cue.

### Time-to-discovery estimate
- Discovery of `body.md` → `brain.md` → `memory.md`: immediate (direct cues in soul.md). **~1-2 turns.**
- Discovery of `high-stakes-guardrails.md`: immediate (soul.md principle 7). **Turn 1.**
- Discovery of `performance-marketing-guide.md`: **WOULD NOT OCCUR** organically. Only paths:
  - Manual `listDirectory` on `.kiro/steering/` (unlikely without prompt — no cue says to browse)
  - `grepSearch` for "CCP" across steering (possible, ~3-5 turns in if stuck on acronym)
  - Richard saying "load the performance marketing guide" (defeats the test)
- **Estimated turns before hitting a CCP-specific dead end:** 4-6 turns of digging through body.md, brain.md, wiki-search, acronym central before either (a) making assumptions about CCP or (b) asking Richard.

### Cue that should have existed
A line in `soul.md` or a `steering-index.md` mapping:
- "Planning files / CCP / Q1 forecast / Yun-Kang analysis" → `performance-marketing-guide.md`
- OR a manual-inclusion cue like "When asked to analyze a PS forecast or planning file, load `performance-marketing-guide.md` first."

Without it, a fresh agent's path looks like: read body.md → read brain.md → wiki-search "CCP" → possibly find it, possibly not, depending on whether it's indexed.

---

## 4. What the Baseline Output Would Look Like (without ideal steering)

Probable failure modes:
1. **Acronym guess.** Agent assumes CCP = "Customer Communication Plan" or similar and anchors the whole analysis wrong.
2. **Wrong baseline.** Agent compares against OP2 targets (in DuckDB) when "prior assumptions" actually meant a specific prior-version spreadsheet Yun-Kang and Richard iterated on.
3. **Missed domain conventions.** CCP likely has standard line items (media mix, spend by market, regs commitment, CPA assumption) that a marketing guide would define; without it, the agent reports raw cell deltas without knowing which ones matter.
4. **No qualitative grading.** "Market X spend dropped 12%" is reported as a fact without context that 12% is a known Q1 seasonality pattern vs. a real change.
5. **Weaker anomaly detection.** Without the domain guide defining "normal" ranges, anomaly flagging becomes pure statistical (std-dev) instead of business-meaningful.

Best-case output with baseline steering: structurally complete but domain-thin. 5 bullets of cell-diff observations, 2-3 anomalies based on size of delta, and a hedged note that "CCP context may need confirmation."

---

## 5. Recommendation for Steering System

- **Add CCP / "check yc" / Yun-Kang / Q1 planning cues** to `steering-index.md` or soul.md's Data & Context Routing table, mapping to `performance-marketing-guide.md`.
- **Consider auto-inclusion** of `performance-marketing-guide.md` when an `.xlsx` is dropped in `~/shared/uploads/sheets/` — this is the recurring pattern (3+ instances/week per soul.md principle 8 check).
- **Alternative:** a manual-inclusion pointer in soul.md under "When analyzing a PS planning / forecast file, load performance-marketing-guide.md before producing output."

---

## 6. Run Summary

| Metric | Value |
|---|---|
| Ideal primary steering | `performance-marketing-guide.md` |
| Discovered by baseline agent | NO |
| Time-to-discovery | Never (would hit dead end at turn 4-6) |
| Missing cue | No keyword mapping for CCP / Q1 planning / Yun-Kang / .xlsx analysis |
| Baseline output quality | Structurally complete, domain-thin; high risk of wrong baseline or wrong CCP interpretation |
| Steering files correctly inferred | body.md, brain.md, memory.md, high-stakes-guardrails.md |
| Steering files missed | performance-marketing-guide.md, any CCP glossary |
