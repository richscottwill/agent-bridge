# Organ Changes Log

## 2026-04-03

**File:** `shared/context/body/gut.md`
**Change:** Removed "or when total body approaches 30,000w safety limit" from the Compression Protocol trigger conditions. Compression now triggers only on Bayesian priors (COMPRESS posterior_mean > 0.7, n > 5), not on total body word count.
**Flags:**
- ⚠️ **Karpathy gate:** gut.md is gated — edit was NOT routed through karpathy agent. May be unauthorized.
- ⚠️ **Cross-organ inconsistency:** `nervous-system.md` line 58 still tracks "Total body words ≤30,000w" as a target metric. If the 30,000w limit is no longer a compression trigger, nervous-system.md should be updated to reflect the new policy (or the metric should be reframed as informational rather than a hard limit).

## 2026-04-04

**File:** `shared/context/body/spine.md`
**Change:** Reformatted "Tool Access & Integrations" section from bullet-list format to markdown table. Same 16 MCP servers, same guards, same notes. "No access" line and tool reference path preserved. No content added or removed — purely a readability/formatting change.
**Flags:**
- ✅ No cross-organ conflicts. `tech.md`, `soul.md`, and `asana-command-center.md` references remain consistent.
- ✅ Not a gated file (not heart.md or gut.md). No karpathy approval required.
- ℹ️ Cosmetic change — table format improves scannability over nested bullets.

## 2026-04-04

**File:** `shared/context/body/eyes.md`
**Change:** Compressed competitor intelligence section. US Walmart entry tightened ("First appeared Jul 2024 on Brand Core" → "Brand Core since Jul 2024"). "Key Trends" section renamed to "Trends" and converted from numbered list (5 items) to bullet list (3 items) — same facts, fewer words. No data points changed.
**Flags:**
- ✅ No cross-organ conflicts. Market performance table (line 23) still references "$65-77 Brand" consistent with compressed competitor entry. No other organs reference the specific trend data that was reformatted.
- ✅ Not a gated file (not heart.md or gut.md). No karpathy approval required.
- ℹ️ Compression pass — aligns with gut.md compression principles (subtraction before addition). ~30 words removed, zero information loss.

## 2026-04-04
- **device.md** — Removed duplicate "📋 Templates" section (3 lines). Content was redundant with Tool Factory section which already lists the same queued templates. Net subtraction, no information loss. No cross-organ conflicts detected.

## 2026-04-04

**File:** `shared/context/body/memory.md`
**Change:** Compressed Carlos Palmos entry. Title shortened ("Marketing Manager MX" → "Mktg Mgr MX"). Removed "Meeting dynamic" line (collaborative context no longer relevant post-CPS transition). Draft style shortened ("Professional, include invoice/PO specifics" → "Professional, invoice/PO specifics"). Net: ~15 words removed, zero information loss.
**Flags:**
- ✅ Not a gated file (not heart.md or gut.md). No karpathy approval required.
- ✅ No cross-organ conflicts introduced. `current.md`, `org-chart.md` Carlos references remain consistent with his CPS transition status.
- ℹ️ Pre-existing staleness noted: `asana-notes-protocol.md` still lists Carlos as MX invoice contact and key contact in the MX project template. Since invoice delegation is VOID per memory.md, those references should be updated to reflect Lorena or Richard as the new owner. Not caused by this edit — flagging for cleanup.

## 2026-04-04 — changelog.md (Karpathy Run 20, Saturday batch 2)

- **device.md**: COMPRESS on Templates + Device Health. 1307w→1240w. Removed empty Templates section, compressed Device Health table. KEEP.
- **memory.md**: REWORD on Relationship Graph (Carlos/Harjeet/Alex). 1777w→1745w. Tightened low-activity entries, identity fields preserved. KEEP.
- **brain.md**: REWORD on Decision Log (D1-D8). 1446w→1410w. Removed redundant principle names from Reinforced tags. KEEP.
- Cross-organ check: No conflicts. All changes are compression/tightening within each organ's domain.
- Gated file check: N/A (changelog.md edited, not heart.md or gut.md). Underlying organ edits by Karpathy — authorized.

## 2026-04-04 — changelog.md (Karpathy Run 21, Saturday batch 3)

