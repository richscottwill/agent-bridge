---
title: "Eval B: WS1 (OCI Bidding) & WS2 (Modern Search) — Subjective Reader Evaluation"
status: DRAFT
audience: amazon-internal
owner: Richard Williams
created: 2026-04-12
updated: 2026-04-12
---
<!-- DOC-0496 | duck_id: wiki-review-ws1-ws2-eval-b -->

# Eval B: WS1 (OCI Bidding) & WS2 (Modern Search) — Subjective Reader Evaluation

Reviewer: wiki-critic | Date: 2026-04-05 | Mode: Blind Eval B
Reader persona: Kate reviewing workstream detail behind the Testing Approach doc. 10 minutes per workstream.

---

## Summary Table

| Article | First Paragraph | Shareability | Actionability | Signal-to-Noise | Voice | Avg | Ships? |
|---------|----------------|-------------|---------------|-----------------|-------|-----|--------|
| WS1: OCI Bidding | 9 | 9 | 8 | 9 | 8 | 8.6 | Yes |
| WS2: Modern Search | 9 | 9 | 9 | 8 | 8 | 8.6 | Yes |

---

## WS1: Intelligent Bidding (OCI) — 8.6/10, Ships

| Dimension | Score | Notes |
|-----------|-------|-------|
| First Paragraph | 9/10 | Three sentences. States what the doc covers, who it's for, and what the reader will know afterward. Kate gets the headline — +35,196 regs, $16.7MM OPS, three markets — without scrolling. The only reason it's not a 10: "It supports the Testing Approach narrative for Kate" is meta-commentary that Kate herself doesn't need. She knows why she's reading it. |
| Shareability | 9/10 | Kate could forward this to Todd or Brandon with zero additional context. The question-driven headers mean a VP can scan the TOC and jump to "How are we scaling in 2026?" without reading the full doc. The appendix tables are self-contained — someone who only sees the DE test data table still gets the story. |
| Actionability | 8/10 | Kate can brief the OCI story, approve the EU4 expansion plan, and ask the right question about hvocijid risk. What keeps it from 9: the "What are the risks" section identifies the hvocijid issue but doesn't give Kate a decision to make. "Under investigation with MarTech" is a status update, not a decision point. A sentence like "If unresolved by [date], the EU4 measurement phase will need to extend by X weeks" would give her something to act on. |
| Signal-to-Noise | 9/10 | Every section answers one question. No section restates another. The competitive strategy section is the tightest example — it takes the Walmart Brand CPA pressure ($40→$65-77), connects it to OCI NB efficiency as the offset, and lands the strategic point in three sentences. The cross-functional partners section is the only candidate for trimming — it reads like a credits roll — but it earns its place because Kate needs to know who to call. |
| Voice | 8/10 | Confident, direct, no hedging where the data is strong. "This is not incremental improvement. It is a fundamental shift in bidding efficiency." That sentence works. The DE underperformance section is honest without being defensive — it explains the DMA constraint and immediately connects it to the EU4 planning response. What holds it at 8: a few passages read more like a well-written brief than a narrative a human would speak aloud. "The team established a phased implementation plan — E2E keyword-level testing, then 25%, 50%, and 100% campaign-level application — with go/no-go gates at each phase" is accurate but mechanical. The information is right; the sentence doesn't breathe. |

### Composite: 8.6/10

Kate finishes this in under 10 minutes. She understands the OCI story, trusts the numbers, and can brief it upward. The doc earns its place as the detail layer behind the Testing Approach narrative. The two areas where it falls short of a 9 composite are (a) the risk section gives her a status update instead of a decision framework, and (b) a handful of sentences prioritize completeness over readability. Neither blocks shipping.

---

## WS2: Modern Search — 8.6/10, Ships

| Dimension | Score | Notes |
|-----------|-------|-------|
| First Paragraph | 9/10 | Leads with the result (+31% regs, +70% CTR), names the method (customer research), and tells Kate what she'll understand afterward. Same minor issue as WS1 — "It supports the Testing Approach narrative for Kate" is self-referential. Kate doesn't need to be told why she's reading a doc she asked for. But the opening sentence does the hard work: it tells her the team restructured campaigns AND rewrote ad copy, which frames the two-part structure of the doc before she encounters it. |
| Shareability | 9/10 | The SP study insight — 50% of Sole Proprietors believed Amazon Business required bulk purchasing, and our ads reinforced that misconception — is the kind of finding that travels. Kate could pull that single paragraph and drop it into a leadership update. The ad copy before/after table in the appendix is a standalone artifact. The UK test results table is clean enough to screenshot. Multiple surfaces for sharing without needing the full doc. |
| Actionability | 9/10 | This is the strongest dimension. Kate can (1) brief the SP study finding as a customer insight, (2) approve the EU4 rollout plan, (3) ask the right question about IT volume, and (4) understand why consolidation is a prerequisite for AI Max. The IT test is honestly flagged as LOW confidence with a clear next step (longer test window or higher-traffic campaign set). The EU4 translation risk is named — localized messaging effectiveness hasn't been validated. Kate has decisions to make, not just information to absorb. |
| Signal-to-Noise | 8/10 | The SP study section is the best-written section across both articles — it moves from survey data to misconception to ad copy fix in a tight logical chain. The campaign consolidation section is necessary but slightly front-loaded with structural detail ("split across device types and narrow keyword themes... each campaign had its own bid strategy operating on a thin slice of data") before reaching the insight. A reader who doesn't manage campaigns needs two reads to understand why fragmentation matters. The scaling section carries one redundant phrase — "combining campaign keyword themes to further reduce campaign count" restates what "keyword theme consolidation" already means. Minor, but it's noise. |
| Voice | 8/10 | "This is not a product problem; it is a messaging problem with a clear fix." That sentence is the best line in either article. It reframes the entire workstream in nine words. The confidence tags (HIGH for UK, LOW for IT) are honest and useful — they tell Kate where to trust the data and where to wait. Same limitation as WS1: some passages are technically precise but don't flow as natural prose. "Fewer campaigns means more conversions per bid strategy, which means faster algorithm learning" is a correct chain of logic, but it reads like a textbook explanation rather than a narrative insight. |

### Composite: 8.6/10

Kate finishes this in under 10 minutes. The SP study insight is the standout — it's the kind of customer research finding that changes how you think about the problem, and the doc builds the entire narrative around it. The ad copy mapping is a repeatable playbook. The UK test results are clean and credible. Where it falls slightly short: the campaign consolidation section requires more domain knowledge than the rest of the doc, and a few sentences optimize for precision over readability. Neither blocks shipping.

---

## Cross-article observations

Both articles share the same structural DNA — question-driven headers, prose-first narrative, appendix-heavy data, YAML frontmatter + AGENT_CONTEXT. This consistency is a feature, not a bug. Kate reads five workstream docs in sequence; the predictable structure means she spends cognitive effort on content, not navigation.

The strongest dimension across both is Shareability (9/9). These docs produce standalone artifacts — the DE test table, the SP study misconception paragraph, the ad copy before/after table — that travel without the full doc. That's the mark of a well-structured workstream detail page.

The weakest dimension across both is Voice (8/8). Both articles are confident and honest, but a handful of sentences in each prioritize mechanical completeness over narrative flow. This is a minor and consistent pattern — the writing is good, it's just occasionally stiff. Not a shipping blocker.

Both ship at 8.6. Both earn their place as the detail layer behind the Testing Approach doc.
