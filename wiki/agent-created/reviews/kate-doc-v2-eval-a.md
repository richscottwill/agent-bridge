---
title: "Review: Paid Search Testing Approach & Year Ahead (Blind Eval A)"
status: DRAFT
audience: amazon-internal
owner: Richard Williams
created: 2026-04-12
updated: 2026-04-12
---
<!-- DOC-0480 | duck_id: wiki-review-kate-doc-v2-eval-a -->

# Review: Paid Search Testing Approach & Year Ahead (Blind Eval A)

**Reviewer:** wiki-critic (Blind Eval A — strict Amazon writing standards)
**Date:** 2026-04-05
**Context:** Kate Rundell (L8 Director) April 16 review. Two-page narrative body + appendix. Kate should get 95% of the value in 8 minutes.

---

## Scores

| Dimension | Score | Notes |
|-----------|-------|-------|
| Usefulness | 8/10 | Strong investment-to-evidence mapping gives Kate what she needs to decide. The "so what" is present for every workstream. |
| Clarity | 7/10 | Structure is logical and scannable, but the methodology section is overlong for this audience, and several workstream sections bury the 2026 ask beneath historical detail Kate already knows. |
| Accuracy | 8/10 | Numbers are internally consistent, sourced, and dated. Confidence levels stated. Minor gap: UK Modern Search pre/post window is noted but no control group detail for the +31% claim. |
| Dual-audience | 8/10 | Rich YAML frontmatter, AGENT_CONTEXT with key_entities, action_verbs, update_triggers, consumed_by. Prose is human-readable. Both audiences served. |
| Economy | 4/10 | This is the fatal dimension. See detailed analysis below. |
| **Overall** | **7.0/10** | |

---

## Verdict

**REVISE**

Economy = 4 blocks publication regardless of the other scores. The doc is roughly 2,400 words of main body content. Kate's brief is two pages (~1,000-1,200 words). The document is 2x the target length because material that belongs in the appendix is in the main body.

---

## Economy: Detailed Findings

### 1. Table abuse — four data tables in the main body without appendix separation

The doc contains four tables in the narrative body:

- OCI results table (4 rows × 5 columns)
- UK Modern Search results table (4 rows × 4 columns)
- 2026 Investment Summary table (5 rows × 4 columns)
- Team table (7 rows × 3 columns)

The OCI and Investment Summary tables are the most defensible — they present comparative data. But even these need "so what" interpretation sentences (the OCI table has one; the Investment Summary table does not — it just ends and the next paragraph starts a new argument about compounding).

The UK Modern Search table presents sequential data (before/after), not a comparison matrix. It should be rewritten as prose: "In the UK, the new ads drove 31% more registrations despite 25% fewer impressions, with CTR improving from 14% to 24% — a +86% improvement over control."

The Team table is pure appendix material. Kate does not need to read a roster to make an investment decision.

**Flag: Table abuse.** Three of four tables either lack interpretation sentences or present sequential data that should be prose. The team table belongs in the appendix.

### 2. Three full sections belong in the appendix

These sections do not serve Kate's two-page read:

- **"The Team"** (full section, ~150 words + table): Kate doesn't need the roster. One sentence in the main body — "Brandon Munday's seven-person team delivers five concurrent workstreams across 10 markets with 12+ cross-functional partners" — replaces the entire section. Move the table and detail to the appendix.

- **"What we do within Paid Search" and "What we also do beyond Paid Search"** (~150 words combined): These are scope descriptions for someone unfamiliar with the team. Kate is not that person. Appendix.

- **"Operational Backbone"** (~120 words): This is important context for a team review, but for Kate's investment decision, it's supporting evidence. One sentence in the main body — "The strategic work runs on a daily/weekly/monthly operational cadence across 10 markets, delivered by the same seven-person team" — and move the detail to the appendix.

Moving these three sections saves ~420 words from the main body without losing any information.

### 3. Methodology section is overweight for this audience

The "How We Test" section is ~280 words with four numbered stages. Kate needs to know the team has a rigorous methodology. She does not need the four-stage breakdown at this level of detail in the main body.

Replace with a compressed paragraph (~80 words): state the methodology exists, name the four stages in a single sentence, give the SyRT incrementality result as the proof point, and move the detailed breakdown to the appendix.

