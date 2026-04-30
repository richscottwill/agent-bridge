---
title: "MX Paid Search — Market Wiki"
status: REVIEW
audience: amazon-internal
owner: Richard Williams
created: 2026-04-12
updated: 2026-04-12
---
<!-- DOC-0321 | duck_id: program-mx-market-wiki -->

---
title: MX Paid Search — Market Wiki
status: DRAFT
doc-type: reference
audience: amazon-internal
level: N/A
owner: Richard Williams
created: 2026-03-25
updated: 2026-04-04
update-trigger: MX sync outcomes, Lorena direction, campaign changes, invoice owner decided
tags: [market-wiki, mx]
replaces: mx-market-wiki, mx-ps-handoff-guide
---

**Key consideration:** This section's content is critical for accurate operation. Cross-reference with related sections for full context.
# MX Paid Search — Market Wiki

> Canonical reference for Mexico. Includes Lorena's onboarding context (formerly in the separate handoff guide, now merged here).

---

## Overview

MX is Richard's second hands-on market and the strongest growth market in the portfolio relative to plan (+32% vs OP2). Primary stakeholder transitioned from Carlos Palmos to Lorena Alvarez Larrea (~3/17/2026) when Carlos moved to CPS. MX does not have OCI support and has no timeline for it.

The market operates under an ie%CCP constraint that limits NB spend. Brand growth has been strong (~2.7x YoY organically in Q1 2026), creating CCP surplus that could fund more NB spend — but only if NB CPA improves or the ie%CCP target loosens. See [ie%CCP Planning Framework](../strategy/ieccp-planning-framework.md) for the full budget model with MX case study.

---

## Current Performance

| Metric | Value | vs OP2 | YoY | Notes |
|--------|-------|--------|-----|-------|
| Registrations (Feb) | 1.1K | +32% | +37% | Strong growth |
| Spend (Feb) | $68K | — | — | — |
| W13 Regs | 354 | +9% WoW | +91% YoY | NB regs +33% above avg |
| W13 CPA | $66 | +6% WoW | — | NB CPA $112 sustained from H2 2025 |
| ie%CCP (corrected) | 93% | — | — | Near 100% target |

MX is outperforming plan by 32% on registrations. The ie%CCP at 93% is near the 100% target, meaning the account is close to its efficiency ceiling under current constraints. Brand growth is the primary lever for creating more NB capacity.

---

## Google Ads Account

| Field | Value |
|-------|-------|
| MCC | NA MCC (683-476-0964) |
| Market | MX (Mexico) |
| Language | Spanish (Mexico) |
| Currency | MXN |

## Campaign Structure

| Campaign | Type | Status | Landing Page |
|----------|------|--------|-------------|
| MX Brand | Brand | Active | business.amazon.com.mx/es |
| MX NB | Non-Brand | Active | business.amazon.com.mx/es |
| MX Auto | Category | Active (page live 3/23) | business.amazon.com.mx/es/cp/auto-shop |
| MX Beauty | Category | Active (page live 3/23) | business.amazon.com.mx/es/cp/beauty |

---

## Key Stakeholders | Name | Role | Tone | Key Context | |------|------|------|-------------| | Lorena Alvarez Larrea | Primary PS stakeholder (L5) | Professional, friendly. "Hi!" openers, signs "Thanks! Lorena Alvarez" | New to PS (since 3/17). Actively engaging — Q2 spend request shows she is thinking ahead on PO. Needs keyword data, negative keyword list, campaign overview. | | Carlos Palmos | Former PS stakeholder (L5) | Professional | Transitioned to CPS ~3/17. MX invoice delegation VOID — needs new owner. | | Pedro Maldonado | Country Leader (L7) | — | Carlos and Lorena's skip. | ### What Lorena Needs to Know
1. Richard manages the Google Ads account directly
2. Lorena's role: market context, keyword opportunities, budget confirmation, strategic direction
3. Richard handles: campaign builds, bid management, reporting, optimization
4. Communication: biweekly sync + ad hoc via email
5. Keyword data export pending (promised in reply draft)

---

## Active Issues (Priority Order)

