# Wiki Candidates Queue

Append-only log of wiki article candidates and enrichment opportunities observed by hooks during their normal runs. Hooks observe — they do not analyze, classify, or draft. The wiki-editor consumes this file during the weekly `wiki-maintenance` manual hook run and proposes action.

## Format

One line per candidate. Loose format — hooks don't judge quality or priority. That's the editor's job.

```
[YYYY-MM-DDTHH:MM hook-name] signal: <one-line observation> | source: <where it came from> | proposed: <article slug or "enrich: existing-slug">
```

## Rules for contributing hooks

- One line per candidate. Do not expand.
- Timestamp in PT (use `TZ=America/Los_Angeles date +%Y-%m-%dT%H:%M`).
- Hook name = your hook's short name (am-auto, eod, session-summary, wbr-callouts).
- `signal:` — what you observed in one sentence.
- `source:` — DuckDB table, file path, Slack thread ID, meeting session ID.
- `proposed:` — either a new article slug OR `enrich: <existing-slug>` if the signal updates an existing doc.
- If unsure whether something is wiki-worthy, err on the side of appending. Noise is cheaper than misses.
- Do not deduplicate against existing entries. The consumer handles dedup.

## Rules for consuming hook (wiki-maintenance)

- Read this file during the manual wiki-maintenance run.
- Dedupe by signal text similarity + proposed slug.
- Group related signals (multiple hooks flagged the same topic = stronger signal).
- Propose top 3-5 items to `_meta/review-queue.md` for Richard's review.
- Archive processed entries by moving them to `archive/wiki-candidates-YYYY-WNN.md`.
- Do not draft articles from this file. Only propose.

## Kill condition

**2026-06-01.** If this queue accumulates >100 unprocessed entries AND wiki-editor hasn't promoted any to review-queue.md, the contribution pattern is noise — delete the file, revert the hook contributions, and go back to manual article creation. Keep-or-kill on 6/1.

---

## Candidates


