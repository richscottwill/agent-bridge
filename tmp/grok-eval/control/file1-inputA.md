# MX NB CPA Trajectory — as of 2026-04-22

**TL;DR:** MX NB CPA is trending **up and wrong direction**. W16 (Apr 12–18, partial) hit **$183**, the highest weekly CPA of the year and +29% WoW from W15's $142. The 4-week trailing average is **$147**, vs. a Jan W2–W4 run rate in the **$74–$98** band. YoY comps are still favorable because Apr 2025 was anomalously expensive, but intra-year the slope is clearly negative. Bayesian forecast for April total: **$143 NB CPA**, which W16 blew past mid-month.

---

## The numbers

### Weekly NB CPA, 2026 (ps.v_weekly, MX)

| Week | Dates | NB regs | NB spend | **NB CPA** | 4-wk avg | CVR | CPC |
|------|-------|---------|---------:|-----------:|---------:|----:|----:|
| W2 | 01-04 | 97 | $7.2K | **$74** | 74 | 1.26% | $0.94 |
| W3 | 01-11 | 117 | $9.9K | **$84** | 79 | 1.24% | $1.04 |
| W4 | 01-18 | 117 | $11.5K | **$98** | 86 | 1.22% | $1.19 |
| W5 | 01-25 | 94 | $13.7K | **$146** | 101 | 1.15% | $1.68 |
| W6 | 02-01 | 89 | $11.8K | **$133** | 115 | 1.22% | $1.62 |
| W7 | 02-08 | 88 | $10.4K | **$118** | 124 | 1.34% | $1.58 |
| W8 | 02-15 | 98 | $13.8K | **$141** | 134 | 1.19% | $1.68 |
| W9 | 02-22 | 96 | $15.5K | **$161** | 138 | 1.13% | $1.82 |
| W10 | 03-01 | 98 | $16.2K | **$165** | 146 | 1.11% | $1.84 |
| W11 | 03-08 | 146 | $17.8K | **$122** | 147 | 1.56% | $1.90 |
| W12 | 03-15 | 121 | $16.0K | **$132** | 145 | 1.37% | $1.81 |
| W13 | 03-22 | 140 | $18.8K | **$134** | 138 | 1.46% | $1.95 |
| W14 | 03-29 | 124 | $16.1K | **$130** | 129 | 1.33% | $1.72 |
| W15 | 04-05 | 142 | $20.2K | **$142** | 135 | 1.32% | $1.88 |
| **W16** | **04-12** | **115** | **$21.1K** | **$183** | **147** | **1.13%** | **$2.07** |

Linear regression on the 13-week window (W4–W16): slope **+$2.59 per week**, R² 0.21. Trend is weakly upward but noisy.

### Monthly trajectory (ps.v_monthly, MX NB)

| Month | NB regs | NB spend | **NB CPA** | NB CVR proxy |
|-------|--------:|---------:|-----------:|-------------:|
| 2025-M10 | 497 | $52.8K | **$106** | — |
| 2025-M11 | 515 | $63.4K | **$123** | — |
| 2025-M12 | 324 | $27.3K | **$84** | seasonal low |
| 2026-M01 | 451 | $45.0K | **$100** | — |
| 2026-M02 | 371 | $51.5K | **$139** | CVR compression |
| 2026-M03 | 562 | $76.4K | **$136** | — |
| **2026-M04 MTD (1-18)** | **324** | **$49.7K** | **$153** | weakest YTD |

### April MTD intra-month decay (daily rollup)

| Period | Days | NB regs | NB spend | CPA |
|--------|-----:|--------:|---------:|----:|
| Apr 1–7 | 7 | 134 | $16.6K | **$124** |
| Apr 8–14 | 7 | 122 | $21.3K | **$174** |
| Apr 15–18 | 4 | 68 | $11.9K | **$175** |

April is front-loaded. Performance got 40% worse after the first week.

### YoY (April MTD, 1–18)

| Metric | 2026 | 2025 | YoY |
|--------|------|------|-----|
| NB regs | 324 | 257 | **+26%** |
| NB spend | $49.7K | $76.7K | -35% |
| NB CPA | $153 | $299 | **-49%** |

YoY optics are great but misleading. Apr 2025 was broken (CPA $299). The real comp is "where were we trending in Q1 2026" — and we've given back about $55 of the $80 improvement we built from Jan through March.

---

## What's driving it

