# Evaluation: Grok Proposal #10 — high_stakes_log DuckDB Table

**Verdict: DEFER.** Existing tables cover 80% of the schema. The missing piece (a generalized "agent output + confidence + outcome" log across task types, not just forecasts) isn't yet justified — we don't have a reader for it (Loop 2 is inactive), we don't have enough volume to calibrate on (the blind A/B only happened 2026-04-22), and Grok is simultaneously proposing a metric (#5) and a separate logging mechanism (#9) that would either collide with this table or duplicate it. Revisit when Loop 2 reactivates AND we have ≥10 real high-stakes outputs with known outcomes.

---

## 1. What Grok is proposing

Schema: `created_at, task_type, confidence_pct, human_review_flagged, human_reviewed, outcome, output_ref, notes`

Intent: let the agent query past flagged outputs and learn calibration patterns.

## 2. What already exists

| Grok column | Existing coverage | Table |
|---|---|---|
| `created_at` | ✅ | `ps.forecasts.created_at`, `ops.hook_executions.created_at`, `main.autoresearch_experiments.created_at` |
| `task_type` | ⚠️ Partial — only for forecasts | `ps.forecasts` implicitly covers forecast/projection. No row for WBR/test_readout/pacing. |
| `confidence_pct` | ⚠️ Indirect — stored as band, not point | `ps.forecasts.confidence_low / confidence_high` (CI band, not single pct) |
| `human_review_flagged` | ❌ Not stored anywhere |  |
| `human_reviewed` | ❌ Not stored anywhere |  |
| `outcome` | ✅ For forecasts | `ps.forecasts.scored`, `ps.forecasts.score` (HIT/MISS/SURPRISE), `ps.forecast_accuracy` (aggregate) |
| `output_ref` | ❌ Not stored; forecasts don't link back to the artifact that cited them |  |
| `notes` | ✅ | `ps.forecasts.notes` |

**Bottom line:** `ps.forecasts` (2,415 rows, 688 already scored, hit_rate tracked in `ps.forecast_accuracy`) already does HIT/MISS scoring for forecasts — which is the high-volume case. What it doesn't do:
- Generalize beyond forecasts (WBR narratives, test readouts, pacing calls)
- Store a single numeric confidence % (only a CI band)
- Track whether a human review was flagged AND whether it actually happened
- Link back to the artifact that used the number

Additional existing infrastructure:
- `ps.calibration_state` — already tracks calibration factors by market/metric, hit_rate, mean_error_pct, updated_at. **This is the Grok calibration-metric target.** No new table needed for calibration.
- `ps.callout_calibration` — already tracks pass/revise rates + quality lenses for callout outputs. Covers the "WBR narrative" high-stakes use case.
- `ps.dive_forecast_calibration` — forecast-specific calibration view.
- `main.autoresearch_experiments` — logs A/B decisions with scores, fast_fail, decision — the pattern Grok is reinventing for high-stakes outputs.

## 3. Double-counting check: #5 + #9 + #10

Grok is proposing three overlapping things in the same batch:
- **#5 Agent Confidence Calibration metric** — reads "average confidence % vs actual accuracy." Requires a log of (confidence, outcome) pairs.
- **#9 Guardrail Usage Log** — "every time a high-stakes output is produced, append: date, task_type, confidence, review_flagged, reviewed, friction notes." A plain-text append log.
- **#10 high_stakes_log DuckDB table** — same columns as #9, stored in DuckDB.

**#9 and #10 are the same thing with different storage.** Picking both = duplicate writes with drift risk. Picking just #10 without #9 = the agent has to write to DuckDB on every high-stakes output, which couples behavior change to DB writes (fragile). Picking just #9 without #10 = #5's calibration metric has to parse a markdown log, which is worse than SQL.

If any of these get built, the question is: one append-only markdown log (cheap, portable, agent-readable) OR one DuckDB table with a sync hook, not both. Grok is proposing both without saying which wins.

## 4. Architectural gap: who writes to high_stakes_log?

Grok's proposal does not specify the writer. The options are all bad right now:

