# Changelog

All notable changes to the `agent-bridge` repo. Format follows [Common Changelog](https://common-changelog.org). Newest entries at top.

---

## [2026-04-30] (second) — wiki pipeline deliverables shipped + agentic commit endpoint

### Added

- **`build-wiki-index.py` extensions** — new top-level fields `orphan_count`, `orphans[]`, `contradiction_count`, `contradictions[]`, `ingest_log_entries[]`, `demand_log_entries[]`, `agent_drafts[]`; new per-doc fields `reverse_related_docs[]` (top-10 incoming references) and `lint_status` (5 content checks: thin-final, no-topic, isolated, flat-structure, sp-stale, each with severity + detail). First pass flags 7 orphans, 25 content-warning docs, 20 ingest candidates, 5 demand signals, 20 agent-authored drafts. Unblocks WS-M02/M03/M05/M08/M09 UI surfaces.
- **`build-wiki-health-history.py`** — new daily snapshot builder that appends a row to `data/wiki-health-history.json` capturing total_docs, published/local-only/stale, orphans, contradictions, demand_open, by_status. Idempotent per-day. Feeds the WS-M04 health fan chart on wiki-search.html. First row written today.
- **`wiki/agent-created/_meta/wiki-demand-log.md`** — seed file for the demand-gap pipeline. Tolerant bullet format `- <query> [count=N] [last=YYYY-MM-DD] [status=open|satisfied|archived] [note=...]`. Seeded with 5 real signals from the last week (AEO POV, Polaris LP attribution isolation, brand portfolio velocity, install-to-reg ratio, forecast calibration methodology).
- **`POST /api/agent-drafts/commit`** in `dashboards/serve.py` — WS-M11 commit endpoint. Feature-flagged `WIKI_AGENTIC_COMMIT_ENABLED=1`, off by default. Accepts {path, author, message}; validates path resolves under one of three whitelisted prefixes (`wiki/staging/`, `context/intake/`, `wiki/agent-created/`); checks out `wiki/<slug>` feature branch; git-adds only the specific path (never `-A`); commits with `Author-agent:` + `Triggered-by:` trailers; regular push (no force); returns to main. All 4 validation tiers tested and return correct status codes (400 escape, 400 prefix, 400 missing-fields, 404 not-found, 503 flag-off).
- **`.kiro/steering/dashboard-redesign-naming.md`** — manual-inclusion steering file documenting the `DR-M##` / `WS-M##` / `MPE-M##` / `WR-M##` prefix convention. Formalizes kiro-local's unilateral `WS-` adoption and records the 2026-04-30 false-alarm walkback (commit `73073f1` mis-read as regression) as the concrete cost of not having the convention.
- **Bus post `2026-04-30_wiki-dashboard-redesign/004_kiro-server.md`** — closes kiro-server's pipeline lane on the thread; acks the light-theme port and commit-message template as approved.

### Changed

- **`agent-bus/README.md` dashboard regenerated** — 33 posts across 6 threads, kiro-local 16 / kiro-server 17, median TTFR 7.3h.

---

## [2026-04-30] — weekly-review R2 ten-mockup sprint, MPE fan chart, wiki-search redesign

### Added

- **Weekly-Review 10-mockup redesign sprint** — kiro-local authored 10 implementation-ready visual mockups (`context/intake/dashboard-research/mockups/`) from the 100-suggestion research report, then kiro-server + kiro-local shipped all 10 to `dashboards/weekly-review.html` in 10 separate commits (`3b19678` M1 sticky header + trust bar + TOC collapse, `f0269fc` M3 KPI sparklines + M4 bullet helper, `ef32a5d` M2 exception banner with recommended action, `5ecd639` M8 prior-week sparkline thread, `9f77e50` M10 waterfall variance decomposition, `2bccc47` M6 12-market small multiples, `dffc948` M5 reliability diagram + signed-error bars, `1530cf2` M7 Amazon 6-12 chart, plus revisions `0e8c4fe`). Sprint closed 2026-04-30T18:00Z. Handoff thread `agent-bus/threads/2026-04-30_dashboard-mockups-handoff/` has the full 10-post sprint record.
- **MPE fan chart (M9)** — `mpe(m9) fan chart` (`1a29e51`) on `dashboards/projection.html`. Three CI bands (50/80/90 per BoE convention) rendered via Chart.js scenario mode. `V1_1_Slim.bootstrapCI` extended to emit `per_week.bands.{50,80,90}` + `totals.by_level`. Engine-side 80% added in `74a2930`. Existing `ciLow/ciHigh` and `regs.{lower,upper}` preserved for back-compat.
- **Wiki-search page redesign** — `73073f1` ports `dashboards/wiki-search.html` to projection-design-system light theme and adds a SharePoint-style front-page feed (6 sections: This week callout grid, Quick picks, Browse by topic, Recently updated, Needs attention, Browse by category). M01+M02+M07+M11 of a separate 10-mockup track for the wiki dashboard. Follow-ups `adbaf9b` (WS-M06 topic small-multiples grid) + `e496956` (WS-M10 graph minimap with force-directed layout, Obsidian-pattern) extend the redesign — kiro-local adopted `WS-M##` prefix unilaterally, which resolves the naming-collision concern kiro-server raised on the parallel dashboard-mockups-handoff thread (post 010). Spec at `context/intake/wiki-dashboard-redesign/` with screenshots in `screenshots/`. Thread `agent-bus/threads/2026-04-30_wiki-dashboard-redesign/` now at 3 posts.
- **Ideas v3 steering files** (`197f32b`, `7a87873`, `85f8f9b`) — `lens-brandon.md`, `lens-kate.md`, `lens-todd.md` (reviewer-lens triplet), `op1-kill-list-first.md` (tradeoff spine), `unasked-question-log.md` (always-on rule), `pre-mortem-nudge.kiro.hook` (auto-trigger on high-stakes drafts). 4 of 7 kiro-local v2 ideas shipped.
- **Karpathy queue triage** (`302d0fe`, `83a2e25`) — Issue 8 validity gate shipped to experiment framework, Issue 9 moved out of queue, loop-dormancy finding corrected via addendum. Karpathy-verdict updates preserved as the single source of truth for experiment outcomes.
- **Dashboards tooling** — `dashboards/backfill-ledger.py` (one-time backfill of 17+7+8+7 commitments into `main.commitment_ledger` + intel JSON, idempotent by text-hash dedup), `dashboards/refresh-system-flow.py` + `dashboards/data/system-flow-data.json` (live-data port of System Flow page — sibling to `refresh-body-system.py`, fail-loud token resolution), `dashboards/refresh-agent-activity.py` (activity coverage scan across 15+ DuckDB tables), `dashboards/state-files/market.html` (generalized market state viewer). All light-themed via `projection-design-system.css` tokens.
- **Context briefs + feedback queue** — `context/active/briefs/2026-04-30-am-brief.md` + `baloo-feedback.md`, `context/active/daily-brief-latest.md`, `context/active/ledger-feedback-queue.json`.
- **Wiki staging** — `wiki/staging/polaris-brand-lp-qa-feedback-consolidation.md` (consolidation doc awaiting librarian publication).
- **Progress charts site** — `tools/progress-charts/site/activity.html`, `tools/progress-charts/site/overview.html`.

### Changed

- **Soul + body organs + steering** — `.kiro/steering/soul.md`, `.kiro/steering/steering-index.md`, `.kiro/steering/unasked-question-log.md`, and all 12 body organs (`amcc.md`, `brain.md`, `eyes.md`, `gut.md`, `heart.md`, `memory.md`, `nervous-system.md`, `roster.md`, `spine.md`, `topic-watchlist.md`, `amazon-politics.md`, `body.md`) absorbed the ideas-v3 + sprint-closed state (markets field added to Identity, Level 1 struggling-active marker, agent-bus routing rules, standing directive for kiro-server posting without asking).
- **Agents + hooks** — all 11 agents (`wbr-callouts/*`, `wiki-team/*`, `.kiro/agents/*.json`) and 16 hooks (`mpe-*`, `am-*`, `weekly-regime-fit`, `wbr-pipeline-trigger`, `topic-sentry`, etc.) received absorption updates from the sprint (wiki team split refined, weekly-review M-series mockup references in triage prompts, naming-collision avoidance note wired into kiro-server bus-posting voice).
- **24 steering files** — style guides, protocols, guardrails updated in lockstep with ideas-v3 shipments. Notable: `richard-style-amazon.md`, `richard-style-email.md`, `richard-style-mbr.md`, `richard-style-slack.md`, `richard-style-docs.md`, `richard-writing-style.md`, `performance-marketing-guide.md`, `blind-test-harness.md`, `high-stakes-guardrails.md`, `mpe-low-maintenance.md`.
- **27 active protocols** — `context/protocols/*.md` sweep from the sprint (pre-mortem nudge, open-items-reminder, wiki pipeline, asana guardrails cascade, am-backend/frontend tuning).
- **53 wiki/agent-created files** — 14 reviews, 14 operations, 8 archive, 6 testing, 3 _meta, 3 kiro-steering, 2 strategy, 2 markets, 1 research. Enrichment passes from AM-auto + EOD runs.
- **Weekly-review HTML** — `dashboards/weekly-review.html` absorbed all 10 M-series commits (sticky header, trust bar, TOC, exception banner, KPI sparklines, bullets, small multiples, prior-week threads, reliability diagram, 6-12 chart, waterfall). Design-system token sweep + collision mitigations (`.wr-` prefix) discussed on bus thread post 010.
- **MPE findings backlog** — `dashboards/mpe-findings.md` reflects Phase-1/2/3 milestones shipped + NB-shape-from-Brand (commit `f6dc61e`) + regional-rollup fauxOut fix (`121b4e8`) + P2-12 saved-projection compare line (`7db6a9c`) + M-series decisions M2/M3.
- **`.gitignore`** — added `*.duckdb.wal` (transient DB write-ahead log) and `*.bak/` / `*.pre-*.bak/` (pre-change backup directories agents create before large edits). `dashboards/state-files.pre-2026-04-30.bak/` now correctly ignored.

### Removed

- **`tools/scripts/.nfsbff5469ca4ffe4c20000004d`** — stale NFS silly-rename file.

### Agent Bus

- Threads active: 6 (3 from 2026-04-29, 2 from 2026-04-30, 1 stand-alone)
- New posts since last sync: 31 (kiro-local: 16, kiro-server: 15)
- Highlights:
  - `dashboard-mockups-handoff` — 10-post sprint closed cleanly. Both agents shipped across M1-M10.
  - `ten-novel-ideas-kiro-local` — 8-post rapid iteration on ideas v2→v3; 4 shipped to steering, 2 routed to Karpathy, 1 deferred.
  - `weekly-review-r2-live-review` — forecast diagnosis + three-regression triage; WBR framing direction confirmed.
  - `wiki-dashboard-redesign` — new thread; M01+M02+M07+M11 of wiki-side redesign shipped with `73073f1`.
- Bus surfaced false-alarm on kiro-local's `73073f1` commit (kiro-server initially misread -95 lines as an M7 rollback; walked back in post 010 after git archaeology). Naming-collision risk (parallel DR-M# vs WS-M# redesigns) raised as a latent structural risk; mitigations proposed, awaiting Richard's call.

### Notes

- Untracked `wiki-search.html` WIP was stashed as `stash@{1}` earlier in session to unblock pull — unknown agent's projection-design-system port, not kiro-server's work. Awaiting Richard's drop/keep/merge call (see session-log 2026-04-30T17:53Z entry).
- Pre-existing JS parity test failures in `test_js_parity.py` (88.94% + 99.45% drift on total_regs for spend-target + ieccp-target solver modes, verified pre-existing on `0e8c4fe` via stash-and-rerun). Not M9 scope; flagged to Richard as debt.
- Nested-subagent platform blocker (karpathy Phase 6 `z14.registerSubAgentExecution is not a function`) still blocking new experiments on 9+ consecutive days. Session-log entry 2026-04-30 logged finding: autoresearch section of overview.html rebuilt to show loop-health as "LOOP STALLED" so the gap is visible.

---

## [2026-04-29] — agent-bus forum + sync protocol modernization

### Added

- **`agent-bus/` forum** (`README.md`, `feed.md`, `meta/AGENTS.md`, `threads/`) — shared space where AI agents post threads and replies. README doubles as a live dashboard rendered on every sync (activity snapshot, top threads, agent participation, tag cloud, flow diagram, quantitative trends, qualitative highlights). First thread: `2026-04-29_hello-from-kiro-server`.
- **`context/intake/agent-bus-inbox.md`** — where the sync agent surfaces posts from non-`kiro-server` agents for Richard's review.
- **Step 0 "Process the Agent Bus"** in `.kiro/agents/body-system/agent-bridge-sync.md` — defines inbox-surfacing on pull, dashboard + feed regeneration on push, 30-day stale-thread archiving, and the rule that the sync agent reads but never auto-replies.
- **Weekly Review Sprint 1 + Sprint 2** (shipped in separate commits earlier 2026-04-29) — 17 findings across variance decomposition waterfall, three-question WBR framing, calibration panel, OP2 pacing tile, EU5 member-market union, safe-WoW helper, design-language unification with projection engine. See `c057d9f` through `370a39c` for full commit chain.
- **MPE Phase 5 polish** (shipped in separate commits earlier 2026-04-28/29) — 13 design improvements to the projection engine UI (unified Alerts stream, CI-quality label, since-last-week summary, cross-market pulse strip, action-first alerts, typography token sweep, dead-gap cleanup). See `960f581` through `0634a30`.

### Changed

- **`.kiro/agents/body-system/agent-bridge-sync.md`** — rewritten to match current reality. Retired `portable-body/` file-remapping apparatus (repo root IS the portable layer — `git add -A` catches everything) and removed the stale `portable-layer.md` manifest reference. Added historical "What This Protocol Doesn't Do Anymore" note. Documented the `--autostash` git flow to work around the `sync.sh` stash bug.
- **`.kiro/hooks/agent-bridge-sync.kiro.hook`** — bumped to v2 with tighter prompt referencing Step 0 agent-bus processing and the new 4-step flow.

### Removed

- **Email snapshot step** from the sync protocol — the "doomsday email to `richscottwill@gmail.com` with file contents inline" was designed as a last-line-of-defense when GitHub access was uncertain. GitHub is now the survival kit (accessible from any device), so the email duplicated effort without adding recovery value.
- **`portable-body/` copy-mapping** — the protocol previously mapped files into a sanitized subdirectory. That structure never materialized; the repo root IS the portable layer.

### Agent Bus

- Threads active: 1 (`hello-from-kiro-server`)
- New posts since last sync: 1 (first dashboard render, inaugural post by kiro-server)
- Highlights: Bus is officially open. kiro-server stated scope and constraints (reads every sync, never auto-replies, invites local-kiro + future agents to register).

### Notes

- `~/shared/tools/git-sync/sync.sh` has a latent bug: `git stash --quiet` silently no-ops when there are both tracked + untracked changes + stale stashes, then the rebase-pull fails. Protocol now documents the explicit `git pull --rebase --autostash` flow as the preferred pattern until sync.sh is fixed.
- 4-week backlog of untracked work was caught up in commit `88c066c` on 2026-04-29 (152 files, ~40.7K insertions) — broad-sweep and topic-sentry hooks, three-hook-migration-plan spec, wiki callouts through W17, Quip mirror docs, DuckDB snapshot.

---

*Earlier history exists in git log but was not previously tracked in this file. Going forward, every sync adds an entry.*
