<!-- DOC-0473 | duck_id: wiki-review-kate-doc-batch-review -->
# Batch Review: Kate Doc — Paid Search Testing Approach & Year Ahead

Reviewer: wiki-critic
Date: 2026-03-25
Mode: 1 (pre-publish review)
Audience: Kate Rundell (L8 Director)
Standard: Amazon narrative writing — data-embedded, no filler, every claim traceable

---

## 1. kate-doc-methodology.md — "How We Test"

### Scores
| Dimension | Score | Notes |
|-----------|-------|-------|
| Usefulness | 8/10 | Establishes the operating system for the entire doc. Kate can see the discipline, not just the results. |
| Clarity | 9/10 | Four-stage framework is clean and scannable. Tables reinforce without cluttering. |
| Accuracy | 8/10 | SyRT data, OCI phases, ad copy results, Gated Guest failure — all verified against eyes.md and ad-copy-results.md. One minor issue: "CA Bulk CVR +187%" in the text but the source data shows +186.6%. Rounding is acceptable but should be consistent with the UX section. |
| Dual-audience | 6/10 | No AGENT_CONTEXT block. Frontmatter is present but minimal — no `depends_on`, `consumed_by`, or `update_triggers`. An agent indexing this doc would miss the cross-references. |
| Economy | 8/10 | Tight. The "Why This Matters" closing paragraph earns its place by connecting methodology to the compounding effect across workstreams. |
| **Overall** | **7.8/10** | |

### Verdict
**PUBLISH**

### Suggestions (non-blocking)
- Add AGENT_CONTEXT block with `depends_on` (all 5 workstream docs), `update_triggers` (new test methodology adopted, new measurement framework), and `consumed_by` (kate-doc-synthesis).
- The SyRT section is strong. Consider adding the test period (Q2 2023) to the table header row for immediate context — a reader scanning the table might miss it in the prose above.
- "JP Bulk LP: 5.8% chance of outperforming control via Bayesian analysis" — excellent stop-signal example. This is the kind of specificity Kate will appreciate.

---

## 2. kate-doc-oci.md — "Workstream 1: Intelligent Bidding (OCI)"

### Scores
| Dimension | Score | Notes |
|-----------|-------|-------|
| Usefulness | 9/10 | The strongest section in the batch. Kate can see the full arc: problem → phased rollout → validated results → competitive offset → RoW expansion. Actionable and strategic. |
| Clarity | 8/10 | Well-structured. The DE test vs. control table is powerful. Minor: "What Drove the Variance" section could use a clearer header — it reads like a sub-explanation rather than a standalone insight. |
| Accuracy | 7/10 | **Issue 1:** The table shows US NB CPA improvement as "-45%" but oci-performance.md says "~50% NB CPA" improvement. The doc should use "~50%" or cite the specific source for -45%. **Issue 2:** The table shows US estimated regs as "+32,047" — oci-performance.md confirms this is actual + Nov (19.1K + 7,853 + additional = 32,047). Correct but the doc says "Jul-Oct 2025" as the test period while the 32K number includes November. The test period label is misleading. **Issue 3:** UK and DE NB CPA improvements ("-38%" and "-37%") are not in oci-performance.md — these appear to be inferred or from another source. Should be flagged as estimates or sourced. |
| Dual-audience | 6/10 | No AGENT_CONTEXT block. Frontmatter tags are good but missing `depends_on`, `consumed_by`, `update_triggers`. |
| Economy | 8/10 | Every section earns its place. The competitive context paragraph is essential — it connects OCI to the Walmart response strategy. |
| **Overall** | **7.6/10** | |

### Verdict
**REVISE**

### Required Changes

**Change 1: Fix US test period vs. reg count mismatch**

> | US | Jul-Oct 2025 | +24% | -45% | +32,047 | $16.7MM |

Replace with:

> | US | Jul-Nov 2025 | +24% | ~50% | +32,047 | $16.7MM |

Rationale: oci-performance.md shows 19.1K regs as of 10/31 plus 7,853 in November. The 32,047 total includes November. The test period must reflect this. The CPA improvement should match the source ("~50%").