1. **Agent writes on every high-stakes output.** Couples behavior change (producing a forecast) to state mutation (writing to DuckDB). Every agent instance needs DuckDB write access. High failure mode: agent produces the artifact but skips the log write, so the log undercounts.
2. **Hook writes after the fact.** Requires a hook that parses artifacts for confidence pct + review flags. We don't have that pattern anywhere. Building the parser is most of the work.
3. **Richard manually logs.** Violates "invisible over visible" (principle #5) — and Richard won't do it consistently. The whole point of the guardrail file is that the agent enforces it.

None of these are designed in Grok's proposal. That's a load-bearing omission, not a detail.

## 5. Nervous-system Loop 2 check

Loop 2 (Prediction Scoring) in nervous-system.md is currently **inactive**:
> "Currently inactive — predicted QA cleared from Eyes (stale content experiment, Run 18). Reactivate when AM-2 generates fresh predictions."

Loop 2 is about predicted meeting questions (HIT/MISS/SURPRISE), not forecast confidence — but the shape of the loop is exactly what would consume `high_stakes_log` if it existed. Building the table before the reader is active is infrastructure-ahead-of-demand. We'd have a log with no scorer, which is how tables become dead data.

The forecast-specific scoring already runs via `ps.forecast_accuracy` + `ps.calibration_state`. A general-purpose high_stakes scorer for WBRs/test readouts/pacing would need a mechanism to determine "outcome" — and for WBR narratives there is no mechanical ground truth, only Richard's retrospective judgment, which makes the `outcome` column mostly NULL.

## 6. Check against the 8 principles

- **Subtraction before addition (#3):** FAILS. `ps.forecasts` + `ps.calibration_state` + `ps.callout_calibration` + `main.autoresearch_experiments` already cover the forecast and callout cases. Grok is adding a table rather than extending existing ones with 2 missing columns (`human_review_flagged`, `output_ref`).
- **Structural over cosmetic (#2):** NEUTRAL. A table is structural. But the behavior change is whether the agent actually writes to it, which isn't designed.
- **Invisible over visible (#5):** RISK. If the agent has to stop and write a log row on every high-stakes output, that's visible friction unless automated — and automation isn't specified.
- **Human-in-the-loop on high-stakes (#7):** This is the principle the proposal is trying to serve. The guardrail file already enforces the *behavior* (explicit confidence, top-3 assumptions, human-review flag). What's missing is *observability over time*, and the question is whether we need a dedicated table or whether existing tables + a 2-column extension to `ps.forecasts` would do.
- **Device.md check (#8):** The friction is "I can't see calibration patterns across my high-stakes outputs." Frequency is currently very low — the guardrails file was adopted 2026-04-22, so we have days of data, not weeks. We don't have 3+ instances/week of the need to query this. One-off curiosity doesn't justify a table.

## 7. Minimal alternative (if we decide we need something)

Instead of a new table, extend what exists:

1. Add 2 columns to `ps.forecasts`: `human_review_flagged BOOLEAN`, `human_review_completed BOOLEAN`. Covers forecasts.
2. For non-forecast high-stakes outputs (WBR narratives, test readouts), `ps.callout_calibration` already covers callouts. Test readouts don't have a table yet, but they have low volume — a plain markdown log is fine.
3. Loop 2 reactivation (when AM-2 writes fresh predictions) is the trigger that creates actual reader demand. Revisit this proposal then.

Confidence on this verdict: 70%. The 30% uncertainty is whether Richard wants the generalized log *specifically* to force himself into a habit of quantifying confidence on non-forecast outputs — in which case a cheap markdown append (Grok's #9, not #10) would be the structural nudge, not a table.

## Verdict

**DEFER.** Reasons:
1. `ps.forecasts` + `ps.calibration_state` + `ps.forecast_accuracy` + `ps.callout_calibration` already cover forecast and callout high-stakes — the two task_types with actual volume.
2. Missing columns (`human_review_flagged`, `output_ref`) are a 2-column `ALTER TABLE ps.forecasts` away, not a new table.
3. No writer is specified. Coupling high-stakes behavior to DB writes without a design is fragile.
4. Loop 2 (the conceptual reader) is inactive. Building a log with no scorer = dead data.
5. Grok is double-counting across #5, #9, #10 — pick one storage, not two.
6. High-stakes volume since guardrail adoption (2026-04-22) is too small to calibrate against. Need ≥10 real outputs with known outcomes before building infrastructure.

**Revisit when:** Loop 2 reactivates (AM-2 writing fresh predictions) AND we have ≥10 high-stakes outputs logged in any form AND Richard confirms the cross-task-type generalization is the actual need (vs. just extending `ps.forecasts`).
