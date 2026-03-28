# Changelog

All notable changes to the portable body system.

Format: [Common Changelog](https://common-changelog.org/)

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
