# Guardrail Usage Log — Grok Proposal vs Existing Machinery

## Grok's proposal (shared/tmp/grok-eval-2/proposed/09-guardrail-usage-log.md)
A lightweight append-only log entry every time a high-stakes output is produced, with six fields:
`date | task type | confidence % | human review flagged Y/N | Richard actually reviewed Y/N | friction noted`

Example Grok gives:
`2026-04-23 | Projection | 62% | Y | Y | Guardrail forced me to quantify the budget sensitivity — much better than before`

The stated purpose: track whether guardrails are being applied consistently and whether they change behavior.

## Existing machinery

### 1. `high-stakes-guardrails.md` (steering, adopted 2026-04-22)
Loads automatically on any file path matching `*{forecast,projection,ceiling,budget,wbr,mbr,pacing,op1,op2,reallocation,ie_ccp,ieccp}*`. Mandates six required behaviors *inside the output itself*:

1. Explicit numeric confidence (e.g., "Confidence: 65%") with why-not-higher / why-not-lower split
2. Top-3 assumptions with directional sensitivity
3. "Human review strongly recommended before action." required closing line
4. No "approved" framing without Richard's explicit confirmation
5. Auto-load `amazon-politics.md` if context is political
6. Use the supplied model in the math, don't reference-then-ignore

In other words: the guardrail's enforcement lives *in the artifact*, not in a side log. Every high-stakes output carries its own confidence score, assumption list, and review flag — permanently, co-located with the number.

### 2. `session-log.md` — 2160 lines of narrative coverage
Every significant session produces a `[YYYY-MM-DD] Topic … | Actions … | Decisions …` block. Today's (2026-04-22) high-stakes items already appear in prose form with the equivalent fields embedded:

- **MX $1.3M email / forecast work** — captured across the 2026-04-21 and 2026-04-22 entries (the Paid App PO, PAM pacing, MX forecast reallocation to Lorena, the 4/22 01:53 Kiro_RW self-note on email overlay, the reversed kill-H1 framing after deeper QA evidence). Confidence posture, assumption changes, and review gate ("awaiting Richard's send/paste call") are all present as text.
- **W17-W22 projection work** — the 2026-04-21 "9pm OOO-prep" and "9pm task triage continued" entries show the W17 WBR sheet fill prioritization, the narrowed 7-item list, the explicit "awaiting Richard's execution start / send-status call" review gate.
- **MPE spec writing** — the MPE (market-projection-engine) spec is an active spec folder (`.kiro/specs/market-projection-engine/`) — spec-level artifacts live in the spec itself, and any high-stakes projection produced *by* MPE would inherit high-stakes-guardrails.md via the filename match on `projection`.

What the session log already captures for every entry:
- **Date** — built into the `[YYYY-MM-DD]` prefix
- **Task type** — readable from the Topic field ("projection", "WBR", "pacing", "forecast")
- **Confidence + assumptions + sensitivities** — present when the output required it (see the 4/21 Enhanced Match / 4/21 Brandon 1:1 / 4/22 email overlay entries)
- **Human review flag** — the `Status: OPEN — awaiting Richard's …` convention is exactly this field
- **Did Richard review** — cross-referencable: the next session's entry closes the loop (`closed via` / `DONE` / next-day action taken)
- **Friction noted** — Decisions field carries every friction observation and process correction (the 4/21 "three meta-failures" entry is a textbook example)

### 3. `rw-tracker.md` — weekly scorecard
Tracks Strategic artifacts shipped, tools built, hours on low-leverage work, meeting output clarity. Weekly granularity, already surfaces whether high-stakes work is shipping.

### 4. `amcc.md` — streak + hard-thing discipline
Captures whether Richard chose the hard thing today and why. Not per-output, but the population-level signal Grok's log is trying to get at ("am I consistently doing the right thing?") is already here at a better abstraction level.

### 5. `main.commitment_ledger` (DuckDB) — already exists
16-column table tracking text_hash, text, source, person, status, days_old, overdue, first_seen, last_seen, completed_date, completed_via. This is the structured companion to session-log's narrative, populated from email/Slack signals. Currently used for commitments to people, not self-generated outputs — but the schema is a superset of what Grok proposes.

## Head-to-head

| Grok's field | Existing coverage | Gap? |
|---|---|---|
| Date | Session-log entry prefix | None |
| Task type | Topic field ("Projection", "WBR", "pacing") | None (free text, not enum — see below) |
| Confidence % | Required in the output itself by high-stakes-guardrails.md | **Strictly stronger** (lives in artifact, not side log) |
| Human review flagged Y/N | "Human review strongly recommended" required closer; Status: OPEN convention | None |
| Richard actually reviewed Y/N | Next session's entry closes the loop explicitly | None, but cross-entry not same-row |
| Friction noted | Decisions field — captures every process correction | None |

