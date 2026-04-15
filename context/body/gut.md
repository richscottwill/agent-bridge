<!-- DOC-0223 | duck_id: organ-gut -->
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

| Function | Input | Output | Waste | Example |
|----------|-------|--------|-------|---------|
| **Digestion** — raw→nutrients | `~/shared/context/intake/` (raw files, notes, data drops) | Compressed facts routed to correct organ | Raw file, archived/deleted after extraction | WBR xlsx → extract "AU Feb: 1.1K regs, CPA $118" → Eyes → archive xlsx |
| **Compression** — keep organs lean | All organ files | Tighter versions of same content | Redundant facts, resolved items, stale predictions | Memory has AU CPA in relationship graph + key metrics → deduplicate, keep in Eyes, pointer in Memory |
| **Excretion** — remove unneeded | Staleness signals, reference counts, completion status | Archived or deleted content | Moved to `~/shared/wiki/archive/` or permanently removed | Completed "MX invoice handoff" with no open deps after 14d → archive |

---

## Digestion Protocol

When new material arrives in `intake/`, the AM-2 hook processes it. The gut adds structure to that processing:

### Intake Triage

For each file in `intake/`: extract minimum viable facts, route to the organ where they're most actionable (decisions → Brain, metrics → Eyes, tasks → Hands, people → Memory, processes → Device). Tag source and date. Archive raw file after extraction unless still useful.

### File Format Rules
| Format | Action |
|--------|--------|
| .md, .txt, .csv | Process directly |
| .json | Process if content, delete if transient |
| .docx | Convert to .md (python-docx), archive original |
| .pdf | Convert to .md (pdfplumber), archive original |
| .xlsx | Process with openpyxl directly (no dedicated script built yet). Extract key findings → route to organ. Archive raw file. |
| .eml | Skip — live email access. Archive. |
| .py | Move to ~/shared/tools/ |

### Extraction Rules
- Extract the *minimum viable fact*, not the full context. Bad: paste entire WBR callout doc. Good: "AU regs 1.1K Feb, -1% vs OP2" → route to Eyes.
- Source tag every fact: `[source: filename, date]`
- Contradiction: newer source wins. Log in changelog.md.
- Ambiguous/unverifiable: tag `[confidence: LOW]`, route anyway. Nervous system catches it in calibration.
- Worked example: Raw intake "AU Feb WBR shows 1.1K regs, CPA $118, -1% vs OP2, NB CPA down 29% from 6wk ago" → Extract: "AU Feb: 1.1K regs, CPA $118 (-1% OP2). NB CPA -29% 6wk. [source: WBR-Feb, 2026-03-05]" → Route to Eyes.

### Current Intake Backlog

| File | Status | Action Needed |
|------|--------|--------------|
| WW Dashboard (folder) | Unprocessed | Extract key metrics → Eyes. Archive raw Excel. |

---

## Compression Protocol

Run when Bayesian priors signal an organ has room to shrink (COMPRESS posterior_mean > 0.7, n > 5). The goal is to maximize *usefulness per token* — organs should answer their questions accurately and self-containedly.

Budgets are LEARNED CONSTRAINTS, not static numbers. Every experiment logs `words_before`, `words_after`, `score_a`, `score_b`, `delta_ab` to DuckDB `autoresearch_experiments`. Over time, this builds a size-accuracy curve per organ. The `autoresearch_organ_health` table tracks word count and accuracy estimate per organ per run. The Bayesian priors on ADD vs COMPRESS per organ ARE the budget signal — no separate budget number needed. ADD consistently KEEP = budget drifts up. COMPRESS consistently KEEP = budget drifts down. ADD consistently REVERT (posterior_mean < 0.3, n > 5) = organ at natural ceiling. COMPRESS consistently KEEP (posterior_mean > 0.7, n > 5) = prioritize for compression.

**Body ceiling: adaptive.** Starting point 24,000w. Actual ceiling = aggregate size-accuracy plateau in `autoresearch_organ_health`. No hard cap — the data decides.

### Baseline Budgets (starting points, not ceilings)

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

### Compression Techniques

| # | Technique | Rule | Example |
|---|-----------|------|---------|
| 1 | Resolve completed | DONE→summary (7d), archive (14d). VALIDATED→one-liner. | "MX invoice handoff to Carlos — DONE 3/17" → archive after 3/31 |
| 2 | Deduplicate | One fact, one organ. People→Memory, metrics→Eyes, tasks→Hands. | AU CPA in both Eyes and Memory → keep in Eyes, pointer in Memory |
| 3 | Compress resolved | RESOLVED patterns→one-liner, strip trainer callouts. | "Admin displacement (3wk STUCK → structural fix applied)" → one-liner in NS |
| 4 | Age decay | 90d no-ref→flag. 60d competitors→one-liner. 90d contacts→Dormant. | Competitor last seen 60d ago → "weareuncapped.com: UK, 24% IS (inactive)" |
| 5 | Structural | Paragraphs→tables, patterns→templates, explanations→cross-refs. | 3-paragraph delegation description → one row in delegation table |
| 6 | Protocol | Internalized procedures→1-2 line summaries. Preserve data tables. | Full bootstrap walkthrough → "Read spine.md → body.md → soul.md" |
| 7 | Identity protection | **Non-compressible.** Pronouns, names, gender. 100% accuracy. See §7. | Brandon's she/her pronouns survive ALL compression passes unchanged |
| 8 | REMOVE pre-check | Unique IDs/URLs/rules/formulas? → REWORD/COMPRESS, not REMOVE. (7/7 reverted.) | MCC ID 873-788-1095 exists only in Eyes → cannot REMOVE, only REWORD |
| 9 | Cross-organ pointers | Same fact in 3+ organs → keep in canonical organ, replace others with pointer. Canonical: metrics→Eyes, people→Memory, tasks→Hands, decisions→Brain. | AU CPA in Eyes + Memory + Hands → keep in Eyes, pointer `(see Eyes)` in others |

