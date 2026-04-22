# Karpathy Triage — 2026-04-21

Triage authority: karpathy. Gatekeeper on heart.md, gut.md, experiment queue, hard-thing-selection protocol. This is a triage pass. No files modified in this pass — Richard sees the verdict first, then authorizes any edits.

## Context read

- `~/shared/.kiro/agents/body-system/karpathy.md` — full file (jurisdiction, gatekeeper protocol, validated anti-patterns, validated winning patterns)
- `~/shared/context/body/heart.md` — full file (target categories, eval types, scoring rules, hyperparameters, PE-1 active)
- `~/shared/context/body/gut.md` — full file (compression protocol, word budgets, bloat thresholds)
- `~/shared/context/intake/karpathy-queue.md` — full file (Issues 1-6)
- `~/shared/context/protocols/hard-thing-selection.md` — full file
- `~/shared/context/protocols/am-backend-parallel.md` — loaded, truncated at line 580 of 599, read enough to triage Issues 1/3/4
- `.kiro/hooks/am-auto.kiro.hook` — full file (trigger = userTriggered, prompt contains Phase 4 ten-item list)
- `~/shared/context/intake/session-log.md` tail — last ~3 days, including 2026-04-21 and 2026-04-22 entries

## Data verification

Queries run against `ps_analytics` on MotherDuck. Five findings directly contradict or complicate the brief's claims.

1. **Hook prompts HAVE been experimented on already.** `autoresearch_priors` contains rows for `am-triage`, `audit-asana-writes`, `eod-refresh` under `eval_type='output_quality'` (11 rows, n=1-3 each). `autoresearch_experiments` contains 5 completed hook-prompt experiments. The brief's claim "hook target category is declared but never exercised" is factually wrong. The category IS exercised — it's just under-sampled.
2. **But the eval is not informative on hook prompts yet.** Of 5 completed hook experiments, 4 scored `delta_ab = 0.0` and one scored +0.167. `score_a` hit 1.0 in both am-triage experiments — ceiling effect. Every change KEEPs because delta >= 0 lets 0.0-delta KEEPs through. This is the class of KEEP that violates karpathy.md "volume over precision — learning from reverts tells us what's load-bearing, keeps tell us what's compressible". 0.0-delta keeps teach nothing.
3. **`ops.hook_executions` stores OUTPUT metadata only, not INPUT state.** Columns are phases_completed, asana_reads, asana_writes, duckdb_queries, summary, errors. There is no snapshot of the signals, tasks, or calendar state the hook consumed. Replay-against-as-of-upstream requires reconstructing input state from `signals.signal_tracker` + `asana.asana_task_history` + `main.calendar_events` filtered by updated timestamps — the brief's claim that "ops.hook_executions is a fixture store" is only true if upstream tables are append-only with granular timestamps.
4. **`signals.signal_tracker` is NOT append-only.** It has `reinforcement_count`, `signal_strength`, `last_seen`, `last_decayed` columns that get mutated on every reinforcement. You CANNOT reconstruct "signal state as of date X" from the current row — the current state reflects all reinforcements since then. As-of replay on this table is broken by design. Issue 4 and Issue 5 both depend on this fixture store working. They need a append-only event-log table, or `signal_tracker_history` partitioned by day. The brief mis-stated this as "fixture store reuse — no new table needed."
5. **`ops.hook_executions` has only 9 total rows across 8 distinct hook names over 2 weeks.** `am-auto` — the hook the brief wants to first-experiment on — has ZERO rows. There is nothing to replay. Logging is inconsistent. Before am-auto is a viable experiment target, `am-auto.kiro.hook` has to start writing to `ops.hook_executions` reliably (relates to Issue 1).
6. **`main.hard_thing_candidates` does not exist.** Confirms Issue 2. And `hard-thing-refresh.py` does NOT contain `CREATE TABLE IF NOT EXISTS` — the script assumes the table exists. First run will fail on write.
7. **`autoresearch_experiments.eval_type` currently holds `information_retrieval`, `info_retrieval` (note: two spellings — existing inconsistency bug), and `output_quality`.** It does NOT hold `ranked_retrieval`. Adding Issue 5's first experiment requires a schema extension (or at minimum a new enum value + new scoring function). Brief called `amcc-halflife-v1` "framework reuse" — it's framework EXTENSION.
8. **18 of 25 completed output_quality experiments are 0.0-delta KEEPs.** The output-quality 5-dimension judge pegs at 1.0 too often. Before extending output-quality into new domains, the eval itself needs to be more discriminating.

