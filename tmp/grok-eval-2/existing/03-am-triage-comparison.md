# Head-to-Head: Grok `03-am-triage-enhanced.md` vs existing `am-triage.md`

**Date:** 2026-04-22
**Files compared:**
- Proposal: `shared/tmp/grok-eval-2/proposed/03-am-triage-enhanced.md` (6 steps, ~15 lines)
- Existing: `shared/context/protocols/am-triage.md` (~300 lines, updated this morning with the blind-A/B-validated Daily Brief Output Format)

**Verdict: REJECT.** Grok's proposal adds nothing the existing protocol doesn't already cover, and its "simplicity" would silently delete the signal routing, admin detection, BAU decomposition, cap enforcement, enrichment, and portfolio scan machinery that the existing protocol encodes. The output-format section Grok invents is a weaker restatement of the section that was added this morning.

---

## 1. Step-by-step mapping

| Grok step | What it says | Coverage in existing am-triage.md |
|-----------|--------------|-----------------------------------|
| **1. Run `tools/excel_ingest.py` (if new files exist)** | Spreadsheet ingest | **Not in am-triage.md by design.** Excel/dashboard ingest is an am-backend concern, not the interactive curate+draft phase. Grok is putting a data-pipeline step into an interactive triage protocol. Wrong architectural layer. |
| **2. Run anomaly detection** | Generic anomaly detection | **Partially covered, more specifically.** Existing protocol runs: Slack decision detection, overdue 7d+ flags, near-due escalation (0–2d), admin 3d+ overdue escalation, stale project detection (14d+), cross-team blocker detection (MX), event-countdown triggers (Paid App), budget 3d threshold (MX + Paid App), status-update staleness, bucket cap overflow, BAU-vs-non-BAU classification on demotion. Grok's single bullet "run anomaly detection" is a massive subtraction dressed as simplification. |
| **3. Load latest `current.md`, `rw-tracker.md`, `eyes.md`** | Context load | **Covered and more complete.** Existing Context Load: `spine.md, current.md, memory.md, richard-writing-style.md, hands.md, amcc.md, rw-tracker.md, asana-command-center.md, ALL intake/ files`. Grok drops spine.md, memory.md, writing style, hands.md, amcc.md, asana-command-center.md, and intake. `eyes.md` is not a known organ in the body map — likely invented. |
| **4. Generate brief using this exact structure (Priorities / Leverage Move / Friction to Remove / Data Snapshot / Open Questions)** | Output format | **Already implemented and validated.** This morning's update added the "Daily Brief Output Format (REQUIRED)" section based on blind A/B test (2-0). Grok's format is a *weaker subset* of the existing format — see §3 below. |
| **5. Apply `high-stakes-guardrails.md` if any forecast/budget numbers appear** | High-stakes flag | **Covered system-wide, not just am-triage.** Principle #7 in soul.md already requires loading `high-stakes-guardrails.md` for projections/forecasts/test readouts >$50K. This is not specific to am-triage; applying it at the protocol level would duplicate the cross-cutting rule. |
| **6. Post brief to Slack (rsw-channel) + save to `current.md`** | Delivery | **Partially covered, but Grok adds risk.** Delivery semantics live in the hook, not the protocol. The existing protocol logs to `hook_executions`; Slack posting is a hook concern. `rsw-channel` is not a known channel name in the body system (the Richard-facing channel handle is not structured this way in soul.md or slack-digest.md). Posting to an invented channel name is a real failure mode. |