Current: ~280 words. Target: ~80 words. Savings: ~200 words.

### 4. Workstream sections carry historical narrative that Kate doesn't need

Each workstream section has an italicized "Progression" subtitle and historical context. For example:

> *Progression: Loss of Google Ads auto-bid strategy and Adobe → OCI success and expansion*
>
> The Paid Search team partnered with MarTech to implement OCI as the first non-retail business unit at Amazon. This required defining the OCI value framework with Data Science, ensuring Legal approved the data flow, building the tracking infrastructure with MarTech, and validating the underlying data.

Kate doesn't need the origin story. She needs: headline result → 2026 investment → expected impact. The partnership context is one sentence, not a paragraph.

This pattern repeats across all five workstreams. Each could lose 30-50 words of historical setup.

### 5. Bullet list sub-rule: not triggered

The document uses narrative prose, not bullet lists. No flag here.

### 6. Formatting as content: borderline

The bold numbered stages in "How We Test" (**1. Hypothesis and Baseline.**, etc.) rely on formatting for scannability, but the prose reads without it. Not flagged, but worth noting — if the methodology moves to the appendix, this becomes moot.

### 7. Duplication

The opening paragraph states "+35,196 incremental registrations and $16.7MM+ in OPS." The OCI section repeats "+32,047 regs" and "$16.7MM OPS." The Investment Summary table repeats "+35K regs / $16.7MM OPS." The same number appears three times. In a two-page doc, that's twice too many.

The "compounding" argument appears twice: once at the end of the Investment Summary table section ("These workstreams compound: campaign consolidation strengthens OCI signals...") and once implicitly in the second paragraph of the opening ("The team is transforming Paid Search from a keyword-driven acquisition channel into an automated, audience-centric engine"). Pick one location and make it count.

---

## Required Changes

### R1: Move "The Team," "What we do," "What we also do," and "Operational Backbone" to the appendix

Replace all four sections with a single paragraph in the main body:

> Brandon Munday's seven-person team delivers five concurrent strategic workstreams across 10 markets while maintaining 25-30 hours per week of operational work, partnering with 12+ cross-functional groups including Google, MarTech, Legal, Data Science, and ABMA. The ratio of strategic to operational capacity is the binding constraint on simultaneous initiatives.

Move the team table, scope descriptions, and operational cadence detail to the appendix.

### R2: Compress "How We Test" from ~280 words to ~80 words

Replace the four-stage detailed breakdown with a single paragraph. Keep the SyRT proof point (82-92% incrementality, p<0.001) and the Gated Guest pivot as the two examples that prove the methodology works. Move the full four-stage breakdown to the appendix.

Suggested replacement:

> The PS team follows a four-stage methodology — hypothesis and baseline, phased rollout, matched measurement, scale or stop — applied consistently across all workstreams. A 2023 Synthetic Regional Test established that 82-92% of Non-Brand registrations are incremental (p<0.001), confirming the channel's value. When the Gated Guest experiment showed -61% registrations after four weeks, the team paused, diagnosed the failure, and pivoted to in-context registration — which delivered +13.6K annualized incremental registrations. Failures are data, not setbacks. The full methodology is detailed in the appendix.

### R3: Rewrite the UK Modern Search table as prose

Replace:

> | Metric | Before | After | Change |
> |--------|--------|-------|--------|
> | Impressions | 37,388 | 28,010 | -25% |
> | Clicks | 5,308 | 6,778 | +28% |
> | Registrations | 273 | 358 | **+31%** |
> | CTR | 14% | 24% | **+70%** |
>
> Pre/post comparison (Dec 27-Jan 28 vs. Jan 29-Mar 2). The test-vs-control CTR improvement over the same period was +86%.

With:

> In the UK Phase 1 test (Jan 29 – Mar 2, 2026), the research-driven ads drove 358 registrations versus 273 in the prior period — a 31% increase despite 25% fewer impressions. CTR improved from 14% to 24%, and the test-versus-control CTR improvement was +86%. Confidence: HIGH.

### R4: Remove the Team table from the main body

The seven-row team roster table is appendix material. Kate does not need to know individual names and levels to make an investment decision. If team capacity is the argument, the one-sentence version in R1 makes it.

