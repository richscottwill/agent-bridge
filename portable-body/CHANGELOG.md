# Changelog

All notable changes to the portable body system.

Format: [Common Changelog](https://common-changelog.org/)

---

## [1.1.0] — 2026-03-31

### Added
- body-diagram.md — Mermaid visual architecture of the entire body system
- architecture-eval-protocol.md — blind evaluation protocol for architecture changes
- 7 new spec sets (agent-consolidation, agentspaces-desktop-launcher, attention-tracker, bayesian-prediction-engine, data-layer-overhaul, shared-directory-reorg, wiki-sharepoint-sync) — 19 spec files total now
- 7 new tool files: schema.sql, query.py, RECONSTRUCTION.md (DuckDB data layer), sync.sh + git-sync-README.md (git sync), generate-charts.py + chart-template.html + progress-charts-README.md (dashboard charts)
- 2 new hooks documented: WBR Callout Pipeline (#4), Portable Body Sync (#10)

### Changed
- 10 body organs updated (brain, device, eyes, gut, hands, heart, memory, nervous-system, spine, soul) — only amcc and body.md unchanged since v1.0.0
- 3 agents updated (eyes-chart, karpathy, portable-body-maintainer)
- Agent consolidation: removed 6 per-region agents (abix-analyst, abix-callout-writer, eu5-analyst, eu5-callout-writer, najp-analyst, najp-callout-writer), replaced with 2 parameterized agents (market-analyst, callout-writer) + updated callout-reviewer. Net: 17 → 13 agents.
- callout-principles.md updated
- ingest.py (dashboard ingester) updated
- hooks-inventory.md expanded from 8 to 10 hooks with richer detail

### Removed
- 6 per-region WBR agents (replaced by consolidated parameterized agents)

### System State at Sync
- Total files: 87 (up from 62)
- Agent count: 13 (down from 17 — consolidation)
- Spec count: 22 files across 8 specs (up from 3 files / 1 spec)
- Tool count: 9 files (up from 1)
- morning-routine-experiments.md: source file no longer exists at original path; portable copy retained as last known version

### Portability Gaps Flagged
- Same as v1.0.0 (CE-6 still queued): file paths are AgentSpaces-specific, hooks are Kiro JSON, some organs reference MCP tools
- morning-routine-experiments.md has no living source — may be stale. Flag for review.
- New tools (query.py, schema.sql) reference DuckDB which is environment-specific infrastructure

---

## [1.0.0] — 2026-03-27

Initial full build of the portable body. Previous syncs existed but the directory was lost. This is a complete rebuild from all living source files post-Run 13.

### Added
- 12 body organ files (body, soul, brain, eyes, hands, memory, spine, heart, device, nervous-system, amcc, gut)
- 6 voice files (core writing style + email, slack, docs, wbr, mbr)
- 5 steering files (trainer, task prioritization, morning routine experiments, callout principles, long-term goals)
- 17 agent definitions (4 body-system, 7 wbr-callouts, 6 wiki-team)
- 8 hooks documented in plain-text inventory (hooks-inventory.md)
- 4 research files + 7 test-docs + 2 automation-impact files
- 1 tool (dashboard ingester)
- 3 spec files (paid-search-daily-audit)
- portable-layer.md manifest
- README.md with architecture, file inventory, bootstrap protocol
- CHANGELOG.md (this file)
- SANITIZE.md with stripping guidance

### System State at Sync
- Autoresearch loop: Run 13 completed (all 9 organs updated)
- Total body words: ~19,500w / 24,000w ceiling
- Experiments: CE-1 through CE-4 adopted, CE-5 applied, CE-6/CE-7 queued
- No Karpathy experiments this week (CE-6 skipped due to per-organ cooldown)
- aMCC streak: 0 days (8 workdays since hard thing set)
- Hard thing: Testing Approach doc for Kate (Apr 16)
- Key events this week: Annual Review shared (3/24), Agent Bridge built (3/27), Flash sections written (3/27), Polaris weblab scoping started (3/27)

### Portability Gaps Flagged
- File paths are AgentSpaces-specific (~/shared/context/, ~/.kiro/steering/)
- Hook definitions are Kiro JSON format (plain-text equivalents in hooks-inventory.md)
- Some organs reference MCP tools without generic alternatives
- CE-6 (Cross-Environment Prompt Portability) is queued to address these
