# Karpathy Triage — 2026-04-29

Triage authority: karpathy. Gatekeeper on heart.md, gut.md, experiment queue, hard-thing-selection protocol. This is the second pass — the 2026-04-21 verdict covered Issues 1-6 with DEFER/REJECT calls on 4-6 pending fixture-store work. Eight days later we check movement on 1-6, accept/reject shipped Issue 8, triage new Issue 7, and acknowledge Issue 9 moved out of jurisdiction.

No files modified in this pass. Richard sees the verdict first, then authorizes edits.

## Context read

- `~/shared/.kiro/agents/body-system/karpathy.md` — full file (jurisdiction, gatekeeper protocol, validated patterns/anti-patterns, execution protocol)
- `~/shared/context/body/heart.md` — full file (target categories, Step 3 structural validity gate now shipped, PE-1 Phase 1 shipped 2026-04-21)
- `~/shared/context/body/gut.md` — full file (compression protocol, adaptive budgets, §7 identity protection)
- `~/shared/context/intake/karpathy-queue.md` — full file (Issues 1-9; 8 shipped 2026-04-29, 9 moved to MPE)
- `~/shared/context/intake/karpathy-verdict.md` — prior 2026-04-21 verdict (format reference + prerequisite audit)
- `~/shared/context/body/soul.md` — loaded via steering, 8 principles available
- `~/shared/tools/scripts/karpathy-loop.sh` — first 120 lines (Step 0 validity gate confirmed in prompt block)

## Data verification

Queries run against `ps_analytics` on MotherDuck. Nine findings — most of the 2026-04-21 blockers have NOT moved, one has partially moved, and one new blocker emerged.

1. **`main.hard_thing_candidates` now exists** (Issue 2 prerequisite partially met). Four tables confirmed: `hard_thing_candidates`, `hard_thing_now` (view), `hard_thing_topic_levels`, `hard_thing_artifact_log`. Schema matches `hard-thing-selection.md`. First population 2026-04-22 14:08 with 3 rows — polaris-brand-lp (rank 1, score 4.05), oci-rollout (2, 3.1), au-cpa-cvr (3, 2.8). **But**: only ONE refresh has run. The table has `refresh_at` 2026-04-22 for all 3 rows and nothing since. The refresh script is not wired to any recurring trigger — single manual invocation, then silence.

2. **`asana.daily_tracker.hard_thing_status` IS being written** (3 rows since 2026-04-21: 2026-04-27 "frozen — polaris-brand-lp incumbent 7d, Testing Doc still unsent" w=4, 2026-04-22 "polaris_no_artifact" w=1, 2026-04-21 "unsent_still" w=23). So aMCC has narrative coverage. But the `hard_thing_now` view is stale — underlying candidates table hasn't refreshed in 7 days.

3. **ZERO new experiments since 2026-04-21.** `autoresearch_experiments` max(created_at) = 2026-04-17 13:07. Twelve days of zero experiments against organs, style guides, hooks, or anything else. This is the loop going dormant, not running. 65 total experiments, 50 information_retrieval + 15 output_quality. Neither eval_type has added a row in 12 days.

4. **`info_retrieval`/`information_retrieval` spelling inconsistency NORMALIZED.** Distinct values now only `information_retrieval` and `output_quality`. The 2026-04-21 verdict flagged this as existing bug; it's been fixed. No `ranked_retrieval` or `retrieval_mrr` values have been added (consistent with Issues 5/6 DEFER/REJECT).

5. **`signals.signal_tracker_history` STILL DOES NOT EXIST.** Only `signals.signal_tracker` is in the schema. It retains `reinforcement_count`, `signal_strength`, `last_seen`, `last_decayed` — all mutate-in-place. The 2026-04-21 blocker for Issues 4 and 5 (cannot reconstruct as-of signal state) is unchanged.

