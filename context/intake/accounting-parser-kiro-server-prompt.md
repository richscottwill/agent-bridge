# First message to paste into the kiro-server session

I need you to continue the accounting-parser project from where kiro-local left it.

Read these in order:

1. `agent-bridge/context/intake/accounting-parser-kiro-server-handoff.md` — full handoff with tiered plan, environment quirks, verified correctness properties.
2. `.kiro/specs/accounting-document-parser/tasks.md` — every task has a status marker. `[x]` done, `[~]` DEFERRED with explicit blocker, `[ ]` open (should be none at this point).
3. `accounting-parser/README.md` in the target repo for the bootstrap commands.

**Step 1: reproduce kiro-local's state.**

```bash
git clone https://github.com/richscottwill/accounting-parser.git
cd accounting-parser
docker compose up -d
cd backend && poetry install && poetry run pytest --no-cov
cd ../frontend && pnpm install && pnpm test && pnpm build
cd ../tests/fixtures && poetry install && poetry run pytest
```

Expected: 88 backend + 79 fixtures = 167/167 green.

Report the count back to me in one line. If anything fails, stop and surface the error — don't improvise fixes to kiro-local's commits.

**Step 2: pick up Tier 1 (Tasks 5, 6, 17) in the handoff doc's prescribed order.**

Start with Task 5 (FastAPI auth middleware + Cognito + WebAuthn signup flow). It's the foundation for Task 6 (ingestion) and Task 17 (workflow engine).

Don't skip ahead. Don't silently defer. When a subtask blocks, flag it, don't pretend.

**Constraints.**

- Each task: feature branch off main, descriptive conventional commits, push to origin.
- Each [Validate] sub-task that requires Playwright must actually drive the running UI. If the UI isn't running, stand it up first — don't fake it against a mock backend.
- Vendor sample licensing: don't pull CCH / AdvanceFlow / UltraTax / Lacerte samples from GitHub mirrors. `tests/fixtures/vendor/README.md` explains why. Use our synthetic factories + manual vendor-sandbox round-trip as the real acceptance gate for the exporters.
- Post a one-line status to `shared/context/intake/session-log.md` at the end of each task.

When Tier 1 is complete, pause and confirm with me before starting Tier 2.
