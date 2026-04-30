<!-- DOC-0223 | duck_id: organ-gut -->


#### preamble — Details


**Example:** This section demonstrates the pattern in practice


# Gut — Digestion, Compression & Waste Removal

*The body eats information constantly
Example: The body eats information constantly

*Operating principle: Subtraction before addition. The gut is the only organ whose primary job is removal. Every other organ wants to grow. The gut enforces the constraint that makes the whole system work: a fixed context budget. Information has a half-life. The gut tracks decay and acts on it.*

Last updated: 2026-04-02 (Karpathy run 16
Created: 2026-03-20

---


[38;5;10m> [0m## Gut Functions & Protocols[0m[0m
[0m[0m
The gut has three functions
### Identity Field Protection (§7)

Non-compressible identity fields get their own subsection to emphasize their special status.


#### Rule
- Identity fields are **non-compressible**. They must survive all COMPRESS, REMOVE, and REWORD experiments unchanged.
- Protected fields: pronouns, preferred names, nicknames, "goes by" entries, gender identity markers.
- Accuracy threshold: 100%
- Applies to: Memory, any organ that stores person-level identity data.

#### Continued


#### Rationale
- Low token cost, high harm if lost. The cost-benefit is asymmetric
- As the relationship graph grows, this list of protected fields may expand. The principle is: if losing a field could cause the agent to misrepresent someone's identity in a communication, it's non-compressible.

---

**Key consideration:** This section's content is critical for accurate operation. Cross-reference with related sections for full context.
### Archive Rules (moved to `~/shared/wiki/archive/`)

**Frequent:**
| Content Type | Archive After | Condition |
|-------------|--------------|-----------|
| Processed intake files | After extraction | Facts routed to organs |
| Completed tasks | 14 days | No open dependencies |
| Old predicted QA | After scoring | Scores in nervous system |

**Periodic:**
| Content Type | Archive After | Condition |
|-------------|--------------|-----------|
| Validated decisions | When compressed to one-liner | Outcome confirmed |
| Resolved patterns | After resolution logged | One-liner stays in NS |
| Dormant contacts (60+ days) | Move to archive section in Memory | Restore if resurfaces |
| Superseded organ versions | After new version confirmed | Keep one version back |

**Delete**: temp MCP/debug files, exact duplicate intake files, failed .bak files. **Never delete:** organ files, changelog.md, Richard's manual files, steering files.

---


The gut runs a bloat check during the heart loop cascade (Phase 2) and flags issues in the daily brief.


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


### Current Intake Backlog

| File | Status | Action Needed |
|------|--------|--------------|
| WW Dashboard (folder) | Unprocessed | Extract key metrics → Eyes. Archive raw Excel. |

---

**Key consideration:** This section's content is critical for accurate operation. Cross-reference with related sections for full context.
### Compression Protocol

Run when Bayesian priors signal an organ has room to shrink. The goal is to maximize *usefulness per token*




Organs hold CURRENT STATE, not history. No append-only logs, streak histories, session logs, scoring logs, or weekly rollups in any organ. changelog.md is the audit trail. archive/ is cold storage. If it grows monotonically, it doesn't belong in an organ.


### Worked Example

Eyes hits 1400w while accuracy stays at 0.95. ADD prior drops to 0.28 (n=7). Gut flags: "Eyes at ceiling

---


### Core Principle 1: Information Half-Life
A fact critical on Monday may be noise by Friday. The gut tracks decay and acts on it. Example: a competitor's impression share from 60 days ago gets compressed to a one-liner.


### Core Principle 3: Learned Budgets
Per-organ budgets and the body ceiling are adaptive

---

*Example:* When this applies, the expected outcome is verified by checking the result.
#### Core Principle 3: Learned Budgets — Details


### Compression Techniques

| # | Technique | Rule | Example |
|---|-----------|------|---------|
| 1 | Resolve completed | DONE→summary (7d), archive (14d). VALIDATED→one-liner. | "MX invoice handoff to Carlos: DONE 3/17" → archive after 3/31 |
| 2 | Deduplicate | One fact, one organ. People→Memory, metrics→Eyes, tasks→Hands. | AU CPA in both Eyes and Memory → keep in Eyes, pointer in Memory |
| 3 | Compress resolved | RESOLVED patterns→one-liner, strip trainer callouts. | "Admin displacement (3wk STUCK → structural fix applied)" → one-liner in NS |
| 4 | Age decay | 90d no-ref→flag. 60d competitors→one-liner. 90d contacts→Dormant. | Competitor last seen 60d ago → "weareuncapped.com: UK, 24% IS (inactive)" |
| 5 | Structural | Paragraphs→tables, patterns→templates, explanations→cross-refs. | 3-paragraph delegation description → one row in delegation table |
| 6 | Protocol | Internalized procedures→1-2 line summaries. Preserve data tables. | Full bootstrap walkthrough → "Read spine.md → body.md → soul.md" |
| 7 | Identity protection | **Non-compressible.** Pronouns, names, gender. 100% accuracy. See §7. | Brandon's she/her pronouns survive ALL compression passes unchanged |
| 8 | REMOVE pre-check | Unique IDs/URLs/rules/formulas? → REWORD/COMPRESS, not REMOVE. (7/7 reverted.) | MCC ID 873-788-1095 exists only in Eyes → cannot REMOVE, only REWORD |
| 9 | Cross-organ pointers | Same fact in 3+ organs → keep in canonical organ, replace others with pointer. Canonical: metrics→Eyes, people→Memory, tasks→Hands, decisions→Brain. | AU CPA in Eyes + Memory + Hands → keep in Eyes, pointer `(see Eyes)` in others |


[38;5;10m> [0m### Bloat Report (included in daily brief when issues detected)[0m[0m
[0m[0m
🫁 GUT CHECK: Total memory size: [X] words.[0m[0m
- [Organ name]: grew beyond expected size — was [X] words on average (over [X] samples)[0m[0m
- Inbox backlog: [X] files waiting to be processed[0m[0m
- [X] facts appear in more than one organ (candidates for dedup)[0m[0m
## When to Read This File
- Heart loop cascade
- Any organ feels bloated or over-budget
- `intake/` has 10+ unprocessed files
- Monthly compression review
- Before ADD to any organ

### Intake Triage

For each file in `intake/`: extract minimum viable facts, route to the organ where they're most actionable (decisions → Brain, metrics → Eyes, tasks → Hands, people → Memory, processes → Device). Tag source and date. Archive raw file after extraction unless still useful.

*Example:* When this applies, the expected outcome is verified by checking the result.
### Extraction Rules
- Extract the *minimum viable fact*
- Source tag every fact: `[source: filename, date]`
- Contradiction between sources: newer source wins. Log in changelog.md.
- Ambiguous/unverifiable facts: tag `[confidence: LOW]`, route anyway. Nervous system catches it in calibration.
- Worked example: Raw intake "AU Feb WBR shows 1.1K regs, CPA $118, -1% vs OP2, NB CPA down 29% from 6wk ago" → Extract: "AU Feb: 1.1K regs, CPA $118 (-1% OP2). NB CPA -29% 6wk. [source: WBR-Feb, 2026-03-05]" → Route to Eyes.


## Governance & Daily Brief Integration

**Karpathy authority** governs all changes to compression protocols, word budgets, bloat thresholds, and excretion rules in this file. "Karpathy authority" = the Karpathy CLI agent running experiment batches, or any agent acting under `~/.kiro/agents/body-system/karpathy.md` identity during governance proposals. Heart loop executes; Karpathy owns the rules

**Daily brief integration:** Gut check included when issues detected (e.g., "🫁 Eyes is 500w over budget," "🫁 3 intake files unprocessed for 5+ days"). On clean days, omit entirely. Silence means health.


### Budget Model & Baselines

Budgets are LEARNED CONSTRAINTS, not static numbers. Every experiment logs `words_before`, `words_after`, `score_a`, `score_b`, `delta_ab` to DuckDB `autoresearch_experiments`. Over time, this builds a size-accuracy curve per organ. The `autoresearch_organ_health` table tracks word count and accuracy estimate per organ per run. The Bayesian priors on ADD vs COMPRESS per organ ARE the budget signal

**Body ceiling: adaptive.** Starting point 24,000w. Actual ceiling = aggregate size-accuracy plateau in `autoresearch_organ_health`. No hard cap


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

## Purpose

Every other organ adds content. The gut removes it. It enforces the context budget so the body gets smarter without getting bigger.


## Excretion Protocol

What gets removed from the body entirely.


#### Part 2


**Example:** This section demonstrates the pattern in practice


#### Part 3