6. **`ops.hook_executions` has the 2026-04-21 problem EXACTLY inverted.** Issue 1's verdict said "am-auto must start logging on every completion." Result 8 days later: `am-auto` has ZERO rows in the table. The related hook chain IS logging — `am-backend` (2 rows, latest 2026-04-22 06:16), `am-frontend` (1 row, 2026-04-22 06:40), `am-backend-remediation` (1 row, 2026-04-22 14:18), `eod-backend` (4 rows, latest 2026-04-28 04:36), `eod-frontend` (1 row, 2026-04-28 04:47). So the hook logging pattern works, but the specific `am-auto.kiro.hook` wrapper either wasn't updated OR was superseded by the `am-backend`/`am-frontend` split. Needs Richard clarification on current topology.

7. **W18 batch (Issue 8 claim) did NOT land in autoresearch_experiments.** Issue 8 states "876 trials" and "13 .kiro.hook JSON files broken." Zero hook-target experiments exist in the DB with revert_reason='structural_invalidity' or any other reason. The 5 output_quality hook experiments in `autoresearch_priors` (am-triage×MERGE, am-triage×ADD, audit-asana-writes×RESTRUCTURE, audit-asana-writes×ADD, eod-refresh×SPLIT) are all n=1 KEEPs from pre-W18 runs. Either W18 ran against a different DB/log instance, the 876 count is inflated, or the batch reverted all results including the successful ones. Flag for Richard — this matters for calibrating the validity gate's real value.

8. **Issue 8's ship IS CONFIRMED in code.** `heart.md` Step 3 contains the "Structural validity gate (mandatory, runs between Step 3 apply and Step 4 eval)" block with the per-extension parse table, auto-REVERT rule, and rationale. `karpathy-loop.sh` contains the "STRUCTURAL VALIDITY GATE (mandatory, pre-eval)" Step 0 block inside the batch prompt with matching per-extension commands. Both files are consistent.

9. **PE-1 Phase 1 shipped 2026-04-21 per heart.md header.** `lead_weeks` and `prediction_run_id` are in `ps.forecasts`. Phase 1 validation queries are spelled out in heart.md. No impact on current triage — PE-1 is its own lane.

---

## Issue 1 — am-auto trigger policy

**Prior verdict (2026-04-21):** APPROVE with correction (promptSubmit + staleness guard + am-auto must write to `ops.hook_executions`).

**Verdict:** NOT SHIPPED — status ambiguous, needs Richard clarification.

**Reasoning:** The am-auto row count in `ops.hook_executions` is still zero over 2+ weeks, which looks like the prior verdict's corollary never shipped. But `am-backend`, `am-frontend`, and `am-backend-remediation` ARE logging — so either (a) the prior `am-auto.kiro.hook` was refactored into a multi-hook pipeline and the name "am-auto" is retired, or (b) am-auto still exists but delegates to am-backend/am-frontend which do the logging. Session-log would clarify but this triage pass doesn't require resolving it — the prior verdict stands either way: first-of-day trigger + staleness guard + self-logging for WHATEVER hook is the canonical morning entry point.

**Also:** the "stale JSON" failure mode from the 2026-04-21 brief hasn't recurred in anything I can see — the am-backend/frontend/remediation chain ran 2026-04-22 and appears healthy. So maybe this shipped under different names and we're fine. Or it shipped partially and the next outage will expose it.

**Next action:** Richard confirms which hook file is currently canonical (am-auto vs am-backend vs am-backend-parallel-v2) and whether the promptSubmit + staleness guard + self-logging triple landed. If any of the three is missing, Issue 1 is still open. Do NOT re-litigate the prior verdict — the direction remains correct.

**Status flag for Richard:** rot risk — 8 days without visible movement on a High-priority issue that unblocks Issues 4/5. If the canonical hook still fires on `userTriggered`, the daily habit loop stays fragile and hook-prompt experiments remain infeasible.

**L1-justification:** unchanged. The morning backend is the cue that starts the routine.

---

## Issue 2 — hard-thing-refresh wiring

**Prior verdict (2026-04-21):** APPROVE (option 1 + 3 — CREATE TABLE IF NOT EXISTS + Phase 2 wiring), REJECT option 2 (double-trigger into eod).

**Verdict:** PARTIALLY SHIPPED — DDL ran once, recurring trigger did not.

