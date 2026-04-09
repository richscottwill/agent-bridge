<!-- DOC-0219 | duck_id: organ-brain -->
# Brain — Decisions & Thinking

*How Richard decides. Past decisions, extracted principles, strategic priorities, and the leverage framework. This is the canonical decision-making reference — no separate decision log needed.*

*Operating principle: Subtraction before addition. When a new decision principle is proposed, check if it's already covered by an existing one. When prioritizing, eliminate before optimizing. The leverage framework exists to say no to good work so Richard can say yes to essential work.*

Last updated: 2026-04-04 (Karpathy Run 25 — Five Levels compressed to 2 lines each, Leverage Assessment compressed to rule:example format)

---

## Decision Principles (ranked by frequency of application)

1. **Evidence over intuition** — Never scale without validated test results. Every initiative goes through structured testing before becoming baseline.
2. **Efficiency over escalation** — When competitors increase pressure, respond with smarter execution (OCI, ad copy, LP optimization) rather than budget escalation or bid wars.
3. **Holistic measurement over segmented goals** — Evaluate performance at the total program level, not Brand vs Non-Brand in isolation.
4. **Phased rollout over full migration** — Prefer 50/50 splits, phased testing, and controlled rollouts over big-bang changes.
5. **Cross-functional partnership over solo execution** — Position PS team as connective tissue between platform capabilities and business objectives, not just a channel executor.
6. **Compression over complexity** — Consolidate campaigns, simplify structures, reduce operational overhead to let algorithms work better.
7. **Customer research over assumptions** — Ground messaging and strategy in actual customer data (e.g., Sole Proprietor study drove ad copy overhaul).

## Prediction Template

When Richard faces a new decision, check:
1. Does it map to an existing principle? Predict he will favor that direction
2. Is there data available? He will want to see it before deciding
3. Can it be phased? He will prefer phased over big-bang
4. Does it involve cross-team work? He will lean into partnership, not solo execution
5. Is someone pushing for speed over evidence? He will push back with a test proposal

**Worked example — AU OCI launch decision:** Lena pushed for immediate full rollout. Template check: #4 (phased > big-bang), #1 (evidence first — CA showed +18.5% vs OP2), #5 (cross-team — MCS page builds needed). Speed pressure from Lena. Result: proposed phased approach with measurement framework. Three principles aligned → high confidence prediction.

---

## Decision Log

Decisions have a relevance half-life. Not every decision stays useful forever.

**Relevance tiers:**
- **FOUNDATIONAL** — Shaped a principle or changed how the team operates. Stays indefinitely. (D1, D2, D3, D5, D6, D8)
- **ACTIVE** — Still influencing current work or pending audit. Stays until outcome is resolved. (D4, D9, D10)
- **RESOLVED** — Outcome confirmed, lesson extracted. Compress to one-liner, archive full entry after 90 days. (D7 is the first candidate)

### Decay Protocol

Karpathy governs, loop executes:
1. When a decision's outcome is VALIDATED or INVALIDATED (via nervous system Loop 1), tag it RESOLVED
2. Extract the lesson into the relevant principle (strengthen, qualify, or retire)
3. Compress the full entry to: `D[X]: [Name] — [Outcome]. Reinforced Principle #[N].`
4. After 90 days in RESOLVED state with no references, archive to `~/shared/wiki/archive/`

### Active Decisions (influencing current work)

| ID | Decision | Detail | Principles |
|----|----------|--------|-----------|
| D4 | AU LP Full Migration | Lena overrode phased rollout — full Polaris switch. Executing. | — |
| D9 | AI Max Testing | US-first with measurement guardrails. Same OCI discipline. | #4, #1 |
| D10 | F90 Lifecycle | Legal SIMs for 3+ purchases targeting. Extends PS beyond registration. | #5 |

### Foundational Decisions (shaped principles — stays indefinitely)

| ID | Decision | Detail | Principles |
|----|----------|--------|-----------|
| D1 | OCI Implementation | Phased rollout with measurement framework. | #1, #4 |
| D2 | Competitive Response to Walmart | Bid caps + NB efficiency via OCI, do NOT escalate auction. | #2, #3 |
| D3 | Ad Copy Overhaul (SP Study) | Shift to price/quality/selection messaging from bulk/B2B. | #7, #1 |
| D5 | Campaign Consolidation | Consolidate campaigns to strengthen OCI data signals. | #6, #1 |
| D6 | Engagement Channel | Lifecycle channel via ABMA partnership, 13%→30% match rate. | #5, #1 |
| D8 | OP1 Structure | Problem→test→result→scale across 5 workstreams. | #5, #1 |

