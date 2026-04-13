---
title: "Batch Review: Five Workstream Articles — Eval A"
status: DRAFT
audience: amazon-internal
owner: Richard Williams
created: 2026-04-12
updated: 2026-04-12
---
<!-- DOC-0459 | duck_id: wiki-review-batch-5-workstreams-eval-a -->

# Batch Review: Five Workstream Articles — Eval A

Reviewer: wiki-critic | Date: 2026-04-05 | Mode: Blind Eval A
Appendix exempted from Economy scoring per instruction.

---

## Summary Table

| Article | Usefulness | Clarity | Accuracy | Dual-audience | Economy | Avg | Verdict |
|---------|-----------|---------|----------|---------------|---------|-----|---------|
| WS1: OCI Bidding | 9 | 9 | 8 | 9 | 8 | 8.6 | PUBLISH |
| WS2: Modern Search | 9 | 9 | 8 | 9 | 8 | 8.6 | PUBLISH |
| WS3: Audiences & Lifecycle | 9 | 9 | 8 | 9 | 7 | 8.4 | REVISE |
| WS4: User Experience | 8 | 8 | 8 | 9 | 7 | 8.0 | REVISE |
| WS5: Algorithmic Ads | 8 | 8 | 7 | 9 | 7 | 7.8 | REVISE |

---

## WS1: Intelligent Bidding (OCI) — PUBLISH (8.6)

| Dimension | Score | Notes |
|-----------|-------|-------|
| Usefulness | 9/10 | Reader understands the problem, the validated results, the scaling plan, and the risks — can brief Kate or make a market-level decision immediately |
| Clarity | 9/10 | Question-driven headers tell the full story; each section answers exactly one question with no re-reading needed |
| Accuracy | 8/10 | Numbers are sourced and dated; UK OPS figure is missing ("—" in the table) but acknowledged implicitly by market size context |
| Dual-audience | 9/10 | Rich YAML frontmatter, AGENT_CONTEXT with machine_summary, key_entities, action_verbs, and update_triggers — both audiences fully served |
| Economy | 8/10 | Tight narrative prose throughout the main body; data embedded in sentences; no bullet list abuse; every section earns its place |
| **Overall** | **8.6** | |

### Suggestions (non-blocking)
- The competitive strategy section ("OCI's efficiency gains are strategically critical because they offset competitive pressure") could embed the Walmart CPA numbers more tightly into the preceding sentence rather than introducing them as a separate thought. Minor.
- Consider adding a confidence tag to the DE privacy impact projection ("we should expect EU4 markets to track closer to DE's 86%") — this is a forward-looking claim based on one market's data. MEDIUM confidence would be honest.

---

## WS2: Modern Search — PUBLISH (8.6)

| Dimension | Score | Notes |
|-----------|-------|-------|
| Usefulness | 9/10 | The SP study insight (50% misconception) is immediately actionable; the ad copy mapping is a repeatable playbook; the reader can brief Kate or replicate the methodology |
| Clarity | 9/10 | Question-driven headers; the SP study → ad copy → test results → scaling flow is logical and scannable |
| Accuracy | 8/10 | UK test data is specific and dated; IT test honestly flagged as LOW confidence; SP study sourced to August 2025 |
| Dual-audience | 9/10 | Full frontmatter, AGENT_CONTEXT with update_triggers, depends_on chain to OCI — agent can index and reason over cross-workstream dependencies |
| Economy | 8/10 | Prose-driven; data embedded in narrative; the SP study data is in the appendix where it belongs with the main body carrying the insight |
| **Overall** | **8.6** | |

### Suggestions (non-blocking)
- "Keyword theme consolidation continues worldwide as part of the OCI rollout to RoW, combining campaign keyword themes to further reduce campaign count and strengthen data signals" — the phrase "combining campaign keyword themes to further reduce campaign count" restates what "keyword theme consolidation" already means. Trim to: "Keyword theme consolidation continues worldwide as part of the OCI rollout to RoW, strengthening data signals for each bid strategy."
- The GlobalLink submission ID (2028024) is useful for traceability but could go in the appendix to keep the scaling section tighter.

---

## WS3: Audiences & Lifecycle — REVISE (8.4)