## Issue 1 — am-auto trigger policy

**Verdict:** APPROVE (option 1 — promptSubmit + staleness guard), with a correction.

**Reasoning:** The current `userTriggered`-only policy means the backend runs only when Richard remembers to fire it. Session-log shows 8-day stale JSONs prior to 2026-04-21. That's a reliability failure, not a governance gap. Soul principle 2 (structural over cosmetic) and principle 5 (invisible over visible) both argue for the trigger to fire automatically on first user message each workday. No filler step, no nag, no decision. The staleness guard (`mtime >= today 04:00 PT`) prevents double-firing during a day Richard happens to work long hours. This does not violate subtraction-before-addition because it is REPLACING the current manual-only trigger with a default — it's a trigger-policy change, not a new hook.

**Next action:** Richard edits `.kiro/hooks/am-auto.kiro.hook` — `when.type` becomes `promptSubmit`, prompt prepends a guard check that reads the mtime of `~/shared/context/active/am-enrichment-queue.json` and bails out silently if >= today 04:00 PT. Brief's option 2 (separate nag hook) is REJECTED — that's addition before subtraction, two hooks where one suffices. Brief's option 3 (time-based schedule) is DEFERRED — Kiro platform does not appear to support it per current hook schema.

**Corollary:** This must be paired with making `am-auto` write one row to `ops.hook_executions` on every completion (`hook_name='am-auto'`, phases_completed, duration_seconds, summary, errors). Right now there are zero am-auto rows in two weeks of runs — which means the hook doesn't log its own runs. Without this, Issue 4's future experiments have no replay fixtures.

**L1-justification:** Issue 1 unblocks L1 daily habit work (the morning brief is the cue that kicks Richard into the routine). Not meta-work.

## Issue 2 — hard-thing-refresh wiring

