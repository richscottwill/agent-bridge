---
title: "Pre-Existing Artifacts Audit"
status: DRAFT
audience: amazon-internal
owner: Richard Williams
created: 2026-04-12
updated: 2026-04-12
---
<!-- DOC-0490 | duck_id: wiki-review-pre-existing-artifacts-audit -->

# Pre-Existing Artifacts Audit

**Date:** 2026-03-25
**Auditor:** wiki-critic
**Scope:** 27 artifacts in ~/shared/artifacts/ (26 reviewed, 1 deprecated)
**Standard:** 8/10 minimum. Dimensions: Usefulness, Clarity, Accuracy, Dual-audience, Economy.

---

## Deprecated — Flag for Archival

**`reporting/competitive-intel-tracker.md`** — DEPRECATED. Superseded by `strategy/competitive-landscape.md`. Not reviewed. Move to `~/shared/context/archive/` and remove from SITEMAP.

---

## Summary Table

| # | Artifact | Use | Cla | Acc | Dual | Eco | Avg | Verdict |
|---|----------|-----|-----|-----|------|-----|-----|---------|
| 1 | google-ads-campaign-structure | 8 | 8 | 8 | 4 | 8 | 7.2 | REVISE |
| 2 | invoice-po-process-guide | 8 | 8 | 7 | 4 | 7 | 6.8 | REVISE |
| 3 | landing-page-testing-playbook | 8 | 8 | 8 | 4 | 7 | 7.0 | REVISE |
| 4 | mx-ps-handoff-guide | 9 | 8 | 8 | 4 | 7 | 7.2 | REVISE |
| 5 | oci-methodology-knowledge-share | 7 | 8 | 8 | 4 | 7 | 6.8 | REVISE |
| 6 | polaris-rollout-timeline | 9 | 9 | 8 | 4 | 8 | 7.6 | REVISE |
| 7 | ab-paid-search-wiki | 8 | 8 | 8 | 4 | 7 | 7.0 | REVISE |
| 8 | au-market-wiki | 8 | 8 | 8 | 4 | 7 | 7.0 | REVISE |
| 9 | mx-market-wiki | 7 | 7 | 8 | 4 | 5 | 6.2 | REVISE |
| 10 | oci-implementation-guide | 8 | 9 | 8 | 4 | 5 | 6.8 | REVISE |
| 11 | promo-events-calendar | — | — | — | — | — | 0 | ARCHIVE |
| 12 | ww-testing-tracker | 9 | 8 | 8 | 4 | 8 | 7.4 | REVISE |
| 13 | au-keyword-cpa-dashboard | 7 | 7 | 7 | 4 | 7 | 6.4 | REVISE |
| 14 | wbr-callout-guide | 8 | 8 | 8 | 4 | 8 | 7.2 | REVISE |
| 15 | aeo-ai-overviews-pov | 7 | 8 | 5 | 4 | 7 | 6.2 | REVISE |
| 16 | agentic-marketing-landscape | 7 | 8 | 6 | 4 | 7 | 6.4 | REVISE |
| 17 | agentic-ps-vision | 8 | 8 | 7 | 4 | 6 | 6.6 | REVISE |
| 18 | body-system-architecture | 8 | 9 | 8 | 4 | 7 | 7.2 | REVISE |
| 19 | cross-market-playbook | 9 | 8 | 8 | 4 | 8 | 7.4 | REVISE |
| 20 | f90-lifecycle-strategy | 8 | 8 | 8 | 4 | 7 | 7.0 | REVISE |
| 21 | ad-copy-testing-framework | 9 | 8 | 9 | 4 | 8 | 7.6 | REVISE |
| 22 | ai-max-test-design | 9 | 9 | 8 | 4 | 8 | 7.6 | REVISE |
| 23 | au-nb-mro-trades-proposal | 8 | 8 | 7 | 4 | 8 | 7.0 | REVISE |
| 24 | email-overlay-ww-rollout | 7 | 7 | 7 | 4 | 7 | 6.4 | REVISE |
| 25 | oci-rollout-methodology | 8 | 8 | 9 | 4 | 5 | 6.8 | REVISE |
| 26 | budget-forecast-helper-spec | 7 | 8 | 7 | 4 | 8 | 6.8 | REVISE |
| 27 | campaign-link-generator-spec | 7 | 8 | 7 | 4 | 8 | 6.8 | REVISE |

