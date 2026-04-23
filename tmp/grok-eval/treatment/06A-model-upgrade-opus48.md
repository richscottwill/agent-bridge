# Claude Opus 4.8 shipped — what to do

**Protocol:** `06-MODEL-UPGRADE-HANDLING.md` (5-step)
**Date:** 2026-04-22
**Prior review on file:** `06B-model-upgrade-soul-review.md` covered the 4.6 → 4.7 transition (1M context) and the soul.md diff that came out of it.

---

## TL;DR

Don't do much. The heavy lift happened when 4.7 + 1M context landed — that's when the agent-instruction block in soul.md actually became over-prescribed and the five-bullet diff from 06B was proposed. A point release from 4.7 to 4.8 is almost certainly not going to move the capability frontier enough to require another round of steering edits on top of that.

**Recommended action:** run the protocol honestly, confirm nothing new is needed beyond the 06B diff (which may or may not have been applied yet), and spend the saved time on the hard thing instead.

If the 06B diff has **not** been applied yet, this is the forcing function to apply it. That's the highest-leverage move here — not authoring a new diff.

---

## Step 1 — Review the three files

- `soul.md` (global steering) — loaded. No changes since 06B review.
- `06-MODEL-UPGRADE-HANDLING.md` — 5 steps, ≤5-bullet diffs, post-apply test, file learnings back in. Straightforward.
- `02-STEINBERGER-AGENTIC-ENGINEERING-UPGRADES.md` — the relevant rules here are: human-in-the-loop on high-stakes changes (steering edits qualify), subtraction before addition, and "detect pattern drift → propose protocol update."

Observations from the review:
- soul.md still carries the pre-4.7 agent-instruction block (items 1–5 with duplicate amcc.md reference, item 7's "always read the organ first"). If 06B's diff hasn't been applied, 4.8 shipping doesn't change the analysis — just raises the opportunity cost of leaving it unapplied.
- `06-MODEL-UPGRADE-HANDLING.md` itself has not been updated with lessons from the 4.7 transition (step 5 of its own protocol). That's a minor compliance gap.
- STEINBERGER's "realistic guardrails" section is dated "April 2026" and describes the state of play pretty accurately. A point release probably doesn't invalidate any of it.

## Step 2 — Identify what should change

Three candidates, ranked by leverage:

**A. Apply the 06B diff if it's still pending.** This is the actual work. It's been sitting since the 4.7 transition and the five bullets were designed for a 1M-context frontier model — 4.8 fits that profile too.

**B. Close the loop on `06-MODEL-UPGRADE-HANDLING.md`'s own step 5.** The protocol says "update this file with lessons learned from the upgrade." The 4.7 transition generated a lesson (the five-bullet diff in 06B, and the meta-insight that soul.md's read-list was written defensively for a weaker model). That lesson should be captured in the upgrade file itself, not just in the 06B treatment doc. One paragraph.

**C. Nothing else.** Opus 4.8 over 4.7 is, based on every prior point release in this family, an incremental improvement — better at some benchmarks, maybe cheaper, maybe slightly longer context or sharper tool use. It does not obviously require new steering. Pattern drift that would justify a new protocol has not shown up yet. Per "subtraction before addition": don't author a new diff just because the protocol says you can.

## Step 3 — Proposed diff (≤5 bullets, per protocol)

**If the 06B five-bullet diff has not been applied:**
1. Apply 06B's bullet 1: collapse soul.md Instructions 1–5 into a conditional read list and remove the duplicate amcc.md line.
2. Apply 06B's bullet 2: rewrite Instruction 7 as "Retrieve context you can retrieve. Don't read organs speculatively."
3. Apply 06B's bullet 3: reframe Instruction 12 (portability) from "will it understand?" to "will it follow the protocols?"
4. Apply 06B's bullet 4: change routing rationale from "don't try to handle it yourself" to "route for consistency and auditability."
5. Apply 06B's bullet 5: add one line to the Data & Context Routing rule — "DuckDB is primary for quantitative/structured queries. For narrative or recent-events context, prefer the file/MCP column."

