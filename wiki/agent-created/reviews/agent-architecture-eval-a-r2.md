<!-- DOC-0454 | duck_id: wiki-review-agent-architecture-eval-a-r2 -->
# Review: Agent System Architecture — Eval A (Revision 2)

Reviewer: wiki-critic (Eval A — rubric)
Date: 2026-04-05
Article: `shared/context/wiki/staging/agent-architecture.md`
Revision: 2 (post-Economy fixes from R1)

## Scores

| Dimension | Score | Notes |
|-----------|-------|-------|
| Usefulness | 9/10 | A new AI or human observer can bootstrap from this doc. Cold start protocol, decision guide, and directory structure make it immediately actionable. The only gap: no worked example of an end-to-end flow (e.g., "Richard clicks morning routine → here's exactly what happens step by step across all three layers"). |
| Clarity | 9/10 | Three-layer structure is clean and the article follows it faithfully. Headers tell the story. The ASCII diagram orients the reader before prose begins. Each section answers one question. Minor: the "How the System Compounds" section is the weakest structurally — it covers three distinct compounding mechanisms (autoresearch, nervous system, wiki externalization) in one paragraph where two sentences would benefit from being unpacked. |
| Accuracy | 8/10 | Claims are well-sourced — 11 sources listed, cross-references to specific files. Numbers are specific (11 organs, 5 hooks, 13 agents, 9 calibration loops, 700+ experiments, 23,000-word budget). The agent consolidation history (6 → 2 parameterized) is cited to a spec. One concern: "700+ experiments as of March 2026" appears twice (Layer 2 and Compounding section) — if the number has changed since March, both instances need updating. The `<!-- TODO -->` discipline from pipeline rules is not needed here since no unverifiable claims about timelines or deliverables are made. |
| Dual-audience | 9/10 | AGENT_CONTEXT block is present with machine_summary, key_entities, action_verbs, and update_triggers. Frontmatter is rich YAML with all required fields (depends_on, consumed_by, update-trigger). Prose serves humans well — narrative structure, not data dump. The directory tree serves both audiences. One gap: the AGENT_CONTEXT machine_summary could include the cold start sequence (portable-body/README.md → body.md → spine.md → soul.md) since that's high-value for agent retrieval. |
| Economy | 8/10 | Significant improvement from R1. Prose-forward throughout — bullets are rare and justified. Tables have interpretive context. No section feels redundant. The Sources section earns its place by being specific (file paths + what each source contributes). The Decision Guide table uses action verbs in every row. Two minor observations: (1) the Portability section's "What's platform-specific" list is a single long sentence with five items separated by commas — this is the one place where a short bullet list would actually improve readability, but the current form is acceptable. (2) "See cold start protocol in Portability section above" in the Decision Guide is a cross-reference within the same doc, which is fine for a doc this length but worth watching if the doc grows. |
| **Overall** | **8.6/10** | |

## Verdict

PUBLISH

## Suggestions (optional, non-blocking)

1. **AGENT_CONTEXT enrichment:** Add the cold start sequence to `machine_summary` — an agent querying "how do I bootstrap this system?" should get that from the structured block without parsing the full prose.

   Current:
   ```
   Designed for portability — all plain text, cold start in 2-3 hours.
   ```
   Suggested:
   ```
   Designed for portability — all plain text, cold start in 2-3 hours via portable-body/README.md → body.md → spine.md → soul.md.
   ```

2. **Compounding section:** Consider splitting the single paragraph into two: one for autoresearch compounding (experiments → accuracy gains), one for system-level compounding (nervous system calibration + wiki externalization freeing word budget). This would make the section's structure match the rest of the doc's one-idea-per-paragraph discipline. Non-blocking because the current version is clear enough.

3. **Duplicate number:** "700+ experiments as of March 2026" appears in both the Autoresearch Loop subsection and the Compounding section. Consider making one the canonical mention and having the other reference it, or updating both to the current count if it has changed since March.
