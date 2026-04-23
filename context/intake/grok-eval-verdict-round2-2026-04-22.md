# Grok Follow-On Round 2 — Blind Test Verdict

**Date:** 2026-04-22
**Protocol:** architecture-eval-protocol.md, with custom test design per proposal type
**Method:** 11 proposals × (comparative or A/B test as appropriate) × blind evaluator = 14 sub-agent invocations + 3 blind evals
**Randomization:** seed 43 for A/B pairs (tests 6, 7, 8)
**Blind evaluator:** fresh `general-task-execution` sub-agents, no knowledge of which arm is which

---

## Headline

**10 of 11 Grok proposals rejected or deferred. 1 partial adoption (🟡 tier convention for pacing alerts).**

This is the opposite pattern of round 1, where 4 of 6 files won empirically. The difference: round 1 files filled real gaps the existing system didn't explicitly cover. Round 2 proposals either duplicate machinery that already runs, reinvent tables that already exist, or propose ceremonies that would violate soul.md principles they claim to respect.

---

## Per-proposal verdicts

### Group 1 — Comparative tests (Grok artifact vs existing equivalent)

| # | Proposal | Verdict | Rationale |
|---|---|---|---|
| 1 | `excel_ingest.py` | **REJECT** | Grok's script is DOA — `~` doesn't expand in Python glob, wrong table names (`FROM ps` — `ps` is a schema), single-sheet `pd.read_excel()` drops data on CCP Q1'26 xlsx, bogus routing heuristic. Existing `dashboard-ingester/ingest.py` (2,355 lines) handles the real WW Dashboard workflow with auto-detection, schema-qualified MotherDuck writes, INSERT OR REPLACE idempotency, per-market callout generation, and downstream pipeline triggers. Replacing 2,400 lines with 35 broken lines is not subtraction. |
| 2 | `anomaly_detector.py` | **REJECT** | On the same W16 MX data: existing MX W16 analyst brief surfaces 8 meaningful flags + 5 ingester anomalies (NB CVR 3-week decline, NB CPA multi-month high, NB CPC 12-week high, Brand coverage anomaly, Sat-18 softness, ie%CCP cadence change, Slack signal, SURPRISE forecast). Grok's script (even fixed) produces 11 false positives — every single flag is weekday/weekend cadence — and 0 true positives. Strict regression. |
| 3 | `am-triage-enhanced.md` | **REJECT** | 0 of 6 Grok steps are net-new. Grok's 6-step version silently deletes the tested protections: signal routing, admin keyword detection, 7-business-day early-start rule, bucket cap enforcement, Engine Room auto-demotion + BAU decomposition, Wiki Pipeline Phase 1B, 11-step Portfolio Scan, interactive Phase 2, hook-execution logging, Asana-write guardrails. Also invents `eyes.md` (not an organ) and `rsw-channel` (not a real channel ID). Cannot execute — no field GIDs. |
| 4 | Pacing Alert | **PARTIAL ADOPT** | Every substantive piece already ships — `ps.monthly_pacing` view is live, daily brief Section 9 prints one-liners with 🔴/🟢 tiering, am-backend fires on morning routine. Grok's real add-value: explicit 10%/20% thresholds as a convention, and the 🟡 middle band for markets in the 90–110% window. **Adopt: update am-backend protocol Section 9 rendering spec** to codify (🔴 >±20pp, 🟡 ±10–20pp, 🟢 within ±10pp). No new hook. No new file. |
| 5 | Agent Confidence Calibration metric | **REJECT — Reactivate Loop 2 instead** | nervous-system.md Loop 2 (Prediction Scoring) is the existing equivalent. Currently inactive because AM-2 stopped writing predicted QA to Eyes. Grok's proposal drops SURPRISE (the overconfidence-vs-blindspot distinction), has no target, no organ routing, no worked example. The quantitative version already runs in production: `ps.forecasts` with confidence bands + `ps.forecast_accuracy` aggregating hit_rate_pct (MX regs 63.6% hit / 16.3% avg err across 22 scored rows). Gap is activation, not a missing metric. |

### Group 2 — A/B tests (control vs treatment with Grok's tool loaded)

