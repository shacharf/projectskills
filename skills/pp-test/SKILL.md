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
   - `plan/language.md` -- test and validation defaults for selected language
   - The implementation source files

3. **Create ONE focused test** (or a small smoke script) that validates core
   behavior from acceptance criteria. This is NOT a comprehensive suite.

   Choose test approach based on artifact and language profile:
   - Library/module -> unit/integration test file in project test framework
   - CLI -> command script validating output/exit behavior
   - API/service -> request script validating responses
   - Embedded/hardware workflow -> compile check + focused behavior smoke validation

4. **Write the test/check file** in the project's test or validation directory.
   The test/check should:
   - Be runnable with a single command
   - Cover core acceptance criteria
   - Have clear pass/fail output
   - Include run command in a top comment when relevant

5. **Run the test/check.** Execute it and capture output.

6. **Apply verification-before-completion discipline:**
   - MUST run before claiming pass
   - Report actual output, not expected output
   - If failed, report failure with actionable details
   - Do NOT claim success without evidence

7. **Check `[x] tested`** in task Progress (only if test/check passes).

8. **Report results:**
   - Test/check file location
   - Command used
   - Actual output (pass/fail)
   - If failed: what went wrong and suggested fix

9. **Tell the user** to run `/pp-done` or `/pp-next` next.

## If the Test Fails

- Report failure clearly
- Do NOT mark "tested" complete
- Suggest specific fixes
- User can fix and re-run `/pp-test`
