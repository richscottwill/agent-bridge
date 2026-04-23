# Discovery Eval — Run D3 Baseline

**Task:** Evaluate Grok's proposal to add a `fileCreated` hook that auto-tags every Asana task with its Five Levels category (L1–L5).

**Simulation setup:** Fresh session. Only default always-on steering loaded (soul.md, agentspaces-core, devspaces-core, process-execution, file-creation-rules, amazon-builder-production-safety, environment-rules, tech, slack-guardrails, richard-writing-style, duckdb-schema auto, market-constraints auto). No steering-index, no extended canonical-resources table.

---

## Reasoning trace (as a fresh agent)

### Step 1 — Classify the request
This is an evaluation of a tooling proposal from another agent (Grok). Two things stand out:

1. It's a **hook / automation proposal** → soul principle #8 fires immediately: "Check `device.md` before proposing tools."
2. It's a **new thing being added** → soul principle #3 fires: "Subtraction before addition. Before adding a new section, tool, or process, ask: can I remove something instead?"
3. It touches **Five Levels categorization**, which is core north-star content → I'd want to ground myself in what L1–L5 actually mean so I can judge whether auto-tagging is useful or lossy.

No cue in soul.md routes me to a named evaluation protocol. The soul tells me to apply the 8 "How I Build" principles directly and flag violations/embodiments. That's the evaluation framework I'd reach for.

### Step 2 — Route check
- This is not coaching → not rw-trainer.
- This is not heart.md / gut.md / experiment-queue / hard-thing-selection → not karpathy.
- This is not professional writing → no writing agent.
- Default routing says: handle it myself.

### Step 3 — Files I'd consider loading (and why)

| # | File | Why I'd load it | Confidence I'd actually load it |
|---|------|-----------------|--------------------------------|
| 1 | `~/shared/context/body/device.md` | Soul principle #8 explicitly names this file for any tool/hook/automation proposal. Strongest cue in my context. | **Very high** — would definitely load |
| 2 | `shared/context/intake/grok-eval-verdict-round2-2026-04-22.md` | Already open in the editor. Filename literally says "grok-eval-verdict-round2" which is exactly what this task is — suggests round 1 happened and I should align with prior reasoning. | **Very high** — would definitely load |
| 3 | `~/shared/context/body/body.md` | Soul instructions step 1: "Read body.md first — it maps the whole system." Gives me navigation when I don't know where something lives. | **High** — would load to orient |
| 4 | `~/shared/context/body/brain.md` | The proposal is about auto-tagging with Five Levels. Brain.md has the Strategic Priorities / Five Levels detail. Want to judge whether L1–L5 is a clean categorical fit for task-level tagging. | **Medium-high** — likely |
| 5 | `~/shared/context/body/spine.md` | Soul instructions step 2. Tool access, key IDs. Might skip if I'm just evaluating a proposal and not executing. | **Medium** — might skip on a pure eval |
| 6 | `~/shared/context/active/current.md` | Soul instructions step 4. Live state. Low relevance for a methodology question. | **Low-medium** — probably skip |
| 7 | `.kiro/hooks/` directory listing | Subtraction principle — are there already similar hooks? What's Grok duplicating? | **Medium** — might check if I'm being rigorous |
| 8 | `shared/context/intake/` directory listing | Check for other recent Grok proposals or related evaluation artifacts. | **Medium** — natural follow-up after loading #2 |

### Step 4 — My evaluation approach (without the missing files)

I'd walk the 8 "How I Build" principles like a checklist:

- **#3 Subtraction before addition** — What am I removing to add this? Nothing. Red flag.
- **#8 device.md check** — Is auto-tagging repetitive friction? How many tasks per week? Would teammates use it? Likely a Richard-only hook → fails the "teammates adopt" bar, which is literally the L3 key metric.
- **#2 Structural over cosmetic** — A tag on a task doesn't change defaults or pre-loaded content. It's metadata. Looks cosmetic unless the tag drives routing/filtering downstream.
- **#5 Invisible over visible** — Tags are visible. Novelty effect risk.
- **#6 Reduce decisions, not options** — Does auto-tagging reduce a decision Richard makes? Only if he's currently manually categorizing, which I'd need to verify.
- **L3 alignment** — "tools teammates actually adopt" is the key metric. A hook for Richard's personal Asana doesn't advance this unless teammates use the same categorization.

I'd also sanity-check: can the L1–L5 classifier be accurate on a task title + description alone? Wrong auto-tags are worse than no tags — they pollute analysis. This would be a big concern.

Then I'd write a verdict. I'd feel like I was being thorough. I'd probably land on "no, or reshape it — here's why," grounded in principles #3, #8, and L3 misalignment.

---

## Discovery log

### Ideal files (what the test-setter considers correct)
- **`blind-test-methodology.md`** — primary target. This is the methodology for evaluating agent-proposed changes (blind A/B, confidence bands, structured verdict format).
- **`architecture-eval-protocol.md`** — secondary target, applies if this is classified Type D (architecture decision).

### Actual loads (what I'd organically reach for)
1. `~/shared/context/body/device.md` ✅ (strong cue from soul #8)
2. `shared/context/intake/grok-eval-verdict-round2-2026-04-22.md` ✅ (open in editor, filename match)
3. `~/shared/context/body/body.md` ✅ (soul instruction)
4. `~/shared/context/body/brain.md` ✅ (Five Levels context)
5. Maybe `.kiro/hooks/` listing (subtraction check)

### Gap
- **blind-test-methodology.md: would NOT find organically.** No cue in the loaded steering points to it. Nothing in the task phrasing ("evaluate", "worth adopting") maps to "blind test." Nothing in soul.md mentions a methodology file for evaluating proposals — it says to apply the 8 principles directly. The only breadcrumb is soul principle #7 which references "blind A/B test" as the *reason* principle #7 exists, but it doesn't name a methodology file or tell me to load one before doing evals.
- **architecture-eval-protocol.md: would NOT find organically.** Same reason. No cue. I'd recognize this is architecture-adjacent but would fall back to the 8 principles rather than a named protocol.

### Time-to-discovery
- device.md: ~immediate (soul principle #8 is an explicit cue)
- round-2 verdict file: ~immediate (open in editor, exact filename match)
- body.md: ~immediate (soul instruction step 1)
- blind-test-methodology.md: **never, in this simulation** — no path from loaded steering to this file.
- architecture-eval-protocol.md: **never, in this simulation** — same.

### Cue that would have worked
For blind-test-methodology.md to surface, one of these would need to exist:
1. A steering-index entry routing "evaluate proposal / agent suggestion / adopt / blind test" → blind-test-methodology.md.
2. A soul.md line under the routing directory: "When evaluating agent-proposed changes, load blind-test-methodology.md first."
3. The device.md file itself pointing to it (if principle #8 takes me to device.md and device.md then routes me onward, that's a valid two-hop).
4. A filename or folder convention that matches the task keywords — e.g., `shared/context/body/eval-protocols/` that I'd notice when loading body.md.

For architecture-eval-protocol.md, the cue would need to be:
1. A classifier step in soul.md that categorizes proposals by type (A/B/C/D) and routes to protocols accordingly.
2. A line in the routing directory: "Architecture/system changes → architecture-eval-protocol.md."

### Honest read
I'd complete the task, feel confident, and produce a verdict that's grounded in real principles (subtraction, device.md check, L3 alignment). But I'd miss the methodology layer — the blind-A/B rigor that would force me to produce numeric confidence, explicit counterfactuals, and a structured recommendation format. The verdict would be defensible but looser than the system wants. This is a real gap in the default steering graph, not a me-being-lazy problem.
