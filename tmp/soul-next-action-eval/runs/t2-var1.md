# t2-var1 — MX Polaris Gen4 Ad Copy Test Readout (W16 close)

**Filter applied:** `var1-next-best-action-filter.md` (4 steps)
**Steering loaded:** soul.md + performance-marketing-guide.md
**Run date:** 2026-04-22

---

## Inputs (as provided by Richard)
- Market: MX, Polaris Gen4 ad copy test
- Window: W13–W16 (4 weeks), closed W16
- Split: 50/50 against Gen3 control
- **Gen4 ("Business Pricing Exclusive"):** 612 regs, $24.8K spend, CVR 4.1%, CPA $40
- **Gen3 (control):** 548 regs, $24.6K spend, CVR 3.6%, CPA $45
- Design: powered to detect ≥5% incrementality at 80%
- Flag raised: creative fatigue concern, W3 (Yun-Kang)

## Stat read (computed, not reported)
- Implied clicks: Gen4 ~14,927 / Gen3 ~15,222
- Two-proportion z = **2.26**, two-sided p = **0.024** → stat sig at 95%
- Observed relative CVR lift: **+13.9%** (Gen4 over control)
- 95% CI on relative lift: **[+1.8%, +26.0%]**
- CPA: −$5 ($45 → $40), −11%
- Total spend in test: **$49.4K** — at the edge of the >$50K high-stakes threshold (soul.md principle 7). Treat as high-stakes.

**Interpretation:** Lift is real (p=0.024). But the CI's lower bound is **below the powered 5% incrementality bar**. The test proves Gen4 ≠ Gen3; it does **not** prove Gen4 clears the pre-registered incrementality threshold. Don't conflate "significant" with "hit the bar."

---

## The Next Best Action Filter (in order)

### 1. Does this advance one of the Five Levels?
**Yes → L2 (Drive WW Testing).** A written, methodologically honest test readout for a closed MX test is exactly the L2 deliverable. Every test needs a written status (per L2 key metric). Passes.

### 2. Is this the highest-leverage move available right now?
Check against `current.md` and the live Leverage Move:
- **Live L1 hard thing:** Testing Approach v5 to Brandon (PUBLISH verdict since 4/5, 23 workdays unshipped). Still unsent as of 2026-04-21 EOD.
- **Higher-leverage move exists.** A Gen4 readout is L2; sending v5 to Brandon is L1 and has been blocked for 23 workdays.
- **BUT:** Richard's explicit request is to analyze *this* readout. The filter doesn't tell me to refuse — it tells me the highest-leverage move is elsewhere. I do the analysis **and flag the drift**. This readout is the wrong thing to spend the next 90 minutes on if v5 is still in draft.

**Filter output:** Proceed with readout, but call the drift.

### 3. Does this reduce future decisions or friction?
Partially. A clean readout with an explicit "scale / hold / retest" recommendation prevents a second-guessing loop in MX sync and gives Lorena + Yun-Kang a shared reference. If the recommendation is vague, it creates *more* friction. So: only valuable if the recommendation is sharp. **Sharpen it.**

### 4. Is this within current context load?
Yes. soul.md + performance-marketing-guide.md + current.md already loaded. No additional organs needed. Passes.

---

## Readout (four-part, per performance-marketing-guide.md)

### Incrementality estimate
- Observed relative lift: **+13.9%** CVR (Gen4 vs Gen3), −11% CPA.
- 95% CI on rel lift: **[+1.8%, +26.0%]**.
- Against the pre-registered **≥5% incrementality bar: INCONCLUSIVE.** The point estimate clears 5%, but the CI straddles it — ~18% posterior probability the true lift is below 5% (rough Bayesian read with flat prior; exact Beta-Binomial posterior would tighten this but not change the qualitative answer).
- **Counterfactual caveat:** this is a concurrent 50/50, so no market-cutover counterfactual framing needed. Cleaner than most MX reads.

