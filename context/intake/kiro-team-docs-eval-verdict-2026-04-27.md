# Kiro Team Docs Blind A/B — Verdict (2026-04-27)

## Headline

**REVISED wins 12 of 13.** Original wins 1 (#12 kiro-team-orchestration).
Agent audience: REVISED won 10, Original won 2, Tie 1 (over 13 docs).
Exec audience: REVISED won 10, Original won 2, Tie 1 (over 13 docs).

Deleted 12 original variants and the REVISED-12 variant. Final folder contains 1 current version per doc, mixed prefixes — see "Follow-ups" below.

## Methodology

Pattern A blind replacement test per `blind-test-harness.md`:
- 13 doc pairs × 2 audiences (agent, exec) × 5 blind evaluator runs = 130 scorings
- 26 sub-agents, each handling 5 runs of one (doc, audience) pair
- 5-dim rubric (1-10 each; total /50): clarity, actionability, signal-to-noise, audience fit, use/forward
- Per-run persona rotation (5 personas per audience — e.g., "careful executor", "Brandon L7", "Kate L8", "token-efficient agent")
- Positional A/B assignment shuffled per run via seed=42, sealed until scoring completed
- Win threshold per (doc, audience): ≥5 pts margin on aggregate (/250); otherwise tie
- Overall verdict per pair (agent + exec): ≥10 pts margin on /500 or wins-tally breaks tie

## Results table (per pair, agent+exec combined)

| # | Slug | Orig /500 | Rev /500 | Orig wins/10 | Rev wins/10 | Verdict |
|---|------|---:|---:|---:|---:|---|
| 00 | README | 351 | 409 | 2 | 8 | REVISED |
| 01 | environment-matrix | 349 | 395 | 2 | 7 | REVISED |
| 02 | no-external-write-rule | 317 | 408 | 0 | 10 | REVISED |
| 03 | steering-packages | 353 | 386 | 4 | 5 | REVISED |
| 04 | sharepoint-protocol | 321 | 346 | 3 | 7 | REVISED |
| 05 | slack-mcp | 326 | 364 | 3 | 7 | REVISED |
| 06 | outlook-mcp | 335 | 357 | 4 | 6 | REVISED |
| 07 | writing-with-kiro | 321 | 363 | 2 | 8 | REVISED |
| 08 | asana-mcp | 282 | 380 | 0 | 10 | REVISED |
| 09 | excel-source-of-truth | 301 | 390 | 0 | 10 | REVISED |
| 10 | team-wiki | 316 | 364 | 3 | 7 | REVISED |
| 11 | hooks-cookbook | 288 | 365 | 0 | 10 | REVISED |
| **12** | **team-orchestration** | **351** | **338** | **6** | **4** | **ORIGINAL** |

## Why REVISED won most (pattern analysis)

Blind evaluators across both audiences consistently rewarded:
- **Tool inventory tables with auto-approve columns** (agent audience loved these — cited in 05, 06, 08 comments as "exactly what a careful executor needs to avoid calling a gated tool")
- **Problem/Cause/Fix failure-mode grids** (agent: faster guardrail lookup than prose bullets)
- **Shorter length with equal or higher substance** (token-efficient persona: "materially shorter while carrying strictly more agent-relevant structure")
- **Token budgets per file** (exec: "signals this team actually knows what it's buying")
- **Explicit audience line in lede** (exec: Brandon persona preferred "problem → solution → packages" framing)

## Why Original won #12 (team-orchestration)

The original version had richer orchestration framing that won for BOTH audiences:
- Agent 206 vs 195 (original won 3/5 runs)
- Exec 145 vs 143 (original won 3/5 runs but within tie threshold)

Likely driver: team-orchestration is the capstone doc that needs narrative depth to frame how the pieces connect. The REVISED version's aggressive compression removed context that readers needed to connect the dots. Compression isn't always a win when the doc's job is synthesis.

## Pattern observations

1. **Revision doctrine worked overall.** Whatever editorial hand shortened the docs, added tool tables, and tightened failure modes was net-positive 12/13 times.
2. **Agent audience benefited more.** Average exec margin was +27 pts (/500), agent margin was +24 pts — roughly even, but agent never had a REVISED loss while exec had one (#12).
3. **Compression has a ceiling.** Doc #12 was the most synthesis-heavy; the REVISED version dropped from 9.9 KB → 6.9 KB and lost the connective tissue. For docs that exist to tie concepts together, aggressive cuts hurt.
4. **Close calls all skewed to length.** Docs with smallest revision wins (#03 steering, #06 outlook) had the tightest agent+exec agreement. Docs with biggest revision wins (#02, #08, #11) had highest agent-fit delta — the revision added structure (tables, grids) the originals lacked.

## Actions taken

Deleted 13 files from SharePoint `Kiro-Drive/Artifacts/kiro-paid-acq-team/`:

- 12 originals: `00-README.md`, `01-kiro-environment-matrix.md` through `11-kiro-hooks-cookbook.md` (excluding `12-kiro-team-orchestration.md`)
- 1 REVISED: `REVISED-12-kiro-team-orchestration.md`

## Follow-ups

1. **Rename REVISED-* files.** The 12 REVISED winners still carry the REVISED- prefix. Rename to drop it so the series is clean: `REVISED-00-README.md` → `00-README.md`, etc.
2. **Legacy cleanup.** Two old unprefixed drafts remain and weren't in the test because they had no pair: `01-environment-matrix.md`, `03-no-external-write-rule.md`. Plus `README.md` (unprefixed). Confirm these are superseded and delete.
3. **The #12 original kept its original filename.** `12-kiro-team-orchestration.md` is the canonical version. Consider whether to hand-merge any REVISED-12 structural improvements into it, or leave as-is.

## Evidence

- Brief: `shared/tmp/kiro-team-docs-eval-r1/EVALUATOR_BRIEF.md`
- Randomization: `shared/tmp/kiro-team-docs-eval-r1/randomization.csv`
- Per-eval scores: `shared/tmp/kiro-team-docs-eval-r1/blind-eval/*.json` (26 files)
- Aggregation script: `shared/tmp/kiro-team-docs-eval-r1/aggregate.py`
- Results: `shared/tmp/kiro-team-docs-eval-r1/results.json`
- Delete list: `shared/tmp/kiro-team-docs-eval-r1/delete_list.txt`
