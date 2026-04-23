# D4-Var1: MBR Section Draft — Fresh Agent Simulation

**Task:** "Draft my MBR section for May covering AU and MX performance. Brandon needs my input by Monday."

**Simulated steering context:**
- Always-on: soul.md, process-execution.md, file-creation-rules.md, devspaces-core.md, amazon-builder-production-safety.md, agentspaces-core.md
- Canonical Resources table inside soul.md maps:
  - MBR section → `richard-style-mbr.md` + `richard-style-amazon.md`
  - Formal docs → `richard-style-docs.md` + `richard-style-amazon.md`
  - WBR callout → `richard-style-wbr.md` + `richard-style-amazon.md`
- No steering-index.

---

## Fresh-agent reasoning

The task has three signal words that matter: **MBR**, **AU/MX performance**, **Brandon**.

From soul.md I already know:
- Richard is Marketing Manager on Amazon Business Paid Search, reports to Brandon Munday.
- AU and MX are his hands-on markets.
- There's a "Professional writing rule" — any professional prose must load the relevant style guide before drafting. The guides listed are richard-writing-style.md (core), richard-style-email, richard-style-wbr, richard-style-mbr, richard-style-docs, richard-style-amazon — all manual inclusion.
- soul.md contains a Canonical Resources table (in this sim) that maps "MBR section" explicitly to `richard-style-mbr.md` + `richard-style-amazon.md`.
- Data routing table tells me where to pull performance data: `ps.v_monthly` with market + period_key filter, with state files in SharePoint `Kiro-Drive/state-files/` as narrative fallback.

So the task splits cleanly:
1. **Style/voice** — load the MBR style guide + Amazon writing overlay. Canonical Resources tells me exactly which.
2. **Data** — pull May AU and MX monthly performance from DuckDB `ps.v_monthly`, cross-check against OP2 targets in `ps.targets`, and read the AU and MX state files for narrative context (active initiatives, open items, what the team already knows).
3. **Context on Brandon's expectations** — check if there's an MBR Loop page or prior MBR sections I should match in structure. soul.md routing says `docs.loop_pages` or SharePoint `sharepoint_read_loop` for Loop content. Artifacts/reporting/ has MBR templates as .docx.

### Files I would load (and why)

**Style guides — required by the professional writing rule:**
1. `richard-writing-style.md` — core voice. Required for any professional prose.
2. `richard-style-mbr.md` — MBR-specific structure, section conventions, what Brandon expects. Canonical Resources says this is the primary for "MBR section."
3. `richard-style-amazon.md` — Amazon writing overlay (narrative, data-backed, no marketing fluff). Canonical Resources pairs this with every formal output.

