---
title: "AU W16 Analysis Brief"
status: FINAL
audience: amazon-internal
owner: Richard Williams
created: 2026-04-20
updated: 2026-04-20
---
<!-- DOC-0013 | duck_id: callout-au-analysis-2026-w16 -->

# AU W16 Analysis Brief

## Registration summary

AU drove 242 registrations (+45% WoW), on $27.6K spend (+7% WoW) at $114 CPA (-26% WoW). This breaks a 5-week declining streak (W11: 241 → W15: 167) and directly validates the W15 callout's stated expectation that the Polaris LP revert would lift CVR and pull CPA back under $140. April is now tracking to ~900 regs at ~$113K spend, $126 CPA. (vs OP2: -16% regs, -23% spend, -9% CPA)

## Why registrations changed

The +45% reg move is overwhelmingly a CVR story, not a traffic story. Blended CVR rose from 2.86% to 3.88% (+35%) while clicks grew only +7% (5,829 → 6,241). Holding clicks flat, the CVR lift alone would have added ~60 regs; holding CVR flat, the click lift would have added only ~12. CVR drove roughly four-fifths of the move.

Both segments responded in the same direction, both CVR-led:
- Brand: 76 → 95 regs (+25%) on CVR 6.00% → 7.80% (+30%), clicks -4%. Brand CPA $53.28 → $37.94 (-29%).
- NB: 91 → 147 regs (+62%) on CVR 1.99% → 2.93% (+47%), clicks +10%. NB CPA $239.34 → $163.50 (-32%).

NB CPC was flat at $4.78 (W15: $4.77), so the NB CPA improvement is entirely conversion-driven. The 7-week NB CPC decline (W6 $6.82 → W13 $4.81) has now held at ~$4.78 for three consecutive weeks, and the bid-strategy savings that built up through the declining streak are now compounding on top of the recovered CVR.

Impressions rose +15% to 68K (highest since W9) at the same CPC, consistent with Adobe's bid strategies accessing more inventory without paying more per click. Brand clicks actually fell -4% while Brand regs rose +25% — a pure CVR story on Brand.

## Trend context

W16's 242 regs is the highest weekly total since W9 (256). The 8-week regs sequence is now W9: 256, W10-13 declining, W14: 171, W15: 167, W16: 242. Blended CVR at 3.88% is back inside the W7-W12 range (3.74%-4.70%, avg 4.15%) after three weeks below 3.20%. Read this as a return to baseline, not an outperformance.

NB CPC has stabilized at ~$4.78 for three weeks (W14-W16), marking the end of the 7-week decline streak. The compounding thesis — lower CPC meeting recovered CVR — is now live: NB CPA $239 to $163 in one week, the lowest NB CPA since W4 ($149).

Brand CVR at 7.80% is in line with the W7-W12 Brand average (~7.5%). W12's 8.54% spike was the outlier; W16 is the normal range.

## Relevant actions and events

- **Polaris LP revert live (completed mid-W15, first full week W16).** W15 callout explicitly stated: expect CVR recovery over W16-W17 to pull CPA back below $140. Delivered on a one-week lag. The LP was flagged as a CVR suppressor from W13 onward; this is the confirmation signal.
- **Clean post-Easter window.** Per the seasonality calendar, Easter 2026 (Apr 3-6, W14) carried the -18.3% AU drag. W15 was partially recovering. W16 is the first fully clean, post-holiday, post-LP-revert week — which is what made the underlying CVR shift visible.
- **NB bid strategy floor.** NB CPC has held at $4.78 for three consecutive weeks after seven weeks of decline. Bid strategies have found their level; volume is now rising on a stable cost base (+10% NB clicks WoW).
- **Anzac Day (Apr 25) falls on Saturday in W17.** Per calendar, ~-3% impact on that day only. Negligible at the weekly aggregate.
- **Two-campaign structure and MCS page replication from MX** remain proposed (Alexis sync 3/24), not yet executed. No structural change in W16 attributable to these.
- **OCI not yet started for AU** (target May 2026). No infrastructure change in W16.

## Monthly projection

**April projection: ~900 regs, ~$113K spend, ~$126 CPA. vs OP2 (1,071 / $147.6K / $138): -16% regs, -23% spend, -9% CPA.**

MTD through W16 (18/30 days): 493 regs, $65,579 spend, $133 CPA.