### R5: Add a "so what" sentence after the Investment Summary table

The table currently ends and the next paragraph starts a new argument about compounding. Add an interpretation sentence between them:

> Every row in this table traces a direct line from a 2025 validated result to a 2026 investment — the team is not proposing new bets, but scaling proven ones.

### R6: Cut one of the three repetitions of the headline number

The "+35,196 regs / $16.7MM OPS" figure appears in the opening paragraph, the OCI results table, and the Investment Summary table. Remove it from the Investment Summary table's "2025 Validated Signal" column (replace with "US +24% reg uplift; ~50% NB CPA improvement") since the OCI section already established the absolute numbers.

### R7: Trim workstream historical context

For each of the five workstream sections, cut the italicized "Progression" subtitle and compress the historical setup paragraph to one sentence. The pattern should be: one-sentence context → headline result (with number) → 2026 investment → expected impact.

Example for OCI — replace:

> *Progression: Loss of Google Ads auto-bid strategy and Adobe → OCI success and expansion*
>
> The Paid Search team partnered with MarTech to implement OCI as the first non-retail business unit at Amazon. This required defining the OCI value framework with Data Science, ensuring Legal approved the data flow, building the tracking infrastructure with MarTech, and validating the underlying data.

With:

> The PS team partnered with MarTech, Data Science, and Legal to implement OCI as the first non-retail business unit at Amazon.

### R8: Remove the second paragraph of the opening

> The team is transforming Paid Search from a keyword-driven acquisition channel into an automated, audience-centric engine — grounded in evidence rather than speculation. Each section below covers one workstream: what we tested, what we learned, and how the validated results directly inform 2026 investment. Cross-functional collaboration spanning Legal, Data Science, MarTech, MCS, ABMA, Customer Research, and international market teams was required for every initiative, with the PS team serving as the connective tissue between platform capabilities and business objectives.

This paragraph is a table of contents in prose form. Kate doesn't need to be told what the sections cover — she'll read them. The cross-functional list is repeated in the team section. Cut entirely.

---

## Estimated Impact of Required Changes

| Change | Words removed from body | Words added |
|--------|------------------------|-------------|
| R1: Move team/ops/scope to appendix | ~420 | ~60 |
| R2: Compress methodology | ~200 | ~80 |
| R3: Table → prose (Modern Search) | ~80 (table) | ~60 |
| R4: Remove team table | ~70 (table) | 0 |
| R7: Trim workstream history | ~150 | ~50 |
| R8: Cut second opening paragraph | ~80 | 0 |
| **Net** | **~1,000** | **~250** |

Current body: ~2,400 words. After changes: ~1,650 words. That's close to the two-page target. Further tightening of individual sentences could bring it to ~1,400, which is a comfortable two pages with the OCI results table and Investment Summary table retained.

---

## Suggestions (non-blocking)

1. The OCI results table is the strongest table in the doc — it presents a genuine four-market comparison. Consider keeping it but adding a "so what" row or sentence: "OCI delivers double-digit registration uplift in every market tested, with the US showing the largest absolute impact."

2. The Challenges section is well-structured but could lead with the highest-risk item (JP -47.5% vs OP2) rather than DE (which missed by only 4%). Kate will read risk in priority order.

3. The AGENT_CONTEXT is solid. Consider adding `word_count_target: 1200` and `appendix_companion: true` to signal the two-page constraint to downstream agents.

4. The "risk of not investing" paragraph at the end of the Investment Summary is strong — it's the counterfactual Kate needs. Consider moving it immediately after the table and before the compounding paragraph, so the argument flows: here's what we'll do → here's what happens if we don't → here's why the pieces fit together.

---

## Summary

The content is strong. The evidence-to-investment mapping is exactly what Kate needs. The problem is structural: this is a three-page doc pretending to be a two-page doc. Roughly 1,000 words of main body content — the team roster, scope descriptions, operational backbone, detailed methodology, and historical workstream context — belongs in the appendix. The tables need either prose conversion (Modern Search) or interpretation sentences (Investment Summary). Fix Economy and this doc ships.

**Overall: 7.0/10 — REVISE. Economy is the blocker.**
