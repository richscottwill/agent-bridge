# US Full-Year Spend Ceiling — 100% ie%CCP, +10% OCI CVR Lift

**Run:** t1-var1 (Next Best Action Filter, variation 1)
**Date:** 2026-04-22
**Data:** ps.v_weekly, market='US', W1-W16 2026 (period_start 2025-12-28 → 2026-04-12)
**CCPs:** Brand $412.51, NB $48.52 (canonical Q1'26 check xlsx column U)

---

## Filter pass (var1)

1. **Advances a Level?** Yes — L2 (Drive WW Testing). A written ceiling informs where OCI-driven CVR tests can land without blowing ie%CCP.
2. **Highest-leverage move right now?** Direct Richard ask; no higher-leverage substitute queued.
3. **Reduces future friction?** Yes — documented ceiling + method becomes reusable for EU5/JP/CA and for OP2 conversations.
4. **Within context load?** Yes — v_weekly + CCPs + guardrails only. No extra organs needed.

Filter passes. Proceeding.

---

## ⚠️ Definitional flag before the number

"Hold 100% ie%CCP" is ambiguous and the interpretation changes the answer by millions.

**ie%CCP = (CCP − CPA) / CCP**

- **100% ie%CCP literally** → CPA = 0. Spend ceiling = $0 at any positive spend. Not a useful answer. Almost certainly not what you mean.
- **"Hold ie%CCP ≥ 0%" (i.e., CPA ≤ CCP, break-even-or-better)** → this is the standard operational reading. This is what I'm computing below. **Confirm if you meant something different** (e.g., "hold ie%CCP at YTD level," or "at OP2 target %").

Everything below assumes **CPA ≤ CCP** as the ceiling.

---

## YTD W1-W16 baseline (US, from v_weekly)

| Metric | Brand | NB |
|---|---|---|
| Registrations | 42,637 | 93,999 |
| Spend | $3,014,649 | $7,199,053 |
| CPA | $70.70 | $76.59 |
| CVR (weighted) | 4.06% | 5.85% |
| CPC (weighted) | $2.87 | $4.48 |
| Weekly avg spend | $188,416 | $449,941 |
| Weekly avg regs | 2,665 | 5,875 |

**CCP reference:** Brand $412.51, NB $48.52
**Current ie%CCP:** Brand +82.9% (well under CCP), NB −57.9% (already over CCP)

---

## OCI-driven +10% CVR lift → projected CPA

Holding CPC flat (CVR lift is customer-side, not auction-side):
- Brand CPA post-lift: $70.70 / 1.10 = **$64.27**
- NB CPA post-lift: $76.59 / 1.10 = **$69.63**

Post-lift ie%CCP:
- Brand: ($412.51 − $64.27) / $412.51 = **+84.4%** (still far from ceiling)
- NB: ($48.52 − $69.63) / $48.52 = **−43.5%** (still over CCP)

---

## Full-year spend ceiling — two regimes

### Brand: ceiling not binding

Brand CPA is already $64 against a $412 CCP. CVR would have to collapse by ~84% before ie%CCP hits 0%. **The ie%CCP ceiling does not bind Brand at any realistic FY spend.** The binding constraint on Brand is **branded-query demand**, not CCP.

- Demand-based FY run-rate (W1-W16 weekly avg × 52, held flat): $188,416 × 52 = **$9.80M**
- With +10% CVR lift, same regs buyable at ~9% less spend → floor ~**$8.91M**
- If we let CPA drift up to CCP (unrealistic but mechanical ceiling): spend is capped only by available clicks × CPC, not by ie%CCP.

**Practical Brand FY ceiling under ie%CCP: ~$9.8M–$10.5M** (demand-capped, not CCP-capped).

### NB: ceiling is binding and already breached

Even with +10% CVR, NB CPA ($69.63) exceeds CCP ($48.52). **There is no incremental NB spend that satisfies CPA ≤ CCP at current auction economics.** To hit the ceiling, we'd need to either:
- Cut NB spend to whatever subset of traffic converts at CPA ≤ $48.52 (small tail), **or**
- Need CVR to rise by ~58% (not 10%) from baseline, or CPC to fall by ~37%.

**Mechanical "hold ie%CCP ≥ 0%" NB FY ceiling:**

If we assume OCI's +10% CVR lift applies uniformly, NB is still over ceiling. The ceiling regime implies cutting NB to the efficient tail. A rough estimate using YTD distribution (assume top-efficiency tranche of NB clicks is ~20% of current spend that converts at ~$48 CPA):
- Efficient-tail FY NB spend ≈ $449,941 × 0.20 × 52 ≈ **$4.68M**

This is a directional order-of-magnitude, not a defensible number without an auction-level cost curve.

### US Total FY ceiling (combined)

| Component | FY ceiling |
|---|---|
| Brand (demand-capped) | ~$9.8M–$10.5M |
| NB (CCP-capped at +10% CVR) | ~$4M–$6M (high uncertainty) |
| **US total FY ceiling** | **~$14M–$16M** |

**Compare to current run-rate:** Brand+NB YTD = $10.21M in 16 weeks → FY run-rate ≈ **$33.2M** if held flat.

**The ceiling under "100% ie%CCP = CPA ≤ CCP with +10% CVR" implies cutting US FY spend roughly in half versus current trajectory.** This is the headline.

---

## Confidence: 45%

**Why not higher:**
- "100% ie%CCP" is ambiguous; I picked the most defensible reading but you may mean something else
- NB ceiling depends on the shape of the CPA-vs-spend curve, which I don't have — I used a flat-20%-efficient-tail heuristic
- +10% CVR lift applied uniformly is a strong assumption; OCI lifts are usually concentrated in specific query classes
- YTD 16-week average may not be a good FY proxy (Q2 seasonality, promo cycles, SOV shifts)

**Why not lower:**
- Core YTD numbers are from canonical v_weekly, not guessed
- CCP values are from the Q1'26 check xlsx Richard cited
- The Brand-is-demand-capped-not-CCP-capped conclusion is robust across CVR-lift assumptions
- The directional conclusion (NB is over ceiling, Brand isn't) holds under any reasonable sensitivity

---

## Top 3 assumptions (directional sensitivities)

1. **"100% ie%CCP" means CPA ≤ CCP (ie%CCP ≥ 0%).** If you meant "hold ie%CCP at current blended level" or "at OP2 target," the ceiling moves materially (could be anywhere from ~$15M to current ~$33M run-rate). **→ Confirm the definition before citing this number.**

2. **+10% CVR lift applies uniformly across Brand and NB, and CPC holds flat.** If the CVR lift is NB-heavy (more likely for OCI-driven optimization), NB ceiling rises — maybe $6M–$8M instead of $4M–$6M. If CPC rises with more aggressive bidding to capture the lift, ceiling falls.

3. **NB efficient-tail heuristic (top 20% of spend at CPA ≤ CCP).** The real number requires an auction-curve / keyword-level CPA distribution from the bid model, not a weekly rollup. If the efficient tail is 10%, NB ceiling ≈ $2.3M. If 35%, NB ≈ $8.2M. **This is the single biggest uncertainty in the combined number.**

---

## What Richard should do next

Before citing any of this to Brandon, Kate, or Lorena:

1. **Confirm the ie%CCP definition.** One-line Slack to whoever asked: "When you say 100% ie%CCP, do you mean CPA ≤ CCP (break-even), or hold at current/OP2 %?" This is a 5-minute unblock that changes the answer by >$10M.
2. **Pull an NB CPA-vs-spend curve from MarTech or the bid team** before committing to the NB ceiling. My tail heuristic is the weakest part of this estimate.
3. **Don't ship the combined $14M–$16M number as a ceiling** until (1) and (2) are resolved. It's directionally correct but the range is too wide to drive reallocation decisions on its own.
4. **If this is for an OCI test business case:** the real question isn't the ceiling — it's "what's the incremental reg lift at the current spend level if CVR +10% holds?" That's a cleaner framing and produces a defensible number faster.

**Human review strongly recommended before action.**

---

## Method notes (for re-run)

```sql
-- Baseline
SELECT SUM(brand_registrations), SUM(nb_registrations),
       SUM(brand_cost), SUM(nb_cost),
       SUM(brand_cost)/SUM(brand_registrations) AS brand_cpa,
       SUM(nb_cost)/SUM(nb_registrations) AS nb_cpa
FROM ps.v_weekly
WHERE market='US' AND period_start BETWEEN '2025-12-28' AND '2026-04-12';
```

- CPA formulas assume CPC flat under CVR lift (customer-side optimization)
- FY run-rate = weekly avg × 52 (ignores seasonality — would refine with ps.v_monthly Q2'25 shape)
- Break-even ie%CCP = 0% is the standard AB paid-search working definition

