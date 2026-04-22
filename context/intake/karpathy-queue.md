# Karpathy Queue

Routing memo for karpathy review. Do not action items here without karpathy's triage.

---

## 2026-04-21 — am-frontend session-summary

### Issue 1: am-auto.kiro.hook trigger policy

**Problem:** The AM-Backend hook (`~/.kiro/hooks/am-auto.kiro.hook`) has `"when": {"type": "userTriggered"}` with no time-based or promptSubmit trigger. As a result, the hook only fires when Richard manually invokes it from the Agent Hooks panel. On 2026-04-21 the hook was invoked but skipped Phase 2.5 / 3B / 4-full / 5.5 (per session-log 2026-04-21 entry), leaving `am-enrichment-queue.json` and `am-portfolio-findings.json` with Apr 13 stamps for 8 days. AM-Frontend has to fall back to live MCP queries and stale JSON to generate the daily brief.

**Evidence:**
- am-auto.kiro.hook line `"when": {"type": "userTriggered"}` (viewed 2026-04-21)
- session-log.md 2026-04-21 entry: "Skipped Phase 2.5 / 3B / 4 full scans / B2 remaining 14 tasks / Phase 5.5 SharePoint sync"
- File stat on am-enrichment-queue.json / am-portfolio-findings.json showed Apr 13 mtime until 2026-04-21 ~08:05 PT when I regenerated them manually from DuckDB
- Display name `.AM-Backend: Ingest + Process` had leading period causing Kiro Agent Hooks panel to hide it — fixed 2026-04-21 to "AM-Backend: Ingest + Process"

**Proposed Fix (karpathy to decide):**
1. Change trigger to `promptSubmit` with a once-per-day guard (check if `am-enrichment-queue.json` mtime >= today 04:00 PT, else fire). Fires on Richard's first message of the day.
2. Keep `userTriggered` but add a promptSubmit staleness nag: separate hook that checks mtime and nudges Richard if stale.
3. Add time-based schedule if Kiro platform supports it (does not appear to per current hook schema).
4. Keep manual BUT guarantee the backend always completes all phases — the current behavior of skipping Phase 4/compile when the hook IS fired is a separate deferral issue acknowledged in session-log 2026-04-21.

**Scope/Impact:** Affects AM-Frontend daily brief accuracy. Current workaround: AM-Frontend frontend queries DuckDB live when JSON is stale — works but adds 20-30s and skips the portfolio/blocker/budget enrichment logic.

**Priority:** High. This is a governance gap in the daily loop.

### Issue 2: hard-thing-refresh.py not wired to any trigger

**Problem:** The hard-thing selection redesign was promoted 2026-04-20 (per session-log 2026-04-20 entry). Infrastructure exists: `~/shared/tools/scripts/hard-thing-refresh.py`, `main.hard_thing_candidates` table DDL, `main.hard_thing_now` view referenced by amcc.md. But on 2026-04-21 a query against `main.hard_thing_candidates` returned "Catalog Error: Table does not exist" — the refresh script has never run in production. amcc.md line ~178 says "Before naming today's hard thing, query main.hard_thing_now" — that query fails silently.

**Evidence:**
- grepSearch for `hard_thing_candidates` found: protocol (shared/context/protocols/hard-thing-selection.md), refresh script (shared/tools/scripts/hard-thing-refresh.py), amcc.md references, session-log 2026-04-20 promotion entry — but NO hook file contains the refresh invocation
- am-auto.kiro.hook prompt does not invoke hard-thing-refresh
- am-backend-parallel.md protocol does not mention hard-thing-refresh step
- DuckDB catalog confirms `main.hard_thing_candidates` does not exist (table was never created, refresh never ran)
- Session-log 2026-04-20 entry notes token dependency: "MotherDuck dependency: signals.signal_tracker lives on MotherDuck, refresh requires motherduck_token in env"

**Proposed Fix (karpathy to decide):**
1. Add `python3 ~/shared/tools/scripts/hard-thing-refresh.py` call to am-backend-parallel.md Phase 2 (post-signal-routing, before Phase 3 enrichment). Verify motherduck_token available in hook context.
2. Also add to eod.kiro.hook (evening refresh catches end-of-day signal shifts).
3. Validate the DDL creates the table on first run (script currently assumes table exists — may need CREATE TABLE IF NOT EXISTS logic).
4. Until wired, amcc.md should note the dependency or fall back gracefully.