**Reasoning:** The four tables exist (DDL step confirmed — option 3 partially landed or was executed manually). `main.hard_thing_candidates` has one row-set dated 2026-04-22 14:08 with 3 plausible candidates (polaris-brand-lp, oci-rollout, au-cpa-cvr). Those are exactly the topics the 2026-04-21 brief said Richard was manually identifying. So the script ran once and produced correct output.

But: no refresh in 7 days. That means option 1 (wire into Phase 2 of am-backend-parallel.md) did NOT land — or landed but the hook path is broken silently. `main.hard_thing_now` reads from `hard_thing_candidates WHERE refresh_at = (SELECT MAX(refresh_at) FROM ...)` so aMCC is pulling a 7-day-stale top-3. Per validated anti-pattern #5 ("empty structural tables are load-bearing"), we now have the inverse: a stale structural table, load-bearing AND misleading.

Even so, `asana.daily_tracker.hard_thing_status` has been written on 2026-04-21, 2026-04-22, and 2026-04-27 with meaningful narrative status strings. So something is tracking the hard thing — but it's writing ad-hoc status strings, not consuming the refresh view. The refresh machinery exists and is disconnected from the daily surface.

**Next action:**
1. Richard or kiro-server confirms whether `hard-thing-refresh.py` is wired into `am-backend-parallel.md` (or whichever the current canonical morning hook is). If not, wire it per the 2026-04-21 verdict.
2. If wired and silently failing, add a non-fatal error log to `ops.hook_executions.errors` so failures are observable.
3. Question for Richard: is the manual `hard_thing_status` string in `daily_tracker` sufficient for aMCC display purposes, or does the ranked top-3 from `hard_thing_candidates` need to be what aMCC surfaces? This drives the Issue 7 dual-display question (below).

**Status flag for Richard:** rotting. The 2026-04-21 verdict said this unblocks protocol experiments. 7 days of staleness means Issue 5's first experiment (`amcc-halflife-v1`) still has no clean fixture store — the very thing DDL creation was supposed to enable isn't accumulating data.

**L1-justification:** unchanged — direct L1 unblocking.

---

## Issue 3 — Step 4 wiki compression + Step 6C staleness

**Prior verdict (2026-04-21):** APPROVE (compress Step 4, remove Step 6C xlsx refs, keep existing weekly wiki-maintenance hook).

**Verdict:** STATUS UNKNOWN in this triage — defer to Richard.

**Reasoning:** I have not read am-frontend.md in this pass to check whether Step 4 was compressed and Step 6C xlsx references removed. This is cheap, low-risk, text-edits-only work. If it shipped, close. If not, ship it this week — it's a time-leak, not a correctness risk, but 8 days of accumulated morning overhead adds up.

**Next action:** Richard confirms whether am-frontend.md edits shipped. If not, 15-minute edit.

**Status flag for Richard:** low rot risk — cheap to close whenever.

---

## Issue 4 — Hook prompt target category

**Prior verdict (2026-04-21):** DEFER. Four prerequisites: (1) Issue 1 ships + 30 days am-auto logging, (2) signal_tracker_history exists or signal_tracker refactored append-only, (3) output-quality eval proven discriminating, (4) ground-truth contamination mitigation workable.

**Verdict:** DEFER (unchanged).

**Reasoning:** Prerequisite check 8 days later:
1. **Issue 1:** not visibly shipped, and even if it shipped yesterday we need 30 days of accumulated am-auto history before first experiment. So best case = 2026-05-29. Likely later.
2. **signal_tracker_history:** still does not exist. Unchanged.
3. **Output-quality eval discrimination:** no new experiments in 12 days means no new evidence. The 15 output_quality experiments in total still show 12 zero-delta KEEPs (80%) — the 1.0 ceiling problem is unresolved and the eval is not more discriminating than it was 8 days ago.
4. **Ground-truth contamination:** no mitigation work shipped, same as before.

Zero prerequisites moved. DEFER stands.

**What has to be true before revisit:** unchanged from 2026-04-21 verdict. Plus now: the loop itself has to resume running. Zero experiments in 12 days on ANY target category is a bigger problem than whether hook prompts are on the menu. Fix the loop before expanding its diet.

**Next action:** none in this pass.

---

## Issue 5 — Protocol target category

