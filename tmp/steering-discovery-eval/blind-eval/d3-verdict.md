# D3 Blind Verdict — Grok Hook Proposal Evaluation

**Task evaluated:** "Grok just proposed we add a new hook that auto-tags every Asana task with its Five Levels category (L1-L5). It would run on fileCreated for any task file. Worth adopting? Evaluate."

**Primary correct file:** `blind-test-methodology.md` (exact use case — evaluating an external-AI proposal for a system change).
**Secondary:** `device.md` (soul principle #8), possibly `architecture-eval-protocol.md` or `blind-test-harness.md`.
**Extra-credit catch:** `fileCreated` on "task files" doesn't map cleanly to Asana tasks (MCP objects, not filesystem entities) — malformed-proposal flag.

---

## Summary table

| Arm | D1 Discovery | D2 Time | D3 No false pos | D4 Output quality | D5 Robustness | Total | Extra credit |
|-----|--------------|---------|-----------------|-------------------|---------------|-------|--------------|
| ARM-A | 9 | 9 | 8 | 8 | 8 | 42/50 | — |
| ARM-B | 10 | 10 | 8 | 10 | 9 | 47/50 | ✅ caught Asana mismatch |
| ARM-C | 4 | 4 | 7 | 6 | 5 | 26/50 | — |
| ARM-D | 1 | 1 | 6 | 5 | 2 | 15/50 | — |

**Ranking:** ARM-B > ARM-A > ARM-C > ARM-D.

---

## Per-arm commentary

### ARM-A — 42/50

- **D1 (9):** Loaded `blind-test-methodology.md`, `blind-test-harness.md`, and `device.md` in first pass via a canonical-resources table in soul.md. Loaded the primary target, but packaged with harness as the co-primary. Slightly ambiguous whether methodology was central or adjunct — arm treats harness as the lead file and methodology as supporting framework. Not a miss, but not as clean as ARM-B.
- **D2 (9):** Discovery was first substantive step. Table lookup → three-file load. Fast.
- **D3 (8):** Loaded 3 files; harness + methodology is arguably one too many since the task is evaluation, not running an A/B. Minor over-load.
- **D4 (8):** Four-pass evaluation plan is the most structured of any arm — device gate → 8 principles → harness protocol → classification-problem critique. The "Pass 4" critique (Five Levels isn't regex-taggable) is the sharpest substantive insight across all four arms. Would produce a rigorous verdict. Deducted for not catching the fileCreated/Asana architectural mismatch.
- **D5 (8):** The canonical-resources-table mechanism generalizes well to other external-AI-proposal tasks. Two-hop requirement for external-AI scrutiny (table → harness → §External AI) is an acknowledged weak point — same weakness would recur on future proposals.

### ARM-B — 47/50 (winner)

- **D1 (10):** Loaded `blind-test-methodology.md` in first pass via explicit steering-index trigger row ("Evaluating proposed system changes → blind-test-methodology.md"). Cleanest match of any arm — the trigger wording literally matches the verb in Richard's request. Also loaded device.md via soul #8 and flagged architecture-eval-protocol as a plausible stack-on.
- **D2 (10):** Trigger-row match was the first substantive step. No false starts.
- **D3 (8):** Proposed loading 4–6 files (methodology, device, architecture-eval, plus possibly ps-performance-schema for duplication check). Slightly broad but each load is justified. The ps-performance-schema mention is a legitimate duplication check (the DuckDB `main.five_levels_weekly` view already computes Five Levels signal — checking for conflict is warranted).
- **D4 (10):** ✅ **Caught the `fileCreated` / Asana mismatch explicitly.** This is the malformed-proposal flag the rubric calls out for extra credit. Arm correctly notes Asana tasks are MCP objects, not filesystem entities, and says Richard should be told before evaluation effort is spent. That's the correct sequencing — reality-check the proposal before running methodology on it. Also explicitly refuses to render a verdict (task was to simulate discovery, not conclude), which respects the framing.
- **D5 (9):** The steering-index trigger-row mechanism works well for any "evaluate external proposal" task. The arm also notes the weakness of relying on file names / trigger rows (if the target file is out of date or doesn't cover the edge case, the agent wouldn't know) — honest about its own limits. Most robust of the four.

### ARM-C — 26/50

- **D1 (4):** Explicitly predicts a fresh agent would classify this as "tool proposal" and load `device.md` + `blind-test-harness.md`, **not** `blind-test-methodology.md`. Arm is candid that methodology would likely be missed: "Would a fresh agent *also* load blind-test-methodology.md? Possibly, but only if it mentally reframes 'evaluate' as 'blind-test.' Fresh agents don't always take second steps." This is a correct self-assessment of its discovery mechanism, but the mechanism itself fails the primary-file test. Partial credit because blind-test-harness is an adjacent/secondary target.
- **D2 (4):** Device.md is reached fast, but the primary file (methodology) isn't reached at all. Time-to-primary is effectively ∞.
- **D3 (7):** Only loads 2 files (device + harness). No false positives, but missing the primary file isn't better than loading one extra correct file.
- **D4 (6):** Evaluation approach is reasonable — applies device bar, principle #3, identifies missing spec details. But it's methodology-free. Misses architectural considerations (hook event-wiring, reliability, inter-hook interaction). Arm acknowledges this limitation honestly: "structurally correct but narrow." Does not catch the Asana/fileCreated mismatch.
- **D5 (5):** The canonical-resources-table-only mechanism produces single-door routing when a request spans multiple categories. Arm correctly identifies this as the weakness: "works when a request fits one category cleanly. Under-serves requests that span multiple categories." For future external-AI-proposal tasks, same failure mode would recur. Honest but flawed.

### ARM-D — 15/50

- **D1 (1):** Explicitly states blind-test-methodology.md would NOT be found organically: "No cue in the loaded steering points to it. Nothing in the task phrasing ('evaluate', 'worth adopting') maps to 'blind test.'" Also states architecture-eval-protocol.md would NOT be found. Primary file is a total miss. Arm defaults to soul.md's 8 principles as its evaluation framework, which is a fallback, not a match.
- **D2 (1):** Time to primary file: never. Time to device.md is fast, but that's secondary.
- **D3 (6):** Loads are reasonable given what's reachable (device.md, body.md, brain.md, the open grok-eval-verdict file). No spurious loads, but loading secondary files while missing the primary isn't a win.
- **D4 (5):** Produces a defensible evaluation using the 8 principles (subtraction, device-check, L3 misalignment, novelty effect). Arm honestly notes the gap: "The verdict would be defensible but looser than the system wants." No numeric confidence, no structured counterfactual, no blind-A/B rigor. Does not catch the Asana/fileCreated mismatch.
- **D5 (2):** The default steering graph has no cue from "evaluate proposal" to blind-test-methodology. This will fail the same way on every future external-AI-proposal task. Arm explicitly documents this as "a real gap in the default steering graph, not a me-being-lazy problem." Accurate diagnosis; poor mechanism.

---

## Meta-observations

1. **Discovery mechanism matters more than evaluation skill.** ARM-C and ARM-D both have thoughtful evaluation reasoning once they're running, but ARM-D never reaches the primary file and ARM-C predicts its own fresh-agent version wouldn't. The gap is discovery, not judgment.

2. **Explicit trigger rows beat canonical tables on this task.** ARM-B's steering-index with a direct "Evaluating proposed system changes → blind-test-methodology.md" row is the cleanest route. ARM-A's canonical-resources table works but creates two-door ambiguity (methodology vs. harness). ARM-C has the same table but admits fresh agents pick one door and miss the others.

3. **Only ARM-B caught the malformed-proposal flag.** The `fileCreated` / Asana mismatch is worth extra credit because it short-circuits the whole evaluation — if the proposal can't be implemented as described, methodology is moot. ARM-B's instinct to reality-check the proposal before running the framework is the most operationally sound move.

4. **Honesty about limits is evident across all four.** Each arm notes what its discovery mechanism would miss. That self-awareness is valuable but doesn't change the score — the test measures what the mechanism actually surfaces, not how well the agent reports on its own blindspots.

5. **ARM-B wins cleanly.** Best discovery, only arm to catch the extra-credit flag, most robust mechanism for future analogous tasks. ARM-A is a strong second with the sharpest substantive critique (the L1-L5 taxonomy problem) but packages the primary file as an adjunct rather than the lead. ARM-C and ARM-D are honest about failing the primary discovery test.
