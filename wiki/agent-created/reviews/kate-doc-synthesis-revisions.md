---
title: "Revisions: kate-doc-synthesis.md"
status: DRAFT
audience: amazon-internal
owner: Richard Williams
created: 2026-04-12
updated: 2026-04-12
---
<!-- DOC-0478 | duck_id: wiki-review-kate-doc-synthesis-revisions -->

# Revisions: kate-doc-synthesis.md

Source: kate-doc-batch-review.md
Verdict: REVISE
Priority: HIGH (this is the doc Kate reads — accuracy must be airtight)

---

## Required Change 1: Fix OCI NB CPA improvement in Workstream 1 table

**Location:** Workstream 1: Intelligent Bidding (OCI) — Results table

**Current text:**
```
| US | +24% | -45% | +32,047 | $16.7MM |
```

**Replace with:**
```
| US | +24% | ~50% | +32,047 | $16.7MM |
```

**Rationale:** Consistent with oci-performance.md. The "-45%" figure is not in the verified source. This is the third doc where this fix applies — all three must be consistent.

---

## Required Change 2: Fix OCI NB CPA in 2026 Investment Summary table

**Location:** 2026 Investment Summary table — OCI Bidding row

**Current text:**
```
| OCI Bidding | +24% reg uplift; -45% NB CPA; +35K regs / $16.7MM OPS | Scale to FR, IT, ES, CA, JP (Jul 2026) | Replicate double-digit reg uplift in RoW |
```

**Replace with:**
```
| OCI Bidding | +24% reg uplift; ~50% NB CPA improvement; +35K regs / $16.7MM OPS | Scale to FR, IT, ES, CA, JP (Jul 2026) | Replicate double-digit reg uplift in RoW |
```

**Rationale:** Same cascading fix. The investment summary table is the single most important table in the entire document — Kate will reference it repeatedly. It must be accurate.

---

## Required Change 3: Clarify UK CTR metric in Modern Search section **Location:** Workstream 2: Modern Search — UK Results table The table currently shows: ``` | CTR | 14% | 24% | **+70%** | ``` Add a clarifying note immediately after the table: ``` Pre/post comparison (Dec 27-Jan 28 vs. Jan 29-Mar 2). The test-vs-control CTR improvement over the same period was +86%. ``` **Rationale:** The synthesis doc's summary tag and the Modern Search doc both reference "+86% CTR" as the headline metric, but the table in the synthesis shows "+70%." Both are correct — +86% is test-vs-control, +70% is pre/post. Without the clarifying note, Kate may see the discrepancy and question the data. The note resolves the ambiguity in one sentence. --- ## Required Change 4: Fix UK/DE NB CPA in Workstream 1 table

**Location:** Workstream 1: Intelligent Bidding (OCI) — Results table

The table currently does not show UK/DE NB CPA (they show "—" for OPS), but the standalone OCI doc's table has the "-38%" and "-37%" figures. Verify the synthesis table matches whatever the OCI doc settles on after revision. If the OCI doc changes to "Significant," the synthesis table header should not include "NB CPA Improvement" as a column unless it has values for all rows.

**Current synthesis table:**
```
| Market | Reg Lift | NB CPA Improvement | Estimated Regs | Estimated OPS |
|--------|----------|---------------------|----------------|---------------|
| US | +24% | -45% | +32,047 | $16.7MM |
| UK | +23% | -38% | +2,400 | — |
| DE | +18% | -37% | +749 | — |
```

#### Required Change 4: Fix UK/DE NB CPA in Workstream 1 table — Details


**Replace with:**
```
| Market | Reg Lift | NB CPA Improvement | Estimated Regs | Estimated OPS |
|--------|----------|---------------------|----------------|---------------|
| US | +24% | ~50% | +32,047 | $16.7MM |
| UK | +23% | Significant | +2,400 | — |
| DE | +18% | Significant | +749 | — |
```

**Rationale:** Consistency with the OCI doc revision and the source data.

---

## Post-Revision Expected Score

| Dimension | Current | Expected |
|-----------|---------|----------|
| Accuracy | 7/10 | 9/10 |
| Overall | 8.0/10 | 8.6/10 |
| Verdict | REVISE | PUBLISH |
