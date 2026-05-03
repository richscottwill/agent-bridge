# Review: AU Keyword CPA Dashboard — Eval B (Reader Simulation)
Reviewed: 2026-05-01 23:20
Slug: au-keyword-cpa-dashboard
Draft version: 2026-05-01
Eval mode: B — reader simulation (Lena Zak, AU PS lead)
Consecutive sub-8: 0

## Persona

Lena Zak. AU PS lead, data-pragmatic, weekly sync attendee. She challenged AU CPC benchmarks publicly (3/19), asked pointed follow-up questions about landing page URLs, repeat-visitor CPA overstating, and redirect attribution (4/1). She wants numbers she can trust and actions she can take. She does not tolerate hand-waving. Secondary reader: Megan Oshry's team, inheriting AU from Richard — they need to run the weekly pull without Richard on the call.

## Constraint check

**Citation integrity.** The Sources section lists six references, all pointing to body system or context files. Two TODO comments remain in the draft: (1) the $140 CPA target source is uncited — the doc says "eyes.md Market Health → AU" but eyes.md shows AU W13 CPA at $118 with NB CPA at $187, no explicit $140 target figure; (2) the 10% attribution gap threshold is flagged as uncalibrated. These are not cosmetic — Lena will ask "where does $140 come from?" in the first sync. **Constraint violation: uncited threshold claim.**

**Reference structure.** Frontmatter is complete: slug, doc-type, audience, status, depends_on, consumed_by, tags, summary. AGENT_CONTEXT block is present with machine_summary, key_entities, action_verbs, and update_triggers. Cross-references to WBR Callout Guide and body system files are valid. No broken links detected.

**Audience alignment.** The doc names Lena as the primary reader in the opening paragraph and addresses her three priorities (keyword CPC/CPA investigation, keyword-to-product mapping, Polaris migration tracking) — all three confirmed in current.md. The transition context for Megan's team is present but thin (one paragraph, no operational detail on who does what).

## Scores

| Dimension | Score | Notes |
|-----------|-------|-------|
| Usefulness | 8/10 | Lena can run the weekly review from this doc. The action threshold table is the strongest section — she can look up a CPA range and know what to do. The "what can go wrong" section preempts her attribution questions. Docked because it does not address her specific 4/1 follow-ups (landing page URLs in the data, repeat-visitor CPA overstating, redirect click counts). |
| Clarity | 8/10 | Structure is scannable. Each view gets its own "How to read" section with a clear question it answers. The CPA-spike diagnostic paragraph (cost increase vs. conversion drop) is excellent — it teaches the reader to think, not just look. Minor ding: the "How to use the keyword-to-product mapping" section buries the Polaris migration caveat in the second paragraph when it should lead, since Polaris is the active disruption Lena cares about. |
| Accuracy | 6/10 | Two uncited claims flagged by the author's own TODO comments. The $140 CPA target is the load-bearing number in the entire doc — every threshold and trend interpretation references it — and it has no verified source. Eyes.md shows AU W13 CPA at $118 and NB CPA at $187 but no $140 target. The 10% attribution divergence threshold is also uncalibrated. The doc correctly states AU uses DB registrations (confirmed in current.md) and correctly describes the manual pull limitation (no API access, confirmed in eyes.md showing AU MCC "Not created"). Historical CPA range ($120-$180) is consistent with eyes.md W13 data. But the two uncited thresholds are the numbers Lena will use to make decisions, and they are the two numbers without sources. |
| Dual-audience | 8/10 | Strong on both sides. Frontmatter is rich enough for agent indexing (consumed_by, depends_on, tags, AGENT_CONTEXT with update_triggers). Prose is written for a human operator. The action threshold table bridges both — an agent can parse it, a human can scan it. The AGENT_CONTEXT machine_summary is accurate and concise. |
| Economy | 7/10 | The "Next steps (historical context)" section is dead weight. It describes tasks from March 2026 that "should be complete by now" — retained for "provenance" but providing zero operational value. Lena does not need provenance; she needs current state. The Automation path section repeats the dashboard ingester description from the data sourcing section (both mention the tool, its status, and the column-format prerequisite). The Delivery section is two sentences that could be folded into the opening paragraph. The Sources section earns its place. The Related section earns its place. Overall the doc is ~1,800 words; it could be ~1,500 without losing value. |
| **Average** | **7.4/10** | |

