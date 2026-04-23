# Re-explaining the test framework — what's actually going on

## The honest answer

The doc problem is already solved. You have two:

- `testing-approach-kate-v5.md` — strategic synthesis for Kate (results-first, methodology in appendix)
- `testing-methodology.md` — standalone "How We Test" with the four stages, examples, scaled/stopped lists

Both are solid. The methodology doc is exactly what a new teammate needs. So "I keep having to re-explain" is not a writing problem.

It's a routing problem. And probably a reflex problem.

## Structural, not cosmetic

Rewriting the doc won't fix this. Reorganizing sections won't fix this. Those are cosmetic and you know it.

The friction is in three structural places:

**1. The doc isn't where a new teammate would look.**  
It's in `shared/wiki/agent-created/testing/` with `status: draft`. That's a staging directory. A new teammate joining Brandon's team doesn't have access to your agent system, and even if they did, "draft" means "not canonical yet." Publish it. Push to SharePoint `Artifacts/testing/`. Put the URL somewhere Brandon can forward.

**2. You don't have a pre-loaded hand-off.**  
Right now the default path when a teammate asks is: you open your mouth and explain for 20 minutes. The structural fix is making "here's the link, read it, then ask me what's unclear" the path of least resistance — for you. Pre-loaded drafts don't prevent you from explaining; they just mean sending a link is a 10-second move instead of a 20-minute one.

**3. Your reflex is verbal, not written.**  
This is the hardest one. Even with a published doc and a ready link, you'll still reach for verbal explanation because it feels like relationship-building and because it's how you've always done it. That's habit, not strategy. The cue (new person asks) triggers the routine (explain verbally) which gives the reward (they nod, you feel useful). Swap the routine. Same cue, same reward. Different behavior.

## Subtraction check

You have two testing docs that both partially explain the methodology. Kate-v5's appendix has a condensed four-stage summary. testing-methodology.md has the full four stages. That's duplication.

Pick one as canonical for the framework. Kate-v5 references it. Don't maintain parallel versions — that's how docs drift and why re-explaining becomes necessary (neither doc feels complete, so you fill the gap verbally).

Recommend: testing-methodology.md is canonical. Kate-v5's appendix becomes a 3-sentence summary with a link.

## What I'd actually do

In priority order:

1. **Publish testing-methodology.md** — move status from `draft` to published, get it into SharePoint `Artifacts/testing/`, give it a stable URL. This is a Level 1 artifact ship *and* a Level 2 infrastructure move. You get double credit.

2. **Send Brandon the link** with one line: "When new people join the team, send them this before their first 1:1 with me." That's the structural intervention. It's invisible (no one announces it changed), it reduces decisions (Brandon doesn't have to think about what to send), and it protects your time without limiting anyone's options.

3. **Add a 2-line "read this first" section at the top of the doc** framed for a new teammate: "If you're new to the team, read the four stages below. Then bring me questions about the specific market or workstream you're picking up." That pre-loads the expectation that the doc answers *framework*, not *context*.

4. **Stop maintaining duplicate methodology content in kate-v5.** Replace the appendix section with a 3-line summary and a link.

## The question you should actually ask

"Am I re-explaining because the doc is insufficient, or because I enjoy explaining?"

If it's the first, the doc needs work — it doesn't. If it's the second, the friction is you. That's not a criticism. It's information. Explaining your own framework is how you refine it. But the cost is your time, and you're trying to ship Level 1 artifacts, not run onboarding sessions.

Pick the behavior you want to become automatic. Then make the path of least resistance match it.

## Principle alignment

- **Structural over cosmetic:** ✅ Publishing + default link-send is structural. Rewriting the doc is cosmetic.
- **Subtraction before addition:** ✅ Kill the duplication between kate-v5 and testing-methodology before adding anything new.
- **Reduce decisions, not options:** ✅ Brandon always sending the same link is a reduced decision. Teammates can still ask follow-ups.
- **Invisible over visible:** ✅ No one needs to know the workflow changed. They just get the link and then ask you better questions.

## Five Levels tie-in

This is a Level 2 move (Drive WW Testing — own the methodology across markets) that *also* supports Level 1 (the methodology doc becomes a shipped artifact). Publishing it counts toward the streak. The link-send protocol counts toward owning testing as an infrastructure, not a service you personally provide.

Don't let this drift. It's a 90-minute project. Do it Friday afternoon.