**Verdict:** APPROVE (brief's option 1 + 3), REJECT option 2.

**Reasoning:** The hard-thing redesign was promoted 2026-04-20 but the DDL never ran. amcc.md queries `main.hard_thing_now` which silently fails. This is worse than not having the redesign at all — it's a known-broken surface. Per validated anti-pattern #5 ("Empty structural tables are load-bearing — don't remove them just because they're empty"), the fix here is to CREATE the table, not defer the protocol. Until this ships, Issue 5's first-experiment (`amcc-halflife-v1`) cannot run. Option 3 (CREATE TABLE IF NOT EXISTS on first run) is mandatory — the script currently assumes the table exists and will hard-error.

**Next action:** Three concrete changes, in order:
1. `hard-thing-refresh.py` — add `CREATE TABLE IF NOT EXISTS main.hard_thing_candidates (...)` using the DDL already spelled out in `hard-thing-selection.md`, plus `CREATE TABLE IF NOT EXISTS main.hard_thing_topic_levels (...)` and `CREATE TABLE IF NOT EXISTS main.hard_thing_artifact_log (...)` and the seed INSERT for topic_levels.
2. `am-backend-parallel.md` Phase 2 — add one line after step 2B: `Run: python3 ~/shared/tools/scripts/hard-thing-refresh.py (non-fatal if motherduck_token missing — logs null-state and continues)`. This fires on every am-auto run. No second eod invocation — subtraction before addition.
3. `am-auto.kiro.hook` prompt — no change needed; Phase 2 protocol edit above covers it.

**Reject option 2 (also in eod).** Two triggers where one suffices. The am-auto run is the primary cue; if eod wants a fresh refresh it can call the same script, but wiring into both hooks doubles failure surface.

**L1-justification:** The hard thing IS Richard's L1 anchor. Without a working refresh, amcc.md surfaces a stale hard thing every morning. This is direct L1 unblocking, not meta-work.

## Issue 3 — Step 4 wiki compression + Step 6C staleness

**Verdict:** APPROVE.

**Reasoning:** Three distinct problems. (a) Step 4 wiki routing duplicates what `wiki-maintenance.kiro.hook` already does weekly (violates subtraction-before-addition, principle 3). (b) `signals.wiki_candidates` is the daily-useful surface and is already surfaced in pre-brief queries — Step 4 as written is dead code that presents a decision. (c) Step 6C references three xlsx files that no longer exist locally (`ps-forecast-tracker.xlsx`, `ps-pacing-dashboard.xlsx`, `command-center.xlsx` — per session-log, dashboard pipeline migrated to JSON-based outputs in `shared/dashboards/data/`). Leaving Step 6C as-is is the "empty structural table" anti-pattern inverted: a populated structural reference pointing at dead resources. The fix is removal, not update.

Validated winning pattern #1 (REWORD with concrete examples) and pattern #3 (SPLIT on structural organization) do NOT apply here — this is REMOVE on validated-dead content. That maps cleanly to "REMOVE on motivational prose keeps — 2/2 kept" adjacent pattern: validated-dead content is safe to REMOVE because it has no query traffic and no unique information.

**Next action:**
1. am-frontend.md Step 4 → compress to a one-line callout pulled from `signals.wiki_candidates` + `wiki.publication_registry`: `"📚 Wiki: N articles in pipeline, top uncovered candidate: [topic] (quality X)"`. If both queries return empty, silence.
2. am-frontend.md Step 6C → remove the three xlsx paths. Replace with nothing if the step has no remaining content; replace with current JSON-served paths from `shared/dashboards/data/` if the step still does real work.
3. Weekly wiki triage → keep the existing `wiki-maintenance.kiro.hook`. Do NOT create a new `wiki-weekly.kiro.hook` (brief suggested one but that's addition).

**L1-justification:** Removing a 2-3-minute step from the daily brief is compounding L1 time recovery across every morning. Medium priority — no correctness risk if deferred, but a time leak.

## Issue 4 — Hook prompt target category

**Verdict:** DEFER.

**Pressure test result:** The brief's claim that `ops.hook_executions` + `signals.*` is a sufficient fixture store without a new `hook_fixtures` table is **false**.
- `ops.hook_executions` captures OUTPUT metadata (phases_completed, summary, errors, per-MCP counts). It does NOT capture the hook's INPUT state at run time. There is no JSON of "what signals did this hook see when it fired" anywhere in the schema.
- `signals.signal_tracker` is MUTATE-IN-PLACE (reinforcement_count, signal_strength, last_seen, last_decayed all get overwritten). You cannot reconstruct "signal state as of date X" from the current row — the row reflects all reinforcements since then. As-of replay is broken.
- `am-auto` specifically has ZERO rows in `ops.hook_executions`. 2 weeks of runs, 0 logged. Even if the replay were architecturally possible, there's nothing to replay against for the brief's first proposed experiment.

**First experiment (if APPROVE):** N/A — deferred.

**What has to be true before revisit:**
1. Issue 1 ships and `am-auto` starts logging to `ops.hook_executions` on every run (at least 30 days of history before first experiment).
2. A new `signals.signal_tracker_history` append-only table exists, OR signal_tracker gets refactored to append-only. Karpathy cannot approve experiments against an as-of replay that is architecturally unable to produce as-of state.
3. The output-quality eval is shown to be more discriminating than it is today. 13/15 current output-quality experiments are 0.0-delta KEEPs with score_a hitting the 1.0 ceiling. Adding another target domain (hook prompts) to a judge that pegs at 1.0 just produces more 0.0-delta KEEPs that teach nothing.
4. Ground-truth contamination mitigation from the brief is unworkable as written. Brief proposes "use items Richard surfaced independently via Slack/email/meeting signals captured *before* the hook ran that morning." But `am-auto` runs first thing in the morning; "signals before 06:00 PT" will usually be from the prior EOD or late-night, which the prior day's `am-auto` run ALREADY surfaced. The counterfactual ("Richard would have surfaced this even without the hook") is not testable from the timestamps alone.

Alternative that might survive triage: REJECT "am-auto Phase 4 taxonomy" as first experiment. Instead, start on hooks that already have richer `ops.hook_executions` history (eod-backend = 2 runs, still undersampled but better than 0) or on output-quality targets where the current 5-dimension judge has already produced non-zero deltas (richard-style-wbr SPLIT had a real REVERT with -0.04). Hooks are not the first priority.

## Issue 5 — Protocol target category

**Verdict:** DEFER.

**Pressure test result:** The brief positioned `amcc-halflife-v1` as "framework reuse — not framework extension." That is **wrong**.

- Existing `eval_type` values: `information_retrieval`, `info_retrieval` (naming inconsistency — existing bug), `output_quality`. `ranked_retrieval` is not in the schema.
- Adding `ranked_retrieval` requires: (a) new eval_type value; (b) new scoring function (precision@K, MRR, or NDCG@K — none of these exist in the current judge protocol); (c) new ground-truth source (asana.asana_task_history as retrospective — untested); (d) same as-of replay problem as Issue 4 because the protocol's scoring function reads `signals.signal_tracker` which is mutate-in-place.
- This is a new eval pipeline, not a new experiment in an existing category. Calling it "reuse" understates the lift.
- `amcc-halflife-v1` also depends on Issue 2 (unblocked but not yet shipped).

**First experiment (if APPROVE):** N/A — deferred.

**What has to be true before revisit:**
1. Issue 2 ships (hard_thing_candidates table created, refresh script wired, 7+ days of snapshot history accumulated).
2. Signal-tracker as-of reconstruction is solved (see Issue 4 prerequisite 2).
3. Karpathy commits to a specific ranked-retrieval scoring function and writes it into heart.md BEFORE the first experiment. Today's heart.md scoring rules are binary or 5-dimension-average. Ranked metrics (precision@K / MRR) need explicit definition, ground-truth tagging rules, and a worked example. Without this, the first experiment's delta is uninterpretable.
4. Ground-truth contamination: brief proposes look-back against Richard's retrospective task completion. This is contaminated because the current protocol output already nudged Richard's action trajectory. Brief's "look-back evaluation on a historical week where the current protocol's output is already in the log" is a reasonable mitigation IF the protocol's historical output IS IN the log — but it isn't yet (Issue 2). Circular.

Once Issue 2 ships and Issue 2's snapshot history accumulates (~30 days), `amcc-halflife-v1` becomes a candidate for a protocol experiment. But even then the first experiment should be on a smaller-surface protocol with binary ground truth (e.g., `signals.wiki_candidates` scoring formula where ground truth = "was this candidate actually published as a wiki article within N weeks" — already in `wiki.publication_registry` as binary).

## Issue 6 — Retrieval target category

**Verdict:** REJECT (hard).

**Pressure test result (existing instrumentation audit):** The brief is honest that this adds new machinery. I applied subtraction-before-addition harder than the brief did.

- VS Code / Kiro already captures tool calls per session — readFile, grepSearch, fileSearch, execute_query — via the agent transcript. This IS the retrieval log. It is not in DuckDB and not structured, but it exists. A read of a handful of transcripts would reveal the worst retrieval paths without building anything.
- `ops.hook_executions` has `duckdb_queries` count and could be extended to capture query text.
- Session-log tail is hand-written but contains "read 3-5 files to find the answer" diagnoses when retrieval fails.
- In other words: the pain that `context_queries` is meant to measure is already observable retrospectively. Build the measurement only when we cannot diagnose the pain retrospectively.

**Why reject now:**
1. Soul principle 3 (subtraction before addition). The brief proposes a new postToolUse hook + new DuckDB table + new retrospective tagging process + N days of data accumulation before any experiment can run. This is the definition of building infrastructure before learning whether you need it.
2. Soul principle 6 (reduce decisions, not options). Adding an always-on postToolUse hook adds a decision for every tool call — "did this call actually help?" — that Richard doesn't want to make, and that the agent cannot reliably self-score.
3. L1 flag. Richard's L1 streak is 22 workdays at zero. Building context-queries hook is 2-3 hours protocol + 1-2 hours hook + N days of fixture accumulation. That is L4 meta-work disguised as L2 tooling. Karpathy's own validated anti-pattern is that new machinery has to earn its place; it hasn't.
4. Even if built, the eval suffers same fixture-store problem as Issues 4/5. Historical agent retry patterns depend on agent model/version which changes; "fix the model across A and B" requires reproducing sessions in a sandbox that doesn't exist today.

**Alternative:** When a specific "retrieval is failing badly on X" moment appears, scan the last 5 session transcripts for that X, manually tag which file had the answer, and propose a targeted RESTRUCTURE or REWORD on body.md/soul.md. Treat retrieval improvements as one-offs driven by pain points, not as a new eval category, until a year of such one-offs makes the case that a formal eval saves time. Validated winning pattern #4 already handles this path — "RESTRUCTURE for actionable-first ordering consistently keeps."

**What has to be true to revisit:** Three concrete retrieval-failure moments documented in session-log within a single month, where the fix would have been different had the routing files been ordered differently. Then karpathy re-evaluates.

## Sequencing

Karpathy's ordering, derived independently. This diverges from the brief.

1. **Issue 1 first — am-auto trigger + self-logging.** Unblocks the daily habit loop AND creates the future fixture store for any hook experiments.
2. **Issue 2 second — hard-thing-refresh DDL + wiring.** Unblocks the aMCC hard thing surface AND creates the future fixture store for protocol experiments.
3. **Issue 3 third — am-frontend Step 4 compression + Step 6C staleness cleanup.** Cheap, low-risk, saves daily time.
4. **Issue 4, 5, 6 — all deferred or rejected for now.** No framework extension until (a) the as-of fixture-store problem is solved and (b) 30 days of clean `ops.hook_executions` history exists and (c) the output-quality eval is shown to break the 1.0 ceiling.
5. **In the meantime — continue existing karpathy loop on organs and style guides.** 118 experiments is still a small sample. 18 of 25 output-quality experiments at delta_ab = 0.0 is a signal that the judge needs sharpening before expanding domains. Revisit Issues 4-6 in ~30 days with fresh data.

The brief's sequencing had amcc-halflife-v1 running on the karpathy framework as an early validation. Rejected. Running an experiment whose fixture store is broken is not validation — it's theater.

## Schema changes needed (if any — do not execute this pass)

1. `main.hard_thing_candidates`, `main.hard_thing_topic_levels`, `main.hard_thing_artifact_log` — three CREATE TABLE IF NOT EXISTS statements pulled verbatim from `hard-thing-selection.md`. Add to `hard-thing-refresh.py` idempotent block at top.
2. `autoresearch_experiments.eval_type` — existing bug: both `info_retrieval` and `information_retrieval` strings are used. Normalize to `information_retrieval`. One `UPDATE main.autoresearch_experiments SET eval_type='information_retrieval' WHERE eval_type='info_retrieval'` once Richard approves. Not triggered by any issue in the queue, but surfaced during triage. Add to housekeeping list.
3. `ops.hook_executions` — `am-auto` hook needs to write to this table on completion. Requires one-line addition to am-auto.kiro.hook prompt (Phase 5 compile section): `INSERT INTO ops.hook_executions (execution_id, hook_name, ...)` — template already exists for other hooks.
4. **Heart.md edit NOT NEEDED in this pass.** Target category "Hook prompts" already declared. `eval_type = 'hook_output'` is not needed — existing `output_quality` covers it (hook prompts already exercised under `output_quality`). Brief's proposed three new eval_type values are rejected.
5. **Gut.md edit NOT NEEDED in this pass.** No new target bloats an organ budget.

## Open questions for Richard

1. **Trigger change to am-auto.** Approve changing `when.type` from `userTriggered` to `promptSubmit` with first-of-day guard? This is a behavioral change — am-auto will fire on the first prompt of every workday whether Richard wants it or not. Staleness guard prevents double-firing.
2. **Hard-thing-refresh DDL.** Approve adding CREATE TABLE IF NOT EXISTS blocks to the refresh script, and approve adding it as a Phase 2 step of am-backend-parallel.md? This makes the hard-thing surface live.
3. **am-frontend Step 4 + 6C cleanup.** Approve compressing Step 4 to a one-line callout and removing Step 6C xlsx references entirely? This is file-level text edits on am-frontend.md.
4. **Karpathy housekeeping.** Approve the `info_retrieval` → `information_retrieval` UPDATE as a one-off cleanup? No behavior change; just data hygiene.
5. **Defer confirmation.** Confirm that deferring Issues 4/5/6 for ~30 days is acceptable. If there is a downstream pressure to demonstrate karpathy-extends-to-hooks for leadership demo or similar, say so — that changes the scope calculation but not the verdict.
