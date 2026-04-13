---
title: "Wiki Articles Batch Review — Batch 2"
status: DRAFT
audience: amazon-internal
owner: Richard Williams
created: 2026-04-12
updated: 2026-04-12
---
<!-- DOC-0495 | duck_id: wiki-review-wiki-articles-batch-review -->

# Wiki Articles Batch Review — Batch 2

Reviewer: wiki-critic
Date: 2026-03-25
Articles reviewed: 5

---

## Summary

| Article | Overall | Verdict | Key Issue |
|---------|---------|---------|-----------|
| competitive-landscape | 6/10 | REVISE | Heavy duplication with published `competitive-intel-tracker.md` — must differentiate or merge |
| oci-playbook | 8/10 | PUBLISH | Strong. Minor accuracy note on AU OCI framing. |
| stakeholder-comms-guide | 8/10 | PUBLISH | Genuinely useful. Tight connection to Annual Review gap. |
| market-reference | 5/10 | REVISE | Massive duplication with `eyes.md`, `cross-market-playbook.md`, and per-market wikis. Needs a sharper reason to exist. |
| agent-architecture | 7/10 | PUBLISH | Good portability doc. Overlaps with published `body-system-architecture.md` but serves a different audience (agent-only vs personal). |

3 PUBLISH, 2 REVISE, 0 REJECT.

---

## 1. competitive-landscape.md

### Scores
| Dimension | Score | Notes |
|-----------|-------|-------|
| Usefulness | 7/10 | Decision guide is strong. A reader can act on the "new competitor appears" scenarios. |
| Clarity | 8/10 | Well-structured. US → EU5 → International flow is logical. "So what" blocks are excellent. |
| Accuracy | 8/10 | All numbers match `competitor-intel.md` and `eyes.md`. Walmart IS, CPC ranges, EU5 data all verified. |
| Dual-audience | 7/10 | AGENT_CONTEXT present and useful. Frontmatter complete. Prose is human-readable. |
| Economy | 4/10 | This is the problem. Published `competitive-intel-tracker.md` already covers the same data in the same structure. The staged article is better written, but it's 80% the same content. |
| **Overall** | **6/10** | |

### Verdict: REVISE

### Required Changes
The article needs to differentiate itself from the published `competitive-intel-tracker.md` or replace it. Right now they're two docs covering the same ground. Options:

1. **Merge and replace:** Kill `competitive-intel-tracker.md`, publish this as the canonical competitive reference. This is the better doc — it has the strategic framing, decision guide, and "so what" blocks that the tracker lacks.
2. **Differentiate:** Make the tracker a data-only weekly-updated table (no narrative), and make this article the strategic interpretation layer that references the tracker for raw data.

Either way, the current state — two docs with 80% overlap — violates subtraction before addition.

See `competitive-landscape-revisions.md` for specific edits.

### Suggestions (non-blocking)
- Add a "Last validated" date next to each competitor entry so readers know how fresh the data is per row, not just per doc.

---

## 2. oci-playbook.md

### Scores
| Dimension | Score | Notes |
|-----------|-------|-------|
| Usefulness | 9/10 | A teammate could replicate the rollout from this doc. The phased approach, exit criteria, and decision guide are all actionable. |
| Clarity | 9/10 | Excellent structure. Phase 1-4 progression is clear. Measurement framework is well-explained. |
| Accuracy | 7/10 | Numbers match sources. One issue: AU section says "Adobe OCI integration planned May 2026 via Suzane Huynh" — this is accurate per `current.md`, but the framing implies AU will get the same OCI as other markets. Adobe OCI is a different integration path. Also, the existing `oci-implementation-guide.md` covers tactical steps — this playbook is strategic. The distinction is valid but should be explicit. |
| Dual-audience | 8/10 | AGENT_CONTEXT is rich. Frontmatter complete. The doc works for both humans and agents. |
| Economy | 7/10 | Some overlap with `oci-implementation-guide.md` (published) and `oci-rollout-methodology.md` (published). But this playbook adds the strategic layer (why, not just how) and the measurement framework that neither of those has. The overlap is in the rollout status table and MCC structure — those could be cross-referenced instead of duplicated. |
| **Overall** | **8/10** | |

### Verdict: PUBLISH

