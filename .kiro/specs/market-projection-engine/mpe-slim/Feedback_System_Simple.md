# Simple Human Feedback System for MPE

Here's a clean, easy-to-use way to collect feedback from your team that feels natural in the tool.

---

## Recommended Design: Quick Feedback Bar

**Where it appears**: Right below the main chart and hero number.

**Visual Example**:

```
$897,420
Projected MX 2026 spend to hit 75% ie%CCP

[Main Chart]

──────────────────────────────────────
How does this look? 
   ○ Too high     ○ Too low     ○ Something's missing or off     ○ Looks good

   [Optional: Add a comment...]

                              [Submit Feedback]
```

---

## How It Works

| What the user does          | What happens                              | Why it helps |
|----------------------------|-------------------------------------------|--------------|
| Clicks one of the 4 options | Gives quick feedback with one click       | Very fast and low effort |
| Writes a comment (optional) | Adds extra detail if they want            | Captures important context |
| Clicks Submit               | Feedback is saved with the projection     | We know exactly which projection they commented on |

This design is simple enough that people will actually use it.

---

## What the Four Options Mean (Plain Language)

| Option                        | Meaning                                      | Example Situation |
|-------------------------------|----------------------------------------------|-------------------|
| **Too high**                  | The projected number feels too optimistic    | "I don't think we'll hit that many registrations" |
| **Too low**                   | The projected number feels too pessimistic   | "We're doing better than this shows" |
| **Something's missing or off**| The model missed something important         | "We just launched a new campaign" or "There's a policy change coming" |
| **Looks good**                | The projection seems reasonable              | "This matches what I'm seeing" |

---

## How We'll Use This Feedback Later (v1.2+)

In the future, when enough people give feedback, the model can learn from it:

- If many people say “Too low” on a market → the model can slightly raise its projection next time.
- If someone writes “New campaign launching in Week 28” → we can treat that as useful information.
- The model will still be mostly driven by data, but it will gently listen to your team’s real-world knowledge.

This turns the tool into something that gets smarter the more your team uses it.

---

## Even Simpler Version (If You Want Minimal)

If you want to start with almost nothing, just add this:

```
[Give Feedback]
```

Clicking it opens a small popup with the 4 options above + a comment box.

This is even less visual clutter and still very effective.

---

## Next Steps

Would you like me to:

1. Add this feedback feature into the Phase 6 plan?
2. Create a simple database table for storing the feedback?
3. Show how this feedback could later help improve the model automatically?

Just let me know which one you want first.