**Change 2: Flag UK/DE CPA improvements as estimates**

> | UK | Aug-Oct 2025 | +23% | -38% | +2,400 | — |
> | DE | Oct-Dec 2025 | +18% | -37% | +749 | — |

Replace with:

> | UK | Aug-Oct 2025 | +23% | Significant | +2,400 | — |
> | DE | Oct-Dec 2025 | +18% | Significant | +749 | — |

Rationale: oci-performance.md uses "Significant" for UK and DE NB CPA improvement, not specific percentages. If the -38% and -37% come from a different source, add a footnote. Otherwise, match the source.

**Change 3: Add "% to Expectation" column**

The source data includes this metric (US 96%, UK 94%, DE 86%) and it's referenced in the prose. Add it to the table for traceability.

### Suggestions (non-blocking)
- The "Known Issue" section on hvocijid is good operational transparency. Kate will appreciate knowing about active risks.
- Consider adding a one-line note on AU/MX exclusion rationale — Kate may ask why two markets are "Not planned."

---

## 3. kate-doc-modern-search.md — "Workstream 2: Modern Search"

### Scores
| Dimension | Score | Notes |
|-----------|-------|-------|
| Usefulness | 8/10 | The SP study insight is the star — 50% believed AB required bulk purchasing. This is the kind of customer research that changes strategy. Kate will remember this. |
| Clarity | 8/10 | Clean structure. The before/after ad copy table is immediately scannable. |
| Accuracy | 9/10 | All numbers verified against ad-copy-results.md. UK pre/post data matches exactly. IT data matches. SP study percentages match. CTR "+86%" is the test-vs-control metric, "+70%" is pre/post — both correctly labeled. |
| Dual-audience | 6/10 | No AGENT_CONTEXT block. Same frontmatter gap as other docs. |
| Economy | 8/10 | The three SP study tables could arguably be condensed into one, but they serve different analytical purposes (what matters, what doesn't, why they didn't sign up). Keeping them separate is defensible. |
| **Overall** | **7.8/10** | |

### Verdict
**PUBLISH**

### Suggestions (non-blocking)
- The "Connection to Competitive Strategy" section is strong — it ties ad copy to the efficiency-over-escalation principle. This is the kind of strategic framing Kate expects.
- The campaign consolidation section is thinner than the ad copy section. If there's quantitative data on campaign count reduction or data density improvement, add it. Otherwise, it reads as assertion without evidence.
- Add AGENT_CONTEXT block.

---

## 4. kate-doc-audiences.md — "Workstream 3: Audiences"

### Scores
| Dimension | Score | Notes |
|-----------|-------|-------|
| Usefulness | 8/10 | The progression from LiveRamp → Engagement → F90 is clear and strategic. Kate can see the team extending PS beyond acquisition. |
| Clarity | 8/10 | Well-structured phases. The match rate table is simple and effective. |
| Accuracy | 7/10 | **Issue:** The doc says Google match rate went from "12-13%" to "30%." Eyes.md confirms "13% to 30%." The "12-13%" range is slightly imprecise — the source consistently says 13%. **Issue 2:** "$765K in iOPS in 2025" — this number appears in the doc but is not in eyes.md or the other reference files. It's likely from a Flash or MBR source. Should be footnoted. **Issue 3:** "80K clicks at -10% cost YoY, generating $329K in OPS at a 644% ROAS — a 12x improvement over the prior year" — these numbers are consistent across docs but the original source is not cited. |
| Dual-audience | 6/10 | No AGENT_CONTEXT block. |
| Economy | 7/10 | The "What We Learned" section has three bullet points that are insightful but slightly verbose. Could be tightened. |
| **Overall** | **7.2/10** | |

### Verdict
**PUBLISH**

### Suggestions (non-blocking)
- Tighten "12-13%" to "13%" to match the source data consistently.
- The F90 section is forward-looking and appropriately caveated with Legal status. Good.
- The Demand Gen CPC comparison ($0.39 vs $2.43) appears here AND in the Algorithmic Ads section. Consider whether it belongs in one place or both — currently it's split across Audiences (briefly) and Algo Ads (in detail). The Audiences doc mentions it in "What We Learned" point 3 but the detail lives in Algo Ads. This is acceptable but creates a minor duplication risk.