**Context — required for the substance:**
4. `~/shared/context/body/body.md` — navigation map, to confirm organ paths before I start pulling.
5. `~/shared/context/body/amcc.md` — streak/hard-thing check before doing the work (soul.md instruction #3 and #5).
6. `~/shared/context/active/current.md` — live state, any MBR-related tasks already in flight.

**Data sources — once I know the shape:**
7. DuckDB `ps.v_monthly WHERE market IN ('AU','MX') AND period_key='2026-May'` — regs, spend, CPA.
8. DuckDB `ps.targets WHERE market IN ('AU','MX') AND period_key='2026-May'` — OP2 targets for variance math.
9. DuckDB `ps.v_weekly` for the May weeks if I need to explain month shape.
10. SharePoint `Kiro-Drive/state-files/AU.md` and `Kiro-Drive/state-files/MX.md` — narrative context, active initiatives, open items.
11. SharePoint `Artifacts/reporting/` — prior MBR templates or prior months' sections to match structure.
12. SharePoint Loop page for the May MBR if Brandon has one open (via `sharepoint_read_loop`).

**Optional but likely useful:**
13. `memory.md` — relationship context on Brandon (how he reads things, what he flags).
14. `~/shared/wiki/agent-created/operations/ps-performance-schema.md` — schema reference for v_monthly.

### Checks I would run before drafting

- **High-stakes check (soul.md principle #7):** An MBR section going to an L7 manager for a formal monthly review qualifies as high-stakes — it's a "final business review" input. I would load `high-stakes-guardrails.md` and apply the explicit-confidence / top-3 assumptions / human-review behavior. Any projection or attribution claim in the draft needs confirmation from Richard before it goes to Brandon.
- **Data freshness:** Query `ops.data_freshness` before trusting `ps.v_monthly` for May. If the month is still in progress or the sync is stale, flag it rather than silently rolling with incomplete data.
- **Structural match:** If Brandon has a specific MBR structure from April, match it. Don't invent a new structure.

### Execution plan (not executed in this sim)

1. Load the three style guides (mbr + amazon + core writing).
2. Read body.md → confirm state file paths → read AU.md, MX.md state files.
3. Query DuckDB for May AU/MX monthly + targets + freshness check.
4. Check SharePoint for the May MBR Loop page and any prior-month MBR sections.
5. Draft in the MBR structure (likely: headline → AU performance vs OP2 + narrative → MX performance vs OP2 + narrative → what's working / what's not / what's next).
6. Flag any number or claim that needs Richard's confirmation before send.
7. Save draft to `~/shared/context/intake/drafts/2026-05-mbr-au-mx.md` (pattern matches the existing draft file for yun-kang-mx-nb-drop visible in open editors).
8. Ask Richard to review before pushing anywhere visible to Brandon.

---

## DISCOVERY LOG

**How did I know which style guides to load?**
Two signals converged cleanly:
1. soul.md's Professional writing rule names all the style guides explicitly and says MBR goes through `richard-style-mbr`.
2. The simulated Canonical Resources table in soul.md maps "MBR section" → `richard-style-mbr.md` + `richard-style-amazon.md` as a direct lookup.

The Canonical Resources table was the load-bearing piece. Without it, I'd still find the guides via the Professional writing rule list, but the table removes ambiguity about which overlay to pair (amazon.md vs docs.md). The rule lists six guides; the table tells me exactly two for this task.

**Friction points:**
- None significant. The soul.md Canonical Resources table did the job of a steering-index for this specific task type.
- Minor: the task doesn't say whether "MBR section" means Richard's contribution to Brandon's consolidated MBR doc or a standalone MBR Richard owns. I'd assume the former (contribution to Brandon's doc) based on "Brandon needs my input" wording, and confirm by checking the Loop page or prior months before drafting.

**What I did NOT need:**
- steering-index (not present, not missed — Canonical Resources covered it)
- Other style guides (email, wbr, docs) — the table disambiguated so I didn't load them speculatively
- callout-principles.md — this isn't a callout
- Any agent routing — rw-trainer isn't the right fit (this is execution work, not coaching or strategic artifact review); karpathy isn't involved (no heart/gut/loop edits)

**What could go wrong with this setup:**
- If the Canonical Resources table inside soul.md drifts out of sync with the actual filenames on disk, a fresh agent would load a guide that doesn't exist. An index would at least be a single source of truth. Inline in soul.md means every edit to the guide roster requires a soul.md edit.
- soul.md is getting dense. Adding a Canonical Resources table on top of the existing Data & Context Routing table, Agent Routing Directory, and Instructions list pushes it toward the "does every element earn its place" question from principle #3 (subtraction before addition). At some point the table of tables becomes its own friction.

**Rating of this steering configuration for this task:** Strong. Single lookup, unambiguous answer, no hunting. The inline table in soul.md works well *for this task type* because the mapping is stable and short. It would scale worse if the number of output types grew (>10 rows), at which point pulling it out into a dedicated file becomes cheaper than keeping soul.md readable.

---

**Simulated — no MBR text produced. No data queries actually run. No files actually loaded.**