1. **Invoice routing: BLOCKING.** Carlos VOID, needs new owner (Lorena or Richard). Cannot submit invoices until decided.
2. **Lorena onboarding: TIME-SENSITIVE.** Needs keyword data, negative keyword list, campaign overview. Relationship is new — be thorough.
3. **Reftag tracking anomaly.** W8 to W9 drop from 87 to 12 unique reftags. Under investigation.
4. **Kingpin Goals: OVERDUE.** Blocked by Andes data.
5. **MX Beauty/Auto pages.** LIVE (3/23). Explore category button cannot be removed, reftags customizable. Monitoring.

---

## Keyword Strategy

- Brand keywords: Amazon Business MX variations (Spanish)
  - *Example:* Brand keywords → apply this when the situation matches the described pattern.
- NB keywords: business supplies, office supplies, industrial supplies (Spanish)
- Negative keywords: in place (will share full list with Lorena)
- Opportunities from Lorena:
  1. APP Download sitelink — target app-intent keywords
  2. Beauty industry keywords — page is now live
  3. Negative keyword review — share current list

---

## Competitors

- **algo-mas.mx:** 11-13% Brand IS, +20% CPC spikes when active. Response: monitor IS weekly, hold bid caps. Not persistent enough to warrant escalation — cycles in and out.
- **Temu:** Emerging on Generic NB (since W23 2025). Monitoring.

---

## Invoice/PO Details

| PO | Number | Vendor | Status |
|----|--------|--------|--------|
| MX | MS-20200908 | Google Mexico | Active |
| WW | 5LN2R - 5489247319 | Google Ireland Ltd | Active (covers multiple markets) |

Invoice routing status: **NEEDS NEW OWNER** (was Carlos). Discuss with Lorena at next sync.

For full invoice process, see [Invoice & PO Process Guide](../operations/invoice-po-process-guide.md).

---

## Recurring Meetings

- MX Paid Search Sync: biweekly (Lorena, Yun, Richard)
- Sync doc: [MX Sync Quip](https://quip-amazon.com/K9OYA9mXm7DU)

---

## Sources
- MX performance (Feb 2026, W13) — source: ~/shared/context/body/eyes.md -> Market Health -> MX
- Carlos to Lorena transition — source: ~/shared/context/active/current.md -> MX Paid Search
- Landing pages live (3/23) — source: Asana notification (Vijeth, Auto-Comms folder)
- algo-mas.mx competitor — source: ~/shared/context/body/eyes.md -> Competitive Landscape -> International
- PO numbers — source: ~/shared/context/body/hands.md -> Admin tasks
- Reftag anomaly — source: ~/shared/context/body/hands.md -> Engine Room -> MX reftags
- Lorena's keyword requests — source: Lorena email "Paid Search Strategy" (3/19)
- ie%CCP corrected to 93% — source: ~/shared/context/body/eyes.md -> Market Health -> MX
- Lorena communication style — source: ~/shared/context/body/memory.md -> Lorena Alvarez Larrea

<!-- AGENT_CONTEXT
machine_summary: "Canonical MX market reference. Merges former MX Market Wiki and MX PS Handoff Guide. Growth market at +32% vs OP2, ie%CCP at 93% (near 100% target). Primary stakeholder transitioned from Carlos to Lorena (3/17). Key issues: invoice routing needs new owner (BLOCKING), Lorena onboarding in progress, reftag tracking anomaly. No OCI support. Competitors: algo-mas.mx (11-13% Brand IS, cycles in/out), Temu emerging on NB."
key_entities: ["MX", "Lorena Alvarez Larrea", "Carlos Palmos", "Pedro Maldonado", "algo-mas.mx", "Temu", "ie%CCP", "MX Brand", "MX NB", "MX Auto", "MX Beauty"]
action_verbs: ["onboard", "transition", "investigate", "route", "expand", "monitor"]
update_triggers: ["MX sync outcomes", "Lorena direction changes", "invoice owner decided", "reftag investigation resolved", "ie%CCP target change"]
-->


## Related

- [OCI Program](../testing/oci-program) — MX OCI currently descoped
- [Polaris Program](polaris-program) — MX early test market
- [MX PS Handoff Guide](../operations/mx-ps-handoff-guide) — Carlos → Lorena transition
- [Paid Search Testing Approach](../testing/testing-approach-kate-v5) — testing methodology
