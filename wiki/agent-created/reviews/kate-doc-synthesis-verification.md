---
title: "Verification Review: Paid Search Testing Approach & Year Ahead"
status: DRAFT
audience: amazon-internal
owner: Richard Williams
created: 2026-04-12
updated: 2026-04-12
---
<!-- DOC-0479 | duck_id: wiki-review-kate-doc-synthesis-verification -->

# Verification Review: Paid Search Testing Approach & Year Ahead

**Reviewer:** wiki-critic (verification pass)
**Date:** 2026-03-25
**Document:** kate-doc-synthesis.md
**Previous review:** kate-doc-synthesis-final-review.md (7.8/10, REVISE)
**Scope:** Verify all 8 changes (R1-R3, S1-S5) landed correctly, re-score, render verdict.

---

## Change Verification

### R1: AGENT_CONTEXT block — ✅ VERIFIED

Present at end of document inside HTML comment. All six required fields present:

| Field | Present | Content Quality |
|-------|---------|----------------|
| machine_summary | ✅ | Rich, accurate. Covers all 5 workstreams with key metrics. Includes the compounding argument. |
| key_entities | ✅ | 12 entities. Includes Kate Rundell, all major projects, key partners. |
| action_verbs | ✅ | 5 verbs. Captures the doc's action orientation. |
| depends_on | ✅ | 9 section docs including kate-doc-appendix (correctly added beyond the 8 in frontmatter). |
| consumed_by | ✅ | Names Kate Rundell review, OP2 planning, Todd Heimes decision. Accurate audience mapping. |
| update_triggers | ✅ | 5 triggers. All actionable and specific. |

The synthesis is now consistent with every other doc in the 10-doc set. The `depends_on` in AGENT_CONTEXT (9 items) is a superset of the frontmatter `depends_on` (8 items) — the appendix was added. Minor inconsistency but acceptable: AGENT_CONTEXT is the richer reference and should include the appendix.

### R2: Executive summary replaces old opening — ✅ VERIFIED

First paragraph after the title:

> "In 2025, the Paid Search team's testing methodology delivered +35,196 incremental registrations and $16.7MM+ in OPS across US, UK, and DE — while building five compounding workstreams now ready to scale worldwide."

The old "This document establishes..." phrasing is completely gone. Kate gets the headline in the first sentence. The second paragraph retains the "transforming Paid Search" framing and cross-functional context — correctly repositioned as supporting narrative rather than the lead.

### R3: Methodology doc -45% fixed — ✅ VERIFIED

kate-doc-methodology.md measurement framework table now reads:

> `| Bidding changes (OCI) | Actualized CPA vs. seasonality-adjusted baseline | US: +24% reg lift, ~50% NB CPA improvement | Isolates OCI effect from seasonal patterns |`

Cross-checked against oci-performance.md source: "Non-Brand CPA improvement: ~50% during test vs control" — consistent. The synthesis OCI table also shows "~50% NB CPA improvement." All three docs now agree. The last cross-doc inconsistency is resolved.

### S1: Challenges and Risks section — ✅ VERIFIED

Present between Algorithmic Ads and Investment Summary (correct placement — before the ask, not after). Contains all four items specified:

| Item | Present | Accurate vs Source |
|------|---------|-------------------|
| DE -4% vs OP2 | ✅ "DE missed OP2 by 4%" | eyes.md: "Missed OP2 by 4%" ✅ |
| JP -47.5% vs OP2 | ✅ "JP is -47.5% vs OP2 after the MHLW campaign ended on 1/31" | eyes.md: "-47.5%" with MHLW context ✅ |
| F90 Legal blocker | ✅ "US LiveRamp 1P positive targeting approval is on track for April, but RoW expansion is blocked pending resolution of Tumble service requirements" | kate-doc-audiences.md language ✅ |
| hvocijid issue | ✅ "hvocijid duplicate parameters affecting EU3 and existing markets are under investigation" | oci-performance.md: "Duplicate hvocijid parameters... EU3 + existing markets... Under investigation" ✅ |

Closing sentence — "Each of these has a defined mitigation path, but none is resolved yet" — is honest without being alarmist. Good tone for Kate.

### S2: Capacity constraint quantified — ✅ VERIFIED

Operational Backbone section now includes:

> "...which spends approximately 25-30 hours per week on operational work — monitoring, reporting, budget management, and stakeholder coordination across 10 markets. The remaining capacity funds the five strategic workstreams."

This gives Kate the capacity math she needs for headcount or prioritization decisions. The number traces to kate-doc-operations.md.

### S3: Risk-of-not-investing sentence — ✅ VERIFIED

Present after the compounding paragraph in the Investment Summary:

> "The risk of not investing: OCI-eligible markets remain on deprecated Adobe bidding with no CPA improvement path, Baloo delays leave Shopping Ads unavailable for AB while competitors access them, and the Engagement infrastructure built in 2025 sits underutilized without F90 activation."

Three concrete consequences, each tied to a specific workstream. Kate can use this language directly with Todd.

### S4: OP2 connection — ✅ VERIFIED

Final sentence of the Investment Summary:

