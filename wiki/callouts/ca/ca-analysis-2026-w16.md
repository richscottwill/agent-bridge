---
title: "CA W16 Analysis Brief"
status: FINAL
audience: amazon-internal
owner: Richard Williams
created: 2026-04-19
updated: 2026-04-19
---

# CA W16 Analysis Brief

## Registration summary
778 regs, +13% WoW (778 vs W15 689). Spend $60,293 (+7% WoW). CPA $77.50 (-5% WoW). CVR 2.78% (+14% WoW from 2.44%). Brand 455 (+9% WoW), NB 323 (+20% WoW). April projection: 3,130 regs at $245K spend, $78 CPA — +28% regs, +14% spend, -11% CPA vs OP2.

## Why registrations changed
CVR-driven recovery, resolving the W15 dip. Clicks were effectively flat WoW (~27,966 vs 28,277, -1%), so the +13% regs came almost entirely from CVR rebounding 2.44% → 2.78% (+14%). This is the mirror image of W15, which fell -18% on CVR with clicks +7%. The W15 callout flagged the CPA spike as CVR-driven, not structural, and said I would monitor W16. W16 confirms the reversion hypothesis.

NB led the rebound:
- NB regs +20% WoW (323 vs 270). NB CVR jumped 1.85% → 2.16% (+17%). NB CPA dropped $115 → $100 (-13%). NB spend was up +4%, so the improvement was conversion efficiency, not volume buying.
- Brand regs +9% WoW (455 vs 419). Brand CVR 3.07% → 3.49% (+14%) on +10% Brand spend. Brand CPA edged up to $62 from $61 (+1%) — Brand CVR gains were offset by higher Brand CPC ($1.87 → $2.15, +16%).

The divergence is clean: NB is where the recovery story lives. Brand regs recovered but Brand CPA didn't participate — CPC inflation absorbed the CVR gain.

## Trend context
8-week regs trend (DuckDB canonical): W9: 689 → W10: 641 → W11: 745 → W12: 675 → W13: 771 → W14: 793 → W15: 689 → W16: 778.

W14 remains the one-week high; W15 was a one-week low; W15–W16 avg of 734 regs is consistent with the W13–W16 running avg of 758, which is meaningfully above the W9–W12 range (688). The March uplift identified in the W13 analysis has held, with volatility around a higher baseline.

CPA context: $77.50 is back in the W9–W14 range ($64–$79). The W15 spike to $82 was the outlier, not a new normal. Brand CPA at $62 remains elevated vs the $46–$56 range seen W11–W14 — this is the one metric not yet fully recovered and deserves a watch.

NB CPC held at $2.16 (within rounding of the $2.10 floor that started forming in W13). OCI E2E (launched 3/4) is now 46 days in; the CVR step-up in NB (1.85% → 2.16%) is directionally consistent with early OCI impact but still within NB's normal weekly CVR variance (1.73%–2.27% over the last 12 weeks), so I won't claim it yet.

## Relevant actions and events
- OCI E2E launched 3/4, now 46 days in. NB CVR recovery is directionally consistent with early OCI impact but not yet distinguishable from normal variance. Full OCI impact still projected for Jul 2026.
- LP optimization gains remain baked into the baseline and continue to underpin the YoY NB CPA compression.
- No CA holidays in W15 or W16 — both are clean reads. Good Friday (Apr 3) fell in W14; the measured CA impact is -16.7% WoW (per seasonality calendar), consistent with W14 actually showing +3% WoW given the 2025 W13 Brand CVR spike baseline. W16 is the first fully clean post-Easter week, so the recovery narrative is uncluttered.
- Next CA holiday: Victoria Day, May 18 (W21). No impact on W17–W20.

## YoY assessment
LY W16: 372 regs, $47,539 spend, $128 CPA, CVR 2.05%. TY at 778 / $60,293 / $77.50 / 2.78%.
- Regs: +109% YoY
- Spend: +27% YoY
- CPA: -39% YoY
- CVR: +36% YoY

The gap widens on the Brand/NB split:
- NB regs: 323 vs 111 = +191% YoY. NB CPA: $100 vs $302 = -67% YoY. This is the standout — LP optimization, OCI rollout, and bid compression compounding against a weak LY NB baseline (LY NB CPC was $4.24 vs TY $2.16, -49%).
- Brand regs: 455 vs 261 = +74% YoY. Brand CPA: $62 vs $54 = +15% YoY. Brand CPA is running hotter than LY — the one YoY regression, driven by Brand CPC inflation ($2.15 vs $1.37 LY, +57%).

