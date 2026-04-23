# MX NB CPA Trajectory — as of 2026-04-22

## Bottom line

**MX NB CPA is rising and the direction is wrong.** We had a clean down-trend from H1→H2 2025 ($202 → $111 quarterly NB CPA), held the gain through January, and have given it all back in Q2 2026. Q2 MTD NB CPA is **$160** — materially worse than Q4 2025 ($107) and Q1 2026 ($125), and back inside Q2 2025 territory. W16 (4/12–4/18) is the worst week of 2026 so far at **$183 NB CPA with regs down -19% WoW** (this is the drop Yun-Kang flagged on the callouts doc).

| Period | NB regs | NB cost | NB CPA | NB CVR |
|---|---|---|---|---|
| Q1 2025 | 1,508 | $396.7K | **$263** | — |
| Q2 2025 | 1,498 | $303.7K | **$203** | — |
| Q3 2025 | 1,317 | $147.2K | **$112** | — |
| Q4 2025 | 1,320 | $141.7K | **$107** | — |
| Q1 2026 | 1,425 | $178.6K | **$125** | — |
| **Q2 2026 MTD** (thru 4/18) | **257** | **$41.2K** | **$160** | — |

Weekly shape of the deterioration (most recent 6 weeks):

| Week | NB regs | NB cost | NB CPA | NB CVR | NB CPC |
|---|---|---|---|---|---|
| W11 | 146 | $17.8K | $121.61 | 1.56% | $1.90 |
| W12 | 121 | $16.0K | $132.37 | 1.37% | $1.81 |
| W13 | 140 | $18.8K | $134.16 | 1.46% | $1.95 |
| W14 | 124 | $16.1K | $129.82 | 1.33% | $1.72 |
| W15 | 142 | $20.2K | $141.99 | 1.32% | $1.88 |
| **W16** | **115** | **$21.1K** | **$183.37** | **1.13%** | **$2.07** |

## What's actually driving it

The Q2 jump is not a volume story — it's a **CVR collapse plus CPC creep**.

- **NB CVR has fallen from ~1.46% (W13) to 1.13% (W16)** — about **-22% in four weeks**. W16 is the lowest NB CVR of 2026.
- **NB CPC is at a 2026 high ($2.07 in W16)**, up from ~$1.88 the prior week and from the $1.57–$1.68 range we held in early February.
- Regs volume is middling (115 in W16), but at this CPC we'd need ~1.5%+ CVR to hold CPA flat. We're not getting it.

Daily data for W16 sharpens this:
- 4/11 spiked to **$266 NB CPA** on 0.68% CVR (worst single day of 2026)
- 4/13 hit **$229 NB CPA** on 0.94% CVR
- 4/18 hit **$224 NB CPA** on 0.81% CVR
- The week had only one "normal" day (4/16 at $155 and 1.48% CVR)

## Why it's happening (hypotheses, in order of likelihood)

1. **Beauty + Auto LP launch lag** — pages went live late-W14, and CVR stabilization typically runs 5–10 days on MX LP launches. The W15–W16 CVR compression timing is consistent with this. If this is the driver, we should see recovery in W17.
2. **ref tag / attribution** — Alex flagged an Italy cp/ps-brand URL overwrite on 4/16 that routed IT regs to AU. Need to confirm MX isn't carrying a similar break in the Polaris/MCS handoff. **This is the cheapest thing to rule out and should be checked first.**
3. **Bid + budget interaction with new LPs** — W15 budget changes overlapped with Beauty+Auto going live. If we pushed spend into the new LPs before CVR stabilized, that mechanically inflates CPA. Worth pulling campaign-level NB cost by LP cluster to confirm.
4. **Sparkle / brand-traffic spillover** — Lorena reported record-high brand traffic on Sparkle "Special Pricing for Business" messaging in the 4/21 sync. If that pulled high-intent users to brand, NB keyword traffic may be shifting toward lower-intent queries. Would show up as NB CVR down + brand regs up in the same window.

## Against plan (OP2)

The OP2 month-level picture is worse than the trajectory alone suggests because M04 target is aggressive:

| Month | Reg target | Cost target | CPA target |
|---|---|---|---|
| 2026-M03 actual | 562 regs / $76.4K / **$136** | vs 859 / $56.6K / **$65.88** | |
| 2026-M04 target | — | — | **$44.34** |
| 2026-M04 MTD (thru 4/18, NB only, total unknown here) | NB 257 / $41.3K / $160 | 791 regs / $35.1K / $44.34 | — |

Total MX ran ~$136 CPA in March against a $65.88 OP2 — we're roughly **2× over plan** on CPA, and M04 targets get tighter, not looser. The agent-trend full-year forecast (MX-ps-cpa-ye) is **$32.19** for 2026. That's not recoverable at current trend.

## So what

- **Short term (this week):** Rule out ref tag / attribution break (hypothesis 2) today — it's a zero-cost diagnosis and if it's broken, it explains some of the CVR drop for free. Confirm Beauty+Auto LP CVR is stabilizing by pulling W17 daily data mid-week.
- **Medium term (next 2 weeks):** If W17 shows CVR recovery, the Beauty+Auto launch lag story holds and CPA should pull back toward $130–$140. If W17 looks like W16, the story is CPC-driven (bid strategy isn't holding up under the new LPs) and we need a bid/budget intervention.
- **For the WBR reply to Yun-Kang:** the -19% NB regs / -15% CVR WoW framing is accurate but understates the issue — the real story is that **MX NB CPA has regressed to Q2 2025 levels** after three quarters of improvement. Worth flagging to Brandon before the WBR publishes so he's not surprised. Current draft reply in `shared/context/intake/drafts/2026-04-22-yun-kang-mx-nb-drop.md` covers the proximate WoW question but doesn't yet frame the quarter-over-quarter regression — consider adding that.
- **For the Lorena IECCP/R&O conversation:** the CPA regression changes the math on the "release ~$800K back to MX" conversation. Worth pressure-testing that number against the current CPA trajectory before sending the reallocation email.

## Confidence + gaps

- **High confidence:** CPA, CVR, CPC numbers — pulled live from `ps_analytics.ps.v_weekly`, `v_daily`, `v_monthly`. Matches the direction of the WBR callout.
- **Medium confidence:** The Beauty+Auto LP lag hypothesis — timing fits, but I haven't pulled LP-level CVR to confirm the drop is concentrated on the new pages vs. spread across the account.
- **Not yet checked:** ref tag integrity for MX; brand-vs-NB query mix shift; campaign-level budget allocation to new LPs in W15.

---

*Sources: `ps_analytics.ps.v_weekly`, `ps.v_daily`, `ps.v_monthly`, `ps.targets`, `ps.forecasts` (pulled 2026-04-22). Live state from `shared/context/active/current.md` and draft at `shared/context/intake/drafts/2026-04-22-yun-kang-mx-nb-drop.md`.*
