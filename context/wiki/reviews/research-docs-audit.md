# Research Docs Audit — Pre-Existing Writing by Richard Williams

Reviewer: wiki-critic · Date: 2026-03-25
Source: ~/shared/research/ (10 docs, written 2022–2026)
Target: ~/shared/artifacts/testing/ (publish candidates)

## Context

These are Richard's original experiment docs, post-mortems, and test results — written before the wiki team existed. They lack AGENT_CONTEXT blocks, artifact front-matter, and "so what" summaries after tables. Scoring adjusts for this: Dual-audience scores reflect missing wiki infrastructure, not content failure. Content quality is the primary gate.

## Scoring Rubric

| Dimension | What it measures |
|-----------|-----------------|
| Usefulness | Can someone act, decide, or understand something new? |
| Clarity | Scannable structure, meaningful headers, followable narrative? |
| Accuracy | Claims supported, numbers present, methodology sound? |
| Dual-audience | Agent-readable structure + human-readable prose? (expected low — pre-wiki) |
| Economy | Every section earning its place? Tight or bloated? |

## Summary Table

| # | Doc | Useful | Clarity | Accuracy | Dual-aud | Economy | Overall | Verdict |
|---|-----|--------|---------|----------|----------|---------|---------|---------|
| 1 | AI Automation Impact | 9 | 8 | 8 | 6 | 7 | **7.6** | PUBLISH |
| 2 | AB Paid Search Measurement (SyRT) | 8 | 6 | 9 | 4 | 6 | **6.6** | REVISE |
| 3 | Audience Post-mortem | 8 | 7 | 8 | 4 | 7 | **6.8** | PUBLISH |
| 4 | DG Test Results + CPS Y25 Plan | 8 | 5 | 8 | 4 | 5 | **6.0** | REVISE |
| 5 | IT Bid Modifiers Test | 8 | 8 | 9 | 4 | 9 | **7.6** | PUBLISH |
| 6 | Yahoo JP NB Experiment | 7 | 7 | 8 | 4 | 8 | **6.8** | PUBLISH |
| 7 | JP NB Experiment (Google) | 8 | 7 | 9 | 4 | 6 | **6.8** | PUBLISH |
| 8 | JP Discovery Experiment | 2 | 3 | 1 | 3 | 3 | **2.4** | ARCHIVE |
| 9 | JP App Testing Results | 8 | 7 | 8 | 4 | 5 | **6.4** | PUBLISH |
| 10 | JP Pmax Experiment | 2 | 3 | 1 | 3 | 3 | **2.4** | ARCHIVE |


---

## ARCHIVE (incomplete — not publishable)

**#8 — JP Discovery Experiment (2023.04)**: Results section is entirely TBD. Setup and creative assets documented but no performance data, no analysis, no recommendation. This is a launch doc, not a results doc. Archive.

**#10 — JP Pmax Experiment (2023.10)**: Identical situation — results TBD, appendix TBD. Setup and creative assets only. Nearly identical structure and content to the Discovery doc (same audiences, same ad copy). Archive.

---

## PUBLISH candidates — fixes needed to reach 8.0

### #1 — AI Automation Impact (7.6 → 8.0+)

Current score: Usefulness 9 | Clarity 8 | Accuracy 8 | Dual-audience 6 | Economy 7

This is the strongest doc in the batch. Comprehensive workflow inventory with measured before/after data, honest about gaps, includes team-scalable patterns. The measurement methodology section alone is worth publishing.

Fixes to reach 8.0:
- Add artifact front-matter (title, author, date, tags, status)
- Add AGENT_CONTEXT block with `depends_on`, `update_triggers`, `key_facts`
- Trim the "What I Built" section — it overlaps with the workflow inventory. Consolidate or cross-reference, don't repeat.
- Add a 2-sentence "so what" after the Savings Summary table: what does 5.3 hrs/week mean in practice? What changed because of it?
- The "Update Protocol" section at the bottom is operational, not informational — move to a separate maintenance doc or strip it for the published version.

### #3 — Audience Post-mortem (6.8 → 8.0)

Current score: Usefulness 8 | Clarity 7 | Accuracy 8 | Dual-audience 4 | Economy 7

Strong post-mortem with genuine self-criticism ("I could have put more attention towards moving forward on the planning"). The lessons are actionable and specific. Appendix B data tables are well-structured with clear comparisons.

