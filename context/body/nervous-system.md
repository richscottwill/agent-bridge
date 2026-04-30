<!-- DOC-0227 | duck_id: organ-nervous-system -->





# Nervous System — Feedback, Calibration & Learning

*Operating principle: Invisible over visible. Surface insights that lead to structural changes — not reports that require Richard to act on them. When a pattern is STUCK for 3 weeks, propose a structural fix.*

Last updated: 2026-04-05 (Karpathy Run 28 — Loop 3 split into Active/New/Root Cause subsections)
Created: 2026-03-20

---






## Governance

All changes to this file are governed by the Karpathy agent. The heart loop cascades data into the tracking tables. Karpathy owns the loop definitions, metrics, and compression of this organ.

**Data flow:** EOD-2 hook → updates tracking tables (Loop 4 delegation status, Loop 5 word counts, Loop 9 communication metrics) → Karpathy experiments on the organ itself (COMPRESS/REWORD/etc.) → results logged to DuckDB `autoresearch_experiments`.

## Five Levels Position






### Parallel Level Activity
**Gate-breaker priority (shortest path to "shipped" wins):** Playbook formalization (fastest — already validated 4/2) → IECCP FAQ (one-page, clear scope) → Year-One one-pager → Negative keyword list (breaks drought but doesn't show strategic thinking).







### L1 Gate-Breaker Candidates (from 4/2 Deep Dive)

| Candidate | Due | Scope | Status |
|-----------|-----|-------|--------|
| Year-One Optimization one-pager | Apr 16 | Smaller than Testing Approach | Unstarted |
| IECCP FAQ | Apr 9 | One-page reference doc | Unstarted |
| Negative keyword list | Immediate | Tactical but shippable today | Unstarted |
| Market Expansion Playbook | — | Already presented 4/2, formalize | Presented |

Richard's strongest group visibility moment in 9+ tracked sessions: playbook presentation on 4/2.






[38;5;10m> [0m### Loop 3: Pattern Trajectory[0m[0m
rw-tracker.md | Weekly (Friday) | Rate each tracked pattern as IMPROVING, STUCK, WORSENING, or RESOLVED. If a pattern stays STUCK for 3+ weeks, stop relying on willpower and make a structural change — e.g., replace "I'll remember to check my dashboard" with a scheduled notification, or swap "I'll try harder at the gym" for a session with a trainer. **Root cause:** If you're avoiding visibility (Level 1), everything downstream stalls — you can't fix patterns you refuse to look at.
#### Active Patterns (3)
| Pattern | Duration | Status | Gate/Fix |
|---------|----------|--------|----------|
| Visibility avoidance | 11wk | WORSENING | Testing Approach doc (L1 gate) |
| Admin displacement | 3wk | STUCK | Trainer escalation triggered |
| Reactive fire drills | 3wk | STUCK | Pre-written response templates needed |






#### New Patterns (2)
| Pattern | Duration | Source |
|---------|----------|--------|
| Have Backbone avoidance | 1wk | Annual review peer feedback |
| Project management gaps | 1wk | Forte 2025 — needs lightweight tracking |






### Loop 5: System Health
All organs | Every run | Word counts, staleness, reliability.

#### Body Metrics


#### | Metric |


| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Total body words | ~19,200w | Adaptive (learned) | ✅ Tracking |
| Budgets | Adaptive (Bayesian) | — | 15 experiments, priors updating |
| Staleness risk | Eyes (Feb data, 30+ days) | <20% stale | ⚠️ Needs Mar WBR |


#### **Reading the metrics:**




#### **Worked example:** Body


**Worked example:** Body at 19,200w with 62% keep rate. Eyes last updated 30+ days ago (stale). Action: prioritize Eyes for ADD experiment (fresh data), then COMPRESS on amcc (largest organ at ~4,400w) if accuracy holds.

#### Experiment Metrics
| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Loop runs | 18 | — | — |
| Experiments | 50 (31 keep, 19 revert) | — | 62% keep rate. Run 28: 4 experiments (4 keep, 0 revert), first batch on fresh DuckDB priors. |
| Experiment targets | 112 (63 organ + 49 style/context) | — | 45 organ combos tested (71%). Style guide combos seeded, untested. |

#### Experiment Metrics — Details


### Loop 4: Delegation Verification
| Delegation | Delegate | Status | Last Checked | Issue | Next Step |
|-----------|----------|--------|-------------|-------|-----------|
| MX Invoicing | Carlos → Lorena | SLIPPING | 3/25 | Handoff incomplete — Carlos departed, Lorena unconfirmed | Confirm with Lorena or escalate to Pedro |
| OP1 Contributors | Various | ON_TRACK | 3/25 | None | — |
### Loop 9: Meeting Communication
Hedy data | Weekly | Speaking share, hedging, filler words, turn length.






#### Baselines & Thresholds
Hedy integrated (Run 8). 9+ sessions processed. Measurement: speaking share (% of total talk time), hedging frequency, filler words, turn length.

| Setting | Speaking Share | Hedging | Status |
|---------|--------------|---------|--------|
| 1:1s | ~40% (healthy) | 0 (strong) | ✅ At baseline |
| Groups | <15% (gap) | Not yet measured | ⚠️ Target ≥20% |







#### Latest Sessions (4/2)
- Market Expansion Playbook Review (53 min): Richard PRESENTED — visibility breakthrough. Led session, team engaged, action items assigned TO him. Strong L2.
- WhatsApp/Push Demo (52 min): Observational. No visibility concern — product demo. Follow-up: coordinate WhatsApp rollout for MX/AU with Lorena/Alexis.

---






### L1 Gate Status
STRUGGLING. Gate metric: consecutive weeks with shipped artifacts. Current streak: 0. Kate Apr 16 meeting CANCELED — Brandon (4/3): "cancel for now and reassess as we clean it up." Kate: "fine keeping it but wanted a plan." Megan declined. Brandon reviewing testing framework doc himself before deciding how to use it. Artifact exists but external deadline pressure removed.






## Common Failures | Failure | Trigger / Threshold | Action | |---------|---------------------|--------| | STUCK = trigger, not label | 3+ weeks at same status | Structural fix: willpower → trainer, systems → device. (e.g., "Admin displacement 3wk" → pre-written templates via device.md.) | | Stale predictions | Unscored >7 days | Score within 7 days or archive. Don't let unscored predictions sit. | | Conflating 1:1 vs group comms | Comparing across settings | Track separately. 1:1s ~40% share (healthy). Groups <15% (gap). | | Cross-organ reference drift | Loop 7 flags mismatch | When a fact cited in one organ doesn't match its canonical source, fix at the source. Don't patch the reference — update the origin. | 

## Purpose

The body's quality-control layer. Measures outcomes against predictions, scores decisions against results, and routes corrections to the right organ. Nine loops, each with its own cadence: daily prediction scoring, weekly pattern tracking, monthly decision audits.

**Worked example:** Brain predicted AU CPA would drop 15% after OCI launch. Nervous system scores the prediction after 4 weeks: actual drop was 8%. Mismatch logged. Correction routed: Brain updates confidence calibration, Eyes updates the AU metric baseline. The prediction was directionally correct but overestimated magnitude — this pattern (optimism bias on new launches) feeds back into future predictions.







### Active Loops

#### Loop 1: Decision Audit ##### Protocol Brain | Monthly | Score decisions against outcomes: VALIDATED (prediction confirmed), PARTIALLY (mixed), INVALIDATED (prediction wrong), PENDING (data insufficient). On INVALIDATED → review and update the driving principle. Worked example: D3 predicted OCI would lift regs 10-20% in CA. If CA shows +15% after 30d → VALIDATED. If lift <5% → PARTIALLY. If CPA worsens → INVALIDATED, review "phase all rollouts" principle. ##### Pending Decisions 5 decisions awaiting audit: D1, D2, D3, D4, D7. ##### Audit Triggers | Decision | Data Needed | Target Date | |----------|-------------|-------------| | D1, D2 | CA/JP/EU3 performance data | Jul 2026 | | D3 | Monthly CPA + OCI conversion data | May 2026 | | D4 | UK +31% regs confirmation (IT when volume sufficient) | Ongoing | | D7 | Polaris +30d deep dive results | Ongoing | ##### Scoring Example D3 (OCI ROW rollout): CA OCI +10-20% reg lift after 30d → VALIDATED. Lift <5% or CPA worsens → PARTIALLY. Tracking failures or negative ROI → INVALIDATED. Target scoring date: May 2026 when CA data available. ### Loop 2: Prediction Scoring
Eyes + agent text outputs | Daily + weekly | Score predicted QA and agent confidence: HIT/MISS/SURPRISE. Target ≥60%. **Reactivated 2026-04-22** after round-2 external-AI-review blind test confirmed the "Agent Confidence Calibration" proposal duplicated this loop — the gap was activation, not a missing metric.
  - *Example:* When reactivation trigger:** am-2 hook writes ≥3 predic, the expected outcome is verified by checking the result.
- **Scoring protocol:** After each meeting/event, compare predicted questions to actual questions asked. HIT = question asked as predicted. MISS = predicted but not asked. SURPRISE = asked but not predicted. Weekly aggregate: hits/(hits+misses) ≥ 60% target.
- **Scope extension (2026-04-22):** Agent text-output confidence — when the agent produces a high-stakes output with an explicit confidence % (per high-stakes-guardrails.md), score the outcome when it resolves. Same HIT/MISS/SURPRISE labels. HIT = outcome within the stated confidence band. MISS = outcome outside and below predicted magnitude. SURPRISE = outcome outside and above. Weekly reliability check: of outputs stated at X% confidence, were X% correct? Log to `ps.callout_calibration` for callouts, `ps.forecasts.scored` for forecasts, and (when volume justifies) a new `ps.high_stakes_scored` table ALTER on ps.forecasts with `human_review_flagged BOOLEAN` + `output_ref VARCHAR` — not a new table per Grok round-2 verdict.
- **Routing on mismatch:** Brain updates confidence calibration, Eyes updates the metric baseline, rw-trainer surfaces patterns in Friday retro.


## Calibration Loops

| # | Organ | Cadence | Status |
|---|-------|---------|--------|
| 1 | Brain | Monthly | 5 PENDING |
| 2 | Eyes | Daily+Wkly | ACTIVE (reactivated 2026-04-22) |
| 3 | rw-tracker | Wkly (Fri) | 3 active, 2 new |
| 4 | Device | Weekly | 1 SLIPPING |
| 5 | All | Every run | ✅ |
| 6 | Brain+soul | Quarterly | Deferred Jun '26 |
| 7 | Cross-organ | Monthly | Deferred 4/20 |
| 8 | Per-source | Ongoing | Active |
| 9 | Hedy | Weekly | Active (9+ sessions) |






### Deferred Loops

**Key consideration:** This section's content is critical for accurate operation. Cross-reference with related sections for full context.
#### Loop 6: Principle Evolution
Do decision principles still match actual behavior? Score each principle against last quarter's decisions.






#### Loop 7: Coherence Audit
Cross-organ refs | Monthly | Next: 4/20
Verify cross-organ pointers remain valid: does a fact cited in one organ still match its canonical source? Flag mismatches for correction. Priority targets: Eyes metrics referenced in Brain decisions, Memory relationship data cited in Hands dependencies.






#### Loop 8: Source Quality Filter
Per-source | Ongoing
T1 (builders+proof) → experiments. T2 (practitioners) → reject unless context matches. T3 (commentary) → discovery only.

*Example:* When this applies, the expected outcome is verified by checking the result.