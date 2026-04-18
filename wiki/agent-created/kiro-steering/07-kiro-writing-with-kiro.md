# Writing with Kiro

**Doc:** 07
**Audience:** Paid Acquisition teammates + their Kiro agents
**Status:** FINAL
**Last updated:** 2026-04-17

## Environment Awareness (for your agent)

| Capability | Remote IDE (DevSpaces) | Local IDE (laptop Kiro) | AgentSpaces (chat) |
|---|---|---|---|
| Load style guide files from `~/shared/wiki/` | ✅ Direct filesystem access | ⚠️ If OneDrive sync includes them | ⚠️ Via SharePoint MCP only |
| Draft a callout/email/doc in chat | ✅ | ✅ | ✅ |
| Save draft to a file | ✅ `~/shared/drafts/` | ✅ laptop | ⚠️ User pastes output manually |
| Post/send the final draft | ❌ Never — draft only, user sends | ❌ | ❌ |
| Run callout linter hook on save | ✅ | ⚠️ Laptop-only | ❌ No hooks |

**The draft-don't-send rule applies everywhere.** Environment doesn't change it.

---

The Paid Acq team writes constantly — weekly callouts, WBR narratives, MBR prose, test designs, stakeholder emails, vendor briefs, ad copy. Kiro can dramatically speed up drafts, but writing is where "agent voice" and "Amazon voice" diverge the hardest. This doc keeps them separate.

## The golden rule

**Your agent never sends written output to other humans. Every piece of writing is a draft the user reviews and sends manually.**

This is especially important for writing because it's where agents sound their most confident. An auto-sent callout with a wrong metric or off-register language lands badly.

## Writing types and register

Paid Acq writes across multiple registers. Match the register to the audience.

| Output | Audience | Register | Style guide |
|---|---|---|---|
| Callouts (weekly) | Brandon + team | Concise, data-first, so-what explicit | `callout-principles.md` |
| WBR narrative | Leadership + cross-team | Formal, narrative, trends > single points | `richard-style-wbr.md` |
| MBR prose | Director/VP level | Most formal, strategic arc, tied to annual goals | `richard-style-mbr.md` |
| Emails to stakeholders | External or cross-team | Professional, clear ask, signature | `richard-style-email.md` |
| Docs (strategy, POVs, frameworks) | Team + cross-team | Long-form, narrative, headers as questions/imperatives | `richard-style-docs.md` |
| Amazon-formal documents (PRFAQ, OP1) | Senior leadership | Tight, no em-dashes, Amazon norms | `richard-style-amazon.md` |
| Internal chat/Slack | Colleagues | Casual, bullet points OK, no filler | Default Richard voice |

**When starting any writing task, your agent should:**
1. Identify the output type.
2. Load the matching style guide (ask the user where they are if not in standard paths).
3. Flag if the user's request doesn't match a known output type — ask.

## Style basics (the shared rules)

These apply across every register unless a style guide explicitly overrides:

- **No em-dashes.** Use commas, periods, or parentheses instead.
- **No filler.** Skip "just wanted to reach out," "quick note," "as discussed." Get to the point.
- **No superlatives.** Avoid "amazing," "incredible," "best-ever." Show don't tell.
- **Data with so-what.** A metric without interpretation is wasted. `CPA up 12% WoW` is half a sentence; add `because Q2 budget pull-forward is frontloading low-intent traffic` and it's useful.
- **Imperatives or questions for headers** in long docs. Not bare nouns. `What's blocking AU?` beats `AU Status`.
- **Narrative over bullet-only.** Bullets for enumeration, prose for reasoning. Amazon-formal documents lean heavy prose.
- **Sign-off:** "Thank you, [Name]" (professional) or "Thanks," (casual).

## The callout pipeline (simplified)

Full version uses analyst → writer → reviewer agents. Simplified for teammates:

1. **Gather data.** Your agent pulls from DuckDB/Excel/Slack — whatever's canonical for the metric.
2. **Identify the so-what.** One sentence: what changed and why does it matter.
3. **Draft.** Follow callout-principles (max word count, data-first structure, one call-to-action at end).
4. **Self-review.** Agent checks: does it have data + so-what + next step? Is the register right? Any em-dashes?
5. **Hand to the user.** User reads, edits, sends.