Remaining 12 days (Apr 19-30): 9 weekdays + 3 weekend days, with Anzac Day on Sat Apr 25 (-3% drag, ~-1 reg).

Methodology. W16 is the first clean post-revert baseline. Daily rates from W16:
- Weekday (Mon-Fri, Apr 13-17): 36.6 regs/day, $3,950/day
- Weekend (Sun Apr 12 + Sat Apr 18): 29.5 regs/day, $3,943/day

Applied to remaining days:
- Weekdays: 9 × 37 = 333 regs; 9 × $3,950 = $35,550
- Weekends: 3 × 29.5 = 89 regs; 3 × $3,943 = $11,829
- Anzac adjustment: -1 reg
- Calibration haircut: 3% on regs (per au-projections.md — persistent optimism in stable weeks; keeping it light since W16 was a recovery week)

Remaining: ~400 regs, ~$47K spend. Total: 493 + 400 = **~900 regs**; $65.6K + $47K = **~$113K**; CPA = **$126**.

This replaces the W15 callout's 359-reg / $38,685 linear projection (which extrapolated from the weakest two weeks and missed the LP recovery) and is modestly lower than the ingester's 908-reg / $113K / $124 estimate (I discount slightly for bounce-back fade and calibration bias).

MoM: April ($113K / 900 / $126) vs March ($125K / 1,030 / $121). Regs down ~13% MoM, CPA up ~4%. The shortfall is real, driven by W14-W15 LP disruption (~100-150 regs lost across those two weeks). W16 shows the baseline has recovered; W17-W18 will confirm whether 220-240 regs/week is sustainable.

## Recommended W17 spend

**W17 spend: $29K** (vs W16 $27.6K, +5%).

Rationale: AU strategy is OP2 registration targets, cut wasted spend. Currently -16% on regs vs OP2 but -23% under on spend, so there is room to lean up while unit economics are working (projected April CPA $126 vs $138 OP2). Proposed split:
- Brand: hold at ~$3,600 (no action — brand CVR recovery should sustain on its own; brand clicks already softening)
- NB: lean up to ~$25.5K (+6% vs W16's $24.0K) while NB CPA holds below $170

Daily run rate moves from $3,950 (W16 weekday) to ~$4,150, still well under the $4,920/day OP2 pace. Conditional trigger: if NB CPA breaks above $180 by midweek, hold W17 flat and wait. If NB CPA holds below $170, W18 can step up another 5-10%.

## Flags

- **5-week decline broken with one week of data.** W16 is a single point. Recovery confirmation requires W17 to hold at 220+ regs and blended CPA below $140. Do not declare victory on the Polaris revert yet.
- **NB regs recovery (+62% WoW) bounces off a depressed base.** 147 regs is within historical range (W3-W8 avg ~160) but lower than the W4 peak (168). Bounce-back math, not outperformance. Watch W17 for overshoot as a competitive-auction signal.
- **Brand clicks -4% WoW at flat impressions.** Click-through compressed while Brand CPA improved. Could be LP-driven (users self-filtering on new copy) or a competitive IS shift. Low-priority watch item; the Brand CPA improvement is the headline.
- **W16 was the first clean post-holiday, post-LP-revert week.** This makes the recovery unambiguous but also means confounds are absent only by luck — W17 with Anzac Day on Saturday remains clean, but W18 enters May with OCI kickoff looming.
- **No YoY data (market launched Jun 2025).** Unchanged structural gap. First AU YoY comparisons available W24 2026.
- **Projection schema caveat.** Previous run noted the ps.projections table schema did not match the agent prompt's expected columns, so automated upsert was skipped. Leaving the projection in au-projections.md (this file) as the durable record. Flag for pipeline maintainer remains open.

## Suggested narrative angle

AU registrations rebounded to 242 (+45% WoW) as the Polaris LP revert drove CVR from 2.86% to 3.88% (+35%), pulling CPA to $114 — a $40 improvement in one week. Both segments responded: Brand CPA $38 (-29%), NB CPA $163 (-32%), with NB volume up +62% on a 47% CVR lift. This directly confirms the W15 callout's thesis. April is now tracking to ~900 regs at $113K and $126 CPA (-16% regs, -23% spend, -9% CPA vs OP2), a meaningful improvement over the W15 linear projection. W17 spend recommended at $29K — a measured NB lean-in while Brand CVR holds. One week is not confirmation; W17 needs to hold 220+ regs and CPA below $140 to close the Polaris story.
