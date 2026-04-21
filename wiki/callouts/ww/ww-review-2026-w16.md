---
title: "WW Review — W16 (Apr 13 – Apr 19)"
status: FINAL
audience: amazon-internal
owner: Richard Williams
created: 2026-04-20
updated: 2026-04-20
---

# WW Review — W16 (Apr 13 – Apr 19)

Reviewer: callout-reviewer agent. Rubric: two-lens scoring per `shared/.kiro/agents/wbr-callouts/callout-reviewer.md` and `richard-style-wbr.md`. Six callout units reviewed: AU, MX, US, CA, JP, EU5.

## 1. Summary

All six W16 callouts PASS. Batch average combined score 8.69 (vs W15 batch 8.69 — flat week-over-week). MX and JP top the batch at 9.00; EU5 brings up the floor at 8.13. Word counts are all within the 100-120 range (prose block excluding Note), ranging 111-120 words. Standout dimensions across the batch: L1 Structure (8.83 avg) and L2 So-what (8.83 avg). Softest dimension: L2 Accuracy (8.67) dragged by one specific EU5 overstatement. No REVISE items and no ESCALATE items. One minor structural issue in CA (fused WoW/YoY paragraph) and one factual softness in EU5 ("nearly doubled" for +61%) are worth correcting for next week but do not fail the PASS bar.

## 2. Per-market scoring table

| Unit | Words | L1 Attr | L1 Struct | L1 Voice | L1 Econ | L1 avg | L2 So-what | L2 Own | L2 Acc | L2 Strat | L2 avg | **Combined** | **Verdict** |
|------|------:|--------:|----------:|---------:|--------:|-------:|-----------:|-------:|-------:|---------:|-------:|-------------:|:------------|
| AU   | 120   | 9 | 9 | 9 | 8 | 8.75 | 9 | 9 | 9 | 8 | 8.75 | **8.75** | PASS |
| MX   | 117   | 9 | 9 | 9 | 9 | 9.00 | 9 | 9 | 9 | 9 | 9.00 | **9.00** | PASS |
| US   | 111   | 9 | 9 | 8 | 9 | 8.75 | 9 | 8 | 9 | 8 | 8.50 | **8.63** | PASS |
| CA   | 118   | 9 | 8 | 8 | 9 | 8.50 | 9 | 8 | 9 | 9 | 8.75 | **8.63** | PASS |
| JP   | 119   | 9 | 9 | 9 | 9 | 9.00 | 9 | 9 | 9 | 9 | 9.00 | **9.00** | PASS |
| EU5  | 119   | 8 | 8 | 8 | 9 | 8.25 | 9 | 8 | 7 | 8 | 8.00 | **8.13** | PASS |
| **Batch** | — | 8.83 | 8.67 | 8.50 | 8.83 | **8.71** | 9.00 | 8.50 | 8.67 | 8.50 | **8.67** | **8.69** | — |

## 3. Market-by-market edits

No REVISE verdicts. The items below are **optional quality nudges** for next week's writer — all current callouts pass as-is.

### EU5 — factual overreach (not blocking)

Current:
> DE drove the spend surge, jumping to $199K (+76% WoW) as NB CPA nearly doubled to $210.

Issue: DE NB CPA went from $130.33 to $210.11 — a +61% increase, not "nearly doubled" (which implies ~90%+). The analysis brief uses the more accurate "NB CPA ran away to $210 from $130". Brandon is likely to run the math; precision matters here.

Suggested replacement:
> DE drove the spend surge, jumping to $199K (+76% WoW) as NB CPA ran away to $210 (+61% WoW).

### CA — paragraph structure (not blocking)

Current (fused single paragraph):
> ...WoW the recovery was CVR-driven (+14%) on flat clicks, confirming W15's CPA spike was CVR, not structural. NB led the rebound with regs +20% on CVR 1.85% to 2.16%, pulling NB CPA to $100 (-13% WoW). Brand regs recovered +9% but Brand CPA held at $62 as Brand CPC inflated to $2.15 (+16% WoW). YoY we spent +27% with +109% registrations, led by NB at -67% CPA YoY ($100 vs $302) as LP gains and OCI ramp compound against a weak LY NB baseline.

