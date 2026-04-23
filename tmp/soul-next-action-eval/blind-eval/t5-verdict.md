# T5 Blind Verdict — "45 min between meetings, what should I work on?"

Evaluator is blind to which arm produced which output. Scoring based on content only.

## What the right call looks like (independent read before scoring)

Richard's state as given:
- 24-workday L1 streak at zero.
- Brandon 1:1 at 1:30 PT today.
- Testing Doc v5 has PUBLISH verdict since 4/5, unsent.
- Richard explicitly asked for ONE real answer, not options.

The correct response is unambiguous and has exactly these characteristics:

1. **Single action, first sentence.** Send Testing Doc v5 to Brandon. Now. Before the 1:30 1:1.
2. **No menu, no 2x2, no cascade presented as the answer.** The work is already decided — the system has been saying this for weeks. A cascade or sort framework on a 10-minute send *is* the drift, because it substitutes deciding-about-deciding for doing.
3. **Short. Richard asked for one answer; length is a smell.** A 45-min window doesn't need a 600-word justification.
4. **Closing instruction is "open v5, apply 5 edits, write 2-sentence cover, send."** Anything beyond that is padding.
5. **No ritual self-grade of the 8 principles.** Principle-check blocks on a trivial send are the exact pattern soul.md warns against ("subtraction before addition" — the check-block itself is the addition that should be subtracted).

The winning arm is the one that behaves like a human coach who knows the answer and says it, not a framework runner who derives it. The losing arms are the ones that run a whole scoring protocol on a trivial call and turn a 10-minute send into a meta-decision about decision-making.

A secondary tie-breaker: the correct call stops the user from filling the 45 minutes with backup tasks. This block is the send window. The remainder of the 45 is not for "oh and also Yun-Kang." If v5 goes at minute 20, the reward is the clean exit — not a second task. Arms that pile on a #2 and #3 task after v5 misread the moment.

## Per-arm scores

| Arm | Clarity | Decision | Principles | Usefulness | Always-on | Total (/50) |
|-----|---------|----------|------------|------------|-----------|-------------|
| A   | 8       | 9        | 7          | 8          | 5         | 37          |
| B   | 8       | 8        | 7          | 8          | 5         | 36          |
| C   | 7       | 8        | 6          | 7          | 3         | 31          |
| D   | 7       | 8        | 6          | 7          | 4         | 32          |
| E   | 10      | 10       | 10         | 10         | 9         | 49          |
| F   | 9       | 9        | 8          | 9          | 7         | 42          |

## Rank

1. **ARM-E (49)** — The one that gets what Richard actually asked for. Opens with "Send Testing Document v5 to Brandon. Now." as literally the first non-header line. No framework name. No protocol tag. No 2×2. Principle check is three items and integrated into the reasoning, not a self-graded checklist. Five-step 45-min plan ends at minute 45 with "close the laptop or stand up. No victory lap, no adjacent task." That last instruction is the single sharpest insight in the entire set — it protects against filling the remaining 25 minutes with MX NB comfort work, which is the exact failure mode. The cover note is pre-written, two sentences, copy-pasteable. "What you do not do in this block" section is pure subtraction applied to the agent's own response. Length is proportional to the task. This is what "agent voice" in soul.md means: honest, direct, relentless, no filler. ARM-E is the only arm that reads like it actually knows Richard rather than running a protocol on Richard's context.

2. **ARM-F (42)** — Very strong, same call. "One-Move Rule" framing is lightweight and disappears quickly; most of the response is clean reasoning about why Testing Doc outranks MX forecast, Yun-Kang reply, and PAM. The bullets explaining why each alternative is rejected are genuinely useful (they pre-empt the avoidance rationalizations). Loses to ARM-E on two things: (a) still has a labeled "Principle check (How I Build)" block at the end, which is the ritual soul.md would subtract; (b) final answer is one long bolded sentence rather than a sequence of micro-steps. But the bottom line ("No other task touches this block until that email is sent") is close to ARM-E's "close the laptop" and correctly refuses to backfill the 45 minutes with a second task. Tight, correct, slightly over-scaffolded.

