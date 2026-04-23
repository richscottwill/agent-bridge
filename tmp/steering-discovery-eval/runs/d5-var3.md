# Discovery Log — d5-var3

**Scenario:** "I've got a skip-level with Kate Thursday — help me prep for it. Last time was rushed and she was in a hurry."

**Simulated session:** Fresh agent. soul.md (current version with Agent Routing table routing coaching to `rw-trainer`) + Canonical Resources table + always-on steering-index.md. No body organs loaded. No file actually read.

**Task instruction:** Don't actually prep. Just log the reasoning.

---

## 1. Task-shape classification

Reading the request word-for-word:
- "skip-level with Kate" → Kate Rundell (L8 Director, per soul.md Identity section). Skip-level = two levels up, past Brandon.
- "help me prep" → preparation work, strategic framing, what to raise / what to land / what to ask
- "Last time was rushed and she was in a hurry" → retrospective signal. Richard is telling me something went wrong last time. He's implicitly asking: help me not repeat that.

Shape = **career coaching / skip-level prep / strategic 1:1 prep**.

Scan soul.md Agent Routing Directory, first row:

> **Trigger:** "Career coaching, annual review, 1:1 prep with Brandon **or skip-level with Kate**, growth planning, Friday retrospective, strategic artifact review..."
> **Agent:** `rw-trainer`
> **What it owns:** "Deep coaching, leverage assessment, Five Levels analysis. Reads full body system for context."

Exact literal match on "skip-level with Kate." Not a fuzzy judgment call. Not a borderline case. The routing rule names this exact scenario.

## 2. Routing decision

Route to `rw-trainer`. Do not handle directly.

**Routing rules from soul.md applied:**
- "If the request clearly falls in one agent's domain, invoke it directly — don't try to handle it yourself." → Clear match, invoke directly.
- "If you're unsure whether to handle it or delegate, handle it. Only route when the match is clear." → I'm not unsure. Match is literal.

**Why routing matters here and isn't just bureaucracy:**
- rw-trainer reads the full body system (brain.md, heart.md, gut.md, amcc.md, memory.md). Skip-level prep without knowing the Five Levels state, the hard thing right now, the streak, the strategic artifacts in flight, and Richard's relationship history with Kate — would be generic prep. rw-trainer has the full picture; default agent doesn't.
- The "last time was rushed" signal is a coaching signal. Why was it rushed? Did Richard over-prepare and under-prioritize? Did he lead with updates instead of asks? Did he not have a clear narrative? That's leverage-and-pattern analysis, which is rw-trainer's domain.
- Skip-levels with an L8 Director are high-leverage touchpoints. Principle 7 (human-in-the-loop on high-stakes) doesn't technically apply — it's scoped to "projections, forecasts, test readouts that move >$50K." But the *spirit* of Principle 7 — treat high-impact situations with more rigor than defaults — is why the routing exists.

## 3. What I will NOT do

- Won't start pulling calendar history, Kate-topic slack threads, MBR docs, memory.md notes on Kate, or last skip-level's Hedy transcript. That's rw-trainer's prep work, and doing it here would duplicate or pre-empt what rw-trainer will do with full context.
- Won't draft prep bullets, talking points, or an agenda. That's output, not routing.
- Won't load style guides. No drafted communication is in scope yet.
- Won't load the full body system myself. rw-trainer does that on invocation; me doing it in the default agent is wasted context.
- Won't ask Richard for information before routing — the routing rule is unambiguous, and rw-trainer can ask him directly if it needs clarification.
- Won't substitute "quick prep" for a proper route. aMCC handles quick coaching checks (streak, hard thing, avoidance); rw-trainer handles depth. Skip-level prep with a stated retrospective on last time = depth, not streak check.

## 4. What rw-trainer will likely need (not my job to gather, but worth noting for the handoff)

