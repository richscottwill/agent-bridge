# US Full-Year Spend Ceiling — 100% ie%CCP with 10% OCI CVR Lift

**Prepared:** 2026-04-23 · **Market:** US · **Framework:** ie%CCP ceiling
**Confidence: 55%** · **Human review strongly recommended before action.**

---

## TL;DR

**Pure ceiling (theoretical, if we held 100% ie%CCP all year with OCI 10% CVR lift): ~$77.0M**

**Pragmatic ceiling (YTD W1–W16 locked at 46% ie%CCP actuals + W17–W52 at 100%): ~$63.1M**

Either number is ~1.8–2.3× OP2 spend of $34.1M. The headroom exists because YTD US is running at only **46.1% ie%CCP** — we're leaving roughly half the allowed CCP on the table.

---

## Inputs (verified from source)

| Input | Value | Source |
|---|---|---|
| Brand CCP | $412.51 | `ps.market_projection_params_current` (seeded from CCP Q1'26 check yc.xlsx col U) |
| NB CCP | $48.52 | Same |
| YTD Brand regs (W1–W16) | 42,637 | `ps.v_weekly` |
| YTD Brand spend | $3,014,649 | `ps.v_weekly` |
| YTD Brand CPA | $70.70 | Derived |
| YTD NB regs (W1–W16) | 93,999 | `ps.v_weekly` |
| YTD NB spend | $7,199,053 | `ps.v_weekly` |
| YTD NB CPA | $76.59 | Derived |
| YTD total spend | $10,213,702 | `ps.v_weekly` |
| YTD ie%CCP (actual) | **46.1%** | spend ÷ (brand_regs × $412.51 + nb_regs × $48.52) |
| OP2 FY spend target | $34,077,222 | `ps.targets` |
| OP2 FY regs target | 360,833 | `ps.targets` |
| OP2 FY CPA | $94.44 | Derived |
| US governing constraint | "Efficiency + volume balance — largest market" | `ps.market_constraints` |
| OCI status | Live | `ps.market_constraints` |

## Formula

Per the canonical MPE spec (`.kiro/specs/market-projection-engine/tasks.md` Task 1.9):

```
ie%CCP = spend / (brand_regs × brand_CCP + nb_regs × nb_CCP) × 100
```

At 100% ie%CCP:
```
spend_ceiling = brand_regs × brand_CCP + nb_regs × nb_CCP
             = brand_regs × $412.51 + nb_regs × $48.52
```

## Math

### W17–W52 baseline run rate (36 weeks remaining)

From YTD actuals:
- Brand: 2,665 regs/wk × 36 = 95,933 regs
- NB: 5,875 regs/wk × 36 = 211,498 regs

### Apply 10% OCI CVR lift to W17–W52

10% CVR lift on remaining weeks (same click volume → 10% more regs):
- Brand lifted: 95,933 × 1.10 = **105,526 regs**
- NB lifted: 211,498 × 1.10 = **232,647 regs**

### Full-year reg volumes (YTD + lifted remainder)

- Brand FY: 42,637 + 105,526 = **148,163 regs**
- NB FY: 93,999 + 232,647 = **326,646 regs**
- Total FY: **474,809 regs** (vs OP2 360,833 → +31.6%)

### Ceiling computation

**Pragmatic (YTD locked, W17–W52 at 100% ie%CCP):**
- YTD spend (locked): $10.214M
- W17–W52 allowance: 105,526 × $412.51 + 232,647 × $48.52 = $43.531M + $11.286M = **$52.817M**
- Full-year total: $10.214M + $52.817M = **~$63.0M**

**Pure ceiling (if we'd held 100% all year):**
- 148,163 × $412.51 + 326,646 × $48.52 = $61.120M + $15.849M = **~$77.0M**

### Sanity vs OP2

- OP2 spend: $34.1M → ceiling is **1.85× to 2.26× OP2**
- Delta over OP2: **+$29M to +$43M full-year**

---

## Top 3 Assumptions That Materially Move the Number

1. **Brand/NB mix holds at YTD ratio (31.2% brand regs / 68.8% NB regs).**
   - Brand CCP is 8.5× NB CCP, so mix shift matters more than volume.
   - Sensitivity: if mix shifts to 25% brand / 75% NB, pure ceiling drops to ~$68M (−$9M). If it shifts to 37% brand / 63% NB, rises to ~$86M (+$9M).
   - Why this matters: OCI tends to optimize NB more than brand (brand is capped by search demand); the lift may skew the mix toward NB.

2. **10% CVR lift translates 1:1 into 10% reg lift at same click volume.**
   - Assumes clicks are not themselves reduced by bid/budget changes and that Google's auction dynamics hold.
   - Sensitivity: if actual lift is 7%, pure ceiling drops to ~$75.6M. If 13%, rises to ~$78.4M. (Lift magnitude is the smaller lever; mix matters more.)
   - OCI results elsewhere (MX) have shown variable lift by market and account type — US result may differ.

3. **No elasticity / diminishing returns applied.**
   - This ceiling is a *linear* CCP-based cap. Reality: doubling spend does not double regs. The balanced US strategy has an unfit elasticity exponent (MPE Task 3.1 not yet complete). If US exponent sits at 0.937 (MX-like), delivering 474K regs at 100% ie%CCP would require even higher CPAs than assumed — effective ceiling likely lower.
   - Sensitivity: at exponent 0.937, real-world ceiling is probably closer to $65–70M, not $77M. **The $77M is the theoretical cap; actual binding constraint is likely efficiency degradation long before 100% ie%CCP.**

## Why 55% Confidence (not higher, not lower)

- **Why not higher:** (a) US elasticity exponent is not fit — using linear math at the ceiling is known to overstate feasible spend. (b) The 10% OCI lift is an assumption, not measured for US (OCI live status ≠ measured 10% lift). (c) Brand/NB mix is held constant but OCI will distort it. (d) Ignores seasonality and Q4 demand ceiling (Brand CCP $412 assumes you can find 148K brand regs in the US — this may not exist at current search demand).
- **Why not lower:** (a) Math is straightforward and directly uses the canonical formula from the MPE spec. (b) CCPs and YTD data are both in the primary source of truth. (c) The 46% YTD ie%CCP baseline is rock-solid, so the direction (large headroom) is not in doubt.

## Flags

- OP2 full-year spend target is $34.1M, set at ie%CCP levels well below 100% — the ceiling is a budgeting upper bound, not a recommendation.
- US elasticity exponent not yet fit (MPE Task 3.1 open). The "pure ceiling" number should not be treated as achievable spend.
- OCI 10% CVR lift is Richard's stated assumption, not measured for US. Consider validating against OCI impact tracking (if any) before using this number externally.
- Governing constraint for US is "efficiency + volume balance" per `ps.market_constraints` — leadership will likely cap well below $77M even if the math supports it.

---

## Richard — what to do next

The useful output from this is **not the ceiling number itself**. The useful output is: **YTD US is at 46% ie%CCP, meaning we're leaving ~$23M of CCP allowance unspent in the first 16 weeks alone.** That's the conversation starter.

**Recommended next moves, in order:**

1. **Don't quote $77M to anyone external yet.** The ceiling is real math but it's a theoretical cap; without an elasticity exponent and without validated OCI lift, the number will get challenged on both inputs. Human review before any stakeholder conversation.

2. **Reframe to the 46% headroom story.** "US is pacing at 46% ie%CCP YTD — we have room to scale before hitting any efficiency wall. OCI is live and showing 10% CVR lift assumption. Before committing to a spend bump, we need: (a) measured OCI lift validation for US, (b) US elasticity exponent fit (MPE Task 3.1)."

3. **Route to the right owner.** Spend reallocation / ceiling conversations go to Brandon or up the chain — not executed solo. This is a Kate-visible magnitude. Soul.md agent-politics guardrail: load `~/shared/context/body/amazon-politics.md` if pitching this upward.

4. **Close the elasticity gap.** MPE Task 3.1 (US fit) is the unblocker for converting this theoretical ceiling into a reliable "recommended spend" answer. If you want to move on this in Q2, fitting US is the prerequisite.

5. **Five Levels check.** This is a Level 2 (Drive WW Testing) and Level 1 (Sharpen Yourself — strategic artifact) move. A one-page POV on "US ie%CCP headroom + OCI lift" is a candidate weekly artifact — more leverage than answering the ceiling Q in isolation.

**Human review strongly recommended before action.**

---

## Provenance

- Data pulled: `ps.v_weekly` (US, 2026-W01–W16), `ps.targets` (US 2026-M01–M12), `ps.market_projection_params_current` (US CCPs), `ps.market_constraints` (US)
- Formula source: `.kiro/specs/market-projection-engine/tasks.md` Task 1.9 (canonical regional rollup)
- Guardrails: `high-stakes-guardrails.md` (auto-loaded on "ceiling"/"projection" keyword match)
- Run: `shared/tmp/soul-next-action-eval/runs/t1-baseline.md`
