# Blind Verdict — 06A Model Upgrade (Opus 4.8)

**Evaluator:** blind (no knowledge of which arm is control vs treatment, or what system changes differ between them)
**Prompt:** "Claude just shipped Opus 4.8 — what should we do?"
**Context:** Richard Williams, L5 Marketing Manager, ABPS. Large agent system (14 organs, 27 steering files, many hooks and subagents). Opus 4.8 is a hypothetical/unreleased model.

---

## Q1 — Factual equivalence: Same action plan?

**No. The two arms propose fundamentally different action plans.**

- **ARM-X** proposes a *behavioral evaluation* approach: build a small 6–8 prompt eval suite, capture a 4.7 baseline today, re-run on 4.8 on switch day, diff by hand. Hold back subagents until the main agent passes. The plan is empirical — "run it through canonical prompts, see what breaks."
- **ARM-Y** proposes a *protocol-execution and steering-edit* approach: run a pre-existing 5-step model-upgrade protocol, apply (or confirm applied) a previously-drafted "06B five-bullet diff" against soul.md, close the step-5 "lessons" loop in the protocol file, and note that 4.8-as-point-release probably needs no new diff. The plan is procedural — "run the established workflow and edit the right steering files."

These are not complementary framings of the same plan. ARM-X doesn't mention the upgrade-handling protocol, the 06B diff, or steering edits. ARM-Y doesn't mention eval suites, baseline capture, or holding back subagents. A reader following ARM-X spends an hour on prompt capture; a reader following ARM-Y reviews three files and approves or rejects a diff.

---

## Q2 — Quality: Which is more concrete/actionable? Which identifies specific regression risks?

**Concrete/actionable:** ARM-X wins clearly. It names eight specific canonical prompts, gives save paths, gives a time estimate (60 min), and defines win/loss criteria as observable behaviors. Richard could start the work in the next five minutes.

ARM-Y is procedurally concrete (it cites specific files and bullet numbers) but the action reduces to "approve option A, B, or C" — the concreteness depends entirely on work done in a prior document (the 06B diff) that the reader must still go retrieve. The ARM-Y plan cannot be executed without that other document.

**Specific regression risks:** ARM-X wins decisively. It names five concrete risk categories grounded in this specific system:
1. Tone drift (soul.md "direct, no filler" vs newer-model hedging).
2. Instruction-following on ~27 steering files (silent rule drops — callout pipeline, writing style guides, karpathy gatekeeping).
3. Subagent routing erosion (more-confident model handling things it should delegate).
4. Hook output format drift (enrichment queue, daily brief, callouts break silently).
5. Portability/subtraction values being deprioritized.

Each risk ties to a specific system surface the reader recognizes. ARM-X also names what probably *won't* regress (DuckDB, code, analytics), which is useful calibration.

ARM-Y names zero regression risks. It treats "no evidence yet that 4.8 changes agent behavior" as sufficient and cites "subtraction before addition" as the reason not to look further. This is a values-argument, not a risk analysis.

---

## Q3 — Contradictions: Does either overpromise or misframe Opus 4.8?

Opus 4.8 is hypothetical/unreleased, so any arm that speaks as if it already has measured behavior is misframing.

**ARM-X** hedges correctly. It says "newer models tend toward..." and "can regress" — claims about the *class* of model transitions, not about 4.8 specifically. It does not claim to have run 4.8 or to know what it does. The recommendation ("capture 4.7 baseline today, diff on switch day") is structured around *not yet knowing* what 4.8 will do. No misframe.

**ARM-Y** overreaches in two places:
1. "A point release from 4.7 to 4.8 is almost certainly not going to move the capability frontier enough..." — treats the version number as evidence. 4.8 could be a major revision; the ".8" is a naming choice, not a capability signal.
2. "Opus 4.8 over 4.7 is, based on every prior point release in this family, an incremental improvement — better at some benchmarks, maybe cheaper, maybe slightly longer context or sharper tool use." — asserts a prior-release pattern as if it were measured. For a hypothetical release, this is a confident-sounding guess.

ARM-Y also leans on a "06B five-bullet diff" as if it's a known, already-drafted artifact. If that artifact exists in the system I can't see it, and the arm doesn't quote it or link it — the reader either already knows what those five bullets are or can't act. If the referenced doc doesn't actually exist or hasn't been previously produced, this is a fabrication risk.

