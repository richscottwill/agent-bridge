---
name: coach
description: "Deep coaching sessions via RW Trainer. Career coaching, annual review prep, 1:1 prep with Brandon or Kate, growth planning, Friday retrospective, strategic artifact review, leverage assessment. Triggers on coaching, career, 1:1 prep, retrospective, growth, annual review."
---

# Coach (RW Trainer)

## Instructions

This skill invokes the rw-trainer agent for deep coaching sessions. Route to rw-trainer — don't handle coaching in the default agent.

### Session Types

- **Career coaching** — Five Levels analysis, leverage assessment, growth trajectory review
- **Annual review prep** — Compile accomplishments, map to leadership principles, draft self-review sections
- **1:1 prep with Brandon** — Review open items, prepare talking points, surface blockers
- **Skip-level prep with Kate** — Strategic framing, org-level impact stories, visibility items
- **Growth planning** — Skill gap analysis, development goals, learning plan
- **Friday retrospective** — Week review, streak check, hard thing assessment, pattern detection
- **Strategic artifact review** — Review Testing Approach, OP1, AEO POV, or other strategic documents for quality and leverage
- **Leverage assessment** — Evaluate current work portfolio against the Five Levels, identify high-leverage vs low-leverage allocation

### Context Loading

The rw-trainer reads the full body system for context:
1. body.md → system navigation
2. brain.md → strategic priorities and Five Levels
3. amcc.md → streak, hard thing, avoidance patterns
4. hands.md → current execution state
5. memory.md → relationship context for 1:1 prep

### Notes

- Quick coaching checks (streak, hard thing, avoidance detection) are handled by aMCC — route to rw-trainer only for depth.
- The trainer's voice is direct and challenging. It pushes Richard, not coddles.
