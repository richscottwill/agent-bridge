---
title: "Batch Critic Review — April 4, 2026"
status: DRAFT
audience: amazon-internal
owner: Richard Williams
created: 2026-04-12
updated: 2026-04-12
---
<!-- DOC-0461 | duck_id: wiki-review-batch-critic-review -->

# Batch Critic Review — April 4, 2026

> Wiki-critic review of all articles created or significantly modified on 2026-04-04.
> Scoring: 5 dimensions (Usefulness, Clarity, Accuracy, Dual-audience, Economy), 1-10 each.
> Threshold: PUBLISH >= 8 avg, no dimension below 7. REVISE >= 6 or any dimension below 7 but fixable.

---

## 1. F90 Lifecycle Strategy (expanded)

| Dimension | Score | Notes |
|-----------|-------|-------|
| Usefulness | 8/10 | Reader can understand the full program, dependencies, and launch plan. Actionable for anyone involved in F90. |
| Clarity | 8/10 | Four-stage workflow is clean. Dependency table is scannable. Risk matrix is practical. |
| Accuracy | 7/10 | Match rate numbers (13% to 30%) sourced. But "35.4% target" lacks the calculation methodology — where does +366 bps come from? The reader has to trust the number. |
| Dual-audience | 7/10 | AGENT_CONTEXT present. But frontmatter missing doc-type field. No update-trigger for "first cohort results" which is the most important trigger. |
| Economy | 7/10 | The "Strategic Context" section (connecting to Level 2, D6, D10) is useful but reads like justification rather than information. Could be one sentence instead of three paragraphs. |
| **Overall** | **7.4/10** | |

**Verdict: REVISE**

Required changes:
1. Add `doc-type: strategy` to frontmatter
2. Cut "Strategic Context" section to 2-3 sentences — the connections are valuable but the section is padded
3. Add source or methodology for the 35.4% target — "where does +366 bps come from?" needs an answer
4. Add "first cohort results available" to update-trigger in frontmatter
5. Every list item in the Dependencies section should start with a verb — "Legal SIMs: navigated" should be "Navigated Legal SIMs" or similar

---

## 2. Ad Copy Testing Framework (expanded)

| Dimension | Score | Notes |
|-----------|-------|-------|
| Usefulness | 9/10 | A teammate could replicate the test in a new market by following this doc. The template section is genuinely actionable. |
| Clarity | 8/10 | SP study data is well-presented. Phase structure is clean. Rollout tracker is scannable. |
| Accuracy | 8/10 | UK results sourced. IT results honestly flagged as LOW confidence. Copy changes mapped to SP study findings. |
| Dual-audience | 6/10 | AGENT_CONTEXT present but frontmatter is incomplete — missing doc-type. Sources section uses arrows instead of standard citation format. No structured tags in frontmatter. |
| Economy | 7/10 | The "Connection to Other Initiatives" section at the end feels tacked on. The SP study data is repeated from the workstream doc — some duplication. |
| **Overall** | **7.6/10** | |

**Verdict: REVISE**

Required changes:
1. Add `doc-type: strategy` to frontmatter
2. Add proper tags array to frontmatter
3. Integrate "Connection to Other Initiatives" into the relevant sections rather than a separate section at the end — OCI connection belongs in the methodology section, Polaris connection belongs in the localization section
4. Fix source citation format — use consistent `source: [path]` format, not arrows
5. The "Localization Protocol" table header says "Translation Method" — should say "Source" to match the column content

---

## 3. Email Overlay WW Rollout (expanded)

| Dimension | Score | Notes |
|-----------|-------|-------|
| Usefulness | 8/10 | Clear problem statement, technical architecture, and measurement framework. The single-point-of-failure analysis is the most useful section. |
| Clarity | 8/10 | Well-structured. The engagement destination table is practical. The blocker analysis is honest. |
| Accuracy | 7/10 | "15-25% of paid search clicks come from existing customers" is flagged as a directional estimate but presented in a way that could be mistaken for a fact. Needs clearer caveat. |
| Dual-audience | 6/10 | Missing doc-type in frontmatter. AGENT_CONTEXT present but update_triggers don't include "Adobe Ad Cloud segment delivered" which is the most important near-term trigger. |
| Economy | 8/10 | Tight. Every section earns its place. The dependency table is clean. |
| **Overall** | **7.4/10** | |

**Verdict: REVISE**

Required changes:
1. Add `doc-type: strategy` to frontmatter
2. Caveat the 15-25% estimate more clearly — add "(unvalidated — Adobe Ad Cloud reporting will provide the actual number)" or similar
3. Add "Adobe Ad Cloud segment delivered" to update_triggers in AGENT_CONTEXT
4. The measurement framework section should explicitly state that the baseline data doesn't exist yet — "this framework is ready to execute once the Adobe Ad Cloud segment is delivered"

