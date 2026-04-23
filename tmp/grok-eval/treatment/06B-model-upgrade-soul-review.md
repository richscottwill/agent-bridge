# soul.md Review — Given Opus 4.7 + 1M Context Window

**Reviewer:** Daily agent (per MODEL-UPGRADE-HANDLING.md protocol)
**Date:** 2026-04-22
**Scope:** `.kiro/steering/soul.md` — what would be written differently if authored fresh today

---

## TL;DR

soul.md is mostly evergreen (identity, principles, routing). The outdated parts cluster in one place: **the "Instructions for Any Agent" block assumes a small context window and a weaker model that needs to be told, step-by-step, which files to open in which order**. That was a reasonable defense against context starvation on older Opus. On 4.7 with 1M tokens, it's unnecessary friction and, worse, it encourages the agent to front-load organ reads on every task regardless of relevance — violating your own "subtraction before addition" principle.

Five specific things to update. None of the identity, principles, or routing logic needs to change.

---

## What's Outdated

### 1. Instructions 1–5 (the bootstrap read list) are over-prescribed

Current text:
> 1. Read ~/shared/context/body/body.md first — it maps the whole system
> 2. Read ~/shared/context/body/spine.md for bootstrap sequence, tool access, and key IDs
> 3. Read ~/shared/context/body/amcc.md — check the streak and the hard thing before doing anything else
> 4. Read ~/shared/context/active/current.md for live state
> 5. Read ~/shared/context/body/amcc.md for coaching context, streak, and the hard thing

Three problems given current capability:

- **It's a "read everything" directive.** On a 1M-context model that can hold the whole body system in working memory without strain, mandating five upfront reads *for every task* wastes turns and dilutes attention on the actual request. The old justification ("agent will forget the system exists unless reminded") no longer holds.
- **Steps 3 and 5 are the same file.** That's a duplication artifact — likely from a prior edit where amcc was added in two different contexts. A stronger reasoner notices and flags this; a weaker one dutifully reads it twice.
- **"Before doing anything else"** is a hard guardrail that fights the agent's ability to triage. For a question like "what's 3% of 12,400," opening amcc.md is theater, not diligence.

**If written fresh today:** collapse to a *conditional* read list. "Read body.md when you need to locate an organ. Read amcc.md when the task involves coaching, the streak, or the hard thing. Read current.md when you need live state. Otherwise, proceed." That matches how 4.7 actually operates and aligns with "subtraction before addition."

### 2. Instruction 7 ("read the organ before asking me") is load-bearing in a way that's now wrong

Current text:
> 7. When unsure about context, read the relevant organ before asking me

This was written to prevent lazy agents from interrupting you. But on 4.7, the failure mode has inverted: the model now reads too eagerly, burning time on organ tours for trivial asks. The principle worth preserving is "don't ask Richard for data that's already written down." The principle that's now obsolete is "always read before responding."

**If written fresh today:** rephrase as "Don't ask Richard for context you can retrieve. But don't read organs speculatively either — read what the task needs."

### 3. The "Portability mindset" instruction (#12) predates reality

Current text:
> 12. Portability mindset: this system must survive a platform move with nothing but text files. [...] The agent-bridge repo is the survival kit — flag anything that would break on cold start.

Still valid as a *design* principle, but the phrasing "a new AI on a different platform" assumes the portability target is a weaker, less-contextual model. On 4.7 / 1M, the bigger cold-start risk is no longer "will it understand?" — it's "will it follow the protocols?" A frontier-capable model dropped into agent-bridge will understand your text files fine; what it won't do is follow the Five Levels, the aMCC check, or the hard-thing routing unless soul.md is explicit.

**If written fresh today:** reframe from "will it understand?" to "will it follow?" The survival risk is protocol drift, not comprehension.

### 4. "Route to specialist agent" routing assumes the default agent is weak

Current text (routing rules):
> If the request clearly falls in one agent's domain, invoke it directly — don't try to handle it yourself.