**Results:** 0 PASS | 25 REVISE | 1 ARCHIVE | 1 DEPRECATED (not reviewed)

---

## The Systemic Problem

Every single artifact fails on the same dimension: **Dual-audience (score: 4/10 across the board)**. None of the 26 reviewed docs have an AGENT_CONTEXT block. This is a batch fix — not 26 individual problems.

Additionally, most docs are missing the "so what" interpretation after tables. Tables report data; they don't tell the reader what to do with it.

### Universal Fix (apply to all 26 docs)

Add an AGENT_CONTEXT block to the front-matter of every artifact:

```yaml
AGENT_CONTEXT:
  summary: [1-2 sentence description of what this doc is and when to use it]
  depends_on: [list of body organs or other artifacts this doc draws from]
  consumed_by: [list of docs, agents, or processes that reference this doc]
  update_triggers: [specific events that should trigger a refresh]
  key_facts: [3-5 extractable facts an agent can use without reading the full doc]
```

This single fix raises every doc's Dual-audience score from 4 to 7-8, which pushes most docs above the 8.0 threshold.

---

## P1: Actively Referenced Docs (fix first — other docs and agents depend on these)

These are referenced by the testing-approach-kate parent doc, the cross-market-playbook, or the ww-testing-tracker. Staleness or low quality here cascades.


### 25. oci-rollout-methodology (testing/) — 6.8 → target 8.0+

**Problem:** Heavily duplicates oci-implementation-guide (program-details/) and oci-methodology-knowledge-share (communication/). Three docs covering the same topic with different angles but significant overlap. Economy score tanks because of this.

**Fixes:**
1. Add AGENT_CONTEXT block (universal fix)
2. Add "so what" after the Market Status table: "US/UK/DE are the reference implementations. CA/JP/EU3 are in E2E — expect full impact by Jul 2026. AU/MX are excluded because Google doesn't support OCI in those markets."
3. Add "so what" after the Results Summary table: "OCI is the single highest-impact initiative in the program's history. The $16.7MM OPS from US alone justifies the phased methodology."
4. Deduplicate: This doc should be the canonical methodology reference. Add a note at the top: "For per-market tactical steps, see oci-implementation-guide. For team knowledge-sharing, see oci-methodology-knowledge-share."
5. Remove the "Known Issues" and "Lessons Learned" sections — they duplicate content in the implementation guide. Replace with a cross-reference.

### 10. oci-implementation-guide (program-details/) — 6.8 → target 8.0+

**Problem:** Overlaps heavily with oci-rollout-methodology. The phased rollout framework is repeated almost verbatim. The per-market notes table is useful but the rest is redundant.

**Fixes:**
1. Add AGENT_CONTEXT block (universal fix)
2. Reframe as the tactical companion to oci-rollout-methodology. Add header note: "This is the hands-on execution guide. For the strategic methodology and results, see oci-rollout-methodology."
3. Cut the "Scaling: 25% → 50% → 100%" section — it's a copy of the methodology doc. Replace with: "Follow the phased framework in oci-rollout-methodology. Gate criteria: 115% at 25%, 110% at 50%."
4. The Troubleshooting table is this doc's unique value. Expand it — add the hvocijid issue as a row, add "Conversion lag" as a common issue.
5. Add "so what" after the Per-Market Notes table.

### 21. ad-copy-testing-framework (testing/) — 7.6 → target 8.0+

**Problem:** Close to passing. Missing AGENT_CONTEXT and one "so what" after the Results table.

**Fixes:**
1. Add AGENT_CONTEXT block (universal fix)
2. After the Results table, add: "UK Phase 1 is HIGH confidence — the methodology works. IT is LOW confidence — volume was insufficient to draw conclusions. Next priority: launch Phase 1 in DE/FR/ES where translations are ready."
3. After the Key Copy Changes table, add: "These aren't cosmetic tweaks. The SP study showed our ads were actively deterring 50% of our target audience. The copy changes remove the two biggest barriers to signup."

