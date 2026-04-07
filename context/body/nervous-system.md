<!-- DOC-0227 | duck_id: organ-nervous-system -->
# Nervous System — Feedback, Calibration & Learning

*Operating principle: Invisible over visible. Surface insights that lead to structural changes — not reports that require Richard to act on them. When a pattern is STUCK for 3 weeks, propose a structural fix.*

Last updated: 2026-04-05 (Karpathy Run 28 — Loop 3 split into Active/New/Root Cause subsections)
Created: 2026-03-20

---

## Purpose

Evaluates the work every other organ does. Looks backward, measures what happened, feeds corrections forward. Nine calibration loops, each with its own cadence and data.

---

## Calibration Loops

| Loop | Organ | Cadence | Status |
|------|-------|---------|--------|
| 1 Decision Audit | Brain | Monthly | 5 PENDING |
| 2 Prediction Scoring | Eyes | Daily+Weekly | Inactive (stale QA cleared) |
| 3 Pattern Trajectory | rw-tracker | Weekly (Fri) | 3 active, 2 new |
| 4 Delegation Verification | Device | Weekly | 1 SLIPPING, 1 ON_TRACK |
| 5 System Health | All | Every run | ✅ Tracking |
| 6 Principle Evolution | Brain+soul | Quarterly | Deferred → Jun 2026 |
| 7 Coherence Audit | Cross-organ | Monthly | Deferred → 4/20 |
| 8 Source Quality Filter | Per-source | Ongoing | Active |
| 9 Meeting Communication | Hedy | Weekly | Active (9+ sessions) |

### Active Loops

#### Loop 1: Decision Audit
Brain | Monthly | Score decisions VALIDATED/PARTIALLY/INVALIDATED/PENDING. INVALIDATED → flag principle.

5 decisions PENDING audit (D1, D2, D3, D4, D7). Triggers: CA/JP/EU3 data Jul 2026, monthly CPA, UK +31% regs (IT when volume), Polaris +30d, deep dive data.

### Loop 2: Prediction Scoring
Eyes | Daily + weekly | Score predicted QA: HIT/MISS/SURPRISE. Target ≥60%. Currently inactive — predicted QA cleared from Eyes (stale content experiment, Run 18). Reactivate when AM-2 generates fresh predictions.

### Loop 3: Pattern Trajectory
rw-tracker.md | Weekly (Friday) | IMPROVING/STUCK/WORSENING/RESOLVED. STUCK 3+ wk → structural fix. Willpower → trainer. Systems → device.

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

#### Root Cause
Visibility avoidance gates L1 → blocks all downstream levels.

### Loop 4: Delegation Verification
Device | Weekly | Score: ON_TRACK / SLIPPING / FAILED.

| Delegation | Delegate | Status | Last Checked | Action |
|-----------|----------|--------|-------------|--------|
| MX Invoicing | Carlos → Lorena | SLIPPING | 3/25 | Handoff incomplete — Carlos departed, Lorena not confirmed |
| OP1 Contributors | Various | ON_TRACK | 3/25 | No action needed |

### Loop 5: System Health
All organs | Every run | Word counts, staleness, reliability.

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Total body words | ~19,200w | Adaptive (learned) | ✅ Tracking |
| Budgets | Adaptive (Bayesian) | — | 15 experiments, priors updating |
| Loop runs | 18 | — | — |
| Experiments | 50 (31 keep, 19 revert) | — | 62% keep rate. Run 28: 4 experiments (4 keep, 0 revert), first batch on fresh DuckDB priors. |
| Experiment targets | 112 (63 organ + 49 style/context) | — | 45 organ combos tested (71%). Style guide combos seeded, untested. |
| Staleness risk | Eyes (Feb data, 30+ days) | <20% stale | ⚠️ Needs Mar WBR |

### Deferred Loops

#### Loop 6: Principle Evolution
Brain + soul.md | Quarterly | Next: Jun 2026
Do decision principles still match actual behavior? Score each principle against last quarter's decisions.

#### Loop 7: Coherence Audit
Cross-organ refs | Monthly | Next: 4/20
Are cross-organ pointers still valid? Check that facts referenced in one organ match the canonical source.

#### Loop 8: Source Quality Filter
Per-source | Ongoing
T1 (builders+proof) → experiments. T2 (practitioners) → reject unless context matches. T3 (commentary) → discovery only.

### Loop 9: Meeting Communication
Hedy data | Weekly | Speaking share, hedging, filler words, turn length.

#### Baselines & Thresholds
Hedy integrated (Run 8). 9+ sessions processed.
- 1:1s: ~40% share (healthy baseline), hedging 0 (strong)
- Groups: target ≥20% share, currently <15% (gap). Hedging not yet measured.
- Confirmed pattern: Strong in 1:1s but <15% in groups (Deep Dive, Weekly Sync). Structural — Richard goes quiet when Andrew or others dominate airtime.

#### Latest Sessions (4/2)
- Market Expansion Playbook Review (53 min): Richard PRESENTED — visibility breakthrough. Led session, team engaged, action items assigned TO him. Strong L2.
- WhatsApp/Push Demo (52 min): Observational. No visibility concern — product demo. Follow-up: coordinate WhatsApp rollout for MX/AU with Lorena/Alexis.

---

## Five Levels Position

### L1 Gate Status
STRUGGLING. Gate: consecutive weeks with shipped artifacts. Currently at 0. W14 day 5 (Friday). Kate Apr 16 meeting OFFICIALLY CANCELED (4/3 email thread: Brandon "cancel for now and reassess as we clean it up," Kate "I'm fine keeping it but wanted to make sure we had a plan," Megan declining from calendar). Brandon reviewing the testing framework doc himself first — will determine how to use it. The document is still the artifact, but the deadline pressure is gone.

### L1 Gate-Breaker Candidates (from 4/2 Deep Dive)
Multiple artifact opportunities emerged from 4/2 Deep Dive. The playbook presentation was Richard's strongest group visibility moment in 9+ sessions tracked.
- Year-One Optimization one-pager — due Apr 16. Smaller scope than Testing Approach. Could be the first shipped artifact.
- IECCP FAQ — due Apr 9. Even smaller. One-page reference doc.
- Negative keyword list — immediate. Tactical but shippable today.
- Market Expansion Playbook — already presented 4/2. Could be formalized into a written artifact.

### Parallel Level Activity
New action items from 4/2 Deep Dive: market expansion playbook (strong L2 visibility), Year-One Optimization one-pager (by Apr 16), IECCP FAQ (by Apr 9), negative keyword list (immediate).

---

## Common Failures in Using This Organ

1. **Treating STUCK as a label, not a trigger.** STUCK 3+ weeks means a structural fix is needed — not more observation. Escalate: willpower patterns → trainer, system patterns → device. Example: "Admin displacement STUCK 3wk" → structural fix = pre-written response templates (device.md), not "keep monitoring."
2. **Scoring predictions after the fact without logging.** If a prediction isn't scored within 7 days, it's stale. Archive it or score it — don't let it sit.
3. **Ignoring the group meeting gap.** Richard's 1:1 communication is strong (~40% share). The gap is in groups (<15%). Don't conflate the two — track them separately.

## Governance

All changes to this file are governed by the Karpathy agent. The heart loop cascades data into the tracking tables. Karpathy owns the loop definitions, metrics, and compression of this organ.
