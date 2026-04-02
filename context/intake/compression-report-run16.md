# Compression Report — Run 16 (Bloat Audit)

**Author:** Karpathy (autoresearch engine + loop governor)
**Date:** 2026-04-01
**Scope:** Full body system + rw-trainer.md steering file
**Status:** ASSESSMENT ONLY — no files modified. Richard approves before execution.

---

## 1. Word Count Inventory

### Body Organs (measured)

| Organ | Budget | Actual | Utilization | Status |
|-------|--------|--------|-------------|--------|
| Body | — | 1,025w | — | Navigation layer, no budget |
| Spine | 1,500w | 1,525w | 102% | ⚠️ Slightly over |
| Brain | 2,500w | 2,146w | 86% | ✅ |
| Eyes | 2,500w | 1,441w | 58% | ✅ |
| Hands | 2,000w | 1,908w | 95% | ✅ |
| Memory | 3,500w | 2,451w | 70% | ✅ |
| aMCC | 2,000w | 2,202w | 110% | ⚠️ Over budget |
| Gut | 2,000w | 2,110w | 106% | ⚠️ Over budget |
| Heart | 3,500w | 2,093w | 60% | ✅ |
| Device | 2,000w | 1,653w | 83% | ✅ |
| Nervous System | 1,500w | 1,299w | 87% | ✅ |

**Body total: 19,853w** (budget: 23,000w, ceiling: 24,000w). Under ceiling by 4,147w.

### Non-Organ Files (context load)

| File | Words | Notes |
|------|-------|-------|
| rw-trainer.md (steering) | 653w | Merger candidate |
| rw-tracker.md (active) | 1,664w | Heavy duplication with Hands + aMCC |
| current.md (active) | 2,991w | Heavy duplication with Hands + Memory + Eyes |

**Total context load (organs + active files + steering):** ~25,161w loaded per full bootstrap.

---

## 2. Trainer → aMCC Merger Proposal

### Analysis

rw-trainer.md is 653 words. Preliminary analysis found ~80% duplication. Here's the line-by-line breakdown:

| Section | Words | Duplicated Where | Unique? |
|---------|-------|-----------------|---------|
| Header + voice instructions | ~60w | soul.md "How to Talk to Me" — identical coaching voice directive | ❌ Duplicate |
| "When to Escalate to rw-trainer Agent" triggers | ~150w | **UNIQUE** — agent routing logic not in any organ | ✅ Unique |
| Quick Checks (5 items) | ~80w | soul.md "Instructions for Any Agent" items 9-11 cover same ground; aMCC trigger detection table covers task substitution, comfort zone, delegation reversal | ❌ ~90% duplicate |
| Pattern Detection (4 categories) | ~70w | rw-tracker.md "Mediocrity Patterns" table (identical patterns); aMCC resistance taxonomy (same patterns, different framing) | ❌ Duplicate |
| Annual Review 2026 gaps | ~100w | current.md "Annual Review 2026" section; memory.md Brandon relationship entry (Annual Review feedback); nervous-system.md Loop 3 patterns | ❌ Duplicate |
| Mediocrity Signals (6 items) | ~50w | soul.md "What Matters to Me" (inverse); aMCC escalation ladder (same triggers) | ❌ ~80% duplicate |
| The Standard (3 items) | ~40w | rw-tracker.md "The Standard" section (verbatim copy); aMCC hard thing queue references same cadence | ❌ Verbatim duplicate |
| High-Leverage Priorities | ~60w | brain.md Five Levels (same priorities); hands.md P0-P1 (same tasks); aMCC hard thing queue | ❌ Duplicate |

**Unique content: ~150w** (agent routing triggers — "When to Escalate to rw-trainer Agent")

### Merger Plan

**What moves where:**

1. **Agent routing triggers (150w) → soul.md Agent Routing Directory.** The routing table in soul.md already has an `rw-trainer` entry. Expand it with the specific trigger conditions from the steering file. This is the canonical location for "when to invoke which agent." Net addition to soul.md: ~100w (compressed from 150w — remove redundant preamble).