YoY gains are accelerating: W14 was +37% regs YoY, W15 +56%, W16 +109%. Part of this is a base effect (LY W16 was a local low at 372 vs LY W15's 442), but the absolute delta is real and consistent with three consecutive quarters of structural improvement.

## Monthly projection
MTD through end of W16 (Apr 18, 18/30 days): 1,889 regs, $145,534 spend, $77.04 CPA (DuckDB `ps.v_monthly` / daily sum).
- Brand MTD: 1,125 regs
- NB MTD: 764 regs

Remaining 12 days (Apr 19–30): W17 full week + W18 partial (5 days, Sun–Thu). No CA holidays. 8 weekdays + 4 weekend days.

Daily rate estimation from W15–W16 blended actuals:
- Weekday avg: ~115 regs/day, ~$8,573 spend/day
- Weekend avg: ~80 regs/day, ~$7,750 spend/day

Remaining estimate:
- Regs: 8 × 115 + 4 × 80 = 920 + 320 = 1,240
- Spend: 8 × $8,573 + 4 × $7,750 = $68,584 + $31,000 = ~$99,584

**Projection: 3,130 regs, $245K spend, $78 CPA.**
- vs OP2 (2,447 / $214,436 / $87.64): **+28% regs, +14% spend, -11% CPA.**

Rationale: CPA has stabilized at $77–78, CVR is back in range, no holidays through month-end. W14 treated as one-week anomaly, not new baseline. Projection uses W15–W16 run rate applied to a weekday/weekend-calibrated remaining calendar. Monthly beat is locked in barring a two-week CVR collapse. The OP2 regs overage (+28%) is consistent with the compounding YoY trend and OCI ramp, not a one-week anomaly.

Note: Prior W16 projection (3,200 regs, $247K, $77 CPA) was close — the refined MTD number (1,889 vs the 1,920 estimate used for the W15 projection row) lowers the total by ~70 regs. Projection accuracy indicator is consistent — both projections deliver a material OP2 beat.

## Recommended W17 spend
**$58K** (hold steady). Matches the W15–W16 run-rate average ($58.4K), CPA has normalized at $77.50, CVR signal recovered. Balanced-market strategy (per CA context: "OP2 targets, OCI E2E ramping") with OP2 on track — no case for aggressive expansion until either Brand CPA normalizes or a sustained multi-week CVR step-up confirms OCI impact.

## Flags
- **Brand CPA at $62 persistently elevated** — has run $56–$62 for three straight weeks (W14–W16) vs the $46–$56 range seen W11–W14. Brand CPC inflated to $2.15 in W16 (+16% WoW, +57% YoY). This is the only metric not participating in the recovery and the likely driver is competitive IS or CPC drift; worth checking the Brand SQR or IS report.
- **W14 anomaly unresolved** — W14's 793 regs / $46 Brand CPA still looks like a one-week high. W15–W16 did not sustain it. Treat W14 as outlier, not new baseline, when forecasting.
- **NB CVR step-up directionally consistent with OCI signal** — 1.85% → 2.16% WoW is in the right direction for OCI E2E at week 6. Not yet attributable above noise, but worth tagging for the W17–W18 observation window. If NB CVR holds ≥2.10% for 3 consecutive weeks, that crosses out of normal variance.
- **YoY comparisons clean** — no CA holiday calendar offset between LY W16 and TY W16; both are non-holiday weeks. YoY figures are reliable.
- **Monthly pacing flag — spend +14% vs OP2** — tracking above OP2 spend while delivering above OP2 regs and below OP2 CPA. Consistent with balanced strategy and the scale of YoY reg growth; no action needed unless CPA drifts back toward OP2.

## Suggested narrative angle
Clean post-Easter recovery. W15's CPA spike was indeed CVR-driven and reverted in W16 as called: +14% CVR, +13% regs, $77.50 CPA back in range. NB led the rebound (+20% regs, -13% CPA to $100). YoY still compounding: +109% regs, +27% spend, -39% CPA, with NB CPA at -67% YoY the standout. April tracking +28% regs and +14% spend vs OP2 at $78 CPA (-11% vs OP2). One open watch: Brand CPA at $62 has held elevated for three weeks, driven by Brand CPC inflation, and has not participated in the recovery.
