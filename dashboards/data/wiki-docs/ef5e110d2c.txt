# Wiki Review Queue

Drafts awaiting wiki-critic review. The critic reads this queue, scores pending drafts on the 5-dimension rubric, and flips status to REVIEW on approval or signals revision via `_meta/revision-queue.md`.

Format: `- [ ] {slug} — drafted YYYY-MM-DD — awaiting wiki-critic`

---

## Batch drafted 2026-04-17 — post-consolidation state

After the 2026-04-17 consolidation pass, the 24 new drafts plus overlapping legacy files were merged into 18 canonical program/topic documents. The list below reflects the canonical slugs only.

### Program docs (merged from multiple sources)

- [ ] liveramp-program — drafted 2026-04-17 — awaiting wiki-critic (merged from liveramp-identity-primer, enhanced-match-liveramp-explainer, enhanced-match-liveramp)
- [ ] f90-program — drafted 2026-04-17 — awaiting wiki-critic (merged from f90-lifecycle-strategy, f90-rollout-state)
- [ ] polaris-program — drafted 2026-04-17 — awaiting wiki-critic (merged from polaris-rollout-status, polaris-rollout-timeline × 2)
- [ ] oci-program — drafted 2026-04-17 — awaiting wiki-critic (merged from oci-business-case, oci-execution-guide, oci-implementation-guide, oci-rollout-playbook, oci-rollout-methodology, workstream-oci-bidding, oci-playbook-rewrite, oci-methodology-knowledge-share, oci-performance)
- [ ] forecast-system — drafted 2026-04-17 — awaiting wiki-critic (merged from forecast-model-multi-signal-blend, forecast-reconciliation-checks)
- [ ] grok-swarm — drafted 2026-04-17 — awaiting wiki-critic (merged from 01-grok-synthesizer, 02-the-director, 03-the-questioner, 04-the-operator, 05-the-engineer)

### Standalone drafts (new from context scan)

- [ ] ai-tool-wbr-callout-workflow — drafted 2026-04-17 — awaiting wiki-critic
- [ ] market-expansion-playbook — drafted 2026-04-17 — awaiting wiki-critic
- [ ] op1-2027-innovation-shortlist — drafted 2026-04-17 — awaiting wiki-critic
- [ ] baloo-ref-tag-attribution-risk — drafted 2026-04-17 — awaiting wiki-critic
- [ ] sid-acquisition-funnel-map — drafted 2026-04-17 — awaiting wiki-critic
- [ ] cpc-benchmark-defense-playbook — drafted 2026-04-17 — awaiting wiki-critic
- [ ] mie-marketing-intelligent-engine — drafted 2026-04-17 — awaiting wiki-critic
- [ ] negative-keyword-ownership-model — drafted 2026-04-17 — awaiting wiki-critic
- [ ] paid-app-attribution-debate — drafted 2026-04-17 — awaiting wiki-critic
- [ ] on-site-placement-catalog — drafted 2026-04-17 — awaiting wiki-critic
- [ ] sharepoint-quip-deprecation-migration — drafted 2026-04-17 — awaiting wiki-critic
- [ ] op1-op2-vocabulary-guide — drafted 2026-04-17 — awaiting wiki-critic
- [ ] kiro-cli-pretooluse-hook-bug — drafted 2026-04-17 — awaiting wiki-critic
- [ ] austin-offsite-strategic-readouts — drafted 2026-04-17 — awaiting wiki-critic
- [ ] meeting-ingestion-pipeline — drafted 2026-04-17 — awaiting wiki-critic
- [ ] quiet-worker-antipattern — drafted 2026-04-17 — awaiting wiki-critic
- [ ] scope-defense-playbook — drafted 2026-04-17 — awaiting wiki-critic

### Folded in (no separate review needed)

- google-summit-ai-max-learnings → absorbed into ai-max-test-design.md as "Google Summit Readout" section

### Pre-existing canonical docs touched by consolidation (no re-review needed unless content changed)

- au-market-wiki (gained Related section)
- mx-market-wiki (gained Related section)
- project-baloo-overview (gained Related section)
- workstream-algorithmic-ads (gained Related section)
- workstream-user-experience (gained Related section)
- ww-testing-tracker (gained Related program references section)
- testing-approach-kate-v5 (gained Related program references section)
- ai-max-test-design (gained Google Summit Readout section + Related section)


---

## Proposals added 2026-04-17 — wiki-maintenance W16 run

Top 5 candidates surfaced by the W16 maintenance run. All come from DuckDB `signals.wiki_candidates` (multi-channel signal strength) except the last, which came from the hook-contribution queue.

- [ ] **polaris-program (enrich)** — quality 20.5, 6 mentions, 3 channels over 9.8 days. Signal: Polaris Brand LP rollout is hottest trending topic. Article exists but pre-dates recent Slack/hedy discussion. Action: wiki-editor assigns enrichment — pull last 7 days of polaris-brand-lp Slack thread + April hedy meetings.
  - **2026-04-17 evening follow-up:** Reviewed signals. Fresh 4/16 signal is "Thursday DDD alignment, WW template changes, Richard owes feedback" — that's a task-manager item, not article content. The substantive 4/8 Brandon/Dwayne feedback-consolidation signals are already reflected in the Decision Log (4/14 + 4/16 entries) and the current article (updated 2026-04-17) is comprehensive through the MCS migration decision. **Disposition: skip enrichment this week**. Article is fresh. The DDD-alignment follow-up belongs in Asana/current.md, not the wiki. Keep proposal P2 for the next weekly run if a new substantive signal lands.