> "These investments directly support the PS team's OP2 registration and OPS commitments — the validated 2025 results provide the evidence base for the 2026 plan."

OP2 is now explicitly named and connected to the investment ask.

### S5: Gated Guest pivot story in UX section — ✅ VERIFIED

UX section now reads:


#### > "After the


> "After the Gated Guest experiment showed -61% registrations, the team paused, deep-dived the data, and pivoted to in-context registration — which delivered +13.6K annualized incremental registrations with 100% probability (APT)."


#### The failure-to-success arc


The failure-to-success arc is present. This is the strongest "we learn from failures" narrative in the doc and it's now visible in the workstream section, not just buried in methodology.

---

## Final Accuracy Spot-Check

Verified key claims against source data one more time:

| Claim | Synthesis | Source | Match |
|-------|-----------|--------|-------|
| +35,196 total regs | ✅ | oci-performance.md: 32,047 + 2,400 + 749 = 35,196 | ✅ |
| $16.7MM+ OPS | ✅ | oci-performance.md: 32,047 × $520 = $16.7MM | ✅ |
| US +24% reg lift | ✅ | oci-performance.md: "+24% reg lift" | ✅ |
| ~50% NB CPA improvement | ✅ (synthesis + methodology) | oci-performance.md: "~50% during test vs control" | ✅ |
| UK +86% CTR test-vs-control | ✅ | eyes.md: "+86% CTR" | ✅ |
| UK +31% regs | ✅ | eyes.md: "+31% regs" | ✅ |
| In-context +13.6K annualized | ✅ | kate-doc-ux.md reference | ✅ |
| DG $0.39 CPC | ✅ | kate-doc-algo-ads.md reference | ✅ |
| DE -4% vs OP2 | ✅ | eyes.md: "Missed OP2 by 4%" | ✅ |
| JP -47.5% vs OP2 | ✅ | eyes.md: "-47.5%" | ✅ |
| ~25-30 hrs/week operational | ✅ | kate-doc-operations.md reference | ✅ |

No unsupported claims. No cross-doc inconsistencies remaining.

---

## Re-Score

| Dimension | Previous | Now | Notes |
|-----------|----------|-----|-------|
| Usefulness | 8 | **9** | Executive summary gives Kate the headline in sentence one. Risk-of-not-investing gives her the negative case for Todd. OP2 connection ties the ask to commitments. Challenges section earns credibility. This is now a doc Kate can act on AND quote from. |
| Clarity | 9 | **9** | Already strong. The additions (Challenges section, capacity number, risk sentence) integrate cleanly without disrupting the structure. The Gated Guest pivot in UX strengthens the narrative arc. No regression. |
| Accuracy | 8 | **9** | The last cross-doc inconsistency (-45% in methodology) is resolved. All numbers now agree across synthesis, methodology, OCI doc, appendix, and source data. Every claim traces to a source. |
| Dual-audience | 6 | **8** | AGENT_CONTEXT block is present with all six fields. The machine_summary is the richest in the doc set — appropriate for the flagship synthesis. An agent can now index, retrieve, and reason over this doc. The gap to 9 would require structured data beyond the comment block (e.g., JSON-LD), which is outside the wiki standard. |
| Economy | 8 | **8** | The additions total ~150 words across 4 insertions. Each earns its place: Challenges section (credibility), capacity number (headcount argument), risk sentence (negative case), OP2 sentence (commitment tie). Nothing should be cut. Nothing was padded. |
| **Overall** | **7.8** | **8.6** | |

---

## Verdict: APPROVED FOR PUBLISHING ✅

Overall 8.6/10. No dimension below 8. Clears the 8/10 bar.

All three required changes landed correctly. All five suggestions were incorporated faithfully. The document is now:

1. **Kate-ready** — executive summary gives her the headline in 15 seconds, investment table gives her the full picture in 2 minutes, risk framing gives her the Todd conversation.
2. **Agent-ready** — AGENT_CONTEXT block makes this indexable, retrievable, and reasonable by the wiki system.
3. **Cross-doc consistent** — no conflicting numbers across the 10-doc set.

The compounding argument remains the single strongest insight in the entire doc set. The Challenges section and risk-of-not-investing framing are what separate "good doc" from "doc Kate uses to justify PS investment." Both are now present.

Ship it.

---

## What Would Push This to a 9

Not blocking — these are observations for future iterations:

1. **Quantified 2026 projections.** The 2025 results have confidence levels. The 2026 investments are presented as logical extensions but lack projected registration or OPS ranges. Even rough ranges ("replicate 15-25% reg uplift in RoW markets") would strengthen the ask.

2. **Capacity math made explicit.** The 25-30 hrs/week number is there, but the full math (280 hrs total → 25-30 ops → ~250 strategic → ~50/workstream across 10 markets) would make the headcount argument self-evident. One sentence would do it.

3. **Confidence levels on 2026 bets.** OCI RoW scaling has HIGH confidence (proven in 3 markets). Baloo is MEDIUM (new architecture, no test data yet). AI Max is LOW (no test design written). Stating this would match the methodology's own standards.

None of these block publishing. The doc clears the bar as-is.
