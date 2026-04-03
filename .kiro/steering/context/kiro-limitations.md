---
inclusion: manual
---

# Kiro Limitations & Workarounds

Capabilities Kiro doesn't currently support, with practical workarounds. Documenting these prevents wasted effort.

## Limitations

1. **Cross-workspace steering sync** — Global steering (~/.kiro/steering/) is per-machine. No built-in sync between DevSpaces instances.
   - Workaround: Use agent-bridge-sync to manually sync steering files via git.

2. **Hook chaining** — Hooks are independent. One hook cannot trigger another. AM-1 → AM-2 → AM-3 requires manual triggering of each.
   - Workaround: Keep manual sequential triggering. Document the sequence in a skill or steering file.

3. **Conditional hook execution** — Hooks fire on their event type unconditionally. Cannot say "only run on Fridays" or "only if Asana has overdue tasks."
   - Workaround: Put conditional logic inside the hook prompt (e.g., "Check if today is Friday. If not, skip.").

4. **Hook scheduling / cron** — userTriggered hooks require manual invocation. No time-based triggers.
   - Workaround: Manually trigger AM/EOD hooks. Could use external cron to send a signal, but Kiro has no native scheduler.

5. **Steering file inheritance** — Cannot have a base steering file that other files extend or override.
   - Workaround: Use file references (`#[[file:]]`) to compose steering from multiple sources.

6. **Dynamic inclusion mode** — Inclusion mode is static in front matter. Cannot change based on time of day, active project, or session type.
   - Workaround: Use `auto` with broad keyword descriptions to approximate dynamic loading.

7. **Skill chaining / pipelines** — Skills are invoked individually. Cannot define "skill A triggers skill B."
   - Workaround: Encode the pipeline sequence in the skill's SKILL.md instructions. The agent follows the sequence.

8. **Hook output sharing** — Each hook execution is independent. AM-2 cannot directly read AM-1's output.
   - Workaround: AM-1 writes to intake/ files. AM-2 reads intake/ files. File system is the shared state.

9. **Multi-model routing** — All hooks use the same model as the current session. Cannot assign different models per hook.
   - Workaround: Use the model that best fits the most demanding hook. For cost optimization, run lightweight hooks in separate sessions with cheaper models.

10. **Steering file versioning** — No built-in version history for steering files.
    - Workaround: Use git (agent-bridge-sync) to version steering files.

## Phase 2 Opportunity

**Custom subagents with isolated context** — Supported (Feb 2026 release). Richard's agent routing patterns (rw-trainer, karpathy, market-analyst, etc.) could each be a custom subagent with its own context window, preventing cross-contamination. This is the most impactful unused capability — deserves its own spec.
