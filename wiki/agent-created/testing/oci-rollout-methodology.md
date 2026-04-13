---
title: "OCI Rollout Methodology"
status: REVIEW
audience: amazon-internal
owner: Richard Williams
created: 2026-04-12
updated: 2026-04-12
---
<!-- DOC-0404 | duck_id: testing-oci-rollout-methodology -->

> **⚠️ ARCHIVED — 2026-04-04. Replaced by oci-rollout-playbook + oci-execution-guide. Do not update this file.**

---
title: OCI Rollout Methodology
status: archived
audience: amazon-internal
level: 2
owner: Richard Williams
created: 2026-03-25
updated: 2026-03-25
update-trigger: new OCI market launches, phase transitions, results updates
---

# OCI Rollout Methodology

---

> For per-market tactical steps, see [OCI Implementation Guide](~/shared/artifacts/program-details/2026-03-25-oci-implementation-guide.md). For team knowledge-sharing, see [OCI Methodology Knowledge Share](~/shared/artifacts/communication/2026-03-25-oci-methodology-knowledge-share.md).

## Overview

Optimized Conversions with Intelligence (OCI) is Google's conversion-based bidding system. AB PS uses a phased rollout methodology validated across US, UK, and DE before scaling to remaining markets.

## Phased Rollout Framework

### Phase 1: E2E (End-to-End) Launch
- Enable OCI at campaign level for NB campaigns only
- No traffic percentage target — Google ramps automatically
- Duration: 2-4 weeks
- Monitor: conversion tracking accuracy, CPA stability

### Phase 2: 25% Traffic
- Set target impression share or budget to ~25% of NB spend
- Duration: 2-4 weeks
- Measurement: actualized CPA vs seasonality-adjusted baseline
- Gate: CPA within 115% of baseline to proceed

### Phase 3: 50% Traffic
- Expand to 50% of NB spend
- Duration: 2-4 weeks
- Measurement: same framework, larger sample
- Gate: CPA within 110% of baseline

### Phase 4: 100% NB
- Full NB migration to OCI
- Brand campaigns remain manual (bid caps for competitive defense)
- Ongoing monitoring: weekly CPA review, monthly deep dive

## Measurement Framework

| Metric | How Measured | Frequency |
|--------|-------------|-----------|
| Reg lift | Test vs control (phased) or pre/post (full) | Weekly |
| CPA | Actualized CPA vs seasonality-adjusted baseline | Weekly |
| Impression share | Google Ads auction insights | Weekly |
| Search term quality | Manual review of new queries | Biweekly |

## Market Status

| Market | Phase | Launch | Full Impact |
|--------|-------|--------|-------------|
| US | Complete (100%) | Jul 2025 | Oct 2025 |
| UK | Complete (100%) | Aug 2025 | Oct 2025 |
| DE | Complete (100%) | Nov 2025 | Jan 2026 |
| CA | E2E | Mar 2026 | Jul 2026 |
| JP | E2E | Feb 2026 | Jul 2026 |
| FR | E2E | Feb 2026 | Jul 2026 |
| IT | E2E | Feb 2026 | Jul 2026 |
| ES | E2E | Feb 2026 | Jul 2026 |
| AU | Not planned | — | — |
| MX | Not planned | — | — |

US/UK/DE are the reference implementations. CA/JP/EU3 are in E2E — expect full impact by Jul 2026. AU/MX are excluded because Google doesn't support OCI in those markets.

## Results Summary

| Market | Reg Lift | CPA Improvement | OPS Impact |
|--------|----------|-----------------|------------|
| US | +24% (+32K regs) | ~50% NB CPA | $16.7MM |
| UK | +23% (+2.4K regs) | Notable | TBD |
| DE | +18% (+749 regs) | Notable | TBD |

OCI is the single highest-impact initiative in the program's history. The $16.7MM OPS from US alone justifies the phased methodology.

## Known Issues & Lessons Learned

For detailed troubleshooting and per-market implementation notes, see [OCI Implementation Guide](~/shared/artifacts/program-details/2026-03-25-oci-implementation-guide.md).


## Sources
- OCI rollout timeline (all markets) — source: ~/shared/context/body/eyes.md → OCI Performance → Rollout Timeline
- OCI results (US/UK/DE lift, OPS) — source: ~/shared/context/body/eyes.md → OCI Performance → Impact Summary
- Phased rollout methodology (E2E→25%→50%→100%) — source: ~/shared/context/body/brain.md → D1: OCI Implementation Approach
- MCC structure — source: ~/shared/context/body/eyes.md → OCI Performance → MCC Structure
- hvocijid duplicate parameter issue — source: ~/shared/context/body/eyes.md → OCI Performance → Known Issues
- Measurement framework (actualized CPA vs seasonality-adjusted baseline) — source: ~/shared/context/body/brain.md → D1

<!-- AGENT_CONTEXT
machine_summary: "Canonical methodology for OCI (Optimized Conversions with Intelligence) phased rollout across AB PS markets. Covers E2E→25%→50%→100% framework, gate criteria, measurement, and results. US/UK/DE complete with +18-24% reg lift; CA/JP/EU3 in E2E."
key_entities: ["OCI", "phased rollout", "US", "UK", "DE", "CA", "JP", "EU3", "NB campaigns", "Google Ads"]
action_verbs: ["launch", "monitor", "gate", "scale", "measure"]
update_triggers: ["new OCI market reaches next phase", "E2E markets complete scaling", "new OCI results available"]
-->
