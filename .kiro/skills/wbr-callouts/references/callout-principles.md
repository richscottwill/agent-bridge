# Callout Principles

The source of truth for all callout writing rules is the callout-writer agent definition:
`shared/.kiro/agents/wbr-callouts/callout-writer.md`

All style rules, word count targets, formatting conventions, and market-specific behaviors are defined there. Do not duplicate rules here — read the writer definition directly.

Callouts are generated via the WBR callout pipeline hook at `shared/.kiro/hooks/wbr-callouts.kiro.hook`. Do not invoke the callout-writer or callout-reviewer agents directly — use the hook.
