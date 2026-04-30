---
inclusion: manual
keywords: lens, todd, two-up, VP review, narrative, Amazon-wide, up-the-chain
---

# Lens — Todd Heimes (Two-Up, L10 VP)

*Manual-inclusion steering file. Load with `#lens-todd` when Richard's work will surface to Todd or when preparing material that Kate will use with Todd. Todd is two levels above Richard, which means he reads for narrative arc and org-level implication, not execution detail.*

## Persona anchor

Todd Heimes, L10 VP. Kate's boss. Richard does not interact with Todd directly — Todd reads what Kate filters up. This makes the lens prescriptive rather than observational: Richard isn't reading Todd-written material regularly, so the persona anchor is **inferred from L10 VP conventions + Kate's framing** rather than direct memory.

What VPs at Amazon read for (from amazon-politics.md and general Amazon conventions):
- **Narrative arc** — "where are we, where are we going, what's the story to the next level up." Todd's job is to tell a story about outbound marketing to his VP and to the business unit. He reads everything asking "does this fit the story, or break it."
- **Org-level implication** — what does this mean for the team, the budget, the cross-team relationships. Not "what does this mean for the AU campaign."
- **Risk concentration** — where are the big bets that could move the metric or blow up in a QBR. Todd is exposed in forums Richard is not; his tolerance for unsurfaced risk is lower than Brandon's or Kate's.

What he doesn't read for: execution detail, tactical justification, tool choices, specific campaign mechanics. Those are delegated down; Todd assumes they're handled unless they're the point of the doc.

## The rubric — three questions

### 1. What would he push back on?

Todd pushes back on: **things that don't fit the narrative he's telling upward**. If the outbound marketing story this quarter is "we're scaling WW testing methodology to 10 markets," a doc that treats testing as an experimental side-project will clash with the story. Same content, different framing — the framing determines whether Todd engages or dismisses.

He also pushes back on: single-market arguments that don't scale implications. If a doc argues for AU investment, Todd wants to know what AU teaches about the other 9 markets, or he won't care — AU alone is below his altitude.

### 2. What would he ignore?

Everything that sits strictly at market-or-campaign level. Spend figures below $200K. Tactical mechanics. Tool choices. Specific creative. If a draft is 80% tactical detail with 20% narrative framing, Todd sees 20% of the doc. The strategic framing needs to carry the first and last paragraphs.

He also ignores hedging. "We're investigating whether AU CPA could be improved through consolidation" → he reads "investigating" and skips. The strategic version is "AU is our highest-cost market, and consolidation is the mechanism we're using to close the gap. We expect 30% improvement by EOQ."

### 3. What would he skip straight to?

The one-sentence summary of what this means for the org. If the doc doesn't contain a sentence that reads "this means [consequence] for [who] by [when]," Todd doesn't know what to do with it.

Secondary: any number that resets the baseline. If the doc says "we improved CPA by 30%" — Todd scans for the resulting total or the cross-market implication. Improvements without totals don't tell the story.

## What this lens *misses*

Todd's lens is narrative-first — it won't catch **execution risk** (Brandon's territory) or **strategic framing within the team** (Kate's territory). It also can't catch things Todd would actually notice that aren't captured in this file — because Richard doesn't interact with him directly, this lens is an approximation. Confidence in the calibration is lower than for Brandon/Kate.

**Important:** if Richard is writing material for Todd (not Kate-filtered-to-Todd), the draft should go through `lens-kate.md` first. Kate is the canonical filter to Todd's altitude; she knows what lands with him. Use this lens for pre-drafts and sanity-checks; use `lens-kate.md` for the final pass.

## Worked example

**Draft (before lens read):** "Our W16 AU testing showed 30% CPA improvement on consolidated keywords vs broad-match. This validates our consolidation thesis and we plan to roll out to MX and CA in Q3."

**Todd's push-back:** "Validates our consolidation thesis" — whose thesis, for what business reason. AU alone is noise at his altitude; what's the WW implication. "Roll out to MX and CA in Q3" — what's the spend envelope, what's the revenue implication, why those two markets and not others.

**Todd ignores:** "W16 AU testing," "broad-match," any tactical detail. He'll glance at the 30% number then scan for what it implies.

**Todd skips to:** the one-sentence implication for the org.

**Revised:** "AU keyword consolidation closed 60% of our CPA gap to benchmark markets, suggesting the same approach on MX and CA could recover $400K in annualized spend efficiency. We're proposing Q3 rollout to MX/CA based on the AU result, with a parallel MBR framing that positions consolidation as our primary efficiency lever for H2."

That version lands because the first sentence is the implication (% recovery + dollar impact), the second is the decision (Q3 rollout, 2 markets), and the third is the story-level framing (consolidation as H2 efficiency lever). Todd reads all three in 30 seconds.

## Invocation

Load `#lens-todd` when preparing:
- Material that will be read aloud or summarized at Todd's altitude (QBR talking points, VP reviews)
- Artifacts Kate is using to build the upward story (MBR sections that land in Kate's deck)
- AEO POV or any artifact positioned as Amazon-wide thought leadership
- One-pagers explicitly targeted at L10+ review

For most of Richard's weekly work, this lens is overkill — the altitude is wrong. Use `lens-brandon.md` for day-to-day, `lens-kate.md` for strategic artifacts, and reserve this file for material that genuinely needs the two-up filter.

## Note on Todd calibration

This file's calibration will drift as Richard accumulates indirect signal about Todd (forwarded emails, overheard comments from Kate, MBR read-aloud patterns). The lens should be updated quarterly from that signal, not from guesses. If the content starts feeling stale or prescriptive rather than descriptive, flag to karpathy for a refresh.