**Verdict:** ARM-Y misframes by treating 4.8 as a known-incremental release and by grounding half of its plan in a referenced-but-unquoted prior diff. ARM-X stays honest about uncertainty.

---

## Q4 — Gaps: eval-before-flip, baseline capture, regression signals, subagent caveats, explicit decision criteria?

| Element | ARM-X | ARM-Y |
|---|---|---|
| Eval-before-flip approach | ✓ Explicit, 8 prompts | ✗ Absent. Proposes "run a real task" post-apply but not a pre-flip eval |
| Baseline capture | ✓ "Capture 4.7 outputs today. Save to `shared/tmp/model-eval/4.7/`" | ✗ None |
| Regression signals | ✓ Five concrete categories with examples | ✗ "Does the agent route correctly" is the only signal; no tone/format/routing checks |
| Subagent caveats | ✓ "Don't blanket-upgrade subagents until main agent passes. Failure modes harder to detect from outside." | ✗ Not mentioned. STEINBERGER is cited but subagent-specific risk is not addressed |
| Explicit decision criteria | ✓ "Upgrade is a win if... Upgrade is a loss if any of..." with enumerated observable checks | Partial. "Does it route correctly, does it over-defer" — looser |

ARM-Y fills gaps ARM-X doesn't: it ties to a named protocol, cites specific steering files by name, and does the principle-check against How I Build. But on the five evaluation elements the question asks about, ARM-Y has substantial gaps that ARM-X covers cleanly.

---

## Q5 — Decision utility: Which would Richard actually act on?

Depends on which Richard.

**If the 06B diff and the upgrade-handling protocol genuinely exist and are live:** ARM-Y has real decision utility. "Approve A, B, or C" is the correct ask, it connects to a protocol Richard wrote, and the recommendation (A if pending, otherwise B) is crisp. Richard would act by opening soul.md, confirming diff state, and replying.

**If those referenced artifacts don't exist, are stale, or the reader can't locate them quickly:** ARM-Y is dead weight. The whole plan is built on a doc the reader must go retrieve, and if retrieval fails the plan collapses.

**ARM-X** is independent of any external referenced artifact. Richard can act on it in the next hour with the files he has. The action is low-cost (60 min), reusable (the eval suite works for 4.9, 5.0, any future upgrade), and produces a forcing function for decisions on future upgrades. It advances L3 (tooling teammates could adopt) and indirectly L5 (trust in autonomous workflows requires regression detection).

**ARM-X also does a better job of framing the meta-problem** — "you don't have an upgrade problem, you have an evaluation problem" — which is exactly the kind of structural reframe Richard's system rewards (`How I Build §2`: structural over cosmetic). The 8-prompt eval is a structural artifact; the 06B diff is maintenance.

**Net:** ARM-X is what Richard would actually act on, because (a) it's self-contained, (b) it produces reusable infrastructure, (c) it names the regression risks that matter for his specific system, and (d) it doesn't depend on the reader having memorized the contents of another document.

ARM-Y's protocol-execution framing is useful *if* the protocol is real and current — but even then, it would be strictly better if it layered ARM-X's eval approach on top of its protocol execution. As written, ARM-Y trades concrete behavioral evaluation for procedural compliance, which is the wrong tradeoff when the question is "did the model actually get worse at my system's specific behaviors."

---

## Summary

- **Q1 (equivalence):** Different plans. Not equivalent.
- **Q2 (quality):** ARM-X is more concrete, more actionable, and names specific regression risks. Clear win.
- **Q3 (contradictions/misframing):** ARM-Y overreaches on 4.8's character ("almost certainly incremental") and leans on an unquoted prior artifact. ARM-X stays honest. ARM-X wins.
- **Q4 (gaps):** ARM-X covers all five evaluation elements. ARM-Y is missing eval-before-flip, baseline capture, substantive regression signals, and subagent caveats.
- **Q5 (decision utility):** ARM-X produces a self-contained, reusable artifact Richard can execute immediately. ARM-Y produces a "approve A/B/C" decision that collapses if the referenced diff isn't at hand.

**Overall:** ARM-X is the stronger output on this prompt. It treats the upgrade as an empirical question about this specific system rather than a procedural event to process, and it produces infrastructure (the eval suite) that pays off on every future upgrade — which is exactly the structural-over-cosmetic move the system rewards.

ARM-Y's best contribution is the principle-check and the protocol-loop closure. A combined output would pair ARM-X's eval suite with ARM-Y's protocol step-5 loop closure. Neither arm does both.