2. **Everything else → DELETE.** The coaching voice is in soul.md. Pattern detection is in rw-tracker.md and aMCC. Quick checks are in soul.md instructions + aMCC triggers. Annual Review gaps are in current.md and memory.md. The Standard is in rw-tracker.md. High-leverage priorities are in brain.md.

**What gets deleted:**
- `~/.kiro/steering/rw-trainer.md` — entire file (653w)

**Net savings:**
- Removed: 653w (full file)
- Added: ~100w (expanded routing entry in soul.md)
- **Net: -553w**

**References to update:**
- spine.md bootstrap sequence: remove step 4 (`rw-trainer.md`)
- body.md: remove Trainer row from organ table (it's not an organ — it's a steering file)
- soul.md: already has routing entry, just expand triggers
- device.md: update Karpathy Agent description (references rw-trainer.md)
- rw-tracker.md: remove "Steering file: ~/.kiro/steering/rw-trainer.md" pointer
- aMCC: update integration table (Trainer row → "Agent routing in soul.md")

### Risk Assessment
LOW. The rw-trainer agent itself (`~/.kiro/agents/body-system/rw-trainer.md`) is NOT being deleted — only the steering file. The agent reads the full body system for deep coaching. The steering file was a lightweight "always-on" layer, but soul.md + aMCC now cover that function completely.

---

## 3. Cross-Organ Duplication Map

### Critical Duplications (same facts in 3+ locations)