| # | Proposal | Blind Verdict | Reasoning |
|---|---|---|---|
| 6 | Test Readout Analyzer | **CONTROL wins** | ARM-X (performance-marketing-guide alone) produced a clearly better readout than ARM-Y (guide + Grok tool). ARM-Y miscalibrated confidence upward (0.70 vs ARM-X's calibrated 0.45), conflated designed MDE with achievable MDE (the test was underpowered — ~9% of required n), recommended "scale with guardrails" inverting the gate/action sequence. ARM-X correctly said "don't scale yet, pull weekly splits first" and actively pulled market-level fatigue evidence. The tool wrapping *hurt* output quality — it made the agent simulate structure instead of do the math. |
| 7 | WBR Narrative Draft | **CONTROL wins decisively** | Existing analyst → writer → reviewer pipeline produced a callout that matched the W16 analyst brief exactly ($107K projection, +205% OP2 spend, 70% ie%CCP, 2 em-dashes, ~135 words). Grok's one-shot tool produced a draft with 6 em-dashes (direct style-rule violation), ~180 words, $105K/+199% numbers that miss the brief, an unverified FX claim, and an unsupported Sparkle→NB cannibalization hypothesis. Bypassing the analyst-writer-reviewer chain degrades output — the pipeline exists for a reason. |
| 8 | Creative Fatigue Scanner | **TREATMENT wins narrowly** | Both arms reached same fatigue diagnosis, same action (refresh as variant test), same confidence (~90%). ARM-X (control, guide alone) produced the tightest analytical core — a 6-row hypothesis-elimination table. ARM-Y (with simulated scanner) produced better decision packaging — explicit Test Analysis Protocol headers, soul-check, Five Levels tie-in, go/no-go thresholds, tough-question prep. Narrow edge to treatment. **But flag:** the "scanner" tool doesn't actually exist; ARM-Y simulated its output. The win is partly a packaging effect, not a real tool capability. |

### Group 3 — Reasoning-based evaluations

| # | Proposal | Verdict | Rationale |
|---|---|---|---|
| 9 | `guardrail-usage-log.md` | **REJECT — build retroactive DuckDB view instead** | The guardrail already lives in the artifact (high-stakes-guardrails.md enforces confidence + assumptions + review flag inline). session-log.md (2,160 lines) already narrates every high-stakes output with topic, confidence posture, assumption shifts, review-gate status, friction. Grok's prospective log violates subtraction-before-addition (#3), invisible-over-visible (#5), and routine-as-liberation (#1). Real alternative: a 30-line `ps.v_high_stakes_outputs` view parsing session-log entries retroactively. Zero habit overhead, append-only reuse. Grok's field schema is useful as the view's output columns — steal that, drop the log. |
| 10 | `high_stakes_log` DuckDB table | **DEFER** | Existing tables already cover 80% of Grok's schema: `ps.forecasts` (2,415 rows, 688 scored HIT/MISS, confidence bands, actuals, error_pct), `ps.calibration_state` (already THIS is the #5 metric source), `ps.forecast_accuracy` (hit_rate aggregation), `ps.callout_calibration` (callout calibration). Missing columns (`human_review_flagged`, `output_ref`) are a 2-column `ALTER TABLE ps.forecasts`, not a new table. Grok doesn't specify who writes to the table. Loop 2 (the conceptual reader) is inactive. Building a log before the scorer = dead data. Revisit when Loop 2 reactivates AND ≥10 real high-stakes outputs exist AND cross-task generalization is confirmed vs just extending ps.forecasts. |
| 11 | Validation Test Ceremony | **REJECT — self-grading rubric trap** | The 4 scoring dimensions (confidence quantification, review flag clarity, actionability, format adherence) are a direct mirror of high-stakes-guardrails.md Required Behavior and am-triage.md Daily Brief Output Format — the rubric IS the answer key. Producer == grader in a single turn, no independent evidence generated, "mental comparison to 2 days ago" is un-verifiable. Contrasted with today's architecture-eval-protocol (36-invocation blind A/B with fresh evaluator sub-agents) which produced actionable signal (9/12 favored treatment). Violates soul.md principles #2, #3, #5. Salvageable version: use archived controls from `shared/tmp/grok-eval/control/` as a reservoir, spawn fresh blind evaluators against real future high-stakes outputs. |

---

## Pattern across round 2

- **Grok proposals that replace existing machinery** (excel_ingest, anomaly_detector, am-triage-enhanced, agent-confidence-calibration): 0-for-4. Each one either doesn't run, deletes tested behavior, or loses diagnostic sophistication.
- **Grok proposals that add net-new behavior** (validation-ceremony, guardrail-usage-log): 0-for-2. Both violate soul.md principles they claim to respect.
- **Grok proposals that layer new infrastructure on working systems** (high_stakes_log table, Test Readout Analyzer, WBR Narrative Draft): 0-for-3. Infrastructure-ahead-of-demand, tool-wrapping degrading the underlying quality, or bypassing validated pipelines.
- **Grok proposals with a genuine partial win**: 1-for-2 (Pacing Alert's 10%/20% threshold convention + 🟡 tier; Creative Fatigue Scanner's packaging effect).

The one pattern that produces real value: **small convention codifications that tighten existing behavior**. The patterns that don't produce value: new scripts, new tables, new protocols, new ceremonies, new tools.

## Meta-lesson

Round 1's 4-of-6 adoption was because those files forced explicit output shapes on tasks where the existing system had only implicit conventions (confidence scores, WBR structure, daily brief format, routing protocol). That's a real gap-filler.

Round 2's 10-of-11 rejection is because once those gaps are filled, further proposals cross into duplicating mature systems or adding ceremony. The existing system has already absorbed what was genuinely missing.

**The signal: external AI review is high-leverage on a first pass when gaps exist. Diminishing returns after the first round. By the second round, the existing system's accumulated failure-mode fixes outweigh any new framing an external reviewer can bring.**

## Concrete actions (awaiting your call)

1. **Adopt the Pacing Alert convention edit** (proposal #4) — append a threshold-tier rule to am-backend protocol Section 9 rendering spec: 🔴 >±20pp, 🟡 ±10–20pp, 🟢 within ±10pp. ~5 lines. No new file.
2. **Reactivate Loop 2 (Prediction Scoring)** (proposal #5 reframe) — restore AM-2 predicted-QA generation OR extend Loop 2 scope to agent-text-output grain inside nervous-system.md. This was already OPEN from yesterday's session-log triage.
3. **Build `ps.v_high_stakes_outputs` view** (proposal #9 reframe) — ~30-line SQL view over session-log, uses Grok's field schema as output columns. Defer until we have 30+ days of session-log entries covering high-stakes outputs.
4. **Skip everything else** — proposals 1, 2, 3, 6, 7, 8 (the tool version), 10, 11 all rejected.

## Evidence files

- Proposed artifacts: `shared/tmp/grok-eval-2/proposed/*.md` and `.py`
- Comparative analyses (Group 1 + 3): `shared/tmp/grok-eval-2/existing/`
- A/B pair outputs: `shared/tmp/grok-eval-2/control/` and `shared/tmp/grok-eval-2/treatment/`
- Blind verdicts: `shared/tmp/grok-eval-2/blind-eval/`
- Randomization: `shared/tmp/grok-eval-2/randomization.csv`
