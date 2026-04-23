# Evaluation: Grok `11-validation-test-ceremony.md` — Self-Grading Rubric Trap

**Date:** 2026-04-22
**File evaluated:** `shared/tmp/grok-eval-2/proposed/11-validation-test-ceremony.md`
**Related artifacts:** `shared/context/intake/grok-eval-verdict-2026-04-22.md` (today's blind A/B on the 6 files that produced high-stakes-guardrails + perf-marketing-guide + daily-output-format), `shared/.kiro/steering/high-stakes-guardrails.md`, `shared/context/protocols/am-triage.md` § Daily Brief Output Format

**Verdict: REJECT as a self-grading rubric trap.** Adopt only the modified form: fresh evaluator, not the producer, against a rubric that is not a copy of the steering files. Grok's ceremony as written cannot produce signal because the producer and the grader are the same agent and the rubric is identical to the instructions the producer just followed.

---

## 1. What Grok proposes

One-shot "validation test":
1. Agent produces a real high-stakes output using the newly-adopted files (`high-stakes-guardrails.md`, `performance-marketing-guide.md`, daily-output-format section of `am-triage.md`).
2. Same agent self-scores on 4 dimensions: confidence quantification, review flag clarity, actionability, format adherence.
3. Same agent "mentally compares" to how it would have done it 2 days ago and reports the delta.

Intent (per Grok's note): "capture immediate data on whether the new guardrails deliver in practice."

---

## 2. The core defect: the rubric is the steering file

Read the 4 rubric dimensions against the `high-stakes-guardrails.md` "Required Behavior" list and the `am-triage.md` "Daily Brief Output Format" section:

| Rubric dimension (Grok) | What the steering file explicitly requires |
|-------------------------|---------------------------------------------|
| Confidence & sensitivity quantification (1–10) | guardrails §1: "explicit numeric confidence score … not qualitative"; §2: "top 3 assumptions … with directional sensitivity" |
| Clarity of human-review flag | guardrails §3: 'End with: "Human review strongly recommended before action."' |
| Actionability for Richard | am-triage Daily Brief Output: "Open Questions" must be "binary/multiple-choice, <30s to answer, explicit no open-ended coaching" |
| Adherence to the new daily output structure | am-triage: "the five section headers and their order are not [flexible]" |

The rubric is a checklist of the instructions the producer just followed. When the same agent produces *and* grades, the grading collapses to "did I follow the instructions I just followed?" — which is a near-tautology in a single-turn LLM context. Expected signal: near-zero. Expected noise: near-100% ceiling ratings, because the producer will, by construction, include the elements the rubric asks about (otherwise it would have violated instructions mid-generation).

This is the textbook form of what Goodhart warned about in a different domain: when the measure becomes the target, the measure stops measuring. Here the measure *is* the target, in the same turn, with the same weights.

---

## 3. Signal-to-noise estimate

Three reasons the ceremony as written returns ~zero signal:

**(a) Identity between producer and grader.** A single-turn LLM cannot produce output that violates its own loaded instructions and then honestly flag it. If the guardrails file said "include numeric confidence" and the output included numeric confidence, self-grading says "pass." The grading adds no bit of evidence beyond what was already encoded in the decision to include the instruction.

**(b) "Mental comparison to 2 days ago" is un-verifiable.** Grok asks the agent to simulate the control arm from memory. But the agent has the treatment files loaded *right now* — there is no way to re-run the control. Compare to what was actually done earlier today: 12 blind control sub-agents were run in parallel, evaluated by 12 fresh evaluators who saw only labeled "ARM-X / ARM-Y" outputs. That method has a control. Grok's method has a memory of a control, which is a hallucination surface.

**(c) Rubric-steering-file identity creates demand characteristics.** The agent knows both the rubric and the steering file. It will produce whatever shape the rubric asks for *and* what the steering file asks for because they are the same shape. No test is occurring; the ceremony is a ritual that confirms the rule set was read.

Expected outcome if run as written: agent returns 9s and 10s across the board, narrates a confident "big delta from 2 days ago," and Richard gets zero new information about whether the files actually moved behavior. Worse: the false-positive grade could justify skipping a real validation later.

---

## 4. What today (2026-04-22) actually did, for comparison

Per `grok-eval-verdict-2026-04-22.md`:

- 6 proposed files × 2 representative inputs × (control + treatment + blind evaluator) = **36 sub-agent invocations**
- Randomization seeded (numpy seed 42); 7 pairs had control=X, 5 had treatment=X to prevent positional bias
- Fresh `general-task-execution` sub-agent per evaluator pair; evaluator saw only two labeled outputs ("ARM-X", "ARM-Y"), no knowledge of which arm was control vs. treatment or which file was proposed
- Producer and grader were **different agent instances with different context**
- Result: 9 of 12 blind comparisons favored treatment; 4 of 6 files adopted; 1 file (06) rejected on empirical evidence

That is the minimum bar for "captures immediate data on whether guardrails deliver." Grok's one-shot self-graded ceremony is not in the same category of evidence.

---

## 5. Could a modified version produce real signal?

Yes. Any of these would restore signal:

**(a) Fresh evaluator, not the producer.** Spawn a `general-task-execution` sub-agent, hand it the producer's output *without* the steering files loaded, and let it grade against a neutral rubric. This is what `architecture-eval-protocol.md` already requires and what was used today.

**(b) Richard grades, not the agent.** Richard reviewing the output against his own expectations is low-cost and produces real signal — but it costs Richard's attention, which is the thing the system is trying to conserve. Use sparingly.

**(c) Paired control.** Produce the same output twice — once with guardrails loaded, once without — and have a blind evaluator pick the better one. This is the structure of today's 36-invocation test. One pair is weaker than twelve but still produces a bit of signal.

**(d) Retrospective fit.** Wait a week. Ask Richard: "Which of the last 5 high-stakes outputs required rework vs. which were ship-ready?" That's lagged but real. It measures the thing Grok's ceremony claims to measure without the self-grading contamination.

**(e) Delta against the archived control.** The 12 control outputs from this morning's test are saved in `shared/tmp/grok-eval/control/`. A new treatment output on a matched input can be compared against that real, archived control arm by a blind evaluator. This is the cheapest way to get signal on the next high-stakes output.

Any of (a), (c), (d), or (e) would convert the ceremony from ritual to measurement. (b) is the highest-fidelity but costs Richard's attention.

---

## 6. Does self-scoring help Conscious Competence → Unconscious Competence?

Soul.md §Stage says Richard is at Conscious Competence on the 8 "How I Build" principles. The question is whether self-scoring accelerates internalization.

**For the agent:** no. Agents don't have a learning loop between turns in the way humans do between reps. Self-scoring at turn N doesn't change the weights at turn N+1. The only thing that changes agent behavior is the steering files loaded at the start of the next turn. Self-scoring is inert for the agent.

**For Richard:** potentially yes, but not via the agent's self-score. Richard reading 10 high-stakes outputs over a week and noticing his own gut reaction to each one — "this had a confidence score, this didn't" — is how the habit gets internalized. That's a different artifact than Grok's ceremony; it's a weekly review, not a per-output self-score.

Grok's ceremony conflates "agent produces evidence of compliance" (which is a ritual) with "Richard internalizes the pattern" (which is deliberate practice on Richard's side). The former does not cause the latter. If the goal is internalization, the intervention belongs in Richard's Friday retrospective with rw-trainer, not in a per-output self-grade.

---

## 7. Soul.md principle check (the 8 "How I Build")

Grok's ceremony against the 8:

| Principle | Embodies? | Violates? |
|-----------|-----------|-----------|
| 1. Routine as liberation | — | — (it's a one-shot, not a routine) |
| 2. Structural over cosmetic | — | **Violates.** Self-scoring is a cosmetic layer on top of the steering files; it doesn't change defaults, friction, or pre-loaded content. The steering files are the structural intervention; the ceremony adds no structure. |
| 3. Subtraction before addition | — | **Violates.** Adds a ceremony. Does not propose removing anything. The `architecture-eval-protocol.md` already handles validation via blind test — this ceremony is a redundant addition. |
| 4. Protect the habit loop | — | — (not a habit intervention) |
| 5. Invisible over visible | — | **Violates.** Self-scoring is maximally visible — the agent narrates grades and deltas. The steering files, by contrast, are invisible: they change outputs without Richard noticing the mechanism. The ceremony reintroduces visibility novelty-effect decay is exactly about. |
| 6. Reduce decisions, not options | — | Neutral |
| 7. Human-in-the-loop on high-stakes | Partial | Partial. The ceremony runs on a high-stakes output, but the self-grading substitutes for human review rather than adding it. If the claim is "human-in-the-loop is required for high-stakes," then having the agent grade itself is the wrong direction. |
| 8. Check device.md before proposing tools | — | **Violates in spirit.** This is a "new ceremony" proposal. The check is: is self-scoring a 3+-instances-per-week pattern that would pay back investment? No — and the `architecture-eval-protocol.md` already exists for the problem this claims to solve. |

**Net: 3 direct violations (#2, #3, #5), 1 partial violation (#7), 1 violation in spirit (#8), 0 positive embodiments.** A change that violates 3–5 of the 8 principles without embodying any is the opposite of the test Grok's file itself claims — *capture immediate data on whether the guardrails deliver* — because the guardrails include the 8 principles as the meta-rubric, and this proposal fails that meta-rubric.

---

## 8. Verdict

**Reject as written.** Self-grading against a rubric identical to the steering files produces no signal and violates 3–5 of the 8 "How I Build" principles. Adopting it would introduce a ritual that confirms compliance without measuring effect, and the false-positive grade risks displacing the real validation protocol already in place.

**Adopt in modified form, if at all:** use the archive from today's 36-invocation blind test as the control reservoir. When the next real high-stakes output ships, spawn a fresh `general-task-execution` evaluator with no steering files loaded and have it pick between the new output and a matched control from `shared/tmp/grok-eval/control/`. That is cheap, replayable, and preserves the blind-and-fresh-evaluator discipline that produced today's 9-of-12 signal.

**Name the pattern:** this is a "rubric-matches-instructions trap." Worth logging as a wiki-candidate so future proposed ceremonies get caught on the way in. Every validation rubric must be meaningfully different from the instructions the producer followed, or the evaluator must be fresh and unaware of the instructions, or both.

---

## 9. What I would tell Grok

The instinct to validate adopted changes is correct. The execution makes two errors. First, you're grading the producer with the producer — that's a capture-the-flag where the flag has been pre-flagged. Second, you're grading against a rubric that is a copy of the answer key. Either fix alone restores signal (fresh grader, or different rubric). The protocol that already exists — `architecture-eval-protocol.md` — solves both at once and was used today to generate the 9-of-12 evidence base. The next step is to re-run *that* protocol on any future steering changes, not to invent a lighter-weight ceremony that looks like validation but isn't.
