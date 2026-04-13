---
title: "Blind Test — Evaluator B"
status: DRAFT
audience: amazon-internal
owner: Richard Williams
created: 2026-04-12
updated: 2026-04-12
---
<!-- DOC-0465 | duck_id: wiki-review-blind-test-evaluator-b -->

# Blind Test — Evaluator B

> Independent evaluation. No prior reviews seen. Scored against wiki-critic.md rubric + richard-writing-style.md + richard-style-docs.md + richard-style-amazon.md as quality bar.
> Date: 2026-04-04

---

## Article 1: OCI Rollout Playbook

**File:** `shared/artifacts/testing/2026-03-25-oci-rollout-playbook.md`
**Type:** Strategy doc (OCI methodology and results)

| Dimension | Score | Notes |
|-----------|-------|-------|
| Usefulness | 9/10 | A teammate can replicate the OCI rollout in a new market by following this doc. The decision guide at the bottom is excellent — situation → action → why. The DE test-vs-control data table is the "prove it works" artifact the team needs. |
| Clarity | 8/10 | Structure is strong: Context → What OCI Does → Phased Rollout → Measurement → Market Status → Known Issues → Decision Guide. Headers are mostly imperative/question-style. "So what" interpretations follow every data table. One minor ding: the MCC Structure section is a reference table that interrupts the narrative flow — could be an appendix. |
| Accuracy | 8/10 | Every claim sourced in the Sources section. Numbers are dated and cross-referenced to research files. The $16.7MM OPS figure traces to oci-performance.md. Market status table has specific launch dates. One concern: the "Rollout Status" table says CA/JP/EU3 are "In Progress" but the Execution Guide (written 10 days later) shows FR/IT/ES/JP at 100% live — this doc's status table is stale relative to the companion doc. |
| Dual-audience | 9/10 | Rich YAML frontmatter (title, slug, type, audience, status, tags, depends_on, consumed_by, summary). AGENT_CONTEXT block present with machine_summary, key_entities, action_verbs, update_triggers. Prose is clean for humans. The `consumed_by` field listing specific analyst agents is a nice touch for agent routing. |
| Economy | 7/10 | At ~2,800 words this is the longest of the five. The Market-Specific Considerations table and the Validated Results table overlap with the Execution Guide — a reader who has both docs gets the same market notes twice. The "Context" section repeats information available in the 30-second summary of the Execution Guide. The Related section has a dead link (`competitive-landscape` with no path). Trim the market considerations table (it's better in the Execution Guide where it's paired with actionable per-market notes) and this tightens to an 8. |
| **Overall** | **8.2/10** | |

**Verdict:** PUBLISH (with minor revision)

**Required changes:**
- Update the Rollout Status table to reflect April 2026 reality (FR/IT/ES/JP now at 100%). Stale status tables erode trust.
- Fix the dead `competitive-landscape` link in Related section — either add the full path or remove it.

**Suggestions:**
- Consider cutting the Market-Specific Considerations table since the Execution Guide covers this better with actionable per-market notes. Cross-reference instead of duplicating.
- The MCC Structure table could move to an appendix or be a cross-reference to the Execution Guide.

---

## Article 2: OCI Execution Guide

**File:** `shared/artifacts/program-details/2026-04-04-oci-execution-guide.md`
**Type:** Execution doc (how-to for implementing OCI)