**Scope/Impact:** aMCC's hard-thing selection currently runs on the old top-down task-queue model, not the new signal-driven model that was explicitly promoted 4/20. Today's morning brief manually identified "Testing Approach / Kate doc" as the hard thing from cross-channel signals (polaris-brand-lp quality 27.5, au-cpa-cvr 14.0, etc.) — correct answer but not reproducible without the refresh procedure running.

**Priority:** High. Blocks the entire redesign from operating.

### Issue 3: Step 4 wiki pipeline usefulness in am-frontend (compression proposal)

**Problem:** am-frontend.md Step 4 reads am-wiki-state.json and routes action to wiki-editor or wiki-maintenance hook. On 2026-04-21 Richard pushed back: (a) wiki-maintenance.kiro.hook already runs weekly and handles stale/drift, (b) signals.wiki_candidates is surfaced in the pre-brief queries and is the useful daily signal, (c) deprecated ABPS AI Content project removed most action-routing, (d) wiki-editor should be pull-based not push-based.

**Evidence:**
- am-frontend.md Step 4 still references wiki-editor / wiki-maintenance routing
- wiki-maintenance.kiro.hook exists and runs on weekly cadence (handles stale/drift already)
- signals.wiki_candidates + wiki.publication_registry are the daily-useful surfaces
- ABPS AI Content Asana project deprecated 2026-04-17 per soul.md
- am-frontend.md Step 6C references `ps-forecast-tracker.xlsx` / `ps-pacing-dashboard.xlsx` / `command-center.xlsx` SharePoint pushes — these xlsx files do not exist locally (dashboard pipeline migrated to JSON-based outputs in shared/dashboards/data/), served via dashboard-server.kiro.hook

**Proposed Fix (karpathy to decide):**
- Compress Step 4 to a one-line callout in the daily brief: "📚 Wiki: N articles in pipeline, top uncovered candidate: [topic] (quality X)" — drawn from signals.wiki_candidates + wiki.publication_registry.
- Remove the standalone Step 4 section from am-frontend.md.
- Route wiki candidate triage to a weekly rhythm (e.g., Friday EOD or a new wiki-weekly.kiro.hook).
- Separately: remove or update Step 6C xlsx references to reflect the JSON-based dashboard pipeline.

**Scope/Impact:** Saves ~2-3 minutes of AM-Frontend wall-clock + reduces decision load on Richard. Aligns with soul.md principle 3 (subtraction before addition) and principle 6 (reduce decisions, not options). Step 6C cleanup is a staleness fix — current references point at files that do not exist.

**Priority:** Medium. Quality-of-life + staleness cleanup, not a correctness issue.

Routed by: am-frontend session-summary 2026-04-21 | For karpathy review

---

## 2026-04-21 — session-summary — Karpathy framework extensions (hooks / protocols / retrieval)

**Request from Richard:** "For the karpathy experiments, can you think about how we could use that same process to improve processes, hooks, and context searching (docs, data, etc)?" Then: "please route all of this, not just your proposed ones, but other context as well, to help karpathy make judgments."

**Framing.** Heart.md already lists hook prompts as a valid target category, and style guides as an output-quality target. In 58 experiments across Runs 19-27 the loop has only actually run on organs and style guides. The hook target category is declared but never exercised. Protocols (multi-step processes like am-backend-parallel.md, callout pipeline, wiki pipeline) and context retrieval (body.md + soul.md routing tables, wiki index structure, DuckDB schema discoverability) are not declared target categories at all. This brief proposes extending the framework to all three with the minimum amount of new machinery.

