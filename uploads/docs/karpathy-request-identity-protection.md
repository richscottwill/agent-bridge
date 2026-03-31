# Karpathy Request: Identity Field Protection in Compression

Date: 2026-03-27
Requested by: Richard (via chat)
Priority: High — data loss already occurred

## What Happened

Brandon Munday's pronouns (she/her) were stored in memory.md's relationship graph. At some point, the autoresearch loop compressed them out — likely during a COMPRESS or REMOVE experiment on Memory. The eval questions didn't test for pronoun accuracy, so the compression passed evaluation despite dropping identity-critical data.

Richard caught it manually. The pronouns have been restored to memory.md.

## Root Cause

The compression logic treats short identity lines (e.g., "Pronouns: she/her") as low-signal because they don't affect whether standard eval questions pass. The dual blind eval asks things like "Who is Brandon Munday and what does she care about?" — which scores CORRECT regardless of whether the pronoun line exists in the organ.

## Requested Changes (two, both in Karpathy-governed files)

### 1. gut.md — Add identity fields as non-compressible

In the Compression Protocol section, add a rule that identity fields (pronouns, preferred names/nicknames, "goes by" entries) are protected from COMPRESS, REMOVE, and REWORD experiments. These fields are low-token-cost but high-harm-if-lost. They should be treated like accuracy-critical data in Brain/Memory (100% threshold).

Suggested location: new subsection under "Compression Techniques" or as a constraint in the protocol header.

### 2. heart.md — Add standing adversarial eval question for Memory

Add a standing eval question that must be included whenever Memory is the experiment target:

"What are Brandon Munday's pronouns?" → Must answer "she/her"

This forces any Memory experiment to fail if identity fields are dropped. As more people's identity details are added to the relationship graph, this list should grow.

## Principle Alignment

- Principle 2 (Structural over cosmetic): Protecting fields via compression rules is structural. Adding an eval question is belt-and-suspenders.
- Principle 5 (Invisible over visible): Once the rule exists, identity fields just survive compression without anyone noticing. That's the point.

## Impact if Not Fixed

The system will keep dropping identity data during compression. Richard will keep catching it manually — or worse, won't catch it, and the agent will misgender someone in a drafted communication.
