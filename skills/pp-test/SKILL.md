---
name: pp-test
description: Create and run a minimal test for the current task based on acceptance criteria.
disable-model-invocation: true
---

# PP Test

Create and run a minimal test for the current task.

## Instructions

1. **Find the active task.** Read the `## Work in Progress` section in `plan/plan.md`
   to get the current task filename. Read that file from `plan/`. If WIP is empty,
   tell the user to run `/pp-task` first.

2. **Read context:**
   - `plan/task-{id}.md` -- acceptance criteria (this defines what to test)
   - The implementation source files

3. **Create ONE focused test** (or a small smoke script) that validates the core
   behavior defined in the acceptance criteria. This is NOT a comprehensive test
   suite -- just enough to verify the task works.

   Choose the test approach based on what's being tested:
   - Python module → pytest test file
   - CLI tool → shell script that runs commands and checks output
   - API → script that makes requests and validates responses
   - Data processing → script with sample input and expected output

4. **Write the test file** in the project's test directory (create if needed).
   The test should:
   - Be runnable with a single command
   - Cover the core acceptance criteria (not every edge case)
   - Have clear pass/fail output
   - Include the run command in a comment at the top

5. **Run the test.** Execute it and capture the output.

6. **Apply verification-before-completion discipline:**
   - You MUST run the test before claiming it passes
   - Report the actual output, not what you expect
   - If the test fails, report the failure with actionable details
   - Do NOT claim success without evidence

7. **Check `[x] tested`** in the task's Progress section (only if the test passes).

8. **Report results:**
   - Test file location
   - Command to run it
   - Actual output (pass or fail)
   - If failed: what went wrong, suggested fix

9. **Tell the user** to run `/pp-done` or `/pp-next` next.

## If the Test Fails

- Report the failure clearly
- Do NOT mark "tested" as complete
- Suggest specific fixes
- The user can fix the issue and re-run `/pp-test`