| Dimension | Score | Notes |
|-----------|-------|-------|
| Usefulness | 9/10 | Three-phase audience strategy is clear and actionable; F90 plan is well-scoped with specific targets |
| Clarity | 9/10 | Logical progression from problem → infrastructure → results → next phase; question headers work well |
| Accuracy | 8/10 | iOPS figure sourced to Paid Acquisition Flash (Andrew Wirtz); Prime Day numbers specific; F90 targets specific with baseline |
| Dual-audience | 9/10 | Full frontmatter and AGENT_CONTEXT; update_triggers well-chosen for the Legal SIM dependency |
| Economy | 7/10 | See required changes below |
| **Overall** | **8.4** | |

Economy=7 blocks PUBLISH. No dimension may be below 7, but the bar is 8 — and this 7 is fixable.

### Required changes

1. **Duplication: Prime Day results appear in both WS3 and WS5.** The sentence "Prime Day 2025, when Engagement campaigns drove 80K clicks at -10% cost YoY, generating $329K in OPS at 644% ROAS — a 12x improvement over the prior year" appears nearly verbatim in both articles. WS3 owns the Engagement channel story; WS5 owns the algorithmic ads story. Pick one home. In WS3, keep the Prime Day reference but trim to one sentence focused on the Engagement channel validation: "Prime Day 2025 confirmed the channel operates at scale — 80K clicks at -10% cost YoY, $329K OPS at 644% ROAS." In WS5, cross-reference WS3 instead of repeating the full stat line.

2. **Duplication: Business Essentials DG stats appear in both WS3 and WS5.** "52K visitors in the first year at a $0.30 CPC" appears in both. WS5 (Algorithmic Ads) is the natural home for Demand Gen performance data. In WS3, replace the BSE detail with a cross-reference: "The Engagement account also enabled the Business Essentials launch through Demand Gen placements (see Workstream 5: Algorithmic Ads for DG performance data)."

3. **"What did we learn about operating engagement differently?" section is partially redundant.** The insight — "platform limitations are problems, not constraints" — is valuable, but the first two sentences restate what the preceding sections already established. Replace:
   - Old: "Engagement requires a fundamentally different operating model than acquisition. Acquisition targets unknown prospects with broad keyword intent. Engagement targets known customers with specific lifecycle goals — different measurement, different creative, different audience strategy."
   - New: "The key operating insight was that the 13% match rate was not a Google limitation to accept — it was an Amazon data integration opportunity to solve. That mindset enabled the ABMA partnership and the match rate improvement."

These three changes bring Economy to 8 and resolve the cross-workstream duplication.

---

## WS4: User Experience — REVISE (8.0)

| Dimension | Score | Notes |
|-----------|-------|-------|
| Usefulness | 8/10 | Covers the full funnel portfolio; the in-context registration result is strong; Baloo/Aladdin are well-explained |
| Clarity | 8/10 | Question headers work; the 2026 portfolio section is the densest and requires careful reading |
| Accuracy | 8/10 | APT-validated result cited with confidence level; Polaris dates specific; CA CVR numbers specific |
| Dual-audience | 9/10 | Full frontmatter and AGENT_CONTEXT with good update_triggers |
| Economy | 7/10 | See required changes below |
| **Overall** | **8.0** | |

Economy=7 blocks PUBLISH.

### Required changes

1. **The 2026 UX portfolio section tries to do too much in prose.** The paragraph beginning "Project Baloo (US Q2 2026) is the most significant UX investment" runs to 5 sentences and covers: what Baloo is, how it differs from Guest, who it targets, the Shopping Ads unlock, and the tech build status. This is three ideas in one paragraph. Split into two paragraphs: (a) what Baloo is and why it matters, (b) the Shopping Ads unlock and its strategic significance. The Shopping Ads point is buried — it deserves its own paragraph because it is a step-change in channel capability.

2. **The final paragraph of the 2026 section is a summary that restates what the preceding paragraphs already said.** "Together, these initiatives address the full funnel: Baloo creates friction-free product engagement at the top, in-context registration and Polaris reduce mid-funnel drop-off, Aladdin eliminates post-registration friction, and F90 plus Guest auto-expiration drive conversion within 90 days." This is a slide-deck summary sentence. The reader already knows this from reading the section. Cut it entirely — the structure of the section already tells this story.

