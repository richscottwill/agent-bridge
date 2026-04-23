# Head-to-Head: Grok `05-agent-confidence-calibration.md` vs existing Loop 2 (nervous-system.md)

**Date:** 2026-04-22
**Files compared:**
- Proposal: `shared/tmp/grok-eval-2/proposed/05-agent-confidence-calibration.md` (5 bullets, ~10 lines)
- Existing: `shared/context/body/nervous-system.md` Loop 2 "Prediction Scoring" + Loop 1 "Decision Audit"
- Data substrate: `ps.forecasts`, `ps.forecast_accuracy` (DuckDB)

**Verdict: Loop 2 is the existing equivalent. The gap is not a missing metric — it is a missing reactivation of an existing loop.** This was explicitly flagged in the 2026-04-22 session-log entry where this exact proposal was triaged (see §4). Adopting Grok's proposal as a net-new metric would add surface area while the loop it duplicates sits dormant with its reactivation trigger fully documented.

---

## 1. Side-by-side: what each design tracks

| Dimension | Grok proposal | Loop 2 (existing, inactive) | Loop 1 (existing, active-PENDING) | ps.forecasts + ps.forecast_accuracy |
|-----------|---------------|-----------------------------|-----------------------------------|-----------------------------------|
| **Unit of measurement** | "Each high-stakes output" (agent statement) | Predicted questions asked in meetings | Decisions with predicted outcomes (D1–D7) | Quantitative forecasts (regs, cost, CPA) per market/metric/period |
| **Scoring labels** | HIT / MISS | HIT / MISS / SURPRISE | VALIDATED / PARTIALLY / INVALIDATED / PENDING | HIT / MISS / SURPRISE (stored in `ps.forecasts.score`) |
| **Confidence representation** | "Stated %" attached to each output (55%, 70%) | Not explicit — binary predicted-or-not | Principle-weight + narrative outcome | `confidence_low` / `confidence_high` bounds (DOUBLE) per forecast |
| **Cadence** | Weekly calibration curve | Daily scoring + weekly aggregate (≥60% hit rate target) | Monthly audit; per-decision target dates (D3 May 2026, D1/D2 Jul 2026) | Continuous (scored when actuals land) |
| **Aggregation** | "Of the things I said 55% about, was I right 55% of the time?" (reliability diagram) | Rolling hit rate, weekly aggregate | On INVALIDATED → review driving principle | `ps.forecast_accuracy` view: total_scored, hits, misses, surprises, avg_error_pct, hit_rate_pct per market×metric |
| **Feedback action** | "Adjust future confidence scores" | Route correction: Brain updates calibration, Eyes updates baseline | Update the driving principle when invalidated | Feeds WBR callouts + `ps.forecast_accuracy` (live; MX regs 63.6% hit / 16.3% avg err / 22 scored) |
| **Status** | Proposed | **Inactive** — AM-2 stopped generating predicted QA (Run 18 stale-content experiment) | Active (5 PENDING audits awaiting data) | Active (22 MX scored rows, live accuracy view running) |

---

## 2. Where Grok's HIT/MISS maps onto the existing stack

Grok's pattern is **already present three times in the existing system**, each tuned to a different unit of analysis:

- **Quantitative forecasts (continuous, automated):** `ps.forecasts` already carries `predicted_value`, `confidence_low`, `confidence_high`, `actual_value`, `error_pct`, `scored`, `score` (HIT/MISS/SURPRISE). `ps.forecast_accuracy` already aggregates hit_rate_pct, avg_error_pct, hits/misses/surprises per market × metric. The loop is closed and scoring is running today.
- **Meeting communication predictions (event-driven, manual):** Loop 2 — HIT / MISS / SURPRISE on predicted questions, daily + weekly, target ≥60%. Inactive only because the upstream AM-2 hook stopped writing predicted QA to Eyes.
- **Decision-level predictions (strategic, slow):** Loop 1 — VALIDATED / PARTIALLY / INVALIDATED / PENDING on decisions, monthly cadence, with driving-principle update on INVALIDATED. This is the "calibration curve" at the decision grain. Five PENDING now (D1, D2, D3, D4, D7) with audit dates mapped.

Grok's proposal is a fourth layer targeting **agent text outputs** ("here's my 70%-confident answer"). That's a legitimately different grain from the three above — but the mechanism is identical, and the existing machinery could absorb it by adding a fourth table/loop if needed, not by inventing a new standalone metric on `rw-tracker.md`.

---

## 3. What the existing Loop 2 already encodes that Grok's 5 bullets lose

Reading Loop 2 line-by-line:

