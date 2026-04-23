# t1-var4 — US Full-Year Spend Ceiling @ 100% ie%CCP (with +10% CVR lift)

**Variation applied:** var4 — Context → Action Trigger (answer the two trigger questions before proceeding).
**Guardrail loaded:** `high-stakes-guardrails.md` (auto-triggered — projection moves ≥ $10M over remainder of year).

---

## Context → Action Trigger — answered before execution

**Q1. What is the single most important thing this context is telling me right now?**
> Brand CPA ($70.70) is already $342 under its CCP — huge headroom. NB CPA ($76.59) is already ~58% over its CCP ($48.52). A +10% CVR lift only takes NB CPA to $69.62 — still 43% over ceiling. **If "hold 100% ie%CCP" means line-level compliance (each category ≤ its own CCP), a 10% CVR lift alone does not unlock NB — the ceiling question becomes Brand-only.** If it means portfolio-level compliance (blended weighted CCP), Brand's surplus subsidizes NB's overage and the ceiling is ~2.4x current run-rate.

**Q2. What is the smallest, highest-leverage action that directly addresses it?**
> Show the ceiling two ways (line-level vs blended), flag the NB constraint, state what's needed to actually hit line-level CCP, and ask Richard which interpretation to use before he takes this number anywhere.

---

## Inputs

- **CCPs (stated):** Brand $412.51, NB $48.52
- **CVR lift assumed:** +10% vs current YTD baseline (OCI-driven)
- **CPC assumption:** held constant (bid strategy unchanged; OCI is a quality-score / relevance lever, not a CPC lever)
- **YTD W1-W16 actuals** (`ps.v_weekly WHERE market='US'`):

| Metric | Brand | NB | Total |
|---|---|---|---|
| Spend | $3,014,649 | $7,199,053 | **$10,213,702** |
| Regs | 42,637 | 93,999 | 136,636 |
| CPA | $70.70 | $76.59 | $74.75 |
| CVR | 4.06% | 5.85% | — |
| CPC | $2.87 | $4.48 | — |
| Weekly run-rate | $188,416 | $449,941 | $638,356 |

---

## Post-lift math (CVR +10%, CPC flat → CPA / 1.10)

| | Brand | NB |
|---|---|---|
| YTD CPA | $70.70 | $76.59 |
| CPA after +10% CVR lift | **$64.28** | **$69.62** |
| CCP | $412.51 | $48.52 |
| Gap to CCP | −$348 (under) | **+$21 (OVER)** |
| % headroom/overage | 84% under | 43% over |
| CVR uplift needed to hit CCP | n/a (already under) | **+57.8%** (not +10%) |

**Key insight:** A 10% CVR lift doesn't get NB to CCP. NB needs roughly a **6x larger** CVR lift *or* a CPC reduction of ~30% *or* both to clear $48.52.

---

## Ceiling — three interpretations

### Scenario A — "Flat run-rate, no ceiling constraint" (reference point only)
If current weekly run-rate ($638K) simply continues W17–W52:
- **FY US spend ≈ $33.2M** (no CCP gating, no lift applied)

### Scenario B — Line-level 100% ie%CCP (each category must ≤ its own CCP)
**This is the binding, conservative interpretation.**
- Brand: post-lift CPA $64.28 ≪ $412.51 → compliant at any volume auction supports.
- NB: post-lift CPA $69.62 > $48.52 → **non-compliant**. To hit CCP at current CPC, required CVR is 9.24% (vs 5.85% today, vs 6.44% after the assumed +10% lift).
- Under this reading, you'd **cut** NB until the remaining spend is CCP-compliant (likely the top-converting slice of NB), and let Brand scale.
- **With the stated +10% CVR lift alone:** NB would effectively need to go to ~zero to hit 100% ie%CCP, which is a non-starter. So the 10% lift does not unlock a "scale up" ceiling on NB — it only reduces spend at flat reg volume.
- **FY US spend at flat regs + 10% lift, both categories:** ~$31.1M (−$2.1M savings vs Scenario A). But this is NOT CCP-compliant on NB.