---

## 4. AI Max Test Design (expanded)

| Dimension | Score | Notes |
|-----------|-------|-------|
| Usefulness | 9/10 | A teammate could set up and run this test by following the doc. Guardrails are specific and actionable. Open questions for Google sync are practical. |
| Clarity | 8/10 | Google automation progression is good framing. The 7-day consecutive rule is well-explained. Risk matrix is clean. |
| Accuracy | 8/10 | OCI comparison is well-calibrated. The 15% floor rationale is honest. Shopping Ads question is flagged appropriately. |
| Dual-audience | 6/10 | Missing doc-type in frontmatter. AGENT_CONTEXT present but the "OVERDUE" status in the body should also be reflected in frontmatter or a status field. |
| Economy | 7/10 | The "Why AI Max Matters" section is good but the 4-stage Google progression could be a table instead of a numbered list — more scannable. The risk assessment table has some overlap with the guardrails table. |
| **Overall** | **7.6/10** | |

**Verdict: REVISE**

Required changes:
1. Add `doc-type: strategy` to frontmatter
2. Convert the Google automation progression to a table for scannability
3. Deduplicate between guardrails table and risk assessment — the "CPA spikes during learning" risk is already covered by the guardrails. Either merge or cross-reference.
4. Add a "Plan to close the gap" sentence after the OVERDUE flag — "Google sync to be scheduled in first two weeks of Q2" or similar

---

## 5. Campaign Link Generator Spec (expanded)

| Dimension | Score | Notes |
|-----------|-------|-------|
| Usefulness | 8/10 | A developer could build v1 from this spec. The reftag convention is well-documented. Validation scenarios are practical. |
| Clarity | 8/10 | Clean structure. Input/output specs are clear. Implementation path is logical. |
| Accuracy | 8/10 | Reftag convention matches what's used in practice. Market domain mapping is correct. |
| Dual-audience | 6/10 | Missing doc-type in frontmatter. This is clearly an execution doc but isn't tagged as such. AGENT_CONTEXT present. |
| Economy | 8/10 | Tight for a tool spec. Every section earns its place. |
| **Overall** | **7.6/10** | |

**Verdict: REVISE**

Required changes:
1. Add `doc-type: execution` to frontmatter
2. The "Impact Estimate" table's "Reftag errors per quarter: 2-3 (estimated)" — either source this or flag it as an estimate more clearly
3. Add a "Definition of Done" section — when is v1 complete? When is v2 complete? The next steps are actions but there's no success criteria.

---

## 6. Budget Forecast Helper Spec (expanded)