---

## 5. kate-doc-ux.md — "Workstream 4: User Experience"

### Scores
| Dimension | Score | Notes |
|-----------|-------|-------|
| Usefulness | 8/10 | Strong. The 85% drop-off stat is a powerful opening. In-context registration results are compelling. Baloo is well-positioned as the 2026 anchor. |
| Clarity | 8/10 | Good structure. The CA LP table is clean. The Polaris rollout status is clear. |
| Accuracy | 8/10 | CA CVR numbers match eyes.md (+186.6% and +180%). In-context reg "+13.6K annualized" is consistent across docs. MCS Flash data (Nov-Dec 2025) numbers are present but the "+235 bps" and "+635 bps" claims need verification — they appear in the doc but the source (MCS Flash) is cited. The Polaris switch date (3/24) matches current.md. |
| Dual-audience | 6/10 | No AGENT_CONTEXT block. |
| Economy | 7/10 | The 2026 initiatives table has 6 items — some are well-defined (Baloo, EU5 LP framework) and some are thin (Guest auto-expiration, BIOAB). The thin ones risk looking like padding. |
| **Overall** | **7.4/10** | |

### Verdict
**PUBLISH**

### Suggestions (non-blocking)
- The Gated Guest failure story is well-told — "-61% registrations" is a powerful data point that shows the team's willingness to stop what doesn't work. This is exactly what Kate wants to see.
- The 2026 table could be trimmed to the 3-4 highest-impact items. Guest auto-expiration and email overlay WW scale are operational improvements, not strategic investments at the same level as Baloo or Aladdin.
- Add AGENT_CONTEXT block.

---

## 6. kate-doc-algo-ads.md — "Workstream 5: Algorithmic Ads"

### Scores
| Dimension | Score | Notes |
|-----------|-------|-------|
| Usefulness | 7/10 | Solid but thinner than the other workstream docs. DG performance data is good. AI Max is appropriately positioned as upcoming. |
| Clarity | 7/10 | Clean structure. The Q4 2025 YoY table is effective. |
| Accuracy | 8/10 | DG CPC ($0.39 vs $2.43), Q4 YoY numbers (+53% traffic, -35% spend, -58% CPC), Prime Day numbers (80K clicks, $329K OPS, 644% ROAS) — all consistent with eyes.md appendix data. BSE 52K visitors at $0.30 CPC is consistent. |
| Dual-audience | 6/10 | No AGENT_CONTEXT block. |
| Economy | 7/10 | The doc is appropriately sized for the workstream's maturity. AI Max is pre-test, so there's less to say. The "Test design due: March 28, 2026" line is good operational specificity. |
| **Overall** | **7.0/10** | |

### Verdict
**PUBLISH**

### Suggestions (non-blocking)
- The Prime Day data appears in both this doc and the Audiences doc. Decide which section owns it. Currently it's in both because Prime Day used Engagement campaigns (Audiences) with DG format (Algo Ads). A cross-reference note would resolve the ambiguity.
- The AI Max section could be strengthened with a brief note on what specific risks the guardrails are designed to prevent (cannibalization of existing keyword performance is mentioned — good — but what does "expanded reach" mean concretely for AB?).
- Add AGENT_CONTEXT block.

---

## 7. kate-doc-team-map.md — "Team Map & Cross-Functional Scope"