Fixes to reach 8.0:
- Add artifact front-matter and AGENT_CONTEXT block
- Add "so what" after each Appendix B table — the US CPS table shows $621 spend vs $5.6M SSR, but the doc never says "this audience was too small to generate signal." State it.
- The Overview section buries the key finding: privacy law killed the program. Lead with that — it's the most important context for anyone reading this in 2026.
- Tighten the Accomplishments section — "Developed relationships" is soft. Either quantify the outcome or cut it.
- Headers need work: "Accomplishments:" and "Challenges:" should be ## level, not ####. The hierarchy is flat.
- Add a "Status" line at top: this program is suspended. A reader in 2026 needs to know immediately that this isn't active.

### #5 — IT Bid Modifiers Test (7.6 → 8.0+)

Current score: Usefulness 8 | Clarity 8 | Accuracy 9 | Dual-audience 4 | Economy 9

The tightest experiment doc in the batch. Clean Question → Setup → Results → Data structure. Bayesian PPR included with Amazon's threshold for context. Every sentence earns its place.

Fixes to reach 8.0:
- Add artifact front-matter and AGENT_CONTEXT block
- Add one "so what" sentence after the results table: "This validates city-level bid modifiers as a lever for volume growth without CPA degradation."
- Add a "Next steps" or "What happened after" line — did IT adopt this permanently? Was it rolled to other markets? A reader needs the sequel.
- Minor: the table uses column letters (A, B, C...) from the spreadsheet conversion. Clean these to meaningful headers.

### #6 — Yahoo JP NB Experiment (6.8 → 8.0)

Current score: Usefulness 7 | Clarity 7 | Accuracy 8 | Dual-audience 4 | Economy 8

Solid first JP NB test. Honest about poor overall performance while surfacing the competitor subdomain finding ($700 CPA vs $1,457 overall). Good audience appendix documenting targeting logic. The follow-up link to the Google NB experiment creates a natural chain.

Fixes to reach 8.0:
- Add artifact front-matter and AGENT_CONTEXT block
- Add "so what" after the audience-level table: the subdomain audience had 2x better CPA with 1/3 the traffic — that's the headline finding, but it's buried in commentary.
- The "Follow-up questions/commentary" section is the most valuable part but reads like notes. Restructure as "Key Findings" with numbered takeaways.
- Typo in table header: "Impresisions" → "Impressions" (appears twice)
- Add explicit connection to the follow-up doc (2023.01_JP-NB) — what changed between tests?
- Usefulness is capped at 7 because the doc doesn't state whether the subdomain audience finding was ever acted on. Add outcome context.

### #7 — JP NB Experiment, Google (6.8 → 8.0)

Current score: Usefulness 8 | Clarity 7 | Accuracy 9 | Dual-audience 4 | Economy 6

The most data-rich doc in the batch. Thorough LP test (Bulk vs Callback with Bayesian analysis), ad group/ad/keyword/search query breakdowns. The recommendation section is honest and forward-looking. Richard's self-attribution on ad performance is refreshingly direct.

Fixes to reach 8.0:
- Add artifact front-matter and AGENT_CONTEXT block
- The appendix keyword table is 50 rows — too granular for a published artifact. Summarize the top 10 performers in the main body, move the full table to a linked data file or collapse it.
- Add "so what" after the LP test results: "Bulk page CVR was less than half of Callback. 5.8% Bayesian probability means this isn't close. Callback wins definitively."
- The Recommendation section is a bullet list of next-test ideas. Separate "what we learned" (publishable insight) from "what to test next" (operational planning). The latter ages badly.
- Search query table has #DIV/0! errors — clean these to "N/A" or "—"
- Add explicit link back to the Yahoo JP NB doc — this is the sequel, and the chain should be navigable.

### #9 — JP App Testing Results (6.4 → 8.0)

Current score: Usefulness 8 | Clarity 7 | Accuracy 8 | Dual-audience 4 | Economy 5

Strong analytical work. The multi-lens approach (PoP, YoY, cross-channel, cross-market, platform data) is rigorous. The conclusion is honest and well-calibrated: "drives incremental impressions and downloads, but difficult to conclude it drives incremental registrations." This is how test results should read.

Fixes to reach 8.0:
- Add artifact front-matter and AGENT_CONTEXT block
- Economy is the main drag. Appendix A has 6 separate weekly tables (registrations, impressions, downloads, DLs/imp, imps/DL) with WoW percentages. This is spreadsheet output, not narrative. Summarize the key PoP numbers in the main body; link to raw data or collapse the appendix.
- Add "so what" after the PoP comparison: "+12% app regs vs flat market" needs interpretation — is 12% on a base of ~20/week meaningful? State the absolute numbers alongside the percentages.
- The Recommendations section is one sentence. Expand: what should happen with the Apple Search Ads budget? Was it reallocated? This is the decision the doc should enable.
- Appendix B platform KPIs: the +189% unique impressions and +82% unique downloads are cited in the main body but the tables show weekly data that's hard to reconcile. Add a summary row or callout.