**Summary:** 0 of 6 Grok steps are net-new. 2 are at the wrong architectural layer (#1 belongs in am-backend; #6 belongs in a hook). 1 is a massive subtraction mislabeled as simplification (#2). 1 drops required context files (#3). 1 duplicates a cross-cutting rule (#5). 1 restates — less well — a section added this morning (#4).

---

## 2. What Grok silently deletes

The existing am-triage.md performs the following that Grok's 6 steps would lose:

1. **Signal routing** — Slack [ACTION-RW] → Asana, email → Asana, Asana digest → hands.md
2. **Admin keyword detection** — override that routes budget/PO/invoice/R&O/compliance directly to Admin regardless of other mapping
3. **Admin early-start due-date enforcement** — auto-set start_on = due_on − 7 business days for Admin tasks so they surface a week before due
4. **Signal-to-Routine mapping table** — 5 categories (Sweep / Core / Engine Room / Admin / Backlog)
5. **Slack Decision Detection** — extract decisions from keywords ('decided', 'agreed', etc.) for Project Notes updates
6. **Bucket cap enforcement** — Sweep 5, Core 4, Engine Room 6, Admin 3
7. **Engine Room auto-demotion + BAU decomposition** — the whole reason this was added was to keep mandatory work moving when the cap fires. Decomposition into 2–3 piggybacked subtasks is the single most important behavioral change in the protocol. Grok deletes it.
8. **Admin 3-day escalation checkpoint** — the single centralized escalation check, per McKeown "one simple check beats triplicated logic"
9. **My Tasks deep enrichment** — four enrichment rules (Kiro_RW brevity, Next action, Begin Date, Priority_RW default) with batched approval
10. **Wiki Article Pipeline Review (Phase 1B)** — stale FINAL detection, SharePoint drift, new-article candidates, do-NOT-create-Asana-tasks rule
11. **Portfolio Project Scan (Phase 1C)** — 11-step scan covering portfolio discovery, per-project task scan, field enrichment, date windows, status staleness, recurring task auto-creation, cross-team blocker detection, event countdown, budget/PO tracking, market context auto-refresh, and findings presentation
12. **Interactive Command Center (Phase 2)** — the human-in-the-loop phase where Richard actually steers the day
13. **Hook execution logging** — INSERT INTO `hook_executions` for observability
14. **Asana-write guardrails** — every write references asana-command-center.md § Guardrail Protocol (read-before-write, audit log, retry once)
15. **Kiro_RW and Next Action field GIDs** — specific field GIDs (`1213915851848087`, `1213921400039514`) required for any write. Grok's version can't execute because it has no field IDs.

None of this is decorative. Each was added after a specific failure mode in a previous version. Replacing 300 lines of encoded failure-mode-fixes with 6 bullets is "simpler" only in the sense that hitting delete is simpler than reading.

---

## 3. Daily Brief Output Format — Grok vs existing (added today)

The existing protocol was updated **this morning (2026-04-22)** after a blind A/B test that came out 2-0 for the structured format. Grok's proposed format shares the same 5-section scaffolding but is materially thinner:

| Section | Existing (post-update) | Grok | Delta |
|---------|------------------------|------|-------|
| Priorities | 3–5 actions, each tagged L1–L5; rank-1 hard thing from `main.hard_thing_now` is Priority #1 if no artifact filed; top-3 time-ordered with clock times | "max 5, tied to Five Levels" | Grok drops hard-thing-as-P1 rule, drops time-ordering, drops artifact-on-file check |
| Leverage Move | Explicit leverage with *what it unblocks, why today, tied to L3 or L5* | "one highest-impact action" | Grok collapses into a generic "impact action" — loses the leverage framing (L3/L5 bias) and the "why today" trigger |
| Friction to Remove | Structural-not-cosmetic requirement explicit, names the principle embodied | "one thing to simplify/automate" | Grok drops the structural-vs-cosmetic guardrail — exactly the test Principle #2 in soul.md requires |
| Data Snapshot | Streak + hard thing, MX+AU pacing vs OP2 with 🔴🟡🟢 + % values, top-5 overdue with age, system health (DuckDB freshness, MCP, hooks) | "key numbers + anomalies from ingest + detector" | Grok drops the concrete field list (streak, hard thing, pacing colors, overdue ages, system health) in favor of vagueness |
| Open Questions | 3–5 binary/multiple-choice, <30s to answer, explicit "avoid open-ended 'what do you think'" | "Open Questions for Richard" | Grok drops the answerability constraint and the coaching-question exclusion |
| EOD addendum | Metrics delta table (Mon/Tue/Δ), Five Levels scorecard with evidence, friction detected, one proposed system improvement | Not mentioned | Grok has no EOD addendum, so this morning's blind-tested EOD scorecard — which the evaluator called "the single most useful artifact in either arm" — is silently dropped |
| Empirical basis | Documents the 2-0 blind test result and why the format is required | None | Grok presents the format as novel. It is not novel — it was already added this morning. |
| What NOT to do | Explicitly rejects the "Master Morning Command" AM-1→AM-2→AM-3 serial chain from an earlier external review because it regresses am-backend parallelism | None | Grok's doc would quietly reopen that rejected design by implying serial execution |

**Net:** Grok's format is a weaker, un-sourced restatement of a section written ~6 hours before Grok's file. Adopting it would regress the protocol.

---

## 4. Architecture: subtraction win, or required-complexity drop?

Principle #3 (subtraction before addition) says every element must earn its place. The test is whether removal causes a real regression.

- **Signal routing table, admin keyword override, admin 7-day early start** → earn their place because Admin tasks were repeatedly missed before these rules. Removal regresses.
- **Engine Room auto-demotion + BAU decomposition** → earned its place because without it, the cap was purely theoretical (Richard deferred every demotion decision). Removal regresses.
- **My Tasks enrichment (4 rules)** → earns its place because Kiro_RW and Next Action fields were silently empty on ~40% of tasks before this. Removal regresses.
- **Portfolio scan (Phase 1C)** → earns its place because AU/MX/Paid App/WW tasks are in *child projects*, not My Tasks. Without the portfolio scan, those tasks are invisible to the brief. Removal regresses catastrophically for the two markets Richard runs hands-on.
- **Phase 2 interactive** → earns its place because it's the only place Richard actually makes decisions on the system's proposals. Removing it makes the whole protocol one-way broadcast with no steer.

Grok's 6 steps are not a subtraction win. They are a subtraction *pretending to be a win* by ignoring what each removed element was protecting against. "Subtraction before addition" doesn't mean "delete until it fits on a napkin." It means every piece must earn its place, and if it does, it stays.

---

## 5. Does Grok's proposal add anything the existing am-triage.md doesn't cover?

**No.**

Every element of Grok's 6-step proposal is either:
- Already present in more specific form (steps 2, 3, 4)
- At the wrong architectural layer (steps 1, 6)
- A duplicate of a cross-cutting rule (step 5)
- A weaker restatement of a section added this morning (step 4)

There is no net-new capability. There is a large net-subtraction of tested, encoded behavior.

---

## Verdict: REJECT

Rejection is justified on:

1. **Nothing net-new** — every Grok step maps to existing coverage, usually more specific.
2. **Wrong layer** — ingest belongs in am-backend, Slack posting belongs in the hook, not the protocol.
3. **Silently deletes tested protections** — bucket caps, BAU decomposition, admin escalation, enrichment, portfolio scan, 11-step market-awareness — all gone.
4. **Restates today's A/B-tested format more weakly** — drops structural-vs-cosmetic test, drops hard-thing-as-P1 rule, drops EOD scorecard, drops empirical basis.
5. **Invents artifacts** — `eyes.md` is not an organ in the body system; `rsw-channel` is not a known Slack channel.
6. **Missing execution substrate** — no field GIDs, no Guardrail Protocol reference, no audit log, no retry policy. The proposal couldn't actually run against Asana.

The existing `shared/context/protocols/am-triage.md` — with this morning's Daily Brief Output Format section — is the superior artifact on every axis that matters: coverage, testedness, executability, and alignment with soul.md principles (#2 structural over cosmetic, #3 subtraction-with-earned-place, #5 invisible-over-visible).

No adoption. No partial merge. The existing protocol stays as-is.
