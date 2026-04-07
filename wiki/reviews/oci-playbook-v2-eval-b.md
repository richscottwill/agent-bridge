<!-- DOC-0489 | duck_id: wiki-review-oci-playbook-v2-eval-b -->
# Blind Eval B: OCI Rollout Playbook v2

**Evaluator**: Eval B (subjective reader simulation — Brandon Munday L7, Kate Rundell L8 Director)
**Date**: 2026-04-04
**Article**: `shared/context/wiki/staging/oci-rollout-playbook-v2.md`
**Note**: This evaluation was conducted blind. No prior reviews or Eval A scores were seen.

---

## Dimension Scores

### 1. FIRST PARAGRAPH TEST — 8/10
*Would Brandon read past it?*

The opening paragraph does three things right: it leads with a result ($16.7MM OPS, 35K registrations), it names the markets where the result was proven, and it states the doc's purpose in one sentence ("Use it to replicate the rollout in any new market"). Brandon sees leverage immediately — this is a replication manual, not a status update. The closing sentence ("A teammate should be able to follow this doc end-to-end without asking the author") is a strong contract with the reader.

What keeps it from a 9: the title "From E2E to 100% in Any Market" is jargon-forward. Brandon knows what E2E means, but if he's forwarding this to a new market owner in JP who joined last month, the title doesn't self-explain. Minor friction, but friction.

### 2. SHAREABILITY — 7/10
*Could Brandon forward to Kate with minimal editing?*

Brandon could forward this, but he'd hesitate. The doc is ~2,200 words. Kate wants one page. This is three pages. The strategic framing is there — the Context section explains why OCI matters and how it connects to competitive strategy — but it's buried under operational detail that Kate doesn't need.

