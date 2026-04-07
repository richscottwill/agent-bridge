# Proposed: shared/wiki/ Structure

## Directory Layout

```
shared/wiki/
├── strategy/              ← Strategic docs (POVs, frameworks, vision)
│   ├── testing-approach-kate.md
│   ├── aeo-ai-overviews-pov.md
│   ├── agentic-ps-vision.md
│   ├── five-year-outlook.md
│   ├── ieccp-planning-framework.md
│   ├── agent-architecture.md
│   └── ...
│
├── testing/               ← Test designs, workstreams, methodologies
│   ├── workstream-algorithmic-ads.md
│   ├── workstream-user-experience.md
│   ├── workstream-modern-search.md
│   ├── workstream-oci-bidding.md
│   ├── ad-copy-testing-framework.md
│   ├── ai-max-test-design.md
│   └── ...
│
├── markets/               ← Market wikis, references, playbooks
│   ├── au-market-wiki.md
│   ├── mx-market-wiki.md
│   ├── market-reference.md
│   ├── cross-market-playbook.md
│   └── ...
│
├── operations/            ← Playbooks, guides, processes
│   ├── oci-rollout-playbook.md
│   ├── oci-execution-guide.md
│   ├── invoice-po-process-guide.md
│   ├── landing-page-testing-playbook.md
│   ├── stakeholder-comms-guide.md
│   └── ...
│
├── reporting/             ← WBR guides, dashboards, callout guides
│   ├── wbr-callout-guide.md
│   ├── au-keyword-cpa-dashboard.md
│   └── ...
│
├── callouts/              ← Weekly market callouts (high volume, 101 files)
│   ├── au/
│   ├── mx/
│   ├── us/
│   ├── ca/
│   ├── jp/
│   ├── uk/
│   ├── de/
│   ├── fr/
│   ├── it/
│   ├── es/
│   └── ww/
│
├── meetings/              ← Meeting notes and series files
│   ├── brandon-sync.md
│   ├── deep-dive-debate.md
│   └── ...
│
├── research/              ← Research briefs, data gathering, analysis
│   ├── five-year-outlook-research-brief.md
│   ├── kate-doc-team-map-research.md
│   └── ...
│
├── reviews/               ← Critic evaluations (ephemeral, clean up periodically)
│   ├── kate-doc-final-review.md
│   └── ...
│
├── archive/               ← Superseded versions, old drafts
│   └── ...
│
└── _meta/                 ← Wiki pipeline config, index, health
    ├── wiki-index.md
    ├── wiki-structure.md
    ├── wiki-pipeline-rules.md
    └── context-catalog.md
```

## What Does NOT Move to shared/wiki/

These stay in shared/context/ because they're system infrastructure, not publishable content:

| What | Stays at | Why |
|------|----------|-----|
| Body organs | shared/context/body/ | Agent runtime config, not content |
| Protocols | shared/context/active/ | Agent behavior rules |
| Experiments | shared/context/experiments/ | Karpathy experiment variants |
| Intake | shared/context/intake/ | Temporary processing queue |
| Portable body | shared/portable-body/ | Bridge export (generated) |

## DuckDB Integration

The `duck_id` prefix maps directly to the directory:

| duck_id prefix | Directory | DuckDB category |
|---------------|-----------|-----------------|
| strategy-* | shared/wiki/strategy/ | strategy |
| testing-* | shared/wiki/testing/ | testing |
| program-* or market-* | shared/wiki/markets/ | program |
| ops-* | shared/wiki/operations/ | ops |
| reporting-* | shared/wiki/reporting/ | ops/reporting |
| callout-* | shared/wiki/callouts/{market}/ | ops/callout |
| meeting-* | shared/wiki/meetings/ | ops/meeting |
| research-* | shared/wiki/research/ | research |
| wiki-review-* | shared/wiki/reviews/ | wiki/review |
| wiki-archive-* | shared/wiki/archive/ | wiki/archive |

Query pattern:
```sql
-- Find all strategy docs
SELECT * FROM ps_analytics.docs.documents WHERE canonical_path LIKE 'shared/wiki/strategy/%';

-- Same thing via duck_id
SELECT * FROM ps_analytics.docs.documents WHERE duck_id LIKE 'strategy-%';
```

## Migration Summary

| Source | Destination | File count |
|--------|------------|------------|
| shared/artifacts/strategy/ | shared/wiki/strategy/ | 13 |
| shared/artifacts/testing/ | shared/wiki/testing/ | 24 |
| shared/artifacts/program-details/ | shared/wiki/markets/ | 11 |
| shared/artifacts/best-practices/ | shared/wiki/operations/ | 3 |
| shared/artifacts/communication/ | shared/wiki/operations/ | 4 |
| shared/artifacts/reporting/ | shared/wiki/reporting/ | 3 |
| shared/artifacts/tools/ | shared/wiki/operations/ | 2 |
| shared/artifacts/grok-swarm/ | shared/wiki/strategy/ | 5 |
| shared/context/wiki/staging/ | shared/wiki/{by topic}/ | 7 |
| shared/context/wiki/reviews/ | shared/wiki/reviews/ | 55 |
| shared/context/wiki/research/ | shared/wiki/research/ | ~10 |
| shared/context/wiki/archive/ | shared/wiki/archive/ | 3 |
| shared/context/active/callouts/ | shared/wiki/callouts/ | 101 |
| shared/context/meetings/ | shared/wiki/meetings/ | 21 |
| shared/research/ | shared/wiki/research/ | ~10 |

## What Gets Deleted After Migration

| Path | Reason |
|------|--------|
| ~/wiki/ | Empty ghost directory |
| ~/artifacts/ | Git repo mirror (bridge-sync will read from shared/wiki/) |
| ~/portable-body/ | Cache recovery copy |
| shared/artifacts/ | Replaced by shared/wiki/ |
| shared/context/wiki/ | Replaced by shared/wiki/ |
| shared/context/meetings/ | Moved to shared/wiki/meetings/ |
| shared/context/active/callouts/ | Moved to shared/wiki/callouts/ |
