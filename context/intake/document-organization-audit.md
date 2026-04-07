<!-- DOC-0172 | duck_id: intake-document-organization-audit -->
# Document Organization Audit — 2026-04-06

## Scale
526 markdown files across ~/shared/. Multiple authoring surfaces (agents, IDE, Asana, DuckDB, wiki pipeline).

## Problem: Three Types of Fragmentation

### 1. Body System Triplication
The same organ files exist in 3 places with different versions:

| File | shared/context/body/ | shared/portable-body/body/ | ~/portable-body/body/ |
|------|---------------------|---------------------------|----------------------|
| spine.md | 7KB (Apr 5) | 12KB (Apr 3) | 12KB (Apr 6, cache) |
| soul.md | 10KB (steering) | 14KB (Apr 3) | 14KB (Apr 6, cache) |
| gut.md | 14KB (Apr 5) | 15KB (Apr 3) | 15KB (Apr 6, cache) |
| heart.md | 27KB (Apr 5) | 20KB (Apr 3) | 20KB (Apr 6, cache) |
| hands.md | 8KB (Apr 6) | 12KB (Apr 3) | 12KB (Apr 6, cache) |

**Root cause**: shared/context/body/ is the live system. shared/portable-body/ is the bridge export. ~/portable-body/ is the cache recovery copy. They diverge because Karpathy experiments modify the live copy but the bridge export isn't always synced.

**Fix**: shared/context/body/ is the source of truth. portable-body/ copies should be generated from it, not maintained independently. The cache copy at ~/portable-body/ should be deleted.

### 2. Document Version Sprawl
Key documents exist as multiple versions across artifacts, wiki staging, wiki reviews, and research:

**Testing Approach (Kate doc)** — 7+ files:
- shared/artifacts/testing/2026-03-25-testing-approach-kate.md (original artifact)
- shared/context/wiki/staging/testing-approach-kate-v5.md (latest staged)
- shared/research/testing-approach-outline.md (early outline)
- shared/context/wiki/reviews/kate-doc-*.md (6+ review files)
- shared/context/wiki/reviews/testing-approach-kate-v2-eval-a.md

**OCI** — 6+ files:
- shared/artifacts/testing/2026-03-25-oci-rollout-methodology.md
- shared/artifacts/testing/2026-03-25-oci-rollout-playbook.md
- shared/artifacts/program-details/2026-04-04-oci-execution-guide.md
- shared/context/wiki/staging/oci-playbook-rewrite.md
- shared/context/wiki/reviews/kate-doc-oci-revisions.md

**Workstreams** — each has 3-4 versions:
- artifacts/testing/2026-03-25-workstream-algorithmic-ads.md (v1)
- wiki/staging/workstream-algorithmic-ads-v4.md
- wiki/staging/workstream-algorithmic-ads-v5.md (latest)
- wiki/reviews/batch-5-workstreams-*.md

**Five Year Outlook** — 5+ files:
- artifacts/strategy/2026-04-05-ps-five-year-outlook.md
- wiki/staging/five-year-outlook-v1.md, v2.md
- wiki/staging/five-year-outlook-research-brief.md
- wiki/staging/ps-five-year-outlook-research-brief.md (empty, 0 bytes)
- wiki/reviews/five-year-outlook-v1-eval-b.md, v2-eval-b.md, etc.

**AU Market** — 4 files:
- artifacts/program-details/2026-03-25-au-market-wiki.md
- artifacts/program-details/2026-04-03-au-market-overview.md
- artifacts/program-details/2026-04-03-au-paid-search-market-overview.md
- artifacts/program-details/2026-04-04-au-market-wiki.md

### 3. Agent/Steering Duplication
- rw-trainer.md: 4 copies (portable-body/agents, portable-body/steering, .kiro/agents, ~/portable-body/agents)
- Writing style guides: 2 copies each (steering + portable-body)
- Wiki agent files: 2 copies each (agents + portable-body)

## Proposed Organization Standard

### Document Lifecycle
```
INTAKE → RESEARCH → DRAFT → REVIEW → STAGED → PUBLISHED → ARCHIVE
```

### Directory Mapping
| Stage | Location | What goes here |
|-------|----------|---------------|
| Intake | shared/context/intake/ | Raw signals, observations, proposals |
| Research | shared/context/wiki/research/ | Research briefs, data gathering |
| Draft | shared/context/wiki/drafts/ | Work-in-progress versions (v1, v2...) |
| Review | shared/context/wiki/reviews/ | Critic evaluations, revision notes |
| Staged | shared/context/wiki/staging/ | Final version ready for publish |
| Published | w.amazon.com (wiki) | Live on internal wiki |
| Archive | shared/context/wiki/archive/ | Superseded versions |

### Rules
1. **One canonical location per document**: The latest version lives in ONE place. Prior versions move to archive/ with date prefix.
2. **artifacts/ is for first drafts only**: When a document enters the wiki pipeline, the artifact version becomes the seed. The wiki staging version becomes canonical.
3. **No version numbers in filenames for artifacts/**: Use date prefix instead (2026-04-06-testing-approach-kate.md). Version numbers only in wiki staging (testing-approach-kate-v5.md).
4. **portable-body/ is generated, not authored**: Bridge sync generates it from shared/context/body/. Never edit portable-body/ directly.
5. **~/portable-body/ (root) should not exist**: Delete it. It's a cache artifact.
6. **Reviews are ephemeral**: After a document is staged, review files can be archived or deleted. They served their purpose.
7. **Empty files should be deleted**: ps-five-year-outlook-research-brief.md (0 bytes) etc.

### Immediate Cleanup Actions
1. Delete ~/portable-body/ (root-level cache copy)
2. Delete 0-byte files
3. Archive superseded artifact versions (e.g., au-market-wiki 2026-03-25 superseded by 2026-04-04)
4. Move completed wiki reviews to archive/
5. Consolidate rw-trainer.md to one canonical location
6. Add a document registry (DuckDB table or markdown index) tracking: document name, canonical path, current version, stage, last modified, Asana task GID