### Suggestions (non-blocking)
- The MCC Structure section and Rollout Status table are duplicated from `eyes.md` and `oci-implementation-guide.md`. Consider replacing with a cross-reference: "See [OCI Implementation Guide] for MCC IDs and current rollout status." This saves ~40 lines and avoids staleness.
- Clarify the AU OCI note: "Adobe OCI integration (different from Google OCI) planned May 2026" — the word "different" matters because the playbook's methodology doesn't apply to Adobe OCI.

---

## 3. stakeholder-comms-guide.md

### Scores
| Dimension | Score | Notes |
|-----------|-------|-------|
| Usefulness | 9/10 | Directly addresses the #1 Annual Review gap. Templates are copy-paste ready. The Lena section alone justifies the doc — "she wants numbers, not explanations" is the kind of insight that prevents a bad meeting. |
| Clarity | 8/10 | Four-tier structure is clean. Per-stakeholder sections are scannable. Templates are well-formatted. |
| Accuracy | 8/10 | Annual Review quotes match `memory.md` and `current.md`. Brandon's "80% writing documents" quote is sourced. Lena's communication preferences match the relationship graph. One minor issue: the doc says "5+ weeks, WORSENING as of 3/25" for visibility avoidance — this is sourced from nervous-system.md but the specific week count should be verified against the latest Loop 3 data. |
| Dual-audience | 7/10 | AGENT_CONTEXT present. But this is a `personal` audience doc — the dual-audience dimension matters less here. The agent context is useful for rw-trainer to reference. |
| Economy | 7/10 | Some overlap with `memory.md` relationship graph (Lena, Brandon, Alexis entries). But the guide adds the "how to talk to them" layer and templates that memory.md doesn't have. The overlap is in the "what they care about" sections, which could be shorter with pointers to memory.md. |
| **Overall** | **8/10** | |

### Verdict: PUBLISH

### Suggestions (non-blocking)
- The Tier 1 (Peers) section is thin compared to the others. Andrew's entry is the most useful ("find moments to add strategic commentary during Andrew's EU updates"). Consider cutting the per-peer table to just Andrew and Adi (the two with actionable dynamics) and making the rest a one-liner: "Stacey, Yun, Dwayne, Peter: casual, direct, no special handling needed."
- Template 4 (Meeting Prep) duplicates what's already in `memory.md` → Meeting Prep Briefs. Consider referencing memory.md for the per-meeting briefs and keeping Template 4 as the generic framework only.

---

## 4. market-reference.md

### Scores
| Dimension | Score | Notes |
|-----------|-------|-------|
| Usefulness | 6/10 | The "tell me everything about [market]" use case is real. But `eyes.md` Market Health + Market Deep Dives already answers this. The W12 snapshot table adds value, but it'll be stale in a week. |
| Clarity | 7/10 | Market profiles are well-structured. The consistent field format (Launch, FY26 Feb, OCI, Key competitor, Key contact, Active initiatives, Narrative) is good. |
| Accuracy | 7/10 | W12 data matches callout sources. Feb data matches `eyes.md`. One issue: CA key contact says "Team-wide (no dedicated CA lead)" — this is accurate but unhelpful. Who actually handles CA day-to-day? If it's Richard or Stacey, say so. Also, the MX section says Carlos "transitioned to CPS" but the key contacts still list him — the note clarifies but the listing is confusing. |
| Dual-audience | 7/10 | AGENT_CONTEXT is good. Frontmatter complete. Callout agents are listed as consumers — they'd benefit from this. |
| Economy | 4/10 | This is the problem. The doc consolidates content from `eyes.md` (Market Health, Market Deep Dives, OCI Performance), `org-chart.md` (contacts), `current.md` (active projects), `competitive-landscape.md` (competitors), and per-market context files. It's a useful consolidation, but it creates a massive staleness surface — 10 markets × 7 fields = 70 data points that need monthly updates. The W12 snapshot will be wrong by next week. The existing `au-market-wiki.md` and `mx-market-wiki.md` already cover AU and MX in more depth. |
| **Overall** | **5/10** | |

### Verdict: REVISE

### Required Changes
The doc needs to decide what it is:

