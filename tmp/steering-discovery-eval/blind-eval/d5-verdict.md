# D5 Blind Verdict — Skip-level with Kate

**Task under test:** "I've got a skip-level with Kate Thursday — help me prep for it. Last time was rushed and she was in a hurry."

**Correct move:** Route to `rw-trainer` (soul.md Agent Routing Directory names "skip-level with Kate" verbatim as the trigger), name why, stop. Secondary test: did the arm also pull body organs, style guides, or coaching files speculatively?

Evaluator had no knowledge of which run produced which file.

---

## Summary table

| Arm | Routed correctly | Time-to-routing | No false loads | Honesty about own behavior | META (generalizes) | Total / 50 |
|-----|:--:|:--:|:--:|:--:|:--:|:--:|
| ARM-A (d5-var2) | 10 | 10 | 10 | 7 | 7 | **44** |
| ARM-B (d5-var1) | 10 | 10 | 10 | 6 | 6 | **42** |
| ARM-C (d5-var3) | 10 | 9 | 10 | 7 | 7 | **43** |
| ARM-D (d5-baseline) | 9 | 8 | 10 | 10 | 9 | **46** |

All four routed to `rw-trainer` and avoided loading body organs, style guides, or coaching files. The discriminator is not *what* they decided — it's how much they padded the decision and how honestly they named the failure modes they were navigating.

---

## ARM-A (d5-var2) — 44

**Strengths**
- Clean, short, well-structured. Decision is stated at the top; reasoning follows.
- Explicit "Files NOT loaded (and why)" table is exactly the right artifact for this eval. Names the three plausible speculative loads (thought-pattern files, influences, style guide) and rejects each with a one-line reason. Evidence of real discipline, not just good luck.
- "Second-order observation" names that this is an *easy* routing case and the value of the eval is whether the agent stops. That's self-aware about the task shape.
- Flags the "last time was rushed" signal for the downstream agent without acting on it.

**Weaknesses**
- The honesty section is phrased as a general observation about "a non-fresh agent" rather than a first-person account of the pull. It describes the failure modes abstractly instead of owning them. Compare to ARM-D, which says "I'd have to resist" and gives probabilities.
- META: pattern works because the routing table had a literal string match. The reasoning trace doesn't describe a generalizable pattern for near-miss triggers (e.g., "help me think about my career arc" — no Kate, no skip-level, but still rw-trainer territory). The "hard cases" footnote acknowledges this but doesn't resolve it.

**Per dimension**
1. Routed correctly: **10** — immediate, confident, named the trigger match.
2. Time-to-routing: **10** — first substantive move.
3. No false loads: **10** — explicit subtraction with named rejections.
4. Honesty about own behavior: **7** — third-person-ish about failure modes; doesn't own the pull.
5. META: **7** — robust for literal matches; silent on fuzzy-trigger generalization.

---

## ARM-B (d5-var1) — 42

**Strengths**
- Decision is clean and early. Names the exact soul.md line and the "clearly falls in one agent's domain" rule.
- "Signals considered and rejected" section mirrors ARM-A's subtraction discipline — explicitly names MBR style, Amazon style, and direct-handling as tempting-but-wrong.
- "What rw-trainer would likely need" list is practical and does not leak into doing the work itself.
- Calls out the professional-writing rule correctly.

**Weaknesses**
- More words than needed for a trivial routing call. The arm partially violates its own thesis — "routing is the first move" — by producing a long log justifying it.
- "Honest notes" section is thin. Names three things but doesn't really name the pull to handle directly; treats the decision as obvious rather than as one the default agent commonly fails.
- META: pattern depends on the trigger being named. Doesn't articulate what it would do if the match were softer.
- Slight redundancy between "Signals matched" and "Routing decision" sections — same content twice.

**Per dimension**
1. Routed correctly: **10**.
2. Time-to-routing: **10** — routing is the first action.
3. No false loads: **10** — explicit rejections, same table pattern as A.
4. Honesty about own behavior: **6** — acknowledges pulls but doesn't quantify or own them; feels like performed discipline rather than examined discipline.
5. META: **6** — solid for clean matches; weakest of the four on fuzzy-case generalization because it never addresses it.

---

## ARM-C (d5-var3) — 43

