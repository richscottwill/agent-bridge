---
title: "Kiro CLI preToolUse Hook Exit-Zero Bug"
slug: "kiro-cli-pretooluse-hook-bug"
doc-type: "execution"
type: "postmortem"
audience: "agent"
status: "DRAFT"
level: "L3"
category: "operations"
created: "2026-04-17"
updated: "2026-04-17"
owner: "Richard Williams"
tags: ["kiro", "cli", "hooks", "pretooluse", "automation", "bug"]
depends_on: []
summary: "Kiro CLI 1.29.0 preToolUse hooks do not auto-approve on exit 0 despite docs. Affects read-only pipeline detection."
---

# Kiro CLI preToolUse Hook Exit-Zero Bug

This document captures a Kiro CLI bug affecting preToolUse hooks that matters for anyone building Kiro-based automations. Abhinav Agrawal surfaced it on April 3 in the `ai-power-user-kiro-cli` channel. The bug blocks a specific automation pattern we care about: read-only shell pipeline auto-approval.

## The bug

Kiro CLI 1.29.0 documentation states that preToolUse hooks returning exit code zero should auto-approve the tool invocation, skipping the user permission prompt. In practice, the hook runs to completion, shows "1 of 1 hooks finished," then still shows the "Allow this action?" prompt. Exit-zero semantics are not being honored.

## Why this matters

The use case Abhinav cited is the one that matters for us: identifying read-only shell pipelines like `cat file | sort | uniq -c | head` and auto-approving them. The `allowedCommands` regex cannot express these multi-command pipeline patterns because it is a per-command matcher. A preToolUse hook is the correct mechanism — inspect the full command, confirm it contains only read operations, exit zero to approve, exit non-zero to block.

With the bug in place, preToolUse hooks are limited to the blocking case. You can still deny dangerous operations, but you cannot grant silent approval for safe ones. Every approval remains a user prompt. The automation value of the hook pattern is cut in half.

## Scope

The bug affects all Kiro CLI users on 1.29.0 who are building preToolUse hooks. No workaround has been documented publicly. The suggested alternative of using `allowedCommands` regex does not cover the pipeline case.

## Our current exposure

Richard's Kiro setup uses hooks extensively for session-log maintenance, dashboard server management, and context pre-loading. None of those hooks currently rely on exit-zero auto-approval because they run on events like `agentStop` rather than `preToolUse`. The exposure is forward-looking: if we want to build pipeline auto-approval (read-only commands pass silently, write commands prompt), this bug blocks it.

## Watch status

The issue was cross-posted from the Kiro IDE channel to the CLI channel on April 3. No resolution has been confirmed through April 17. Monitor the `ai-power-user-kiro-cli` channel and Kiro release notes for fixes.

## Workaround options

Three partial workarounds exist, none fully equivalent.

First, use `allowedCommands` regex patterns for single-command read operations (for example `^ls`, `^cat`, `^grep`). This covers common cases but fails on pipelines.

Second, accept the prompt on every operation and batch approvals by using `allowedTools` for read-heavy sessions. Reduces friction without eliminating it.

Third, split read operations into a trusted tool namespace if the Kiro version supports it. This is an infrastructure-level change and not worth it for single-user setups.

## Next Steps

1. Track the issue weekly in the `ai-power-user-kiro-cli` Slack channel.
2. If we build Kiro automations that would benefit from exit-zero auto-approval, flag and defer until the bug ships a fix.
3. Report any new manifestations or version-specific behavior to the Kiro team.

## Related

- [Kiro Hooks Cookbook](11-kiro-hooks-cookbook)
- [Kiro No External Write Rule](02-kiro-no-external-write-rule)

<!-- AGENT_CONTEXT
machine_summary: "Kiro CLI 1.29.0 preToolUse hook exit 0 does not auto-approve despite docs. Read-only pipeline auto-approval blocked. Affects multi-command pipelines not expressible as allowedCommands regex."
key_entities: ["Kiro CLI", "preToolUse hook", "Abhinav Agrawal", "allowedCommands", "read-only pipelines"]
action_verbs: ["hook", "approve", "pipeline", "regex"]
update_triggers: ["bug fix ships", "Kiro CLI version update", "workaround pattern discovered"]
-->
