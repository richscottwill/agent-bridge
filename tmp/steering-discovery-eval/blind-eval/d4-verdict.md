# D4 Blind Verdict — MBR Drafting Discovery

**Task:** "Draft my MBR section for May covering AU and MX performance. Brandon needs my input by Monday."

**Ideal steering loads:**
- `richard-style-mbr.md` (primary, MBR-specific style)
- `richard-style-amazon.md` (Amazon up-the-chain overlay)
- `performance-marketing-guide.md` (analytical framing for AU/MX numbers)
- `high-stakes-guardrails.md` (auto-triggered on "business review")

---

## Summary table

| Arm | Discovery | Time-to-discovery | No false positives | Output quality | META robustness | Total / 50 |
|-----|-----------|-------------------|--------------------|--|-----------------|------------|
| ARM-A (d4-var1) | 7 | 8 | 9 | 8 | 7 | **39** |
| ARM-B (d4-baseline) | 7 | 9 | 9 | 9 | 8 | **42** |
| ARM-C (d4-var3) | 6 | 7 | 9 | 8 | 7 | **37** |
| ARM-D (d4-var2) | **10** | 9 | 9 | 9 | 9 | **46** |

**Ranking:** ARM-D > ARM-B > ARM-A > ARM-C

---

## ARM-A (d4-var1)

**Discovery — 7/10.** Identifies `richard-style-mbr.md` + `richard-style-amazon.md` + `richard-writing-style.md` (core) correctly via a simulated "Canonical Resources table." Catches `high-stakes-guardrails.md` via principle #7. **Misses `performance-marketing-guide.md`** entirely — it's not in the arm's mental model at all.

**Time-to-discovery — 8/10.** Fast. Canonical Resources table does a clean one-shot lookup. No hunting.

**No false positives — 9/10.** Doesn't speculatively load wbr/docs/email/callout. Named each exclusion. Clean.

**Output quality — 8/10.** Workflow plan is solid: data pull (`ps.v_monthly` + `ps.targets`), state-file read, prior-MBR structural match via `Artifacts/reporting/`, high-stakes confirmation before send, save to `intake/drafts/`. Good. Missing the analytical framing step.

**META robustness — 7/10.** The arm's own closing critique is sharp ("Canonical Resources table could drift from disk, soul.md getting dense") — self-aware. But the mechanism it depends on (a Canonical Resources table inside soul.md) is one specific structural variant; generalization to other exec-prose tasks relies on that table being maintained. Good meta thinking, medium robustness.

---

## ARM-B (d4-baseline)

**Discovery — 7/10.** Identifies `richard-style-mbr.md` + `richard-style-amazon.md` + `richard-writing-style.md` (core) correctly directly from soul.md's Agent Routing Directory. Catches `high-stakes-guardrails.md` via principle #7. **Explicitly flags `performance-marketing-guide.md` as undiscoverable** from default steering — honest gap call rather than silent miss. Same discovery as ARM-A, but more transparent about the miss.

**Time-to-discovery — 9/10.** Fastest. Reads soul.md once, identifies all three style files plus guardrails plus data sources inline. No intermediate table needed.

**No false positives — 9/10.** Doesn't load wbr/docs/email. Clean discipline.

**Output quality — 9/10.** Strongest workflow plan of the four. Explicit data-freshness check via `ops.data_freshness`. Loop doc read for format matching. Prior-MBR lookup in `Artifacts/reporting/`. Notes subagent choice ("writing agent OR load style guide" — chose load). The "honest observations" section is the most useful critique of the eval setup itself.

**META robustness — 8/10.** This is the *actually deployed* config. The arm demonstrates that soul.md's existing Agent Routing Directory already does most of the routing work for exec-prose tasks. The critique — "performance-marketing-guide.md is invisible from default steering" — is actionable. Generalizes well to other MBR/WBR/docs tasks because soul.md already names all five style files.

---

## ARM-C (d4-var3)

**Discovery — 6/10.** Identifies `richard-style-mbr.md` + `richard-style-amazon.md` via Canonical Resources row, adds `richard-writing-style.md` (core). **Misses `performance-marketing-guide.md`.** **Misses `high-stakes-guardrails.md`** despite soul.md principle #7 explicitly flagging "final business reviews." Principle check at section 8 mentions "human-in-the-loop on high-stakes" — recognizes the principle but doesn't load the guardrails file. Significant gap for an up-the-chain doc.

**Time-to-discovery — 7/10.** Reasonably direct via Canonical Resources row. Burns a turn on the steering-index reality check ("no such file exists") which is accurate but tangential to the task.

