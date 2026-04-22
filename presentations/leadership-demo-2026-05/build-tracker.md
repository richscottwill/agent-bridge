# Build Tracker — Leadership Demo Week of 2026-05-04

Last updated: 2026-04-21 (end of day 1)

---

## Sprint Status

| # | Build | Est. | Status | Notes |
|---|-------|------|--------|-------|
| 1 | Provenance bar on dashboard cards | 2h | ✅ **DONE** | `provenance.js` + `provenance-registry.js`. Wired into Command Center. 8 section configs registered. |
| 2 | Agent Activity Feed tab | 3h | ✅ **DONE** | `agent-activity.html` + demo-seed JSON. New nav tab. Click-to-expand rows. Quality-gate badges. |
| 3 | Sankey contribution-flow chart | 2h | ✅ **DONE** | `system-flow.html`. Native canvas Sankey, 16 nodes, 25 flows. Hover tooltips. |
| 4 | Contribute affordance | 1h | ✅ **DONE** | `contribute.html`. 4-stage animated confirmation (signal accepted → classified → routed → surfaced). Demo mode — client-side simulation. |
| 5 | Demo script | 1h | ✅ **DONE** | 15-min minute-by-minute. Q&A bank (5 probes with 60s answers). Bridge-back phrases. Hard rules. |
| 6 | One-pager leave-behind | 1h | ✅ **DONE** | Diagram + by-the-numbers + before/after + "what if resourced" (3 scaling moves). Security model. "What this is not." |
| 7 | Risk log + Q&A prep | 30m | ✅ **DONE** | 3 risk categories. 24h checklist. 5 Q&A answers. Includes "prompt wrapper" rebuttal. |
| 8 | Offline screenshot fallbacks | 30m | Pending (24h before) | Can't prep early — dashboard changes until then. Capture between 5/3 and demo time. |

**Day-1 result: 7/8 builds complete (~10 hours). ~30 min remaining for screenshots 24h before.**

---

## Files Delivered

### In the dashboard (`~/shared/dashboards/`)
- `shared/provenance.js` — reusable provenance bar module (CSS injected on load)
- `shared/provenance-registry.js` — section-to-producer mapping, 8 entries
- `agent-activity.html` — new tab, feed of recent agent actions
- `data/agent-activity-feed.json` — demo-seed data (12 realistic activities)
- `system-flow.html` — new tab, Sankey diagram (16 nodes, 25 flows)
- `contribute.html` — new tab, human-to-agent signal drop with animated confirmation
- `index.html` — updated nav (4 new tabs), provenance bars auto-applied on load

### In SharePoint (`Documents/Kiro-Drive/Artifacts/leadership-demo-2026-05/`)
- `README.md` — vision, audience implications, 15-min flow, Q&A prep
- `build-tracker.md` — this file
- `demo-script.md` — minute-by-minute, rehearsal schedule, hard rules
- `risk-log.md` — technical/narrative/scheduling risks, 24h checklist
- `one-pager.md` — leave-behind for leaders

---

## Demo Surface Inventory (what the 15 min actually shows)

| Minute | Tab | Focus |
|--------|-----|-------|
| 0:00-1:00 | Command Center | Cold open, no narration |
| 1:00-4:00 | Command Center | Provenance tour (3 sections) |
| 4:00-6:00 | System Flow | Sankey, convergence story |
| 6:00-9:00 | Contribute | Live signal drop, 4-stage confirmation |
| 9:00-12:00 | Agent Activity | Feed walkthrough + quality gate example |
| 12:00-15:00 | Command Center | Close + Q&A |

---

## Rehearsal Schedule

| Date | Event |
|------|-------|
| 4/28 (Mon) | Solo rehearsal, timed, self-video |
| 4/30 (Wed) | Rehearsal with non-leader (Adi or Dwayne) |
| 5/2 (Fri) | Substance rehearsal with Brandon |
| 5/3 or 5/4 | Capture offline screenshot fallbacks |
| Week of 5/4 | Demo delivered |

---

## Open Questions (for Richard)

1. **Exact day within week of 5/4?** Narrows rehearsal schedule.
2. **In-person vs remote attendee split?** Affects which laptop/display is primary.
3. **Is Kate presenting or passively attending?** Changes opener framing (Kate-first vs room-first).
4. **Brandon has seen most of this — what should be new to him?** Pick one deep-dive segment tailored to surprise him.
5. **Should the "Contribute" form actually write to intake/ during demo, or stay as client-only simulation?** If the former, I'll wire the Python endpoint. Adds real-time magic but adds failure surface.

---

## Known Limitations (for rehearsal awareness)

- **Agent Activity Feed is demo-seeded, not live.** If a tech leader asks "where does this data come from right now?", the honest answer is: *"Today, it's a static snapshot I pre-loaded for the demo. In production, it'd be a live query against the ops schema."* Don't over-sell — they'll respect the transparency.
- **"Contribute" is client-side only.** The 4-stage confirmation is a simulation. The actual intake routing happens on DevSpaces, not in the browser. Same honesty principle.
- **Provenance registry is manually maintained.** Every new dashboard section needs a manual registry entry. Acceptable for demo scale; would need automation for org-scale productization.

---

## Next Actions

1. **Today (4/21):** End-of-day. Sprint complete. Take a break.
2. **This week (4/22-4/25):** Don't touch anything. Let it settle. Use dashboard daily, note quirks.
3. **Next Monday (4/28):** First rehearsal. Record it. Watch it back.
4. **Rest of rehearsal schedule:** See above.