**Prior verdict (2026-04-21):** DEFER. Four prerequisites: Issue 2 ships + accumulates, signal_tracker as-of solved, karpathy commits to ranked-retrieval scoring function in heart.md BEFORE first experiment, ground-truth contamination handled via look-back on historical weeks.

**Verdict:** DEFER (unchanged).

**Reasoning:** Prerequisite check:
1. **Issue 2:** DDL shipped, recurring trigger did not. One refresh worth of data (3 rows) is not "~30 days of snapshot history accumulated." Partial progress but nowhere near sufficient.
2. **signal_tracker as-of:** unchanged.
3. **Ranked-retrieval scoring function in heart.md:** not written. heart.md has the PE-1 Phase 1 entry and the new structural validity gate, but no new scoring protocol. Consistent with DEFER — nothing has been committed to.
4. **Historical look-back contamination mitigation:** partial progress. We now HAVE a historical snapshot (the 2026-04-22 refresh) that can be compared to subsequent action. But a single snapshot is a single data point; the look-back needs multiple snapshots across weeks to be anything other than anecdote.

One prerequisite moved partially (Issue 2 DDL ran), three unchanged. Still DEFER.

**Next action:** none in this pass. When Issue 2 is fully wired and ~30 days of refresh history exist, reopen.

---

## Issue 6 — Retrieval target category

**Prior verdict (2026-04-21):** REJECT (hard). Three documented retrieval-failure moments in session-log required before revisit.

**Verdict:** REJECT (unchanged).

**Reasoning:** No session-log evidence surfaced in this triage of the three-documented-moments trigger firing. No new machinery proposed by any agent since. Soul principle 3 (subtraction before addition) still argues against building a context_queries table for a pain point that remains hypothetical.

Separately: the loop being dormant 12 days is more signal than any retrieval eval would produce. Fix what's already built before building more.

**Next action:** none.

---

## Issue 7 — Streak + rate dual-display

**Source:** agent-bus ideas v2 #6 (2026-04-29). kiro-local proposed swap streak → 7-day hit rate; kiro-server mutated to keep both.

**Verdict:** APPROVE-WITH-CORRECTION.

### (a) Is this karpathy jurisdiction?

Yes. `main.hard_thing_now` is Karpathy-owned territory per soul.md ("Sole authority on heart.md, gut.md, experiment queue, hard-thing-selection protocol"). aMCC rendering logic that reads this view is downstream — the data shape the view exposes is mine; the rendering template on top of it is ambiguous but the DATA COLUMN decision is squarely mine. Having opinions on the bus is fine; shipping the column is Karpathy.

### (b) Does dual-display violate any soul.md principle?

Check all 8:

1. **Routine as liberation** — mixed. Two metrics side-by-side is two things to track, but both are already implicit in `daily_tracker` — computing the rate is free. The "liberation" argument is that a zero streak no longer reads as total failure, which protects the routine from all-or-nothing thinking.
2. **Structural over cosmetic** — ✅ passes. This is a data change (new column + rendering rule), not a format/layout change.
3. **Subtraction before addition** — ⚠️ tension. Adding a second metric next to an existing one. Counter-argument: the streak-only metric is actively harmful (zero-reset creates fragility soul.md itself flags as anti-pattern). So this is subtract-brittle-semantics-then-add-durable-semantics. Acceptable, but the addition has to earn its place.
4. **Protect the habit loop** — ✅ passes. The cue (morning aMCC surface) and reward (seeing the number move) are unchanged. The metric ON the surface evolves; the surface itself does not.
5. **Invisible over visible** — ⚠️ slight tension. This IS a visible change. Richard will notice a second number appear. Novelty decay risk. Counter-argument: the CURRENT streak going to zero was visible-and-punishing; replacing punishment with a graded number is less punishment visibility, which over a week trends invisible.
6. **Reduce decisions, not options** — ✅ passes. Richard doesn't decide which metric to look at; both are there. The rate takes over mental weight when streak = 0 by design, not by choice.
7. **Human-in-the-loop on high-stakes** — N/A, this isn't a >$50K projection.
8. **Check device.md before proposing tools** — ✅ passes. This isn't a new tool — it's adding a column to an existing view.

