# T4 Blind Verdict — Daily Brief + Highest-Leverage Move

Evaluator is blind to which arm produced which output. Scoring based on content only.

## What the right call looks like (independent read before scoring)

Richard's state on 2026-04-22 (Wed AM):

- **L1 streak: 23–24 workdays at zero** (every arm flags this) — the hard thing has been Testing Document v5 for Kate since at least early April.
- **Testing Doc v5 has PUBLISH verdict (8.4/10) since 4/5.** Critic fixes queued. It is a **10-minute send**, not a work session. Send-ready for weeks.
- **Brandon 1:1 at 1:30 PT** — the 4/21 session collapsed to 4 min because of a laptop issue. The "send during the 1:1" pattern has now failed twice in a row.
- **MX pacing 🔴 128.8% regs / 🔴 150.1% spend** — Brandon expects a decay-narrative forecast by 10:00 PT.
- **`main.hard_thing_now` rank 1 = polaris-brand-lp** (score 4.05, valuable-and-avoided, 4 channels, no Richard artifact on file). This *may* have flipped overnight because the incumbent ledger either correctly or incorrectly treated Testing Doc v5 as "shipped" on 4/5. The arms disagree about whether v5 was ever sent to Brandon.
- **5/5 AU handoff** at T-13d. Brandon explicitly asked 4/21 to "scope Kiro weekly AU change aggregator."

