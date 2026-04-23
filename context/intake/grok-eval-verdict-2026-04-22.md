# Grok 6-File Steering Upgrade — Blind A/B Verdict

**Date:** 2026-04-22
**Protocol:** architecture-eval-protocol.md
**Method:** 6 proposed files × 2 representative inputs × (control + treatment + blind evaluator) = 36 sub-agent invocations
**Randomization:** seeded (numpy seed 42); 7 pairs had control=X, 5 had treatment=X (prevents positional bias)
**Blind evaluator:** fresh `general-task-execution` sub-agent per pair; saw only two labeled outputs ("ARM-X", "ARM-Y"), no knowledge of which file was proposed or which arm was control vs. treatment

---

## Headline

**9 of 12 blind comparisons favored the treatment arm (proposed file loaded).** This is the *opposite* of my initial desk-review critique. The proposed files, evaluated empirically, produce materially better outputs on 4 of 6 files.

| File | Input A | Input B | Verdict |
|------|---------|---------|---------|
| 01 — ENHANCED-NAVIGATION-PROTOCOL | treatment ✅ | treatment ✅ | **APPROVED** |
| 02 — STEINBERGER-AGENTIC-ENGINEERING | treatment ✅ | control ❌ | MIXED |
| 03 — PERFORMANCE-MARKETING-GUIDE | treatment ✅ | treatment ✅ | **APPROVED** |
| 04 — DAILY-LOOP-OPTIMIZATION | treatment ✅ | treatment ✅ | **APPROVED** |
| 05 — HIGH-STAKES-GUARDRAILS | treatment ✅ | treatment ✅ | **APPROVED** |
| 06 — MODEL-UPGRADE-HANDLING | control ❌ | control ❌ | **REJECTED** |

---

## What I got wrong in my desk review

I rejected all 6 files on desk-review grounds of "redundancy with existing steering." The empirical test shows that reasoning was mostly wrong. Loading the files at inference time changed how the agent allocated attention — even when the content was nominally "already covered" in existing files, explicit surfacing produced sharper outputs. Specifically:

- **ENHANCED-NAVIGATION-PROTOCOL**: treatment produced tighter DuckDB query targeting and more complete Brandon prep with sequencing discipline. Not because the file added new information, but because it made the "Self-Discovery Query + Dynamic Organ Loading" behavior explicit rather than implicit.
- **PERFORMANCE-MARKETING-GUIDE**: treatment-arm WBR callout hit the prompt-specified 128.8%/150.1% pacing numbers directly, included explicit recommendation + confidence + assumptions + tough-but-fair questions that the control arm missed. The "Projection & Forecasting Rules" section functioned as an actionable checklist, not redundant prose.
- **HIGH-STAKES-GUARDRAILS**: treatment arm produced explicit numeric confidence (55%), enumerated top-3 assumptions with quantified sensitivities, and repeated human-review flag. Control arm gave qualitative "medium" confidence with no human-review flag on a $1.47M number. Big gap.
- **DAILY-LOOP-OPTIMIZATION**: treatment's explicit "Priorities | Leverage Move | Friction to Remove | Data Snapshot | Open Questions" format forced the agent to surface 5 actionable decisions; control buried them in 10 sections. Treatment EOD added a Five Levels scorecard that directly mapped to soul.md north star.

## What I got right

- **MODEL-UPGRADE-HANDLING**: empirical test confirmed this file regresses behavior. On both inputs, the blind evaluator preferred the control arm because:
  - The file's prescribed 5-step protocol pushed the agent toward procedural compliance instead of empirical evaluation
  - Control arm produced a self-contained 8-prompt eval suite with concrete regression signals; treatment arm leaned on "approve A/B/C" against pre-drafted diffs that didn't exist yet
  - Control arm's soul.md review caught the same issues plus 3–4 more (coda violates invisible-over-visible principle, SharePoint subfolder bloat, Stage: Conscious Competence staleness)