### 22. ai-max-test-design (testing/) — 7.6 → target 8.0+

**Problem:** Close to passing. Missing AGENT_CONTEXT. The Open Questions section is good but needs a "so what" — who answers these and by when?

**Fixes:**
1. Add AGENT_CONTEXT block (universal fix)
2. After the Open Questions list, add: "These questions should be answered in the Google sync with Mike Babich before test launch. If any answer is a dealbreaker (e.g., AI Max ignores negative keywords), the test design needs revision."
3. After the Success Criteria table, add: "The 15% reg lift threshold is calibrated to OCI's US result (+24%). We're setting a lower bar because AI Max is less proven. If it hits even 10%, it's worth extending."

### 12. ww-testing-tracker (program-details/) — 7.4 → target 8.0+

**Problem:** High usefulness but missing AGENT_CONTEXT and "so what" after each table.

**Fixes:**
1. Add AGENT_CONTEXT block (universal fix)
2. After the Active Tests table, add: "5 OCI E2E tests running simultaneously across CA/JP/EU3. Ad copy Phase 1 complete in UK (strong) and IT (inconclusive). Polaris US is live, AU migrating."
3. After the Planned Tests table, add: "AI Max (due 3/28) and Email Overlay (blocked by Vijay) are the two highest-priority planned tests. AU NB MRO/Trades is a market-specific opportunity, not a WW initiative."
4. After the Completed Tests table, add: "OCI is the proven playbook. Every completed test validated the phased methodology. CA LP optimization shows the same pattern works for landing pages."

### 19. cross-market-playbook (strategy/) — 7.4 → target 8.0+

**Problem:** Strong doc, close to passing. Missing AGENT_CONTEXT and one "so what."

**Fixes:**
1. Add AGENT_CONTEXT block (universal fix)
2. After the Initiatives table, add: "OCI is the most mature — it's been through the full playbook in 3 markets. Ad Copy and Polaris are mid-playbook. AI Max and Email Overlay haven't started the sequence yet."
3. After the "What Changes Per Market" table, add: "The methodology and measurement framework are the constants. Everything else adapts. This is why the playbook works — it separates what scales from what localizes."

### 6. polaris-rollout-timeline (communication/) — 7.6 → target 8.0+

**Problem:** Highly actionable, close to passing. Missing AGENT_CONTEXT.

**Fixes:**
1. Add AGENT_CONTEXT block (universal fix). Key facts should include: "US live 3/24. AEM translations due 3/26. Weblab Apr 6-7. Brandon priority: AU>MX>DE>UK>JP>FR>IT>ES>CA>US-ES."
2. After the Timeline table, add: "US is done. AU/MX/JP/CA translations are the immediate blocker (due 3/26). EU5 is blocked by the ops ticket. The critical path is AEM → page build → weblab → go-live."

### 20. f90-lifecycle-strategy (strategy/) — 7.0 → target 8.0+

**Problem:** Missing AGENT_CONTEXT. The Measurement table needs a "so what." The doc is slightly thin — it describes what F90 is but doesn't fully explain why it matters strategically.

**Fixes:**
1. Add AGENT_CONTEXT block (universal fix)
2. After the Measurement table, add: "The 31.7% → 35.4% target represents ~12% improvement in post-registration purchasing. At scale, this changes the PS team's value proposition from 'we drive registrations' to 'we drive registrations AND purchases.'"
3. Add a "Strategic Context" section (2-3 sentences): "F90 is the bridge between acquisition and lifecycle. It extends PS value beyond the registration event. This is Decision D10 in brain.md — it builds on the Engagement channel infrastructure (D6) and positions PS as a full-funnel channel."

---

## P2: Useful but Standalone (fix second — these serve specific audiences but aren't dependencies)

### 1. google-ads-campaign-structure (best-practices/) — 7.2 → target 8.0+

