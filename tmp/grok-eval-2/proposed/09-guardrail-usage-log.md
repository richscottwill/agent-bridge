# Guardrail Usage Log (Lightweight)

Every time a high-stakes output is produced, the agent should append:
- Date
- Task type (projection / test readout / WBR / pacing)
- Confidence % given
- Was human review flagged? (Y/N)
- Did Richard actually review before action? (Y/N)
- Any friction or improvement noted

Example entry:
`2026-04-23 | Projection | 62% | Y | Y | Guardrail forced me to quantify the budget sensitivity — much better than before`
