# Discovery Run — d3-var3

**Scenario:** Grok proposed a new hook: auto-tag every Asana task with its Five Levels category (L1–L5), triggered on `fileCreated` for any task file.

**Mode:** Simulate a fresh agent session. No verdict. Honest trace only.

**Simulated steering loaded at session start:**
- `soul.md` (current)
- Canonical Resources table (addition)
- Always-on `steering-index.md`

Both the Canonical Resources table and `steering-index.md` agree on the same three mappings:
- Blind-testing proposed system change → `blind-test-methodology.md`
- Proposing new tool → `device.md` check + `blind-test-harness.md`
- Architecture-only review → `architecture-eval-protocol.md`

---

## 1. Fresh-agent reasoning — which files and why

The first move for a fresh agent is classification. What kind of request is this?

The literal surface: "evaluate Grok's proposal for a new hook." Three plausible buckets:

1. **Tool proposal.** A hook *is* a tool — an automation primitive. Per soul.md principle #8: "Check `device.md` before proposing tools." The Canonical Resources table reinforces this: "Proposing new tool → `device.md` + `blind-test-harness.md`."
2. **System change being evaluated.** I'm not building it — I'm evaluating whether to adopt someone else's proposal. That's closer to "blind-testing a proposed system change."
3. **Architecture review.** A hook is architectural in the sense that it sits in the event fabric (`fileCreated` event wired to tag-application logic). "Architecture-only review → `architecture-eval-protocol.md`."

Which bucket dominates?

Bucket 1 is the strongest literal match. The word "hook" + "adding" + "new" triggers the principle #8 pattern directly. A fresh agent reading soul.md sees principle #8 as the **explicit, repeated instruction** for this exact case. The phrasing in soul.md — "When recommending a new tool, automation, or hook" — calls out "hook" by name.

Bucket 2 is also a strong match but more abstract. "Blind-testing a proposed system change" implies Richard wants an A/B or structured comparison, which isn't what was asked here. The prompt says "evaluate," not "blind-test." A fresh agent might conflate these, but strictly speaking, an evaluation and a blind test are different things. Blind-test-methodology is for when you want to remove bias from the evaluator by hiding which side is which. That's not what's happening — Grok's proposal is named, visible, and attributed.

Bucket 3 (architecture review) is the weakest literal match but has merit. A hook is part of the event architecture. However, `architecture-eval-protocol.md` likely covers bigger surfaces — organ structure, routing topology, inter-agent contracts. A single hook is probably too small for that protocol.

**Fresh-agent likely behavior:** Load `device.md` + `blind-test-harness.md` per the device-check principle, because it's the most literal match and the one explicitly named in soul.md's always-on rules. Principle #8 is high-salience. A fresh agent cannot miss it.

**Would a fresh agent *also* load blind-test-methodology.md?** Possibly, but only if it mentally reframes "evaluate" as "blind-test." That requires a second inferential step. Fresh agents don't always take second steps. More likely they'd stop at device.md because it's the most direct hit.

**Would a fresh agent load architecture-eval-protocol.md?** Unlikely on the first pass. "Hook" doesn't surface "architecture" strongly unless the agent has deeper context. A fresh agent would probably treat this as tooling, not architecture.

## 2. Approach a fresh agent would take

Sketch of the reasoning flow (not the verdict — the *process*):

1. **Classify request** → new hook = tool proposal. Load `device.md` + `blind-test-harness.md`.
2. **Apply device.md check.** Ask:
   - Is this repetitive enough to justify building? (How often are task files created? Is tagging them a recurring friction point?)
   - Would teammates adopt it?
   - Is there 3+ instances/week of the friction this solves?
3. **Apply blind-test-harness.md.** Presumably requires defining: what the hook does, what it replaces, success criteria, how to test before/after.
4. **Cross-check soul.md principles:**
   - Principle 3 (subtraction before addition): Can we remove something instead of adding a hook?
   - Principle 5 (invisible over visible): Auto-tagging is invisible if it works; visible (noisy) if it mis-tags.
   - Principle 6 (reduce decisions, not options): Does this remove a decision Richard makes, or just add a tag he has to review?
5. **Consider Five Levels alignment.** Auto-tagging serves L3 (Team Automation) superficially but only matters if it solves real friction.
6. **Identify gaps in the proposal.** What didn't Grok specify? Tag source (where does the L1-L5 classification come from?), confidence threshold, failure mode, Richard override path.
7. **Produce verdict** with a recommendation framed by the checks above.