## Verdict

**REVISE**

The doc is close. The structure is right, the action framework is right, and Lena would recognize her priorities in it. But she would not trust the $140 target without a source, and she would notice that her three specific follow-up questions from 4/1 are not addressed. The Economy issues are fixable in one pass.

## The core Eval B question: does Lena have what she needs?

Lena can run the weekly review mechanically — pull data, populate views, read the threshold table, decide what to flag. That workflow is well-documented. But three gaps would surface in the first sync:

1. **The $140 target is unjustified.** Lena challenged AU CPC benchmarks publicly. She will challenge this number. If it comes from an OP2 plan, cite the plan. If it is a team convention, say so. If it is aspirational, say that too. But "AU CPA target: $140" with no source will not survive her scrutiny.

2. **Her 4/1 questions are unanswered.** She asked: (a) can we get data with landing page URLs? (b) how many clicks redirect because the customer is already logged in? (c) are we overstating CPAs due to repeat visitors? The doc's "what can go wrong" section touches on attribution gaps and redirect chains but does not directly answer these questions or explain whether the dashboard can surface landing page URL data. A one-paragraph addition addressing each question (even if the answer is "the dashboard does not currently include this; here is how to get it") would close the gap.

3. **Megan's team handoff is too thin.** The transition context is one paragraph naming the handoff. Megan's team needs to know: who currently does the weekly pull (Richard? Alexis?), what the export template looks like, where the joined dataset lives, and who to escalate to when the data looks wrong. Without this, the first week Richard is not on the call, the pull does not happen.

Can Megan's team pick this up without Richard? Not from this doc alone. The methodology is clear, but the operational "who does what, where does the file go, what does the export template look like" is missing.

## Required changes

1. **Cite or qualify the $140 CPA target.** The TODO comment at line 51 must be resolved before publishing. Either cite the source (OP2 plan, Brandon directive, team convention) or rewrite as: "The working AU CPA target is $140, established during the Brandon sync on 2026-03-23 as the threshold for keyword-level action. This is a team operating target, not an OP2 plan figure." — whichever is accurate.

2. **Cite or qualify the 10% attribution gap threshold.** The TODO comment at line 106 must be resolved. Either calibrate from historical data or state: "The 10% threshold is a starting heuristic. Calibrate against the first four weeks of dashboard data and adjust."

3. **Address Lena's 4/1 follow-up questions.** Add a subsection under "What can go wrong with this data" or as a standalone FAQ:
   - Landing page URLs: state whether the Google Ads export includes final URL data and whether the dashboard surfaces it.
   - Repeat visitor / logged-in redirect clicks: state whether the attribution methodology accounts for these or whether they inflate CPA.
   - If the answers are unknown, say so explicitly and name the action to resolve them.

4. **Cut the "Next steps (historical context)" section.** It provides no operational value. If provenance matters, move it to an HTML comment or a changelog appendix. It should not be in the main body.

5. **Consolidate the dashboard ingester references.** The ingester is described in "How the data is sourced and refreshed" (paragraph 3) and again in "Automation path." Merge into one location — the Automation path section — and remove the duplicate from the sourcing section. Replace with a forward reference: "For the automation path to replace this manual process, see the Automation section below."

6. **Expand the transition context for Megan's team.** Add operational detail: who currently performs the weekly pull, where the export template lives (or that one needs to be created), where the joined dataset is stored, and who the escalation contact is for data quality issues. Two to three sentences minimum.

## Suggestions (optional, non-blocking)

- The keyword-to-product mapping section should lead with the Polaris migration caveat, not bury it in paragraph two. Lena's third priority is Polaris migration tracking — put the active disruption first.
- Consider adding a "Weekly review checklist" — a 5-step numbered list (export, validate row counts, join, populate views, flag actions) that Megan's team can follow mechanically. This would be the single most useful addition for the handoff audience.
- The Delivery section ("delivered as an Excel or Quip table, per Lena's preference") could be folded into the opening paragraph to tighten the doc.
- Eyes.md shows AU NB CPC declining for 7 weeks ($6.82→$4.81, -29%) — the doc could note this trend as context for interpreting CPC in the Top 20 views, since a declining CPC baseline changes what "high CPC" means week to week.