### Confidence (split per the guide)
- **Sign (Gen4 > Gen3):** HIGH. p=0.024, direction consistent across 4 weeks (assumed — Richard should eyeball weekly splits to confirm no late-week reversal).
- **Magnitude:** MEDIUM-LOW. Point estimate is healthy (+13.9%) but the CI lower bound (+1.8%) doesn't clear the 5% design threshold. Powered for 5% detection, got 13.9% — which means we're seeing a real effect but the test wasn't long enough to tightly bound it at the designed sensitivity.
- **Generalizability:** MEDIUM. "Business Pricing Exclusive" is a pricing-anchored claim. It likely travels to other price-sensitive LATAM contexts but should NOT be assumed to generalize to EU5/JP without a retest. AU is a closer analog than EU.

**Overall numeric confidence in "scale Gen4":** ~70%. Top-3 assumptions:
1. W3 creative fatigue flag did not cause end-of-window CVR decay that masks a larger early-window lift (needs weekly decomposition).
2. "Business Pricing Exclusive" messaging is compliant with MX legal/pricing claim rules for sustained use (not just test window).
3. Gen4's lift is driven by copy, not by confounded traffic mix (share of brand vs non-brand keywords was held constant across arms).

**Human-review flag: YES.** Total test spend $49.4K is at the >$50K threshold boundary. Any decision to roll Gen4 to 100% in MX, or replicate to another market, requires Richard + Brandon + Lorena sign-off before execution.

### Recommended next action
**Scale Gen4 to 100% in MX with a 2-week fatigue-guard window.** Not "retest" — the effect is real and the CPA win is material ($5 × monthly NB reg volume = meaningful). But scale conditionally:

- **Week 1–2 at 100%:** daily CVR + CTR monitoring. If CVR drops >10% below the 4.1% test mean in any 3-day rolling window, pause and investigate fatigue.
- **Queue Gen5 variant NOW.** Yun-Kang's W3 fatigue signal is the single biggest risk to scaling. Having a ready replacement compresses the response window from weeks to days if decay shows up.
- **Do NOT replicate to AU/EU/JP yet.** Run a scoped MX-to-AU retest (AU is closest analog) before generalizing. Different pricing claim norms, different keyword mix.

### Creative fatigue signal — rule in or rule out
**Cannot rule out from aggregate readout alone.** Yun-Kang's W3 flag is a directional warning that a 4-week aggregate can mask. Required before scaling:
- Pull **weekly CVR + CTR by arm** from DuckDB (`ps.v_daily WHERE market='MX' AND period_start BETWEEN '2026-W13-start' AND '2026-W16-end'`).
- Look for: monotonic CTR decline in Gen4 across weeks (fatigue tell), or CVR-stable-but-CTR-falling pattern (impression-level fatigue).
- If either pattern shows, the true steady-state lift is **lower than 13.9%** and may be below the 5% bar. Adjust the scale decision accordingly.

This weekly decomposition is a <30-min DuckDB pull. It should happen **before** a scale decision is communicated to Lorena.

---

## Tie to the Five Levels
- **L2 evidence.** Written test status for a closed test — directly on the L2 key metric.
- Readout should be saved to `shared/wiki/testing/` or the MX state file (`Kiro-Drive/state-files/mx-state.md`) for durability.

## Principle checks (soul.md "How I Build")
- **Principle 7 (human-in-the-loop high-stakes):** Applied — $49.4K test + scale decision flagged for Richard/Brandon/Lorena review.
- **Principle 3 (subtraction):** The readout could propose *more* tests. It proposes one (scoped MX→AU retest) and stages the rest. Passes.
- **Principle 8 (don't build):** No new tool proposed. Weekly decomposition uses existing DuckDB views. Passes.

---

## Next step

**Before communicating scale to Lorena:** Run the weekly CVR + CTR decomposition from DuckDB (`ps.v_daily`, MX, W13–W16, by arm). 30 minutes. That pull either rules out the W3 fatigue flag — in which case scale Gen4 to 100% in MX with the 2-week monitoring window and queue Gen5 — or it confirms decay and you drop the recommendation to "scale to 75%, accelerate Gen5, retest in 4 weeks."

**Reminder (flagged from filter step 2):** Testing Approach v5 to Brandon is still unsent at 23 workdays zero-L1. This readout is L2. Send v5 first thing AM before opening the DuckDB pull. It's a 10-min SEND, not a work session.
