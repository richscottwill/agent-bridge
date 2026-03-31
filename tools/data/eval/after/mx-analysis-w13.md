# MX W13 Analysis Brief

## Registration summary
354 registrations, +9% WoW (vs 326 in W12). This is a partial recovery from the W12 dip (-16% WoW) but still below the W11 peak of 392. The rebound is click-driven across both Brand and NB, not CVR-driven.

## Why registrations changed
The primary driver was click volume: both Brand and NB clicks grew +9% WoW. Brand clicks rose from 3,384 to 3,698; NB clicks from 8,826 to 9,618. Brand CVR actually declined 4% WoW (5.79% vs 6.03%), partially offsetting the click gains — Brand regs grew only +5% (214 vs 204). NB CVR improved modestly (+6% WoW, 1.46% vs 1.38%), amplifying the click growth into +15% NB reg growth (140 vs 122). Spend rose +15% WoW ($23.2K vs $20.1K), outpacing registration growth, pushing CPA up 6% to $66. The spend increase came primarily from NB (+17%, $18.8K vs $16.0K), with NB CPC rising to $1.95 (from $1.81). Brand spend grew +8% ($4.4K vs $4.1K).

## Trend context
The 8-week trend shows a volatile but upward trajectory: W6: 229, W7: 246, W8: 368, W9: 264, W10: 298, W11: 393, W12: 326, W13: 354. The W8 and W11 spikes followed by pullbacks suggest a sawtooth pattern rather than smooth growth. W13 at 354 is above the 8-week average of 310. NB regs at 140 are 33% above the 8-week average of 105, flagged as an anomaly. Spend at $23.2K is 24% above the 8-week average of $18.7K.

## Relevant actions and events
- Negative keyword restructuring (W11) continues to improve query routing, likely contributing to sustained NB efficiency gains
- Brand coverage scaling ongoing: Brand spend at $4.4K/wk, up from ~$470/wk a year ago
- algo-mas.mx competitor at 13% IS on Brand with +20% CPC spikes — Brand CPC at $1.20 remains low but worth monitoring
- No major holidays in W13 (Benito Juárez was W12, Easter is W15)
- AU/MX OCI planned for May 2026 — not yet impacting performance

## YoY assessment
+91% regs YoY (354 vs 185) on -32% spend ($23K vs $34K). Brand regs +182% YoY, reflecting the massive Brand coverage scaling from ~$460/wk to $4.4K/wk. NB regs +28% YoY despite NB spend declining significantly — NB CPA dropped 57% YoY ($134 vs $309), driven by bid strategy optimization and negative keyword work compounding. The YoY efficiency story continues to accelerate: this is the best YoY reg growth in the recent trend. LY W13 WoW was +6%; TY W13 WoW is +9%, showing stronger momentum this year.

## ie%CCP analysis
Blended ie%CCP for W13: 99% (CPA $65.59 / CCP per account $66.27). CCP per account = (Brand CCP $90 × 214 Brand regs + NB CCP $30 × 140 NB regs) / 354 total regs = $66.27. This is effectively at the 100% target — right at break-even. Brand ie%CCP: $21/$90 = 23% (highly efficient). NB ie%CCP: $134/$30 = 447% (deeply inefficient in isolation). The blended number works because Brand's 214 regs at 23% ie%CCP subsidize NB's 140 regs at 447%. The Brand/NB mix (60/40) is the key lever. If NB spend continues to grow faster than Brand (+17% vs +8% WoW), the mix will shift unfavorably and ie%CCP will breach 100%. MTD ie%CCP is tracking ~95-99%, effectively at target for March.

## Monthly projection
March projected: 1,500 regs, $96K spend, $64 CPA (vs OP2: 859 regs, $57K spend, $66 CPA — +75% regs, +69% spend, CPA $2 below target).

Remaining 3 days (Sat 3/29, Sun 3/30, Mon 3/31): estimated 125 regs (Sat ~30, Sun ~45, Mon ~50) based on W12-W13 weekend/weekday averages. No holidays in remaining days. MTD 1,370 + 125 = 1,495, rounded to 1,500.

Spend: $86K MTD + ~$10K remaining (3 days at ~$3.3K/day) = $96K.

## Recommended W14 spend
$20,000. Rationale: April OP2 budget is $35K for the full month (~$8.8K/wk). However, ie%CCP is at 99% — right at the 100% ceiling. W13 spend of $23.2K is unsustainable into April without breaching ie%CCP. Recommend pulling back NB spend to ~$14K (from $18.8K) while maintaining Brand at ~$4.5K, targeting blended ie%CCP of 90-95%. The $20K weekly run rate would put April at ~$80K, well above OP2's $35K, so further NB cuts may be needed as April progresses. Monitor ie%CCP weekly and adjust NB down if blended exceeds 95%.

## Flags
- NB regs 33% above 8-week average — anomaly. Could be negative keyword restructuring paying off, or noise. Watch W14 for confirmation.
- Spend 24% above 8-week average — driven by NB CPC increase ($1.95, highest in 8 weeks). algo-mas.mx at 13% IS may be contributing to CPC pressure.
- ie%CCP at 99% is at the ceiling. Any NB CPA increase or Brand reg decline will push it over 100%.
- April OP2 budget ($35K) is 64% below March's run rate (~$96K). Significant spend reduction required.
- Monthly metrics table in DuckDB appears garbled for March 2026 (spend showing $214K, regs 86K). Data quality issue — do not use monthly_metrics for MX March; use weekly rollups instead.
- ie%CCP value in ieccp table (65.59) is the CPA value, not the actual ie%CCP percentage. The ingester bug fix may not have fully propagated. Actual ie%CCP = 99%.

## Suggested narrative angle
MX recovered from the W12 dip with +9% regs on click growth across both segments, while YoY efficiency gains continue to compound (+91% regs on -32% spend). The headline story is ie%CCP at 99% — right at the 100% target — heading into an April with 64% less budget. The transition from March's $96K run rate to April's $35K OP2 will require significant NB pullback.
