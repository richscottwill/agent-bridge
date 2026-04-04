---
title: "Workstream 1: Intelligent Bidding (OCI)"
slug: "kate-doc-oci"
type: "playbook"
audience: "org"
status: "draft"
doc-type: strategy
created: "2026-03-25"
updated: "2026-03-25"
owner: "Richard Williams"
tags: ["oci", "bidding", "kate-doc"]
summary: "OCI bidding: +35K regs, $16.7MM OPS across US/UK/DE. Scaling to 5 more markets by July 2026."
---

# Workstream 1: Intelligent Bidding (OCI)

*Progression: Loss of Google Ads auto-bid strategy and Adobe → OCI success and expansion*

## What We Did

To launch OCI bidding, accurate tracking of campaign traffic and conversions was required. The Paid Search team partnered with the MarTech team to implement OCI as the first non-retail business unit at Amazon. This was not a plug-and-play integration — it required defining the OCI value framework with Data Science, ensuring Legal approved the data flow, building the tracking infrastructure with MarTech, and validating the underlying data to support accurate optimization.

The team established a phased implementation and measurement plan: E2E keyword-level testing → 25% → 50% → 100% campaign-level application. At each phase, we evaluated performance lift against a seasonality-adjusted baseline and made a go/no-go decision before proceeding. The measurement framework — actualized CPA vs. prior-quarter baseline with seasonality adjustments — has since become the standard approach for each new market rollout.

## What We Learned

### Performance Lift by Market

| Market | Test Period | Reg Lift | NB CPA Improvement | Estimated Regs | Estimated OPS | % to Expectation |
|--------|-----------|----------|---------------------|----------------|---------------|------------------|
| US | Jul-Nov 2025 | +24% | ~50% | +32,047 | $16.7MM | 96% |
| UK | Aug-Oct 2025 | +23% | Significant | +2,400 | — | 94% |
| DE | Oct-Dec 2025 | +18% | Significant | +749 | — | 86% |
| **Total** | | | | **+35,196** | **$16.7MM+** | |

The US met 96% of expectations, UK met 94%, and DE met 86%. Brand CPA improved -10% to -14% across all three markets with +1% registration lift, aligned with expectations given the lower improvement opportunity on high-intent Brand terms.

### DE Test vs. Control Data (from WBR)

| Week | Segment | Cost | Regs | ROAS | CPA |
|------|---------|------|------|------|-----|
| W44 | NB Control | $44,592 | 36 | 3% | $1,239 |
| W44 | NB Test (OCI) | $64,565 | 200 | 13% | $323 |
| W44 | **Difference** | **+45%** | **+456%** | **+333%** | **-74%** |
| W45 | NB Control | $56,790 | 55 | 3% | $1,033 |
| W45 | NB Test (OCI) | $66,182 | 253 | 13% | $262 |
| W45 | **Difference** | **+17%** | **+360%** | **+333%** | **-75%** |

The DE data illustrates the magnitude of OCI's impact: NB CPA dropped from $1,239 to $323 in the first test week, and from $1,033 to $262 in the second. This is not incremental improvement — it is a step-change in bidding efficiency.

### What Drove the Variance

UK performance was slightly below US due to EU DMA privacy restrictions limiting the data signals available to the bidding algorithm. DE was further impacted by privacy-driven variability in OCI values and higher cost-per-clicks (+27% vs. UK), which constrained efficient volume capture at scale. These learnings directly inform the EU4 rollout timeline — we are building longer stabilization windows into markets with DMA-driven data restrictions.

### Competitive Context

OCI's efficiency gains are strategically critical because they offset competitive pressure. In the US, Walmart Business has driven Brand CPA from ~$40 to $65-77. Rather than escalating bids, we absorb the Brand CPA increase through NB efficiency gains from OCI, keeping total program CPA healthy. This is a sustainable competitive response because it is based on algorithmic improvement, not budget escalation.

## 2026: RoW Expansion

| Market | Status | Launch Date | Full Impact (Projected) |
|--------|--------|-------------|-------------------------|
| CA | In Progress | Mar 2026 (E2E 3/4) | Jul 2026 |
| JP | In Progress | Feb 2026 (E2E 2/26) | Jul 2026 |
| FR | In Progress | Feb 2026 (E2E 2/26) | Jul 2026 |
| IT | In Progress | Feb 2026 (E2E 2/26) | Jul 2026 |
| ES | In Progress | Feb 2026 (E2E 2/26) | Jul 2026 |

Tech-readiness is complete in Q1 2026. The phased implementation and measurement framework developed in 2025 is the standard playbook for each new market. The privacy-related learnings from DE are directly informing milestone timelines for EU4 markets.

### Known Issue
Duplicate hvocijid parameters are appearing in landing page URLs across EU3 and existing markets, causing "Duplicate query param found" errors in event processing. JP is not affected. Under investigation with MarTech.

## Cross-Functional Partners
- MarTech (Joel Mallory): OCI implementation infrastructure, tracking, hvocijid investigation
- Data Science (Yogesh): OCI value framework, incrementality modeling
- Legal: Data flow approval for conversion data sent to Google
- Google (Mike Babich): Biweekly sync on OCI performance, learning phases, account structure
- Adobe (Suzane Huynh): OCI reporting feed, transition from Adobe bidding
