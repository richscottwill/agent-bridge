# Gut — Digestion, Compression & Waste Removal

*The body eats information constantly — email, calendar, meetings, signals, research. The gut decides what gets absorbed as nutrition (compressed into organs) and what gets expelled as waste (archived, pruned, or discarded). Without it, the body bloats until it can't move.*

*Operating principle: Subtraction before addition. The gut is the only organ whose primary job is removal. Every other organ wants to grow. The gut enforces the constraint that makes the whole system work: a fixed context budget. Information has a half-life. The gut tracks decay and acts on it.*

Last updated: 2026-03-25 (Karpathy — added portable body staleness signal to bloat detection)
Created: 2026-03-20

---

## Purpose

Every other organ adds content. The gut removes content. It enforces the fixed context budget. The body gets smarter without getting bigger.

**Core principles:**
1. **Information has a half-life.** A fact critical on Monday may be noise by Friday. The gut tracks decay and acts on it.
2. **Current-state-only.** Organs hold CURRENT STATE, not history. No append-only logs, streak histories, session logs, scoring logs, or weekly rollups in any organ. changelog.md is the audit trail. archive/ is cold storage. If it grows monotonically, it doesn't belong in an organ.

---

## Three Functions

### 1. Digestion — Process raw material into nutrients
**Input:** `~/shared/context/intake/` (raw files, notes, data drops)
**Output:** Compressed facts routed to the correct organ
**Waste:** The raw file, archived or deleted after extraction

### 2. Compression — Keep organs lean
**Input:** All organ files
**Output:** Tighter versions of the same content
**Waste:** Redundant facts, resolved items, stale predictions

### 3. Excretion — Remove what the body no longer needs
**Input:** Staleness signals, reference counts, completion status
**Output:** Archived or deleted content
**Waste:** Moved to `~/shared/context/archive/` or permanently removed

---

## Digestion Protocol

When new material arrives in `intake/`, the morning routine processes it. The gut adds structure to that processing:

### Intake Triage

For each file in `intake/`:

| Question | If Yes | If No |
|----------|--------|-------|
| Does it contain facts that update an organ? | Extract facts → route to organ | → |
| Does it contain a new decision or position? | Extract → Brain | → |
| Does it contain performance data? | Extract → Eyes | → |
| Does it contain a new task or action? | Extract → Hands | → |
| Does it contain relationship/contact info? | Extract → Memory | → |
| Does it contain a process or delegation? | Extract → Device | → |
| Is the raw file still useful after extraction? | Keep in intake/ with `PROCESSED: [date]` tag | Archive to `archive/` |
| Is it a one-time data dump (CSV, Excel, JSON)? | Extract key findings, archive the raw file | — |

### File Format Rules
| Format | Action |
|--------|--------|
| .md, .txt, .csv | Process directly |
| .json | Process if content, delete if transient |
| .docx | Convert to .md (python-docx), archive original |
| .pdf | Convert to .md (pdfplumber), archive original |
| .xlsx | Process with openpyxl directly (no dedicated script built yet). Extract key findings → route to organ. Archive raw file. |
| .eml | Skip — live email access. Archive. |
| .py | Move to ~/shared/context/tools/ |

### Extraction Rules
- Extract the *minimum viable fact*, not the full context. "AU regs were 1.1K in Feb, -1% vs OP2" is a nutrient. The full WBR callout doc is bulk.
- Every extracted fact must have a source tag: `[source: filename, date]`
- If a fact contradicts an existing organ fact, the newer source wins. Log the contradiction in changelog.md.
- If a fact is ambiguous or unverifiable, tag it `[confidence: LOW]` and route it anyway. The nervous system will catch it during calibration.

### Current Intake Backlog

| File | Status | Action Needed |
|------|--------|--------------|
| WW Dashboard (folder) | Unprocessed | Extract key metrics → Eyes. Archive raw Excel. |

---

## Compression Protocol

Run monthly (or when any organ exceeds its word budget). The goal is to maximize *usefulness per token* — organs should answer their questions accurately and self-containedly within the budget ceiling.

Word budgets are CONSTRAINTS (like a context window), not OBJECTIVES. The gut enforces the ceiling. Experiments optimize for usefulness within that ceiling. An organ at 95% of budget that answers everything correctly is fine — no need to compress further. An organ at 50% of budget that misses questions needs content added, not celebrated for being small.

### Word Budget Enforcement

**STATUS: CE-1 budget rebalancing ADOPTED (Runs 8-9, ratified by Karpathy 3/24). Budgets below are locked baseline.**

| Organ | Budget | Actual | Utilization | Status |
|-------|--------|--------|-------------|--------|
| Memory | 3500w | 2371w | 68% | ✅ |
| Heart | 3500w | 2602w | 74% | ✅ |
| Brain | 2500w | 2090w | 84% | ✅ |
| Eyes | 2500w | 1923w | 77% | ✅ |
| aMCC | 2000w | 2155w | 108% | ⚠️ (within tolerance, post CE-3) |
| Hands | 2000w | 1859w | 93% | ✅ |
| Device | 2000w | 1464w | 73% | ✅ |
| Gut (this file) | 2000w | 1938w | 97% | ✅ |
| Nervous System | 1500w | 1197w | 80% | ✅ |
| Spine | 1500w | 1422w | 95% | ✅ |

**Total body budget:** 23,000w. Hard ceiling: 24,000w.
**Actual body total:** ~19,021w (run 12). Under ceiling by ~4,979w.
**Over-budget organs:** aMCC (108%) — within tolerance. No critical overages.

