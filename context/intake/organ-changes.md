<!-- DOC-0180 | duck_id: intake-organ-changes -->
# Organ Change Log

## 2026-04-05 — amcc.md

**Summary:** Streak updated from 0 → 1 day. Testing Approach doc marked COMPLETED (v5 PUBLISH verdict 8.4/10). Hard thing rotated from "Ship Testing Approach doc for Kate" to "Send Testing Approach v5 to Brandon." Resistance taxonomy expanded from 3-col back to 4-col format. Escalation ladder example column removed. Avoidance Ratio section removed. Common Failures section removed. Integration section converted from prose to table format. Implementation intention updated for Monday 4/7 (apply 5 critic fixes, send to Brandon).

**Structural issues detected in edit:**
- Duplicate "Current Streak" tables with conflicting data (1 day vs 0 days)
- Duplicate "Growth Model" section headers
- Duplicate Hard Thing Queue table headers
- Stray fragment in streak table row
- Missing newline at EOF

**Cross-organ consistency:** No conflicts with other organs on substance. Hands.md and current.md should be verified to reflect the Testing Approach completion and new hard thing.

**Gated file:** No — amcc.md is not gated (heart.md and gut.md only).

## 2026-04-05 (second edit) — amcc.md

**Summary:** Major content expansion. Added: After Intervention protocol (push-through/override logging, streak reset rules), Hard Thing Queue section (single hard thing principle, current: "Send Testing Approach v5 to Brandon"), Resistance Taxonomy (6 types: visibility avoidance, blank page paralysis, competence anxiety, comfort zone gravity, delegation guilt, urgency addiction), Integration with Other Organs section, Avoidance Ratio tracking table (empty — ready for population), Growth Model with metrics/targets (30d/90d), Common Failures section (4 failure modes).

**Gated file:** No — amcc.md is not gated (heart.md and gut.md only). No karpathy authorization required.

**Cross-organ consistency issues detected:**

1. **amcc.md ↔ hands.md CONFLICT — Hard Thing status.** The new amcc.md Hard Thing Queue says "Send Testing Approach v5 to Brandon" and notes "Doc is done (PUBLISH verdict). 5 minor subtractive edits remain." But hands.md P0 still reads: "Testing Approach doc outline — Kate Apr 16. THE HARD THING. 16 workdays at zero. Status: NOT STARTED." The streak section (top of amcc.md, from the earlier edit) already reflects completion (streak = 1, completed 4/5), so hands.md is stale. **Action needed:** hands.md P0 should be updated to reflect the doc is complete and the hard thing is now "send to Brandon."

2. **amcc.md ↔ hands.md — Overdue count.** amcc.md references no specific overdue context, but hands.md shows 17 items overdue. No direct conflict, but the implementation intention ("IF Richard opens a new chat session on Monday 4/7, THEN apply 5 critic fixes and send to Brandon") should be cross-referenced with hands.md Monday signals which already list Refmarker audit, Lorena, Andrew, and Lena as Monday priorities. The hard thing should be sequenced first per aMCC protocol.

3. **amcc.md Integration section — references are directionally correct.** Brain (decides what's right), Eyes (deadline urgency), Hands (task list), Memory (stakeholder reframes), Device (catches device-level work), NS (measures after), Gut (prevents low-leverage), Heart (loop outputs), Trainer (retrospective standard) — all align with current organ purposes. No conflicts.

4. **Growth Model targets vs current state.** amcc.md sets "Current streak: 1" with 30d target of 5+ and 90d target of 10+. This is consistent with the streak section at the top of the file. No conflict.

## 2026-04-06 — device.md

**Change:** PS Analytics Database section rewritten from local DuckDB to MotherDuck Cloud. Old: local file at `~/shared/data/duckdb/ps-analytics.duckdb` with `query.py` CLI. New: cloud DB `md:ps_analytics` on MotherDuck (aws-us-east-1), MCP-only access, `ensure-schema.sql` guard, local .duckdb as cold backup only. Added 46 tables + 39 views inventory, key analytical views list, motherduck extension. Removed: Python `query.py` CLI references, VSS table details, old agent access patterns.

**Cross-organ inconsistencies detected:**
- `heart.md` (DuckDB Integration section, ~line 313): Still references `~/shared/data/duckdb/ps-analytics.duckdb` as the active DB path. Needs update to `md:ps_analytics` on MotherDuck. ⚠️ heart.md is karpathy-gated — route update through karpathy.
- `spine.md` (Key Paths table, ~line 82): Still references `~/shared/data/duckdb/ps-analytics.duckdb` with old CLI access pattern (`python3 ~/shared/tools/data/query.py`). Needs update to MotherDuck cloud path and MCP-only access pattern.

**Karpathy gate:** Not applicable (device.md is not gated). However, the required follow-up fix to heart.md IS gated — must route through karpathy.

## 2026-04-06 — device.md

**Section:** PS Analytics Database (DuckDB → MotherDuck Cloud)
**Change:** Updated to reflect schema migration from flat `main` schema to 8 named schemas (asana, signals, karpathy, ns, ops, wiki, ps, main). Updated table/view counts to 55 tables + 34 views. Added schema-qualified name requirement. Flagged ensure-schema.sql and FTS index as needing updates. Removed enumerated analytical views list (views still exist, just not listed). Added `USE ps_analytics` note.
**Cross-organ check:** No conflicts. Consistent with duckdb-schema.md steering file and MCP capability/integration specs.
**Karpathy gate:** N/A (device.md is not gated)
**Action items surfaced by edit:** (1) ensure-schema.sql needs update, (2) FTS index on signals.slack_messages needs rebuild
