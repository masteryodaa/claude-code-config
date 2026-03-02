---
name: debug
description: Systematic 6-step debugging workflow
---

# /debug — Systematic Debugging

## Usage
```
/debug <description of the bug>
/debug                          # Interactive — will ask what's wrong
```

## The 6 Steps

### Step 1: Reproduce
- Get the exact error message, stack trace, or unexpected behavior
- Identify the minimal reproduction steps
- Note the environment (OS, runtime version, dependencies)
- If no repro yet, help the user create one

### Step 2: Isolate
- Narrow down to the specific file(s) and function(s)
- Use git blame / git log to find when the behavior changed
- Check if it's a regression (did it ever work?)
- Use binary search through commits if regression is suspected

### Step 3: Root Cause
- Read the full context of the failing code
- Trace data flow from input to failure point
- Check for common causes:
  - Off-by-one errors
  - Null/undefined handling
  - Race conditions
  - State mutations
  - Wrong assumptions about API behavior
  - Environment differences (dev vs prod)
- Form a hypothesis and verify it

### Step 4: Fix
- Write the minimal fix that addresses the root cause
- Don't fix symptoms — fix the actual problem
- Consider edge cases the fix might introduce
- Keep the fix focused — resist the urge to refactor nearby code

### Step 5: Verify
- Run the specific test that failed (or write one if none exists)
- Run the broader test suite to check for regressions
- Manually verify the original reproduction steps
- Check that the fix handles edge cases

### Step 6: Document
- Add a comment if the fix is non-obvious
- If the bug pattern is novel, save to memory/debugging.md
- Format for memory:
  ```
  ## [Short title]
  **Symptom**: what it looked like
  **Root cause**: what actually went wrong
  **Fix**: what solved it
  **Lesson**: what to watch for next time
  ```

## Guidelines
- Prefer reading code over guessing
- Don't change multiple things at once — isolate variables
- If stuck after 3 attempts, step back and re-examine assumptions
- Ask the user for more context rather than guessing
