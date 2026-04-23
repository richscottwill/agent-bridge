# T3 Blind Evaluation Verdict — AU W16 WBR Callout

**Task:** Draft the AU W16 WBR callout for Kate's reporting — regs/spend/CPA vs OP2, test activity, April pacing.

**Ground truth anchors** (from task context):
- W16 AU: 242 regs +45% WoW, $27.6K spend +7%, CPA $114 -26%.
- Polaris **brand LP un-gating test (AU's own)** reverted 4/18 after -34% NB CVR.
- April projection: ~$108K / ~814 regs / $132 CPA vs OP2: **-27% spend, -24% regs, -4% CPA**.

---

## Summary scores

| Criterion | ARM-A | ARM-B | ARM-C | ARM-D |
|-----------|:----:|:----:|:----:|:----:|
| 1. Clarity of Next Best Action | 8 | 7 | 8 | 7 |
| 2. Decision Quality (narrative, pacing, exec-ready) | 4 | 3 | 9 | 5 |
| 3. Adherence to Richard's principles (subtraction, invisible) | 4 | 3 | 6 | 7 |
| 4. Overall Usefulness (drop-in for Kate) | 3 | 2 | 8 | 5 |
| 5. META — Always-on cost tradeoff | 5 | 3 | 7 | 7 |
| **Total** | **24** | **18** | **38** | **31** |

**Ranking: C > D > A > B.**

---

## ARM-A

**Verdict:** Well-structured, good writing discipline, but hallucinates the revert narrative.

- Invents an **Italy→AU Polaris misattribution window** ("IT Polaris template overwrote PS ref tag, redirecting IT traffic to AU registration"). The ground truth is that Polaris was **AU's own brand LP un-gating test**, reverted 4/18 after -34% NB CVR. A's story is fabricated cross-market contamination. This would confuse Kate and create a narrative the team would have to retract.
- April projection math lands close to truth ($109.5K / 822 regs / -23%/-26%/-3.6%). That part is solid.
- Two callout variants (128 and 115 words), five appendices, applied-rules section, NBA at the end. This is ceremony. Richard would ask "which one do I send?" and delete the scaffolding.
- NBA is clear: re-baseline W17 before calling NB structural. Good instinct.
- Violates **subtraction** (two variants, five appendices) and **invisible over visible** (process exposition visible throughout). Reads like a worksheet.

**Drop-in for Kate?** No. The Italy misattribution paragraph would need to be deleted, and the assumption that drove it was wrong.

---

## ARM-B

**Verdict:** Highest procedural discipline (explicit confidence %, top-3 assumptions, human-review flag), applied to the wrong narrative.

- Same **Italy→AU misattribution fabrication** as ARM-A. Worse: explicitly cites `project_timeline` entries that say "traffic redirected to Australia registration." If those entries are real, the model is pattern-matching on a different incident; if not, it's invented. Either way, the callout leads Kate down a path that contradicts the actual Polaris revert story.
- April projection **badly wrong:** $147K / 1,074 regs / $137 CPA → nearly on-pace with OP2 (-0.3% spend, +0.3% regs). Ground truth is -27% / -24%. This is the number Kate will ask about and it is materially incorrect. Unusable as-is.
- Two "open questions for Richard before this goes to Kate" — this is the right human-in-the-loop instinct but it's asking Richard to confirm numbers the model got wrong, not numbers the model is uncertain about.
- 95% headline confidence is overconfident given the fabricated contamination thesis and wrong April math.
- Clarity Check, Guardrails, Style-guide Compliance Check — three scaffolding sections before the callout. Heavy ceremony. Violates **subtraction** and **invisible over visible** hard.

**Drop-in for Kate?** No — would have to rewrite the April projection from scratch and strip the Italy narrative.

**Always-on cost:** The guardrails procedure is valuable in theory, but if it attaches to fabricated inputs it produces confident-sounding wrong outputs. Net noise in this instance.

---

## ARM-C (baseline)

**Verdict:** Correct narrative, correct numbers, exec-ready with minor trim.

- **Gets the Polaris story right:** AU's own brand LP un-gating test, -34% NB CVR, reverted 4/18. CVR trajectory cited (NB 2.0% W15 → 2.9% W16) as evidence the recovery is real.
- **April projection exactly matches ground truth:** $108K / 814 regs / $132 CPA / -27% spend / -24% regs / -4% CPA. This is what Kate is going to reference.
- NBA is clear and sequential: (1) send through callout pipeline, (2) confirm April projection with Brandon, (3) validate W17 NB CVR, (4) source YoY baseline. Action-oriented, appropriately paranoid about a single post-revert week.
- Explicit human-review flag on the April projection. Confidence stated (medium, 60%). Projection sensitivity range given (730–880 regs).
- Appendix is denser than strictly needed (6-week trend, MTD pacing table, daily CVR pattern, assumptions) but every table earns its place for a high-stakes readout.
- Mild demerit: the "What Richard should do next" section leaks process into the artifact (references `shared/.kiro/hooks/wbr-callouts.kiro.hook`). That's system plumbing, not WBR content. Would strip before sending.

**Drop-in for Kate?** Yes, with two tweaks: delete the "send through pipeline" line and tighten the CVR pattern subsection.

**Always-on cost:** The discipline here (correct anchoring to stated context, explicit confidence, projection sensitivity) is the baseline every high-stakes readout should carry. Low incremental noise.

---

## ARM-D

**Verdict:** Tightest prose, most operational, but numbers drift from ground truth.

- **Narrative structurally right**: CVR-driven lift (2.9→3.9% blended), Brand CVR recovery, NB CPA holding below run-rate. Attributes to reverting to PS templated landing pages. Close enough to truth without fabricating a cross-market story.
- **But:** says "mid-W15 revert" when truth is 4/18 (end of W16). Small factual slip but it's the anchor of the narrative.
- **April projection off:** ~900 regs / $113K / $126 CPA → -16% / -23% / -9%. Ground truth is -24% / -27% / -4%. Not catastrophically wrong but materially different from what the context says. Kate would ask "why different from the pacing doc?"
- **Forward-looking posture is the strongest of the four:** concrete W17 spend recommendation ($29K, conditional on NB CPA holding below $170/$180), specific watch thresholds, Anzac Day noted. This is WBR-grade operator content.
- Cleanest separation of callout prose vs supporting tables. No ceremony sections (no "applied rules," no "clarity check").
- Missing: explicit confidence, human-review flag, projection assumptions visible to the reader. Violates **human-in-the-loop on high-stakes** (principle 7).

**Drop-in for Kate?** Partial — prose is usable, projection numbers need to be reconciled with the canonical April pacing before sending.

**Always-on cost:** This is the style Richard should want always-on: subtraction-first, operator-forward, no meta commentary. Low noise, high leverage across all tasks.

---

## Cross-cutting observations

**Two arms (A, B) fabricated an Italy→AU Polaris misattribution story that isn't in the task context.** That's a decision-quality failure specific to those arms — whatever steering they're running on pushed toward over-reading `project_timeline` signals at the expense of what was actually stated.

**Only C and A anchored the April projection to the stated context.** B invented near-on-pace numbers; D drifted mid-range. For a number going to a Director, anchoring matters more than ceremony.

**Richard's principles scorecard across arms:**
- **Subtraction:** D > C > A > B. B is worst — three pre-callout scaffolding sections.
- **Structural over cosmetic:** All four get the structure (headline + WoW + cause + pacing). Differences are in content accuracy, not shape.
- **Invisible over visible:** D wins — no exposed process. A, B, C all show scaffolding the reader doesn't need.
- **Human-in-the-loop on high-stakes:** B formally applies it (confidence %, assumptions, review flag) — wasted on wrong inputs. C applies it lightly and correctly. A applies it in the NBA. D skips it entirely, which is the actual miss.

**What the "right" always-on procedure looks like for WBR callouts:** D's discipline (operator-forward, no ceremony) + C's accuracy (anchored to given context, correct Polaris narrative, projection sensitivity) + a lightweight guardrail layer (confidence, top assumption, review flag) invoked only on high-stakes outputs — not on every task.

---

## Recommendation

**Use ARM-C as the basis for the Kate-facing callout.** Trim the "send through pipeline" line. Consider grafting D's concrete W17 spend recommendation and Anzac Day callout onto C's accurate narrative. Discard A and B — the Italy fabrication is not recoverable.
