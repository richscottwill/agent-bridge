# Artifact Sitemap

_Last generated: 2026-04-05_

```
AB PAID SEARCH — ARTIFACT DIRECTORY
====================================

TESTING (13 docs)
├── testing-approach-kate ........... Testing Approach & Year Ahead (Kate)             [strategy]  [L2] [FINAL]
│   ├── workstream-oci-bidding ...... ↳ WS1: OCI Bidding deep-dive                   [strategy]  [L2] [FINAL]
│   ├── workstream-modern-search .... ↳ WS2: Modern Search (Ad Copy)                  [strategy]  [L2] [FINAL]
│   ├── workstream-audiences ....... ↳ WS3: Audiences & Lifecycle (F90)               [strategy]  [L2] [FINAL]
│   ├── workstream-user-experience .. ↳ WS4: User Experience (Polaris, LPs)           [strategy]  [L2] [FINAL]
│   └── workstream-algorithmic-ads .. ↳ WS5: Algorithmic Ads (AI Max, Baloo)          [strategy]  [L2] [FINAL]
├── oci-rollout-playbook ............ OCI Rollout Playbook (strategy)                  [strategy]  [L2] [FINAL]
├── ai-max-test-design .............. AI Max Test Design — US Market                   [strategy]  [L2] [DRAFT]
├── ad-copy-testing-framework ....... Ad Copy Testing Framework (SP Study)             [strategy]  [L2] [DRAFT]
├── email-overlay-ww-rollout ........ Email Overlay WW Rollout Plan                    [strategy]  [L2] [DRAFT]
├── au-nb-mro-trades-proposal ....... AU NB Testing — MRO/Trades Vertical              [strategy]  [L2] [DRAFT]
├── project-baloo-overview .......... Project Baloo — Shopping Ads for AB              [strategy]  [L2] [DRAFT]
└── enhanced-match-liveramp ......... Enhanced Match / LiveRamp Expansion              [strategy]  [L2] [FINAL]

STRATEGY (12 docs)
├── agent-architecture .............. Agent System Architecture                        [strategy]  [L5] [DRAFT]
├── ieccp-planning-framework ........ ie%CCP Planning & Optimization                   [strategy]  [L2] [FINAL]
├── competitive-landscape ........... Competitive Landscape: Who's Bidding             [strategy]  [L2] [DRAFT]  *orphan — needs indexing*
├── q2-initiative-status ............ Q2 2026 Initiative Status & Priorities           [strategy]  [L2] [DRAFT]
├── oci-business-case ............... OCI Impact Summary — Business Case               [strategy]  [L2] [DRAFT]
├── genai-search-traffic ............ GenAI Search Traffic — What We Know              [strategy]  [L4] [DRAFT]
├── f90-lifecycle-strategy .......... F90 Lifecycle Program Strategy                    [strategy]  [L2] [DRAFT]
├── cross-market-playbook ........... Cross-Market Playbook (US→EU5→RoW)               [strategy]  [L2] [DRAFT]
├── aeo-ai-overviews-pov ............ AEO / AI Overviews POV                           [strategy]  [L4] [DRAFT]
├── agentic-ps-vision ............... Agentic Paid Search — Vision & Roadmap           [strategy]  [L5] [DRAFT]
├── body-system-architecture ........ The Body System — Architecture                   [strategy]  [L5] [DRAFT]
└── agentic-marketing-landscape ..... Agentic Marketing — Industry Landscape           [strategy]  [L4] [DRAFT]

PROGRAM DETAILS (8 docs)
├── ab-paid-search-wiki ............. AB Paid Search Program Wiki                      [reference] [--] [DRAFT]
├── au-market-wiki .................. AU Paid Search — Market Wiki                     [reference] [--] [FINAL]
├── mx-market-wiki .................. MX Paid Search — Market Wiki                     [reference] [--] [DRAFT]
├── oci-execution-guide ............. OCI Execution Guide (how-to)                     [execution] [--] [FINAL]
├── ww-testing-tracker .............. WW Testing Tracker (all tests)                   [reference] [L2] [DRAFT]
├── market-reference ................ Market Reference: 10 Markets                     [reference] [L2] [DRAFT]
├── team-workload-distribution ...... Team Capacity & Workload                         [reference] [--] [DRAFT]
└── polaris-rollout-status .......... Polaris WW Rollout Status                        [reference] [L2] [DRAFT]

REPORTING (2 docs)
├── au-keyword-cpa-dashboard ........ AU Keyword CPA Dashboard Design                  [execution] [L1] [DRAFT]
└── wbr-callout-guide ............... WBR Callout Template & Guide                     [execution] [L1] [DRAFT]

TOOLS (2 docs)
├── campaign-link-generator-spec .... Campaign Link Generator Spec                     [execution] [L3] [DRAFT]
└── budget-forecast-helper-spec ..... Budget Forecast Helper Spec                      [execution] [L3] [DRAFT]

COMMUNICATION (1 doc)
└── stakeholder-comms-guide ......... Stakeholder Communication Guide                  [execution] [L1] [DRAFT]

BEST PRACTICES (3 docs)
├── google-ads-campaign-structure ... Google Ads Campaign Structure Standards           [execution] [--] [DRAFT]
├── landing-page-testing-playbook ... Landing Page Testing Playbook                    [execution] [--] [DRAFT]
└── invoice-po-process-guide ........ Invoice & PO Process Guide                       [execution] [--] [DRAFT]

====================================
TOTAL: 40 artifacts | 29 DRAFT | 0 REVIEW | 11 FINAL
DOC-TYPES: ~18 strategy | ~12 execution | ~10 reference
LEVELS: L1×4 | L2×18 | L3×2 | L4×3 | L5×3 | N/A×10
```

## Document Relationships

```
testing-approach-kate (PARENT)
  ├── workstream-oci-bidding ──────→ oci-rollout-playbook (strategy), oci-execution-guide (execution)
  ├── workstream-modern-search ───→ aeo-ai-overviews-pov, email-overlay-ww-rollout
  ├── workstream-audiences ───────→ f90-lifecycle-strategy, enhanced-match-liveramp
  ├── workstream-user-experience ─→ polaris-rollout-status, landing-page-testing-playbook, au-market-wiki
  └── workstream-algorithmic-ads ─→ ai-max-test-design, project-baloo-overview

oci-rollout-playbook (STRATEGY) ←→ oci-execution-guide (EXECUTION)
  └── oci-business-case (LEADERSHIP SUMMARY)

agentic-ps-vision (STANDALONE)
  └── body-system-architecture, agentic-marketing-landscape

cross-market-playbook (STANDALONE)
  └── references all workstream docs + market wikis

ww-testing-tracker (STANDALONE)
  └── references all testing/ docs

q2-initiative-status (STANDALONE)
  └── references all active initiatives

genai-search-traffic → aeo-ai-overviews-pov (enriches)
enhanced-match-liveramp → f90-lifecycle-strategy (match rate dependency)
```

## How This Stays Current

Regenerated when: new artifact created, status changes, or directory structure changes.
The wiki-librarian regenerates by scanning ~/shared/artifacts/ and reading frontmatter.