**Prior work karpathy should weigh:**
- `amcc-halflife-v1` is already filed as pending (session-log 2026-04-20 entry) and is de facto a protocol experiment — hyperparameter tuning on the hard-thing-selection protocol's decay half-life. Running it through the karpathy framework is the cheapest way to validate the framework extends to protocols. This is framework reuse, not framework extension.
- `main.hard_thing_candidates` table does not yet exist (see Issue 2 above in this file) — so `amcc-halflife-v1` cannot actually execute until Issue 2 is resolved. Dependency to flag.
- `main.autoresearch_experiments` + `autoresearch_priors` + `autoresearch_organ_health` already exist and are working. Extending them to hold `eval_type = 'ranked_retrieval'` or `'hook_output'` is a schema delta, not a new subsystem.
- `ops.hook_executions` + `ops.hook_reliability` already track hook runs. That is the starting surface for hook eval — we do not need a new `hook_fixtures` table on day 1; we can use the existing execution history as the fixture store, replaying against the same day's upstream Slack/email/calendar signals that signals.* already captures.
- `signals.signal_tracker` + `signals.wiki_candidates` + `signals.heat_map` are already a ranked-retrieval fixture store for protocol experiments — the signals schema IS the time-series of inputs, and Richard's actual downstream actions (Asana task completions, wiki articles eventually written, Slack replies sent) are the ground truth, already in `asana.*` and `wiki.*` and Slack history.

### Issue 4: Extend target category — hook prompts (eval_type = hook_output)

**Problem.** Heart.md declares `~/.kiro/hooks/*.kiro.hook` a valid output-quality target but no experiment has run on one. Meanwhile hook prompts accumulate drift — Issue 1 and Issue 3 above are both symptoms of prompts that no longer match what downstream consumers need. The current mechanism for detecting this is Richard noticing the drift, which is exactly what the body system is supposed to eliminate.

**Eval design proposal.**
- **Target:** a hook prompt string inside a `.kiro.hook` JSON file (e.g., `am-auto.kiro.hook` `then.prompt`, `open-items-reminder.kiro.hook` prompt, `eod.kiro.hook` prompt).
- **Techniques:** same 7 (COMPRESS, ADD, RESTRUCTURE, REMOVE, REWORD, MERGE, SPLIT).
- **Fixture store:** not a new table on day 1. Use `ops.hook_executions` to pick a historical run date, then replay against the upstream signal snapshot as-of that date (signals.signal_tracker + asana.asana_task_history + main.calendar_events filtered by `updated_at <= run_date`). For hooks that produce JSON outputs, the replay output is the hook's output file for that run.
- **Agent A:** CLI agent running modified prompt + as-of upstream data → produces hook output JSON.
- **Agent B:** CLI agent running original prompt + same upstream → produces hook output JSON.
- **Agent C:** CLI agent running modified prompt + as-of upstream, zero system context (no body.md, no soul.md) → portability check.
- **Ground truth:** Richard's engagement signal on the day-after. For am-auto, this means: of the items the hook surfaced in `am-enrichment-queue.json`, which ones did Richard actually action within 24 hours (Asana task touched, Slack reply sent, calendar block completed)? That is binary per-item ground truth available in DuckDB already.
- **Score:** precision (of items surfaced, fraction Richard actioned) + recall (of items Richard actioned, fraction the hook surfaced). `delta_ab = F1_A - F1_B`.
- **Keep rule:** delta_ab ≥ 0, same as organ rule.

**Contamination risk.** If Richard's engagement is caused by the hook surfacing it (he only saw it because the hook flagged it), using it as ground truth is circular. Mitigation: use items Richard surfaced independently via Slack/email/meeting signals captured *before* the hook ran that morning. The signal timestamps in signals.signal_tracker are granular enough to separate "signal existed before 06:00 PT hook run" from "signal created by hook output".

**First concrete experiment to propose:** REWORD the am-auto prompt's Phase 4 portfolio scan bullet list — compress the 10 portfolio scan items into a tighter taxonomy. Today's am-auto prompt has 10 Phase 4 items that overlap (discovery / enrichment / dates / staleness / recurring / blockers / events / budget / context refresh). Test whether collapsing to 5 reduces the phase-skip failure mode that caused Issue 1.

### Issue 5: Extend target category — protocols (eval_type = ranked_retrieval)

**Problem.** Protocols like am-backend-parallel.md, hard-thing-selection.md, and the callout pipeline have decision points and ranking formulas that are hyperparameters in disguise. They get tuned by "Richard eyeballs the output and says that's wrong" (see session-log 2026-04-21 Polaris dial-up and email overlay status errors). That is not scalable and it is not measurable. The karpathy framework's Bayesian prior mechanism is exactly the tool for this class of problem.