Net: no hard violation. Principle 3 and 5 have mild tension; both are resolved by the subtract-brittle-add-durable framing. Approve.

### (c) Is "coexist vs swap-at-streak=0" question material?

Yes, and kiro-server's instinct is right but incomplete. Three options:

**A. Always coexist:** display "streak Xd · rate Y/7" on every render. Simplest. One rendering rule. Passes all principles.

**B. Swap at streak=0:** when streak > 0 show streak; when streak = 0 show rate. Conditional rendering rule. More complex logic, marginal principle-4 advantage (invariant display shape on good days).

**C. Always coexist with visual weight swap:** both always visible, but primary font weight follows whichever metric is currently "telling the better story" (streak when > 3d, rate otherwise). Too clever. Adds a threshold that will get relitigated.

**Karpathy call: Option A.** Always coexist. Reasoning:
- Principle 1 (routine-as-liberation) is strongest when the rule is invariant. One rendering shape, no branch.
- Option B's "swap at streak=0" means Richard's mental model has to track which metric is currently primary. That's a decision he now has to make subconsciously ("am I in streak mode or rate mode?"). Violates principle 6.
- The streak going to 0 is ALREADY visually muted by showing "streak 0d" — you don't need to hide it to make the rate primary. The rate being present does the work.
- Option A is 1 rendering rule; Option B is 3 (streak>0 case, streak=0 case, transition); Option C is 5+. Subtraction before addition.

### (d) Implementation spec (if approved)

**Schema change (main.hard_thing_now view):**
- Add column `rate_7d DOUBLE` = rolling 7-day count of days where `asana.daily_tracker.hard_thing_status` indicates a shipped artifact / 7.
- Ground truth for "shipped": Richard to confirm — but the 2026-04-21/22/27 status strings already encode "artifact vs no artifact" narratively. Simplest heuristic: status text matches `/shipped|sent|completed|published/i` → counted as hit. If that's too noisy, add a binary `hard_thing_completed BOOLEAN` column to `daily_tracker` and source `rate_7d` from that cleanly.

**Rendering rule (aMCC):**
- Format: `streak Nd · rate K/7` (e.g., "streak 3d · rate 5/7", "streak 0d · rate 4/7")
- Always both. No conditional.
- Placement: wherever the current streak is rendered in amcc.md. Replace single metric with the two-part string.

**Bayesian framing:** once this ships, `rate_7d` itself becomes a target. If the rolling window of 7 is wrong (too short = too noisy, too long = too slow to respond to real change), that's an `amcc-ratewindow` experiment. But ship the 7-day window first — it's the instinct in the thread, and tuning before shipping is premature optimization.

**Timing:** independent of Issues 1/2/4/5/6. Can ship anytime. Actually good choice to ship while the loop is dormant because it needs no eval machinery.

**Status flag for Richard:** confirm (a) which rendering file holds the aMCC display logic (amcc.md consumer or a downstream template), (b) whether `hard_thing_completed BOOLEAN` should be added to `daily_tracker` to simplify the rate calc, (c) whether the 7-day window or a different period (5 workdays? 14 days? 30?) better matches the rhythm of hard-thing work cadence. Default to 7 if Richard doesn't have a strong opinion.

**L1-justification:** direct. A graded metric that survives single-day misses protects the L1 habit loop from the all-or-nothing reset that's been breaking it for 23+ workdays.

---

## Issue 8 — Evaluator file-type validity gate (SHIPPED 2026-04-29 by kiro-server)

**Verdict:** ACCEPTED, with one calibration note.

### Review of shipped implementation

Read heart.md Step 3 structural validity gate block and karpathy-loop.sh Step 0 block. Both present, consistent, with matching per-extension table:

| Extension | Check |
|---|---|
| `.kiro.hook`, `.json` | `python3 -c "import json,sys; json.loads(open(sys.argv[1]).read())" <path>` must return 0 |
| `.py` | `python3 -c "import ast,sys; ast.parse(open(sys.argv[1]).read())" <path>` must return 0 |
| `.sh` | `bash -n <path>` must return 0 |
| `.yml`, `.yaml` | `python3 -c "import yaml,sys; yaml.safe_load(open(sys.argv[1]))" <path>` must return 0 |
| `.md`, `.txt`, unknown | no structural gate |