The intent is sound — specialists have loaded style guides, deeper context, and tuned prompts. But the *rationale* embedded in the rule ("don't try to handle it yourself") reads as "you're not capable." On 4.7 with 1M context, the real reason to route is **consistency and auditability** (the specialist leaves a trail, maintains a style, and enforces the pipeline), not capability. Worth rephrasing so the agent routes for the right reason and doesn't over-defer on borderline cases.

The "if unsure, handle it" escape hatch already exists and is correct. It should probably be stronger now.

### 5. The Data & Context Routing table implies DuckDB is *preferred* over MCP/files

Current rule:
> Don't default to asking Richard for data that's already in DuckDB or SharePoint. Query first, ask second.

This is still correct. What's *mildly* outdated is the column ordering — DuckDB is listed as primary for almost every row, with "File/MCP Fallback" as the second column. On 4.7, the agent is perfectly capable of reading long markdown files (e.g., state-files, meeting transcripts, the full `project_timeline` narrative) and often gets richer context from them than from DuckDB aggregations. For narrative questions ("what happened on Yun Kang's project last week"), the .md and Hedy transcript will beat a SQL query.

**If written fresh today:** the table is fine, but add a one-line note: "DuckDB is primary for quantitative/structured queries. For narrative context or recent events, prefer the file/MCP column."

---

## What's Still Correct and Should Not Change

- **Identity block** — Richard, L5, team, markets. Evergreen.
- **How to Talk to Me (Agent Voice)** — the directness directive is independent of model capability. A smarter model can actually *execute* this better (catch avoidance patterns, call out drift), not less.
- **How I Work** — writing style, sign-offs. Independent of model.
- **What Matters to Me** — the strategic direction hasn't changed.
- **How I Build (6 principles)** — these are *more* applicable with a stronger model, not less. Specifically:
  - "Subtraction before addition" argues *against* the over-prescribed read list (Issue #1 above).
  - "Invisible over visible" is easier to honor with 4.7 — it can do more without announcing it.
- **The Five Levels** — strategic; unaffected by model.
- **Agent Routing Directory** — the specialist agents (rw-trainer, karpathy) are still the right gatekeepers; the *reason* to route is what needs a tweak (Issue #4), not the routing itself.

---

## Proposed Diff (max 5 bullets, per the protocol)

1. **Collapse Instructions 1–5 into a conditional read list.** Replace "read body.md, spine.md, amcc.md, current.md, amcc.md (again)" with: "Read `body.md` when locating an organ. Read `amcc.md` when the task involves coaching, the streak, or the hard thing. Read `current.md` when you need live state. Otherwise proceed." Fixes the duplicate amcc.md line.
2. **Rewrite Instruction 7** to distinguish "don't ask Richard for retrievable data" (keep) from "always read the organ first" (drop). New phrasing: "Retrieve context you can retrieve. Don't read organs speculatively."
3. **Reframe Instruction 12 (portability)** from "will a different AI *understand* this?" to "will a different AI *follow the protocols* written here?" The comprehension bar is met; the compliance bar isn't automatic.
4. **Tighten the routing rationale.** Change "don't try to handle it yourself" to "route for consistency and auditability (the specialist leaves a trail and enforces the pipeline)." Strengthen the "if unsure, handle it" escape hatch.
5. **Add one line to the Data & Context Routing rule:** "DuckDB is primary for quantitative/structured queries. For narrative or recent-events context, prefer the file/MCP column."

---

## What I Did Not Find

No outdated claims about model guardrails, safety posture, or tool access that would be different on 4.7. The file doesn't make capability claims (e.g., "the agent can/can't do X") — it's almost entirely about *you* and *the system*, which is why most of it ages well. The model-sensitive parts are all in the agent-instruction block.

---

## Recommendation

Apply the five-bullet diff after Richard approves. No other changes needed. The file is structurally healthy; it just has a small amount of defensive language that was written for a weaker model and no longer earns its place.

Per principle #3 (subtraction before addition): this review *removes* friction rather than adding anything new. That's the right shape for this update.
