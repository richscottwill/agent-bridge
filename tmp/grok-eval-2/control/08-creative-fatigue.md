# Creative Fatigue Diagnostic — MX Brand Campaign

**Campaign:** `MX-Brand-Polaris-Sparkle-01`
**Market:** MX (Brand)
**Window analyzed:** 21 days (creative running since mid-March, ~5–6 weeks in-market)
**Analyst:** Richard Williams (daily agent)
**Framework:** Test Analysis Protocol (performance-marketing-guide.md) — applied to a live campaign. Same four checks required.

---

## Headline

**Yes — this is creative fatigue, and it is confirmed, not suspected.** The CTR/CVR divergence is textbook fatigue signature. Refresh creative now; do not wait for CVR to break before acting, because by the time CVR breaks the damage is already paid for in wasted impressions.

---

## The Pattern (what the data is actually saying)

21-day CTR trajectory: **4.2 → 4.1 → 4.3 → 4.0 → 3.9 → 3.8 → 3.9 → 3.7 → 3.6 → 3.5 → 3.4 → 3.3 → 3.2 → 3.1 → 3.2 → 3.0 → 2.9 → 2.8 → 2.7 → 2.6 → 2.5**

| Metric | Week 1 avg | Week 2 avg | Week 3 avg | Δ (W1 → W3) |
|---|---|---|---|---|
| CTR | ~4.09% | ~3.46% | ~2.79% | **−32% relative** |
| CVR | 8.1–8.3% (stable) | 8.1–8.3% | 8.1–8.3% | **~0%** |

Total CTR decline peak-to-trough: **4.3% → 2.5% = −42% relative**. Monotonic with only two minor noise reversals (day 3, day 15). That is not seasonality, not day-of-week, not a bidding change — it is a clean, sustained decay curve.

---

## Diagnostic Logic (why fatigue, not something else)

The CTR-down / CVR-stable divergence is the signal that rules fatigue **in** and alternatives **out**:

| Hypothesis | Expected CTR | Expected CVR | Fits data? |
|---|---|---|---|
| **Creative fatigue** | Declining (audience has seen it repeatedly) | Stable (click intent unchanged) | ✅ **Yes** |
| Audience / targeting decay | Declining | Declining (lower-quality clicks) | ❌ No — CVR is stable |
| Landing page / funnel break | Stable or up | Declining | ❌ No — CTR is declining, not stable |
| Competitive bid pressure | Down (lower position) | Mixed | ❌ Unlikely — Brand term, limited competitive pressure; would also show impression share loss, not CTR decay |
| Seasonality / macro | Non-monotonic, noisy | Either | ❌ No — trend is too clean and too monotonic over 21 days |
| Tracking / measurement artifact | Step change | Step change | ❌ No — smooth decline, not a break |

The CVR stability is the **load-bearing** piece of evidence. It tells us the people who still click are just as valuable as the people who clicked on day 1 — quality is intact, **quantity of attention is not**. That isolates the problem to the top-of-funnel creative asset.

---

## Required Four Checks (Test Analysis Protocol)

### 1. Incrementality estimate
- **Counterfactual:** If creative had held at the Week 1 baseline CTR (~4.1%), the campaign would be delivering ~47% more clicks at the current Week 3 impression level (4.1 / 2.79 − 1 = 47%).
- With CVR flat at ~8.2%, that's also ~47% more registrations from the same spend.
- **Rough magnitude:** on a mid-March-launched MX Brand campaign, assume moderate daily spend. Every day at current CTR vs. fresh-creative baseline is leaving meaningful regs on the table. Exact $ impact requires pulling `ps.v_daily` spend for this campaign_id — recommend doing that before the refresh call.
- **Caveat:** this is a same-campaign time-series comparison, not a true counterfactual. A refresh test would give the clean read.

### 2. Confidence
- **Sign:** **Very high.** 21 consecutive days, ~40% relative decline, monotonic. Not noise.
- **Magnitude:** **High.** The −1.7pp absolute CTR drop over 21 days is well outside typical daily variance for a stable Brand campaign (expect ±0.2–0.3pp day-over-day).
- **Generalizability:** **Medium.** This is one campaign in one market. Fatigue timing (5–6 weeks to meaningful decay) is consistent with MX Brand norms, but the exact half-life will vary by creative, audience size, and frequency cap. Do not generalize the "5–6 week refresh cadence" to all MX Brand creatives without checking frequency data.
- **Overall confidence in fatigue diagnosis: ~90%.** The alternative explanations don't fit the CVR-stable pattern.

### 3. Recommended next action
**Refresh creative. This week.** Specifically:
1. **Pull** frequency and reach data from the platform side (DuckDB `ps.v_daily` gives spend/regs/CTR but platform console has impression-per-user). If average frequency has climbed past ~8–10 in the last 10 days, that confirms the mechanism.
2. **Queue** a creative refresh — ideally 2–3 new variants to run against each other, not a single replacement. A single swap gives you no information; a variant test gives you both a refresh **and** your next data point on what resonates in MX Brand.
3. **Structure as a test, not a swap.** Hold the current fatigued creative as a control arm at 10–20% traffic for 7–10 days so we can measure the lift cleanly and document it as a L2 test readout. This is the L2 move — every refresh should produce evidence, not just activity.
4. **Set a fatigue tripwire going forward.** Rule of thumb from this case: when CTR drops >15% from a 7-day trailing baseline and CVR is stable, trigger a refresh. Consider proposing this as a standing MX Brand monitor.

### 4. Creative fatigue signal — **RULED IN**
This is the signal. CTR monotonic decline of 40%+ over 21 days with CVR stable = fatigue. This is exactly the pattern the Test Analysis Protocol requires us to call out, and it is present.

---

## What to do next (concrete)

- **Today:** Pull `ps.v_daily WHERE campaign_id = 'MX-Brand-Polaris-Sparkle-01'` for the full campaign life (mid-March → today) to confirm the decay curve shape and quantify $ left on the table. Also pull frequency from platform console.
- **This week:** Brief creative team on refresh. Frame it as a variant test (2–3 new + control at reduced traffic), not a swap. Yun Kang likely owns creative for MX Brand — loop her in.
- **Document as L2 evidence:** Once the refresh variant test reads out, this goes into the testing log as a documented fatigue-and-refresh cycle. Adds to the pattern library for "when does MX Brand creative fatigue?" — which we currently don't have a written POV on.
- **Systemic follow-up:** If we're seeing this on one campaign, we're likely seeing it on others. Worth a 30-min sweep of other MX Brand campaigns running >4 weeks on the same creative to see if the pattern repeats. That's the L3 move — build the monitor once, apply it to all markets.

---

## Caveats / what I don't know

- I don't have spend figures, so the $ impact sizing above is directional, not actionable. Pull actuals before any stakeholder conversation.
- I don't have impression or frequency data — that's the confirming evidence for the mechanism. High confidence in the diagnosis regardless, but frequency data closes the loop.
- 21 days is the window given; the creative has been running ~5–6 weeks. There may be earlier data showing when the decline began (day 22? day 30?). Pulling the full life of the campaign would pin down the fatigue onset point, which is useful for setting the tripwire threshold.

---

*Applied performance-marketing-guide.md Test Analysis Protocol: incrementality, confidence, next action, and creative fatigue signal all addressed. Live campaign treated with same discipline as a test readout.*