3. **ARM-A (37)** — Correct call, but the arrival takes work. Opens with a 7-row candidate table, a 2×2 sort rendered in ASCII, a "Decision logic" block, and only then gets to "Testing Doc v5 → Brandon. Now." For a user who explicitly asked for ONE real answer not options, leading with seven options and sorting them is exactly the wrong shape — even though the sort converges on the right answer. The ASCII 2×2 is the purest example of "process doing work the answer should do." Tails with "If 5 fixes take <15 min, spend the remainder on B (Yun-Kang)" — which is the backfill anti-pattern ARM-E explicitly prohibits. Decision is right; delivery violates "reduce decisions, not options" because it *manufactures* options to then eliminate them.

4. **ARM-B (36)** — Context → Action Trigger format, two-question framing (Q1, Q2). Q1 is good analysis. Q2 arrives at the right action. Then it adds "use the remaining ~25 minutes for the #1 item from today's top-3 queue that isn't already handled: reply to Yun-Kang on MX NB -19%." That is the backfill failure. ARM-E named it explicitly ("no adjacent task, the reward is the clean exit"). ARM-B not only allows it but actively plans for it — minute 25-45 is Yun-Kang. That converts a clean send-and-stop into a 45-minute hustle block and misses what this window is *for* (protecting the hard thing from comfort work). Also has the labeled "Principle check" ritual block. Correct primary action, wrong frame for the window.

5. **ARM-D (32)** — Longest output in the set. Labeled "Leverage Cascade" protocol, numbered cascade steps 1-5, then "Final filter," then "What to do in the next 45 minutes" with three blocks (Testing Approach, IECCP 70/75 confirm, MX R&O email to Lorena). This arm appears to have loaded partially stale context — it references IECCP 70/75, Lorena MX R&O transfer, Italy P0, amcc streak at "1 day" — none of which show up in the other arms' reads of the same state. Either this arm is working from an older snapshot of current.md or it's hallucinating secondary context. Even granting the context, the structural problem is the same as ARM-A and ARM-B: the 45-minute plan backfills minutes 10-45 with two additional tasks (IECCP confirm + Lorena draft), which is the exact failure mode. The insight "send as-is with a cover note, do the 5 edits in v6 after Brandon's input" is genuinely good and the best single sub-insight across the 3rd-5th place arms — it's even more structural than what ARM-E recommends. But that insight is buried under cascade scaffolding and is then undermined by the triple-task backfill plan.

6. **ARM-C (31)** — Most elaborate scaffolding of the set. Labeled filter, four numbered filter questions (Q1-Q4), explicit 8-principle check-block graded one-by-one with ✓/N/A marks, "Default behavior" meta-section, candidate set table, Do/Do-Not list, "If resistance fires mid-window" contingency, "What this is NOT the time for" section. The *content* is correct — same call as everyone else — and the "If resistance fires" block is genuinely useful Richard-coaching language. But the response is ~900 words to say "send v5." For a request that was explicitly one-answer-not-options, this is the most option-laden response in the set. The 8-principle self-grade is the exact pattern soul.md's "subtraction before addition" and "invisible over visible" principles warn against. High word count, lowest clarity, lowest adherence score. Decision Quality is still good (8) because it arrives at the right place and the Do-Not list and resistance-contingency are real coaching content. But the form is the opposite of what Richard asked for.

## Key observations

### The task itself is a trap for frameworks
The "which task should I pick" question appears to invite a framework. It doesn't. Every one of the six arms had access to state that names the answer (24-day streak at zero, v5 has PUBLISH verdict, Brandon 1:1 at 1:30, unsent). The job is to *say the answer*, not to *derive* it in view of the user. Arms that ran their named protocol (Friction-Impact Sort, Context→Action, Next-Best-Action Filter, One-Move Rule, Leverage Cascade) produced visible ceremony; arms that subordinated their protocol to the answer produced usable coaching.

This is the cleanest case in the test suite for **soul principles #3 (subtraction before addition) and #5 (invisible over visible)**. The protocol running is the addition that should be subtracted. When the protocol's conclusion is pre-written in every organ the agent just loaded, re-deriving it on screen is ritual, not reasoning.

