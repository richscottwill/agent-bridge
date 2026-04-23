# Pacing Alert (Grok proposal)

Daily check if you're >10% off pace with recommended action.

Rule: each morning, compute MTD spend + regs vs OP2 monthly target for each active market.
- If >10% under pace → flag with "underpacing, recommend [action]"
- If >10% over pace → flag with "overpacing, recommend pull back"
- If within 10% band → quiet

Output: single-line per market, tier as 🔴 (>20% off), 🟡 (10-20% off), 🟢 (within 10%).