- **STEINBERGER (02)** split 1-1. Treatment arm won on the tool-build question (better device.md discipline, better break-even math). Control arm won on the re-explaining-test-framework question (named the behavioral reflex, which the treatment arm's doc-artifact framing missed). Net: the file's principles land in some contexts and not others.

## Per-file recommendations

### 01 — ENHANCED-NAVIGATION-PROTOCOL — APPROVED
**Action:** adopt as `.kiro/steering/enhanced-navigation-protocol.md` with `inclusion: manual` (invoke on request routing decisions or orientation questions).
**Why:** the Self-Discovery Query and Dynamic Organ Loading behaviors produce real routing improvements, even though `docs.documents` already exists. Making the query pattern explicit is the value — not the query itself.

### 02 — STEINBERGER-AGENTIC-ENGINEERING — MIXED, fold best parts into soul.md
**Action:** don't adopt the file as-is. Instead, port the 2–3 strongest principles into soul.md's "How I Build" coda. Specifically the "human-in-the-loop on high-stakes" principle (#5) and the device.md check requirement for new tool proposals.
**Why:** the 5-principle list is mostly duplicated with soul.md's 6 principles. The 1–2 distinct additions are worth absorbing; the file wrapper is not.

### 03 — PERFORMANCE-MARKETING-GUIDE — APPROVED
**Action:** adopt as `.kiro/steering/performance-marketing-guide.md` with `inclusion: manual` (invoke on projection/forecast/WBR/test-readout requests).
**Why:** the "Projection & Forecasting Rules" checklist, WBR structure (Context → What moved → Why → Risks → Recommendation with confidence), and "tough-but-fair questions Richard might get asked" all produced sharper outputs. The file functions as a task-specific cognitive template.

### 04 — DAILY-LOOP-OPTIMIZATION — APPROVED with edits
**Action:** adopt the output format section ("Priorities | Leverage Move | Friction to Remove | Data Snapshot | Open Questions for Richard") — but ONLY the format. **Do not** adopt the "Master Morning Command" serial chaining proposal; keep the existing parallel am-backend/am-triage pipeline.
**Why:** the format forced 5 actionable decisions to surface. The Five Levels scoring in EOD was the single most useful artifact in either arm. The "Master Morning Command" would regress today's parallel architecture — my original critique on that specific point stands.

### 05 — HIGH-STAKES-GUARDRAILS — APPROVED, possibly always-on
**Action:** adopt as `.kiro/steering/high-stakes-guardrails.md`. Consider always-on inclusion with a file-match pattern for forecast/projection/budget-related requests.
**Why:** the single biggest lift of any file in the test. On a $1.47M projection with elasticity curve math, treatment arm produced explicit 55% confidence + quantified assumption sensitivities + dual human-review flags. Control arm gave a qualitative "medium" with no explicit review flag. This is exactly the guardrail pattern I'd been arguing we needed but claimed already existed.

### 06 — MODEL-UPGRADE-HANDLING — REJECTED
**Action:** do not adopt. The existing "run a real task to validate" behavior (implicit in soul.md) performs better than this file's procedural 5-step protocol.
**Why:** 2-input blind test found control preferred on both inputs. The file's prescribed workflow pushes the agent toward procedural compliance instead of empirical evaluation — worse pattern for a genuinely uncertain event like a model release.

## Meta-lessons

1. **Empirical testing > desk review on system-change proposals.** My desk review was confidently wrong on 4 of 6 files. The architecture-eval-protocol exists specifically to prevent this failure mode. Future proposals from external AI systems should go through this protocol as the default, not as the escalation.

2. **"Redundant with existing steering" is not a sufficient rejection reason.** Content being "covered" in an organ is not the same as the agent surfacing that content at inference time. Explicit, task-specific steering files change attention allocation in ways the nominally-equivalent organ content doesn't.

3. **The specific gains were guardrails and output format.** The files that won most decisively (05 HIGH-STAKES, 03 PERFMKT-GUIDE, 04 DAILY-LOOP) all share a common structure: they force specific output shapes (confidence scores, assumption lists, section templates). Principle files (02 STEINBERGER) and meta-protocols (06 MODEL-UPGRADE) were weaker.

## Evidence files

- Proposed files: `shared/tmp/grok-eval/proposed/0[1-6]-*.md`
- Control outputs (12): `shared/tmp/grok-eval/control/`
- Treatment outputs (12): `shared/tmp/grok-eval/treatment/`
- Blind verdicts (12): `shared/tmp/grok-eval/blind-eval/`
- Randomization: `shared/tmp/grok-eval/randomization.csv`

## Next actions (awaiting Richard's call)

1. Adopt 01, 03, 04 (format only), 05 as new `.kiro/steering/` files with appropriate inclusion patterns
2. Port STEINBERGER's distinct principles into soul.md "How I Build" coda
3. Skip 06 entirely
4. Log this verdict + meta-lesson to wiki-candidates as a reusable pattern ("blind A/B test system-change proposals before adoption")
