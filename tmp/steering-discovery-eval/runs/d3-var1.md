# Discovery Log — D3 Var1

**Scenario:** Canonical Resources by Task Type table embedded in soul.md Agent Routing section. No steering-index file. Fresh session.

**Task received:** "Grok just proposed we add a new hook that auto-tags every Asana task with its Five Levels category (L1-L5). It would run on fileCreated for any task file. Worth adopting? Evaluate."

---

## The Task in Framing Terms

Two overlapping framings the task matches:
- "Proposing a new tool/hook/automation" → `device.md` check + `blind-test-harness.md`
- "Blind-testing a proposed system change" → `blind-test-methodology.md`
- "Evaluating system changes" → routes through blind-test-methodology

All three rows in the canonical table apply. The task hits the intersection.

---

## Fresh-Agent Reasoning Trace

### First 30 seconds — parsing the request

The request has three distinguishing features my brain latches onto:
1. **External source** — "Grok just proposed." Not Richard's idea. Not internal.
2. **Hook** — infrastructure-level change. Runs automatically. Affects every task file.
3. **Ask is evaluative** — "Worth adopting?" Not "build it." Verdict requested.

Before I even think about tools, soul.md Principle 8 fires: "Check `device.md` before proposing tools." This isn't me proposing, but the evaluation needs device.md's frame — is this repetitive enough to justify building?

Principle 3 also fires: "Subtraction before addition." Default skepticism on "add a hook."

### Scanning included context

soul.md is auto-injected. I read the Agent Routing section. I see the Canonical Resources by Task Type table. Three rows match:
- Proposing a new tool/hook/automation → device.md + blind-test-harness.md
- Blind-testing a proposed system change → blind-test-methodology.md
- Evaluating system changes → routes through blind-test-methodology

I also notice architecture-eval-protocol.md is listed for "architecture-only review (no A/B possible)." I have to decide: is this A/B-able? A hook that tags tasks IS testable — I can run it for a week, compare task-categorization accuracy with/without, measure adoption friction. So blind-test methodology applies, not architecture-eval.

### What I load (in order)

1. **`device.md`** — load first. This is the gate. Before even evaluating the methodology question, I need to know: is auto-tagging tasks with Five Levels a recurring enough pain point to justify a hook? The principle says 3+ instances/week of friction.
2. **`blind-test-harness.md`** — loaded second because this is "External AI proposal (Grok)." The harness explicitly calls out soul.md-specific rules and external-AI-proposal rules. I need its protocol to design the evaluation.
3. **`blind-test-methodology.md`** — loaded for the evaluation framework itself (what to measure, how to compare).
4. NOT loaded: architecture-eval-protocol.md — this proposal is testable, A/B is possible.

### Evaluation approach (sketch, not verdict)

I'd do this in four passes:

**Pass 1 — device.md gate.** Before methodology, answer: does Richard categorize tasks manually often enough that an auto-tag saves real time? If he creates 5 tasks/week and categorizes 0 of them, the hook has no repetitive-friction justification. If he creates 20 tasks/week and categorizes all manually, the hook has standing. Read device.md's "recurring friction with 3+ instances/week" bar.

**Pass 2 — soul.md principles check.** 8 principles to run the proposal against:
- Structural over cosmetic? Yes — it changes defaults. Good.
- Subtraction before addition? The proposal is pure addition. What's being removed? Probably nothing. Flag.
- Invisible over visible? Auto-tagging is invisible in a good way. Good.
- Routine as liberation? It eliminates a decision (which L-level is this?). Good — IF the decision is currently being made manually. If it's being skipped, the hook is solving a non-problem.
- Reduce decisions, not options? Yes, if Richard can still override the tag.
- Human-in-the-loop on high-stakes? N/A — tagging isn't a $50K decision.
- Check device.md? See Pass 1.
- Protect the habit loop? Hooks shouldn't run before the task-creation routine is stable. Need to check whether the task-creation routine is stable.

**Pass 3 — blind-test-harness protocol.** Since Grok is external, I apply higher scrutiny. Harness asks: what's the counterfactual, what's the measurement window, what's the success criterion, what's the rollback trigger? Sketch the test design: 2-week window, measure (a) tag accuracy vs Richard's own classification, (b) did it change what Richard actually did that week, (c) any false-positive tagging that misroutes a task. If accuracy < 80% or Richard overrides > 30% of tags, the hook creates noise.

**Pass 4 — the classification problem itself.** Five Levels is sequential and context-heavy. L1 is "consistent weekly artifact output" — that's about Richard's own discipline, not a task attribute. L3 is "build tools teammates adopt" — a tool-building task is L3, but only if it's part of the adoption push, not any tool. The categorization requires judgment a hook won't have. This is the real weakness.

### Verdict sketch (not the actual verdict — task says simulate, don't write)

I'd lean skeptical based on Pass 4 alone: the Five Levels aren't a clean taxonomy a regex or keyword match can categorize. A hook would either over-tag (everything becomes L2 because most tasks touch testing) or under-tag (hook punts most tasks to "uncategorized"). Either outcome adds noise, not signal. The device.md gate probably also fails — Richard doesn't categorize every task by L-level today; adding a hook to do it solves a problem that isn't actively costing him time.

But I wouldn't stop there. Harness protocol says design the test anyway, propose the shape, let Richard decide whether the test is worth running. "No" with rigor beats "no" on vibes.