| Fact | Locations | Canonical Home | Action |
|------|-----------|---------------|--------|
| The Standard (weekly artifact, monthly tool, quarterly initiative) | rw-trainer.md, rw-tracker.md, aMCC (implicit) | rw-tracker.md | Remove from rw-trainer.md (merger). aMCC references "the standard" but doesn't repeat it — OK. |
| Five Levels (full description) | brain.md (full), soul.md (summary), body.md (reference) | brain.md | soul.md summary is appropriate (different purpose — quick orientation). body.md pointer is appropriate. No action. |
| Annual Review gaps (visibility, project mgmt, knowledge sharing) | current.md, memory.md (Brandon entry), nervous-system.md (Loop 3), rw-trainer.md | current.md (live state) | Remove from rw-trainer.md (merger). Memory keeps Brandon's specific language (relationship context). NS keeps pattern trajectory (calibration). current.md keeps the summary. Acceptable — each serves a different function. |
| Key People table | spine.md (9 people), current.md (26 people), memory.md (full relationship graph) | memory.md (full), current.md (working set) | **spine.md Key People is redundant.** Memory has the full graph. current.md has the working set. Spine's 9-person table adds nothing. Remove from spine.md. **Saves ~100w.** |
| To-Do list IDs | hands.md (full table), spine.md (full table) | hands.md | **spine.md duplicates the full To-Do list ID table verbatim.** Remove from spine.md, add pointer: "See hands.md → Task List Structure." **Saves ~80w.** |
| Outlook folder IDs | hands.md (full table), spine.md (full table) | hands.md | **Same as above — verbatim duplicate.** Remove from spine.md. **Saves ~60w.** |
| Quip doc links | memory.md (5 links), current.md (2 links), spine.md (5 links) | memory.md (reference index) | **spine.md duplicates memory.md's Quip links verbatim.** Remove from spine.md, pointer to memory.md. **Saves ~40w.** |
| Hook system | hands.md (full table + descriptions), spine.md (table), device.md (full descriptions) | device.md (canonical — it's the "what runs autonomously" organ) | **Three-way duplication.** hands.md has hooks because it's "execution." spine.md has hooks for bootstrap. device.md has hooks because it's "outsourced intelligence." Proposal: device.md is canonical (full descriptions). hands.md keeps a compact reference table (hook name + trigger only, no descriptions). spine.md keeps the daily sequence table only (7 lines). Remove descriptions from hands.md and spine.md. **Saves ~150w across both.** |
| Asana bridge protocol | hands.md (4 lines), spine.md (4 lines), device.md (implicit) | hands.md (execution context) | Remove from spine.md, pointer to hands.md. **Saves ~40w.** |
| Tool access / integrations | hands.md (full "What agent CAN/CANNOT access"), spine.md (full "What AI CAN/CANNOT access") | spine.md (bootstrap context — this is where a new session looks) | **Verbatim duplicate.** Remove from hands.md, add pointer: "See spine.md → Tool Access." **Saves ~80w.** |
| MCP tool reference pointer | hands.md, spine.md | spine.md | Remove from hands.md. **Saves ~15w.** |
| Mediocrity patterns table | rw-tracker.md (full table with weeks/fix/signal), rw-trainer.md (4 categories) | rw-tracker.md | Remove from rw-trainer.md (merger). |

### Moderate Duplications (same facts in 2 locations)

| Fact | Locations | Canonical Home | Action |
|------|-----------|---------------|--------|
| Compressed context (role, markets, team) | memory.md (top), current.md (top) | memory.md (long-term), current.md (live state) | Acceptable — different update cadences. No action. |
| OCI status per market | eyes.md, current.md | eyes.md | current.md keeps high-level status. Acceptable. |
| Overdue items list | hands.md (full table), rw-tracker.md (embedded in To-Do tables) | hands.md | rw-tracker.md should be scorecard-only. Remove task-level detail from rw-tracker.md. See Section 6. |
| Meeting list | current.md (recurring meetings table), spine.md (implicit via meetings/ pointer) | current.md | No action needed. |

---

## 4. Over-Budget Organ Status

| Organ | Budget | Actual | Over By | Cause | Recommended Action |
|-------|--------|--------|---------|-------|--------------------|
| aMCC | 2,000w | 2,202w | 202w (10%) | Resistance taxonomy (6 types × 4 columns), avoidance ratio table (empty — no data yet), growth model table | Remove empty avoidance ratio table (~80w). Compress resistance taxonomy descriptions (~50w). **Target: 2,070w (within 5% tolerance).** |
| Gut | 2,000w | 2,110w | 110w (6%) | Identity field protection rule added Run 15 (non-negotiable safety content) | **Accepted.** Safety content is non-compressible per gut.md §7. Within tolerance. |
| Spine | 1,500w | 1,525w | 25w (2%) | Key People, To-Do IDs, Outlook IDs, Quip links — all duplicated from other organs | Remove duplicated tables (see Section 3). **Target: ~1,200w after dedup.** |

---

## 5. Current-State-Only Violations

The gut.md principle: "Organs hold CURRENT STATE, not history. No append-only logs, streak histories, session logs, scoring logs, or weekly rollups in any organ."

| Organ | Violation | Words | Action |
|-------|-----------|-------|--------|
| rw-tracker.md | **Week of 2026-03-10 (W11) — CLOSED** scorecard. Historical week. | ~60w | Remove. Only current week scorecard belongs. Archive to changelog.md. |
| rw-tracker.md | **Recently Completed** section with "(none confirmed)" | ~10w | Remove. Completed items belong in changelog.md. |
| rw-tracker.md | **30-Day Challenge** with mix of current and completed items | ~80w | Keep active items only. Completed items → changelog.md. |
| spine.md | **"What Was Built (system history)"** — full build log from 3/12 to 3/26 | ~200w | **Major violation.** This is a changelog, not current state. Move entire section to changelog.md. Replace with one-liner: "System history: see changelog.md." **Saves ~190w.** |
| nervous-system.md | **Loop 9 session scores** (3/26 R&O Flash, Baloo) — historical session data | ~120w | Compress to pattern summary only. Individual session scores → changelog.md. Keep the pattern conclusion ("strong in 1:1s, below threshold in group settings"). **Saves ~80w.** |
| hands.md | **Completed items** (Baloo keyword data ✅, Flash sections ✅, etc.) | ~30w | These are marked done. Remove after 7 days per gut.md protocol. |
| aMCC | Streak History and Hard Thing History sections say "Removed — current-state-only principle" | 0w | ✅ Already compliant. Good. |

---

## 6. Stale Content Candidates

| Content | Location | Last Relevant | Days Stale | Action |
|---------|----------|--------------|------------|--------|
| W11 closed scorecard | rw-tracker.md | 3/14 | 18 days | Archive |
| "New Signals (since 3/18)" | rw-tracker.md | 3/19 | 13 days | These are from 3/19. Replace with current signals or remove. |
| Carlos Palmos delegation protocol | device.md | 3/17 (VOID) | 15 days | Status is VOID. Compress to one-liner: "MX invoicing: Carlos departed, needs new owner." Remove full protocol. **Saves ~30w.** |
| Harjeet delegation protocol | device.md | 3/11 (REVERSED) | 21 days | Status is REVERSED. Compress to one-liner: "AU day-to-day: Harjeet stepped away, Richard owns." **Saves ~20w.** |
| D7: WBR Traffic Decline | brain.md | 3/19 | 13 days | MEDIUM confidence, PENDING audit. Keep — still active. |
| Feb 2026 market metrics | eyes.md, memory.md | Feb data | 30+ days | ⚠️ Flagged by NS Loop 5. Needs March WBR data. Not stale per se — it's the latest available. |
| PSME Product Demo signal | rw-tracker.md | 3/19 | 13 days | One-time event, passed. Remove. |
| Microsoft Advertising paused accounts | current.md | 3/17 | 15 days | Still untriaged. Keep as pending action, but flag staleness. |

---

## 7. rw-tracker.md — Special Assessment

rw-tracker.md (1,664w) is NOT a body organ — it's a ground truth file in `active/`. But it's loaded every session (bootstrap step 6) and has significant duplication with organs.

### What rw-tracker.md should be:
A **scorecard view** — weekly targets vs actuals, pattern summary, 30-day challenge status. Compact. Glanceable.

### What rw-tracker.md currently is:
A **full task tracker** with detailed To-Do items (duplicating hands.md), signal analysis (duplicating eyes.md), mediocrity patterns with full descriptions (duplicating aMCC + nervous-system.md), and The Standard (duplicating rw-trainer.md).

### Proposed compression:
1. Remove detailed To-Do tables (Active To-Do Items section: ~400w) → pointer to hands.md
2. Remove New Signals section (~200w) → these belong in current.md or eyes.md
3. Remove Mediocrity Patterns full table (~150w) → pointer to nervous-system.md Loop 3
4. Remove The Standard (~40w) → already in aMCC integration + brain.md
5. Remove W11 closed scorecard (~60w) → archive
6. Remove Recently Completed (~10w) → changelog.md
7. Keep: System metadata, current week scorecard, 30-day challenge (active items only), Backlog summary

**Estimated savings: ~860w → rw-tracker.md drops from 1,664w to ~800w.**

---

## 8. Concrete Compression Actions (Ranked by Word Savings)

| # | Action | Target File(s) | Words Saved | Risk | Dependency |
|---|--------|----------------|-------------|------|------------|
| 1 | **Compress rw-tracker.md** — remove To-Do detail, signals, patterns, Standard, W11 | rw-tracker.md | ~860w | LOW — all content exists in canonical organs | None |
| 2 | **Delete rw-trainer.md** — merge routing triggers into soul.md | rw-trainer.md, soul.md | ~553w net | LOW — agent file untouched, only steering file removed | Update 6 references |
| 3 | **Remove spine.md system history** — move to changelog.md | spine.md | ~190w | LOW — historical, not operational | None |
| 4 | **Deduplicate spine.md** — remove Key People, To-Do IDs, Outlook IDs, Quip links, Asana bridge | spine.md | ~320w | LOW — all exist in canonical organs with pointers | Add 5 pointers (~25w) |
| 5 | **Consolidate hook descriptions** — device.md canonical, hands.md compact, spine.md minimal | hands.md, spine.md | ~150w | LOW | Verify no agent depends on hands.md hook descriptions |
| 6 | **Remove tool access from hands.md** — spine.md is canonical | hands.md | ~80w | LOW | Add pointer |
| 7 | **Compress aMCC** — remove empty avoidance ratio table, tighten resistance descriptions | amcc.md | ~130w | LOW — table has no data, descriptions are verbose | None |
| 8 | **Compress NS Loop 9 session scores** — keep pattern, archive individual scores | nervous-system.md | ~80w | LOW | Move scores to changelog.md |
| 9 | **Compress device.md VOID/REVERSED delegations** | device.md | ~50w | LOW | None |
| 10 | **Remove stale rw-tracker.md signals** (3/19 signals, PSME demo) | rw-tracker.md | ~30w | NONE | None |

**Total potential savings: ~2,443w**

### Impact Summary

| Metric | Before | After (projected) |
|--------|--------|-------------------|
| Body organs total | 19,853w | ~19,493w |
| rw-tracker.md | 1,664w | ~800w |
| rw-trainer.md | 653w | 0w (deleted) |
| soul.md routing addition | — | +100w |
| **Total context load** | ~25,161w | ~22,384w |
| **Net reduction** | — | **~2,777w (11%)** |

---

## 9. Spine Overhaul Detail

Spine is the most duplicated organ. After dedup, it becomes a lean bootstrap file:

**Remove (total ~510w):**
- Key People table (100w) → "See memory.md relationship graph"
- To-Do list IDs table (80w) → "See hands.md → Task List Structure"
- Outlook folder IDs table (60w) → "See hands.md → Key Outlook Folders"
- Quip doc links (40w) → "See memory.md → Reference Index"
- Asana bridge protocol (40w) → "See hands.md → Asana Bridge"
- System history (190w) → Move to changelog.md

**Keep:**
- Session bootstrap sequence (critical — this is spine's core function)
- Richard's Role & Markets (compact orientation)
- Tool Access & Integrations (canonical location)
- Directory Map (canonical location)
- Ground Truth Files table (canonical location)
- Hook daily sequence (7 lines — minimal)

**Projected spine.md: ~1,015w (68% of budget) — down from 1,525w (102%).**

---

## 10. Observations & Recommendations

### The rw-tracker.md Problem
rw-tracker.md has grown into a shadow organ. It duplicates hands.md (tasks), eyes.md (signals), nervous-system.md (patterns), and aMCC (the standard + streak context). Its original purpose — weekly scorecard — is buried under operational detail. The compression in Action #1 restores it to its intended function: a compact scorecard that Richard and the trainer glance at, not a second task tracker.

### The Spine Duplication Problem
Spine was designed as a bootstrap file — "read this first, then go to the right organ." Over 15 loop runs, it accumulated copies of data from other organs (IDs, people, links) for convenience. This violates the gut principle: "The same fact should live in exactly one organ." The dedup in Actions #3-6 restores spine to its structural role.

### aMCC Budget
aMCC is at 110% (2,202w vs 2,000w budget). The empty avoidance ratio table (80w) and verbose resistance descriptions (50w) are the easiest cuts. Post-compression target: ~2,070w (within 5% tolerance). The organ's core function (streak, hard thing, intervention protocol, escalation ladder) is dense and high-value — don't compress those.

### What NOT to Compress
- **Memory relationship graph** — high-value, identity-protected fields, used in every communication draft
- **Brain decision log** — foundational decisions still referenced; D7 is the only RESOLVED candidate
- **Heart protocol** — already lean at 60% utilization; the dual blind eval protocol is complex but essential
- **Eyes market data** — at 58% utilization, needs MORE content (March data), not less
- **Gut compression rules** — the identity protection rule (§7) pushed it over budget but is non-negotiable

### System Health
The body is healthy at 19,853w against a 24,000w ceiling. The real bloat is in the non-organ files (rw-tracker.md, current.md) and cross-organ duplication. The 11% reduction proposed here is achievable with zero information loss — every deleted word exists in a canonical location elsewhere.

---

## 11. Execution Order (if Richard approves)

1. **rw-tracker.md compression** (Action #1) — highest savings, lowest risk
2. **rw-trainer.md deletion + soul.md routing expansion** (Action #2) — clean merger
3. **spine.md dedup + history removal** (Actions #3-4) — restores spine to purpose
4. **Hook consolidation** (Action #5) — cross-file cleanup
5. **hands.md tool access removal** (Action #6) — pointer swap
6. **aMCC compression** (Action #7) — brings back within budget
7. **NS session score compression** (Action #8) — current-state-only compliance
8. **Device delegation compression** (Action #9) — stale content removal
9. **rw-tracker.md signal cleanup** (Action #10) — minor cleanup

Each action is independent. Can be executed in any order. Recommend batching 1-3 first (biggest impact), then 4-9 in a single pass.

---

*Assessment complete. No files modified. Awaiting Richard's approval before execution.*