**Proximate cause (W16 specifically):** CVR collapsed back to **1.13%** from W15's 1.32% — same pattern Yun-Kang flagged on W15. Spend held flat-to-up while regs dropped 115 vs. 142. CPC is also climbing (W16 $2.07, the highest weekly CPC on record; Jan was under $1.00).

**Structural drivers (the Jan→Apr drift):**
1. **CPC creep.** NB CPC doubled from ~$0.94 (W2) to ~$2.07 (W16). That alone moves CPA from $74 to ~$163 at constant CVR. This is the dominant factor.
2. **CVR compression.** Jan ran ~1.2%, Feb–Apr ran 1.1–1.5% with spikes (W11 1.56%, W13 1.46%). Average CVR hasn't gotten worse, but it's volatile and W15/W16 dip is real.
3. **Spend up, regs flat-ish.** Monthly NB spend went $45K → $51K → $76K → $50K (MTD); the March push bought 562 regs at $136 CPA, April is tracking to buy fewer regs at higher CPA.

**Open hypotheses (from the Yun-Kang thread, unresolved):**
- **Beauty + Auto page rollout lag** — pages went live late-W14; if CVR is still stabilizing, W16 is the back-half of that adjustment period. Would expect recovery in W17.
- **ABIX feed / reftag attribution** — Italy had a cp/ps-brand issue on 4/16. MX not yet verified as clean.
- **W15 bid/budget interaction** — changes around the Beauty+Auto launch may be bidding into lower-intent inventory.

## Forecast vs. reality

Current forecasts (ps.forecasts, bayesian_brand_nb_split, run 2026-04-13):

| Horizon | Metric | Forecast | Actual/Pacing |
|---------|--------|----------|----------------|
| 2026-M04 (monthly) | NB CPA | **$143** | **$153 MTD** (over by 7%) |
| 2026-Q2 (13-wk) | NB CPA | **$144** | on track if W17+ stabilize |
| 2026-M04 (monthly) | NB regs | 558 | 324 through 4/18 → pacing ~540 |
| 2026-M04 (monthly) | NB spend | $82.6K | $49.7K through 4/18 → pacing ~$83K |

The forecast expected drift to $143. W16's $183 is inside the noise band but at the upper edge. If W17 doesn't revert toward $130 we'll miss the April NB CPA forecast materially.

## OP2 context

OP2 targets are set at the **total PS level**, not split Brand/NB. Full-year 2026 MX OP2: **11,178 regs / $541,860 / $48.48 CPA** (Brand + NB combined). April OP2 target is **$44 CPA / 791 regs**. April MTD total PS CPA is **$52** (regs 1,205, spend $62.8K) — running hot on CPA but regs are pacing well.

Implicit NB-only OP2 back-out (using Q1 actual Brand/NB mix and planner assumptions) lands NB target CPA in the **$70–$90 band**. W16 at $183 is roughly **2x** the implicit NB OP2. That's the real story — we are not on track for any reasonable NB CPA target.

## Trajectory call

- **Short-term (W17 read):** Expect bounce toward $130–$140. If W16 was the Beauty+Auto CVR lag, W17 resolves it. If W17 holds above $160, it's not a one-week noise event.
- **April close:** Pacing to **~$155 NB CPA** vs. forecast $143 and implicit OP2 target in the $70s. **Will miss.**
- **Q2:** Current run rate puts us on a trend of **$140–$150 NB CPA** through June, versus Q1's $124 average. Absent intervention, Q2 NB CPA will be **worse than Q1**.
- **Underlying signal:** CPC is the real trajectory problem, not CVR. Even in good weeks, CPC has ratcheted up 2x since January. CVR fixes help the margin but don't reset the baseline.

## What I'd do next

1. **Reply to Yun-Kang today** (draft exists in intake) with W16 read — not a clean story yet, flag the CVR + CPC combo.
2. **Diagnostic deep-dive on CPC:** query-level audit — which NB queries/keywords drove the $0.94 → $2.07 CPC climb? Is this an auction-pressure issue, a bid strategy change, or a query-mix shift?
3. **Confirm ABIX / reftag** — rule out attribution breakage before blaming performance.
4. **Re-baseline the forecast** after W17 lands. If W16 is the new baseline, the April and Q2 Bayesian forecasts need to be rerun.
5. **Ping Lorena on ie%CCP trajectory** — at $153 CPA and assumed CCP ~$69, ie%CCP is running ~220%, way outside the 90–110% bound the forecaster uses.

---

*Sources: ps.v_weekly, ps.v_monthly, ps.v_daily, ps.targets, ps.forecasts (DuckDB ps_analytics, MotherDuck). Pulled 2026-04-22.*