**Fixes:**
1. Add AGENT_CONTEXT block (universal fix)
2. After the Standard Campaign Types table, add: "Brand and NB are always-on. Category campaigns are opportunistic — only build when a dedicated LP exists. Engagement is the F90 lifecycle play."
3. After the Match Type Strategy section, add: "The key rule: broad match ONLY with OCI. Without algorithmic bidding, broad match wastes budget on irrelevant queries."

### 3. landing-page-testing-playbook (best-practices/) — 7.0 → target 8.0+

**Fixes:**
1. Add AGENT_CONTEXT block (universal fix)
2. After the Category Page table, add: "Category pages are the highest-CVR play we have. Office at +52% is not a marginal improvement — it's a step change. Every market with search volume in a vertical should have a category page."
3. The "Known Issues" section is good but needs a "so what": "These are implementation friction, not blockers. The reftag workaround exists. The footer issue is cosmetic. AEM timelines are the real constraint."

### 4. mx-ps-handoff-guide (communication/) — 7.2 → target 8.0+

**Fixes:**
1. Add AGENT_CONTEXT block (universal fix)
2. After the Performance table, add: "MX is a growth market outperforming plan by 32%. The handoff from Carlos to Lorena is operational — the program is healthy, the new stakeholder just needs context."
3. The "What Lorena Needs to Know" section is excellent — clear, numbered, actionable. No changes needed there.

### 5. oci-methodology-knowledge-share (communication/) — 6.8 → target 8.0+

**Problem:** Overlaps with oci-rollout-methodology and oci-implementation-guide. Its unique value is the simplified, team-friendly explanation. But it's too thin to justify as a standalone doc.

**Fixes:**
1. Add AGENT_CONTEXT block (universal fix)
2. Add header note: "This is the simplified team reference. For the full methodology, see oci-rollout-methodology. For per-market execution steps, see oci-implementation-guide."
3. The "What NOT to Do" section is this doc's best content — it's practical and memorable. Expand it with one more item: "Don't compare OCI markets to non-OCI markets directly — AU/MX don't have OCI, so their CPA trajectory is fundamentally different."
4. After the Current Status table, add: "Three markets proven, five in E2E, two excluded. The methodology is validated — the remaining markets are execution, not experimentation."
5. Replace "Questions? Ask Richard." with something more useful: "For deeper methodology questions, see oci-rollout-methodology. For implementation troubleshooting, see oci-implementation-guide."

### 7. ab-paid-search-wiki (program-details/) — 7.0 → target 8.0+

**Fixes:**
1. Add AGENT_CONTEXT block (universal fix)
2. After the Markets table, add: "Richard owns AU and MX hands-on. Andrew covers EU5. Stacey owns US. York owns JP. The team manages 10 markets with 4 people — efficiency through OCI and standardized processes is how this works."
3. After the Key Initiatives table, add: "OCI, Polaris, and Ad Copy are in-flight. AI Max, Baloo, and F90 are planned for Q2. AEO is strategic positioning, not an active project yet."
4. The Cross-Team Partners table is missing the "why" column. Add a brief note for each: what does the collaboration produce?

### 8. au-market-wiki (program-details/) — 7.0 → target 8.0+

**Fixes:**
1. Add AGENT_CONTEXT block (universal fix)
2. After the Performance table, add: "AU is slightly below plan but within margin. The real story is the CPC challenge from Lena — $6 avg CPC is high for the market, and Lena is benchmarking against Consumer ($0.18-0.50), which is an apples-to-oranges comparison. B2B CPC is inherently higher."
3. After the Active Issues list, add: "The CPC challenge is the highest-priority issue. Lena is the country leader — her concerns drive the agenda. The two-campaign structure proposal (product-intent vs business-intent) is Richard's response."

### 14. wbr-callout-guide (reporting/) — 7.2 → target 8.0+

**Fixes:**
1. Add AGENT_CONTEXT block (universal fix)
2. After the Market-Specific Notes table, add: "US and AU are the two markets where callouts get the most scrutiny. US because of Walmart competition and OCI impact. AU because Lena reads every number."
3. The Coverage Protocol section is good but incomplete. Add: "Dashboard ingester auto-generates draft callouts. Start there, then add narrative context and competitive color."