Behavior: auto-REVERT with `revert_reason='structural_invalidity'` on fail, eval scores NULL, priors updated (β+1), snapshot restored. This is the right behavior. Cheap check, correct placement (pre-eval), correct failure mode (revert not crash).

### The one concern

The 876-trials / 13-broken-hooks claim in Issue 8 does not match what's in `autoresearch_experiments`. Zero rows exist with `revert_reason='structural_invalidity'`, and zero experiments at all since 2026-04-17. Either:

- The W18 batch ran against a different DB/log and the results never synced in.
- The 876 figure is the attempted-invocation count, not experiments that recorded rows.
- The batch aborted mid-run and reverts were applied via `git checkout` without writing DB rows (per Issue 8 statement "Reverted via git checkout").

The third option is most plausible given the language "reverted via git checkout, all hooks now parse" — the fix was at file-system level, not via the prior-update protocol. That means the W18 batch produced zero learning: no β+1 updates against the broken target×technique combos, so the priors don't know that (say) am-triage×REMOVE reliably breaks the JSON.

### Calibration note

The validity gate shipped correctly, but the W18 batch's handling revealed a gap: when a batch is reverted manually via git outside the KARPATHY protocol, the priors don't update. This means next batch's target selection will re-propose the same broken combos. Two options to address:

1. **Retroactive prior update** — query which targets × techniques were in the W18 batch, manually β+1 them, log as `revert_reason='structural_invalidity'` with NULL scores. Captures the signal. But this is Richard-approve territory because it's a hand-edit to the prior table, not an organic loop output.

2. **Treat W18 as a null batch** — accept that the broken attempts don't feed priors, trust the shipped validity gate to catch the same failures going forward, and let the Bayesian priors re-learn those combos are bad through future organic reverts.

**Karpathy call: option 2.** Let the validity gate catch it organically going forward. Option 1 risks imprinting a revert signal based on mixed causes (structural invalidity AND prose degradation would both be lumped together), and the validity gate + fast-fail gate + A/B/C eval is enough mechanism to rediscover which combos are load-bearing. Forcing manual prior updates fights the autoresearch-ness of the system.

**Next action:** nothing in this pass. Issue 8 closed. The gate is correct as shipped.

**Flag for Richard:** if a future batch produces another "fix via git checkout not via protocol" outcome, that's a signal that the loop protocol itself has a hole — the protocol should be able to auto-revert without requiring manual filesystem surgery. Separate issue if it recurs.

---

## Issue 9 — US baseline model architecture (MOVED OUT)

Acknowledged. Moved to `~/shared/context/active/mpe-followups/us-baseline-architecture.md`. Correct routing call by kiro-server — fit-protocol architecture for the MPE is not Karpathy jurisdiction. No triage by me.

---

## Sequencing recommendation

This is the critical section. The 2026-04-21 sequencing was "Issue 1 → 2 → 3, defer/reject 4/5/6." Eight days later the real sequencing is different because the loop itself has gone dormant.

1. **REVIVE THE LOOP FIRST.** Zero experiments in 12 days on ANY target is the biggest single issue in the queue. Not hooks, not protocols, not retrieval — just getting the existing loop running against organs and style guides. The 2026-04-21 verdict called out "18 of 25 output-quality experiments at delta_ab = 0.0" as judge-discrimination problem; the fact we haven't added any new data points since means we don't know if the judge has gotten better or worse. Ship anything — a 10-experiment batch on any target — to confirm the loop still runs end-to-end post-Issue-8 validity gate ship. If it doesn't run, we have a regression in the gate implementation.

2. **Clarify Issue 1 status.** Which hook is the canonical morning entry point? If am-auto is retired and am-backend/am-frontend carry the load, update the 2026-04-21 verdict language to reflect. If am-auto is still there and unchanged, wire it per the prior verdict. This is a 15-minute clarification, not a design decision.