3. **"How bad was the baseline?" section — the three data points (85% LP drop-off, 60% registration drop-off, re-search friction) are strong but the third is stated as a process description rather than a metric.** Replace "Customers who completed registration had to manually re-search for the same products they found on Google" with "Customers who completed registration lost their product context entirely — they had to re-search for the same products they found on Google, creating a post-registration drop-off point with no measured recovery rate." This makes the third point parallel in structure to the first two (quantified friction points) and honestly flags that the re-search drop-off was not measured.

These changes bring Economy to 8.

---

## WS5: Algorithmic Ads — REVISE (7.8)

| Dimension | Score | Notes |
|-----------|-------|-------|
| Usefulness | 8/10 | Demand Gen results are clear and actionable; AI Max test design is well-framed with specific risks |
| Clarity | 8/10 | Logical flow from Demand Gen (proven) → AI Max (planned); question headers work |
| Accuracy | 7/10 | See required changes — one forward-looking claim needs a confidence tag, and the AI Max test design status is ambiguous |
| Dual-audience | 9/10 | Full frontmatter and AGENT_CONTEXT; depends_on chain to Modern Search is correct |
| Economy | 7/10 | See required changes below |
| **Overall** | **7.8** | |

Accuracy=7 and Economy=7 both need to come up.

### Required changes

1. **Cross-workstream duplication (same as WS3 note).** The Prime Day paragraph ("Engagement campaigns drove 80K clicks at -10% cost YoY, generating $329K in OPS at 644% ROAS — a 12x improvement over the prior year") and the BSE paragraph ("52K visitors in the first year at a $0.30 CPC") duplicate WS3 nearly verbatim. This article should own the Demand Gen efficiency story. Keep the BSE/DG CPC data here. For Prime Day, keep a tighter version focused on the DG channel validation: "Prime Day 2025 validated Demand Gen at scale — Engagement campaigns drove $329K OPS at 644% ROAS, a 12x YoY improvement, confirming that visual ad formats deliver during peak events." Remove the 80K clicks and -10% cost detail (that's the Engagement channel story, which WS3 owns).

2. **AI Max test design status is ambiguous.** "The AI Max test design was due March 28, 2026 — status of completion is the immediate open question." This was written on April 5. Either the test design was completed (update the sentence to reflect that) or it was not (flag it as a risk with a specific next step). The current phrasing reads like the author didn't check. Replace with either: "The AI Max test design was due March 28, 2026. As of this writing, [status — completed/delayed/pending]. [Next step if not completed.]" This is an Accuracy issue — the doc should not present a past-due date without resolving it.

3. **The Discovery Ads history paragraph is padding.** "The team began testing this in 2023 with Discovery Ads. Initial registrations were limited, but the team continued iterating mid-funnel strategies. In 2024, LiveRamp targeting capabilities were incorporated to reach existing customer audiences in the US, improving audience precision for engagement campaigns." The 2023 Discovery Ads detail adds no value to the current narrative — the reader needs to know Demand Gen works now, not that Discovery Ads didn't work in 2023. The LiveRamp point is already covered in WS3. Replace the entire paragraph with: "By 2025, Demand Gen had matured into a proven channel after two years of iteration on mid-funnel ad formats and audience targeting."

4. **"How is Demand Gen expanding in 2026?" section is thin.** Three sentences that say video CPCs match image CPCs and the Creative team is developing assets. This doesn't answer the header question with enough substance. Either expand with specific timeline/volume expectations for video, or merge this into the preceding Demand Gen results section as a forward-looking paragraph. A section that can be absorbed into another section without losing anything is not earning its place.

These changes bring Accuracy to 8 and Economy to 8.

---

## Cross-cutting observations

All five articles share the same structural DNA — question-driven headers, prose-first narrative, appendix-heavy structure, YAML frontmatter + AGENT_CONTEXT. This is the right template. The quality is consistently high. The issues are at the margin: cross-workstream duplication (WS3/WS5 share Prime Day and BSE stats), occasional summary sentences that restate what the reader already knows, and one unresolved date in WS5.

The two PUBLISH articles (WS1, WS2) are the strongest because they have the tightest problem→test→result→scaling arcs with no duplication. WS3, WS4, and WS5 are all fixable with targeted edits — none require structural rework.