| Dimension | Score | Notes |
|-----------|-------|-------|
| Usefulness | 8/10 | A developer could build this from the spec. The projection logic is clear. The blocker (OP2 numbers) is honestly flagged. |
| Clarity | 8/10 | Technical design section is clean. The architecture diagram (text-based) is helpful. |
| Accuracy | 7/10 | The projection logic is sound but the "trailing 4-week average" limitation (won't predict spikes) should be more prominent — it's buried in a parenthetical. |
| Dual-audience | 6/10 | Missing doc-type in frontmatter. AGENT_CONTEXT present. |
| Economy | 8/10 | Tight. The validation plan is practical without being over-specified. |
| **Overall** | **7.4/10** | |

**Verdict: REVISE**

Required changes:
1. Add `doc-type: execution` to frontmatter
2. Promote the trailing 4-week average limitation from a parenthetical to a "Known Limitations" section — this is important for anyone using the tool's output
3. Add a "Definition of Done" section with success criteria for v1

---

## 7. Q2 2026 Initiative Status (new)

| Dimension | Score | Notes |
|-----------|-------|-------|
| Usefulness | 9/10 | Brandon could use this directly for team management and upward reporting. The three-tier scorecard is immediately actionable. |
| Clarity | 8/10 | Well-structured. The "What's Working" and "What Needs Attention" sections are the right framing. |
| Accuracy | 8/10 | Initiative statuses match eyes.md and current.md. OCI count (7/10) is current. |
| Dual-audience | 7/10 | Missing doc-type in frontmatter. AGENT_CONTEXT present and useful. The "Key Dates" table is good for both audiences. |
| Economy | 7/10 | The narrative sections ("What's Working", "What Needs Attention") repeat information from the scorecard tables. Either cut the narrative or cut the tables — having both is redundant. |
| **Overall** | **7.8/10** | |

**Verdict: REVISE**

Required changes:
1. Add `doc-type: reference` to frontmatter
2. Cut the "What's Working" narrative to 2-3 sentences max — the scorecard already shows what's working. The narrative should add interpretation, not repeat the data.
3. Same for "What Needs Attention" — tighten to the "so what" only, not the full explanation (which is already in the scorecard's Risk/Blocker columns)

---

## 8. OCI Business Case (new)

| Dimension | Score | Notes |
|-----------|-------|-------|
| Usefulness | 9/10 | Brandon could hand this to Kate. The talking points section is exactly what's needed. |
| Clarity | 9/10 | Opens with the one-line story. DE proof point is well-placed. The "why it matters beyond the numbers" section is the strongest part. |
| Accuracy | 9/10 | Numbers match eyes.md. OCI status is current (7/10 at 100%). |
| Dual-audience | 7/10 | Missing doc-type in frontmatter. AGENT_CONTEXT present. |
| Economy | 8/10 | Tight for a leadership doc. The investment case table at the end is useful but the projections are clearly labeled as estimates. |
| **Overall** | **8.4/10** | |

**Verdict: PUBLISH**

Minor suggestions (non-blocking):
1. Add `doc-type: strategy` to frontmatter
2. The "Talking Points" section could include a "what NOT to say" — e.g., don't compare OCI markets to non-OCI markets directly

---

## 9. Team Workload Distribution (new)

| Dimension | Score | Notes |
|-----------|-------|-------|
| Usefulness | 9/10 | Brandon needs this. The coverage gap analysis and overload assessment are the most valuable sections. |
| Clarity | 8/10 | Well-structured. The market coverage map is scannable. The delegation opportunities table is practical. |
| Accuracy | 7/10 | Time estimates are directional ("4-5 hrs/wk") — these should be flagged as estimates, not presented as measured. The "16-24 hrs/wk" range for Richard is wide enough to be imprecise. |
| Dual-audience | 6/10 | Missing doc-type in frontmatter. AGENT_CONTEXT present. |
| Economy | 7/10 | The "Workload Distribution by Function" section has two tables (Campaign Management + Reporting) that could be merged into one. The "Delegation Opportunities" table includes tools that don't exist yet — should be clearly separated into "actionable now" vs "requires building." |
| **Overall** | **7.4/10** | |

**Verdict: REVISE**

Required changes:
1. Add `doc-type: reference` to frontmatter
2. Flag time estimates as estimates: "~4-5 hrs/wk (estimated)" not "4-5 hrs/wk"
3. Split delegation opportunities into "Actionable now" (invoice handoff to Lorena) vs "Requires building" (dashboard, tools)
4. Merge the two workload tables into one

---

## 10. Polaris Rollout Status (new)

| Dimension | Score | Notes |
|-----------|-------|-------|
| Usefulness | 8/10 | Good single-source-of-truth tracker. The decision log is valuable. |
| Clarity | 8/10 | Status table is clean. The AU full-switch risk analysis is honest. |
| Accuracy | 6/10 | The status table shows FR/IT/ES as "Pending EU5 ops ticket" but eyes.md shows them at 100% OCI (dialed up 3/30). The Polaris status may be different from OCI status, but this needs clarification — are FR/IT/ES Polaris pages pending or just OCI? The doc conflates the two. |
| Dual-audience | 7/10 | doc-type present (reference). AGENT_CONTEXT present. |
| Economy | 8/10 | Tight. Cross-initiative dependencies table is useful. |
| **Overall** | **7.4/10** | |

**Verdict: REVISE**

Required changes:
1. Clarify FR/IT/ES status — the OCI dial-up (3/30) is separate from Polaris LP rollout. Make sure the status table reflects Polaris LP status specifically, not OCI status.
2. Update the status table with current data from eyes.md and current.md
3. The "Measurement Framework" section's 45% CP threshold needs a source citation

---

## 11. Project Baloo Overview (new)

| Dimension | Score | Notes |
|-----------|-------|-------|
| Usefulness | 8/10 | Good overview for Brandon. The "What Brandon Needs to Know" section is exactly right. |
| Clarity | 8/10 | Well-structured. The cost comparison table is helpful. |
| Accuracy | 7/10 | "Shopping Ads account for roughly 60-65% of all Google Ads clicks in retail e-commerce" — this is industry knowledge without a source. Either cite it or caveat it. |
| Dual-audience | 6/10 | Missing doc-type in frontmatter. AGENT_CONTEXT present. |
| Economy | 7/10 | The proposed test design is speculative — the 150% CPA guardrail and $5-10K/week budget are placeholders. This should be clearly labeled as "proposed, pending Google sync" rather than presented as a plan. |
| **Overall** | **7.2/10** | |

**Verdict: REVISE**

Required changes:
1. Add `doc-type: strategy` to frontmatter
2. Cite or caveat the 60-65% Shopping Ads claim
3. Label the test design section as "Proposed — Pending Cost Guardrail Finalization" rather than just "Proposed"
4. The open questions table should include "Who owns Baloo long-term?" as the first question, not the fourth — ownership is the most important open question for Brandon

---

## 12. OCI Execution Guide (new, consolidated)

| Dimension | Score | Notes |
|-----------|-------|-------|
| Usefulness | 9/10 | A teammate could implement OCI in a new market by following this doc. The "What NOT to Do" section is the most valuable part. |
| Clarity | 9/10 | Step-by-step is clean. Troubleshooting table is comprehensive. Per-market notes are practical. |
| Accuracy | 8/10 | Market statuses are current. Gate criteria match brain.md D1. |
| Dual-audience | 7/10 | doc-type present (execution). AGENT_CONTEXT present. |
| Economy | 8/10 | Good consolidation of three docs into one. No significant duplication. |
| **Overall** | **8.2/10** | |

**Verdict: PUBLISH**

Minor suggestions (non-blocking):
1. The "Current Market Status" table at the bottom duplicates the "Per-Market Notes" table above it. Consider merging into one table with status + notes columns.

---

## 13. AU Market Wiki (merged)

| Dimension | Score | Notes |
|-----------|-------|-------|
| Usefulness | 9/10 | Canonical AU reference. A teammate covering AU could get up to speed from this doc alone. |
| Clarity | 8/10 | Well-structured. The CPC Challenge section is the right level of detail. |
| Accuracy | 8/10 | Performance data matches eyes.md. Stakeholder dynamics match memory.md. |
| Dual-audience | 7/10 | doc-type present (reference). AGENT_CONTEXT present. Tags present. |
| Economy | 8/10 | Good merge of two docs. No significant duplication. |
| **Overall** | **8.0/10** | |

**Verdict: PUBLISH**

No required changes. Clean merge.

---

## 14. MX Market Wiki (merged)

| Dimension | Score | Notes |
|-----------|-------|-------|
| Usefulness | 8/10 | Canonical MX reference with Lorena onboarding context integrated. |
| Clarity | 8/10 | Well-structured. Active issues in priority order is the right approach. |
| Accuracy | 8/10 | Performance data matches eyes.md. Stakeholder info is current. |
| Dual-audience | 7/10 | doc-type present (reference). AGENT_CONTEXT present. Tags present. |
| Economy | 8/10 | Good merge. Handoff guide content integrated naturally. |
| **Overall** | **7.8/10** | |

**Verdict: REVISE (barely)**

Required changes:
1. The ie%CCP reference should link to the ie%CCP Planning Framework doc — currently just mentions it in the overview without a link

---

## 15. WW Testing Tracker (rewritten)

| Dimension | Score | Notes |
|-----------|-------|-------|
| Usefulness | 9/10 | The portfolio health narrative and blocker analysis transform this from a spreadsheet into a useful doc. |
| Clarity | 9/10 | Well-structured. The "What's Blocked and Why" table is the most valuable addition. |
| Accuracy | 7/10 | The active tests table shows JP/FR/IT/ES as "100% live" for OCI but the "Active Tests" framing implies these are still being tested. They should be moved to "Completed" or the table should distinguish between "monitoring lift" and "active test." |
| Dual-audience | 7/10 | doc-type present (reference). AGENT_CONTEXT present. |
| Economy | 8/10 | The "Test Pipeline by Workstream" table at the bottom is a nice addition — shows the portfolio shape at a glance. |
| **Overall** | **8.0/10** | |

**Verdict: PUBLISH**

Minor suggestion: Move FR/IT/ES/JP OCI from "Active Tests" to "Completed Tests" since they're at 100% live. Keep CA in Active since it's still in E2E.

---

## Summary

| Article | Score | Verdict |
|---------|-------|---------|
| F90 Lifecycle Strategy | 7.4 | REVISE |
| Ad Copy Testing Framework | 7.6 | REVISE |
| Email Overlay WW Rollout | 7.4 | REVISE |
| AI Max Test Design | 7.6 | REVISE |
| Campaign Link Generator Spec | 7.6 | REVISE |
| Budget Forecast Helper Spec | 7.4 | REVISE |
| Q2 Initiative Status | 7.8 | REVISE |
| OCI Business Case | 8.4 | PUBLISH |
| Team Workload Distribution | 7.4 | REVISE |
| Polaris Rollout Status | 7.4 | REVISE |
| Project Baloo Overview | 7.2 | REVISE |
| OCI Execution Guide | 8.2 | PUBLISH |
| AU Market Wiki | 8.0 | PUBLISH |
| MX Market Wiki | 7.8 | REVISE |
| WW Testing Tracker | 8.0 | PUBLISH |

**4 PUBLISH, 11 REVISE, 0 REJECT**

The most common issues across REVISE articles:
1. Missing `doc-type` in frontmatter (10 of 11 REVISE articles)
2. Unsourced or under-caveated estimates presented as facts
3. Economy violations — sections that repeat information already in tables
4. Dual-audience gaps — AGENT_CONTEXT present but frontmatter incomplete