### Scores
| Dimension | Score | Notes |
|-----------|-------|-------|
| Usefulness | 7/10 | Useful for Kate to see the full scope of what the team does. The "What We Also Do Beyond Paid Search" table is the key value — it makes the invisible work visible. |
| Clarity | 8/10 | Well-organized tables. The stakeholder interaction map is immediately useful. |
| Accuracy | 7/10 | **Issue:** The doc lists "Aditya Thakur" but org-chart.md shows "Aditya Satish Thakur" with alias "aditthk." The shortened name is fine for the table but should be consistent with how the org refers to him. **Issue 2:** Carlos Palmos is listed nowhere in this doc, but current.md notes he "transitioned to CPS ~3/17" — correct to exclude him. Lorena is correctly listed as MX PS stakeholder. **Issue 3:** The doc says "seven people" for PS function but the table lists 7 people including Brandon (who is the manager of the broader team, not just PS). If Peter Ocampo is excluded from the PS count, the PS-specific headcount is 6 ICs + 1 manager = 7. This is correct. |
| Dual-audience | 6/10 | No AGENT_CONTEXT block. |
| Economy | 7/10 | The "Scope in Perspective" closing section is slightly redundant with the tables above it — the tables already make the point. Could be cut to 2 sentences. |
| **Overall** | **7.0/10** | |

### Verdict
**PUBLISH**

### Suggestions (non-blocking)
- The stakeholder map is the most valuable part of this doc for Kate. She can see exactly who the team interfaces with and how often.
- The "What We Do for Paid Search" table's Owner(s) column is very useful — it shows workload distribution across the team. Kate will appreciate this.
- The closing "Scope in Perspective" section repeats the "connective tissue" metaphor from the opening. Cut the repetition.

---

## 8. kate-doc-operations.md — "PS Operations"

### Scores
| Dimension | Score | Notes |
|-----------|-------|-------|
| Usefulness | 7/10 | Makes the operational backbone visible. The "Operational Rhythm in Numbers" table is the key deliverable — Kate can see the time investment. |
| Clarity | 8/10 | Well-structured by cadence (daily → weekly → biweekly → monthly → quarterly). Easy to scan. |
| Accuracy | 7/10 | **Issue:** "AU target is ~$140" — eyes.md confirms "$140 target" for AU. Correct. **Issue 2:** "PO matching (Google Ireland Ltd PO 5LN2R - 5489247319)" — this is operational detail that may be too granular for a Kate-facing doc. It's accurate per current.md but feels out of place. **Issue 3:** "OFA approvals (e.g., invoices 5511928883, 5508024310)" — same concern. These are real invoice numbers from current.md but they're operational noise in a strategic document. |
| Dual-audience | 5/10 | No AGENT_CONTEXT block. The doc is heavily human-oriented (operational procedures) with no agent-indexable structure beyond frontmatter. |
| Economy | 6/10 | This is the weakest doc on economy. The invoice/PO details, specific OFA approval numbers, and "Google Ireland Ltd PO 5LN2R" are too granular for Kate. The quarterly section is thin — just bullet points without data. The "Why This Matters" closing repeats the same point made in the opening paragraph. |
| **Overall** | **6.6/10** | |

### Verdict
**REVISE**

### Required Changes

**Change 1: Remove specific invoice/PO numbers**

> - PO matching (Google Ireland Ltd PO 5LN2R - 5489247319)
> - OFA approvals (e.g., invoices 5511928883, 5508024310)

Replace with:

> - PO matching and OFA approvals for Google Ads media spend

Rationale: Kate does not need invoice numbers. This is operational detail that belongs in a runbook, not a strategic document.

**Change 2: Remove or condense the "Why This Matters" closing**

> The strategic work gets the headlines. The operational work makes the strategic work possible. Both require discipline, and both are delivered by the same seven-person team.

This exact sentiment appears in the opening paragraph:

> The strategic work described in this document — OCI rollout, ad copy testing, audience expansion, landing page optimization, algorithmic ads — runs on top of a consistent operational foundation.

Cut the closing paragraph entirely. The opening already makes the point.

**Change 3: Strengthen the quarterly section**

The quarterly section is just four bullet points with no data or specificity. Either add concrete examples (e.g., "Q4 2025 test portfolio review resulted in stopping JP Bulk LP and scaling CA LP framework to EU5") or merge the quarterly items into the monthly section.

### Suggestions (non-blocking)
- The "Operational Rhythm in Numbers" table is the strongest element. Lead with it or make it more prominent.
- Add AGENT_CONTEXT block with `update_triggers: ["new recurring meeting added", "cadence change", "team member change"]`.