---

## REVISE (needs substantive content work)

### #2 — AB Paid Search Measurement / SyRT (6.6 → 8.0)

Current score: Usefulness 8 | Clarity 6 | Accuracy 9 | Dual-audience 4 | Economy 6

This is the most methodologically important doc in the batch — it documents the SyRT incrementality test that proved NB paid search drives 82-92% incremental registrations in the US. That's a landmark finding. But the doc reads like a measurement team deliverable, not a PS team artifact.

Why REVISE instead of PUBLISH:
- Clarity 6: The MDE explanation, treatment allocation tables, and statistical notes are written for a measurement scientist, not a PS practitioner. The doc needs a "Plain English Summary" section at the top that states: "We proved NB paid search drives ~16% incremental lift in US registrations. That means 82-92% of NB registrations are incremental — they wouldn't have happened without paid search."
- Economy 6: The experimental design section (MDE calculations, treatment allocation methodology) is important for reproducibility but buries the findings. Restructure: Findings first, methodology second.
- The Germany arm was cancelled — this is mentioned in the header links but never explained. Either explain why or remove DE references.
- The "Note" section at the bottom contains the most important calculation (82-92% incrementality) but it's formatted as a footnote. This IS the headline. Move it up.
- UK results showed no significant lift — the doc states this but doesn't interpret it. Why did UK fail where US succeeded? Budget difference ($3M vs $400K)? Market maturity? State a hypothesis.

### #4 — DG Test Results + CPS Y25 Testing Plan (6.0 → 8.0)

Current score: Usefulness 8 | Clarity 5 | Accuracy 8 | Dual-audience 4 | Economy 5

Why REVISE instead of PUBLISH:
- Clarity 5: This is the worst-formatted doc in the batch. The PDF-to-markdown conversion created duplicate tables (Brand Lift results appear twice, performance data appears twice with slightly different formatting). The targeting appendix tables are mangled — competitor lists render as run-on text blocks. A reader can't parse the US vs UK targeting strategy without significant effort.
- Economy 5: The doc tries to be two things — a DG test results report AND a CPS Y25 testing plan. These should be separate artifacts. The test results are backward-looking evidence; the testing plan is forward-looking strategy. Combining them creates a doc that's too long and serves neither purpose well.
- The search lift data (+76% US, +135% UK, +142% JP) is compelling but presented without context. What's the baseline? How does this compare to other upper-funnel channels?
- Brand Lift results are mixed (US showed almost no lift) but the narrative frames everything positively. The doc needs the same honesty Richard shows in other experiment docs. "US brand lift was negligible despite being our largest market" — say it.
- The CPS Testing Details section has "Landing page: TBD (Marci)" — this is operational planning, not a publishable artifact. Strip operational TBDs or update them.
- Targeting tables need complete reformatting — the current rendering is unreadable.

Recommendation: Split into two docs. (1) "DG Campaign Test Results (US/UK/JP)" — the evidence. (2) "CPS Y25 DG Testing Plan" — the strategy. The first is publishable with cleanup. The second may be superseded by now (it's Y25 planning from late 2024).

---

## Cross-cutting observations

1. **JP test chain is valuable**: Docs #6 → #7 → #8 → #9 → #10 form a chronological testing narrative for the JP market (Yahoo NB → Google NB → Discovery → App → Pmax). Even with #8 and #10 archived, the remaining three tell a useful story. Consider publishing them as a linked series with a "JP Testing History" index page.

2. **Consistent quality pattern**: Richard's experiment docs follow a reliable Question → Setup → Results → Recommendation structure. The content quality is consistently high. The gap to 8.0 is almost entirely structural (missing front-matter, missing AGENT_CONTEXT, tables without interpretation) rather than substantive.

3. **All docs need the same 3 fixes**: (a) artifact front-matter, (b) AGENT_CONTEXT block, (c) "so what" after every data table. These are mechanical — a wiki-writer could batch-process them.

4. **The SyRT doc (#2) is the highest-value artifact in this batch** despite needing the most work. The 82-92% incrementality finding is the kind of evidence that justifies the entire NB paid search program. It should be the first one revised and published.