### Scenario C — Blended-portfolio 100% ie%CCP (portfolio CPA ≤ weighted CCP)
Weighted CCP at current Brand/NB reg mix (31%/69%): **$162.10**. Blended CPA after lift: **$67.96**.
- **Scale multiplier at blended ceiling: 2.39x** current run-rate.
- **FY US spend ceiling ≈ $60.0M** (YTD $10.2M + 36 remaining weeks at 2.39x weekly run-rate @ post-lift CPA).

> ⚠️ Scenario C assumes (a) you can actually find 2.4x more profitable volume in the US auction — historically SEM brand has inventory but NB at scale gets much worse CPAs, and (b) leadership reads "hold 100% ie%CCP" as portfolio-blended, not line-level. **Neither is safe to assume.**

---

## Confidence: **35%**

**Why not higher:**
- The ceiling is dominated by which CCP interpretation leadership uses (line vs blended). That's a business definition question, not a math question. No amount of analysis pins this down.
- The +10% CVR lift assumption is not grounded — it's a hypothesis about OCI impact. OCI impact on NB specifically has not been measured at this magnitude in US. Historical OCI lift evidence comes from other markets and was smaller.
- Auction depth is assumed to absorb 2.4x volume at post-lift CPAs with no marginal CPA inflation. That's almost certainly wrong for NB — marginal CPA rises as you scale into lower-intent queries.

**Why not lower:**
- YTD data is clean and recent (W1–W16, $10.2M, 136K regs). The starting point is solid.
- CCP inputs are exactly as Richard provided.
- The math holds given the assumptions.

---

## Top 3 assumptions (directional sensitivity)

1. **Interpretation of "100% ie%CCP" = line-level vs blended.** Swinging to blended unlocks ~$29M of extra ceiling in Scenario C. Line-level drops ceiling to effectively "Brand only" plus a trimmed NB, possibly **$20M–$25M FY**.
2. **OCI delivers +10% CVR lift in US.** If actual lift is +5%, NB post-lift CPA = $72.94 (still 50% over CCP, Scenario B gets worse). If +15%, NB CPA = $66.60 (still 37% over). NB does not hit CCP at any reasonable OCI-only lift.
3. **CPC stays flat as spend scales.** Scaling NB 2.4x (Scenario C) likely raises marginal CPC 15–30%. That pushes blended CPA back up and trims the true ceiling by **$5M–$10M**.

---

## What Richard should do next

**Before taking any of these numbers anywhere, confirm the CCP interpretation.** Specifically:

1. **Ask Lorena (or whoever owns the US CCP math):** Is "100% ie%CCP" compliance measured line-level (Brand CPA ≤ $412.51 AND NB CPA ≤ $48.52) or blended (weighted portfolio CPA ≤ weighted CCP)? This single question changes the answer by ~$30M.
2. **Do not cite any single ceiling number in a stakeholder conversation yet.** If pressed for a range, use "$30M–$60M FY depending on CCP interpretation and OCI realized lift" with explicit caveats.
3. **Pressure-test the 10% CVR lift on NB specifically.** The blind spot in this analysis is whether OCI meaningfully helps NB at all, or disproportionately helps Brand where it matters less (Brand CVR going 4.06% → 4.47% doesn't unlock ceiling — Brand isn't the constraint).
4. **If line-level is the right interpretation,** the real question stops being "what's the ceiling" and becomes "what does NB have to do to hit $48.52 CPA" — a CVR, CPC, or query-mix problem, not a budget problem. That's a different project.

**Human review strongly recommended before action.**

---

## Principle check (soul.md "How I Build")

- **#7 Human-in-the-loop on high-stakes:** applied — explicit confidence, top-3 assumptions, review flag. ✓
- **#2 Structural over cosmetic:** flagged that the binding constraint isn't the math, it's the CCP definition. Answering that definition is the structural fix, not running more scenarios. ✓
- **#3 Subtraction before addition:** didn't add a new forecast model; used existing YTD data + stated inputs. ✓

---

**Save path:** `shared/tmp/soul-next-action-eval/runs/t1-var4.md`
