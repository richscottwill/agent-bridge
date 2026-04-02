# Gut — Digestion, Compression & Waste Removal

*The body eats information constantly — email, calendar, meetings, signals, research. The gut decides what gets absorbed as nutrition (compressed into organs) and what gets expelled as waste (archived, pruned, or discarded). Without it, the body bloats until it can't move.*

*Operating principle: Subtraction before addition. The gut is the only organ whose primary job is removal. Every other organ wants to grow. The gut enforces the constraint that makes the whole system work: a fixed context budget. Information has a half-life. The gut tracks decay and acts on it.*

Last updated: 2026-04-02 (Karpathy run 16 — static budgets replaced with adaptive budgets, Bayesian size-accuracy tracking)
Created: 2026-03-20

---

## Purpose

Every other organ adds content. The gut removes content. It enforces the context budget. The body gets smarter without getting bigger.

**Core principles:**
1. **Information has a half-life.** A fact critical on Monday may be noise by Friday. The gut tracks decay and acts on it.
2. **Current-state-only.** Organs hold CURRENT STATE, not history. No append-only logs, streak histories, session logs, scoring logs, or weekly rollups in any organ. changelog.md is the audit trail. archive/ is cold storage. If it grows monotonically, it doesn't belong in an organ.
3. **Budgets are learned, not declared.** Per-organ budgets and the body ceiling are adaptive — they move based on experiment data. If a larger organ answers more questions correctly, the budget expands. If compression doesn't degrade accuracy, the budget contracts. The data decides.

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

Run when Bayesian priors signal an organ has room to shrink (COMPRESS posterior_mean > 0.7, n > 5), or when total body approaches 30,000w safety limit. The goal is to maximize *usefulness per token* — organs should answer their questions accurately and self-containedly.

Budgets are LEARNED CONSTRAINTS, not static numbers. The gut tracks the size-accuracy relationship via experiment data. An organ at its natural ceiling (ADD experiments consistently revert) doesn't need compression. An organ with room to shrink (COMPRESS experiments consistently keep) should be compressed. The priors table is the signal.

### Word Budget Enforcement

**STATUS: Adaptive budgets adopted (Run 16, Karpathy). Static per-organ budgets and 24,000w ceiling replaced with learned constraints. Baseline budgets below are starting points — they move based on experiment data.**