What Grok catches that is real:
1. **Task type is free text, not an enum.** "Projection" vs "projection" vs "forecast" vs "MX forecast" all appear. Retroactive aggregation ("how often did I ship a projection?") requires fuzzy matching. A controlled vocabulary would help — but the right place is a DuckDB view over session-log, not a new log.
2. **Richard-reviewed state is inferred across entries, not stored as one row.** Today's "Status: OPEN — awaiting Richard's call" is closed by tomorrow's "Richard approved … executed." Querying "what % of high-stakes outputs got reviewed within 24h" requires joining consecutive entries. Again — a view, not a new log.

## Evaluation against the 8 "How I Build" principles

1. **Routine as liberation (#1)** — ⚠️ The log adds a new post-output ritual. Every high-stakes artifact now needs a log-append step. That's friction inside the creative moment, not liberation from it.
2. **Structural over cosmetic (#2)** — ❌ The existing guardrail is structural (it changes the artifact). A parallel log is cosmetic tracking of whether the structure fired.
3. **Subtraction before addition (#3)** — ❌ Direct violation. Nothing is removed. A new file + a new habit + a new field taxonomy are all added.
4. **Protect the habit loop (#4)** — ⚠️ No new cue/routine/reward designed. The "append to log" step has no clear cue (when does it fire? Post-output? Pre-send? Who enforces?).
5. **Invisible over visible (#5)** — ❌ Logging is a visible ritual. Richard will notice it; the guardrail in the artifact (already live) is designed to be invisible — the output just has better bones.
6. **Reduce decisions, not options (#6)** — Neutral. Doesn't add decisions, but doesn't reduce any either.
7. **Human-in-the-loop on high-stakes (#7)** — Already satisfied by high-stakes-guardrails.md. The log is downstream of what already works.
8. **Check `device.md` before proposing tools (#8)** — Fail the "3+ instances/week" test by intent — Grok is proposing a habit, not a tool. And the friction it's trying to solve ("am I applying guardrails?") isn't a documented recurring pain. The blind A/B test on 4/22 showed guardrails are already improving output quality without a log.

## Does the log change behavior?

The theory of change is: "tracking guardrail adoption will make guardrails better-followed."

That theory only holds if guardrails are being *skipped*. They are not — high-stakes-guardrails.md is auto-loaded via filename match, and the 4/22 blind A/B test went 2-0 for treatment with the biggest delta of any file tested. The structural intervention is already working.

The log would turn a *working* invisible intervention into a visible self-surveillance loop. Behavior change through measurement requires a feedback mechanism — who reads the log? When? What does a pattern of 55% confidence scores on projections tell Richard that the artifacts themselves don't? The proposal has no answer.

## Verdict

**REJECT the log. Build a retroactive query over session-log + high-stakes artifacts instead.**

The information is already captured — in the artifact (confidence, assumptions, review flag), in the session-log (narrative + status + friction + review closure), in amcc.md (streak-level signal), and in rw-tracker (weekly scorecard). What's missing is *retrospective aggregation*, not prospective logging.

### Alternative: a `ps.v_high_stakes_outputs` DuckDB view

A view — not a table, not a log — that:
- Parses session-log entries with Topic matching `{forecast|projection|WBR|MBR|pacing|ceiling|reallocation|ie.?ccp}`
- Extracts status (OPEN/DONE/awaiting-review)
- Computes days-to-close (same-entry, next-entry, later)
- Aggregates: "How many high-stakes outputs last 30d? What % had explicit confidence? What % closed within 24h?"

This is a 30-line SQL view. It adds zero habit overhead, reuses the existing append-only session-log, and surfaces the exact question Grok's log is trying to answer ("am I applying guardrails consistently?") — but *without* forcing a new ritual into every output.

If the query ever shows a pattern of skipped guardrails, *then* add a structural fix (not a log): tighten the file-match pattern in high-stakes-guardrails.md, or add a postToolUse hook that audits outputs for the three required elements and flags misses.

### What to adopt from Grok

Grok's contribution is the **field schema** — the six fields are a reasonable set for the retroactive view. Steal those as the output columns of `ps.v_high_stakes_outputs`. That's it.

## One-line reply

The guardrail already lives in the artifact (high-stakes-guardrails.md) and the session-log already narrates every high-stakes output with status + friction — build a retroactive DuckDB view (`ps.v_high_stakes_outputs`) to aggregate the existing data, don't add a prospective log that creates a new ritual and violates subtraction-before-addition.