**Eval design proposal.**
- **Target:** a protocol section that produces a ranked output. Concrete candidates: `hard-thing-selection.md` decay half-life and incumbent margin; `am-backend-parallel.md` Phase 2 signal routing rules; `signals.wiki_candidates` scoring formula (currently lives in a DuckDB view definition, which is a protocol in SQL form).
- **Techniques:** same 7, applied to the protocol file's relevant section.
- **Fixture store:** the signals.* schema AS OF a past date (use `updated_at` column filters or the time-series nature of `signal_tracker`). No new table needed.
- **Agent A / Agent B:** each runs the modified vs. original protocol's ranking logic against the same as-of signal snapshot, producing a top-K list.
- **Agent C:** zero-context portability check — same eval, no body.md/soul.md.
- **Ground truth:** for hard-thing-selection, use Richard's own retrospective "what did I actually work on / avoid this week" signal from asana.asana_task_history + project_timeline. For wiki_candidates, use which candidate topics actually became wiki articles in the following N weeks (wiki.publication_registry).
- **Score:** precision@K, recall@K, MRR (mean reciprocal rank), or NDCG@K depending on whether the ground truth is binary-relevant or graded. For a top-3 hard-thing list against binary ground truth, precision@3 + MRR is sufficient.
- **Keep rule:** delta_ab ≥ 0 on the composite metric.

**Contamination risk.** Richard's action trajectory is partially caused by the hard-thing protocol's current output (the aMCC check surfaces the hard thing each day, which nudges Richard toward it). Mitigation: use a "look-back evaluation" on a historical week where the current protocol's output is already in the log. The counterfactual is "would a different half-life have surfaced a better top-3 that matched Richard's actual retrospective?" — not "did Richard do the thing the protocol said."

**First concrete experiment to propose:** Reuse `amcc-halflife-v1` (already filed, pending). Run it through this framework's eval loop. If it works end-to-end, it both tests the hyperparameter AND validates the framework extension in one run. Double-duty.

**Dependency for karpathy to flag:** `main.hard_thing_candidates` table does not exist (Issue 2 above). `amcc-halflife-v1` cannot execute until Issue 2 is resolved. Sequencing: Issue 2 first, then Issue 5's first experiment.

### Issue 6: Extend target category — context retrieval (eval_type = retrieval_mrr)