3. **Finish Issue 2 wiring.** DDL ran manually once. Wire the recurring trigger. Without it, Issue 5 prerequisites never accumulate.

4. **Ship Issue 7.** Independent of 1/2/4/5/6. Cheap. Direct L1 protection. Adding `rate_7d` to `hard_thing_now` view is a 30-minute ticket. No eval dependency. No contamination risk. Fastest win in the queue.

5. **Close Issue 3** if not already closed. 15-minute text edit.

6. **Issues 4/5/6 remain DEFER/DEFER/REJECT.** Zero prerequisites moved enough to reopen. Revisit 2026-05-29 at earliest (30 days from today) IF the loop has resumed AND Issues 1/2 have accumulated clean fixture data.

Divergence from 2026-04-21 verdict: the prior pass treated "the loop is running fine, we're just deciding what to add" as given. It wasn't. The loop has been idle since 2026-04-17. Priority 0 is getting it running again. Nothing else matters until that's confirmed.

---

## Schema changes needed (if any — do not execute this pass)

1. **`main.hard_thing_now` view** — add `rate_7d DOUBLE` column for Issue 7. Richard approves exact definition.
2. **`asana.daily_tracker.hard_thing_completed BOOLEAN`** — OPTIONAL but recommended for Issue 7 rate calc cleanliness. Source: Richard's morning tracker entry. Default = NULL, back-fill 2026-04-21/22/27 rows per narrative status strings.
3. **Issue 1's `am-auto → ops.hook_executions` logging** — still pending IF am-auto is still canonical. No schema change; hook prompt addition only.
4. **No changes to heart.md, gut.md, or hard-thing-selection.md in this pass.** Issue 8 already updated heart.md Step 3. No other triaged issue requires karpathy-file edits.
5. **Housekeeping from 2026-04-21 carried over:** the `info_retrieval` → `information_retrieval` normalization appears to have been done (only `information_retrieval` remains as a distinct value). Close that housekeeping item.

---

## Flags for Richard

1. **The loop is dormant.** 12 days without a new experiment is the single most important signal in this triage. Everything else is noise if the engine isn't running. Before authorizing any of the triage items below, confirm whether the loop is stopped on purpose (per your call) or stopped accidentally (broken somewhere). If accidental, fixing it comes first.

2. **Issue 1 status clarification.** Which hook is the canonical morning entry point as of 2026-04-29? am-auto has zero logging; am-backend / am-frontend / am-backend-remediation are logging. If the topology changed, the 2026-04-21 verdict's recommendations should be re-pointed at whatever the current canonical hook is.

3. **Issue 2 finish-line.** DDL ran; recurring trigger did not. Authorize wiring `hard-thing-refresh.py` into the canonical morning hook (whichever it is per flag 2) as a Phase 2 step, non-fatal.

4. **Issue 7 — confirm window.** 7-day rolling window is the default instinct. If you have a different view (5 workdays to match weekly rhythm, or 14 for longer-cycle work), say so before ship. Karpathy default is 7.

5. **Issue 7 — confirm rendering surface.** `main.hard_thing_now` is the view; the actual display text comes from something downstream (amcc.md or a hook template). Confirm which file owns the template so rendering changes land in the right place.

6. **W18 batch auditability.** The claim of 876 trials + 13 broken hooks is not evidenced in `autoresearch_experiments`. If this batch was instrumented differently (different DB, different log path, different agent config), capture that in a session-log note so future karpathy passes can reconstruct what happened. If it ran but results are lost, that's a reliability signal about the loop's own observability that Karpathy should track separately.

7. **DEFER confirmation carried over.** Issues 4/5/6 remain DEFER/DEFER/REJECT. If a leadership demo, business review, or upward story REQUIRES demonstrating framework-extends-to-hooks in the next 30 days, that changes the calc — say so and Karpathy will design a minimal-machinery showcase experiment that's honest about the fixture-store gap. Otherwise, 30-day patience holds.

