---
inclusion: manual
---

# Enhanced Navigation Protocol

*Adopted 2026-04-22 after blind A/B test (2-0 for treatment). Invoke on routing/orientation questions or when facing a new task type where the right organ isn't obvious.*

This protocol **builds on** the existing navigation in `soul.md`, `body.md`, and `spine.md`. It makes discovery faster, more reliable, and self-improving.

## Master Navigation Rule (when invoked)
1. Start every session exactly as `spine.md` instructs (body → spine → soul → amcc → current).
2. **Before any action or question to Richard**, run this internal check:
   - Do I have the latest `current.md` and `rw-tracker.md`?
   - Have I queried the DuckDB registry (`ps_analytics.docs.documents`) for any relevant `duck_id`?
   - Is there a more specific organ or protocol file I should load first?
3. If still uncertain after loading 2–3 organs → use the **Self-Discovery Query** below.

## Self-Discovery Query
When lost or facing a new task type, immediately run:
```sql
SELECT duck_id, title, canonical_path, stage, last_modified
FROM ps_analytics.docs.documents
WHERE duck_id ILIKE '%[task-keyword]%' OR title ILIKE '%[task-keyword]%'
ORDER BY last_modified DESC
LIMIT 10;
```
Then load the top 1–2 most relevant files before proceeding.

## Dynamic Organ Loading (optimization)
- Never load the entire body at once.
- Use this priority order for common tasks:
  - Projections / forecasting → eyes.md + brain.md + ps schema (+ performance-marketing-guide.md)
  - Test analysis / readouts → eyes.md + karpathy protocol + testing organ (+ performance-marketing-guide.md)
  - Business review / WBR prep → brain.md + richard-style-wbr.md + amazon-politics.md (+ performance-marketing-guide.md)
  - Excel / data drop → uploads/ processing protocol
  - High-stakes recommendation → always load `high-stakes-guardrails.md` for confidence scoring and human-review flagging

## Agent Self-Improvement Trigger
At the end of every major loop (EOD or after completing a complex task), ask yourself:
> "What friction did I experience today? Should we create or update a protocol/organ/hook to remove it?"
> If yes → propose the change in `~/shared/context/intake/` with clear reasoning. Do not implement without Richard's approval (except for minor steering wording).

This turns the agent into an active participant in improving its own harness — not a passive rule-follower.

## Why this file exists (empirical basis)
Blind A/B test on 2026-04-22 found that explicitly surfacing the Self-Discovery Query + Dynamic Organ Loading behavior at inference time changes attention allocation even though `docs.documents` and body.md's Task Routing table already exist. Making the query pattern explicit is the value — not the query itself.
