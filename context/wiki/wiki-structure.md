# Wiki Structure

> The wiki pipeline (research → staging → review) lives in `~/shared/context/wiki/`.
> The OUTPUT — published articles — lives in `~/shared/artifacts/{category}/`.
> The wiki infrastructure is the production process; artifacts is the product.

## Categories

Categories align 1:1 with the `~/shared/artifacts/` folder structure.

| Category | Slug | Artifact Folder | Description | Article count |
|----------|------|-----------------|-------------|---------------|
| Paid Search Operations | ps-ops | `program-details/` | Day-to-day PS workflows, account details, campaign structures | 6 |
| Testing & Experimentation | testing | `testing/` | Test designs, methodologies, experiment frameworks | 11 |
| Market Playbooks | markets | `program-details/` | Per-market wikis (AU, MX, etc.) — subset of program-details | (counted in ps-ops) |
| Tools & Automation | tools | `tools/` | Tool specs, automation docs, process docs | 2 |
| Strategy & Frameworks | strategy | `strategy/` | POVs, playbooks, strategic narratives, OP1 docs | 6 |
| Reporting | reporting | `reporting/` | Dashboards, analysis docs, performance summaries | 3 |
| Communication | communication | `communication/` | Stakeholder docs, handoff guides, knowledge-sharing artifacts | 3 |
| Best Practices | best-practices | `best-practices/` | Operational standards, how-tos, reusable frameworks | 3 |
| System Documentation | system | _(wiki-only or future artifacts/system/)_ | Body system, agent architecture, hooks | 0 |

### Category → Folder Mapping Notes

- **Paid Search Operations** and **Market Playbooks** both map to `program-details/`. Market wikis (au-market-wiki, mx-market-wiki) are a subset — tagged `market-wiki` for filtering.
- **System Documentation** has no artifact folder yet. System docs (body system, agent architecture) currently live in `~/shared/context/body/` and steering files. If system docs become publishable artifacts, create `artifacts/system/`.
- The wiki index uses the artifact folder as the canonical location. The slug is for wiki navigation; the folder is for file placement.

## Navigation Hierarchy

```
Wiki (wiki-index.md)
├── Testing & Experimentation (testing/)
│   ├── testing-approach-kate (parent)
│   │   ├── workstream-oci-bidding
│   │   ├── workstream-modern-search
│   │   ├── workstream-audiences-lifecycle
│   │   ├── workstream-user-experience
│   │   └── workstream-algorithmic-ads
│   ├── ai-max-test-design
│   ├── oci-rollout-methodology
│   ├── ad-copy-testing-framework
│   ├── email-overlay-ww-rollout
│   └── au-nb-mro-trades-proposal
├── Strategy & Frameworks (strategy/)
│   ├── agentic-ps-vision
│   ├── body-system-architecture
│   ├── agentic-marketing-landscape
│   ├── aeo-ai-overviews-pov
│   ├── cross-market-playbook
│   └── f90-lifecycle-strategy
├── Paid Search Operations / Market Playbooks (program-details/)
│   ├── ab-paid-search-wiki
│   ├── au-market-wiki
│   ├── mx-market-wiki
│   ├── oci-implementation-guide
│   ├── ww-testing-tracker
│   └── promo-events-calendar
├── Reporting (reporting/)
│   ├── au-keyword-cpa-dashboard
│   ├── wbr-callout-guide
│   └── competitive-intel-tracker
├── Tools & Automation (tools/)
│   ├── campaign-link-generator-spec
│   └── budget-forecast-helper-spec
├── Communication (communication/)
│   ├── polaris-rollout-timeline
│   ├── mx-ps-handoff-guide
│   └── oci-methodology-knowledge-share
├── Best Practices (best-practices/)
│   ├── google-ads-campaign-structure
│   ├── landing-page-testing-playbook
│   └── invoice-po-process-guide
└── System Documentation
    └── (no published articles yet)
```

## Publishing Workflow

When an article passes the wiki-critic review and is approved for publishing:

1. **Source**: Read the staged article at `~/shared/context/wiki/staging/{topic-slug}.md`
2. **Review**: Read the critic's review at `~/shared/context/wiki/reviews/{topic-slug}-review.md`
3. **Validate**:
   - Frontmatter is complete (all required fields present)
   - `depends_on` slugs point to articles that exist
   - `tags` use existing taxonomy terms (or flag new ones for approval)
   - `AGENT_CONTEXT` block is present and well-formed
   - No unresolved `<!-- TODO -->` markers remain
4. **Convert to artifact format**:
   - Rename to artifact naming convention: `YYYY-MM-DD-short-description.md`
   - Replace wiki frontmatter with artifact front-matter standard:
     ```
     ---
     title: [Document title]
     status: DRAFT | REVIEW | FINAL
     audience: amazon-internal | personal | agent-only
     level: [1-5 or N/A]
     owner: [who maintains this doc]
     created: YYYY-MM-DD
     updated: YYYY-MM-DD
     update-trigger: [what context change should trigger a refresh]
     ---
     ```
   - Preserve the article body content, AGENT_CONTEXT block, and Sources section
5. **Publish**: Move the converted article to `~/shared/artifacts/{category}/`
   - Map the wiki category to the correct artifact folder (see table above)
6. **Update cross-references**:
   - Update `wiki-index.md` with the new article entry pointing to `~/shared/artifacts/`
   - Update the SITEMAP.md in `~/shared/artifacts/`
   - Add this article to the `consumed_by` field of any article it `depends_on`
7. **Clean up**: Remove the staged version from `~/shared/context/wiki/staging/`
8. **Log**: Add entry to the wiki-index.md update log

### Key principle: The wiki pipeline stays in `~/shared/context/wiki/`. The output goes to `~/shared/artifacts/`.

```
~/shared/context/wiki/          ← PROCESS (research, drafts, reviews)
  ├── research/                 ← Research briefs
  ├── staging/                  ← Draft articles (wiki-writer writes here)
  ├── reviews/                  ← Review reports (wiki-critic writes here)
  ├── archive/                  ← Deprecated articles
  ├── health/                   ← Health check reports
  ├── wiki-index.md             ← Index OVER ~/shared/artifacts/
  ├── wiki-structure.md         ← This file (taxonomy, workflow)
  └── roadmap.md                ← Content pipeline

~/shared/artifacts/             ← PRODUCT (published articles)
  ├── testing/
  ├── strategy/
  ├── reporting/
  ├── tools/
  ├── communication/
  ├── program-details/
  ├── best-practices/
  ├── SITEMAP.md
  └── README.md
```

### Deprecated: `~/shared/context/wiki/published/`

The `published/` directory is **deprecated**. Published articles go to `~/shared/artifacts/{category}/`, not to `published/`. This directory exists as an empty placeholder and should not be used. All publishing workflows target the artifacts folder.

## Taxonomy (controlled vocabulary for tags)

### Domain tags
paid-search, brand, non-brand, oci, ad-copy, landing-page, bid-strategy, budget, cpa, cvr, cpc

### Market tags
us, ca, jp, uk, de, fr, it, es, au, mx, eu5, najp, abix, ww

### Process tags
wbr, callout, testing, reporting, automation, delegation, morning-routine

### System tags
body-system, agent, hook, steering, tool, mcp, agent-bridge

### Artifact type tags
market-wiki, test-design, pov, playbook, tool-spec, handoff, knowledge-share, dashboard, tracker, process-guide