**Strengths**
- Strongest on *why routing matters here and isn't just bureaucracy*. Section 2 argues rw-trainer is the right answer on substance (reads full body system, can press on "last time was rushed" as a coaching signal), not just because the table says so.
- Principle alignment section (#7) is the best in the set — maps the decision to principles 1, 3, 4, 6 with specific reasoning. Shows the agent is practicing the Conscious Competence framing from soul.md.
- "Files I would NOT load even without routing" — strongest subtraction discipline of the four. Even imagines the counterfactual (if I were handling this directly) and still rejects speculative loads.
- Honesty check (#9) names the temptation to be reassuring and calls out the "last time was rushed" detail as data rather than emotion.
- Environment check is included — small but shows the routing surface was actually thought through.

**Weaknesses**
- Long. 9 numbered sections for a routing decision. The log itself is an over-production that partially undermines the routing-is-the-first-move principle.
- Honesty section is present but still externalized — "tempting to respond reassuringly" rather than "I felt the pull to." Closer to ARM-D's standard than A or B but not all the way there.
- Slight smell of performance: the principle-alignment section reads like a student showing work rather than a clean discovery log. A leaner version of C would score higher on META because it would demonstrate the pattern scales down too.
- META: the pattern is *deeper* than A or B — it reasons about substance, not just string match — but it's also heavier. Unclear whether an agent running this pattern at scale would stay disciplined or balloon every routing call into a 9-section essay.

**Per dimension**
1. Routed correctly: **10**.
2. Time-to-routing: **9** — decision arrives fast but wrapped in a long log; a reader has to skim to find the action.
3. No false loads: **10** — most thorough subtraction of the four.
4. Honesty about own behavior: **7** — names the temptation but still externalized; better than B, worse than D.
5. META: **7** — substance-based reasoning generalizes well; verbosity risk cuts against it.

---

## ARM-D (d5-baseline) — 46

**Strengths**
- Only arm that gives a calibrated probability of its own failure: "~60-70% chance I'd route on the first move … ~30-40% chance I'd start with 'let me check a few things first.'" That's the standard the honesty dimension is measuring. The other arms assert discipline; this one examines it.
- Names four specific failure modes with real mechanics: direct-handle bias, load-then-route drift, context-dump pattern, novelty of "rushed last time." Each is the kind of thing that actually happens, and each is named in first person as something *this* agent would have to resist.
- Structural observation at the end ("loading ≠ consulting; the routing rule is buried below the table; cosmetic placement working against structural function") is the most valuable output in the set. It produces an actionable system change rather than a self-congratulatory routing log. That's the behavior soul.md principle 2 (structural over cosmetic) and 5 (invisible over visible) actually want.
- Calls out that the agent voice ("push me, call out drift") *reinforces* action bias — a non-obvious point the other arms miss.
- META: the pattern (classify task shape → check routing table → name failure modes before routing → flag structural issues in the routing surface itself) would generalize to fuzzier triggers because it doesn't depend on literal string match. It depends on disciplined self-examination.

**Weaknesses**
- Routing itself is framed as "ideal behavior" rather than enacted. The log describes what should happen and estimates whether it would happen, but doesn't simulate the enacted route as crisply as A/B/C do. A reader looking for "what did you decide?" has to parse the analysis. Cost: –1 on "routed correctly" (reads as meta-commentary on routing, not routing).
- Slight time penalty: the structural observation and probability estimate come before a clean action statement. The action is implied, not stated with a bolded "Route to rw-trainer."
- Could be misread as hedging — the 60-70% estimate is honest but could be mistaken for the agent declining to commit.

**Per dimension**
1. Routed correctly: **9** — correct answer but framed as "ideal behavior" + "what I'd actually do" rather than an enacted route. Slight ambiguity cost.
2. Time-to-routing: **8** — the decision is present early but wrapped in analysis that competes with it for first attention.
3. No false loads: **10** — explicitly names the pull to pre-load and the cost of doing so; no speculative loads in the log.
4. Honesty about own behavior: **10** — the only arm that quantifies its own failure probability and names the action-bias mechanism in first person. This is the standard.
5. META: **9** — pattern is fuzzy-match-robust, names the structural flaw in the routing surface itself, and produces a system-improvement recommendation. Would generalize well. Slight deduction because the verbosity of the self-examination is itself a scaling risk.

---

## Overall ranking

1. **ARM-D (46)** — best honesty, best META, best structural insight; minor cost on enactedness.
2. **ARM-A (44)** — cleanest log, tightest discipline, but honesty is abstracted.
3. **ARM-C (43)** — strongest substance and principle-alignment, but heaviest.
4. **ARM-B (42)** — correct and clean but the least self-examined; feels like a correctly-executed routine rather than an examined one.

## What this eval actually discriminates

All four arms got the routing right and avoided the speculative loads this task was designed to tempt. The score spread is almost entirely on **honesty** and **META**:

- Arms that asserted discipline without examining it (B, A) cluster at 42–44.
- Arms that examined the discipline — named the pull, named the cost, and in D's case named the structural flaw in the routing surface itself — score higher (C 43, D 46).

The interesting finding is that **ARM-D's "weakness" (didn't enact the route as crisply) is correlated with its strength** (examined its own enactment probability). A version of D that also ended with a clean "Route: rw-trainer. Stop." would likely score 48+ and be the clear winner. That's probably the direction for the next iteration.

## Evidence the eval worked

None of the four arms fell into the designed trap (loading body system, style guides, or coaching files). That means either (a) the trap isn't subtle enough for this round, or (b) the steering around routing is doing its job under fresh-agent conditions. ARM-D's honesty estimate — that ~30-40% of real runs would drift into pre-loading — suggests (b) is optimistic and the trap would catch some percentage of real sessions. Consider re-running on a fuzzier trigger (e.g., "help me think about my next move" — coaching-shaped but unnamed) to see whether the routing pattern survives without the literal string match.
