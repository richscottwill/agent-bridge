---
title: "Review: Paid Search Five-Year Outlook: 2026–2030"
status: DRAFT
audience: amazon-internal
owner: Richard Williams
created: 2026-04-12
updated: 2026-04-12
---
<!-- DOC-0468 | duck_id: wiki-review-five-year-outlook-v1-review -->

# Review: Paid Search Five-Year Outlook: 2026–2030

Eval: A (Rubric)
Reviewer: wiki-critic
Date: 2026-04-05
Audience: Leadership (Kate Rundell L8, Brandon Munday L7)

## Scores
| Dimension | Score | Notes |
|-----------|-------|-------|
| Usefulness | 8/10 | Each year separates grounded from speculative and ends with a "what changes if we are wrong" section — Kate can use this to make investment decisions and calibrate risk. Loses a point because the doc never synthesizes a single recommendation or decision ask across the five years; Kate must assemble the strategic implications herself. |
| Clarity | 7/10 | Year-by-year structure is scannable and the four-part framework (know / betting / watching / wrong) is excellent. But the main body is ~3,800 words — nearly double the two-page maximum for Kate-level docs. The "Broader Agentic Evolution" section restates points already made in the year sections. Several paragraphs in 2028-2030 repeat the same hedging pattern ("if the trajectory holds… the team retains…") to diminishing returns. A reader who knows the domain can follow it, but the length forces re-reading to extract the signal. |
| Accuracy | 8/10 | 2026 claims are well-sourced and match the research brief (OCI numbers, ad copy results, Baloo timeline, F90 metrics). External citations include source and date consistently. The research brief itself flags that web search was unavailable and several external claims (Gartner $15T, Forrester 35% efficiency, McKinsey workforce framing) could not be independently verified — the article cites them with attribution but does not flag the verification gap. The confidence tiering (HIGH/MEDIUM/LOW) in frontmatter is honest and useful. One minor issue: the article states "Seven of ten markets now run at 100% OCI deployment" but the research brief's DuckDB table shows only US/UK/DE at 100% with FR/IT/ES/JP recently dialed up (3/30-3/31) — "seven markets at 100%" is directionally correct per eyes.md but the brief notes DuckDB still shows "in_progress" for four of them. This is a timing nuance, not a factual error, but Kate-level docs should not have ambiguity on current state. |
| Dual-audience | 6/10 | YAML frontmatter is present with useful fields (confidence, update-trigger). Prose serves humans well. However: no AGENT_CONTEXT block, no `depends_on` or `consumed_by` fields, no `tags` or `category` for agent indexing. An agent swarm cannot determine what this doc relates to, what triggers a refresh, or where it sits in the wiki graph without parsing the full prose. For a doc this important to the strategic narrative, the agent metadata gap is significant. |
| Economy | 6/10 | The main body exceeds the two-page Kate-level maximum by roughly 2x. The "Broader Agentic Evolution" section (~500 words) largely duplicates points already embedded in the year sections — the market size projections, the multi-agent architecture patterns, the cancellation counternarrative, and the UCP/ACP discussion all appear twice. The 2029 and 2030 sections repeat the same structural pattern as 2028 with diminishing new information; 2029-2030 could be compressed into a single "2029-2030: Directional Vision" section without losing value. Several paragraphs across 2027-2030 end with the same "if wrong, we still have X" hedge — the pattern is valuable once (2026) but becomes padding by the fourth repetition. The appendices are well-structured and do not count against economy. |
| **Overall** | **7.0/10** | |

## Verdict
REVISE

## Required changes

### 1. Add AGENT_CONTEXT block (Dual-audience: 6 → 8 target)

After the YAML frontmatter, add an AGENT_CONTEXT block. Minimum fields:

```markdown
<!-- AGENT_CONTEXT
depends_on:
  - shared/artifacts/testing/2026-04-03-testing-approach-outline.md
  - shared/artifacts/strategy/2026-03-25-agentic-ps-vision.md
  - shared/artifacts/strategy/2026-03-25-aeo-ai-overviews-pov.md
consumed_by:
  - wiki-index
  - quarterly-strategy-review
tags: [strategy, five-year, paid-search, agentic, AI-Max, OCI, leadership]
category: strategy
refresh_trigger: annual review, major Google Ads platform change, OCI expansion results
decision_framework: year-by-year grounded-vs-speculative with contingency planning
key_entities: [OCI, AI Max, Baloo, F90, UCP, ACP, AI Overviews]
-->
```

