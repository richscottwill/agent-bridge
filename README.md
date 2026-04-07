# Richard Williams — Personal Operating System

AI-augmented work system for Amazon Business Paid Search. Text files + DuckDB registry that let any AI platform understand how Richard thinks, works, and operates.

## Quick Start

1. Read `context/body/body.md` — maps the whole system
2. Read `context/body/spine.md` — bootstrap sequence and key IDs
3. Query `ps_analytics.docs.documents` in MotherDuck — the document registry

## Structure

| Directory | Purpose |
|-----------|---------|
| `wiki/` | All publishable content — strategy, testing, markets, operations, reporting, callouts, meetings, research, reviews, archive |
| `context/` | Agent infrastructure — body organs, protocols, active state, experiments, intake |
| `tools/` | Automation scripts — asana, comms, bridge, prediction, data, sharepoint-sync |
| `data/` | DuckDB databases, exports, processed data, state files |
| `uploads/` | Human drop zone — sheets, changelogs, docs |
| `dashboards/` | HTML dashboards (Dives live in MotherDuck) |
| `.kiro/` | Agents, hooks, specs, steering, skills, settings |

## Document Registry

Every document has a `duck_id` (searchable slug) and a `<!-- DOC-XXXX | duck_id: slug -->` stamp on line 1.

```sql
-- Find a document
SELECT duck_id, title, canonical_path, stage
FROM ps_analytics.docs.documents
WHERE duck_id ILIKE '%keyword%';
```

## Key Files

| File | What |
|------|------|
| `context/body/body.md` | System navigation map |
| `context/body/brain.md` | Strategy, Five Levels, priorities |
| `context/body/amcc.md` | Coaching, streak, hard thing |
| `context/body/spine.md` | Bootstrap, tool access, key IDs |
| `context/active/asana-command-center.md` | Asana task management protocol |
| `wiki/testing/testing-approach-kate-v5.md` | Kate testing doc (staged) |
| `wiki/strategy/agent-architecture.md` | Agent system architecture |
| `wiki/strategy/five-year-outlook-v2.md` | PS five-year outlook |

## MotherDuck

Database: `ps_analytics` on MotherDuck. Key schemas:
- `ps` — paid search metrics, forecasts, projections, pacing
- `docs` — document registry (duck_id, canonical paths, stages)
- `asana` — task sync, daily tracker
- `signals` — Slack, email ingestion
- `karpathy` — autoresearch experiments

Dives (interactive dashboards):
- PS Forecast Tracker — cumulative actuals vs predictions with CI bands
- PS Team Testing Dashboard — 24 tests across 10 markets
- Karpathy Autoresearch Lab — Bayesian experiment dashboard
- Monday Command Center — daily work dashboard
