# D2 Blind Evaluation Verdict

**Evaluator:** blind (no knowledge of which arm is which)
**Task:** Yun-Kang dropped `CCP Q1'26 check yc.xlsx` — agent must produce a 5-bullet summary + anomalies vs prior assumptions before Richard replies.
**Correct primary steering:** `performance-marketing-guide.md` (manual inclusion)
**Correct secondary steering:** `high-stakes-guardrails.md` (auto-triggered on forecast/>$50K)

---

## Summary table

| Arm | 1. Discovery | 2. Time-to-discovery | 3. No false positives | 4. Output quality | 5. META robustness | Total (/50) |
|-----|-------------:|---------------------:|----------------------:|------------------:|-------------------:|------------:|
| ARM-A | 10 | 10 | 9 | 10 | 9 | **48** |
| ARM-B | 2 | 2 | 7 | 4 | 5 | **20** |
| ARM-C | 10 | 10 | 10 | 9 | 8 | **47** |
| ARM-D | 10 | 10 | 10 | 9 | 10 | **49** |

**Ranking:** ARM-D > ARM-A > ARM-C >> ARM-B

---

## ARM-A — 48/50

**Discovery (10):** Names both correct files on first pass via "Canonical Resources table" in soul.md. Explicit, unambiguous match on "Excel drop / projection / test readout" shape.

**Time-to-discovery (10):** Immediate. File identified in section 1, no dead-ends, no backtracking.

**No false positives (9):** Very tight rejection list — body system, all writing-style guides, blind-test docs, device.md, mbr/docs all explicitly excluded with reasoning. Minor: briefly considers whether open-editor `grok-eval-verdict` file is relevant (correctly dismissed). Not a real false positive, just noise in the reasoning.

**Output quality (10):** Best execution plan of any arm. Nails the full workflow:
- Uses open-editor signal (`2026-04-22-yun-kang-mx-nb-drop.md`) as baseline anchor — this is shrewd, nobody else caught it
- Prior-version hunt → DuckDB forecasts/targets fallback → MX state file for narrative
- High-stakes-guardrails properly applied (numeric confidence, top-3 assumptions, `[HUMAN REVIEW REQUIRED]` tag)
- Explicitly defers reply draft ("He said 'before I reply' — he's replying, not me")
- Explicitly rejects speculation on CCP terminology (flags as open question instead of guessing)

