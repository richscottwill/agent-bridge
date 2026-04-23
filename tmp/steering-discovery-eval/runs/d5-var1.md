# Discovery Log — d5-var1

**Task:** "I've got a skip-level with Kate Thursday — help me prep for it. Last time was rushed and she was in a hurry."

**Session framing:** Fresh agent. Simulated steering = soul.md (current) + Canonical Resources by Task Type rows. No steering-index.

---

## Signals matched

From the steering I had loaded:

1. **soul.md — Agent Routing Directory, row 1.** The trigger list names this almost verbatim: *"Career coaching, annual review, **1:1 prep with Brandon or skip-level with Kate**, growth planning, Friday retrospective..."* → route to `rw-trainer`.
2. **Canonical Resources table (simulated) — "Career coaching / 1:1 prep with Brandon or skip-level with Kate / annual review / growth planning"** → `rw-trainer`. Same routing, reinforced.
3. **soul.md routing rule:** *"If the request clearly falls in one agent's domain, invoke it directly — don't try to handle it yourself."*

Match is unambiguous. "Skip-level with Kate" is named by person and by meeting type in both resources.

## Signals considered and rejected

- **richard-style-mbr.md** (simulated as available) — MBR writing style. Skip-level prep is not an MBR section. Reject unless Kate specifically asks for MBR-style narrative during the prep.
- **richard-style-amazon.md** (simulated as available) — Amazon-wide communication. Skip-level is a 1:1, not a broadcast. Reject.
- **Handle it myself** — soul.md says handle it only when unsure, and the match here is clear. Reject.

## Routing decision

**Delegate to `rw-trainer`.**

Reasoning: named trigger, named meeting, named person. rw-trainer owns "Deep coaching, leverage assessment, Five Levels analysis. Reads full body system for context." Last-time-was-rushed context is exactly the kind of input that benefits from full-body-system reading — rw-trainer can pull prior skip-level notes (if any), streak state, current hard thing, Five Levels progress, and what Kate has historically cared about, and compress that into a prep that respects her time constraint.

## What rw-trainer would likely need to load (not my job to do it — noting for completeness)

- `amcc.md` — streak, hard thing, avoidance patterns
- `brain.md` — Five Levels state, strategic priorities
- `memory.md` or `main.relationship_activity` — Kate interaction history
- `main.meeting_series` + `main.meeting_highlights` — prior skip-level content if indexed
- Any Loop page for the prior skip-level (`docs.loop_pages` or SharePoint `sharepoint_read_loop`)
- `Kiro-Drive/meeting-briefs/` — if a brief was already pushed

I'm *not* loading these. That's rw-trainer's job.

## What I would NOT do as the default agent

- Draft talking points myself (violates professional-writing rule — skip-level prep involves writing that Kate sees indirectly, and more importantly it's coaching depth that rw-trainer owns).
- Open Asana / DuckDB / SharePoint to pull context before routing. Routing is the first move. Context-pulling belongs to the specialist.
- Ask Richard clarifying questions before routing. The match is clear enough; rw-trainer can ask if needed.

## Honest notes

- The "last time was rushed and she was in a hurry" detail is a real prep signal (compress ruthlessly, lead with the ask, have a single crisp update) but it's rw-trainer's job to translate that into prep structure, not mine.
- If rw-trainer weren't available, I'd fall back to loading `amcc.md` + `brain.md` + `memory.md` myself and producing a leaner prep — but I'd flag that I'm operating out of my lane.
- The routing directive in soul.md is strong and specific. Ignoring it to "just help" would be the wrong call even though the task feels simple.

## Action

Route to `rw-trainer` with the task and the "last time was rushed" context. Stop.
