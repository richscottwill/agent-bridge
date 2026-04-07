<!-- DOC-0462 | duck_id: wiki-review-blind-test-2-evaluator-a -->
# Blind Test 2 — Evaluator A (Strict Amazon Writing Standards)

**Date:** 2026-04-04
**Evaluator:** Evaluator A — Amazon narrative standards, wiki-critic rubric (updated), richard-style-amazon.md
**Rubric sources:** `shared/.kiro/agents/wiki-team/wiki-critic.md` + `.kiro/steering/richard-style-amazon.md`
**Methodology:** No prior reviews consulted. Each article scored independently against the updated rubric with strict application of Economy sub-rules (bullet list abuse, table abuse, formatting as content) and Amazon narrative standards (18-20 word sentence average, purpose in first paragraph, prose as default, embedded data).

---

## Article 1: OCI Rollout Playbook

**File:** `shared/artifacts/testing/2026-03-25-oci-rollout-playbook.md`

### Economy Analysis (Pre-Score)

**Bullet/list vs prose ratio:** Approximately 45-50% of the document is structured as bullet lists, numbered steps, or table content. The phased rollout sections (Phase 1-4) are almost entirely numbered lists. The "Market-Specific Considerations" section is a table. The "Known Issues" section is bullet-formatted. The "Decision Guide" is a table. This exceeds the 30% threshold significantly.