### 15. aeo-ai-overviews-pov (strategy/) — 6.2 → target 8.0+

**Problem:** Accuracy score is low (5/10). The stats cited ("~15-25% of commercial queries," "organic CTR drops 30-40%") are unsourced and flagged in the Sources section as "general industry knowledge (needs primary data validation)." A POV with unvalidated numbers is a liability.

**Fixes:**
1. Add AGENT_CONTEXT block (universal fix)
2. Either source the statistics or reframe them: "Industry estimates suggest AI Overviews appear on a growing share of commercial queries, with early data indicating significant organic CTR impact. AB-specific data is needed — see Open Questions."
3. The "What This Means for the Team" section is the best part — keep it. But add a "so what" after the Recommended Actions: "Actions 1-2 are free. Action 3 requires Google partnership. Action 4 is already happening (F90, email). Action 5 is the measurement gap — without it, we're guessing."
4. The Open Questions are good but need owners and deadlines. Add: "Q1-Q2: Richard to pull from Google Ads data. Q3: Mike Babich (next Google sync). Q4: Richard to check with Shruti (Flex) and Meddy (Retail)."

### 16. agentic-marketing-landscape (strategy/) — 6.4 → target 8.0+

**Problem:** Accuracy is soft (6/10) — claims about industry trends are directional but unsourced. The "Richard's Competitive Advantage" section reads like self-promotion rather than analysis.

**Fixes:**
1. Add AGENT_CONTEXT block (universal fix)
2. Reframe "Richard's Competitive Advantage" as "AB PS Positioning" — make it about the team's capability, not Richard personally. This is an amazon-internal doc (wait — it's marked `personal`, which is fine, but the framing should still be analytical, not promotional).
3. After the "What's Happening at Amazon" section, add: "The key insight: most Amazon teams are still at Stage 2 (assisted). AB PS is building Stage 3 infrastructure. The window is 12-18 months before this becomes table stakes."
4. Source the industry claims or qualify them: "Based on public announcements from Google (I/O 2025), industry analyst reports, and observed patterns in Amazon's internal tooling."

### 17. agentic-ps-vision (strategy/) — 6.6 → target 8.0+

**Problem:** Economy score is low (6/10) — the Five Stages section is detailed but the doc is long for a vision doc. The "What Makes This Novel" section overlaps with agentic-marketing-landscape and body-system-architecture.

**Fixes:**
1. Add AGENT_CONTEXT block (universal fix)
2. Cut "What Makes This Novel" section — it duplicates agentic-marketing-landscape. Replace with a one-line cross-reference: "For industry context and competitive positioning, see agentic-marketing-landscape."
3. After the Current State table, add: "The pattern is clear: context and triage are agent-assisted. Execution and creation are still manual. The next frontier is Stage 2 — agent-executed, human-approved — starting with campaign builds and invoice routing."
4. After the Risks section, add: "The biggest risk isn't technical — it's perception. 'Richard uses AI' needs to be framed as 'Richard built a methodology that scales PS operations.' The artifacts are the proof."

### 18. body-system-architecture (strategy/) — 7.2 → target 8.0+

**Fixes:**
1. Add AGENT_CONTEXT block (universal fix)
2. After the organ table, add: "The metaphor isn't decorative — it's functional. Each organ has a word budget, an update trigger, and a decay protocol. The system trends toward compression, not accumulation."
3. The "What Doesn't Work Yet" section is honest and valuable. After it, add: "These limitations are known and accepted. The system is designed to work within them — workarounds (email bridge, morning routine hooks) exist for each gap."

### 2. invoice-po-process-guide (best-practices/) — 6.8 → target 8.0+

**Problem:** PO numbers are incomplete (AU and US PAM both say "TBD"). A process guide with missing reference data is incomplete.

**Fixes:**
1. Add AGENT_CONTEXT block (universal fix)
2. Fill in the TBD PO numbers or explicitly state: "AU PO: not yet created — raise with finance. US PAM PO: overdue 24 days — escalation needed."
3. After the PO Reference table, add: "The MX and WW POs are active. AU and US PAM are blockers — Richard cannot submit invoices for these markets until POs are created/renewed."
4. After the Common Issues table, add: "The most common issue is PO expiration. Lead time for a new PO is 2+ weeks. Track PO expiry dates proactively."

