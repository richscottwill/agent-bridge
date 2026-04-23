# Pilot Review — 2026-04-22

**T0**: 2026-04-21T00:00:00+0000  
**T30**: 2026-04-22T00:00:00+0000  
**Duration**: 1 days

## Outcome: FAIL

0 of 9 skills activated at least once in the 30-day window (threshold: ≥5). 0 skill(s) reached KEEP (≥3 activations); 9 flagged PRUNE-CANDIDATE. Breadth threshold NOT met — adoption habit is not sticking. Do NOT build new skills; revisit the design (matcher, triggers, or whether the corpus fits) per design §Post-pilot decision point.

**Pass threshold**: ≥5 of 9 skills activated AND ≥3 activations per activated skill

## Skills activated at all: 0/9
## Powers activated at all: 0/4

## Per-asset activation metrics

| Kind | Name | Activations | Missed-by-feedback | First | Last | Outcome |
|------|------|-------------|--------------------|-------|------|---------|
| skill | bridge-sync | 0 | 0 | — | — | PRUNE-CANDIDATE |
| skill | charts | 0 | 0 | — | — | PRUNE-CANDIDATE |
| skill | coach | 0 | 0 | — | — | PRUNE-CANDIDATE |
| skill | cr-tagging | 0 | 0 | — | — | PRUNE-CANDIDATE |
| skill | sharepoint-sync | 0 | 0 | — | — | PRUNE-CANDIDATE |
| skill | wbr-callouts | 0 | 0 | — | — | PRUNE-CANDIDATE |
| skill | wiki-audit | 0 | 0 | — | — | PRUNE-CANDIDATE |
| skill | wiki-search | 0 | 0 | — | — | PRUNE-CANDIDATE |
| skill | wiki-write | 0 | 0 | — | — | PRUNE-CANDIDATE |
| power | aws-agentcore | 0 | 0 | — | — | PRUNE-CANDIDATE |
| power | flow-gen | 0 | 0 | — | — | PRUNE-CANDIDATE |
| power | hedy | 0 | 0 | — | — | PRUNE-CANDIDATE |
| power | power-builder | 0 | 0 | — | — | PRUNE-CANDIDATE |

## Skills / powers failing criterion (suggested PRUNE-CANDIDATEs)

Each row below is a pre-filled suggestion. Take these into a Group 6 pruning review: mark APPROVE / DEFER / PROTECT and only then call `pruning.execute_prune()` against the approved rows.

- [ ] **bridge-sync** (skill) — suggested action: `APPROVE (suggested)`. Rationale: Failed pilot criterion: 0 activations in 30-day window (threshold: ≥3).
- [ ] **charts** (skill) — suggested action: `APPROVE (suggested)`. Rationale: Failed pilot criterion: 0 activations in 30-day window (threshold: ≥3).
- [ ] **coach** (skill) — suggested action: `APPROVE (suggested)`. Rationale: Failed pilot criterion: 0 activations in 30-day window (threshold: ≥3).
- [ ] **cr-tagging** (skill) — suggested action: `APPROVE (suggested)`. Rationale: Failed pilot criterion: 0 activations in 30-day window (threshold: ≥3).
- [ ] **sharepoint-sync** (skill) — suggested action: `APPROVE (suggested)`. Rationale: Failed pilot criterion: 0 activations in 30-day window (threshold: ≥3).
- [ ] **wbr-callouts** (skill) — suggested action: `APPROVE (suggested)`. Rationale: Failed pilot criterion: 0 activations in 30-day window (threshold: ≥3).
- [ ] **wiki-audit** (skill) — suggested action: `APPROVE (suggested)`. Rationale: Failed pilot criterion: 0 activations in 30-day window (threshold: ≥3).
- [ ] **wiki-search** (skill) — suggested action: `APPROVE (suggested)`. Rationale: Failed pilot criterion: 0 activations in 30-day window (threshold: ≥3).
- [ ] **wiki-write** (skill) — suggested action: `APPROVE (suggested)`. Rationale: Failed pilot criterion: 0 activations in 30-day window (threshold: ≥3).
- [ ] **aws-agentcore** (power) — suggested action: `APPROVE (suggested)`. Rationale: Failed pilot criterion: 0 activations in 30-day window (threshold: ≥3).
- [ ] **flow-gen** (power) — suggested action: `APPROVE (suggested)`. Rationale: Failed pilot criterion: 0 activations in 30-day window (threshold: ≥3).
- [ ] **hedy** (power) — suggested action: `APPROVE (suggested)`. Rationale: Failed pilot criterion: 0 activations in 30-day window (threshold: ≥3).
- [ ] **power-builder** (power) — suggested action: `APPROVE (suggested)`. Rationale: Failed pilot criterion: 0 activations in 30-day window (threshold: ≥3).

## Next-round direction (Richard decides)

The adoption habit did NOT stick. Do NOT build new skills. Do NOT implement routing tree / safe-creation (if still deferred). Investigate the cause first:

1. **Check if the pre-draft keyword matcher is firing** (Group 3.4). A broken matcher looks identical to an unused corpus from the log's perspective. Verify with a test request that clearly hits a skill's trigger keywords and watch whether an `activated` row appears.
2. **Compare the `missed-by-feedback` tally to zero-activation skills.** If the same skills appear in both, the matcher is missing them — the triggers are wrong, not the skill itself.

Then pick one of four options:

- **Fix the matcher** (3.4 bug) — re-baseline, re-run the 30-day pilot. Groups 4–8 stay deferred.
- **Update trigger lists** via touch-it-classify-it (5.4) — edit the legacy skill's description to include the triggers Richard's requests actually used. No Group 5.3 new-asset writes until activation works.
- **Accept skills don't fit** — some of the 9 may be METAPHOR-ONLY (audit methodology). Run Group 6 pruning to remove the dead weight.
- **Revisit the design** — if fixing the matcher or the triggers won't help, the adoption-system hypothesis is falsified for this corpus. Pull the work back to design, not forward to more implementation.

