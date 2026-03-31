# 🗺️ Artifact Sitemap

_Last generated: 2026-03-25_

```
AB PAID SEARCH — ARTIFACT DIRECTORY
====================================

TESTING (11 docs)
├── testing-approach-kate ........... Testing Approach & Year Ahead (Kate Apr 16)     [amazon-internal] [L2] [DRAFT]
│   ├── workstream-oci-bidding ...... ↳ WS1: OCI Bidding deep-dive                   [amazon-internal] [L2] [DRAFT]
│   ├── workstream-modern-search .... ↳ WS2: Modern Search (Redirects, AEO)           [amazon-internal] [L2] [DRAFT]
│   ├── workstream-audiences ....... ↳ WS3: Audiences & Lifecycle (F90)               [amazon-internal] [L2] [DRAFT]
│   ├── workstream-user-experience .. ↳ WS4: User Experience (Polaris, LPs)           [amazon-internal] [L2] [DRAFT]
│   └── workstream-algorithmic-ads .. ↳ WS5: Algorithmic Ads (AI Max, Baloo)          [amazon-internal] [L2] [DRAFT]
├── ai-max-test-design .............. AI Max Test Design — US Market                   [amazon-internal] [L2] [DRAFT]
├── oci-rollout-methodology ......... OCI Rollout Methodology                          [amazon-internal] [L2] [DRAFT]
├── ad-copy-testing-framework ....... Ad Copy Testing Framework (SP Study)             [amazon-internal] [L2] [DRAFT]
├── email-overlay-ww-rollout ........ Email Overlay WW Rollout Plan                    [amazon-internal] [L2] [DRAFT]
└── au-nb-mro-trades-proposal ....... AU NB Testing — MRO/Trades Vertical              [amazon-internal] [L2] [DRAFT]

STRATEGY (6 docs)
├── agentic-ps-vision ............... Agentic Paid Search — Vision & Roadmap           [amazon-internal] [L5] [DRAFT]
├── body-system-architecture ........ The Body System — Architecture                   [personal]        [L5] [DRAFT]
├── agentic-marketing-landscape ..... Agentic Marketing — Industry Landscape           [personal]        [L4] [DRAFT]
├── aeo-ai-overviews-pov ............ AEO / AI Overviews POV                           [amazon-internal] [L4] [DRAFT]
├── cross-market-playbook ........... Cross-Market Playbook (US→EU5→RoW)               [amazon-internal] [L2] [DRAFT]
└── f90-lifecycle-strategy .......... F90 Lifecycle Program Strategy                    [amazon-internal] [L2] [DRAFT]

REPORTING (3 docs)
├── au-keyword-cpa-dashboard ........ AU Keyword CPA Dashboard Design                  [amazon-internal] [L1] [DRAFT]
├── wbr-callout-guide ............... WBR Callout Template & Guide                     [amazon-internal] [L1] [DRAFT]
└── competitive-intel-tracker ....... Competitive Intelligence Tracker                  [amazon-internal] [L2] [DRAFT]

TOOLS (2 docs)
├── campaign-link-generator-spec .... Campaign Link Generator Spec                     [amazon-internal] [L3] [DRAFT]
└── budget-forecast-helper-spec ..... Budget Forecast Helper Spec                      [amazon-internal] [L3] [DRAFT]

COMMUNICATION (3 docs)
├── polaris-rollout-timeline ........ Polaris Brand LP Rollout Timeline                [amazon-internal] [L1] [DRAFT]
├── mx-ps-handoff-guide ............. MX PS Handoff Guide (Carlos→Lorena)              [amazon-internal] [L1] [DRAFT]
└── oci-methodology-knowledge-share . OCI Methodology — Knowledge Sharing              [amazon-internal] [L1] [DRAFT]

PROGRAM DETAILS (5 docs)
├── ab-paid-search-wiki ............. AB Paid Search Program Wiki                      [amazon-internal] [--] [DRAFT]
├── au-market-wiki .................. AU Market Wiki                                   [amazon-internal] [--] [DRAFT]
├── mx-market-wiki .................. MX Market Wiki                                   [amazon-internal] [--] [DRAFT]
├── oci-implementation-guide ........ OCI Implementation Guide (Per-Market)            [amazon-internal] [--] [DRAFT]
└── ww-testing-tracker .............. WW Testing Tracker (All Tests)                   [amazon-internal] [L2] [DRAFT]

BEST PRACTICES (3 docs)
├── google-ads-campaign-structure ... Google Ads Campaign Structure Standards           [amazon-internal] [--] [DRAFT]
├── landing-page-testing-playbook ... Landing Page Testing Playbook                    [amazon-internal] [--] [DRAFT]
└── invoice-po-process-guide ........ Invoice & PO Process Guide                       [amazon-internal] [--] [DRAFT]

====================================
TOTAL: 33 artifacts | 33 DRAFT | 0 REVIEW | 0 FINAL
AUDIENCE: 30 amazon-internal | 2 personal | 0 agent-only
LEVELS: L1×5 | L2×15 | L3×2 | L4×2 | L5×2 | N/A×7
```