- [ ] **ieccp-planning-framework + mx-market-wiki (cross-link + enrich)** — quality 13.5, 3 mentions, 2 channels. Signal: MX budget/ie%CCP conversations clustering in hedy (Kate sync) + ab-paid-search-abix. Action: enrich mx-market-wiki's budget section; add backlink from ieccp-planning-framework.

- [ ] **oci-program (enrich)** — quality 11.5, 3 mentions, 2 channels. Signal: OCI rollout still trending despite being one of the oldest topics. Action: verify all FR/IT/ES/JP status markers reflect 100% rollout per audit 4/4 note; pull any recent OCI learnings from slack + hedy.
  - **2026-04-17 evening follow-up: CA row updated.** The article had CA as "April 7, 2026 On track for launch" but Brandon signals from 4/16 (ab-paid-search-oci channel + slack thread with Mukesh) show CA launch is targeted for week of April 20 — MCM readiness confirmed but the Austin offsite pushed execution out. Updated the market status table row to reflect new targeted date + coordination state. No other rollout-table changes needed (FR/IT/ES/JP already correct at 100% per 3/28 updates). **Disposition: factual update only; no full rewrite warranted.**

- [ ] **au-market-wiki (enrich CPA/CVR section)** — quality 9.5, 2 mentions, 2 channels. Signal: AU CPA/CVR conversations recurring. Action: add or strengthen CPA/CVR performance section; cross-link au-keyword-cpa-dashboard.

- [ ] **paid-app-attribution-debate (enrich) OR new `pam-budget-availability`** — quality 6.0, 1 channel, 1 mention (Brandon signal from 4/16). Signal: PAM Budget Availability flagged as top priority in AM-Auto brief. Action: either absorb into existing paid-app-attribution-debate article under a "Budget context" section, OR draft a tactical doc if Brandon's @mention turns into a sustained thread. P2 — wait one more signal before drafting new.

## Proposals added 2026-04-17 — hook-contribution candidate (P3)

- [ ] **distributed-contribution-hook-pattern (new)** — source: session-summary hook, 2026-04-17T18:16. Signal: the hook-observe + central-consume pattern itself merits documentation. Audience would be agent + personal. Low priority: this is meta-infrastructure, not paid-search content. Could fold into agent-architecture.md as a new section instead of a standalone article. Defer — not worth a dedicated doc unless the pattern expands to more than 4 contributing hooks.

## Proposals added 2026-04-17 (evening run) — hook-contribution cluster

- [x] **agent-architecture (enrich)** — **DISPATCHED 2026-04-17 evening.** Added 2 new sections to `strategy/agent-architecture.md`: "Agent Operating Norms" (4 norms: sensible defaults, caution-as-procrastination, act-on-reversible-in-context, silent-when-clean) and "Wiki System Topology" (three-surface architecture, crawler-authoritative, cache-and-derive pattern). Updated `updated:` field to 2026-04-17, added 3 tags (operating-norms, wiki-topology, cache-and-derive), added 2 entries to Sources list, refreshed AGENT_CONTEXT machine_summary + key_entities + update_triggers. Made local copy newer than SharePoint → now flagged as 1 published-stale in dashboard (expected signal, queues SharePoint re-push). Signals consumed: 4 from session-summary hook (2026-04-17T18:32/18:42/18:44/18:58).

## Actions for Richard

- ~~Confirm which of the 5 signal-driven enrichments to prioritize for next week's wiki-team runs~~ — **executed inline on 2026-04-17 evening.** Polaris: skipped (article fresh). OCI: factual CA-row update applied. Agent-architecture: full enrichment applied (2 new sections). Remaining P2 proposals (mx-budget-ieccp cross-link, au-cpa-cvr, PAM budget) stay in queue for next weekly run; they have lower quality scores and no urgent factual errors to fix.
- ~~Decide: absorb distributed-contribution-hook-pattern into agent-architecture~~ — **DONE as part of the agent-architecture enrichment above.**
- Separately: the morning maintenance run surfaced 46-article index drift and 0% blackboard adoption. See health-2026-04-17.md + audit-2026-04-17.md (morning) and -run2.md files (evening). Index drift is now fixed (82 indexed, 0 orphans). Blackboard still at 0% — track to 4/30 build-start check.
- ~~Low priority: 9 legacy `~/shared/artifacts/*` cross-refs need a systematic swap-pass~~ — **DONE.** 9 refs fixed across 6 files. Post-edit broken-ref count: 0.
- New: 1 SharePoint-stale doc after agent-architecture enrichment (local newer than SP copy). Will be picked up by the next sharepoint-sync run; no immediate action needed.
