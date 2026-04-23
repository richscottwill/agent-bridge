# AU W16 WBR Callout — Draft

**Audience:** Kate (leadership-facing)
**Stakes:** High — leadership-visible, April pacing material, >$50K monthly spend. Human-review flag ON.

---

## Clarity Check (applied before drafting)

**Q1. Most important signal:** AU W16 posted +45% regs WoW at a $114 CPA, but part of the lift sits inside the W16 window in which the Italy Polaris LP was published with the wrong template (4/16) and redirected IT traffic to the AU registration path before Alex reverted it. The clean read on AU is W17, not W16. Reporting the headline without caveating the Italy spillover would mis-credit AU performance.

**Q2. Smallest, highest-leverage action:** Lead with the headline, attribute what is cleanly attributable (NB efficiency), explicitly flag the Italy contamination, and commit to a W17 clean read. Do not hide the lift, do not overclaim it.

---

## Callout (prose, ~110 words)

AU: AU drove 242 registrations (+45% WoW), +7% spend WoW, CPA $114 (-26% WoW). April is projected to close at $147K spend and 1,074 registrations at a $137 CPA (vs. OP2: -0.3% spend, +0.3% registrations). WoW we held budgets flat. NB bid strategies drove the lift: NB regs +62%, NB CPA -32%, with NB clicks +7%. Brand regs +25% WoW on flat spend. Note: the Italy Polaris LP error 4/14–4/16 redirected IT traffic to the AU registration path before the 4/16 revert; daily AU regs peaked 4/14–4/15 (43/day vs. ~27/day run-rate) then normalized 4/17–4/18. I am treating the NB efficiency gain as real and the absolute volume lift as partially contaminated, and will use W17 as the clean read.

\* NB CPA $163 (W16) vs. $239 (W15), driven by bid-strategy learning on campaigns I adjusted W14–W15; holding changes through W17 to isolate.
\* April MTD through 4/18: 493 regs / $65.6K spend, pacing to full-month OP2 of 1,071 regs / $147.6K. On-pace at day 18 would be 60% of month (643 regs / $88.6K); actuals are running 46% regs / 44% spend of full-month OP2.
\* YoY context unavailable: 2025-W16 AU row not in `ps.v_weekly` (will confirm via Y25 Final and restate in W17 callout if material).

---

## High-Stakes Guardrails

**Confidence in headline numbers:** 95% (direct pull from `ps.v_weekly` 2026-W16, verified against daily roll-up).

**Confidence in "+45% WoW is partly contaminated by Italy spillover":** 65% — signal is the 4/14–4/15 daily spike above run-rate coinciding with the published Italy Polaris error, but I do not have the Adobe segmentation to size the IT-misdirected volume inside AU. W17 will either confirm (regs drop back to run-rate) or disconfirm (regs hold at W16 level).

**Top-3 assumptions:**
1. The Italy Polaris ref tag error on 4/16 actually routed measurable IT traffic to the AU registration path during W16 (source: `project_timeline` 4/16 and 4/20 entries; 4/16 entry states "traffic redirected to Australia registration"). Not independently verified via Adobe.
2. The April projection is a straight-line extrapolation of MTD (493 regs × 30/18 days ≈ 822, adjusted upward for typical late-month pacing to ~1,074). Actual close could swing ±10% on Brand seasonality and any W17/W18 budget action.
3. The 2026-W15 AU baseline (167 regs) was itself depressed (-2% WoW vs. W14 at 171); some of the +45% W16 lift is recovery from a soft W15, not new strength.

**Recommend human review before sending:** Yes. Two open questions for Richard before this goes to Kate:
- Do we have Adobe data on how much AU volume came from misdirected IT refs during 4/14–4/16? If yes, size it and remove from the W16 number.
- Is the "AU pacing 38.2% regs / 36.2% spend vs OP2" in the prompt context pulled through a different cutoff than 4/18 EOD? My MTD-through-4/18 math lands at 46% / 44% of full-month OP2. Reconcile before the version that goes into the Kate deck.

---

## Style-guide compliance check

- [x] No em-dashes in the callout prose
- [x] Word count ~110 (prose paragraph, excluding appendix bullets and guardrails)
- [x] Headline metric → monthly projection → WoW attribution → Note line
- [x] Brand and NB broken out separately
- [x] Specific causal attribution (NB bid strategies, Italy spillover)
- [x] Forward-looking action ("will use W17 as the clean read")
- [x] Volume changes as percentages in prose; raw numbers only where the number is the point (242 regs, $114 CPA, $147K April projection)
- [x] Week references plain text ("W17", "4/14–4/16"), not parenthesized
- [x] "I" for personal decisions, "we" for team actions
- [x] ie%CCP omitted: `ieccp` is NULL for AU W16 in `ps.v_weekly` — do not fabricate. Will backfill in W17 callout if populated.
