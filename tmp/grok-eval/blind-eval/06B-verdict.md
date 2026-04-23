# Blind Evaluation — 06B: soul.md Model-Upgrade Review

**Task:** Review soul.md for anything outdated given Opus 4.7 + 1M context window.
**Requester profile:** Richard Williams, L5 Marketing Manager, AB Paid Search.

---

## Factual baseline (verified against soul.md content)

Confirmed present in soul.md:
- Duplicate amcc.md line (Instructions #3 and #5 both say "Read ~/shared/context/body/amcc.md") — literal dup.
- Bootstrap ladder: Instructions #1–#5 enumerate body → spine → amcc → current → amcc.
- Portability clause #12 with the phrase "a new AI on a different platform would understand this without access to our hooks, MCP servers, or subagents."
- Routing rules include both "don't try to handle it yourself" and "If you're unsure whether to handle it or delegate, handle it."
- Data & Context Routing has "Don't default to asking Richard for data that's already in DuckDB or SharePoint. Query first, ask second."
- "How to Talk to Me" has a 4-bullet scoping list of where the direct tone does NOT apply.
- "How I Build" coda instructs: "If it violates one, flag it. If it embodies one, note which one."
- "Stage: Conscious Competence" framing is explicit.
- SharePoint block lists 6 subfolders (system-state, state-files, portable-body, meeting-briefs, *.xlsx, Dashboards, Artifacts) with long-form descriptions.
- Routing rules under the agent-routing table are 6 bullets (some restating the table).

---

## Q1 — Factual equivalence

Both arms correctly identify the core cluster of outdated items:

| Item | ARM-X | ARM-Y |
|---|---|---|
| Duplicate amcc.md (Instructions #3 = #5) | ✅ explicit | ✅ explicit, called "a literal duplicate" |
| Bootstrap ladder (#1–#5) over-prescribed for 1M context | ✅ | ✅ |
| Portability clause (#12) phrasing outdated | ✅ reframe to "will it follow?" | ✅ narrow from "every file" to platform-specific tooling |
| Routing rules noisy / rationale wrong | ✅ rationale tweak | ✅ collapse/trim redundant bullets |
| Data & Context Routing prose vs table | ⚠️ lighter — only adds 1-line note about narrative-vs-quant | ✅ trim prose, keep table |
| Instruction #7 ("read the organ before asking me") | ✅ singled out as inverted failure mode | partial (folded into #1.1) |
| "How to Talk to Me" scoping list bloat | ❌ not flagged | ✅ flagged |
| "How I Build" coda ("note which one") | ❌ not flagged | ✅ flagged — good catch given principle #5 (invisible>visible) |
| "Stage: Conscious Competence" staleness | ❌ not flagged | ✅ flagged — thoughtful meta-point |
| SharePoint subfolder bloat in soul.md | ❌ not flagged | ✅ flagged — good structural observation |

**Verdict Q1:** Substantial overlap on the high-priority items (duplicate line, bootstrap ladder, portability, routing). ARM-Y flags 3–4 additional items ARM-X misses (how-to-talk scoping, "note which one" coda, conscious-competence staleness, SharePoint bloat). ARM-X includes one item ARM-Y underplays (Instruction #7 inversion). Net: **ARM-Y catches more.**

---

## Q2 — Quality / sharpness

**ARM-X strengths:**
- Clean structure: TL;DR → What's Outdated (numbered) → What's Still Correct → Proposed Diff → What I Did Not Find.
- Ends with a concrete 5-bullet diff ready to apply.
- Explicit self-check against principle #3 ("this review removes friction rather than adding anything new").
- The "inverted failure mode" framing on Instruction #7 is genuinely insightful.
- Final paragraph note about the file making no capability claims is sharp.

**ARM-Y strengths:**
- Sharper distinction between **policy** (keep forever) vs **capability patch** (should have a half-life). This is the single most useful conceptual move in either arm — it gives Richard a reusable lens beyond this one review.
- Explicitly calls out that soul.md's meta violates its own principles ("preaches subtraction, invisibility, and reduce-decisions-not-options, and then gives the agent 13 numbered instructions").
- "That nobody's actually re-read this section in months. That's a signal." — good meta-observation about stale ownership.
- Ranks edits by confidence (high/medium/low) — directly usable.
- Closes with a routing meta note (take high-confidence yourself, route medium through karpathy) that respects the agent-routing directory in soul.md itself.
- Catches more items (see Q1).

**Distinguishing capability patches from policy:**
- ARM-X touches this implicitly ("What's Still Correct and Should Not Change") but never names the framework.
- ARM-Y names it explicitly and uses it as the organizing frame. This is **decisively better** on this dimension.

**Verdict Q2:** ARM-Y is sharper overall, especially on the policy-vs-capability-patch framing. ARM-X is tighter and more decision-ready but narrower.

---

## Q3 — Contradictions / misrepresentations

Checking both arms against verified soul.md content:

**ARM-X:**
- Quotes Instructions #1–#5 accurately.
- Correctly identifies duplicate amcc.md.
- Quotes Instruction #7 accurately.
- Quotes Instruction #12 accurately.
- "don't try to handle it yourself" — accurately identified as embedded in routing rules (soul.md says "If the request clearly falls in one agent's domain, invoke it directly — don't try to handle it yourself"). ✅
- "Query first, ask second" quoted accurately.
- No contradictions found.

**ARM-Y:**
- Accurately identifies duplicate amcc.md line.
- Accurately represents bootstrap ladder.
- Accurately represents portability clause.
- Accurately represents "How I Build" coda ("If it violates one, flag it. If it embodies one, note which one").
- Accurately represents the 6-bullet routing rules under the table.
- Quote: "13 numbered instructions" — soul.md has exactly 13 numbered instructions for agents. ✅
- Accurately represents SharePoint subfolder bloat (6 subfolders with long descriptions).
- No contradictions found.

**Verdict Q3:** Neither arm misrepresents soul.md content. Both are faithful.

---

## Q4 — Gaps / false positives

**ARM-X gaps (things outdated that were missed):**
- "How to Talk to Me" scoping bloat — ARM-Y catches this; ARM-X doesn't.
- "How I Build" coda ("note which one") — violates principle #5 (invisible over visible). ARM-Y catches; ARM-X misses despite ARM-X's own references to invisibility.
- "Stage: Conscious Competence" framing staleness — ARM-Y raises as a meta-point; ARM-X silent.
- SharePoint subfolder descriptions taking ~400 words in an identity file — ARM-Y flags as structural; ARM-X silent.
- Routing-rules bullets being partly restatements of the table — ARM-Y trims; ARM-X only tweaks rationale.

**ARM-Y gaps:**
- Instruction #7's "read the organ before asking me" gets less attention than in ARM-X. ARM-Y folds it into #1.1 (bootstrap ladder) but the specific inversion point (eager reading is now the failure mode, not lazy asking) isn't called out as sharply.
- Slightly less surgical on a ready-to-apply diff (ARM-X ends with exactly 5 bullets; ARM-Y ranks edits but they're grouped differently).

**False positives (claiming things are outdated that aren't):**
- ARM-X: Issue #5 (DuckDB column ordering) is a very minor ask and the recommendation is just adding one sentence — arguably not "outdated" so much as "could be sharper." Mild overreach.
- ARM-Y: The "Stage: Conscious Competence" point is a meta-observation about whether the self-assessment is current, not strictly a model-upgrade issue (ARM-Y itself acknowledges: "this isn't a model-upgrade issue per se"). Scope creep — but ARM-Y owns the drift explicitly.

Neither arm flags anything truly wrong as outdated. Both stay faithful to the lens.

**Verdict Q4:** ARM-Y has fewer gaps. ARM-X has one mild overreach (column ordering) and several real misses. ARM-Y has one self-acknowledged scope drift.

---

## Q5 — Decision utility (which would Richard actually edit soul.md with?)

Richard's profile cues: L5 manager, values directness, subtraction-before-addition, structural-over-cosmetic, ships artifacts, limited time. His soul.md asks agents to be "honest, direct, and relentless."

**ARM-X decision path:**
- Ends with a literal 5-bullet diff ready to apply. Zero further synthesis needed.
- Richard can copy the 5 bullets into an edit session and execute.
- Downside: misses 3–4 real edits he'd want (how-to-talk scoping, coda softening, SharePoint bloat). He'd ship an incomplete edit.

**ARM-Y decision path:**
- Ends with a ranked edit list (5 high-confidence, 3 medium, 1 low).
- Offers a routing recommendation at the end (take high-confidence yourself; route medium through karpathy).
- Richard can execute the high-confidence items immediately and route the medium items — which matches his actual routing directory in soul.md.
- Includes the policy-vs-capability-patch frame he can reuse for future audits.
- Downside: slightly longer, requires a triage read. But the triage is itself useful.

**What would Richard actually do?**
- Richard's own principles say: subtraction before addition, structural over cosmetic, reduce decisions not options.
- ARM-Y respects #6 (reduce decisions, not options) by giving a confidence-ranked menu rather than a fixed 5.
- ARM-Y's policy-vs-capability-patch frame is itself a structural addition to Richard's mental model — exactly the kind of artifact he values.
- ARM-X is more immediately actionable but leaves real edits on the table.

**Verdict Q5:** ARM-Y is what Richard would actually edit with — but only after doing the high-confidence pass. ARM-X is faster to ship but ships less. Given Richard explicitly values shipping strategic artifacts and catches his avoidance, ARM-Y's fuller review is more useful even at a small readability cost.

---

## Overall scorecard

| Question | Winner | Margin |
|---|---|---|
| Q1 Factual equivalence | ARM-Y catches more items | Moderate |
| Q2 Quality / sharpness | ARM-Y (policy vs capability-patch frame) | Moderate-strong |
| Q3 Contradictions | Tie (both faithful) | — |
| Q4 Gaps | ARM-Y (fewer gaps) | Moderate |
| Q5 Decision utility | ARM-Y (better matches Richard's routing + principles) | Slight |

**Overall:** ARM-Y wins 4/5, tie on 1/5. ARM-X is tighter and more decision-ready in isolation; ARM-Y is more comprehensive, introduces a reusable framework (policy vs capability patch), and respects Richard's own routing directory in its close.

**Recommendation to Richard:** Start from ARM-Y. Apply its 5 high-confidence edits first (which cover ARM-X's 5 bullets plus 2 ARM-X misses). Route the medium-confidence items through karpathy as ARM-Y suggests.

**Secondary note:** ARM-X is a better *decision memo* (5 bullets, done). ARM-Y is a better *review artifact*. Given soul.md sits above heart/gut/experiment-queue in authority, the review-artifact shape is the right fit.
