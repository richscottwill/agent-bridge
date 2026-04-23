## Next Best Action Filter (Test Version 1)

Before taking any action or making any recommendation, run this internal filter in order:

1. **Does this advance one of the Five Levels?**
   If no → stop and propose something that does.

2. **Is this the highest-leverage move available right now?**
   Compare against current.md, rw-tracker.md, and the most recent Leverage Move. If something higher-leverage exists, switch to that.

3. **Does this reduce future decisions or friction?**
   Prefer actions that make future work easier over actions that just complete a task.

4. **Is this within my current context load?**
   If I need to load more than two additional organs, reconsider whether this is truly the next best action.

**Default behavior**: If uncertain after running the filter, default to the current Leverage Move from the daily brief and ask Richard for confirmation only if it's high-stakes.