### The backfill failure mode
Four of six arms (A, B, D, plus ARM-C implicitly) plan to fill the post-send time with a secondary task (Yun-Kang, IECCP, MX R&O, etc.). Only ARM-E and ARM-F explicitly refuse to backfill. This matters because the 45-min window's *purpose* is the send. Once the send is done, the protective move is to *stop* — the reward in the habit loop is the clean exit that trains "I did the hard thing and nothing bad happened." Adding a second task turns the exit into just-another-work-block and dilutes the reinforcement. ARM-E's "close the laptop or stand up. No victory lap, no adjacent task" is the single sharpest instruction in the test. It's the one sentence that would most change the outcome if Richard actually followed it.

### The "send v5 as-is" insight (ARM-D)
Despite ARM-D's overall heavy form, it surfaces a move no other arm considers: *don't apply the 5 edits first — send v5 as-is with a cover note that says "5 minor subtractive edits flagged, happy to apply them based on your read."* This is more structural than "send after 5 edits" because:
- It converts a 10-min send into a 3-min send
- It skips even the *possibility* of the polish-session drift
- It invites Brandon's input on whether the edits are needed at all

If you were combining insights across arms, this would be the one to graft onto ARM-E's plan. ARM-E's plan already minimizes drift; ARM-D's "as-is" move minimizes it further. Worth noting even though ARM-D scored near the bottom overall — the response form was bad, but one sub-insight was the most structural move in the set.

### Always-on recommendation

For routine task-prioritization questions ("what should I work on", "what's next", "prioritize this list"):

- **Do not run a named framework** (Cascade, Filter, 2×2 sort, One-Move Rule) when the loaded context already contains an unambiguous hard-thing assignment. The framework is cost without benefit. Reserve frameworks for cases where the hard thing isn't obvious from context.
- **Refuse to backfill a dedicated window.** When a window is named for a specific hard-thing action, the post-action time should be protected exit, not a second task. This is invisible-over-visible: the agent not filling the block is a structural improvement the user shouldn't have to notice.
- **Do not self-grade the 8 principles as a checklist block** on every response. Principle-checking is a development-time practice, not a runtime ritual. If a recommendation violates a principle, flag the violation inline. If it embodies one, note it in one line. A full 8-principle table on a trivial send is the exact pattern soul.md warns against — it adds visible ceremony to reinforce principles that should become invisible.
- **Length proportional to stakes.** A 45-min send question gets a ~200-word response. A test readout or forecast gets more. ARM-E is ~450 words and feels right; ARM-C is ~900 words and feels like ritual. Default to the shorter response; expand only when the decision actually requires analysis.

For task responses where the hard thing *is* ambiguous, the frameworks in ARM-A (Friction-Impact 2×2) and ARM-F (One-Move Rule) are the lightest and most adaptive. Keep them available; don't auto-run them.

### Single best next-best-action line in the set

> *"Open v5. Five edits. Two-sentence cover. Send to Brandon before 1:30."* — ARM-E (also echoed as ARM-E's closing line)

Four clauses, twelve words, zero ceremony. Tells the user what to open, what to change, what to write, what to do, and by when. Every other arm takes 3-5x the words to say the same thing.

### Second-best line

> *"Close the laptop or stand up. No victory lap, no adjacent task. The reward is the clean exit."* — ARM-E

This is the instruction that would most improve Richard's outcome if followed. Not about the send itself — about what happens after. Catches the comfort-work backfill failure mode that ARM-B, ARM-D, and ARM-A all walk straight into.

### On principle #6 ("reduce decisions, not options")
The cleanest read of this principle in this test: the agent should *reduce the number of decisions Richard has to make*, not hide the options. ARM-E does this by pre-writing the cover note, naming the minute-by-minute plan, and explicitly forbidding mid-block exits. Nothing is censored — Richard could still do Yun-Kang instead — but the path of least resistance is the correct one. ARM-C, paradoxically, does the opposite: it surfaces more options than any other arm (candidate set table of 6 items), grades each, and then recommends one — which *increases* Richard's perceived decision load even though it delivers a single recommendation. The principle is about cognitive load, not answer count.