<!-- Full decision details: db("SELECT id, name, tier, description, alternatives, rationale, principles, confidence FROM decisions ORDER BY id") -->

---

## Strategic Priorities — The Five Levels

Sequential. Each funds the next. Don't skip ahead.

### Level 1: Sharpen Yourself
Build consistent strategic output habits. Systems in place: Trainer, autoresearch loop, context cascade.
Key metric: consecutive weeks with a strategic artifact shipped.

### Level 2: Drive & Communicate Worldwide Testing
Scalable tests across all PS accounts globally. Drive end-to-end: hypothesis → design → execution → communication → results.
Key metric: every active WW test has a written status the team can reference without asking Richard.

### Level 3: Give Your Team Leverage Through Automation
Build tools a non-tech team can actually adopt. Richard is the bridge — most willing to go outside the non-tech comfort zone.
Key metric: at least one tool adopted by a teammate.

### Level 4: Own the Zero-Click Future
AEO POV as foundational artifact. Sequence after Levels 1-3 so credibility and bandwidth exist.
Key metric: published POV or framework that shapes team strategy.

### Level 5: Full Agentic Orchestration of PS Work
End state: agent swarm runs PS operations autonomously. Gap: "agent assists" → "agent operates" is an architecture shift.
Key metric: a PS workflow that runs end-to-end without human intervention.

### Level Graduation Criteria

Graduation is not a date — it's evidence. The nervous system (Loop 6) tracks these.

| From → To | Gate | Evidence Required |
|-----------|------|-------------------|
| 1 → 2 | Consistent output | 4 consecutive weeks with a strategic artifact shipped (aMCC streak proxy) |
| 2 → 3 | Test ownership | 3+ WW tests with written status docs that the team references without asking Richard |
| 3 → 4 | Team adoption | 1+ tool built by Richard and actively used by a teammate for 30+ days |
| 4 → 5 | Strategic authority | Published POV or framework that influenced a team-level decision (Kate or Brandon cited it) |

### Current Level Status

**Position:** Level 1 (struggling — 0 consecutive weeks, 14 workdays at zero). Level 2 work happening in parallel (OCI 7/10 markets at 100%, AU weekly updates, ad copy tests, W13 callouts, Flash sections). Level 3 accelerating (prediction engine, data layer, callout pipeline, attention tracker, Slack ingestion). Level 5 also active (agent bridge, DuckDB agent state, Asana integration). Level 1 gate not passed — Testing Approach doc for Kate is the convergence point (L2 artifact that proves L1 consistency).

**Rule:** You can DO work at multiple levels simultaneously, but you don't GRADUATE until the gate is met. The aMCC tracks Level 1 progress via the streak. The nervous system tracks all levels via Loop 6.

---

## OP1 Strategic Narrative

Core argument: Every 2026 investment maps to a validated 2025 signal. PS transforming from keyword-driven to automated, audience-centric engine. Cross-functional collaboration is the differentiator. 5 workstreams (OCI Bidding, Modern Search, Audiences, User Experience, Algorithmic Ads), each problem→test→result→scale. Full draft: `~/shared/wiki/research/op1-ps-testing-framework-draft.md`.

---

## Leverage Assessment Framework

When multiple tasks compete for a spot, apply these tiebreakers:
- **Strategic artifacts > tactical execution:** a test design doc beats a sitelink update.
- **Compounding work > one-and-done work:** a playbook beats a single campaign build.
- **Visibility work > invisible work:** a Kingpin update beats internal cleanup.
- **Automation opportunities > manual repetition:** if a task keeps recurring, flag it as a tool candidate.
- **30-day test:** "Will this matter in 30 days?" If no, don't let it take a Core slot over something that compounds.

**Worked example:** Richard has 3 tasks competing for a Core slot: (1) update MX sitelinks, (2) draft Testing Approach doc for Kate, (3) fix a broken Asana automation. Apply tiebreakers: #2 is a strategic artifact (beats #1 tactical), compounds (reusable framework), and is visibility work (Kate sees it). #3 is automation but one-and-done fix. #1 fails the 30-day test. Winner: #2.