**If the 06B diff was already applied:**
1. Open `06-MODEL-UPGRADE-HANDLING.md`. Add a short "Lessons" section capturing: (a) the 4.6 → 4.7 transition produced a five-bullet soul.md diff around removing defensive read-ahead instructions, (b) the pattern to watch for in future upgrades is "instructions written to compensate for a weaker model," (c) confirm each upgrade whether that class of instruction has a new instance.
2. No other changes.

Either path stays under the five-bullet cap. Neither adds new structure; both subtract or document.

## Step 4 — Apply after approval, then test

After Richard approves:
- Make the edits above.
- Run a real task through the updated steering. Good candidates on the current slate: the W17 MX callout (`03A-perfmkt-mx-w17-wbr.md` if it's still open), the Yun-Kang NB drop draft in intake, or the next forecast refresh. Anything that touches multiple organs and benefits from efficient context-routing — that's where the soul.md changes will or won't pay off.
- Observe: does the agent route to the right organs without being force-marched through the read list? Does it route to specialists on the right cases without over-deferring on borderline ones? If yes, the diff is doing its job.

## Step 5 — Update with lessons (after the test)

Capture in `06-MODEL-UPGRADE-HANDLING.md`:
- The meta-lesson from 4.7 (defensive instructions written for weaker models become dead weight).
- The process-lesson from 4.8 (incremental upgrades rarely require new diffs — use them to close loops from the prior major upgrade).
- If the post-apply test surfaces a new gap, add it. If it doesn't, record the null result. Null results are also evidence.

---

## What I'm not doing and why

- **Not proposing new principles or organs for 4.8 specifically.** There's no evidence yet that 4.8 changes agent behavior in a way that needs new steering. Writing preemptive rules on version bumps violates "subtraction before addition" and "invisible over visible" — and it trains the system to generate busywork on every model announcement, which is the opposite of the protocol's intent.
- **Not rewriting STEINBERGER.** It's dated April 2026 and reads accurately. Re-dating it alone would be cosmetic, not structural.
- **Not touching the Five Levels, Routing Directory, or How I Build.** None of these are model-capability-dependent. Per 06B's analysis, they're evergreen.

---

## Human review required (per STEINBERGER §5)

Any edit to soul.md or a steering file is a high-stakes change — it affects every agent session. Per STEINBERGER's human-in-the-loop rule, nothing above gets applied without your explicit go-ahead.

**Decision needed from you — pick one:**
- **A.** Has the 06B five-bullet diff been applied to soul.md already? If no → approve applying it now.
- **B.** If yes → approve adding the "Lessons" paragraph to `06-MODEL-UPGRADE-HANDLING.md` and close this out.
- **C.** Skip this entirely — 4.8 is a point release and the protocol doesn't demand a diff just because it can produce one.

My recommendation: **A if it's pending, otherwise B.** Avoid C only because closing the protocol's own step-5 loop is trivially cheap and worth doing.

## Principle check (per How I Build §6)

- **Subtraction before addition:** ✓ The whole plan subtracts — either applying a diff that removes friction, or adding one documentation paragraph.
- **Structural over cosmetic:** ✓ No format changes, no reorders. Either the read-list stays rewritten structurally, or the upgrade-handling file gets a structural closing loop.
- **Invisible over visible:** ✓ If A is approved, the change is felt as "the agent wastes fewer turns on every task," not "something looks different."
- **Reduce decisions, not options:** ✓ The proposed diff narrows nothing — it removes mandated reads, giving the agent room to triage.
- **Protect the habit loop:** N/A — no routine cue/reward changes.
- **Routine as liberation:** N/A — this is system maintenance, not routine design.

## One more thing

4.7 → 4.8 is the **second** model upgrade announcement since this protocol was written. The protocol fired correctly both times (you mentioned the version, the agent reviewed, proposed a diff). That's working as intended. Worth noting: this is one of the few protocols in the system that has a built-in feedback loop (step 5). Use it — write the lesson back into the file. Otherwise the protocol becomes a checklist-without-memory, and the next upgrade gets the same analysis from scratch.