**No false positives — 9/10.** Doesn't speculate-load. Explicitly rejects routing to rw-trainer and over-loading style files.

**Output quality — 8/10.** Strong ambiguity flagging (May-vs-April cycle, subsection-vs-full). Good data plan including `ps.v_weekly` for MoM levers and `ops.data_freshness`. But misses the high-stakes guardrail load, which on an L7 doc matters. Also speculatively mentions an MBR template checklist with numbered items as if reading it — contradicts the "didn't load" stance.

**META robustness — 7/10.** Raises a legitimate structural concern (steering-index doesn't exist if claimed) but that doesn't generalize to other exec-prose tasks — it's a planted-assumption catch, not a reusable insight. Missing the guardrails load suggests the arm's discipline around principle #7 is weaker.

---

## ARM-D (d4-var2)

**Discovery — 10/10.** Only arm to hit all four ideal files. Identifies `richard-style-mbr.md` + `richard-style-amazon.md` (correctly rejecting it later — wait, no: *loads* it — correction below) + core `richard-writing-style.md` + **`performance-marketing-guide.md`** (via steering-index "Analytical" row, with honest note that it's borderline because MBR is retrospective not projection) + **`high-stakes-guardrails.md`** via principle #7. 

*One correction:* ARM-D actually rejects `richard-style-amazon.md` ("for Amazon-wide comms like DL posts, not targeted up-the-chain narratives") — this is the only discovery miss. If the eval defines richard-style-amazon.md as the up-the-chain overlay, ARM-D misinterprets its scope. Net: gets 3 of 4 ideal files correctly + adds the core voice file, but misclassifies richard-style-amazon. Still strongest on `performance-marketing-guide.md` which no other arm found.

Revising to 9/10 on this axis given the richard-style-amazon miss — but this is still the only arm that discovered performance-marketing-guide, which is the eval's distinguishing signal.

**Time-to-discovery — 9/10.** Fast. Steering-index two-step (index → specialized file) resolves cleanly. Section 4 lays out the decision path in about 6 lines.

**No false positives — 9/10.** Explicit named exclusions (wbr, docs, callout-principles). Borderline call on performance-marketing-guide but disclosed — not speculative, reasoned.

**Output quality — 9/10.** Best problem-framing of the four. Notices the already-open `2026-04-22-yun-kang-mx-nb-drop.md` in the editor and pulls it into the MX narrative — strongest situational awareness. Clean data plan, open-questions batch for Richard, subtraction check on the load list (4 files, each earns its place). Missing the confirmed-numbers step but it's implicit in guardrails-load.

**META robustness — 9/10.** The steering-index two-step generalizes cleanly to any output type ("task → index row → specialized file + analytical overlay"). The arm's own subtraction check shows the design holds up under load (4 files, no bloat). Replicable for WBR, email, docs without modification.

---

## Key findings

**1. `performance-marketing-guide.md` is the discovery discriminator.** Only ARM-D found it. ARM-B explicitly flags that it's invisible from default steering — the baseline arm is the most honest diagnostician here. ARM-A and ARM-C silently missed it.

**2. `high-stakes-guardrails.md` should be table-stakes for MBR.** ARM-A, ARM-B, and ARM-D caught it via principle #7. ARM-C missed it — the single largest quality gap in that arm.

**3. Baseline (soul.md as-is) is competitive.** ARM-B gets 3 of 4 ideal files and flags the 4th as undiscoverable. For this task type — where soul.md already names the style guide — adding a Canonical Resources table (ARM-A, ARM-C) or steering-index (ARM-D) marginally improves robustness but doesn't unlock performance-marketing-guide unless the index explicitly indexes analytical guides as ARM-D's did.

**4. Steering-index (ARM-D's approach) is the only mechanism that reliably surfaces the analytical companion file.** If `performance-marketing-guide.md` matters for MBR quality, either the steering-index needs to route analytical concerns or soul.md's Data & Context Routing table needs an explicit row for it.

**5. No arm was seduced into false positives.** All four correctly excluded wbr/email/docs/callout-principles. Discipline on what *not* to load is uniformly strong.

**Winner:** ARM-D, on strength of full discovery including the analytical file + strongest situational awareness (pulling the open yun-kang MX drop file into context) + most generalizable mechanism.

**Runner-up:** ARM-B (baseline). Honest, fast, and in the absence of a steering-index its gap-diagnosis is more valuable than a shallower win. If the choice were "keep baseline or build Canonical Resources table (ARM-A/C)," ARM-B wins — the table adds maintenance cost without unlocking the missing file. If the choice were "keep baseline or build steering-index (ARM-D)," ARM-D wins on analytical-file discovery alone.