<!-- Hooks append below this line -->
<!-- Last archive: 2026-W16 second pass (2026-04-17 19:00 PT). Prior entries moved to archive/wiki-candidates-2026-W16.md. -->
<!-- Last archive: 2026-W18 (2026-05-01). 362 entries moved to archive/wiki-candidates-2026-W18.md. -->
<!-- Last archive: 2026-W18 second pass (2026-05-01 19:00 PT). 5 pipeline-meta entries archived; no topic promotions. -->
[2026-05-01T15:59 session-summary] signal: Weekly maintenance hooks need an idempotency check before Half A executes — same-day re-invocation should detect prior-run artifacts (state-file mtimes, review file mtimes, cache timestamps) and skip-report rather than produce duplicate enrichments or re-grade completed DRAFTs; session-log scan works but is fragile as the sole tripwire. | source: this-session | proposed: enrich: wiki-pipeline-rules
[2026-05-01T16:29 session-summary] signal: Stage-level idempotency beats run-level idempotency for weekly maintenance hooks — re-running the same hook the same day still produces throughput if each stage independently checks "has my input changed since last fire?" rather than the orchestrator checking "has this hook run today?"; morning noop'd Stage 4 ran cleanly in the evening by picking an executable item from the same queue. | source: this-session | proposed: enrich: wiki-pipeline-rules
[2026-05-01T16:29 session-summary] signal: Blind dual-eval protocol (pipeline-rules §1) produces split verdicts on borderline articles where rubric-mode approves but reader-simulation finds packaging issues — the split IS the signal, not noise; articles that score 7-8 on rubric but 7 on reader-sim belong in revision-queue not FINAL, and the reader-persona catches audience-specific concerns (Kate's wall-of-prose scanning pattern, Lena's practical follow-up questions) the rubric structurally can't see. | source: this-session | proposed: enrich: wiki-pipeline-rules
[2026-05-01T16:36 session-summary] signal: "Richard-blocked" status in pipeline tracking should require a concrete clarifying question in one sentence, not fuzzy "needs Richard input somehow" — three of four blockers surfaced in the W18 re-run failed this test (stale cached values, premature decomposition ask, orphaned ops flag reference); anything that can't pass the one-sentence-question test belongs in process-observations, not pending-decisions. | source: this-session | proposed: enrich: wiki-pipeline-rules
[2026-05-01T16:36 session-summary] signal: Wiki articles that reference canonical numbers (CCP values, OP2 targets, rate card) should cite the source-of-truth location (column U of CCP Q1'26 check yc.xlsx + ps.market_constraints_manual), not bake in specific values — the source-of-truth pattern decouples article freshness from rate-card negotiation cadence and prevents the "pre-negotiation value gets enshrined as canonical" failure mode that happened with MX $90/$30 getting propagated across the W18 queue for 10 days before correction. | source: this-session | proposed: enrich: ieccp-planning-framework
[2026-05-01T20:16 session-summary] signal: "no, don't just hand it off with a bus post because you think it's too big" — when an agent has override authority for a single-shot completion session, declining items with reasoning that rationalizes not trying (pipeline-work / UX-reshape / too-large-scope) is a failure mode; the fix is to re-examine each declined item for what's the narrowest-useful version, not to punt | source: this-session | proposed: enrich: existing-slug agent-load-shape-discipline

[2026-05-01T21:30 session-summary] signal: "env-gated" skip labels are first-draft judgments — always re-examine before closing a shipping window to find narrower-but-honest scope cuts; 4 of 6 env-gated items in this session turned out to be shippable once the LLM/integration framing was dropped. | source: this-session | proposed: enrich: agent-load-shape-discipline
[2026-05-03T13:00 session-summary] signal: Kiro hook-schema drift — non-canonical fields (workspaceFolderName, shortName) cause the loader to misclassify a hook as a spec; diff against working siblings is the fastest diagnostic. | source: this-session | proposed: kiro-hook-schema-troubleshooting
[2026-05-03T06:15 session-summary] signal: Internal-vs-external infra decisions for small-scale agent workloads should start with "who already runs this for my team?" (ABMA sandbox + QuickSuite) before scoping a build — the replace-external framing is usually wrong; the real leverage is teammate self-serve, not eliminating the external dep. | source: this-session | proposed: enrich: ps-analytics-backend-options
[2026-05-03T06:17 session-summary] signal: Before recommending a ticket/access-request, enumerate the user's existing LDAP/team memberships — "what can you already do today?" is a materially different question from "what would you need access for?" and the first-draft answer was wrong because I skipped the enumeration step. | source: this-session | proposed: enrich: ps-analytics-backend-options
[2026-05-03T13:25 session-summary] signal: DevSpaces container can't reach ABDAI Redshift VPC via TCP — the `ada + DuckDB` path works for auth but not network, meaning agent-side hooks must stay on MotherDuck even when teammate-facing surfaces move to Redshift; this is a correctness boundary not a weakness, and the migration decision split is "agents = MotherDuck, humans = Hubble/QuickSuite" rather than "everything moves." | source: this-session | proposed: enrich: ps-analytics-backend-options
[2026-05-03T13:45 session-summary] signal: Asana registry stale-GID detection (AU/MX archived projects returning 424) should be a Phase 0 check in am-backend, not a mid-Phase-1 failure — schema drift handling protocol needs proactive probe before execution | source: this-session | proposed: enrich: asana-schema-drift-handling (likely new slug, no existing article)
[2026-05-03T22:45 session-summary] signal: Redshift client-side architecture — "postgres wire protocol + IAM-minted password" (what DuckDB postgres extension does) looks like it should work but fails BDT Shepherd audit because it doesn't federate SDO identity; the correct path is Redshift JDBC driver with groupFederation=true, OR Redshift Data API for programmatic clients. This pattern matters because it's easy to stand up the wrong thing and get a Shepherd ticket 10 days later. | source: this-session | proposed: new: redshift-client-path-selection
[2026-05-03T16:55 session-summary] signal: ABDAI `Redshift_Person_SDO_Identity_Access_Role` has ONLY `redshift:GetClusterCredentialsWithIAM` — not `GetClusterCredentials` (no WithIAM) and not `redshift-data:ExecuteStatement` — which means only specific IAM-federated JDBC paths work; Data API, default `redshift_connector(iam=True)`, and older postgres-style IAM clients all AccessDenied. This is the canonical compatibility matrix any future agent/person integrating with ABDAI Redshift needs up front. | source: this-session | proposed: enrich: ps-analytics-backend-options
