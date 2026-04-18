# Eval B — Subjective Reader Evaluation: Workstream 5: Algorithmic Ads (v5)

**Evaluator persona**: Kate, reviewing the workstream detail behind the Testing Approach doc. 10-minute read.
**Date**: 2026-04-05
**Prior context**: Blind eval. No visibility into Eval A or prior version reviews.

---

## Scores

| Dimension | Score | Assessment |
|-----------|-------|------------|
| First Paragraph Test | 8/10 | See below |
| Shareability | 8/10 | See below |
| Actionability | 7/10 | See below |
| Signal-to-Noise | 8/10 | See below |
| Voice | 8/10 | See below |
| **Composite** | **7.8/10** | |

---

## First Paragraph Test — 8/10

The opening paragraph does three things well: it names the subject (algorithmic ad formats), states the purpose (evidence base for the 2026 AI Max test), and tells the reader what they will know after reading (DG results, AI Max test design, Modern Search dependencies). That is a clean contract with the reader.

What keeps it from a 9: the phrase "tested and scaled algorithmic ad formats — Demand Gen and the upcoming AI Max — to extend reach beyond traditional keyword campaigns" is doing a lot of work in one clause. A reader unfamiliar with the distinction between DG and AI Max has to hold that parenthetical in memory while also parsing the purpose statement. The sentence would land harder if it separated the backward-looking proof (DG) from the forward-looking bet (AI Max) into two beats. As written, it is functional but slightly compressed.

## Shareability — 8/10

If Kate forwarded this to a peer on another marketing team or a finance partner asking "what is the Paid Search team doing with algorithmic formats?", the doc would hold up. The question-based headers ("What opportunity do algorithmic ads address?", "How is the team managing AI Max risk?") mean a reader can scan the structure and find the section relevant to their question without reading linearly. The numbers are embedded in narrative rather than dumped in tables — the body tells the story, the appendix provides the receipts.

The cross-functional partners section is the weakest for shareability. It reads as a roster rather than a narrative — five sentences, each following the same "[Name/Team] is doing [thing]" pattern. A reader outside the team does not need to know every name; they need to understand the dependency structure. "Creative is developing video and image assets. Google is advising on AI Max planning. Hydra coordination prevents internal auction overlap." — that is the shareable version. The names belong in a RACI or contact list, not in the narrative.

## Actionability — 7/10

This is where the doc falls short of the 8 bar. The Demand Gen sections are retrospective — they prove the channel works, and they do it convincingly. The AI Max sections describe a test that is planned but not yet designed in detail. The reader learns that guardrails are needed for cannibalization and budget inflation, and that coordination with Hydra is required. But the doc does not answer the questions a reader would ask next:

- What are the specific guardrail thresholds? "Detect both within the first two weeks" is a timeline, not a mechanism. What CPC increase triggers a pause? What registration-to-click ratio signals low intent?
- What does the phased rollout look like? US-first is stated, but how many campaigns? What percentage of budget? What is the decision gate between phase 1 and phase 2?
- What happens if the Hydra coordination fails? The dependency is named but the contingency is not.

The doc says the team "is developing the AI Max test design" — which means the detail may not exist yet. If so, the doc should say that explicitly: "Test design is in progress; guardrail thresholds and rollout phases will be documented in [location] by [date]." As written, the reader is left wondering whether the detail exists elsewhere or has not been created.

The DG Video paragraph is similarly thin on forward-looking action. "Early testing shows video CPCs in line with image asset CPCs at $0.30" — and then what? What is the decision point for scaling video? What volume targets would justify increased creative investment?

## Signal-to-Noise — 8/10

The doc is tight. No bullet lists in the body. Tables are confined to the appendix and each has an interpretation paragraph — the "so what" is present. The narrative carries the argument without relying on formatting as a crutch. Removing all bold and italic would not make the doc unreadable.

Two minor noise issues. First, the BSE paragraph in the DG section introduces a sub-topic (Business Essentials launch) that is interesting but slightly tangential to the main argument. The main thread is "DG works, here is the proof, now we are extending to AI Max." BSE is a proof point, but the paragraph gives it nearly equal weight to Prime Day — which was a much more significant validation event. One sentence on BSE would suffice; the current paragraph is four sentences including the video extension.

Second, Appendix C largely restates what the body already covers. The body says "clear baselines, phased rollout, incrementality benchmarks" and the appendix says "clear baselines before launch, phased US-first rollout, incrementality benchmarks." That is duplication, not elaboration. Either the appendix should add detail the body does not contain (specific metrics, timelines, campaign IDs) or it should be cut.

## Voice — 8/10

The prose reads like a person explaining a strategy to a colleague, not like a slide deck converted to sentences. Sentence length varies naturally — short declarative statements ("This is not a volume play; it is an efficiency play") alternate with longer explanatory sentences. The question-based headers give the doc a conversational structure without being informal.

The voice is consistent throughout with one exception: the cross-functional partners section drops into a flat roster tone that breaks the narrative flow. Every other section answers a question; this section just lists facts. Reframing it as "Who does this depend on and why?" would maintain the voice.

The doc avoids jargon inflation — it explains what AI Max does ("showing text ads to users whose queries signal business intent without matching our exact keywords") rather than assuming the reader knows. The DG-vs-AI-Max distinction is drawn clearly: DG extends reach through visual placements in mid-funnel surfaces, AI Max extends reach within search itself. That is a clean, memorable contrast.

---

## Composite: 7.8/10

## Does it ship?

**No.** The composite is 7.8 and Actionability scores 7 — below the 7 floor for any single dimension under the PUBLISH threshold.

The doc is close. The retrospective half (DG proof, Prime Day, BSE) is strong — well-evidenced, well-narrated, efficient. The forward-looking half (AI Max) describes the shape of the test without enough specificity to be actionable. The fix is either (a) adding the guardrail thresholds and rollout parameters if they exist, or (b) explicitly stating they are in development with a pointer to where they will land and when.

## Required changes to reach 8

1. **AI Max guardrails need specificity or an explicit "TBD" with a pointer.** Replace "The guardrail design needs to detect both within the first two weeks of the test" with either the actual thresholds (CPC increase %, registration-to-click ratio) or a statement like "Guardrail thresholds are being defined as part of the test design; they will be documented in [location] by [date]." The reader needs to know whether the detail exists or is forthcoming.

2. **Trim Appendix C or add real detail.** Currently it restates the body. Either cut it entirely (the body covers the same ground) or populate it with the specific test parameters that would make the AI Max section actionable — campaign scope, budget allocation, phase gates, success/failure criteria.

3. **Compress the cross-functional partners section.** Rewrite as 2-3 sentences focused on dependency structure rather than a name roster. Move names to a footnote or AGENT_CONTEXT metadata if agent indexing of contacts is needed.

## Non-blocking suggestions

- The BSE paragraph could be tightened to two sentences without losing the proof point. The video extension detail ("short video creative and increased image variations developed in collaboration with the Creative team") is operational detail that belongs in a campaign brief, not a strategy doc.
- The first paragraph would land harder if it separated the DG proof story from the AI Max bet into two distinct beats rather than compressing both into one clause.
