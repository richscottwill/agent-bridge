---
title: "Eval A Review: Paid Search Five-Year Outlook v2"
status: DRAFT
audience: amazon-internal
owner: "Richard Williams"
created: 2026-05-01
updated: 2026-05-01
---

# Review: Paid Search Five-Year Outlook v2 (Eval A — Strict Rubric)

Reviewed: 2026-05-01 23:10
Slug: five-year-outlook-v2
Draft version: 2026-04-05 (from frontmatter `updated` date)
Consecutive sub-8: 0 (no prior Eval A review found for v2)

---

## Constraint check

No `constraints:` list declared in article frontmatter. Evaluated against default style/audience-by-doc-type defaults per wiki-pipeline-rules.md §8 equivalent defaults.

| Default constraint | Verdict | Rationale |
|--------------------|---------|-----------|
| **Audience: amazon-internal leadership tone** (Kate-level reader) | PASS | Prose is direct, data-grounded, avoids jargon without explanation. Confidence labels are explicit. The Purpose paragraph frames an ask (endorsement of 2026 test plan). Tone is appropriate for a VP reading a strategy doc — no coaching language, no hype. |
| **Doc-type: strategy doc — decision framing and fallback positions** | PASS | The executive summary decision table provides four bets with explicit "if it works / if it doesn't / when we know" framing. The Downside section addresses the speculative horizon. Each bet has a named fallback. This is a strategy doc that asks for a decision and shows what happens if the bets fail. |
| **Citation discipline: substantive claims cited** | PASS | Every external claim carries a parenthetical source and date (Nav43 2025, Stackmatix/Conductor/Seer 2026 Q1, Gartner 2024, etc.). Internal claims reference body system docs by name. Appendix A organizes sources by confidence tier (HIGH/MEDIUM/LOW). No `<!-- TODO: cite -->` markers found (grep confirmed). |

---

## TODO marker check

Grep for `TODO: cite` and `TODO`: **zero matches**. No uncited claims flagged by the author.

---

## Scores

| Dimension | Score | Notes |
|-----------|-------|-------|
| Usefulness | 9/10 | Reader can endorse or reject four named bets, each with a go/no-go date and fallback. The decision table alone makes this actionable. A leadership reader gets 95% of the value from the main body without touching the appendix. |
| Clarity | 8/10 | Structure is clean: Purpose → Executive Summary → 2026 (high confidence) → 2027 (medium) → Downside → Appendices. Confidence labels in headers orient the reader. One minor issue: the 2026 section covers seven distinct topics (OCI status, ad copy test, Baloo, F90, AI Max, external signals, agentic tooling) in a single run of prose without subheadings, which makes scanning harder than it should be for a section of that density. |
| Accuracy | 8/10 | Internal claims (OCI 35K regs, $16.7M OPS, UK ad copy 86% CTR lift, F90 $765K iOPS) are attributed to named body system docs with dates. External claims carry source and date. Confidence tiers in Appendix A are honest about what is measured vs. directional vs. forecast. One minor concern: the frontmatter `updated: 2026-04-05` is 26 days old — if the article was revised for v2, the updated date should reflect the revision date, not the original creation date. This is a metadata hygiene issue, not a factual accuracy issue. |
| Dual-audience | 9/10 | AGENT_CONTEXT block is present with depends_on, consumed_by, tags, category, refresh_trigger, key_entities, and a machine_summary. Frontmatter includes confidence, update-trigger, and level. Prose serves humans. An agent swarm can index, retrieve, and reason over this doc. The machine_summary is a good one-paragraph distillation. |
| Economy | 7/10 | The main body is tight and narrative-driven — no bullet list abuse, no table abuse (the one table IS the argument), no formatting-as-content. Appendix A earns its place by organizing sources by confidence tier. However: Appendix B (Internal Reference Documents) is a six-item bullet list of file paths that duplicates information already in the AGENT_CONTEXT `depends_on` block and in the body's parenthetical citations. It adds no value for a human reader (who won't navigate file paths) and no value for an agent (who already has `depends_on`). This section should be cut. Additionally, the 2027 section's paragraph on Gartner's 75% AI adoption and 40% cancellation projections, followed by "The teams that survive build for sustainability, not hype," reads as editorializing rather than analysis — it doesn't connect back to a specific AB decision or action. That sentence should either tie to a concrete PS team implication or be cut. |
| **Average** | **8.2/10** | |

---

## Verdict

**PUBLISH**

Overall average 8.2/10. No dimension below 7. The article meets the bar.

---

## Required changes

None required for PUBLISH verdict. Economy at 7 is the floor — the two issues below are strong recommendations that would lift it to 8.

---

## Suggestions (non-blocking)

1. **Cut Appendix B.** The six-item reference list duplicates `depends_on` in AGENT_CONTEXT and the inline citations in the body. Neither a human reader nor an agent gains value from a list of file paths. Removing it tightens Economy without losing information.

2. **Tighten the 2027 Gartner editorial.** The sentence "The teams that survive build for sustainability, not hype" is a general truism, not an AB-specific insight. Replace with a concrete implication:

   > Current: "The teams that survive build for sustainability, not hype."
   >
   > Suggested: "The PS team's text-file-based infrastructure avoids the enterprise platform costs that drive Gartner's projected cancellation wave."

   This connects the external signal to the specific AB advantage.

3. **Add subheadings to the 2026 section.** The section covers seven topics in continuous prose. Adding three subheadings (e.g., "OCI and Campaign Foundation," "New Bets: Baloo, F90, AI Max," "External Signals and Agentic Tooling") would improve scannability without adding words. This is a Clarity improvement that would push the score from 8 to 9.

4. **Update frontmatter `updated` date.** Currently reads `2026-04-05`, which appears to be the v1 creation date. If this is v2, the updated field should reflect the revision date.
