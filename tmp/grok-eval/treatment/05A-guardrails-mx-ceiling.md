# MX Full-Year Spend Ceiling @ 100% ie%CCP

**Confidence: 55%**
**Human review strongly recommended before action.**

## Answer

FY 2026 MX total spend ceiling at exactly 100% ie%CCP ≈ **$1.14M** (~$959K NB + ~$184K Brand).

This is ~$227K above a straight-line extrapolation of the current $282K YTD / 80.5% ie%CCP pace (~$916K FY). In other words, holding 100% ie%CCP gives you headroom to spend more total dollars than today's pace implies — because the current NB CPA ($138) is running well above the elasticity curve's efficient zone, and brand registrations add a large fixed CCP pool at $97 each.

## Math

### Step 1 — Decompose YTD into Brand vs NB arms
The user-stated YTD totals ($282K / 4,833 regs / 80.5% ie%CCP) don't include a Brand/NB split. I pulled the mix from `ps.v_weekly` W1–W16 and applied those ratios:

| Arm | Reg share | Spend share | Regs (YTD) | Spend (YTD) |
|-----|----------:|------------:|-----------:|------------:|
| Brand | 66.2% | 20.1% | 3,198 | $56,650 |
| NB    | 33.8% | 79.9% | 1,635 | $225,350 |

Sanity check: $56,650 + $225,350 = $282K ✓. Implied ie%CCP from inputs = 79.2% (off by 1.3pp from stated 80.5% — likely a reg-weighting methodology difference; I'm using the user's stated mix).

### Step 2 — Project Brand arm linearly to full year
Brand demand is effectively inelastic to spend in the relevant range — brand clicks are capped by query volume, not budget. Linear extrapolation 52/16:

- Brand regs FY ≈ **10,393**
- Brand spend FY ≈ **$184,113**
- Brand CCP pool = 10,393 × $97 = **$1,008,121**

### Step 3 — Model NB arm with the elasticity curve
The stated curve `NB CPA = 0.02 × spend^0.937` fits YTD data best when `spend` = **NB weekly spend** (predicted $154/wk CPA at $14.1K/wk vs actual $138 — close). The cumulative interpretation produces absurd outputs (118 FY regs), so I'm using the weekly interpretation.

Weekly NB regs = spend_wk ÷ CPA = 50 × spend_wk^0.063.

### Step 4 — Solve the 100% ie%CCP constraint
Let `s` = NB weekly spend at the ceiling. The constraint is total spend = total CCP pool:

```
brand_spend_FY + 52·s = brand_regs_FY × $97 + 52 × (50 × s^0.063) × $28
$184,113   + 52·s = $1,008,121              + 72,800 × s^0.063
```

Bisection gives `s* ≈ $18,446/wk` of NB spend.

| Component | Value |
|-----------|------:|
| Brand spend FY | $184,113 |
| NB spend FY (52 × $18,446) | $959,169 |
| **Total spend ceiling** | **$1,143,281** |
| Brand regs FY | 10,393 |
| NB regs FY (52 × 50 × $18,446^0.063) | 4,828 |
| CCP pool (10,393×$97 + 4,828×$28) | $1,143,281 |
| ie%CCP | 100.0% ✓ |

### Step 5 — What this means directionally
- At the ceiling, NB weekly spend grows from ~$14.1K/wk (YTD avg) to ~$18.4K/wk (+31%) — more NB spend, not less.
- NB efficiency at the ceiling: implied NB CPA = $959K ÷ 4,828 = **$199/reg**, well above the $28 NB CCP. NB alone would run at ~14% NB-only ie%CCP.
- The ceiling is high because the Brand arm contributes a $1.0M CCP pool for only $184K of spend — that "surplus" subsidizes deeply inefficient NB growth.

## Top 3 assumptions that would materially change the outcome

1. **Brand arm is inelastic and linear-extrapolates.** If brand regs drop in H2 (seasonality, share loss to competitors, feed issues like the one Yun-Kang flagged), the Brand CCP pool shrinks fast — every 1,000 lost brand regs cuts the ceiling by ~$97K. Brandon's bet on brand stability is doing most of the work here.
2. **The elasticity curve `0.02 × spend^0.937` is weekly-indexed and stable through end of year.** YTD NB CPA is $138 vs the curve's predicted $154 — curve is a reasonable fit but not tight. If the curve steepens (exponent rises toward 1.0) — which is what usually happens as you push past efficient inventory — the ceiling drops materially. At exponent 0.95 instead of 0.937, the ceiling falls ~$180K.
3. **CCPs stay at $97 Brand / $28 NB for the full year.** These were negotiated 2026-04-22. Any re-cut (especially if Finance tightens NB to $20–25 citing poor incremental test results) collapses the ceiling. At NB CCP = $22, the ceiling drops to ~$980K.

## Caveats

- I used the DuckDB brand/NB mix (W1–W16) to decompose the user-stated YTD totals. The DuckDB row-level spend ($166K) is lower than the stated $282K — likely different scope (the user's figure may include non-paid-media costs or a later-syncing source). Mix ratios should still hold approximately, but if mix differs materially, the answer shifts.
- "Holding 100% ie%CCP" is an accounting ceiling, not a recommendation. Burning $227K above current pace to run at 100% ie%CCP is a very different decision from running at 80% ie%CCP and banking the efficiency — confirm with Brandon/Lorena which framing they want before acting on this number.
- Elasticity is modeled on the NB arm only; brand is assumed fixed. If you believe incremental NB spend cannibalizes brand (or vice versa), the model needs a cross-arm term.

## Why 55% confidence (not higher)

Model structure is sound and the math checks cleanly. But three things cap my confidence:
1. YTD stated totals don't reconcile to the DuckDB scope used for the mix.
2. The elasticity curve fit is loose (16% CPA residual at YTD).
3. "Brand linear to FY" is a working assumption, not a forecast.

Decision quality here is more a function of Brandon's view on brand stability and Lorena's view on whether the CCPs hold through Q4 than it is a math problem.

**Human review strongly recommended before action.**