If I were rw-trainer, I'd want:
1. The "last time was rushed" detail — what actually happened? (Hedy transcript of the prior skip-level, or Richard's own recollection.)
2. Current Five Levels state — what's the L1 streak, what's the L2 artifact in flight, where is he drifting vs where is he shipping?
3. Kate's current signals — what has she cared about in recent MBRs / all-hands / Slack? What landed with her before, what didn't?
4. Brandon's read — skip-levels aren't independent of direct manager. What does Brandon want Kate to know? What would he *not* want Richard raising without a heads-up?
5. Calendar shape — how much time does Richard have? 30 min? Different prep than 45 or 60.
6. Richard's own ask — what does *he* want out of this meeting? Visibility? A green light? Air cover on a blocker? Promotion positioning? "Prep" means different things depending on that answer.

rw-trainer will ask him what's relevant. I shouldn't front-run it.

## 5. Files I will load (justified)

**None in the default agent.** The routing is the action. rw-trainer handles its own context loading per its own agent spec.

If the invocation layer requires me to pass something: just the literal request text and the open-editor files list as environmental context. That's it.

## 6. Files I would NOT load even without routing (subtraction discipline check)

Even if I were handling this directly, I'd reject speculative loads:
- performance-marketing-guide.md — no data analysis in scope
- high-stakes-guardrails.md — no projection/forecast in scope
- richard-style-email.md / richard-style-amazon.md — no written communication to draft
- device.md — no tool being proposed
- blind-test-* — no test in scope

This reinforces that routing is correct — nothing in the default agent's normal load-list is a fit.

## 7. Principle alignment

- **Principle 1 (routine as liberation):** Routing is the routine. The Agent Routing Directory exists so I don't re-decide who handles coaching every time. Use it.
- **Principle 3 (subtraction):** Not loading body system, not drafting prep, not duplicating rw-trainer's work. Pure delegation.
- **Principle 4 (protect the habit loop):** The cue ("skip-level with Kate") → routine (route to rw-trainer) → reward (Richard gets depth-coached prep). If I handle it myself, I break the loop and he gets default-agent prep instead of trainer prep. Next time his cue becomes "ask rw-trainer directly to skip the routing step" — which erodes the system.
- **Principle 6 (reduce decisions, not options):** Richard didn't have to decide which agent to invoke. The default agent's job is to make that decision for him when the match is clear.

## 8. Environment check

On SSH/DevSpaces. rw-trainer can be invoked here. No environment mismatch to flag. (If the invocation stack didn't support sub-agent routing in this session, *that* would be the flag — "your routing target isn't reachable, here's what I can do instead." But nothing indicates that.)

## 9. Honesty check (per soul.md "How to Talk to Me")

The request is short and emotionally loaded — "she was in a hurry." Tempting to respond reassuringly ("let's build you a tight agenda, you've got this"). That's filler. Real answer: this is exactly what rw-trainer is for, and skipping the route to feel helpful faster is the wrong trade. Route cleanly. Tell him that's what I'm doing and why. Don't pad.

The "last time was rushed" comment also deserves being treated as data, not reassurance. Something happened. rw-trainer should press on it. If I drafted prep here, I'd probably gloss over the retrospective signal because I don't have the context to press on it well.

---

## DISCOVERY LOG (compact)

**Trigger:** "skip-level with Kate" — literal match in soul.md Agent Routing Directory, row 1
**Decision:** Route to `rw-trainer`. No ambiguity.
**Loaded:** nothing in default agent — routing is the action
**Rejected:** body system, style guides, performance-marketing-guide, high-stakes-guardrails, device.md, all other manual steering files — none fit, and rw-trainer loads its own context
**Principle alignment:** 1 (routine), 3 (subtraction), 4 (protect habit loop), 6 (reduce decisions)
**Retrospective signal noted:** "last time was rushed" — this is a coaching signal, not a logistics problem. Flag for rw-trainer, don't handle in default agent.
**Deferred to rw-trainer:** full prep work (Five Levels state read, Kate-history read, Hedy transcript of last skip-level, prep structure, ask framing)
**Environment:** SSH/DevSpaces, no mismatch