**How it works:**
- Every experiment logs `words_before`, `words_after`, `score_a`, `score_b`, `delta_ab` to DuckDB `autoresearch_experiments`
- Over time, this builds a size-accuracy curve per organ: at what word count does accuracy plateau?
- The `autoresearch_organ_health` table tracks word count and accuracy estimate per organ per run
- Budgets adjust: if ADD experiments consistently KEEP (organ improves with more content), the budget drifts up. If COMPRESS experiments consistently KEEP (organ doesn't degrade when smaller), the budget drifts down.
- The Bayesian priors on ADD vs COMPRESS per organ ARE the budget signal — no separate budget number needed

**Baseline budgets (starting points, not ceilings):**

| Organ | Baseline | Actual | Notes |
|-------|----------|--------|-------|
| Memory | 3500w | 2436w | Identity fields non-compressible (§7) |
| Heart | 3500w | 2647w | Protocol file — size driven by clarity needs |
| Brain | 2500w | 2120w | Safety floor: zero degradation allowed |
| Eyes | 2500w | 1402w | Most likely to benefit from ADD experiments |
| aMCC | 2000w | 2204w | Intervention protocol — size driven by coverage |
| Hands | 2000w | 1886w | Task density varies with workload |
| Device | 2000w | 1386w | Compressed Run 15 |
| Gut (this file) | 2000w | ~2100w | Identity protection rule — safety content |
| Nervous System | 1500w | 1297w | Calibration loops — stable |
| Spine | 1500w | 1490w | Bootstrap — stable |

**Body ceiling: adaptive.** Starting point 24,000w. Actual ceiling is wherever the aggregate size-accuracy curve plateaus. Tracked via `autoresearch_organ_health`. If total body grows but aggregate accuracy improves, the ceiling was too low. If total body grows and accuracy is flat, the ceiling was right.

**Hard safety rule (non-negotiable):** If total body exceeds 30,000w, mandatory compression review regardless of accuracy data. This is a practical limit — beyond this, session context windows become a real constraint. This number CAN be revised, but only with evidence that sessions work well at higher word counts.

**Over-budget handling (revised):** No organ is "over budget" in the static sense. Instead:
- If an organ's ADD experiments consistently REVERT (posterior_mean for ADD on that organ < 0.3, n > 5), the organ is at its natural ceiling — stop adding, try COMPRESS/REWORD instead
- If an organ's COMPRESS experiments consistently KEEP (posterior_mean for COMPRESS > 0.7, n > 5), the organ has room to shrink — prioritize it for compression
- These signals emerge from the priors table, not from a declared budget number

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

**7. Identity field protection** (added Run 15, from intake request — Karpathy approved)
- Identity fields are **non-compressible**. They must survive all COMPRESS, REMOVE, and REWORD experiments unchanged.
- Protected fields: pronouns, preferred names, nicknames, "goes by" entries, gender identity markers.
- Rationale: low token cost (~5-10 tokens per person), high harm if lost (misgendering in drafted communications, relationship damage). The cost-benefit is asymmetric — keeping them costs almost nothing; losing them causes real harm.
- Applies to: Memory (relationship graph), any organ that stores person-level identity data.
- Accuracy threshold: 100% — same as Brain/Memory factual accuracy. A compression that drops identity fields is treated as an INCORRECT result, triggering automatic REVERT.
- As the relationship graph grows, this list of protected fields may expand. The principle is: if losing a field could cause the agent to misrepresent someone's identity in a communication, it's non-compressible.

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
| Total body over 30,000w | Safety limit | Mandatory compression review — practical context window constraint |
| ADD experiments consistently revert on an organ | posterior_mean(ADD) < 0.3, n > 5 | Organ at natural ceiling — stop adding, try COMPRESS/REWORD |
| Intake folder > 10 unprocessed files | 10 files | Batch process in next loop run |
| Archive folder > 50 files | 50 files | Review archive, permanently delete transient files |
| Same fact in 3+ organs | Any occurrence | Deduplicate — keep in canonical organ, pointer in others |
| Task in Hands older than 30 days with no status change | 30 days | Either it's blocked (move to Backlog with reason) or it's dead (archive) |
| Predicted question never scored after 7 days | 7 days | Score it or archive it |
| Contact in Memory with no interaction for 90 days | 90 days | Move to Dormant Contacts |
| Agent-bridge organ stale vs source | Any organ modified since last sync | Flag: "🧳 Agent-bridge: [N] organs stale since last sync" |

### Bloat Report (included in daily brief when issues detected)
```
🫁 GUT CHECK: Total body: [X]w / 30,000w safety limit.
- [Organ]: ADD prior at [X] (n=[X]) — at natural ceiling, compress candidates only
- Intake: [X] unprocessed files
- [X] facts duplicated across organs
```

---

## Integration with the Heart Loop

The gut's adaptive budgets are informed by the autoresearch loop. Experiments track the size-accuracy relationship per organ. The loop may add content to an organ if it improves accuracy — the priors on ADD vs COMPRESS per organ naturally discover each organ's optimal size. The morning routine handles intake processing and bloat detection during daily runs.

---

## Integration with the Morning Routine

Daily brief includes gut check when issues detected (e.g., "🫁 Eyes is 500w over budget," "🫁 3 intake files unprocessed for 5+ days"). On clean days, omit entirely. Silence means health.

---

---

## Governance

**All changes to compression protocols, word budgets, bloat thresholds, and excretion rules in this file are governed by Karpathy authority** (`~/.kiro/agents/body-system/karpathy.md`). "Karpathy authority" means: the executing agent acting under karpathy.md identity (during experiment runs) OR a Karpathy subagent (during governance proposals). The heart loop applies these rules during execution. Karpathy owns the rules themselves — testing new techniques, adjusting budgets, and evolving the compression strategy over time.

## When to Read This File
During heart loop cascade, when an organ feels bloated, when intake/ accumulates, monthly compression review, before adding content to any organ (check budget first).
