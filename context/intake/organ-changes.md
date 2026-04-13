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

## 2026-04-12 — device.md

**Section:** Installed Apps → AM Hooks + EOD Hooks
**Change:** Hook architecture consolidated from 5 hooks (AM-1/AM-2/AM-3 + EOD-1/EOD-2) to 3 hooks (AM-Backend/AM-Frontend + EOD). AM-Backend (`am-auto`) replaces AM-1/AM-2/AM-3 with parallel 6-subagent ingestion → sequential processing → SharePoint sync (~12 min). AM-Frontend (`am-triage`) is interactive: briefs, calendar blocks, triage, command center (~10 min). EOD (`eod`) unifies EOD-1 + EOD-2 into single backend+frontend hook (~20 min). New protocol files referenced: `am-backend-parallel.md`, `am-frontend.md`, `eod-backend.md`, `eod-frontend.md`.

**Karpathy gate:** N/A (device.md is not gated).

**Cross-organ inconsistencies detected (stale references to old hook names):**

1. **tech.md** (steering) — Still references "EOD-1: Meeting Sync" and "EOD-2: System Refresh" as separate hooks. Needs update to unified EOD hook.
2. **kiro-limitations.md** (steering) — Multiple references to AM-1 → AM-2 → AM-3 chaining pattern and AM-1/AM-2 output sharing workaround. Needs rewrite to reflect AM-Backend/AM-Frontend architecture.
3. **slack-deep-context.md** (steering) — fileMatchPattern references `hooks/eod-2*`. Needs update to match new hook naming (`hooks/eod*`). Also references `eod-2-system-refresh.kiro.hook` by name.
4. **duckdb-schema.md** (steering) — References "EOD-2 (delta sync)" in DuckDB-First Principle section. Needs update to "EOD" or "EOD-Backend".
5. **wiki-editor.md** (agent) — References "AM-2" as the triage invoker for ABPS AI tasks, AM-2 date window checks, and AM-2 presentation format. Needs update to "AM-Frontend".
6. **wiki-writer.md** (agent) — References "AM-2 detects the approval" for Stage 5 expansion trigger. Needs update to "AM-Frontend".
7. **wiki-researcher.md** (agent) — References "AM-2 hook" as invocation trigger for ABPS AI tasks. Needs update to "AM-Frontend".
8. **steering-integrity.md** (steering) — References "EOD-2 housekeeping" for batch commits. Needs update to "EOD".
9. **device.md itself** — Device Health table at bottom still references old groupings: "AM Hooks (AM-1, AM-2, AM-3)" and "EOD Hooks (EOD-1, EOD-2)". Needs update to match new hook names.
10. **kiro-setup-optimization spec** (completed spec) — Multiple references to old hook names in requirements.md, design.md, tasks.md. Lower priority since spec is completed, but worth noting for historical accuracy.

**Action items:**
- Update tech.md, kiro-limitations.md, slack-deep-context.md, duckdb-schema.md, steering-integrity.md (steering files — no gate)
- Update wiki-editor.md, wiki-writer.md, wiki-researcher.md (agent files — no gate)
- Update device.md Device Health table (self-consistency fix — no gate)
- heart.md may also reference old hook names — check and route through karpathy if so

## 2026-04-12 — device.md

**Section:** Installed Apps → SharePoint Durability Layer
**Change:** SharePoint paths line updated. Removed `Kiro-Drive/artifacts/` (published docs) from the durability layer path list. Added clarifying note: "Published artifacts go to `Artifacts/wiki-sync/` via the separate sharepoint-sync hook." This reflects the earlier session's decision to rename `Kiro-Drive/artifacts/` to `_artifacts-deprecated` since it was redundant with the separate `Artifacts/wiki-sync/` pipeline managed by the sharepoint-sync hook.

**Karpathy gate:** N/A (device.md is not gated).

