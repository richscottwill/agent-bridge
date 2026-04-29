---
inclusion: auto
---

# Document Registry Protocol

All documents are tracked in MotherDuck at `ps_analytics.docs`. Every file has a `<!-- DOC-XXXX | duck_id: slug -->` stamp on line 1. The `duck_id` is a descriptive, searchable slug — guess it from the topic.

## Document Home: shared/wiki/

All publishable content lives in `shared/wiki/` organized by topic:
- `shared/wiki/strategy/` — POVs, frameworks, vision docs
- `shared/wiki/testing/` — test designs, workstreams, methodologies
- `shared/wiki/markets/` — market wikis, references
- `shared/wiki/operations/` — playbooks, guides, processes
- `shared/wiki/reporting/` — WBR guides, dashboards
- `shared/wiki/callouts/{market}/` — weekly market callouts
- `shared/wiki/meetings/` — meeting notes
- `shared/wiki/research/` — research briefs
- `shared/wiki/reviews/` — critic evaluations (ephemeral)
- `shared/wiki/archive/` — superseded versions

System files stay in `shared/context/` (organs, protocols, experiments, intake).

## Quick Reference — Key Documents

| duck_id | What | Path |
|---------|------|------|
| wiki-testing-approach-kate | Kate testing doc | shared/wiki/testing/testing-approach-kate-v5.md |
| organ-brain | Brain (strategy) | shared/context/body/brain.md |
| organ-amcc | aMCC (coaching) | shared/context/body/amcc.md |
| protocol-asana-command-center | Asana command center | shared/context/active/asana-command-center.md |
| strategy-aeo-ai-overviews-pov | AEO POV | shared/wiki/strategy/2026-03-25-aeo-ai-overviews-pov.md |
| program-au-market-wiki | AU market wiki | shared/wiki/markets/2026-04-04-au-market-wiki.md |
| program-mx-market-wiki | MX market wiki | shared/wiki/markets/2026-03-25-mx-market-wiki.md |

## Searching the Registry

The `duck_id` is designed to be guessable. Pattern: `category-topic-detail`.

```sql
-- Just guess the duck_id:
SELECT * FROM ps_analytics.docs.documents WHERE duck_id ILIKE '%kate%';
SELECT * FROM ps_analytics.docs.documents WHERE duck_id ILIKE '%organ%';
SELECT * FROM ps_analytics.docs.documents WHERE duck_id ILIKE '%oci%';

-- By category prefix:
SELECT * FROM ps_analytics.docs.canonical WHERE duck_id LIKE 'testing-%';
SELECT * FROM ps_analytics.docs.canonical WHERE duck_id LIKE 'organ-%';
SELECT * FROM ps_analytics.docs.canonical WHERE duck_id LIKE 'strategy-%';

-- By stage:
SELECT * FROM ps_analytics.docs.canonical WHERE stage = 'staged';

-- Find duplicates:
SELECT * FROM ps_analytics.docs.duplicates;
```

## Before Creating or Editing a Document

1. Search the registry first — the document may already exist
2. If it exists, use the `canonical_path`. Do NOT create a new file.
3. If creating new, register it immediately:

```sql
INSERT INTO ps_analytics.docs.documents (duck_id, title, canonical_path, stage, current_version, category)
VALUES ('category-my-topic', 'My Document', 'shared/path/to/file.md', 'draft', 1, 'category');
```

4. Stamp the file on line 1: `<!-- DOC-XXXX | duck_id: category-my-topic -->`


> **Example:** A typical use of this section involves reading the above rules and applying them to the current context.
## Moving a Document Between Stages

```sql
INSERT INTO ps_analytics.docs.versions (version_id, duck_id, version, file_path, stage, change_summary)
VALUES ('my-topic-v2', 'category-my-topic', 2, 'shared/new/path.md', 'staged', 'Revised after review');

UPDATE ps_analytics.docs.documents
SET canonical_path = 'shared/new/path.md', stage = 'staged', current_version = 2
WHERE duck_id = 'category-my-topic';
```

## Stages

intake → research → draft → review → staged → published → archived

## Rules

1. ONE canonical path per document. Query before creating.
2. When a document moves stages, UPDATE the registry.
3. Prior versions get status='archive-candidate' in file_index.
4. artifacts/ is archived — all content now in shared/wiki/.
5. portable-body/ was removed — shared/ is the single source of truth, synced to agent-bridge repo.
6. Every new file gets a DOC stamp on line 1.
7. New publishable docs go in shared/wiki/{topic}/. System docs go in shared/context/.