1. **SURPRISE label.** Grok has HIT/MISS only. Loop 2 distinguishes MISS (predicted but didn't happen) from SURPRISE (happened but not predicted). This is the difference between "overconfident" and "blindspot" — collapsing them hides whichever failure mode is actually in play. `ps.forecasts.score` uses the same three-class scheme for the same reason.
2. **Reactivation trigger is already defined.** "AM-2 hook writes ≥3 predicted questions to Eyes 'Predicted Questions' section. Once present, Loop 2 auto-resumes daily scoring." Grok didn't need to propose anything — the restart condition exists in the protocol.
3. **Scoring protocol is spec'd.** "After each meeting/event, compare predicted questions to actual questions asked." Grok's "after outcome is known, score HIT/MISS" is a less-specific restatement.
4. **Target is quantified.** ≥60% hit rate. Grok has no target.
5. **Routing on mismatch is defined.** "Brain updates confidence calibration, Eyes updates the AU metric baseline." Grok stops at "adjust future confidence scores" with no organ-level routing.
6. **Worked example is in the protocol.** The nervous-system.md preamble literally uses a calibration scenario: "Brain predicted AU CPA would drop 15%... actual drop was 8%. Mismatch logged. Correction routed... optimism bias on new launches feeds back into future predictions." Grok offers nothing at this specificity.

Grok's proposal is a 10-line sketch of what Loop 2 already is, minus the three-class labels, minus the reactivation trigger, minus the target, minus the routing, minus the worked example.

---

## 4. The session-log already triaged this exact proposal

From `shared/context/intake/session-log.md`, 2026-04-22 entry on the Grok follow-on triage:

> "Agent Confidence Calibration = nervous-system.md Loop 2 (currently inactive because AM-2 not generating predicted QA)."

And the explicit recommendation from that session:

> "Recommended instead: ... (2) reactivate nervous-system.md Loop 2 Prediction Scoring instead of building Agent Confidence Calibration from scratch ... Status: OPEN — awaiting Richard's call on whether to reactivate Loop 2 now or defer."

So this is not a new evaluation. It's the second pass on an already-made call. The answer is the same: Loop 2 is the equivalent. Build nothing. Reactivate.

---

## 5. ps.forecasts schema confirms the quantitative layer is already built

`ps.forecasts` columns (from `information_schema.columns`):

```
forecast_id, market, channel, metric_name, forecast_date, target_period, period_type,
predicted_value, confidence_low, confidence_high, method, actual_value, error_pct,
scored, score, notes, created_at, lead_weeks, prediction_run_id
```

`ps.forecast_accuracy` columns:

```
market, metric_name, total_scored, hits, misses, surprises, avg_error_pct, hit_rate_pct
```

Live data example (from today's session): MX regs 63.6% hit rate / 16.3% avg err / 22 scored rows; MX brand_regs 0% hit / 100% upward surprises across 13 scored weeks (W12–W16 run).

Translation: the quantitative version of Grok's proposal **is in production**. Forecasts carry confidence bands, actuals score them, an accuracy view aggregates hit rates, and today's session pulled those numbers to sanity-check the MX $1.3M scenario. Adding "Agent Confidence Calibration" to `rw-tracker.md` as a separate metric would stand up a duplicate reliability scorecard alongside one that already exists in DuckDB.

---

## 6. Principle check

| soul.md principle | Grok's proposal | Loop 2 reactivation |
|-------------------|-----------------|---------------------|
| #2 Structural over cosmetic | Adds a new rw-tracker section (cosmetic surface) | Flips an existing loop back on (structural) |
| #3 Subtraction before addition | Adds a fourth calibration layer alongside three existing ones | Zero addition — reuses existing machinery |
| #4 Protect the habit loop | Introduces a new weekly artifact cadence competing with Loop 3 Friday cadence | Restores the documented daily+weekly cadence |
| #5 Invisible over visible | New visible metric, novelty decay risk | Resumes a loop that already ran quietly when active |

Grok's proposal violates #2, #3, and #5. Loop 2 reactivation embodies all four.

---

## Verdict

**Loop 2 is the existing equivalent. Grok's proposal duplicates it with fewer features.**

The gap in today's system is not a missing metric. It is a missing **activation** — AM-2 stopped writing predicted QA to Eyes, so the loop that would score agent predictions has no input stream. The fix is to either:

1. Restore AM-2 predicted-QA generation (surfaces ≥3 questions per meeting into Eyes "Predicted Questions"), triggering Loop 2 auto-resume per the protocol, OR
2. If the target is agent **text-output** confidence specifically (not meeting QA and not quantitative forecasts), extend Loop 2's scope to include a fourth grain — but do it inside the existing nervous-system.md structure with HIT/MISS/SURPRISE labels and organ-level routing, not as a standalone `rw-tracker.md` table.

Either way: no net-new metric. Grok's proposal is rejected on grounds of duplication and principle-violation. The right behavioral change is reactivating Loop 2, which was already flagged as OPEN pending Richard's call in today's session-log.

**No adoption.** **Reactivate Loop 2** (pending Richard's go-ahead) — that's the one line of work this proposal is pointing at.