**Problem.** The highest-frequency failure mode in the body system is silent retrieval failure. When Richard asks a question, the agent reads 3-5 files to find the answer; if the body.md/soul.md routing pointed at the right file first, it would be 1 file. That latency compounds across every session. Unlike organs (where evals exist) and protocols (where at least Richard's retrospective is a signal), retrieval failure is invisible — no one is scoring it.

**Eval design proposal.**
- **Target:** the body.md navigation map, soul.md routing table, wiki index structure, steering file inclusion rules, DuckDB view naming/comments.
- **Techniques:** same 7. RESTRUCTURE and REWORD are probably the dominant techniques here.
- **Fixture store needed.** This is the one piece of actual new machinery. Proposed: a `context_queries` table populated by a lightweight postToolUse hook that records each readFile / grepSearch / fileSearch / DuckDB query made during a session, plus the final "did the agent complete the user's request without retrying" signal. Schema:
  ```
  context_queries (
    session_id VARCHAR,
    turn_number INT,
    user_intent_tag VARCHAR,    -- optional topic/tag from the user's request
    tool_name VARCHAR,           -- readFile, grepSearch, fileSearch, mcp_duckdb_execute_query, etc.
    query_text VARCHAR,          -- path or query string
    result_used BOOLEAN,         -- did the agent act on this result or retry with a different query?
    ts TIMESTAMP
  )
  ```
- **Agent A / Agent B:** simulated agents given the same historical user question, with modified vs. original routing files, each recording which sources they consulted in which order.
- **Agent C:** zero-context portability check — agent gets only the routing files and the question, no body.md/soul.md priming.
- **Ground truth:** the actual source that contained the correct answer, tagged retrospectively from the session log.
- **Score:** MRR (1 if first consulted source had the answer, 0.5 if second, 0.33 if third, ..., 0 if not found in N tries) + absolute count of tool calls used.
- **Keep rule:** delta_ab ≥ 0 on MRR.

**Contamination risk.** The agent's retry pattern can reflect agent skill, not routing quality. Mitigation: fix the agent model/version across A and B (same CLI agent config). Any retry-pattern variance is then attributable to the target file change, not the evaluator.

**Cold-start cost.** This is the one proposal with real new machinery. The postToolUse hook + the `context_queries` table + the retrospective tagging of which source was correct. Estimate: 2-3 hours of protocol work + 1-2 hours of hook implementation + N days of query log accumulation before any experiment has enough fixtures to run on. Karpathy should decide whether this is worth it or whether retrieval should stay out of scope for now.

**Why it is still worth proposing.** Retrieval is the most-frequent operation in the body system and the least-measured. If the framework does not reach it, the system plateaus at "organs and style guides are optimized, but finding the right organ is still trial-and-error." The compounding return is large.

**First concrete experiment to propose (once fixtures exist):** RESTRUCTURE the soul.md Data & Context Routing table — reorder rows by observed query frequency from the first month of `context_queries` data. Predicted keep (this is what precision@1 optimization looks like). Could also test REWORD of the "If you need..." column headers for disambiguation.

### Principles check (6 principles applied to all three proposals)

1. **Routine as liberation** ✅ — automates "should we tweak this hook / protocol / routing table?" decisions. Same liberation mechanism as the current experiment queue on organs.
2. **Structural over cosmetic** ✅ — fixture-store reuse (ops.hook_executions, signals.*, optional new context_queries) is structural. Proposal 3 is honest about adding new machinery; proposals 1 and 2 explicitly avoid adding tables by reusing what already exists.
3. **Subtraction before addition** ⚠️ — proposal adds three eval_type values and (in proposal 3) one new table. Before any build: karpathy should confirm there is not an existing process already doing part of this. `amcc-halflife-v1` is a partial hit for proposal 2. Kill the redundant machinery before building.
4. **Protect the habit loop** ✅ — the karpathy batch run's cue (scheduled / on-demand) and reward (metabolism report) are invariant. What changes is what is inside the batch.
5. **Invisible over visible** ✅ — if this works, hooks get slightly better each week and Richard does not notice why. That is the target state.
6. **Reduce decisions, not options** ✅ — Richard stops eyeballing "is this hook prompt good enough?" The eval decides. Options unchanged.

### Sequencing recommendation for karpathy

1. **Unblock Issue 2 first.** Wire hard-thing-refresh.py and create `main.hard_thing_candidates`. Without this, amcc-halflife-v1 cannot run and proposal 2 has nothing to run against.
2. **Promote amcc-halflife-v1 through this framework** as the first protocol experiment (Issue 5 first concrete experiment). This is the cheapest end-to-end validation — reuses an already-filed experiment, tests framework extension, and ships L2 progress on the hard-thing infrastructure simultaneously.
3. **Run the first hook experiment** (Issue 4 first concrete experiment, REWORD am-auto Phase 4 taxonomy) only after Issue 1's trigger policy is resolved. Otherwise the replay fixtures are biased toward the skipped-phase failure mode rather than the prompt quality.
4. **Defer Issue 6 (retrieval)** until there is a specific "retrieval is failing badly on X" moment. Do not build the context_queries hook prophylactically. Wait for the pain.
5. **Karpathy decides the eval_type enum.** Current `autoresearch_experiments.eval_type` column holds 'information_retrieval' and 'output_quality'. Adding 'hook_output', 'ranked_retrieval', 'retrieval_mrr' is karpathy's gatekeeper call — this is schema evolution on a file he owns.

### Flags for karpathy

- **L1 streak is at zero 22 workdays (per session-log).** Any new framework that takes more than a week of Richard's calendar to build is L4 meta-work in L1 clothing. Karpathy should scope aggressively and revert if the build starts extending.
- **Ground-truth contamination is the central risk across all three proposals.** Each has its own contamination story above. Karpathy should pressure-test each before approving the first experiment.
- **Output-quality evals are already agent-judged (5 dimensions: voice / structure / data / audience / actionability).** Extending this to hook outputs and ranked retrieval introduces more agent-as-judge tokens. Karpathy should cap the per-batch token budget or split to overnight only.
- **This brief itself is session-summary output, not karpathy output.** Karpathy has not triaged this. Treat the proposals and principle check as input, not as approved design.

Routed by: session-summary 2026-04-21 | For karpathy review alongside Issues 1-3
