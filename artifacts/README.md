# Artifacts

Strategic work product. Organized by type. If it's a doc, framework, test design, POV, or playbook — it lives here.

This is the Level 1 evidence folder. Every file here is proof of an artifact shipped.

## Structure

```
artifacts/
├── testing/          — Test designs, methodologies, experiment frameworks
├── strategy/         — POVs, playbooks, strategic narratives, OP1 docs
├── reporting/        — Dashboards, analysis docs, performance summaries
├── tools/            — Automation specs, tool designs, process docs
├── communication/    — Stakeholder docs, handoff guides, knowledge-sharing artifacts
├── program-details/  — Wiki-style program documentation, campaign structures, account details
├── best-practices/   — Operational standards, how-tos, reusable frameworks
└── SITEMAP.md        — Full directory index (wiki-style, flat navigation)
```

## Document Standard

Every artifact MUST have this front-matter block:

```
---
title: [Document title]
status: DRAFT | REVIEW | FINAL
audience: amazon-internal | personal | agent-only
  amazon-internal = shareable with team, stakeholders, leadership
  personal = Richard's working docs, not for distribution
  agent-only = system context the agent uses, not human-facing
level: [1-5 or N/A] (which Five Level does this advance?)
owner: [who maintains this doc]
created: YYYY-MM-DD
updated: YYYY-MM-DD
update-trigger: [what context change should trigger a refresh]
---
```

Every artifact MUST end with:

```
## Sources
- [fact] — source: [file path, email thread, meeting, Quip doc, date]
```

## Rules
- One artifact per file. Name it: `YYYY-MM-DD-short-description.md`
- Drafts are fine — ship ugly, refine later.
- When an artifact ships, log it in the weekly scorecard (rw-tracker.md).
- The morning routine checks this folder to track Level 1 progress.
- When a source organ or context file changes, check if dependent artifacts need updating.

## Audience Guide

| Tag | Meaning | Can Share With |
|-----|---------|---------------|
| amazon-internal | Professional doc for Amazon audience | Team, stakeholders, leadership, cross-functional partners |
| personal | Richard's working notes, analysis, personal frameworks | Richard only |
| agent-only | System context for the AI agent | Not human-facing — agent reads this to maintain artifacts |

## Staleness Rule
Every doc has an `update-trigger` field. When that trigger fires (e.g., "new OCI market launches" or "weekly dashboard data refreshed"), the artifact is flagged for update. The morning routine or loop can check this.
