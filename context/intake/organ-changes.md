# Organ Changes Log

## 2026-04-04 — changelog.md (Karpathy Run 26)

**File:** `shared/context/body/changelog.md`
**Author:** Karpathy (autoresearch engine)
**Summary:** Run 26 logged — 10 experiments across 6 organs using underexplored techniques (REMOVE/SPLIT/MERGE/RESTRUCTURE). 5 KEPT, 5 REVERTED. All 5 REMOVE experiments reverted (unique content pattern). KEEPs: amcc Growth Model SPLIT, heart Design Choices COMPRESS (-264w), heart DuckDB Integration RESTRUCTURE, nervous-system Loop 3 MERGE (-69w), device Tool Factory RESTRUCTURE. Gated files (heart.md, gut.md): heart had 2 authorized Karpathy modifications; gut REVERT means no net change. No cross-organ inconsistencies detected.

## 2026-04-04 — changelog.md (Karpathy Run 27)

**File:** `shared/context/body/changelog.md`
**Author:** Karpathy (autoresearch engine)
**Summary:** Run 27 logged — 10 output-quality experiments on wiki agents (wiki-writer, wiki-editor, wiki-researcher, wiki-critic) and style guides (richard-style-email, richard-style-slack, richard-style-docs, richard-style-wbr). 5 KEPT, 5 REVERTED (50% revert rate — target for randomized exploration). KEEPs: wiki-writer dual-audience SPLIT (structural headers), wiki-editor kill criteria REWORD (30d→14d threshold), wiki-researcher ABPS section SPLIT (structural), wiki-critic design philosophy REMOVE (-49w), richard-style-docs post-mortem RESTRUCTURE (lessons-first). REVERTs: wiki-writer REMOVE (behavioral constraints load-bearing), wiki-editor pipeline COMPRESS (checkpoint granularity needed), richard-style-email MERGE (distinct registers), richard-style-slack REMOVE (behavioral correction layer), richard-style-wbr SPLIT (YoY context not optional). No gated files modified (heart.md/gut.md untouched). No cross-organ inconsistencies — all changes target agent prompt files and style guides, not body organs. Wiki-editor kill criteria tightening (30d→14d) aligns with portfolio management staleness thresholds.

## 2026-04-04 — heart.md (Experiment Technique Priors)

**File:** `shared/context/body/heart.md`
**Author:** Karpathy (autoresearch engine) — authorized (gated file, within jurisdiction)
**Summary:** Step 3 experiment technique definitions enriched with learned priors from Runs 26-27. ADD: portable "Common Failures" pattern noted. RESTRUCTURE: lessons-first ordering keeps. REMOVE: caution added — ~80% revert rate, pre-check for unique IDs/URLs/rules/constraints before attempting. REWORD: flagged as highest keep rate (~90%), concrete examples > abstract rules. MERGE: caution for distinct registers/categories. SPLIT: structural splits keep, "optional" labeling reverts. No cross-organ inconsistencies. These annotations encode experiment selection intelligence directly into the protocol, reducing future revert waste.
