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