1. **If it's a snapshot:** Accept that it's point-in-time and add a prominent "Data as of W12 2026" header. Remove the W12 table (it'll be stale immediately) and replace with a pointer to the WW summary: "For current weekly data, see `callouts/ww/ww-summary-2026-w{XX}.md`." Keep the market profiles as structural references (contacts, OCI status, narrative) that change monthly, not weekly.

2. **If it's a living reference:** The update-trigger says "Monthly after MBR data refresh" but the W12 table is weekly data. Pick one cadence. Monthly is more sustainable.

Either way: cut the Cross-Market Patterns section — it duplicates the published `cross-market-playbook.md` and `eyes.md` Market Deep Dives. Cut the AU and MX profiles to stubs that point to the published `au-market-wiki.md` and `mx-market-wiki.md` — those are more detailed and already maintained.

See `market-reference-revisions.md` for specific edits.

### Suggestions (non-blocking)
- The Decision Guide is the best part of this doc. Keep it. It's the only place that answers "what do I do when a market misses OP2 for 2+ months?" — that's genuinely useful.

---

## 5. agent-architecture.md

### Scores
| Dimension | Score | Notes |
|-----------|-------|-------|
| Usefulness | 8/10 | A new AI could bootstrap from this. The three-layer model, organ map, and routing rules are all actionable. The cold start protocol is the key use case. |
| Clarity | 8/10 | ASCII diagrams are helpful. The layer model (Body → Hooks → Agents) is intuitive. Agent team tables are scannable. |
| Accuracy | 7/10 | Organ map matches `body.md`. Hook list matches `device.md`. Agent routing matches `soul.md`. One issue: the doc says "9 completed runs as of 3/25/2026. 8 experiments completed with 100% keep rate. 4 compression experiments adopted, saving 2,827 words (29% across 4 organs)." — the 9 runs / 8 experiments distinction is confusing. If 9 runs happened but only 8 experiments completed, what happened on run 9? Clarify. Also, the wiki team pipeline diagram shows `wiki-editor (publish/revise/kill decision)` but per the wiki-critic agent definition, the critic doesn't publish — the librarian does. The diagram should show critic → librarian → editor (final approval). |
| Dual-audience | 9/10 | This is the best dual-audience doc in the batch. AGENT_CONTEXT is comprehensive. The doc explicitly addresses both "a new AI on a different platform" and "a human observer." The portability section is excellent. |
| Economy | 5/10 | Significant overlap with published `body-system-architecture.md`. That doc covers the organ map, design principles, autoresearch loop, and habit loop. This doc adds the hook system, agent swarm, routing rules, and directory structure — which are genuinely new content. But the Layer 1 section (~40% of the doc) is largely redundant with the published article. |
| **Overall** | **7/10** | |

### Verdict: PUBLISH

The overlap with `body-system-architecture.md` is real, but the audience is different (agent-only vs personal) and this doc adds the hook and agent layers that the published article doesn't cover. The right long-term move is to merge them, but for now, publishing both is acceptable because they serve different consumers.

### Suggestions (non-blocking)
- Compress Layer 1 (Body System) to a summary + pointer to `body-system-architecture.md`. The organ map table, word budget system, and data flow diagram are all in the published article. Replace with: "For the full body system architecture, see [Body System Architecture]. Key facts: 11 organs, 23,000-word budget, self-maintaining via autoresearch loop." This would cut ~800 words and eliminate the staleness risk of maintaining the same content in two places.
- Fix the wiki team pipeline diagram — the flow should be: editor → researcher → writer → critic → librarian (publishes) → editor (final approval). Currently shows editor appearing twice in the wrong positions.
- Clarify the "9 runs / 8 experiments" discrepancy.

---

## Cross-Batch Observations

1. **Duplication is the batch's biggest weakness.** Three of five articles have significant overlap with existing published artifacts. The wiki is 34 articles deep now — every new article needs to justify why it can't be a section in an existing doc.

2. **Decision Guides are the batch's biggest strength.** Every article has one, and they're all genuinely useful. The "Situation → Action → Why" format works. This should be a standard section in every wiki article.

3. **The "So what" blocks are excellent.** The competitive-landscape and oci-playbook articles both use "So what:" after data sections. This is the right pattern — data without interpretation is noise.

4. **Staleness risk varies dramatically.** The stakeholder-comms-guide and agent-architecture are structurally stable (quarterly updates). The market-reference has 70+ data points that change weekly. The oci-playbook is in between (changes when markets go live). Articles should be designed for their update cadence — don't put weekly data in a monthly doc.

5. **The PUBLISH articles are genuinely good.** The oci-playbook is the best article in the batch — a teammate could actually replicate the rollout from it. The stakeholder-comms-guide directly addresses the #1 growth area. The agent-architecture serves the portability use case well. These earn their place.
