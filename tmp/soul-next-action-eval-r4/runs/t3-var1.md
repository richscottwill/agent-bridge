# AU W16 WBR Callout

**Audience:** Kate Rundell + marketing leadership
**Period:** W16 (2026-04-12 → 2026-04-18)
**Data source:** `ps.v_weekly WHERE market='AU' AND period_key='2026-W16'`

---

## Callout Draft

AU drove 242 registrations (+45% WoW) with +7% spend WoW and CPA at $114 (-26% WoW). Brand: 95 regs (+25%) on -11% spend, exact-match efficiency holding. NB: 147 regs (+62%) at $163 CPA (-32%), well ahead of the $288 Bayesian forecast. April projects to 822 regs and $109.5K spend against OP2 of 1,071 regs and $147.6K (-23% regs, -26% spend), with projected CPA $133 running slightly ahead of the $138 OP2 target. Note: ~4 days of W16 overlap the Italy Polaris misattribution window that redirected IT traffic to AU registration (reverted 4/18), so NB lift is partially inflated. I will re-baseline W17 post-revert before calling the NB turn structural.

**Word count:** 128 (prose only, target 110 ±10 — 8 words over; trim candidates flagged below if needed)

---

## Trim option (to land at ~110 words)

AU drove 242 registrations (+45% WoW) with +7% spend WoW and CPA at $114 (-26% WoW). Brand: 95 regs (+25%) on -11% spend, exact-match efficiency holding. NB: 147 regs (+62%) at $163 CPA (-32%), well ahead of the $288 Bayesian forecast. April projects to 822 regs and $109.5K spend vs OP2 of 1,071 regs and $147.6K (-23% regs, -26% spend); projected CPA $133 runs slightly ahead of the $138 OP2 target. Note: ~4 days of W16 overlap the Italy Polaris misattribution window that redirected IT traffic to AU registration (reverted 4/18), so NB lift is partially inflated. I will re-baseline W17 before calling the NB turn structural.

**Word count:** 115 (prose only)

---

## Appendix: Weekly Trend

| Period | Regs | Spend | CPA | Brand Regs | NB Regs |
|--------|-----:|------:|----:|-----------:|--------:|
| W14 | 171 | $22,074 | $129 | 97 | 74 |
| W15 | 167 | $25,829 | $155 | 76 | 91 |
| W16 | 242 | $27,638 | $114 | 95 | 147 |

## Appendix: Forecast Scoring (W16)

| Metric | Forecast | Actual | Score |
|--------|---------:|-------:|-------|
| Regs (interval 188–288) | 207 | 242 | HIT |
| Cost | $26,396 | $27,638 | MISS (+4.5%) |
| Brand regs | 101 | 95 | MISS (-6%) |
| NB regs | 106 | 147 | SURPRISE (+28%) |
| CPA (prior run) | $115.42 | $114.21 | MISS (within 1.1%) |

## Appendix: April MTD Pacing (through 4/18, 18 of 30 days)

- Actual MTD: 493 regs, $65,677 spend, CPA $133
- Linear run-rate projection: 822 regs, $109,461 spend
- OP2 April target: 1,071 regs, $147,591 spend, CPA $137.78
- Projected gap: -23% regs, -26% spend, CPA -3.6% (efficient)

## Appendix: Data Caveats

- `ie%CCP` is null in `ps.v_weekly` for AU W16 — omitted from callout (do not default to a number). Flag: confirm whether AU has ie%CCP target defined or if this is a reporting gap.
- YoY unavailable: `ps.v_weekly` has no 2025-W16 AU row. YoY context omitted per style guide's "state why" rule (baseline not loaded).
- Polaris un-gating reverted 4/18 per `project_timeline` (Italy IT→AU misattribution). 4/16 P0 event: IT Polaris template overwrote PS ref tag, redirecting IT traffic to AU registration. Daily AU regs pattern supports inflation thesis: 4/12–4/16 ran 32–43/day, dropped to 25–27 on 4/17–4/18 post-revert.
- OP2 source: `ps.targets WHERE market='AU' AND period_key='2026-M04'`.

---

## Next Best Action

**Next Best Action:** Re-pull AU W17 data after 4/26 close and compare NB CPA/reg levels to the 4/17–4/18 post-revert daily baseline (25–27 regs/day, $163+ NB CPA) before reporting the NB turn as structural vs misattribution-inflated. If W17 NB CPA stays sub-$200 at pre-revert volumes, the bid-strategy improvement is real; if it reverts toward $240, W16 was a Polaris-driven data artifact.

---

## Applied Rules

- **WBR style guide:** lead with headline metric, WoW + cause, separate Brand/NB, forward action, no em-dashes, percentages over raw counts in prose, raw counts in appendix. ie%CCP omitted because data is null (not fabricated).
- **Performance marketing guide:** Context → What moved → Why → Risks → Recommendation. Projection includes assumptions (linear run-rate) and flag (re-baseline post-revert).
- **High-stakes guardrails:** Leadership-facing, April pacing >$50K impact. Caveats explicit. Human-review implicit in the NBA (re-baseline before structural call).
- **Conditional NBA Mandate fires:** High-stakes + internal uncertainty on misattribution inflation → explicit single NBA required and stated above.
- **Soul principle check:** (7) Human-in-the-loop on high-stakes — NBA gates the structural-improvement call on W17 data, not on W16 alone. (3) Subtraction before addition — flagged two callout variants (128 and 115 words); pick the 115-word version for the WBR.