### Compression Techniques

**1. Resolve and archive completed items**
- Hands: tasks marked DONE for 7+ days → move to a "Recently Completed" summary line, then archive after 14 days
- Brain: decisions with OUTCOME = VALIDATED and no open questions → compress to one-line summary, archive full entry
- Device: delegations with status ACTIVE for 30+ days → compress to one line in a "Completed Delegations" table
- Eyes: predicted QA from past sessions → archive after scoring (nervous system has the scores)

**2. Deduplicate across organs**
- The same fact should live in exactly one organ. If it appears in two, keep it in the organ where it's most actionable and remove from the other.
- Common duplicates to watch:
  - Key people appearing in Memory (relationship graph) AND Spine (quick reference) AND current.md → canonical home is Memory. Others get a pointer: "See Memory."
  - Metrics appearing in Eyes AND Memory (compressed context) → canonical home is Eyes.
  - Task status appearing in Hands AND rw-tracker.md → canonical home is Hands. rw-tracker.md gets the scorecard view only.

**3. Compress resolved patterns**
- Nervous system tracks pattern trajectories. When a pattern reaches RESOLVED status:
  - Remove from rw-tracker.md active patterns table
  - Add one-line entry to nervous-system.md "Resolved Patterns" archive
  - Remove any related trainer callouts from the daily brief template

**4. Age-based decay**
- Facts older than 90 days with no references in the last 30 days → flag for review
- Meeting briefs for meetings that no longer recur → archive
- Competitor data for competitors who haven't appeared in 60 days → compress to one-line historical note
- Relationship graph entries for contacts with no interaction in 60 days → move to a "Dormant Contacts" section (don't delete — they may resurface)

**5. Structural compression**
- Replace verbose paragraphs with tables where possible
- Replace repeated patterns with templates + variables
- Replace full explanations with references to other organs: "See Brain → D1 for rationale"

**6. Protocol compression** (added Run 8, from CE-2)
- Procedural knowledge (how-to protocols, step-by-step instructions) that the agent has internalized after multiple runs can be compressed to 1-2 line summaries
- Keep data tables intact — compress the descriptions around them
- Test: can the agent still execute the protocol correctly from the compressed version? If yes, compress.

---

## Excretion Protocol

What gets removed from the body entirely (archived or deleted).

### Archive Rules (moved to `~/shared/context/archive/`)

| Content Type | Archive After | Condition |
|-------------|--------------|-----------|
| Completed tasks | 14 days | No open dependencies |
| Validated decisions | When compressed to one-liner | Outcome confirmed |
| Old predicted QA | After scoring | Scores in nervous system |
| Resolved patterns | After resolution logged | One-liner stays in NS |
| Processed intake files | After extraction | Facts routed to organs |
| Superseded organ versions | After new version confirmed | Keep one version back |
| Dormant contacts (60+ days) | Move to archive section in Memory | Restore if resurfaces |

### Delete Rules
Only delete content with zero future value: temp MCP/debug files (immediately), exact duplicate intake files, failed experiment .bak files (after confirmed).

### Never Delete
Organ files, changelog.md, Richard's manual files, steering files.

---

## Bloat Detection

The gut runs a bloat check during the heart loop cascade (Phase 2) and flags issues in the daily brief.

### Bloat Signals

| Signal | Threshold | Action |
|--------|-----------|--------|
| Organ over word budget | >110% of budget | Mandatory compression before next content addition |
| Total body over 24K words | Any amount over | Identify largest organ, compress or archive |
| Intake folder > 10 unprocessed files | 10 files | Batch process in next loop run |
| Archive folder > 50 files | 50 files | Review archive, permanently delete transient files |
| Same fact in 3+ organs | Any occurrence | Deduplicate — keep in canonical organ, pointer in others |
| Task in Hands older than 30 days with no status change | 30 days | Either it's blocked (move to Backlog with reason) or it's dead (archive) |
| Predicted question never scored after 7 days | 7 days | Score it or archive it |
| Contact in Memory with no interaction for 90 days | 90 days | Move to Dormant Contacts |
| Portable body organ stale vs source | Any organ modified since last sync | Flag: "🧳 Portable body: [N] organs stale since last sync" |

### Bloat Report (included in daily brief when issues detected)
```
🫁 GUT CHECK: [X] organs over budget. Total body: [X]w / 24,000w ceiling.
- [Organ]: [X]w over → [specific compression action]
- Intake: [X] unprocessed files
- [X] facts duplicated across organs
```

---

## Integration with the Heart Loop

The gut's word budgets are enforced as hard ceilings by the autoresearch loop. Experiments optimize for usefulness per token (accuracy + completeness) within those ceilings. The loop may add content to an organ if it improves accuracy or completeness, as long as the organ stays within budget. The morning routine handles intake processing and bloat detection during daily runs.

---

## Integration with the Morning Routine

Daily brief includes gut check when issues detected (e.g., "🫁 Eyes is 500w over budget," "🫁 3 intake files unprocessed for 5+ days"). On clean days, omit entirely. Silence means health.

---

---

## Governance

**All changes to compression protocols, word budgets, bloat thresholds, and excretion rules in this file are governed by the Karpathy agent** (`~/shared/.kiro/agents/karpathy.md`). The heart loop applies these rules during execution. Karpathy owns the rules themselves — testing new techniques, adjusting budgets, and evolving the compression strategy over time.

## When to Read This File
During heart loop cascade, when an organ feels bloated, when intake/ accumulates, monthly compression review, before adding content to any organ (check budget first).
