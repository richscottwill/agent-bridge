---
inclusion: manual
---

# Enhanced Agent Navigation Protocol (v2 — April 2026)

This protocol **builds on** the existing navigation in `soul.md`, `body.md`, and `spine.md`. It makes discovery faster, more reliable, and self-improving.

## Master Navigation Rule (always active)
1. Start every session exactly as `spine.md` instructs (body → spine → soul → amcc → current).
2. **Before any action or question to Richard**, run this internal check:
   - Do I have the latest `current.md` and `rw-tracker.md`?
   - Have I queried the DuckDB registry (`ps_analytics.docs.documents`) for any relevant `duck_id`?
   - Is there a more specific organ or protocol file I should load first?
3. If still uncertain after loading 2–3 organs → use the **Self-Discovery Query** below.

## Self-Discovery Query (new capability)
When lost or facing a new task type, immediately run:
```sql
SELECT duck_id, title, canonical_path, stage, last_updated
FROM ps_analytics.docs.documents
WHERE duck_id ILIKE '%[task-keyword]%' OR title ILIKE '%[task-keyword]%'
ORDER BY last_updated DESC
LIMIT 10;
```
Then load the top 1–2 most relevant files before proceeding.

## Dynamic Organ Loading (optimization)
- Never load the entire body at once.
- Use this priority order for common tasks:
  - Projections / forecasting → eyes.md + brain.md + ps schema
  - Test analysis / readouts → eyes.md + karpathy protocol + testing organ
  - Business review / WBR prep → brain.md + richard-style-wbr.md + amazon-politics.md
  - Excel / data drop → uploads/ processing protocol (see new file below)
  - High-stakes recommendation → always load nervous-system.md for confidence scoring

## Agent Self-Improvement Trigger
At the end of every major loop (EOD or after completing a complex task), ask yourself:
> "What friction did I experience today? Should we create or update a protocol/organ/hook to remove it?"
> If yes → propose the change in `context/intake/` with clear reasoning. Do not implement without Richard's approval (except for minor steering wording).

This protocol makes navigation faster and turns the agent into an active participant in improving its own harness (Steinberger principle).