**Correct highest-leverage move (given Richard's state):**

The 24-day streak is the top-priority behavioral signal. The only move that (a) breaks it today, (b) uses the 1:30 PT forcing function, (c) fits in 10 minutes, and (d) is already PUBLISH-ready is **Send Testing Doc v5 to Brandon before 1:30 PT** — preferably earlier (scheduled send or pre-loaded draft) so the 1:1 opens on "v5 is in your inbox" rather than "still coming."

Polaris is a legitimate hard-thing signal and a legitimate L2 artifact, but a Polaris one-pager is 60–90 minutes of net-new work and has no v0. Recommending Polaris as today's leverage move means skipping the 10-minute send that breaks the streak and adding a fresh high-friction task on a day that already has a forcing function for the low-friction one. Polaris is tomorrow's move.

The AU change aggregator is a real L3 opportunity but it's Brandon's 1-day-old ask and does not resolve the 24-day streak today. It's a legitimate secondary move but not the highest-leverage move.

**Decision-quality ordering:**
1. Testing Doc v5 → Brandon before 1:30 PT (breaks streak, low friction, ready)
2. MX decay forecast before 10am (time-boxed acute)
3. Polaris one-pager OR AU aggregator scope (L2/L3 after acute is cleared)
4. Yun-Kang WBR reply (blocks publish)

Arms that led with **Testing Doc v5 send** got the call right. Arms that demoted it to secondary or picked Polaris / AU aggregator as the leverage move got it partially wrong — they over-indexed on signal rotation at the expense of breaking the streak with the cheapest possible move.

## Per-arm scores

| Arm | Clarity | Decision | Format/Principles | Usefulness | Always-on | Total (/50) |
|-----|---------|----------|-------------------|------------|-----------|-------------|
| A   | 8       | 6        | 9                 | 7          | 7         | 37          |
| B   | 9       | 10       | 9                 | 10         | 8         | 46          |
| C   | 8       | 7        | 9                 | 8          | 7         | 39          |
| D   | 7       | 6        | 8                 | 7          | 6         | 34          |
| E   | 9       | 8        | 10                | 9          | 9         | 45          |
| F   | 8       | 6        | 9                 | 7          | 7         | 37          |

## Rank

1. **ARM-B (46)** — Strongest overall and the only arm that leads with the obvious right move. Opens Priority #1 as "Testing Doc v5 → Brandon before 1:30, THE HARD THING, 10-min send not a work session." Recognizes v5 is PUBLISH verdict since 4/5 and the only remaining action is transmission. Friction fix is structural and on-point: decouple send from the 1:1, pre-load Outlook by 11:00, schedule unconditional 12:00 send — directly addresses the "last-moment barrier" pattern that killed the 4/21 1:1 send. Correctly flags MX forecast as >$50K → high-stakes guardrails. Correctly flags the polaris-vs-testing-doc ledger conflict and asks Richard to choose rather than picking for him. Applies the Next Best Action Filter visibly at the end and shows all four gates. Five sections present. Tier convention used. Uniquely calls the AU running cold at ~half expected — a legitimate hedge. The "schedule send for 12:00 PT unconditionally" is the single best structural fix in the set.

2. **ARM-E (45)** — Most disciplined structure in the set. The 2×2 Friction-Impact sort puts Testing Doc v5 in High-Impact / Low-Friction → DO IMMEDIATELY, Polaris in High-Impact / High-Friction → decompose, AU aggregator in High-Impact / Medium-Friction → today PM. The matrix makes the gating logic fully visible and robust. BUT — and this is why it lands second, not first — the actual "Leverage Move" section picks the AU aggregator, not the Testing Doc send, even though the 2×2 surfaces the Testing Doc as the highest-leverage-per-minute item. The "09:30 PT structural slot for Testing Doc send" friction fix is excellent and structurally superior to B's 12:00 scheduled send (an earlier, recurring slot is harder to slide than a noon one). Cleaner tier convention with explicit bands. Best format adherence in the set (10/10 on format — every element present and correctly used). If the leverage move had matched the matrix output, this would tie B.

3. **ARM-C (39)** — Strong ledger-conflict handling and the cleanest "rank=1 with no Richard artifact = Priority #1" rule application per the stated format. Treats Polaris as Priority #1 and Testing Doc as Priority #2 — internally consistent. Friction fix (wire `main.hard_thing_now.rank=1` directly into the brief template, routed to karpathy as the gatekeeper) is thoughtful structural work and correctly routes to karpathy. BUT the top-3 queue crowds into the morning: 10am MX forecast + before-1:30 Testing Doc send + 60-90min Polaris core block + Yun reply, all before 1:30. That's optimistic at best. The leverage move is Polaris, not the streak-breaking Testing Doc send. Good principle checks. Tier convention used cleanly. Notes the 🔴 AU technicality but defers to existing narrative — fair.

4. **ARM-A (37)** — Strongest ledger-conflict framing of any arm — opens with a clear explanation that the retrospective correction happened 4/22 AM and why the brief diverges from daily-brief-latest.md. Reads like a briefing from someone who actually understands the system state. BUT the leverage move is "scope the AU weekly change aggregator" — a legitimate L3 play, but it skips the 10-minute Testing Doc send entirely. Relegates Testing Doc to "Core #2... recovery-of-visibility send, not the hard thing." That's the wrong call given a 24-day streak. The principle checks are visible and well-reasoned but applied to the wrong move. Friction fix (pre-draft Brandon sends into `brandon-drafts/` folder) is structural and has a real subtraction-check (removes Section 10 of daily brief). Best example of "right process, wrong decision."

5. **ARM-F (37)** — Confidently states "Testing Approach v5 shipped 4/5, incumbent ledger was inheriting incorrectly" — makes the strongest factual claim of any arm about v5's status. If that claim is correct, the Polaris pivot is the right leverage move. But the v5-already-shipped framing contradicts the "24 workdays at zero" signal from every other arm including the baseline. Leverage Cascade reasoning (v1 one-pager, not the perfect one) is genuinely useful — "the smallest viable artifact beats the comprehensive one that doesn't exist" is a Richard-aligned move. Friction fix (block brief generation if hard_thing_now refresh >12h stale) is a real infrastructure-level structural fix. Tier convention with explicit bands justified. Five sections present. But the Testing Doc item ("close the loop, ask Brandon if it landed") treats a 24-day avoidance pattern as a status question — that's a miss. If v5 were truly sent, the streak would have reset to 0 for the right reason. Calling the leverage move "ship the Polaris one-pager" while the streak state is ambiguous is the same error as Arm C, with more confidence.

6. **ARM-D (34)** — Uses the Context-Action Trigger Q1/Q2 protocol visibly and correctly — the opening pre-execution paragraph is useful scaffolding. But D makes the strongest and most falsifiable factual claim of any arm: "Streak reset to 1 yesterday (v5 Testing Doc shipped after 23 workdays at zero — good)." No other arm says v5 was sent 4/21; most say it's still unsent. If D is right, the Polaris pivot is the right call and the brief is excellent. If D is wrong, the brief buries the actual 24-day hard thing under a newly-pivoted Polaris framing and misses the single highest-leverage action available. Given five of six arms read the state as "still unsent," D is most likely working from a hallucinated state transition. Friction fix (persist `MOTHERDUCK_TOKEN` in `.bashrc`) is useful but low-leverage compared to the actual behavioral structural fix needed. Five sections present. Decent but the factual claim risk drops it to the bottom.

## Key observations

### Which arm got the highest-leverage-move call right

**Arm B.** The only arm that led with "send the 10-minute ready artifact that breaks the 24-day streak." Arm E had the right matrix analysis but picked a different move. Arms A, C, D, F all picked Polaris or AU aggregator — higher-friction moves that either add work or depend on a state transition (v5 already shipped) that may not be real.

The tell: on any day where a 24-day L1 streak is active AND a send-ready artifact exists AND a forcing-function meeting is scheduled, the leverage move is the send. Not the next scoping doc. Not the next rollout tracker. The send. Arm B understood that. The others rotated to shinier signals.

### Which arm handled the hard-thing ledger conflict best

**Arm A.** Opens with the cleanest explanation: "retrospectively corrected this morning... the incumbent ledger had been inheriting Testing Approach v5 forward incorrectly 4/14–4/21. Current rank 1 is polaris-brand-lp." That framing is what a Richard reading cold at 6am actually needs to see first — the brief doesn't match yesterday's state, here's why. Arm C and Arm F also handled it well but assumed their interpretation was correct; Arm A showed its work. This is the signature Arm-A quality: best process, wrong output.

### Which arm is most actionable in the next 30 minutes

**Arm B.** "Pre-load Outlook by 11:00, schedule send for 12:00 PT unconditionally, then work MX forecast" is a sequenced instruction Richard can execute without further decision-making. Arm E's "09:30 PT structural slot" is arguably better as a habit fix but more disruptive in a brief-the-day context.

### Format adherence (5 sections, tier convention, hard-thing handling)

All six arms produced the five sections. Tier convention usage ranged from explicit with legend (E, F) to implicit with emoji only (A, B, C, D). The hard-thing handling split:

- **Treat Testing Doc v5 as the hard thing:** B (correct call given streak state), E (via the matrix, though leverage move disagreed).
- **Treat Polaris as the hard thing per ledger rotation:** A, C, F.
- **Treat Polaris as the hard thing because v5 already shipped:** D.

Per the stated "am-triage Daily Brief Output Format + principles," if `hard_thing_now.rank=1` has no Richard artifact AND the L1 streak is at 23+ workdays, the operative hard thing is the avoidance pattern, not the freshly-rotated signal. B and E got that right. A, C, D, F got that wrong — though F and D made the argument that the avoidance pattern had already been broken (which, if true, would flip the right answer to Polaris).

### Always-on cost tradeoff

**Arm B's Next Best Action Filter (4 gates):** Low cost per invocation. Runs in under a paragraph. Surfaces the leverage-vs-friction comparison cleanly. Could safely run on every task without drowning simple requests. Recommend **always-on**.

**Arm E's Friction-Impact 2×2:** Very low cost — the matrix is a 6-row table. Makes the gating logic visible and catches the "high-friction task masquerading as today's move" trap that hit A, C, and D. Strongest always-on candidate in the set. Recommend **always-on**, particularly for daily brief surface and weekly retros.

**Arm A's Leverage-Cascade style principle checks:** Heavier, more prose-y. Useful for strategic artifacts (Testing Doc review, OP1) but would add ceremony to routine requests. Recommend **manual-only** — surface via rw-trainer coaching rather than every task.

**Arm C's `rank=1-no-artifact = Priority #1` rule:** Cheap to encode and enforces correct ledger-driven priority. BUT it's too rigid — misses the case where the incumbent is the real hard thing (avoidance pattern). Recommend **always-on with a secondary check**: if rank 1 flips AND the L1 streak is >15 workdays, the brief should surface BOTH candidates and let Richard choose, not auto-select the new rank 1.

**Arm D's Context-Action Trigger Q1/Q2:** Medium cost. The explicit Q1/Q2 scaffolding is useful once per session, not per task. Recommend **session-start only**, not per-task.

**Arm F's Leverage Cascade:** Heaviest of the set. 4-step filter explicitly invoked in prose. Adds real scaffolding when pivoting away from stale priorities but would bloat routine replies. Recommend **manual-only**.

### Single best next-best-action line in the set

> *"Pre-load v5 email draft into Outlook by 11:00 PT with subject + 2-sentence body + v5 attached. Schedule it to send at 12:00 PT unconditionally. The 1:30 PT 1:1 then becomes discussion of a received artifact, not the delivery mechanism for it."* — Arm B

Names the artifact, the location, the time, the trigger, the default behavior, and names the structural pattern being fixed (send-is-not-coupled-to-meeting). No other arm packages all five into one sequence.

### Second observation worth flagging

The six arms are essentially running two different implicit priors about state:

- **Prior A (B, C, E + baseline):** Testing Doc v5 is still unsent. Streak is 23–24 days. The hard thing is the send.
- **Prior B (D, F, and A partially):** Testing Doc v5 already shipped. The incumbent ledger was wrong. The streak broke yesterday. The hard thing rotated to Polaris.

This is a genuine data-layer ambiguity, not a reasoning failure. Whatever arm produces the morning brief should be forced to surface this ambiguity explicitly when it exists rather than pick a prior silently. Arm A did this best (ledger conflict at top of document). Arm B handled it by letting Richard resolve in Open Question #2 ("Testing Doc, Polaris, or both"). Arm D silently chose Prior B. If Prior B is wrong — which the streak signal suggests — Arm D's brief misdirects the day.

The meta-lesson: the daily brief should never silently resolve a hard-thing ledger conflict. Flag it, show both paths, ask.