**Cross-organ consistency:** ✅ No conflicts detected.
- `sharepoint-durability-sync.md` already correctly separates `Kiro-Drive/` paths from `Artifacts/wiki-sync/` and explicitly notes artifacts are managed by the sharepoint-sync hook, not the durability protocol.
- `hook-protocol-audit.md` already reflects the two separate SharePoint pipelines.
- `sharepoint-sync.kiro.hook` (v2.0.0) correctly targets `Artifacts/wiki-sync/`.
- Session log documents the rename of `Kiro-Drive/artifacts/` → `_artifacts-deprecated`.
- No other organ files reference the removed `Kiro-Drive/artifacts/` path (only historical session-log entries, which is correct).

**Action items:** None. All related files were updated in the same session.

## 2026-04-13 — amcc.md

**Section:** Real-Time Intervention Protocol → Trigger Detection table
**Change:** Added new avoidance signal row: "Unread message accumulation." Detects when Slack messages or emails from stakeholders sit unread for 3+ days. Data sources: email-triage.md (UNREAD flags), Slack digest (unanswered items), DuckDB `signals.emails_unanswered`. Escalation weighted by stakeholder importance (Brandon, Lena, Lorena flagged explicitly). aMCC response template: "You have [N] messages unread for [X] days. [Person] is waiting. Reading takes 2 minutes — reply or acknowledge now."

**Karpathy gate:** N/A (amcc.md is not gated — only heart.md and gut.md are gated).

**Cross-organ consistency:** ✅ No conflicts detected.
- Data sources referenced (`signals.emails_unanswered`, email-triage.md, Slack digest) all exist and are populated by AM-Backend ingestion (device.md).
- Stakeholder names (Brandon, Lena, Lorena) align with memory.md relationship graph and current.md active contacts.
- Does NOT overlap with Nervous System Loop 3 (pattern tracking is weekly/retrospective; this detector is real-time/prospective — complementary, not redundant).
- Does NOT conflict with Device.md email/Slack ingestion (device collects data; aMCC uses it for intervention).
- The "Email as escape" detector (existing row) covers mid-task email checking during focus blocks — different trigger than unread accumulation over days. No overlap.

**Action items:** None. Clean addition — no follow-up edits needed in other organs.

## 2026-04-13 (second edit) — amcc.md

**Section:** Real-Time Intervention Protocol → Trigger Detection table → "Unread message accumulation" row
**Change:** Upgraded the unread message accumulation detector with specific DuckDB query references and priority tiers. Old version referenced generic sources (email-triage.md, Slack digest, `signals.emails_unanswered`). New version adds: (1) `signals.slack_unanswered` view with specific columns (`days_old`, `priority` [critical/high/medium/normal], `richard_responded_24h`, `richard_responded_ever`, `richard_reacted`), (2) explicit queries: `SELECT * FROM signals.slack_unanswered WHERE richard_responded_ever = FALSE AND richard_reacted = FALSE` + `SELECT * FROM signals.emails_unanswered WHERE action_needed = 'respond'`, (3) stakeholder priority tiers: Brandon (critical), Kate/Lena/Lorena (high). Fire template updated to split Slack mentions and emails separately.

**Karpathy gate:** N/A (amcc.md is not gated — only heart.md and gut.md are gated).

**Cross-organ consistency:** ✅ No conflicts detected.
- `signals.slack_unanswered` view confirmed in DuckDB — all referenced columns exist: `days_old` (DOUBLE), `priority` (VARCHAR), `richard_responded_24h` (BOOLEAN), `richard_responded_ever` (BOOLEAN), `richard_reacted` (BOOLEAN).
- `signals.emails_unanswered` view confirmed — `action_needed` (VARCHAR), `days_old` (BIGINT), `priority` (VARCHAR) all exist.
- Stakeholder priority tiers (Brandon=critical, Kate/Lena/Lorena=high) align with memory.md relationship graph and org chart.
- Kate added to high-priority tier (was not in previous version) — correct, she's the L8 Director.
- No overlap with other detectors. No conflicts with other organs.

**Action items:** None. Clean upgrade — schema-verified, no follow-up edits needed.