**Tables without "so what":** 5 tables total. The "Validated Results by Market" table has a "So what" sentence — good. The "DE Test vs Control Data" table has a "So what" sentence — good. The "MCC Structure" table has no interpretation. The "Rollout Status" table has no interpretation. The "Market-Specific Considerations" table has no interpretation sentence (the considerations are embedded in the table cells, but there's no narrative synthesis). Score: 3 of 5 tables lack "so what" interpretation.

**Plain text readability:** If you stripped all formatting (bold, tables, numbered lists), the document would be difficult to follow. The phased rollout sections rely on numbered step formatting to convey sequence. The tables are the primary content delivery mechanism for market status and MCC structure. This is formatting-as-content.

**Purpose in first paragraph:** Yes. "This playbook codifies the OCI rollout methodology that produced +35K registrations and $16.7MM+ OPS across US, UK, and DE. A teammate should be able to replicate the rollout in a new market by following this doc." Clear purpose, clear audience, clear outcome.

**Sentence length:** The prose paragraphs average approximately 22-24 words per sentence. Slightly above the 18-20 target. Some sentences are compound: "The methodology was developed through US (Jul 2025), refined in UK (Aug 2025) and DE (Nov 2025), and is now being applied to CA, JP, and EU3 (Feb-Mar 2026)" — 33 words.

### Scores

| Dimension | Score | Notes |
|-----------|-------|-------|
| Usefulness | 9/10 | Genuinely enables action. A teammate could replicate OCI rollout in a new market using this doc alone. Decision guide is practical. |
| Clarity | 8/10 | Well-structured, scannable headers, logical flow from context → phases → measurement → troubleshooting. Minor: some sections are dense. |
| Accuracy | 8/10 | Claims sourced. Numbers dated. Cross-references valid. DE test-vs-control data is specific and verifiable. Minor: some market status may be stale (written 3/25, markets moved since). |
| Dual-audience | 8/10 | Rich frontmatter, AGENT_CONTEXT block present with good machine_summary, key_entities, action_verbs, update_triggers. Prose serves humans. Both audiences well-served. |
| Economy | 5/10 | **FLAGGED: Bullet list abuse.** ~45-50% of content is lists/tables. The phased rollout is entirely numbered steps — this should be narrative prose describing the methodology with steps embedded. **FLAGGED: Table abuse.** 3 of 5 tables lack "so what" interpretation (MCC, Rollout Status, Market Considerations). **FLAGGED: Formatting as content.** Remove the numbered lists and tables and the document becomes unreadable — the structure IS the content, not the prose. The Amazon standard is narrative with bullets as exceptions. This reads like a reference card, not a narrative. |
| **Overall** | **7.6/10** | |

### Verdict: REVISE

### Required Changes
1. Rewrite Phase 1-4 sections as narrative prose. The steps can remain as short enumerations (3-5 items) but the methodology explanation should be paragraphs, not numbered lists. Example: "Phase 2 allocates 25% of NB traffic to OCI bidding while the remaining 75% serves as a control. Run this configuration for a minimum of four weeks to accumulate sufficient conversion data, then compare the OCI segment against the control on registrations, CPA, and ROAS."
2. Add "so what" interpretation sentences after the MCC Structure, Rollout Status, and Market-Specific Considerations tables.
3. Convert the "Market-Specific Considerations" table into prose paragraphs — each market gets 2-3 sentences of narrative, not a table cell.
4. Break compound sentences (>25 words) into two sentences. Target 18-20 word average.

---

## Article 2: OCI Execution Guide

**File:** `shared/artifacts/program-details/2026-04-04-oci-execution-guide.md`

### Economy Analysis (Pre-Score)

**Bullet/list vs prose ratio:** Approximately 55-60% of the document is bullet lists, numbered steps, checklists, or table content. The "What NOT to Do" section is a numbered list. "Prerequisites" is a checklist. "Step-by-Step: E2E Launch" is entirely numbered steps with a monitoring table. "Scaling" is a table. "Troubleshooting" is a table. "Per-Market Notes" is a table. "Current Market Status" is a table. "How to Check OCI Performance" is a numbered list. This is the most list/table-heavy document in the batch.

**Tables without "so what":** 7 tables total. The monitoring checklist table (Step 3) has no "so what." The Scaling phases table has no "so what." The Troubleshooting table has no "so what" (it's a lookup table — arguably self-interpreting, but the standard says every table needs interpretation). The Per-Market Notes table has no "so what." The Current Market Status table has no "so what." The MCC Structure table has no "so what." Score: 6 of 7 tables lack "so what" interpretation.

**Plain text readability:** This document would be nearly unreadable as plain text. It is fundamentally a reference card — checklists, lookup tables, step sequences. The prose paragraphs are thin connective tissue between structured elements. This is the clearest case of formatting-as-content in the batch.

**Purpose in first paragraph:** The document opens with a blockquote pointing to the Rollout Playbook, then a horizontal rule, then "What OCI Is (30-Second Version)." The purpose is implicit but not stated in the first paragraph. The first real paragraph explains what OCI is, not what this document is for or what the reader should do after reading it. The blockquote says "This doc is the how-to" but blockquotes are not the first paragraph.

**Sentence length:** Prose paragraphs average approximately 16-18 words per sentence — actually within range. But there's so little prose that the average is skewed by the short imperative sentences in the step lists.

### Scores

| Dimension | Score | Notes |
|-----------|-------|-------|
| Usefulness | 9/10 | Extremely actionable. Someone could execute OCI implementation step-by-step. The troubleshooting table is genuinely useful for operational support. The "What NOT to Do" section prevents common mistakes. |
| Clarity | 7/10 | Scannable and well-organized for a reference card. But the Amazon standard is narrative, not reference cards. Headers are good (action-oriented). The sheer density of tables makes it hard to read linearly — it's designed for lookup, not reading. |
| Accuracy | 8/10 | Claims sourced. Market status dated. MCC IDs specific. Troubleshooting based on operational experience. Minor: "Current Market Status" section says "as of April 2026" but some entries may already be stale (CA "on track" for 4/7 — has it launched?). |
| Dual-audience | 7/10 | Frontmatter present. AGENT_CONTEXT block present. But the document is so table-heavy that agent extraction would be complex — tables are harder to parse than prose with embedded data. The "replaces" field is good (consolidation signal). |
| Economy | 3/10 | **FLAGGED: Bullet list abuse.** ~55-60% of content is lists/tables/checklists. This is a slide deck, not a narrative. **FLAGGED: Table abuse.** 6 of 7 tables lack "so what" interpretation. The Per-Market Notes and Current Market Status tables are data dumps. **FLAGGED: Formatting as content.** Strip formatting and this document is unreadable. It is entirely dependent on checkboxes, numbered lists, and table structure. **FLAGGED: No purpose statement in first paragraph.** The blockquote is not a purpose statement. The first prose paragraph explains OCI, not the document's purpose. **FLAGGED: Duplicate content.** The MCC Structure table, Per-Market Notes, and Current Market Status tables duplicate content from the OCI Rollout Playbook. The Economy sub-rule says "cut anything duplicative." |
| **Overall** | **6.8/10** | |

### Verdict: REVISE

### Required Changes
1. Add a proper purpose statement as the first paragraph: "This guide is the step-by-step execution reference for implementing OCI in any AB Paid Search market. Follow it to launch, monitor, scale, and troubleshoot OCI. For the business case and strategic rationale, see the OCI Rollout Playbook."
2. Rewrite "What NOT to Do" as a prose paragraph with the key warnings embedded: "Do not judge OCI by its first week — the algorithm needs 2-4 weeks to learn, and CPA will spike before normalizing. Never apply OCI to Brand campaigns, which require manual bid caps for competitive defense. Always use seasonality-adjusted baselines rather than raw pre/post comparisons."
3. Convert the Step-by-Step section from numbered lists to narrative prose with embedded steps.
4. Add "so what" sentences after every table, or convert sequential tables to prose with embedded data.
5. Remove duplicate content (MCC table, Per-Market Notes, Current Market Status) — reference the Rollout Playbook instead.
6. Target: reduce list/table content from ~60% to under 30%.

---

## Article 3: AU Paid Search — Market Wiki

**File:** `shared/artifacts/program-details/2026-04-04-au-market-wiki.md`

### Economy Analysis (Pre-Score)

**Bullet/list vs prose ratio:** Approximately 35-40% of the document is tables or bullet content. The "Current Performance" section has a table. "Campaign Structure" is a table. "Key Stakeholders" is a table. "Key Decisions" is a table. "Open Questions" is a numbered list. However, the "Overview," "The CPC Challenge," "Competitors," and "Active Initiatives" subsections are mostly prose. This is closer to the threshold but still exceeds 30%.

**Tables without "so what":** 5 tables total. The "Current Performance" table has contextual prose before it but no explicit "so what" after it — the preceding prose does the interpretation, which is acceptable but inverted from the standard (interpretation should follow, not precede). The "Campaign Structure" table has no interpretation. The "Key Stakeholders" table has no "so what" (it's a reference lookup — but the standard applies). The "Key Decisions" table has no interpretation. Score: 3-4 of 5 tables lack explicit "so what" interpretation.

**Plain text readability:** Better than the OCI docs. The prose sections (Overview, CPC Challenge, Active Initiatives) read well as plain text. The tables are supplementary, not primary. If you removed the tables, you'd lose reference data but the narrative would still make sense. Partial pass.

**Purpose in first paragraph:** The blockquote says "Canonical reference for Australia. One doc, one source of truth." This is a purpose statement but it's in a blockquote, not the first paragraph. The first real paragraph (under "Overview") does state what AU is and provides context, but doesn't say what the reader should do after reading it or what decision it supports. Partial pass.

**Sentence length:** The prose paragraphs average approximately 20-23 words per sentence. Slightly above target. Some sentences are long: "AU does not yet have OCI support (target: May 2026), which means it is running without the conversion signal infrastructure that drives 16-20% registration lifts in other markets" — 30 words. But most are reasonable.

### Scores

| Dimension | Score | Notes |
|-----------|-------|-------|
| Usefulness | 8/10 | Genuinely useful as a market reference. Someone prepping for an AU sync would find everything they need: performance, stakeholders, initiatives, open questions. The stakeholder communication styles are particularly valuable. |
| Clarity | 8/10 | Well-organized. Headers are descriptive. The "CPC Challenge" section is a model of clear explanation — states the problem, explains why the comparison is wrong, provides the response. Active Initiatives subsections are clear. |
| Accuracy | 7/10 | Most claims sourced. Performance data dated (Feb 2026, W13). But some data is already aging — W13 data in an April doc means the "most recent" data is 3+ weeks old. The "Competitors: None" claim is surprising and unsourced. |
| Dual-audience | 7/10 | Frontmatter present with good metadata. AGENT_CONTEXT block present. But the "replaces" field lists three docs — good consolidation signal. The stakeholder table is human-optimized but not great for agent extraction (communication style in prose within table cells). |
| Economy | 5/10 | **FLAGGED: Bullet list abuse (borderline).** ~35-40% list/table content. Just above the 30% threshold. **FLAGGED: Table abuse.** 3-4 tables lack "so what" interpretation. The Campaign Structure table is 3 rows — this should be a prose sentence: "AU runs two active campaigns: Brand (manual CPC with bid caps for competitive defense) and NB (manual CPC, no OCI, primary growth driver). A Category campaign targeting MRO/Trades verticals is proposed but not yet live." **FLAGGED: Purpose statement weak.** The blockquote is not a proper purpose statement. The first paragraph should say: "This is the canonical reference for AU Paid Search. Use it to prep for AU syncs, understand market dynamics, and track active initiatives. It consolidates three former docs into one source of truth." |
| **Overall** | **7.0/10** | |

### Verdict: REVISE

### Required Changes
1. Replace the blockquote with a proper first-paragraph purpose statement that says what the doc is, who it's for, and what the reader does with it.
2. Convert the Campaign Structure table to a prose paragraph (it's only 3 rows — tables are for comparisons across many dimensions, not 3-item lists).
3. Add "so what" interpretation after the Current Performance table: "The headline: AU is tracking to OP2 on registrations and CPA, but the NB efficiency story is incomplete — CPC gains are not translating to CPA improvement because conversion rate is the binding constraint."
4. Add "so what" after the Key Decisions table: "The pattern: Lena drives fast, unilateral decisions (Polaris full migration, CPC scrutiny). Brandon provides air cover. Richard's role is to own the narrative with data."
5. Tighten sentence length — break any sentence over 25 words.

---

## Article 4: Enhanced Match / LiveRamp — Audience Expansion for Paid Search

**File:** `shared/artifacts/testing/2026-04-04-enhanced-match-liveramp.md`

### Economy Analysis (Pre-Score)

**Bullet/list vs prose ratio:** Approximately 15-20% of the document is bullet/list content. The "Brandon's Four Questions" section is a numbered list. The "Next Steps" section is a numbered list. The "Connection to Existing Initiatives" section uses bold sub-headers but is prose. The rest is narrative paragraphs. This is the most prose-heavy document in the batch and passes the 30% threshold comfortably.

**Tables without "so what":** 0 tables. No tables in the document at all. This is pure narrative. Pass.

**Plain text readability:** Excellent. Strip all formatting and the document reads cleanly as a narrative. The bold sub-headers in "Connection to Existing Initiatives" are emphasis, not structural dependencies. The numbered lists (Brandon's questions, Next Steps) are short enumerations that would read fine as prose. Strong pass.

**Purpose in first paragraph:** The first section is "What's Happening" and the first paragraph states: "Brandon initiated an Enhanced Match investigation on 3/30, asking Richard to partner with Abdul Bishar (Brand & Paid Media) to scope the opportunity." This tells you what's happening and who's involved, but doesn't explicitly state what the document is for or what the reader should do. It's a situation report, not a purpose statement. The purpose is implicit (track this initiative) but not explicit. Partial pass.

**Sentence length:** Prose paragraphs average approximately 21-24 words per sentence. Above the 18-20 target. Several sentences are long: "Enhanced Match is LiveRamp's capability to improve the match rate between Amazon's customer data and Google's user graph" — 18 words (fine). "The current LiveRamp integration sends customer identifiers to Google for audience targeting (suppression, engagement)" — 14 words (fine). But: "Enhanced Match expands the data signals sent, potentially increasing the match rate beyond the current 30% achieved through Associated Accounts" — 19 words (fine). The average is pulled up by a few compound sentences in the "Connection to Existing Initiatives" section.

### Scores

| Dimension | Score | Notes |
|-----------|-------|-------|
| Usefulness | 7/10 | Useful as a situation tracker — someone picking up this initiative would understand the state of play. But it's more "here's what's happening" than "here's what to do." The Next Steps are actionable but the doc doesn't enable independent action — it's a briefing, not a guide. |
| Clarity | 8/10 | Well-written narrative. Each section flows logically. The "Connection to Existing Initiatives" section is particularly clear — it explains why Enhanced Match matters beyond its own scope. Headers are descriptive. |
| Accuracy | 8/10 | Claims sourced to specific Slack messages with dates. The 5.6M→1.2M audience drop is flagged with the source (Andrew Wirtz, 4/2). Brandon's questions are attributed. The DMA blocker is sourced. Minor: some claims about Enhanced Match's technical capabilities are stated without external verification (e.g., "every percentage point of match rate improvement translates to more precise targeting"). |
| Dual-audience | 6/10 | Frontmatter present. AGENT_CONTEXT block present with good machine_summary. But the document lacks structured data that agents could extract — no tables, no decision guides, no parameterizable examples. It's optimized for human reading but an agent would struggle to extract structured guidance. The update_triggers are good. |
| Economy | 7/10 | Passes the prose-over-bullets test. No table abuse (no tables). No formatting-as-content. The numbered lists (Brandon's questions, Next Steps) are appropriate short enumerations. Minor bloat: the "ABMA SIM Escalation Protocol" section feels tangential — it's relevant but could be a one-sentence reference rather than a full section. The "Current State" section repeats some context from "What's Happening." One redundant section = minor economy violation. |
| **Overall** | **7.2/10** | |

### Verdict: REVISE

### Required Changes
1. Add an explicit purpose statement as the first sentence: "This document tracks the Enhanced Match / LiveRamp audience expansion initiative for Paid Search — what it is, where it stands, and what needs to happen next."
2. Compress the "ABMA SIM Escalation Protocol" section to one sentence within the "Current State" or "Next Steps" section: "Note: Brandon announced a new ABMA SIM protocol on 4/3 — submit at Sev 2.5 with Vijay Kumar as watcher for any registration-related SIMs, including LiveRamp integration issues."
3. Remove the overlap between "What's Happening" and "Current State" — the LiveRamp architecture description appears in both sections implicitly.
4. Add a decision guide or structured element for agent consumption — even a simple "what to do when" table would improve dual-audience score.
5. Break sentences over 25 words. Target 18-20 word average.

---

## Article 5: ie%CCP Planning & Optimization Framework

**File:** `shared/artifacts/strategy/2026-03-30-ieccp-planning-framework.md`

### Economy Analysis (Pre-Score)

**Bullet/list vs prose ratio:** Approximately 30-35% of the document is bullet lists, code blocks, or table content. The "Why It's Confusing" section uses code blocks for formulas. The "Blended Math" section uses code blocks. The "Optimization Playbook" scenarios use bullet lists for levers. The "Levers (Ranked by Impact)" section uses bullet lists. The "MX Case Study" section has tables. However, the majority of the document is narrative prose — the explanations, the scenario descriptions, the "so what" interpretations are all paragraphs. This is right at the 30% threshold.

**Tables without "so what":** 6 tables total. The "What the number means" table has implicit interpretation in the "Implication" column — acceptable. The "NB per Brand Reg" formula table has a "so what" sentence after it ("The ratio tells you...") — good. The "What Changes the Plan" table has no explicit "so what" — it's a reference lookup. The MX Case Study tables (Scenario 1, Scenario 2, vs OP2, Marginal economics) have interpretation prose between them — good. The "Marginal CPA Curve" code block has interpretation ("This is why cutting NB spend improves CPA disproportionately...") — good. Score: 1 of 6 tables lacks "so what" interpretation. Strong performance.

**Plain text readability:** Good. The code blocks for formulas would lose formatting, but the surrounding prose explains the formulas in words. The tables are supplementary to narrative explanations. If you stripped all formatting, the document would still be comprehensible — the prose carries the argument. The code blocks are the weakest point (formulas need formatting), but the prose restates the math in words. Pass.

**Purpose in first paragraph:** The blockquote says "How to understand, plan around, and optimize ie%CCP for Paid Search budget decisions." This is a purpose statement but it's in a blockquote. The first section is "What ie%CCP Measures" which opens with "ie%CCP answers one question: how much are we paying to acquire a customer, relative to what that customer is worth?" This is a strong conceptual opening but doesn't state what the document is for or what the reader should do. The blockquote does the purpose work. Partial pass — the purpose is present but not in the standard location (first paragraph of prose).

**Sentence length:** Prose paragraphs average approximately 18-21 words per sentence. Close to the 18-20 target. Some sentences are long: "When finance revises CCP, the ie%CCP math shifts immediately" — 10 words (fine). "This is the single biggest ie%CCP shock — it forced the $1.97M → $1.07M budget cut in FY25" — 18 words (fine). The scenario descriptions occasionally run long but are generally well-controlled.

### Scores

| Dimension | Score | Notes |
|-----------|-------|-------|
| Usefulness | 9/10 | Exceptional. This doc enables someone to understand ie%CCP from scratch, model scenarios, make budget recommendations, and write callouts. The four scenarios are practical and cover real situations. The MX case study grounds the theory in reality. The "Applying This to Callouts" section directly enables action. |
| Clarity | 9/10 | The best-written document in the batch. The "Why It's Confusing" section is a masterclass in anticipating reader confusion and addressing it head-on. The subsidy model explanation is clear. The four scenarios are well-differentiated. The "Quick Reference" at the end is a clean summary. |
| Accuracy | 8/10 | MX case study uses specific numbers that are internally consistent. CCP values are dated and sourced. The formula derivation is mathematically correct. Minor: the "Conservative Brand estimates" haircut (-10%) is stated without justification for why 10% vs 15% or 20%. |
| Dual-audience | 7/10 | Frontmatter present. AGENT_CONTEXT block present with good machine_summary. The formulas in code blocks are agent-parseable. But the document is long (~2500 words) and the agent would need to extract the formula, the scenarios, and the case study separately — no structured decision guide table for quick agent lookup. |
| Economy | 7/10 | **Borderline on bullet list abuse** — ~30-35%, right at the threshold. The bullet lists in the "Levers" section and "Optimization Playbook" scenarios are appropriate (they're short enumerations of levers, 3-5 items each). The code blocks for formulas are necessary — math needs formatting. 1 table lacks "so what" (minor). The "Quick Reference" section at the end is slightly redundant with the body — it restates key points. But it's short and serves as a genuine quick-reference, so the duplication is functional. Minor economy violations only. The document earns its length — every section adds unique value. |
| **Overall** | **8.0/10** | |

### Verdict: PUBLISH (conditional)

### Conditions for Publication
1. Move the purpose statement from the blockquote into the first prose paragraph: "This framework explains how to understand, plan around, and optimize ie%CCP — the ratio of acquisition cost to customer value — for Paid Search budget decisions. Use it to model scenarios, evaluate incremental spend, and frame recommendations for finance."
2. Add a "so what" sentence after the "What Changes the Plan" table.
3. Minor: break any remaining sentences over 25 words.

### Suggestions (non-blocking)
1. The "Quick Reference" section could be cut if the purpose statement and section headers are strong enough — it's functional duplication.
2. Consider adding a one-line "when to use this doc" to the AGENT_CONTEXT for better retrieval.

---

## Summary Table

| # | Article | Usefulness | Clarity | Accuracy | Dual-Audience | Economy | Overall | Verdict |
|---|---------|-----------|---------|----------|---------------|---------|---------|---------|
| 1 | OCI Rollout Playbook | 9 | 8 | 8 | 8 | 5 | 7.6 | REVISE |
| 2 | OCI Execution Guide | 9 | 7 | 8 | 7 | 3 | 6.8 | REVISE |
| 3 | AU Market Wiki | 8 | 8 | 7 | 7 | 5 | 7.0 | REVISE |
| 4 | Enhanced Match / LiveRamp | 7 | 8 | 8 | 6 | 7 | 7.2 | REVISE |
| 5 | ie%CCP Planning Framework | 9 | 9 | 8 | 7 | 7 | 8.0 | PUBLISH (conditional) |

---

## Cross-Article Observations

### The pattern is clear: these articles were written as reference cards, not narratives.

Four of five articles fail Economy because they rely on bullet lists, tables, and formatting as their primary content delivery mechanism. The Amazon standard is unambiguous: "Prose is the default. Bullets are the exception." These documents invert that standard.

The OCI Execution Guide (Article 2) is the worst offender — it's essentially a checklist with thin prose connective tissue. It scores a 3/10 on Economy. The OCI Rollout Playbook (Article 1) is similar but has more narrative sections. The AU Market Wiki (Article 3) is better but still table-heavy.

The ie%CCP Framework (Article 5) is the only article that approaches the Amazon narrative standard. It uses prose to explain concepts, embeds data in sentences, and uses tables/code blocks as supplements rather than primary content. It's the model for what the other four should aspire to.

The Enhanced Match doc (Article 4) is the most prose-heavy but scores lower on Usefulness and Dual-audience because it's a situation report rather than a guide or framework — it tells you what's happening but doesn't enable independent action.

### Specific recurring violations:

1. **Bullet list abuse (4 of 5 articles):** Articles 1, 2, 3, and 5 (borderline) exceed the 30% threshold. Article 2 is at ~60%.
2. **Table abuse (3 of 5 articles):** Articles 1, 2, and 3 have multiple tables without "so what" interpretation. Article 5 is the model — nearly every table has interpretation.
3. **Formatting as content (2 of 5 articles):** Articles 1 and 2 would be unreadable without their formatting. Articles 3, 4, and 5 would survive formatting removal.
4. **Purpose statement missing or weak (4 of 5 articles):** Articles 2, 3, 4, and 5 use blockquotes or implicit purpose rather than a clear first-paragraph purpose statement. Only Article 1 has a proper purpose statement in the first paragraph.
5. **Sentence length (3 of 5 articles):** Articles 1, 3, and 4 average above 20 words per sentence. Article 5 is closest to the 18-20 target.

### The fix is structural, not cosmetic:

These articles need to be rewritten with prose as the primary content format. Tables should be reserved for genuine comparisons across multiple dimensions. Bullet lists should be 3-5 items max, used for short enumerations within prose sections. Every table needs a "so what" sentence. Every document needs a purpose statement in the first paragraph.

The content is strong. The writing quality within prose sections is good. The problem is the format — these are reference cards masquerading as narratives. The Amazon standard demands narrative. The content deserves it.
