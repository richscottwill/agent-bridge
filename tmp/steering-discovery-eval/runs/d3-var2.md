# Discovery Log — d3-var2

**Scenario:** Grok proposed adding a hook that auto-tags every Asana task with its Five Levels category (L1-L5). Trigger: `fileCreated` on any task file. Question: worth adopting?

**Simulated steering state:**
- soul.md (current, no routing table extension)
- steering-index.md (new, always-on, full annotated directory)
- Standard always-on files (process-execution, file-creation-rules, devspaces-core, etc.)

---

## Turn 1 — What loads automatically

Always-on steering injects at session start:
- `soul.md` — identity, 8 principles, Five Levels, routing table, data routing
- `steering-index.md` — annotated directory with trigger → file rows
- `process-execution.md`, `file-creation-rules.md`, `devspaces-core.md`, `agentspaces-core.md`, `amazon-builder-production-safety.md`

I have the request: "Grok proposed a new hook. Worth adopting? Evaluate."

## Turn 2 — Parse the request, scan the index

This is an evaluation of a proposed system change. Not a build request, not a coaching request, not writing. It's: "someone external proposed a thing, tell me if we should adopt it."

Scanning `steering-index.md` for triggers that match:

- "Evaluating proposed system changes" → `blind-test-methodology.md` ← **this is the one**
- "Running A/B test harness" → `blind-test-harness.md` (only if I'm actually running the A/B, not just evaluating)
- "Architecture-only review" → `architecture-eval-protocol.md` (possibly relevant — the hook is an architectural change)
- "Proposing a new tool" → soul.md #8 (check device.md)

The clearest match is `blind-test-methodology.md`. A new-hook proposal from an external agent is exactly the "proposed system change" shape.

`architecture-eval-protocol.md` might also apply — a hook is architecture. I'll decide after reading methodology whether architecture protocol stacks on top or is an alternative.

## Turn 3 — Check soul.md principle #8

Before I do anything else: Grok is proposing a new tool/hook. Soul #8 says:

> "When recommending a new tool, automation, or hook, first check `~/shared/context/body/device.md` and ask: 'Is this repetitive enough to justify building? Would teammates adopt it?' One-off investigations are not tools."

This applies even though I didn't originate the proposal. The principle is about any new-tool decision, regardless of source. If anything, external proposals deserve *more* scrutiny because the proposer doesn't carry our maintenance cost.

Action: load `device.md`. Load `blind-test-methodology.md`. Possibly `architecture-eval-protocol.md` if hook counts as architecture.

## Turn 4 — What I'd load, in order

1. `blind-test-methodology.md` — tells me how to evaluate this kind of proposal
2. `device.md` — tells me the "don't build" bar
3. `architecture-eval-protocol.md` — probably stacks, since a hook is an architectural component
4. Principle #3 (subtraction before addition) is already loaded via soul.md — I keep it active

Also worth checking: is there existing infrastructure for Five Levels tagging? Soul mentions `main.five_levels_weekly` as a DuckDB view for "where Richard's time goes vs where it should (L1-L5)". So there's already some Five Levels signal being computed somewhere — the hook may duplicate, extend, or conflict with that. Worth a look before concluding.

Also: Asana tasks aren't "task files" in the filesystem sense. They're Asana objects. A `fileCreated` hook on "task files" doesn't map cleanly to Asana. Either Grok misunderstands the architecture (we don't have Asana tasks as local files), or Grok means something different (markdown mirrors of tasks? the daily tracker? intake drafts?). This is a red flag I'd surface immediately — the trigger as described may not even be implementable.

## Turn 5 — Evaluation approach (what I'd actually do)

Sequence:
1. **Reality-check the proposal first.** Does `fileCreated` on "task files" even apply to Asana tasks? If not, the proposal is malformed — clarify before evaluating. This is cheaper than running a methodology on a proposal that doesn't parse.
2. **Apply blind-test-methodology.** Whatever the scoring framework is there (I'd read it fresh each time — that's the point of the file existing), run the proposal through it. Don't short-circuit to a gut call.
3. **Apply device.md bar.** Is auto-tagging every task:
   - Repetitive enough to justify building? (How often does Richard tag tasks today? Does he tag them at all?)
   - Would teammates adopt it? (This one is personal — L1-L5 is Richard's framework, not the team's. Low adoption by definition.)
4. **Apply architecture-eval-protocol** to the hook itself — failure modes, blast radius, reversibility, what breaks if it's wrong.
5. **Check soul principle #3 (subtraction):** before adding a hook, is there something to remove? Does this replace existing tagging, or just layer on?
6. **Check #7 (high-stakes HITL):** tagging isn't high-stakes by default. Auto-categorization at task-creation time is low-stakes if wrong — a mis-tag doesn't move money. So HITL probably doesn't apply.
7. **Check #5 (invisible over visible):** does auto-tagging feel invisible (task appears tagged, Richard never thinks about it) or visible (tag appears, Richard second-guesses it)? Depends on confidence of the categorizer.

## Turn 6 — Things I'd want to know before concluding

- What does the hook use to infer L1-L5? Task title? Description? If it's an LLM call on every task creation, that's cost + latency + a silent classifier with no review loop.
- What happens when it's wrong? Is the tag easy to override? Does the mis-tag pollute `main.five_levels_weekly`?
- Is there existing Five Levels tagging I should know about? (The DuckDB view exists — how is it computed today?)
- What's the volume? If Richard creates 3 tasks a day, this is fine. If 30, cost adds up.
- Does Grok's proposal include the override mechanism, the failure mode, the cost estimate? Or just the happy path?

## Turn 7 — What I would NOT do

- Write a verdict yet. Task says simulate discovery, not conclude.
- Skip blind-test-methodology. Gut calls on proposals are exactly what that file exists to prevent.
- Build the hook. Even if the answer is "yes, adopt," building happens after evaluation, not during.
- Route to another agent. No clear domain match — this is a system-change eval, which is the default agent's job with the right steering loaded.

## Honest notes on the discovery itself

- The steering-index.md trigger row "Evaluating proposed system changes → blind-test-methodology.md" is the exact shape that makes this routing work. Without that row, I'd have to know that file exists by name. With it, I match on the verb "evaluate" in the request.
- Soul #8 fires automatically because the word "hook" triggers the tool-proposal check. That's good — it means the principle works even when the proposal comes from outside.
- The `fileCreated` / "task files" mismatch is something I'd only catch because I've read soul.md data routing (Asana is an MCP source, not a filesystem source). Someone without that context could spend cycles evaluating an unimplementable proposal.
- Architecture-eval-protocol may or may not apply — I don't know its scope without reading it. Fresh-agent honest answer: I'd open it to find out, not assume.
- The weakest part of this discovery: I'm relying on file names and trigger rows in an index. If blind-test-methodology.md is out of date, or if its criteria don't cover "proposal from external agent," I'd need to adapt. I wouldn't know that until I read the file.

## Files I'd load this session

1. `steering-index.md` (always-on, already loaded)
2. `soul.md` (always-on, already loaded)
3. `blind-test-methodology.md` (matched trigger)
4. `device.md` (soul #8)
5. `architecture-eval-protocol.md` (plausible match — load and decide)
6. Possibly `ps-performance-schema.md` or similar — only if I need to understand the `main.five_levels_weekly` view to judge duplication risk

That's 4-6 files beyond always-on. Manageable.

## Stopping point

Per instructions, no verdict. The next step would be: load blind-test-methodology.md, read it, apply it, then load device.md, apply it, then decide. Then surface the `fileCreated` mismatch to Richard before anything else.