## Document Relationships

```
testing-approach-kate (PARENT)
  ├── workstream-oci-bidding ──────→ oci-rollout-methodology (reference)
  │                                  oci-implementation-guide (reference)
  │                                  oci-methodology-knowledge-share (reference)
  ├── workstream-modern-search ───→ aeo-ai-overviews-pov (reference)
  │                                  email-overlay-ww-rollout (reference)
  ├── workstream-audiences ───────→ f90-lifecycle-strategy (reference)
  ├── workstream-user-experience ─→ polaris-rollout-timeline (reference)
  │                                  landing-page-testing-playbook (reference)
  │                                  au-market-wiki (reference)
  └── workstream-algorithmic-ads ─→ ai-max-test-design (reference)

agentic-ps-vision (STANDALONE)
  └── body-system-architecture (reference)
      agentic-marketing-landscape (reference)

cross-market-playbook (STANDALONE)
  └── references all workstream docs + market wikis

ww-testing-tracker (STANDALONE)
  └── references all testing/ docs
```

## How This Stays Current

This sitemap is regenerated when:
- A new artifact is created
- An artifact status changes (DRAFT → REVIEW → FINAL)
- The artifact directory structure changes

The agent regenerates by scanning `~/shared/artifacts/` and reading front-matter from each file.
# Reference Index

A central index of documents and resources for quick access.

## Quip — Outbound Marketing (Internal)
Main folder: https://quip-amazon.com/UZ3VOhztKN4s/Outbound-Marketing-Internal

### Top-Level Docs
- [Paid Acq Projects](https://quip-amazon.com/bXT9AA5YdtN) — spreadsheet, active project tracker
- [PO Process Options - Paid Search](https://quip-amazon.com/NXF9AAy02OQ) — PO/invoicing process
- [Outbound Holiday Tracker](https://quip-amazon.com/dGM9AARtQnG) — spreadsheet
- [MBet Process Improvement](https://quip-amazon.com/FZQ9AARARAN)

### Subfolders
- [Testing](https://quip-amazon.com/NfR9OA6clcH/) — 20 items, paid search testing docs
- [Review](https://quip-amazon.com/MRQ9OA8fzMn/) — 15 items, WBR/review docs
- [Planning](https://quip-amazon.com/QcL9OAla0aR/) — 4 items
- [Onboarding/Best Practice](https://quip-amazon.com/JeH9OAHbCkF/) — 4 items
- [Events](https://quip-amazon.com/Afc9OA7yLSI/) — 5 items
- [Creative](https://quip-amazon.com/bfX9OAk81Ay/) — 1 item
- [...NA](https://quip-amazon.com/JTP9OAfqvcL/) — North America
- [..EU](https://quip-amazon.com/aXF9OAXXhSH/) — 8 items, European markets
- [..JP](https://quip-amazon.com/Xca9OAoab2S/) — 5 items, Japan
- [.ABIX](https://quip-amazon.com/dOP9OAN9Quw/) — 2 items, International Expansion
- [.Mobile App](https://quip-amazon.com/XGH9OAGo2yM/) — 2 items
- [.Partnerships](https://quip-amazon.com/FCE9OAGNr3n/) — 4 items

## Quip — Sync Docs
- [AB MX Paid Search Sync](https://quip-amazon.com/K9OYA9mXm7DU/AB-MX-Paid-Search-Sync)
- [WW AB Traffic Marketing Pre-WBR Callouts](https://quip-amazon.com/MMgBAzDrlVou)

## Key Contacts
See ~/shared/context/active/org-chart.md

## Project Briefs
<!-- Link to or summarize active project context -->

## Templates
<!-- Reference reusable email/doc templates -->