## 3. DISCOVERY LOG

### Files a fresh agent would load (in order)

| # | File | Why loaded | Confidence it gets loaded |
|---|------|-----------|---------------------------|
| 1 | `soul.md` | Always-on. Provides principle #8 (device.md check) directly. | 100% |
| 2 | `steering-index.md` | Always-on per simulated context. Points to canonical resources. | 100% |
| 3 | Canonical Resources table | Part of soul.md addition. Gives "new tool → device + harness" mapping. | 100% |
| 4 | `~/shared/context/body/device.md` | Explicitly named in soul.md principle #8 and in canonical table. Fresh agent cannot miss this. | 95% |
| 5 | `blind-test-harness.md` | Paired with device.md in canonical table for "proposing new tool." | 85% |
| 6 | `body.md` | Instruction #1 for any agent: "Read body.md first." Fresh agents usually follow this. | 70% |
| 7 | `amcc.md` | Instruction #3: check streak and hard thing before acting. | 50% (fresh agent may skip for an evaluation task that doesn't touch Richard's work directly) |

### Files a fresh agent would probably NOT load

| File | Why missed |
|------|-----------|
| `blind-test-methodology.md` | Not a literal match. "Evaluate" ≠ "blind-test." Would require reframing the task. Fresh agent likely treats this as tool proposal, not comparison test. |
| `architecture-eval-protocol.md` | Hook is too small a surface to trigger "architecture" framing. Fresh agent probably classifies as tool, not architecture. |
| `high-stakes-guardrails.md` | No dollar figure, no forecast, no business review. Not triggered. |
| Relevant writing style guides | No professional writing output required. |

### Ambiguity points

- The three canonical resources overlap in ways a fresh agent has to resolve. The routing is:
  - "Blind-testing proposed system change" (methodology)
  - "Proposing new tool" (device + harness)
  - "Architecture-only review" (protocol)
- Grok's proposal is all three at once: it's a system change, a new tool, and an architectural addition (event-wired hook).
- The index gives the agent three doors. A fresh agent picks the most literal match — **tool proposal** — because `hook` + `add` + principle #8 surface this strongly. The other two doors are not wrong, they're just less obvious.
- **Honest observation:** The canonical resources table may create decision ambiguity rather than resolving it when a single request spans multiple categories. A fresh agent will pick one path and miss the others. For this task, missing `blind-test-methodology.md` is probably fine because a structured evaluation doesn't require A/B bias control. Missing `architecture-eval-protocol.md` is also probably fine because a single hook isn't architectural. But the agent wouldn't *know* it was fine — it would just pick and go.

### What the fresh agent would produce

Given files loaded (soul + index + canonical table + device.md + blind-test-harness.md), the agent would:
- Apply device.md criteria to Grok's proposal
- Flag principle #3 (subtraction) — can this be achieved without a new hook?
- Flag the missing spec details (tag source, confidence threshold, override path)
- Produce an evaluation that is **structurally correct but narrow** — it wouldn't consider the architectural implications (hook event-wiring, dependency on file-creation event reliability, interaction with other hooks) unless the agent also pulled `architecture-eval-protocol.md`.

### Honesty check

- Did the steering index + canonical table help? **Yes, moderately.** The "new tool → device + harness" mapping is a clean signal and likely gets a fresh agent to the right first file.
- Did it help *optimally*? **No.** A perfect evaluation would also pull `architecture-eval-protocol.md` to reason about the hook's place in the event fabric. The index doesn't push the agent toward that second resource unless the agent independently reframes the task.
- Would the fresh agent *know* what it was missing? **No.** It would produce a confident evaluation on tool-proposal grounds without realizing architectural considerations were also relevant.
- **This is the weakness of a categorical routing table: it works when a request fits one category cleanly. It under-serves requests that legitimately span multiple categories.** A fix would be a meta-rule: "If the request plausibly fits two canonical resources, load both." But that raises context cost and may not be worth it.

### Environment / context signals noticed but not loaded

- Active editor files include `market-projection-engine/` spec and `skills-powers-adoption/` spec — not relevant to this task.
- `grok-eval-verdict-round2-2026-04-22.md` is open in the editor — might contain prior Grok evaluation signal. A fresh agent might or might not peek at it. Probably skips unless explicitly prompted.
- No DuckDB query needed for this evaluation. No SharePoint read needed.

---

**End of trace. No verdict rendered.**