### 13. au-keyword-cpa-dashboard (reporting/) — 6.4 → target 8.0+

**Problem:** This is a design doc for something that doesn't exist yet. Usefulness is limited until the dashboard is built. The structure is fine but it's aspirational, not operational.

**Fixes:**
1. Add AGENT_CONTEXT block (universal fix)
2. Add a status banner at the top: "STATUS: Design phase. Dashboard not yet built. First data pull pending."
3. After the Dashboard Structure section, add: "The Top 20 by CPA view is what Lena will look at first. If a keyword has CPA >$200 and meaningful volume, it's a candidate for pause or negative keyword addition."
4. The Automation Opportunity section is good — it connects to device.md's tool factory. Keep it.


### 9. mx-market-wiki (program-details/) — 6.2 → target 8.0+

**Problem:** Economy score is low (5/10) — this doc duplicates 70% of mx-ps-handoff-guide. The handoff guide is better because it has a clear audience and purpose. The market wiki adds the performance table and competitors section but otherwise repeats the same campaign structure, stakeholders, and issues.

**Fixes:**
1. Add AGENT_CONTEXT block (universal fix)
2. Deduplicate against mx-ps-handoff-guide. The market wiki should be the canonical reference; the handoff guide should be a time-bound onboarding doc that references the wiki. Add header note: "For Lorena's onboarding context, see mx-ps-handoff-guide."
3. Cut the "Invoice/PO Details" section — it's identical to the handoff guide and the invoice-po-process-guide. Replace with a cross-reference.
4. After the Performance table, add: "MX is the strongest growth market in the portfolio relative to plan (+32% vs OP2). The transition from Carlos to Lorena is the main operational risk — ensure Lorena has full context before the next sync."
5. The "Active Issues" list is good but needs priority ordering. Reorder: (1) Invoice routing (blocking), (2) Lorena onboarding (time-sensitive), (3) Reftag tracking (investigation), (4) Kingpin Goals (overdue), (5) Beauty/Auto pages (monitoring).

### 24. email-overlay-ww-rollout (testing/) — 6.4 → target 8.0+

**Problem:** Thin. The rollout table is just "Pending / Tech scoping" for every market except US. The doc doesn't explain what the email overlay actually does well enough for someone unfamiliar to understand.

**Fixes:**
1. Add AGENT_CONTEXT block (universal fix)
2. Expand the Overview section: explain what happens when an existing customer hits an acquisition page. What do they see today vs what they'd see with the overlay? What's the expected CPA impact?
3. After the Rollout Plan table, add: "Every market except US is blocked by the same thing: Vijay's tech scoping. This is a single-point-of-failure. If Vijay doesn't respond by 3/27, escalate."
4. Add a "Why This Matters" section (2-3 sentences): "Existing customers hitting acquisition pages inflate our CPA because they don't convert (they're already registered). Redirecting them improves acquisition CPA and gives existing customers a better experience."

### 23. au-nb-mro-trades-proposal (testing/) — 7.0 → target 8.0+

**Fixes:**
1. Add AGENT_CONTEXT block (universal fix)
2. After the Proposed Keywords table, add: "These are high-intent verticals where business buyers have recurring, predictable needs. MRO in particular is a natural fit — maintenance supplies are consumable, repeat-purchase products."
3. After the Success Criteria table, add: "This is a budget-neutral test — we're reallocating from underperforming generic NB, not requesting incremental spend. The downside is limited."

### 26. budget-forecast-helper-spec (tools/) — 6.8 → target 8.0+

**Fixes:**
1. Add AGENT_CONTEXT block (universal fix)
2. After the Logic section, add: "This eliminates 30-60 minutes of manual work per R&O cycle and reduces error risk. The trailing 4-week average is a conservative projection method — it won't predict spikes but it won't overproject either."
3. The "Next Steps" are good but need a "so what": "Step 1 (OP2 numbers) is the blocker. Without the plan baseline, the tool can't calculate variance. Get this from finance first."