| Dimension | Score | Notes |
|-----------|-------|-------|
| Usefulness | 9/10 | This is the doc the style guide calls "Instructional / How-To" — and it nails the pattern. Imperative mood throughout ("Select campaigns", "Change bidding strategy", "Monitor"). The "What NOT to Do" section up front is exactly what richard-style-docs.md prescribes. The troubleshooting table is immediately actionable. A teammate can execute OCI in a new market without asking Richard. |
| Clarity | 9/10 | Excellent structure: What OCI Is (30-sec) → What NOT to Do → Prerequisites → Step-by-Step → Scaling → Troubleshooting → Per-Market Notes → Quick Reference. Headers are imperative. The monitoring table (What to check / Where / What to Look For) is perfectly scannable. The cross-reference to the Playbook at the top cleanly separates strategy from execution. |
| Accuracy | 8/10 | Sources section is thorough. Gate criteria (115%, 110%) are honestly noted as "derived from D1 methodology + operational experience" rather than pretending they're empirically validated — good intellectual honesty. Market status table is current as of April 2026. One flag: the "What NOT to Do" rule #5 says "AU/MX do not have OCI" but the Per-Market Notes show AU targeting May 2026 — this is consistent but could confuse a reader in June 2026 when AU may be live. Needs an update trigger. |
| Dual-audience | 8/10 | YAML frontmatter present with `replaces` field (nice — tells agents which old docs this supersedes). AGENT_CONTEXT block with machine_summary, key_entities, action_verbs, update_triggers. The `replaces: oci-implementation-guide, oci-methodology-knowledge-share` is excellent for agent deduplication. Minor ding: `level: N/A` in frontmatter — this should be level 2 (it's a team-facing execution doc). |
| Economy | 8/10 | Tight. The "What NOT to Do" section is 6 items — exactly the right length (style guide says max 3 bullets per list, but these are numbered rules, not bullets, and each earns its place). The Per-Market Notes table is concise — one row per market, one sentence each. The Quick Reference at the end is a smart addition for repeat users who don't need the full walkthrough. No significant bloat. |
| **Overall** | **8.4/10** | |

**Verdict:** PUBLISH

**Suggestions:**
- Set `level: 2` in frontmatter (this is clearly a team-facing doc).
- Add a note to "What NOT to Do" #5 that it should be updated when AU goes live on OCI.
- The monitoring cadence table in Step 3 is good but could add "Where" column entries for the Google Ads navigation paths (some are there, some aren't).

---

## Article 3: AU Market Wiki

**File:** `shared/artifacts/program-details/2026-04-04-au-market-wiki.md`
**Type:** Reference doc (Australia market)

| Dimension | Score | Notes |
|-----------|-------|-------|
| Usefulness | 8/10 | This is the "one doc, one source of truth" for AU — and it delivers. Before a meeting with Lena, you load this. Before writing an AU callout, you check this. The stakeholder table with communication styles is genuinely useful ("Expects numbers, not narratives" for Lena). The CPC Challenge section pre-loads the counter-argument Richard needs. Open Questions section drives action. |
| Clarity | 8/10 | Clean structure: Overview → Performance → Campaign Structure → Active Initiatives → Stakeholders → CPC Challenge → Competitors → Meetings → Decisions → Open Questions. Headers are descriptive. The performance table is scannable. One ding: the "Active Initiatives" section has 4 subsections of varying depth — OCI Integration is 3 sentences while Polaris is a full paragraph. Normalize the depth or use a consistent format. |
| Accuracy | 8/10 | Sources section maps every claim to a body organ or context file. Performance data is dated (Feb 2026, W13). Stakeholder dynamics sourced to memory.md. One concern: "No competitors in AU currently" is a strong claim — is this verified recently, or is it an absence-of-evidence situation? The doc doesn't distinguish. Also, the W13 data (207 regs, -16% WoW) is a single week — presenting it alongside monthly data without flagging the volatility risk is slightly misleading. |
| Dual-audience | 8/10 | YAML frontmatter with `replaces` field (good for agent dedup). AGENT_CONTEXT block present and useful. The `update-trigger` field is specific and actionable ("AU performance shifts >10%, OCI AU launch"). Minor ding: the Key Decisions table is useful for humans but not structured for agent extraction — adding decision IDs that cross-reference brain.md would help. |
| Economy | 7/10 | The Competitors section is one sentence: "No competitors in AU currently." That's a section header for one line — either expand it (when did we last check? what would change this?) or fold it into Overview. The Recurring Meetings section is 2 lines — same issue. The "Key Decisions" table has 4 entries, which is fine, but the "Rationale" column is thin ("Lena overrode phased test recommendation" — what was the rationale for the override?). Some sections don't earn their headers. |
| **Overall** | **7.8/10** | |

**Verdict:** REVISE

**Required changes:**
1. Fold the Competitors section into Overview or expand it with verification date and monitoring approach. A one-sentence section violates economy.
2. Fold Recurring Meetings into a line in the Stakeholders section or remove it — 2 lines don't earn a header.
3. The "No competitors" claim needs a confidence qualifier: "No competitors identified as of [date]. Last verified: [source]." Unqualified absence claims are accuracy risks.
4. Normalize Active Initiatives subsection depth — either all get 2-3 sentences or all get a paragraph. The inconsistency makes it look unfinished.

**Suggestions:**
- Add decision IDs to Key Decisions table that cross-reference brain.md (e.g., "D4: AU Landing Page").
- The Open Questions section is strong — consider adding owner and target date for each question to make it actionable rather than just informational.
- W13 weekly data should be flagged as "single week, directional only" to avoid over-indexing on one data point.

---

## Article 4: Enhanced Match / LiveRamp

**File:** `shared/artifacts/testing/2026-04-04-enhanced-match-liveramp.md`
**Type:** Strategy doc (LiveRamp Enhanced Match)

| Dimension | Score | Notes |
|-----------|-------|-------|
| Usefulness | 7/10 | This doc captures an in-flight investigation — it tells you what's happening and what needs to happen next. The Next Steps section is clear. The Connection to Existing Initiatives section is genuinely useful for understanding why this matters. But the core problem: Brandon's 4 questions are unanswered. The doc is a well-organized status update, not a strategy doc. It helps you UNDERSTAND the situation but doesn't help you DO or DECIDE anything beyond "Richard needs to call Abdul." |
| Clarity | 7/10 | Structure is logical: What's Happening → Brandon's Questions → Current State → EU Expansion → Connections → ABMA Protocol → Next Steps. Headers are descriptive. But the doc reads more like synthesized meeting notes than a strategy document. The ABMA SIM Escalation Protocol section feels bolted on — it's tangentially related but breaks the narrative flow. The "What's Happening" section is 2 paragraphs of context-setting before getting to the substance. |
| Accuracy | 8/10 | Every claim sourced to specific Slack messages with dates and participants. The 13%→30% match rate improvement is sourced to brain.md. The 5.6M→1.2M audience drop is attributed to Andrew Wirtz with a specific date. This is well-sourced for a doc that's essentially synthesizing real-time signals. |
| Dual-audience | 7/10 | YAML frontmatter present but thinner than the other docs (no `replaces`, no `consumed_by`, no `depends_on`). AGENT_CONTEXT block is present and useful. The `update-trigger` field is good. But the doc lacks the structured data that makes it agent-queryable — there's no table summarizing the current state, no structured timeline, no decision matrix. An agent can read it but can't easily extract structured answers. |
| Economy | 6/10 | The ABMA SIM Escalation Protocol section is 1 paragraph that belongs in a different doc (maybe a process doc or memory.md). It's relevant context but doesn't earn a full section in a strategy doc about Enhanced Match. The "What's Happening" section's first paragraph is 4 sentences of background that could be 1. The "Connection to Existing Initiatives" section has 3 subsections — the OCI Bidding connection is speculative ("could indirectly benefit") and the Email Overlay connection is thin. Two strong connections (F90, Email Overlay) would be tighter than three where one is weak. |
| **Overall** | **7.0/10** | |

**Verdict:** REVISE

**Required changes:**
1. Remove or relocate the ABMA SIM Escalation Protocol section. It's a process update, not Enhanced Match strategy. Move it to memory.md or a separate process doc.
2. Cut the OCI Bidding connection paragraph — it's speculative and adds no actionable insight. Two strong connections > three where one is filler.
3. Tighten "What's Happening" — the first paragraph should be 1-2 sentences, not 4. Lead with the "so what": "Brandon is driving an Enhanced Match investigation to improve LiveRamp match rates beyond the current 30%. Robert Skenes confirmed Richard's segment is approved."
4. Add a structured summary table at the top: Current match rate, Target match rate (if known), Status, Blocker, Owner, Next action, Due date. This makes the doc queryable for both humans and agents.
5. Add `depends_on` and `consumed_by` to frontmatter.

**Suggestions:**
- This doc will improve dramatically once Brandon's 4 questions are answered. Consider marking it as "INVESTIGATION" rather than "DRAFT" in status — it's not a strategy doc yet, it's an investigation tracker.
- The audience drop (5.6M→1.2M) deserves its own subsection under Current State rather than being buried in a paragraph. That's a 78% drop — it should be visually prominent.

---

## Article 5: ie%CCP Planning & Optimization Framework

**File:** `shared/artifacts/strategy/2026-03-30-ieccp-planning-framework.md`
**Type:** Strategy doc (ie%CCP budget framework)

| Dimension | Score | Notes |
|-----------|-------|-------|
| Usefulness | 9/10 | This is the doc the style guide calls a "Testing Plan / Strategy Document" — and it's the strongest of the five. Someone who doesn't understand ie%CCP will after reading this. Someone who does understand it will find the four scenarios, the marginal CPA curve, and the MX case study immediately actionable. The "Applying This to Callouts" section is brilliant — it pre-loads the exact framing for weekly decisions. The Quick Reference at the end is a cheat sheet that earns its place. |
| Clarity | 9/10 | Exceptional structure. Builds from simple (what ie%CCP measures) to complex (blended math, four scenarios, marginal CPA curve) to applied (MX case study, callout framing). The ASCII diagrams for the formula and the lever maps are effective. The "Why It's Confusing" section is honest and pedagogically smart — it names the trap before the reader falls into it. Headers are questions or imperatives throughout. The subsidy model explanation (Brand CPA $21 vs NB CPA $134) is crystal clear. |
| Accuracy | 7/10 | The MX case study uses specific numbers ($1.8M allocation, $542K OP2, Brand CPA $21, NB CPA $134) that appear internally consistent. The FY25 historical example (budget cut from $1.97M to $1.07M) adds credibility. But: the Sources section is missing. There is no Sources section at all. For a doc that makes specific claims about CCP values ($150/$50 → $80/$30 → $90/$30), OP2 targets, and Brand performance (2.7x YoY), the absence of source attribution is a significant gap. The AGENT_CONTEXT block exists but doesn't compensate for missing source traceability in the prose. Also: "Conservative Brand estimates (LY seasonal shape × 2.7x, then -10% haircut)" — what's the basis for the 10% haircut? It's presented as a methodology choice without justification. |
| Dual-audience | 8/10 | YAML frontmatter present with good metadata. AGENT_CONTEXT block is strong — the machine_summary captures the key insight ("Brand is the engine"). But no `depends_on`, `consumed_by`, or `replaces` fields. The structured tables throughout serve both audiences well. The formula blocks are agent-parseable. Minor ding: the four scenarios would benefit from scenario IDs (S1-S4) that agents could reference. |
| Economy | 8/10 | At ~3,000 words this is the longest article, but every section earns its place. The four scenarios could arguably be condensed — Scenario 4 (unconstrained + loose) is acknowledged as "rare in practice" and gets 5 lines, which is appropriate. The Levers section (ranked 1-4) is well-structured. The MX case study is detailed but justified — it's the proof that the framework works. One ding: the "Budget Planning: The Stakeholder View" section's "What Changes the Plan" table has 6 rows that could be 4 (combine the CCP rows, combine the Brand rows). Minor bloat. |
| **Overall** | **8.2/10** | |

**Verdict:** PUBLISH (with minor revision)

**Required changes:**
- Add a Sources section. This is the only article of the five without one, and it makes the most specific numerical claims. Every CCP value, every OP2 target, every Brand performance figure needs a source. This is a hard blocker — the wiki-critic rubric says "Every claim traceable to a source" for an 8+ accuracy score.

**Suggestions:**
- Add `depends_on` and `consumed_by` to frontmatter for agent routing.
- Justify the "10% haircut" on Brand estimates — is this a standard conservatism factor, or based on historical forecast accuracy?
- Add scenario IDs (S1-S4) to the four scenarios for cross-referencing in callouts and other docs.
- The "What Changes the Plan" table could consolidate CCP-up and CCP-down into one row with bidirectional arrows, same for Brand-up and Brand-down.

---

## Summary Table

| # | Article | Use | Clarity | Accuracy | Dual-Aud | Economy | Overall | Verdict |
|---|---------|-----|---------|----------|----------|---------|---------|---------|
| 1 | OCI Rollout Playbook | 9 | 8 | 8 | 9 | 7 | **8.2** | PUBLISH (minor rev) |
| 2 | OCI Execution Guide | 9 | 9 | 8 | 8 | 8 | **8.4** | PUBLISH |
| 3 | AU Market Wiki | 8 | 8 | 8 | 8 | 7 | **7.8** | REVISE |
| 4 | Enhanced Match / LiveRamp | 7 | 7 | 8 | 7 | 6 | **7.0** | REVISE |
| 5 | ie%CCP Planning Framework | 9 | 9 | 7 | 8 | 8 | **8.2** | PUBLISH (minor rev) |

**Portfolio average: 7.9/10**

---

## Style Guide Compliance Notes

**Richard's voice (richard-writing-style.md):**
- Articles 1, 2, and 5 nail the voice: direct, opinionated, evidence-based. "Never go from 0% to 100%" (Art 1), "Do not judge OCI by week 1" (Art 2), "Brand is the engine; NB is the passenger" (Art 5) — these are Richard's voice.
- Article 3 is competent but slightly flat — it reads more like a reference card than something Richard wrote. The stakeholder section has personality ("Expects numbers, not narratives") but the rest is neutral.
- Article 4 reads like synthesized Slack notes. It has Richard's parenthetical style ("(13% match rate)") but lacks the opinionated framing that characterizes his best work.

**Amazon writing norms (richard-style-amazon.md):**
- "Lead with the so what": Articles 1, 2, and 5 do this well. Article 4 buries the so-what under context paragraphs. Article 3 leads with overview (acceptable for a reference doc).
- "Connect metrics to registrations/OPS/CX": Articles 1 and 2 connect OCI to $16.7MM OPS and +35K regs. Article 5 connects ie%CCP to registration capacity. Article 4 connects match rate to F90 addressable audience. Article 3 connects CPC decline to CPA (but doesn't close the loop to registrations).
- "State confidence levels": None of the five articles use the HIGH/MEDIUM/LOW confidence framework from the Amazon style guide. Article 1 comes closest with "statistically meaningful lift" language. This is a systematic gap.

**Doc style guide (richard-style-docs.md):**
- "Headers must be questions or imperatives, never bare nouns": Articles 2 and 5 comply well. Article 1 mostly complies but has "MCC Structure" and "Rollout Status" (bare nouns). Article 3 has "Current Performance", "Campaign Structure", "Competitors" (bare nouns). Article 4 has "Current State", "Next Steps" (bare nouns). Systematic weakness.
- "Every list item must start with a verb or a number": Articles 1 and 2 comply. Article 5 complies. Articles 3 and 4 have noun-only list items in places.
- "Max 3 bullet points per list": Article 2's "What NOT to Do" has 6 items (but they're numbered rules, not bullets — arguable). Article 4's Next Steps has 5 items. Generally compliant.

**Confidence calibration gap:** The biggest systematic issue across all five articles is the absence of confidence levels. The Amazon style guide defines HIGH/MEDIUM/LOW with specific criteria (weeks of data, event counts, trend consistency). None of the articles use this framework. The ie%CCP doc's "Conservative Brand estimates" section would benefit most — the 2.7x Brand growth claim should carry a confidence tag.

---

## Evaluator B Assessment

The two OCI docs (Playbook + Execution Guide) are the strongest pair. They complement each other well — strategy vs. execution — and both meet the 8/10 bar. The ie%CCP framework is the most intellectually ambitious and nearly meets the bar, but the missing Sources section is a real gap for a doc making specific financial claims.

The AU Market Wiki is close but has structural issues (one-sentence sections, inconsistent subsection depth) that make it feel unfinished. A focused revision pass would bring it to 8.

The Enhanced Match doc is the weakest — it's an investigation tracker masquerading as a strategy doc. It needs either more substance (answers to Brandon's questions) or a reclassification to "investigation" status. At 7.0, it's the furthest from shippable.

No article uses the confidence calibration framework. This should be a standard element in any doc that makes data claims.