If Brandon forwards this to Kate, she reads the first paragraph (good), the Context section (good), skims the four phases (too much detail for her), lands on the DE table (useful but she'd want the "so what" faster), and probably stops before "Known Issues." The cross-market patterns section is exactly what Kate wants — strategic insight from execution — but it's on page two. Kate might not get there.

Brandon would need to write a two-sentence email: "This is the playbook that produced $16.7MM. Skip to 'What the rollout taught us' for the strategic patterns." That's one sentence too many. A truly shareable doc would have the strategic layer on top and the operational layer underneath.

### 3. ACTIONABILITY — 9/10
*Can someone DO something after reading?*

This is the doc's strongest dimension. A market owner in CA or MX could pick this up and execute. The phases are sequenced logically. Each phase has a clear goal, a duration, a success criterion, and a decision rule for proceeding. The decision table at the end covers the five most common "what do I do when..." scenarios. The cross-reference to the OCI Execution Guide for step-by-step Google Ads setup is the right call — keeps this doc at the strategy/methodology level without losing the reader who needs tactical detail.

The Known Issues section is genuinely useful — it names a specific bug (duplicate `hvocijid` parameters), explains the potential impact (conversion tracking loss), and gives a workaround (monitor match rates, escalate below 90%). A market owner hitting this issue would know what to do.

One gap: the doc doesn't say who to contact when something goes wrong. "Escalate to Google" — through whom? The Google rep? A shared channel? Brandon would know, but the stated goal is that a teammate can follow this without asking the author.

### 4. SIGNAL-TO-NOISE — 7/10
*Would a busy L8 with 15 minutes get the value?*

Kate has 15 minutes. She'd get value, but she'd have to work for it. The signal is strong — the three cross-market patterns are genuine strategic insight, the DE data is compelling proof, and the competitive framing (OCI enables efficiency-based response to Walmart/bruneau.fr) is exactly the kind of structural argument Kate thinks in.

The noise: Phase 1 through Phase 4 descriptions are operational. Kate doesn't need to know that Phase 1 takes two to four weeks or that conversion counts should match within 5% tolerance. That's for the market owner. The doc tries to serve two audiences (strategic reader and operational executor) in a single linear flow, and the operational sections dilute the signal for the strategic reader.

The DE table is the right data to include, but it takes up visual space. The interpretation paragraph after it is good — it explains what the numbers mean. But Kate would absorb "NB CPA dropped 74-75% in a clean test-versus-control" faster as a sentence in prose than as a table she has to parse.

The JP structural headwind paragraph is a good inclusion — it shows the author isn't cherry-picking favorable markets — but it's a single paragraph orphaned at the end of the cross-market section. It reads like an afterthought rather than a deliberate acknowledgment of where OCI doesn't solve everything.

### 5. VOICE — 8/10
*Does this sound like Richard?*

This reads like someone who has run the rollout, learned from the mistakes, and is writing for the next person who has to do it. The voice is confident without being promotional. Sentences like "The default posture is patience — OCI's learning period means early volatility is expected. Premature intervention is the most common mistake" sound like hard-won operational wisdom, not textbook advice.

The competitive framing is sophisticated — "OCI makes the NB side efficient enough to absorb Brand CPA pressure" is a structural argument, not a feature pitch. The doc consistently treats OCI as a tool within a strategy rather than the strategy itself. That's a mature perspective.

The "What the rollout taught us" section is the strongest voice section. Pattern recognition across ten markets, stated plainly, with specific examples. "Not every market enters OCI from a position of growth" — that's an honest sentence that most people would leave out of a playbook.

Minor voice issue: the frontmatter is heavy. Seventeen metadata fields before the first sentence. Richard writes for humans first. The YAML block is necessary for agent consumption but it creates a wall before the prose starts.

---

## Persona Summaries

### Brandon would...

...read the whole thing. He'd bookmark it. He'd send it to the CA and MX market owners with "follow this." He'd appreciate that the decision table at the end saves him from fielding Slack questions about edge cases. He'd flag the Known Issues section as something to track in his next sync.

He would not forward it to Kate as-is. He'd extract the first paragraph, the three cross-market patterns, and the DE data into a half-page summary and send that instead. The doc is too long and too operational for Kate's inbox. Brandon values leverage — this doc gives him leverage over his market owners, but it doesn't give him leverage upward without editing.

Brandon's one complaint: "Where's the timeline for the remaining three markets? You tell me seven of ten are done but not when the other three land. I need that for my planning."

### Kate would...

...read the first two paragraphs and the cross-market patterns section. She'd pull the $16.7MM figure and the "50% NB CPA improvement" for her next leadership review. She'd appreciate the structural argument about OCI enabling efficiency-based competitive response — that's the kind of framing she can use with Todd.

She would not read Phases 1 through 4. She would not read the DE table row by row. She would skim Known Issues and flag it mentally as a risk item. She'd want to know: "What's the ask? More budget? More headcount? Or is this just informational?" The doc doesn't have a clear ask, which means Kate files it as "good work, noted" rather than "I need to act on this."

Kate's one complaint: "This is a playbook for your team. Why am I reading it? Send me the one-pager with the results and the three things you learned. I'll read that in three minutes instead of fifteen."

---

## Composite Score

| Dimension | Score |
|-----------|-------|
| First Paragraph Test | 8/10 |
| Shareability | 7/10 |
| Actionability | 9/10 |
| Signal-to-Noise | 7/10 |
| Voice | 8/10 |
| **Composite** | **7.8/10** |

### Assessment

This is a strong operational playbook that slightly overreaches its audience. It tries to be both the strategic case for OCI and the execution manual for market owners, and the two goals create tension. The operational content is excellent — a 9 on actionability is rare. But the strategic reader (Kate) has to wade through operational detail to find the insights she cares about, and the operational reader (new market owner) has to wade through strategic framing to get to the steps.

The doc would score 8+ if it committed to one audience. As a pure playbook for market owners, cut the competitive strategy framing and the cross-market patterns into a separate "OCI Strategy Brief" and this becomes a tight 9. As a strategic brief for Kate, cut Phases 1-4 down to a single paragraph ("four-phase rollout validated across seven markets — see playbook for details") and expand the cross-market patterns.

As written, it's a 7.8 — a very good doc that doesn't quite clear the 8 bar because it's serving two masters. Brandon would use it daily. Kate would use 30% of it once.