Issue: Writer spec calls for a separate YoY paragraph (single line break between WoW and YoY paragraphs). The current draft runs WoW and YoY together as one block, which slightly obscures the structural weighting. All other markets maintain the break.

Suggested replacement (insert line break before "YoY"):
> ...Brand regs recovered +9% but Brand CPA held at $62 as Brand CPC inflated to $2.15 (+16% WoW).
>
> YoY we spent +27% with +109% registrations, led by NB at -67% CPA YoY ($100 vs $302) as LP gains and OCI ramp compound against a weak LY NB baseline.

## 4. Cross-market consistency check

- **Headline format:** All six units follow the standard `{Unit} drove X regs (+W% WoW), with +S% spend WoW and $C CPA (+P% WoW). {Monthly projection vs OP2}` template. MX correctly carries ie%CCP. AU correctly omits YoY per `has_yoy=false` config. EU5 correctly aggregates rather than listing per-market headlines. No deviations.
- **OP2 comparisons:** All six include regs+spend vs OP2 using rounded values ($113K, $107K, $2.89M, $245K, $165K, $1.8M). JP and AU also include CPA vs OP2 in the analysis briefs but appropriately compress to regs+spend in the callout prose.
- **YoY framing:** Consistent across the five markets that carry YoY. All use "we spent +X% with +Y% registrations" or close variant. AU correctly has no YoY.
- **Em-dashes:** None detected in any callout.
- **Holiday naming:** No holiday names in WoW attribution. JP names Golden Week in the forward-looking Note (W18 budget pull trigger) — acceptable since this is planning, not attribution. AU and MX name Anzac Day and Día del Trabajo only below the separator. Compliant.
- **Cross-market anchors:** EU5 correctly positions UK as the OCI-mature subsidizer of the group and FR/IT/ES as OCI E2E learning-phase. CA prose aligns OCI E2E thesis ("NB CVR step-up is directionally consistent with OCI E2E at week 6") with the EU5 frame on FR/IT/ES. US frames OCI as "at 100% on NB" with the NB CPC uptick as the first sign of a ceiling. The OCI narrative is consistent across units.
- **WW-level aggregate:** No unit quotes a WW total, so no cross-check required. Six-unit coverage sum (single markets + EU5 rollup) = 17,163 regs for the big markets; this is complete coverage minus the non-reporting long-tail.
- **Status flag:** JP callout is marked `status: DRAFT` in frontmatter while the other five are `FINAL`. Not a content issue but worth a mechanical promotion to FINAL before the WBR send.

## 5. Week-over-week quality trend vs W15

Batch averages from `ps.callout_scores`:

| Metric | W15 | W16 | Delta |
|---|---:|---:|---:|
| Combined avg | 8.69 | 8.69 | flat |
| L1 Attribution | 9.00 | 8.83 | -0.17 |
| L1 Structure | 8.83 | 8.67 | -0.16 |
| L1 Voice | 8.67 | 8.50 | -0.17 |
| L1 Economy | 8.50 | 8.83 | +0.33 |
| L2 So-what | 9.00 | 9.00 | flat |
| L2 Ownership | 8.50 | 8.50 | flat |
| L2 Accuracy | 8.83 | 8.67 | -0.16 |
| L2 Strategic | 8.17 | 8.50 | +0.33 |

Per-unit movement W15 → W16: AU 8.63 → 8.75 (+0.12), MX 8.88 → 9.00 (+0.12), US 8.63 → 8.63 (flat), CA 8.88 → 8.63 (-0.25), JP 8.75 → 9.00 (+0.25), EU5 8.38 → 8.13 (-0.25).

Read: Batch overall is flat. Economy and Strategic signal both improved (+0.33), reflecting tighter word counts (W15 EU5 ran 140 words; W16 EU5 lands at 119) and better forward-looking framing (AU recovery-confirmation framing, JP pre-brief of W18 GW pull, MX capital-discipline posture). The small softness in L2 Accuracy is EU5-specific ("nearly doubled") and isolated — not a pattern. CA's paragraph-break regression is mechanical and easy to fix. The batch is holding the W15 quality floor without yet clearing it; consistency is the signal, not acceleration.