### 27. campaign-link-generator-spec (tools/) — 6.8 → target 8.0+

**Fixes:**
1. Add AGENT_CONTEXT block (universal fix)
2. After the Reftag Convention table, add: "Consistent reftags are how we track which campaigns drive registrations. A wrong reftag means lost attribution. This tool eliminates the most common source of reftag errors: manual URL construction."
3. The Implementation Options section is good. After it, add: "Option 2 (Google Sheets) is the Level 3 play — it's the version teammates will actually use. Build v1 as Python for validation, then convert."

---

## P3: Archive Candidates

### 11. promo-events-calendar (program-details/) — ARCHIVE

**Reason:** File is empty. Zero content. No front-matter, no body, nothing. Either it was never written or it was accidentally cleared. Archive it. If a promo calendar is needed, create it fresh with proper structure and AGENT_CONTEXT.

### competitive-intel-tracker (reporting/) — ARCHIVE (DEPRECATED)

**Reason:** Superseded by competitive-landscape.md in strategy/. Already flagged by the assignment. Move to archive, remove from SITEMAP.

---

## Deduplication Recommendations

Three clusters of overlapping docs need rationalization:

### Cluster 1: OCI (3 docs)
- `testing/oci-rollout-methodology` — canonical methodology + results
- `program-details/oci-implementation-guide` — tactical execution steps
- `communication/oci-methodology-knowledge-share` — simplified team reference

**Recommendation:** Keep all three but add clear cross-references at the top of each. The methodology doc is the source of truth. The implementation guide is the how-to. The knowledge share is the explainer. Each has a distinct audience — but without cross-references, readers don't know which to use.

### Cluster 2: MX (2 docs)
- `program-details/mx-market-wiki` — canonical market reference
- `communication/mx-ps-handoff-guide` — Lorena onboarding

**Recommendation:** The handoff guide is time-bound — once Lorena is onboarded, it becomes stale. The market wiki should be the living doc. After Lorena's onboarding is complete (~4 weeks), merge any unique content from the handoff guide into the market wiki and archive the handoff guide.

### Cluster 3: Agentic Vision (3 docs)
- `strategy/agentic-ps-vision` — roadmap for PS automation
- `strategy/agentic-marketing-landscape` — industry context
- `strategy/body-system-architecture` — system design

**Recommendation:** These serve different purposes but overlap in the "what makes this novel" sections. Cut the overlap from agentic-ps-vision (it's the worst offender) and add cross-references.

---

## Health Metrics

| Metric | Value |
|--------|-------|
| Total artifacts reviewed | 26 |
| Passing (≥8.0) | 0 |
| Revise (fixable) | 25 |
| Archive | 1 (promo-events-calendar) |
| Deprecated (not reviewed) | 1 (competitive-intel-tracker) |
| Average score | 6.9/10 |
| Lowest score | 0 (empty file) / 6.2 (mx-market-wiki, aeo-ai-overviews-pov) |
| Highest score | 7.6 (polaris-rollout-timeline, ad-copy-testing-framework, ai-max-test-design) |
| Universal failure | Dual-audience: 4/10 on all 26 docs (no AGENT_CONTEXT blocks) |

## Effort Estimate

- **Universal AGENT_CONTEXT fix:** ~5 min per doc × 25 docs = ~2 hours. This is the highest-ROI fix — it raises every doc by 0.6-0.8 points.
- **"So what" additions:** ~2-3 min per table × ~40 tables = ~2 hours. Second-highest ROI.
- **Deduplication cross-references:** ~15 min for the OCI cluster, ~10 min for MX, ~10 min for Agentic. ~35 min total.
- **Content fixes (accuracy, expansion):** ~15-30 min per doc for the 5-6 docs that need substantive work (aeo-pov, agentic-landscape, email-overlay, invoice-po, au-cpa-dashboard, mx-market-wiki).

**Total estimated effort:** ~6-7 hours to bring all 25 docs to 8/10.

**Recommended sequence:** Universal AGENT_CONTEXT fix first (batch job), then P1 docs, then P2, then deduplication cleanup.