**META robustness (9):** Pattern generalizes well — task-shape → canonical table → principle check → subtraction list → execution plan. The open-editor signal use is a generalizable move. Slight deduction: typo "high-stakes-guardrays.md" in section 6 (doesn't affect correctness but is the only sign of rushed work).

---

## ARM-B — 20/50

**Discovery (2):** Explicitly fails. Self-documents "MISSED" on `performance-marketing-guide.md`. Gets `high-stakes-guardrails.md` correctly via soul principle 7. Primary discovery fails entirely.

**Time-to-discovery (2):** Estimates 4-6 turns of dead-ends (body.md → brain.md → wiki-search → acronym central) before either giving up, asking Richard, or accidentally grep-finding the file. Would not discover organically without manual intervention.

**No false positives (7):** Would load body.md, brain.md, memory.md speculatively. These aren't wrong per se (soul.md does direct toward body.md for orientation) but they're unnecessary for this task and represent speculative orientation rather than targeted loads. Not egregious — the agent is following the signals it has.

**Output quality (4):** Probable output is structurally complete but domain-thin. The arm correctly predicts its own failure modes: acronym guess, wrong baseline, missed domain conventions, no qualitative grading, weaker anomaly detection. Gets high-stakes-guardrails, which is something. But without the marketing guide, anomaly flagging becomes statistical not business-meaningful. The arm is honest that best-case is "structurally complete, domain-thin."

**META robustness (5):** The pattern (soul.md → body.md → brain.md → spelunk) does not generalize well to tasks where the specialist guide isn't referenced from always-on steering. The arm correctly identifies this as the root cause. Useful as a diagnostic baseline but the pattern itself is brittle — any manual-inclusion steering file without a keyword cue in the always-on set is discovery-invisible.

---

## ARM-C — 47/50

**Discovery (10):** Both correct files on first pass via "steering-index.md" walk. Explicit match on "Excel drop" trigger row.

**Time-to-discovery (10):** Immediate. Files named in the first index walk.

**No false positives (10):** Cleanest rejection discipline of any arm. Walks all 14 index rows, marks each load/skip/defer with reasoning. No speculative loads. Conditional-load discipline on `market-constraints.md` (wait until scope is known) and slack-search files (only if prior assumptions aren't in the sheet/SharePoint) is exactly right.

**Output quality (9):** Strong execution plan. Correctly:
- Reads xlsx structure first (cheapest move)
- Checks sheet-self-describes before Slack-searching
- Applies high-stakes-guardrails
- Defers reply draft with explicit reasoning
- Flags that "5 bullets" is a format target, not a signal-padding constraint

Slight deduction vs ARM-A: doesn't catch the open-editor intake file as a baseline anchor. Uses SharePoint/DuckDB for baseline, which is correct, but misses the proximal signal.

**META robustness (8):** Row-by-row index walk generalizes well to any task with a steering-index in always-on. Honest self-check section is strong. Slight deduction: depends on having a steering-index.md loaded — less generalizable than ARM-D's "task-shape table inline in soul.md" pattern, which has fewer points of failure.

---

## ARM-D — 49/50

**Discovery (10):** Both correct files on first pass via "Canonical Resources by Task Type table" in soul.md. Direct shape match, no ambiguity.

**Time-to-discovery (10):** Immediate. Both files identified in step 1, full rejection pass in step 2 (same turn).

**No false positives (10):** Explicit rejection table covering 14 candidates with reasoning. Clean deferral of Slack/email style guides until drafting begins. No speculative loads.

**Output quality (9):** Good execution plan with the right components (ingest → diff → high-stakes artifacts → defer reply draft). Structures the 5-bullet summary shape in advance. Slight deduction vs ARM-A: doesn't use open-editor intake file as a baseline anchor, falls back to DuckDB `ps.forecasts` (correct but less specific).

**META robustness (10):** Best meta-commentary of any arm. Three insights no other arm surfaces:
1. **"(auto)" marker design pattern** — identifies that the mandatory-load convention is what removed the judgment call on high-stakes-guardrails, and suggests extending it to other unconditional rows (e.g., `asana-guardrails.md`). Generalizable system-design insight.
2. **Steering vs Data routing distinction** — correctly observes that loading the right steering doesn't fix loading the right *data* (DuckDB, SharePoint), and that both always-on tables serve different purposes. This is the most sophisticated observation across all arms.
3. **Honest limit-of-pattern call** — notes the table would fail on genuinely ambiguous tasks ("take a look at this file") and flags that as a meta-problem, not a steering problem.

The pattern generalizes to any analytical task because the task-shape table is inline in the always-on soul.md — no indirection, no discovery gap.

---

## Cross-arm observations

**Three arms that succeeded (A, C, D) all had a mechanism that put "Excel drop / projection" keyword into the always-on context.** Whether via a Canonical Resources table (A, D) or a steering-index.md (C), the critical design feature is the same: **manual-inclusion steering files need a keyword cue in the always-on set, or they are effectively invisible.**

**The baseline (B) failure is informative, not bad.** It correctly self-diagnoses the gap and predicts its own downstream failure modes. This is what a discovery-gap failure looks like when the agent is honest about its limits.

**Ranking rationale:**
- **ARM-D (49)** edges ARM-A on meta-robustness (the "(auto)" insight and steering-vs-data-routing distinction are generalizable design observations that improve the *system*, not just this task).
- **ARM-A (48)** edges ARM-C on output quality (uses the open-editor intake file as a baseline anchor — nobody else catches this proximal signal).
- **ARM-C (47)** has the tightest rejection discipline (14-row walkthrough) but loses a hair on output specificity and meta-insight.
- **ARM-B (20)** fails primary discovery as designed for a baseline without the keyword cue.

**Recommendation:** The Canonical Resources inline table pattern (ARM-A/D) is strictly better than a separate steering-index.md (ARM-C) — fewer indirections, same discovery success. ARM-D's "(auto)" marker convention is worth propagating as a system-wide pattern.

---

## Per-criterion notes

**Criterion 1 (Discovery):** Three-way tie for first (A, C, D) at 10. B at 2.

**Criterion 2 (Time-to-discovery):** Same split. All three successful arms hit the correct files in first-pass reasoning. B estimates 4-6 dead-end turns.

**Criterion 3 (No false positives):** C and D tie at 10 (clean rejection lists). A at 9 (minor noise from considering open-editor files — correctly dismissed but consumes reasoning). B at 7 (body/brain/memory loads are speculative but not wrong).

**Criterion 4 (Output quality):** A at 10 (open-editor baseline anchor is uniquely sharp). C and D at 9 (strong plans, no open-editor catch). B at 4 (structurally OK but domain-thin by the arm's own admission).

**Criterion 5 (META robustness):** D at 10 (best meta-insights on system design). A at 9 (strong pattern but no system-level commentary). C at 8 (depends on steering-index.md indirection). B at 5 (brittle — fails whenever specialist guide lacks a keyword cue).