**Never skip steps 2 and 4.** Data without so-what is noise. Self-review catches register slips before they land in front of Brandon.

## Templates (reference by name)

Your agent should recognize these template names and use them:

- **weekly-market-callout** — Weekly market performance summary. Structure: Headline (1 sentence), Metric summary (3 rows), What's driving (2 paragraphs), What's next (3 bullets).
- **stakeholder-update** — Cross-team update (MarTech, Legal, DS, etc.). Structure: Context, Ask, Next step, Timeline.
- **test-result-summary** — Test writeup. Structure: Hypothesis, Setup, Result, What we're doing with it.
- **ad-hoc-data-brief** — Quick data answer. Structure: Question asked, Headline answer, Method, Caveats.

If your agent doesn't have template definitions loaded, it should ask the user for the template file location (typically `~/shared/wiki/templates/` or equivalent).

## Draft workflows

### Draft an email

```
User: "Draft a reply to Dwayne's thread on Polaris template changes. Thank him for the latest iteration, confirm we'll test the JP version next, ask when the DE rollout date is firm."

Agent:
1. Loads richard-style-email.md.
2. Pulls context from the thread (Outlook MCP).
3. Drafts in Richard's voice — no em-dashes, concise, clear ask.
4. Saves draft to Outlook drafts folder (requires manual approval to save).
5. Tells user: "Draft saved to Outlook drafts. Subject: '[...]'. Review and send."
```

### Draft a callout

```
User: "Write the AU weekly callout for W16."

Agent:
1. Loads callout-principles.md and richard-style-wbr.md.
2. Pulls W16 metrics from pacing/forecast source.
3. Drafts following weekly-market-callout template.
4. Self-reviews against callout-principles.
5. Saves to ~/shared/callouts/intake/2026-W16-AU-<alias>.md (drops in team intake folder if user wants to contribute).
6. Posts draft in chat for user to review before promoting to canonical.
```

### Draft an Amazon-formal doc (PRFAQ/OP1)

```
User: "Draft the PS OP1 paid acq section — $Xm budget, focus on AU/MX scale, JP launch."

Agent:
1. Loads richard-style-amazon.md (strictest style).
2. Gathers required inputs from user (budget splits, priorities, hypothesis).
3. Drafts in Amazon 6-pager / OP1 format.
4. Flags: this is leadership-facing; draft only, heavy review needed.
5. Saves to a draft location, never submits.
```

## Anti-patterns (don't do these)

- **Don't use agent default voice for external writing.** Always load the style guide first.
- **Don't auto-populate templates with made-up data.** If your agent doesn't have the metric, it says so.
- **Don't submit drafts as final.** Even if the user approves once, re-read before send.
- **Don't bulk-draft callouts across all markets in one pass.** Each market has context; generic callouts land flat.
- **Don't let the agent "punch up" language.** Paid Acq voice is plain. Flowery = wrong.

## Failure modes

- **Draft reads generic or too confident** → you forgot to load the style guide. Restart with the style file loaded.
- **Callout has data but no so-what** → run it back through the callout pipeline step 2.
- **Em-dashes keep appearing** → add an explicit rule in your steering: "Never use em-dashes. Use commas, periods, or parentheses."
- **Register mismatch (too casual for Amazon-formal, or too stiff for Slack)** → loaded wrong style guide. Confirm the output type before drafting.

## Steering file for writers

Install this at your Kiro steering folder as `writing-starter.md` (in `.kiro/steering/` inside your workspace, or `~/.kiro/steering/` for user-level):

```markdown
---
inclusion: always
---

# Writing Rules

For any written output that goes to another human:
1. Identify the output type (callout, email, doc, WBR, MBR, chat, Amazon-formal).
2. Load the matching style guide before drafting.
3. Draft in plain, direct voice. No em-dashes. No filler. No superlatives.
4. Data always pairs with so-what.
5. Self-review before handing to user.
6. Produce a draft — user sends manually.

Never auto-send emails, post Slack messages, or publish docs on behalf of the user. The draft stops at "saved to drafts" or "here's the text, copy-paste when ready."

If the user's request doesn't match a known output type, ask — don't guess the register.
```
