---
title: "Topic Registry"
status: ACTIVE
owner: Richard Williams
created: 2026-05-06
updated: 2026-05-06
---
<!-- DOC-TOPICS-REGISTRY -->

# Topic Registry

Canonical list of every registered topic. Machine-readable for hook ingest and topic-discovery reconciliation. Human-maintained for slug discipline.

**Columns**: slug | type | status | hedy_topic_id | aliases | notes

Hooks read this file to determine whether a signal maps to a registered topic. Signals matching an ACTIVE slug route to the topic doc. Signals matching no slug feed the discovery queue.

## Tests

| Slug | Status | Hedy Topic ID | Aliases | Notes |
|---|---|---|---|---|
| `polaris-brand-lp` | ACTIVE | — | polaris brand lp, brand landing page, polaris, polaris_brandlp, mx-polaris-test, polaris-lp-testing | Seed doc populated |
| `oci-rollout` | ACTIVE | tFEsxgnyO4QYp2x7TNrI | oci, oci-rollout-canada, oci-ca-launch | CA dial-up started 2026-04-14; doc created |
| `ai-max` | PLANNED | — | ai-max-questions, ai-max-implementation, google-summit-ai-max, ai-max-us-weblab | US weblab timeline Aug 2026 |
| `f90-audience` | PLANNED | — | f90, f90-lifecycle, f90-liveramp-filter | Blocked on InfoSec TPS |
| `baloo-shop-subdomain` | ACTIVE | n7WMdRSB3fXXzuP3cCXJ | baloo, baloo-phase1, baloo-deep-dive, au on baloo roadmap intake request, shop.business.amazon.com, ungated AB | Phase 1 launched; ref-tag persistence + URL flip issues open. Doc created 2026-05-06 |
| `liveramp-enhanced-match` | PLANNED | — | enhanced match, liveramp, liveramp-enhanced-match | Legal approval in flight |
| `paid-app-mx` | PLANNED | — | paid-app-marketing | Waiting on H2 2026 measurement |
| `email-overlay-ww-rollout` | PLANNED | — | email-overlay | Zero movement ~4 weeks |
| `in-context-email` | PLANNED | — | — | Zero movement since 3/17 |
| `au-max-clicks-revert` | PLANNED | — | au max clicks revert and keyword analysis process | Reverted from Adobe bidding |
| `canada-mobile-optimization` | PLANNED | — | canada-mobile-optimization | — |
| `ww-sitelink-audit` | PLANNED | — | ww-sitelink-audit, sbcc-sitelinks-paused | Brandon 4/15 ask, Asana 1214074477110993 |

## Markets

| Slug | Status | Hedy Topic ID | Aliases | Notes |
|---|---|---|---|---|
| `au` | ARCHIVED | N6kHmgM0rOdDdah7iNNf | australia, au paid search, au-transition, au_handoff, au handover, au deliverables due | Handed to ABix 2026-05-05, doc created |
| `mx` | ACTIVE | NVS0tfApqgEYYa839QNq | mexico, mx paid search, mx-budget-ieccp, mx-budget-transparency | Seed doc populated |
| `us` | PLANNED | — | — | Largest market by volume |
| `ca` | PLANNED | — | canada | — |
| `uk` | PLANNED | — | — | — |
| `de` | PLANNED | — | germany | — |
| `fr` | PLANNED | — | — | — |
| `it` | PLANNED | — | italy, italy-ref-tag, it tax fix verification | Ref tag issue active |
| `es` | PLANNED | — | — | — |
| `jp` | PLANNED | — | japan, wk17-dashboard-jp, jp minami sea visit 4/27 | — |
| `ww` | PLANNED | — | worldwide, ww testing | WW rollup |

## Initiatives

| Slug | Status | Hedy Topic ID | Aliases | Notes |
|---|---|---|---|---|
| `op1-2026` | ACTIVE | — | op1, op1-strategy, op1-planning, op1-forecast-flat-budget, op1-tech-intake | First draft due 5/12. Doc created 2026-05-06 |
| `mcs-polaris-migration` | ACTIVE | idSAffMcAegZh6MhQNyA | mcs, mcs-polaris, mcs-template, polaris-template-migration, mcs-coordination-ownership | Platform-side template migration; MX first Polaris test market. Doc created 2026-05-06 |
| `au-abix-transition` | COMPLETED | — | au handover, au-transition, au handoff doc final review | Transfer completed 2026-05-05, doc created |
| `ieccp-planning` | PLANNED | — | ieccp-quarterly, iaprstccp | Q2 2026 push for MX |
| `genbi-migration` | PLANNED | — | genbi, genbi-traffic-dataset, genbi vs adobe attribution for paid search handoff | Adobe analytics context |
| `aeo-ai-overviews` | ACTIVE | — | aeo, ai-overviews, ai-search-aeo, zero-click, answer-engine, chatgpt-ads-launch, gen-ai-search, forrester-aeo | Forrester brief 12/22/25 (Joe Cicman); L4 POV target per brain.md. Doc created 2026-05-06 |
| `agentic-ps` | PLANNED | — | — | L5 future state |
| `wbr-callouts-system` | PLANNED | — | wbr-callouts, callout-automation, monthly callouts loop comments, loop-callout-updates | System-internal |
| `kiro-system` | PLANNED | — | kiro-system, kiro-power-user, kiro-shared-directory, kiro-status-page, agentspaces-platform, agentspaces-stability | System-internal |
| `reftag-taxonomy-system` | ACTIVE | — | reftag-taxonomy, refmarker-taxonomy, feature-registry-replacement | Christine-led, replacing Feature Registry Q2 2026. Doc created 2026-05-06 |

## Projects

| Slug | Status | Hedy Topic ID | Aliases | Notes |
|---|---|---|---|---|
| `mpe-market-projection-engine` | PLANNED | — | — | Demo target 2026-05-16 |
| `testing-approach-doc` | PLANNED | — | au-testing-document | Kate review, Brandon gate |
| `forecasting-dashboard` | PLANNED | — | forecasting-dashboard, dive_forecast_* | Harmony app shipped |
| `annual-review-prep` | PLANNED | — | — | Growth-area-1 visibility |
| `au-handoff-doc` | PLANNED | — | au handover, au handoff doc final review | Feeds into au-abix-transition initiative |

## People (optional — track only when recurring cross-project signal)

Not every stakeholder needs a topic doc. Create only when the same person's behavior, decisions, or relationship pattern crosses 3+ topics and is worth tracking separately from meeting-series files.

| Slug | Status | Hedy Topic ID | Notes |
|---|---|---|---|
| — | — | — | — |

## Status values

- **ACTIVE** — topic doc exists and is being updated
- **PLANNED** — topic surfaced in discovery, doc not yet created; hooks will route signals to discovery queue
- **PAUSED** — topic paused (no new entries expected); preserve doc, pause ingest
- **COMPLETED** — deliverable shipped or test concluded; final entry logged, doc archived
- **ARCHIVED** — topic no longer relevant; doc preserved for history but excluded from discovery

## Reconciliation

wiki-maintenance Stage 5 runs weekly and reconciles this registry against `signals.signal_tracker` topic counts. New candidates with ≥3 mentions not in the registry get promoted to `_discovery-queue.md`. Registered slugs with no mentions for 60+ days get flagged for deprecation review.
