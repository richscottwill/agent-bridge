<!-- DOC-0191 | duck_id: intake-wiki-session-handoff -->
# Wiki Session Handoff — April 4, 2026

## What Was Done Today

This was a massive wiki session covering article creation, expansion, consolidation, quality review, Asana sync, and infrastructure upgrades. Here's the state for the next session.

## Current State

### Asana (ABPS AI Content Project)
- 39 active wiki tasks, all with full article content in html_notes
- 37 archived (completed old pipeline stubs)
- Pipeline_RW field set on all tasks: 3 Rewrite, 36 Review
- Audience_RW field set on all tasks: 20 Leadership, 15 Team, 4 Personal
- All tasks currently in Review section (Asana sections) — Pipeline_RW field is the canonical stage tracker now

### Articles Needing Rewrite (Pipeline_RW = Rewrite)
These scored <8 on BOTH blind evaluators and need structural rewriting:

1. **OCI Execution Guide** — Eval A: 6.8, Eval B: 6.6. Problem: 60% bullet/table content, formatting-as-content, duplicates Playbook. Fix: rewrite as narrative prose, remove duplicated content, add purpose statement.
2. **AU Market Wiki** — Eval A: 7.0, Eval B: 5.6. Problem: opens with background not results, one-sentence sections, not shareable to Kate. Fix: lead with strategic situation, fold thin sections, add next steps with owners/dates.
3. **Enhanced Match / LiveRamp** — Eval A: 7.2, Eval B: 8.0 (disagreement). Problem per Eval A: ABMA section tangential, Current State overlaps What's Happening. But Eval B says it's the best doc because it opens with what Brandon asked for. Fix: tighten structure per Eval A while preserving the Brandon-response framing that Eval B praised.

### Articles in Review (Pipeline_RW = Review, 36 tasks)
These need re-evaluation with the updated rubric (Amazon narrative standard). The blind test only covered 5 articles — the other 31 haven't been scored with the new rubric yet. Priority order for review:
1. Testing Approach Kate (THE Level 1 artifact — must be accurate for Brandon)
2. OCI Rollout Playbook (Eval A: 7.6, Eval B: 7.8 — close to passing, needs Economy fixes)
3. ie%CCP Framework (Eval A: 8.0, Eval B: 5.2 — strong disagreement. Well-written but tutorial format. Needs decision-first restructure.)
4. All remaining articles

### Key Insight from Blind Test 2
The two evaluators genuinely disagreed (max delta 2.8). The ie%CCP doc scores 8.0 on the rubric (best prose) but 5.2 subjectively (Brandon wouldn't read past the first section — it's a tutorial, not a decision doc). The Enhanced Match doc scores 7.2 on rubric but 8.0 subjectively (exactly what Brandon asked for). **Lesson: well-written prose that doesn't serve the reader's decision is worse than imperfect prose that does.**

### Updated Standards
- Wiki-writer voice rules now include "Amazon narrative standard" (prose over bullets, 18-20 word sentences, purpose first, data embedded, cut duplicative)
- Wiki-critic Economy rubric now includes bullet list abuse (>30% = flag), table abuse (no "so what" = flag), formatting-as-content (unreadable without formatting = flag)
- richard-style-amazon.md now includes full "Amazon Narrative Standard" section derived from 30 internal Amazon writing templates and Doc Ninja reviews
- Audience_RW maps to writing register: Leadership = strict Amazon narrative, Team = actionable execution, Personal = lighter review

### Infrastructure
- Pipeline_RW field replaces section-based pipeline tracking
- All field names now end with _RW
- asana-command-center.md updated with all new GIDs
- Wiki agent definitions updated (critic, writer, librarian, concierge, editor)
- SITEMAP.md regenerated
- wiki-structure.md navigation hierarchy updated
- wiki-index.md at 41 articles (40 indexed + competitive-landscape added)
- 7 superseded files archived with ARCHIVED headers

## What the Next Session Should Do

1. **Rewrite the 3 Rewrite articles** using the wiki-writer with style guides loaded
2. **Re-score all 36 Review articles** with the updated rubric — batch by Audience (Leadership first, then Team, then Personal)
3. **Move passing articles to Published** (Pipeline_RW = Published)
4. **Move failing articles to Rewrite** (Pipeline_RW = Rewrite) with specific revision notes
5. **Update OCI status** across 7 articles that show stale FR/IT/ES/JP data (audit flagged this)
6. **Sync updated content to Asana** after rewrites (update html_notes on changed tasks)

## File Locations
- Blind test results: shared/context/wiki/reviews/blind-test-2-evaluator-a.md, blind-test-2-evaluator-b.md
- Critic audit: shared/context/wiki/audits/audit-2026-04-04.md
- Health check: shared/context/wiki/health/health-2026-04-04.md
- Sync log: shared/tools/wiki-asana-sync/sync-log-2026-04-04.md
- Wiki roadmap: shared/context/wiki/roadmap.md
- Command center: shared/context/active/asana-command-center.md
- Amazon writing templates: shared/context/wiki/AMZ/ (30 .docx files)