8. **Principle-3 temperature check.** soul.md principle 3 (subtraction before addition) has been load-bearing in both 2026-04-21 and 2026-04-29 verdicts — it's the justification for rejecting the retrieval target category, deferring hook/protocol extensions until fixture stores exist, and the mild tension with Issue 7's dual-display. If you think Karpathy is being too conservative with it (i.e., the bar for "earning its place" is too high), say so. The verdicts can be re-evaluated. Right now the combination of dormant loop + zero prerequisite movement over 8 days reinforces conservative default, not the opposite.

Triage complete — verdict file written.


---

## ADDENDUM — 2026-04-29 19:20 — Loop-dormancy finding was FALSE

Triage authority: kiro-server, correcting the earlier karpathy sub-agent verdict.

**The verdict above claims the loop has been dormant for 12 days. That is wrong.** The loop is running and has been running. The data-plane was lying.

### What actually happened

The sub-agent that wrote this verdict used `mcp_duckdb_execute_query` to verify state. That tool connects to **MotherDuck `ps_analytics`**, which shows `MAX(created_at) = 2026-04-17 13:07` on `autoresearch_experiments`.

The karpathy loop writes to the **local DuckDB at `/home/prichwil/shared/data/duckdb/ps-analytics.duckdb`** (per `~/shared/.kiro/agents/karpathy.json` prompt). That's a different database. Queried directly via Python:

- 2,238 experiments total across 4 eval_types
- Most recent: 2026-04-30 04:25 (minutes before this addendum was written)
- Batches 151-156 ran 2026-04-29 19:56 through 2026-04-30 04:25 — 8.5 hours continuous, 1,056 experiments, 57% keep rate
- Loop is currently mid-batch 157 (PID 195023, started Apr 29, spawning kiro-cli eval subprocesses)

`experiment-log.tsv` and `karpathy-loop.log` both corroborate this — the TSV has fresh `run_W18_batch156` rows, the log shows 330 EXP entries and active `INSERT INTO autoresearch_experiments` calls.

### What's actually broken

**MotherDuck sync.** Local DuckDB → MotherDuck `ps_analytics.autoresearch_experiments` has not pushed since 2026-04-17. Every agent that queries the autoresearch schema via the MCP DuckDB tool sees a 12-day-stale snapshot. This is broader than karpathy — **any agent decision that used `autoresearch_experiments`, `autoresearch_priors`, or `autoresearch_selection_weights` via MCP since 4/17 is based on stale data.**

### What the corrected verdicts are

- **Issue 4/5/6 DEFER/DEFER/REJECT reasoning based on "loop not running" is invalid.** Actual prerequisite check requires querying local DuckDB, not MotherDuck. Re-triage should pull from `/home/prichwil/shared/data/duckdb/ps-analytics.duckdb` directly.
- **"Priority 0: revive the loop" inverts to: "Priority 0: fix the MotherDuck sync."** The loop is fine. The visibility into the loop is broken.
- **W18 batch claim in Issue 8** (876 trials, 13 broken hooks) — directly confirmed in the local DB. The batch happened. Keep rates visible: `run_W18_batch151` = 248 exp / 190 keeps (77%), `batch153` = 208 exp / 138 keeps (66%). Validity gate rationale stands.
- **Karpathy's own verdict reading MotherDuck-via-MCP is structurally prone to this failure.** Any future karpathy triage should include an explicit "query the local DuckDB, not MCP" line in the context-read list. Adding this to the triage protocol is a follow-up for wiki-candidates (`operations/karpathy-triage-protocol`).

### What Richard needs to act on (next session)

1. **MotherDuck sync audit.** Identify the sync script/hook, figure out why it's been silent since 4/17, wire a post-batch or EOD-Phase-7.5 push. Until fixed, every MCP DuckDB query on the autoresearch schema is a trap. Asana task filed.
2. **US baseline Option 2.** Richard approved. 4-6 hour build in `write_v1_1_slim_forecasts.py` — add `yoy_growth - lag(yoy_growth, N)` regressor, schema update for `nb_yoy_accel`, backfill, rerun backtests. Asana task filed.
3. **Issue 7 (rate_7d)** and the remaining verdict items (Issues 1-6) can resume from the corrected diagnosis when the MotherDuck sync is fixed and data is readable again.

Addendum complete — original verdict preserved above for audit trail, supersession of "loop dormant" finding recorded here.
