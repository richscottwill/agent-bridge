---
inclusion: manual
---

# Karpathy — File Type Awareness for Experiments

*Rule added 2026-04-29 after run_W18 batch produced 7 broken JSON hook files with KEEP decisions. Karpathy's blind content evaluator scored output_quality highly on prose additions to hook files but didn't check that the result still parses as JSON.*

## The core rule

**Before any experiment KEEPs a modified file, verify the file still parses as its declared type.** Content evaluation is not sufficient. A markdown hook file that reads beautifully but fails to parse as JSON is worse than the unmodified original — it breaks the hook entirely.

## File type matrix

| Path pattern | Type | Validity check |
|---|---|---|
| `.kiro/hooks/*.kiro.hook` | JSON | `json.loads(file.read())` must succeed |
| `.kiro/agents/*.json` | JSON | `json.loads(file.read())` must succeed |
| `.kiro/agents/*.md` | Markdown with YAML frontmatter | frontmatter parseable + body renders as markdown |
| `.kiro/steering/*.md` | Markdown with YAML frontmatter | frontmatter parseable + body renders as markdown |
| `context/body/*.md` | Markdown | headers balanced, no orphan ``` blocks |
| `context/active/*.json` | JSON | `json.loads` must succeed |
| `context/active/*.jsonl` | JSONL | each line must parse as JSON |
| `context/active/*.tsv` | TSV | column count consistent across rows |
| `context/active/*.md` | Markdown | headers balanced |
| `context/protocols/*.md` | Markdown | headers balanced |
| `tools/**/*.py` | Python | `ast.parse(file.read())` must succeed |
| `tools/**/*.sh` | Shell | `bash -n file` must succeed |
| `dashboards/**/*.py` | Python | `ast.parse` must succeed |
| `dashboards/**/*.html` | HTML | not automatically checked — avoid experimenting unless you have a harness |
| `wiki/**/*.md` | Markdown | headers balanced |

## What counts as "parses"

- **JSON:** `json.loads(Path(p).read_text())` completes without exception
- **Python:** `ast.parse(Path(p).read_text())` completes without exception
- **Shell:** `subprocess.run(['bash', '-n', p])` returns 0
- **YAML frontmatter:** frontmatter between `---` markers parses as YAML via `yaml.safe_load`
- **Markdown:** headers balanced (every `#` has matching closing), no orphan fence markers (every ` ``` ` has a pair)

## Proposed experiment flow for structured files

When running experiments against any file type other than plain markdown/prose:

1. Before modification: record baseline validity (expected: valid).
2. Apply the technique.
3. **Before** running the output_quality evaluation, run the structural validity check.
4. If validity check fails: mark BLOCKER with reason `structural_invalidity`, revert, skip content evaluation. The content score cannot compensate for a file that no longer works.
5. If validity check passes: proceed to content evaluation as normal.

## Why this matters

The W18 batch scored `session-summary.kiro.hook` modifications at `output_quality=0.8` — the content additions (preamble rewording, section splitting) read well as prose. But the result wasn't valid JSON, so the hook wouldn't execute at all. A hook that scores 0.8 on prose quality but cannot run is strictly worse than an unmodified hook that scores 0.7.

The KEEP decision metric implicitly assumes: "a higher-scoring version of this file is better." That assumption holds for markdown, where parseability is forgiving. It breaks for structured files, where parseability is a precondition for any function.

## Dashboard of broken files to repair

As of 2026-04-29 after run_W18, these hooks were broken and have been reverted to last-good state from git:

- `.kiro/hooks/am-backend.kiro.hook`
- `.kiro/hooks/am-triage.kiro.hook`
- `.kiro/hooks/audit-asana-writes.kiro.hook`
- `.kiro/hooks/eod.kiro.hook`
- `.kiro/hooks/guard-email.kiro.hook`
- `.kiro/hooks/mpe-acceptance-core.kiro.hook`
- `.kiro/hooks/mpe-demo-prep.kiro.hook`
- `.kiro/hooks/organ-change-detector.kiro.hook`
- `.kiro/hooks/ps-audit.kiro.hook`
- `.kiro/hooks/session-summary.kiro.hook`
- `.kiro/hooks/sharepoint-sync.kiro.hook`
- `.kiro/hooks/topic-sentry.kiro.hook`
- `.kiro/hooks/wbr-pipeline-trigger.kiro.hook`

## Learnings from run_W18 that are independently valuable

- HOOK/SCRIPT targets: 9% KEEP rate vs 25% on markdown. The evaluator already implicitly penalizes structured files; making that penalty explicit (via file-type-aware validity) should raise the KEEP rate because content-only wins on structured files currently fail silently at the file-validity layer.
- REMOVE technique: 18% KEEP (lowest), REMOVE+REVERT at 37% is the highest revert rate. The system is at a compression plateau. Prefer MERGE (29% KEEP) and ADD (26%) over REMOVE and SPLIT for future batches.
- Body organs vary widely: brain 57% KEEP, gut 55% KEEP — lived-in files benefit from clarification. amcc 19%, heart 25%, nervous-system 26% — philosophy-heavy files resist improvement. Karpathy may want to reduce experiment volume on low-KEEP-rate files until a new angle is identified.
- Overall: 202 KEEP vs 213 REVERT — near-plateau. Before the next big batch, look for a new experiment dimension (e.g., cross-file coherence checks, template-driven generation) rather than more random technique × target pairs.

## Routing

This rule is owned by karpathy. Do not modify without routing through the karpathy agent. The experiment protocol, hard-thing-selection protocol, and evaluator code all live in karpathy's domain per soul.md.

If a new file type needs the validity matrix extended (e.g., `.yaml`, `.toml`, `.sql`), propose the extension in intake and route to karpathy for approval.
