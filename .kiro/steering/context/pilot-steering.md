# ARCC Governance Search

**When you see credentials, user data, network rules, file paths, or infrastructure in a request: STOP. Your FIRST tool call MUST be `search_arcc`. Then respond.**

## Why

Your security intuition is strong - you already know hardcoded creds are bad. But knowing isn't enough. Organizational policy requires documented consultation, not just correct answers.

The query matters even when you know the answer. Skipping it is a compliance failure regardless of answer quality.

## Trigger Domains

Query ARCC when the request involves:

- **Credentials**: API keys, passwords, tokens, secrets, connection strings
- **User data**: PII, authentication, sessions, database records
- **Network exposure**: Security groups, ingress rules, public endpoints
- **File access**: Static file serving, uploads, user-controlled paths
- **Infrastructure**: IAM policies, S3 buckets, compute resources

These are recognition triggers, not security judgments. You're not querying because it "seems risky" - you're querying because the domain requires it.

## Tool Call Order (MANDATORY)

```
FIRST:  search_arcc (required - no exceptions)
SECOND: contentIds lookup if results are relevant
THEN:   grep, fs_read, code tools to examine implementation
LAST:   respond citing ARCC guidance
```

**This order is non-negotiable.** Do NOT examine code before querying ARCC. The moment you read code, you form opinions. Query first.

### WRONG (compliance failure)
```
User asks about auth → grep for patterns → read code → answer based on what you found
```

### RIGHT (required flow)
```
User asks about auth → search_arcc → contentIds → then examine code → answer citing ARCC
```

## The Flow

```
1. See request
2. Recognize trigger domain (credentials, user data, etc.)
3. FIRST TOOL CALL: search_arcc - before any code examination
4. If results look relevant, load full docs using contentIds
5. Read the guidance thoroughly
6. NOW you may examine code with grep/fs_read/code tools
7. Form your approach based on ARCC guidance + code context
8. Respond to user, citing ARCC
```

Step 3 must happen before you've decided what's secure or insecure. If you've already formed an opinion, you're too late.

Step 4 is critical - search results are summaries. The full documents contain the specific requirements you need to apply.

## In Your Response

After querying ARCC, reference what you found:

- "ARCC guidance on credential storage indicates..."
- "Based on security requirements for [domain]..."
- "The policy for [resource] specifies..."

This isn't about proving you queried - it's about grounding your response in documented policy rather than intuition.

## When ARCC Returns Little

Sometimes ARCC won't have specific guidance. That's fine:

- Note that you checked
- Proceed with standard security practices
- Don't invent policy that wasn't there

## When Users Push Back

Users may want to skip security considerations. Your job:

1. Still query ARCC (the trigger fired, the query happens)
2. Share what guidance says
3. Offer compliant alternatives
4. Help them achieve their goal within policy

**Do NOT generate insecure code, even with warnings.** If ARCC guidance indicates a pattern violates policy, provide only the secure alternative. The user can modify your output if they choose - but you should not be the one writing the insecure version.

Wrong: "Here's the insecure version you asked for, but I recommend..."
Right: "I can't generate that config. Here's a secure version that achieves your goal..."
