<!-- DOC-0455 | duck_id: wiki-review-agent-architecture-eval-b -->
# Review: Agent System Architecture (Eval B — Reader Simulation)

**Reviewer persona**: Brandon Munday (L7, Richard's manager)
**Reader question**: How does Richard's agent system work? Is the architecture sound — maintainable, portable, scalable? Could someone else pick it up?
**Date**: 2026-04-05

## Scores

| Dimension | Score | Notes |
|-----------|-------|-------|
| Usefulness | 8/10 | Brandon can assess the architecture, understand the pieces, and evaluate bus-factor risk. The Decision Guide table at the end is genuinely actionable — it answers "what do I do when X happens?" The cold start protocol gives him confidence someone else could bootstrap. Falls short of 9 because it doesn't address scaling limits or failure modes — Brandon would want to know what breaks first under load, and what happens when an experiment corrupts an organ. |
| Clarity | 7/10 | The three-layer structure is clean and the ASCII diagram earns its place. The progression from Body → Hooks → Agents is logical. However, two sections bury their key insight. The "How the System Compounds" section opens with a general claim ("designed to get better over time without getting bigger") and takes three paragraphs to explain three distinct mechanisms — each paragraph is doing double duty as both explanation and evidence, which forces re-reading. The "Safety Guards" subsection is nested under Hooks but describes a fundamentally different concept (structural prevention vs. event-driven automation) — Brandon would pause and wonder why guards are hooks. The Routing Rules table headers ("Trigger Pattern" / "Route To") are clear, but the table itself is a reference lookup, not a narrative — it interrupts the flow of the Agent Swarm section rather than supporting it. |
| Accuracy | 8/10 | Claims are well-sourced — the Sources section at the bottom traces every major claim to a specific file. The agent count (13 custom) is verifiable against the directory structure. The consolidation history (6 per-region → 2 parameterized) is specific and dated. The "630 lines, 700 experiments" claim for the autoresearch loop is precise enough to check. One concern: the doc states the cold start takes "2-3 hours" but provides no evidence for this estimate — is it tested or aspirational? Brandon would want to know if anyone has actually done a cold start. The word budget figure (23,000 with 24,000 ceiling) is stated without explaining what happens when the ceiling is hit. |
| Dual-audience | 8/10 | The AGENT_CONTEXT block is present and well-structured — machine_summary, key_entities, action_verbs, and update_triggers all serve agent indexing. The frontmatter is rich. The prose serves Brandon well as a human reader. The directory structure diagram is useful for both audiences. Minor gap: the agent team tables are structured data that agents can parse, but they lack the "so what" interpretation that would help Brandon prioritize which teams matter most. The Related section uses file paths that serve agents but are opaque to Brandon — he doesn't know what `~/shared/context/body/heart.md` contains without clicking through. |
| Economy | 6/10 | This is where the doc loses ground. Several specific violations: |

**Economy violations (detailed):**

1. **Bullet list abuse.** The "Design philosophy draws from three sources" list is noun-phrase padding. "Andrej Karpathy's autoresearch — small, fast, autonomous experimentation loops that compound" contains no verb telling Brandon what to do with this information. Same for the Duhigg and McKeown bullets. These should be woven into the Context paragraph as prose: "The design draws on Karpathy's autoresearch pattern (small autonomous loops that compound), Duhigg's habit loops (cue → routine → reward to eliminate decision fatigue), and McKeown's essentialism (subtract before adding)." One sentence replaces three bullets.

2. **Table abuse.** The Active Hooks table, the Body System Agents table, the WBR Callout Pipeline agents table, the Wiki Team agents table, the Routing Rules table, and the Decision Guide table — six tables total. The Active Hooks table and Routing Rules table lack "so what" interpretation. Brandon reads the hooks table and thinks "okay, five hooks exist" but doesn't learn which ones matter most or how much time they save. The Routing Rules table is a reference lookup that could be a sentence: "soul.md routes requests to the matching agent — career coaching goes to rw-trainer, WBR callouts flow through the three-agent pipeline, wiki work starts with wiki-editor."

3. **Duplication.** The cold start protocol appears twice — once in the Portability section ("a new AI reads portable-body/README.md → body.md → spine.md → soul.md") and again in the Decision Guide table ("Read portable-body/README.md → body.md → spine.md → soul.md"). The agent definition pattern (`.md` is portable, `.json` is platform-specific) is explained in the "Agent Definition Pattern" subsection and then restated in the Portability section and again in the Decision Guide's "Platform migration" row. Three explanations of the same concept.

4. **The "How the System Compounds" section is three paragraphs that each make one claim without evidence.** "The autoresearch loop runs structured experiments on organs" — yes, this was already explained in Layer 2. "The nervous system runs nine calibration loops" — this is a new claim introduced in the compounding section with no prior setup. "The wiki externalizes knowledge" — true but already implicit from the wiki team description. This section either needs to add new information (e.g., quantified compounding results) or be cut entirely because the compounding story is already told by the three layers.

5. **The Related section is six links.** Brandon doesn't know which ones to read. A one-sentence annotation per link ("Heart — the experiment methodology, read this if you want to understand how the loop decides what to test") would earn the section's place. Without annotations, it's a nav menu, not content.

| **Overall** | **7.4/10** | |

## Verdict

**REVISE**

The doc is structurally sound and answers Brandon's core questions about what the pieces are and how they connect. The three-layer model is the right organizing principle. The portability story is convincing. But the Economy score drags it below the bar — there's meaningful duplication, several tables that present data without interpretation, and a compounding section that restates what earlier sections already established.

## Required changes

1. **Cut the design philosophy bullets.** Replace the three-bullet list under Context with a single prose sentence embedding all three sources. The current bullets are noun-phrase padding with no verbs.

2. **Add "so what" sentences after the Active Hooks table and Routing Rules table.** After the hooks table: one sentence explaining which hooks run autonomously vs. which require Richard's judgment, and roughly how much daily time the morning routine saves. After the routing rules table: cut the table entirely and replace with a prose sentence — the table adds no information that the agent team descriptions didn't already provide.

3. **Eliminate the cold start duplication.** Keep the cold start protocol in the Portability section (that's where Brandon expects it). Remove the duplicate from the Decision Guide table — replace with "See Portability section above."

4. **Eliminate the agent definition pattern duplication.** The `.md` portable / `.json` platform-specific distinction is explained three times. Keep the full explanation in the "Agent Definition Pattern" subsection. In the Portability section, reference it: "The dual-file agent pattern (see Agent Definition Pattern above) means only the `.json` configs need recreation on a new platform." Remove the restatement from the Decision Guide.

5. **Rewrite or cut "How the System Compounds."** Option A: cut it entirely — the compounding story is implicit in the three layers. Option B: keep it but add quantified evidence (e.g., "After 700 experiments, average organ accuracy improved from X% to Y%" or "The wiki now holds N articles that replaced M thousand words of organ content"). Without evidence, the section is assertion, not argument.

6. **Annotate the Related section.** Add a one-sentence description after each link explaining what the reader will find and when they'd need it. Six bare links is a nav menu, not a useful section.

7. **Add a "Limitations and failure modes" section.** Brandon's key unanswered question: what breaks? What happens when an experiment corrupts an organ? What's the recovery path? What are the scaling limits — can this handle 30 agents? 50? Is there a point where the routing in soul.md becomes unwieldy? A 3-4 sentence paragraph addressing failure modes and known limits would significantly increase Brandon's confidence in the architecture's soundness.

## Suggestions (optional, non-blocking)

- The "Safety Guards" subsection sits awkwardly under Hooks. Consider renaming the Layer 2 header to "Hooks, Automation & Guards" or adding a one-sentence bridge: "Two hooks serve a different purpose — they're not automation triggers but structural safety guards that prevent accidental external communication."

- The nervous system's nine calibration loops are mentioned in "How the System Compounds" but never listed or explained anywhere in this doc. If they matter to the architecture story, they deserve a brief treatment. If they don't, cut the reference.

- Brandon would benefit from a simple count summary early in the doc: "The system comprises 11 organ files, 5 hooks, 13 custom agents organized into 3 teams, and 9 calibration loops." This gives him the scale picture before he dives into details.

- The `artifact-audience: agent-only` in the frontmatter contradicts the doc's stated purpose of serving both human observers and new AIs. If Brandon is a target reader, the audience field should reflect that.