### 2. Cut "Broader Agentic Evolution" section entirely (Economy: 6 → 7+ target)

Delete the entire "Broader Agentic Evolution — Parallel Track" section (~500 words). Every substantive point it makes already appears in the year-by-year sections:
- Market size projections → already in 2028 ("$25-30 billion") and 2030 ("$52-57 billion")
- Multi-agent architecture patterns → already in 2027 ("existing multi-agent infrastructure")
- Cancellation counternarrative → already in 2027 ("40% of agentic AI projects will be canceled")
- UCP/ACP → already in 2027 and 2028

If any unique point survives the cut (e.g., the "53% multi-agent market share" stat), embed it in the relevant year section in a single sentence.

### 3. Merge 2029 and 2030 into a single section (Economy: targets 8)

Replace the separate "2029 — Predictive and Autonomous" and "2030 — Fully Agentic Acquisition" sections with a single "2029–2030 — Directional Vision" section. Both are LOW confidence and share the same structural pattern. The merged section should:
- State the directional thesis in one paragraph (keyword-to-signal transition completes, agentic stages 4-5)
- Identify the two or three signals worth monitoring (agent-to-agent commerce, headcount model, outcome-based billing)
- Provide one "what changes if we are wrong" paragraph covering both years

Target: ~400 words total, down from ~1,100 across the two current sections.

### 4. Consolidate the "what changes if we are wrong" sections (Economy + Clarity)

The current pattern — a "what changes if we are wrong" subsection at the end of every year — is valuable for 2026 (grounded, specific) and 2027 (medium confidence, still useful). For 2028 and the merged 2029-2030, the hedges become repetitive ("the team retains a strong foundation," "the infrastructure still delivers value," "the incremental approach means no single year's bet is existential"). 

Replace the 2028 and 2029-2030 hedges with a single paragraph at the end of the merged 2029-2030 section titled "Downside across the speculative horizon" that covers all three years in ~100 words. The core message — incremental bets, no existential risk, each stage delivers standalone value — needs to be said once, not three times.

### 5. Add a synthesis paragraph to the Purpose section (Usefulness: 8 → 9 target)

The Purpose section states the thesis but does not state what Kate should DO with this document. After the second paragraph ("The question is not whether these shifts happen…"), add one paragraph that answers: "What decision does this document support?" For a Kate-level strategy doc, the first section should make clear whether this is informational, whether it requests investment approval, or whether it frames a portfolio of bets for OP1 planning. The current framing implies OP1 planning but never says so explicitly.

### 6. Tighten the OCI deployment claim (Accuracy)

Replace: `"Seven of ten markets now run at 100% OCI deployment."`

With: `"Seven of ten markets run at 100% OCI deployment as of late March 2026 (US, UK, DE since Q4 2025; FR, IT, ES, JP dialed to 100% on March 30-31). CA targets April 7. AU and MX have no confirmed timelines, with neither MCC created."`

The subsequent sentence already covers CA/AU/MX, so this is a matter of precision in the lead claim. The current phrasing is correct per eyes.md but the research brief flags a DuckDB lag — Kate-level docs should not leave room for a "but the data says otherwise" challenge.

## Suggestions (optional, non-blocking)

1. The confidence tiering in frontmatter (`"2026 HIGH, 2027 MEDIUM, 2028+ LOW"`) is excellent. Consider adding a one-line confidence statement at the top of each year section as well, so a reader scanning headers gets the signal without checking frontmatter. The current `### Confidence: HIGH` pattern is close but inconsistent — 2026 uses a sentence after the header, while later years use the same pattern. Standardize.

2. The Appendix A source citations are organized by confidence tier, which is useful. Consider adding a one-sentence "what this means for the reader" note: "HIGH sources are internally measured and verified. MEDIUM sources are external and not AB-specific. LOW sources are industry forecasts — directional, not plannable."

3. The sentence "This is the same sequential logic as the Five Levels framework: you do not skip ahead, and you do not lose what you have already built" in the 2030 section reads like coaching language from the agent system. Apply the trainer-voice test: would Richard say this to Kate? If not, cut it or rephrase as a straightforward operational statement.