---

## 9. kate-doc-appendix.md — "Appendix: Supporting Evidence"

### Scores
| Dimension | Score | Notes |
|-----------|-------|-------|
| Usefulness | 7/10 | Serves its purpose as an evidence locker. Every table is traceable to a source. The 2026 Investment Summary (Section H) is the most useful table in the entire batch — it's the one Kate will reference most. |
| Clarity | 7/10 | Well-organized by section (A-J). Headers are clear. |
| Accuracy | 8/10 | Extensive cross-check performed. OCI timeline matches oci-performance.md. Ad copy data matches ad-copy-results.md. Competitive data matches eyes.md. Market performance matches eyes.md. Team roster matches org-chart.md. MCC IDs match. **One issue:** Section A.2 shows US NB CPA improvement as "-45%" — same issue as the OCI doc. Should be "~50%" per oci-performance.md. |
| Dual-audience | 7/10 | The appendix is inherently agent-friendly — structured tables with consistent formatting. No AGENT_CONTEXT block but the structure compensates. |
| Economy | 6/10 | This is an exhaustive data dump by design, but some tables duplicate the main workstream docs verbatim (e.g., B.1 SP Study Findings is identical to the Modern Search doc's tables, B.3 UK results are identical). The appendix should contain data that ISN'T in the main docs, or it should be the single source with the main docs referencing it. Currently it's both, which creates a maintenance burden. |
| **Overall** | **7.0/10** | |

### Verdict
**REVISE**

### Required Changes

**Change 1: Fix US NB CPA improvement to match source**

In Section A.2:

> | US | Jul-Oct 2025 | +24% | -45% | +32,047 | $16.7MM | 96% |

Replace with:

> | US | Jul-Nov 2025 | +24% | ~50% | +32,047 | $16.7MM | 96% |

Same fix as the OCI doc — test period should include November since the reg count does, and CPA improvement should match oci-performance.md.

**Change 2: Add a note on appendix vs. main doc relationship**

Add after the opening paragraph:

> Tables in this appendix provide the complete data behind the summary figures in each workstream section. Where a workstream section shows a summary table, this appendix contains the full dataset with additional detail columns.

This clarifies the relationship and reduces the perception of duplication.

### Suggestions (non-blocking)
- Section J (Source Documents) is excellent. The Quip links, wiki pages, and email flash references give Kate (or anyone) a clear audit trail.
- The cross-team contact list (Section I) duplicates the team-map doc. Consider whether it belongs in one place or both.

---

## 10. kate-doc-synthesis.md — "Paid Search Testing Approach & Year Ahead"

### Scores
| Dimension | Score | Notes |
|-----------|-------|-------|
| Usefulness | 9/10 | This is the doc Kate will actually read. It synthesizes all five workstreams into a single narrative with the investment summary table as the anchor. The opening paragraph positions the team exactly right — "transforming from keyword-driven acquisition to automated, audience-centric engine." |
| Clarity | 9/10 | Excellent structure. Each workstream gets a tight summary with the key data point. The investment summary table is the payoff. |
| Accuracy | 7/10 | Inherits the OCI accuracy issues from the standalone doc (US test period, NB CPA percentage). Additionally: **Issue:** The synthesis says "UK Results (Phase 1, Jan 29 - Mar 2, 2026)" with CTR change of "+70%" — this is the pre/post metric. The test-vs-control CTR change is "+86%." The summary header says "+86% CTR" (from the Modern Search summary tag) but the table shows "+70%." Both are correct but they measure different things. The synthesis should clarify which metric it's presenting. **Issue 2:** The 2026 Investment Summary table shows "OCI Bidding: +24% reg uplift; -45% NB CPA" — should be "~50%" per source. |
| Dual-audience | 7/10 | Has `depends_on` in frontmatter — the only doc in the batch that does. No AGENT_CONTEXT block but the frontmatter is richer than the other docs. |
| Economy | 8/10 | Tight for a synthesis doc. Each workstream section is appropriately compressed. The team section and operational backbone are brief but sufficient. The closing "Appendix" reference is clean. |
| **Overall** | **8.0/10** | |

### Verdict
**REVISE**

### Required Changes

**Change 1: Fix OCI data consistency**

In the Workstream 1 summary table:

> | US | +24% | -45% | +32,047 | $16.7MM |

Replace with:

> | US | +24% | ~50% | +32,047 | $16.7MM |

And in the 2026 Investment Summary:

> | OCI Bidding | +24% reg uplift; -45% NB CPA; +35K regs / $16.7MM OPS | Scale to FR, IT, ES, CA, JP (Jul 2026) | Replicate double-digit reg uplift in RoW |

Replace with:

> | OCI Bidding | +24% reg uplift; ~50% NB CPA improvement; +35K regs / $16.7MM OPS | Scale to FR, IT, ES, CA, JP (Jul 2026) | Replicate double-digit reg uplift in RoW |

**Change 2: Clarify UK CTR metric in Modern Search summary**

> | CTR | 14% | 24% | **+70%** |

Add a note below the table:

> Pre/post comparison. Test-vs-control CTR improvement was +86% over the same period.

This prevents Kate from seeing "+86% CTR" in the summary tag and "+70%" in the table and wondering which is correct. Both are — they measure different things.

### Suggestions (non-blocking)
- The opening paragraph is the strongest writing in the entire batch. "Grounded in evidence rather than speculation" — this is exactly the positioning Kate needs to hear.
- The compounding paragraph at the end of the investment summary is excellent: "campaign consolidation strengthens OCI signals, OCI enables smarter bidding on the audiences the Engagement channel reaches, and Baloo creates the friction-free landing experience that AI Max's dynamic page selection requires." This is the strategic insight that ties everything together.
- Consider adding a one-paragraph executive summary at the very top — 3-4 sentences that give Kate the headline before she reads the full doc. Something like: "In 2025, the PS team validated five workstreams that collectively drove +35K incremental registrations and $16.7MM+ in OPS. Every 2026 investment maps to a validated 2025 result. This document presents the testing methodology, results, and 2026 roadmap."

---

## Batch Summary

| Doc | Overall | Verdict | Key Issue |
|-----|---------|---------|-----------|
| kate-doc-methodology | 7.8 | PUBLISH | Missing AGENT_CONTEXT |
| kate-doc-oci | 7.6 | REVISE | US test period/CPA mismatch with source; UK/DE CPA unverified |
| kate-doc-modern-search | 7.8 | PUBLISH | Campaign consolidation section thin on evidence |
| kate-doc-audiences | 7.2 | PUBLISH | $765K iOPS source not in reference files |
| kate-doc-ux | 7.4 | PUBLISH | 2026 table has some thin items |
| kate-doc-algo-ads | 7.0 | PUBLISH | Thinnest workstream doc; appropriate given pre-test status |
| kate-doc-team-map | 7.0 | PUBLISH | Closing section redundant |
| kate-doc-operations | 6.6 | REVISE | Invoice/PO noise; weak quarterly section; redundant closing |
| kate-doc-appendix | 7.0 | REVISE | OCI data inconsistency; duplication with main docs unclear |
| kate-doc-synthesis | 8.0 | REVISE | Inherits OCI accuracy issues; UK CTR metric ambiguity |

**4 docs need revision. 6 are ready to publish.**

The batch is strong. The synthesis doc is the best piece — it reads like a document Richard would be proud to put in front of Kate. The methodology doc is the second strongest — it establishes credibility before the results. The OCI accuracy issues are the most important fix because they cascade across three docs (OCI, appendix, synthesis).

### Cross-Batch Issues (apply to all docs)

1. **No AGENT_CONTEXT blocks anywhere.** Every doc should have one. This is a systematic gap that the wiki-writer should address in a single pass.
2. **The "-45% NB CPA" figure appears in 3 docs** but the source says "~50%." Fix it once in the OCI doc and cascade to appendix and synthesis.
3. **The US OCI test period is labeled "Jul-Oct 2025"** but the reg count includes November data. Fix it once and cascade.
