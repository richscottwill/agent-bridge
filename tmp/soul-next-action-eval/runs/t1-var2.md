# US Full-Year Spend Ceiling at 100% ie%CCP (+10% CVR lift)

**Ask:** Full-year US spend ceiling if we hold 100% ie%CCP, assuming OCI-driven +10% CVR lift from current baseline.
**Stakes:** High-stakes — projection > $50K, touches budget pacing. Guardrails active.

## Inputs (queried, not assumed)

YTD W1–W16 (2025-12-28 → 2026-04-19, `ps.v_weekly WHERE market='US'`):

| Metric | Brand | NB | Total |
|---|---:|---:|---:|
| Regs | 42,637 | 93,999 | 136,636 |
| Spend | $3.01M | $7.20M | $10.21M |
| CPA (YTD) | $70.70 | $76.59 | $74.75 |
| CCP (supplied) | $412.51 | $48.52 | — |
| ie%CCP component | 17.1% | 157.8% | — |

**Blended YTD ie%CCP** = $10.21M / (42,637×$412.51 + 93,999×$48.52) = $10.21M / $22.15M = **46.1%**.
Brand is massively under-pacing the ceiling; NB is already ~58% over CCP.

## Formula used (from `state-file-mx-ps.md`, applied to US)

```
ie%CCP = (Brand_Spend + NB_Spend) / (Brand_Regs × Brand_CCP + NB_Regs × NB_CCP)
```

At 100% ie%CCP: **Spend_Ceiling = Brand_Regs × $412.51 + NB_Regs × $48.52**.
A +10% CVR lift at unchanged clicks = +10% regs (Brand and NB alike) = +10% ceiling.

## Full-year ceiling

Annualize YTD linearly (×52/16 = 3.25) to an FY reg baseline, then apply +10% CVR:

| Line | Value |
|---|---:|
| FY baseline Brand regs (YTD × 3.25) | 138,570 |
| FY baseline NB regs (YTD × 3.25) | 305,497 |
| +10% CVR → Brand regs | 152,427 |
| +10% CVR → NB regs | 336,046 |
| **FY spend ceiling at 100% ie%CCP (lifted)** | **~$79.2M** |
| For reference — ceiling without the CVR lift | ~$72.0M |
| For reference — current FY spend pace | ~$33.2M |

**Headroom vs current pace: ~$46M of unspent ceiling** before we cross 100% ie%CCP — gated by whether we can find enough incremental registrations worth $412.51 (Brand) / $48.52 (NB) to absorb that spend.

## Confidence: **45%**

Why not higher:
- Linear ×3.25 annualization ignores seasonality (Prime Day, Q4, summer lull). Real FY regs likely non-linear — this is the biggest error source.
- 10% CVR lift is a point estimate with no confidence interval supplied. OCI lift could land anywhere 5–15%.
- NB ie%CCP is already 158% YTD. Driving blended ie%CCP to 100% at current Brand/NB mix requires Brand to carry the weight — a CVR lift alone doesn't rebalance mix.
- Spend ceiling assumes *linear* reg supply at current CPAs. In practice, the supply curve bends: adding $46M of spend will raise CPA before we hit the reg volume implied here.

Why not lower:
- Math is mechanical once YTD sums and CCPs are fixed — no model uncertainty in the formula itself.
- Inputs are deterministic SQL sums against `ps.v_weekly`, not forecasts.
- +10% CVR lift applied linearly is the standard OCI framing.

## Top 3 assumptions (ranked by sensitivity)

1. **Linear reg supply at fixed CPAs** — treating the $46M of headroom as spendable at current CPAs. Reality: diminishing returns. If marginal CPA rises 20% as spend scales, the practical ceiling drops to roughly **~$65–70M**, not $79M. *Biggest directional risk.*
2. **×3.25 annualization** — ignores seasonality and OCI ramp curve. If H2 runs 15% higher than H1 (typical), ceiling rises to ~$85M. If flat, ~$79M holds.
3. **CCP values static at $412.51 / $48.52** — if Brand CCP drops to $380 (e.g., LTV reforecast), ceiling falls ~$5M. If NB CCP lifts to $55, ceiling rises ~$3M. CCPs move; verify against the Q1'26 check sheet before anchoring.

## Caveats

- This is a **mechanical ceiling**, not a spend plan. It says "up to this much spend would still be defensible at 100% ie%CCP" — it does not say "we can actually find this much demand."
- NB is the gating lever for blended ie%CCP compliance, not the overall ceiling size — the ceiling is Brand-weighted (Brand CCP is 8.5× NB CCP, Brand regs scale the ceiling hardest).
- If the ask is actually "what should we spend in FY?", this ceiling is the wrong frame. The right frame is incremental CPA ≤ CCP at the margin, which requires the supply curve, not YTD averages.

**Human review strongly recommended before action.**
Do not cite "$79M ceiling" in any stakeholder conversation (Brandon 1:1, Kate review, Lorena budget ask) without a second pass on: (a) the ×3.25 annualization vs a proper seasonal forecast, (b) the linear-supply assumption, (c) the source of the +10% CVR lift estimate.

---

**Next Best Action:** Validate the $412.51 Brand CCP and $48.52 NB CCP against the Q1'26 check sheet and confirm the OCI +10% CVR is a point estimate or a range before taking this number to Brandon.