**7. Identity field protection** (added Run 15, from intake request — Karpathy approved)

#### Rule
- Identity fields are **non-compressible**. They must survive all COMPRESS, REMOVE, and REWORD experiments unchanged.
- Protected fields: pronouns, preferred names, nicknames, "goes by" entries, gender identity markers.
- Accuracy threshold: 100% — same as Brain/Memory factual accuracy. A compression that drops identity fields is treated as an INCORRECT result, triggering automatic REVERT.
- Applies to: Memory (relationship graph), any organ that stores person-level identity data.

#### Rationale
- Low token cost (~5-10 tokens per person), high harm if lost (misgendering in drafted communications, relationship damage). The cost-benefit is asymmetric — keeping them costs almost nothing; losing them causes real harm.
- As the relationship graph grows, this list of protected fields may expand. The principle is: if losing a field could cause the agent to misrepresent someone's identity in a communication, it's non-compressible.

---

## Excretion Protocol

What gets removed from the body entirely (archived or deleted).

### Archive Rules (moved to `~/shared/wiki/archive/`)

| Content Type | Archive After | Condition |
|-------------|--------------|-----------|
| Completed tasks | 14 days | No open dependencies |
| Validated decisions | When compressed to one-liner | Outcome confirmed |
| Old predicted QA | After scoring | Scores in nervous system |
| Resolved patterns | After resolution logged | One-liner stays in NS |
| Processed intake files | After extraction | Facts routed to organs |
| Superseded organ versions | After new version confirmed | Keep one version back |
| Dormant contacts (60+ days) | Move to archive section in Memory | Restore if resurfaces |

**Delete** (zero future value only): temp MCP/debug files, exact duplicate intake files, failed .bak files. **Never delete:** organ files, changelog.md, Richard's manual files, steering files.

---

## Bloat Detection

The gut runs a bloat check during the heart loop cascade (Phase 2) and flags issues in the daily brief.

### Bloat Signals

| Signal | Threshold | Action |
|--------|-----------|--------|
| Body word count ↑ while accuracy flat/↓ | `autoresearch_organ_health` trend | Compression review — body past useful size |
| ADD reverts consistently on organ | posterior_mean(ADD) < 0.3, n > 5 | Organ at ceiling — COMPRESS/REWORD only |
| Intake backlog | > 10 unprocessed files | Batch process next loop |
| Archive bloat | > 50 files | Review, delete transient |
| Cross-organ duplication | Same fact in 3+ organs | Deduplicate → canonical organ + pointers |
| Stale task in Hands | > 30 days, no status change | Backlog (if blocked) or archive (if dead) |
| Unscored prediction | > 7 days | Score or archive |
| Dormant contact in Memory | > 90 days no interaction | Move to Dormant |
| Agent-bridge stale | Any organ modified since last sync | Flag: "🧳 Agent-bridge: [N] organs stale" |
| DuckDB table size | > 500 rows | Archive old → parquet, keep last 100 active |

### Bloat Report (included in daily brief when issues detected)
```
🫁 GUT CHECK: Total body: [X]w.
- [Organ]: ADD prior at [X] (n=[X]) — at natural ceiling, compress candidates only
- Intake: [X] unprocessed files
- [X] facts duplicated across organs
```

---

## Integration with the Heart Loop

The gut's adaptive budgets are informed by the autoresearch loop. Experiments track the size-accuracy relationship per organ. The loop may add content to an organ if it improves accuracy — the priors on ADD vs COMPRESS per organ naturally discover each organ's optimal size. The AM hooks handle intake processing and bloat detection during daily runs.

---

## Integration with AM-3 Brief

Daily brief includes gut check when issues detected (e.g., "🫁 Eyes is 500w over budget," "🫁 3 intake files unprocessed for 5+ days"). On clean days, omit entirely. Silence means health.

---

---

## Governance

**All changes to compression protocols, word budgets, bloat thresholds, and excretion rules in this file are governed by Karpathy authority** (`~/.kiro/agents/body-system/karpathy.md`). "Karpathy authority" means: the Karpathy CLI agent (`karpathy.json`) running experiment batches, or any agent acting under karpathy.md identity during governance proposals. The heart loop applies these rules during execution. Karpathy owns the rules themselves — testing new techniques, adjusting budgets, and evolving the compression strategy over time. Karpathy authority also extends to style guide experiments and output-quality evals — any experiment that modifies style guides, market context files, callout principles, or hook prompts falls under the same governance as organ compression experiments.

## When to Read This File
During heart loop cascade, when an organ feels bloated, when intake/ accumulates, monthly compression review, before adding content to any organ (check budget first).