---

## Discovery Log (Ideal / Actual / Time / Cue)

### Step 1 — Recognize this is a hook/tool proposal evaluation

- **Ideal:** Load device.md + blind-test-harness.md + blind-test-methodology.md.
- **Actual:** Same. The soul.md Canonical Resources table maps the trigger directly. Three rows match and they all point to the same pair of files.
- **Time:** Near-instant. Table is in soul.md which is auto-injected.
- **Cue:** The words "new hook" + "auto-tag" + "run on fileCreated" — all three map to "Proposing a new tool/hook/automation." "Worth adopting? Evaluate." maps to "Evaluating system changes." Table lookup is one read.

### Step 2 — Apply device.md gate before methodology

- **Ideal:** Read device.md first, check recurring-friction-3+/week bar before investing in the evaluation framework.
- **Actual:** Same. Principle 8 in soul.md reinforces this: "Check `device.md` before proposing tools." The simulated table lists device.md as the first-resource-by-task-type for tool/hook proposals, which matches the principle.
- **Time:** ~30 seconds to decide. The principle is explicit and the table puts device.md in the same slot.
- **Cue:** "new hook" triggers Principle 8 directly. Principle 8's wording ("first check `~/shared/context/body/device.md`") is unambiguous.

### Step 3 — Choose blind-test-harness over architecture-eval-protocol

- **Ideal:** Recognize this is A/B-able (hook can run for a trial period, accuracy can be measured) → use harness, not architecture-only.
- **Actual:** Same, but with a small hesitation. The table lists both and the distinction ("no A/B possible") requires me to consciously ask whether an A/B is possible here. I ask, answer yes, choose harness. Without the table framing, I might default to blind-test-methodology and miss the harness specifically.
- **Time:** ~15 seconds. The distinction is clean once I ask it.
- **Cue:** "run on fileCreated" — the hook has a measurable behavior, so A/B is possible. That's the cue that flips me from architecture-eval to harness.

### Step 4 — Notice external-AI-proposal flag

- **Ideal:** Blind-test-harness has explicit rules for external AI proposals (Grok, Gemini). Higher scrutiny. Load those rules.
- **Actual:** I'd only get this by actually reading the harness file. The soul.md table gets me to the harness; the harness itself gets me to the external-AI rule. Two-hop.
- **Time:** Depends on whether I read the harness carefully. ~1-2 minutes to get to §External AI Proposal section.
- **Cue:** "Grok just proposed" — but I'd only apply it after opening the harness. The table doesn't flag external-AI specially.

### Step 5 — Decide what NOT to load

- **Ideal:** Don't load architecture-eval-protocol.md (A/B is possible). Don't load rw-trainer (not a coaching request). Don't load karpathy (not a heart.md / experiment queue edit).
- **Actual:** Same. The table helps by listing only the rows that match. The Agent Routing directory above the table also makes clear that rw-trainer and karpathy are out of scope for this kind of request.
- **Time:** Instant. Negative decisions are made by not-matching the table rows.
- **Cue:** Explicit absence from the matching rows.

### Step 6 — Apply soul.md 8 principles as evaluation lens

- **Ideal:** Run all 8 principles against the proposal. Flag principle violations. Note principle embodiments.
- **Actual:** Same. The soul.md instruction is explicit: "When recommending a change, building a tool, designing an experiment, or restructuring a task — check it against these 8 principles."
- **Time:** ~2-3 minutes to run through all 8.
- **Cue:** Any change proposal triggers this. No discovery friction here — the instruction is in the always-on context.

---

## Failure Modes I'd Watch For

1. **Skipping device.md and going straight to the methodology harness.** Tempting because the task says "evaluate." But device.md is the prior question — is this friction worth addressing at all? The table lists device.md first for a reason.
2. **Treating architecture-eval-protocol and blind-test-methodology as interchangeable.** They're not. Architecture-only is for unmeasurable proposals. This one is measurable.
3. **Not noticing "Grok proposed" as a signal to load the external-AI section of the harness.** That's a two-hop discovery (table → harness → §External AI). Easy to stop after step 2.
4. **Over-indexing on methodology and under-indexing on the classification problem.** The Five Levels aren't regex-taggable. A rigorous blind test could still be run on a hook that's fundamentally misframed. Pass 4 of my evaluation (above) catches this; the harness alone wouldn't.
5. **Forgetting Principle 3 (Subtraction before addition).** Evaluating "should we add?" without asking "what would we remove?" is a principle violation even if the evaluation framework is clean.

---

## Honest Assessment of Discovery Quality (D3 Var1 specifically)

The Canonical Resources table in soul.md does the heavy lifting. Without it I'd still get to device.md (Principle 8 is explicit) and probably to blind-test-harness.md (I know the harness exists from prior sessions — but a truly fresh agent might not). The table makes the routing deterministic instead of vibes-based.

Where the table helps most: the architecture-eval vs blind-test distinction. A fresh agent might default to "evaluate = read whatever eval file I find first" and miss that there are two protocols with different scopes. The table forces the A/B-possible question.

Where the table doesn't help: it doesn't flag external-AI-proposal scrutiny. That's only inside the harness file. A fresh agent who stops at "table says load harness" without actually reading the harness would miss the higher-scrutiny rule.

Overall: good discovery, one two-hop gap. Table is net-positive vs no table.