- **wiki-writer style guide**: 5 output-quality experiments on wiki-writer agent config. REWORD on Voice rules (2761w→2698w, Δ=+0.15, KEEP). ADD on Voice rules (2698w→2718w, Δ=+0.02, KEEP). RESTRUCTURE on Draft structure template (2718w→2730w, Δ=+0.01, KEEP). COMPRESS on Article types (2730w→2710w, Δ=-0.01, REVERT — lost guide/playbook distinction). COMPRESS on Design philosophy (2730w→2702w, Δ=0.00, KEEP).
- Net: 4 kept, 1 reverted. wiki-writer config at 2702w (down from 2761w baseline).
- Cross-organ check: ✅ No conflicts. Changes target wiki-writer agent config, not body organs. No organ content modified.
- Gated file check: ✅ N/A (changelog.md edited, not heart.md or gut.md). Experiments executed by Karpathy — authorized.

## 2026-04-04 — changelog.md (Karpathy Run 22, Saturday batch 4)

- **wiki-researcher agent config**: 3 output-quality experiments. RESTRUCTURE on Research sources priority (1476w→1510w, Δ=+0.09, KEEP — moved DuckDB and Slack above meeting transcripts). ADD on Research brief format (1510w→1535w, Δ=+0.08, KEEP — added Confidence assessment section). REWORD on Research principles (1535w→1548w, Δ=+0.09, KEEP — structured citation format [source: type, date, confidence]).
- **wiki-critic agent config**: 3 output-quality experiments. REWORD on Score dimensions (2131w→2310w, Δ=+0.06, KEEP — concrete examples at each score level across 5 dimensions). ADD on Economy dimension (2310w→2355w, Δ=+0.04, KEEP — verb rule for list items). RESTRUCTURE on Thresholds (2355w→2397w, Δ=+0.04, KEEP — raised dimension floor from 6 to 7).
- Net: 6 kept, 0 reverted. wiki-researcher at 1548w, wiki-critic at 2397w.
- Cross-organ check: ✅ No conflicts. The dimension floor change (6→7) in wiki-critic is internal to the critic's scoring rubric and does not affect the overall 8/10 approval threshold documented in ABPS AI spec (Property 8, Requirements 3.5/10.7). The approval gate remains: average >= 8 → approve, average < 8 → revise. The floor change means no single dimension can score below 7 even if the average is >= 8 — a stricter quality bar, consistent with the spec's intent.
- Gated file check: ✅ N/A (changelog.md edited, not heart.md or gut.md). Experiments executed by Karpathy — authorized.

## 2026-04-04 — changelog.md (Karpathy Run 23, Saturday batch 5)

- **wiki-editor agent config**: 2 output-quality experiments. MERGE on Work_Product type table (2175w→2148w, Δ=-0.06, REVERT — guide/playbook merge lost branching-logic distinction). ADD on Work_Product type heuristic (2175w→2214w, Δ=+0.05, KEEP — name-pattern heuristic for person names → reference, process verbs → guide).
- **richard-style-docs steering file**: 3 output-quality experiments. REWORD on Experiment Documents structure (565w→579w, Δ=+0.04, KEEP). ADD on Universal Rules (579w→619w, Δ=+0.03, KEEP — 3-bullet max + verb-start rule). RESTRUCTURE on header rule (619w→659w, Δ=+0.05, KEEP — question/imperative headers).
- **richard-style-amazon steering file**: 2 output-quality experiments. REWORD on Analytical Patterns metric rule (351w→373w, Δ=+0.05, KEEP — metric template). ADD on Confidence calibration table (373w→462w, Δ=+0.06, KEEP — HIGH/MEDIUM/LOW criteria with data thresholds, highest delta in batch).
- Net: 6 kept, 1 reverted. Key finding: guide/playbook MERGE reverted on both wiki-writer (Run 21) and wiki-editor (Run 23) — the DO vs FOLLOW distinction is validated as a real semantic boundary.
- Cross-organ check: ✅ No conflicts. Changes target agent configs and steering files, not body organs. The confidence calibration table in richard-style-amazon is additive and doesn't conflict with any organ content. The guide/playbook validation is consistent with the ABPS AI design doc's Work_Product type classification (guide, reference, decision, playbook, analysis).
- Gated file check: ✅ N/A (changelog.md edited, not heart.md or gut.md). Experiments executed by Karpathy — authorized.
