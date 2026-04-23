# Test Readout Analyzer (Grok proposal)

Script that takes raw test data → structured readout + next action + confidence.

Pairs with performance-marketing-guide.md.

Intent: agent invokes this tool on a test that just closed. Tool produces:
- Incrementality estimate
- Confidence (sign/magnitude/generalizability)
- Recommended next action
- Creative fatigue signal
